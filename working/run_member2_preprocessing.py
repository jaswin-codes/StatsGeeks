"""Execute every Notebook 3 code cell, headlessly, and validate its artifact.
Run from the repository root: python working/run_member2_preprocessing.py
"""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import pickle
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ['MPLBACKEND'] = 'Agg'
import numpy as np

notebook = ROOT / 'working/3-Preprocessing_member2_baseline.ipynb'
nb = json.loads(notebook.read_text(encoding='utf-8'))
original = ROOT / 'original/3-Preprocessing.ipynb'
original_hash = hashlib.sha256(original.read_bytes()).hexdigest()
ns = {'__name__': '__main__'}
log_path = ROOT / 'working/member2_preprocessing_execution.log'
with log_path.open('w', encoding='utf-8') as log:
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        try:
            count = 0
            for i, cell in enumerate(nb['cells']):
                if cell['cell_type'] != 'code':
                    continue
                count += 1
                print(f'=== Cell {i} ===', flush=True)
                output = io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    exec(compile(''.join(cell['source']), f'{notebook.name}:cell{i}', 'exec'), ns)
                text = output.getvalue()
                print(text, flush=True)
                cell['execution_count'] = count
                cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': text.splitlines(True)}] if text else []
            artifact = ns['save_path']
            with artifact.open('rb') as f:
                loaded = pickle.load(f)
            names = loaded['feature_names']
            assert names == ns['FEATURE_COLS']
            assert len(names) == len(set(names)) == 60
            assert names == sum(loaded['feat_groups'].values(), [])
            scaler = loaded['scaler']
            from working.minimal_standard_scaler import StandardScaler
            assert type(scaler) is StandardScaler
            assert scaler.n_features_in_ == 60
            raw_madrid = ns['features_madrid'][names].to_numpy(dtype=np.float64)
            np.testing.assert_allclose(scaler.mean_, raw_madrid.mean(axis=0))
            np.testing.assert_allclose(scaler.var_, raw_madrid.var(axis=0, ddof=0))
            # sklearn treats numerically indistinguishable constant columns as constant.
            eps = np.finfo(np.float64).eps
            n = len(raw_madrid)
            constant = scaler.var_ <= n * eps * scaler.var_ + (n * scaler.mean_ * eps) ** 2
            expected_scale = np.sqrt(scaler.var_)
            expected_scale[constant] = 1.0
            np.testing.assert_allclose(scaler.scale_, expected_scale, rtol=1e-12, atol=1e-12)
            for city in ['madrid', 'amsterdam']:
                X, y = loaded[f'X_{city}'], loaded[f'y_{city}']
                raw = ns[f'features_{city}'][names].to_numpy(dtype=np.float64)
                assert X.shape == (len(y), 60)
                assert loaded[f'pixel_ids_{city}'].shape == (len(y), 2)
                assert np.isfinite(X).all()
                assert set(np.unique(y)) == {1, 2, 3, 4}
                np.testing.assert_array_equal(X, ns[f'X_{city}'])
                np.testing.assert_array_equal(y, ns[f'y_{city}'])
                np.testing.assert_allclose(scaler.transform(raw), X)
                print(f'{city}: X={X.shape}, y={y.shape}; finite, labels, pixel IDs, reload and transform PASS')
            np.testing.assert_allclose(loaded['X_madrid'].mean(axis=0), 0, atol=1e-10)
            np.testing.assert_allclose(loaded['X_madrid'].var(axis=0)[~constant], 1, atol=1e-10)
            print(f'Scaler: {type(scaler).__module__}.{type(scaler).__name__}; n_features_in_={scaler.n_features_in_}')
            print('Scaler population variance and constant-column handling: PASS on notebook data')
            print('Feature names:', names)
            assert hashlib.sha256(original.read_bytes()).hexdigest() == original_hash
            print('Original notebook unchanged; SHA256:', original_hash)
            print('Artifact:', artifact, 'bytes:', artifact.stat().st_size)
            print('VALIDATION PASSED', flush=True)
        except BaseException:
            traceback.print_exc()
            raise
executed = ROOT / 'working/3-Preprocessing_member2_baseline_executed.ipynb'
executed.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'Completed. See {log_path.relative_to(ROOT)}')
