"""Privileged Gate4A evidence certification and exclusive evaluator manifest creation.
No notebook/model execution, fitting, inference, or scoring. Windows approved host.
"""
import datetime
import hashlib
import json
from pathlib import Path
import pickle
import subprocess
import sys
import numpy as np
from verify_gate4a_episodes import generate, array_hash, canonical, sha, packet_hashes

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'working/G4A-TEARDOWN-002'
MANIFEST = ROOT / 'working/gate4_episode_manifest.json'


def integrity():
    pins = json.loads((ROOT/'working/gate4_dependency_repair_entry.json').read_text())['protected_input_hashes']
    for p, h in pins.items():
        assert sha(ROOT/p) == h, ('STOP protected mutation', p)
    assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT)
    assert not subprocess.check_output(['git','diff','--','original/'],cwd=ROOT)
    assert (ROOT/'original/Open Notebook.onetoc2').stat().st_file_attributes & 1
    return pins


def main():
    assert not MANIFEST.exists(), 'Never overwrite existing manifest'
    pins = integrity()
    old = json.loads((ROOT/'working/gate4_episode_manifest_validation.json').read_text())
    replay_path = ROOT/'working/gate4_teardown_sampler_002.json'
    replay = json.loads(replay_path.read_text())
    for k in ['episodes_diagnostic_fingerprints','budgets','trials','seed','rng','rng_policy','ordered_schema_sha256','sampler_source_cell_sha256']:
        assert old[k] == replay[k], k
    rtpath = ROOT/'working/gate4_teardown_runtime_rebuild_002.json'
    runtime = json.loads(rtpath.read_text())
    assert runtime['independent_full_tree_rebuild'] == 'PASS' and runtime['files'] == 4355
    lockpath = ROOT/'working/gate4_runtime_narwhals_lock.json'
    assert sha(lockpath) == runtime['runtime_lock_sha256']
    evidence = {p.relative_to(ROOT).as_posix():sha(p) for p in [rtpath,replay_path,lockpath]}
    allruns = []
    for suite in ['certification_v2','independent_repeat']:
        path = RUN/suite/'suite_001/summary.json'
        summary = json.loads(path.read_text())
        assert summary['status'] == 'PASS' and summary['production_real_episode_probes'] == 7
        assert summary['matched_three_consumer_transport'] and not summary['comparator_models_executed']
        assert all(summary['output_negative_tests'].values())
        evidence[path.relative_to(ROOT).as_posix()] = sha(path)
        for name, h in summary['code_hashes'].items():
            assert sha(ROOT/'working'/name) == h
            evidence['working/'+name] = h
        for name, h in summary['evidence_hashes'].items():
            p = path.parent/name
            assert sha(p) == h
            evidence[p.relative_to(ROOT).as_posix()] = h
            ev = json.loads(p.read_text()); life = ev['lifecycle']
            assert ev['status'] == 'PASS' and ev['teardown_pass'] and life['pass_']
            assert life['subreaper_enabled'] and not life['final_survivors'] and not ev['namespace_survivors']
            assert life['reaped'], 'Each fork test must include contemporaneous adoption/reaping'
            for reaped in life['reaped']:
                assert str(reaped['pid']) in life['known_identities']
                assert life['known_identities'][str(reaped['pid'])] == reaped['start_ticks']
                assert any(e['kind']=='waitpid_reaped' and e['pid']==reaped['pid'] for e in life['events'])
                assert any(e['kind']=='observation' and e['pid']==reaped['pid'] and e['process'] is not None and e['process']['state']=='Z' and e['process']['ppid']==life['owner_pid'] for e in life['events'])
            if ev['interrupted']:
                assert ev['reason']=='controlled_interrupt' and ev['returncode'] != 0
                assert ev['stderr']=='GATE4_PROBE_READY\n' and ev['stdout_bytes']==0
            else:
                assert ev['returncode']==0 and not ev['stderr'] and ev['reason'] is None
            allruns.append(ev)
    sys.path.insert(0,str(ROOT))
    with (ROOT/'data/preprocessed/preprocessed_data.pkl').open('rb') as f:
        data = pickle.load(f)
    x,y,ids = data['X_amsterdam'],data['y_amsterdam'],data['pixel_ids_amsterdam']
    episodes = generate(y)
    assert len(episodes)==60
    # Independently confirm persisted production packets contain exactly allowed
    # source data and selected current-episode labels, and no extra references.
    packet_validation = []
    for i,name in enumerate(['current_packet.json','second_packet.json']):
        p = ROOT/'working/G4A-PRODUCTION-001'/name
        packet = json.loads(p.read_text()); e=episodes[i];s,q=e['support'],e['query']
        expected={'X_source':data['X_madrid'].tolist(),'y_source':data['y_madrid'].tolist(),
                  'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),
                  'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'parameters':{'teardown_child':True}}
        assert packet == expected
        for ev in allruns:
            if ev['episode_index'] == i:
                packet['parameters']={'teardown_child':True,'interrupt':ev['interrupted']}
                assert hashlib.sha256(canonical(packet)).hexdigest()==ev['packet_sha256']
        packet_validation.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'episode_index':i,'exact_allowed_content':True})
    details=[]
    for e, ref in zip(episodes,replay['episodes_diagnostic_fingerprints']):
        s,q=e['support'],e['query']
        assert array_hash(s)==ref['support_row_indices_sha256']
        assert array_hash(q)==ref['query_row_indices_sha256']
        assert array_hash(ids[s])==ref['support_pixel_ids_sha256']
        assert array_hash(ids[q])==ref['query_pixel_ids_sha256']
        assert e['rng_before']==ref['rng_before'] and e['rng_after']==ref['rng_after']
        assert not np.intersect1d(s,q).size
        d={k:ref[k] for k in ['budget','trial','support_count','query_count','support_row_indices_sha256','query_row_indices_sha256','support_pixel_ids_sha256','query_pixel_ids_sha256','rng_before','rng_after']}
        d.update(episode_id=f"G4A-B{e['budget']:03d}-T{e['trial']:02d}",
                 support_row_indices=s.tolist(),support_pixel_ids=ids[s].tolist(),
                 support_query_disjoint=True,exact_rng_replay=True,
                 X_support_sha256=array_hash(x[s]),X_query_sha256=array_hash(x[q]))
        details.append(d)
    for name in ['certify_gate4_manifest.py','independently_verify_gate4_manifest.py']:
        evidence['working/'+name]=sha(ROOT/'working'/name)
    verdict=dict(status='PASS',run_id='G4A-TEARDOWN-002',candidate_modelling=False,notebook4_rerun=False,
                 checks={k:'PASS' for k in ['runtime','real_episode_transport','query_label_isolation','cross_episode_isolation','fresh_state','prediction_finalisation','normal_teardown','abnormal_teardown','sixty_episode_replay','matched_comparator_routing','protected_33','original_clean']},
                 production_packets=packet_validation,evidence_sha256=evidence,
                 historical_pid_limit='Historical PIDs432/434 had no state/start records. New reproduction shows asynchronous namespace teardown; new adopted init zombies are explicitly reaped.',
                 label_scope='Privileged sampler/evaluator holds full target labels; worker only source labels and current-episode selected support labels. No query labels transported. No scoring occurred.',
                 kernel_trust='Trusted WSL/Linux kernel and host controller; unprivileged isolated code, fixed audited probe. No claim against malicious host/kernel.',
                 expiry_control='Keyring canary lasts 300s; sequential episode intervals in lifecycle timestamps must remain below this.')
    with (RUN/'pre_manifest_validation.json').open('x') as f:
        json.dump(verdict,f,indent=2,sort_keys=True);f.write('\n')
    evidence[(RUN/'pre_manifest_validation.json').relative_to(ROOT).as_posix()]=sha(RUN/'pre_manifest_validation.json')
    manifest=dict(artifact_type='gate4a_certified_evaluator_only_episode_manifest',version=1,gate4a='PASS',
                  run_id='G4A-TEARDOWN-002',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  access='EVALUATOR ONLY: full ordered support lists implicitly encode cross-episode labels. Never mount or serialize this manifest to workers.',
                  candidate_visible_inputs=sorted(['X_source','y_source','X_support','y_support','support_ids','X_query','query_ids','parameters']),
                  candidate_execution_authorized=False,notebook4_rerun=False,
                  sampler=dict(seed=42,bit_generator='PCG64',numpy='2.4.6',policy=replay['rng_policy'],
                               budgets=replay['budgets'],trials=replay['trials'],classes=[1,2,3,4],
                               support_order='sampled order retained within ascending class blocks',
                               query_order='ascending original rows, exact complement of current supports',
                               source_cell_sha256=replay['sampler_source_cell_sha256']),
                  hash_encoding=replay['hash_encoding'],input_sha256=pins['data/preprocessed/preprocessed_data.pkl'],
                  feature_names=data['feature_names'],ordered_schema_sha256=replay['ordered_schema_sha256'],
                  target_shape=list(x.shape),source_shape=list(data['X_madrid'].shape),
                  runtime_lock_sha256=sha(lockpath),evidence_sha256=evidence,baseline_protected_sha256=pins,
                  git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  git_dirty_state=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
                  git_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=ROOT)).hexdigest(),
                  episodes=details)
    integrity()
    with MANIFEST.open('x',encoding='utf-8') as f:
        json.dump(manifest,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'manifest_created':str(MANIFEST),'sha256':sha(MANIFEST),'independent_verification_and_freeze_pending':True}))


if __name__=='__main__':
    main()
