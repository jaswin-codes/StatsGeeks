# Gate 4 — Frozen baseline error and domain-shift analysis

**Audit ID:** G4-AUDIT-001 · **Date:** 2026-09-08 · **Owner:** Member 3 (agent; lead review pending)

**Scope:** Read-only diagnostics of existing reference artifacts. No training, candidate predictions, model selection, support sampling, baseline rerun, or production transformation. This is not a candidate experiment or final-audit evaluation.

Labels throughout: **FACT** = measured from existing artifacts or inspected code; **INFERENCE** = interpretation supported but not proved by those measurements; **HYPOTHESIS** = unexecuted proposal; **UNKNOWN** = unavailable evidence.

Related: [experiment plan](gate4_candidate_experiment_plan.md), [readiness audit](gate4_readiness_audit.md).

## 1. Evidence, provenance, and validation

**FACT:** User's current handoff accepts the measured reference and recovered payloads. Older master-plan and presentation placeholders lag that state; they are not the source of current scores.

- Git: `main`, HEAD `165fe11df8779eed514c75bd2852c2b9588a18a4`. Working tree dirty before this audit; HEAD alone does not identify the uncommitted baseline implementation.
- Diagnostics interpreter: existing Python 3.11.9, NumPy 2.4.6; RF unpickled with the existing scikit-learn environment. Recovery metadata records SciPy 1.17.1 / sklearn 1.9.0. No packages installed or policy changes.
- Protected inputs were SHA256-snapshotted before analysis (32 files: originals, raw Parquets, pickle, reference notebooks/helpers, both frozen-artifact directories including their OneNote indices).
- All six payload hashes in `working/baseline_artifacts/recovery_manifest.json` matched; input pickle hash matched its accepted value.
- NPZs loaded with `allow_pickle=False`; trusted local preprocessing/RF pickles were read only. RF was inspected for attributes, **not** asked to fit, predict, or apply leaves.
- Saved labels and pixel IDs exactly match the preprocessing pickle. IDs are unique within each city. Every Madrid row occurs five times in OOF arrays; `oof_true == y_madrid[oof_indices]`.
- All 25 fold F1s independently recomputed from saved predictions match saved `fold_f1` within absolute tolerance `1e-14`. Fold segments use 15,253/15,253/15,253/15,252/15,252 rows per repeat, in recorded order. No CV split generated or changed.
- Probability arrays are finite, sum to one, and their argmax agrees with saved hard predictions.

### Artifact anchors (SHA256)

| File | Hash |
|---|---|
| `data/preprocessed/preprocessed_data.pkl` | `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe` |
| `working/baseline_artifacts/rf_final.pkl` | `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870` |
| `working/baseline_artifacts/madrid_cv_oof.npz` | `a52a7d721e505f3983fc470e1ef1785fac8ce7e6e4d59e0e09e663c425e2cbc5` |
| `working/baseline_artifacts/amsterdam_zero_shot.npz` | `e1d13830cc0d8d0f820aa0cc93a923b32117101b6ae1cea2c19c28ecb532523c` |
| `working/baseline_artifacts/prototype_trial_scores.npz` | `637631d7df4cf0d9f315424e9a3411744b26aeeea91b5c152da41ab7788c29ab` |
| `working/baseline_artifacts/feature_schema.json` | `bea946aaf7d96e12370af5800f4e719bafe0f7b30fee4354278f7ef36e1f107a` |
| `working/baseline_artifacts/recovery_validation.json` | `f58c4ad5c99a0031eb5c2673905c53802484247a70874170e10f796fa15706f9` |
| `working/baseline_artifacts/recovery_manifest.json` | `01a6eb4b2e18f1eb99e06ddb84b6d2927d4992c0e999f7d9366f5af6ca26ff73` |
| `original/4-Modelling.ipynb` and unexecuted reference copy | `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae` |

The temporary audit script/results are outside the repository in the OS temp directory `statsgeeks_gate4_audit/`; they are not candidate code or a durable artifact contract. Tables, definitions, and reproduction recipe below retain the substantive evidence.

## 2. Frozen scores — FACT

| Evaluation | Macro F1 | SD (`ddof=0`) | Unit |
|---|---:|---:|---|
| Madrid CV | 0.6281315050690548 | 0.004265247306708275 | 25 fold scores, 5 folds × 5 repeats |
| Amsterdam RF zero-shot | **0.443273608786401** | Not a repeated-run SD | All 25,992 target pixels |
| Amsterdam 5/class prototype | 0.5436864655 | 0.0324010057 | 10 support draws; query excludes 20 supports |
| 10/class (diagnostic) | 0.5648726211 | 0.0311867256 | Query excludes 40 supports |
| 25/class | 0.5985975030 | 0.0176369237 | Query excludes 100 supports |
| 50/class | 0.6078789325 | 0.0101154195 | Query excludes 200 supports |
| 100/class | 0.6128982734 | 0.0097440393 | Query excludes 400 supports |
| 200/class | 0.6149548502 | 0.0035964674 | Query excludes 800 supports |

**Comparability warning:** `0.4433` is the mandatory frozen zero-shot reference. Differences between that full-target score and few-shot query-only scores are descriptive comparisons across label budgets, not equal-information or exactly matched-query gains. Future few-shot methods must beat the same-budget raw prototype on matched episodes, as well as report the frozen zero-shot reference. No old starter Madrid/zero-shot value is used as the current baseline here.

## 3. Per-class error analysis — FACT

Class ordering throughout is 1,2,3,4. Madrid C1 ends at 1960; Amsterdam C1 ends at 1945; other boundaries are 1984/2004, all right-inclusive. The C1/C2 semantic difference complicates cross-city comparisons.

### Counts and predictions

| Class | Madrid pixels | Madrid prior % | Madrid OOF predicted % | Amsterdam pixels | Amsterdam prior % | Amsterdam RF predicted % |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 13,794 | 18.09 | 16.17 | 7,568 | 29.12 | 26.53 |
| 2 | 27,152 | 35.60 | 39.32 | 8,802 | 33.86 | 56.90 |
| 3 | 18,672 | 24.48 | 23.30 | 6,745 | 25.95 | 6.27 |
| 4 | 16,645 | 21.83 | 21.21 | 2,877 | 11.07 | 10.31 |

Amsterdam hard-prediction counts are `[6895,14789,1629,2679]`. Class 3 is severely underpredicted; class 2 overprediction is not explained by class 2 being more frequent in Amsterdam (its true proportion is slightly smaller there).

| Class | Madrid OOF precision | recall | F1 | Amsterdam precision | recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| 1 | .5938 | .5307 | .5605 | .4635 | .4223 | .4420 |
| 2 | .6174 | .6819 | .6480 | .3862 | .6489 | .4843 |
| 3 | .6184 | .5885 | .6031 | .7741 | .1870 | .3012 |
| 4 | .7110 | .6911 | .7009 | .5659 | .5269 | .5457 |

Madrid metrics pool 381,315 OOF appearances, **not independent pixels**. Pooled macro F1 `.6281324561` is not the definition of the headline mean of fold F1s `.6281315051`; their near equality here is incidental.

### Raw confusion matrices

Rows true, columns predicted:

```text
Madrid OOF (five appearances per pixel)
             C1     C2     C3     C4
C1        36605  24924   4296   3145
C2        19168  92573  15508   8511
C3         4068  22632  54941  11719
C4         1803   9810  14098  57514

Amsterdam zero-shot (one appearance per pixel)
             C1     C2     C3     C4
C1         3196   4207     47    118
C2         2527   5712    172    391
C3          921   3909   1261    654
C4          251    961    149   1516
```

### Row-normalised confusion (%; diagonals are recall, not F1)

| City/true class | Pred 1 | Pred 2 | Pred 3 | Pred 4 |
|---|---:|---:|---:|---:|
| Madrid 1 | 53.07 | 36.14 | 6.23 | 4.56 |
| Madrid 2 | 14.12 | 68.19 | 11.42 | 6.27 |
| Madrid 3 | 4.36 | 24.24 | 58.85 | 12.55 |
| Madrid 4 | 2.17 | 11.79 | 16.94 | 69.11 |
| Amsterdam 1 | 42.23 | 55.59 | 0.62 | 1.56 |
| Amsterdam 2 | 28.71 | 64.89 | 1.95 | 4.44 |
| Amsterdam 3 | 13.65 | 57.95 | 18.70 | 9.70 |
| Amsterdam 4 | 8.72 | 33.40 | 5.18 | 52.69 |

**INFERENCE:** The priority is recovering C3 without indiscriminately relabelling C2: C3 precision is already .7741. C1↔C2 accounts for 47.07% of Amsterdam errors; C2↔C3 adds 28.52%. In Madrid these pairs account for 31.57% and 27.30%. C1 is Madrid's hardest F1 class; C3 becomes Amsterdam's hardest. Neither a global accuracy-only objective nor only fixing C1/C2 addresses the full target failure.

### Repeat stability, not independent uncertainty

**FACT:** Of 76,263 Madrid pixels, correct-prediction counts over five held-out appearances are:

| Correct appearances | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Pixels | 23,105 | 2,620 | 2,034 | 2,268 | 3,039 | 43,197 |

30.30% are wrong in all five appearances; 56.64% correct in all five. Always-wrong fractions by true class: C1 40.77%, C2 24.04%, C3 34.54%, C4 27.07%.

**INFERENCE:** Many errors persist under resplitting, suggesting systematic feature/class difficulty rather than one unlucky fold. This does not establish the cause or a benefit from adding repeats. Never use the 381,315 appearances as independent observations in confidence intervals.

## 4. Prototype learning curve — FACT and limits

| Labels/class | Mean | SD | Min trial | Max trial | Gain over preceding listed budget |
|---|---:|---:|---:|---:|---:|
| 5 | .5437 | .0324 | .4904 | .6004 | — |
| 10 | .5649 | .0312 | .5217 | .6146 | +.0212 |
| 25 | .5986 | .0176 | .5672 | .6295 | +.0337 |
| 50 | .6079 | .0101 | .5956 | .6267 | +.0093 |
| 100 | .6129 | .0097 | .5933 | .6256 | +.0050 |
| 200 | .6150 | .0036 | .6093 | .6242 | +.0021 |

**FACT:** The descriptive 5-shot minus full zero-shot difference is `.1004128567`; 25-shot minus 5-shot is `.0549110376`. Only `.0163573472` additional mean F1 appears between 25 and 200 shots, with lower draw variation. Budgets are not nested or matched; no paired significance across budget positions is justified. All ten recorded 5-shot scores exceed the full-target zero-shot number, but that is still not an equal-information comparison.

**INFERENCE:** A small target-labelled centroid adjustment helps a great deal in the existing feature space. At 25 shots, reducing metric bias/redundancy may have greater value than simply seeking more labels. There is no proof that the plateau is an irreducible Bayes limit.

**UNKNOWN:** Per-class prototype gains, per-episode confusion, support representativeness, and paired RF-vs-prototype deltas cannot be computed from the retained scores alone. The separate 25/100-shot notebook illustrations use a different RNG stream from the ten-trial benchmark. Do not substitute those pictures for per-trial arrays.

**HYPOTHESIS, not causal finding:** The 5-shot jump could reflect class-conditional centre shift, differing decision boundaries, representation/metric effects, or the equal-centroid decision rule. It does not isolate calibration: both algorithm and access to target labels changed. It also does not prove source-supervised transfer; raw prototypes use only target support means plus source scaling.

## 5. Saved-probability diagnostics — FACT

| Statistic | Madrid OOF appearances | Amsterdam zero-shot |
|---|---:|---:|
| Accuracy (secondary diagnostic) | .6337 | .4496 |
| Mean maximum predicted probability | .5505 | .4276 |
| Mean entropy, bits (max 2) | 1.4747 | 1.7671 |
| Mean negative log2 true-class probability | 1.2956 | 1.6448 |
| Multiclass Brier, sum over 4 classes | .4948 | .6381 |
| Top-label ECE, 10 equal-width bins | .0832 | .0398 |
| Fraction max probability ≥ .8 | 11.9728% | .1308% |
| Accuracy within that ≥ .8 subset | .9519 | .5000 (34 pixels only) |
| True class in top two probabilities | .8632 | .8268 |

ECE uses `b=min(floor(10*max_probability),9)` so every row falls in exactly one bin; sums validated at 381,315 / 25,992. NLL uses a `1e-15` lower bound only for safe logarithms. These diagnostic definitions do not replace the frozen evaluation metric.

**FACT:** Amsterdam top-two coverage by class is C1 .9577, C2 .9671, C3 .5610, C4 .6764. For 43.90% of actual C3 pixels, C3 is absent even from the top two probabilities; a simple top-two switch would therefore leave a substantial part of the problem unresolved. Confidence is generally lower in Amsterdam. A smaller ECE does not imply a better classifier or prove calibrated class probabilities: top-label calibration can look better simply because both confidence and accuracy are low. Reliability bins have very few high-confidence target observations.

**INFERENCE:** Blind high-confidence pseudo-labelling risks reinforcing errors. Scalar temperature scaling with positive temperature preserves argmax, so by itself it cannot improve macro F1 at the unchanged hard-label decision rule. Class-specific threshold/bias fitting would be a distinct few-shot experiment with support-only labels, not a calibration free lunch.

## 6. Domain-shift analysis — FACT

All distribution summaries use the existing 60-feature pickle, **not new raw preprocessing**. Madrid was globally standardised in the reference. For nonconstant columns, mean differences below are in source-standard-deviation units; target/source SD ratios are separate. `has_early_data` is constant zero in scaled space and excluded from correlations/SD ratios. KS is the empirical maximum CDF gap, an effect size only; no IID p-values under spatial dependence are claimed.

**FACT:** 45 of 59 nonconstant features shift by more than .5 source SD; 24 shift by more than 1 source SD.

### Largest marginal mean shifts

| Feature | Target minus source mean | Target/source SD | KS CDF gap |
|---|---:|---:|---:|
| Red_early_mean | -2.1811 | .6896 | .8221 |
| Red_mean | -1.9986 | .7408 | .8061 |
| SWIR2_early_mean | -1.9732 | .6476 | .7710 |
| SWIR1_early_mean | -1.8426 | .7195 | .7161 |
| Green_early_mean | -1.8204 | .7138 | .7433 |
| SWIR1_mean | -1.7101 | .7233 | .7035 |
| SWIR2_mean | -1.7071 | .6252 | .7349 |
| Blue_early_mean | -1.6123 | .7554 | .6939 |
| Green_mean | -1.5765 | .7642 | .7327 |
| Red_late_mean | -1.5513 | .7807 | .7340 |
| NIR_mean | -1.4711 | 1.0101 | .5452 |
| NIR_early_mean | -1.4684 | 1.0590 | .5220 |

### Group-level diagnostics

RMS shift is `sqrt(mean_j((mean_A_j-mean_M_j)^2))`; comparable per feature, not a sum favouring large groups. Equal-class RMS replaces city priors with 1/4 per class before computing shifts.

| Feature group | n | Mean absolute shift | RMS shift | Median SD ratio | Mean KS | Equal-class RMS shift |
|---|---:|---:|---:|---:|---:|---:|
| Overall | 12 | 1.1713 | 1.2859 | .8810 | .5546 | 1.2103 |
| Indices | 10 | .5756 | .6682 | .9798 | .2675 | .7233 |
| Early | 12 | 1.2314 | 1.3933 | .8220 | .5506 | 1.3448 |
| Late | 12 | .9084 | .9802 | .8989 | .5250 | .8965 |
| YOY | 12 | .7577 | .8347 | .7540 | .4439 | .7707 |
| Indicators | 2 | .0202 | .0286 | .3553 (one nonconstant) | .0009 | .0307 |

**FACT:** Shift persists within named classes. Early-group class-conditional RMS shifts for C1–C4 are `[1.4289,1.3568,1.1228,1.5255]`; index-group values are `[.8401,.7444,.7123,.8667]`. Less marginal shift in indices does not establish that indices alone classify best or that their conditional structure is stable.

For source class means `mu_Mc`, target class means `mu_Ac`, and priors `p_Mc,p_Ac`, decompose exactly:

`mu_A-mu_M = sum_c (p_Ac-p_Mc)*mu_Mc + sum_c p_Ac*(mu_Ac-mu_Mc)`.

L2 norms across nonconstant source-standardised features:
- Total marginal shift: **8.2156**.
- Source-conditional prior-change component: **.6791**.
- Conditional-mean-change component: **7.7772**.

**INFERENCE:** Pure class-prior shift is an inadequate explanation of observed feature means under this decomposition. Norms are not additive percentages or causal attributions. C1/C2 boundaries differ; domain sampling, feature selection, real land cover, sensor, season, and urban history could contribute. `P(X|Y)` differences do not prove invariant `P(Y|X)` (pure covariate shift), nor establish concept shift separately. Do not infer a safe global alignment from these diagnostics.

**Label-access boundary:** This class-conditional analysis was explicitly authorised as retrospective baseline EDA. No target class centroids/covariances were saved as fitted state or used to create candidate predictions. Future candidates must not use these full-target statistics as transformation parameters, feature weights, class priors, or hyperparameter-selection targets.

### Range and overlap

**FACT:** Only 1.71% of Amsterdam `Red_early_mean` values lie beyond the Madrid observed min/max, yet 51.99% lie outside Madrid's central 1–99% interval. For `Green_early_mean`, these are 2.54% and 51.69%; for `NIR_early_mean`, .41% and 34.82%. Absolute range overlap hides substantial density shift. These are univariate comparisons, not multivariate support-overlap estimates.

**INFERENCE:** A forest can encounter unfamiliar combinations and density regions without features being outside every source range. Min/max checks alone will miss the domain gap. Raw standardisation is source-fitted; it does not centre Amsterdam at zero and cannot eliminate source/target distribution differences.

### Redundancy and distance geometry

**FACT:** Among 59 nonconstant features, 34/1,711 pairs have absolute correlation > .9 in Madrid, versus 49 in Amsterdam. Examples in Madrid: Blue/Green late means .9832; Blue/Green overall means .9814; NDBI/BSI means .9792. Correlation participation ratio `(trace C)^2 / trace(C^2)` is 5.6010 for Madrid, 4.8037 for Amsterdam. This is not a chosen embedding dimension or proof that six components suffice.

**INFERENCE:** Equal Euclidean weight per standardised column can count correlated signals repeatedly. A regularised, source-supervised metric is a defensible first hypothesis; full inverse covariance without shrinkage is not.

**FACT:** `has_early_data` is constant (all scaled values zero). `has_late_data=0` originally occurs in 163 Madrid and 7 Amsterdam pixels; after source scaling these are -21.6072 versus +.04628 for observed late data. The squared distance between the two values is about 468.88 from a single indicator.

**INFERENCE:** Rare binary missingness can disproportionately affect Euclidean distances despite tiny RF importance. This is a targeted future ablation concern, not justification to change the accepted preprocessing or silently drop columns.

## 7. Exact model inspection — FACT

Zero-based cell indices (some older readiness notes use one-based numbering):

- Notebook 3 working copy: cells 8/10/12/14/17 select first QA-valid per-band observations, drop missing bands, filter Blue > 15,000, record coverage before filling, interpolate complete 1984–2025 trajectories with edge fill, calculate five indices, aggregate 60 features, and fit source-only global scaling.
- Features: 12 overall band mean/std + 10 index mean/std + 12 early (1984–2003) + 12 late (2004+) + 12 annual-difference mean/std + 2 coverage indicators. `age_class`, `weighted_mean_year`, and coordinates are not predictive columns. Feature construction nonetheless requires labels to filter/group rows and carry metadata: label-free raw inference is not implemented.
- With 42 complete annual samples, mean annual first-difference telescopes to `(last-first)/41`. It is a net endpoint-change feature, not an estimate of construction-event timing. This is mathematical interpretation of the unchanged feature definition, not a newly tested feature.
- Notebook 4 cell 6: `RepeatedStratifiedKFold(5,5,random_state=42)`; `RandomForestClassifier(n_estimators=500,class_weight='balanced',random_state=42,n_jobs=-1)` for every fold. Learned scaling is already global before CV; spatial blocks are not used.
- Cell 13: final RF fits all Madrid. Defaults recovered from saved RF include `criterion='gini'`, `max_features='sqrt'`, `bootstrap=True`, `max_depth=None`, `min_samples_split=2`, `min_samples_leaf=1`, `ccp_alpha=0`, `max_samples=None`, `oob_score=False`, `warm_start=False`.
- Saved RF contains 500 trees and 13,912,642 total nodes; tree depths min/median/max are 31/37/48. Pickle is 1,336,382,673 bytes. Plan memory and export costs accordingly.
- Cells 18/21: frozen final forest predicts/provides probabilities on Amsterdam; labels only evaluate these outputs.
- Cell 24: nearest class mean in Madrid-scaled raw features; equal-centroid Euclidean argmin, no source-RF state. `default_rng(42)` advances over budgets `[5,10,25,50,100,200]`, ten trials each, ascending classes; without replacement within each support draw; queries are the complement. `min(n_shots,n_class)` exists but does not bind on these class counts.
- Cells 27/29: separate illustration RNGs, not benchmark trial IDs. Softmax of negative L2 distances is a heuristic, not calibrated probabilities.

### Source RF impurity importance (read from saved state)

| Feature | Importance |
|---|---:|
| NIR_early_mean | .03871 |
| Red_late_std | .03045 |
| NIR_mean | .02837 |
| UI_mean | .02633 |
| Red_std | .02590 |
| Green_late_std | .02363 |
| Red_early_std | .02197 |
| Blue_late_std | .02178 |
| SWIR1_late_std | .02121 |
| Green_std | .02038 |

Group sums: early .20970; late .22949; overall .20896; YOY .17614; indices .17567; indicators .0000506. Group sizes differ; impurity importance is source-training descriptive evidence, not a causal or target-transfer ranking. The highest-ranked feature, NIR early mean, shifts by -1.4684 source SD. Avoid directly equating importance with transfer robustness.

## 8. What cannot be concluded

- Prototype per-class benefits and exact paired uncertainty: missing episode predictions/indices.
- Final RF in-sample predictions or individual CV forests: not retained; not needed to rerun this audit and **not a reason to rerun Notebook 4**.
- Calibration as the cause of the gap, sensor/season as the cause of a feature shift, or covariate-vs-concept shift isolation: not established.
- A candidate's score, optimal dimension, feature subset, regularisation, or calibration rule: none evaluated.
- An untouched final audit set: full-target labels already participated in baseline evaluation and authorised retrospective EDA. New episode draws over the same pixels do not erase this exposure.

## 9. Reproduction of core diagnostics (read-only recipe)

Run from repository root with the approved existing environment; do not execute reference runners. This snippet only recalculates metrics from saved predictions:

```python
import numpy as np
for path, yk, pk in [
    ('working/baseline_artifacts/madrid_cv_oof.npz', 'oof_true', 'oof_pred'),
    ('working/baseline_artifacts/amsterdam_zero_shot.npz', 'y_amsterdam', 'y_ams_pred_zero'),
]:
    with np.load(path, allow_pickle=False) as a:
        y, p = a[yk], a[pk]
        cm = np.bincount(4*(y-1)+(p-1), minlength=16).reshape(4, 4)
        f1 = 2*cm.diagonal() / (cm.sum(0)+cm.sum(1))
        print(path, cm, f1, f1.mean(), sep='\n')
```

Distribution recipe: use the accepted matrices; population means/SD (`ddof=0`); per-feature empirical KS `max_x |F_M(x)-F_A(x)|` at pooled observed values (right-continuous CDF); quantiles `[0,.01,.05,.5,.95,.99,1]`; class means only for the authorised diagnostic decomposition. Correlations exclude the source-constant feature. Do not reuse resulting target summaries as candidate fitting inputs. No bootstrap, new seeds, prediction rerun, or significance test was performed.
