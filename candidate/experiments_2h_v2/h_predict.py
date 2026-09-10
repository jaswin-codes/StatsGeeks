"""EXP-H_mean: inductive backup. Query rows never fit any target statistic."""
import numpy as np
from candidate.exp010_predict import SUPPORTED_SCHEDULE
from models import C,residual_cov,regularize,metric_prob

def fit_source(frozen_source_artifact,X_source,y_source):
 out={}
 for k in [30,45]:
  ix=np.sort(np.argsort(frozen_source_artifact['feature_importances'])[::-1][:k]);w=np.asarray(frozen_source_artifact['metric_weights'])[ix];Z=X_source[:,ix]*w
  delta=np.array([Z[y_source==c].mean(0)-Z.mean(0)for c in C])
  out[k]={'columns':ix,'weights':w,'covariance':residual_cov(Z,y_source),'offsets':delta}
 return out

def adapt_and_predict(source_state,X_support,y_support,X_query,budget):
 if budget not in SUPPORTED_SCHEDULE:raise ValueError('Unsupported budget')
 if len(y_support)!=4*budget or any(np.sum(y_support==c)!=budget for c in C):raise ValueError('Exactly budget labelled examples per class required')
 k=SUPPORTED_SCHEDULE[budget][0];st=source_state[k];S=X_support[:,st['columns']]*st['weights'];Q=X_query[:,st['columns']]*st['weights'];Cs=residual_cov(S,y_support);Cm=st['covariance'];g=k/(k+len(y_support));Cm=Cm*np.trace(Cs)/max(np.trace(Cm),1e-12);V=np.linalg.inv(regularize((1-g)*Cs+g*Cm));P=metric_prob(S,y_support,Q,V,st['offsets'],.6*g)
 return C[P.argmax(1)]
