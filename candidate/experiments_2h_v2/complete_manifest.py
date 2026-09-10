"""Final read-only verification and comprehensive evidence checksums."""
from pathlib import Path
import hashlib,json,subprocess,datetime
H=Path(__file__).resolve().parent;R=H.parents[1];F=R/'candidate/competitor_forensics'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 out=H/'FULL_EVIDENCE_SHA256.json';assert not out.exists()
 protected=json.loads((F/'protected_before.json').read_text());assert all(sha(R/p)==s for p,s in protected.items())
 package=json.loads((H/'FINAL_SHA256SUMS.json').read_text());assert all(sha(R/p)==s for p,s in package.items())
 clean=json.loads((H/'locked_clean_replay/run.json').read_text());assert clean['pass']and clean['reference_arrays_exact']==1500 and clean['trials_per_budget']==100
 assert json.loads((H/'final_verification.json').read_text())['pass']
 head=subprocess.check_output(['git','-C',str(F/'competitor_snapshot'),'rev-parse','HEAD'],text=True).strip();assert head=='cf9af6cffea292af9460bf572de33c32a10212d9'
 subprocess.run(['git','-C',str(F/'competitor_snapshot'),'diff','--exit-code','HEAD'],check=True,stdout=subprocess.DEVNULL)
 files={};size=0
 for parent in [H,F]:
  for p in sorted(parent.rglob('*')):
   if not p.is_file()or'competitor_snapshot'in p.parts or p.suffix=='.onetoc2' or p.name=='complete_manifest.log':continue
   files[str(p.relative_to(R))]=sha(p);size+=p.stat().st_size
 result={'pass':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_protected_files_exact':len(protected),'initial_final_package_sha_exact':len(package),'competitor_snapshot_head':head,'competitor_tracked_worktree_unmodified':True,'source_and_500_episode_rebuild_pass':True,'candidate_reference_arrays_exact':1500,'files':files,'total_bytes_hashed':size,'exclusions':['OneNote ambient index files','competitor_snapshot: identified by immutable git SHA and clean tracked tree','this self-referential checksum file','active complete_manifest.log']}
 out.write_text(json.dumps(result,indent=2),encoding='utf-8');print('FINAL PASS;',len(files),'evidence files;',size,'bytes; frozen EXP010 and presentation intact',flush=True)
if __name__=='__main__':main()
