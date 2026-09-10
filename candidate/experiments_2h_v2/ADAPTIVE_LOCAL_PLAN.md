# Final local-geometry check

Source-context +Gaussian smoothing reaches .729520 at200, .623439 at5. Raw local RF is better at5; whitened local RF is better at25–200. Source and smoothing are now held fixed.

Test ONE predetermined covariance schedule, no sweep: rho=min(1,d/N_support), with d=60 and N_support=4*n. Below one labelled observation per feature, keep only diagonal target covariance (RF-equivalent to per-column scaling); above that ratio, gradually permit full decorrelation. Use raw physical feature units recovered from the supplied Madrid scaler, because the earlier coordinate-basis ablation modestly favored that basis. This is a dimension/sample-size heuristic, not a claimed optimal shrinkage estimator.

Only local geometry changes; same200-tree leaf2 RF, same120-feature one-iteration source prior, same alpha=20/(20+N_support), same Gaussian probability smoothing. Controls: existing raw/pool constant-metric arms. No target labels outside support enter the fit. If useful, freeze and audit; do not continue adjusting the schedule.

A later, separate capacity control may compare RF default leaf1 against the existing conservative leaf2, holding everything else fixed. This has scientific justification as testing whether local underfitting explains the remaining gap, NOT adopting an unavailable competitor winner. No depth/tree-count/feature-fraction sweep.
