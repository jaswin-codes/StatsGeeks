# Tonight revision — high-value facts only

## Problem in three sentences
We classify four construction-era labels for mixed 30 m Landsat pixels, not exact ages for individual buildings. Madrid is the labelled source; Amsterdam is adapted using b labelled support pixels per class. We report macro F1 on other eligible target pixels, with repeated support draws and explicit limits on geographic independence.

## Data and metric
- **76,263 Madrid / 25,992 Amsterdam pixels**, 60 ordered input features, observed annual data 1984–2025.
- Amsterdam class counts: 7,568 / 8,802 / 6,745 / 2,877. Class 2 is largest.
- Oldest boundary differs: Madrid 1960, Amsterdam 1945; later cutpoints 1984/2004.
- Macro F1 = equal mean of four class F1s; F1 = `2TP/(2TP+FP+FN)`.
- Confusion row diagonal = recall, **not** F1. ± below means population SD, **not** CI.

## Method ladder — do not mix models
| Method | Memorize this |
|---|---|
| Reference baseline | Madrid RF for source/zero-shot; target prototype path does not consume supervised RF learning. Local source CV .6281, zero-shot .4433; exact cause of discrepancy from organizer .6179/.3427 remains unresolved. |
| EXP-010 | Source RF importance/ranking + recentered Madrid class geometry; compact target prototypes. k=30, lambda=.6 at 5; k=45, lambda=0 otherwise. Historical 200-shot .623982; 45/50 historical paired wins. |
| EXP-F | Same compact source-ranked space, support prototypes with regularized within-support covariance. Historical 200-shot .658664; five-shot spatial weakness. |
| ASTRA | Contextual source prior + adaptive full-target covariance + support RF + source blend + Gaussian graph. Historical .735239 is not the current paired control. |
| Coordinate_RF | ASTRA with two standardized local coordinate columns: 62 local inputs; source prior still 120. Development-locked research incumbent, not the model in the old deck. |

## Current locked F1 table
200 paired episodes per budget; final queries exclude the fixed 800-label development bank and current support.

| Shots/class | Mean ± population SD | Gain vs matched ASTRA | Wins vs ASTRA |
|---:|---:|---:|---:|
| 5 | **0.650253 ± 0.011246** | +0.000289 | 106/200 |
| 25 | **0.687664 ± 0.012145** | +0.005045 | 171/200 |
| 50 | **0.708436 ± 0.011277** | +0.009213 | 193/200 |
| 100 | **0.729839 ± 0.008802** | +0.013803 | 200/200 |
| 200 | **0.749299 ± 0.005716** | **+0.016262** | **200/200** |

At 200, matched EXP-010=.622840 and EXP-F=.657602; gains **+.126459 / +.091697**. Matched ASTRA=.733037. Do not subtract historical .623982/.658664/.735239 instead.

## Strongest improvement / biggest limitation
**Strongest focused claim:** +.016262 over matched ASTRA at 200, all 200 pairs positive; paired-bootstrap interval about [.015856,.016669]. The larger gain over EXP-010 changes more mechanisms/information privileges and is not a pure coordinate effect.

**Biggest weakness:** no independent city/test; inherited historical audit exposure and extra development labels. Coordinate_RF spatial four-direction mean **.694216 < .696672 ASTRA**; worst direction **.644816 < .658183**. Five-shot coordinate benefit is inconclusive.

## Leakage and reproducibility in one breath
“Current fitting receives source labels or the designated episode support labels; the evaluator uses labels for stratified support construction and scoring. The separate 800-label bank informed development and is excluded from final queries. Historical target-audit selection and label-dependent preprocessing remain disclosed. Exact clean-process replay and saved metrics support the internal result, not new-city independence.”

Existing fresh-source replay: **4,000 prediction arrays / 1,000 episodes**. Publication ZIP: isolated extraction, five reference predictions, byte-identical rebuilt CSVs. No fitting or prediction was rerun in this preparation task.

## Competitor comparison
Latest locally evidenced claim: **.7373 ±.0053**, 200 shots, 20 episodes, commit `cf9af6c`. Winning configuration missing; fallback mechanism reproduction **.736392**, not exact winner reproduction. Historical ASTRA matched-20 result **.737388**, 13/20 wins, near parity—not universal dominance. Current .749299 uses a different protocol. No new remote fetch; no subsequent breakthrough demonstrated in local evidence, not proof of no later progress. No competitor payload is in the safety snapshot.

## Twenty likely judge questions — short answers
1. **What are you predicting?** Four construction-era classes for mixed pixels.
2. **What transfers?** Source ranking/geometry in EXP-010; contextual source prior in the current RF recipe.
3. **How many labels at five shots?** Twenty episode support labels, plus separately disclosed development supervision across research.
4. **Why macro F1?** Equal class weighting with precision/recall balance under imbalance.
5. **Why not accuracy?** Majority classes can flatter it; macro F1 is the stated summary.
6. **Why RF?** Nonlinear tabular learner with actual frozen development/replay evidence, not a universal best-classifier claim.
7. **Why not neural nets/XGBoost?** No validated advantage recorded; do not invent a comparison. Recorded BoostedTrees is sklearn histogram boosting.
8. **What changed in Coordinate_RF?** Two local coordinate columns after the 60-input whitening transform.
9. **Did you use query labels?** Not in current estimator fitting; evaluation/sampling and historical selection uses are disclosed.
10. **Is full-pool use allowed?** It is the transductive research assumption; organizer delivery instructions do not confirm that privilege.
11. **Why believe .7493?** All episodes retained, paired predictions saved, exact replay and metric reconstruction.
12. **Could it still overfit?** Yes to this historically explored city/regime; independent geography is missing.
13. **What happens at five shots?** .650253 overall, but only .000289 better than ASTRA and inconclusive.
14. **Why spatial evaluation?** Random neighbors can make prediction easier than regional extrapolation.
15. **Is spatial performance better?** Not overall versus ASTRA; .694216 vs .696672.
16. **What failed?** 94-feature expansion, E1, E3 production hypothesis; E2 inconclusive under its fixed threshold; some alternatives unselected/blocked.
17. **Did E3 validate?** Production completed; independent scientific reconstruction stopped at `Original tree dirty`.
18. **Did you beat the competitor?** No exact/current paired winning-config comparison is established.
19. **Can the model run elsewhere?** The publication archive passed isolated tested-environment replay; current pool is row-bound, not arbitrary-city inference.
20. **What next?** Complete a consistent final notebook/deck outside the snapshot and obtain an independent evaluation/information contract, not automatic more tuning.

## Ten number-cards everyone must memorize
1. **4 classes; 5/25/50/100/200 shots per class.**
2. **76,263 / 25,992 pixels.**
3. **20 labels at five shots; 800 at 200 shots.**
4. **800 additional fixed development labels**, excluded from final queries.
5. **60 / 120 / 62 dimensions**: raw/local ASTRA, source context, coordinate local head.
6. **0.749299 ±0.005716**, current 200-shot score.
7. **+.016262, 200/200**, matched ASTRA gain and wins.
8. **+.126459 / +.091697**, matched EXP-010 / EXP-F gains at 200.
9. **.694216 vs .696672**, current coordinate/ASTRA spatial means.
10. **1,000 episodes / 4,000 model prediction arrays**, not independent datasets.

## Ten concepts to understand
1. Source versus target domain shift.
2. Support versus query versus development bank.
3. Macro versus per-class F1, precision and recall.
4. Inductive versus transductive information access.
5. Prototype shrinkage versus probability blending.
6. Covariance, whitening and regularization.
7. Pseudo-labels versus true labels.
8. Random-pixel versus geographic generalization.
9. Paired tests/SD/CI and their conditional scope.
10. Byte integrity, computational reproducibility and external validation as separate claims.

## Ten mistakes to avoid
1. Calling .749299 organizer-scored or independent-city performance.
2. Claiming only five total labels, or omitting the development bank.
3. Using historical means as current paired controls.
4. Calling the existing EXP-010 deck a Coordinate_RF deck.
5. Calling a reference notebook the final-method solution.
6. Claiming full-pool permission from a delivery email.
7. Saying no target labels were ever used anywhere in research.
8. Calling E2 successful or E3 fully independently validated.
9. Claiming exact competitor dominance or fabricated personal authorship.
10. Editing/re-zipping the whole frozen safety directory to hide gaps or include background OneNote indexes.

## Immediate submission reality
The clean protected fallback is `candidate/SUBMISSION_SAFETY_SNAPSHOT.zip`; intended 13-file payload and manifest hashes verify. The directory has seven unsealed background OneNote indexes, which were not deleted. Existing presentation/text describe EXP-010; the included notebooks are reference evidence, **not** the missing final-method notebooks. Recipient: **uctstatsgeekssociety@uct.ac.za**. Do not claim the submission is complete or sent.
