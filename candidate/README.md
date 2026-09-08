# `candidate/` — the source-learned transfer method

This folder contains the team's actual transfer learning method: the thing the
organiser's starter code does **not** do.

> **The one-line version.** The starter trains a Random Forest on Madrid, then
> throws it away and builds Amsterdam prototypes from Amsterdam data alone. That
> is target-only fitting, not transfer. Everything here exists to fix that and to
> *prove* the fix helped.

Everything below was produced on branch `member2-baseline`, tag `day1-candidate-v1`.
Status: **smoke/development**. Not reviewed by another member.

---

## Before you can run anything

You need two files that are **not in this repository** (too large for GitHub):

```
data/madrid_train.parquet        142 MB   from the organisers / hackathon VM
data/amsterdam_data.parquet       44 MB   from the organisers / hackathon VM
```

Then generate the feature cache once (~13½ minutes):

```bash
# run the working copy of the organiser's Notebook 3 with CWD = working/
cd working && jupyter nbconvert --to notebook --execute --inplace 3-Preprocessing.ipynb
```

That writes `data/preprocessed/preprocessed_data.pkl` (48 MB, also not in git).
It should have **SHA256 `f6f588c4e3cfa2e0793354bc7772228bd4c749b39fce67bde5302f4c63955f33`** —
check it matches, or your features differ from the ones every number here was
computed on, and no comparison will be valid.

**All scripts run from the repository root**, not from inside `candidate/`.

---

## The scripts, in the order they were run

| File | What it does | Runtime |
|---|---|---|
| `transfer_candidate.py` | First candidate. Five representations, select on trials 0–4, audit on 5–9. | ~2 min |
| `search_representations.py` | Nine representations, eight hypotheses. **Selection trials only** — never touches the audit set. | ~4 min |
| `final_audit.py` | Single audit run of the selected method on the sealed trials. Writes the final Stage 1 artifact. | ~2 min |
| `reload_test.py` | **Gate S.** Reloads the artifact in a clean session and adapts with no query labels present. 17 checks. | ~5 s |
| `validity_checks.py` | Label-boundary inclusivity + spatial sensitivity. | ~1 min |
| `make_figures.py` | Exports the six presentation figures. Re-runs no model. | ~10 s |

**If you only run one thing, run `reload_test.py`.** Gate S requires it to be
executed by someone *other* than its author, and that has not happened yet.

```bash
python candidate/reload_test.py
```

---

## `artifacts/` — what each file is

| File | Size | What it is |
|---|---|---|
| `stage1_madrid.pkl` | **3 KB** | **The deliverable.** Frozen Madrid state that adaptation consumes. |
| `stage1_rf.joblib` | 244 MB | The source Random Forest. **Not in git.** Only needed to reproduce zero-shot — adaptation does not use it. |
| `episodes.npz` | 52 KB | The stored support-pixel indices for every trial and budget. |
| `final_audit.json` | — | The headline results: audit trials only. |
| `search_selection.json` | — | All nine methods, selection trials only. |
| `results.json` | — | The earlier five-method run. |
| `validity_checks.json` | — | Boundary and spatial-sensitivity results. |

### Why the deliverable is 3 KB and the model is 244 MB

The transfer is carried by **60 importance weights and a 30-feature subset** —
not by the forest. The forest is only the apparatus that derived them. So the
artifact you actually ship is 3 KB, and it reloads anywhere instantly.

### Why episode indices are stored rather than a seed

A seed is a *recipe*; it only reproduces in an identical environment. This project
has direct evidence that this matters — the same `random_state=42` produces
different Random Forest results on our scikit-learn than on the organiser's
(see `docs/EXPERIMENT_LOG.md` EXP-001). Storing the drawn indices is immune to that.

---

## How the method works

Every method here is the **same procedure**, so comparisons are controlled:

```
1. Learn a transform T on MADRID ONLY, then freeze it.
2. Push Amsterdam support and query features through T.
3. Class prototypes = mean of the support pixels of each class, in T-space.
4. Each query pixel gets the class of its nearest prototype.
```

Only `T` changes between methods:

| method | `T(x)` | what it means |
|---|---|---|
| `raw` | `x` | **the control** — no Madrid learning at all |
| `rfw` | `x * sqrt(importances)` | Madrid says *which features matter* |
| `top30` | top 30 features, weighted | Madrid *selects* as well as weights |
| `leaf` | RF leaf co-occupancy | Madrid's learned *partition* |
| `lda` | LDA projection (rank 3) | Madrid's supervised directions |
| `wcw*` | within-class whitening | Madrid says which directions are *noise* |
| `proba` | `RF.predict_proba(x)` | Madrid classifier's output space |

**`raw` is the comparison that matters.** Beating zero-shot proves nothing —
zero-shot is a terrible bar. Beating target-only prototypes *on identical
episodes* is what demonstrates that Madrid's supervision helped.

---

## The results

Final audit, trials 5–9, sealed until reported once:

| shots/class | control | top30 | benefit | paired wins |
|---|---|---|---|---|
| 5 | 0.5556 | 0.5589 | +0.0033 | 4/5 |
| 25 | 0.5956 | 0.6028 | +0.0072 | 3/5 |
| 50 | 0.6152 | 0.6179 | +0.0026 | 4/5 |
| 100 | 0.6191 | 0.6208 | +0.0018 | 3/5 |
| 200 | 0.6185 | 0.6227 | +0.0042 | 5/5 |

Zero-shot (no Amsterdam labels): **0.4433**. Madrid CV on full data: **0.6281**.

### Read these honestly

- **The effect is small** (+0.002 to +0.007). The evidence is *consistency across
  matched episodes*, not magnitude. Do not describe this as a large improvement.
- **Standard deviations are spreads across 5 episodes, not confidence intervals.**
- **Two methods have been audited** (`rfw`, then `top30`). Each cycle was clean
  individually, but choosing between them on their audit scores would be
  selection on audit data. **It has not been done and must not be.** The
  defensible claim is: *several source-learned representations give roughly
  +0.002 to +0.007 over target-only prototypes and are not distinguishable at
  this sample size.*

### The finding worth presenting

**The ranking of methods depends on the label budget.**

| method | 5 shots | 200 shots |
|---|---|---|
| `wcw10` | **−0.0218** | **+0.0090** |
| `wcw10_rfw` | **−0.0131** | **+0.0131** |

Within-class whitening amplifies low-variance directions. With 5 support points
per class that is destructive; with 200 the prototypes are stable enough to
benefit. The same transform, opposite verdict, depending only on how much target
data you have.

This also explains why `lda` failed: not because Madrid's supervision is useless,
but because rank-3 projection discards too much. Full-rank whitening recovers the
benefit at high budgets.

---

## `figures/`

| File | Use |
|---|---|
| `fig1_learning_curve.png` | **Required deliverable** — F1 with error bars vs log₂(sample size) |
| `fig2_transfer_benefit.png` | The gain over the control, per budget |
| `fig3_method_ablation.png` | All nine representations ranked |
| `fig4_budget_dependence.png` | The budget-dependence finding |
| `fig5_confusion.png` | Where it still fails (Class 2 is hardest) |
| `fig6_per_class.png` | Per-class F1, control vs candidate |

---

## Known limitations — state these, do not hide them

1. **Features are still built label-dependently.** Feature generation filters on
   `age_class.notna()`, inherited from the organiser's Notebook 3. There is no
   *target* leakage — the scaler saw only Madrid — but the pipeline could not
   currently generate features for an unlabelled hidden test set.
   (MASTER_PLAN priorities #10, #11 remain open.)
2. **Scaling is fitted on all Madrid before cross-validation.** Not fold-safe.
3. **The audit set has informed two decisions.** See above.
4. **No independent verification yet.** Gate S needs a different member.
5. **We appear to be near a ceiling.** Amsterdam few-shot at 200 shots (0.6227)
   has essentially caught Madrid's own full-data CV score (0.6281). The labels are
   intrinsically noisy — `weighted_mean_year` is an area-weighted average over
   whatever buildings fall in a 30 m pixel, so a pixel with a 1950s block and a
   2010s block gets a class describing neither. Further tuning is unlikely to help.
