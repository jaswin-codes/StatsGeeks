"""Bounded Linux episode-owned process observation/reaping, standard library only.
PID + /proc start ticks are identities. Zombies are retained, never filtered out.
No process is signalled by this module; waitpid targets only tracked adopted children.
"""
import ctypes
import os
from pathlib import Path
import time


def state(pid):
    root = Path('/proc') / str(pid)
    try:
        raw = (root / 'stat').read_text()
        close = raw.rfind(')')
        fields = raw[close+2:].split()
        result = dict(pid=pid, command=raw[raw.find('(')+1:close], state=fields[0],
                      ppid=int(fields[1]), process_group=int(fields[2]), session=int(fields[3]),
                      start_ticks=int(fields[19]), exit_signal=int(fields[35]),
                      exit_code=int(fields[49]) if len(fields) > 49 else None)
        try:
            result['pid_namespace'] = os.readlink(root / 'ns/pid')
        except FileNotFoundError:
            result['pid_namespace'] = None  # Zombies often lose namespace links.
        text = (root / 'status').read_text()
        result['namespace_pids'] = next((l.split()[1:] for l in text.splitlines() if l.startswith('NSpid:')), [])
        result['cmdline'] = (root / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace')
        # Verify start identity again to reject PID reuse during the observation.
        raw2 = (root / 'stat').read_text()
        if int(raw2[raw2.rfind(')')+2:].split()[19]) != result['start_ticks']:
            return None
        return result
    except (FileNotFoundError, ProcessLookupError):
        return None


def all_states():
    result = {}
    for p in Path('/proc').iterdir():
        if p.name.isdecimal():
            try:
                s = state(int(p.name))
            except PermissionError:
                continue  # unrelated processes; known identities checked separately
            if s is not None:
                result[s['pid']] = s
    return result


class Lifecycle:
    def __init__(self, reap=False):
        self.started = time.monotonic()
        self.owner = os.getpid()
        self.reap_enabled = reap
        self.known = {}
        self.last = {}
        self.events = []
        self.reaped = []
        self.namespace = None
        self.samples = 0
        self.prior_subreaper = 0
        if reap:
            # Require an exclusive supervisor with no unrelated children.
            children = Path(f'/proc/self/task/{self.owner}/children').read_text().strip()
            if children:
                raise RuntimeError('Subreaper requires a dedicated child-free supervisor')
            libc = ctypes.CDLL(None, use_errno=True)
            previous = ctypes.c_int()
            if libc.prctl(37, ctypes.byref(previous), 0, 0, 0) != 0:
                raise OSError(ctypes.get_errno(), 'PR_GET_CHILD_SUBREAPER')
            self.prior_subreaper = previous.value
            if libc.prctl(36, 1, 0, 0, 0) != 0:
                raise OSError(ctypes.get_errno(), 'PR_SET_CHILD_SUBREAPER')

    def event(self, kind, **data):
        self.events.append(dict(monotonic_seconds=time.monotonic()-self.started,
                                wall_time_ns=time.time_ns(), kind=kind, **data))

    def attach(self, pid):
        s = state(pid)
        if s is None:
            raise RuntimeError('Launcher vanished before identity capture')
        self.launcher = pid
        self.known[pid] = s['start_ticks']
        self.observe('launch')

    def observe(self, stage):
        self.samples += 1
        states = all_states()
        # Retain ancestry through reparenting and namespace-link loss in zombies.
        changed = True
        while changed:
            changed = False
            for pid, s in states.items():
                parent_known = s['ppid'] in self.known and (s['ppid'] not in states or states[s['ppid']]['start_ticks'] == self.known[s['ppid']])
                in_namespace = self.namespace is not None and s['pid_namespace'] == self.namespace
                if pid not in self.known and (parent_known or in_namespace):
                    self.known[pid] = s['start_ticks']
                    changed = True
        present = []
        for pid, start in list(self.known.items()):
            # Direct read of known IDs must not silently ignore permission failures.
            s = state(pid)
            if s is not None and s['start_ticks'] != start:
                self.event('pid_reused', stage=stage, pid=pid, original_start=start, observed=s)
                s = None
            if s is not None:
                present.append(s)
            if self.last.get(pid, 'UNSEEN') != s:
                self.event('observation', stage=stage, pid=pid, start_ticks=start, process=s)
                self.last[pid] = s
        return present

    def finish(self, launcher_returncode, deadline_seconds=5):
        self.event('launcher_wait_completed', returncode=launcher_returncode)
        deadline = time.monotonic() + deadline_seconds
        immediate = self.observe('immediate_post_wait')
        present = immediate
        while True:
            if self.reap_enabled:
                for s in present:
                    if s['pid'] == self.launcher or s['ppid'] != self.owner:
                        continue
                    # No signalling. waitpid confirms actual parent ownership and exit.
                    current = state(s['pid'])
                    if current is None or current['start_ticks'] != s['start_ticks']:
                        continue
                    try:
                        pid, status = os.waitpid(s['pid'], os.WNOHANG)
                    except ChildProcessError:
                        self.event('not_waitable', pid=s['pid'], start_ticks=s['start_ticks'])
                        continue
                    if pid:
                        item = dict(pid=pid, start_ticks=s['start_ticks'], wait_status=status,
                                    exit_code=os.waitstatus_to_exitcode(status))
                        self.reaped.append(item)
                        self.event('waitpid_reaped', **item)
            present = self.observe('bounded_settle')
            if not present or time.monotonic() >= deadline:
                break
            # Poll condition until a fixed deadline, NOT sleep then assume success.
            time.sleep(.01)
        passed = not present
        self.event('teardown_complete' if passed else 'teardown_deadline_failed', survivors=present)
        if passed and self.reap_enabled:
            remaining_children = Path(f'/proc/self/task/{self.owner}/children').read_text().strip()
            if remaining_children:
                passed = False
                self.event('unexpected_unreaped_child', children=remaining_children)
            else:
                libc = ctypes.CDLL(None, use_errno=True)
                if libc.prctl(36, self.prior_subreaper, 0, 0, 0) != 0:
                    raise OSError(ctypes.get_errno(), 'Restore subreaper setting')
        return dict(pass_=passed, subreaper_enabled=self.reap_enabled, samples=self.samples,
                    owner_pid=self.owner, known_identities=self.known, immediate_post_wait=immediate,
                    final_survivors=present, reaped=self.reaped, deadline_seconds=deadline_seconds,
                    events=self.events, historical_432_434_state='Not recorded; cannot retrospectively determine')
