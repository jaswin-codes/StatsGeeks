"""Sequential real-packet certification probes; no model implementation/scoring."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from gate4_production_boundary import canonical, run, sanitize, sha, finalize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--packet-directory', type=Path)
    args = parser.parse_args()
    out = args.directory / 'suite_001'
    out.mkdir()
    packet_directory = args.packet_directory or args.directory
    paths = [packet_directory / 'current_packet.json', packet_directory / 'second_packet.json']
    packets = [json.loads(p.read_text()) for p in paths]
    code_path = Path(__file__).with_name('gate4_production_probe.py')
    code = code_path.read_bytes()
    runs = []
    sequence = [(0, False), (1, False), (0, True), (1, False)] + [(0, False)] * 3
    for i, (index, interrupt) in enumerate(sequence):
        p = dict(packets[index])
        p['parameters'] = {'teardown_child': True, 'interrupt': interrupt}
        try:
            raw, ev = run(p, code, timeout=60, interrupt_after=8 if interrupt else None)
        except Exception as error:
            with (out / f'probe_{i+1}_failure.json').open('x') as f:
                json.dump({'status':'BLOCKED','error':repr(error),'candidate_modelling':False}, f, indent=2)
            raise
        if interrupt:
            passed = ev['reason'] == 'controlled_interrupt' and ev['returncode'] != 0 and not raw and ev['stderr'] == 'GATE4_PROBE_READY\n'
        else:
            try:
                passed = ev['returncode'] == 0 and not ev['stderr'] and set(finalize(raw, p, ev)) == {1}
            except Exception as e:
                ev['validation_error'] = repr(e)
                passed = False
        ev.update(status='PASS' if passed and ev['teardown_pass'] else 'BLOCKED', episode_index=index,
                  interrupted=interrupt, candidate_modelling=False,
                  routing_role=['raw_prototype','frozen_rf','future_E1'][i-4] if i >= 4 else 'isolation_probe')
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
    for name, raw in [('invalid_json', b'{'), ('duplicate_field', b'{"predictions":[],"predictions":[]}'), ('nonfinite', b'{"query_fingerprint":"x","predictions":[NaN]}')]:
        try:
            sanitize(raw, p)
            rejected[name] = False
        except ValueError:
            rejected[name] = True
    for name, ev in [('worker_failure',dict(returncode=1,reason=None,teardown_pass=True)),
                     ('unreaped',dict(returncode=0,reason=None,teardown_pass=False)),
                     ('interrupted',dict(returncode=0,reason='controlled_interrupt',teardown_pass=True))]:
        try:
            finalize(canonical(good), p, ev)
            rejected[name] = False
        except ValueError:
            rejected[name] = True
    for name, field, value in [('extra_label','y_query',[1]), ('extra_episode_packet','other_episode',{})]:
        bad = dict(p, **{field:value})
        try:
            run(bad, code)
            rejected[name] = False
        except ValueError:
            rejected[name] = True
    assert all(rejected.values())
    assert sanitize(canonical(good), p) == tuple(good['predictions'])
    assert len({ev['packet_sha256'] for ev in runs[4:]}) == 1
    assert len({ev['stdout_sha256'] for ev in runs[4:]}) == 1
    assert runs[4]['packet_sha256'] == runs[0]['packet_sha256']
    result = dict(status='PASS', production_real_episode_probes=len(runs), two_distinct_episode_packets=True,
                  matched_three_consumer_transport=True, comparator_models_executed=False,
                  normal_and_detached_child_teardown=True, abnormal_ready_marker_before_termination=True,
                  post_abnormal_fresh_state=True, output_negative_tests=rejected, candidate_modelling=False,
                  code_hashes={q.name:sha(q) for q in [Path(__file__),code_path,Path(__file__).with_name('gate4_production_boundary.py'),Path(__file__).with_name('gate4_lifecycle.py')]},
                  evidence_hashes={q.name:sha(q) for q in sorted(out.glob('probe_*.json'))})
    with (out / 'summary.json').open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
