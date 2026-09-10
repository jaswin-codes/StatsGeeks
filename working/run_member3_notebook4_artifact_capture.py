"""Run unchanged Notebook 4 cells once, then serialize their in-memory outputs.

The added terminal capture cell runs only after all organiser cells have completed.
It does not alter source cell text, input data, model parameters, seeds, or metrics.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
WORKING = ROOT / "working"
SOURCE = WORKING / "4-Modelling_member3_reference.ipynb"
OUTPUT = WORKING / "4-Modelling_member3_reference_capture_executed.ipynb"

CAPTURE_SOURCE = r'''
# Artifact-capture sidecar: executes after all untouched organiser Notebook 4 cells.
import hashlib
import json
import platform
import sys
import sklearn
import scipy

artifact_dir = Path('baseline_artifacts')
artifact_dir.mkdir(parents=True, exist_ok=True)

def _sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

with open(artifact_dir / 'rf_final.pkl', 'wb') as handle:
    pickle.dump(rf_final, handle, protocol=pickle.HIGHEST_PROTOCOL)

np.savez_compressed(
    artifact_dir / 'madrid_cv_oof.npz',
    fold_f1=np.asarray(fold_f1),
    oof_true=oof_true,
    oof_pred=oof_pred,
    oof_proba=oof_proba,
    oof_indices=oof_indices,
    y_madrid=y_madrid,
    pixel_ids_madrid=pixel_ids_madrid,
)
np.savez_compressed(
    artifact_dir / 'amsterdam_zero_shot.npz',
    y_amsterdam=y_amsterdam,
    y_ams_pred_zero=y_ams_pred_zero,
    proba_amsterdam_zero=proba_amsterdam_zero,
    pixel_ids_amsterdam=pixel_ids_amsterdam,
)
np.savez_compressed(
    artifact_dir / 'prototype_trial_scores.npz',
    **{f'shots_{shots}': np.asarray(scores) for shots, scores in proto_results.items()},
)
(artifact_dir / 'feature_schema.json').write_text(
    json.dumps({'feature_names': feature_names, 'feat_groups': data['feat_groups']}, indent=2, sort_keys=True) + '\n',
    encoding='utf-8',
)
metadata = {
    'artifact_type': 'notebook4_reference_artifact_capture',
    'capture_note': 'Sidecar capture after unchanged organiser cells; no model/evaluation rerun beyond this one identical reference execution.',
    'python': sys.version.replace('\n', ' '),
    'python_executable': sys.executable,
    'platform': platform.platform(),
    'numpy': np.__version__,
    'scipy': scipy.__version__,
    'scikit_learn': sklearn.__version__,
    'rf_params': RF_PARAMS,
    'cv_params': {'n_folds': N_FOLDS, 'n_repeats': N_REPEATS, 'random_state': 42},
    'prototype_params': {'shots_per_class': SHOTS_PER_CLASS, 'n_trials': N_TRIALS, 'rng': 'np.random.default_rng(42), advancing across budgets/trials'},
    'measured': {
        'madrid_cv_mean': float(np.mean(fold_f1)),
        'madrid_cv_std_ddof0': float(np.std(fold_f1)),
        'amsterdam_zero_shot_macro_f1': float(f1_zero),
        'prototype_mean_std': {str(k): {'mean': float(np.mean(v)), 'std_ddof0': float(np.std(v))} for k, v in proto_results.items()},
    },
    'input_shapes': {'X_madrid': list(X_madrid.shape), 'X_amsterdam': list(X_amsterdam.shape)},
    'classes': {'madrid': np.unique(y_madrid).tolist(), 'amsterdam': np.unique(y_amsterdam).tolist()},
    'source_cell_count': 32,
    'capture_episode_indices_note': 'The organiser prototype loop does not retain per-trial support/query indices; unavailable without changing that loop.',
}
metadata_path = artifact_dir / 'metadata.json'
metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + '\n', encoding='utf-8')
payloads = [
    artifact_dir / 'rf_final.pkl', artifact_dir / 'madrid_cv_oof.npz',
    artifact_dir / 'amsterdam_zero_shot.npz', artifact_dir / 'prototype_trial_scores.npz',
    artifact_dir / 'feature_schema.json', metadata_path,
]
manifest = {
    'artifact_type': 'manifest',
    'files': {path.name: {'sha256': _sha256(path), 'bytes': path.stat().st_size} for path in payloads},
    'source_notebook_sha256': _sha256(Path('../working/4-Modelling_member3_reference.ipynb')),
    'input_pickle_sha256': _sha256(Path('../data/preprocessed/preprocessed_data.pkl')),
}
(artifact_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print('ARTIFACT_CAPTURE_COMPLETE', artifact_dir)
'''


def main() -> None:
    os.environ["PYTHONPATH"] = str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", "")
    notebook = nbformat.read(SOURCE, as_version=4)
    source_cells = list(notebook.cells)
    notebook.cells.append(nbformat.v4.new_code_cell(CAPTURE_SOURCE, metadata={"artifact_capture_sidecar": True}))
    client = NotebookClient(notebook, timeout=None, resources={"metadata": {"path": str(WORKING)}})
    client.execute(cwd=str(WORKING))
    if any(cell.source != original.source for cell, original in zip(notebook.cells[:len(source_cells)], source_cells)):
        raise RuntimeError("An organiser source cell changed during capture execution")
    nbformat.write(notebook, OUTPUT)
    print(f"Artifact capture complete: {OUTPUT}")


if __name__ == "__main__":
    main()
