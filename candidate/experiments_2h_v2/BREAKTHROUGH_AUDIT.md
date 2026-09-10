# >.70 pause and audit

Stage1 pool_RF60_smooth reached .722616 at200 and .707289 at100. No immediate stacking: ran clean repeat, fresh seed8675309, spatial half split and source refit.

- Original unchanged60 features and exact EXP-010 episodes: baseline matched six decimals (full-precision comparison packaged later).
- Target information: full target covariance and coordinates; transductive, disclosed. No query labels in candidate fitting. Smoothing includes support-trained in-sample predictions, so adjacency may help.
- Exact source refit: same argmax, maximum probability difference3.33e-16 with parallel reduction. Source receives Madrid labels only.
- Clean-process repeat: **150 arrays across both smoothed RF arms and H_mean identical**, including the >.70 candidate. Full omnibus assertion failed on12 other arrays, each with one changed prediction. All historical results retained. `tie_audit.json` found top-two probabilities differing by5.55e-17 at an affected forest vote. Stage2 uses stable serial tree-order probability aggregation with parallel training to eliminate this avoidable reproducibility issue. Do not label the entire stage1 omnibus exact.
- Fresh-seed pool_RF60_smooth200=.7208,100=.7031: >.70 survives new episodes on SAME population.
- Spatial-half200=.6715 (vs EXP-010 .6178; EXP-F .6370); marked drop from random .7226. Spatially robust improvement, not spatial invariance. At5 this method falls to .4854: unacceptable as a universal candidate.
- Source/local alpha=.5 markedly helps low-shot, including spatial5=.5876. This justifies a low-shot source prior, not a per-budget exhaustive search.
- Reused target audit is model-selection exploration, not untouched validation. No claimed organizer test score.

Gate decision: proceed with the small STAGE2_PLAN ablations, retaining all failures and explicit transductive label.
