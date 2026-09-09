"""Fixed G4C methods; source state and current support labels only."""
import sys
sys.path.insert(0,'/numeric')
import hashlib,json,os,gc,resource,pickle,warnings,stat
from pathlib import Path
import numpy as np
for path in ['/mnt','/home','/run','/data','/working','/proc/1/root/mnt','/proc/1/root/home']:
    assert not Path(path).exists(),path
assert not Path('/tmp/g4c_prior_state').exists()
APPROVED_RUNTIME_DESCRIPTOR={'/usr/lib/x86_64-linux-gnu/libffi.so.8':'1a0dc86f787f73e025a6e521056360afcbe70f2a82cd808132fefc2b4ee95daa'}
def file_sha(path):
    with open(path,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def audit_descriptors(stage):
    accepted=[];forbidden=[];vanished=[]
    for name in os.listdir('/proc/self/fd'):
        fd=int(name)
        if fd<=2:continue
        try:
            target=os.readlink('/proc/self/fd/'+name);before=os.fstat(fd);info=Path('/proc/self/fdinfo/'+name).read_text();after=os.fstat(fd)
        except (FileNotFoundError,OSError):vanished.append(fd);continue
        if (before.st_dev,before.st_ino)!=(after.st_dev,after.st_ino):forbidden.append({'fd':fd,'reason':'identity changed during audit'});continue
        flags=int(next(line.split()[1] for line in info.splitlines() if line.startswith('flags:')),8);expected=APPROVED_RUNTIME_DESCRIPTOR.get(target)
        if expected and stat.S_ISREG(before.st_mode) and (flags & os.O_ACCMODE)==os.O_RDONLY and file_sha(target)==expected:
            accepted.append({'fd':fd,'target':target,'sha256':expected,'access':'O_RDONLY','stage':stage})
        else:forbidden.append({'fd':fd,'target':target,'flags_octal':oct(flags),'stage':stage})
    assert not forbidden,{'forbidden_descriptors':forbidden,'accepted':accepted,'vanished_scan_entries':vanished}
    return {'accepted':accepted,'vanished':vanished,'forbidden':[]}
fd_audit_before=audit_descriptors('before_packet_parse')
p=json.load(sys.stdin);sys.stdin.close()
fd_audit_after=audit_descriptors('after_packet_parse')
assert set(p)=={'X_support','y_support','support_ids','X_query','query_ids','source_state','parameters'}
assert set(p['parameters'])=={'episode_id','budget','trial','classes','candidate'}
assert p['parameters']['classes']==[1,2,3,4]
for name in ('y_query','y_amsterdam','y_target','full_target_labels','other_episode_support_labels','evaluator','manifest'):
    assert name not in globals()
    for mod in list(sys.modules.values()):
        if mod is not None:assert name not in vars(mod)
xs=np.asarray(p['X_support'],dtype=np.float64);ys=np.asarray(p['y_support'],dtype=np.int64);xq=np.asarray(p['X_query'],dtype=np.float64)
b=p['parameters']['budget'];method=p['parameters']['candidate'];st=p['source_state']
assert xq.shape==(25992-4*b,60) and np.isfinite(xq).all()
if b:
    assert xs.shape==(4*b,60) and np.array_equal(ys,np.repeat([1,2,3,4],b)) and np.isfinite(xs).all()
    assert len(set(map(tuple,p['support_ids'])))==len(xs)
    assert not(set(map(tuple,p['support_ids']))&set(map(tuple,p['query_ids'])))
else:assert method=='E4' and not len(ys) and not len(p['support_ids'])
assert len(set(map(tuple,p['query_ids'])))==len(xq)
Path('/tmp/g4c_prior_state').write_text(json.dumps(p['y_support']))
def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def nearest(q,c):return np.argmin(((q[:,None,:]-c[None,:,:])**2).sum(2),axis=1)+1
pred={};adapt={};warn=[]
if b:
    prototypes=np.stack([xs[ys==c].mean(0) for c in [1,2,3,4]])
    pred['raw_prototype']=nearest(xq,prototypes);adapt['prototypes']=prototypes.tolist()
if method=='E2':
    assert st['parameters']=={'candidate':'E2','epsilon':1e-6,'clip':[.25,4.0],'identity_mixture':.5}
    active=np.asarray(st['active_indices']);w=np.asarray(st['weights']);assert w.shape==(59,) and (w>0).all()
    dist=(((xq[:,None,active]-prototypes[None,:,active])**2)*w).sum(2)
    pred['candidate']=np.argmin(dist,axis=1)+1
    # Fixed all-ones ablation is the exact unchanged 60-column P0 comparator;
    # also retain 59-active all-ones predictions to document constant-mask effects.
    pred['all_ones_active']=nearest(xq[:,active],prototypes[:,active])
elif method=='E4':
    assert st['parameters']=={'candidate':'E4','shrinkage':.1,'max_rank':3,'eigenvalue_relative_threshold':1e-10}
    active=np.asarray(st['active_indices']);A=np.asarray(st['embedding']);m=np.asarray(st['grand_mean']);source=np.asarray(st['source_means'])[:,active]
    assert A.shape[0]==59 and 1<=A.shape[1]<=3
    q=(xq[:,active]-m)@A
    pred['source_centroid']=nearest(q,(source-m)@A)
    if b:pred['candidate']=nearest(q,(prototypes[:,active]-m)@A)
    else:pred['candidate']=pred['source_centroid']
else:
    assert method in ['E3','E5']
    rfpath=Path('/app/rf_final.pkl')
    with rfpath.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()=='5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870'
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        with rfpath.open('rb') as f:rf=pickle.load(f)
        assert len(rf.estimators_)==500 and rf.n_features_in_==60 and np.array_equal(rf.classes_,[1,2,3,4])
        pred['rf_reproduced']=rf.predict(xq).astype(np.int64)
        if method=='E3':
            assert st['parameters']=={'candidate':'E3','translation_strength':1.0,'continuous_indices':list(range(58))}
            delta=(prototypes-np.asarray(st['source_means'])).mean(0);delta[58:]=0
            translated=xq-delta;assert np.array_equal(translated[:,58:],xq[:,58:])
            pred['candidate']=rf.predict(translated).astype(np.int64);adapt['translation']=delta.tolist()
        else:
            assert st['parameters']=={'candidate':'E5','trees':500,'embedding':'equal-weight leaf one-hot','distance':'squared centroid distance'}
            support=rf.apply(xs);counts=[];norm=np.zeros(4)
            for t in range(500):
                ct=[]
                for ci,c in enumerate([1,2,3,4]):
                    leaves,nums=np.unique(support[ys==c,t],return_counts=True);freq=nums/b
                    ct.append((leaves,freq));norm[ci]+=np.sum(freq**2)/500
                counts.append(ct)
            out=[]
            for start in range(0,len(xq),2048):
                leaves=rf.apply(xq[start:start+2048]);dots=np.zeros((len(leaves),4))
                for t in range(500):
                    for ci,(keys,freq) in enumerate(counts[t]):
                        pos=np.searchsorted(keys,leaves[:,t]);valid=pos<len(keys);safe=np.minimum(pos,len(keys)-1);valid &= keys[safe]==leaves[:,t]
                        dots[:,ci]+=np.where(valid,freq[safe],0)/500
                out.extend((np.argmin(1-2*dots+norm,axis=1)+1).tolist())
            pred['candidate']=np.asarray(out);adapt['centroid_norm_squared']=norm.tolist();adapt['support_leaf_ids']=support.tolist()
        warn=[str(w.message) for w in caught]
# No estimator mutation/refitting, no persistence except private tmpfs destroyed at exit.
result={'query_fingerprint':hashlib.sha256(canon(p['query_ids'])).hexdigest(),'predictions':{k:v.tolist() for k,v in pred.items()},'adaptation_state':adapt,'source_state_sha256':hashlib.sha256(canon(st)).hexdigest(),'label_access':{'source_state_only':True,'current_support_labels':len(ys),'query_labels':0,'other_episode_labels':0},'fresh_state_probe':True,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'warnings':warn,'descriptor_audit':{'before':fd_audit_before,'after':fd_audit_after}}
print(json.dumps(result,separators=(',',':'),allow_nan=False))
