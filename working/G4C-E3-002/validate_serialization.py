"""Independent strict archive/payload audit and unchanged Windows producer byte replay."""
import hashlib,importlib.util,io,json,pathlib,pickle,sys,time,types,zipfile
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2];RUN=ROOT/'working/G4C-E3-002'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(p.read_text())
start=time.perf_counter();rows=load(RUN/'results/per_episode_results.json');manifest=load(RUN/'checkpoint/episode_manifest.json')
assert len(rows)==60 and [r['episode_id'] for r in rows]==[e['episode_id'] for e in manifest['episodes']]
helper=ROOT/'working/minimal_standard_scaler.py';assert sha(helper)=='c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111'
package=types.ModuleType('working');package.__path__=[];sys.modules['working']=package
spec=importlib.util.spec_from_file_location('working.minimal_standard_scaler',helper);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
with (ROOT/'data/preprocessed/preprocessed_data.pkl').open('rb') as f:d=pickle.load(f)
ids=d['pixel_ids_amsterdam'];names=['query_indices','query_ids','raw_prototype','rf_reproduced','candidate','frozen_rf'];records=[]
assert ids.dtype==np.dtype('<i4')
for i,(e,r) in enumerate(zip(manifest['episodes'],rows)):
    p=ROOT/r['prediction_artifact'];assert p==RUN/'predictions'/(e['episode_id']+'.npz') and not p.is_symlink()
    assert sha(p)==r['prediction_sha256'];s=np.array(e['support_row_indices'],dtype=np.int64);q=np.setdiff1d(np.arange(len(ids)),s)
    ep=RUN/'evidence'/f'worker_{i+1:02d}.json';assert sha(ep)==r['worker_output_sha256'];ev=load(ep);out=ev['result']
    assert ev['boundary_evidence']['teardown_pass'] and not ev['boundary_evidence']['lifecycle']['final_survivors']
    assert out['query_fingerprint']==hashlib.sha256(canon(ids[q].tolist())).hexdigest()
    native=ev['infrastructure_io'];assert not native['created'] and native['path']=='/home/jaswin/.local/share/statsgeeks/frozen_rf/5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870.pkl'
    assert native['sha256']=='5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870' and native['bytes']==1336382673
    for values in out['predictions'].values():assert len(values)==len(q) and all(type(v) is int and v in (1,2,3,4) for v in values)
    expected={'query_indices':q,'query_ids':ids[q],**{k:np.asarray(out['predictions'][k],dtype=np.int64) for k in ('raw_prototype','rf_reproduced','candidate')}}
    with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as base:expected['frozen_rf']=base['y_ams_pred_zero'][q]
    members=[]
    with zipfile.ZipFile(p) as z,np.load(p,allow_pickle=False) as a:
        assert z.namelist()==[k+'.npy' for k in names] and a.files==names
        for k in names:
            value=a[k];dtype='<i4' if k=='query_ids' else '<i8';shape=(len(q),2) if k=='query_ids' else (len(q),)
            assert value.dtype.str==dtype and value.shape==shape and np.array_equal(value,expected[k])
            payload=z.read(k+'.npy');buf=io.BytesIO();np.lib.format.write_array(buf,expected[k],allow_pickle=False)
            assert buf.getvalue()==payload
            members.append({'name':k+'.npy','dtype':value.dtype.str,'shape':list(value.shape),'npy_sha256':hashlib.sha256(payload).hexdigest()})
    replay=io.BytesIO();np.savez_compressed(replay,**{k:expected[k] for k in names})
    assert replay.getvalue()==p.read_bytes()
    records.append({'episode_id':e['episode_id'],'status':'PASS','prediction_sha256':r['prediction_sha256'],'members':members,'windows_producer_byte_identity':True,'native_rf_created':native['created']})
result={'status':'PASS','episodes':60,'archive_order':['query_indices.npy','query_ids.npy','raw_prototype.npy','rf_reproduced.npy','candidate.npy','frozen_rf.npy'],'exact_npy_members':360,'same_windows_producer_byte_replays':60,'cross_compressor_raw_zip_identity_required':False,'prior_E3_predictions_loaded':False,'seconds':time.perf_counter()-start,'records':records}
with (RUN/'validation/serialization_validation.json').open('x') as f:json.dump(result,f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
