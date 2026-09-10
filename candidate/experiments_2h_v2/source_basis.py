"""Source-only physical-unit CORAL ablation, with immutable local probability fields."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,pickle
import numpy as np
from scipy.spatial import cKDTree
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import C,align_source
from stage2_models import forest,immediate_grid,conditional_step
from candidate.experiments_2h.run import setup,save,sha

def make_prior(d,refit=False):
 cache=H/'physical_source_priors.npz'
 if cache.exists()and not refit:return dict(np.load(cache))
 mats=[]
 for city in ['madrid','amsterdam']:
  X=d['X_'+city]*d['scaler'].scale_+d['scaler'].mean_;G=immediate_grid(d['pixel_ids_'+city]);mats.append(np.column_stack([X,G@X]))
 M,A=mats;ym=d['y_madrid'];T=align_source(M,A);probs={};models={};counts={}
 for it in [0,1]:
  model=forest().fit(T,ym);probs['physical'+str(it)]=model.predict_proba(A);models[it]=model;print('physical source',it,'done',flush=True)
  if it==0:T,counts=conditional_step(T,ym,A,model)
 if refit:
  old=np.load(cache)
  for k,p in probs.items():np.testing.assert_array_equal(old[k],p)
  save(H/'physical_source_reproduction.json',{'pass':True,'source_probability_arrays_exact':2})
 else:
  np.savez_compressed(cache,**probs);save(H/'physical_source_counts.json',counts)
  with(H/'physical_source_models.pkl').open('wb')as f:pickle.dump(models,f)
 return probs

def main():
 mode=sys.argv[1];repeat='--repeat'in sys.argv;tag='source_basis_'+mode+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();st,d=setup();priors=make_prior(d,'--refit-source'in sys.argv);y=d['y_amsterdam'];dist,nn=cKDTree(d['pixel_ids_amsterdam']).query(d['pixel_ids_amsterdam'],k=9);w=np.exp(-dist**2/2);w/=w.sum(1,keepdims=True);suffix='_repeat'if repeat else '';fields=np.load(H/(f'adaptive_leaf2_{mode}'+suffix+'_fields.npz'));arrays=np.load(H/(f'adaptive_leaf2_{mode}'+suffix+'.npz'));controls=json.loads((H/f'stage2_{mode}.json').read_text());rec=[];payload={}
 for t in range(10):
  for b in [5,25,50,100,200]:
   tag0=f'b{b}_t{t}';s=arrays[tag0+'_s'];q=arrays[tag0+'_q'];P=fields[tag0];alpha=20/(20+len(s));base=next(r['f1']for r in controls['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010');predictions={}
   for name,prior in priors.items():
    field=alpha*prior+(1-alpha)*P
    predictions[name]=C[field[q].argmax(1)];predictions[name+'_gaussian']=C[np.sum(field[nn]*w[:,:,None],axis=1)[q].argmax(1)]
   payload[tag0+'_s']=s;payload[tag0+'_q']=q
   for name,p in predictions.items():
    pc=f1_score(y[q],p,labels=C,average=None,zero_division=0);rec.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=C).tolist()});payload[tag0+'_'+name]=p
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in predictions:
   rr=[r for r in rec if r['budget']==b and r['method']==name];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 save(out,{'records':rec,'summary':summary,'selection':'source-only coordinate basis ablation, audit exploration','source_zero_shot':{k:float(f1_score(y,C[p.argmax(1)],average='macro'))for k,p in priors.items()},'script_sha':sha(Path(__file__))});np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((H/('source_basis_'+mode+'.json')).read_text());assert old['records']==rec
  with np.load(H/('source_basis_'+mode+'.npz'))as data:
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  save(H/('source_basis_'+mode+'_reproducibility.json'),{'pass':True,'arrays_exact':len(payload),'upstream':'independent adaptive-local refit fields; source refit optionally verified separately'})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
