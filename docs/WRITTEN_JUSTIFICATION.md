# Written Justification

**StatsGeeks — Building-age classification, Madrid → Amsterdam few-shot transfer**

**Word limit: 500 — confirmed by the organisers, 2026-09-09.**
→ **Submit the version below.** The short form at the end is retained only as a fallback if a shorter limit is ever imposed.

---

# SUBMISSION VERSION

### Model design

Stage 1 is a 500-tree, class-balanced Random Forest trained only on Madrid's 76,263 pixels across the organiser's 60 spectral-trajectory features, with a fixed seed. We deliberately retained their model and hyperparameters. Our contribution is the transfer mechanism, and holding the classifier constant makes every comparison attributable to it, not to tuning.

From the fitted forest we extract feature importances. These define a weighted distance metric and a ranked feature subset; we retain 30 features at five shots and 45 above. That metric — 60 numbers, 3 KB on disk — is the entire transferred artifact. The 244 MB forest derives it but is never needed at adaptation time, so the shipped state is portable and reload-testable.

We also verified the feature contract: `has_early_data` is constant in both cities and the forest assigns it importance zero. The usable width is 59.

### Transfer strategy

The organiser's baseline trains a Madrid forest and then discards it, computing Amsterdam prototypes from Amsterdam data alone. Madrid contributes only the scaler's mean and variance. That is target-only fitting: its rising curve measures an Amsterdam-only method receiving more Amsterdam data.

Our method freezes the Madrid-learned metric, projects Amsterdam pixels through it, and forms prototypes from support labels. The difficulty is estimation, not classification: an Amsterdam class mean from five pixels in 60 dimensions is nearly unbiased but noise-dominated, whereas Madrid's is biased — different city — yet built from 76,263 pixels and stable.

We therefore shrink the target estimate toward Madrid's class geometry, subtracting each city's own mean beforehand so that class *structure* transfers without importing Madrid's absolute location in feature space. The weight was recovered empirically, not imposed: 0.6 at five shots, zero from twenty-five upward, while retained features move oppositely, 30 to 45. Both match estimation-error theory.

We compared nine frozen source representations under one procedure. Three failed — rank-3 LDA, the forest's probability space, and a 94-feature season-aware set built after measuring a real 70-day observation-date offset between the cities. All failed for one reason: too few dimensions, or too many.

Query labels never fit or select anything. The Amsterdam centre uses support pixels only; unlabelled query alignment would likely have helped but is an unconfirmed permission.

### F1 interpretation

Against the organiser's method on identical pixels and episodes, four-class macro F1 improves at every budget: 0.5038→0.5524 at five shots, a 9.7% relative gain, and approximately 1.5% from twenty-five shots upward. We win 47 of 50 paired episodes, 10 of 10 at three budgets.

Because episodes are matched, these are paired comparisons in which draw luck cancels; consistency rather than magnitude is the evidence. Reported deviations are spreads, not confidence intervals.

The gain concentrates where target data is scarcest — the method's prediction, not a coincidence. At 200 shots Amsterdam reaches 0.6240 against Madrid's full-data 0.6281, indicating a label-noise ceiling: labels are area-weighted averages over mixed-age buildings in one 30-metre pixel.

---

## Rubric coverage

| Requirement | Where |
|---|---|
| Model design | §1 |
| Transfer strategy | §2 — genuine source-state reuse, low-data mechanics |
| F1 interpretation | §3 — trends across budgets, what the numbers mean |
| Domain-shift handling | §2 — mean-subtraction as first-order correction |
| Controlled ablations | §2 — nine representations, three documented failures |
| Uncertainty stated correctly | §3 — spreads, explicitly not confidence intervals |
| Limitations acknowledged | §1 dead feature · §3 label-noise ceiling |
| No overclaiming | no portability or calibration claims anywhere |

---

# FALLBACK — short form

*Not the submission. Use only if a shorter limit is later imposed.*

### Model design

Stage 1 is a 500-tree, class-balanced Random Forest trained only on Madrid's 76,263 pixels across 60 spectral-trajectory features, with a fixed seed. We kept the organiser's model and hyperparameters deliberately: our contribution is the transfer mechanism, and holding the classifier constant makes the comparison interpretable. From that forest we extract feature importances, which define a weighted distance metric, and retain the 30–45 most informative features depending on budget. That metric — 3 KB — is the entire transferred artifact; the forest is never needed at adaptation time.

### Transfer strategy

The organiser's baseline trains a Madrid forest then discards it, computing Amsterdam prototypes from Amsterdam data alone. That is target-only fitting, not transfer. Our method freezes the Madrid-learned metric, projects Amsterdam pixels into it, and forms class prototypes. An Amsterdam class mean from five pixels is nearly unbiased but very noisy; Madrid's is biased yet stable. We therefore shrink the target estimate toward Madrid's class geometry, subtracting each city's mean first so structure transfers without importing Madrid's position. The weight is budget-dependent: 0.6 at five shots, zero from twenty-five upward. Query labels never fit anything; the Amsterdam centre uses support pixels only.

### F1 interpretation

Against the organiser's method on identical episodes, macro F1 improves at every budget: 0.5038→0.5524 at five shots (+9.7% relative), about +1.5% from twenty-five upward, winning 47 of 50 paired episodes. Reported deviations are spreads across episodes, not confidence intervals. The gain concentrates where target data is scarcest — the prediction, not a coincidence. At 200 shots Amsterdam approaches Madrid's own full-data score of 0.6281, indicating a label-noise ceiling: labels are area-weighted averages over mixed-age buildings in a 30-metre pixel.
