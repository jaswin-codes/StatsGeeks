"""Linux trusted probe orchestrator; output evidence never fed back into a worker."""
import argparse
import json
from pathlib import Path
import sys
import traceback
from gate4_production_boundary import run, sanitize, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--interrupt', action='store_true')
    args = parser.parse_args()
    assert not args.output.exists()
    packet = json.loads(args.packet.read_text())
    code_path = Path(__file__).with_name('gate4_production_probe.py')
    code = code_path.read_bytes()
    raw, evidence = run(packet, code, timeout=60, interrupt_after=8 if args.interrupt else None)
    evidence.update(artifact_type='real_episode_infrastructure_probe_not_predictions', candidate_modelling=False,
                    code_file_sha256=sha(code_path), boundary_sha256=sha(Path(__file__).with_name('gate4_production_boundary.py')),
                    forbidden_target_labels_supplied=False)
    if args.interrupt:
        passed = evidence['reason'] == 'controlled_interrupt' and evidence['returncode'] != 0 and not raw and not evidence['stderr']
    else:
        try:
            pred = sanitize(raw, packet)
            passed = evidence['returncode'] == 0 and not evidence['stderr'] and set(pred) == {1}
        except Exception as error:
            evidence['validation_error'] = repr(error)
            passed = False
    evidence['status'] = 'PASS' if passed and evidence['teardown_pass'] else 'BLOCKED'
    with args.output.open('x') as f:
        json.dump(evidence, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(evidence, indent=2))
    sys.exit(0 if evidence['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
