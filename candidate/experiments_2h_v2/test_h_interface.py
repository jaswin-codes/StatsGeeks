from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,pickle
import numpy as np
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from candidate.experiments_2h.run import setup,save
from h_predict import fit_source,adapt_and_predict
with threadpool_limits(limits=1):
 st,d=setup();state=fit_source(st,d['X_madrid'],d['y_madrid']);count=0
 for mode in ['audit','fresh','spatial']:
  data=np.load(H/(mode+'.npz'))
  for t in [0,9]:
   for b in [5,25,50,100,200]:
    tag=f'b{b}_t{t}';s=data[tag+'_s'];q=data[tag+'_q'];p=adapt_and_predict(state,d['X_amsterdam'][s],d['y_amsterdam'][s],d['X_amsterdam'][q],b);np.testing.assert_array_equal(p,data[tag+'_H_mean']);count+=1
 # No-query-fitting contract: a query can be predicted singly or in any other batch.
 s=data['b200_t9_s'];q=data['b200_t9_q'];batch=adapt_and_predict(state,d['X_amsterdam'][s],d['y_amsterdam'][s],d['X_amsterdam'][q[:20]],200)
 for j in range(20):np.testing.assert_array_equal(batch[j:j+1],adapt_and_predict(state,d['X_amsterdam'][s],d['y_amsterdam'][s],d['X_amsterdam'][q[j:j+1]],200))
 with(H/'h_source_state.pkl').open('wb')as f:pickle.dump(state,f)
 save(H/'h_interface_reproduction.json',{'pass':True,'exact_episode_arrays':count,'inductive_query_batch_invariance_checks':20,'target_pool_statistics':False})
 print('PASS',count,flush=True)
