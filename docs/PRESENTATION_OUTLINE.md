# Presentation Outline — StatsGeeks

**Status:** Day 1 skeleton. Structure and content agreed; slides not yet built.
**Time limit:** ⚠️ **UNCONFIRMED** — the plan lists this as an open organiser
question. Timings below assume **10 minutes**. Confirm before rehearsing; if it
is 5 minutes, cut slides 4, 8 and 11 first (marked ✂).

**Rubric weighting:** 30 challenge understanding & transfer · 40 originality &
creativity · 30 presentation & collaboration.

**Every member speaks.** Transitions are written in — say them, they are what
makes four speakers read as one talk rather than four.

---

## The spine

The talk has one argument. Everything serves it:

> **The starter code looks like transfer learning but transfers nothing. We
> proved that, built something that does, and measured the difference honestly.**

If a slide does not advance that argument, cut it.

---

## Slide-by-slide

| # | Slide | Speaker | Time | Figure |
|---|---|---|---|---|
| 1 | Abstract | M1 | 0:45 | — |
| 2 | The problem | M1 | 0:45 | — |
| 3 | The data | M2 | 0:50 | — |
| 4 | ✂ Labels are noisy by construction | M2 | 0:40 | — |
| 5 | Reproducing the baseline | M2 | 0:50 | — |
| 6 | The defect nobody had noticed | M2 → M3 | 0:50 | — |
| 7 | What we actually transfer | M3 | 1:00 | — |
| 8 | ✂ Making the comparison fair | M3 | 0:45 | — |
| 9 | Does it work? | M3 | 0:50 | `fig1_learning_curve.png` |
| 10 | What's worth transferring | M3 → M4 | 0:50 | `fig3_method_ablation.png` |
| 11 | ✂ The finding: it depends on the budget | M4 | 0:50 | `fig4_budget_dependence.png` |
| 12 | Reading the numbers honestly | M4 | 0:50 | `fig2_transfer_benefit.png` |
| 13 | Where it still fails | M4 | 0:40 | `fig5_confusion.png` |
| 14 | Limitations | M4 | 0:40 | — |
| 15 | Conclusion | M1 | 0:35 | — |

**Total ≈ 10:00.**

---

## Content per slide

### 1 — Abstract *(M1)*
First slide, **≤150 words**, verbatim from the draft below. Do not paraphrase it
live; read the room, not the slide.

### 2 — The problem *(M1)*
Building age drives retrofit and energy policy; records are incomplete. Classify
the construction era of buildings in a **30 m × 30 m Landsat pixel** into four
classes. Train on **Madrid**, adapt to **Amsterdam** with as few as **5 labelled
examples per class**. Metric: **four-class macro F1**.
→ *"So what are we actually looking at? [M2]"*

### 3 — The data *(M2)*
Six spectral bands, once a year, **1984–2025**. Madrid 76,263 pixels, Amsterdam
25,992. Each pixel becomes a 42-year trajectory summarised into 60 features.
Class 2 is the largest class in both cities. **Say 59, not 60** — see slide 5.

### 4 — ✂ Labels are noisy by construction *(M2)*
`weighted_mean_year` is an **area-weighted average** over whatever buildings fall
in the pixel. A pixel with a 1950s block and a 2010s block gets a class
describing neither. **There is a ceiling below 1.0 and nobody knows where it is.**
Good honesty slide; cut only under time pressure.

### 5 — Reproducing the baseline *(M2)*
Ran the organiser's notebooks unchanged — **zero code edits**. Every non-Random-
Forest result matched to four decimal places. Both RF results did not:
Madrid CV **0.6281 vs 0.6179**, zero-shot **0.4433 vs 0.3427**.
Diagnosed to a scikit-learn version difference; refitting twice gave
**0 of 25,992 predictions differing**, so it is systematic, not noise.
Also found `has_early_data` is **constant** — the feature set is **59 informative,
not 60**.

### 6 — The defect nobody had noticed *(M2 → M3)*
The starter's few-shot path **never uses the Madrid-trained forest.** It computes
Amsterdam prototypes from Amsterdam data alone; Madrid contributes only scaling
constants. Rising F1 with more labels measures an Amsterdam-only method getting
more Amsterdam data.
**And that flaw became our instrument** — because it touches no scikit-learn tree
code, it acted as a control proving the data pipeline was identical, which is how
we isolated the version difference.
→ *"So we built one that actually transfers. [M3]"*

### 7 — What we actually transfer *(M3)*
Four steps: learn a transform **T on Madrid only** → freeze it → push Amsterdam
support and query through T → nearest class prototype from support labels.
**We transfer a metric, not a classifier.** Madrid teaches *which of the 60
measurements matter*; Amsterdam supplies the examples.
**The shipped artifact is 3 KB.** The forest is 244 MB. Everything that transfers
fits in 3 KB.

### 8 — ✂ Making the comparison fair *(M3)*
Episodes **matched** across methods and **nested** across budgets, so a budget
increase adds pixels and changes nothing else. Support indices **stored**, not
regenerated from a seed — we had direct evidence that seeds don't survive
environment changes. Selection on trials 0–4, audit on 5–9.
**Beating zero-shot proves nothing. Beating the target-only control does.**

### 9 — Does it work? *(M3)* · `fig1_learning_curve.png`
Yes, consistently, and by a small margin. Quote the audit table. Say plainly:
*"the lines are close, and that is the honest picture."*

### 10 — What's worth transferring *(M3 → M4)* · `fig3_method_ablation.png`
Nine frozen source representations, same procedure otherwise. Crude beat clever:
importance weighting worked; **rank-3 LDA and the classifier's probability space
both hurt** — they compress 60 dimensions into 3–4 and discard what Amsterdam
needs.
→ *"And then something we didn't expect. [M4]"*

### 11 — ✂ The finding *(M4)* · `fig4_budget_dependence.png`
**The ranking depends on the label budget.** Within-class whitening is
**−0.0218 at 5 shots** and **+0.0090 at 200**. Same transform, opposite verdict.
Whitening amplifies low-variance directions: destructive when 5 points estimate a
prototype, helpful when 200 do. This also explains the LDA failure — rank-3
collapse, not useless supervision.
**This is the originality slide. Protect it in any cut.**

### 12 — Reading the numbers honestly *(M4)* · `fig2_transfer_benefit.png`
The gain is **+0.002 to +0.007** — small. The evidence is **consistency across
matched episodes**, not magnitude. Error bars are **spreads, not confidence
intervals**. Confusion diagonals are **recall, not F1**. Accuracy (0.4496) exceeds
macro F1 (0.4433) on zero-shot, so accuracy would have flattered us.
**Disclose: two methods were audited, so we do not claim one is best.**

### 13 — Where it still fails *(M4)* · `fig5_confusion.png`
Class 2 is hardest — **37% of true Class 2 pixels are predicted Class 1**.
Zero-shot Class 3 recall was 0.19 against precision 0.77: the Madrid model
almost never predicted it, but was usually right when it did.

### 14 — Limitations *(M4)*
1. Features still built label-dependently — could not generate features for an
   unlabelled hidden test set as it stands
2. Scaling fitted before cross-validation — not fold-safe
3. The audit set informed two decisions
4. No independent verification yet *(update if Gate S is done)*
5. Near a ceiling: Amsterdam at 200 shots (0.6227) ≈ Madrid's own full-data CV
   (0.6281)
**No claims of worldwide portability or calibrated confidence.**

### 15 — Conclusion *(M1)*
The starter's transfer learning transferred nothing. We proved it, built a real
one, and measured it honestly. The improvement is small; the method is sound; the
failures are documented. **A number without a mechanism is not a finding.**

---

## Abstract — draft, 148 words

> Building age drives urban retrofit and energy policy, but records are
> incomplete. We classify the construction era of buildings within 30-metre
> Landsat pixels into four classes, training on Madrid and adapting to Amsterdam
> with as few as five labelled examples per class.
>
> The organiser's starter pipeline appears to perform transfer learning but does
> not: its Madrid-trained Random Forest is discarded, and Amsterdam prototypes
> are computed from Amsterdam data alone. We reproduced that baseline exactly,
> then built a method that genuinely reuses Madrid-learned state — a frozen,
> importance-weighted distance metric — and demonstrated its benefit against a
> target-only control on matched, nested episodes.
>
> The gain is small but consistent across every budget. Our main finding is that
> the ranking of source representations depends on the label budget: within-class
> whitening hurts at five shots and helps at two hundred. We report two failed
> approaches and five stated limitations.

---

## Written justification — draft, 297 words

**Model design.** Stage 1 is a 500-tree, class-balanced Random Forest trained
only on Madrid's 76,263 pixels across 60 spectral-trajectory features, with a
fixed seed. We kept the organiser's model and hyperparameters deliberately: our
contribution is the transfer mechanism, and holding the classifier constant makes
the comparison interpretable. From that forest we extract feature importances,
which define a weighted distance metric, and select the 30 most informative
features. That metric — 60 numbers, 3 KB — is the entire transferred artifact.
The forest itself is never needed at adaptation time.

**Transfer strategy.** Adaptation freezes the Madrid metric, projects Amsterdam
support and query pixels into that space, computes class prototypes from support
labels only, and assigns each query pixel its nearest prototype. Query labels
are never used for fitting. Episodes are matched across methods and nested across
budgets, so a budget increase adds pixels and changes nothing else; support
indices are stored rather than regenerated from a seed. Method selection used
trials 0–4; trials 5–9 were sealed and reported once. Critically, our comparison
baseline is target-only prototypes on identical episodes, not zero-shot —
beating zero-shot would demonstrate nothing about transfer.

**F1 interpretation.** Four-class macro F1 rises from 0.5589 at five shots per
class to 0.6227 at two hundred, against a target-only control of 0.5556 to
0.6185. The benefit is +0.002 to +0.007: small, but positive at every budget.
The evidence is consistency across matched episodes rather than magnitude.
Reported standard deviations are spreads across five episodes, not confidence
intervals. Two methods were audited, so we do not claim any single
representation is best. At 200 shots Amsterdam approaches Madrid's own full-data
cross-validated score of 0.6281, suggesting a label-noise ceiling — the labels
are area-weighted averages over mixed buildings — rather than a modelling gap.

---

## Before Thursday

- [ ] Confirm the **time limit** with organisers — currently unknown
- [ ] Confirm justification word limit: **300** (Notebook 1) vs **500** (rubric).
      Drafted to 297 to satisfy both.
- [ ] Build the slides from this outline
- [ ] Gate S run by a member other than its author → update slide 14
- [ ] Timed rehearsal, all four speaking, with the transitions
- [ ] Export **PDF** and confirm it opens offline
- [ ] Backup slides: label derivation, leakage controls, episode sampling,
      the version-drift diagnosis, negative results

## Q&A — who takes what

| Topic | Owner |
|---|---|
| Problem framing, evaluation contract, integration | M1 |
| Data, features, reproducibility, the version difference | M2 |
| Transfer mechanics, episodes, the ablation | M3 |
| Results interpretation, limitations, what we'd do next | M4 |

**If asked something nobody knows: say so.** Do not invent an organiser answer,
a completed experiment, or a generalisation claim. "We didn't test that" is a
better answer than a guess, and it is consistent with everything else in this talk.
