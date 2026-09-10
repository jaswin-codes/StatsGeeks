"""Independent privileged E2 reload/reconstruction verifier; no coordinator imports."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[_k]='1'
import hashlib,importlib.util,json,pathlib,pickle,subprocess,sys,time,traceback,types
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[3];RUN=ROOT/'working/G4C-E2-004';MH='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
def sha(p):
 with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def score(y,p):
 cm=np.zeros((4,4),dtype=np.int64);np.add.at(cm,(y-1,p-1),1);tp=np.diag(cm);den=cm.sum(0)+cm.sum(1);f=np.divide(2*tp,den,out=np.zeros(4),where=den>0);pr=np.divide(tp,cm.sum(0),out=np.zeros(4),where=cm.sum(0)>0);re=np.divide(tp,cm.sum(1),out=np.zeros(4),where=cm.sum(1)>0)
 return {'macro_f1':float(f.mean()),'per_class_f1':f.tolist(),'precision':pr.tolist(),'recall':re.tolist(),'accuracy':float(tp.sum()/cm.sum()),'confusion':cm.tolist()}
def nearest(q,c):return np.argmin(np.stack([np.sum((q-v)**2,axis=1) for v in c],axis=1),axis=1)+1
def install_pickle_dependency():
 path=ROOT/'working/minimal_standard_scaler.py';assert sha(path)=='c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111';assert 'working' not in sys.modules
 package=types.ModuleType('working');package.__path__=[];package.__package__='working';spec=importlib.util.spec_from_file_location('working.minimal_standard_scaler',path);assert spec and spec.loader;module=importlib.util.module_from_spec(spec);sys.modules['working']=package;sys.modules['working.minimal_standard_scaler']=module;setattr(package,'minimal_standard_scaler',module);before=list(sys.path);spec.loader.exec_module(module);assert list(sys.path)==before and module.StandardScaler.__module__=='working.minimal_standard_scaler'
def main():
 started=time.perf_counter();summary=json.loads((RUN/'results/execution_summary.json').read_text());rows=json.loads((RUN/'results/per_episode_results.json').read_text());saved=json.loads((RUN/'candidate_state/source_state.json').read_text());state=saved['source_state'];params={'candidate':'E2','epsilon':1e-6,'clip':[.25,4.0],'identity_mixture':.5}
 assert summary['parameters']==state['parameters']==params and summary['episodes_completed']==len(rows)==60 and summary['all_predictions_finalized_before_scoring']
 assert sha(ROOT/'working/gate4_episode_manifest.json')==MH;m=json.loads((ROOT/'working/gate4_episode_manifest.json').read_text());assert len(m['episodes'])==60 and m['gate4a']=='PASS'
 install_pickle_dependency()
 with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:d=pickle.load(f)
 X,Y,x,y,ids=d['X_madrid'],d['y_madrid'],d['X_amsterdam'],d['y_amsterdam'],d['pixel_ids_amsterdam']
 active=np.flatnonzero(X.var(0)>0);means=np.stack([X[Y==c].mean(0) for c in [1,2,3,4]]);mu=means[:,active];grand=mu.mean(0);between=((mu-grand)**2).mean(0);within=np.stack([X[Y==c][:,active].var(0,ddof=0) for c in [1,2,3,4]]).mean(0);ratios=between/(within+1e-6);clipped=np.clip(ratios/ratios.mean(),.25,4);weights=.5+.5*clipped/clipped.mean()
 assert active.tolist()==state['active_indices'];assert np.allclose(means,state['source_means'],rtol=1e-11,atol=1e-13);assert np.allclose(ratios,state['fisher_ratios'],rtol=1e-11,atol=1e-13);assert np.allclose(clipped,state['clipped_normalized'],rtol=1e-11,atol=1e-13);assert np.allclose(weights,state['weights'],rtol=1e-11,atol=1e-13)
 state_hash=hashlib.sha256(canonical(state)).hexdigest();assert state_hash==saved['source_state_sha256']==summary['source_state_sha256']
 z=X[:,active];d0=z-z.mean(0);cov=d0.T@d0/len(z);reg=.9*cov+.1*np.trace(cov)/len(active)*np.eye(len(active));e,v=np.linalg.eigh(reg);u0=(v*(1/e))@v.T
 with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as a:rf=a['y_ams_pred_zero'];assert np.array_equal(a['y_amsterdam'],y) and np.array_equal(a['pixel_ids_amsterdam'],ids)
 historical=np.load(ROOT/'working/baseline_artifacts/prototype_trial_scores.npz',allow_pickle=False);rng=np.random.default_rng(42)
 for i,(episode,row) in enumerate(zip(m['episodes'],rows)):
  b=episode['budget'];assert (episode['episode_id'],b,episode['trial'])==(row['episode_id'],row['budget'],row['trial']);assert rng.bit_generator.state==episode['rng_before'];s=np.concatenate([rng.choice(np.flatnonzero(y==c),b,replace=False) for c in [1,2,3,4]]);assert np.array_equal(s,episode['support_row_indices']);assert rng.bit_generator.state==episode['rng_after'];q=np.setdiff1d(np.arange(len(y)),s,assume_unique=True);assert not np.intersect1d(s,q).size
  centers=np.stack([x[s][y[s]==c].mean(0) for c in [1,2,3,4]]);raw=nearest(x[q],centers);diff=x[q,None,active]-centers[None,:,active];candidate=np.argmin(np.sum(diff*diff*weights,axis=2),axis=1)+1;active_ones=nearest(x[q][:,active],centers[:,active]);up=[]
  for start in range(0,len(q),4096):
   block=diff[start:start+4096];up.append(np.argmin(np.einsum('ncd,de,nce->nc',block,u0,block,optimize=True),axis=1)+1)
  pred={'candidate':candidate,'raw_prototype':raw,'all_ones_active':active_ones,'unsupervised_covariance':np.concatenate(up),'frozen_rf':rf[q]}
  path=ROOT/row['prediction_artifact'];assert sha(path)==row['prediction_sha256']
  with np.load(path,allow_pickle=False) as a:
   assert set(a.files)==set(pred)|{'query_indices','query_ids'};assert np.array_equal(a['query_indices'],q) and np.array_equal(a['query_ids'],ids[q])
   for name,p in pred.items():
    assert np.array_equal(a[name],p),(episode['episode_id'],name,int(np.count_nonzero(a[name]!=p)));calculated=score(y[q],p);assert calculated==row['metrics'][name];assert hashlib.sha256(canonical(calculated['confusion'])).hexdigest()==row['confusion_sha256'][name]
  assert row['metrics']['raw_prototype']['macro_f1']==historical[f'shots_{b}'][episode['trial']-1]
  with np.load(ROOT/'working/G4B-E1-001/predictions'/f"{episode['episode_id']}.npz",allow_pickle=False) as old:assert np.array_equal(old['unsupervised_covariance'],pred['unsupervised_covariance']) and np.array_equal(old['raw_prototype'],raw)
  ev=json.loads((RUN/row['worker_evidence']).read_text())['boundary_evidence'];assert ev['teardown_pass'] and ev['lifecycle']['pass_'] and not ev['lifecycle']['final_survivors'] and ev['returncode']==0 and ev['reason'] is None and not ev['stderr']
  packet={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'source_state':state,'parameters':{'episode_id':episode['episode_id'],'budget':b,'trial':episode['trial'],'classes':[1,2,3,4],'candidate':'E2'}};assert ev['packet_sha256']==hashlib.sha256(canonical(packet)).hexdigest()
  print('verified',i+1,episode['episode_id'],flush=True)
 for budget,items in summary['summary'].items():
  group=[r for r in rows if r['budget']==int(budget)]
  for name,v0 in items.items():
   if name.startswith('candidate_minus_'):
    comp={'candidate_minus_raw':'raw_prototype','candidate_minus_u0':'unsupervised_covariance','candidate_minus_rf':'frozen_rf'}[name];vals=np.array([r['metrics']['candidate']['macro_f1']-r['metrics'][comp]['macro_f1'] for r in group]);assert v0['positive_trials']==int((vals>0).sum())
   else:vals=np.array([r['metrics'][name]['macro_f1'] for r in group]);assert v0['per_class_mean']==np.mean([r['metrics'][name]['per_class_f1'] for r in group],0).tolist()
   assert v0['mean']==vals.mean() and v0['std_ddof0']==vals.std() and v0['values']==vals.tolist()
 p=summary['summary']['25'];reg=np.asarray(p['candidate']['per_class_mean'])-p['raw_prototype']['per_class_mean'];criteria={'mean_gain_over_raw_ge_0.0100':p['candidate_minus_raw']['mean']>=.01,'positive_raw_gain_ge_8_of_10':p['candidate_minus_raw']['positive_trials']>=8,'no_mean_per_class_regression_worse_than_0.0200':bool(np.all(reg>=-.02)),'positive_gain_over_same_query_rf':p['candidate_minus_rf']['mean']>0};assert criteria==summary['success_criteria'];verdict='PROMISING' if all(criteria.values()) else ('FALSIFIED' if p['candidate_minus_raw']['mean']<=0 or not criteria['no_mean_per_class_regression_worse_than_0.0200'] else 'INCONCLUSIVE');assert verdict==summary['scientific_verdict']
 entry=json.loads((ROOT/'working/G4B-E1-001/entry.json').read_text());assert len(entry['protected_hashes'])==33 and all(sha(ROOT/p)==h for p,h in entry['protected_hashes'].items());assert sha(ROOT/'working/baseline_artifacts/rf_final.pkl')=='5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870';assert sha(ROOT/'working/gate4_episode_manifest.json')==MH;assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT)
 for label in ['preflight_1','preflight_2','post_candidate_probe']:
  z=json.loads((RUN/'evidence'/f'{label}.json').read_text());assert z['result']['status']=='PASS' and z['boundary_evidence']['teardown_pass'] and not z['boundary_evidence']['lifecycle']['final_survivors']
 result={'status':'PASS','run_id':'G4C-E2-004','independent_source_state':True,'exact_predictions':60,'independent_score_confusion_records':60,'historical_raw_exact':60,'historical_u0_exact':60,'same_query_alignment':True,'packet_hash_reconstruction':60,'rng_manifest_replay':60,'worker_teardown':60,'fresh_state_probes':3,'protected_33':'PASS','original_clean':True,'manifest_sha256':MH,'verdict':verdict,'seconds':time.perf_counter()-started,'verifier_sha256':sha(__file__),'label_boundary':'Verifier privileged; candidate workers limited to source state/current support and never receive query labels/manifest'}
 with (RUN/'results/independent_verification.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException:
  p=RUN/'results/VERIFICATION_STOP_REASON.md'
  if not p.exists():
   with p.open('x') as f:f.write('# Independent verification STOP — no repair/retry\n\n```\n'+traceback.format_exc()+'\n```\n')
  raise
