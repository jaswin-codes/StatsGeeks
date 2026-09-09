"""Provision a private, hash-pinned Linux runtime; no project data or model access.

Run once in WSL Ubuntu. Reuses ONLY the already-downloaded hash-pinned wheels;
copies Python, stdlib and declared OS shared-library dependencies into a fresh
label-free image outside Git. Preserves failed v2 staging; no network or installs.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

PINS = {'numpy': '2.4.6', 'scipy': '1.17.1', 'scikit-learn': '1.9.0',
        'joblib': '1.5.3', 'threadpoolctl': '3.6.0'}
ROOT = Path(__file__).resolve().parents[1]
CACHE = Path.home() / '.local/share/gate4a/runtime_v2/wheels'
DEST = Path.home() / '.local/share/gate4a/runtime_v3'
LOCK = ROOT / 'working/gate4_runtime_lock.json'
WHEELS = {
    'numpy': ('numpy-2.4.6-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl', 'a2c306dea656c12c68f51f4cea133cbe78ca7435eb28c735eac1d3ebe73be6e8'),
    'scipy': ('scipy-1.17.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl', 'eee2cfda04c00a857206a4330f0c5e3e56535494e30ca445eb19ec624ae75118'),
    'scikit-learn': ('scikit_learn-1.9.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl', '1fea2cc5677ab49d6f5bade978c866da44957b712d92e9635e8b4f723013c3cb'),
    'joblib': ('joblib-1.5.3-py3-none-any.whl', '5fc3c5039fc5ca8c0276333a188bbd59d6b7ab37fe6632daa76bc7f9ec18e713'),
    'threadpoolctl': ('threadpoolctl-3.6.0-py3-none-any.whl', '43a0b8fd5a2928500110039e43a5eed8480b918967083ea48dc3ab9f13c4a7fb'),
}


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    if DEST.exists() or LOCK.exists():
        raise FileExistsError('Exclusive runtime provisioning; preserve existing evidence')
    if sys.version_info[:2] != (3, 14) or os.uname().machine != 'x86_64':
        raise RuntimeError('This pinned image requires observed CPython 3.14 x86_64')
    DEST.mkdir(parents=True)
    image = DEST / 'image'
    wheels = DEST / 'wheels'
    wheels.mkdir()
    records = {}
    for name, version in PINS.items():
        filename, expected = WHEELS[name]
        cached = CACHE / filename
        if sha(cached) != expected:
            raise RuntimeError('Cached wheel integrity mismatch')
        path = wheels / filename
        shutil.copy2(cached, path)
        if sha(path) != expected:
            raise RuntimeError('Staged wheel integrity mismatch')
        with zipfile.ZipFile(path) as z:
            for member in z.infolist():
                p = Path(member.filename)
                if p.is_absolute() or '..' in p.parts:
                    raise RuntimeError('Unsafe wheel member')
            z.extractall(image / 'numeric')
        records[name] = {'version': version, 'filename': path.name,
                         'source': str(cached), 'sha256': sha(path)}
    python = Path(sys.executable).resolve()
    target = image / 'usr/bin/python3.14'
    target.parent.mkdir(parents=True)
    shutil.copy2(python, target)
    stdlib = Path('/usr/lib/python3.14')
    shutil.copytree(stdlib, image / 'usr/lib/python3.14',
                    ignore=shutil.ignore_patterns('__pycache__', 'site-packages', 'dist-packages'))
    # ldd on a bundled leaf DSO does not inherit the importing extension's RPATH.
    # Declare wheel-local search paths explicitly, including the libquadmath sibling.
    wheel_dirs = sorted(p for p in (image / 'numeric').glob('*.libs') if p.is_dir())
    loader_dirs = wheel_dirs + [image / 'lib/x86_64-linux-gnu', image / 'usr/lib/x86_64-linux-gnu']
    loader_env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C',
                  'LD_LIBRARY_PATH': ':'.join(map(str, loader_dirs))}
    elf = [target] + [p for p in image.rglob('*') if p.is_file() and '.so' in p.name]
    done = set()
    decisions = []
    native_sources = {}
    while elf:
        path = elf.pop()
        if str(path) in done:
            continue
        done.add(str(path))
        with path.open('rb') as f:
            if f.read(4) != b'\x7fELF':
                continue
        out = subprocess.run(['/usr/bin/ldd', str(path)], capture_output=True, text=True,
                             env=loader_env, check=True)
        decisions.append({'elf': str(path.relative_to(image)), 'ldd': out.stdout})
        for line in out.stdout.splitlines():
            if '=> not found' in line:
                raise RuntimeError('Unresolved runtime dependency: ' + line)
            words = line.split()
            dependencies = [w for w in words if w.startswith('/')]
            for dep in dependencies:
                src = Path(dep).resolve()
                # Already-staged paths are reused, NEVER prefixed by image again.
                if src.is_relative_to(image):
                    elf.append(src)
                    continue
                if not str(src).startswith(('/usr/lib/', '/lib/', '/lib64/')):
                    raise RuntimeError('Undeclared native-library source: ' + str(src))
                dst = image / dep.lstrip('/')
                native_sources[str(dst.relative_to(image))] = {'source': str(src), 'sha256': sha(src)}
                if not dst.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst, follow_symlinks=True)
                    elf.append(dst)
    for directory in ['app', 'proc', 'dev', 'tmp']:
        (image / directory).mkdir(exist_ok=True)
    # Keep execute permission for the ELF interpreter as well as Python itself.
    inventory = {str(p.relative_to(image)): sha(p) for p in sorted(image.rglob('*')) if p.is_file()}
    for p in image.rglob('*'):
        p.chmod(0o555 if p.is_dir() or p.stat().st_mode & 0o111 else 0o444)
    image.chmod(0o555)
    lock = {'version': 3,
            'interpreter_path': '/usr/bin/python3.14',
            'interpreter_source': str(python),
            'interpreter_sha256': sha(target),
            'dependency_resolution': decisions, 'declared_native_sources': native_sources,
            'provisioning_loader_environment': loader_env,
            'sandbox_environment': {'LD_LIBRARY_PATH': ':'.join('/' + str(p.relative_to(image)) for p in wheel_dirs),
                                    'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1',
                                    'HOME': '/tmp', 'PATH': '/usr/bin'},
            'sandbox_sys_path_addition': '/numeric',
            'network_used': False, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'image_path': str(image), 'python': sys.version, 'kernel': os.uname().release,
            'wheels': records, 'files': inventory,
            'tree_sha256': hashlib.sha256(json.dumps(inventory, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'bwrap_sha256': sha(Path('/usr/bin/bwrap')),
            'bwrap_version': subprocess.check_output(['bwrap', '--version'], text=True).strip(),
            'provisioner_sha256': sha(Path(__file__))}
    with LOCK.open('x') as f:
        json.dump(lock, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: lock[k] for k in ['image_path', 'tree_sha256', 'bwrap_version']}))


if __name__ == '__main__':
    main()
