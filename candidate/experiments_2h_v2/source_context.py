"""Independent source context ablation: source prior only changes; local remains60.
Save probability fields for a later controlled smoothing ablation without refitting.
"""
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

def priors(d,refit=False):
 cache=H/'source_context_priors.npz'
 if cache.exists()and not refit:return dict(np.load(cache))
 mats=[]
 for city in ['madrid','amsterdam']:
  X=d['X_'+city];G=immediate_grid(d['pixel_ids_'+city]);mats.append(np.column_stack([X,G@X]))
 M,A=mats;ym=d['y_madrid'];T=align_source(M,A);result={};models={};counts={}
 for iteration in [0,1]:
  model=forest().fit(T,ym);result['ctx'+str(iteration)]=model.predict_proba(A);models[iteration]=model;print('source context',iteration,'done',flush=True)
  if iteration==0:T,counts=conditional_step(T,ym,A,model)
 if refit:
  old=np.load(cache)
  for k,p in result.items():np.testing.assert_array_equal(p,old[k])
  save(H/'source_context_source_reproduction.json',{'pass':True,'source_probability_arrays_exact':2})
 else:
  np.savez_compressed(cache,**result);save(H/'source_context_counts.json',counts)
  with(H/'source_context_models.pkl').open('wb')as f:pickle.dump(models,f)
 return result

def main():
 mode=sys.argv[1];repeat='--repeat'in sys.argv;tag='source_context_'+mode+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();st,d=setup();A=d['X_amsterdam'];y=d['y_amsterdam'];G=immediate_grid(d['pixel_ids_amsterdam']);nn=neighbours(d['pixel_ids_amsterdam']);ps=priors(d,'--refit-source'in sys.argv);seed=8675309 if mode=='fresh'else 31337;eps=episodes(y,seed,10);queries=None;meta={'seed':seed}
 if mode=='spatial':eps,queries,meta=spatial_episodes(d)
 W=power(regularize(np.cov(A,rowvar=False)),-.5);Z=(A-A.mean(0))@W;control=json.loads((H/f'stage2_{mode}.json').read_text());rec=[];payload={};fields={};start=time.time()
 for t in range(10):
  for b in [5,25,50,100,200]:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s)if queries is None else queries[t];ys=y[s].copy();predictions={};tag0=f'b{b}_t{t}'
   for basis,F in [('raw',A),('pool',Z)]:
    P=forest().fit(F[s],ys).predict_proba(F);fields[tag0+'_'+basis]=P
    for priorname,prior in ps.items():
     alpha=20/(20+len(s));blend=alpha*prior+(1-alpha)*P
     for m,p in [(basis+'_'+priorname,blend),(basis+'_'+priorname+'_grid',G@blend),(basis+'_'+priorname+'_knn',smooth(blend,nn))]:predictions[m]=C[p[q].argmax(1)]
   payload[tag0+'_s']=s;payload[tag0+'_q']=q;base=next(r['f1']for r in control['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010')
   for name,p in predictions.items():
    pc=f1_score(y[q],p,labels=C,average=None,zero_division=0);rec.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=C).tolist()});payload[tag0+'_'+name]=p
   print(mode,t,b,'done',flush=True)
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in predictions:
   rr=[r for r in rec if r['budget']==b and r['method']==name];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 save(out,{'records':rec,'summary':summary,'meta':meta,'seconds':time.time()-start,'selection':'source-context hypothesis, audit-based exploration','source_zero_shot':{k:float(f1_score(y,C[p.argmax(1)],average='macro'))for k,p in ps.items()},'script_sha':sha(Path(__file__))});np.savez_compressed(H/(tag+'.npz'),**payload);np.savez_compressed(H/(tag+'_fields.npz'),**fields)
 if repeat:
  old=json.loads((H/('source_context_'+mode+'.json')).read_text());assert old['records']==rec
  with np.load(H/('source_context_'+mode+'.npz'))as data:
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  with np.load(H/('source_context_'+mode+'_fields.npz'))as data:
   for k,v in fields.items():np.testing.assert_array_equal(v,data[k])
  save(H/('source_context_'+mode+'_reproducibility.json'),{'pass':True,'prediction_arrays_exact':len(payload),'probability_fields_exact':len(fields)})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
