"""Read-only inventory of existing research files; never import model code.

Writes a new audit directory exclusively. Git internals, virtual environments,
and bytecode caches are excluded explicitly, not treated as scientific evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'reproducibility' / 'repository_polish'
EXCLUDED = {'.git', '.venv_baseline', '__pycache__', '.venv', '.venv-publication'}


def sha256(path: Path) -> str:
    """Hash bytes without loading or executing serialized objects."""
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def inventory() -> dict:
    """Record each non-environment file at its original relative path."""
    records = {}
    for directory, children, names in os.walk(ROOT):
        children[:] = sorted(n for n in children if n not in EXCLUDED)
        for name in sorted(names):
            path = Path(directory) / name
            if DEST == path or DEST in path.parents:
                continue
            records[path.relative_to(ROOT).as_posix()] = {
                'bytes': path.stat().st_size, 'sha256': sha256(path)
            }
    return records


def main() -> None:
    """Create a baseline, duplicate index, size index and Git snapshot."""
    if DEST.exists():
        raise FileExistsError(DEST)
    records = inventory()
    DEST.mkdir(parents=True, exist_ok=False)
    groups = {}
    folders = {}
    for name, item in records.items():
        groups.setdefault(item['sha256'], []).append(name)
        folder = name.split('/')[0] if '/' in name else '(root files)'
        info = folders.setdefault(folder, {'files': 0, 'bytes': 0})
        info['files'] += 1
        info['bytes'] += item['bytes']
    payloads = {
        'baseline.json': {'excluded_directory_names': sorted(EXCLUDED), 'files': records},
        'inventory_summary.json': {
            'folders': folders,
            'largest_files': sorted(records, key=lambda n: records[n]['bytes'], reverse=True)[:50],
            'duplicate_groups': [v for v in groups.values() if len(v) > 1],
            'notebooks': [n for n in records if n.endswith('.ipynb')],
            'temporary_candidates': [n for n in records if n.endswith(('.tmp', '.bak', '.onetoc2', '.pre_completion', '.pre_dependency_repair'))],
            'python_scripts': [n for n in records if n.endswith('.py')],
        },
    }
    for name, payload in payloads.items():
        with (DEST / name).open('x', encoding='utf-8') as stream:
            json.dump(payload, stream, indent=2)
    for name, args in [('git_status_before.txt', ['status', '--short']), ('git_head_before.txt', ['rev-parse', 'HEAD'])]:
        result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, check=True)
        with (DEST / name).open('x', encoding='utf-8') as stream:
            stream.write(result.stdout)
    print(json.dumps({'files': len(records), 'bytes': sum(r['bytes'] for r in records.values()), 'folders': folders}, indent=2))


if __name__ == '__main__':
    main()
