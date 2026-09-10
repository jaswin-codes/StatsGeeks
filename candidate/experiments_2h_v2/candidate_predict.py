"""ASTRA-AGF public transductive interface. No target-truth argument in pool fitting.
Input60 columns must already use the supplied Madrid scaler/order. Rebuild the pool
state for a different target population; it is NOT an inductive EXP-010 replacement API.
"""
import hashlib
import numpy as np
from scipy.spatial import cKDTree
from models import C,align_source,power
from stage2_models import forest,immediate_grid,conditional_step
BUDGETS=(5,25,50,100,200)

def _matrix(X,ncols=60):
 X=np.asarray(X,dtype=float)
 if X.ndim!=2 or X.shape[1]!=ncols or not np.isfinite(X).all():raise ValueError('Finite n x60 matrix required')
 return X

def _coords(X,n):
 X=np.asarray(X)
 if X.shape!=(n,2)or not np.isfinite(X).all()or not np.equal(X,np.round(X)).all():raise ValueError('Integer unit-lattice pixel keys required')
 if len(np.unique(X,axis=0))!=n:raise ValueError('Duplicate pixel keys')
 return X

def pool_hash(X,coords):
 h=hashlib.sha256();h.update(np.ascontiguousarray(X,dtype='<f8').tobytes());h.update(np.ascontiguousarray(coords,dtype='<i8').tobytes());return h.hexdigest()

def fit_pool(source_features,source_labels,source_coords,target_features,target_coords,
             source_mean,source_scale,*,source_basis,local_leaf=2,
             aligned_source_model=None,aligned_model_pool_hash=None):
 """Source labels + full UNLABELLED target covariates/coordinates only.
 An externally saved aligned_source_model may be reused ONLY with an explicit
 matching pool hash. Otherwise learn global+one-step pseudo-class alignment here.
 """
 if source_basis not in ('standardized','physical')or local_leaf not in (1,2):raise ValueError('Unsupported frozen recipe')
 M=_matrix(source_features);A=_matrix(target_features);cm=_coords(source_coords,len(M));ca=_coords(target_coords,len(A));ym=np.asarray(source_labels)
 if ym.shape!=(len(M),)or not np.array_equal(np.unique(ym),C):raise ValueError('All four source classes required')
 scale=np.asarray(source_scale);mean=np.asarray(source_mean)
 if scale.shape!=(60,)or mean.shape!=(60,)or not np.isfinite(scale).all()or not np.isfinite(mean).all()or (scale<=0).any():raise ValueError('Invalid Madrid scaler')
 raw=A*scale+mean;fingerprint=pool_hash(A,ca)
 source_X=M if source_basis=='standardized'else M*scale+mean;target_X=A if source_basis=='standardized'else raw
 Xm=np.column_stack([source_X,immediate_grid(cm)@source_X]);Xa=np.column_stack([target_X,immediate_grid(ca)@target_X])
 if aligned_source_model is None:
  T=align_source(Xm,Xa);first=forest().fit(T,ym);T,_=conditional_step(T,ym,Xa,first);model=forest().fit(T,ym)
 else:
  if aligned_model_pool_hash!=fingerprint:raise ValueError('Aligned source model belongs to a different or undocumented pool')
  model=aligned_source_model
 if not np.array_equal(model.classes_,C):raise ValueError('Source probability class ordering mismatch')
 prior=model.predict_proba(Xa);cov=np.cov(raw,rowvar=False);representations={}
 for b in BUDGETS:
  rho=min(1,60/(4*b));use=(1-rho)*cov+rho*np.diag(np.diag(cov))+1e-7*np.eye(60);representations[b]=(raw-raw.mean(0))@power(use,-.5)
 dist,nn=cKDTree(ca).query(ca,k=9);weights=np.exp(-dist**2/2);weights/=weights.sum(1,keepdims=True)
 return {'method':'ASTRA-AGF','source_basis':source_basis,'local_leaf':local_leaf,'pool_hash':fingerprint,'representations':representations,'prior':prior,'neighbours':nn,'weights':weights,'classes':C.copy(),'information_regime':'transductive; full pool moments, source pseudo-labels, feature/prediction neighbours; no true target labels'}

def adapt_and_predict(pool_state,support_indices,support_labels,budget,return_proba=False):
 """Return predictions for EVERY row of the bound pool, never anchored to truth.
 Caller excludes support rows from query scoring. Labels are support-only.
 """
 if budget not in BUDGETS:raise ValueError('Unsupported budget')
 s=np.asarray(support_indices);ys=np.asarray(support_labels);Z=pool_state['representations'][budget]
 if s.ndim!=1 or s.dtype.kind not in 'iu'or ys.shape!=s.shape or len(s)!=4*budget or len(np.unique(s))!=len(s)or(s<0).any()or(s>=len(Z)).any():raise ValueError('Invalid support indices or count')
 if not np.array_equal(np.unique(ys),C)or any(np.sum(ys==c)!=budget for c in C):raise ValueError('Exactly budget labels per class required')
 model=forest().set_params(min_samples_leaf=pool_state['local_leaf']).fit(Z[s],ys);local=model.predict_proba(Z);alpha=20/(20+len(s));field=alpha*pool_state['prior']+(1-alpha)*local
 probability=np.sum(field[pool_state['neighbours']]*pool_state['weights'][:,:,None],axis=1);pred=C[probability.argmax(1)]
 return (pred,probability)if return_proba else pred
