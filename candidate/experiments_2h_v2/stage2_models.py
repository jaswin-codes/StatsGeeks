"""Independent stage2: local grid averaging and pseudo-label conditional transport.
Imports only our stage1 mathematical primitives, never competitor code.
"""
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from models import align_source,C
class DeterministicForest(RandomForestClassifier):
 """Parallel tree fitting; stable tree-order probability summation at prediction."""
 def predict_proba(self,X):
  jobs=self.n_jobs
  try:
   self.n_jobs=1
   return super().predict_proba(X)
  finally:self.n_jobs=jobs

def forest():return DeterministicForest(n_estimators=200,min_samples_leaf=2,class_weight='balanced',max_features='sqrt',random_state=42,n_jobs=4)
def immediate_grid(coords):
 # Exact lattice topology rather than unconstrained k-NN or tuned distance kernel.
 lookup={tuple(row):i for i,row in enumerate(coords)};rows=[];cols=[];weights=[]
 for i,(x,y)in enumerate(coords):
  ids=[lookup[(x+dx,y+dy)] for dx in [-1,0,1] for dy in [-1,0,1] if (x+dx,y+dy)in lookup]
  rows.extend([i]*len(ids));cols.extend(ids);weights.extend([1/len(ids)]*len(ids))
 return csr_matrix((weights,(rows,cols)),shape=(len(coords),len(coords)))
def conditional_step(transported_source,source_y,target_X,teacher):
 pseudo=teacher.predict(target_X);out=transported_source.copy();counts={}
 for c in C:
  target=target_X[pseudo==c];mask=source_y==c;counts[int(c)]=len(target)
  if len(target)>target_X.shape[1]:out[mask]=align_source(transported_source[mask],target)
 return out,counts

def predict_episode(S,ys,all_X,grid,prior,budget):
 """Deployment-ready main candidate: scalar prior weight, local forest, grid graph.
 Feature scaler belongs to source stage; all_X is unlabelled target pool including S.
 """
 model=forest().fit(S,ys);local=model.predict_proba(all_X);alpha=20/(20+4*budget)
 return grid@(alpha*prior+(1-alpha)*local)
