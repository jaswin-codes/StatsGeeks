"""Gate 4A DIAGNOSTIC-ONLY Bubblewrap prototype; NOT approved for real episodes.

No model implementation, fitting, inference, or scoring here. Full manifests and
labels stay on the host. Only a single packet is serialized, never Python objects.
Caller must pin code/source state before target exposure; do not feed outputs or
scores into later inputs. This minimal boundary permits no source-state files.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WORKER = Path(__file__).with_name('gate4_isolated_worker.py')
FIELDS = {'support_ids', 'X_support', 'y_support', 'query_ids', 'X_query'}
SYNTHETIC_PACKET = {
    'support_ids': [[-1, -1]], 'X_support': [[0.0]], 'y_support': [1],
    'query_ids': [[-2, -i] for i in range(1, 13)], 'X_query': [[0.0]] * 12,
}


def run_episode(*args, **kwargs):
    """Fail closed: numerical runtime/deployment verification is incomplete."""
    raise RuntimeError('GATE 4A BLOCKED: incomplete sandbox runtime; no episode execution')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linux_path(path: Path) -> str:
    return subprocess.check_output(
        ['wsl', '-d', 'Ubuntu', '--exec', 'wslpath', '-a', path.resolve().as_posix()],
        text=True, timeout=15).strip()


def run_isolation_probe(packet: dict, code: Path, expected_code_hash: str,
                expected_worker_hash: str, *, timeout: int = 30) -> tuple[int, ...]:
    """One fresh sandbox, no label RPC, no persistent writes, sealed plain output.

    Trusted evaluator supplies ONLY current permitted fields. Returned tuple is
    materialized after ALL sandbox processes exit. No pickle/object deserialization.
    Candidate function is entry(packet); source dependencies require new review.
    """
    if packet != SYNTHETIC_PACKET:
        raise ValueError('Diagnostic-only boundary: real episode data forbidden')
    if set(packet) != FIELDS:
        raise ValueError('Exactly one episode packet required; no extra fields')
    ns, nq = len(packet['support_ids']), len(packet['query_ids'])
    if not ns or not nq or len(packet['X_support']) != ns or len(packet['y_support']) != ns or len(packet['X_query']) != nq:
        raise ValueError('Row counts mismatch')
    if any(type(y) is not int or y not in (1, 2, 3, 4) for y in packet['y_support']):
        raise ValueError('Invalid support labels')
    # Pin trusted launcher and pre-approved candidate bytes. Copying a manifest,
    # labelled artifact, source cache, or mutable adaptation file as code is forbidden.
    if digest(code) != expected_code_hash or digest(WORKER) != expected_worker_hash:
        raise ValueError('Code changed after approval')
    command = [
        'wsl', '-d', 'Ubuntu', '--exec', 'bwrap', '--unshare-all', '--unshare-user',
        '--die-with-parent', '--new-session', '--disable-userns',
        '--cap-drop', 'ALL', '--clearenv',
        '--ro-bind', '/usr', '/usr', '--symlink', 'usr/lib', '/lib',
        '--symlink', 'usr/lib64', '/lib64', '--proc', '/proc', '--dev', '/dev',
        '--tmpfs', '/tmp', '--dir', '/app',
        '--ro-bind', linux_path(WORKER), '/app/worker.py',
        '--ro-bind', linux_path(code), '/app/entry.py',
        '--chdir', '/tmp', '--setenv', 'PATH', '/usr/bin',
        '--setenv', 'HOME', '/tmp', '--setenv', 'PYTHONDONTWRITEBYTECODE', '1',
        '--', '/usr/bin/python3', '-I', '-B', '/app/worker.py',
    ]
    payload = json.dumps(packet, allow_nan=False, separators=(',', ':')).encode()
    completed = subprocess.run(command, input=payload, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, timeout=timeout, check=False)
    if completed.returncode:
        # Never route worker stderr or output into another worker's inputs.
        raise RuntimeError('Sandbox execution failed; no scoring permitted')
    raw = completed.stdout  # Immutable bytes, acquired only after sandbox exit.
    if len(raw) > 3 * nq + 2:
        raise ValueError('Oversized/non-prediction output')
    result = json.loads(raw)
    if type(result) is not list or len(result) != nq:
        raise ValueError('Predictions only; exact query count required')
    if any(type(v) is not int or v not in (1, 2, 3, 4) for v in result):
        raise ValueError('Integer class predictions only')
    return tuple(result)
