"""Read-only independent reconstruction of approved additive runtime; no models/data."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def tree(p):
    return {f.relative_to(p).as_posix(): sha(f) for f in sorted(p.rglob('*')) if f.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'working/gate4_approved_runtime_tree_validation.json')
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve().parent != ROOT / 'working':
        raise ValueError('Require a new output directly under working/')
    lock_path = ROOT / 'working/gate4_runtime_narwhals_lock.json'
    lock = json.loads(lock_path.read_text())
    evidence = json.loads((ROOT / 'working/gate4_approved_runtime_validation.json').read_text())
    assert sha(lock_path) == evidence['runtime_lock_sha256']
    assert tree(Path(lock['image_path'])) == lock['files']
    expected = sorted((n, r['version']) for n, r in lock['wheels'].items())
    for run in evidence['runs']:
        assert run['returncode'] == 0 and not run['stderr']
        r = run['result']
        assert sorted(map(tuple, r['distributions'])) == expected
        assert all(v == 'PASS' for v in r['imports'].values())
        assert all(p.lstrip('/') in lock['files'] for p in r['mapped_files'])
        assert r['project_mount_absent']
    with tempfile.TemporaryDirectory(prefix='gate4_approved_independent_') as tmp:
        rebuilt = Path(tmp)
        for record in lock['wheels'].values():
            assert sha(record['source']) == record['sha256']
            with zipfile.ZipFile(record['source']) as z:
                z.extractall(rebuilt / 'numeric')
        shutil.copytree('/usr/lib/python3.14', rebuilt / 'usr/lib/python3.14', ignore=shutil.ignore_patterns('__pycache__', 'site-packages', 'dist-packages'))
        (rebuilt / 'usr/bin').mkdir(parents=True)
        shutil.copy2(lock['interpreter_source'], rebuilt / 'usr/bin/python3.14')
        for path, record in lock['declared_native_sources'].items():
            assert sha(record['source']) == record['sha256']
            dest = rebuilt / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(record['source'], dest)
        assert tree(rebuilt) == lock['files']
    output = dict(independent_full_tree_rebuild='PASS', exact_six_distributions='PASS',
                  declared_native_mappings_only='PASS', runtime_lock_sha256=sha(lock_path),
                  tree_sha256=lock['tree_sha256'], files=len(lock['files']),
                  production_isolation='NOT_RUN', candidate_modelling=False, notebook4_rerun=False)
    path = args.output
    with path.open('x') as f:
        json.dump(output, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
