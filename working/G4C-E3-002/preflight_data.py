"""Host fingerprint and frozen array/manifest checks; no fitting or worker launch."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import importlib.util,json,pathlib,pickle,platform,sys,zlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2];RUN=ROOT/'working/G4C-E3-002'
def mod(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=mod('coordinator_preflight',RUN/'coordinator/execution_coordinator.py')
v=mod('validator_preflight',RUN/'coordinator/e3_validator.py')
assert platform.python_version()=='3.14.6' and np.__version__=='2.5.3' and zlib.ZLIB_RUNTIME_VERSION=='1.3.1.zlib-ng'
assert pathlib.Path(sys.executable).resolve()==(ROOT/'.venv_baseline/Scripts/python.exe').resolve()
c.preexisting_integrity();c.install_pickle_dependency()
with (ROOT/'data/preprocessed/preprocessed_data.pkl').open('rb') as f:d=pickle.load(f)
schema=json.loads((ROOT/'working/baseline_artifacts/feature_schema.json').read_text())
assert d['feature_names']==schema['feature_names'] and len(schema['feature_names'])==60
assert schema['feature_names'][-2:]==['has_early_data','has_late_data']
arrays={}
for city,n in [('madrid',76263),('amsterdam',25992)]:
    x,y,ids=(d[k+'_'+city] for k in ('X','y','pixel_ids'))
    assert x.shape==(n,60) and x.dtype==np.dtype('float64') and np.isfinite(x).all()
    assert y.shape==(n,) and np.array_equal(np.unique(y),[1,2,3,4])
    assert ids.shape==(n,2) and len(np.unique(ids,axis=0))==n
    for key in ('X','y','pixel_ids'):
        a=d[key+'_'+city];arrays[key+'_'+city]={'dtype':a.dtype.str,'shape':list(a.shape),'array_sha256':v.array_hash(a)}
x,y,ids=(d[k+'_amsterdam'] for k in ('X','y','pixel_ids'))
m=json.loads((RUN/'checkpoint/episode_manifest.json').read_text());rng=np.random.default_rng(42)
assert len(m['episodes'])==60 and len({e['episode_id'] for e in m['episodes']})==60
for i,e in enumerate(m['episodes']):
    b,t=[5,10,25,50,100,200][i//10],i%10+1
    assert (e['budget'],e['trial'],e['episode_id'])==(b,t,f'G4A-B{b:03d}-T{t:02d}')
    assert rng.bit_generator.state==e['rng_before']
    s=np.concatenate([rng.choice(np.flatnonzero(y==cl),b,replace=False) for cl in [1,2,3,4]])
    assert np.array_equal(s,e['support_row_indices']) and rng.bit_generator.state==e['rng_after']
    q=np.setdiff1d(np.arange(len(y)),s)
    assert len(q)==25992-4*b and np.array_equal(ids[s],e['support_pixel_ids'])
    for name,a in [('support_row_indices',s),('query_row_indices',q),('support_pixel_ids',ids[s]),('query_pixel_ids',ids[q]),('X_support',x[s]),('X_query',x[q])]:assert v.array_hash(a)==e[name+'_sha256'],name
record={'status':'PASS','python':sys.version,'executable':sys.executable,'numpy':np.__version__,'zlib':zlib.ZLIB_RUNTIME_VERSION,'arrays':arrays,'feature_names':schema['feature_names'],'episodes':60,'budgets':[5,10,25,50,100,200],'trials':10,'seed':42,'rng':'PCG64','manifest_sha256':v.MH,'preprocessing_sha256':c.sha(ROOT/'data/preprocessed/preprocessed_data.pkl'),'parameters':c.PARAMS,'scientific_operations':'No preprocessing refit, RF fit or target query scoring. Existing frozen supervised Madrid means and support-only translation protocol.','command':['.venv_baseline/Scripts/python.exe','-I','-B','working/G4C-E3-002/coordinator/execution_coordinator.py']}
with (RUN/'checkpoint/data_host_preflight.json').open('x') as f:json.dump(record,f,indent=2)
print('PASS: host fingerprint, source integrity, dataset/schema and all 60 manifest bindings')
