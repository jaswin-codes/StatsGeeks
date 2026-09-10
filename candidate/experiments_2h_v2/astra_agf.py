"""Pinned final ASTRA-AGF entry point (no experimental recipe defaults exposed)."""
from candidate_predict import fit_pool as _fit_pool,adapt_and_predict as _predict

def fit_pool(source_features,source_labels,source_coords,target_features,target_coords,
             source_mean,source_scale,*,aligned_source_model=None,aligned_model_pool_hash=None):
 return _fit_pool(source_features,source_labels,source_coords,target_features,target_coords,
                  source_mean,source_scale,source_basis='physical',local_leaf=1,
                  aligned_source_model=aligned_source_model,aligned_model_pool_hash=aligned_model_pool_hash)

def adapt_and_predict(pool_state,support_indices,support_labels,budget,return_proba=False):
 if pool_state.get('method')!='ASTRA-AGF'or pool_state.get('source_basis')!='physical'or pool_state.get('local_leaf')!=1:
  raise ValueError('Not the locked final ASTRA-AGF recipe')
 return _predict(pool_state,support_indices,support_labels,budget,return_proba=return_proba)
