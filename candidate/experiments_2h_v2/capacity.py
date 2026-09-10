"""Final capacity-only control: default leaf1 versus existing leaf2 via public API.
Source basis physical, same prior/whitening/blend/Gaussian graph. No other knob changes.
"""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,pickle,time
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from candidate_predict import fit_pool,pool_hash,adapt_and_predict,BUDGETS
from candidate.experiments_2h.run import setup,spatial_episodes,save,sha
from candidate.joint_sweep import episodes

def build_state(d,leaf):
 with(H/'physical_source_models.pkl').open('rb')as f:model=pickle.load(f)[1]
 return fit_pool(d['X_madrid'],d['y_madrid'],d['pixel_ids_madrid'],d['X_amsterdam'],d['pixel_ids_amsterdam'],d['scaler'].mean_,d['scaler'].scale_,source_basis='physical',local_leaf=leaf,aligned_source_model=model,aligned_model_pool_hash=pool_hash(d['X_amsterdam'],d['pixel_ids_amsterdam']))

def main():
 mode=sys.argv[1];leaf=int(sys.argv[2]);repeat='--repeat'in sys.argv;tag=f'capacity_leaf{leaf}_{mode}'+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();st,d=setup();state=build_state(d,leaf);np.testing.assert_array_equal(state['prior'],np.load(H/'physical_source_priors.npz')['physical1']);y=d['y_amsterdam'];seed=8675309 if mode=='fresh'else 31337;eps=episodes(y,seed,10);queries=None;meta={'seed':seed}
 if mode=='spatial':eps,queries,meta=spatial_episodes(d)
 control=json.loads((H/f'stage2_{mode}.json').read_text());rec=[];payload={};start=time.time()
 for t in range(10):
  for b in BUDGETS:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s)if queries is None else queries[t];full,prob=adapt_and_predict(state,s,y[s].copy(),b,return_proba=True);p=full[q];pc=f1_score(y[q],p,labels=[1,2,3,4],average=None,zero_division=0);base=next(r['f1']for r in control['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010');rec.append({'budget':b,'trial':t,'method':'ASTRA_AGF','f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=[1,2,3,4]).tolist()});tag0=f'b{b}_t{t}';payload[tag0+'_s']=s;payload[tag0+'_q']=q;payload[tag0+'_pred']=p
   if leaf==2:
    with np.load(H/f'source_basis_{mode}.npz')as old:np.testing.assert_array_equal(p,old[tag0+'_physical1_gaussian'])
   print(mode,leaf,t,b,flush=True)
 summary={}
 for b in BUDGETS:
  rr=[r for r in rec if r['budget']==b];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 save(out,{'records':rec,'summary':summary,'meta':meta,'leaf':leaf,'seconds':time.time()-start,'public_api_source_prior_exact':True,'selection':'final default-versus-conservative tree-leaf control; no other setting changed','script_sha':sha(Path(__file__)),'candidate_sha':sha(H/'candidate_predict.py')});np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((H/(f'capacity_leaf{leaf}_{mode}.json')).read_text());assert old['records']==rec
  with np.load(H/(f'capacity_leaf{leaf}_{mode}.npz'))as data:
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  save(H/(f'capacity_leaf{leaf}_{mode}_reproducibility.json'),{'pass':True,'arrays_exact':len(payload)})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
