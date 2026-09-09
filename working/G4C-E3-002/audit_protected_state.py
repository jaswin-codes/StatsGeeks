"""Post-execution exact audit against this run's prelaunch expectations."""
import datetime,hashlib,json,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[2];RUN=ROOT/'working/G4C-E3-002'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
start=time.perf_counter();before=json.loads((RUN/'preflight_integrity.json').read_text());checks=[]
for c in before['historical_checks']:
    p=ROOT/c['path'];v={'sha256':sha(p),'bytes':p.stat().st_size} if p.is_file() else None
    checks.append({'path':c['path'],'expected':c['observed'],'observed':v,'pass':v==c['observed']})
protected=[{'path':c['path'],'expected_sha256':c['expected_sha256'],'observed_sha256':sha(ROOT/c['path']),'pass':sha(ROOT/c['path'])==c['expected_sha256']} for c in before['protected_checks']]
original=subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT).decode()
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_checks':checks,'protected_checks':protected,'original_git_status':original,'seconds':time.perf_counter()-start}
r['status']='PASS' if all(c['pass'] for c in checks+protected) and not original else 'FAIL'
with (RUN/'hashes/protected_after.json').open('x') as f:json.dump(r,f,indent=2)
print(json.dumps({'status':r['status'],'historical_files':len(checks),'protected_files':len(protected),'seconds':r['seconds'],'failures':[c for c in checks+protected if not c['pass']]},indent=2))
if r['status']!='PASS':raise SystemExit(1)
