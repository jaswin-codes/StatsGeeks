"""Privileged coordinator: fixed manifest, one fresh sandbox per source/episode."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,json,pickle,hashlib,subprocess,time,datetime,traceback
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
MH='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def save(p,obj):
    with p.open('x',encoding='utf8') as f:json.dump(obj,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def readonly(p):subprocess.run(['attrib','+R',str(p.resolve())],check=True,capture_output=True)
def linux(p):
    s=pathlib.Path(p).resolve().as_posix();return '/mnt/'+s[0].lower()+s[2:]
def integrity():
    cp=json.loads((ROOT/'working/G4C-PROVENANCE-CHECKPOINT/input_artifact_hashes.json').read_text())
    failures=[p for p,v in cp.items() if sha(ROOT/p)!=v['sha256']]
    assert not failures,('Pre-existing input/code/evidence mutation',failures)
    assert sha(ROOT/'working/gate4_episode_manifest.json')==MH
    assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT)
    return cp
PARAMS={'E2':{'candidate':'E2','epsilon':1e-6,'clip':[.25,4.0],'identity_mixture':.5},'E3':{'candidate':'E3','translation_strength':1.0,'continuous_indices':list(range(58))},'E4':{'candidate':'E4','shrinkage':.1,'max_rank':3,'eigenvalue_relative_threshold':1e-10},'E5':{'candidate':'E5','trees':500,'embedding':'equal-weight leaf one-hot','distance':'squared centroid distance'}}
def metrics(y,p):
    cm=np.bincount(4*(y-1)+(p-1),minlength=16).reshape(4,4);tp=np.diag(cm);den=cm.sum(0)+cm.sum(1)
    f=np.divide(2*tp,den,out=np.zeros(4),where=den>0);pr=np.divide(tp,cm.sum(0),out=np.zeros(4),where=cm.sum(0)>0);re=np.divide(tp,cm.sum(1),out=np.zeros(4),where=cm.sum(1)>0)
    return {'macro_f1':float(f.mean()),'per_class_f1':f.tolist(),'precision':pr.tolist(),'recall':re.tolist(),'confusion':cm.tolist(),'accuracy':float(tp.sum()/cm.sum())}
def main(method):
    assert method in PARAMS
    run=ROOT/'working'/f'G4C-{method}-001';run.mkdir(exist_ok=False);(run/'evidence').mkdir();(run/'predictions').mkdir();(run/'code').mkdir()
    started=time.perf_counter()
    try:
        inputs=integrity();m=json.loads((ROOT/'working/gate4_episode_manifest.json').read_text());assert m['gate4a']=='PASS' and len(m['episodes'])==60
        params=PARAMS[method];save(run/'parameters.json',params)
        codefiles=['g4c_boundary.py','g4c_linux_call.py','g4c_source_worker.py','g4c_episode_worker.py','run_g4c_candidate.py','verify_g4c_candidate.py','gate4_lifecycle.py','gate4_production_boundary.py','gate4b_preflight_worker.py']
        codehash={}
        for name in codefiles:
            data=(ROOT/'working'/name).read_bytes();dest=run/'code'/name
            with dest.open('xb') as f:f.write(data)
            codehash[name]=hashlib.sha256(data).hexdigest()
        entry={'run_id':run.name,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dirty_state_authorized':True,'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'git_status':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),'parameters':params,'code_hashes':codehash,'manifest_sha256':MH,'source_rng':'No stochastic candidate fitting','sampler':'frozen 60-episode PCG64(42), budget-major advancing state','rng_start':m['episodes'][0]['rng_before'],'runtime':'working/G4C-PROVENANCE-CHECKPOINT/runtime_verification.json','resource_limits':{'address_space_gib':6,'cpu_seconds':180,'wall_timeout_seconds':180,'threads':1},'baseline_and_input_hashes_reference':'working/G4C-PROVENANCE-CHECKPOINT/input_artifact_hashes.json'};save(run/'entry.json',entry)
        with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:d=pickle.load(f)
        x,y,ids=d['X_amsterdam'],d['y_amsterdam'],d['pixel_ids_amsterdam'];xm,ym=d['X_madrid'],d['y_madrid']
        schema=json.loads((ROOT/'working/baseline_artifacts/feature_schema.json').read_text());assert schema['feature_names'][-2:]==['has_early_data','has_late_data']
        with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as a:
            rf=a['y_ams_pred_zero'].copy();assert np.array_equal(a['y_amsterdam'],y) and np.array_equal(a['pixel_ids_amsterdam'],ids)
        # Independent advancing sampler reconstruction before candidate packets.
        rng=np.random.default_rng(42)
        for i,e in enumerate(m['episodes']):
            assert (e['budget'],e['trial'])==([5,10,25,50,100,200][i//10],i%10+1)
            assert rng.bit_generator.state==e['rng_before']
            s=np.concatenate([rng.choice(np.flatnonzero(y==c),e['budget'],replace=False) for c in [1,2,3,4]])
            assert np.array_equal(s,e['support_row_indices']) and rng.bit_generator.state==e['rng_after']
        def call(packet,worker,role,label,with_rf=False):
            for name,h in codehash.items():assert sha(ROOT/'working'/name)==h
            tmp=run/'evidence'/f'{label}_input.json';save(tmp,packet);out=run/'evidence'/f'{label}.json'
            cmd=['wsl','-d','Ubuntu','--exec','/usr/bin/python3','-B',linux(ROOT/'working/g4c_linux_call.py'),linux(tmp),linux(ROOT/'working'/worker),role,linux(out)]
            if with_rf:cmd+=['--rf',linux(ROOT/'working/baseline_artifacts/rf_final.pkl')]
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
            save(run/'evidence'/f'{label}_transport.json',{'command':cmd,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'input_sha256':sha(tmp)})
            assert proc.returncode==0,(label,proc.stderr)
            z=json.loads(out.read_text());ev=z['boundary_evidence'];assert ev['teardown_pass'] and not ev['lifecycle']['final_survivors'] and ev['returncode']==0 and not ev['stderr']
            assert ev['packet_sha256']==hashlib.sha256(canon(packet)).hexdigest()
            readonly(out);tmp.unlink();return z
        e=m['episodes'][0];s=np.asarray(e['support_row_indices']);q=np.setdiff1d(np.arange(len(y)),s)
        probe={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'parameters':{'mode':'preflight'}}
        for n in [1,2]:
            z=call(probe,'gate4b_preflight_worker.py','preflight',f'preflight_{n}');assert z['result']['status']=='PASS'
        if method!='E5':
            z=call({'X_source':xm.tolist(),'y_source':ym.tolist(),'parameters':params},'g4c_source_worker.py','source','source_worker');state=z['result']['source_state'];assert z['result']['target_rows_received']==0
        else:state={'parameters':params,'rf_sha256':sha(ROOT/'working/baseline_artifacts/rf_final.pkl')}
        sh=hashlib.sha256(canon(state)).hexdigest();save(run/'source_state.json',{'source_state':state,'source_state_sha256':sh});readonly(run/'source_state.json')
        rows=[]
        episodes=list(m['episodes'])
        if method=='E4':episodes.append({'budget':0,'trial':0,'episode_id':'E4-zero-shot-all-target','support_row_indices':[]})
        for i,e in enumerate(episodes):
            assert sha(ROOT/'working/gate4_episode_manifest.json')==MH
            s=np.asarray(e['support_row_indices'],dtype=np.int64);q=np.setdiff1d(np.arange(len(y)),s,assume_unique=True)
            packet={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'source_state':state,'parameters':{'episode_id':e['episode_id'],'budget':e['budget'],'trial':e['trial'],'classes':[1,2,3,4],'candidate':method}}
            z=call(packet,'g4c_episode_worker.py','episode',f'worker_{i+1:02d}',method in ['E3','E5']);r=z['result']
            assert r['label_access']=={'source_state_only':True,'current_support_labels':len(s),'query_labels':0,'other_episode_labels':0}
            assert r['fresh_state_probe'] and r['source_state_sha256']==sh and r['query_fingerprint']==hashlib.sha256(canon(ids[q].tolist())).hexdigest()
            predictions={k:np.asarray(v,dtype=np.int64) for k,v in r['predictions'].items()};predictions['frozen_rf']=rf[q]
            if 'rf_reproduced' in predictions:assert np.array_equal(predictions['rf_reproduced'],rf[q]),'Frozen RF prediction reproduction failure'
            assert all(v.shape==(len(q),) and np.isin(v,[1,2,3,4]).all() for v in predictions.values())
            if method=='E2':
                with np.load(ROOT/'working/G4B-E1-001/predictions'/f"{e['episode_id']}.npz",allow_pickle=False) as a:
                    assert np.array_equal(q,a['query_indices']) and np.array_equal(ids[q],a['query_ids']);predictions['unsupervised_covariance']=a['unsupervised_covariance'].copy()
            path=run/'predictions'/f"{e['episode_id']}.npz"
            with path.open('xb') as f:np.savez_compressed(f,query_indices=q,query_ids=ids[q],**predictions)
            readonly(path)
            row={'episode_id':e['episode_id'],'budget':e['budget'],'trial':e['trial'],'prediction_artifact':path.relative_to(ROOT).as_posix(),'prediction_sha256':sha(path),'worker_evidence':f'evidence/worker_{i+1:02d}.json','worker_sha256':sha(run/'evidence'/f'worker_{i+1:02d}.json'),'worker_seconds':z['boundary_evidence']['elapsed_seconds'],'peak_rss_kib':r['peak_rss_kib'],'warnings':r['warnings'],'source_state_sha256':sh}
            rows.append(row);print(method,i+1,e['episode_id'],row['worker_seconds'],flush=True)
        # Post-candidate fresh state probe, before scoring feedback exists.
        z=call(probe,'gate4b_preflight_worker.py','preflight','post_candidate_probe');assert z['result']['status']=='PASS'
        for row in rows:
            with np.load(ROOT/row['prediction_artifact'],allow_pickle=False) as a:
                q=a['query_indices'];row['metrics']={k:metrics(y[q],a[k]) for k in a.files if k not in ['query_indices','query_ids']}
                score=row['metrics']['candidate']['macro_f1'];row['paired_deltas']={k:score-v['macro_f1'] for k,v in row['metrics'].items() if k!='candidate'}
                row['confusion_sha256']={k:hashlib.sha256(canon(v['confusion'])).hexdigest() for k,v in row['metrics'].items()}
        save(run/'per_episode_results.json',rows)
        summary={}
        for b in [5,10,25,50,100,200]+([0] if method=='E4' else []):
            group=[r for r in rows if r['budget']==b];summary[str(b)]={}
            for k in group[0]['metrics']:
                vals=np.asarray([r['metrics'][k]['macro_f1'] for r in group]);pc=np.asarray([r['metrics'][k]['per_class_f1'] for r in group]);summary[str(b)][k]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'per_class_mean':pc.mean(0).tolist(),'values':vals.tolist()}
            for k in group[0]['paired_deltas']:
                vals=np.asarray([r['paired_deltas'][k] for r in group]);summary[str(b)]['delta_'+k]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'positive_trials':int((vals>0).sum()),'values':vals.tolist()}
        p=summary['25'];reg=np.asarray(p['candidate']['per_class_mean'])-p['raw_prototype']['per_class_mean'];criteria={'mean_gain_raw_ge_0.0100':p['delta_raw_prototype']['mean']>=.01,'positive_raw_trials_ge_8':p['delta_raw_prototype']['positive_trials']>=8,'per_class_regression_ge_minus_0.0200':bool(np.all(reg>=-.02)),'positive_same_query_rf_gain':p['delta_frozen_rf']['mean']>0}
        status='PROMISING' if all(criteria.values()) else ('FALSIFIED' if p['delta_raw_prototype']['mean']<=0 or np.any(reg<-.02) else 'INCONCLUSIVE')
        extra={}
        if method=='E3':extra['translation_success_vs_rf']={'gain_ge_0.0100':p['delta_frozen_rf']['mean']>=.01,'per_class_safeguard':bool(np.all(np.asarray(p['candidate']['per_class_mean'])-p['frozen_rf']['per_class_mean']>=-.02))}
        if method=='E4':
            zero=summary['0'];cr={'gain_ge_0.0100':zero['delta_frozen_rf']['mean']>=.01,'per_class_safeguard':bool(np.all(np.asarray(zero['candidate']['per_class_mean'])-zero['frozen_rf']['per_class_mean']>=-.02))};extra['zero_shot_criteria']=cr;extra['zero_shot_status']='PROMISING' if all(cr.values()) else 'FALSIFIED'
        integrity()
        result={'run_id':run.name,'candidate':method,'execution_status':'COMPLETED_PENDING_INDEPENDENT_VERIFICATION','verdict':status,'episodes_completed':60,'zero_shot_records':int(method=='E4'),'parameters':params,'summary':summary,'success_criteria':criteria,'primary_per_class_delta':reg.tolist(),'source_state_sha256':sh,'runtime_wall_seconds':time.perf_counter()-started,'peak_worker_rss_kib':max(r['peak_rss_kib'] for r in rows),'warnings':[{'episode':r['episode_id'],'warnings':r['warnings']} for r in rows if r['warnings']],'extra_criteria':extra,'dirty_start_authorized':True,'notebook4_rerun':False}
        save(run/'summary.json',result);print(json.dumps({'candidate':method,'status':status,'primary':p['candidate'],'criteria':criteria}),flush=True)
    except BaseException:
        text=traceback.format_exc()
        with (run/'STOP_REASON.md').open('x') as f:f.write('# STOP — entire G4C suite\n\nNo retry or repair authorized.\n\n```\n'+text+'\n```\n')
        raise
if __name__=='__main__':main(sys.argv[1])
