"""Predetermined dimension/sample-size local covariance schedule; no sweeping."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,time
import numpy as np
from scipy.spatial import cKDTree
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import C,power
from stage2_models import forest
from candidate.experiments_2h.run import setup,spatial_episodes,save,sha
from candidate.joint_sweep import episodes

def main():
 mode=sys.argv[1];leaf=int(sys.argv[2])if len(sys.argv)>2 and sys.argv[2].isdigit()else 2;repeat='--repeat'in sys.argv;tag=f'adaptive_leaf{leaf}_{mode}'+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();st,d=setup();y=d['y_amsterdam'];X=d['X_amsterdam']*d['scaler'].scale_+d['scaler'].mean_;prior=np.load(H/'source_context_priors.npz')['ctx1'];dist,nn=cKDTree(d['pixel_ids_amsterdam']).query(d['pixel_ids_amsterdam'],k=9);w=np.exp(-dist**2/2);w/=w.sum(1,keepdims=True);seed=8675309 if mode=='fresh'else 31337;eps=episodes(y,seed,10);queries=None;meta={'seed':seed}
 if mode=='spatial':eps,queries,meta=spatial_episodes(d)
 cov=np.cov(X,rowvar=False);Z={}
 for b in [5,25,50,100,200]:
  rho=min(1,60/(4*b));V=(1-rho)*cov+rho*np.diag(np.diag(cov))+1e-7*np.eye(60);Z[b]=(X-X.mean(0))@power(V,-.5)
 controls=json.loads((H/f'stage2_{mode}.json').read_text());records=[];payload={};fields={};start=time.time()
 for t in range(10):
  for b in [5,25,50,100,200]:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s)if queries is None else queries[t];ys=y[s].copy();model=forest().set_params(min_samples_leaf=leaf).fit(Z[b][s],ys);P=model.predict_proba(Z[b]);alpha=20/(20+len(s));blend=alpha*prior+(1-alpha)*P
   probs={'local':P,'local_gaussian':np.sum(P[nn]*w[:,:,None],axis=1),'blend':blend,'blend_gaussian':np.sum(blend[nn]*w[:,:,None],axis=1)};predictions={k:C[p[q].argmax(1)]for k,p in probs.items()};tag0=f'b{b}_t{t}';payload[tag0+'_s']=s;payload[tag0+'_q']=q;fields[tag0]=P;base=next(r['f1']for r in controls['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010')
   for name,p in predictions.items():
    pc=f1_score(y[q],p,labels=C,average=None,zero_division=0);records.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=C).tolist()});payload[tag0+'_'+name]=p
   print(mode,leaf,t,b,'done',flush=True)
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in predictions:
   rr=[r for r in records if r['budget']==b and r['method']==name];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 save(out,{'records':records,'summary':summary,'meta':meta,'seconds':time.time()-start,'rho':'min(1,60/(4*budget))','leaf':leaf,'selection':'predeclared final local-geometry/capacity ablation, audit exploration','script_sha':sha(Path(__file__))});np.savez_compressed(H/(tag+'.npz'),**payload);np.savez_compressed(H/(tag+'_fields.npz'),**fields)
 if repeat:
  old=json.loads((H/(f'adaptive_leaf{leaf}_{mode}.json')).read_text());assert old['records']==records
  with np.load(H/(f'adaptive_leaf{leaf}_{mode}.npz'))as data:
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  with np.load(H/(f'adaptive_leaf{leaf}_{mode}_fields.npz'))as data:
   for k,v in fields.items():np.testing.assert_array_equal(v,data[k])
  save(H/(f'adaptive_leaf{leaf}_{mode}_reproducibility.json'),{'pass':True,'prediction_arrays_exact':len(payload),'probability_fields_exact':len(fields)})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
