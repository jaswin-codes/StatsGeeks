"""Standalone clean replay of the LOCKED method. No historical model/cache required.
Example from repository root:
 .venv_baseline/Scripts/python.exe -I -B candidate/experiments_2h_v2/reproduce_locked.py --outdir candidate/astra_replay_001
Choose a NEW output directory for each invocation; historical evidence is never overwritten.
"""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,argparse,json,pickle,time
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from astra_agf import fit_pool,adapt_and_predict
from candidate.experiments_2h.run import setup,save,sha
from candidate.joint_sweep import episodes

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--outdir',required=True,type=Path);parser.add_argument('--trials',type=int,default=100);parser.add_argument('--seed',type=int,default=104729);args=parser.parse_args();assert args.trials>0;args.outdir.mkdir(parents=True,exist_ok=False)
 cfg=json.loads((H/'FINAL_SELECTION.json').read_text())
 for f,h in cfg['files_sha256'].items():assert sha(H/f)==h,f
 start=time.time();st,d=setup()
 # All source training is recomputed. NO target truth is an argument to fit_pool.
 state=fit_pool(d['X_madrid'],d['y_madrid'],d['pixel_ids_madrid'],d['X_amsterdam'],d['pixel_ids_amsterdam'],d['scaler'].mean_,d['scaler'].scale_)
 if (H/'physical_source_priors.npz').exists():np.testing.assert_array_equal(state['prior'],np.load(H/'physical_source_priors.npz')['physical1'])
 print('source rebuilt from scratch',flush=True);y=d['y_amsterdam'];eps=episodes(y,args.seed,args.trials);records=[];arrays={}
 for t in range(args.trials):
  for b in [5,25,50,100,200]:
   s=eps[t][b];q=np.setdiff1d(np.arange(len(y)),s);p=adapt_and_predict(state,s,y[s].copy(),b)[q];pc=f1_score(y[q],p,labels=[1,2,3,4],average=None,zero_division=0);records.append({'budget':b,'trial':t,'f1':float(pc.mean()),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=[1,2,3,4]).tolist()});tag=f'b{b}_t{t}';arrays[tag+'_s']=s;arrays[tag+'_q']=q;arrays[tag+'_pred']=p
  print('episode',t+1,'/',args.trials,flush=True)
 checked=0
 if args.seed==104729 and(H/'final_100.npz').exists():
  with np.load(H/'final_100.npz')as ref:
   for t in range(min(100,args.trials)):
    for b in [5,25,50,100,200]:
     tag=f'b{b}_t{t}'
     for new,old in [('_s','_s'),('_q','_q'),('_pred','_ASTRA_AGF')]:np.testing.assert_array_equal(arrays[tag+new],ref[tag+old]);checked+=1
 summary={b:{'mean':float(np.mean([r['f1']for r in records if r['budget']==b])),'sd':float(np.std([r['f1']for r in records if r['budget']==b]))}for b in [5,25,50,100,200]}
 np.savez_compressed(args.outdir/'predictions.npz',**arrays)
 save(args.outdir/'run.json',{'pass':True,'source_trained_from_scratch':True,'target_labels_in_source_fit':False,'recipe':cfg,'seed':args.seed,'trials_per_budget':args.trials,'records':records,'summary':summary,'reference_arrays_exact':checked,'seconds':time.time()-start,'script_sha':sha(Path(__file__))})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
