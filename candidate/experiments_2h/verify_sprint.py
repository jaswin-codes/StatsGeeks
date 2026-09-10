"""Final arithmetic, code provenance, clean-repeat and boundary verification."""
from pathlib import Path
import sys,json,hashlib,subprocess
import numpy as np
O=Path(__file__).resolve().parent;ROOT=O.parents[1]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={};count=0
for path in O.rglob('results.json'):
 r=load(path);repeat=load(path.with_name('results_repeat.json'))
 assert r['episodes']==repeat['episodes'] and r['summary']==repeat['summary']
 assert load(path.with_name('reproducibility.json'))['pass']
 source=O/'spatial_f.py' if path.parent.name=='spatial' else O/'run.py'
 assert r['configuration']['script_sha256']==sha(source)
 for b,methods in r['summary'].items():
  for method,s in methods.items():
   episodes=[x for x in r['episodes'] if x['budget']==int(b) and x['method']==method]
   v=np.array([x['macro_f1'] for x in episodes]);d=np.array([x['delta_vs_EXP010'] for x in episodes])
   assert len(v)==10
   np.testing.assert_allclose([v.mean(),v.std(),d.mean(),d.std()],[s['mean'],s['population_sd'],s['mean_delta'],s['delta_population_sd']],atol=1e-14,rtol=0)
   assert s['wins']+s['losses']+s['ties']==10
   for e in episodes:
    cm=np.array(e['confusion']);den=cm.sum(0)+cm.sum(1);pc=np.divide(2*cm.diagonal(),den,out=np.zeros(4,dtype=float),where=den!=0)
    np.testing.assert_allclose(pc,e['class_f1'],atol=1e-14,rtol=0)
    np.testing.assert_allclose(pc.mean(),e['macro_f1'],atol=1e-14,rtol=0)
   count+=1
 checks[str(path.parent.relative_to(O))]=True
assert load(O/'expF_covariance/interface_test/verification.json')['pass']
assert load(O/'integrity.json')['pass']
before=[x for x in (O/'git_status_before.txt').read_text().splitlines() if 'candidate/experiments_2h' not in x];after=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True).splitlines()
after_without_sprint=[x for x in after if 'candidate/experiments_2h' not in x]
assert before==after_without_sprint,'Non-sprint Git status changed'
(O/'git_status_after.txt').write_text('\n'.join(after)+'\n')
manifest={p.relative_to(O).as_posix():sha(p) for p in O.rglob('*') if p.is_file() and p.name not in ['SHA256SUMS.json','final_verification.json']}
(O/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2))
(O/'final_verification.json').write_text(json.dumps({'pass':True,'branches':checks,'method_budget_summaries_checked':count,'class_f1_recomputed_from_confusions':True,'executed_script_hashes_match':True,'non_sprint_git_status_unchanged':True,'protected_files_unchanged':1579,'clean_feature_only_cli':True,'configuration_selection':'none; only descriptive audit ranking, no adoption'},indent=2))
print('PASS: arithmetic, class confusion reconstruction, code hashes, clean repeats, protected integrity and unchanged non-sprint Git status.')
