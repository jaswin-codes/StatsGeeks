"""Final read-only consistency/security audit; no prediction or scoring execution."""
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1];RUN=ROOT/'working/G4B-E1-001';MH='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def main():
 m=json.load(open(ROOT/'working/gate4_episode_manifest.json'));rows=json.load(open(RUN/'per_episode_results.json'));summary=json.load(open(RUN/'summary.json'));source=json.load(open(RUN/'source_state.json'))
 assert sha(ROOT/'working/gate4_episode_manifest.json')==MH and len(rows)==60
 assert json.load(open(RUN/'independent_verification.json'))['status']=='PASS'
 assert hashlib.sha256(canonical(source['source_state'])).hexdigest()==source['source_state_sha256']
 for e,row in zip(m['episodes'],rows):
  assert e['episode_id']==row['episode_id'];p=RUN/'evidence'/('worker_'+f"{m['episodes'].index(e)+1:02d}.json");z=json.load(open(p));r=z['result'];ev=z['boundary_evidence']
  expected=hashlib.sha256(canonical(e['support_pixel_ids'])).hexdigest();assert r['adaptation_state']['support_ids_sha256']==expected
  assert r['adaptation_state']['source_state_sha256']==source['source_state_sha256']
  assert r['query_fingerprint']==hashlib.sha256(canonical(__import__('numpy').load(ROOT/row['prediction_artifact'])['query_ids'].tolist())).hexdigest()
  assert r['label_access']=={'source_state_only':True,'current_support_labels':4*e['budget'],'query_labels':0,'other_episode_labels':0}
  assert ev['returncode']==0 and ev['reason'] is None and not ev['stderr'] and ev['teardown_pass'] and not ev['lifecycle']['final_survivors']
 assert summary['episodes_completed']==60 and summary['candidate_models']==['E1 only'] and not summary['backup_candidates_run']
 pins=summary['baseline_hashes'];assert len(pins)==33 and all(sha(ROOT/p)==h for p,h in pins.items())
 assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT);assert not subprocess.check_output(['git','diff','--','original/'],cwd=ROOT)
 result={'status':'PASS','episode_outputs':60,'query_fingerprints':60,'source_state_hashes':60,'current_support_label_scopes':60,'teardown':60,'E2_E5':False,'manifest_sha256':MH,'protected_33':'PASS','original_clean':True,'auditor_sha256':sha(__file__)}
 with (RUN/'final_audit.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
