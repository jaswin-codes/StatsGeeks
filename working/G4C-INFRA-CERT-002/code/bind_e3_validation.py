"""Binding/report-inventory operations only. Never launches a coordinator/worker.

Use `bind RUN_DIR` AFTER the unchanged optimized preparation and BEFORE execution.
Use `seal-report RUN_DIR` AFTER complete primary output and BEFORE independent
validation. All writes are exclusive; historical/closed identities are rejected.
"""
import argparse
import json
from pathlib import Path
import re
import sys

from e3_validator import MH, RFH, require, sha, load, report_text, local_path

HERE = Path(__file__).resolve().parent


def bind_e3_validation(run_dir):
    run = Path(run_dir).absolute()
    require(run.resolve() == run and not run.is_symlink(), 'Noncanonical target')
    require(re.fullmatch(r'G4C-E3-\d{3}', run.name) and run.parent.name == 'working', 'Invalid E3 target')
    require(run.is_dir(), 'Prepare a separately authorized new run first')
    require(not (run/'artifact_hash_manifest.json').exists(), 'Historical/finalized run forbidden')
    require(not (run/'checkpoint/execution_authorization.json').exists(), 'Bind before execution; never retrofit historical runs')
    prep_path = run/'checkpoint/infrastructure_preparation.json'
    prep = load(prep_path)
    auth = prep['authorization']
    require(auth['run_id'] == run.name and auth['candidate'] == 'E3' and auth['scope'] == 'execution', 'Wrong approval')
    root = run.parent.parent
    manifest = root/'working/gate4_episode_manifest.json'
    require(sha(manifest) == MH and sha(root/'working/baseline_artifacts/rf_final.pkl') == RFH, 'Frozen anchors changed')
    for name, expected in prep['code_hashes'].items():
        require(sha(local_path(run, 'coordinator/'+name)) == expected, 'Prepared code changed')
    validator = HERE/'e3_validator.py'
    record = {'binding_version': 1, 'run_id': run.name, 'candidate': 'E3',
              'manifest_sha256': MH, 'rf_sha256': RFH, 'validator_sha256': sha(validator),
              'preparation_sha256': sha(prep_path),
              'paths': {'manifest': 'checkpoint/episode_manifest.json', 'state': 'candidate_state/source_state.json',
                        'rows': 'results/per_episode_results.json', 'summary': 'results/execution_summary.json',
                        'report': 'EXECUTION_REPORT.md', 'inventory': 'artifact_hash_manifest.json'},
              'historical_output_fallback': False, 'validation_command': ['e3_validator.py', run.name]}
    destinations = [run/'coordinator/e3_validator.py', run/'checkpoint/episode_manifest.json', run/'checkpoint/validation_binding.json']
    require(not any(p.exists() for p in destinations), 'Binding already exists; no overwrite')
    for path, data in zip(destinations, [validator.read_bytes(), manifest.read_bytes(), (json.dumps(record,indent=2)+'\n').encode()]):
        with path.open('xb') as stream:
            stream.write(data)
    return record


def seal_report(run_dir):
    run = Path(run_dir).absolute()
    from e3_validator import validate_layout
    validate_layout(run)
    summary = load(local_path(run, 'results/execution_summary.json'))
    require(summary['run_id'] == run.name and summary['episodes_completed'] == 60 and
            summary['execution_status'] == 'COMPLETED_PENDING_INDEPENDENT_VERIFICATION', 'Incomplete/wrong primary output')
    report = run/'EXECUTION_REPORT.md'
    require(not report.exists() and not (run/'artifact_hash_manifest.json').exists(), 'Already sealed; no overwrite')
    with report.open('x',encoding='utf8',newline='\n') as stream:
        stream.write(report_text(summary))
    files = {}
    for path in sorted(run.rglob('*')):
        if path.is_file():
            require(not path.is_symlink(), 'Symlink payload forbidden')
            files[path.relative_to(run).as_posix()] = {'bytes': path.stat().st_size, 'sha256': sha(path)}
    manifest = {'run_id': run.name, 'candidate': 'E3', 'status': 'PENDING_INDEPENDENT_VALIDATION',
                'files': files, 'excludes_self': True}
    with (run/'artifact_hash_manifest.json').open('x',encoding='utf8') as stream:
        json.dump(manifest,stream,indent=2);stream.write('\n')
    return {'status': 'SEALED_PENDING_VALIDATION', 'run_id': run.name, 'files': len(files)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['bind','seal-report'])
    parser.add_argument('run_dir', type=Path)
    args = parser.parse_args()
    print(json.dumps((bind_e3_validation if args.operation == 'bind' else seal_report)(args.run_dir),indent=2))
