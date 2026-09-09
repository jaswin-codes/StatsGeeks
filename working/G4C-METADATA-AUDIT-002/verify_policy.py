"""Independent evidence review + synthetic fail-closed policy tests, no model data."""
from pathlib import Path
import json, hashlib, copy, datetime, importlib.util
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
def load(name):return json.loads((OUT/name).read_text())
initial=load('initial_metadata.json');later=load('metadata_after_observation.json');obs=load('observations.json');assoc=load('windows_file_association.json');refs=load('static_reference_audit.json')
assert initial['header_guid_le']==later['header_guid_le']=='43ff2fa1-efd9-4c76-9ee2-10ea5722765f'
assert assoc['.onetoc2']=='OneNote.TableOfContents.12'
assert assoc['OneNote.TableOfContents.12']=='Microsoft OneNote Table Of Contents'
assert 'ONENOTE.EXE' in assoc['OneNote.TableOfContents.12\\shell\\open\\command'].upper()
assert initial['sha256']!=later['sha256'] and initial['size']!=later['bytes']
assert obs['samples'][0]['sha256']==later['sha256'] and all(s['stable_during_read'] for s in obs['samples'])
assert 'G4C-METADATA-AUDIT-002' in later['utf16_directory_strings']
# Review actual worker input boundary without invoking it.
worker=(ROOT/'working/g4c_episode_worker.py').read_text();source=(ROOT/'working/g4c_source_worker.py').read_text();boundary=(ROOT/'working/g4c_boundary.py').read_text();runner=(ROOT/'working/run_g4c_candidate.py').read_text()
assert 'onetoc2' not in worker.lower()+source.lower()+boundary.lower()
assert "'/working'" in worker and "'/mnt'" in worker
assert "assert set(p)=={'X_support','y_support','support_ids','X_query','query_ids','source_state','parameters'}" in worker
assert "assert set(p)=={'X_source','y_source','parameters'}" in source
assert "cmd[ix:ix]=['--ro-bind',str(rf_path),'/app/rf_final.pkl']" in boundary
assert "cp=json.loads((ROOT/'working/G4C-PROVENANCE-CHECKPOINT/input_artifact_hashes.json').read_text())" in runner
# Absence of literal references is supplemented by explicit packet and mount review.
assert all(not c['literal_metadata_references'] for c in refs['code_files'] if c['path'] in ['working/g4c_episode_worker.py','working/g4c_source_worker.py','working/g4c_boundary.py'])
spec=importlib.util.spec_from_file_location('audit_policy',OUT/'integrity_policy.py');policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
assert policy.MUTABLE_PATH=='working/Open Notebook.onetoc2'
base={'sha256':'before','bytes':1,'mtime_ns':1,'file_id':17,'attributes':32,'signature_hex':policy.TOC_SIGNATURE.hex(),'regular':True,'links':1}
paths=['working/Open Notebook.onetoc2','working/g4c_episode_worker.py','working/run_g4c_candidate.py','working/G4C-E2-002/parameters.json','data/preprocessed/preprocessed_data.pkl','working/baseline_artifacts/rf_final.pkl','working/baseline_artifacts/Open Notebook.onetoc2','working/gate4_episode_manifest.json','working/G4C-E2-001/summary.json','working/G4C-E2-002/predictions/episode.npz','original/Open Notebook.onetoc2','original/4-Modelling.ipynb','working/nested/Open Notebook.onetoc2','working/another.onetoc2','working/gate4_runtime_narwhals_lock.json','runtime/numeric/numpy/__init__.py']
before={p:copy.deepcopy(base) for p in paths};tests=[]
for p in paths:
    after=copy.deepcopy(before);after[p]['sha256']='changed';after[p]['bytes']=2;after[p]['mtime_ns']=2
    result=policy.classify(before,after);expected=p==policy.MUTABLE_PATH
    assert result['pass']==expected,p
    tests.append({'change':p,'expected':'ALLOW_AND_LOG' if expected else 'STOP','passed':True})
for mode in ['delete','reparse','hardlink','wrong_signature','new_identity','attribute_change']:
    after=copy.deepcopy(before);r=after[policy.MUTABLE_PATH]
    if mode=='delete':del after[policy.MUTABLE_PATH]
    elif mode=='reparse':r['attributes']|=0x400
    elif mode=='hardlink':r['links']=2
    elif mode=='wrong_signature':r['signature_hex']='00'*16
    elif mode=='new_identity':r['file_id']=18
    elif mode=='attribute_change':r['attributes']=33
    assert not policy.classify(before,after)['pass'],mode
    tests.append({'change':'allowlisted metadata '+mode,'expected':'STOP','passed':True})
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata_type':'Windows-registered OneNote Table Of Contents; matching binary GUID and directory-name contents','external_mutability_established':True,'evidence':'Initial and subsequent reads changed without any audit writer targeting the file; new audit directory name appears in metadata. No candidate launched.','writer_pid_attributed':False,'writer_attribution_limit':'OneNote/OneDrive processes present; Restart Manager returned no resource users; neither proves write-event ownership.','policy_justified':True,'justification':'Exact path is unrelated to model/data packet contents and cannot be mounted in candidate sandbox. Existing broad integrity inventory is its only G4C execution dependency. Metadata mutability is established even though writer identity is not.','allowed_path':policy.MUTABLE_PATH,'tests':tests,'tests_count':len(tests),'test_method':'Synthetic dictionaries only, no mutations to any project input','no_candidate_workers':True,'policy_sha256':hashlib.sha256((OUT/'integrity_policy.py').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (OUT/'independent_policy_verification.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'tests':len(tests),'external_mutability':True,'writer_identified':False}))
