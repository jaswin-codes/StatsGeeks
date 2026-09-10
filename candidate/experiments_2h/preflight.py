from pathlib import Path
import hashlib,json,subprocess,time
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()

def manifest():
 return {p.relative_to(ROOT).as_posix():digest(p) for folder in ['candidate','data','original','working','docs','presentation','submission','submission_dry_run','models','scripts'] for p in (ROOT/folder).rglob('*') if p.is_file() and OUT not in p.parents and '__pycache__' not in p.parts}
if __name__=='__main__':
 import sys
 if '--verify' in sys.argv:
  before=json.loads((OUT/'protected_before.json').read_text()); after=manifest()
  changes=[k for k,v in before.items() if after.get(k)!=v]
  (OUT/'integrity.json').write_text(json.dumps({'pass':not changes,'changed_or_missing':changes,'files_checked':len(before),'artifact_sha256':after['candidate/artifacts/exp010_stage1_madrid.pkl']},indent=2))
  assert not changes,changes
 else:
  assert not (OUT/'protected_before.json').exists()
  (OUT/'git_status_before.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=ROOT))
  (OUT/'start.json').write_text(json.dumps({'unix_time':time.time(),'local_time':time.strftime('%Y-%m-%d %H:%M:%S')}))
  (OUT/'protected_before.json').write_text(json.dumps(manifest(),indent=2))
 print('Protection manifest complete')
