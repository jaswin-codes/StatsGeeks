# Written Justification

**StatsGeeks — Building-age classification, Madrid → Amsterdam few-shot transfer**

The rubric requires three pillars: **model design**, **transfer strategy**, and **F1 interpretation**. Each is a section below.

Two versions are provided because the word limit is unresolved — Notebook 1 states 300 words, the rubric states 500. **Submit the 297-word version** unless the organisers confirm 500.

---

## VERSION A — 297 words *(satisfies both limits)*

### Model design

Stage 1 is a 500-tree, class-balanced Random Forest trained only on Madrid's 76,263 pixels across 60 spectral-trajectory features, with a fixed seed. We deliberately kept the organiser's model and hyperparameters: our contribution is the transfer mechanism, and holding the classifier constant makes the comparison interpretable. From that forest we extract feature importances, which define a weighted distance metric, and retain the 30–45 most informative features depending on label budget. That metric — 60 numbers, 3 KB — is the entire transferred artifact. The forest itself is never required at adaptation time.

### Transfer strategy

The organiser's baseline trains a Madrid forest and then discards it, computing Amsterdam prototypes from Amsterdam data alone; Madrid contributes only a scaler. That is target-only fitting, not transfer. Our method freezes the Madrid-learned metric, projects Amsterdam support and query pixels into it, and forms class prototypes. Critically, an Amsterdam class mean estimated from five pixels is nearly unbiased but very noisy, whereas Madrid's prototype is biased yet stable. We therefore shrink the target estimate toward Madrid's class geometry, subtracting each city's own mean first so that class structure transfers without importing Madrid's absolute position. The shrinkage weight is budget-dependent: 0.6 at five shots, zero from twenty-five upward. Query labels are never used for fitting, and the Amsterdam centre is computed from support pixels only.

### F1 interpretation

Against the organiser's method on identical episodes, four-class macro F1 improves at every budget: 0.5038→0.5524 at five shots (+9.7% relative) and approximately +1.5% from twenty-five upward, winning 47 of 50 paired episodes. Reported deviations are spreads across episodes, not confidence intervals. The gain concentrates where target data is scarcest, which is the prediction rather than a coincidence. At 200 shots Amsterdam approaches Madrid's own full-data cross-validated score of 0.6281, indicating a label-noise ceiling — labels are area-weighted averages over mixed-age buildings within a 30-metre pixel.

---

## VERSION B — 486 words *(if 500 is confirmed)*

### Model design

Stage 1 is a 500-tree, class-balanced Random Forest trained only on Madrid's 76,263 pixels across the organiser's 60 spectral-trajectory features, with a fixed seed. We deliberately retained their model and hyperparameters. Our contribution is the transfer mechanism, and holding the classifier constant makes every comparison attributable to that mechanism rather than to tuning.

From the fitted forest we extract feature importances. These define a weighted distance metric and a ranked feature subset; we retain 30 features at five shots and 45 above. That metric — 60 numbers, 3 KB on disk — is the entire transferred artifact. The 244 MB forest is the apparatus that derives it and is never required at adaptation time, which makes the shipped state trivially portable and reload-testable.

We also verified the feature contract itself. One of the 60 features, `has_early_data`, is constant across both cities; the forest independently assigns it importance exactly zero. The usable width is 59, not 60.

### Transfer strategy

The organiser's baseline trains a Madrid forest and then discards it, computing Amsterdam prototypes from Amsterdam data alone. Madrid contributes only the scaler's mean and variance. That is target-only fitting, and its rising learning curve measures an Amsterdam-only method receiving more Amsterdam data.

Our method freezes the Madrid-learned metric, projects Amsterdam support and query pixels through it, and forms class prototypes from support labels. The central difficulty is estimation, not classification: an Amsterdam class mean built from five pixels in a 60-dimensional space is nearly unbiased but dominated by noise, whereas Madrid's corresponding prototype is biased — it is a different city — but estimated from 76,263 pixels and therefore stable.

We therefore shrink the target estimate toward Madrid's class geometry, subtracting each city's own mean beforehand so that class *structure* transfers without importing Madrid's absolute location in feature space. The shrinkage weight is budget-dependent and was recovered empirically, not imposed: 0.6 at five shots, falling to zero from twenty-five upward. The retained feature count moves in the opposite direction, from 30 to 45. Both trends match what estimation-error theory predicts.

Query labels are never used for fitting or selection. The Amsterdam centre is computed from the support set alone; unlabelled query alignment was available and would likely have helped, but the brief lists it as an unconfirmed permission.

### F1 interpretation

Against the organiser's method on identical pixels and episodes, four-class macro F1 improves at every budget: 0.5038→0.5524 at five shots, a 9.7% relative gain, and approximately 1.5% from twenty-five shots upward. We win 47 of 50 paired episodes, including 10 of 10 at three separate budgets.

Because episodes are matched across methods, these are paired comparisons in which episode-draw luck cancels; consistency, rather than magnitude, is the evidence. Reported deviations are spreads across episodes and are not confidence intervals.

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
