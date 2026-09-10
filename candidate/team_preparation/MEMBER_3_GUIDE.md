# Member 3 — Evidence, robustness and reproducibility presenter

**Balanced speaking assignment, not a historical authorship claim.** The third remaining team member's identity and personal implementation contributions are not established by the inspected Git/log evidence. The historical “Member 3” log names Ametor covering that scope; it must not be used as proof that the person now assigned this study pack wrote those algorithms.

## 1. Role in the project
Own the evidence story: paired evaluation, uncertainty, Gate4 outcomes, geographic trade-offs, exact replay and honest limits. This is a substantial technical presentation role. You should be able to show why a result is trustworthy within its scope without claiming you personally ran the earlier experiments.

## 2. What you actually contributed, where evidenced
No person-specific code or experiment contribution can be assigned to this third speaker from the records inspected. Do not fill that gap with a fictional implementation biography. The *new assigned responsibility* is studying and presenting the evidence; completion of that learning/rehearsal is not claimed by document generation itself.

Safe wording: **“Our team implemented and recorded the pipeline. My presentation responsibility is explaining its evaluation, reproducibility and limitations.”** If you perform a future review or rehearsal, record it truthfully outside the frozen snapshot; only then claim that action. AI-generated preparation documents are not proof that a human independently validated a model. [S17]

## 3. What you must explain
- Current versus historical score protocols and correct paired controls.
- How 200 trials/budget become 1,000 episodes and 4,000 model prediction arrays.
- Support/query separation and exclusion of the development bank.
- Population SD versus confidence intervals and paired significance.
- Four spatial directions, worst-direction reporting and same-query comparisons.
- E1 falsified, E2 inconclusive, E3 coordinator falsified but independent validation blocked.
- Replay/hash evidence versus independent-city or independent-human evidence.
- Competitor claim versus original-code fallback reproduction versus our own candidate.

## 4. Understand even if another teammate implemented it
Know the entire method at a high level: source prior, target covariance, support RF, source blend and graph; coordinate addition changes local width from 60 to 62. Understand EXP-010's historical compact prototypes and EXP-F's within-support metric. Know what label information is available at each stage. You cannot defend leakage checks without knowing what the estimator actually receives.

## 5. Presentation responsibilities
**Current-research rehearsal plan:** current learning curve, paired gains, spatial trade-off, reproducibility/limitations. Use one table with the exact current comparisons, not a collage of different protocol means.

**Existing fallback deck:** slides 6–7 and 10–12, with 14–17 as qualified backup. Those slides describe EXP-010, not Coordinate_RF. Flag “OFFICIAL 25-SHOT RESULT” as internal audit wording, not organizer scoring. Clarify that “selection/audit sets never overlap” does not mean pixel-disjoint cities or globally separate query populations. Explain later research only after explicitly naming its different protocol.

Handoff to Member 1: “The evidence is reproducible for this fixed-city regime, but the deployment and organizer-deliverable boundaries still matter.”

## 6. Technical talking points
### Pairing
A paired difference uses two model scores on the *same support/query* at the same budget/trial. Current 200-shot Coordinate_RF is compared with ASTRA 0.733037, EXP-010 0.622840 and EXP-F 0.657602. Historical means .735239, .623982 and .658664 are not the current paired controls.

### Statistical scope
Population SD uses ddof=0 across 200 episode scores. The paired bootstrap resamples episode pairs, not supposedly independent pixels. Paired t/Wilcoxon tests and Holm correction concern conditional support-draw variability on one target city. A large paired Cohen dz is not a general city-level effect. At five shots, the coordinate-minus-ASTRA interval includes zero.

### Spatial scope
The four-direction audit uses 10 trials per direction, 200 shots/class and a ten-key buffer. Same-direction methods are paired; random-versus-spatial means have different query geography. Coordinate_RF's four-direction mean and worst directional mean are lower than ASTRA's.

### Reproducibility scope
Existing original fresh-source replay: eight state arrays and 4,000 prediction arrays exact across 1,000 episodes. Publication: saved metric reconstruction, ten diagnostic reference calls, protected-file checks, then isolated archive testing with five inference references and byte-identical rebuilt CSVs. This preparation task does not rerun model fitting. [S12-S16]

## 7. Key numbers to memorize
- Current Coordinate_RF: **.650253 / .687664 / .708436 / .729839 / .749299** at 5/25/50/100/200.
- 200-shot SD **.005716**, gain vs ASTRA **.016262**, **200/200** wins.
- 200-shot gains vs EXP-010 **.126459**, EXP-F **.091697**.
- Five-shot coordinate gain **.000289**, **106/200** wins, not convincing.
- Spatial means **.694216 vs .696672**; worst **.644816 vs .658183**.
- **800** development labels excluded from final queries.
- **1,000 episodes**, **4,000 prediction arrays**; these are not independent datasets.
- Gate4 E2 **+.004953 < +.0100**, despite **10/10** positive 25-shot pairs.

## 8. Likely questions and 9. Model answers
### “Why should we believe 0.7493?”
**Answer:** “It is the average of all 200 saved episodes at 200 shots under a locked protocol. Predictions and confusion/F1 records are preserved, a fresh-source replay matched arrays, and the publication was rebuilt outside the live repository. That supports the stated internal result, not unseen-city superiority.”
**Follow-up:** Give .016262 and 200/200 versus matched ASTRA, then its spatial limitation.

### “How do you know it is not overfitting?”
**Answer:** “We cannot rule out target-population overfitting. The latest choice was locked on a designated bank before final query scoring, but historical ASTRA had audit exposure and the same city is reused. Spatial stress and independent future geography are essential complements to exact replay.”
**Follow-up:** Do not confuse reproducibility with generalization.

### “Did query labels leak?”
**Answer:** “Current model fitting receives support labels, not query truth; the evaluator constructs stratified supports and scores held-out queries. Current development labels are separate and excluded from final queries. Historical target selection feedback and the label-dependent preprocessing membership path remain disclosed.”
**Follow-up:** Explain each use separately; do not answer “we never accessed target labels.”

### “Your spatial performance is worse—why package Coordinate_RF?”
**Answer:** “The development lock selected it before final scoring for the stated random-pixel/full-pool use case. We did not reverse that decision or invent a hybrid after observing the audit. The lower four-direction mean is precisely why we do not claim universal superiority over ASTRA.”
**Follow-up:** A different deployment geography may justify a separately evaluated choice, not a silent score substitution.

### “What exactly happened in Gate4?”
**Answer:** “E1 failed its fixed 25-shot prototype comparison and was independently reconstructed. E2's exact positive gain was .004953, below the required .0100, so its rule said inconclusive. E3 production completed and its coordinator said falsified, but independent validation stopped at `Original tree dirty` before scientific reconstruction.”
**Follow-up:** Older stopped run IDs are historical; don't infer E2 never ran from an earlier FINAL report.

### “Are your p-values valid with overlapping queries?”
**Answer:** “They describe conditional support-sampling comparisons on a fixed target population, not independent-pixel or city-level inference. We resample episode pairs, report effect sizes and Holm-adjusted tests, and explicitly limit the conclusion. They do not erase selection history or spatial dependence.”
**Follow-up:** At five shots, the ASTRA difference is inconclusive under the recorded tests.

### “How do you compare with the competitor?”
**Answer:** “We do not subtract their .7373 claim from our current .749299 and call it paired. Their exact winning config is missing and their protocol differs. Historical ASTRA was near-parity with a separately labelled fallback reproduction on matched 20-draw episodes, not proven superior to the missing winner.”
**Follow-up:** Their locally recorded weighted-smoothing update was real reported progress; no subsequent local breakthrough is demonstrated, and no new remote check occurred.

### “Did you independently verify the model yourself?”
**Answer:** “The repository records software/clean-process verification; I will not claim a personal independent validation run that is not documented. My role here is to explain those checks and their limits accurately.”
**Follow-up:** If you later perform an authorized read-only review, record its exact scope before claiming it.

### “What does the safety archive contain?”
**Answer:** “An immutable EXP-010 presentation/text fallback, strongest audited reference notebooks, minimal matching code/state and manifests. It does not contain the current-method final notebook, because none was found. No sealed evaluation/development data or competitor payload was included.”
**Follow-up:** The intended 13 files verify; seven background directory indexes are excluded from the clean sealed ZIP.

## 10. Follow-ups to rehearse
- Derive class precision/recall/F1 from a 2×2 class-versus-rest count.
- Explain why pooling confusion counts changes weighting compared with averaging episode F1.
- Explain nested-budget dependence and why a support-stratified query complement remains imbalanced.
- Distinguish frozen source hashes from pool/order hashes.
- Explain why 200/200 wins is stronger than a single best episode but weaker than evidence on new cities.
- State which runtime/calibration measurements are unavailable rather than guessing.

## 11. Redirect appropriately
Give the interpretation first, then direct exact covariance-transform implementation questions to Member 2. Direct organizer permission/deadline/submission decisions to Member 1. You own uncertainty, leakage distinctions and spatial evidence; do not redirect those basic concepts merely because another person wrote the evaluator.

## 12. Thirty-second explanation
“My responsibility is to explain what the evidence actually supports. Coordinate_RF improves the matched random-pixel evaluation at 200 shots by 0.016262 over ASTRA, winning all 200 pairs. Saved predictions, exact replay and reconstructed tables support that internal result. But the five-shot coordinate gain is inconclusive, the spatial mean is slightly worse, and the target city was used throughout research. We therefore defend reproducibility and the stated scope, not universal generalization.”

## 13. Two-minute explanation
“Our final evaluation compares four unchanged models on the same support/query draws. At each of five budgets there are 200 trials, making 1,000 episodes and 4,000 prediction arrays. Every final query excludes both the fixed 800-label development bank and its current support set. The coordinate variant was chosen before final query scoring, although the inherited ASTRA recipe had earlier target-audit exposure.

“The main random-pixel result is 0.749299 ±0.005716 macro F1 at 200 shots/class. Against matched ASTRA 0.733037, the gain is 0.016262 and all 200 pairs improve. A paired bootstrap interval is roughly .015856 to .016669. Those are conditional support-sampling statistics on one city. At five shots the added-coordinate gain is only .000289, with 106 wins and an interval including zero.

“The spatial audit is the important counterexample. Four buffered directions give Coordinate_RF .694216 versus ASTRA .696672 on average, and the worst direction is also weaker. We show this rather than selecting the favorable directions.

“Reproducibility evidence includes the existing fresh-source/state replay, exact prediction arrays, reconstruction of all confusion/F1 records and a publication ZIP tested outside the repository with byte-identical rebuilt CSVs. None of that makes it a new-city test or proves a second human reviewed every step. Our honest conclusion is a strong, reproducible internal improvement under explicit full-pool assumptions, with external validation and submission notebook readiness still unresolved.”

## 14. Deep technical explanation
For budget b and trial t, define `d_bt = F1_coordinate_bt - F1_control_bt` on the same query set. A paired analysis removes much between-draw variation that would obscure a small method difference. Population SD of individual scores uses divisor n; Cohen dz uses sample SD of differences and has a different interpretation. Bootstrap confidence intervals resample the paired difference vector; they do not bootstrap every repeated query pixel as if independent. Holm correction controls a family of 15 tested comparisons separately for the chosen t/Wilcoxon families under their assumptions; it does not adjust away historical model search.

The metric reconstruction checks observed predictions against truth after the model boundary, while integrity checks bind immutable code/state to the experiment. Those are distinct from rule eligibility. E3 illustrates why completed prediction production plus a coordinator score cannot be called independently scientifically certified after the validator stops. The snapshot illustrates the analogous packaging distinction: correct hashes do not conjure a missing final-method notebook, and extra unsealed metadata must be disclosed even when the intended payload remains unchanged.

## 15. Common traps
Do not claim personal experiment authorship; do not conflate software replay with a separate human; do not label SD as CI; do not call a confusion diagonal F1; do not compare unpaired historical means; do not claim zero target research exposure; do not say E3 passed full independent validation; do not upgrade E2's verdict; do not describe coordinates as universally robust; do not claim the existing baseline notebooks implement the current headline.
