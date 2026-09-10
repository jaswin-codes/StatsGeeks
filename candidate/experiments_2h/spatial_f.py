"""Fixed spatial follow-up for every EXP-F arm. See SPATIAL_ADDENDUM.md."""
from pathlib import Path
import sys,time,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run as r
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits

def main():
 t0=time.perf_counter(); repeat='--repeat' in sys.argv; suffix='_repeat' if repeat else ''
 folder=HERE/'expF_covariance/spatial'; folder.mkdir(exist_ok=True)
 assert not (folder/f'results{suffix}.json').exists()
 st,d=r.setup(); X=d['X_amsterdam']; y=d['y_amsterdam']; eps,queries,spatial=r.spatial_episodes(d)
 config={'seed':31337,'trials':list(range(10)),'budgets':r.BUD,'spatial':spatial,'configurations':{b:r.configurations('F',b) for b in r.BUD},'data_sha256':st['source_data_sha256'],'script_sha256':r.sha(Path(__file__)),'shared_script_sha256':r.sha(HERE/'run.py'),'addendum_sha256':r.sha(HERE/'expF_covariance/SPATIAL_ADDENDUM.md'),'selection':'none; all predeclared F arms','purpose':'exploratory robustness; not independent confirmation','population_sd_ddof':0}
 r.save(folder/f'configuration{suffix}.json',config)
 records=[]; payload={}; reps={k:r.representation(st,d,k) for k in [30,45]}
 for t in range(10):
  for b in r.BUD:
   sup=eps[t][b]; q=queries[t]; ys=y[sup]; assert not np.intersect1d(sup,q).size
   predictions={'EXP010':r.adapt_and_predict(st,X[sup],ys,X[q],b,31337)}
   for name,cfg in r.configurations('F',b).items():
    Z,delta=reps[cfg['k']]; predictions[name]=r.predict(Z[sup],ys,Z[q],delta,metric=cfg['metric'])
   yq=y[q]; base=f1_score(yq,predictions['EXP010'],labels=r.CLS,average='macro',zero_division=0)
   tag=f'b{b}_t{t}'; payload[tag+'_support']=sup; payload[tag+'_query']=q
   for name,pred in predictions.items():
    payload[tag+'_'+name]=pred; cm=confusion_matrix(yq,pred,labels=r.CLS); pc=f1_score(yq,pred,labels=r.CLS,average=None,zero_division=0)
    records.append({'budget':b,'trial':t,'seed':31337,'method':name,'macro_f1':float(pc.mean()),'delta_vs_EXP010':float(pc.mean()-base),'class_f1':pc.tolist(),'confusion':cm.tolist(),'confusion_row_normalized':(cm/cm.sum(1,keepdims=True)).tolist(),'support_counts':[int((ys==c).sum()) for c in r.CLS],'query_counts':cm.sum(1).tolist()})
 summary={}
 for b in r.BUD:
  summary[b]={}
  for name in ['EXP010','euclidean','diagonal','regularized']:
   rows=[x for x in records if x['budget']==b and x['method']==name]; scores=np.array([x['macro_f1'] for x in rows]); delta=np.array([x['delta_vs_EXP010'] for x in rows])
   summary[b][name]={'mean':float(scores.mean()),'population_sd':float(scores.std()),'paired_deltas':delta.tolist(),'mean_delta':float(delta.mean()),'delta_population_sd':float(delta.std()),'wins':int((delta>1e-12).sum()),'losses':int((delta< -1e-12).sum()),'ties':int((abs(delta)<=1e-12).sum())}
 result={'configuration':config,'episodes':records,'summary':summary,'runtime_seconds':time.perf_counter()-t0}
 r.save(folder/f'results{suffix}.json',result); np.savez_compressed(folder/f'predictions{suffix}.npz',**payload)
 if repeat:
  old=json.loads((folder/'results.json').read_text()); assert old['episodes']==records; assert old['summary']==json.loads(json.dumps(summary))
  with np.load(folder/'predictions.npz') as original:
   assert set(original.files)==set(payload)
   for key,value in payload.items(): assert np.array_equal(original[key],value),key
  r.save(folder/'reproducibility.json',{'pass':True,'exact_prediction_arrays_checked':len(payload),'episodes_equal':True,'command':'python -I -B candidate/experiments_2h/spatial_f.py --repeat','runtime_seconds':result['runtime_seconds']})
 print(json.dumps(summary,indent=2))
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
