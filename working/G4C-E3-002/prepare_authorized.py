"""Apply existing asset generator to explicitly authorized prelaunch-only directory."""
import datetime, hashlib, importlib.util, json, pathlib, sys, shutil
ROOT=pathlib.Path(__file__).resolve().parents[2];RUN=ROOT/'working/G4C-E3-002'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
assert json.loads((RUN/'preflight_integrity.json').read_text())['status']=='PASS'
assert not (RUN/'coordinator').exists()
for d in ('coordinator','checkpoint','candidate_state','evidence','predictions','results','validation','hashes'):(RUN/d).mkdir()
old=RUN/'EXECUTION_REPORT.md';original_hash=sha(old)
old.rename(RUN/'checkpoint/PRELAUNCH_EXECUTION_REPORT.md')
assert sha(RUN/'checkpoint/PRELAUNCH_EXECUTION_REPORT.md')==original_hash
approval={'run_id':RUN.name,'candidate':'E3','scope':'execution','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorization':'User explicitly authorizes proceeding after prelaunch stop and accepting only CERT-004 documented OneNote metadata change; all scientific/runtime/isolation/integrity/validation checks retained. No E4/E5.','metadata_exception':{'path':'working/G4C-INFRA-PERF-001/code/Open Notebook.onetoc2','accepted_sha256':'e2e685e8b6be61f2d70f5e33191a4629a1b92d1516f1f6c1738ace9a75904025'},'prelaunch_report_preserved_sha256':original_hash,'no_prior_predictions_or_state_reused':True}
p=load_module('approved_preparation',ROOT/'working/G4C-INFRA-PERF-001/code/prepare_assets.py')
files=p.asset_bytes()
for name,data in files.items():
    assert data==(ROOT/'working/G4C-INFRA-CERT-004/coordinator'/name).read_bytes(),name
files['execution_coordinator.py']=files['execution_coordinator.py'].replace(b'G4C-E3-001',RUN.name.encode())
files['native_cache.json']=(ROOT/'working/G4C-INFRA-CERT-004/coordinator/native_cache.json').read_bytes()
for name,data in files.items():
    with (RUN/'coordinator'/name).open('xb') as f:f.write(data)
record={'authorization':approval,'source':'working/G4C-E3-001/coordinator','changes':['existing certified bounded signature read','existing certified native RF transport','new run identity only','authorized preparation in existing prelaunch-only directory'],'code_hashes':{n:hashlib.sha256(v).hexdigest() for n,v in files.items()},'experiments_launched':0}
with (RUN/'checkpoint/infrastructure_preparation.json').open('x') as f:json.dump(record,f,indent=2)
# Existing binding tool is copied unchanged; it exclusively copies/binds the validator.
for name in ('bind_e3_validation.py',):
    with (RUN/'coordinator'/name).open('xb') as f:f.write((ROOT/'working/G4C-INFRA-CERT-003/code'/name).read_bytes())
sys.path.insert(0,str(ROOT/'working/G4C-INFRA-CERT-003/code'))
import bind_e3_validation
print(json.dumps(bind_e3_validation.bind_e3_validation(RUN),indent=2))
