from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,time,pickle
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import C,power,regularize,align_source,neighbours,smooth
from stage2_models import forest,immediate_grid,conditional_step
from candidate.experiments_2h.run import setup,spatial_episodes,save,sha
from candidate.joint_sweep import episodes
from candidate.exp010_predict import adapt_and_predict

def stage1(M,ym,A,repeat=False):
 cache=H/'conditional_priors.npz'
 if cache.exists() and not repeat:return dict(np.load(cache))
 transported=align_source(M,A);prior={};counts={};models={}
 for r in range(3):
  model=forest().fit(transported,ym);prior['cc'+str(r)]=model.predict_proba(A);models[r]=model
  print('source conditional iteration',r,'done',flush=True)
  if r<2:transported,counts[r]=conditional_step(transported,ym,A,model)
 if repeat:
  old=np.load(cache)
  for key,v in prior.items():np.testing.assert_array_equal(v,old[key])
  save(H/'conditional_source_reproduction.json',{'pass':True,'probability_arrays_exact':3})
 else:
  np.savez_compressed(cache,**prior);save(H/'conditional_pseudo_counts.json',counts)
  with (H/'conditional_source_models.pkl').open('wb')as f:pickle.dump(models,f)
 return prior

def main():
 mode=sys.argv[1];repeat='--repeat'in sys.argv;tag='stage2_'+mode+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists()
 st,d=setup();A=d['X_amsterdam'];M=d['X_madrid'];ym=d['y_madrid'];y=d['y_amsterdam'];priors=stage1(M,ym,A,'--refit-source'in sys.argv)
 seed=8675309 if mode=='fresh'else 31337;eps=episodes(y,seed,10);queries=None;meta={'seed':seed,'query':'complement'}
 if mode=='spatial':eps,queries,meta=spatial_episodes(d)
 grid=immediate_grid(d['pixel_ids_amsterdam']);knn=neighbours(d['pixel_ids_amsterdam']);W=power(regularize(np.cov(A,rowvar=False)),-.5);Z=(A-A.mean(0))@W;rec=[];payload={};start=time.time()
 for t in range(10):
  for b in [5,25,50,100,200]:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s)if queries is None else queries[t];assert not np.intersect1d(s,q).size;ys=y[s].copy()
   raw=forest().fit(A[s],ys).predict_proba(A);pool=forest().fit(Z[s],ys).predict_proba(Z)
   predictions={'EXP010':adapt_and_predict(st,A[s],ys,A[q],b,seed)}
   for name,p in [('raw',raw),('pool',pool)]:
    predictions[name]=C[p[q].argmax(1)];predictions[name+'_knn']=C[smooth(p,knn)[q].argmax(1)];predictions[name+'_grid']=C[(grid@p)[q].argmax(1)]
    for iteration,prior in priors.items():
     alpha=20/(20+len(s));field=alpha*prior+(1-alpha)*p
     predictions[name+'_'+iteration]=C[field[q].argmax(1)];predictions[name+'_'+iteration+'_grid']=C[(grid@field)[q].argmax(1)]
   tag0=f'b{b}_t{t}';payload[tag0+'_s']=s;payload[tag0+'_q']=q
   # All arms complete before evaluator sees truth.
   truth=y[q];base=f1_score(truth,predictions['EXP010'],average='macro')
   for name,p in predictions.items():
    pc=f1_score(truth,p,labels=C,average=None,zero_division=0);rec.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(truth,p,labels=C).tolist()});payload[tag0+'_'+name]=p
   print(mode,t,b,'done',flush=True)
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in predictions:
   rr=[r for r in rec if r['budget']==b and r['method']==name];scores=np.array([r['f1']for r in rr]);delta=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(scores.mean()),'sd':float(scores.std()),'delta':float(delta.mean()),'wins':int((delta>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 result={'records':rec,'summary':summary,'mode':mode,'meta':meta,'seed':seed,'n_trials':10,'source_zero_shot':{k:float(f1_score(y,C[p.argmax(1)],average='macro'))for k,p in priors.items()},'seconds':time.time()-start,'selection':'audit-based stage2 exploration, no independent target holdout','script_sha':sha(Path(__file__)),'models_sha':sha(H/'stage2_models.py')}
 save(out,result);np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  original=json.loads((H/('stage2_'+mode+'.json')).read_text());assert rec==original['records']
  with np.load(H/('stage2_'+mode+'.npz'))as data:
   for key,val in payload.items():np.testing.assert_array_equal(val,data[key])
  save(H/('stage2_'+mode+'_reproducibility.json'),{'pass':True,'arrays_exact':len(payload),'episode_records_exact':True})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
