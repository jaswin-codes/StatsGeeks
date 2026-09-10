# Autonomous ASTRA-AGF sprint

## Decision
Historical incumbent: ASTRA-AGF (0.735239 on its historical protocol). Development-selected candidate: **Coordinate_RF**. Selection was locked before final query scoring; no query-driven promotion or rejection.

Fresh source prior was trained from supplied Madrid data, not competitor caches. Frozen EXP-010 remains unchanged.

The new mechanism appends two full-pool-standardized lattice-coordinate columns to the 60 adaptively whitened local inputs (62 local RF inputs). The 120-feature contextual source prior, RF200/leaf1/seed42, budget-dependent source blend, and Gaussian graph remain unchanged. No new raw spectral features, target labels, or true-label spatial anchors were added.

## Fresh locked evaluation
Macro F1 mean ± population SD; paired trials; query excludes all 800 fixed development pixels. This changed query population is NOT an exact reproduction of the historical 0.735239 benchmark.

| Shots | Selected mean ± SD | Gain vs EXP010 | Gain vs EXPF | Gain vs ASTRA | Wins vs 010/F/ASTRA |
|---|---|---|---|---|---|
| 5 | 0.650253 ± 0.011246 | +0.078258 | +0.097634 | +0.000289 | 200/200/106 of 200 |
| 25 | 0.687664 ± 0.012145 | +0.077709 | +0.050950 | +0.005045 | 200/200/171 of 200 |
| 50 | 0.708436 ± 0.011277 | +0.090618 | +0.059705 | +0.009213 | 200/200/193 of 200 |
| 100 | 0.729839 ± 0.008802 | +0.108518 | +0.075414 | +0.013803 | 200/200/200 of 200 |
| 200 | 0.749299 ± 0.005716 | +0.126459 | +0.091697 | +0.016262 | 200/200/200 of 200 |

## Spatial robustness
200 shots/class; 10-key-unit buffer; fixed development bank excluded. Four directions are all reported, not selected.

- ASTRA_AGF: x support low → opposite: 0.700548 ± 0.007979
- ASTRA_AGF: x support high → opposite: 0.673486 ± 0.011888
- ASTRA_AGF: x-half mean 0.687017
- ASTRA_AGF: y support low → opposite: 0.658183 ± 0.011881
- ASTRA_AGF: y support high → opposite: 0.754470 ± 0.008240
- ASTRA_AGF: y-half mean 0.706326
- ASTRA_AGF: worst direction 0.658183; four-direction mean 0.696672
- Coordinate_RF: x support low → opposite: 0.719836 ± 0.007908
- Coordinate_RF: x support high → opposite: 0.644816 ± 0.015204
- Coordinate_RF: x-half mean 0.682326
- Coordinate_RF: y support low → opposite: 0.669160 ± 0.009801
- Coordinate_RF: y support high → opposite: 0.743052 ± 0.010872
- Coordinate_RF: y-half mean 0.706106
- Coordinate_RF: worst direction 0.644816; four-direction mean 0.694216
- EXP010: x support low → opposite: 0.635312 ± 0.003101
- EXP010: x support high → opposite: 0.596549 ± 0.006075
- EXP010: x-half mean 0.615930
- EXP010: y support low → opposite: 0.557275 ± 0.003819
- EXP010: y support high → opposite: 0.681828 ± 0.004586
- EXP010: y-half mean 0.619552
- EXP010: worst direction 0.557275; four-direction mean 0.617741
- EXPF: x support low → opposite: 0.647910 ± 0.002712
- EXPF: x support high → opposite: 0.623740 ± 0.011088
- EXPF: x-half mean 0.635825
- EXPF: y support low → opposite: 0.588341 ± 0.006912
- EXPF: y support high → opposite: 0.708744 ± 0.003500
- EXPF: y-half mean 0.648542
- EXPF: worst direction 0.588341; four-direction mean 0.642184

## Information regime and validity
TARGET_FEATURES_USED = TRUE; COORDINATES_USED = TRUE; TARGET_LABELS_USED (outside designated support) = FALSE for fitting/selection/adaptation. Query labels are used ONLY for evaluation. Source uses all labelled Madrid rows. Initial selection uses five folds of a fixed 800-label development-support bank (160 training + 40 validation per class). Top three variants plus ASTRA then undergo 20 repeated support-only holdouts at 5/25/50/100/160 training shots per class, followed by four development-support spatial directions. Repeated holdouts are correlated, not independent validation populations. These development labels are NEVER scored as final query labels. Final support is drawn outside the bank.

The inherited ASTRA recipe was historically query-audit-selected; this cannot be undone. New seeds and support exclusion do not create an independent city or organizer test. Additional 800 development labels constitute research supervision beyond an individual episode budget, explicitly disclosed. Baseline and selected model receive identical current-episode support, full-pool access only for transductive models. EXP010 and EXPF remain inductive controls.

## Reproducibility and integrity
Clean-process artifact replay: {'pass_': True, 'source_refitted_from_scratch': True, 'exact_state_arrays': ['raw', 'standard', 'coords', 'prior', 'cov', 'nn', 'dist', 'classes'], 'exact_prediction_arrays': 4000, 'episodes': 1000, 'trials_per_budget': 200, 'seed_regenerated_exactly': 20260910, 'support_query_disjoint': True, 'development_query_disjoint': True, 'query_labels_used_for_scoring_or_selection': False, 'frozen_files_unchanged': True, 'seconds': 2150.631590604782, 'model_sha256': '26b2299ad50dcf935fb8bc1a89d4e79f82cf2c68881619a6eaf1330f813a7533', 'rebuilt_pool_sha256': 'b975db430b4a00d1c90d59d10a76ef11a6c3727be42e22f41bec49a6f6c28007'}. Feature names/order are stored in pool_state.pkl and provenance.json. Source-prior comparison is in port_check.json. Input hashes and all final session file hashes are retained.

## Rejected and failed experiments
All ablation/optimization results and configurations are retained. Rejection is based ONLY on development-support folds and geographic safeguards, never final query truth.
- Bilateral_graph: support CV 0.762404; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- BoostedTrees: support CV 0.747317; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Confidence_prior: support CV 0.765015; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Covariance_blend: support CV 0.766241; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- ExtraTrees: support CV 0.770155; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Less_diagonal: support CV 0.760011; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- No_source_prior: support CV 0.760888; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- RF_half_features: support CV 0.754911; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Stronger_diagonal: support CV 0.758102; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Two_step_graph: support CV 0.766736; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Wide_graph: support CV 0.763424; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Coordinate_ensemble: support CV 0.765968; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Extra600: support CV 0.765177; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Extra_coordinates: support CV 0.769610; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Extra_leaf2: support CV 0.756281; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Extra_sqrt: support CV 0.760380; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- Forest_ensemble: support CV 0.770286; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.
- RF600: support CV 0.760122; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.

Factorial A=RF; B=pool covariance; C=Gaussian coordinates; D=budget-adaptive covariance. Source prior disabled in factorial arms to avoid hidden coordinate access; original ASTRA evaluated separately. D without B borrows support covariance, so these are operational ablations, not fully independent causal factors.

## Recommended model and exact packaging files
For continued packaging use development-locked **Coordinate_RF**, while retaining ASTRA as historical incumbent; no independent-test superiority is asserted. Required files: agf_model.py, pool_state.pkl, SELECTION_LOCK.json, INFERENCE_MANIFEST.json, reproduce_best.py, requirements-repro.txt. Optional cached replay inputs: verification_inputs/b5.npz, b25.npz, b50.npz, b100.npz, b200.npz (contain support labels and expected predictions, not query truth). Source/provenance files: configuration.json, provenance.json, SHA256SUMS.json. The pool artifact is tied to the supplied ordered Amsterdam population and integer lattice coordinates; rebuild for a new pool. Do not package sealed_evaluation.npz or development labels for inference.

See reproduce_best.py for inference/verification commands. The runner and all raw per-episode predictions remain in the timestamped directory.

## Headline and geographic trade-off

The prelocked coordinate variant scores **0.749299 ± 0.005716** at 200 shots/class, versus paired ASTRA **0.733037 ± 0.006106**, gain **+0.016262**, **200/200 wins**. The full independent source refit and replay matches **4000 prediction arrays across 1000 episodes**, including both inductive controls.

This is a robust support-sampling gain on the stated random-pixel population, NOT independent-city superiority. Five-shot gain is tiny (+0.000289; 106/200 wins), so no meaningful low-budget superiority is claimed. No recipe changes or candidate reselection followed audit scores.

Coordinate-RF spatial x-half = **0.682326**, y-half = **0.706106**, worst direction = **0.644816**, four-direction mean = **0.694216**. Matched ASTRA: x-half **0.687017**, y-half **0.706326**, worst **0.658183**, mean **0.696672**. In particular high-x → low-x loses approximately **0.028670**. Thus the coordinate variant is NOT an automatic universal replacement. ASTRA remains the historical incumbent; the development-locked coordinate variant is packaged for the explicitly stated random-pixel/full-pool use case. Official submission promotion remains unclaimed.

## Figures

- figures\01_budget_performance.png
- figures\02_paired_gains.png
- figures\03_spatial_directions.png
- figures\04_support_ablation.png
- figures\05_confusion_matrices.png
- figures\06_per_class_f1.png
- figures\07_prediction_maps.png

## Compute and failure accounting

Completed: fresh source rebuild; 50-episode baseline; 8 factorial RF arms plus controls; 12 first-pass alternatives; 7 refinements; 400 budget-stability support evaluations; support-only four-direction safeguards; 1000 locked paired final episodes; 40 spatial episodes; fresh source rebuild and exact 1000-episode replay. No model-fit exceptions occurred in this session. The network/pause interval was resumed without restarting completed stages. Source models use 200 trees except explicitly archived 600-tree experiments. The experiment named Confidence_prior is a stronger fixed pseudo-count prior (60), NOT an implemented confidence gate. No true confidence-gated adaptation was tested.

No query truth was used for model fitting, hyperparameter selection, candidate selection, adaptation, or stopping. Query labels were read only for scoring/figures and class-stratified benchmark episode construction. Development-support labels are research supervision, not an organizer-held-out test.
