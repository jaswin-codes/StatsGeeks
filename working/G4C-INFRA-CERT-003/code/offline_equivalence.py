"""Bounded privileged OFFLINE E3 reconstruction; NEVER launches candidate workers.

Three preregistered archived episodes (ordinals 1,21,51) are reconstructed from
both original RF bytes and native-staged RF bytes. No complete experiment,
aggregate E3 evaluation, model fitting, or candidate worker code execution.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k]='1'
import gc
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import pickle
import sys
import time
import types

ROOT=Path(__file__).resolve().parents[3]
CERT=Path(__file__).resolve().parents[1]
# This privileged verifier imports the approved numerical packages on the host.
# It is NOT a sandbox/worker launch or isolation recertification.
lock=json.loads((ROOT/'working/gate4_runtime_narwhals_lock.json').read_text())
sys.path.insert(0,lock['image_path']+'/numeric')
import numpy as np
import sklearn
import e3_validator as v
from prediction_equivalence import Artifact, compare_artifacts
sys.path.insert(0,str(ROOT/'working/G4C-INFRA-PERF-001/code'))
from immutable_io import stage_frozen_file

SELECTED=(0,20,50)


def main():
    start=time.perf_counter();record={'mode':'OFFLINE_PRIVILEGED_RECONSTRUCTION','selected_episode_ordinals':[i+1 for i in SELECTED],
        'worker_launches':0,'full_experiments':0,'python':sys.version,'numpy':np.__version__,'sklearn':sklearn.__version__}
    v.require(v.sha(ROOT/'working/gate4_runtime_narwhals_lock.json')==v.RUNTIME_HASH,'Runtime lock changed')
    image=Path(lock['image_path']);t=time.perf_counter()
    actual={p.relative_to(image).as_posix():v.sha(p) for p in sorted(image.rglob('*')) if p.is_file()}
    v.require(actual==lock['files'],'Runtime package tree changed')
    for item in lock['wheels'].values():v.require(v.sha(item['source'])==item['sha256'],'Wheel source changed')
    v.require(v.sha('/usr/bin/bwrap')==lock['bwrap_sha256'],'Bubblewrap binary changed')
    record['runtime_tree_files']=len(actual);record['runtime_verification_seconds']=time.perf_counter()-t
    helper=ROOT/'working/minimal_standard_scaler.py'
    v.require(v.sha(helper)=='c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111','Pickle helper hash mismatch')
    package=types.ModuleType('working');package.__path__=[];sys.modules['working']=package
    spec=importlib.util.spec_from_file_location('working.minimal_standard_scaler',helper);module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    with (ROOT/'data/preprocessed/preprocessed_data.pkl').open('rb') as f:data=pickle.load(f)
    x,y,ids=data['X_amsterdam'],data['y_amsterdam'],data['pixel_ids_amsterdam']
    archive=ROOT/'working/G4C-E3-001';statefile=v.load(archive/'candidate_state/source_state.json');state=statefile['source_state']
    v.require(state['parameters']==v.PARAMS and v.digest(state)==statefile['source_state_sha256'],'Archived E3 state changed')
    means=np.stack([data['X_madrid'][data['y_madrid']==c].mean(0) for c in [1,2,3,4]])
    v.require(np.allclose(means,state['source_means'],rtol=1e-10,atol=1e-12),'Independent source means mismatch')
    v.require(v.sha(ROOT/'working/gate4_episode_manifest.json')==v.MH,'Frozen manifest mismatch')
    manifest=v.load(ROOT/'working/gate4_episode_manifest.json');rng=np.random.default_rng(42)
    for e in manifest['episodes']:
        v.require(rng.bit_generator.state==e['rng_before'],'RNG mismatch')
        s=np.concatenate([rng.choice(np.flatnonzero(y==c),e['budget'],replace=False) for c in [1,2,3,4]])
        v.require(np.array_equal(s,e['support_row_indices']) and rng.bit_generator.state==e['rng_after'],'RNG replay mismatch')
    record['rng_manifest_replays']=60
    original=ROOT/'working/baseline_artifacts/rf_final.pkl'
    native_record=stage_frozen_file(original,Path.home()/'.local/share/statsgeeks/frozen_rf',v.RFH)
    paths={'original':original,'optimized_native':Path(native_record['path'])}
    record['native_staging']=native_record;record['paths']={k:str(p) for k,p in paths.items()};record['runs']={}
    for name,path in paths.items():
        t=time.perf_counter();v.require(v.sha(path)==v.RFH,'RF bytes changed');hash_seconds=time.perf_counter()-t
        t=time.perf_counter()
        with path.open('rb') as f:forest=pickle.load(f)
        load_seconds=time.perf_counter()-t;out=[]
        for index in SELECTED:
            e=manifest['episodes'][index];t=time.perf_counter()
            s,q,centers,delta,pred,packet=v.reconstruct_episode(x,y,ids,state,e,forest)
            compute_seconds=time.perf_counter()-t
            saved_path=archive/'predictions'/f"{e['episode_id']}.npz"
            evidence=v.load(archive/f'evidence/worker_{index+1:02d}.json')
            v.require(v.digest(packet)==evidence['boundary_evidence']['packet_sha256'],'Archived packet hash mismatch')
            with np.load(saved_path,allow_pickle=False) as saved:
                v.require(np.array_equal(q,saved['query_indices']) and np.array_equal(ids[q],saved['query_ids']),'Archived query mismatch')
                pred['frozen_rf']=pred['rf_reproduced'].copy()
                for key,value in pred.items():
                    v.require(np.array_equal(value,saved[key]),'Prediction divergence: '+e['episode_id']+'/'+key)
                arrays={'query_indices':q,'query_ids':ids[q],**pred}
                # Preserve the producer's archive member order and serializer.
                buffer=io.BytesIO();np.savez_compressed(buffer,**{key:arrays[key] for key in saved.files})
            generated_sha=hashlib.sha256(buffer.getvalue()).hexdigest()
            generated_path=CERT/'evidence/reconstructed'/name/(e['episode_id']+'.npz')
            generated_path.parent.mkdir(parents=True,exist_ok=True)
            with generated_path.open('xb') as stream:stream.write(buffer.getvalue())
            frozen_inventory=v.load(archive/'artifact_hash_manifest.json')['files']
            expected_sha=frozen_inventory[saved_path.relative_to(ROOT).as_posix()]['sha256']
            reference=Artifact(archive,saved_path.relative_to(archive).as_posix(),e['episode_id'],expected_sha)
            generated=Artifact(CERT,generated_path.relative_to(CERT).as_posix(),e['episode_id'],generated_sha)
            payload_check=compare_artifacts(reference,generated,reference_owner=archive,candidate_owner=CERT,episode_id=e['episode_id'])
            # Full-archive byte identity is checked by producer_byte_replay.py
            # on the unchanged ORIGINAL WINDOWS coordinator serializer.
            metric_hash=v.digest({key:v.score(y[q],value) for key,value in pred.items()})
            out.append({'episode_id':e['episode_id'],'budget':e['budget'],'query_rows':len(q),'compute_seconds':compute_seconds,
                'prediction_npz_sha256':generated_sha,'metric_sha256':metric_hash,'packet_sha256':v.digest(packet),
                'reference_npz_sha256':expected_sha,'certification_artifact':generated_path.relative_to(CERT).as_posix(),
                'payload_check':payload_check,
                'array_hashes':{key:v.array_hash(value) for key,value in arrays.items()},
                'prototypes_sha256':v.array_hash(centers),'translation_sha256':v.array_hash(delta),
                'rng_before':e['rng_before'],'rng_after':e['rng_after']})
        record['runs'][name]={'rf_hash_seconds':hash_seconds,'rf_load_seconds':load_seconds,'episodes':out}
        del forest;gc.collect()
    for old,new in zip(record['runs']['original']['episodes'],record['runs']['optimized_native']['episodes']):
        v.require({k:a for k,a in old.items() if k not in ('compute_seconds','certification_artifact')}=={k:a for k,a in new.items() if k not in ('compute_seconds','certification_artifact')},'Original/native verification divergence')
    record['status']='OFFLINE_PAYLOAD_EQUIVALENCE_PASS_PENDING_PRODUCER_BYTE_REPLAY';record['total_seconds']=time.perf_counter()-start
    record['limits']=['No sandbox transport or candidate process launched; isolation code identity only.',
        'Three archived episodes, not full 60-episode experimental evaluation.','No E3 scientific verdict generated.']
    with (CERT/'evidence/offline_equivalence.json').open('x',encoding='utf8') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':
    try:main()
    except Exception as exc:
        with (CERT/'evidence/offline_equivalence_failure.json').open('x',encoding='utf8') as f:
            json.dump({'status':'FAIL','error':str(exc),'selected_episode_ordinals':[i+1 for i in SELECTED],'worker_launches':0},f,indent=2)
        raise
