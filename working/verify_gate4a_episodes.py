"""Gate 4A sampler-only diagnostics; never runs notebooks, models, or scoring.

Run with the approved environment from any cwd:
    python -B working/verify_gate4a_episodes.py --output <new diagnostic JSON path>

Output is exclusive-create diagnostic evidence, NOT a passing episode manifest.
A data-packet test is not a security boundary for an arbitrary future candidate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import pickle
import platform
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BUDGETS = [5, 10, 25, 50, 100, 200]
TRIALS = 10
SEED = 42
CLASSES = np.array([1, 2, 3, 4])


def sha(path: Path) -> str:
    """SHA256 a file without rewriting it."""
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def array_hash(value: np.ndarray) -> str:
    """Hash dtype, shape, and C-order contents; retains ordered identities."""
    value = np.ascontiguousarray(value)
    digest = hashlib.sha256(canonical([value.dtype.str, list(value.shape)]))
    digest.update(value.tobytes())
    return digest.hexdigest()


def draw_reference(y: np.ndarray, budget: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Copy of the inspected reference sampler only, with budget renamed."""
    support_idx = []
    for cls in np.unique(y):
        cls_idx = np.where(y == cls)[0]
        chosen = rng.choice(cls_idx, min(budget, len(cls_idx)), replace=False)
        support_idx.extend(chosen.tolist())
    support_idx = np.array(support_idx)
    query_mask = np.ones(len(y), dtype=bool)
    query_mask[support_idx] = False
    return support_idx, np.flatnonzero(query_mask)


def generate(y: np.ndarray) -> list[dict]:
    """Preserve budget-major/trial-major order and one advancing PCG64 stream."""
    rng = np.random.default_rng(SEED)
    episodes = []
    for budget in BUDGETS:
        for trial in range(1, TRIALS + 1):
            before = copy.deepcopy(rng.bit_generator.state)
            support, query = draw_reference(y, budget, rng)
            episodes.append(dict(budget=budget, trial=trial, support=support, query=query,
                                 rng_before=before, rng_after=copy.deepcopy(rng.bit_generator.state)))
    return episodes


def packet_hashes(x: np.ndarray, y: np.ndarray, ids: np.ndarray, support: np.ndarray,
                  query: np.ndarray) -> dict[str, str]:
    """Diagnostic DTO: support-fitting fields and separate label-free query fields."""
    return {
        'support_ids': array_hash(ids[support]),
        'X_support': array_hash(x[support]),
        'y_support': array_hash(y[support]),
        'query_ids': array_hash(ids[query]),
        'X_query': array_hash(x[query]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Diagnostic output exists; never overwrite evidence')
    if args.output.resolve().parent != (ROOT / 'working').resolve():
        raise ValueError('Diagnostic output must be a new file directly under working/')
    if args.output.name == 'gate4_episode_manifest.json':
        raise ValueError('This verification-only harness cannot freeze a manifest')
    sys.path.insert(0, str(ROOT))
    paths = list((ROOT / 'original').rglob('*'))
    paths += list((ROOT / 'working/baseline_artifacts').rglob('*'))
    paths += list((ROOT / 'working/member3_baseline_frozen').rglob('*'))
    paths += list((ROOT / 'working').glob('*.ipynb'))
    paths += list((ROOT / 'working').glob('*.py'))
    paths += list((ROOT / 'data').glob('*.parquet'))
    paths += [ROOT / 'data/preprocessed/preprocessed_data.pkl']
    before = {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in paths if p.is_file()}
    manifest = json.loads((ROOT / 'working/baseline_artifacts/recovery_manifest.json').read_text())
    for name, item in manifest['files'].items():
        assert before['working/baseline_artifacts/' + name] == item['sha256']
    assert before['data/preprocessed/preprocessed_data.pkl'] == '51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe'
    nb = json.loads((ROOT / 'original/4-Modelling.ipynb').read_text(encoding='utf-8'))
    cell = ''.join(nb['cells'][24]['source'])
    # Pin source before copying/replaying its sampler. No cell is compiled/executed.
    assert before['original/4-Modelling.ipynb'] == '709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae'
    assert 'rng             = np.random.default_rng(42)' in cell
    assert 'SHOTS_PER_CLASS = [5, 10, 25, 50, 100, 200]' in cell
    assert 'N_TRIALS        = 10' in cell
    for p in ['working/4-Modelling_member3_reference.ipynb', 'working/4-Modelling_member3_reference_executed.ipynb']:
        working = json.loads((ROOT / p).read_text(encoding='utf-8'))
        assert len(working['cells']) == len(nb['cells'])
        assert all(a['source'] == b['source'] for a, b in zip(nb['cells'], working['cells']))
    with (ROOT / 'data/preprocessed/preprocessed_data.pkl').open('rb') as handle:
        data = pickle.load(handle)  # Trusted local input; privileged verifier, not candidate.
    x, y, ids = data['X_amsterdam'], data['y_amsterdam'], data['pixel_ids_amsterdam']
    assert x.shape == (25992, 60) and y.shape == (25992,) and ids.shape == (25992, 2)
    assert np.isfinite(x).all() and len(np.unique(ids, axis=0)) == len(y)
    schema = json.loads((ROOT / 'working/baseline_artifacts/feature_schema.json').read_text())
    assert schema['feature_names'] == data['feature_names']
    assert len(set(schema['feature_names'])) == 60
    assert not {'age_class', 'weighted_mean_year'}.intersection(schema['feature_names'])
    assert np.array_equal(np.unique(y), CLASSES)
    with np.load(ROOT / 'working/baseline_artifacts/amsterdam_zero_shot.npz', allow_pickle=False) as saved:
        assert np.array_equal(y, saved['y_amsterdam'])
        assert np.array_equal(ids, saved['pixel_ids_amsterdam'])
        assert saved['y_ams_pred_zero'].shape == y.shape  # No model inference or score.
    episodes, regenerated = generate(y), generate(y)
    pools = [np.flatnonzero(y == c) for c in CLASSES]
    rng_independent = np.random.default_rng(SEED)
    assert rng_independent.bit_generator.__class__.__name__ == 'PCG64'
    details = []
    known_from_previous = set()
    all_support = set(np.concatenate([e['support'] for e in episodes]).tolist())
    first_query = set(episodes[0]['query'].tolist())
    for e, regenerated_e in zip(episodes, regenerated):
        b, s, q = e['budget'], e['support'], e['query']
        assert np.array_equal(s, regenerated_e['support']) and np.array_equal(q, regenerated_e['query'])
        assert e['rng_before'] == regenerated_e['rng_before'] and e['rng_after'] == regenerated_e['rng_after']
        # Independent implementation: fixed precomputed pools and concatenation, same stream.
        independent_s = np.concatenate([rng_independent.choice(pool, b, replace=False) for pool in pools])
        independent_q = np.setdiff1d(np.arange(len(y)), independent_s)
        assert np.array_equal(s, independent_s) and np.array_equal(q, independent_q)
        assert rng_independent.bit_generator.state == e['rng_after']
        replay_rng = np.random.default_rng(SEED)
        replay_rng.bit_generator.state = copy.deepcopy(e['rng_before'])
        replay_s, replay_q = draw_reference(y, b, replay_rng)
        assert np.array_equal(s, replay_s) and np.array_equal(q, replay_q)
        assert replay_rng.bit_generator.state == e['rng_after']
        assert len(s) == 4*b and len(q) == len(y)-4*b
        assert len(np.unique(s)) == len(s) and len(np.unique(q)) == len(q)
        assert np.intersect1d(s, q).size == 0
        assert np.array_equal(np.sort(np.concatenate([s, q])), np.arange(len(y)))
        assert np.array_equal(y[s], np.repeat(CLASSES, b))
        assert all((y[s] == c).sum() == b for c in CLASSES)
        # One diagnostic dispatch contract for four named consumers; these are NOT models.
        packet = packet_hashes(x, y, ids, s, q)
        assert set(packet) == {'support_ids', 'X_support', 'y_support', 'query_ids', 'X_query'}
        for role in ['raw_prototype', 'frozen_rf', 'future_E1', 'future_candidate']:
            assert packet == packet_hashes(x, y, ids, s, q), role
        changed_query_labels = y.copy()
        changed_query_labels[q] = 0  # In-memory isolation probe only; no artifact changed.
        assert packet == packet_hashes(x, changed_query_labels, ids, s, q)
        assert packet != packet_hashes(x, y, ids, s, q[::-1])
        assert packet != packet_hashes(x, y, ids, s, q[:-1])
        previous_exposure = len(set(q.tolist()).intersection(known_from_previous))
        known_from_previous.update(s.tolist())
        details.append(dict(budget=b, trial=e['trial'], support_count=len(s), query_count=len(q),
                            support_class_counts={str(c): b for c in CLASSES},
                            query_class_counts={str(c): int((y == c).sum())-b for c in CLASSES},
                            support_row_indices_sha256=array_hash(s), query_row_indices_sha256=array_hash(q),
                            support_pixel_ids_sha256=packet['support_ids'], query_pixel_ids_sha256=packet['query_ids'],
                            rng_before=e['rng_before'], rng_after=e['rng_after'],
                            support_query_disjoint=True, deterministic_regeneration=True,
                            state_replay=True, packet_query_label_mutation_invariant=True,
                            four_consumer_packet_identity=True,
                            query_pixels_labelled_in_earlier_episode_supports=previous_exposure))
    query_pair_overlaps = [np.intersect1d(a['query'], b['query']).size for i,a in enumerate(episodes) for b in episodes[i+1:]]
    # Readability is not proof of misuse; it is a concrete unclosed access path.
    full_target_label_paths = [p for p in ['data/preprocessed/preprocessed_data.pkl', 'working/baseline_artifacts/amsterdam_zero_shot.npz'] if (ROOT / p).is_file()]
    changed = [p for p,h in before.items() if sha(ROOT / p) != h]
    assert not changed, changed
    original_status = subprocess.check_output(['git', 'status', '--short', '--', 'original/'], cwd=ROOT).decode()
    assert not original_status
    checks = {name: 'PASS' for name in [
        'frozen_hashes', 'feature_schema', 'row_pixel_alignment', 'sixty_episodes',
        'support_query_disjointness', 'budget_correctness', 'class_balance',
        'deterministic_regeneration', 'independent_implementation_agreement',
        'rng_state_replay', 'packet_query_label_mutation_invariance',
        'four_consumer_matched_packets', 'query_reordering_rejected', 'query_truncation_rejected',
        'original_clean', 'protected_files_unchanged']}
    checks['candidate_query_label_access_prevented'] = 'FAIL_NOT_ENFORCED'
    checks['cross_episode_label_access_prevented'] = 'FAIL_NOT_ENFORCED'
    checks['historical_trial_prediction_score_match'] = 'NOT_TESTED_SAMPLER_ONLY'
    result = {
        'status': 'BLOCKED', 'artifact_type': 'diagnostic_failure_report_not_manifest',
        'manifest_created': False, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'git_head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
        'working_tree_state': subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),
        'environment': {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
                        'numpy': np.__version__, 'scipy': importlib.metadata.version('scipy'),
                        'sklearn': importlib.metadata.version('scikit-learn')},
        'seed': SEED, 'rng': 'numpy.random.Generator(PCG64), default_rng(42)',
        'rng_policy': 'one advancing stream; budget-major, trial-major, class ascending; no reseeding',
        'total_episodes': len(episodes), 'budgets': BUDGETS, 'trials': list(range(1,11)),
        'query_label_isolation': 'Packet-only isolation PASS; current runtime/file/cross-episode isolation NOT ENFORCED',
        'sampler_source_cell_index_zero_based': 24,
        'sampler_source_cell_sha256': hashlib.sha256(cell.encode('utf-8')).hexdigest(),
        'harness_sha256': sha(Path(__file__)),
        'ordered_schema_sha256': hashlib.sha256(canonical(schema['feature_names'])).hexdigest(),
        'hash_encoding': 'ordered arrays: SHA256(canonical JSON [dtype.str,shape] + C-order bytes); schema: sorted-key compact JSON list UTF-8',
        'protected_input_hashes': before, 'checks': checks, 'episodes_diagnostic_fingerprints': details,
        'query_pair_overlap_min': int(min(query_pair_overlaps)), 'query_pair_overlap_max': int(max(query_pair_overlaps)),
        'unique_support_pixels_across_all_episodes': len(all_support),
        'first_episode_query_labels_inferable_from_all_ordered_support_lists': len(first_query.intersection(all_support)),
        'episodes_with_previous_support_labels_in_current_query': sum(d['query_pixels_labelled_in_earlier_episode_supports']>0 for d in details),
        'full_target_label_files_readable_in_current_runtime': full_target_label_paths,
        'blockers': [
            'No enforced evaluator/candidate boundary: reference kernel/global data and same-runtime readable input artifacts expose full target labels.',
            'A candidate-readable full manifest or persistent worker can expose query labels via other episodes: support lists are ordered in known class blocks.',
            'Future candidate code/dispatcher isolation has not been implemented or verified; DTO equality tests do not prove inaccessibility.'
        ],
        'training_performed': False, 'candidate_modelling': False, 'candidate_performance_calculated': False,
        'prototype_predictions_or_scores_calculated': False, 'notebook4_rerun': False,
        'protected_files_changed': changed,
    }
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({k: result[k] for k in ['status','total_episodes','checks','unique_support_pixels_across_all_episodes','first_episode_query_labels_inferable_from_all_ordered_support_lists','episodes_with_previous_support_labels_in_current_query','query_pair_overlap_min','query_pair_overlap_max']}, indent=2))
    print('DIAGNOSTIC_SHA256',sha(args.output))


if __name__ == '__main__':
    main()
