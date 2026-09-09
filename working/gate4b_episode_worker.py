"""Fixed current-episode P0/U0/E1 prediction; no evaluator/query labels."""
import sys;sys.path.insert(0,'/numeric')
import hashlib,json,os,gc
from pathlib import Path
import numpy as np
for p in ['/mnt','/home','/run','/data','/working','/proc/1/root/mnt','/proc/1/root/home']:assert not Path(p).exists(),p
packet=json.load(sys.stdin);sys.stdin.close()
assert set(packet)=={'X_support','y_support','support_ids','X_query','query_ids','source_state','parameters'}
assert set(packet['parameters'])=={'episode_id','budget','trial','classes'} and packet['parameters']['classes']==[1,2,3,4]
for name in ('y_query','y_amsterdam','y_target','full_target_labels','other_episode_support_labels','evaluator','manifest'):
 assert name not in globals()
 for m in list(sys.modules.values()):
  if m is not None:assert name not in vars(m)
 for o in gc.get_objects():
  if type(o) is dict and name in o:assert type(o[name]) is str and o[name]==name
xs=np.asarray(packet['X_support'],dtype=np.float64);ys=np.asarray(packet['y_support'],dtype=np.int64);xq=np.asarray(packet['X_query'],dtype=np.float64)
b=packet['parameters']['budget'];assert xs.shape==(4*b,60) and xq.shape==(25992-4*b,60);assert np.array_equal(ys,np.repeat([1,2,3,4],b));assert np.isfinite(xs).all() and np.isfinite(xq).all()
assert len(set(map(tuple,packet['support_ids'])))==len(xs) and len(set(map(tuple,packet['query_ids'])))==len(xq) and not(set(map(tuple,packet['support_ids']))&set(map(tuple,packet['query_ids'])))
st=packet['source_state'];active=np.asarray(st['active_indices'],dtype=np.int64);assert len(active)==59
m1=np.asarray(st['e1_metric'],dtype=np.float64);m0=np.asarray(st['u0_metric'],dtype=np.float64);assert m1.shape==m0.shape==(59,59)
prototypes=np.stack([xs[ys==c].mean(axis=0) for c in [1,2,3,4]])
def predict_raw():
 dist=((xq[:,None,:]-prototypes[None,:,:])**2).sum(axis=2);return np.argmin(dist,axis=1)+1
def predict_metric(metric):
 pred=np.empty(len(xq),dtype=np.int64)
 for start in range(0,len(xq),4096):
  diff=xq[start:start+4096,None,active]-prototypes[None,:,active]
  dist=np.einsum('ncd,de,nce->nc',diff,metric,diff,optimize=True)
  pred[start:start+4096]=np.argmin(dist,axis=1)+1
 return pred
p0=predict_raw();u0=predict_metric(m0);e1=predict_metric(m1)
def ah(a):
 a=np.ascontiguousarray(a);h=hashlib.sha256(json.dumps([a.dtype.str,list(a.shape)],separators=(',',':')).encode());h.update(a.tobytes());return h.hexdigest()
qhash=hashlib.sha256(json.dumps(packet['query_ids'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
result={'query_fingerprint':qhash,'predictions':{'raw_prototype':p0.tolist(),'unsupervised_covariance':u0.tolist(),'e1':e1.tolist()},'adaptation_state':{'prototype_array_sha256':ah(prototypes),'support_ids_sha256':hashlib.sha256(json.dumps(packet['support_ids'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'source_state_sha256':packet['parameters'].get('source_state_sha256','') if False else hashlib.sha256(json.dumps(st,sort_keys=True,separators=(',',':')).encode()).hexdigest()},'label_access':{'source_state_only':True,'current_support_labels':len(ys),'query_labels':0,'other_episode_labels':0}}
print(json.dumps(result,separators=(',',':')))
