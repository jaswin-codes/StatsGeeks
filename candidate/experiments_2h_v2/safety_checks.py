"""Fresh-process source refit + mathematical/data-access tests for >.70 audit."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,json,inspect,hashlib
import numpy as np
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import *
from candidate.experiments_2h.run import setup,save

def main():
 out=H/'safety_checks.json';assert not out.exists();st,d=setup();M,A=d['X_madrid'],d['X_amsterdam'];ym=d['y_madrid'];y=d['y_amsterdam'];rng=np.random.default_rng(99381);s=np.concatenate([rng.choice(np.flatnonzero(y==c),5,False)for c in C]);ys=y[s].copy()
 # Models receive only S,y_support,Q. A query-label permutation cannot enter their API.
 lp,rp=support_models(A[s],ys,A); perm=rng.permutation(len(A));l2,r2=support_models(A[s],ys,A[perm]);inv=np.argsort(perm)
 np.testing.assert_allclose(lp,l2[inv],atol=1e-12,rtol=0);np.testing.assert_allclose(rp,r2[inv],atol=1e-12,rtol=0)
 nn=neighbours(d['pixel_ids_amsterdam']);sm=smooth(rp,nn);assert np.isfinite(sm).all();np.testing.assert_allclose(sm.sum(1),1,atol=1e-12)
 source=rf().fit(align_source(M,A),ym).predict_proba(A);original=np.load(H/'source_coral_prob.npy');err=float(np.max(np.abs(source-original)));np.testing.assert_allclose(source,original,atol=1e-12,rtol=0);assert np.array_equal(source.argmax(1),original.argmax(1));np.save(H/'source_coral_prob_repeat.npy',source)
 manifest=json.loads((R/'candidate/competitor_forensics/protected_before.json').read_text());changed=[p for p,h in manifest.items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
 save(out,{'pass':not changed,'source_prob_max_abs_clean_refit_difference':err,'source_predictions_identical':True,'query_row_permutation_equivariance':True,'target_labels_only_support_API':str(inspect.signature(support_models)),'true_label_anchoring':False,'smoothed_probability_normalization':True,'frozen_changed_files':changed,'query_labels_role':'evaluation and stratified sampling only; source fitting has no target labels','caveat':'audit-based configuration selection is not an untouched target holdout; pool statistics and spatial neighbours are transductive'})
 print('PASS',flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
