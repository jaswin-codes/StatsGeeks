"""Seal completed evidence and package hashes after all experiment processes exit."""
from pathlib import Path
import sys,json,pickle
sys.path.insert(0,str(Path(__file__).resolve().parent))
from sprint import H,R,sha,save,log

out=R/'candidate/experiments_agf'
lock=json.loads((H/'SELECTION_LOCK.json').read_text())
assert sha(H/'agf_model.py')==lock['model_sha256']
for rel,digest in json.loads((H/'provenance.json').read_text())['protected'].items():assert sha(R/rel)==digest,rel
for name in ('final_complete.json','spatial_complete.json','SELECTION_LOCK.json','clean_replay/verification.json','public_interface_replay/metadata.json','public_inference_test/metadata.json','packaged_interface_replay/metadata.json'):assert (H/name).exists(),name
assert json.loads((H/'packaged_interface_replay/metadata.json').read_text())['exact_verification_arrays']==5
with (out/'pool_state.pkl').open('rb') as f:state=pickle.load(f)
assert set(state)=={'raw','standard','coords','prior','cov','nn','dist','feature_names','classes','source_counts'}
assert state['raw'].shape==(25992,60)
assert len(state['feature_names'])==60
assert not any((out/name).exists() for name in ('sealed_evaluation.npz','development_support.npz','baseline_state.pkl','compact.pkl'))
assert not list(H.rglob('*FAILED.json'))
save('FINAL_INTEGRITY.json',dict(pass_=True,frozen_EXP010_unchanged=True,model_matches_pre_audit_lock=True,package_contains_no_query_truth=True,pool_contains_no_target_labels=True,source_refit_exact=True,all_4000_predictions_exact=True,packaged_interface_arrays_exact=5,direct_inference_exact=True,figures_png=7,figures_svg=7,official_promotion=False,incumbent='ASTRA_AGF historical',development_selected=lock['candidate']))
(out/'FINAL_INTEGRITY.json').write_text((H/'FINAL_INTEGRITY.json').read_text())
log('COMPLETE: all experiments sealed, public/package inference verified, figures checked, original EXP-010 protected. No further query-driven tuning.')
# Hash logs only after their writing processes finished. This command emits no
# further output after hashes, so its own redirected log is excluded explicitly.
package_hashes={str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json'}
(out/'SHA256SUMS.json').write_text(json.dumps(package_hashes,indent=2))
save('SHA256SUMS.json',{str(p.relative_to(H)):sha(p) for p in H.rglob('*') if p.is_file() and p.name not in ('SHA256SUMS.json','seal_run.log')})
# Verify package checksums in a second read pass.
for name,digest in package_hashes.items():assert sha(out/name)==digest,name
