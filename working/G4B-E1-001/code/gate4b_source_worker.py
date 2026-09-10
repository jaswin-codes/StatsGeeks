"""Fixed E1/U0 source-state fit: Madrid only, no target inputs."""
import sys;sys.path.insert(0,'/numeric')
import hashlib,json,os
from pathlib import Path
import numpy as np
for p in ['/mnt','/home','/data','/working']:assert not Path(p).exists()
packet=json.load(sys.stdin);sys.stdin.close()
assert set(packet)=={'X_source','y_source','parameters'}
assert packet['parameters']=={'classes':[1,2,3,4],'shrinkage':0.1,'covariance_ddof':0}
x=np.asarray(packet['X_source'],dtype=np.float64);y=np.asarray(packet['y_source'],dtype=np.int64)
assert x.shape==(76263,60) and y.shape==(76263,) and np.array_equal(np.unique(y),[1,2,3,4]) and np.isfinite(x).all()
var=x.var(axis=0);active=np.flatnonzero(var>0);assert len(active)==59
z=x[:,active];w=np.zeros((59,59))
for c in [1,2,3,4]:
 a=z[y==c];d=a-a.mean(axis=0);w += d.T@d/len(a)/4
d=z-z.mean(axis=0);u=d.T@d/len(z)
def regularize(cov):
 tr=float(np.trace(cov));assert np.isfinite(tr) and tr>0
 reg=.9*cov+.1*(tr/len(active))*np.eye(len(active));e,v=np.linalg.eigh(reg)
 assert np.isfinite(e).all() and e[0]>0
 metric=(v*(1/e))@v.T
 return reg,e,metric
wr,we,wm=regularize(w);ur,ue,um=regularize(u)
def ah(a):
 a=np.ascontiguousarray(a);h=hashlib.sha256(json.dumps([a.dtype.str,list(a.shape)],separators=(',',':')).encode());h.update(a.tobytes());return h.hexdigest()
state={'active_indices':active.tolist(),'e1_metric':wm.tolist(),'u0_metric':um.tolist(),'parameters':packet['parameters'],'diagnostics':{'within_trace':float(np.trace(w)),'total_trace':float(np.trace(u)),'e1_min_eigenvalue':float(we[0]),'e1_max_eigenvalue':float(we[-1]),'u0_min_eigenvalue':float(ue[0]),'u0_max_eigenvalue':float(ue[-1]),'e1_metric_array_sha256':ah(wm),'u0_metric_array_sha256':ah(um),'X_source_array_sha256':ah(x),'y_source_array_sha256':ah(y)}}
raw=json.dumps(state,sort_keys=True,separators=(',',':'),allow_nan=False).encode();out={'source_state':state,'source_state_sha256':hashlib.sha256(raw).hexdigest(),'fit_scope':'Madrid only','target_rows_received':0}
print(json.dumps(out,separators=(',',':'),allow_nan=False))
