# Experiment Log

Every run, including failures and abandoned attempts. Claims are labelled
**starter reference**, **reproduced reference**, **smoke/development**, or
**final audited**. No entry here is final audited.

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

## Open items

| # | Item | Owner |
|---|---|---|
| 1 | scikit-learn version hypothesis untested (EXP-001) | unassigned |
| 2 | No experiment reviewed by another member | Team Lead |
| 3 | Gate S reload must be run by someone other than its author | any other member |
| 4 | 244 MB `stage1_rf.joblib` not in git and not backed up | Member 2 |
