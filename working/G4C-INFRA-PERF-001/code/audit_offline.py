"""Independent read-only artifact/science audit. No production-module imports.

Does not fit, adapt, launch workers, load the forest, or score partial E3 results.
Archived E2 metrics are independently recomputed from saved prediction arrays.
"""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[3]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    started = time.perf_counter()
    anchors = {
        'G4C-E2-008': '6bab2d294b291cda113b471921299224051d390dfbe5c9a58e42df8ba42570bd',
        'G4C-E3-001': '60d74b21be8825af89917895b45cc64e7bf1021b7321042345383686152454a8',
    }
    counts = {}
    for identity, expected in anchors.items():
        manifest = ROOT/'working'/identity/'artifact_hash_manifest.json'
        if sha(manifest) != expected:
            raise RuntimeError('Historical inventory anchor changed')
        inventory = json.loads(manifest.read_text())
        for path, spec in inventory['files'].items():
            item = ROOT/path
            if sha(item) != spec['sha256'] or item.stat().st_size != spec['bytes']:
                raise RuntimeError(f'Historical artifact mutation: {path}')
        counts[identity] = len(inventory['files'])
    protected = json.loads((ROOT/'working/G4B-E1-001/entry.json').read_text())['protected_hashes']
    if len(protected) != 33 or any(sha(ROOT/p) != h for p, h in protected.items()):
        raise RuntimeError('Protected artifact mismatch')
    rows = json.loads((ROOT/'working/G4C-E2-008/results/per_episode_results.json').read_text())
    with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz', allow_pickle=False) as baseline:
        labels = baseline['y_amsterdam'].copy()
    records = 0
    for row in rows:
        with np.load(ROOT/row['prediction_artifact'], allow_pickle=False) as saved:
            truth = labels[saved['query_indices']]
            for name, expected in row['metrics'].items():
                pred = saved[name]
                cm = np.zeros((4, 4), dtype=np.int64)
                np.add.at(cm, (truth-1, pred-1), 1)
                den = cm.sum(axis=0) + cm.sum(axis=1)
                f1 = np.divide(2*cm.diagonal(), den, out=np.zeros(4), where=den != 0)
                if cm.tolist() != expected['confusion'] or float(f1.mean()) != expected['macro_f1'] or f1.tolist() != expected['per_class_f1']:
                    raise RuntimeError('Archived E2 score disagreement')
                records += 1
    if len(rows) != 60:
        raise RuntimeError('Archived E2 episode count mismatch')
    # Inspect prepared (not executed) code emitted by the preparation utility.
    manifest = json.loads((ROOT/'working/G4C-INFRA-PERF-001/evidence/prepared_asset_hashes.json').read_text())
    unchanged = ['episode_worker.py', 'source_worker.py', 'preflight_worker.py',
                 'g4c_boundary.py', 'gate4_production_boundary.py', 'gate4_lifecycle.py']
    for name in unchanged:
        if manifest[name] != sha(ROOT/'working/G4C-E3-001/coordinator'/name):
            raise RuntimeError(f'Unexpected scientific/boundary code change: {name}')
    print(json.dumps({
        'status': 'OFFLINE_CHECKS_PASS', 'seconds': time.perf_counter()-started,
        'historical_inventory_payloads_verified': counts, 'protected_artifacts_verified': 33,
        'manifest_sha256': sha(ROOT/'working/gate4_episode_manifest.json'),
        'rf_sha256': sha(ROOT/'working/baseline_artifacts/rf_final.pkl'),
        'unchanged_worker_and_boundary_assets': unchanged,
        'archived_E2_episodes': len(rows), 'archived_E2_method_metric_records': records,
        'archived_E3_predictions_hash_checked_only': 52,
        'optimized_prediction_equivalence': 'NOT_EXECUTED: worker launch prohibited',
        'new_scientific_conclusions': False, 'worker_launches': 0, 'experiments_started': 0,
        'independence_scope': 'Separate verification implementation/process; not another human reviewer',
        'execution_readiness_certification': 'PENDING authorized end-to-end equivalence and E4/E5 bindings'
    }, indent=2))


if __name__ == '__main__':
    main()
