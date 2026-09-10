from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,json
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import rf
from candidate.experiments_2h.run import setup,save
st,d=setup();z=np.load(H/'audit.npz');s=z['b25_t0_s'];q=z['b25_t0_q'];a=z['b25_t0_RF60'];z2=np.load(H/'audit_repeat.npz');j=np.flatnonzero(a!=z2['b25_t0_RF60']);model=rf().fit(d['X_amsterdam'][s],d['y_amsterdam'][s]);X=d['X_amsterdam'][q[j]]
p4=np.array([model.predict_proba(X)for _ in range(30)]);model.n_jobs=1;p1=np.array([model.predict_proba(X)for _ in range(3)]);assert np.array_equal(p1[0],p1[1]) and np.array_equal(p1[0],p1[2])
with np.load(H/'audit.npz')as x,np.load(H/'audit_repeat.npz')as y:
 keys=[k for k in x.files if k.endswith('RF60_smooth')or k.endswith('H_mean')];same=all(np.array_equal(x[k],y[k])for k in keys)
save(H/'tie_audit.json',{'differing_example_query_indices':q[j].tolist(),'parallel_probabilities':p4.tolist(),'serial_probabilities':p1.tolist(),'parallel_class_predictions':(p4.argmax(2)+1).tolist(),'serial_repeats_identical':True,'max_top_two_margin':float(np.max(np.diff(np.sort(p4,axis=2)[:,:,-2:],axis=2))),'strong_candidates_exact_arrays_checked':len(keys),'strong_candidate_arrays_identical':same,'interpretation':'n_jobs=4 reduction order creates machine-epsilon argmax ambiguity at exact forest ties. Stage2 uses serial prediction aggregation, parallel tree fitting. Historical runs retained.'})
print('strong arrays',same,'parallel classes',np.unique(p4.argmax(2)),flush=True)
