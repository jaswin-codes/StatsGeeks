"""Replay ONLY serialization on the original Windows coordinator environment.

Consumes certification reconstruction artifacts; does not load a model or launch
workers. Retains the complete historical NPZ SHA256 equality assertion in addition
to strict decompressed-payload identity and each artifact's provenance hashes.
"""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import zlib
import numpy as np
import e3_validator as v
from prediction_equivalence import Artifact, NAMES, compare_artifacts

ROOT=Path(__file__).resolve().parents[3]
CERT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'working/G4C-E3-001'


def main():
    v.require(sys.platform=='win32','Byte-replay gate requires original Windows producer platform')
    profile=v.load(CERT/'evidence/npz_forensics_windows.json')
    v.require(np.__version__==profile['numpy'] and zlib.ZLIB_RUNTIME_VERSION==profile['zlib_runtime'], 'Producer serializer profile changed')
    v.require(v.sha(np.lib._npyio_impl.__file__)==profile['numpy_writer_source_sha256'] and
              v.sha(zipfile.__file__)==profile['zipfile_source_sha256'],'Producer serializer source changed')
    records=v.load(CERT/'evidence/offline_equivalence.json')
    v.require(records['status']=='OFFLINE_PAYLOAD_EQUIVALENCE_PASS_PENDING_PRODUCER_BYTE_REPLAY','Payload gate not passed')
    inventory=v.load(ARCHIVE/'artifact_hash_manifest.json')['files'];results=[]
    for mode,data in records['runs'].items():
        for episode in data['episodes']:
            eid=episode['episode_id'];source=CERT/episode['certification_artifact'];archived=ARCHIVE/'predictions'/(eid+'.npz')
            expected=inventory[archived.relative_to(ROOT).as_posix()]['sha256']
            reference=Artifact(ARCHIVE,'predictions/'+eid+'.npz',eid,expected)
            generated=Artifact(CERT,episode['certification_artifact'],eid,episode['prediction_npz_sha256'])
            compare_artifacts(reference,generated,reference_owner=ARCHIVE,candidate_owner=CERT,episode_id=eid)
            with np.load(source,allow_pickle=False) as saved:
                arrays={key:saved[key].copy(order='K') for key in NAMES}
            replays=[]
            for repeat in (1,2):
                target=CERT/'evidence/producer_replay'/mode/str(repeat)/(eid+'.npz');target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as stream:np.savez_compressed(stream,**arrays)
                actual=v.sha(target)
                v.require(actual==expected,'FULL_ARCHIVE_BYTE_IDENTITY_FAILED: '+eid+'/'+mode)
                replay=Artifact(CERT,target.relative_to(CERT).as_posix(),eid,actual)
                check=compare_artifacts(reference,replay,reference_owner=ARCHIVE,candidate_owner=CERT,episode_id=eid)
                v.require(check['archive_bytes_equal'],'NPZ SHA equality without actual byte equality')
                replays.append({'path':target.relative_to(CERT).as_posix(),'bytes':target.stat().st_size,'sha256':actual})
            v.require(replays[0]['sha256']==replays[1]['sha256'],'Repeat serializer nondeterminism')
            results.append({'mode':mode,'episode_id':eid,'replays':replays,'reference_sha256':expected,
                            'file_byte_identity':True,'payload_identity':True})
    for eid in {r['episode_id'] for r in results}:
        same=[r['reference_sha256'] for r in results if r['episode_id']==eid]
        v.require(len(same)==2 and len(set(same))==1,'Original/optimized archive mismatch')
    record={'status':'BYTE_AND_PAYLOAD_EQUIVALENCE_PASS','python':sys.version,'numpy':np.__version__,
            'zlib':zlib.ZLIB_RUNTIME_VERSION,'episodes':3,'inference_paths':2,'serialization_replays':len(results)*2,
            'results':results,'workers_launched':0,'models_loaded':0,'production_writer_modified':False}
    with (CERT/'evidence/producer_byte_equivalence.json').open('x',encoding='utf8') as stream:
        json.dump(record,stream,indent=2);stream.write('\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
