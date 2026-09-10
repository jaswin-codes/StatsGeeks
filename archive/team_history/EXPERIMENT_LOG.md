# Experiment Log

Every run, including failures and abandoned attempts. Claims are labelled
**starter reference**, **reproduced reference**, **smoke/development**, or
**final audited**. EXP-010 below is the frozen primary scientific result.

Shared context for all entries: Python 3.13.15, pandas 3.0.5, numpy 2.5.1,
scikit-learn 1.9.0, Windows 11, 16 CPUs. Features from
`data/preprocessed/preprocessed_data.pkl`, SHA256 `f6f588c4…5f33`, 60 columns,
Madrid (76263, 60), Amsterdam (25992, 60). Metric is four-class macro F1
throughout. Seed 42 everywhere.

---

## EXP-001 — Reproduce the organiser baseline

**Status:** reproduced reference · **Commit:** `52c7357` · **Owner:** Member 2

**Hypothesis.** The organiser's saved outputs can be reproduced on this machine
from the unmodified notebooks.

**Changes.** None. Zero source-code edits across all 53 cells. Working copies
run with CWD `working/`, which makes the hardcoded `../data` resolve correctly.

**Result.** Notebook 3 reproduced every documented dataset fact exactly. Notebook
4 split cleanly: all six prototype budgets matched the organiser to four decimal
places (delta 0.0000), while both Random-Forest-dependent results differed —
Madrid CV 0.6281 vs 0.6179 (+0.0102), zero-shot 0.4433 vs 0.3427 (+0.1006).
25 of 25 CV fits confirmed by counting individual output lines.

**Interpretation.** The prototype path never uses the fitted RF, so it acted as
an unintended control: it exercises the whole data pipeline and the numpy RNG
while touching no scikit-learn tree code. Its exact match isolates the
divergence to the Random Forest implementation.

**Decision.** Keep. These become the team's reference datum on this hardware.

**Limitations.** The library-version explanation is *inferred from the control*,
not measured. Installing the organiser's scikit-learn and re-running would test
it; that has not been done. Open.

---

## EXP-002 — Determinism of the reference Random Forest

**Status:** reproduced reference · **Commit:** `52c7357` · **Owner:** Member 2

**Hypothesis.** The RF gap versus the organiser is systematic, not run-to-run
noise. A systematic difference and an unrepeatable run look identical from a
single run but have opposite consequences.

**Changes.** `scripts/determinism_check.py` — refit the final Madrid RF twice
from a separate process, identical settings, compare predictions exactly.

**Result.** Zero-shot macro F1 `0.4432736088` on both runs. **0 of 25,992
predictions differed**; probability matrices bit-identical; F1 delta exactly
`0.00e+00`. Reproduced four times in total across separate processes.

**Decision.** Keep. Determinism established, so 0.6281 is usable as a datum.

**Limitations.** Rules out randomness only. Says nothing about scikit-learn
versions — that remains EXP-001's open question. The script's own printed
conclusion overstates this and should be read with that correction.

---

## EXP-003 — First source-learned transfer candidate

**Status:** smoke/development · **Commit:** `f9dce46` · **Owner:** Member 3 scope

**Hypothesis.** Freezing state learned on Madrid and routing Amsterdam through
it will beat target-only prototypes on matched episodes. Beating zero-shot would
*not* demonstrate transfer; beating the target-only control does.

**Changes.** `candidate/transfer_candidate.py`. Every method is the same
procedure — freeze transform T learned on Madrid only, take Amsterdam prototypes
in T-space from support labels. Methods differ only in T:
`raw` (control, T=identity), `rfw` (importance weighting), `lda` (rank-3
supervised projection), `proba` / `logit` (RF output space).

**Protocol.** Matched, nested episodes; support indices stored rather than
regenerated from a seed; selection on trials 0–4, audit on trials 5–9; source
state frozen; label-free inference verified.

**Result.** `rfw` selected on 25-shot selection performance, then audited:

| shots | control | rfw | benefit | paired wins |
|---|---|---|---|---|
| 5 | 0.5556 | 0.5628 | +0.0072 | 5/5 |
| 25 | 0.5956 | 0.6023 | +0.0067 | 5/5 |
| 50 | 0.6152 | 0.6180 | +0.0028 | 5/5 |
| 100 | 0.6191 | 0.6215 | +0.0025 | 5/5 |
| 200 | 0.6185 | 0.6217 | +0.0033 | 5/5 |

**Decision.** Keep as a demonstrated transfer path. 25/25 paired wins.

**Limitations.** The effect is small (+0.003 to +0.007). The evidence is
consistency across matched episodes, not magnitude. `lda`, `proba` and `logit`
all *hurt* — recorded as negative results, not hidden.

---

## EXP-004 — Representation search over nine source states

**Status:** smoke/development, selection trials only · **Commit:** `96435da`

**Hypothesis.** Richer uses of the Madrid model should transfer better than a
60-number importance summary. Eight hypotheses tested (H1–H8), including
within-class whitening (H5: LDA's metric without LDA's rank-3 collapse) and RF
leaf-partition proximity (H8: the forest's actual learned partition).

**Result (selection trials 0–4, mean macro F1 across budgets).**

| method | mean | vs control | paired wins |
|---|---|---|---|
| top30 | 0.5978 | +0.0052 | 18/25 |
| leaf | 0.5974 | +0.0048 | 17/25 |
| rfw | 0.5966 | +0.0040 | 20/25 |
| wcw10_rfw | 0.5952 | +0.0026 | 17/25 |
| **raw (control)** | 0.5926 | — | — |
| lda | 0.5870 | −0.0056 | 8/25 |
| proba | 0.5315 | −0.0611 | 2/25 |

**Main finding — the ranking depends on label budget.** Within-class whitening
inverts across the curve:

| method | 5 shots | 200 shots |
|---|---|---|
| `wcw10` | **−0.0218** | **+0.0090** |
| `wcw10_rfw` | **−0.0131** | **+0.0131** |

Whitening amplifies low-variance directions. With 5 support points per class
that is destructive; with 200 the prototypes are stable enough to benefit. This
also explains EXP-003's LDA failure: LDA failed from the rank-3 collapse, not
because Madrid's supervision is useless — full-rank whitening recovers the
benefit at high budgets.

**Decision.** Report the budget-dependence as the substantive result. Do **not**
claim a single best method: the top four are separated by 0.0012 across 5 trials
and are not distinguishable.

---

## EXP-005 — Final audit of `top30`

**Status:** smoke/development · **Commit:** `96435da`

**Selection rule, fixed in advance.** `MASTER_PLAN.md` names 25-shot stability as
the target before any result was seen, so applying it is not post-hoc. `top30`
wins on that criterion.

**Result (trials 5–9, sealed until this run).**

| shots | control | top30 | benefit | wins |
|---|---|---|---|---|
| 5 | 0.5556 | 0.5589 | +0.0033 | 4/5 |
| 25 | 0.5956 | 0.6028 | +0.0072 | 3/5 |
| 50 | 0.6152 | 0.6179 | +0.0026 | 4/5 |
| 100 | 0.6191 | 0.6208 | +0.0018 | 3/5 |
| 200 | 0.6185 | 0.6227 | +0.0042 | 5/5 |

19/25 paired wins — weaker than EXP-003's 25/25 despite `top30` leading on
selection. Textbook regression to the mean: part of its selection lead was luck.

**DISCLOSURE — a procedural weakness that must be reported.** Two methods have
now been audited: `rfw` (EXP-003) and `top30` (EXP-005). Each select-then-audit
cycle was individually clean, but the audit set has now informed two decisions.
**Choosing between them on their audit scores would be selection on audit data
and must not be done.** The defensible claim is the weaker, truthful one:
several source-learned representations give roughly +0.002 to +0.007 over
target-only prototypes, and they are not distinguishable at this sample size.

**Decision.** Report both audits and the disclosure. Do not crown a winner.

**Bug found and fixed.** After the artifact schema changed, `reload_test.py`
still applied full 60-feature weighting while reporting PASS — validating a
different method than the one audited. Now asserts 30 dimensions explicitly.
Gate S passes 17/17.

**Ceiling context.** Amsterdam few-shot at 200 shots (0.6227) has essentially
caught Madrid's own full-data CV score (0.6281). That suggests a feature and
label-noise ceiling rather than a modelling gap, and argues against further
tuning. `weighted_mean_year` is an area-weighted average over mixed buildings in
a 30 m pixel, so the labels are intrinsically noisy.

---

## EXP-006 — Season-controlled, coverage-aware, label-free features (v2)

**Status:** smoke/development · **Commit:** `5f4cd4b` · **Owner:** Member 2/3 scope

**Motivation.** All nine representations in EXP-004 landed within 0.011 of each
other around a control of 0.5926. Nine different ways of using Madrid's learning
barely moved the result — the signature of a **feature** bottleneck, not a method
bottleneck.

**Hypothesis.** Three signals the starter discards carry usable information, the
largest being season. Measured directly from the raw data:

| | Madrid | Amsterdam |
|---|---|---|
| Median day-of-year | **175** (late June) | **105** (mid April) |
| June–August share | 48.3% | 20.5% |

A **70-day offset**. Vegetation phenology moves NDVI substantially between those
dates, so part of what a model reads as domain shift is season, not architecture.
The starter never uses `doy`. It also drops `coverage` (building fraction, mean
0.505 Madrid vs 0.421 Amsterdam) and records no observation density.

**Changes.** `candidate/build_features_v2.py` — 94 features: May–Sep
season-controlled spectral statistics, day-of-year summaries, `coverage`
restored, observation-density and gap features, explicit late-minus-early change
magnitudes, and label-free change timing. Vectorised gap-fill runs in **85 s**
against the starter's 13.5 min.

**Structural result — MASTER_PLAN #10 addressed.** `build_features()` never sees
a label; labels are derived separately and joined by pixel key. The same function
would run unchanged on a hidden test set with no label column.

**Bug found and fixed during development.** The observation-density features were
initially all constant: the mask was built from the *interpolated* grid, which has
no NaNs left, so every pixel showed 42 observations. Fixed by adding a
no-interpolate path.

---

## EXP-007 — Does v2 beat v1? **No. Rejected.**

**Status:** smoke/development · **Commit:** `5f4cd4b`

Both feature sets evaluated on the **same pixels in the same episodes**, aligned
by `(px_key, py_key)`, so only the representation differs.

| | selection mean | audit | zero-shot |
|---|---|---|---|
| v1 best (`topk`) | 0.6049 | — | 0.4433 |
| v2 best (`rfw`) | **0.6050** | worse at 4 of 5 budgets, **8/25 wins** | 0.4316 |

**+0.0001 on selection. Nothing.**

**Diagnosis.** The new features are mildly informative but **dilutive**. They hold
**29.1% of RF importance across 38% of the columns** — below average per column.
Best new feature (`NIR_warm_mean`) ranks 8th of 94; `coverage` only 40th. Going
from 60 to 94 dimensions makes prototype estimation noisier, which is why v2
loses most at **5 shots (−0.0166)**.

**This is the same mechanism as EXP-004's whitening result:** in the low-data
regime, extra dimensions cost more in estimation error than they add in signal.
Two independent experiments now point at the same principle.

**Decision.** Per the gate fixed before running, **v1 is kept for the
submission.** The seasonal offset is reported as a measured finding with a
negative test — the hypothesis was well-motivated, correctly tested, and wrong.

---

## EXP-008 — Fresh-episode supporting test

**Status:** smoke/development · **Commit:** `5f4cd4b`

**Why.** The Day-1 audit set had informed two decisions (DEC-012), capping what
could honestly be claimed. EXP-007 required a new episode draw, giving a
legitimate opportunity to test the **already-fixed** v1 method on episodes that
did not exist when it was chosen. Seed **2026**, never used for any selection.

| shots | control | v1_topk | gain | paired wins |
|---|---|---|---|---|
| 5 | 0.4922 | 0.5100 | **+0.0178** | 4/5 |
| 25 | 0.6037 | 0.6082 | +0.0046 | 3/5 |
| 50 | 0.6107 | 0.6117 | +0.0010 | 2/5 |
| 100 | 0.6163 | 0.6194 | +0.0031 | 5/5 |
| 200 | 0.6168 | 0.6204 | +0.0036 | 5/5 |
| | | | | **19/25** |

**This is a fresh-episode supporting comparison, not independent replication**, so it does
not inherit the DEC-012 caveat. Positive at every budget in both runs, and the
5-shot gain is now the largest of the five — the regime the challenge cares most
about.

**Ceiling evidence, now three independent lines:** nine transfer methods within
0.011; two separately built feature sets both plateau near 0.62; Amsterdam
few-shot at 200 shots approaches Madrid's own full-data CV of 0.6281.
**Recommendation: stop optimising.**

---

## EXP-009 — Prototype-shrinkage foundation

**Status:** supporting methodological development. Madrid class offsets are re-centred on the Amsterdam support mean and blended with target support prototypes. `shrinkage.json` stores the selection and audit arrays. This experiment motivates EXP-010 but is not the headline.

`shrinkage_chain.json` is **partially verified**: every `topk` array and each scheduled `shrunk` array exactly matches the corresponding `shrinkage.json` audit array; its `raw` arrays have no second stored trace. Keep the artifact, but do not elevate that chain over EXP-010.

---

## EXP-010 — Frozen primary result: joint dimensionality and shrinkage schedule

**Status:** final audited / scientific freeze · **Authoritative artifact:** `candidate/artifacts/joint_sweep.json`

**Control:** `k=60, lambda=0`. **Tuned schedule:** `k=30, lambda=0.6` at five shots; `k=45, lambda=0` at 25/50/100/200 shots. Selection seed 2026; audit seed 31337.

| shots | tuned | control | gain | wins |
|---:|---:|---:|---:|---:|
| 5 | 0.552428 ± 0.059539 | 0.515220 ± 0.070198 | +0.037208 | 7/10 |
| 25 | 0.612174 ± 0.013057 | 0.608872 ± 0.014539 | +0.003302 | 8/10 |
| 50 | 0.617273 ± 0.007839 | 0.613500 ± 0.008332 | +0.003773 | 10/10 |
| 100 | 0.619513 ± 0.004770 | 0.614502 ± 0.004810 | +0.005011 | 10/10 |
| 200 | 0.623982 ± 0.003646 | 0.618943 ± 0.003824 | +0.005040 | 10/10 |

Arithmetic-only re-aggregation of the stored arrays confirms all means, population standard deviations, gains, per-budget wins, and **45/50** total wins. No model was rerun. The primary claim is:

> Madrid-supervised feature selection combined with budget-dependent prototype shrinkage improves few-shot transfer from Madrid to Amsterdam, with the largest benefit when only 5 labels per class are available. As target labels increase, dimensionality reduction remains beneficial while shrinkage becomes unnecessary.

`final_vs_starter.json` is **partially verified**: its `ours` arrays exactly equal EXP-010 tuned arrays and all arithmetic is reproducible, but its `starter` arrays lack a second existing provenance trace. Therefore 47/50 and 9.7% are not retained.

**Packaging correction:** legacy `stage1_madrid.pkl` is the older top-30 method. A separate `exp010_stage1_madrid.pkl` packages the already-frozen EXP-010 source state and schedule without model fitting; the legacy artifact remains unchanged.

---

## Gate4 final classification

E1 **FALSIFIED**. E2 **INCONCLUSIVE**: +0.004953 at 25 shots did not meet the preregistered +0.0100 threshold. E3 **FALSIFIED** and must not be presented as successful. E3 execution/protocol/serialization checks passed, but the full independent scientific validator stopped at `Original tree dirty` before prediction/metric reconstruction; full independent scientific validation was not obtained.

---

## Open items

| # | Item | Owner |
|---|---|---|
| 1 | scikit-learn version hypothesis untested (EXP-001) | unassigned |
| 5 | v2 features rejected but the label-free builder is unused in the shipped pipeline (EXP-006) | deferred, documented |
| 2 | No experiment reviewed by another member | Team Lead |
| 3 | Gate S reload must be run by someone other than its author | any other member |
| 4 | 244 MB `stage1_rf.joblib` not in git and not backed up | Member 2 |
