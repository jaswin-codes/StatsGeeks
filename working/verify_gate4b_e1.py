"""Independent privileged reload/prediction/score verifier for fixed E1 run."""
import hashlib,json,pathlib,pickle,subprocess,sys,time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];RUN=ROOT/'working/G4B-E1-001';MH='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def ah(a):
 a=np.ascontiguousarray(a);h=hashlib.sha256(json.dumps([a.dtype.str,list(a.shape)],separators=(',',':')).encode());h.update(a.tobytes());return h.hexdigest()
def metric(c):
 tr=np.trace(c);r=.9*c+.1*tr/len(c)*np.eye(len(c));e,v=np.linalg.eigh(r);assert e[0]>0;return (v*(1/e))@v.T
def predict(xq,p,m=None):
 if m is None:return np.argmin(((xq[:,None,:]-p[None,:,:])**2).sum(2),1)+1
 out=[]
 for i in range(0,len(xq),4096):
  d=xq[i:i+4096,None,:]-p[None,:,:];out.append(np.argmin(np.einsum('ncd,de,nce->nc',d,m,d,optimize=True),1)+1)
 return np.concatenate(out)
def metrics(y,p):
 cm=np.bincount(4*(y-1)+(p-1),minlength=16).reshape(4,4);den=cm.sum(0)+cm.sum(1);pc=np.divide(2*np.diag(cm),den,out=np.zeros(4),where=den>0);return cm,pc,float(pc.mean())
def main():
 sys.path.insert(0,str(ROOT))
 assert sha(ROOT/'working/gate4_episode_manifest.json')==MH
 m=json.load(open(ROOT/'working/gate4_episode_manifest.json'));summary=json.load(open(RUN/'summary.json'));rows=json.load(open(RUN/'per_episode_results.json'));saved=json.load(open(RUN/'source_state.json'))
 with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:d=pickle.load(f)
 xm,ym,x,y,ids=d['X_madrid'],d['y_madrid'],d['X_amsterdam'],d['y_amsterdam'],d['pixel_ids_amsterdam']
 active=np.flatnonzero(xm.var(0)>0);z=xm[:,active];w=0
 for c in [1,2,3,4]:a=z[ym==c];a=a-a.mean(0);w=w+a.T@a/len(a)/4
 a=z-z.mean(0);u=a.T@a/len(a);me,mu=metric(w),metric(u)
 st=saved['source_state'];assert active.tolist()==st['active_indices'];assert np.allclose(me,st['e1_metric'],rtol=1e-10,atol=1e-12);assert np.allclose(mu,st['u0_metric'],rtol=1e-10,atol=1e-12)
 assert hashlib.sha256(canonical(st)).hexdigest()==saved['source_state_sha256']==summary['source_state_sha256']
 with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as a:rf=a['y_ams_pred_zero'];assert np.array_equal(a['y_amsterdam'],y)
 with np.load(ROOT/'working/baseline_artifacts/prototype_trial_scores.npz',allow_pickle=False) as historical:
  for i,(e,row) in enumerate(zip(m['episodes'],rows)):
   assert e['episode_id']==row['episode_id'];s=np.array(e['support_row_indices']);q=np.setdiff1d(np.arange(len(y)),s,assume_unique=True);p=np.stack([x[s][y[s]==c].mean(0) for c in [1,2,3,4]])
   independently={'raw_prototype':predict(x[q],p),'unsupervised_covariance':predict(x[q][:,active],p[:,active],mu),'e1':predict(x[q][:,active],p[:,active],me),'frozen_rf':rf[q]}
   with np.load(ROOT/row['prediction_artifact'],allow_pickle=False) as a:
    assert sha(ROOT/row['prediction_artifact'])==row['prediction_sha256'];assert np.array_equal(a['query_indices'],q) and np.array_equal(a['query_ids'],ids[q])
    for name,pred in independently.items():
     assert np.array_equal(a[name],pred),(e['episode_id'],name);cm,pc,score=metrics(y[q],a[name]);assert cm.tolist()==row['confusion_matrices'][name];assert np.allclose(pc,row['per_class_f1'][name],atol=1e-15);assert abs(score-row['scores'][name])<1e-15
   b=e['budget'];trial=e['trial']-1;assert row['scores']['raw_prototype']==historical[f'shots_{b}'][trial]
 for b,v in summary['summary'].items():
  group=[r for r in rows if r['budget']==int(b)]
  for name in ['raw_prototype','unsupervised_covariance','e1','frozen_rf']:
   a=np.array([r['scores'][name] for r in group]);assert v[name]['mean']==a.mean() and v[name]['std_ddof0']==a.std()
 pins=summary['baseline_hashes'];assert all(sha(ROOT/p)==h for p,h in pins.items());assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT);assert not subprocess.check_output(['git','diff','--','original/'],cwd=ROOT)
 ev=list((RUN/'evidence').glob('worker_*.json'));assert len(ev)==60
 for p in ev:
  z=json.load(open(p));assert z['boundary_evidence']['teardown_pass'] and not z['boundary_evidence']['stderr'];assert not z['boundary_evidence']['lifecycle']['final_survivors']
 result={'status':'PASS','independent_source_state':True,'independent_predictions':60,'independent_scores':60,'historical_raw_trial_scores_exact':60,'same_query_alignment':True,'worker_teardown':60,'manifest_sha256':MH,'protected_hashes':33,'original_clean':True,'candidate_label_access':'source state + current support labels only; independent verifier privileged and does not alter candidate outputs','verifier_sha256':sha(__file__)}
 with (RUN/'independent_verification.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
