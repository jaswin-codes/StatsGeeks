"""Unpromoted EXP-F regularized prototype: source artifact + support, no query labels.

Fixed metric for ALL budgets, no post-audit hybrid schedule. Input is already
Madrid-standardized 60-feature data in the frozen ordered schema.
"""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,argparse,hashlib
import numpy as np
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'candidate'))
from exp010_predict import load_stage1_artifact,SUPPORTED_SCHEDULE

def predict(stage1,support_X,support_y,query_X,shots):
 if shots not in SUPPORTED_SCHEDULE:raise ValueError('Unsupported budget')
 S=np.asarray(support_X,dtype=float); Q=np.asarray(query_X,dtype=float); ys=np.asarray(support_y)
 if S.shape!=(4*shots,60) or Q.ndim!=2 or Q.shape[1]!=60 or not len(Q):raise ValueError('Invalid feature shapes')
 if ys.shape!=(len(S),) or not np.isfinite(S).all() or not np.isfinite(Q).all():raise ValueError('Invalid labels or nonfinite features')
 classes=np.asarray(stage1['classes'])
 if any(np.count_nonzero(ys==c)!=shots for c in classes):raise ValueError('Expected balanced support')
 k=SUPPORTED_SCHEDULE[shots][0]; ix=np.asarray(stage1['representations'][str(k)]['selected_feature_idx']);w=np.asarray(stage1['metric_weights'])[ix]
 S=S[:,ix]*w; Q=Q[:,ix]*w; P=np.stack([S[ys==c].mean(0) for c in classes])
 residual=S-np.stack([P[np.flatnonzero(classes==c)[0]] for c in ys]); C=residual.T@residual/(len(S)-4)
 V=np.linalg.inv(.5*C+.5*np.trace(C)/k*np.eye(k)+1e-8*np.eye(k))
 dd=np.stack([np.einsum('ij,jk,ik->i',Q-p,V,Q-p,optimize=True) for p in P],axis=1)
 return classes[dd.argmin(1)]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--artifact',type=Path,required=True);p.add_argument('--support',type=Path,required=True);p.add_argument('--query',type=Path,required=True);p.add_argument('--shots',type=int,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 assert hashlib.sha256(args.artifact.read_bytes()).hexdigest()=='2f4dc0f7a84ea54e967d7a96573b349331e1777ddb0a4a46e4925cad7bd6d266'
 st=load_stage1_artifact(args.artifact)
 with np.load(args.support,allow_pickle=False) as f:
  assert set(f.files)=={'X','y','feature_names'}
  S=f['X'];ys=f['y'];assert f['feature_names'].tolist()==st['feature_names']
 with np.load(args.query,allow_pickle=False) as f:
  # Reject labels rather than merely ignoring them.
  assert set(f.files)=={'X','feature_names'},'Query must contain features/schema ONLY'
  Q=f['X'];assert f['feature_names'].tolist()==st['feature_names']
 assert not args.output.exists(),'Refusing overwrite'
 np.save(args.output,predict(st,S,ys,Q,args.shots),allow_pickle=False)
if __name__=='__main__':
 with threadpool_limits(limits=1): main()
