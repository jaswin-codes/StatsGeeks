# Member 3 Log — Modelling Engineer

**Name:** Ametor Humelo Buanyomi *(covering Member 3 scope by Team Lead authorisation, 2026-09-08, after completing Member 2's baseline early. Intended as depth of understanding and a fallback, **not** as a replacement for Member 3's own work.)*
**Role:** Candidate model/adaptation, interface tests, artifact saving/reloading, authorised correctness/transfer changes.

Own this log. Update before lunch, handoffs, and day close. Record hypothesis, configuration, seeds, evidence and limitations for every run. Distinguish authorised candidate work from reference reproduction.

## Daily entry

**Day/date:** Day 1 — 2026-09-08
**Branch/base commit:** `member2-baseline` @ `96435da`
**Current status:** Candidate implemented, searched and audited. **Documentation complete; review, independent verification and backup outstanding.**

### Daily Goals

- [x] Confirm the baseline handoff and feature contract before starting
- [x] Implement a candidate that genuinely consumes Madrid-learned state
- [x] Keep raw target prototypes as the required comparison
- [x] Matched episodes, all five budgets, deterministic seeds
- [x] Save and reload-test Stage 1 state; verify label-free inference
- [x] Record failures as evidence
- [ ] Request Team Lead review via `REVIEW_CHECKLIST.md`
- [ ] Independent Gate S reload by another member
- [ ] Handoff to Member 4 for the presentation

### Completed Tasks

- Confirmed the starting point. **There is no Stage 1 artifact to inherit** — Notebook 4 saves no model, so Madrid-side state had to be trained fresh from the pickle and then frozen. Recorded as a consequence of baseline defect 4.
- Built `candidate/transfer_candidate.py`. Every method is one procedure — freeze transform T learned on Madrid only, take Amsterdam prototypes in T-space from support labels — so only T varies and the comparison is controlled.
- Built a matched, **nested** episode harness with **stored indices**. Nesting verified in code, not assumed.
- Ran EXP-003: `rfw` selected on trials 0–4, audited on 5–9. 25/25 paired wins.
- Built `candidate/search_representations.py`. Eight hypotheses, nine representations, selection trials only.
- Ran EXP-004. Found the budget-dependent ranking (below).
- Ran EXP-005: single final audit of `top30` on the sealed trials.
- Built `candidate/reload_test.py`. Gate S passes 17/17 in a clean interpreter.

### Important Decisions

- **DEC-M3-01.** Candidate work lives in `candidate/`, entirely separate from Member 2's `working/` reference copies. No reference file was modified.
- **DEC-M3-02.** Episode support indices are **stored** (`episodes.npz`), not regenerated from a seed. A seed is a recipe that only reproduces in an identical environment — EXP-001 is direct evidence that this matters.
- **DEC-M3-03.** Budgets are **nested**: the 5-shot support is a prefix subset of the 25-shot support. A budget increase then adds pixels and changes nothing else, so improvements are attributable to data volume rather than draw luck. Accepted cost: the curve's points are correlated and cannot be treated as independent measurements.
- **DEC-M3-04.** The comparison baseline is **target-only prototypes on identical episodes**, not zero-shot. Beating zero-shot would not demonstrate transfer.
- **DEC-M3-05.** The source RF (244 MB) is **excluded from the adaptation artifact**. Adaptation needs only the 60 importance weights and the selected feature subset, so the shipped artifact is 3 KB. The forest is a separate optional file needed solely to reproduce zero-shot.
- **DEC-M3-06 (escalate).** Two methods have now been audited. See the disclosure below — this constrains what the team may claim.

### Problems Encountered

- **Procedural weakness — the audit set has informed two decisions.** `rfw` was selected then audited (EXP-003); later `top30` was selected then audited (EXP-005). Each cycle was individually clean, but **choosing between them on their audit scores would be selection on audit data**, which the rubric penalises as scientific unsoundness. It has not been done. The defensible claim is deliberately the weaker one: *several source-learned representations give roughly +0.002 to +0.007 over target-only prototypes and are not distinguishable at this sample size.*
- **Bug in `reload_test.py`, found and fixed.** After the Stage 1 schema changed, the test still applied full 60-feature weighting while reporting PASS — it was validating a different method than the one audited. It now asserts the 30-dimension transform explicitly. Had this shipped, the "runnable adaptation script" deliverable would not have implemented the reported method.
- **My leading hypothesis was wrong.** I expected prototypes in the Madrid classifier's probability space (`proba`) to be strongest, because it directly targets the observed zero-shot failure (Class 3 recall 0.19). It was the **worst** method tested (2/25 wins, −0.061 mean). Collapsing 60 dimensions to 4 discards information Amsterdam needs.

### AI Prompts Used (one-line summary only)

- Implement a source-learned transfer candidate with matched nested episodes and final-audit separation; allowed files limited to `candidate/`.
- Search source representations under stated hypotheses on selection trials only; audit once.
- Write experiment and member logs from the recorded run outputs.

### Files Modified

- `candidate/transfer_candidate.py`, `candidate/search_representations.py`, `candidate/final_audit.py`, `candidate/reload_test.py` — new.
- `candidate/artifacts/` — `stage1_madrid.pkl` (3 KB), `episodes.npz`, `results.json`, `search_selection.json`, `final_audit.json`. `stage1_rf.joblib` (244 MB) deliberately **not** committed.
- `docs/EXPERIMENT_LOG.md`, `docs/member3_log.md`.
- **Unchanged:** all organiser originals, raw data, and Member 2's `working/` reference copies.

### Evidence Produced

**Final audit, `top30` vs target-only control (trials 5–9, sealed until reported once):**

| shots | control | top30 | benefit | paired wins |
|---|---|---|---|---|
| 5 | 0.5556 ±0.0291 | 0.5589 ±0.0258 | +0.0033 | 4/5 |
| 25 | 0.5956 ±0.0071 | 0.6028 ±0.0112 | +0.0072 | 3/5 |
| 50 | 0.6152 ±0.0039 | 0.6179 ±0.0050 | +0.0026 | 4/5 |
| 100 | 0.6191 ±0.0036 | 0.6208 ±0.0012 | +0.0018 | 3/5 |
| 200 | 0.6185 ±0.0028 | 0.6227 ±0.0027 | +0.0042 | 5/5 |

Standard deviations are spreads across 5 episodes, **not** confidence intervals.

**Main scientific finding — method ranking depends on label budget:**

| method | 5 shots | 200 shots |
|---|---|---|
| `wcw10` (within-class whitening) | −0.0218 | +0.0090 |
| `wcw10_rfw` (whiten then weight) | −0.0131 | +0.0131 |

Whitening amplifies low-variance directions: destructive when 5 points must estimate a prototype, helpful once 200 make the estimate stable. This also explains the LDA failure — LDA failed from rank-3 collapse, not from Madrid's supervision being useless.

**Negative results, kept deliberately:** `lda` 8/25 wins, −0.0056 mean. `proba` 2/25, −0.0611 — the worst method tested.

**Gate S:** 17/17 in a clean interpreter. Artifact reloads, support/query disjoint, inference runs with no query labels present, source state unchanged by adaptation, transform confirmed to be the audited 30-dimension one.

### Next Steps

1. Team Lead review via `REVIEW_CHECKLIST.md`, scope **candidate experiment**.
2. **Another member** must run `python candidate/reload_test.py` — Gate S explicitly requires a different person than the author.
3. Back up `candidate/artifacts/stage1_rf.joblib` (244 MB, not in git).
4. Handoff to Member 4: model design, transfer mechanics, the budget-dependence finding, and the audit disclosure.
5. Not started: the scikit-learn version test that would close EXP-001's open question.

### Reflection

- The starter's worst defect turned out to be the most useful instrument on the project. Because its prototype path never touches the Random Forest, it functioned as a control that isolated the library difference in EXP-001 — and it later became the honest comparison baseline for every candidate. A flaw in the code under test was the thing that made the testing rigorous.
- Two of my three "sophisticated" ideas lost to a crude one. `proba` and `lda` both compress 60 dimensions into 3 or 4 and lose what Amsterdam needs; weighting 60 features by importance keeps everything and just re-ranks it. Worth remembering that in the low-data regime, discarding dimensions is expensive.
- The most valuable output today is probably not the +0.007. It is knowing that the ranking flips with budget, and being able to explain why. A number without a mechanism is not a finding.
- The limitation that must not be dressed up: **the effect is small and two audits have been run.** Anyone reading these tables should see the disclosure alongside them, not after being told a winner.
