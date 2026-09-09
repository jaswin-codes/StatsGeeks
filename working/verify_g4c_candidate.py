"""Separate privileged verifier; no primary coordinator/candidate imports."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,pathlib,pickle,json,hashlib,subprocess,warnings
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def near(q,centers):
    return np.argmin(np.stack([np.sum((q-c)**2,axis=1) for c in centers],axis=1),axis=1)+1
def score(y,p):
    cm=np.zeros((4,4),dtype=np.int64)
    np.add.at(cm,(y-1,p-1),1)
    tp=cm.diagonal();den=cm.sum(0)+cm.sum(1);f=np.divide(2*tp,den,out=np.zeros(4),where=den>0)
    return {'macro_f1':float(f.mean()),'per_class_f1':f.tolist(),'precision':np.divide(tp,cm.sum(0),out=np.zeros(4),where=cm.sum(0)>0).tolist(),'recall':np.divide(tp,cm.sum(1),out=np.zeros(4),where=cm.sum(1)>0).tolist(),'accuracy':float(tp.sum()/cm.sum()),'confusion':cm.tolist()}
def main(method):
    run=ROOT/'working'/f'G4C-{method}-001';assert not (run/'independent_verification.json').exists()
    entry=json.loads((run/'entry.json').read_text());saved=json.loads((run/'source_state.json').read_text());state=saved['source_state'];rows=json.loads((run/'per_episode_results.json').read_text());summary=json.loads((run/'summary.json').read_text());params=json.loads((run/'parameters.json').read_text())
    assert params==entry['parameters']==state['parameters']==summary['parameters']
    for name,h in entry['code_hashes'].items():assert sha(run/'code'/name)==sha(ROOT/'working'/name)==h
    assert sha(ROOT/'working/gate4_episode_manifest.json')=='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
    m=json.loads((ROOT/'working/gate4_episode_manifest.json').read_text());assert m['gate4a']=='PASS'
    with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:data=pickle.load(f)
    X,Y,x,y,ids=data['X_madrid'],data['y_madrid'],data['X_amsterdam'],data['y_amsterdam'],data['pixel_ids_amsterdam']
    active=np.flatnonzero(X.var(0)>0);means=np.stack([X[Y==c].mean(0) for c in [1,2,3,4]])
    if method!='E5':assert active.tolist()==state['active_indices'] and np.allclose(means,state['source_means'],rtol=1e-10,atol=1e-12)
    sh=hashlib.sha256(canon(state)).hexdigest();assert sh==saved['source_state_sha256']==summary['source_state_sha256']
    if method=='E2':
        assert params=={'candidate':'E2','epsilon':1e-6,'clip':[.25,4.0],'identity_mixture':.5}
        mu=means[:,active];between=np.mean((mu-mu.mean(0))**2,0);within=np.mean([np.var(X[Y==c][:,active],axis=0,ddof=0) for c in [1,2,3,4]],axis=0)
        ratios=between/(within+1e-6);clipped=np.clip(ratios/ratios.mean(),.25,4);weights=.5+.5*clipped/clipped.mean();assert np.allclose(weights,state['weights'],rtol=1e-10,atol=1e-12)
        z=X[:,active];centered=z-z.mean(0);cov=centered.T@centered/len(z);reg=.9*cov+.1*np.trace(cov)/59*np.eye(59);e,v=np.linalg.eigh(reg);u0=(v*(1/e))@v.T
    elif method=='E4':
        assert params=={'candidate':'E4','shrinkage':.1,'max_rank':3,'eigenvalue_relative_threshold':1e-10}
        z=X[:,active];mu=means[:,active];grand=mu.mean(0);W=np.zeros((59,59))
        for c in [1,2,3,4]:
            a=z[Y==c];d=a-a.mean(0);W+=d.T@d/len(a)/4
        reg=.9*W+.1*np.trace(W)/59*np.eye(59);e,v=np.linalg.eigh(reg);R=(v*(1/np.sqrt(e)))@v.T
        d=mu-grand;B=d.T@d/4;ev,U=np.linalg.eigh(R@B@R);keep=np.flatnonzero(ev>1e-10*ev[-1])[-3:][::-1];A=R@U[:,keep]
        original=np.asarray(state['embedding']);assert np.allclose(A@A.T,original@original.T,rtol=1e-9,atol=1e-11)
    elif method in ['E3','E5']:
        assert sha(ROOT/'working/baseline_artifacts/rf_final.pkl')=='5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870'
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('always')
            with open(ROOT/'working/baseline_artifacts/rf_final.pkl','rb') as f:forest=pickle.load(f)
        assert len(forest.estimators_)==500
    with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as a:
        rf=a['y_ams_pred_zero'].copy();assert np.array_equal(a['y_amsterdam'],y) and np.array_equal(a['pixel_ids_amsterdam'],ids)
    historical=np.load(ROOT/'working/baseline_artifacts/prototype_trial_scores.npz',allow_pickle=False)
    rng=np.random.default_rng(42);episodes=list(m['episodes'])
    if method=='E4':episodes.append({'budget':0,'trial':0,'episode_id':'E4-zero-shot-all-target','support_row_indices':[]})
    assert len(rows)==len(episodes)==(61 if method=='E4' else 60)
    for i,(episode,row) in enumerate(zip(episodes,rows)):
        b=episode['budget'];assert (episode['episode_id'],b,episode['trial'])==(row['episode_id'],row['budget'],row['trial'])
        if b:
            assert rng.bit_generator.state==episode['rng_before']
            s=np.concatenate([rng.choice(np.flatnonzero(y==c),b,replace=False) for c in [1,2,3,4]])
            assert np.array_equal(s,episode['support_row_indices']) and rng.bit_generator.state==episode['rng_after']
        else:s=np.array([],dtype=np.int64)
        q=np.flatnonzero(~np.isin(np.arange(len(y)),s));assert not np.intersect1d(s,q).size and len(q)+len(s)==len(y)
        packet={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'source_state':state,'parameters':{'episode_id':episode['episode_id'],'budget':b,'trial':episode['trial'],'classes':[1,2,3,4],'candidate':method}}
        ep=run/row['worker_evidence'];assert sha(ep)==row['worker_sha256'];evidence=json.loads(ep.read_text());ev=evidence['boundary_evidence'];out=evidence['result']
        assert ev['code_sha256']==entry['code_hashes']['g4c_episode_worker.py'] and ev['packet_sha256']==hashlib.sha256(canon(packet)).hexdigest()
        assert ev['teardown_pass'] and ev['lifecycle']['pass_'] and not ev['lifecycle']['final_survivors'] and not ev['stderr'] and ev['returncode']==0 and ev['reason'] is None
        assert out['label_access']=={'source_state_only':True,'current_support_labels':len(s),'query_labels':0,'other_episode_labels':0} and out['fresh_state_probe'] and out['source_state_sha256']==sh
        assert out['query_fingerprint']==hashlib.sha256(canon(ids[q].tolist())).hexdigest()
        preds={'frozen_rf':rf[q]}
        if b:
            centers=np.stack([x[s][y[s]==c].mean(0) for c in [1,2,3,4]]);preds['raw_prototype']=near(x[q],centers)
            assert np.array_equal(centers,np.asarray(out['adaptation_state']['prototypes']))
        if method=='E2':
            dd=(x[q,None,active]-centers[None,:,active]);preds['candidate']=np.argmin(np.sum(dd*dd*weights,axis=2),axis=1)+1
            preds['all_ones_active']=near(x[q][:,active],centers[:,active]);u=[]
            for start in range(0,len(q),4096):
                diff=dd[start:start+4096];u.append(np.argmin(np.einsum('ncd,de,nce->nc',diff,u0,diff,optimize=True),axis=1)+1)
            preds['unsupervised_covariance']=np.concatenate(u)
        elif method=='E4':
            transformed=(x[q][:,active]-grand)@A;preds['source_centroid']=near(transformed,(mu-grand)@A)
            preds['candidate']=near(transformed,(centers[:,active]-grand)@A) if b else preds['source_centroid']
        elif method=='E3':
            assert params=={'candidate':'E3','translation_strength':1.0,'continuous_indices':list(range(58))}
            delta=(centers-means).mean(0);delta[58:]=0;assert np.allclose(delta,out['adaptation_state']['translation'],rtol=1e-10,atol=1e-12)
            preds['candidate']=forest.predict(x[q]-delta);preds['rf_reproduced']=forest.predict(x[q])
        elif method=='E5':
            assert params=={'candidate':'E5','trees':500,'embedding':'equal-weight leaf one-hot','distance':'squared centroid distance'}
            # Independent tree-by-tree dictionary frequency scoring, no candidate lookup implementation.
            distances=np.ones((len(q),4));leaves=forest.apply(x[s]);assert leaves.tolist()==out['adaptation_state']['support_leaf_ids']
            for t,tree in enumerate(forest.estimators_):
                target=tree.apply(np.asarray(x[q],dtype=np.float32))
                for ci,c in enumerate([1,2,3,4]):
                    keys,counts=np.unique(leaves[y[s]==c,t],return_counts=True);freq=dict(zip(keys,(counts/b).tolist()));norm=sum(v*v for v in freq.values())
                    overlap=np.fromiter((freq.get(v,0.) for v in target),dtype=float,count=len(q));distances[:,ci]+=(norm-2*overlap)/500
            preds['candidate']=np.argmin(distances,axis=1)+1;preds['rf_reproduced']=forest.predict(x[q])
        with np.load(ROOT/row['prediction_artifact'],allow_pickle=False) as a:
            assert sha(ROOT/row['prediction_artifact'])==row['prediction_sha256'] and np.array_equal(q,a['query_indices']) and np.array_equal(ids[q],a['query_ids'])
            assert set(a.files)==set(preds)|{'query_indices','query_ids'}
            for name,pred in preds.items():
                assert np.array_equal(pred,a[name]),('Prediction disagreement',method,episode['episode_id'],name,int(np.count_nonzero(pred!=a[name])))
                if name in out['predictions']:assert np.array_equal(pred,out['predictions'][name])
                calculated=score(y[q],pred);assert calculated==row['metrics'][name],('Metric disagreement',i,name)
                assert hashlib.sha256(canon(calculated['confusion'])).hexdigest()==row['confusion_sha256'][name]
            for name,delta in row['paired_deltas'].items():assert delta==row['metrics']['candidate']['macro_f1']-row['metrics'][name]['macro_f1']
        if b:assert row['metrics']['raw_prototype']['macro_f1']==historical[f'shots_{b}'][episode['trial']-1]
        print('verified',method,i+1,flush=True)
    for budget,items in summary['summary'].items():
        group=[r for r in rows if r['budget']==int(budget)]
        for name,v in items.items():
            if name.startswith('delta_'):
                values=np.asarray([r['paired_deltas'][name[6:]] for r in group]);assert v['positive_trials']==int(np.sum(values>0))
            else:
                values=np.asarray([r['metrics'][name]['macro_f1'] for r in group]);assert v['per_class_mean']==np.mean([r['metrics'][name]['per_class_f1'] for r in group],0).tolist()
            assert v['mean']==values.mean() and v['std_ddof0']==values.std() and v['values']==values.tolist()
    p=summary['summary']['25'];pc=np.asarray(p['candidate']['per_class_mean'])-p['raw_prototype']['per_class_mean'];criteria={'mean_gain_raw_ge_0.0100':p['delta_raw_prototype']['mean']>=.01,'positive_raw_trials_ge_8':p['delta_raw_prototype']['positive_trials']>=8,'per_class_regression_ge_minus_0.0200':bool(np.all(pc>=-.02)),'positive_same_query_rf_gain':p['delta_frozen_rf']['mean']>0};assert summary['success_criteria']==criteria
    verdict='PROMISING' if all(criteria.values()) else ('FALSIFIED' if p['delta_raw_prototype']['mean']<=0 or np.any(pc<-.02) else 'INCONCLUSIVE');assert verdict==summary['verdict']
    for path in [run/'evidence/preflight_1.json',run/'evidence/preflight_2.json',run/'evidence/post_candidate_probe.json']:
        a=json.loads(path.read_text());assert a['result']['status']=='PASS' and a['boundary_evidence']['teardown_pass'] and not a['boundary_evidence']['lifecycle']['final_survivors']
    if method!='E5':
        a=json.loads((run/'evidence/source_worker.json').read_text());assert a['result']['target_rows_received']==0 and a['boundary_evidence']['teardown_pass']
        packet={'X_source':X.tolist(),'y_source':Y.tolist(),'parameters':params};assert a['boundary_evidence']['packet_sha256']==hashlib.sha256(canon(packet)).hexdigest()
    pins=json.loads((ROOT/'working/G4C-PROVENANCE-CHECKPOINT/input_artifact_hashes.json').read_text());assert all(sha(ROOT/p)==v['sha256'] for p,v in pins.items())
    assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT)
    result={'status':'PASS','candidate':method,'independent_source_reconstruction':True,'exact_prediction_records':len(rows),'exact_score_confusion_records':len(rows),'historical_raw_match':60,'rng_episode_replay':60,'same_query_alignment':True,'packet_reconstruction_hash_match':True,'worker_teardown':len(rows),'fresh_state_probes':3,'protected_files':33,'all_checkpoint_inputs_unchanged':True,'original_clean':True,'verifier_sha256':sha(__file__),'trust_scope':'privileged independent verifier; candidate sealed code with private namespaces, current packet only, approved runtime, optional exact RF-only read-only mount; trusted host/kernel'}
    with (run/'independent_verification.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result),flush=True)
if __name__=='__main__':
    try:main(sys.argv[1])
    except BaseException:
        import traceback
        p=ROOT/'working'/f'G4C-{sys.argv[1]}-001'/'STOP_REASON.md'
        with p.open('x') as f:f.write('# STOP — independent verification failed; no repair/retry\n\n```\n'+traceback.format_exc()+'\n```\n')
        raise
