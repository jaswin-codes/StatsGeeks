"""Synthetic negative-access tests only. Never imports or executes a model.

Exclusive diagnostic output; cannot emit a passing manifest. Incomplete numerical
runtime and deployment verification stop the repair; the contract is not weakened.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid

from gate4_isolation import ROOT, WORKER, SYNTHETIC_PACKET, digest, run_isolation_probe, run_episode

# This code tests access, not a predictive rule. Integers are test status codes.
PROBE = r'''
import ctypes
import gc
import pathlib
import sys

def entry(packet):
    names = {'y_amsterdam', 'full_target_labels', 'other_episode_support_labels',
             'evaluator', 'prior_episode_support_labels', 'adaptation_state'}
    namespace_clean = not names.intersection(globals())
    modules_clean = all(not names.intersection(vars(m)) for m in list(sys.modules.values()) if m is not None)
    # CPython's intern table contains name -> identical string entries, not labels.
    hidden_clean = not any(isinstance(o, dict) and any(k in o and not (type(o[k]) is str and o[k] == k) for k in names) for o in gc.get_objects())
    paths = TARGET_PATHS
    file_denied = []
    for path in paths:
        try:
            # Permission probe ONLY: no label file bytes are read or deserialized.
            with open(path, 'rb'):
                pass
            file_denied.append(False)
        except (PermissionError, FileNotFoundError, NotADirectoryError):
            file_denied.append(True)
    marker = pathlib.Path('/tmp/prior_support_synthetic')
    tmp_clean = not marker.exists()
    marker.write_text('SYNTHETIC_ONLY_NOT_A_TARGET_LABEL')
    try:
        pathlib.Path('/usr/gate4_synthetic_write_probe').write_text('SYNTHETIC')
        readonly = False
    except OSError:
        readonly = True
    # x86_64 Linux key syscalls; sentinel only, never any target data.
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    description = KEY_DESCRIPTION
    keyring = libc.syscall(250, 0, -4, 1)  # KEYCTL_GET_KEYRING_ID, USER_KEYRING
    found = libc.syscall(250, 10, keyring, ctypes.c_char_p(b'user'), ctypes.c_char_p(description), 0)
    recovered = False
    if found >= 0:
        buffer = ctypes.create_string_buffer(128)
        size = libc.syscall(250, 11, found, buffer, 128)  # KEYCTL_READ
        recovered = size == len(b'SYNTHETIC_PRIOR_EPISODE_STATE') and buffer.raw[:size] == b'SYNTHETIC_PRIOR_EPISODE_STATE'
        if libc.syscall(250, 9, found, keyring) != 0:  # unlink our own temporary test key
            raise RuntimeError('Synthetic key cleanup failed')
        key_status = 2 if recovered else 3
    elif keyring >= 0:
        value = b'SYNTHETIC_PRIOR_EPISODE_STATE'
        added = libc.syscall(248, ctypes.c_char_p(b'user'), ctypes.c_char_p(description), ctypes.c_char_p(value), len(value), keyring)
        if added >= 0 and libc.syscall(250, 15, added, 60) != 0:
            libc.syscall(250, 9, added, keyring)
            raise RuntimeError('Could not bound synthetic key lifetime')
        key_status = 1 if added >= 0 else 4
    else:
        key_status = 4
    ok = lambda x: 1 if x else 2
    return [ok(namespace_clean), ok(modules_clean), ok(hidden_clean),
            *[ok(v) for v in file_denied], ok(tmp_clean), ok(readonly), key_status]
'''


def child() -> None:
    host = ROOT.as_posix()
    linux_root = '/mnt/' + host[0].lower() + host[2:]
    paths = [linux_root + '/' + p for p in [
        'data/preprocessed/preprocessed_data.pkl',
        'working/baseline_artifacts/amsterdam_zero_shot.npz',
        'working/gate4_episode_manifest_validation.json',
        'working/gate4_episode_manifest.json',
    ]]
    paths += ['/proc/1/root' + paths[0], '/home/jaswin']
    probe = PROBE.replace('TARGET_PATHS', repr(paths)).replace(
        'KEY_DESCRIPTION', repr(('gate4-synthetic-' + uuid.uuid4().hex).encode()))
    # Parent-only synthetic evaluator state; never serialized into sandbox input.
    evaluator = {'full_target_labels': 'EVALUATOR_ONLY_SYNTHETIC'}
    with tempfile.TemporaryDirectory(prefix='gate4_isolation_') as temp:
        code = Path(temp) / 'negative_access_probe.py'
        code.write_text(probe, encoding='utf-8')
        h, w = digest(code), digest(WORKER)
        first = run_isolation_probe(SYNTHETIC_PACKET, code, h, w)
        second = run_isolation_probe(SYNTHETIC_PACKET, code, h, w)
        rejected = {}
        for name, expression in [
            ('hidden_labels_object', "{'predictions':[1]*12,'hidden_labels':[4]}"),
            ('label_request', "{'request':'y_amsterdam'}"),
            ('extra_prediction', '[1]*13'), ('non_integer', '[True]*12'),
        ]:
            code.write_text('def entry(packet):\n    return ' + expression + '\n', encoding='utf-8')
            try:
                run_isolation_probe(SYNTHETIC_PACKET, code, digest(code), w)
                rejected[name] = False
            except ValueError:
                rejected[name] = True
        code.write_text('import numpy\ndef entry(packet):\n    return [1]*12\n', encoding='utf-8')
        try:
            run_isolation_probe(SYNTHETIC_PACKET, code, digest(code), w)
            numerical_runtime_ready = True
        except RuntimeError:
            numerical_runtime_ready = False
    try:
        run_episode(None)
        disabled = False
    except RuntimeError:
        disabled = True
    assert evaluator['full_target_labels'] == 'EVALUATOR_ONLY_SYNTHETIC'
    print(json.dumps({
        'first_sandbox_status_codes': first, 'second_sandbox_status_codes': second,
        'namespace_module_gc_named_reference_checks_pass': first[:3] == second[:3] == (1,1,1),
        'label_files_other_manifest_and_parent_root_inaccessible': first[3:9] == second[3:9] == (1,)*6,
        'fresh_tmp_and_readonly_runtime_pass': first[9:11] == second[9:11] == (1,1),
        'cross_process_user_keyring_synthetic_state_recovered': first[11] == 1 and second[11] == 2,
        'synthetic_key_cleanup': 'recovered key unlinked; newly added keys expire after 60 seconds in disposable user namespace',
        'numerical_runtime_ready': numerical_runtime_ready,
        'strict_output_rejections': rejected,
        'production_entrypoint_disabled': disabled,
        'real_target_labels_supplied_to_probe': False,
        'models_executed': False,
    }))


def sha_stream(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--child', action='store_true')
    args = parser.parse_args()
    if args.child:
        child()
        return
    output = ROOT / 'working/gate4_isolation_repair_validation.json'
    sampler = ROOT / 'working/gate4_isolation_sampler_reverification.json'
    if output.exists() or sampler.exists():
        raise FileExistsError('Preserve prior evidence; output already exists')
    prior_path = ROOT / 'working/gate4_episode_manifest_validation.json'
    prior = json.loads(prior_path.read_text())
    protected = prior['protected_input_hashes']
    before = {p: sha_stream(ROOT / p) for p in protected}
    assert before == protected, 'Protected files differ from accepted Gate 4A snapshot'
    runs = [json.loads(subprocess.check_output(
        [sys.executable, '-B', str(Path(__file__).resolve()), '--child'],
        cwd=ROOT, text=True, timeout=180)) for _ in range(2)]
    assert all(not r['numerical_runtime_ready'] for r in runs), 'Reassess deployment if runtime changed'
    assert all(not r['cross_process_user_keyring_synthetic_state_recovered'] for r in runs)
    assert all(r['namespace_module_gc_named_reference_checks_pass'] for r in runs)
    # Existing sampler executes as an independent fresh process, unchanged.
    subprocess.run([sys.executable, '-B', str(ROOT / 'working/verify_gate4a_episodes.py'),
                    '--output', str(sampler)], cwd=ROOT, check=True, stdout=subprocess.PIPE, timeout=180)
    replay = json.loads(sampler.read_text())
    fields = ['episodes_diagnostic_fingerprints', 'budgets', 'trials', 'seed', 'rng',
              'rng_policy', 'sampler_source_cell_sha256', 'ordered_schema_sha256']
    identity = {field: prior[field] == replay[field] for field in fields}
    assert all(identity.values())
    after = {p: sha_stream(ROOT / p) for p in protected}
    assert before == after
    assert not (ROOT / 'working/gate4_episode_manifest.json').exists()
    result = {
        'status': 'BLOCKED', 'artifact_type': 'isolation_failure_diagnostic_not_manifest',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'git_head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'working_tree_state': subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
        'mechanism': 'WSL2 Ubuntu Bubblewrap unshare-all + explicit user namespace, readonly /usr, tmpfs /tmp, no project mounts, cleared environment, stdin packet, post-exit integer-only output',
        'blocker': 'The minimal sandbox cannot import NumPy, so the agreed numerical comparator/E1 runtime is not available. Production routing remains disabled: no approved numerical/source-state mount exists, and timeout descendant teardown/resource containment are not verified. Passing synthetic namespace checks is not a deployment/isolation PASS.',
        'fresh_process_runs': runs, 'identity_reverification': identity,
        'total_episodes': 60, 'sampler_changed': False,
        'sampler_diagnostic_sha256': sha_stream(sampler),
        'prior_validation_sha256': sha_stream(prior_path),
        'mechanism_code_sha256': {p.name: sha_stream(p) for p in [Path(__file__), WORKER, WORKER.with_name('gate4_isolation.py')]},
        'protected_input_hashes': before, 'protected_files_changed': [],
        'original_git_status': subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT,text=True),
        'matched_comparators': 'Identity/packet routing feasible for raw prototypes, saved frozen RF predictions, future E1. Existing sampler routing checks replay PASS; no model adapters executed. Sandbox Python lacks NumPy; future numerical runtime also requires provisioning and revalidation.',
        'prediction_finalisation': 'Synthetic outputs collected after subprocess termination, parsed as JSON and frozen as tuple. Hidden object/label request/length/type rejection tested. No actual predictions or scores calculated. Not a production isolation pass.',
        'namespace_test_limits': 'Named globals, loaded module dictionaries, GC-tracked dictionaries excluding name-to-identical-string intern entries, file-open permission probes. No label references found. User-keyring access is possible but cross-process recovery did NOT occur with explicit fresh user namespaces; not a demonstrated bypass. Arbitrary object graphs/kernel channels/timeout cleanup are not exhaustively certified.',
        'manifest_created': False, 'candidate_modelling': False, 'notebook4_rerun': False,
        'stopped_on_failure': True,
    }
    with output.open('x', encoding='utf-8') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    print('STATUS BLOCKED')
    print('VALIDATION_SHA256', sha_stream(output))
    print('SAMPLER_SHA256', sha_stream(sampler))


if __name__ == '__main__':
    main()
