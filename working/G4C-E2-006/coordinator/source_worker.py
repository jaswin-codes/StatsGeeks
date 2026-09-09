"""Fixed E2/E3/E4 Madrid-only state, isolated stdin contract."""
import sys
sys.path.insert(0, '/numeric')
import json, hashlib, resource
from pathlib import Path
import numpy as np
for p in ['/mnt','/home','/run','/data','/working','/proc/1/root/mnt','/proc/1/root/home']:
    assert not Path(p).exists(), p
p=json.load(sys.stdin);sys.stdin.close()
assert set(p)=={'X_source','y_source','parameters'}
params=p['parameters'];method=params['candidate']
expected={'E2':{'candidate':'E2','epsilon':1e-6,'clip':[.25,4.0],'identity_mixture':.5},'E3':{'candidate':'E3','translation_strength':1.0,'continuous_indices':list(range(58))},'E4':{'candidate':'E4','shrinkage':.1,'max_rank':3,'eigenvalue_relative_threshold':1e-10}}
# E3 indices must be supplied from the frozen named schema, not assumed order.
if method!='E3':assert params==expected[method]
x=np.asarray(p['X_source'],dtype=np.float64);y=np.asarray(p['y_source'],dtype=np.int64)
assert x.shape==(76263,60) and y.shape==(76263,) and np.isfinite(x).all() and np.array_equal(np.unique(y),[1,2,3,4])
active=np.flatnonzero(x.var(0)>0);assert len(active)==59
means=np.stack([x[y==c].mean(0) for c in [1,2,3,4]])
st={'parameters':params,'active_indices':active.tolist(),'source_means':means.tolist()}
if method=='E2':
    m=means[:,active];grand=m.mean(0);between=((m-grand)**2).mean(0)
    within=np.stack([x[y==c][:,active].var(0,ddof=0) for c in [1,2,3,4]]).mean(0)
    q=between/(within+1e-6);assert np.isfinite(q).all() and q.mean()>0
    v=np.clip(q/q.mean(),.25,4);w=.5+.5*v/v.mean()
    st.update(weights=w.tolist(),fisher_ratios=q.tolist(),clipped_normalized=v.tolist())
elif method=='E3':
    assert set(params)=={'candidate','translation_strength','continuous_indices'} and params['translation_strength']==1.0
    assert len(params['continuous_indices'])==len(set(params['continuous_indices']))==58
elif method=='E4':
    z=x[:,active];m=means[:,active];grand=m.mean(0);W=np.zeros((59,59))
    for c in [1,2,3,4]:
        a=z[y==c];d=a-a.mean(0);W+=d.T@d/len(a)/4
    tr=np.trace(W);assert np.isfinite(tr) and tr>0
    reg=.9*W+.1*tr/59*np.eye(59);e,v=np.linalg.eigh(reg);assert e[0]>0
    R=(v*(1/np.sqrt(e)))@v.T;B=(m-grand).T@(m-grand)/4
    ev,U=np.linalg.eigh(R@B@R);assert np.isfinite(ev).all() and ev[-1]>0
    keep=np.flatnonzero(ev>1e-10*ev[-1])[-3:][::-1];assert 1<=len(keep)<=3
    A=R@U[:,keep];st.update(embedding=A.tolist(),grand_mean=grand.tolist(),eigenvalues=ev.tolist(),rank=len(keep))
raw=json.dumps(st,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
print(json.dumps({'source_state':st,'source_state_sha256':hashlib.sha256(raw).hexdigest(),'fit_scope':'Madrid only','target_rows_received':0,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},separators=(',',':'),allow_nan=False))
