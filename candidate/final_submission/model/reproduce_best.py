"""Pool-bound inference or cached-reference replay, without loading query truth.
python -I -B reproduce_best.py --support support.npz --out NEW_DIRECTORY
python -I -B reproduce_best.py --verify --out NEW_DIRECTORY
Support NPZ fields: indices, labels, budget (scalar). Optional query indices.
Full ordered pool is prebound to the trusted, hash-checked local artifact.
"""
from pathlib import Path
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys,json,pickle,hashlib,argparse,time
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import numpy as np
from threadpoolctl import threadpool_limits
from agf_model import probabilities,CLASSES,BUDGETS

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--support',type=Path);g.add_argument('--verify',action='store_true');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    manifest=json.loads((H/'INFERENCE_MANIFEST.json').read_text())
    for name,expected in manifest['files'].items():
        if digest(H/name)!=expected:raise ValueError('Artifact hash mismatch: '+name)
    lock=json.loads((H/'SELECTION_LOCK.json').read_text())
    # Only deserialize trusted local files after checking their published hashes.
    with (H/'pool_state.pkl').open('rb') as f:state=pickle.load(f)
    if state['feature_names']!=manifest['feature_names']:raise ValueError('Feature order mismatch')
    a.out.mkdir(parents=True,exist_ok=False);started=time.time();checks=0
    if a.verify:
        reference=H/'verification_inputs'
        for b in BUDGETS:
            with np.load(reference/f'b{b}.npz',allow_pickle=False) as r:
                pp=probabilities(state,r['support'],r['support_labels'],b,lock['config']);pred=CLASSES[pp.argmax(1)]
                np.testing.assert_array_equal(pred[r['query']],r['expected'])
                np.savez_compressed(a.out/f'b{b}.npz',prediction=pred,probability=pp);checks+=1
    else:
        with np.load(a.support,allow_pickle=False) as r:
            b=r['budget'].item()
            if isinstance(b,bool) or not isinstance(b,int) or b not in BUDGETS:raise ValueError('Budget must be a supported integer')
            s=r['indices'];ys=r['labels'];pp=probabilities(state,s,ys,b,lock['config']);pred=CLASSES[pp.argmax(1)]
            if 'query' in r.files:
                q=r['query']
                if q.ndim!=1 or q.dtype.kind not in 'iu' or len(np.unique(q))!=len(q) or (q<0).any() or (q>=len(pred)).any() or np.intersect1d(s,q).size:raise ValueError('Invalid/overlapping query indices')
            else:q=np.setdiff1d(np.arange(len(pred)),s)
            np.savez_compressed(a.out/'predictions.npz',query=q,prediction=pred[q],probability=pp[q])
    metadata=dict(candidate=lock['candidate'],config=lock['config'],pool_sha256=digest(H/'pool_state.pkl'),classes=CLASSES.tolist(),feature_names=state['feature_names'],query_labels_used=False,target_features_used=True,coordinates_used=True,support_labels_used=True,exact_verification_arrays=checks,seconds=time.time()-started)
    (a.out/'metadata.json').write_text(json.dumps(metadata,indent=2));print(json.dumps(metadata,indent=2))

if __name__=='__main__':
    with threadpool_limits(limits=1):main()
