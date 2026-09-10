from pathlib import Path
import os
for key in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS']: os.environ[key]='1'
import sys,json,time,hashlib
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(HERE))
from candidate.experiments_2h.run import setup,representation,predict,spatial_episodes,save,sha
from candidate.exp010_predict import adapt_and_predict,SUPPORTED_SCHEDULE
from candidate.joint_sweep import episodes
from models import *

def main():
 mode=sys.argv[1] if len(sys.argv)>1 else 'audit'; repeat='--repeat' in sys.argv
 seed=8675309 if mode=='fresh' else 31337
 tag=mode+('_repeat' if repeat else ''); out=HERE/(tag+'.json'); assert not out.exists()
 st,d=setup(); A=d['X_amsterdam']; M=d['X_madrid']; y=d['y_amsterdam']; ym=d['y_madrid']; n=len(y)
 eps=episodes(y,seed,10); queries=None
 if mode=='spatial': eps,queries,meta=spatial_episodes(d)
 else: meta={'seed':seed,'nested':True,'query':'all support complement'}
 # Stage 1 sees source labels and target FEATURES ONLY. Save source probabilities as immutable cache.
 cache=HERE/'source_coral_prob.npy'
 if cache.exists(): prior=np.load(cache)
 else:
  print('fitting independently CORAL-aligned source RF',flush=True)
  prior=rf().fit(align_source(M,A),ym).predict_proba(A); np.save(cache,prior)
 neigh=neighbours(np.asarray(d['pixel_ids_amsterdam'],float))
 W=power(regularize(np.cov(A,rowvar=False)),-.5); Aw=(A-A.mean(0))@W
 compact={}
 for k in [30,45]:
  Z,delta=representation(st,d,k); ix=np.sort(np.argsort(st['feature_importances'])[::-1][:k]); Zm=M[:,ix]*np.asarray(st['metric_weights'])[ix]
  source=residual_cov(Zm,ym); pool=np.cov(Z,rowvar=False); w=power(regularize(pool),-.5)
  compact[k]=(Z,delta,source,pool,w,residual_cov(Zm@w,ym))
 rec=[]; payload={}; t0=time.time()
 for t in range(10):
  for b in [5,25,50,100,200]:
   s=eps[t][b]; q=np.setdiff1d(np.arange(n),s) if queries is None else queries[t]
   assert not np.intersect1d(s,q).size
   ys=y[s].copy(); k,lam=SUPPORTED_SCHEDULE[b]; Z,delta,Cm,Ca,w,Cmw=compact[k]; S=Z[s]; Cs=residual_cov(S,ys)
   pred={'EXP010':adapt_and_predict(st,A[s],ys,A[q],b,seed),'EXPF':predict(S,ys,Z[q],delta,metric='regularized')}
   for name,gamma in [('k',k/(k+len(s))),('4k',4*k/(4*k+len(s))),('half',.5)]:
    source=Cm*np.trace(Cs)/max(np.trace(Cm),1e-12); V=np.linalg.inv(regularize((1-gamma)*Cs+gamma*source))
    p=metric_prob(S,ys,Z[q],V); pred['H_'+name]=C[p.argmax(1)]
    if name=='k': pred['H_mean']=C[metric_prob(S,ys,Z[q],V,delta,.6*gamma).argmax(1)]
   pred['pool_metric']=C[metric_prob(S,ys,Z[q],np.linalg.inv(regularize(Ca))).argmax(1)]
   Zw=Z@w; Csw=residual_cov(Zw[s],ys)
   pred['pool_F']=C[metric_prob(Zw[s],ys,Zw[q],np.linalg.inv(regularize(Csw))).argmax(1)]
   g=k/(k+len(s)); blend=(1-g)*Csw+g*Cmw*np.trace(Csw)/max(np.trace(Cmw),1e-12)
   pred['pool_H']=C[metric_prob(Zw[s],ys,Zw[q],np.linalg.inv(regularize(blend))).argmax(1)]
   lp,rp=support_models(A[s],ys,A); wr=rf().fit(Aw[s],ys).predict_proba(Aw)
   for name,p in [('LR60',lp),('RF60',rp),('pool_RF60',wr)]:
    pred[name]=C[p[q].argmax(1)]; pred[name+'_smooth']=C[smooth(p,neigh)[q].argmax(1)]
   for a in [0,.25,.5,.75,1]:
    for name,p in [('blend',rp),('pool_blend',wr)]:
     field=a*prior+(1-a)*p; pred[f'{name}_{a:.2f}']=C[field[q].argmax(1)]
   tag0=f'b{b}_t{t}'; payload[tag0+'_s']=s; payload[tag0+'_q']=q
   # ONLY evaluator reads query truth. Prediction functions have no access to it.
   truth=y[q]; base=float(f1_score(truth,pred['EXP010'],average='macro'))
   for name,p in pred.items():
    pc=f1_score(truth,p,labels=C,average=None,zero_division=0); score=float(pc.mean())
    rec.append({'budget':b,'trial':t,'method':name,'f1':score,'delta':score-base,'class_f1':pc.tolist(),'cm':confusion_matrix(truth,p,labels=C).tolist()}); payload[tag0+'_'+name]=p.astype(np.int8)
   print(mode,t,b,'LR',round(rec[[r['method'] for r in rec].index('LR60')]['f1'],3) if t==0 and b==5 else 'done',flush=True)
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in pred:
   rr=[r for r in rec if r['budget']==b and r['method']==name]; vals=np.array([r['f1'] for r in rr]); dv=np.array([r['delta'] for r in rr])
   summary[b][name]={'mean':float(vals.mean()),'sd':float(vals.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1'] for r in rr],axis=0).tolist()}
 result={'mode':mode,'meta':meta,'seed':seed,'trials':10,'selection':'audit exploration, not independent validation','ddof':0,'records':rec,'summary':summary,'seconds':time.time()-t0,'script_sha':sha(Path(__file__)),'models_sha':sha(HERE/'models.py'),'plan_sha':sha(HERE/'PLAN.md')}
 save(out,result); np.savez_compressed(HERE/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((HERE/(mode+'.json')).read_text()); assert old['records']==rec
  with np.load(HERE/(mode+'.npz')) as p:
   assert set(p.files)==set(payload)
   for key,value in payload.items(): assert np.array_equal(p[key],value),key
  save(HERE/(mode+'_reproducibility.json'),{'pass':True,'arrays_compared':len(payload),'records_identical':True})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1): main()
