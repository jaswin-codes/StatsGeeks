"""Isolated, predeclared sprint evaluator. See PLAN.md; no model receives query labels."""
from pathlib import Path
import os
for key in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS']: os.environ[key]='1'
import sys,json,pickle,time,hashlib,platform
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import sklearn
from sklearn.metrics import confusion_matrix,f1_score
from threadpoolctl import threadpool_limits
from candidate.exp010_predict import load_stage1_artifact,adapt_and_predict,SUPPORTED_SCHEDULE
from candidate.joint_sweep import episodes
OUT=Path(__file__).resolve().parent
BUD=[5,25,50,100,200]; CLS=np.array([1,2,3,4])
FOLDERS={'A':'expA_source_local','B':'expB_dim_shrink','C':'expC_class_diagnostic','D':'expD_spatial','E':'expE_temporal','F':'expF_covariance'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj): p.write_text(json.dumps(obj,indent=2,allow_nan=False))

def setup():
 artifact=ROOT/'candidate/artifacts/exp010_stage1_madrid.pkl'
 assert sha(artifact)=='2f4dc0f7a84ea54e967d7a96573b349331e1777ddb0a4a46e4925cad7bd6d266'
 st=load_stage1_artifact(artifact); data=ROOT/'data/preprocessed/preprocessed_data.pkl'
 assert sha(data)==st['source_data_sha256']
 with data.open('rb') as f: d=pickle.load(f)
 assert d['feature_names']==st['feature_names']
 assert np.isfinite(d['X_amsterdam']).all()
 return st,d

def representation(st,d,k,temporal=False):
 ix=np.sort(np.argsort(st['feature_importances'])[::-1][:k]); w=np.asarray(st['metric_weights'])[ix]
 M=d['X_madrid'][:,ix]*w; A=d['X_amsterdam'][:,ix]*w
 if temporal:
  names=d['feature_names']; sc=d['scaler']; blocks=[]
  for city in ['madrid','amsterdam']:
   X=d['X_'+city]; cols=[]
   for band in ['NIR','SWIR1','SWIR2']:
    i=names.index(band+'_late_mean'); j=names.index(band+'_early_mean')
    cols.append(X[:,i]*sc.scale_[i]+sc.mean_[i]-X[:,j]*sc.scale_[j]-sc.mean_[j])
   blocks.append(np.column_stack(cols))
  mu=blocks[0].mean(0); sd=blocks[0].std(0); sd=np.maximum(sd,1e-12)
  weight=np.sqrt(np.mean(np.asarray(st['feature_importances'])[ix]))
  M=np.column_stack([M,(blocks[0]-mu)/sd*weight]); A=np.column_stack([A,(blocks[1]-mu)/sd*weight])
 delta=np.stack([M[d['y_madrid']==c].mean(0)-M.mean(0) for c in CLS])
 if not temporal and k in [30,45]:
  np.testing.assert_allclose(delta,st['representations'][str(k)]['madrid_class_offsets'],rtol=0,atol=1e-12)
  delta=np.asarray(st['representations'][str(k)]['madrid_class_offsets'])
 return A,delta

def probs(dist,temp):
 logits=-dist/temp; logits-=logits.max(1,keepdims=True); v=np.exp(logits); return v/v.sum(1,keepdims=True)
def predict(Zs,ys,Zq,delta,lam=0,alpha=None,metric='euclidean'):
 # Deliberately no query-label argument; no query distribution estimation.
 centre=Zs.mean(0); local=np.stack([Zs[ys==c].mean(0) for c in CLS])
 P=centre+lam*delta+(1-lam)*(local-centre)
 residual=Zs-np.stack([local[np.flatnonzero(CLS==c)[0]] for c in ys])
 def dist(proto):
  return (Zq**2).sum(1)[:,None]-2*Zq@proto.T+(proto**2).sum(1)[None,:]
 if alpha is not None:
  temp=max(float(np.mean(np.sum(residual**2,axis=1))),1e-12)
  p=alpha*probs(dist(centre+delta),temp)+(1-alpha)*probs(dist(local),temp)
  return CLS[p.argmax(1)]
 if metric!='euclidean':
  C=residual.T@residual/max(len(ys)-4,1); k=C.shape[0]
  if metric=='diagonal': V=np.diag(1/np.maximum(np.diag(C),1e-8))
  else: V=np.linalg.inv(.5*C+.5*np.trace(C)/k*np.eye(k)+1e-8*np.eye(k))
  dd=np.stack([np.einsum('ij,jk,ik->i',Zq-p,V,Zq-p,optimize=True) for p in P],axis=1)
 else: dd=dist(P)
 return CLS[dd.argmin(1)]

def configurations(branch,b):
 k,lam=SUPPORTED_SCHEDULE[b]
 if branch=='A': return {f'alpha_{a:.2f}':dict(k=k,alpha=a) for a in [0,.25,.5,.75,1]}
 if branch=='B': return {'all60_l0':dict(k=60,lam=0),'compact_l0':dict(k=k,lam=0),'all60_l04':dict(k=60,lam=.4),'compact_l04':dict(k=k,lam=.4),'compact_l06':dict(k=k,lam=.6)}
 if branch=='C': return {'joint_control':dict(k=60,lam=0),'compact_local':dict(k=k,lam=0)}
 if branch=='D': return {'alpha_0.50':dict(k=k,alpha=.5)}
 if branch=='E': return {'temporal3':dict(k=k,lam=lam,temporal=True)}
 if branch=='F': return {m:dict(k=k,metric=m) for m in ['euclidean','diagonal','regularized']}
 raise ValueError(branch)

def spatial_episodes(d):
 ids=np.asarray(d['pixel_ids_amsterdam']); x=ids[:,0]; cut=float(np.median(x)); y=d['y_amsterdam']; rng=np.random.default_rng(31337); eps={}; queries={}
 for t in range(10):
  support_region=x<=cut if t%2==0 else x>cut
  q=np.flatnonzero(x>cut+10 if t%2==0 else x<cut-10)
  pools={c:np.flatnonzero(support_region&(y==c)) for c in CLS}
  assert all(len(p)>=200 for p in pools.values()),'Insufficient spatial support'
  assert set(np.unique(y[q]))==set(CLS),'Missing spatial query class'
  perms={c:rng.permutation(p)[:200] for c,p in pools.items()}
  eps[t]={b:np.concatenate([perms[c][:b] for c in CLS]) for b in BUD}; queries[t]=q
 return eps,queries,{'key':'px_key','cut':cut,'buffer_key_units':10,'support_side':'alternates by trial parity','pixel_ids_shape':list(ids.shape),'coordinate_min':ids.min(0).tolist(),'coordinate_max':ids.max(0).tolist(),'units':'coordinate-key units; not assumed metres'}

def main():
 branch=sys.argv[1]; repeat='--repeat' in sys.argv
 folder=OUT/FOLDERS[branch]; folder.mkdir(exist_ok=True)
 suffix='_repeat' if repeat else ''
 assert not (folder/f'results{suffix}.json').exists(),'Refusing to overwrite evidence'
 t0=time.perf_counter(); st,d=setup(); X=d['X_amsterdam']; y=d['y_amsterdam']; n=len(y)
 budgets=[5,25,200] if branch=='E' else BUD
 eps=episodes(y,31337,10); queries=None; spatial=None
 if branch=='D': eps,queries,spatial=spatial_episodes(d)
 config={'branch':branch,'seed':31337,'trials':list(range(10)),'budgets':budgets,'protocol':'EXP010 nested support / complement query' if branch!='D' else 'fixed spatial split; see spatial','spatial':spatial,'data_sha256':st['source_data_sha256'],'artifact_sha256':sha(ROOT/'candidate/artifacts/exp010_stage1_madrid.pkl'),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(OUT/'PLAN.md'),'python':platform.python_version(),'numpy':np.__version__,'sklearn':sklearn.__version__,'population_sd_ddof':0,'selection':'NONE; all arms predeclared; audit reused for evaluation only','configurations':{b:configurations(branch,b) for b in budgets},'feature_representation':'Madrid-standardized 60 features, sqrt RF importance weighted, compact Madrid ranking','baseline':'frozen artifact interface; exact schedule'}
 save(folder/f'configuration{suffix}.json',config)
 reps={}; records=[]; payload={}
 frozen=json.loads((ROOT/'candidate/artifacts/joint_sweep.json').read_text())
 for t in range(10):
  for b in budgets:
   sup=eps[t][b]; qm=np.ones(n,bool); qm[sup]=False; q=np.flatnonzero(qm) if queries is None else queries[t]
   assert not np.intersect1d(sup,q).size
   ys=y[sup].copy(); predictions={'EXP010':adapt_and_predict(st,X[sup],ys,X[q],b,31337)}
   for name,cfg in configurations(branch,b).items():
    cfg=cfg.copy(); k=cfg.pop('k'); temporal=cfg.pop('temporal',False); key=(k,temporal)
    if key not in reps: reps[key]=representation(st,d,k,temporal)
    Z,delta=reps[key]; predictions[name]=predict(Z[sup],ys,Z[q],delta,**cfg)
   # Labels sliced only after every arm has predicted this episode.
   yq=y[q]; tag=f'b{b}_t{t}'; payload[tag+'_support']=sup; payload[tag+'_query']=q
   base=float(f1_score(yq,predictions['EXP010'],labels=CLS,average='macro',zero_division=0))
   if branch!='D': np.testing.assert_allclose(base,frozen['audit'][str(b)]['tuned_trials'][t],rtol=0,atol=1e-12)
   for name,pred in predictions.items():
    payload[tag+'_'+name]=pred
    cm=confusion_matrix(yq,pred,labels=CLS); pc=f1_score(yq,pred,labels=CLS,average=None,zero_division=0); score=float(pc.mean())
    records.append({'budget':b,'trial':t,'seed':31337,'method':name,'macro_f1':score,'delta_vs_EXP010':score-base,'class_f1':pc.tolist(),'confusion':cm.tolist(),'confusion_row_normalized':(cm/np.maximum(cm.sum(1,keepdims=True),1)).tolist(),'support_counts':[int((ys==c).sum()) for c in CLS],'query_counts':cm.sum(1).tolist()})
 summary={}
 for b in budgets:
  summary[b]={}
  for name in ['EXP010',*configurations(branch,b)]:
   r=[r for r in records if r['budget']==b and r['method']==name]; scores=np.array([v['macro_f1'] for v in r]); delta=np.array([v['delta_vs_EXP010'] for v in r])
   summary[b][name]={'mean':float(scores.mean()),'population_sd':float(scores.std()),'paired_deltas':delta.tolist(),'mean_delta':float(delta.mean()),'delta_population_sd':float(delta.std()),'wins':int((delta>1e-12).sum()),'losses':int((delta< -1e-12).sum()),'ties':int((abs(delta)<=1e-12).sum())}
 np.savez_compressed(folder/f'predictions{suffix}.npz',**payload)
 result={'configuration':config,'episodes':records,'summary':summary,'runtime_seconds':time.perf_counter()-t0}
 save(folder/f'results{suffix}.json',result)
 if repeat:
  before=json.loads((folder/'results.json').read_text()); assert before['episodes']==records; assert before['summary']==json.loads(json.dumps(summary))
  with np.load(folder/'predictions.npz') as original:
   assert set(original.files)==set(payload)
   for key,val in payload.items(): assert np.array_equal(original[key],val),key
  save(folder/'reproducibility.json',{'pass':True,'command':f'python -I -B candidate/experiments_2h/run.py {branch} --repeat','exact_prediction_arrays_checked':len(payload),'episodes_equal':True,'runtime_seconds':result['runtime_seconds']})
 lines=['# EXP-'+branch,'','See ../PLAN.md for the predeclared method and information-access boundaries.','',f'Run: `python -I -B candidate/experiments_2h/run.py {branch}`; clean repeat: append `--repeat`.','Existing results are never overwritten. To rerun elsewhere copy the sprint code without generated outputs.','', '| Budget | Method | Mean | Population SD | Delta vs EXP010 | W/L/T |','|---|---|---:|---:|---:|---|']
 for b,methods in summary.items():
  for name,r in methods.items(): lines.append(f"| {b} | {name} | {r['mean']:.6f} | {r['population_sd']:.6f} | {r['mean_delta']:+.6f} | {r['wins']}/{r['losses']}/{r['ties']} |")
 if not repeat: (folder/'README.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'branch':branch,'repeat':repeat,'runtime_seconds':result['runtime_seconds'],'summary':summary},indent=2))
if __name__=='__main__':
 with threadpool_limits(limits=1): main()
