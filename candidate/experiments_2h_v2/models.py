"""Independent implementations. No target/query-label argument except support y.
Source geometry and full unlabelled target statistics are explicitly separate.
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import softmax
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
C=np.array([1,2,3,4])
def rf():
 return RandomForestClassifier(n_estimators=200,min_samples_leaf=2,class_weight='balanced',max_features='sqrt',random_state=42,n_jobs=4)
def power(A,p):
 v,U=np.linalg.eigh(A); return (U*np.maximum(v,1e-7)**p)@U.T
def residual_cov(X,y):
 means=np.array([X[y==c].mean(0) for c in C]); E=X-means[np.searchsorted(C,y)]
 return E.T@E/max(len(y)-4,1)
def regularize(A):
 return .5*A+(.5*np.trace(A)/len(A)+1e-8)*np.eye(len(A))
def align_source(M,A):
 cm=np.cov(M,rowvar=False)+1e-5*np.eye(M.shape[1]); ca=np.cov(A,rowvar=False)+1e-5*np.eye(A.shape[1])
 return (M-M.mean(0))@power(cm,-.5)@power(ca,.5)+A.mean(0)
def metric_prob(S,y,Q,V,offset=None,lam=0):
 means=np.array([S[y==c].mean(0) for c in C]); means=(1-lam)*means+lam*(S.mean(0)+offset) if lam else means
 D=np.array([np.einsum('ij,ij->i',(Q-m)@V,Q-m) for m in means]).T
 # Same mean residual distance temperature in each metric; no query statistics.
 R=S-np.array([S[y==c].mean(0) for c in C])[np.searchsorted(C,y)]
 temp=max(float(np.einsum('ij,ij->i',R@V,R).mean()),1e-8)
 return softmax(-D/temp,axis=1)
def neighbours(coords):
 dist,ids=cKDTree(coords).query(coords,k=9)
 return ids
def smooth(P,ids): return P[ids].mean(1)
def support_models(S,y,Q):
 lr=LogisticRegression(C=1,max_iter=1000,random_state=42).fit(S,y)
 forest=rf().fit(S,y)
 return lr.predict_proba(Q),forest.predict_proba(Q)
