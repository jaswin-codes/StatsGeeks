"""Provenance checkpoint and passive metadata exception dry-run. No model imports."""
from pathlib import Path
import datetime,hashlib,json,subprocess,time,importlib.util,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];CP=ROOT/'working/G4C-PROVENANCE-CHECKPOINT-002'
spec=importlib.util.spec_from_file_location('metadata_integrity_policy',OUT/'integrity_policy.py');policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
def save(p,obj):
    with p.open('x',encoding='utf8') as f:json.dump(obj,f,indent=2);f.write('\n')
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def git(args):return subprocess.check_output(['git']+args,cwd=ROOT,stderr=subprocess.DEVNULL)
def linux(p):
    s=p.resolve().as_posix();return '/mnt/'+s[0].lower()+s[2:]
def runtime(output):
    code='''import pathlib,json,hashlib,sys
root=pathlib.Path(sys.argv[1]); output=pathlib.Path(sys.argv[2])
def sha(p):
 with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
p=root/'working/gate4_runtime_narwhals_lock.json';lock=json.loads(p.read_text());image=pathlib.Path(lock['image_path'])
actual={f.relative_to(image).as_posix():sha(f) for f in sorted(image.rglob('*')) if f.is_file()}
r={'lock_sha256':sha(p),'tree_sha256':lock['tree_sha256'],'files':len(actual),'tree_match':actual==lock['files'],'wheel_matches':{n:sha(v['source'])==v['sha256'] for n,v in lock['wheels'].items()},'bwrap_match':sha('/usr/bin/bwrap')==lock['bwrap_sha256'],'python':sys.version,'no_worker_launched':True}
assert r['lock_sha256']=='cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514'
assert r['tree_match'] and all(r['wheel_matches'].values()) and r['bwrap_match']
with output.open('x') as f:json.dump(r,f,indent=2)
print(json.dumps(r))
'''
    result=subprocess.run(['wsl','-d','Ubuntu','--exec','/usr/bin/python3','-B','-c',code,linux(ROOT),linux(output)],capture_output=True,text=True,timeout=120)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    return json.loads(output.read_text())
def frozen():
    entry=json.loads((ROOT/'working/G4B-E1-001/entry.json').read_text());matches={p:sha(ROOT/p)==h for p,h in entry['protected_hashes'].items()};assert len(matches)==33 and all(matches.values())
    checks={}
    for run in ['G4A-TEARDOWN-002','G4B-E1-001']:
        inv=json.loads((ROOT/'working'/run/'artifact_hash_manifest.json').read_text())
        checks[run]={p:sha(ROOT/p)==v['sha256'] for p,v in inv['files'].items() if p.startswith('working/')}
        assert all(checks[run].values())
    closed=json.loads((ROOT/'working/G4C-E2-001/artifact_hash_manifest.json').read_text())
    closedcheck={p:sha(ROOT/p)==v['sha256'] for p,v in closed['files'].items()};assert all(closedcheck.values())
    assert not git(['status','--short','--','original/']) and not git(['diff','--','original/'])
    mh=sha(ROOT/'working/gate4_episode_manifest.json');assert mh=='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
    # Read historical result summary only, never candidate feature/model arrays.
    e1=json.loads((ROOT/'working/G4B-E1-001/summary.json').read_text());assert e1['verdict']=='FALSIFIED' and e1['status']=='PASS'
    baseline=e1['summary']['25']['raw_prototype'];assert round(baseline['mean'],4)==.5986 and round(baseline['std_ddof0'],4)==.0176
    assert not any((ROOT/'working'/f'G4C-E{k}-001').exists() for k in [3,4,5]) and not (ROOT/'working/G4C-E2-002').exists()
    return {'protected_33':matches,'historical_inventories':checks,'closed_E2_inventory':closedcheck,'manifest_sha256':mh,'rf_sha256':sha(ROOT/'working/baseline_artifacts/rf_final.pkl'),'original_clean':True,'E1_verdict':'FALSIFIED','Gate4A':'PASS','Gate4B':'PASS','baseline_25':baseline,'candidate_workers_launched':0}
def paths():
    files={p for top in ['working','data','original'] for p in (ROOT/top).rglob('*') if p.is_file()}
    tracked=git(['ls-files','-z']).decode().split('\0')
    files.update(ROOT/p for p in tracked if p and (ROOT/p).is_file())
    return {p.relative_to(ROOT).as_posix() for p in files}
def main():
    verification=json.loads((OUT/'independent_policy_verification.json').read_text());assert verification['policy_justified'] and verification['status']=='PASS'
    assert verification['policy_sha256']==sha(OUT/'integrity_policy.py')
    before_creation=policy.fingerprint(ROOT,policy.MUTABLE_PATH)
    # New evidence directory only; no previous checkpoint or run may be overwritten.
    CP.mkdir(exist_ok=False)
    for name,args in [('git_HEAD.txt',['rev-parse','HEAD']),('git_status.txt',['status','--short']),('git_diff_stat.txt',['diff','--stat']),('git_diff.binary.patch',['diff','--binary']),('git_diff_cached.binary.patch',['diff','--cached','--binary']),('git_index.txt',['ls-files','--stage'])]:
        with (CP/name).open('xb') as f:f.write(git(args))
    with (CP/'authorization.md').open('x',encoding='utf8') as f:f.write('# Authorization\n\nUser authorized metadata provenance analysis, path-scoped policy justification, a new checkpoint, and non-modelling dry-run only. No E2/E3/E4/E5 execution or candidate worker launch is authorized. Historical dirty state is preserved. No cleanup/reset/restore/checkout/stash/commit was performed.\n\nOpen Notebook.onetoc2 is explicitly treated as external mutable\nmetadata under a path-specific integrity exception. All other\npre-existing experiment files remain immutable.\n\nExact mutable path: `working/Open Notebook.onetoc2`. Writer identity is not proven. Reference policy is audit-only and not installed in existing runners.\n')
    save(CP/'metadata_exception_policy.json',json.loads((OUT/'exception_policy.json').read_text()))
    save(CP/'frozen_preconditions.json',frozen());runtime(CP/'runtime_verification_before.json')
    # Capture ALL current pre-existing working files (including current new evidence),
    # datasets/original and tracked project files. No extension excludes.
    selected=sorted(paths());before={p:policy.fingerprint(ROOT,p) for p in selected}
    save(CP/'file_fingerprints.json',before)
    save(CP/'checkpoint.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git_head':git(['rev-parse','HEAD']).decode().strip(),'allowed_mutable_paths':[policy.MUTABLE_PATH],'fingerprint_count':len(before),'fingerprints_sha256':sha(CP/'file_fingerprints.json'),'policy_sha256':sha(OUT/'integrity_policy.py'),'metadata_before_directory_creation':before_creation,'metadata_at_checkpoint':before[policy.MUTABLE_PATH],'new_evidence_destinations':['working/G4C-METADATA-AUDIT-002/','working/G4C-PROVENANCE-CHECKPOINT-002/'],'no_candidate_execution_authorized':True})
    samples=[];started=time.monotonic()
    for i in range(37):
        if i:time.sleep(max(0,started+i*5-time.monotonic()))
        record=policy.fingerprint(ROOT,policy.MUTABLE_PATH);record['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();samples.append(record)
        result=policy.classify({policy.MUTABLE_PATH:before[policy.MUTABLE_PATH]},{policy.MUTABLE_PATH:{k:v for k,v in record.items() if k!='utc'}})
        if not result['pass']:raise RuntimeError(str(result))
    elapsed=time.monotonic()-started
    after={p:policy.fingerprint(ROOT,p) for p in selected if (ROOT/p).exists()};classification=policy.classify(before,after)
    newpaths=paths()-set(selected)
    newaudit=[p for p in sorted(newpaths) if p.startswith('working/G4C-METADATA-AUDIT-002/') or p.startswith('working/G4C-PROVENANCE-CHECKPOINT-002/')]
    unexpected=sorted(newpaths-set(newaudit))
    result={'status':'PASS' if classification['pass'] and not unexpected else 'STOP','seconds':elapsed,'samples':samples,'classification':classification,'preexisting_file_count':len(before),'unexpected_additions':unexpected,'new_evidence_files':newaudit,'candidate_workers_launched':0,'candidate_data_loaded':False,'candidate_models_fit':0,'policy_tests':'independent_policy_verification.json (22 synthetic tests)','baseline':'0.5986 +/- 0.0176','runner_modified':False}
    save(OUT/'dry_run_results.json',result)
    if result['status']!='PASS':raise RuntimeError(str(classification)+str(unexpected))
    save(OUT/'frozen_postflight.json',frozen());runtime(OUT/'runtime_verification_after.json')
    print(json.dumps({'status':result['status'],'files_checked':len(before),'seconds':elapsed,'metadata_changes':classification['allowed_metadata_changes'],'new_evidence_files':newaudit},indent=2))
if __name__=='__main__':
    try:main()
    except BaseException:
        import traceback
        with (OUT/'STOP_REASON.md').open('x',encoding='utf8') as f:f.write('# STOP — metadata checkpoint/dry-run failure\n\n```\n'+traceback.format_exc()+'\n```\n')
        raise
