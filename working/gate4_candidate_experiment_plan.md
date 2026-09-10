# Gate 4 — Candidate experiment plan (NOT AUTHORISED TO EXECUTE)

**Audit:** G4-AUDIT-001 · **Date:** 2026-09-08 · **Owner:** Member 3 · **Status:** Proposed; Team Lead review required.

**HYPOTHESIS only:** None of the interventions below has been implemented, fitted, used for prediction, tuned, or scored. No candidate metric exists. The user authorised research/read-only analysis, not Gate 4 execution.

Read alongside [measured error analysis](gate4_baseline_error_analysis.md) and [readiness blockers](gate4_readiness_audit.md).

## 1. Decision summary

**Recommended Experiment 1: Madrid-supervised shrinkage Mahalanobis metric + Amsterdam support prototypes.**

Keep target support/query mechanics fixed. Replace only the distance geometry of the raw-feature prototype baseline with a regularised within-class metric learned entirely from Madrid. Save that source state before exposing target support; keep it immutable across episodes. This is the source-supervised weighting/metric direction already in the master plan, not a new model-family sweep.

**Why highest expected value (INFERENCE):**

1. Target class means already produce .5986 at 25 labels/class, well above the .4433 zero-shot reference, without learned source geometry. Matching or exceeding the prototype reference is the real few-shot bar.
2. Source features are highly correlated (34 pairs with |r|>.9; correlation participation ratio 5.60), so per-column Euclidean distance duplicates directions. Within-class covariance uses source supervision to define noise directions; shrinkage protects against unstable inverse covariance.
3. Target prototypes accommodate target class locations. A common translation of all target supports and queries cancels from their pairwise differences, whereas a frozen RF's thresholds do not adapt. This avoids assuming that a single full-city alignment solves the conditional shifts.
4. No unlabelled-query fitting permission is needed. No new RF training, neural framework, external data, query pseudo-labels, or full all-pixel distance matrix is required for the Amsterdam arm.
5. The failure mode is testable: source within-class geometry may not transfer. An unsupervised source covariance control and identity-metric target-only control distinguish label-derived benefit from generic decorrelation.

This is a ranked hypothesis, not evidence of improvement. Domain-specific covariance may make the metric worse; the fallback is diagonal supervised weighting, not an unconstrained search.

## 2. Frozen comparators and strict information regimes

**FACT:** Frozen all-Amsterdam zero-shot RF macro F1 is **0.4433**, full precision `.443273608786401`. Madrid CV is **.6281 ± .0043**. Frozen same-budget raw prototype summaries are 5: `.5437±.0324`; 10 diagnostic: `.5649±.0312`; 25: `.5986±.0176`; 50: `.6079±.0101`; 100: `.6129±.0097`; 200: `.6150±.0036`.

### Required result fields for every future candidate

- `frozen_zero_shot_all_target = .443273608786401`, identified as **0 labels** and all 25,992 pixels.
- A zero-shot candidate, if one exists, is evaluated on exactly those rows and reports a direct delta to .4433. It must not fit target labels, target distribution summaries, or query alignment state.
- A few-shot candidate has a separate row for **each** support budget and the **same query IDs** as all few-shot comparators. Report `F1(candidate,Q_bt) - F1(raw_prototype,Q_bt)` as the primary paired comparison.
- Also score the **saved RF predictions restricted to Q_bt**, without refitting, for an exact-query reference. Report `F1(candidate,Q_bt) - F1(frozen_RF,Q_bt)` as a label-assisted comparison, not an equal-information zero-shot improvement.
- A simple subtraction of a few-shot mean from .4433 is **descriptive/contextual only**: both label information and evaluated pixels differ. Do not claim the 5-shot +.1004 is a controlled method improvement.
- No hypothetical zero-shot score is supplied for a method that requires support. Mark that arm N/A, not zero or .4433 as if it were the candidate's score.

## 3. Evaluation contract required BEFORE execution

**PROPOSED, no changes made now.** Team Lead must explicitly approve this contract and the target-label development policy before any experiment starts.

### Reference-comparison track

1. Preserve seed **42**, NumPy `default_rng(42)` and its bit generator/environment, exact row order, ascending classes `[1,2,3,4]`, budgets `[5,10,25,50,100,200]`, and ten trials per budget. One RNG advances over the entire budget/trial loop. Do not reseed each budget, skip earlier draws, make the budgets nested, or silently substitute a fresh random sampler.
2. Prototype indices are missing. In a **separately approved comparator/sampler task**, deterministically replay the sampling algorithm (not Notebook 4; no RF fits) using the accepted labels/row order and preserve all support/query indices before evaluation. An isolated unchanged raw-prototype comparator evaluation can check all retained full-precision trial scores. Until that check succeeds, describe the new IDs as reconstructed/proposed, not recovered originals. Disagreement blocks paired claims; stop rather than changing seeds or overwriting the frozen trial scores.
3. Every candidate reuses that frozen episode manifest; adaptation receives only the selected support labels. Query labels reside in the evaluator. Sampling infrastructure may read labels to balance draws, but must not pass the full label array into adaptation.
4. Keep original counts exactly: queries have `25992-4*b` rows. Validate unique support IDs, support/query disjointness and exhaustive union, exact per-class budgets, pixel keys and matrix/schema order. Here every class has enough samples; fail on insufficient budgets rather than relying on `min` to reduce them.
5. Primary reporting: four-class `macro F1(labels=[1,2,3,4],zero_division=0)`, per-trial values and mean/SD `ddof=0`. Per-class precision/recall/F1 and raw/row-normalised confusion are diagnostics. Never choose a candidate using accuracy instead.
6. The frozen benchmark has already exposed Amsterdam evaluation labels through baseline results and this explicitly authorised diagnostic audit. Treat this track as **development/reference-comparison**, never an untouched final audit. Running fresh episodes on the same pixels does not reset label exposure.

The missing episode arrays are **not permission or a reason to rerun Notebook 4**. The isolated comparator task is a proposed prerequisite for future matched experiments; it was not executed here.

### Candidate training and validation boundaries

- Any new learned scaler/metric/representation for Madrid validation is fitted only within the existing 5×5, seed-42 source training folds; retain that split protocol rather than silently switching to spatial blocks or a new seed.
- Start from the 60-column accepted feature contract. Its cached source scaling is global. For candidate fold-local fitting, a separately authorised candidate layer can recover numerical raw units via `U = Z*saved_scale + saved_mean`, then fit its own training-fold scaler and constant-feature mask. Float64 inverse arithmetic is approximate; record and test reconstruction tolerance. Do not present inverse arithmetic as proof of a label-free raw feature extractor.
- Refit source state on all Madrid only after source-side design choices are locked. A frozen full-Madrid RF/leaf embedding is valid source state for Amsterdam testing, but cannot be reused to claim honest Madrid OOF representation performance.
- For fixed designs below, no target hyperparameter search is proposed. If source validation fails or instability requires parameter changes, stop for a newly logged specification; do not choose a value by Amsterdam query F1.
- A development/audit separation decision is missing. The lead must define permissible use of the already-observed target data and an independent final evaluation route (e.g. organiser-held-out labels). A retrospectively reserved subset of already-audited data is not magically untouched. Any new partition/protocol requires a separate decision; this task creates none.
- Label-free raw preprocessing and inference checks remain separate submission-safety work. Cached-vector development is not submission-ready raw inference. Approve a narrowly scoped safety implementation first or explicitly record a restricted cached-feature development exception; never silently mark Gate O passed.

### Uncertainty and proposed go/no-go rule

**HYPOTHESIS evaluation rule to preregister, not a prediction:** primary budget 25/class. Call a candidate promising only if its matched mean delta versus raw prototypes is at least **+.0100**, at least **8/10** matched trial deltas are positive, and mean per-class F1 has no drop larger than **.0200**. Inspect C3 recall/precision explicitly; do not reward recall gained by an indiscriminate C3 collapse. Also require a positive mean delta versus the frozen RF on the identical query rows. Report all budgets, including failures at 5 shots; preserve 10-shot diagnostic labelling.

For E1, positive performance versus the **source-unsupervised covariance control** is needed to support the narrower claim that source labels improve the metric. Without that, report generic decorrelation benefit, not demonstrated supervision benefit.

Thresholds are proposed practical decision thresholds, not significance levels or expected scores. A paired uncertainty interval crossing zero is inconclusive, not an improvement claim. If authorised later, estimate uncertainty over paired support draws with a declared fixed-seed procedure (keep seed 42); describe it as conditional on this city/dataset. Ten overlapping-query episodes cannot establish independent city/generalisation confidence. Pixel-level IID bootstraps and treating repeated CV appearances as independent would be misleading; a separately approved spatial-cluster sensitivity analysis needs its own protocol, not a silent replacement of the frozen benchmark.

## 4. Ranked hypotheses and intervention matrix

**All parameters below are proposed fixed values; search space is a singleton for the first comparison.** None was optimised or tested. IDs `G4-P01`–`G4-P05` are planning IDs, not shared EXP IDs; lead allocates unique `EXP-...` IDs on approval.

Let `Z` denote Madrid-standardised features under the source training contract, `m_c` the source mean for class c, and `S_c` the selected target supports for that class. Mask source-training zero-variance columns in candidate state only (59 active in full Madrid here); do not edit the accepted 60-feature pickle. Resolve distance ties by ascending class ID. No test-time label fields enter prediction.

| Rank / plan | Hypothesis and exact intervention | Fixed parameters / search | Required state and cost | Main risk |
|---|---|---|---|---|
| **1 / G4-P01** | Source within-class shrinkage Mahalanobis distance improves target prototypes by discounting redundant/noisy source directions. See formula below. | Covariance shrinkage .10; no target search | Madrid X/y for metric; target support X/y and query X; 59×59 state; source cost O(n d²), query O(n d² + 4nd), cheap relative to RF | Source noise geometry may not transfer; rare indicators/low eigenvalues |
| **2 / G4-P02** | Bounded diagonal Fisher weighting gives useful supervised feature importance without fragile cross-feature covariance. | .50 identity mixture; ratio epsilon 1e-6; weight clipping [.25,4] before mixture; no search | Madrid class means/variances; O(nd), 59 weights; target supports/queries | Source-discriminative bands may also be city-specific; redundancy remains |
| **3 / G4-P03** | Support-only class-balanced translation restores compatibility with frozen RF thresholds. Apply an estimated common shift to target queries, not to the forest. | Translation strength 1.0; continuous columns only; no search | Frozen RF plus Madrid class centres and target supports; O(nd) summary and one frozen RF inference pass per episode | Single translation cannot fix class-dependent/covariance shifts; 5-shot noise; C1/C2 semantic mismatch |
| **4 / G4-P04** | A compact source-supervised discriminant embedding isolates era separation useful for target prototypes. | Shrinkage .10; rank ≤3; no residual mixture or dimension search | Madrid X/y, class scatter/eigendecomposition; O(nd²); optional distinct 0-shot arm | Discards target-informative directions; source-only boundaries may not transfer |
| **5 / G4-P05** | Frozen RF leaf-cooccurrence geometry transfers source-supervised nonlinear similarity better than raw L2. Class-centroid distance in sparse leaf one-hot space. | All 500 existing trees, equal weight; no tuning | Frozen RF `apply` only in future; leaf caches and sparse per-class counts; avoid all-pixel pairs | RF already transfers poorly, leaves sparse; largest artifact/memory and implementation burden |

### Exact formula: Experiment 1 — supervised shrinkage metric

For d active dimensions, calculate population within-class covariance in each source class and average classes equally:

`W = (1/4) * sum_c [(1/n_c) * sum_{i:y_i=c} (z_i-m_c)(z_i-m_c)^T]`.

`W_reg = .90*W + .10*(trace(W)/d)*I`.

Require finite `trace(W)>0` and positive eigenvalues; on failure stop, do not silently change shrinkage. Save `R = W_reg^(-1/2)` in source state. For target support class mean `s_c`, choose

`argmin_c ||(z_query - s_c) R||²`.

**Single intervention:** replace identity distance with R. Class means, supports, queries, labels, budgets, seed, prediction tie-break, and metric definition remain unchanged. Fit R on Madrid only; no Amsterdam mean/covariance is used except the selected support means.

**Controls (all proposed):**
- P0: unchanged raw Euclidean target prototypes (`R=I`).
- U0: regularised **total** source covariance at the same .10 shrinkage, without source class labels, followed by target prototypes. This separates supervised within-class geometry from generic source decorrelation.
- Frozen RF restricted to the identical query IDs; full zero-shot .4433 remains a separate reference row.

**Success:** shared 25-shot rule above, plus improvement over U0 before claiming source-label benefit. **Falsification for this specification:** no positive matched mean improvement over P0, systematic C3 loss, or numerical instability. Near-zero gains/uncertainty overlapping zero are inconclusive; do not tune on query scores to rescue the result. Failure falsifies this fixed design on this benchmark, not all metric learning.

### Exact formula: Experiment 2 — diagonal Fisher weighting

Source class-balanced grand mean `m=(1/4)sum m_c`.

`B_j=(1/4)sum_c(m_cj-m_j)^2`; `V_j=(1/4)sum_c var(Z_j|c,ddof=0)`.

`q_j=B_j/(V_j+1e-6)`; require mean(q)>0.

`v=clip(q/mean(q), .25, 4)`; `w=.50 + .50*v/mean(v)`.

Target class decision minimises `sum_j w_j*(z_qj-s_cj)^2`. Source weights are saved/frozen. This is a **separate** alternative to E1, not a stack of both interventions. P0 and frozen RF are the controls; an all-ones weight is the unlearned representation control.

**Success:** shared 25-shot rule; exact source-state reload and all-ones ablation. **Falsification:** no positive matched P0 gain or excessive per-class regression. **Why backup 2:** smallest implementation/numerical risk, fits the existing source-supervised reweighting plan, but cannot correct correlations.

### Exact formula: Experiment 3 — support-only RF translation

On 58 continuous band/index/temporal features only (exclude the two availability indicators), compute

`delta=(1/4)sum_c(s_c-m_c)`;

`z'_q = z_q - delta` on those columns, leaving both indicators untouched. Feed `z'_q` to the immutable existing RF. No prediction calibration, RF parameter changes, covariance matching, or full-target prior estimation. Source means use full Madrid corresponding to the final RF; target means use only selected supports.

**Controls:** frozen RF on identical query rows; P0 same-budget prototypes to see whether this actually competes with the already-strong simple adaptation. **Success:** mean same-query RF gain ≥+.0100 and shared per-class safeguards; it must also meet the shared P0 rule before being preferred to E1/P0 as the final method. **Falsification:** nonpositive matched RF gain or class-dependent harm; RF gain without P0 gain is an adaptation lesson, not a winning candidate. **Why backup 3:** directly tests the large location-shift signature while genuinely consuming saved source RF state, with no unlabelled-query fitting privilege.

### Exact formula: Experiment 4 — shrinkage LDA geometry

Use the same source class-balanced W and .10 regularisation as E1. Define `B=(1/4)sum_c(m_c-m)(m_c-m)^T`. Eigendecompose `R B R`; retain up to three eigenvectors with eigenvalues > `1e-10*largest_eigenvalue`. Save `A=R U` and use squared L2 distances in `(z-m)A`.

Separate declared arms:
- **0-shot:** nearest transformed source class mean with equal class priors. Compare on all 25,992 target rows directly against .4433. Success: ≥+.0100 full-target macro-F1 delta with per-class F1 regression no worse than .0200. Deterministic result has no trial SD; inference uncertainty requires a separately approved procedure.
- **Few-shot:** nearest transformed target support class mean, same exact episodes. Shared P0/RF rule applies.

**Falsification:** lost discrimination, nonpositive gain on its corresponding comparator, or unstable eigensystem. Equal priors and the source-classifier change are explicit parts of the 0-shot arm, not evidence that geometry alone explains its difference from RF. No dimension sweep or target-based selection.

### Exact formula: Experiment 5 — frozen RF leaf-space centroids

Each x maps to a one-hot leaf per tree, concatenated and scaled by `1/sqrt(500)`. A class centroid is the average of these sparse vectors over its support. Compute squared distance to centroids as `1 - 2*dot(phi(x),centroid_c) + ||centroid_c||²`, using per-tree/per-class leaf frequencies. The centroid-norm term matters; merely maximising mean co-leaf frequency is not identical when class centroids have different norms.

No full pairwise Madrid or Amsterdam matrix. Cache leaf IDs in bounded chunks only after approval; 25,992×500 int32 leaf IDs are about 52 MB, excluding overhead/RF memory. Sparse lookup scoring is roughly O(500*n_query*4) per episode; avoid O(n_query*n_support*500) dense comparisons. Validate exact source RF hash before/after; no new forests, tuning, or refits. Raw P0/frozen RF are comparators; identity/raw representation is the unlearned control. **Success/falsification:** shared few-shot rule; stop if near-zero support/query leaf overlap makes the representation unusable. Higher implementation cost and the source RF's target error structure make this lower priority.

### Matrix fields common to all rows (explicitly fixed)

| Required field | Contract |
|---|---|
| Motivation | Measured class-3 collapse, conditional feature shifts, redundancy, and target prototype learning curve; no claimed causal source |
| Unchanged | Accepted raw data/features/label boundaries, source/target direction, saved RF bytes and parameters, reference notebook protocol, seed 42, four-class macro F1, same ordered feature names, reference budgets/trial counts, exact episode masks once approved |
| Inputs | Versioned accepted pickle/schema; specified saved RF where relevant; source training labels only for source fitting; selected support labels only for adaptation; query labels evaluator-only |
| Hyperparameter search | None in first tests (singleton configurations above). Any later search is a new preregistered source-side or legally support-internal task, not unrestricted target tuning |
| Protocol | Source 5×5 seed-42 fold-local checks for new source representations; full-source frozen state for Amsterdam; exact reference-comparison episodes; per-budget separation |
| Metric/comparator | Macro F1 classes 1–4; frozen 0-shot .4433 contextual reference for all; exact same-query RF and same-budget P0 for few-shot; U0 additional supervision ablation in E1 |
| Cost reporting | Measured wall time, peak memory, state size; estimates above are complexity estimates, not benchmark runtimes. One coordinated CPU job; no GPU required |
| Save | Source state, mask/scaler/schema/class order, episode adaptation state, predictions/probabilities if defined, supports/queries, per-trial/class scores, config, hashes |
| Failure | Stop/log numerical errors, schema mismatch, mismatched episode controls, policy-blocked imports, leakage, or resource overrun; no adaptive repair/tuning based on query F1 |

## 5. Alternatives considered but not recommended now

- **Full-target mean/variance alignment or CORAL:** large observed shifts motivate considering them, but fitting query distributions is transductive. Current instructions do not confirm that privilege. Different priors/conditional means make unconditional alignment potentially destructive. Defer pending explicit data-use permission; do not secretly use the descriptive target statistics computed in this audit.
- **Pure prior correction:** class 2's actual target prior is smaller, yet it is overpredicted; the conditional mean-change component dominates the measured marginal shift. Prior-only methods require assumptions not supported here. True full-target priors cannot be used as adaptation input.
- **Scalar temperature calibration:** preserves argmax, so cannot alone lift unchanged-rule macro F1. Support-fitted class offsets could be a later distinct supervised adaptation, but 20 total labels at 5/class risk overfitting and are not the first test.
- **Pseudo-label self-training/domain-adversarial adaptation:** permissions unresolved; class-2 overprediction and sparse reliable high confidence make confirmation bias plausible. No authorisation, no implementation.
- **RF tuning, broad alternative-model sweeps, neural triplet learning:** lower value per review/compute minute than a compact source metric; source CV gains alone do not establish Amsterdam benefit. No such tuning is proposed.
- **Fixed feature-group ablations / robust QA/season features:** scientifically interesting later (indices shift less; indicators can dominate rare distances), but would add a second intervention and need separately versioned preprocessing. Do not drop features based on target-label diagnostics or alter the accepted cache in this phase.
- **Ensembling candidate outputs:** defer until standalone candidates pass matched comparisons; weights must not be selected using query labels. No ad hoc blend of .4433 RF and prototypes is authorised.

## 6. Reproducibility contract for each future experiment

**Design only:** suggested `working/candidate_artifacts/EXP-.../` is not created or approved by this audit. Lead confirms paths and IDs; never write under either frozen baseline directory. An immutable run directory with exclusive creation should reject an existing run ID rather than silently overwrite.

Required run record fields:

```text
experiment_id, parent_plan_id, status (proposed/running/pass/fail/inconclusive), hypothesis
lead_approval_id, owner, reviewer, timestamp_utc, local_timezone
branch, git_head, git_dirty_status, dirty_diff_hash, code_file_hashes
baseline_recovery_manifest_sha256, baseline_rf_sha256, baseline_prediction_sha256
input_pickle_sha256, raw_data_sha256, ordered_feature_schema_sha256
source_city, target_city, class_order, exact_label_intervals, annual_horizon
python_executable, python_version, numpy/scipy/sklearn versions, OS/CPU/thread settings
configuration (all defaults explicit), random_seed=42, RNG algorithm/state
source_fold_manifest_hash, training_ids_hash, fit_scope_per_transform
support_query_manifest_hash, budget, trial, support_ids, query_ids
permitted_label_access, development_or_audit_scope, final_audit_policy
start_time, end_time, wall_seconds, peak_RAM, artifact_bytes
source_state_hash, adaptation_state_hash, prediction/probability_hashes
metric_name=macro_F1, labels=[1,2,3,4], zero_division=0, std_ddof=0
per_trial_F1, per_class_metrics, raw_confusion, mean/std
frozen_zero_shot_all_target=0.443273608786401
matched_RF_F1, matched_P0_F1, paired_delta_RF, paired_delta_P0
zero_shot_delta_if_same_all_target_conditions, contextual_delta_if_unmatched
uncertainty_method/unit/seed/limits, exact_completed_trial_count
failure_reason, warning_log, keep/reject/defer_reason, limitations
output_manifest (every payload size and SHA256), independent_reload_result
```

Checks required before result sign-off:

1. No forbidden label fields in prediction inputs; adaptation function cannot access query labels or full target statistics.
2. One geographic pixel per row; same IDs/order across methods and features; no support/query intersection, duplicate supports, missing classes, or silent budget reductions.
3. Source transforms fit within folds; full-source state frozen before target use; shared source file hash unchanged across episodes.
4. Save every trial, not only best draws or aggregate means. Recompute F1 independently from stored prediction/true-label evaluator arrays with class order fixed.
5. Preserve state and run logs on failure. Do not overwrite a failed run as a success. Re-run requires new explicit run identity/approval.
6. Another member reloads source/adaptation state and reproduces predictions without label fields. Environment/pickle portability and label-free raw feature generation are separate checks.
7. Record scientific vs engineering controls separately. A snapshot/hash pass does not prove the model's scientific validity; target labels already viewed cannot become unseen by renaming an artifact.

## 7. Stop / handoff

**Recommended order:** Lead resolves evaluation/label-use and safety scope → approves comparator/episode manifest task and evidence records → approves a single E1 fixed design → only then authorises execution. E2/E3 are backups, not permission to run three experiments unattended. E4/E5 remain deferred proposals.

No candidate run, source metric fit, new RF fit, support draw, protocol revision, or reference rerun occurred during this audit. **STOP here for Team Lead review.**
