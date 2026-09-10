"""Locked candidate validation only. No selection or configuration changes here."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,time,pickle,hashlib
import numpy as np
from scipy.spatial import cKDTree
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from capacity import build_state
from candidate_predict import adapt_and_predict as candidate_predict,BUDGETS
from candidate.experiments_2h.run import setup,representation,predict,save,sha
from candidate.exp010_predict import adapt_and_predict as frozen_predict,SUPPORTED_SCHEDULE
from candidate.joint_sweep import episodes
from h_predict import fit_source as fit_h,adapt_and_predict as h_predict
C=np.array([1,2,3,4])

def main():
 mode=sys.argv[1];repeat='--repeat'in sys.argv;tag='final_'+mode+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();cfg=json.loads((H/'FINAL_SELECTION.json').read_text())
 for f,h in cfg['files_sha256'].items():assert sha(H/f)==h,f
 st,d=setup();A=d['X_amsterdam'];y=d['y_amsterdam'];coords=d['pixel_ids_amsterdam'];state=build_state(d,cfg['local_leaf']);assert cfg['source_basis']==state['source_basis'];hstate=fit_h(st,d['X_madrid'],d['y_madrid']);compact={k:representation(st,d,k)for k in [30,45]};seed=cfg['final_episode_seed'];nt=100 if mode=='100'else 10;eps=episodes(y,seed,nt);queries=None;meta={'seed':seed,'trials_per_budget':nt,'support':'nested class-stratified without replacement','query':'all support complement','fresh_population':False,'selection':'recipe locked before seed104729 scores'}
 if mode=='yspatial':
  yy=coords[:,1];cut=float(np.median(yy));rng=np.random.default_rng(seed);eps={};queries={};availability=[]
  for t in range(nt):
   side=yy<=cut if t%2==0 else yy>cut;q=np.flatnonzero(yy>cut+10 if t%2==0 else yy<cut-10);pools={c:np.flatnonzero(side&(y==c))for c in C};counts=[len(pools[c])for c in C];assert min(counts)>=200;assert np.array_equal(np.unique(y[q]),C);perms={c:rng.permutation(pools[c])[:200]for c in C};eps[t]={b:np.concatenate([perms[c][:b]for c in C])for b in BUDGETS};queries[t]=q;availability.append(counts)
  meta.update({'spatial_axis':'py_key','median_cut':cut,'buffer_key_units':10,'support_side':'alternating north/south','support_region_class_counts':availability,'query':'opposite half beyond buffer'})
 elif mode!='100':raise ValueError(mode)
 rec=[];payload={};start=time.time();minimum_distance=[]
 for t in range(nt):
  for b in BUDGETS:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s)if queries is None else queries[t];assert not np.intersect1d(s,q).size;ys=y[s].copy();k=SUPPORTED_SCHEDULE[b][0];Z,delta=compact[k]
   predictions={'ASTRA_AGF':candidate_predict(state,s,ys,b)[q],'EXP010':frozen_predict(st,A[s],ys,A[q],b,seed),'EXPF':predict(Z[s],ys,Z[q],delta,metric='regularized'),'EXPH':h_predict(hstate,A[s],ys,A[q],b)}
   if queries is not None:minimum_distance.append(float(cKDTree(coords[s]).query(coords[q])[0].min()))
   # Target query truth is first sliced after all predictions have finished.
   truth=y[q];base=f1_score(truth,predictions['EXP010'],average='macro');tag0=f'b{b}_t{t}';payload[tag0+'_s']=s;payload[tag0+'_q']=q
   for name,p in predictions.items():
    pc=f1_score(truth,p,labels=C,average=None,zero_division=0);rec.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(truth,p,labels=C).tolist()});payload[tag0+'_'+name]=p.astype(np.int8)
  print(mode,'episode',t+1,'/',nt,flush=True)
 summary={}
 for b in BUDGETS:
  summary[b]={}
  for name in predictions:
   rr=[r for r in rec if r['budget']==b and r['method']==name];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 if minimum_distance:meta['minimum_support_query_distances']=minimum_distance
 save(out,{'records':rec,'summary':summary,'meta':meta,'seconds':time.time()-start,'configuration':cfg,'script_sha':sha(Path(__file__)),'ddof':0});np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((H/('final_'+mode+'.json')).read_text());assert old['records']==rec
  with np.load(H/('final_'+mode+'.npz'))as data:
   assert set(data.files)==set(payload)
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  save(H/('final_'+mode+'_reproducibility.json'),{'pass':True,'arrays_exact':len(payload),'episodes_per_budget':nt})
 for f,h in cfg['files_sha256'].items():assert sha(H/f)==h,f
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
