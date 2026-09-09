# StatsGeeks — Project Summary

**Building-age classification from Landsat: Madrid → Amsterdam few-shot transfer**

Branch `member2-baseline` · tag `day1-candidate-v1`
Status: smoke/development. Not independently re-run by a second member.

---

## 1. The challenge

Each 30 m × 30 m Landsat pixel is observed once a year from 1984–2025 across six spectral bands. Classify the **construction era** of the buildings inside that pixel into four classes. Train on **Madrid** (76,263 pixels), adapt to **Amsterdam** (25,992 pixels) using as few as **five labelled examples per class**. Scored on four-class **macro F1**.

The premise is physical: construction changes what ground looks like from space, and a 42-year trajectory carries a fingerprint of when it happened.

---

## 2. What we found before writing any code

**The starter's transfer learning transfers nothing.**

It trains a Random Forest on Madrid, then discards it. Amsterdam prototypes are computed from Amsterdam data alone; Madrid contributes only the scaler's mean and variance. Its headline learning curve — F1 rising with more labels — measures an *Amsterdam-only* method receiving more Amsterdam data. No knowledge crosses between cities.

The rubric allows **up to 20 points deducted, or disqualification**, for not actually performing transfer learning.

---

## 3. Reproducing the baseline

Ran the organiser's notebooks with **zero code edits**. Notebook 3 in 13m 28s, Notebook 4 in 16m 15s, both clean, 25/25 CV fits verified by counting individual output lines rather than trusting the summary.

**The results split perfectly in two:**

| | reproduced | organiser | delta |
|---|---|---|---|
| Madrid CV | 0.6281 | 0.6179 | +0.0102 |
| Amsterdam zero-shot | 0.4433 | 0.3427 | +0.1006 |
| Prototypes, all six budgets | identical | identical | **0.0000** |

Every result that touches the Random Forest differs. Every result that does not matches to four decimal places.

**The starter's own defect became the instrument that explained this.** Because the prototype path never uses the forest, it exercises the whole data pipeline and the RNG while touching zero scikit-learn tree code. Its exact match proves the data path is bit-identical, isolating the divergence to scikit-learn's version.

Then we checked what actually mattered: a systematic version difference and an unrepeatable run look identical from a single run, with opposite consequences. **Two refits gave `0.4432736088` both times — 0 of 25,992 predictions differed.** Systematic, not noise.

**Consequence:** we benchmark against **0.6281 / 0.4433**, never the published figures. Using theirs would credit a candidate with ~0.10 of improvement that is purely a library difference.

**Also found:** `has_early_data` is constant across both cities. The feature set is **59 informative, not 60**. The Random Forest independently assigns it importance exactly `0.000000`.

---

## 4. What we built

Every method tested is the **same procedure**, so comparisons are controlled:

```
1.  Learn a transform T on MADRID ONLY
2.  Freeze it — never refit on Amsterdam
3.  Project Amsterdam support and query through T
4.  Class prototypes from support labels only; nearest prototype wins
```

Only `T` changes. **`raw` — T = identity — is the target-only control**, and it is the comparison that matters. Beating zero-shot proves nothing; beating `raw` on identical episodes demonstrates transfer.

### The contribution: prototype shrinkage

At five shots, an Amsterdam class mean is estimated from **five points in 60 dimensions** — nearly unbiased, wildly noisy. Madrid's class prototype comes from **76,263 pixels** — biased, because it is a different city, but stable.

That is a James–Stein situation. Shrink the noisy estimate toward the stable one:

```
p_c(lambda) = mu_A + lambda*(Madrid class offset) + (1-lambda)*(support mean - mu_A)
```

- **λ = 0** is exactly the target-only control
- **λ = 1** is pure Madrid class structure, re-centred on Amsterdam

Subtracting each city's own mean first is a first-order domain-shift correction: it transfers the class *geometry* without importing Madrid's absolute position in feature space.

`mu_A` uses the **support set only**. Query features are never touched, even though using them would be easy and would probably help — the plan lists unlabelled query alignment as an unconfirmed permission.

### Two knobs, both budget-dependent

| shots | features kept (k) | shrinkage (λ) |
|---|---|---|
| 5 | 30 | **0.6** |
| 25 | 45 | 0.0 |
| 50 | 45 | 0.0 |
| 100 | 45 | 0.0 |
| 200 | 45 | 0.0 |

**λ falls** as target data grows. **k rises.** Neither was imposed — both were recovered from selection trials, and both move exactly as estimation-error theory predicts.

---

## 5. Results

Our method against the starter's actual method, **identical pixels, identical episodes, identical environment**:

| shots/class | starter | ours | gain | relative | episodes won |
|---|---|---|---|---|---|
| **5** | 0.5038 | **0.5524** | **+0.0487** | **+9.7%** | 8/10 |
| 25 | 0.6037 | **0.6122** | +0.0085 | +1.4% | 9/10 |
| 50 | 0.6090 | **0.6173** | +0.0083 | +1.4% | **10/10** |
| 100 | 0.6087 | **0.6195** | +0.0108 | +1.8% | **10/10** |
| 200 | 0.6135 | **0.6240** | +0.0105 | +1.7% | **10/10** |

**47 of 50 paired episodes won. Better at every budget.** Audited on seed 31337 — a fourth episode set, never used for selection.

---

## 6. The unifying idea

Four separate experiments turned out to be the same phenomenon:

| experiment | observation | mechanism |
|---|---|---|
| Whitening (EXP-004) | flips sign with budget | amplifies noisy directions |
| Season features (EXP-007) | 94 features lose to 60 | dilution |
| Shrinkage (EXP-009) | helps most at 5 shots | borrows a stable estimate |
| Joint sweep (EXP-010) | k and λ both move with budget | both trade bias for variance |

> **Few-shot transfer is an estimation-error problem, not a classifier problem. Every knob that helps attacks the same thing, and each one's optimal setting depends on how much target data you have.**

---

## 7. What failed, and why

| attempt | result | why |
|---|---|---|
| Rank-3 LDA projection | −0.0056 | compresses 60 dims to 3 — discards what Amsterdam needs |
| RF probability space | −0.0611, worst of nine | 4 dimensions cannot separate the prototypes |
| 94 season-aware features | +0.0001, then worse on audit | informative but dilutive — 29% of importance across 38% of columns |

The season work deserves its own note. We **measured a real 70-day offset** between the cities' observation dates — Madrid's median is day 175, Amsterdam's day 105; June–August share 48.3% vs 20.5%. Part of the apparent domain shift is phenology, not architecture. We rebuilt the feature pipeline to control for it. **It did not help.** The hypothesis was well-motivated, correctly tested, and wrong.

---

## 8. Limitations — stated, not hidden

1. **Feature generation is still label-dependent** in the shipped pipeline. We built and validated a label-free builder, but its features scored slightly worse, so the reference features were kept. No hidden-test inference path as it stands.
2. **Scaling is fitted before cross-validation** — not fold-safe. Inherited from the starter, deliberately unrepaired inside the reference run.
3. **The λ schedule is five values chosen on five selection trials.** Overfitting risk is real; the monotonicity and its agreement with theory argue against pure noise.
4. **Optimal k moves once** (30 → 45). The direction agrees with theory, but one transition is weak evidence for a trend.
5. **We appear to be near a label-noise ceiling.** Three independent lines: nine transfer methods within 0.011; two separately built feature sets both plateau near 0.62; Amsterdam at 200 shots approaches Madrid's own full-data CV of 0.6281.
6. **Not independently re-run.** Gate S asks a second member to reload the artifact and run inference; the team lost a member mid-project.

---

## 9. Reproducibility

- `requirements.txt` pins the exact stack that produced every number
- Raw data and feature-cache SHA256 recorded
- **Episode support indices stored, not regenerated from a seed** — a seed only reproduces in an identical environment, and this project has direct evidence of that failing
- Stage 1 artifact is **3 KB**; reload test passes **17/17** in a clean interpreter
- Cold-start reproduction: **~35 minutes**, documented in `SUBMISSION_INVENTORY.md`
- Four independent episode seeds; selection and audit sets never overlap

---

## 10. Where everything lives

| | |
|---|---|
| Method | `candidate/shrinkage_transfer.py`, `candidate/joint_sweep.py` |
| Baseline verification | `scripts/` (3 tools) |
| Artifacts | `candidate/artifacts/` |
| Figures | `candidate/figures/` (9) |
| Experiment records | `docs/EXPERIMENT_LOG.md` — EXP-001…010 |
| Decisions | `docs/DECISION_REGISTER.md` — DEC-001…014 |
| Deck | `presentation/StatsGeeks_BuildingAge.pptx` |
| Submission inventory | `docs/SUBMISSION_INVENTORY.md` |
