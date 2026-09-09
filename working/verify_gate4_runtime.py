"""Independent runtime-only verification: no dataset access or model execution."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SMOKE = r'''
import sys, json, pathlib
sys.path.insert(0, '/numeric')
import numpy as np
import scipy, scipy.linalg, scipy.special
import sklearn, joblib, threadpoolctl
assert np.__version__ == '2.4.6' and scipy.__version__ == '1.17.1'
assert sklearn.__version__ == '1.9.0' and joblib.__version__ == '1.5.3'
assert threadpoolctl.__version__ == '3.6.0'
a = np.array([[2., 0.], [0., 3.]])
assert np.allclose(np.linalg.eigvalsh(a), [2., 3.])
assert np.allclose(scipy.linalg.solve(a, np.array([4., 9.])), [2., 3.])
assert scipy.special.expit(0.) == .5
modules = {m.__name__: m.__file__ for m in [np, scipy, sklearn, joblib, threadpoolctl]}
assert all(p.startswith('/numeric/') for p in modules.values())
assert sys.executable == '/usr/bin/python3.14'
assert not pathlib.Path('/home').exists() and not pathlib.Path('/mnt').exists()
paths = sorted({line.split()[-1] for line in pathlib.Path('/proc/self/maps').read_text().splitlines() if line.split()[-1].startswith('/')})
print(json.dumps({'modules': modules, 'executable': sys.executable, 'sys_path': sys.path,
                  'mapped_files': paths, 'numerical_operations': 'PASS', 'models_run': False}))
'''


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def inventory(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}


def verify():
    lock = json.loads((ROOT / 'working/gate4_runtime_lock.json').read_text())
    image = Path(lock['image_path'])
    assert inventory(image) == lock['files'], 'Image changed'
    assert sha('/usr/bin/bwrap') == lock['bwrap_sha256']
    # Rebuild the complete file tree independently from wheel bytes + pinned OS files.
    with tempfile.TemporaryDirectory(prefix='gate4_runtime_rebuild_') as temp:
        rebuilt = Path(temp)
        for record in lock['wheels'].values():
            wheel = Path(record['source'])
            assert sha(wheel) == record['sha256']
            with zipfile.ZipFile(wheel) as z:
                z.extractall(rebuilt / 'numeric')
        shutil.copytree('/usr/lib/python3.14', rebuilt / 'usr/lib/python3.14',
                        ignore=shutil.ignore_patterns('__pycache__', 'site-packages', 'dist-packages'))
        (rebuilt / 'usr/bin').mkdir(parents=True)
        shutil.copy2(lock['interpreter_source'], rebuilt / 'usr/bin/python3.14')
        for relative, record in lock['declared_native_sources'].items():
            assert sha(record['source']) == record['sha256']
            target = rebuilt / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(record['source'], target)
        assert inventory(rebuilt) == lock['files'], 'Independent rebuild differs'
    command = ['bwrap', '--unshare-all', '--unshare-user', '--disable-userns',
               '--die-with-parent', '--new-session', '--cap-drop', 'ALL',
               '--ro-bind', str(image), '/', '--proc', '/proc', '--dev', '/dev',
               '--tmpfs', '/tmp', '--chdir', '/tmp', '--clearenv']
    for k, v in lock['sandbox_environment'].items():
        command += ['--setenv', k, v]
    command += ['--', lock['interpreter_path'], '-I', '-B', '-c', SMOKE]
    run = subprocess.run(command, capture_output=True, text=True, timeout=45)
    if run.returncode:
        raise RuntimeError('Isolated numerical runtime failed: ' + run.stderr)
    smoke = json.loads(run.stdout)
    assert all(p.lstrip('/') in lock['files'] for p in smoke['mapped_files']), 'Undeclared native mapping'
    assert inventory(image) == lock['files']
    return {'status': 'PASS', 'independent_full_tree_rebuild': True,
            'tree_sha256': lock['tree_sha256'], 'runtime_lock_sha256': sha(ROOT / 'working/gate4_runtime_lock.json'),
            'host_runtime_mounts': [], 'undeclared_native_mappings': [],
            'smoke': smoke, 'environment': lock['sandbox_environment']}


if __name__ == '__main__':
    try:
        print(json.dumps(verify(), sort_keys=True))
    except Exception as error:
        print(json.dumps({'status': 'BLOCKED', 'error': repr(error)}))
        sys.exit(1)
