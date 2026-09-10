# Unpromoted review candidate: EXP-F regularized support covariance

**Status: exploratory review package, NOT selected for deployment.** Descriptive ranking identifies this arm as strongest at25–200 shots. Selecting it as a winner on these scores would be **EXPLORATORY — AUDIT-SET SELECTION**, not independent confirmation. No hybrid with EXP010 at5 shots has been created, tuned or evaluated.

Fixed schedule: k30 at5, k45 at25/50/100/200. Source-standardized features and sqrt Madrid RF importance weights exactly as frozen. Labelled-support class means, no source prototype shrinkage. Let R be within-class support residuals, C=R.T@R/(4*shots-4), k=dimension. Distance precision is inverse(0.5*C + 0.5*trace(C)/k*I + 1e-8*I). Parameters fixed before all sprint results; same at every budget. Query enters only pointwise distance calculation.

Source state remains candidate/artifacts/exp010_stage1_madrid.pkl, read-only; no replacement source artifact required. candidate_predict.py is a separate feature-only-query CLI; query NPZ with any label key is rejected. Input preprocessing contract must match the frozen60-feature schema.

Example (from repository root after tests have generated inputs; use a NEW output path):

```bash
python -I -B candidate/experiments_2h/expF_covariance/candidate_predict.py --artifact candidate/artifacts/exp010_stage1_madrid.pkl --support candidate/experiments_2h/expF_covariance/interface_test/support_25.npz --query candidate/experiments_2h/expF_covariance/interface_test/query_25.npz --shots 25 --output candidate/experiments_2h/expF_covariance/new_predictions_25.npy
```

Clean evaluation repeats match every prediction for all50 random and50 spatial episodes. Five independent CLI processes, each with feature-only full query arrays, match saved episode0 at all budgets exactly; query-label-key rejection also passes. See interface_test/verification.json.

Why not promote now: at5 shots random gain is only+0.000317, and spatial gain is-0.025769 (3/10 wins). The25–200 spatial gains remain positive, but this is a two-region stress on the already reused Amsterdam pool, not new labelled validation. Keep EXP010 while the team reviews the candidate and arranges genuinely independent evidence. No submission, presentation or written justification changed.
