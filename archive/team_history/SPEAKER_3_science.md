# Speaker 3 — The Science, the Failures, and the Close

**Slides 8–12** · roughly **4 minutes**
Your job: deliver the finding that makes this a piece of science rather than a leaderboard entry, then close honestly.

> **You carry the originality marks — 40 of the 100.** Slide 8 is the intellectual peak of the talk. Slides 10 and 11 are what separate a trustworthy team from a lucky one. Do not treat them as filler.

---

## Slide 8 — The finding *(~90 s)* ← **your key slide**

Set it up as a puzzle:

> "We had two knobs. How many features to keep, and how much to trust Madrid. We swept both, at every label budget, and something clean fell out."

Point at the table:

> "When you have five labels, keep 30 features and trust Madrid 60%. When you have 25 or more, keep 45 features and stop using Madrid entirely."

**Then the meaning:**

> "Less data — lean on the other city, use fewer features. More data — trust your own city, afford more features. Both knobs move in the direction you'd predict if the real problem is *estimation error*, not classification."

**Then the line that matters:**

> "We didn't impose that shape. We swept a grid and that's what came back. It's what shrinkage theory predicts — James–Stein — recovered from the data."

**Optional, if the room is technical:**

> "With five points in 60 dimensions, your estimate of a class centre is almost pure noise. Madrid's estimate comes from 76,000 pixels — it's biased, wrong city, but it's *stable*. Trading a little bias for a lot of variance is the right move, and the data agrees on exactly when to stop."

---

## Slide 9 — What failed *(~50 s)*

> "Three things we tried that didn't work, and they failed for the same reason."

- **Rank-3 LDA** — compresses 60 dimensions to 3. Too much thrown away.
- **The forest's probability space** — 4 dimensions. Worst of the nine methods we tested.
- **94 season-aware features** — we'll come back to this one.

> "All three are the same mistake in opposite directions: too few dimensions, or too many. Which is the same estimation-error story from the previous slide."

---

## Slide 10 — What we're not claiming *(~45 s)*

Deliver this **confidently**, not apologetically. It is a strength.

> "Some things we want to be straight about."

- Gains beyond five shots are about 1.5% — small
- Error bars are spreads across episodes, not confidence intervals
- Confusion-matrix diagonals are recall, not F1
- Accuracy would have flattered us — we report macro F1, which is stricter here
- **We do not compare against the organisers' published numbers**

> "Different episodes, different scikit-learn. Our own run of *their* method gives 0.5038 at five shots against their published 0.5437. Comparing across those would manufacture an improvement. So we don't."

---

## Slide 11 — Limitations *(~45 s)*

Move briskly — five items, one line each. Do not dwell, do not skip.

The two worth a beat:

> "Number three: our shrinkage schedule is five values chosen on five trials. There's real overfitting risk there. What argues against it being noise is that it's monotonic and it agrees with theory — but we'd want more trials to be sure."

> "Number five: we think we're near a ceiling. Three independent lines of evidence point at it, and the labels being area-weighted averages is why."

---

## Slide 12 — Conclusion *(~30 s)*

Three lines, then stop.

> "The starter's transfer transferred nothing. We proved it. We built one that does, and measured it against the right control. Better at every budget, and nearly 10% better where the data is scarcest."

*(pause)*

> "A number without a mechanism isn't a finding. Thank you."

**Then stop talking.** Do not add anything after that line.

---

## If you have 30 seconds less

Compress slide 9 to one sentence. Keep 8, 10, 11, 12 intact.

---

## Questions likely to come to you

**"Isn't your improvement within noise?"**
> At five shots, no — 8 of 10 paired episodes, +9.7% relative. Beyond that the gain is ~1.5% and we're honest that it's small. What makes it credible is that episodes are matched: every method sees identical support draws, so we compare paired differences and episode luck cancels. 47 of 50 paired wins, 10/10 at three budgets.

**"Shrinkage estimators aren't new."**
> Agreed — James–Stein is from 1961. What we contribute is applying it to few-shot domain transfer and showing the optimal shrinkage is budget-dependent, recovered empirically rather than assumed. We're not claiming a new estimator.

**"Your F1 is basically the starter's."**
> On absolute score, close — and we think that's a property of the problem. The labels are area-weighted averages over mixed-age pixels, so there's a ceiling. Three independent lines say we're near it: nine methods within 0.011, two separately built feature sets both plateauing, and Amsterdam few-shot at 200 shots reaching Madrid's own full-data score. What we'd claim is that we know *why* it's hard, and we improve where it counts.

**"Why didn't the seasonal correction work?"** *(likely — it's on a backup slide)*
> The offset is real — 70 days between the cities' median observation dates. But adding 34 features to control for it made the prototypes noisier than the correction was worth. Those features held 29% of the model's importance across 38% of the columns — below average per column. It's the dilution effect again.

**"How do we know you didn't tune on your test set?"**
> Four independent episode seeds. Selection and audit never overlap. We also disclose that two methods were audited on the original set, which is why we don't crown a single best representation there. The headline result was later replicated on episodes that didn't exist when the method was chosen.

**"What would you do next?"**
> Three things: test whether the scikit-learn version really explains the baseline gap — that's still inferred, not measured. Make feature generation label-free end to end so there's a hidden-test path. And get more trials behind the λ schedule.

**"Who did what?"** *(collaboration question — be straight)*
> We lost a member partway through. The remaining three covered the work, and the logs record who did what. It's in our team log and decision register.
