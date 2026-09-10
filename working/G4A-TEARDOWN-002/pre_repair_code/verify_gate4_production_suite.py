"""Sequential real-packet certification probes; no model implementation/scoring."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from gate4_production_boundary import canonical, run, sanitize, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    out = args.directory / 'suite_001'
    out.mkdir()
    paths = [args.directory / 'current_packet.json', args.directory / 'second_packet.json']
    packets = [json.loads(p.read_text()) for p in paths]
    code_path = Path(__file__).with_name('gate4_production_probe.py')
    code = code_path.read_bytes()
    runs = []
    for i, (index, interrupt) in enumerate([(0, False), (1, False), (0, True), (1, False)]):
        p = dict(packets[index])
        p['parameters'] = {'teardown_child': True, 'interrupt': interrupt}
        raw, ev = run(p, code, timeout=60, interrupt_after=8 if interrupt else None)
        if interrupt:
            passed = ev['reason'] == 'controlled_interrupt' and ev['returncode'] != 0 and not raw and ev['stderr'] == 'GATE4_PROBE_READY\n'
        else:
            try:
                passed = ev['returncode'] == 0 and not ev['stderr'] and set(sanitize(raw, p)) == {1}
            except Exception as e:
                ev['validation_error'] = repr(e)
                passed = False
        ev.update(status='PASS' if passed and ev['teardown_pass'] else 'BLOCKED', episode_index=index,
                  interrupted=interrupt, candidate_modelling=False)
        with (out / f'probe_{i+1}.json').open('x') as f:
            json.dump(ev, f, indent=2, sort_keys=True)
        runs.append(ev)
        if ev['status'] != 'PASS':
            print(json.dumps(ev, indent=2))
            sys.exit(1)
    p = packets[0]
    fingerprint = hashlib.sha256(canonical(p['query_ids'])).hexdigest()
    good = dict(query_fingerprint=fingerprint, predictions=[1]*len(p['query_ids']))
    rejected = {}
    cases = {
        'hidden_labels':dict(good, y_query=[4]), 'label_request':{'request':'y_query'},
        'extra_episode':dict(good, other_episode={}), 'invalid_class':dict(good, predictions=[0]*len(p['query_ids'])),
        'boolean':dict(good, predictions=[True]*len(p['query_ids'])), 'short':dict(good, predictions=[1]),
        'duplicate_or_reordered_ids':dict(good, query_fingerprint='0'*64), 'path':dict(good, path='/tmp/result'),
    }
    for name, value in cases.items():
        try:
            sanitize(canonical(value), p)
            rejected[name] = False
        except ValueError:
            rejected[name] = True
    assert all(rejected.values())
    assert sanitize(canonical(good), p) == tuple(good['predictions'])
    result = dict(status='PASS', production_real_episode_probes=4, two_distinct_episode_packets=True,
                  normal_and_detached_child_teardown=True, abnormal_ready_marker_before_termination=True,
                  post_abnormal_fresh_state=True, output_negative_tests=rejected, candidate_modelling=False,
                  code_hashes={q.name:sha(q) for q in [Path(__file__),code_path,Path(__file__).with_name('gate4_production_boundary.py')]},
                  evidence_hashes={q.name:sha(q) for q in sorted(out.glob('probe_*.json'))})
    with (out / 'summary.json').open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
