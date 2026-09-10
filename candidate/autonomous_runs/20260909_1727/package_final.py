"""Explicitly stage the final candidate; never overwrite a previous package."""
from pathlib import Path
import sys,shutil,json,platform
sys.path.insert(0,str(Path(__file__).resolve().parent))
from sprint import H,R,sha,save,log
import numpy,scipy,sklearn,matplotlib,threadpoolctl

out=R/'candidate/experiments_agf'
assert not out.exists(),'Refusing to overwrite a prior final package'
files=['README.md','AUTONOMOUS_LEADERBOARD.json','LEADERBOARD.json','LATEST_BEST.json','FINAL_RESULTS.json','FINAL_REPORT.md','reproduce_best.py','agf_model.py','pool_state.pkl','SELECTION_LOCK.json','INFERENCE_MANIFEST.json','requirements-repro.txt','configuration.json','provenance.json','port_check.json','FIGURE_MANIFEST.json']
out.mkdir()
for name in files:shutil.copy2(H/name,out/name)
for name in ('verification_inputs','figures'):shutil.copytree(H/name,out/name)
shutil.copy2(H/'clean_replay/verification.json',out/'REPRODUCIBILITY.json')
for rel,digest in json.loads((H/'provenance.json').read_text())['protected'].items():assert sha(R/rel)==digest,rel
save('environment_final.json',dict(python=platform.python_version(),platform=platform.platform(),numpy=numpy.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,matplotlib=matplotlib.__version__,threadpoolctl=threadpoolctl.__version__))
shutil.copy2(H/'environment_final.json',out/'environment_final.json')
save('PACKAGING.json',dict(destination=str(out.relative_to(R)),official_winner_promotion=False,reason='Explicit final-candidate packaging only; development-locked coordinate variant, historical ASTRA retained',copied_files=[str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()],forbidden_training_material_absent=not (out/'sealed_evaluation.npz').exists(),protected_files_unchanged=True))
log('Final candidate staged at candidate/experiments_agf; no existing submission/presentation/baseline files changed')
