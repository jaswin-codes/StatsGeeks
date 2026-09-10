"""One hypothesis: budget-dependent diagonal shrinkage and ZCA coordinate basis.
No new features, source prior or forest settings. No competitor imports.
"""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,time
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import C,power,neighbours,smooth
from stage2_models import forest,immediate_grid
from candidate.experiments_2h.run import setup,spatial_episodes,save,sha
from candidate.joint_sweep import episodes

def main():
 mode=sys.argv[1];repeat='--repeat'in sys.argv;tag='whitening_'+mode+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();st,d=setup();A=d['X_amsterdam'];y=d['y_amsterdam'];G=immediate_grid(d['pixel_ids_amsterdam']);nn=neighbours(d['pixel_ids_amsterdam']);prior=np.load(H/'conditional_priors.npz')['cc1'];seed=8675309 if mode=='fresh'else 31337;eps=episodes(y,seed,10);queries=None;meta={'seed':seed}
 if mode=='spatial':eps,queries,meta=spatial_episodes(d)
 control=json.loads((H/f'stage2_{mode}.json').read_text());rec=[];payload={};start=time.time();features={}
 for basis,X in [('standardized',A),('rawunit',A*d['scaler'].scale_+d['scaler'].mean_)]:
  cov=np.cov(X,rowvar=False);d0=X.shape[1]
  for b in [5,25,50,100,200]:
   rho=d0/(d0+4*b);covuse=(1-rho)*cov+rho*np.diag(np.diag(cov))+1e-7*np.eye(d0);features[b,basis]=(X-X.mean(0))@power(covuse,-.5)
 for t in range(10):
  for b in [5,25,50,100,200]:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s)if queries is None else queries[t];ys=y[s].copy();predictions={}
   for basis in ['standardized','rawunit']:
    F=features[b,basis];P=forest().fit(F[s],ys).predict_proba(F);alpha=20/(20+len(s));blend=alpha*prior+(1-alpha)*P
    for m,p in [(basis,P),(basis+'_grid',G@P),(basis+'_knn',smooth(P,nn)),(basis+'_cc1',blend),(basis+'_cc1_grid',G@blend),(basis+'_cc1_knn',smooth(blend,nn))]:predictions[m]=C[p[q].argmax(1)]
   tag0=f'b{b}_t{t}';payload[tag0+'_s']=s;payload[tag0+'_q']=q;base=next(r['f1']for r in control['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010')
   for name,p in predictions.items():
    pc=f1_score(y[q],p,labels=C,average=None,zero_division=0);rec.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=C).tolist()});payload[tag0+'_'+name]=p
   print(mode,t,b,'done',flush=True)
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in predictions:
   rr=[r for r in rec if r['budget']==b and r['method']==name];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 save(out,{'records':rec,'summary':summary,'meta':meta,'seconds':time.time()-start,'selection':'whitening-coordinate hypothesis, audit-based exploration','rho':'d/(d+4*n)','script_sha':sha(Path(__file__))});np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((H/('whitening_'+mode+'.json')).read_text());assert old['records']==rec
  with np.load(H/('whitening_'+mode+'.npz'))as data:
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  save(H/('whitening_'+mode+'_reproducibility.json'),{'pass':True,'arrays_exact':len(payload)})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
