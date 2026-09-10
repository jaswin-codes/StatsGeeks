"""Offline, additive runtime repair only; no dataset or model execution.
Preserves v3 and records a separate v4 image/lock. Never resolves dependencies.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '1f0f403e8c7e4463cde9bfe78b12fdd809e3ae3dda6d9b2f802934fb9c7a6a8f'
WHEEL = 'narwhals-2.25.0-py3-none-any.whl'
SOURCE = Path('/mnt/c/Users/jaswi/AppData/Local/pip/Cache/http-v2/0/5/2/8/0/05280cda432a199e99befa1378983526a79ebfe8f09c7acb977a04c6.body')
DEST = Path.home() / '.local/share/gate4a/runtime_v4_narwhals'
LOCK = ROOT / 'working/gate4_runtime_narwhals_lock.json'
REPORT = ROOT / 'working/gate4_approved_runtime_validation.json'


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    assert not DEST.exists() and not LOCK.exists() and not REPORT.exists(), 'Exclusive outputs required'
    protected = json.loads((ROOT / 'working/gate4_dependency_repair_entry.json').read_text())['protected_input_hashes']
    assert all(sha(ROOT / p) == h for p, h in protected.items()), 'STOP: protected hash mismatch'
    assert sha(SOURCE) == EXPECTED, 'Wheel hash mismatch before staging'
    old_path = ROOT / 'working/gate4_runtime_lock.json'
    old = json.loads(old_path.read_text())
    assert inventory(Path(old['image_path'])) == old['files'], 'Existing image differs from lock'
    assert sha('/usr/bin/bwrap') == old['bwrap_sha256']
    for r in old['wheels'].values():
        assert sha(r['source']) == r['sha256']
    DEST.mkdir()
    image = DEST / 'image'
    shutil.copytree(old['image_path'], image)
    numeric = image / 'numeric'
    numeric.chmod(0o755)
    wheel = DEST / WHEEL
    shutil.copy2(SOURCE, wheel)
    assert sha(wheel) == EXPECTED
    with zipfile.ZipFile(wheel) as z:
        for info in z.infolist():
            p = Path(info.filename)
            assert not p.is_absolute() and '..' not in p.parts
            assert p.parts[0] in ('narwhals', 'narwhals-2.25.0.dist-info')
            assert not (numeric / p).exists(), 'Never overwrite an existing member'
        z.extractall(numeric)
        for info in z.infolist():
            if not info.is_dir():
                assert sha(numeric / info.filename) == hashlib.sha256(z.read(info)).hexdigest()
    for p in numeric.rglob('*'):
        if p.parts[len(numeric.parts)] in ('narwhals', 'narwhals-2.25.0.dist-info'):
            p.chmod(0o555 if p.is_dir() else 0o444)
    numeric.chmod(0o555)
    wheel.chmod(0o444)
    files = inventory(image)
    assert all(files[p] == h for p, h in old['files'].items())
    lock = copy.deepcopy(old)
    lock.update(version=4, image_path=str(image), files=files,
                created_utc=datetime.now(timezone.utc).isoformat(),
                parent_lock_sha256=sha(old_path), provisioner_sha256=sha(__file__),
                approval='Team Lead user task: exact Narwhals wheel approved; no other package changes',
                tree_sha256=hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest())
    lock['wheels']['narwhals'] = dict(version='2.25.0', filename=WHEEL, source=str(wheel), sha256=EXPECTED, cache_source=str(SOURCE))
    with LOCK.open('x') as f:
        json.dump(lock, f, indent=2, sort_keys=True)
        f.write('\n')
    smoke = r'''
import sys, json, importlib, importlib.util, importlib.metadata, pathlib
sys.path.insert(0, '/numeric')
result = {'python': sys.version, 'executable': sys.executable, 'sys_path': sys.path, 'modules': {}, 'imports': {}, 'tooling': {}}
for name in ['numpy', 'scipy', 'sklearn', 'joblib', 'threadpoolctl', 'narwhals']:
    try:
        m = importlib.import_module(name)
        result['modules'][name] = {'version': m.__version__, 'path': m.__file__}
        assert m.__file__.startswith('/numeric/')
    except Exception as e:
        result['modules'][name] = {'error': repr(e)}
for module, name in [('sklearn.ensemble', 'RandomForestClassifier'), ('sklearn.model_selection', 'RepeatedStratifiedKFold')]:
    try:
        getattr(importlib.import_module(module), name)
        result['imports'][name] = 'PASS'
    except Exception as e:
        result['imports'][name] = repr(e)
for name in ['jupyter', 'jupyter_core', 'nbconvert', 'nbclient']:
    result['tooling'][name] = importlib.util.find_spec(name) is not None
result['distributions'] = sorted((d.metadata['Name'], d.version) for d in importlib.metadata.distributions(path=['/numeric']))
result['mapped_files'] = sorted({line.split()[-1] for line in pathlib.Path('/proc/self/maps').read_text().splitlines() if line.split()[-1].startswith('/')})
result['project_mount_absent'] = not pathlib.Path('/mnt').exists() and not pathlib.Path('/home').exists()
print(json.dumps(result))
'''
    command = ['bwrap', '--unshare-all', '--unshare-user', '--disable-userns', '--die-with-parent', '--new-session', '--cap-drop', 'ALL', '--ro-bind', str(image), '/', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--chdir', '/tmp', '--clearenv']
    for k, v in lock['sandbox_environment'].items():
        command += ['--setenv', k, v]
    command += ['--', lock['interpreter_path'], '-I', '-B', '-c', smoke]
    runs = []
    for _ in range(2):
        p = subprocess.run(command, capture_output=True, text=True, timeout=90)
        runs.append(dict(returncode=p.returncode, stderr=p.stderr, result=json.loads(p.stdout) if p.returncode == 0 else p.stdout))
    assert inventory(image) == files
    assert inventory(Path(old['image_path'])) == old['files']
    assert all(sha(ROOT / p) == h for p, h in protected.items()), 'STOP: protected hash mismatch'
    report = dict(status='BLOCKED_PENDING_REQUIREMENT_REVIEW', created_utc=datetime.now(timezone.utc).isoformat(),
                  narwhals=dict(version='2.25.0', wheel=WHEEL, sha256=EXPECTED, staging='PASS', original_image_preserved=True),
                  runtime_lock_sha256=sha(LOCK), runs=runs, protected_files_verified=33,
                  candidate_modelling=False, notebook4_rerun=False, manifest_created=False,
                  original_git_status=subprocess.check_output(['git', 'status', '--short', '--', 'original/'], cwd=ROOT, text=True),
                  original_git_diff=subprocess.check_output(['git', 'diff', '--', 'original/'], cwd=ROOT, text=True))
    with REPORT.open('x') as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
