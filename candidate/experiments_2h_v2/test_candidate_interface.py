"""Clean public-API source rebuild, artifact reload, input safety and exact predictions."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,pickle,inspect,hashlib
import numpy as np
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from candidate_predict import fit_pool,adapt_and_predict
from candidate.experiments_2h.run import setup,save,sha

def main():
 reload='--reload'in sys.argv;out=H/('candidate_interface_reload.json'if reload else'candidate_interface.json');assert not out.exists();st,d=setup();cfg=json.loads((H/'FINAL_SELECTION.json').read_text())
 if reload:
  with(H/'astra_pool_state.pkl').open('rb')as f:state=pickle.load(f)
 else:
  # The public pool fitter is supplied NO target labels or target-derived class counts.
  state=fit_pool(d['X_madrid'],d['y_madrid'],d['pixel_ids_madrid'],d['X_amsterdam'],d['pixel_ids_amsterdam'],d['scaler'].mean_,d['scaler'].scale_,source_basis=cfg['source_basis'],local_leaf=cfg['local_leaf'])
  np.testing.assert_array_equal(state['prior'],np.load(H/'physical_source_priors.npz')['physical1'])
  state['feature_names']=d['feature_names'];state['source_data_sha256']=st['source_data_sha256'];state['frozen_recipe']=cfg
  with(H/'astra_pool_state.pkl').open('xb')as f:pickle.dump(state,f)
 arrays=np.load(H/'capacity_leaf1_audit.npz');n_checked=0
 for t in [0,9]:
  for b in [5,25,50,100,200]:
   tag=f'b{b}_t{t}';s=arrays[tag+'_s'];q=arrays[tag+'_q'];p,prob=adapt_and_predict(state,s,d['y_amsterdam'][s].copy(),b,return_proba=True);np.testing.assert_array_equal(p[q],arrays[tag+'_pred']);assert np.isfinite(prob).all();np.testing.assert_allclose(prob.sum(1),1,atol=1e-12,rtol=0);n_checked+=1
 s=arrays['b5_t0_s'];ys=d['y_amsterdam'][s].copy();invalid=[(s[:-1],ys[:-1],5),(np.zeros_like(s),ys,5),(s,ys,6),(s,np.full_like(ys,9),5),(np.full_like(s,-1),ys,5)];rejected=0
 for si,yi,b in invalid:
  try:adapt_and_predict(state,si,yi,b)
  except ValueError:rejected+=1
  else:raise AssertionError('Invalid support accepted')
 forbidden={'age_class','weighted_mean_year','coverage','px_key','py_key'};assert not forbidden.intersection(d['feature_names'])
 for f,h in cfg['files_sha256'].items():assert sha(H/f)==h
 save(out,{'pass':True,'reload_only':reload,'exact_episode_prediction_arrays':n_checked,'invalid_support_cases_rejected':rejected,'probability_normalization':True,'source_prior_reproduced_from_scratch':not reload,'target_labels_in_fit_pool_signature':False,'fit_pool_signature':str(inspect.signature(fit_pool)),'adapt_signature':str(inspect.signature(adapt_and_predict)),'forbidden_feature_names_absent':True,'target_state_has_no_ground_truth_labels':not any('label'in k for k in state),'artifact_sha256':sha(H/'astra_pool_state.pkl'),'pool_hash':state['pool_hash'],'frozen_recipe_hashes_pass':True})
 print('PASS','reload'if reload else'fresh source and inference',flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
