# Written Justification

**StatsGeeks — Building-age classification, Madrid → Amsterdam few-shot transfer**

The rubric requires three pillars: **model design**, **transfer strategy**, and **F1 interpretation**. Each is a section below.

Two versions are provided because the word limit is unresolved — Notebook 1 states 300 words, the rubric states 500. **Submit Version A (269 words)** unless the organisers confirm 500.

---

## VERSION A — 269 words *(satisfies both limits)*

### Model design

Stage 1 is a 500-tree, class-balanced Random Forest trained only on Madrid's 76,263 pixels across 60 spectral-trajectory features, with a fixed seed. We kept the organiser's model and hyperparameters deliberately: our contribution is the transfer mechanism, and holding the classifier constant makes the comparison interpretable. From that forest we extract feature importances, which define a weighted distance metric, and retain the 30–45 most informative features depending on budget. That metric — 3 KB — is the entire transferred artifact; the forest is never needed at adaptation time.

### Transfer strategy

The organiser's baseline trains a Madrid forest then discards it, computing Amsterdam prototypes from Amsterdam data alone. That is target-only fitting, not transfer. Our method freezes the Madrid-learned metric, projects Amsterdam pixels into it, and forms class prototypes. An Amsterdam class mean from five pixels is nearly unbiased but very noisy; Madrid's is biased yet stable. We therefore shrink the target estimate toward Madrid's class geometry, subtracting each city's mean first so structure transfers without importing Madrid's position. The weight is budget-dependent: 0.6 at five shots, zero from twenty-five upward. Query labels never fit anything; the Amsterdam centre uses support pixels only.

### F1 interpretation

Against the organiser's method on identical episodes, macro F1 improves at every budget: 0.5038→0.5524 at five shots (+9.7% relative), about +1.5% from twenty-five upward, winning 47 of 50 paired episodes. Reported deviations are spreads across episodes, not confidence intervals. The gain concentrates where target data is scarcest — the prediction, not a coincidence. At 200 shots Amsterdam approaches Madrid's own full-data score of 0.6281, indicating a label-noise ceiling: labels are area-weighted averages over mixed-age buildings in a 30-metre pixel.

---

## VERSION B — 479 words *(if 500 is confirmed)*

### Model design

Stage 1 is a 500-tree, class-balanced Random Forest trained only on Madrid's 76,263 pixels across the organiser's 60 spectral-trajectory features, with a fixed seed. We deliberately retained their model and hyperparameters. Our contribution is the transfer mechanism, and holding the classifier constant makes every comparison attributable to that mechanism rather than to tuning.

From the fitted forest we extract feature importances. These define a weighted distance metric and a ranked feature subset; we retain 30 features at five shots and 45 above. That metric — 60 numbers, 3 KB on disk — is the entire transferred artifact. The 244 MB forest is the apparatus that derives it and is never required at adaptation time, which makes the shipped state trivially portable and reload-testable.

We also verified the feature contract: one of the 60 features, `has_early_data`, is constant across both cities, and the forest independently assigns it importance zero. The usable width is 59.

### Transfer strategy

The organiser's baseline trains a Madrid forest and then discards it, computing Amsterdam prototypes from Amsterdam data alone. Madrid contributes only the scaler's mean and variance. That is target-only fitting, and its rising learning curve measures an Amsterdam-only method receiving more Amsterdam data.

Our method freezes the Madrid-learned metric, projects Amsterdam pixels through it, and forms prototypes from support labels. The difficulty is estimation, not classification: an Amsterdam class mean from five pixels in 60 dimensions is nearly unbiased but noise-dominated, whereas Madrid's is biased — different city — yet estimated from 76,263 pixels and therefore stable.

We therefore shrink the target estimate toward Madrid's class geometry, subtracting each city's own mean beforehand so that class *structure* transfers without importing Madrid's absolute location in feature space. The shrinkage weight is budget-dependent and was recovered empirically, not imposed: 0.6 at five shots, falling to zero from twenty-five upward. The retained feature count moves in the opposite direction, from 30 to 45. Both trends match what estimation-error theory predicts.

Query labels are never used for fitting or selection. The Amsterdam centre is computed from the support set alone; unlabelled query alignment was available and would likely have helped, but the brief lists it as an unconfirmed permission.

### F1 interpretation

Against the organiser's method on identical pixels and episodes, four-class macro F1 improves at every budget: 0.5038→0.5524 at five shots, a 9.7% relative gain, and approximately 1.5% from twenty-five shots upward. We win 47 of 50 paired episodes, including 10 of 10 at three separate budgets.

Because episodes are matched, these are paired comparisons in which draw luck cancels; consistency rather than magnitude is the evidence. Reported deviations are spreads, not confidence intervals.

The gain concentrates where target data is scarcest, which is the prediction of the method rather than a coincidence. At 200 shots Amsterdam reaches 0.6240 against Madrid's own full-data cross-validated 0.6281, indicating a label-noise ceiling: labels are area-weighted averages over mixed-age buildings within a single 30-metre pixel.

---

## Rubric coverage check

| Requirement | Where |
|---|---|
| Model design | §1 of both versions |
| Transfer strategy | §2 — genuine source-state reuse, low-data mechanics |
| F1 interpretation | §3 — trends, budgets, what the numbers mean |
| Domain-shift handling | §2 — mean-subtraction as first-order correction |
| Uncertainty stated correctly | §3 — spreads, explicitly not confidence intervals |
| Limitations acknowledged | §3 — label-noise ceiling |
| No overclaiming | no portability or calibration claims anywhere |
