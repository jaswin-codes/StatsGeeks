"""Separate audit implementation; no production or equivalence-helper imports.

Read-only ZIP/NPY/hash/metric checks on the selected archived/certification files.
No model deserialization, prediction calculation, or worker launch.
"""
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
CERT=Path(__file__).resolve().parents[1]


def hash_bytes(raw):return hashlib.sha256(raw).hexdigest()

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def metrics(y,p):
    cm=np.bincount(4*(y-1)+p-1,minlength=16).reshape(4,4)
    tp=cm.diagonal();d=cm.sum(0)+cm.sum(1)
    f=np.divide(2*tp,d,out=np.zeros(4),where=d!=0)
    return {'macro_f1':float(f.mean()),'per_class_f1':f.tolist(),
        'precision':np.divide(tp,cm.sum(0),out=np.zeros(4),where=cm.sum(0)!=0).tolist(),
        'recall':np.divide(tp,cm.sum(1),out=np.zeros(4),where=cm.sum(1)!=0).tolist(),
        'accuracy':float(tp.sum()/cm.sum()),'confusion':cm.tolist()}


def main():
    offline=json.loads((CERT/'evidence/offline_equivalence.json').read_text())
    producer=json.loads((CERT/'evidence/producer_byte_equivalence.json').read_text())
    manifest=json.loads((ROOT/'working/gate4_episode_manifest.json').read_text())
    inventory=json.loads((ROOT/'working/G4C-E3-001/artifact_hash_manifest.json').read_text())['files']
    with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as b:
        y=b['y_amsterdam'].copy();ids=b['pixel_ids_amsterdam'].copy()
    rng=np.random.default_rng(42)
    for e in manifest['episodes']:
        assert rng.bit_generator.state==e['rng_before']
        s=np.concatenate([rng.choice(np.where(y==c)[0],e['budget'],replace=False) for c in (1,2,3,4)])
        assert s.tolist()==e['support_row_indices'] and rng.bit_generator.state==e['rng_after']
    comparisons=[]
    for index in (0,20,50):
        e=manifest['episodes'][index];eid=e['episode_id']
        archived=ROOT/'working/G4C-E3-001/predictions'/(eid+'.npz');raw=archived.read_bytes()
        assert hash_bytes(raw)==inventory[archived.relative_to(ROOT).as_posix()]['sha256']
        with np.load(io.BytesIO(raw),allow_pickle=False) as a:
            query=np.setdiff1d(np.arange(len(y)),e['support_row_indices'])
            assert np.array_equal(a['query_indices'],query) and np.array_equal(a['query_ids'],ids[query])
            metric={name:metrics(y[query],a[name]) for name in ('candidate','raw_prototype','rf_reproduced','frozen_rf')}
        for mode in ('original','optimized_native'):
            record=next(r for r in offline['runs'][mode]['episodes'] if r['episode_id']==eid)
            generated=CERT/record['certification_artifact'];candidate=generated.read_bytes()
            assert hash_bytes(candidate)==record['prediction_npz_sha256']
            assert hash_bytes(canonical(metric))==record['metric_sha256']
            with zipfile.ZipFile(io.BytesIO(raw)) as a,zipfile.ZipFile(io.BytesIO(candidate)) as b:
                assert a.namelist()==b.namelist() and len(a.namelist())==len(set(a.namelist()))==6
                for name in a.namelist():
                    left,right=a.read(name),b.read(name)
                    assert left==right,('Decompressed NPY byte disagreement',name)
                    la=np.load(io.BytesIO(left),allow_pickle=False);ra=np.load(io.BytesIO(right),allow_pickle=False)
                    assert la.dtype.str==ra.dtype.str and la.shape==ra.shape and np.array_equal(la,ra)
            replay_record=next(r for r in producer['results'] if r['mode']==mode and r['episode_id']==eid)
            for replay in replay_record['replays']:
                rep=(CERT/replay['path']).read_bytes()
                assert rep==raw and hash_bytes(rep)==replay['sha256']
            comparisons.append({'episode_id':eid,'mode':mode,'query_rows':len(query),
                                'npy_members_exact':6,'producer_replays_exact':2,'metrics_exact':True})
    before=json.loads((CERT/'evidence/protected_before.json').read_text());changed=[]
    for path,expected in before['files'].items():
        p=ROOT/path
        with p.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
        if actual!=expected['sha256'] or p.stat().st_size!=expected['bytes']:changed.append(path)
    assert not changed,changed
    result={'status':'INDEPENDENT_BYTE_PAYLOAD_METRIC_AUDIT_PASS','comparisons':comparisons,
            'unique_episode_query_predictions':sum(r['query_rows'] for r in comparisons if r['mode']=='original'),
            'historical_files_verified':len(before['files']),'historical_changes':changed,
            'rng_replays':60,'new_worker_launches':0,'new_model_loads':0,
            'scope':'Separate implementation/process; not independent human review; runtime not certified'}
    with (CERT/'evidence/independent_audit.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
