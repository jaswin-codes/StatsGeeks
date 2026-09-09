"""Independent evaluator-only manifest/identity/evidence verifier; no model/scoring.
Does NOT import the manifest builder, sampler, runner or any candidate function.
"""
import argparse
import hashlib
import json
from pathlib import Path
import pickle
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'working/gate4_episode_manifest.json'


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def ah(a):
    a=np.ascontiguousarray(a)
    h=hashlib.sha256(json.dumps([a.dtype.str,list(a.shape)],sort_keys=True,separators=(',',':')).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expect-hash',required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--require-readonly',action='store_true')
    args=parser.parse_args()
    assert not args.output.exists()
    assert sha(PATH)==args.expect_hash
    m=json.loads(PATH.read_text())
    assert m['artifact_type']=='gate4a_certified_evaluator_only_episode_manifest' and m['gate4a']=='PASS'
    assert m['candidate_execution_authorized'] is False
    assert 'EVALUATOR ONLY' in m['access']
    assert m['target_shape']==[25992,60] and m['source_shape']==[76263,60]
    pins=json.loads((ROOT/'working/gate4_dependency_repair_entry.json').read_text())['protected_input_hashes']
    assert m['baseline_protected_sha256']==pins
    for p,h in pins.items():
        assert sha(ROOT/p)==h,p
    for p,h in m['evidence_sha256'].items():
        assert sha(ROOT/p)==h,p
    assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT)
    assert not subprocess.check_output(['git','diff','--','original/'],cwd=ROOT)
    assert (ROOT/'original/Open Notebook.onetoc2').stat().st_file_attributes & 1
    old=json.loads((ROOT/'working/gate4_episode_manifest_validation.json').read_text())
    assert len(m['episodes'])==60 and m['ordered_schema_sha256']==old['ordered_schema_sha256']
    sys.path.insert(0,str(ROOT))
    with (ROOT/'data/preprocessed/preprocessed_data.pkl').open('rb') as f:
        data=pickle.load(f)
    x,y,ids=data['X_amsterdam'],data['y_amsterdam'],data['pixel_ids_amsterdam']
    assert m['feature_names']==data['feature_names']
    assert hashlib.sha256(json.dumps(m['feature_names'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==m['ordered_schema_sha256']
    rng=np.random.Generator(np.random.PCG64(42))
    pools=[np.flatnonzero(y==c) for c in (1,2,3,4)]
    universe=np.arange(25992,dtype=np.int64)
    episode=0
    for budget in [5,10,25,50,100,200]:
        for trial in range(1,11):
            e=m['episodes'][episode];ref=old['episodes_diagnostic_fingerprints'][episode]
            assert e['episode_id']==f'G4A-B{budget:03d}-T{trial:02d}'
            assert (e['budget'],e['trial'])==(budget,trial)
            assert rng.bit_generator.state==e['rng_before']==ref['rng_before']
            s=np.concatenate([rng.choice(pool,size=budget,replace=False) for pool in pools])
            q=np.setdiff1d(universe,s,assume_unique=True)
            assert rng.bit_generator.state==e['rng_after']==ref['rng_after']
            replay=np.random.Generator(np.random.PCG64())
            replay.bit_generator.state=e['rng_before']
            s2=np.concatenate([replay.choice(pool,size=budget,replace=False) for pool in pools])
            assert np.array_equal(s,s2) and replay.bit_generator.state==e['rng_after']
            assert np.array_equal(s,np.array(e['support_row_indices'],dtype=np.int64))
            assert np.array_equal(ids[s],np.array(e['support_pixel_ids']))
            assert np.unique(s).size==len(s)==4*budget and len(q)==25992-4*budget
            assert e['support_count']==len(s) and e['query_count']==len(q)
            assert np.intersect1d(s,q).size==0 and np.array_equal(np.sort(np.r_[s,q]),universe)
            assert np.array_equal(y[s],np.repeat([1,2,3,4],budget))
            for field,value in [('support_row_indices_sha256',s),('query_row_indices_sha256',q),('support_pixel_ids_sha256',ids[s]),('query_pixel_ids_sha256',ids[q])]:
                assert ah(value)==e[field]==ref[field]
            assert ah(x[s])==e['X_support_sha256'] and ah(x[q])==e['X_query_sha256']
            assert not {'y_query','y_target','y_amsterdam','query_labels','support_labels','query_class_counts'} & set(e)
            episode+=1
    # Verify actual contemporaneous state/reaping evidence, not just PASS summaries.
    counts={'normal':0,'abnormal':0,'waitpid_reaped':0}
    for suite in ['certification_v2','independent_repeat']:
        base=ROOT/'working/G4A-TEARDOWN-002'/suite/'suite_001'
        summary=json.loads((base/'summary.json').read_text())
        assert summary['status']=='PASS' and all(summary['output_negative_tests'].values())
        previous_start=None
        packets=[]
        for i in range(1,8):
            p=base/f'probe_{i}.json';assert sha(p)==summary['evidence_hashes'][p.name]
            ev=json.loads(p.read_text());life=ev['lifecycle']
            assert ev['status']=='PASS' and ev['teardown_pass'] and life['pass_']
            assert life['subreaper_enabled'] and not life['final_survivors'] and not ev['namespace_survivors']
            events=life['events'];assert events[-1]['kind']=='teardown_complete'
            if previous_start is not None:
                assert (events[-1]['wall_time_ns']-previous_start)/1e9 < 300, 'Canary may have expired between probes'
            previous_start=events[0]['wall_time_ns']
            assert life['reaped']
            for r in life['reaped']:
                zs=[e for e in events if e['kind']=='observation' and e['pid']==r['pid'] and e['process'] and e['process']['state']=='Z']
                assert zs and any(z['process']['ppid']==life['owner_pid'] for z in zs)
                reaps=[e for e in events if e['kind']=='waitpid_reaped' and e['pid']==r['pid'] and e['start_ticks']==r['start_ticks']]
                assert len(reaps)==1 and reaps[0]['monotonic_seconds']>=zs[0]['monotonic_seconds']
                assert events[-1]['monotonic_seconds']-next(e['monotonic_seconds'] for e in events if e['kind']=='launcher_wait_completed') <= life['deadline_seconds']+1
                counts['waitpid_reaped']+=1
            if ev['interrupted']:
                assert ev['returncode']!=0 and ev['reason']=='controlled_interrupt' and ev['stdout_bytes']==0
                assert ev['stderr']=='GATE4_PROBE_READY\n'
                counts['abnormal']+=1
            else:
                assert ev['returncode']==0 and ev['reason'] is None and not ev['stderr']
                counts['normal']+=1
            if i>=5:
                packets.append(ev['packet_sha256'])
        assert len(set(packets))==1
    assert counts['normal']==12 and counts['abnormal']==2
    readonly=bool(PATH.stat().st_file_attributes & 1)
    if args.require_readonly:
        assert readonly
    assert sha(PATH)==args.expect_hash
    result={'status':'PASS','manifest_sha256':sha(PATH),'independent_ordered_reconstruction':60,
            'exact_per_episode_rng_replays':60,'protected_hashes_verified':33,'original_clean':True,
            'readonly':readonly,'teardown_checks':counts,'matched_routing':'PASS','label_fields_absent':True,
            'candidate_modelling':False,'notebook4_rerun':False,'verifier_sha256':sha(__file__)}
    with args.output.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
