"""Independent ASTRA mechanism implementation; fitting accepts no query truth."""
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
CLASSES=np.arange(1,5)
BUDGETS=(5,25,50,100,200)

def power(a,p):
    v,u=np.linalg.eigh(a)
    return (u*np.maximum(v,1e-7)**p)@u.T

def transport(x,target):
    return (x-x.mean(0))@power(np.cov(x,rowvar=False)+1e-5*np.eye(x.shape[1]),-.5)@power(np.cov(target,rowvar=False)+1e-5*np.eye(x.shape[1]),.5)+target.mean(0)

def grid_average(coords):
    lookup={tuple(x):i for i,x in enumerate(coords)}; rows=[]; cols=[]; values=[]
    for i,(x,y) in enumerate(coords):
        nn=[lookup[x+dx,y+dy] for dx in (-1,0,1) for dy in (-1,0,1) if (x+dx,y+dy) in lookup]
        rows.extend([i]*len(nn)); cols.extend(nn); values.extend([1/len(nn)]*len(nn))
    return csr_matrix((values,(rows,cols)),shape=(len(coords),len(coords)))

def forest(kind='rf',leaf=1,features='sqrt',trees=200):
    cls=ExtraTreesClassifier if kind=='extra' else RandomForestClassifier
    return cls(n_estimators=trees,min_samples_leaf=leaf,max_features=features,class_weight='balanced',random_state=42,n_jobs=4)

def stable_probability(model,x):
    if hasattr(model,'n_jobs'):
        old=model.n_jobs; model.n_jobs=1
        try: return model.predict_proba(x)
        finally: model.n_jobs=old
    return model.predict_proba(x)

def fit_pool(source_x,source_y,source_coords,target_x,target_coords,mean,scale,feature_names):
    source_x=np.asarray(source_x)*scale+mean; raw=np.asarray(target_x)*scale+mean
    assert raw.shape[1]==60 and len(set(feature_names))==60
    assert np.isfinite(raw).all() and np.array_equal(np.unique(source_y),CLASSES)
    assert len(np.unique(target_coords,axis=0))==len(raw)
    assert np.equal(target_coords,np.round(target_coords)).all()
    m=np.column_stack((source_x,grid_average(source_coords)@source_x))
    a=np.column_stack((raw,grid_average(target_coords)@raw))
    aligned=transport(m,a); first=forest(leaf=2).fit(aligned,source_y)
    pseudo=CLASSES[stable_probability(first,a).argmax(1)]
    refined=aligned.copy()
    for c in CLASSES:
        mask=source_y==c; target=a[pseudo==c]
        if len(target)>a.shape[1]: refined[mask]=transport(aligned[mask],target)
    second=forest(leaf=2).fit(refined,source_y)
    prior=stable_probability(second,a)
    dist,nn=cKDTree(target_coords).query(target_coords,k=25)
    return dict(raw=raw,standard=np.asarray(target_x),coords=np.asarray(target_coords),prior=prior,cov=np.cov(raw,rowvar=False),nn=nn,dist=dist,feature_names=list(feature_names),classes=CLASSES,source_counts={int(c):int((pseudo==c).sum()) for c in CLASSES})

BASE=dict(kind='rf',leaf=1,features='sqrt',trees=200,pool=True,adaptive=True,spatial=True,prior=20.,rho_factor=1.,sigma=1.,neighbours=9,steps=1,coord=False,bilateral=False,covblend=0.)

def probabilities(state,s,ys,budget,config=None):
    cfg={**BASE,**(config or {})}; s=np.asarray(s); ys=np.asarray(ys)
    if s.dtype.kind not in 'iu' or len(s)!=len(np.unique(s)) or len(s)!=4*budget or ys.shape!=s.shape or (s<0).any() or (s>=len(state['raw'])).any(): raise ValueError('Invalid support')
    if any(np.sum(ys==c)!=budget for c in CLASSES): raise ValueError('Exactly budget support labels per class required')
    x=state['raw']; z=state['standard']
    if cfg['pool'] or cfg['adaptive']:
        cov=state['cov'] if cfg['pool'] else np.cov(x[s],rowvar=False)
        rho=min(1,60/(4*budget)*cfg['rho_factor']) if cfg['adaptive'] else .5
        cov=(1-rho)*cov+rho*np.diag(np.diag(cov))+1e-7*np.eye(60)
        z=(x-x.mean(0) if cfg['pool'] else x-x[s].mean(0))@power(cov,-.5)
    if cfg['coord']:
        xy=state['coords']; z=np.column_stack((z,(xy-xy.mean(0))/np.maximum(xy.std(0),1)))
    if cfg['kind']=='hist': model=HistGradientBoostingClassifier(max_iter=160,max_leaf_nodes=15,l2_regularization=10,learning_rate=.06,random_state=42)
    else: model=forest(cfg['kind'],cfg['leaf'],cfg['features'],cfg['trees'])
    model.fit(z[s],ys); p=stable_probability(model,z)
    if cfg.get('ensemble',False):
        other=forest('extra',cfg['leaf'],.5,cfg['trees']).fit(z[s],ys)
        p=.5*p+.5*stable_probability(other,z)
    if cfg['covblend']:
        from scipy.special import softmax
        centers=np.array([z[s][ys==c].mean(0) for c in CLASSES]); residual=z[s]-centers[np.searchsorted(CLASSES,ys)]
        cov=residual.T@residual/max(len(s)-4,1); v=np.linalg.inv(.5*cov+(.5*np.trace(cov)/len(cov)+1e-8)*np.eye(len(cov)))
        ds=np.column_stack([np.einsum('ij,ij->i',(z-c)@v,z-c) for c in centers]); temp=max(np.einsum('ij,ij->i',residual@v,residual).mean(),1e-8)
        p=(1-cfg['covblend'])*p+cfg['covblend']*softmax(-ds/temp,axis=1)
    alpha=cfg['prior']/(cfg['prior']+len(s)); p=(1-alpha)*p+alpha*state['prior']
    if cfg['spatial']:
        # Query topology is label-free. No support truth anchoring.
        # k=9 is re-queried to preserve the historical cKDTree tie convention.
        dist,nn=cKDTree(state['coords']).query(state['coords'],k=cfg['neighbours'])
        w=np.exp(-dist**2/(2*cfg['sigma']**2))
        if cfg['bilateral']:
            zz=state['standard']; delta=np.mean((zz[:,None,:]-zz[nn])**2,axis=2); w*=np.exp(-delta/2)
        w/=w.sum(1,keepdims=True)
        for _ in range(cfg['steps']): p=np.sum(p[nn]*w[:,:,None],axis=1)
    assert np.isfinite(p).all(); np.testing.assert_allclose(p.sum(1),1,atol=1e-10)
    return p
