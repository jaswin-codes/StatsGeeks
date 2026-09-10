"""Optional expensive source-state verification, never optimization. Not run in Phase 2.
python -B candidate/publication/verify_source.py --out NEW_DIRECTORY
"""
from pathlib import Path
import os
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[k]='1'
import sys,argparse,pickle,json,hashlib,time
import numpy as np
from threadpoolctl import threadpool_limits
R=Path(__file__).resolve().parents[2];B=R/'candidate/best_model'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    manifest=json.loads((B/'INFERENCE_MANIFEST.json').read_text())
    for n,h in manifest['files'].items():assert sha(B/n)==h,n
    protected=json.loads((B/'provenance.json').read_text())['protected'];data=R/'data/preprocessed/preprocessed_data.pkl'
    expected=next(v for k,v in protected.items() if k.replace('\\','/').endswith('preprocessed_data.pkl'));assert sha(data)==expected
    args.out.mkdir(parents=True,exist_ok=False)
    with data.open('rb') as f:d=pickle.load(f)
    # The historical container also contains target truth; remove it before any model call.
    d.pop('y_amsterdam',None)
    with (B/'pool_state.pkl').open('rb') as f:old=pickle.load(f)
    sys.path.insert(0,str(B));from agf_model import fit_pool
    start=time.perf_counter()
    with threadpool_limits(limits=1):new=fit_pool(d['X_madrid'],d['y_madrid'],d['pixel_ids_madrid'],d['X_amsterdam'],d['pixel_ids_amsterdam'],d['scaler'].mean_,d['scaler'].scale_,d['feature_names'])
    keys=['raw','standard','coords','prior','cov','nn','dist','classes']
    for k in keys:np.testing.assert_array_equal(old[k],new[k])
    assert old['feature_names']==new['feature_names']
    (args.out/'verification.json').write_text(json.dumps(dict(passed=True,exact_state_arrays=keys,seconds=time.perf_counter()-start,query_labels_supplied_to_model=False),indent=2))
    print('Exact source-state verification passed')
if __name__=='__main__':main()
