"""Independent read-only reload of checkpoint, passive evidence, and frozen hashes."""
from pathlib import Path
import hashlib,json,subprocess,datetime,os,stat
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];CP=ROOT/'working/G4C-PROVENANCE-CHECKPOINT-002'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def load(p):return json.loads(p.read_text())
check=load(CP/'checkpoint.json');dry=load(OUT/'dry_run_results.json');pins=load(CP/'file_fingerprints.json')
assert sha(CP/'file_fingerprints.json')==check['fingerprints_sha256']
assert check['allowed_mutable_paths']==['working/Open Notebook.onetoc2']
assert dry['status']=='PASS' and dry['seconds']>=180 and len(dry['samples'])==37
assert not dry['unexpected_additions'] and not dry['classification']['failures'] and dry['candidate_workers_launched']==0
assert sha(OUT/'integrity_policy.py')==check['policy_sha256']
changed=[]
for rel,before in pins.items():
    p=ROOT/rel;s=p.lstat();assert stat.S_ISREG(s.st_mode) and not s.st_file_attributes&0x400 and s.st_nlink==1
    with p.open('rb') as f:signature=f.read(16).hex()
    after={'sha256':sha(p),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'file_id':s.st_ino,'attributes':s.st_file_attributes,'signature_hex':signature,'regular':True,'links':1}
    if before!=after:
        assert rel=='working/Open Notebook.onetoc2',rel
        for key in ['file_id','attributes','signature_hex','regular','links']:assert before[key]==after[key]
        changed.append({'path':rel,'before':before,'after':after})
# Independently confirm the second externally observed update, captured around
# necessary checkpoint-directory creation, not during the later stable wait.
a=check['metadata_before_directory_creation'];b=check['metadata_at_checkpoint'];assert a['sha256']!=b['sha256']
for key in ['file_id','attributes','signature_hex','regular','links']:assert a[key]==b[key]
assert b['signature_hex']=='a12fff43d9ef764c9ee210ea5722765f'
entry=load(ROOT/'working/G4B-E1-001/entry.json')
assert len(entry['protected_hashes'])==33 and all(sha(ROOT/p)==h for p,h in entry['protected_hashes'].items())
assert sha(ROOT/'working/gate4_episode_manifest.json')=='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT)
closed=load(ROOT/'working/G4C-E2-001/artifact_hash_manifest.json');assert all(sha(ROOT/p)==v['sha256'] for p,v in closed['files'].items())
pre=load(CP/'runtime_verification_before.json');post=load(OUT/'runtime_verification_after.json')
assert pre==post and post['tree_match'] and post['files']==4355 and post['bwrap_match'] and all(post['wheel_matches'].values())
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoint_files_rehashed':len(pins),'nonallowlisted_changes':0,'metadata_changes_since_checkpoint':changed,'second_observed_metadata_update_valid_under_policy':True,'metadata_samples_in_dryrun':37,'dryrun_seconds':dry['seconds'],'dryrun_changes':0,'protected_33':'PASS','original_clean':True,'closed_G4C_E2_001_inventory':'PASS','runtime_before_after':'MATCH','candidate_workers_launched':0,'candidate_data_loaded':False,'candidate_prediction_verification':'NOT_RUN_NOT_AUTHORIZED','policy_scope':'Exact path only; tests use synthetic maps, not modified real files','verifier_sha256':sha(Path(__file__))}
with (OUT/'independent_dryrun_verification.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
