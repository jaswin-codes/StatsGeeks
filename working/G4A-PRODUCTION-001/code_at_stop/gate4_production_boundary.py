"""Linux-only Gate 4 transport infrastructure. No models, target lookup or scoring.
Only sealed code bytes and a single JSON packet cross the namespace boundary.
The caller is privileged. Full manifests and label artifacts must never be mounted.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import selectors
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / 'working/gate4_runtime_narwhals_lock.json'
LOCK_HASH = 'cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514'
FIELDS = {'X_source', 'y_source', 'X_support', 'y_support', 'support_ids', 'X_query', 'query_ids', 'parameters'}


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def runtime_check():
    assert sha(LOCK_PATH) == LOCK_HASH
    lock = json.loads(LOCK_PATH.read_text())
    image = Path(lock['image_path'])
    actual = {p.relative_to(image).as_posix(): sha(p) for p in sorted(image.rglob('*')) if p.is_file()}
    assert actual == lock['files'], 'Runtime mutation'
    for r in lock['wheels'].values():
        assert sha(r['source']) == r['sha256'], 'Wheel mutation'
    assert sha('/usr/bin/bwrap') == lock['bwrap_sha256']
    return lock


def sealed(data):
    fd = os.memfd_create('gate4-label-free-code', os.MFD_ALLOW_SEALING | os.MFD_CLOEXEC)
    with os.fdopen(os.dup(fd), 'wb') as f:
        f.write(data)
    os.lseek(fd, 0, 0)
    fcntl.fcntl(fd, fcntl.F_ADD_SEALS, fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL)
    return fd


def members(ns):
    found = []
    for p in Path('/proc').iterdir():
        if p.name.isdecimal():
            try:
                if os.readlink(p / 'ns/pid') == ns:
                    found.append(int(p.name))
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                pass
    return sorted(found)


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_AS, (6 * 1024**3, 6 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024**2, 64 * 1024**2))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))


def sanitize(raw, packet):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                raise ValueError('Duplicate output field')
            d[k] = v
        return d
    result = json.loads(raw, object_pairs_hook=pairs)
    if type(result) is not dict or set(result) != {'query_fingerprint', 'predictions'}:
        raise ValueError('Only prediction array and ordered query fingerprint allowed')
    expected = hashlib.sha256(canonical(packet['query_ids'])).hexdigest()
    if result['query_fingerprint'] != expected:
        raise ValueError('Query identity mismatch')
    pred = result['predictions']
    if type(pred) is not list or len(pred) != len(packet['query_ids']):
        raise ValueError('Prediction count mismatch')
    if any(type(v) is not int or v not in (1, 2, 3, 4) for v in pred):
        raise ValueError('Invalid class values')
    return tuple(pred)


def run(packet, code, *, timeout=90, interrupt_after=None):
    """Returns raw bounded evidence after namespace teardown; no evaluator labels."""
    if set(packet) != FIELDS:
        raise ValueError('Exactly current-episode allowed fields required')
    ns, nq = len(packet['support_ids']), len(packet['query_ids'])
    if ns not in (20, 40, 100, 200, 400, 800) or nq != 25992 - ns:
        raise ValueError('Episode budget mismatch')
    if len(packet['y_support']) != ns or len(packet['X_support']) != ns or len(packet['X_query']) != nq:
        raise ValueError('Row count mismatch')
    if len(set(map(tuple, packet['support_ids']))) != ns or len(set(map(tuple, packet['query_ids']))) != nq:
        raise ValueError('Duplicate IDs')
    if set(map(tuple, packet['support_ids'])) & set(map(tuple, packet['query_ids'])):
        raise ValueError('Support/query overlap')
    payload = canonical(packet)
    lock = runtime_check()
    fd = sealed(code)
    ir, iw = os.pipe()
    command = ['/usr/bin/bwrap', '--unshare-all', '--unshare-user', '--disable-userns', '--die-with-parent', '--new-session', '--cap-drop', 'ALL', '--ro-bind', lock['image_path'], '/', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--chdir', '/tmp', '--clearenv', '--tmpfs', '/app', '--ro-bind-data', str(fd), '/app/entry.py', '--remount-ro', '/app', '--info-fd', str(iw)]
    for k, v in lock['sandbox_environment'].items():
        command += ['--setenv', k, v]
    command += ['--', lock['interpreter_path'], '-I', '-B', '/app/entry.py']
    started = time.monotonic()
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            pass_fds=(fd, iw), close_fds=True, start_new_session=True, preexec_fn=limits)
    os.close(fd)
    os.close(iw)
    sel = selectors.DefaultSelector()
    for stream, event, name in [(proc.stdin, selectors.EVENT_WRITE, 'input'), (proc.stdout, selectors.EVENT_READ, 'output'), (proc.stderr, selectors.EVENT_READ, 'error'), (ir, selectors.EVENT_READ, 'info')]:
        fileno = stream if isinstance(stream, int) else stream.fileno()
        os.set_blocking(fileno, False)
        sel.register(stream, event, name)
    buffers = {'output': bytearray(), 'error': bytearray(), 'info': bytearray()}
    maximum = {'output': 3*nq+256, 'error': 65536, 'info': 4096}
    offset, namespace, initial_members, reason = 0, None, [], None
    child_pid = None
    try:
        while sel.get_map():
            elapsed = time.monotonic() - started
            if reason is None and (elapsed > timeout or (interrupt_after is not None and elapsed > interrupt_after and offset == len(payload) and b'GATE4_PROBE_READY\n' in buffers['error'])):
                reason = 'controlled_interrupt' if interrupt_after is not None else 'timeout'
                # This group contains only our bwrap launcher. Namespace init death
                # causes the kernel to terminate descendants, even setsid children.
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if reason and elapsed > timeout + 15:
                raise RuntimeError('Teardown deadline exceeded')
            for key, _ in sel.select(.05):
                stream, name = key.fileobj, key.data
                fileno = stream if isinstance(stream, int) else stream.fileno()
                if name == 'input':
                    try:
                        n = os.write(fileno, payload[offset:offset+65536])
                        offset += n
                    except BrokenPipeError:
                        offset = len(payload)
                    if offset == len(payload):
                        sel.unregister(stream)
                        stream.close()
                else:
                    data = os.read(fileno, 65536)
                    if not data:
                        sel.unregister(stream)
                        if isinstance(stream, int):
                            os.close(stream)
                        else:
                            stream.close()
                    else:
                        buffers[name].extend(data)
                        if len(buffers[name]) > maximum[name]:
                            reason = 'output_limit'
                            del buffers[name][maximum[name]:]
                            try:
                                os.killpg(proc.pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                        if name == 'info' and namespace is None:
                            try:
                                info = json.loads(buffers['info'])
                                child_pid = info['child-pid']
                                namespace = os.readlink(f'/proc/{child_pid}/ns/pid')
                                initial_members = members(namespace)
                            except (ValueError, FileNotFoundError):
                                pass
        returncode = proc.wait(timeout=10)
    finally:
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=10)
        for key in list(sel.get_map().values()):
            try:
                os.close(key.fd)
            except OSError:
                pass
        sel.close()
    survivors = members(namespace) if namespace else None
    evidence = dict(returncode=returncode, reason=reason, elapsed_seconds=time.monotonic()-started,
                    namespace=namespace, namespace_initial_members=initial_members, namespace_survivors=survivors,
                    child_pid=child_pid, code_sha256=hashlib.sha256(code).hexdigest(),
                    packet_sha256=hashlib.sha256(payload).hexdigest(), packet_fields=sorted(packet),
                    stdout_sha256=hashlib.sha256(buffers['output']).hexdigest(), stderr=buffers['error'].decode(errors='replace'),
                    runtime_lock_sha256=LOCK_HASH, stdout_bytes=len(buffers['output']),
                    resource_limits={'address_space_bytes':6*1024**3,'cpu_seconds':120,'output_bytes':maximum['output'],'threads':1},
                    teardown_pass=namespace is not None and survivors == [])
    return bytes(buffers['output']), evidence
