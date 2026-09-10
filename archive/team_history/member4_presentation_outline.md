# Presentation Outline — Final Scientific Freeze

**Primary result:** EXP-010. **Safe headline:** 45/50 paired wins.  
No independent replication of EXP-010, universal-superiority, global-generalisation, exact-organiser-reproduction, E3-success, 47/50, or 9.7% claims.

1. **Problem — Madrid → Amsterdam domain shift.** Four building-age classes from 30 m Landsat pixels; macro F1.
2. **Few-shot challenge.** Only 5/25/50/100/200 Amsterdam labels per class; support/query separation.
3. **Baseline.** Target-only prototypes (`k=60, lambda=0`). Explain the baseline discrepancy as a reproducibility limitation: local `0.6281 ± 0.0043 / 0.4433`, organiser-saved `0.6179 ± 0.0043 / 0.3427`, cause unidentified.
4. **Hypothesis.** Prototype estimation error dominates when labels are scarce.
5. **Madrid-supervised feature selection.** Madrid learns feature ranking and weights; the representation is frozen.
6. **Prototype estimation problem.** Amsterdam support labels estimate target prototypes; five samples per class are noisy.
7. **Budget-dependent shrinkage.** Re-centred Madrid class geometry; `k=30, lambda=0.6` at 5, `k=45, lambda=0` thereafter.
8. **EXP-010 main result.** Show tuned/control/gain and **45/50** paired wins from `joint_sweep.json`; deviations are episode spreads.
9. **EXP-008 supporting evidence.** Fresh episodes support the claim that Madrid-learned feature representation can improve target-side few-shot transfer. Do not call it EXP-010 replication.
10. **Failed/negative hypotheses.** EXP-004 whitening reverses with budget; EXP-007 expanded season/coverage representation did not improve v1; Gate4 E1/E3 falsified, E2 inconclusive.
11. **Reproducibility controls.** Exact manifests, RNG binding, support/query isolation, immutable source state, fresh workers/teardown, hashes, protected-state audits, NPZ payload validation, and container-vs-scientific identity. Infrastructure is not scientific superiority.
12. **Limitations.** Two cities; no global claim; no independent EXP-010 replication; schedule selection risk; label-dependent feature build; non-fold-safe scaling; provenance-limited auxiliary comparisons.
13. **Conclusion.** Use the frozen claim verbatim:

> Madrid-supervised feature selection combined with budget-dependent prototype shrinkage improves few-shot transfer from Madrid to Amsterdam, with the largest benefit when only 5 labels per class are available. As target labels increase, dimensionality reduction remains beneficial while shrinkage becomes unnecessary.

14. **Team contributions.** Confirm real names and speaking roles before submission.

## Primary table

| shots | tuned | control | gain | wins |
|---:|---:|---:|---:|---:|
| 5 | 0.552428 ± 0.059539 | 0.515220 ± 0.070198 | +0.037208 | 7/10 |
| 25 | 0.612174 ± 0.013057 | 0.608872 ± 0.014539 | +0.003302 | 8/10 |
| 50 | 0.617273 ± 0.007839 | 0.613500 ± 0.008332 | +0.003773 | 10/10 |
| 100 | 0.619513 ± 0.004770 | 0.614502 ± 0.004810 | +0.005011 | 10/10 |
| 200 | 0.623982 ± 0.003646 | 0.618943 ± 0.003824 | +0.005040 | 10/10 |

## Gate4 note

E1 **FALSIFIED**; E2 **INCONCLUSIVE** (+0.004953 at 25 shots, below +0.0100); E3 **FALSIFIED**. E3's full independent scientific validator stopped at `Original tree dirty` before prediction/metric reconstruction, so do not claim full independent validation.
