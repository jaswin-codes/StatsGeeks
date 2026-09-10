"""Certification preflight only: no candidate launch and no infrastructure repair.

Fails closed before prediction-subset execution if production validation is unbound.
"""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time
import types

ROOT = Path(__file__).resolve().parents[2]
CERT = Path(__file__).resolve().parent
PERF = ROOT / 'working/G4C-INFRA-PERF-001'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    started = time.perf_counter()
    result = {'certification_status': 'FAIL', 'checks': {}, 'failures': [],
              'new_E3_run_created': False, 'candidate_workers_launched': 0,
              'prediction_subset': 'NOT_RUN: preflight must pass first',
              'native_runtime_live_check': 'NOT_RUN', 'infrastructure_modified': False}
    anchors = {
        'G4C-INFRA-PERF-001': '32f9378c2242f7a1ec9c3d82a85938addf4f43cbdf929618a837721827acc6f2',
        'G4C-E2-008': '6bab2d294b291cda113b471921299224051d390dfbe5c9a58e42df8ba42570bd',
        'G4C-E3-001': '60d74b21be8825af89917895b45cc64e7bf1021b7321042345383686152454a8',
    }
    try:
        for identity, expected in anchors.items():
            manifest = ROOT / 'working' / identity / 'artifact_hash_manifest.json'
            if sha(manifest) != expected:
                raise RuntimeError(f'Inventory anchor changed: {identity}')
            payloads = json.loads(manifest.read_text())['files']
            bad = [p for p, v in payloads.items() if not (ROOT/p).is_file()
                   or (ROOT/p).stat().st_size != v['bytes'] or sha(ROOT/p) != v['sha256']]
            result['checks'][identity] = {'payloads': len(payloads), 'mismatches': bad}
            if bad:
                raise RuntimeError(f'Historical/package artifact mutation: {bad}')
        protected = json.loads((ROOT/'working/G4B-E1-001/entry.json').read_text())['protected_hashes']
        bad = [p for p, expected in protected.items() if sha(ROOT/p) != expected]
        result['checks']['protected'] = {'count': len(protected), 'mismatches': bad}
        if len(protected) != 33 or bad:
            raise RuntimeError('Protected input mismatch')
        result['checks']['original_rf_sha256'] = sha(ROOT/'working/baseline_artifacts/rf_final.pkl')
        result['checks']['episode_manifest_sha256'] = sha(ROOT/'working/gate4_episode_manifest.json')
        sys.path.insert(0, str(PERF/'code'))
        import prepare_assets
        assets = prepare_assets.asset_bytes()  # Bytes only; no coordinator main or run creation.
        original = (ROOT/'working/G4C-E3-001/coordinator/execution_coordinator.py').read_bytes()
        optimized = assets['execution_coordinator.py']
        def definitions(source):
            return {n.name: ast.dump(n) for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
        before, after = definitions(original), definitions(optimized)
        changed = [n for n in before if before[n] != after.get(n)]
        if changed != ['preexisting_integrity'] or set(after)-set(before) != {'signature_hex'}:
            raise RuntimeError('Unexpected coordinator scientific/control-flow modification')
        result['checks']['coordinator_AST'] = {'changed_functions': changed,
            'added_functions': ['signature_hex'], 'main_metric_call_unchanged': True}
        identical = []
        for name in ['episode_worker.py', 'source_worker.py', 'preflight_worker.py',
                     'g4c_boundary.py', 'gate4_production_boundary.py', 'gate4_lifecycle.py']:
            if assets[name] != (ROOT/'working/G4C-E3-001/coordinator'/name).read_bytes():
                raise RuntimeError(f'Unexpected frozen worker/boundary change: {name}')
            identical.append(name)
        result['checks']['unchanged_assets'] = identical
        outcomes = []
        for name, code in [('original', original), ('optimized', optimized)]:
            module = types.ModuleType('certification_' + name)
            module.__file__ = str(ROOT/'working/G4C-E3-001/coordinator/execution_coordinator.py')
            exec(compile(code, module.__file__, 'exec'), module.__dict__)
            outcomes.append(module.preexisting_integrity())
        if outcomes[0] != outcomes[1]:
            raise RuntimeError('Paired integrity checks returned different results')
        result['checks']['complete_original_optimized_integrity_checks'] = 'PASS; identical results'
        result['checks']['prepared_assets'] = sorted(assets)
        # A production run must have a bound independent validator compatible with its
        # identity and output contract before any candidate prediction is authorized.
        validators = [n for n in assets if 'verif' in n.lower() or 'validat' in n.lower()]
        result['checks']['prepared_validator_assets'] = validators
        result['checks']['producer_output_contract'] = [
            'candidate_state/source_state.json', 'results/per_episode_results.json',
            'results/execution_summary.json', 'coordinator/*']
        legacy = ROOT/'working/verify_g4c_candidate.py'
        result['checks']['legacy_verifier'] = {
            'path': str(legacy.relative_to(ROOT)), 'sha256': sha(legacy),
            'fixed_identity': 'G4C-{method}-001',
            'expected_files': ['entry.json', 'source_state.json', 'per_episode_results.json',
                               'summary.json', 'parameters.json', 'code/*'],
            'compatible_with_prepared_output_contract': False}
        if not validators:
            raise RuntimeError('VALIDATION_BINDING_MISSING: optimized preparation emits no independent E3 validator. '
                               'Legacy verify_g4c_candidate.py targets the closed -001 identity and an incompatible '
                               'file/schema layout. No unchanged production verification path is bound to a new run.')
        raise RuntimeError('Certification script requires a reviewed validator contract before further stages')
    except Exception as exc:
        result['failures'].append({'type': type(exc).__name__, 'message': str(exc)})
    result['seconds'] = time.perf_counter()-started
    with (CERT/'certification.json').open('x', encoding='utf8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
