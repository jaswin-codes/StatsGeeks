"""Read-only prelaunch audit; only writes evidence inside the authorized run."""
import datetime, hashlib, json, pathlib, subprocess, time
ROOT = pathlib.Path(__file__).resolve().parents[2]
RUN = ROOT/'working/G4C-E3-002'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    start=time.perf_counter()
    cert=ROOT/'working/G4C-INFRA-CERT-004'
    expected=json.loads((cert/'hashes/protected_before.json').read_text())['files']
    exception='working/G4C-INFRA-PERF-001/code/Open Notebook.onetoc2'
    expected[exception]={'sha256':'e2e685e8b6be61f2d70f5e33191a4629a1b92d1516f1f6c1738ace9a75904025','bytes':6160}
    expected.update(json.loads((cert/'artifact_hash_manifest.json').read_text())['files'])
    expected['working/G4C-INFRA-CERT-004/artifact_hash_manifest.json']={'sha256':sha(cert/'artifact_hash_manifest.json'),'bytes':(cert/'artifact_hash_manifest.json').stat().st_size}
    checks=[]
    for rel,v in expected.items():
        p=ROOT/rel
        observed={'sha256':sha(p),'bytes':p.stat().st_size} if p.is_file() else None
        checks.append({'path':rel,'expected':v,'observed':observed,'pass':observed is not None and all(observed[k]==v[k] for k in ('sha256','bytes'))})
    protected=json.loads((ROOT/'working/G4B-E1-001/entry.json').read_text())['protected_hashes']
    protected_checks=[{'path':p,'expected_sha256':h,'observed_sha256':sha(ROOT/p),'pass':sha(ROOT/p)==h} for p,h in protected.items()]
    original=subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT).decode()
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorized_exception':exception,'historical_checks':checks,'protected_checks':protected_checks,'original_git_status':original,'seconds':time.perf_counter()-start}
    result['status']='PASS' if all(c['pass'] for c in checks+protected_checks) and not original else 'FAIL'
    with (RUN/'preflight_integrity.json').open('x') as f: json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'historical_count':len(checks),'protected_count':len(protected_checks),'failures':[c for c in checks+protected_checks if not c['pass']],'seconds':result['seconds']},indent=2))
    if result['status']!='PASS': raise SystemExit(1)
if __name__=='__main__':main()
