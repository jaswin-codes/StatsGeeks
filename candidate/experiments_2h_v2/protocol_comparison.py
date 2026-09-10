"""Validate the >.70 result under competitor's exact episode RNG reset convention.
No new model settings. Our independently implemented 60-feature candidates only.
"""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,json,time
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent; R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import *
from candidate.experiments_2h.run import setup,save
from candidate.exp010_predict import adapt_and_predict

def main():
 out=H/'competitor_protocol.json';assert not out.exists();st,d=setup();A=d['X_amsterdam'];y=d['y_amsterdam'];coords=d['pixel_ids_amsterdam'];W=power(regularize(np.cov(A,rowvar=False)),-.5);Z=(A-A.mean(0))@W;nn=neighbours(coords);records=[];arrays={};start=time.time()
 for b in [5,25,50,100,200]:
  rng=np.random.default_rng(42)
  for t in range(20):
   s=np.concatenate([rng.choice(np.flatnonzero(y==c),b,replace=False) for c in C]);q=np.setdiff1d(np.arange(len(y)),s);ys=y[s]
   raw=rf().fit(A[s],ys).predict_proba(A);pool=rf().fit(Z[s],ys).predict_proba(Z)
   predictions={'EXP010':adapt_and_predict(st,A[s],ys,A[q],b,42),'RF60_smooth':C[smooth(raw,nn)[q].argmax(1)],'pool_RF60_smooth':C[smooth(pool,nn)[q].argmax(1)]}
   arrays[f'{b}_{t}_s']=s;arrays[f'{b}_{t}_q']=q
   for m,p in predictions.items():
    pc=f1_score(y[q],p,labels=C,average=None,zero_division=0); records.append({'budget':b,'trial':t,'method':m,'f1':float(pc.mean()),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=C).tolist()});arrays[f'{b}_{t}_{m}']=p
  print(b,'done',flush=True)
 summary={b:{m:{'mean':float(np.mean([r['f1'] for r in records if r['budget']==b and r['method']==m])),'sd':float(np.std([r['f1'] for r in records if r['budget']==b and r['method']==m]))} for m in predictions}for b in [5,25,50,100,200]}
 save(out,{'records':records,'summary':summary,'seed':42,'n_trials':20,'rng':'reset per budget; choice without replacement, complement query','seconds':time.time()-start});np.savez_compressed(H/'competitor_protocol.npz',**arrays)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
