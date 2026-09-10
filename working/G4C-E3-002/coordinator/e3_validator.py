"""Independent E3 validator for exactly one explicit run directory.

No coordinator/worker imports, no worker launches, no historical-output fallback.
Production entry validates all 60 episodes. Private fixture context is not exposed
by the CLI and can never issue a production PASS.
"""
from __future__ import annotations
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import pickle
import re
import subprocess
import sys
import time
import types
import warnings
import numpy as np

MH = '9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
RFH = '5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870'
ENTRY_HASH = '34a69ebe9c99544aabfd4932dc57d384dbd96ea538fbbf0feed39aadb26a02c3'
RUNTIME_HASH = 'cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514'
PARAMS = {'candidate': 'E3', 'translation_strength': 1.0, 'continuous_indices': list(range(58))}
METHODS = ('candidate', 'raw_prototype', 'rf_reproduced', 'frozen_rf')
BUDGETS = (5, 10, 25, 50, 100, 200)


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canon(value)).hexdigest()


def _pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(encoding='utf8'), object_pairs_hook=_pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValidationError('Nonfinite JSON: '+x)))


def local_path(run, reference):
    """Allow run-relative or the producer's exact project-relative current-run path."""
    require(isinstance(reference, str) and '\\' not in reference and ':' not in reference,
            'Invalid artifact reference')
    prefix = f'working/{run.name}/'
    if reference.startswith('working/'):
        require(reference.startswith(prefix), 'Cross-run artifact reference')
        reference = reference[len(prefix):]
    parts = PurePosixPath(reference).parts
    require(parts and not PurePosixPath(reference).is_absolute() and all(p not in ('..', '.') for p in parts),
            'Unsafe artifact path')
    path = run
    for part in parts:
        path = path / part
        require(not path.is_symlink(), 'Symlink artifact forbidden')
    require(path.resolve().is_relative_to(run.resolve()), 'Artifact escaped target run')
    return path


def validate_layout(run):
    run = Path(run).absolute()
    require(not run.is_symlink() and run.resolve() == run, 'Run path must be canonical and not a symlink')
    require(re.fullmatch(r'G4C-E3-\d{3}', run.name) is not None, 'Wrong run identity')
    require(run.parent.name == 'working', 'Target must be project/working/current-run')
    require(run.is_dir(), 'Missing target run')
    for p in ('results/stop_summary.json', 'results/EXECUTION_STOP_REASON.md', 'results/EXTERNAL_STOP_REASON.md'):
        require(not local_path(run, p).exists(), 'Closed/failed run cannot be treated as current completed run')
    binding = load(local_path(run, 'checkpoint/validation_binding.json'))
    require(binding['run_id'] == run.name and binding['candidate'] == 'E3', 'Binding identity mismatch')
    auth = load(local_path(run, 'checkpoint/execution_authorization.json'))
    require(auth['run_id'] == run.name and auth['candidate'] == 'E3 only', 'Execution authorization identity mismatch')
    require(auth['parameters'] == PARAMS and auth['E4_E5'] is False and auth['notebook4_rerun'] is False,
            'Authorization scope/parameters mismatch')
    prep = load(local_path(run, 'checkpoint/infrastructure_preparation.json'))
    approval = prep['authorization']
    require(approval['run_id'] == run.name and approval['candidate'] == 'E3' and approval['scope'] == 'execution',
            'Preparation authorization mismatch')
    require(binding['preparation_sha256'] == sha(local_path(run, 'checkpoint/infrastructure_preparation.json')),
            'Preparation provenance changed')
    return run, binding, auth, prep


def score(y, pred):
    cm = np.zeros((4, 4), dtype=np.int64)
    np.add.at(cm, (y-1, pred-1), 1)
    tp = cm.diagonal()
    den = cm.sum(0)+cm.sum(1)
    f = np.divide(2*tp, den, out=np.zeros(4), where=den>0)
    return {'macro_f1': float(f.mean()), 'per_class_f1': f.tolist(),
            'precision': np.divide(tp, cm.sum(0), out=np.zeros(4), where=cm.sum(0)>0).tolist(),
            'recall': np.divide(tp, cm.sum(1), out=np.zeros(4), where=cm.sum(1)>0).tolist(),
            'accuracy': float(tp.sum()/cm.sum()), 'confusion': cm.tolist()}


def near(query, centers):
    return np.argmin(np.stack([np.sum((query-c)**2, axis=1) for c in centers], axis=1), axis=1)+1


def reconstruct_episode(x, y, ids, state, episode, forest):
    """Legacy independent E3 reconstruction, unchanged arithmetic and RF inference."""
    support = np.asarray(episode['support_row_indices'], dtype=np.int64)
    query = np.flatnonzero(~np.isin(np.arange(len(y)), support))
    centers = np.stack([x[support][y[support] == c].mean(0) for c in [1, 2, 3, 4]])
    delta = (centers-np.asarray(state['source_means'])).mean(0)
    delta[58:] = 0
    translated = x[query]-delta
    require(np.array_equal(translated[:, 58:], x[query, 58:]), 'Indicators changed')
    predictions = {'candidate': forest.predict(translated), 'rf_reproduced': forest.predict(x[query]),
                   'raw_prototype': near(x[query], centers)}
    packet = {'X_support': x[support].tolist(), 'y_support': y[support].tolist(),
              'support_ids': ids[support].tolist(), 'X_query': x[query].tolist(),
              'query_ids': ids[query].tolist(), 'source_state': state,
              'parameters': {'episode_id': episode['episode_id'], 'budget': episode['budget'],
                             'trial': episode['trial'], 'classes': [1, 2, 3, 4], 'candidate': 'E3'}}
    return support, query, centers, delta, predictions, packet


def array_hash(value):
    value = np.ascontiguousarray(value)
    h = hashlib.sha256(canon([value.dtype.str, list(value.shape)]))
    h.update(value.tobytes())
    return h.hexdigest()


def linux_path(path):
    value = Path(path).resolve().as_posix()
    return '/mnt/'+value[0].lower()+value[2:] if len(value)>1 and value[1]==':' else value


def check_transport(transport, run, label, role, packet):
    require(transport['returncode'] == 0 and not transport['stderr'], 'Transport failure')
    expected = ['wsl', '-d', 'Ubuntu', '--exec', '/usr/bin/python3', '-B',
                linux_path(run/'coordinator/g4c_linux_call.py'),
                linux_path(run/f'evidence/{label}.input.json'),
                linux_path(run/'coordinator'/({'episode':'episode_worker.py', 'source':'source_worker.py', 'preflight':'preflight_worker.py'}[role])),
                role, linux_path(run/f'evidence/{label}.json')]
    if role == 'episode':
        expected += ['--rf', linux_path(run.parent/'baseline_artifacts/rf_final.pkl')]
    require(transport['command'] == expected, 'Cross-run or altered transport command')
    raw = (json.dumps(packet, indent=2, sort_keys=True, allow_nan=False)+'\n').replace('\n', '\r\n').encode()
    require(transport['input_sha256'] == hashlib.sha256(raw).hexdigest(), 'Transport input digest mismatch')


def report_text(summary):
    """Deterministic rendering of existing results, not new scoring or verdict logic."""
    return ('# E3 execution report — '+summary['run_id']+'\n\n'
            'Primary execution results; independent validation is a separate required record.\n\n'
            '```json\n'+json.dumps(summary, indent=2, sort_keys=True, allow_nan=False)+'\n```\n')


def check_boundary(evidence, role, expected_code, packet, runtime_hash):
    ev = evidence['boundary_evidence']
    require(ev['role'] == role and ev['code_sha256'] == expected_code, 'Worker code/role mismatch')
    require(ev['packet_sha256'] == digest(packet), 'Worker packet mismatch')
    life = ev['lifecycle']
    require(ev['teardown_pass'] and life['pass_'] and life['subreaper_enabled'] and not life['final_survivors'],
            'Worker isolation/teardown failure')
    require(ev['returncode'] == 0 and ev['reason'] is None and not ev['stderr'], 'Worker failure')
    require(ev['runtime_lock_sha256'] == runtime_hash, 'Worker runtime lock mismatch')
    require(isinstance(ev['namespace'], str) and ev['namespace'].startswith('pid:['), 'Missing worker namespace')
    require(np.isfinite(ev['elapsed_seconds']) and ev['elapsed_seconds'] >= 0, 'Invalid runtime')
    return evidence['result'], ev


def _validate(run, context):
    """Shared substantive checks. Only production_context can yield production PASS."""
    started = time.perf_counter()
    run, binding, auth, prep = validate_layout(run)
    require(binding['manifest_sha256'] == auth['manifest_hash'] == context['manifest_hash'], 'Wrong manifest')
    require(binding['rf_sha256'] == auth['rf_hash'] == context['rf_hash'], 'RF anchor mismatch')
    manifest_path = local_path(run, 'checkpoint/episode_manifest.json')
    require(sha(manifest_path) == context['manifest_hash'], 'Run manifest changed')
    manifest = load(manifest_path)
    require(manifest['gate4a'] == 'PASS' and len(manifest['episodes']) == 60, 'Manifest episode contract mismatch')
    for name, expected in prep['code_hashes'].items():
        require('/' not in name and sha(local_path(run, 'coordinator/'+name)) == expected, 'Code provenance mismatch')
    require(sha(local_path(run, 'coordinator/e3_validator.py')) == binding['validator_sha256'], 'Validator hash mismatch')
    for name, expected in context['worker_hashes'].items():
        require(prep['code_hashes'][name] == expected, 'Unapproved worker/boundary code')
    inventory = load(local_path(run, 'artifact_hash_manifest.json'))
    require(inventory['run_id'] == run.name, 'Artifact inventory run mismatch')
    inventoried = {}
    for reference, expected in inventory['files'].items():
        path = local_path(run, reference)
        require(path not in inventoried, 'Duplicate normalized inventory path')
        require(path.is_file() and sha(path) == expected['sha256'] and path.stat().st_size == expected['bytes'],
                'Missing or modified inventoried artifact: '+reference)
        inventoried[path] = expected
    def required(relative):
        path = local_path(run, relative)
        require(path in inventoried, 'Required artifact not inventoried: '+relative)
        return path
    for rel in ['checkpoint/validation_binding.json', 'checkpoint/execution_authorization.json',
                'checkpoint/infrastructure_preparation.json', 'checkpoint/episode_manifest.json']:
        required(rel)
    summary = load(required('results/execution_summary.json'))
    rows = load(required('results/per_episode_results.json'))
    saved = load(required('candidate_state/source_state.json'))
    state = saved['source_state']
    require(summary['run_id'] == run.name, 'Summary run identity mismatch')
    require(summary['execution_status'] == 'COMPLETED_PENDING_INDEPENDENT_VERIFICATION', 'Incomplete execution')
    require(summary['parameters'] == state['parameters'] == PARAMS, 'E3 parameters mismatch')
    require(summary['episodes_completed'] == len(rows) == 60, 'Missing/extra episode rows')
    require(summary['all_predictions_finalized_before_scoring'] and not summary['E4_E5_run']
            and not summary['notebook4_rerun'], 'Execution/scoring boundary mismatch')
    ids_expected = [e['episode_id'] for e in manifest['episodes']]
    require(len(set(ids_expected)) == 60 and [r['episode_id'] for r in rows] == ids_expected,
            'Duplicate, missing, reordered or wrong episode identity')
    expected_npz = {e+'.npz' for e in ids_expected}
    require({p.name for p in (run/'predictions').glob('*.npz')} == expected_npz, 'Unexpected or missing prediction')
    expected_worker_files = {f'worker_{i:02d}.json' for i in range(1, 61)}
    actual_worker_files = {p.name for p in (run/'evidence').glob('worker_*.json') if not p.name.endswith('.transport.json')}
    require(actual_worker_files == expected_worker_files, 'Unexpected, missing or partial worker evidence')
    X, Y, x, y, ids = (context[k] for k in ('X', 'Y', 'x', 'y', 'ids'))
    means = np.stack([X[Y == c].mean(0) for c in [1, 2, 3, 4]])
    active = np.flatnonzero(X.var(0) > 0)
    require(active.tolist() == state['active_indices'], 'Source active feature mismatch')
    require(np.allclose(means, state['source_means'], rtol=1e-10, atol=1e-12), 'Source means mismatch')
    sh = digest(state)
    require(sh == saved['source_state_sha256'] == summary['source_state_sha256'], 'Source state hash mismatch')
    rng = np.random.default_rng(42)
    for i, (episode, row) in enumerate(zip(manifest['episodes'], rows)):
        b = BUDGETS[i//10]
        require((episode['budget'], episode['trial']) == (b, i%10+1), 'Manifest ordering mismatch')
        require((row['budget'], row['trial']) == (b, i%10+1), 'Row ordering mismatch')
        require(rng.bit_generator.state == episode['rng_before'], 'RNG before mismatch')
        sampled = np.concatenate([rng.choice(np.flatnonzero(y == c), b, replace=False) for c in [1, 2, 3, 4]])
        require(np.array_equal(sampled, episode['support_row_indices']), 'Support replay mismatch')
        require(rng.bit_generator.state == episode['rng_after'], 'RNG after mismatch')
        support, query, centers, delta, predictions, packet = reconstruct_episode(x, y, ids, state, episode, context['forest'])
        require(len(set(support.tolist())) == 4*b and not np.intersect1d(support, query).size
                and len(support)+len(query) == len(y), 'Support/query partition mismatch')
        require(np.array_equal(ids[support], episode['support_pixel_ids']), 'Support pixel identity mismatch')
        for field, value in [('support_row_indices_sha256', support), ('query_row_indices_sha256', query),
                             ('support_pixel_ids_sha256', ids[support]), ('query_pixel_ids_sha256', ids[query]),
                             ('X_support_sha256', x[support]), ('X_query_sha256', x[query])]:
            require(array_hash(value) == episode[field], 'Manifest array digest mismatch: '+field)
        for field in ['support_row_indices_sha256', 'query_row_indices_sha256', 'query_pixel_ids_sha256']:
            require(row[field] == episode[field], 'Manifest row digest mismatch')
        predictions['frozen_rf'] = context['rf_predictions'][query]
        require(np.array_equal(predictions['rf_reproduced'], predictions['frozen_rf']), 'Frozen RF reload predictions mismatch')
        prediction_path = local_path(run, row['prediction_artifact'])
        require(prediction_path == required('predictions/'+episode['episode_id']+'.npz'), 'Cross-run/noncanonical prediction path')
        require(sha(prediction_path) == row['prediction_sha256'], 'Prediction hash mismatch')
        evidence_path = local_path(run, row['worker_evidence'])
        require(evidence_path == required(f'evidence/worker_{i+1:02d}.json'), 'Cross-run/noncanonical evidence path')
        require(sha(evidence_path) == row['worker_output_sha256'], 'Worker evidence hash mismatch')
        evidence = load(evidence_path)
        out, ev = check_boundary(evidence, 'episode', context['worker_hashes']['episode_worker.py'], packet, context['runtime_hash'])
        require(out['source_state_sha256'] == sh and out['fresh_state_probe'], 'Adaptation state/isolation mismatch')
        require(out['label_access'] == {'source_state_only': True, 'current_support_labels': len(support),
                                      'query_labels': 0, 'other_episode_labels': 0}, 'Worker label boundary mismatch')
        require(out['query_fingerprint'] == digest(ids[query].tolist()), 'Query fingerprint mismatch')
        require(np.array_equal(centers, out['adaptation_state']['prototypes']), 'Prototype reconstruction mismatch')
        require(np.allclose(delta, out['adaptation_state']['translation'], rtol=1e-10, atol=1e-12), 'Translation mismatch')
        require(set(out['predictions']) == {'candidate', 'raw_prototype', 'rf_reproduced'}, 'Worker prediction keys mismatch')
        for stage in ('before', 'after'):
            require(out['descriptor_audit'][stage]['forbidden'] == [], 'Forbidden worker descriptor')
        transport = load(required(f'evidence/worker_{i+1:02d}.transport.json'))
        check_transport(transport, run, f'worker_{i+1:02d}', 'episode', packet)
        if not context.get('synthetic'):
            native = evidence['infrastructure_io']
            config = load(required('coordinator/native_cache.json'))
            require(native['sha256'] == config['rf_sha256'] == RFH and native['bytes'] == 1336382673,
                    'Native RF provenance mismatch')
            require(native['path'] == config['directory'].rstrip('/')+'/'+RFH+'.pkl', 'Native RF path mismatch')
        require(row['worker_seconds'] == ev['elapsed_seconds'] and row['peak_rss_kib'] == out['peak_rss_kib']
                and row['warnings'] == out['warnings'] and row['worker_teardown'], 'Episode resource/warning mismatch')
        require(out['peak_rss_kib'] > 0, 'Missing peak memory')
        with np.load(prediction_path, allow_pickle=False) as saved_predictions:
            require(set(saved_predictions.files) == set(METHODS)|{'query_indices', 'query_ids'}, 'Prediction archive schema mismatch')
            require(np.array_equal(saved_predictions['query_indices'], query) and np.array_equal(saved_predictions['query_ids'], ids[query]), 'Query row alignment mismatch')
            require(set(row['metrics']) == set(METHODS), 'Metric method set mismatch')
            for name, pred in predictions.items():
                require(pred.shape == (len(query),) and np.isin(pred, [1, 2, 3, 4]).all(), 'Invalid prediction values')
                require(np.array_equal(pred, saved_predictions[name]), 'Independent prediction disagreement: '+name)
                if name in out['predictions']:
                    require(np.array_equal(pred, out['predictions'][name]), 'Worker/archive disagreement')
                calculated = score(y[query], pred)
                require(calculated == row['metrics'][name], 'Independent metric disagreement')
                require(digest(calculated['confusion']) == row['confusion_sha256'][name], 'Confusion hash mismatch')
        require(row['metrics']['raw_prototype']['macro_f1'] == context['historical_raw'][b][i%10], 'Frozen raw comparator mismatch')
        require(row['paired_deltas'] == {
            'candidate_minus_raw': row['metrics']['candidate']['macro_f1']-row['metrics']['raw_prototype']['macro_f1'],
            'candidate_minus_rf': row['metrics']['candidate']['macro_f1']-row['metrics']['frozen_rf']['macro_f1']}, 'Paired delta mismatch')
    require(set(summary['summary']) == {str(b) for b in BUDGETS}, 'Missing/extra summary budget')
    for b in BUDGETS:
        group = [r for r in rows if r['budget'] == b]
        calculated = {}
        for name in METHODS:
            values = np.array([r['metrics'][name]['macro_f1'] for r in group])
            calculated[name] = {'mean': float(values.mean()), 'std_ddof0': float(values.std()), 'values': values.tolist(),
                               'per_class_mean': np.mean([r['metrics'][name]['per_class_f1'] for r in group], 0).tolist()}
        for name in ('candidate_minus_raw', 'candidate_minus_rf'):
            values = np.array([r['paired_deltas'][name] for r in group])
            calculated[name] = {'mean': float(values.mean()), 'std_ddof0': float(values.std()),
                               'values': values.tolist(), 'positive_trials': int((values>0).sum())}
        require(calculated == summary['summary'][str(b)], 'Summary statistics mismatch')
    p = summary['summary']['25']
    raw_reg = np.asarray(p['candidate']['per_class_mean'])-p['raw_prototype']['per_class_mean']
    rf_reg = np.asarray(p['candidate']['per_class_mean'])-p['frozen_rf']['per_class_mean']
    criteria = {'mean_gain_over_raw_ge_0.0100': p['candidate_minus_raw']['mean']>=.01,
                'positive_raw_gain_ge_8_of_10': p['candidate_minus_raw']['positive_trials']>=8,
                'no_mean_per_class_raw_regression_worse_than_0.0200': bool(np.all(raw_reg>=-.02)),
                'mean_gain_over_same_query_rf_ge_0.0100': p['candidate_minus_rf']['mean']>=.01,
                'no_mean_per_class_rf_regression_worse_than_0.0200': bool(np.all(rf_reg>=-.02))}
    verdict = 'PROMISING' if all(criteria.values()) else ('FALSIFIED' if p['candidate_minus_rf']['mean']<=0 or np.any(rf_reg<-.02) or p['candidate_minus_raw']['mean']<=0 or np.any(raw_reg<-.02) else 'INCONCLUSIVE')
    require(criteria == summary['success_criteria'] and verdict == summary['scientific_verdict'], 'E3 criteria/verdict mismatch')
    require(raw_reg.tolist() == summary['primary_per_class_delta_candidate_minus_raw'] and rf_reg.tolist() == summary['primary_per_class_delta_candidate_minus_rf'], 'Per-class summary delta mismatch')
    require(summary['peak_worker_rss_kib'] == max(r['peak_rss_kib'] for r in rows), 'Peak resource summary mismatch')
    require(summary['warnings'] == [{'episode_id': r['episode_id'], 'warnings': r['warnings']} for r in rows if r['warnings']], 'Warning summary mismatch')
    first = manifest['episodes'][0]
    s = np.asarray(first['support_row_indices']); q = np.setdiff1d(np.arange(len(y)), s)
    probe = {'X_support': x[s].tolist(), 'y_support': y[s].tolist(), 'support_ids': ids[s].tolist(),
             'X_query': x[q].tolist(), 'query_ids': ids[q].tolist(), 'parameters': {'mode': 'preflight'}}
    for label in ('preflight_1', 'preflight_2', 'post_candidate_probe'):
        out, ev = check_boundary(load(required('evidence/'+label+'.json')), 'preflight', context['worker_hashes']['preflight_worker.py'], probe, context['runtime_hash'])
        require(out['status'] == 'PASS' and out['model_computation'] is False, 'Preflight failed')
        check_transport(load(required('evidence/'+label+'.transport.json')), run, label, 'preflight', probe)
    source_packet = {'X_source': X.tolist(), 'y_source': Y.tolist(), 'parameters': PARAMS}
    out, ev = check_boundary(load(required('evidence/source_worker.json')), 'source', context['worker_hashes']['source_worker.py'], source_packet, context['runtime_hash'])
    require(out['target_rows_received'] == 0 and out['fit_scope'] == 'Madrid only'
            and out['source_state'] == state and out['source_state_sha256'] == sh, 'Source worker reconstruction mismatch')
    check_transport(load(required('evidence/source_worker.transport.json')), run, 'source_worker', 'source', source_packet)
    require(required('EXECUTION_REPORT.md').read_text(encoding='utf8') == report_text(summary), 'Execution report corrupted or inconsistent')
    return {'status': 'SYNTHETIC_TEST_PASS' if context.get('synthetic') else 'PASS', 'run_id': run.name,
            'candidate': 'E3', 'exact_prediction_records': 60, 'exact_score_confusion_records': 60,
            'historical_raw_match': 60, 'rng_episode_replay': 60, 'worker_teardown': 60,
            'fresh_state_probes': 3, 'scientific_verdict': verdict, 'seconds': time.perf_counter()-started}


def production_context(run):
    root = run.parent.parent
    entry = root/'working/G4B-E1-001/entry.json'
    require(sha(entry) == ENTRY_HASH, 'Frozen protected registry anchor changed')
    protected = load(entry)['protected_hashes']
    require(len(protected) == 33, 'Protected registry size mismatch')
    for path, expected in protected.items():
        require(sha(root/path) == expected, 'Protected artifact changed: '+path)
    checkpoint = root/'working/G4C-PROVENANCE-CHECKPOINT-002/file_fingerprints.json'
    require(sha(checkpoint) == 'e1e1d8bda427d15f41ee06ed1ff5e391d6210ab2637b950cd4ac5158f9fd1a2a', 'Checkpoint anchor changed')
    for path, item in load(checkpoint).items():
        current = root/path
        if path == 'working/Open Notebook.onetoc2':
            # Only the already-approved path-specific external-metadata exception.
            with current.open('rb') as stream:
                require(stream.read(16).hex() == 'a12fff43d9ef764c9ee210ea5722765f', 'Metadata exception signature changed')
            require(not current.is_symlink() and current.is_file() and current.stat().st_nlink == 1, 'Metadata type changed')
        else:
            require(sha(current) == item['sha256'], 'Frozen checkpoint input changed: '+path)
    require(sha(root/'working/gate4_episode_manifest.json') == MH, 'Frozen manifest changed')
    require(sha(root/'working/baseline_artifacts/rf_final.pkl') == RFH, 'Frozen RF changed')
    require(not subprocess.check_output(['git', 'status', '--short', '--', 'original/'], cwd=root), 'Original tree dirty')
    helper = root/'working/minimal_standard_scaler.py'
    require(sha(helper) == 'c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111', 'Pickle dependency changed')
    if 'working.minimal_standard_scaler' not in sys.modules:
        package = types.ModuleType('working'); package.__path__ = []
        spec = importlib.util.spec_from_file_location('working.minimal_standard_scaler', helper)
        module = importlib.util.module_from_spec(spec)
        sys.modules['working'] = package; sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    else:
        require(Path(sys.modules['working.minimal_standard_scaler'].__file__).resolve() == helper.resolve(), 'Wrong pickle module origin')
    with (root/'data/preprocessed/preprocessed_data.pkl').open('rb') as stream:
        data = pickle.load(stream)
    require(data['X_madrid'].shape == (76263,60) and data['X_amsterdam'].shape == (25992,60), 'Dataset schema mismatch')
    schema = load(root/'working/baseline_artifacts/feature_schema.json')
    require(schema['feature_names'][-2:] == ['has_early_data', 'has_late_data'], 'Feature order mismatch')
    with warnings.catch_warnings(record=True):
        warnings.simplefilter('always')
        with (root/'working/baseline_artifacts/rf_final.pkl').open('rb') as stream:
            forest = pickle.load(stream)
    require(len(forest.estimators_) == 500 and forest.n_features_in_ == 60 and np.array_equal(forest.classes_, [1,2,3,4]), 'Frozen RF contract mismatch')
    with np.load(root/'working/baseline_artifacts/amsterdam_zero_shot.npz', allow_pickle=False) as ref:
        require(np.array_equal(ref['y_amsterdam'], data['y_amsterdam']) and np.array_equal(ref['pixel_ids_amsterdam'], data['pixel_ids_amsterdam']), 'Baseline target alignment mismatch')
        rf = ref['y_ams_pred_zero'].copy()
    with np.load(root/'working/baseline_artifacts/prototype_trial_scores.npz', allow_pickle=False) as ref:
        raw = {b: ref[f'shots_{b}'].copy() for b in BUDGETS}
    return {'X': data['X_madrid'], 'Y': data['y_madrid'], 'x': data['X_amsterdam'], 'y': data['y_amsterdam'],
            'ids': data['pixel_ids_amsterdam'], 'forest': forest, 'rf_predictions': rf, 'historical_raw': raw,
            'manifest_hash': MH, 'rf_hash': RFH, 'runtime_hash': RUNTIME_HASH,
            'worker_hashes': {'episode_worker.py': 'b3cf5ab28ccbac2506c8ed7398a3b25254b24c86d8e58e5f1de742577660c350',
                              'source_worker.py': 'c00c31624c9e107ce5aba2024c9c834648ff92f816acb390127846a2b3938d30',
                              'preflight_worker.py': 'bb5a3114ebfaa4cf0716d9cf4f4467c6682924c95ffd7fa631b40ca4b513e2f6'}}


def validate_e3_run(run_dir):
    run, binding, auth, prep = validate_layout(run_dir)
    require(binding['validator_sha256'] == sha(Path(__file__)), 'Running validator differs from bound validator')
    context = production_context(run)
    result = _validate(run, context)
    # Reload protected hashes at the end, without retaining a second forest/data copy.
    root = run.parent.parent
    for path, expected in load(root/'working/G4B-E1-001/entry.json')['protected_hashes'].items():
        require(sha(root/path) == expected, 'Protected artifact changed during verification')
    result['protected_artifacts'] = 33
    result['verifier_sha256'] = sha(Path(__file__))
    return result


def inspect_closed_run(run_dir):
    """Hash-only, read-only inspection; never returns production validation PASS."""
    run = Path(run_dir).resolve()
    inventory = load(run/'artifact_hash_manifest.json')
    for reference, expected in inventory['files'].items():
        path = local_path(run, reference)
        require(sha(path) == expected['sha256'], 'Historical evidence changed')
    return {'status': 'HISTORICAL_EVIDENCE_ONLY', 'run_id': run.name, 'payloads': len(inventory['files'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run_dir', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(validate_e3_run(args.run_dir), indent=2))
    except Exception as exc:
        print(json.dumps({'status': 'FAIL', 'run_dir': str(args.run_dir), 'error': str(exc)}))
        raise SystemExit(1)
