# Pixel Prophets — Presentation Guide

**The only active rehearsal guide.** Use [FINAL_SUBMISSION/presentation.pptx](../../FINAL_SUBMISSION/presentation.pptx), its [PDF](../../FINAL_SUBMISSION/presentation.pdf) and the [approved justification](../../FINAL_SUBMISSION/written_explanation/written_justification.txt). This guide follows the actual approved ten-slide order, not earlier EXP-010 or companion decks.

## Overview

- **Competition:** StatsGeeks building-age transfer-learning hackathon; official submission/timing rules remain organizer-dependent.
- **Project:** four construction-era classes from 30 m Landsat pixels; Madrid source → few-label Amsterdam adaptation.
- **Model:** Coordinate-RF (`Coordinate_RF` in frozen files).
- **Final score:** **0.749299 ± 0.005716 macro-F1**, 200 labels/class, 200 paired fixed-city random-pixel episodes. ± is population SD.
- **Duration:** target **9 minutes**, acceptable rehearsal range **8–10 minutes**, excluding Q&A. This is a team rehearsal plan, not a confirmed competition limit.
- **Team:** Pixel Prophets. Three speaking slots follow the member preparation packs. Member 1: Jaswin Chinthala (integration role supported by historical records); Member 2: Ametor Humelo Buanyomi (early implementation/presentation role supported by records); Member 3: identity to confirm. Names/attendance and personal claims require human confirmation. Assignments are speaking responsibilities, not evidence of authorship.

## Evidence map

| ID | Source |
|---|---|
| E1 | [Approved final deck](../../FINAL_SUBMISSION/presentation.pptx), slides numbered 1–10 |
| E2 | [Approved written justification](../../FINAL_SUBMISSION/written_explanation/written_justification.txt) |
| E3 | [Frozen results](../../candidate/reports/RESULTS.md) and [submitted learning curve](../../FINAL_SUBMISSION/results_summary/learning_curve.csv) |
| E4 | [Frozen methods](../../candidate/reports/METHODS.md) and [configuration](../../FINAL_SUBMISSION/model/configuration.json) |
| E5 | [Statistical analysis](../../candidate/reports/STATISTICAL_ANALYSIS.md) and [significance table](../../candidate/tables/significance.md) |
| E6 | [Spatial analysis](../../candidate/reports/SPATIAL_ANALYSIS.md) |
| E7 | [Scientific reproducibility record](../../candidate/reports/REPRODUCIBILITY.md) and [package README](../../FINAL_SUBMISSION/README.md) |
| E8 | [Dataset documentation](../../data/README.md) and [limitations](../methodology/LIMITATIONS.md) |
| E9 | [Submission inventory](../judge/SUBMISSION_INVENTORY.md) and [competition transcript](../building_age_transfer_learning_hackathon.md) |
| E10 | Historical member packs, narrative, Q&A and source notes preserved verbatim in the appendix below; historical facts must not override E1–E9 |

## Approved wording: consistency cautions

The approved PPTX and justification were copied without editorial changes. Rehearse the following qualifications rather than quietly broadening the science:

- Slides 2/4: probability blending is not a guarantee of **calibration**; Random Forest is not immune to overfitting. Say “probability prediction” and “the frozen forest choice has project evidence.”
- Slides 3/10: “no leakage” concerns the current estimator boundary. The evaluator uses labels for sampling/scoring, the separate 800-label bank informed development, and inherited ASTRA has historical audit exposure. Do not say no query-label feedback ever influenced historical research.
- Slides 6/7/10: “best at every budget” is the numerical locked mean among the compared methods, not statistically meaningful superiority at five shots or against all competition entries.
- Slide 6: the displayed bootstrap score interval and population SD are different quantities. Both concern support-sampling variability in the same city, not unseen-city uncertainty.
- Slide 7: confusion-matrix diagonal percentages are recall, not per-class F1; a plausible confusion pattern does not prove a causal age representation.
- Slides 8/9: the recipe is a possible blueprint; deployment in another city has not been validated. “Fully reproducible” refers to the recorded artifact/replay scope, not a new clean installation or raw-data rebuild performed now.
- Old appendix text saying the final notebook is missing, the current deck is EXP-010, or 47/50 wins is not current guidance. The submitted notebook exists, remains frozen, and was not executed here. Historical EXP-010's safe headline is 45/50, not Coordinate-RF's 200/200 matched ASTRA wins.

## Slide ownership and talking points

Each transition below is the recommended exact spoken sentence. Original embedded notes/transitions are preserved in the appendix; these qualified transitions are the active rehearsal version.

### Slide 1 — Classifying building age in a city with almost no local labels
- **Member:** 1. **Timing:** 50 seconds, 0:00–0:50.
- **Talking points:** four era classes; Madrid supplies source learning; Amsterdam supplies 5–200 labels per class; pixels are mixed 30 m units, not individual buildings. Macro-F1 weights classes equally.
- **Transition:** “Here is how information moves from labelled Madrid to a lightly labelled Amsterdam.”
- **Backup explanation:** five shots means twenty support labels in total. The goal is era classification, not exact construction-year estimation. Do not read every slide line.

### Slide 2 — One pipeline, five stages
- **Member:** 2. **Timing:** 55 seconds, 0:50–1:45.
- **Talking points:** data → source prior → local model → blend and smooth → prediction/evaluation. Explain the Madrid-trained prior and support-only local forest. Unlabelled target features and coordinates are used transductively.
- **Transition:** “Before explaining the forest, let us make the data and label-access contract explicit.”
- **Backup explanation:** source context uses 60 original plus 60 neighbourhood features; local inputs are 60 whitened features plus two coordinates. Blended probabilities are not asserted to be calibrated.

### Slide 3 — Two cities, one clean protocol
- **Member:** 1. **Timing:** 60 seconds, 1:45–2:45.
- **Talking points:** common ordered spectral schema; class-balanced support budgets; query excludes current support and the 800-label development bank. Source pseudo-labels are model guesses, not query truth. Disclose historical audit exposure.
- **Transition:** “Under that explicit full-pool contract, these are the three frozen design choices.”
- **Backup explanation:** sampling/scoring machinery can inspect labels; the current predictor receives only support truth. Development supervision is additional to each episode's nominal budget. Distinct roles do not imply independent-city validation.

### Slide 4 — Coordinate-RF: three design choices
- **Member:** 2. **Timing:** 65 seconds, 2:45–3:50.
- **Talking points:** balanced 200-tree local RF; append standardized x/y after spectral whitening; source-prior weight `20/(20+4b)` declines with support budget; nine-neighbour Gaussian smoothing acts on blended probabilities.
- **Transition:** “With the procedure frozen, the comparison uses the same evaluation design at every label budget.”
- **Backup explanation:** source weight is 0.5 at five/class and about 0.02439 at 200/class. Coordinates allow regional splits; smoothing averages neighbouring probabilities. Trees can still overfit; no universal classifier claim.

### Slide 5 — Five budgets, evaluated the same way every time
- **Member:** 3. **Timing:** 45 seconds, 3:50–4:35.
- **Talking points:** 5/25/50/100/200 per class; 200 paired episodes each; same support/query per method; population SD across episodes. Name Coordinate-RF, ASTRA, EXP-F and EXP-010 without mixing historical scores.
- **Transition:** “Those matched episodes give the locked result, rather than a selected best run.”
- **Backup explanation:** 1,000 episodes across budgets are not 1,000 independent cities. Macro-F1 averages four class F1 values; pooling confusion counts is a different aggregation.

### Slide 6 — 0.749299 macro-F1
- **Member:** 3. **Timing:** 65 seconds, 4:35–5:40.
- **Talking points:** exact headline and SD; +0.016262 over matched ASTRA at 200/class, 200/200 wins. Gains over EXP-F/EXP-010 are +0.091697/+0.126459. Numerically top locked means do not establish meaningful five-shot superiority.
- **Transition:** “The learning curve and confusion matrix show both the trend and the kinds of remaining mistakes.”
- **Backup explanation:** ASTRA's matched score is 0.733037, not historical 0.735239. Distinguish mean-score CI, paired-gain CI and population SD. At five shots the paired gain interval includes zero.

### Slide 7 — Consistent gains as labels grow
- **Member:** 3. **Timing:** 60 seconds, 5:40–6:40.
- **Talking points:** score rises from 0.650253 at five/class to 0.749299 at 200/class; 25/class is 0.687664. Explain near-tie at five, increasing higher-budget separation, and adjacent-era confusion.
- **Transition:** “A random-pixel learning curve is not enough to establish geographic generalization.”
- **Backup explanation:** normalized confusion diagonals are recalls. Mixed labels and correlated geography make errors interpretable, but do not establish a known irreducible ceiling or causal spectral mechanism.

### Slide 8 — Where the method is honest about its limits
- **Member:** 3. **Timing:** 65 seconds, 6:40–7:45.
- **Talking points:** four-direction spatial mean 0.694216 versus ASTRA 0.696672; worst 0.644816 versus 0.658183. Pool-bound transduction; one target city; historical audit exposure; organizer permissions unresolved.
- **Transition:** “Within those limits, the value is label efficiency and a traceable, reusable research procedure.”
- **Backup explanation:** spatial and random-pixel tests have different query geography. Coordinates support interpolation but do not guarantee extrapolation. A new pool needs separately authorized preparation/evaluation; never silently reorder rows.

### Slide 9 — Why this is useful beyond one leaderboard score
- **Member:** 2. **Timing:** 40 seconds, 7:45–8:25.
- **Talking points:** label-efficiency trend; frozen configurations, hashes and recorded replay; potential blueprint for similar low-label tasks. Separate recorded reproducibility from present deployment certification.
- **Transition:** “We close with the result, the matched evidence, and the boundary of the claim.”
- **Backup explanation:** no latency, calibration, licensing or production-readiness promise is implied. No model replay, fitting or notebook execution took place in this release synchronization.

### Slide 10 — What to remember about Coordinate-RF
- **Member:** 1. **Timing:** 35 seconds, 8:25–9:00.
- **Talking points:** 0.749299 ± 0.005716; 200/200 matched high-budget wins; current support/query separation with disclosed development history; honest pool-bound scope. Thank the judges and stop.
- **Transition:** “Thank you. We welcome questions on the method, evaluation contract, or limitations.”
- **Backup explanation:** lead with the direct answer, then evidence and limits. Member 1 owns competition/data contract, Member 2 architecture, Member 3 evidence. Speaking roles do not invent implementation credit.

## Transitions

Use the exact transition sentence at the end of each slide section, in order. Speaker handoffs are 1→2 after slide 1, 2→1 after slide 2, 1→2 after slide 3, 2→3 after slide 4, 3→2 after slide 8, and 2→1 after slide 9. The receiving speaker starts immediately with the next slide's first point; no repeated introduction is needed.

## Timing

| Slide | Seconds | Cumulative | Member |
|---|---:|---:|---|
| 1 | 50 | 0:50 | 1 |
| 2 | 55 | 1:45 | 2 |
| 3 | 60 | 2:45 | 1 |
| 4 | 65 | 3:50 | 2 |
| 5 | 45 | 4:35 | 3 |
| 6 | 65 | 5:40 | 3 |
| 7 | 60 | 6:40 | 3 |
| 8 | 65 | 7:45 | 3 |
| 9 | 40 | 8:25 | 2 |
| 10 | 35 | **9:00** | 1 |

Totals: Member 1 2:25; Member 2 2:40; Member 3 3:55. These reflect evidence-heavy slide ownership, not equal authorship. To reach 8:00, trim 10 seconds each from slides 1, 2, 4, 6, 7 and 9. At 10:00, allow that same minute for pauses; never cut the development-bank or spatial caveats. Rehearse offline with the actual PDF/PPTX. Q&A is separate.

## Judge questions

Probability labels below are qualitative rehearsal priorities, not measured frequencies. Answers draw only on the final deck and preserved repository. Each long answer expands the short answer without introducing new experiments.

### Dataset
**Question:** What exactly is an example, and why four classes?

**Short answer:** A 30 m pixel with spectral summaries and a construction-era class, not one building or an exact year.

**Long answer:** The input has 60 ordered spectral features. Madrid has 76,263 pixels and Amsterdam 25,992; multiyear observations span 1984–2025. Mixed-pixel labels can aggregate buildings of different ages. The oldest class boundary differs by city (1960 Madrid, 1945 Amsterdam); the frozen task definition is preserved.

**Evidence:** E8, E2. **Relevant slide:** 1, 3. **Probability:** High.

### Method
**Question:** What knowledge actually transfers from Madrid?

**Short answer:** A source-learned, covariance-aligned probability prior that is blended with the local support forest.

**Long answer:** Contextual source learning uses neighbourhood spectral features and unlabelled target alignment. Source-model pseudo-labels guide conditional alignment, not target query truth. The local forest uses current support labels; the prior weight declines with budget. That is genuine source-state reuse, but it explicitly assumes full-pool target access.

**Evidence:** E2, E4. **Relevant slide:** 2, 4. **Probability:** High.

### Coordinate-RF
**Question:** What distinguishes Coordinate-RF from ASTRA?

**Short answer:** Two standardized local coordinate inputs are appended to the local forest's whitened spectral inputs.

**Long answer:** Local width changes from 60 to 62; the inherited source prior, budget-dependent whitening, forest/blend and smoothing recipe remain the frozen procedure. Coordinate splits give local geography a direct role, unlike smoothing alone. The observed improvement is conditional on this random-pixel/full-pool regime and is not universal.

**Evidence:** E2, E4, E6. **Relevant slide:** 2, 4, 8. **Probability:** High.

### Random Forest
**Question:** Why Random Forest, and can it overfit?

**Short answer:** It models nonlinear tabular interactions and has project evidence; it can still overfit.

**Long answer:** The local head is a balanced 200-tree forest with leaf size 1 and square-root feature subsampling. Very small support sets remain a risk; bagging does not remove target-population selection bias. No validated claim that every neural or boosting alternative is worse exists. Historical histogram boosting is not XGBoost; do not invent a new comparison.

**Evidence:** E4, E10 historical method/Q&A records. **Relevant slide:** 4. **Probability:** High.

### Coordinates
**Question:** Are coordinates leakage, and why help if you already smooth?

**Short answer:** They are supplied covariates, not query truth; their availability must be allowed by the organizer.

**Long answer:** Coordinates permit regional tree splits, while smoothing averages neighbouring probabilities after blending. These are distinct mechanisms. Spatially correlated neighbourhoods can make random-pixel prediction easier, which is why the lower directional spatial scores matter. Calling coordinates covariates does not establish permission or unseen-region generalization.

**Evidence:** E2, E4, E6, E9. **Relevant slide:** 3, 4, 8. **Probability:** High.

### Results
**Question:** What does 0.749299 ± 0.005716 mean, and do you win at five shots?

**Short answer:** Mean macro-F1 and population SD over 200 episodes at 200 labels/class; five-shot superiority over ASTRA is inconclusive.

**Long answer:** The 200-shot paired gain over ASTRA is +0.016262, with all 200 pairs won. Five-shot Coordinate-RF is 0.650253 ± 0.011246, only +0.000289 over ASTRA with 106/200 wins and a paired interval including zero. “Best at every budget” describes the numerical means of these compared locked methods. It is not an independent competition ranking or a CI interpretation of SD.

**Evidence:** E3, E5. **Relevant slide:** 5–7, 10. **Probability:** High.

### Validation
**Question:** Did query labels influence the model, and are episodes independent tests?

**Short answer:** Current fitting receives support truth only; additional development labels and historical audit exposure are disclosed. Episodes reuse one city.

**Long answer:** Final queries exclude the current support and designated 800-label development bank. The evaluator uses truth for balanced sampling and post-prediction scoring. Source pseudo-labels are model predictions. The latest lock predates final query scoring, but inherited ASTRA has audit exposure. Paired tests and episode bootstraps quantify conditional support-sampling variation; they do not create fresh-city evidence or erase selection history.

**Evidence:** E2, E3, E5. **Relevant slide:** 3, 5, 8, 10. **Probability:** High.

### Limitations
**Question:** What is the biggest weakness?

**Short answer:** External validity and the pool-bound inference contract.

**Long answer:** Only one target city is studied, query pixels are spatially correlated, development supervision is additional, and organizer-held-out testing is not claimed. Four-direction spatial mean and worst direction are below ASTRA. Mixed-pixel labels add ambiguity, but no proven accuracy ceiling is asserted. A reproducible internal result is not a production certificate.

**Evidence:** E2, E6, E8. **Relevant slide:** 8. **Probability:** High.

### Generalization
**Question:** Can we use this artifact on another city or reorder Amsterdam rows?

**Short answer:** Not directly. The frozen artifact requires the supplied ordered Amsterdam pool.

**Long answer:** Cached prior/state and coordinate/index relationships are tied to that pool. Another pool requires organizer features, exact feature order, source-fitted scaling and matching coordinates, followed by a separately authorized preparation and evaluation. No new-city score can be inherited from 0.749299. Spatial testing already warns against assuming interpolation transfers to extrapolation.

**Evidence:** E2, E6, E7. **Relevant slide:** 8, 9. **Probability:** High.

### Future work
**Question:** What would you do next?

**Short answer:** Confirm the deployment information contract and evaluate untouched geography before further tuning.

**Long answer:** Useful future directions are an independent-city or spatially separated evaluation, a portable pool/input contract and validation of permitted source-state exports. Those are proposals, not completed experiments. Nothing in this release changes the locked model, evaluation or predictions, and no additional search was authorized.

**Evidence:** E2, E8, E9. **Relevant slide:** 8, 9. **Probability:** High.

### Deployment
**Question:** How can we reproduce or deploy it today?

**Short answer:** Inspect the saved notebook/results and verify package checksums; runtime use requires the documented environment and ordered pool.

**Long answer:** The package includes state, code, configuration, verification inputs and pinned requirements. Its runtime `--verify` and `--support` paths fit support forests; neither was run during this no-execution release. Check actual delivered binaries rather than assuming a Git clone includes ignored assets. New clean installation, operational latency, calibration and redistribution rights are not newly certified.

**Evidence:** E7, E9. **Relevant slide:** 8, 9. **Probability:** Medium.

### Innovation
**Question:** What is original if forests and spatial smoothing already exist?

**Short answer:** The problem-specific integration and conditional evidence, not invention of Random Forest.

**Long answer:** The method combines contextual source transfer, budget-dependent local geometry, coordinate-aware low-label fitting, source blending and probability smoothing. Adding coordinates is a small, interpretable change with a matched high-budget gain and an explicit geographic trade-off. Historical ablations are operational comparisons, not an additive causal decomposition of every component. We do not claim a new universal estimator.

**Evidence:** E2, E3, E4, E6. **Relevant slide:** 2, 4, 9. **Probability:** High.

### Competition
**Question:** Is this an organizer-scored winning result, and who did what?

**Short answer:** It is a locked internal result; eligibility and final upload rules need confirmation. Speaking assignments are not invented authorship.

**Long answer:** Full-pool features, coordinates, the extra development bank and source-export expectations must match the organizer contract. Competitor headlines with different protocols are not paired controls. Historical records support Jaswin's integration work and Ametor's early implementation/presentation work; the third speaker's identity and personal history need confirmation. Team/agent-assisted work must be acknowledged honestly. No email, commit, push or submission was performed by this synchronization.

**Evidence:** E9, E10 member attribution records. **Relevant slide:** 1, 8–10. **Probability:** High.

## Backup discussion

- **Interesting observations:** the coordinate gain grows with label budget; source-prior weight shrinks with budget; high-budget random-pixel gains coexist with a worse spatial mean. A plausible interpretation is stronger local interpolation, not established universal mechanism.
- **Failed ideas:** historical probability compression/LDA and the 94-feature expansion did not become the final method. EXP-F's higher-budget improvement did not remove its five-shot spatial weakness. Gate4 E1 was falsified; E2 was inconclusive (+0.004953 below its +0.0100 practical threshold); E3's coordinator was negative, but independent validation stopped at `Original tree dirty`. Do not call blocked validation a completed scientific replication. These are old records, not experiments run now.
- **Why Coordinate-RF:** the development-locked selection for the stated random-pixel/full-pool regime; no post-audit switch or new hybrid was made.
- **Why RF:** nonlinear tabular interaction modelling with existing project evidence; not proof that all other classifiers fail or that 20 support labels eliminate overfitting risk.
- **Mechanism details:** whitening uses budget-dependent diagonal shrinkage `rho=min(1,60/(4b))`; coordinate standardization is appended after whitening. Covariance rotation is not mere feature rescaling. Gaussian averaging operates on probabilities, followed by argmax; do not alter ordering when explaining the frozen implementation.
- **Limitations:** one explored city, extra research supervision, inherited audit feedback, correlated queries, mixed pixels, pool/order dependence and conditional organizer permission.
- **Future work:** untouched geographic evaluation and a portable permitted input contract; higher-resolution or external data only if authorized, with no promised gain.
- **Common misconceptions:** five shots ≠ five labels total; SD ≠ CI; recall ≠ F1; pseudo-label ≠ ground truth; hash match ≠ organizer approval; software replay ≠ independent human review; existing saved notebook ≠ notebook executed in this release; “no current query-truth fitting” ≠ no historical target-label exposure; EXP-010's prototype `lambda` ≠ Coordinate-RF's probability blend weight.
- **Emergency answer pattern:** claim → evidence → limit → next check. Answer the core point before handing implementation details to Member 2 or uncertainty to Member 3.

## Historical preservation appendix

The appendix below preserves source documents and embedded notes verbatim as text, including superseded claims, slide numbering and old path references. **It is archival, not an alternative script.** Relative links inside archived text are intentionally literal and are resolved from the original source locations, not from this guide. Current guidance above overrides obsolete wording. No scientific evidence or historical seals were rewritten to modernize these notes.

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/MEMBER_1_GUIDE.md</summary>

````````text
# Member 1 — Problem, integration and submission steward

**Speaking-role assignment, not equal-code-credit fiction.** The most defensible identity mapping is Jaswin Chinthala as repository/integration lead, supported by Git history. This assignment does not prove he personally authored every Gate4 or autonomous-model line. If a different person takes this speaking slot, treat the ownership paragraph as team history rather than a first-person claim.

## 1. Role in the project
Own the problem statement, source/target contract, submission safety, study's scope and opening/closing narrative. Keep the team from mixing historical EXP-010 slides with current Coordinate_RF numbers. Be the person who distinguishes technical capability from organizer permission.

## 2. Contributions supported by evidence
Git attributes initial repository/README setup, the integration merge (`fc463e5`), Gate4/documentation integration (`0179d59`) and runtime/verification-framework commit (`7f012bb`) to Jaswin Chinthala. That supports integration/repository stewardship. `docs/member1_log.md` is mostly an unfilled role template and is not evidence of completed personal tasks. Much newer model/publication work is uncommitted and agent-assisted; do not attribute its implementation to an individual solely because it resides in their account's directory.

Safe wording: **“I coordinated the repository/integration role reflected in our history. Our team developed the model and verification pipeline; I will explain the task and the submission/evaluation boundaries.”** Use “I” only if it matches your actual experience. [S16,S17]

## 3. What you should be able to explain
- Why building-era prediction matters and what a mixed satellite pixel represents.
- Madrid source supervision versus Amsterdam support adaptation and query evaluation.
- Four-class macro F1, class imbalance, shots/class versus total support.
- Why beating a source-only zero-shot baseline is not sufficient evidence of transfer.
- Research incumbent versus historical fallback versus final notebook readiness.
- The exact organizer message and what it does **not** authorize.
- The safety snapshot's hash/protection boundary and its clean ZIP.

## 4. Understand even if another teammate implemented it
Know the one-sentence EXP-010, EXP-F, ASTRA and Coordinate_RF descriptions. Know that Coordinate_RF adds two local coordinate columns, not a new neural network. Know the difference between a source prior, support labels, query truth and pseudo-labels. Know that the original source rebuild/4,000-array replay is existing evidence, not work rerun in this preparation task. Know why the current result is conditional on full-pool access and a single target city.

## 5. Presentation responsibilities
**Current-research rehearsal plan:** opening problem/abstract; data/metric slide; closing scope and future validation. Hand to Member 2 with: “The reference target prototype did not use Madrid-supervised knowledge, so our first question was what exactly should transfer.” After Member 3's evidence section, close with the paired gain and spatial limitation together.

**Existing 17-slide fallback:** cover slides 1–4 and 13. Do not introduce Coordinate_RF as the algorithm shown on these slides. If asked about later work, explicitly switch protocol: “That deck is our frozen EXP-010 fallback; our later research package evaluates Coordinate_RF under a different, transductive protocol.” Existing slide 2's “5 labels” shorthand means five/class, twenty total.

Do not send files or claim notebook completion automatically. The operative destination is `uctstatsgeekssociety@uct.ac.za`; the current task did not email it.

## 6. Technical talking points
**Input contract:** 76,263 Madrid and 25,992 Amsterdam pixel vectors, 60 ordered inputs; current local RF appends two coordinates after whitening. The target is four eras, not exact years.

**Information contract:** inference assumes the full ordered unlabelled target pool and coordinates plus the current balanced support labels. A separate fixed 800-label bank informed selection. Organizer email instructions do not settle whether this access is permitted.

**Safety contract:** 13 intended files are immutable and hash-verified. Seven background OneNote indexes appeared after the seal; they were not deleted. The sealed ZIP is clean and protected. This is a fallback with a known notebook gap, not a complete current-model organizer submission.

## 7. Key numbers to memorize
- **4** classes; budgets **5/25/50/100/200 per class**.
- **20** support labels at five shots; **800** at 200, plus **800** separate development labels used in research.
- **0.749299 ±0.005716**, current 200-shot macro F1.
- **+0.016262**, **200/200** wins versus matched ASTRA.
- **0.694216 vs 0.696672**, coordinate/ASTRA spatial four-direction means.
- **45/50**, historical EXP-010 wins; do not attach to Coordinate_RF.
- **13 intended snapshot files**; missing final-method notebook remains the main organizer-delivery gap.

## 8. Likely questions and 9. Model answers
### “What does the hackathon ask you to solve?”
**Answer:** “Transfer building-era classification from labelled Madrid pixels to Amsterdam using small labelled support samples, and explain/evaluate it with macro F1. The current operative submission is presentation, written explanation included in that presentation, and final notebook solutions.”
**Follow-up:** “Is your final notebook present?” — “No valid existing final-method notebook was found. We preserved audited reference notebooks and disclose that they are not the notebook for either headline method.”

### “Why should we trust your team's result?”
**Answer:** “The current locked run has saved paired predictions, exact source/state replay and reconstruction of all 4,000 confusion/F1 records. That supports the internal result. We do not call it an independent-city test.”
**Follow-up:** “Who independently reviewed it?” — “Clean-process/software reconstruction is recorded. That is not a blanket claim of a separate human reviewer.”

### “Did you use Amsterdam labels?”
**Answer:** “Yes: designated support labels for episode fitting and a disclosed development bank for selection. Query truth is for scoring; historical ASTRA selection also used target audit feedback. We separate those uses rather than claiming no target labels were ever read.”
**Follow-up:** Ask Member 3 to detail episode/development exclusions after giving this correct high-level answer.

### “Why is your current model not in the deck?”
**Answer:** “The repository contains a validated later research package but only an older EXP-010 organizer-facing deck. This preparation task froze the strongest existing fallback without fabricating or relabelling a notebook. The gap is documented; we are not claiming the deck already presents Coordinate_RF.”
**Follow-up:** “Can you change the safety copy?” — “No. Any future approved revision must be a separate package outside the immutable snapshot.”

### “Can you use all unlabelled target pixels?”
**Answer:** “That is the research method's explicit transductive assumption. The organizer instruction we have now specifies deliverables, not information-access approval. We need that contract before treating the score as eligible under a future hidden-test protocol.”
**Follow-up:** “What if not?” — “Use a separately qualified inductive model such as the preserved EXP-010 fallback; do not reuse the transductive score.”

### “What was your personal contribution?”
**Answer:** State your actual role, then cite repository/integration commits if applicable. “Our Git history records integration and verification-framework work under my name; the method and evidence are team outputs, including agent-assisted work.”
**Follow-up:** Do not claim authorship of Ametor's EXP-010/presentation commits or undocumented autonomous code.

### “What would you prioritize next?”
**Answer:** “First a consistent final notebook/presentation package and a confirmed inference contract. Scientifically, an untouched geographic/city test matters more than another search over the same Amsterdam audit population.”
**Follow-up:** “Will you optimize tonight?” — “This task does not start or authorize discovery; any later task must preserve all frozen artifacts and use separate outputs.”

### “Is the safety folder a perfect submission fallback?”
**Answer:** “Its intended payload and clean ZIP are verified and write-protected, but it has explicit readiness gaps: the final-method notebook is absent, reference notebook data are external, and the deck is historical. The directory also has seven unsealed background indexes; use the sealed ZIP, not a new whole-folder archive.”
**Follow-up:** “Was anything corrupted?” — “Intended file hashes match. Unsolicited extra files are a directory-membership issue, not changed scientific bytes.”

## 10. Follow-ups to rehearse
- Difference between a labelled development bank and episode support.
- Why the original 0.623982 EXP-010 score is not the current matched 0.622840 control.
- Whether 30 m mixed pixels can identify each building's age.
- Difference between a read-only file, NTFS deny-write permissions and WORM storage.
- How a Git commit and a dirty-worktree artifact manifest identify different things.
- Why exact repeatability is compatible with an unresolved baseline-provenance cause.

## 11. When to redirect
After answering the core point, hand detailed covariance/forest questions to Member 2; exact statistical interpretation, Gate4 run identities and spatial comparisons to Member 3. Say: “The contract-level answer is X; my teammate can give the implementation detail.” Do not redirect the basic label/metric/safety questions you own.

## 12. Thirty-second explanation
“We classify construction eras from satellite pixel histories, learning from Madrid and adapting with a few labelled Amsterdam pixels. Our current research model combines a source prior with a target-support forest and spatial information. It reaches 0.7493 macro F1 at 200 labels per class, with consistent paired gains on random pixels. We also report that it is slightly worse than ASTRA on geographic-half averages. I focus on making the problem, evaluation contract and submission scope clear so those results are not overstated.”

## 13. Two-minute explanation
“Each example is a 30 m pixel, not an individual building, and the four labels summarize construction eras. Madrid supplies 76,263 source pixels; Amsterdam has 25,992 target pixels. An episode gives us a fixed number of support labels per class and asks us to predict other eligible target pixels. Macro F1 gives each class equal weight.

“The reference trained a source forest, but its few-shot prototype path did not actually use the supervised forest. Our early EXP-010 method corrected that information path using source-ranked features and source class geometry. Later work developed a transductive RF recipe using unlabelled target geometry, source probabilities and spatial smoothing. Coordinate_RF adds two local coordinate inputs to that recipe and was locked before final query scoring.

“At 200 shots/class it scores 0.749299 ±0.005716, with a paired gain of 0.016262 over matched ASTRA and 200 wins out of 200 episodes. That is a reproducible internal random-pixel result, not proof of unseen-city performance. The geographic audit shows a small aggregate regression versus ASTRA, and the research also used an extra 800-label development bank.

“Our current organizer-facing fallback remains the older EXP-010 presentation and explanation. We found no final-method notebook, so we did not invent one. The immutable safety ZIP protects the best existing fallback while the missing deliverable and organizer information-access questions remain explicit.”

## 14. Deep technical explanation
The evaluation object is not just a fitted classifier: it is a tuple of input artifact, feature order, eligible population, support sampler, configuration, source/pool state and metric aggregation. Source/target labels play distinct roles. Given a target label vector, the privileged benchmark constructs class-balanced support indices; the predictor receives only selected support labels, while unlabelled pool statistics are allowed under the recorded research assumption. The scorer reads query truth after prediction. Final queries exclude all 800 development indices and each current support set.

This contract explains why passing hashes, reproducing predictions and receiving organizer permission are different tests. A byte-identical result could still violate a future rule that forbids transduction; a statistically positive result could still miss a preregistered practical effect threshold; a safe archive could still lack a requested notebook. Your role is to maintain those distinctions across the talk and submission.

## 15. Common traps
Do not say 0.7493 is organizer-scored; do not claim the baseline notebook implements Coordinate_RF; do not hide the development bank; do not claim exact baseline-version causation; do not infer equal implementation contributions from three speakers; do not promise total immutability against administrators; do not alter the snapshot to resolve a presentation discrepancy; do not let an old “primary result” document silently override the latest research lock.

````````

</details>

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/MEMBER_2_GUIDE.md</summary>

````````text
# Member 2 — Data, transfer mechanisms and model architecture

**Speaking-role assignment with evidence-based attribution.** Ametor Humelo Buanyomi is explicitly named in the baseline/member-3/member-4 logs as covering multiple scopes, and Git records the early model/EXP-010/presentation commits under Ametor Buanyomi. This supports a broad early implementation role, not authorship of all later uncommitted autonomous work.

## 1. Role in the project
Explain how source knowledge reaches the target and why the method evolved from weighted prototypes to covariance-aware prototypes and the current support RF. Own the precise formulas and keep forest counts, feature dimensions and model names straight.

## 2. Contributions supported by evidence
Commit `52c7357` records baseline evidence; `f9dce46` the first source-learned candidate; `96435da` representation search; `5f4cd4b` seasonal-feature investigation/supporting tests; `7faee9f` shrinkage; `c53275c` EXP-010; `1763d9b` presentation/narrative work. Logs explicitly say Ametor covered Member 3 and Member 4 scope by authorization after baseline work and a team departure.

That is defensible evidence of early baseline/model/presentation contributions. It does not establish that you authored every Gate4 infrastructure change, the scaler-shim adaptation on this machine, or the subsequent autonomous ASTRA/Coordinate_RF implementation. Say **“Our team later implemented the RF-based extension; I can explain how it connects to the earlier transfer work.”** Do not convert current understanding into a false implementation claim. [S02,S04,S17]

## 3. What you must explain
- The 60-feature source/target contract and reference preprocessing caveats.
- Why source-only RF and target-only prototypes are distinct paths.
- EXP-010 ranking, square-root importance weighting, source offsets and k/lambda schedule.
- EXP-F residual covariance and why shrinkage stabilizes it.
- ASTRA contextual prior, global/conditional alignment, pool covariance, local RF, blend and graph.
- Coordinate_RF's only local-head change: append x/y standardized coordinates.
- What was rejected and why the evidence does not prove a universal mechanism.

## 4. Understand outside your implementation area
Know exact current results and the geographic counterexample. Know that old “not independently replicated” statements and later clean-process replays refer to different evidence layers. Know the selection bank and episode exclusions; a source-only feature ranking does not mean no target-side research selection occurred. Know that the current safety deck is EXP-010 and no final candidate notebook exists.

## 5. Presentation responsibilities
**Current-research rehearsal plan:** baseline defect/EXP-010 bridge, useful negative experiments, ASTRA mechanism diagram, coordinate change and pre-query lock. Use one clean mechanism diagram rather than a list of every historical experiment.

**Existing fallback deck:** slides 5, 8 and 9; assist with method questions on slides 6–7. Keep the historical claim “five shots is the practical anchor” restricted to EXP-010's comparison; the added-coordinate gain is tiny at five shots. Explain source ranking/geometry clearly before saying lambda switches off above five.

Handoff to Member 3: “That is the frozen procedure and how it was selected. Now the question is what its matched and geographic evaluation actually supports.”

## 6. Technical talking points
### EXP-010
Madrid RF: 500 trees; source importance ranking. Select top k, weight each input by square-root importance. Let source class offsets be `delta_c`, target support mean `m_s`, target support class mean `mu_c`. Prototype: `m_s + lambda*delta_c + (1-lambda)*(mu_c-m_s)`. Nearest squared Euclidean prototype produces the label. k=30/lambda=.6 at 5; k=45/lambda=0 otherwise.

### EXP-F
Same compact source-ranked space. Compute within-support residuals around support class means and pooled covariance. Use inverse of `0.5 C + 0.5 trace(C)/k I + 1e-8 I` for class distances. No unlabelled-pool covariance, coordinate graph or local RF. Better at 25–200 under the reused historical audit, but five-shot spatial regression blocks a simple universal promotion.

### ASTRA and Coordinate_RF
Source prior: 60 raw features + 60 lattice-neighbor means = 120 contextual inputs. Global covariance transport, 200-tree leaf-2 source RF, one pseudo-class alignment/refit, cached target prior. Local geometry: `rho=min(1,60/(4b))`, diagonal-shrunk pool covariance with 1e-7 ridge, symmetric whitening. Local RF: 200 trees, leaf 1, sqrt feature subsampling, balanced weights, seed 42. Source weight: `20/(20+4b)`. One Gaussian step over self +8 neighbors, sigma 1 key unit. Coordinate_RF appends two full-pool-standardized coordinates, making local width 62; original local ASTRA width is 60. [S05,S06,S12,S14]

## 7. Key numbers to memorize
- **500** trees: EXP-010 source importance learning.
- **200** trees: current source/prior/local forests; local leaf **1**, prior leaf **2**.
- **60 / 120 / 62**: original local inputs / contextual source inputs / coordinate local inputs.
- **k=30, lambda=.6** at five; **45,0** otherwise in EXP-010.
- **rho=1** at five; **rho=.075** at 200.
- **alpha=.5** at five; **20/820≈.02439** at 200.
- Current **0.749299 ±.005716**; matched ASTRA gain **.016262**.
- Historical EXP-F **.658664** at 200 versus current matched EXP-F **.657602**: do not mix protocols.

## 8. Likely questions and 9. Model answers
### “What is learned from Madrid?”
**Answer:** “In EXP-010, relevance weights, feature ranking and relative class offsets. In the current RF recipe, a contextual source prior aligned using unlabelled target statistics. Local supervised fitting still uses only the episode support.”
**Follow-up:** “At lambda zero is there still transfer?” — “Yes: source-ranked/weighted representation remains; source prototype shrinkage is only one transfer mechanism.”

### “Why square-root importance weights?”
**Answer:** “Because squared Euclidean distance squares the transformed coordinates, multiplying each feature by square-root importance weights its squared-distance contribution by the importance.”
**Follow-up:** Impurity importance is not a causal feature effect; source relevance can transfer imperfectly.

### “Why does covariance matter if forests are insensitive to scaling?”
**Answer:** “Simple rescaling and covariance rotation are not the same operation. Axis-aligned trees can change when correlated features are mixed by whitening. Our adaptive geometry changes the coordinate frame, not just numeric units.”
**Follow-up:** “Did you isolate every cause?” — “No. Operational ablations differ in information/representation and are not a complete causal decomposition.”

### “Why use diagonal shrinkage?”
**Answer:** “It limits unstable off-diagonal geometry in very small support regimes. The fixed formula depends on 60 dimensions relative to total support 4b. It is not tuned using each final query's labels.”
**Follow-up:** EXP-F instead estimates within-support covariance and shrinks to a trace-matched identity; do not confuse the two rules.

### “Is a pseudo-label another target training label?”
**Answer:** “It is a source-model guess used for class-conditional source alignment, not target ground truth. It may reinforce errors. The exact algorithm checks group size before alignment and does one conditional iteration in the frozen current recipe.”
**Follow-up:** Do not describe two conditional iterations merely because two source forests are fitted.

### “Why does Coordinate_RF need coordinates if ASTRA already smooths spatially?”
**Answer:** “ASTRA's graph averages prediction probabilities and its prior uses neighborhood context. Direct coordinates let the local RF split on regional location in addition to spectra. That is a distinct mechanism and can help random pixels while worsening geographic extrapolation.”
**Follow-up:** Cite the worse four-direction/worst-direction comparisons, then let Member 3 give exact directional numbers.

### “Why not XGBoost or neural networks?”
**Answer:** “The selected recipe has the recorded evidence; no XGBoost or neural advantage is established. A sklearn histogram-boosting alternative was tested and not selected. ExtraTrees was competitive. These facts do not prove all other classifiers inferior.”
**Follow-up:** Never relabel HistGradientBoostingClassifier as XGBoost.

### “What failed, and what did you learn?”
**Answer:** “Source probability compression and LDA often lost useful target structure in early comparisons. The 94-feature branch did not win despite a measured seasonal shift. EXP-F's low-shot spatial regression showed why a higher high-shot random score is insufficient for universal promotion.”
**Follow-up:** “Was dilution the cause?” — “It is an interpretation consistent with some results, not a proven causal explanation.”

### “Did you personally implement Coordinate_RF?”
**Answer:** “The repository supports my early baseline/representation/EXP-010/presentation work. The later work is recorded as team/agent-assisted research; I would not claim personal authorship beyond what is documented. I can explain its equations and evidence.”
**Follow-up:** Understanding a method is an honest presentation contribution even where another member or agent implemented it.

## 10. Follow-ups to prepare
Be ready to derive alpha and rho at five and 200 shots, explain why source context is 120 dimensions, distinguish label-centred residual covariance from pool covariance, and define the local forest's class weighting. Know that exact covariance transport requires numerical regularization and that Gaussian graph weights sum to one per row. Know what is cached versus fitted per episode.

## 11. Redirect appropriately
Member 3 owns statistical assumptions, exact Gate4 verdict nuances, artifact-replay scopes and spatial-table details. Member 1 owns organizer requirements, authorship coordination and submission-readiness decisions. Answer the basic fact before handing off. Do not hand off the architecture or claim that a missing notebook is somebody else's irrelevant problem.

## 12. Thirty-second explanation
“We began with a transfer problem where the reference's few-shot prototypes did not use supervised Madrid knowledge. EXP-010 transferred source feature relevance and class geometry into target prototypes. EXP-F improved the distance metric using regularized support covariance. Our current RF recipe goes further: a contextual source prior, adaptive target geometry, a support-trained forest and spatial averaging. Coordinate_RF adds only two local coordinate inputs to ASTRA, producing a reproducible random-pixel gain but a geographic trade-off.”

## 13. Two-minute explanation
“EXP-010 is intentionally simple. A source RF tells us which spectral features matter in Madrid. We retain a compact subset and weight distances, then estimate Amsterdam support prototypes. When only five labels per class are available, those means are noisy, so we mix them with recentered Madrid class offsets. At higher budgets, target means are better estimated and source prototype shrinkage switches off, while source feature selection remains.

“EXP-F kept that compact representation but replaced Euclidean distance with regularized within-support covariance. It helped at larger budgets, yet had a serious five-shot spatial weakness. This told us not to promote a method just because its best-looking mean improved.

“ASTRA uses a different, explicitly transductive regime. A source prior is built from 120 contextual inputs and aligned to the unlabelled target. The local head sees 60 adaptively whitened features, fits a 200-tree RF on current support labels, blends with the prior and averages neighboring probabilities. Coordinate_RF makes that local head 62-dimensional by adding standardized x and y. Other inherited settings stay fixed.

“The final development-selected coordinate model reaches 0.749299 macro F1 at 200 shots, but the local-coordinate difference at five shots is inconclusive and spatial averages are slightly worse than ASTRA. I would therefore explain it as a conditional random-pixel improvement, not the universally best way to transfer building-age prediction.”

## 14. Deep technical explanation
Distinguish three mathematical objects. First, EXP-010 estimates class means in a fixed source-selected metric; its source offset is a mean-shrinkage target, not a probability vector. Second, EXP-F estimates a within-support residual covariance around class means and inverts its regularized form; the source representation is frozen, but its metric is episode-specific. Third, ASTRA/Coordinate_RF uses full-pool covariance to construct a symmetric whitening transform, followed by nonlinear axis-aligned RF partitions and probability operations.

The contextual prior uses full unlabelled target moments and model-generated partitions. The local head consumes support labels. The source weight depends on 4b, while covariance rho uses 60/(4b). Coordinate_RF appends x/y after whitening rather than whitening a 62×62 joint covariance. The graph averages final blended probabilities, not features or truth labels, and class prediction is argmax afterward. These details matter: silently changing transform ordering, neighbor tie handling, probability aggregation or row order can change predictions even if the prose method seems the same.

## 15. Common traps
Do not call Coordinate_RF 120 local dimensions; do not say its covariance formula uses 62 rather than the frozen 60; do not confuse pseudo-labels with truth; do not say source ranking proves absence of target selection; do not treat the rejected feature branch as current preprocessing; do not claim independent-city validation; do not conflate prototype shrinkage with source-probability blending; do not invent personal implementation credit; do not update any frozen implementation while preparing an explanation.

````````

</details>

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/MEMBER_3_GUIDE.md</summary>

````````text
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

````````

</details>

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/PROJECT_MASTER_GUIDE.md</summary>

````````text
# PROJECT MASTER GUIDE — StatsGeeks

> Team preparation, not a new experiment. Read the evidence-status language as carefully as the scores. This guide distinguishes the current **Coordinate_RF research incumbent**, the historical **ASTRA-AGF comparison**, the **EXP-010 organizer-facing fallback**, and the **reference notebooks**. They are not interchangeable.

## How to study this guide
1. Everybody: sections A, H–K and the numerical ledger; then `TONIGHT_REVISION.md`.
2. Presenter 1: problem, data, evaluation contract and opening/closing. Presenter 2: source transfer, prototypes, covariance and current architecture. Presenter 3: evidence, Gate4, spatial caveats and reproducibility.
3. Everybody: practice the question bank aloud. Give the short answer first; use the deeper answer only when asked. Say what is known, what is inferred, and what was not tested.
4. These are speaking assignments, not invented implementation credits. Exactly three member guides assign balanced coverage. Repository history documents Jaswin Chinthala and Ametor Buanyomi; a third presenter's personal contribution is not established by the records inspected.
5. The snapshot is frozen. Never update its deck or notebook while rehearsing. Draft future organizer revisions outside it under a separate task.

## Evidence map and precedence
All repository paths below are root-relative unless marked external. Bracketed IDs are source citations used throughout the study material.

| ID | Evidence | What it supports |
|---|---|---|
| S01 | `original/1-Introduction.ipynb`; `docs/building_age_transfer_learning_hackathon.md` | Task rationale and earlier organizer context; latest email instruction is supplied in the current task |
| S02 | `docs/member2_log.md`; commit `52c7357` | Original baseline execution narrative; later audits qualify several early causal/provenance claims |
| S03 | `working/member2_baseline_handoff.md`; `docs/member3_baseline_discrepancy_audit.md` | Accepted local scaler-shim artifact, notebook execution, unresolved baseline discrepancy |
| S04 | `docs/EXPERIMENT_LOG.md`; `candidate/artifacts/` | Early EXP-001–010 chronology and stored results; old “primary/ceiling” prose is historical |
| S05 | `candidate/artifacts/joint_sweep.json`; `candidate/exp010_predict.py` | Exact frozen EXP-010 numbers and deployed schedule |
| S06 | `candidate/experiments_2h/SPRINT_REPORT.md` | EXP-A–G controlled sprint, EXP-F positive result and low-shot spatial failure |
| S07 | `working/G4B-E1-001/REPORT.md` | E1 independently verified fixed-specification failure |
| S08 | `working/G4C-E2-008/EXECUTION_REPORT.md` | Latest completed E2; overrides earlier NOT_RUN/stop reports |
| S09 | `working/G4C-E3-002/EXECUTION_REPORT.md` | E3 production completed, coordinator FALSIFIED, independent validation blocked |
| S10 | Own external-quarantine `COMPARABILITY_AUDIT.md`, `FORENSIC_TRACE.md`, `SEARCH_SCOPE_ADDENDUM.md` | Competitor claim versus mechanism reproduction, missing configuration, latest locally evidenced update |
| S11 | `candidate/experiments_2h_v2/README.md`; `FINAL_SELECTION.json`; `final_100.json` | Historical ASTRA-AGF recipe and 100-trial protocol |
| S12 | `candidate/autonomous_runs/20260909_1727/SELECTION_LOCK.json`, `configuration.json`, `FINAL_REPORT.md`, `final_complete.json` | Current development lock, final 200-trial-per-budget results and disclosures |
| S13 | Same run's `spatial_complete.json`; `candidate/reports/SPATIAL_ANALYSIS.md` | Four-direction current geographic trade-off |
| S14 | `candidate/reports/METHODS.md`, `RESULTS.md`, `STATISTICAL_ANALYSIS.md`; `candidate/tables/` | Current publication definitions, conditional statistics and diagnostics |
| S15 | `candidate/reproducibility/final_validation.json`; `candidate/publication/distribution_test_receipt.json`; original `clean_replay/verification.json` | Protected files, exact numerical replay, isolated archive test |
| S16 | `candidate/team_preparation/SNAPSHOT_SEAL.json`, `SNAPSHOT_PROTECTION.json`, `INSPECTION_AND_SUBMISSION_DECISION.md` | Actual fallback contents, hashes, notebook gap and OneNote exception |
| S17 | Git history; `docs/member2_log.md`, `member3_log.md`, `member4_log.md` | Attribution; logs explicitly record one member covering several scopes |

Precedence rule: use specific validated run artifacts over an older “FINAL” filename; use later qualified audits over early confident explanations; use source code for algorithm details; never infer that a new seed means a new city. Earlier reports remain true descriptions of their point in the project, not current recommendations.

## Executive summary: what we can defend
We predict four construction-era classes for 30 m Landsat pixels, using labelled Madrid data and small class-balanced Amsterdam support sets. Our early work transferred Madrid feature relevance and class geometry into target prototypes. Later independently implemented research used a richer local classifier, unlabelled-target covariance, a contextual source prior and geographic smoothing. The current development-locked Coordinate_RF adds two standardized coordinate columns to ASTRA's 60-input local RF, while retaining its prior, adaptive covariance and Gaussian graph.

At 200 shots/class, Coordinate_RF has **0.749299 ± 0.005716 macro F1**, versus matched ASTRA **0.733037**; paired gain **+0.016262**, **200/200 wins**. This is strong conditional support-sampling evidence on the stated random-pixel target population. It is **not** an independent organizer-held-out city/test. At five shots the ASTRA difference is tiny and inconclusive. On spatial separation the coordinate model's four-direction mean is **worse**, 0.694216 versus 0.696672, and the worst direction is also worse.

Operational warning: the existing 17-slide presentation and written justification still describe EXP-010. No final candidate notebook exists in the inspected repository. The sealed fallback preserves that older coherent pair and explicitly labelled reference notebooks; it must not be sold as a complete current-model submission. [S05, S12–S16]

## Chronological reconstruction — do not confuse parallel branches with a single run

| Recorded period / milestone | What the evidence says | Source / caution |
|---|---|---|
| 8 September 2026 | Repository setup, reference preprocessing/modelling and the first source-learned candidate were recorded. | Git `165fe11`, `52c7357`, `f9dce46`; later local audits qualify historical input/version claims. |
| 8 September 2026 | Representation search, audit disclosure, reload checks and first presentation drafts followed. | `96435da`, `b6615dc`, `115e294`, `177f11c`; separate commit and execution clocks are not interchangeable. |
| 9 September, early development commits | Season/coverage features and fresh-draw support tests, then prototype shrinkage and joint k/lambda development. | `5f4cd4b`, `7faee9f`, `c53275c`; EXP-010 commit recorded 10:37:31 +02:00. |
| Parallel Gate4 line, before/around integration | Fixed E1/E2/E3 evaluations accumulated alongside infrastructure/provenance work. | E3-002 records 08:50:21–09:52:00 UTC; this overlaps the other branch's morning work, not a clean sequential experiment ladder. |
| 9 September integration | Baseline branch merge, documentation and Gate4 framework were committed. | `fc463e5`, `0179d59`, HEAD `7f012bb`; later autonomous artifacts remain uncommitted worktree evidence. |
| Later 9 September controlled sprint | EXP-A–F completed; EXP-G blocked; EXP-F retained for review without changing the EXP-010 presentation. | `experiments_2h/SPRINT_REPORT.md`; exact run identities, not guessed wall-clock ordering. |
| 9 September forensic / ASTRA research | Locally recorded competitor weighted-smoothing update, separate mechanism audit, independently implemented ASTRA and its locked 100-trial evaluation. | Competitor commit `cf9af6c` 14:23:35 +02:00; historical ASTRA evidence remains a different protocol. |
| Current autonomous lock | Coordinate_RF chosen under the support-development rule; lock records 2026-09-09 17:50:37 without an explicit timezone. Final query scoring followed the lock. | `autonomous_runs/20260909_1727/SELECTION_LOCK.json`; do not convert an unspecified local timestamp to UTC by assumption. |
| 9 September 18:39:47 UTC | Final publication ZIP sealed, later independently extracted for inference/evidence replay. | Existing distribution receipt; no model optimization in publication. |
| 9 September 19:08:50 UTC | This task created the pre-overnight fallback seal, then team-preparation guides. | `SNAPSHOT_SEAL.json`; no new model fitting/predictions; final-method notebook gap disclosed. |

The story below is organized by mechanisms so it can be presented coherently. That organization must not be mistaken for proof that all development, Gate4 and integration work happened serially or was personally implemented by one speaker.

## A. Problem definition
### What building-age prediction means
The target is a categorical construction-era label, not an exact year or a prediction for each individual roof. Each observation is a roughly 30 m satellite pixel, which can contain buildings from several periods plus vegetation, roads or water. A weighted mean construction year is converted into one of four city-specific classes. A mixed pixel's assigned class can summarize a collection of buildings rather than identify any one building exactly.

Building-age information can inform retrofit planning, energy-use understanding and urban development analysis where records are incomplete. This motivation is not evidence that the model is deployment-ready or fair across neighborhoods. The study is a benchmark on the supplied data. [S01, S03]

### Source city versus target city
Madrid is the labelled **source**: it supplies learning that should help elsewhere. Amsterdam is the **target**: an episode supplies only a small labelled support sample, and predictions are evaluated on other eligible pixels. Both cities have labels in the research data, but availability in a file is not permission to give them all to the estimator.

Different architecture, historical class cutoffs, land cover, sampling season and observation distributions create domain shift. A rule learned in Madrid may assign Amsterdam pixels incorrectly even if it performs well within Madrid. The project therefore needs adaptation, not merely a source score. [S01–S04]

### Why transfer and few-shot learning
Transfer means Madrid-supervised information actually enters Amsterdam prediction. Few-shot means each episode has b labels/class, for b in {5,25,50,100,200}; with four classes, total labelled support is 4b. Five shots means **20**, not five, target labels. Two hundred shots means **800**, not 200 total. The current method additionally used an **800-label fixed development bank** during research selection. That is separate supervision and must be disclosed rather than hidden behind the episode budget. [S12]

### Metric in plain language and equations
For a class, precision asks how often a predicted label is right; recall asks how many true members are found. F1 is their harmonic mean, `2TP/(2TP+FP+FN)`. Macro F1 averages the four class F1 values equally. It avoids letting the largest class dominate the summary as much as raw accuracy would, although it does not itself remove class imbalance or spatial dependence.

A row-normalized confusion diagonal is **recall**, not F1. The mean of episode macro F1 is not generally equal to macro F1 computed from one pooled confusion matrix. Population SD describes how scores vary across the episode draws; it is not automatically a confidence interval for an unknown-city performance mean. [S14]

## B. Starting point: what the baseline actually did
### Data and preprocessing
The accepted artifact has 76,263 Madrid pixels and 25,992 Amsterdam pixels, each with 60 ordered features. The raw panels contain roughly 3.17 million and 1.06 million pixel-year rows; these must not be called millions of independent buildings. Locally observed years are 1984–2025, 42 distinct years, despite earlier explanatory text saying 1984–2024.

The reference workflow selects QA-valid annual band values from available observation slots, screens extreme blue-band haze, interpolates missing annual observations, forms five spectral indices, aggregates temporal statistics and applies Madrid-fitted standardization. Six base bands are Blue, Green, Red, NIR, SWIR1 and SWIR2. The 60-column contract includes overall, early/late, annual-change and availability features. One availability column is constant in the observed data; “60 inputs” is the interface width, not a proof of 60 useful independent signals. Do not say the other 59 are all established as informative.

Class counts in Amsterdam are 7,568 / 8,802 / 6,745 / 2,877 for classes 1–4. Madrid counts are 13,794 / 27,152 / 18,672 / 16,645. Class 2 is the largest in both cities. Madrid's oldest-class division is 1960, Amsterdam's 1945, with later cutpoints 1984 and 2004. Exact boundary inclusion follows code, not casual interval notation. [S02, S03]

### Source RF, zero-shot and target-only prototypes
Notebook 4 trains a class-balanced 500-tree Random Forest on Madrid, evaluates repeated Madrid CV, and applies the source model directly to Amsterdam for zero-shot context. But its few-shot prototype path does **not** consume the trained RF. It computes Amsterdam support class means and uses nearest Euclidean distance. Madrid contributes scaling but not supervised feature relevance or learned class structure to that path. This is why a target-only prototype is the right equal-support control; outperforming zero-shot alone would not prove transfer.

Organizer-saved Madrid CV is **0.6179 ± 0.0043**, with Amsterdam zero-shot **0.3427**. Measured local reference-protocol values are **0.6281 ± 0.0043** and **0.4433**. The local prototype curve matches the saved reference at displayed precision: 0.5437 at five shots and about 0.6150 at 200, with intermediate 0.5986/0.6079/0.6129 at 25/50/100. These are a different episode protocol from the later EXP-010 and Coordinate_RF evaluations.

Early logs attributed the RF discrepancy too confidently to package versions. The later discrepancy audit says the precise cause is **not identifiable** from available historical input/package provenance. Stable repeated numbers in some early records are not sufficient to establish source/input equivalence on the later local shim artifact. Do not tell a judge “we proved it was sklearn.” [S02–S04]

### Baseline weaknesses worth understanding
- Label-dependent feature construction filters/groups using class metadata. This creates an unavailable-label deployment-path problem even though `age_class` is not an RF input column.
- Madrid scaling occurred before CV folds, so the reference CV preprocessing is not fold-safe.
- The reference notebook saved no deployable source RF or adaptation state by itself; recoverability needed separate work.
- Support draws were not stored/nested by the original starter in the way later matched candidate episodes were.
- Fine-grained building/parcel IDs were unavailable for a building-disjoint geographic audit.
- A plateau near 0.62 in the early prototype family was once interpreted as a possible ceiling. Later stronger transductive methods disprove treating **0.62 as a universal ceiling**. The early statement is a hypothesis that did not survive broader evidence. [S03, S04, S11, S12]

## C. EXP-010: how the frozen fallback was built
### Early representation work
Commit `f9dce46` introduced source-learned representations and matched episodes. `rfw` weighted inputs by square-root Madrid RF importance; initial audit gains were small but consistently positive. Subsequent representation search compared compact feature selection, within-class whitening, source probability/logit embeddings, LDA and RF-related representations. This did not establish that every sophisticated method was superior: a probability-space representation lost about 0.0611 mean macro F1 on the recorded selection comparison and won only 2/25 pairs. Compressing to source class outputs may discard target-relevant distinctions; that is a plausible interpretation, not a general theorem against dimensionality reduction.

Whitening showed budget dependence: `wcw10` changed from roughly −0.0218 at five shots to +0.0090 at 200 in the recorded comparison; whitening-plus-RF-weighting changed from −0.0131 to +0.0131. Small support sets make geometry/prototype estimation fragile. Another top-30 audit returned 19/25 wins, less than its selection promise. Repeated audit exposure was disclosed rather than treated as a pristine test. [S04]

### EXP-006–008 and the rejected feature expansion
A 94-feature seasonal/coverage branch measured median acquisition days 175 in Madrid versus 105 in Amsterdam—a 70-day difference. Its label-free builder separated label derivation from feature construction, an engineering improvement. But the broader feature set did not reliably improve F1: about +0.0001 selection mean and 8/25 audit wins, worse at four of five budgets. It was not adopted. “Feature dilution” is a possible mechanism; the outcome alone does not prove that causal account.

EXP-008 provided a fresh-episode supporting test of a fixed earlier representation, 19/25 wins. Those are fresh draws from the same target population, not a new city or exact independent replication of EXP-010, which was developed afterward. [S04]

### EXP-009 and EXP-010 mechanics
A source RF learns a feature ranking/importance vector on Madrid. Inputs are weighted by square-root feature importance so squared distances weight by the importance itself. The target support mean recenters source class offsets, helping separate transferable *relative class geometry* from an absolute city location shift.

Let `delta_c` be Madrid class-c mean minus Madrid overall mean in the selected weighted space. Let `m_s` be the Amsterdam support mean and `mu_c` its support class mean. The EXP-010 prototype is `m_s + lambda*delta_c + (1-lambda)*(mu_c-m_s)`. Predictions use squared Euclidean distance to these prototypes. At lambda zero this reduces to support-only class means—but the representation still transfers Madrid-supervised ranking/weights.

The frozen schedule is **k=30, lambda=0.6 at five shots** and **k=45, lambda=0 otherwise**. The RF has 500 trees at source learning; it is **not** a 500-tree local target classifier in EXP-010. Its small 6,221-byte adaptation artifact stores learned summaries, not the original full forest. The different legacy `stage1_madrid.pkl` must not be substituted. [S05]

### Exact historical EXP-010 result
Ten seed-31337 audit episodes/budget, mean ± population SD:

| Shots/class | EXP-010 | Matched full-feature target-only control | Gain | Wins |
|---:|---:|---:|---:|---:|
| 5 | 0.552428 ± 0.059539 | 0.515220 ± 0.070198 | +0.037208 | 7/10 |
| 25 | 0.612174 ± 0.013057 | 0.608872 ± 0.014539 | +0.003302 | 8/10 |
| 50 | 0.617273 ± 0.007839 | 0.613500 ± 0.008332 | +0.003773 | 10/10 |
| 100 | 0.619513 ± 0.004770 | 0.614502 ± 0.004810 | +0.005011 | 10/10 |
| 200 | 0.623982 ± 0.003646 | 0.618943 ± 0.003824 | +0.005040 | 10/10 |

Safe historical headline: **45/50 paired wins**. Do not use the provenance-limited “47/50” or “9.7%” comparison. Five selection trials and repeated target exposure limit selection claims; separate seed values do not make query pixels independent. Freezing protected a reproducible known result against more speculative changes and gave the team an explainable fallback. Later research did not retroactively change those arrays. [S04, S05]

## D. EXP-F and controlled alternatives
The first controlled sprint kept EXP-010 rather than automatically promoting its highest scoring new arm. EXP-A compared fixed source/local combinations; EXP-B crossed dimensions and shrinkage; EXP-C diagnosed class errors; EXP-D used spatial separation; EXP-E examined three temporal contrasts; EXP-F changed the support distance metric; EXP-G was blocked because full-pool privileges were not explicitly confirmed at that stage. Do not describe a blocked experiment as a failed model.

EXP-F uses compact Madrid-ranked/weighted inputs, support class means and a pooled within-support residual covariance `C=R.T R/(4b-4)`. Its inverse metric is based on `0.5 C + 0.5 trace(C)/k I + 1e-8 I`. This regularizes noisy correlations toward an isotropic distance. It does not use query-pool covariance or train a new local RF.

Historical reused-audit EXP-F at 200 shots: **0.658664 ± 0.004417**, gain +0.034681 over paired EXP-010, 10/10 wins. At 25: **0.638010 ± 0.014197**, gain +0.025835, 10/10 wins. But at five-shot spatial evaluation it scored **0.507618**, losing **0.025769** to the matched EXP-010 control. Its better random-pixel high-shot mean was therefore not a defensible all-budget promotion on its own. No new EXP-010-at-five/EXP-F-elsewhere hybrid was validated from that report. [S06]

Concrete lessons: correlation-aware metrics can help; diagonal-only normalization is not equivalent; low-shot covariance is unstable; source blending is not uniformly beneficial; class diagnostics guide interpretation, not permission to fit post-hoc class thresholds. The most difficult classes under one early low-shot protocol were not necessarily the same bottleneck under every later classifier.

## E. Gate4: experimental discipline, not a winning model name
### What the gates were for
Gate4 sought trustworthy fixed-specification tests with frozen episode manifests, constrained worker information, separate privileged scoring, immutable source state, exact hashes and clean-process teardown. These controls answer “was this exact experiment run under its stated boundary?” They do not answer “is this model superior?”

Different stopped/preflight identities remain in the tree. A filename like `G4C-FINAL-REPORT.md` reports an earlier NOT_RUN stop and must not override the later completed E2-008/E3-002 reports. Ten shots appears here as an extra diagnostic budget: 60 episodes means 10 trials at **six**, not five, budgets. [S07–S09]

### E1 — source within-class covariance geometry
E1 used 59 source-nonconstant dimensions and a fixed class-balanced within-class covariance shrunk as `0.9 W + 0.1 trace(W)/d I`. U0 was a total-source-covariance control; raw P0 and same-query frozen RF were retained. At the predeclared primary 25 shots, E1 scored **0.59008 ± 0.03214** versus raw **0.59860 ± 0.01764**, gain **−0.00852** and 4/10 positive pairs. It failed the +0.0100 threshold and class-regression safeguards despite beating the source zero-shot control. **FALSIFIED for that fixed specification**, independently reconstructed. High-shot gains could not move the goalposts. [S07]

### E2 — restrained source Fisher feature weighting
E2 estimated per-feature between-class/within-class variance ratios on Madrid, normalized/clipped them and mixed with identity weighting. Its fixed epsilon was 1e-6, clip [0.25,4.0], identity mixture 0.5. It classified by weighted support-prototype distances, not a target RF.

The latest complete identity E2-008 scored **0.603550 ± 0.015364** at 25 shots versus raw **0.598598 ± 0.017637**: **+0.004953**, 10/10 positive pairs and no mean per-class regression. That failed the preregistered **+0.0100** mean-gain requirement. Verdict: **INCONCLUSIVE / does not meet the success criterion**, not “promising” and not proof of a zero effect. Independent exact reconstruction passed all 60 records. A verifier-only advanced-indexing fix did not rerun or alter candidate predictions. [S08]

### E3 — target-support translation toward frozen source RF geometry
E3 computed source class means and a fixed support-derived translation on 58 continuous coordinates, leaving the two availability indicators unchanged, then used the frozen source RF. Production completed all 60 episodes. At 25 shots its coordinator reported **0.509079 ± 0.020012**, raw **0.598598**, delta **−0.089519**; all ten raw comparisons lost and class 1 suffered severely.

The frozen coordinator's verdict is **FALSIFIED**, but independent scientific validation stopped at **`Original tree dirty` before prediction/metric reconstruction**. Do not say “E3 was fully independently verified,” and do not claim the score itself was caused by an integrity failure. Execution/protocol/serialization checks and scientific reconstruction are separate layers. This is a negative production result with incomplete independent certification. E4/E5 were not subsequently run in the cited path. [S09]

### What survived Gate4
Useful outputs were not winning parameters: manifest binding, explicit class order, same-query controls, worker teardown, packet/hash checks, distinction between NPZ container bytes and array identity, and respect for stop conditions. A successful infrastructure certificate is not scientific superiority; a failed integrity gate is not automatically corruption of protected model bytes. The careful vocabulary protected the project from overstating its evidence.

## F. Competitor forensics: learn the comparison boundary, not a copied solution
### What is actually evidenced
Our own forensic audits identify the latest **locally evidenced** competitor branch commit as `cf9af6cffea292af9460bf572de33c32a10212d9`, dated 2026-09-09 14:23:35 +02:00. No remote fetch occurred in this preparation task. Therefore “latest” means latest recorded local evidence—not a live claim about what the other team has done since.

The recorded competitor progression was approximately **0.717 unsmoothed**, then **0.7259 ± 0.0049** with uniform smoothing, then a final claimed **0.7373 ± 0.0053** at **200 shots/class, 20 episodes** after distance weighting. The last update is a real reported improvement over the earlier uniform smoother; it would be inaccurate to say nothing changed. But there is **no locally demonstrated subsequent breakthrough beyond that claim**, and exact tuned-config reproducibility remains unresolved. [S10]

### Why headline subtraction is misleading
Frozen EXP-010 used 10 nested seed-31337 episodes and compact source-ranked features, without full-pool fitting. The competitor used 20 seed-42 draws with RNG reset per budget, support-complement queries, a different feature representation, full-target distribution information, pseudo-label alignment and spatial smoothing. The headline evaluates the full target population including earlier tuning regions; it is not an untouched half-test score. Same city, class labels, budget and metric are necessary but insufficient conditions for a fair paired comparison.

The reported winning `overnight_best.json` was missing from searched sources. A broad user-profile search timed out; that is limited search evidence, not proof the file exists nowhere. Our historical isolated original-code **fallback mechanism reproduction** reached **0.736392 ± 0.004722** using 108 features and a documented fallback configuration, not the unrecovered tuned winner. The literal 60-feature fallback already reached about **0.735655** at 200, so “48 extra features explain all of 0.73” is unsupported. Exact original raw-file provenance was also incomplete. [S10]

### What our comparison established—and what it did not
Historical ASTRA on the same 20-draw convention scored **0.737388** versus the reproduced fallback **0.736392**, a **+0.000995** mean difference and **13/20 wins**. It was worse at 5, 50 and 100 on that comparison. This is near parity at high shot count, not universal competitor dominance or an exact comparison to the missing tuned model.

Current Coordinate_RF's 0.749299 comes from a **different** 200-trial protocol excluding the development bank. Do not subtract 0.7373 and call the result a paired competitive advantage. We can discuss the method's own matched controls without needing a competition leaderboard claim. [S10–S12]

### What was learned and what was not copied
The investigation pointed to information regime, local nonlinear capacity, covariance geometry, pseudo-labelled source alignment and spatial processing as important mechanisms. Our subsequent candidate implementation uses the repository's own 60 inputs, a 120-input contextual source prior, one conditional alignment iteration, 200-tree forests, a dimension/support-ratio covariance schedule and Gaussian graph weights. It does not import the competitor implementation, reproduce its 108-feature list verbatim, or claim its unavailable tuned configuration.

Be honest about mechanism inspiration: **“independently implemented” does not mean “we never inspected another method.”** Historical forensic execution of original competitor code was separately recorded and quarantined. It is not part of our model implementation, current publication evidence or safety snapshot. No competitor figures, documentation, workflows, source code, predictions or data were copied into the organizer fallback. Absolute originality cannot be proved by a filename scan; the claim rests on reviewed own-source implementations and preserved provenance. [S10, S12, S16]

## G. ASTRA-AGF in three levels
### Ten-second explanation
“We adapted both the decision rule and the feature geometry to the target, reused a source prior, and averaged predictions locally without using query truth.”

### Plain-language stages
1. **Source prior:** use Madrid labels to provide an informed initial probability over the four target classes.
2. **Target geometry:** estimate how the unlabelled target features vary together so distances/axes are less dominated by redundant features.
3. **Budget adaptivity:** at tiny support counts, stay close to diagonal scaling; at larger counts permit more covariance structure.
4. **Support RF:** learn nonlinear target class boundaries from the current support labels rather than forcing every class into one prototype.
5. **Blend:** trust the source more when support is scarce and progressively less as support grows.
6. **Spatial smoothing:** aggregate neighboring predicted probabilities using coordinates; never clamp query labels or use ground-truth spatial anchors.

### Exact inherited recipe
Recover raw units from the saved scaler. Concatenate 60 raw features with their available 3×3 lattice-neighbour averages, yielding 120 contextual source-prior features. Globally transport source mean/covariance to the target, fit a balanced 200-tree RF with leaf size 2, pseudo-label target rows, then perform one class-conditional alignment/refit where the target pseudo-class is sufficiently populated. The resulting target prior is cached.

For b shots/class, local covariance shrinkage is `rho=min(1,60/(4b))`; use `(1-rho)C + rho diag(C) + 1e-7 I` to whiten the pool-centred 60 inputs. Fit a balanced 200-tree support RF, leaf size 1, square-root feature subsampling, seed 42. Blend with source weight `alpha=20/(20+4b)`. Apply one Gaussian averaging pass over self plus eight nearest lattice neighbors with sigma 1 key unit. The 120-context inputs belong to the source prior; the original local ASTRA head has 60—not 120—inputs. [S11, S12, S14]

### Why the method was interesting
It improved the much narrower prototype family while exposing its information advantages explicitly. Historical locked ASTRA reached **0.735239 ± 0.005406** at 200 under 100 newly seeded support trials/budget, seed 104729. That number stays historical. The inherited recipe was historically audit-selected; later locking and new seeds improve procedural clarity/repeatability but do not erase that exposure. [S11]

## H. Coordinate_RF: the current development-locked research incumbent
### The actual change
Append **two** standardized coordinate columns to the local RF inputs after adaptive whitening. Coordinates are centred and standardized using the full target pool, with standard deviations bounded below by one. The local head therefore has **62 inputs**. The contextual source prior remains 120-dimensional; forest settings, prior weighting and Gaussian graph remain unchanged. No new spectral features, query labels, class-specific thresholds or ground-truth geographic anchors were added. [S12, S14]

Coordinates were considered because nearby neighborhoods can share development history and spectra alone may not capture all regional structure. That hypothesis can work for random pixels yet fail under geographic extrapolation, exactly the distinction tested by the spatial audit. Coordinates are not proof of building identity or chronological causality.

### How selection was controlled
A fixed 800-label bank (200/class, seed 20260909) was used for support-only development. Initial five folds used 160 train/40 validation per class. Promising candidates underwent 20 repeated holdouts at 5/25/50/100/160 train shots and support-only directional safeguards. Final lock records Coordinate_RF and ExtraTrees as the top ranked options; Coordinate_RF's locked 160-shot repeated-holdout mean was **0.779338**, versus ASTRA **0.771304**, gain **0.008034**, 15/20 paired wins. These are development-support scores—not the final 200-shot query result.

The lock requires a 160-shot gain >0.002, at least 70% paired wins, no other budget worse by more than 0.005, and geographic mean/worst safeguards on the development bank. Passing that development check does not guarantee the later final spatial audit will improve. The rule/configuration were not changed after final-query scoring. [S12]

### Why call it incumbent carefully
Coordinate_RF is the **development-selected packaged research model** for the stated random-pixel/full-pool regime. It is not an officially scored organizer winner, not a universal spatial replacement for ASTRA, and not the model in the existing EXP-010 deck. Team members should always qualify “best” with protocol and scope. Model development is frozen in this preparation task.

## I. Current locked numerical ledger
Mean macro F1 ± population SD, **200 paired episodes per budget**, final seed **20260910**. All eligible final queries exclude the fixed development bank and current support. These values match the user-supplied target table and authoritative saved results; no stronger superseding validated result was found.

| Shots/class | Coordinate_RF | Gain vs matched ASTRA | Wins vs ASTRA |
|---:|---:|---:|---:|
| 5 | **0.650253 ± 0.011246** | +0.000289 | 106/200 |
| 25 | **0.687664 ± 0.012145** | +0.005045 | 171/200 |
| 50 | **0.708436 ± 0.011277** | +0.009213 | 193/200 |
| 100 | **0.729839 ± 0.008802** | +0.013803 | 200/200 |
| 200 | **0.749299 ± 0.005716** | **+0.016262** | **200/200** |

At 200: matched ASTRA **0.733037**; EXP-010 **0.622840**; EXP-F **0.657602**. Gains: **+0.016262 / +0.126459 / +0.091697** respectively. These comparisons are paired within the current run, not subtractions from old 0.735239/0.623982/0.658664 means.

The 200-shot paired-bootstrap 95% gain interval versus ASTRA is approximately **[0.015856, 0.016669]**. At five shots it is approximately **[-0.000077, 0.000667]**; paired t p≈0.125, Wilcoxon p≈0.255. The five-shot advantage is not statistically persuasive or practically substantial. Fifteen paired comparisons were analyzed, with Holm correction separately across the t-test and Wilcoxon families. Effect sizes are conditional: a large paired Cohen dz reflects small paired-difference variance, not an enormous transferable city-level effect. [S12, S14]

### Spatial ledger: memorize the exception, not just the win
At 200 shots, ten trials per direction, ten-key buffer:

| Diagnostic | Coordinate_RF | Matched ASTRA |
|---|---:|---:|
| x-half mean | 0.682326 | 0.687017 |
| y-half mean | 0.706106 | 0.706326 |
| worst directional mean | 0.644816 | 0.658183 |
| four-direction mean | **0.694216** | **0.696672** |

High-x support to low-x query loses about **0.028670** versus ASTRA. Do not describe Coordinate_RF as geographically robust without immediately giving the comparator/caveat. The random-pixel control has a different query geography; random-versus-spatial differences are not exact same-query paired effects. Lattice-key units are the authoritative buffer units; do not casually substitute metres without a verified mapping. [S13]

## J. Reproducibility: several claims, several levels
### Episodes and labels
The final harness constructs class-stratified support sets from eligible labels using seed 20260910, one permutation per class/trial with nested prefixes across budgets. Query is the eligible complement. It excludes all 800 development pixels from every final query. The 1,000 episodes are 200 trials × five budgets; 4,000 saved prediction arrays reflect four methods—not 4,000 independent experiments or cities.

Stratified episode construction uses labels to select the support samples; this is an evaluator function, not evidence that all those labels entered model fitting. Fitting receives Madrid source labels or current support labels only. Historical audit selection is a separate exposure that remains disclosed. The feature builder's label-dependence is yet another issue and cannot be waved away by saying the estimator has no query-label argument.

### Model and pool identity
Current model code SHA256: `26b2299ad50dcf935fb8bc1a89d4e79f82cf2c68881619a6eaf1330f813a7533`.

Current pool SHA256: `b975db430b4a00d1c90d59d10a76ef11a6c3727be42e22f41bec49a6f6c28007`.

Frozen EXP-010 state SHA256: `2f4dc0f7a84ea54e967d7a96573b349331e1777ddb0a4a46e4925cad7bd6d266`.

Accepted preprocessing SHA256: `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`.

The older preprocessing digest `f6f588c4…` in early member logs belongs to a different recorded artifact. Do not replace the accepted digest with it. Hashes bind bytes; they do not prove scientific correctness or make unknown pickle files safe to deserialize. [S03, S05, S12, S15]

### Clean replay evidence
The completed original fresh-source replay rebuilt eight state arrays and matched **4,000 prediction arrays across 1,000 episodes**. Publication later used ten fixed-reference ASTRA/Coordinate_RF calls for exact checks and observational runtime/importance diagnostics, recalculated all 4,000 confusion/F1 records, checked the 1,000 support/development exclusions, and verified 1,622 protected files in that publication freeze scope. Its distribution validator sealed 1,856 files after final additions.

The final publication ZIP was extracted outside the research repository, with no Git directory. Five packaged Coordinate_RF reference predictions passed and every rebuilt publication CSV was byte-identical. This is strong evidence of portable *inference/evidence replay under the tested environment*, not a claim that every Python version/platform will produce bit-identical bytes. Figure/PDF metadata and runtime measurements need not be byte-identical when regenerated.

This current preparation task performed **no new fitting or prediction**. It inspected those existing receipts and made read-only hash/static checks. Snapshot hash counts use a new, different scope: **13 intended files**, not the historical 1,622/1,856 counts. Explain the scope before quoting a count. [S15, S16]

### Runtime and interpretability boundaries
Current publication runtime instrumentation covered ten fixed-reference RF-method calls, not an optimized performance benchmark. Reported sampled peak RSS is not guaranteed OS high-water memory; local RF fit/predict timing excludes source-prior refit and does not account for all transform/smoothing time. All-model historical call times exist, but separate historical CPU/memory and fit/predict measurements do not.

Coordinate_RF impurity importance was observed from verification fits. The 60 whitened axes mix original features; they cannot be labelled as direct raw spectral feature importance. Coordinate split usage is not causal attribution. Calibration plots use existing probabilities for ASTRA/Coordinate_RF on one predeclared 200-shot episode; no calibrator was fitted and baseline hard predictions cannot yield probability calibration. Transfer-stage bars likewise show internal stages on one shared episode, not independently tuned causal interventions. [S14]

## K. Limitations we should volunteer
1. **No independent organizer-held-out city/test:** final data are the same Amsterdam population used throughout research.
2. **Historical selection exposure:** inherited ASTRA was audit-selected. The newer fixed bank/lock improves the protocol without erasing that history.
3. **Extra development supervision:** 800 labels beyond any one episode's budget were used during model selection.
4. **Spatial sensitivity:** coordinate gains under random pixels do not imply geographic extrapolation gains; our own spatial comparison is worse.
5. **Transductive assumption:** the full ordered target pool and coordinates are needed. Organizer approval for that privilege is not established by a message about submitting slides/notebooks.
6. **Deployment feature issue:** the accepted 60-feature preprocessing remains label-dependent; a rejected label-free feature branch does not automatically fix the current production path.
7. **Reference CV limitation:** scaling was fitted before source folds. Current target results should not be conflated with unbiased source CV.
8. **Label and unit semantics:** mixed building-age labels, city-specific old-era boundaries and unavailable building/parcel IDs limit interpretation.
9. **Competitor uncertainty:** missing tuned config, incomplete original data provenance and no new remote check prevent exact/current leaderboard claims.
10. **Reproducibility limits:** exact tested replay is not every-platform compatibility, independent human verification, raw-data permission or proof of absence of every conceivable leak.
11. **Optional source-rebuild archive dependency:** static inspection found the publication ZIP contains a preprocessing pickle referencing `working.minimal_standard_scaler` but not that module. Its optional `verify_source.py` therefore has an unresolved standalone import dependency. This does not undo the tested inference/evidence replay, which does not load that pickle; do not claim every optional source-rebuild command is self-contained.
12. **Submission readiness gap:** a model artifact and publication ZIP are not the requested final notebook. The safety fallback is preserved with explicit gaps.
13. **Snapshot directory metadata:** seven unsolicited OneNote indexes appeared after sealing. Intended files are unchanged; the protected ZIP is the exact clean fallback. Do not create a new ZIP from the whole directory and include those indexes. [S03, S10–S16]

## L. Concrete lessons from the journey
- **Transfer needs an information path.** Training a Madrid RF somewhere in a notebook is not enough if the target classifier ignores it.
- **Use an equal-support comparator.** Beating zero-shot with 800 target labels is not a clean proof of useful source transfer.
- **Few-shot geometry is fragile.** Whitening/source offsets help or hurt depending on the sample budget and representation; frozen formulas matter.
- **More columns are not automatically better.** The 94-feature negative result beat the intuition, not the original representation.
- **Do not promote a score without its access regime.** A pool-aware spatial RF and an inductive prototype have different privileges.
- **Coordinates encode useful structure and brittle shortcuts.** Both are compatible with the observed random/spatial trade-off.
- **A negative preregistered test is useful.** E1 failed despite beating RF; E2's consistent small gain still missed the predefined practical threshold.
- **Separate implementation validation from scientific validation.** E3 illustrates why a completed worker log is not a full independent scientific pass.
- **Preserve failures.** Numerical RF ties, verifier bugs, blocked runtime checks and missing configs should not be erased to make a clean story.
- **A hash is a contract about bytes.** Source code, pool state, feature order, episode indices and environment all matter; an unchanged seed alone is insufficient.
- **New seeds are not new data distributions.** More episodes can tighten conditional sampling estimates while leaving deployment uncertainty unchanged.
- **Stop when packaging is the bottleneck.** The current missing notebook is a more immediate organizer-delivery risk than an extra decimal point of F1.
- **Attribution and insight are different.** Everyone can understand and defend the method without claiming authorship of another member's code.
- **Scientific stories should update.** The old hypothesized 0.62 ceiling and categorical version-drift explanation are not current facts.

## M. Presentation strategy and rehearsal
### Choose the story before choosing the slides
There are two possible narratives, and mixing them is the main risk:
- **Immutable fallback:** existing EXP-010 deck/text, historically matched 45/50 result, plus explicitly reference notebooks. Do not announce 0.749299 while displaying that deck as if it implemented the result.
- **Current-research presentation plan:** a future separately approved deck/notebook package would explain Coordinate_RF, its development supervision and its spatial trade-off. The plan below is a rehearsal outline, not a claim that those slides already exist.

### Recommended current-research story arc (10 content slides, adjustable to organizer time)
| Slide | Purpose | Lead | One point to land |
|---|---|---|---|
| 1 | Problem and honest abstract | Member 1 | Building-era transfer with little target supervision |
| 2 | Data, source/target, budget and metric | Member 1 | Four classes; b/class; macro F1; one target city |
| 3 | Baseline flaw and EXP-010 bridge | Member 2 | Madrid-supervised ranking/geometry must actually reach target predictions |
| 4 | What experiments taught us | Member 2 | Covariance helps at some budgets; feature expansion and several hypotheses failed |
| 5 | ASTRA mechanism diagram | Member 2 | Prior + adaptive covariance + support RF + Gaussian smoothing |
| 6 | Coordinate_RF change and selection lock | Member 2 | Only two local coordinate columns; bank/lock before final scoring |
| 7 | Current paired learning curves | Member 3 | 0.749299 at 200; +0.016262 vs matched ASTRA; five-shot gain inconclusive |
| 8 | Spatial challenge | Member 3 | Four-direction mean is slightly worse than ASTRA |
| 9 | Trust evidence and limitations | Member 3 | Exact replay and exclusions, but no independent city/test |
| 10 | Takeaway, practical scope, next validation | Member 1 | Strong conditional result, explicitly limited deployment claim |

If time is short, move Gate4 details, full competitor discussion, covariance equations, class metrics and runtime to Q&A. Do not spend a third of the talk describing failed infrastructure. Show it only as evidence discipline when relevant. Keep one clear curve and one spatial plot rather than a wall of 32 figures.

### Existing 17-slide fallback: how to avoid stale claims
Slides 1–5 establish EXP-010's problem and method; 6–8 carry its historical results/schedule; 9–12 cover negative findings and caveats; 13 concludes; 14–17 are backup. The new member guides reassign those speaking sections among three presenters without altering the file. Read `CONSISTENCY_AUDIT.md` before rehearsal: it flags “official” wording, overlapping-pixel interpretation, causal seasonal prose and historical reproducibility statements.

### Explain concepts simply
- **Prototype:** a representative average for each class, estimated from support labels.
- **Shrinkage:** stabilize a noisy estimate by mixing it with a simpler or source-informed estimate.
- **Covariance:** how feature dimensions move together; it can reveal duplicated directions.
- **Whitening:** re-express features so correlated directions are decorrelated/scaled, with regularization to avoid unstable amplification.
- **Source prior:** a source-informed initial distribution over class labels, not a supplied target answer.
- **Pseudo-label:** the model's own guess, not newly acquired ground truth; errors can reinforce themselves.
- **Transduction:** use the unlabelled features of the actual prediction pool when adapting the model.
- **Spatial smoothing:** neighboring probability vectors vote with fixed distance-based weights.
- **Paired trial:** both models receive the same support and query; compare within that draw.
- **Population SD:** the observed spread across the benchmark episodes, not “plus/minus certainty.”

### Answer “Why did you do this?”
Use a four-step answer: **problem → hypothesis → controlled evidence → boundary**. Example: “Support prototypes ignore nonlinear class shape. We tested a richer support classifier under explicit pool access. The frozen RF-based recipe improved matched random-pixel scores. But it needs the full target pool and spatial generalization remains limited.” Do not reverse-engineer a just-so mechanism from a positive number.

### Answer “Why should we trust this?”
Lead with evidence and its limit: “We froze the choice, saved support/query sets, checked exclusions, replayed predictions and rebuilt all numerical tables. That makes the stated internal result reproducible. It does not make it an independent-city result.” Then give the 200-shot paired gain, its interval and the negative spatial comparison if asked.

### Team rehearsal protocol
Each member gives their 30-second area summary, then answers one question outside their own area. Correct vocabulary before speed. Practice saying “that is not established” without apologizing excessively. The designated evidence presenter checks whether a question concerns old EXP-010, historical ASTRA or current Coordinate_RF before answering. Never make an unsupported authorship claim to balance speaking time.

## N. Judge question bank
The following bank contains three questions in each of the 22 requested categories. Every answer has a short version, a deeper version, key facts and a common error to avoid. The source IDs above are factual anchors, not claims of independent verification by the speaker.

### 1. Problem understanding

#### Q01
**QUESTION:** What are you predicting?
**SHORT ANSWER:** One of four construction-era classes for each Landsat pixel.
**DEEPER ANSWER:** The labels summarize building ages within mixed 30 m pixels. We are not estimating an exact year for every individual roof. The application motivation is incomplete urban records, but our evidence is a supplied two-city classification benchmark, not a deployed urban-planning system.
**KEY NUMBERS/FACTS:** Four classes; Madrid source, Amsterdam target. [S01,S03]
**COMMON MISTAKE TO AVOID:** Calling a pixel an independent building or claiming exact-year prediction.

#### Q02
**QUESTION:** What makes this transfer learning rather than ordinary classification?
**SHORT ANSWER:** Source-supervised information must influence target predictions.
**DEEPER ANSWER:** In EXP-010, Madrid supplies feature relevance and class offsets. In ASTRA/Coordinate_RF, a Madrid-trained aligned contextual prior contributes to target probabilities. The reference few-shot prototypes largely use target support means; a source RF trained elsewhere in the notebook does not automatically make that prototype path supervised transfer.
**KEY NUMBERS/FACTS:** EXP-010: source ranking/geometry; current model: contextual prior. [S04,S05,S12]
**COMMON MISTAKE TO AVOID:** Saying the baseline target-only prototype directly consumes the fitted RF.

#### Q03
**QUESTION:** What would success outside this benchmark require?
**SHORT ANSWER:** A specified deployment information contract and genuinely unseen geographic evaluation.
**DEEPER ANSWER:** We would need to know whether full unlabelled target features and coordinates are available, fix the label-dependent preprocessing membership path, and evaluate a locked method on an untouched city or organizer split. Current exact replays establish internal reproducibility, not those missing deployment conditions.
**KEY NUMBERS/FACTS:** One target city; pool-bound current artifact. [S12-S16]
**COMMON MISTAKE TO AVOID:** Equating a higher internal F1 with city-portable deployment.

### 2. Dataset

#### Q04
**QUESTION:** How many observations do you have?
**SHORT ANSWER:** 76,263 Madrid and 25,992 Amsterdam pixel vectors, each with 60 input columns.
**DEEPER ANSWER:** Raw data are annual records: about 3.17 million Madrid and 1.06 million Amsterdam pixel-year rows. Aggregation creates one vector per pixel. Counting annual rows as independent training examples would exaggerate the effective spatial sample size; neighboring pixels also remain correlated.
**KEY NUMBERS/FACTS:** 76,263 / 25,992 pixels; observed 1984-2025, 42 years. [S02,S03]
**COMMON MISTAKE TO AVOID:** Saying millions of independent buildings or using the earlier 2024 end year as a verified current data fact.

#### Q05
**QUESTION:** Are the classes balanced and identical between cities?
**SHORT ANSWER:** No: counts are unequal, and the oldest-era boundary differs by city.
**DEEPER ANSWER:** Amsterdam counts are 7,568, 8,802, 6,745 and 2,877. Both cities share later cutpoints, but Madrid uses 1960 for its early boundary and Amsterdam 1945. Balanced support sampling and class-balanced forests help define the experiment; they do not make the naturally imbalanced query distribution balanced.
**KEY NUMBERS/FACTS:** Amsterdam classes 1-4: 7568/8802/6745/2877. [S03]
**COMMON MISTAKE TO AVOID:** Saying Class 1 is largest or that balanced support means balanced queries.

#### Q06
**QUESTION:** Are your labels exact ground truth for each building?
**SHORT ANSWER:** They are supplied pixel-level age summaries and can represent mixed buildings.
**DEEPER ANSWER:** A pixel may contain buildings from several periods plus non-building surfaces. The weighted construction-year label is a useful benchmark target, but it does not identify every roof or quantify label uncertainty. We have not measured a Bayes-error ceiling or verified parcel-disjoint evaluation.
**KEY NUMBERS/FACTS:** 30 m pixels; building/parcel IDs unavailable for that audit. [S01,S10]
**COMMON MISTAKE TO AVOID:** Claiming a measured performance ceiling or perfectly noise-free labels.

### 3. Preprocessing

#### Q07
**QUESTION:** What transforms raw observations into the model inputs?
**SHORT ANSWER:** QA screening, annual gap filling, spectral/temporal summaries and Madrid-fitted scaling.
**DEEPER ANSWER:** The reference selects valid observations, filters high-blue haze, interpolates missing years, computes indices and temporal summaries, then standardizes with source statistics. The accepted local artifact uses a documented minimal scaler shim. The current local RF then restores raw units for its own pool-based covariance transform; preprocessing and model whitening are different stages.
**KEY NUMBERS/FACTS:** 60 ordered features; accepted preprocessing hash begins 51f11bc9. [S03,S14]
**COMMON MISTAKE TO AVOID:** Presenting the minimal scaler as proven identical to every sklearn API/version.

#### Q08
**QUESTION:** Why is label-dependent feature construction a concern?
**SHORT ANSWER:** It prevents claiming a clean raw-data path for hidden-label deployment.
**DEEPER ANSWER:** The reference feature builder filters/groups using age-class metadata even though the numerical class is not one of the 60 model features. Thus the feature values and benchmark membership path are not a certified generic hidden-test pipeline. A separate label-free 94-feature branch existed but was rejected and is not silently substituted into the frozen method.
**KEY NUMBERS/FACTS:** Current inference features exclude age_class; raw builder membership remains label-dependent. [S03,S04]
**COMMON MISTAKE TO AVOID:** Answering that everything is leakage-free simply because the RF feature list excludes the target column.

#### Q09
**QUESTION:** Was your source CV preprocessing fold-safe?
**SHORT ANSWER:** No; the reference scaler was fitted before Madrid CV.
**DEEPER ANSWER:** The source reference result must carry that limitation. In an unbiased future source-CV design, preprocessing should be fitted inside each training fold. We did not repair or rerun that baseline in preparation, and the current target paired evaluation should not be mislabelled as corrected source CV.
**KEY NUMBERS/FACTS:** Reference Madrid CV 0.6281 ±0.0043; pre-CV scaler. [S03]
**COMMON MISTAKE TO AVOID:** Claiming independent source CV with fold-local preprocessing.

### 4. Random Forest

#### Q10
**QUESTION:** What is a Random Forest and why can it help here?
**SHORT ANSWER:** An ensemble of decision trees captures nonlinear interactions in tabular features.
**DEEPER ANSWER:** Trees partition feature space through threshold splits; bootstrap samples and feature subsampling diversify the trees. Averaging probabilities can reduce individual-tree variance. This is well suited to structured spectral summaries, but a forest is not immune to small-support overfitting, geographic shortcuts or source-target shift.
**KEY NUMBERS/FACTS:** Current local RF: 200 trees, balanced weights, leaf 1, sqrt features. [S12,S14]
**COMMON MISTAKE TO AVOID:** Saying forests cannot overfit or do not need validation.

#### Q11
**QUESTION:** Are the source and target forests the same model?
**SHORT ANSWER:** No; distinguish the historical source-ranking forest from the current source-prior and local forests.
**DEEPER ANSWER:** EXP-010 uses a 500-tree Madrid RF to derive importance summaries, then target prototypes. ASTRA/Coordinate_RF fit two successive 200-tree source-prior forests with leaf 2 and a separate 200-tree local target-support forest with leaf 1. The current prior is cached; episode adaptation fits the local head.
**KEY NUMBERS/FACTS:** 500 source-ranking trees versus current 200-tree source/local forests. [S05,S14]
**COMMON MISTAKE TO AVOID:** Claiming EXP-010 fits a local RF or Coordinate_RF uses the 500-tree ranking forest as its local head.

#### Q12
**QUESTION:** Why is the forest seed not enough to guarantee identical predictions?
**SHORT ANSWER:** Inputs, ordering, versions and floating-point aggregation also matter.
**DEEPER ANSWER:** Historical v2 replays exposed one-prediction differences near machine-epsilon probability ties in some arrays. Stable serial aggregation was introduced before the final recipe lock. Exact input/state hashes and prediction-array checks are more convincing than a seed alone, and do not promise every-platform equivalence.
**KEY NUMBERS/FACTS:** Seed 42; historical ties about 5.55e-17. [S11,S15]
**COMMON MISTAKE TO AVOID:** Concluding fixed random_state guarantees bit equality on any machine.

### 5. Transfer learning

#### Q13
**QUESTION:** What exactly transfers in EXP-010?
**SHORT ANSWER:** Madrid-supervised feature relevance and relative class geometry.
**DEEPER ANSWER:** The selected source-ranked features are weighted by square-root importance. Source class means are expressed as offsets from the source overall mean and recentered on target support. A budget-dependent mixture stabilizes target class prototypes at five shots; above five the representation still transfers even though prototype shrinkage is zero.
**KEY NUMBERS/FACTS:** k=30/lambda=.6 at 5; k=45/lambda=0 otherwise. [S05]
**COMMON MISTAKE TO AVOID:** Saying no transfer remains when lambda is zero.

#### Q14
**QUESTION:** How does the current source prior adapt without target truth?
**SHORT ANSWER:** It aligns source statistics to unlabelled target features and uses model-generated pseudo-labels.
**DEEPER ANSWER:** A globally aligned source forest predicts target pseudo-classes. Source class clouds are aligned once more to corresponding pseudo-labelled target groups before a second forest supplies probabilities. Those guesses may be wrong, so this is not equivalent to obtaining extra labelled target examples or proving that conditional class distributions match.
**KEY NUMBERS/FACTS:** 120 contextual inputs; one conditional alignment iteration. [S12,S14]
**COMMON MISTAKE TO AVOID:** Calling pseudo-labels true target labels or guaranteed correct.

#### Q15
**QUESTION:** Why not use the source model unchanged?
**SHORT ANSWER:** Local zero-shot performance showed substantial source-target mismatch.
**DEEPER ANSWER:** The measured local source RF scores about 0.4433 zero-shot, while even target-support prototype adaptation helps. That motivates adaptation but is not the fair primary comparator for transfer benefit: our method must be compared with alternatives receiving the same support labels and query sets.
**KEY NUMBERS/FACTS:** Local zero-shot 0.4433; organizer-saved 0.3427 is a separate record. [S03,S05]
**COMMON MISTAKE TO AVOID:** Claiming the full difference from zero-shot measures transfer improvement.

### 6. Few-shot setup

#### Q16
**QUESTION:** What is an episode?
**SHORT ANSWER:** One support selection and its held-out eligible query set.
**DEEPER ANSWER:** In the current run, each class supplies a random ordered support prefix; all models receive identical support and query rows for that budget/trial. The query excludes the fixed development bank and current support. The same city and many query pixels are reused across episodes, so episodes measure support-sampling variability rather than independent-city variability.
**KEY NUMBERS/FACTS:** 200 trials × five budgets = 1,000 paired episodes. [S12]
**COMMON MISTAKE TO AVOID:** Calling each episode a new dataset or city.

#### Q17
**QUESTION:** How many target labels does the current method use?
**SHORT ANSWER:** An episode uses 4b support labels, plus a separately disclosed 800-label research-development bank.
**DEEPER ANSWER:** The model recipe was selected using the fixed development bank. The final episode model receives only its current support labels for local fitting, while full-pool features/coordinates enter transductive operations. It would be misleading to call the entire research project a 20-label exercise because one evaluated episode has five shots/class.
**KEY NUMBERS/FACTS:** 5/class=20; 200/class=800; separate development bank=800. [S12]
**COMMON MISTAKE TO AVOID:** Hiding development supervision behind the episode budget.

#### Q18
**QUESTION:** Are budgets nested and trials independent?
**SHORT ANSWER:** Budgets are nested within a trial; query populations overlap heavily across trials.
**DEEPER ANSWER:** One per-class permutation supplies prefixes for the current five budgets, reducing irrelevant differences between learning-curve points. This creates correlation between budgets. Conditional episode bootstrap can describe the saved support-draw regime but is not a pixel-independent or city-level resampling procedure. Competitor headline budgets followed a different RNG convention.
**KEY NUMBERS/FACTS:** Final seed 20260910; nested prefixes. [S10,S12,S14]
**COMMON MISTAKE TO AVOID:** Treating all 1,000 episode scores as independent observations in a pooled test.

### 7. Feature selection

#### Q19
**QUESTION:** How were EXP-010 features selected?
**SHORT ANSWER:** By Madrid-supervised RF importance, retaining the frozen top-k dimensions.
**DEEPER ANSWER:** The ranking uses source labels, not final-query labels. Square-root weighting turns importance into a multiplier of squared Euclidean distance. The choice of k/lambda was a historical development decision, so source-only ranking does not make the entire selection process independent of target research feedback.
**KEY NUMBERS/FACTS:** Top 30 at 5, top 45 at 25-200. [S05]
**COMMON MISTAKE TO AVOID:** Confusing source-only ranking with no target-side model selection ever.

#### Q20
**QUESTION:** Why did 94 engineered features not win?
**SHORT ANSWER:** The saved comparison showed little selection benefit and worse audit performance at most budgets.
**DEEPER ANSWER:** Additional seasonal, coverage and temporal information was plausible and a label-free builder was useful. However, the measured feature comparison did not support adoption. More noisy or redundant dimensions may worsen few-shot estimates, but the exact causal reason was not isolated; the negative result is narrower than all feature engineering being useless.
**KEY NUMBERS/FACTS:** About +.0001 selection mean; 8/25 audit wins. [S04]
**COMMON MISTAKE TO AVOID:** Claiming dilution was proved or all extra features are bad.

#### Q21
**QUESTION:** Can RF importance tell us which original spectral band caused the gain?
**SHORT ANSWER:** Not from the current whitened-axis impurity ranking alone.
**DEEPER ANSWER:** The local RF uses covariance-transformed axes that mix raw inputs. Its impurity importances indicate split usage in that representation and can favor some variable types. Coordinates can be separately identified as appended columns, but even their importance is descriptive, not causal or a validated feature-ablation effect.
**KEY NUMBERS/FACTS:** Current local dimensions: 60 whitened axes +2 coordinates. [S14]
**COMMON MISTAKE TO AVOID:** Relabelling a whitened axis as raw NIR importance or calling importance causal attribution.

### 8. ASTRA-AGF

#### Q22
**QUESTION:** Explain adaptive geometry without equations.
**SHORT ANSWER:** It uses target feature correlations but trusts a simpler geometry when support is tiny.
**DEEPER ANSWER:** Full unlabelled target covariance describes how features vary together. Budget-dependent shrinkage reduces off-diagonal covariance at small support counts, then permits more decorrelation as support increases. That transformed representation feeds a support-trained RF; it is not just a different Euclidean prototype or a learned neural embedding.
**KEY NUMBERS/FACTS:** rho=min(1,60/(4b)); 60 local inputs. [S11,S14]
**COMMON MISTAKE TO AVOID:** Saying rho is newly tuned per final query set.

#### Q23
**QUESTION:** What does the spatial graph do?
**SHORT ANSWER:** It averages neighboring predicted probabilities with fixed Gaussian weights.
**DEEPER ANSWER:** After source/local blending, self plus eight nearest lattice neighbors contribute one smoothing step. No ground-truth query labels or support-truth clamping are used. Support predictions are still influenced by support fitting, so prediction-only smoothing can benefit from spatial adjacency; it does not establish independent samples.
**KEY NUMBERS/FACTS:** Nine neighbors including self; sigma=1 key unit; one pass. [S14]
**COMMON MISTAKE TO AVOID:** Saying no truth anchors means no spatial dependence or shortcut benefit.

#### Q24
**QUESTION:** Which ASTRA score should we quote?
**SHORT ANSWER:** Use 0.733037 as the matched 200-shot control for current Coordinate_RF comparisons.
**DEEPER ANSWER:** Historical ASTRA 0.735239 ±0.005406 comes from its 100-trial seed-104729 regime, without the later development-query exclusion. It remains valid historical evidence but is not the paired control for Coordinate_RF 0.749299. A third value, 0.737388, belongs to the earlier competitor-convention comparison.
**KEY NUMBERS/FACTS:** Historical .735239; current matched .733037; same-20 comparison .737388. [S10-S12]
**COMMON MISTAKE TO AVOID:** Mixing means from different protocols because the model name is the same.

### 9. Coordinate-RF

#### Q25
**QUESTION:** What changed relative to ASTRA?
**SHORT ANSWER:** Two full-pool-standardized coordinate columns were appended to the local RF inputs.
**DEEPER ANSWER:** The 60 whitened local features become 62. The 120-feature contextual source prior, source blending schedule, covariance rule, RF settings and Gaussian graph remain unchanged. This is a development-selected variant of the existing recipe, not a new raw spectral representation or a different classifier.
**KEY NUMBERS/FACTS:** Local 62; source context 120; config {coord: true}. [S12,S14]
**COMMON MISTAKE TO AVOID:** Claiming only Coordinate_RF uses space; ASTRA already uses spatial context and smoothing.

#### Q26
**QUESTION:** Why is Coordinate_RF the current incumbent?
**SHORT ANSWER:** It was selected and locked on the designated development protocol before final-query scoring.
**DEEPER ANSWER:** Its 160-shot repeated development-holdout mean improved by about .008034 over ASTRA with 15/20 wins and passed the stated development safeguards. Its later random-query gain was not used to retune or reselect it. Incumbent means the packaged research choice in this access regime, not an official organizer promotion.
**KEY NUMBERS/FACTS:** Lock 2026-09-09 17:50:37 local recorded time; final seed 20260910. [S12]
**COMMON MISTAKE TO AVOID:** Saying we chose it because its final 0.749299 was highest.

#### Q27
**QUESTION:** Does the artifact predict arbitrary new cities?
**SHORT ANSWER:** No; it is bound to the supplied ordered target pool and coordinates.
**DEEPER ANSWER:** The cached prior, covariance and neighbor structure belong to 25,992 Amsterdam rows. A different or reordered pool violates the input contract. A future new-pool evaluation would need the unchanged source-fitting procedure with appropriate source data and new target features, plus an independently justified evaluation protocol.
**KEY NUMBERS/FACTS:** 25992-row pool; exact feature order and row indices. [S11,S14]
**COMMON MISTAKE TO AVOID:** Treating the cached Amsterdam artifact as a generic unseen-city pointwise estimator.

### 10. Spatial robustness

#### Q28
**QUESTION:** Why test geographic halves?
**SHORT ANSWER:** Random-pixel sampling may benefit from nearby, similar locations and hide extrapolation difficulty.
**DEEPER ANSWER:** A buffered opposite-half query tests a harder geography under the same transductive access regime. All four directions are reported, not just the favorable side. It is still one city’s diagnostic with limited partitions; building/parcel independence is not established.
**KEY NUMBERS/FACTS:** 200 shots; 10 trials/direction; 10-key buffer. [S13]
**COMMON MISTAKE TO AVOID:** Calling four directions four independent cities.

#### Q29
**QUESTION:** Does Coordinate_RF improve geographic robustness over ASTRA?
**SHORT ANSWER:** No, not in the reported overall directional comparison.
**DEEPER ANSWER:** Its x-half and four-direction means are lower, its y-half mean is nearly equal but lower, and its worst-direction mean is worse. Random-pixel gains coexist with poorer regional extrapolation. This is exactly why we cannot claim it is a universal replacement despite 200/200 high-shot random wins.
**KEY NUMBERS/FACTS:** Four-direction .694216 vs .696672; worst .644816 vs .658183. [S13]
**COMMON MISTAKE TO AVOID:** Omitting ASTRA or quoting only the coordinate variant directions that improved.

#### Q30
**QUESTION:** Is the buffer 300 metres and does it prevent all leakage?
**SHORT ANSWER:** The audited contract is ten lattice-key units; it is not a universal leakage guarantee.
**DEEPER ANSWER:** Older notes interpret keys as a 30 m lattice, but the latest method/report treats key units as authoritative rather than casually asserting geographic metres. A buffer reduces immediate support adjacency across the split, while full-pool statistics and spatial dependence still exist. It does not identify same-building overlap or prove domain generalization.
**KEY NUMBERS/FACTS:** 10 key units; coordinates must follow the supplied integer lattice. [S10,S13,S14]
**COMMON MISTAKE TO AVOID:** Equating a distance buffer with fully independent geographic validation.

### 11. Validation

#### Q31
**QUESTION:** How was model selection separated from final evaluation?
**SHORT ANSWER:** The latest candidate was locked using designated support-development labels before final-query scoring.
**DEEPER ANSWER:** A fixed 800-label bank supported initial folds, repeated holdouts and development spatial safeguards. Those pixels are excluded from final queries, and final support comes from outside the bank. The inherited ASTRA recipe had earlier audit exposure; the new separation cannot erase its history or create an organizer-hidden population.
**KEY NUMBERS/FACTS:** Development seed 20260909; final seed 20260910. [S12]
**COMMON MISTAKE TO AVOID:** Claiming the whole project has an untouched test set.

#### Q32
**QUESTION:** What do the paired tests establish?
**SHORT ANSWER:** Conditional evidence for mean support-sampling gains on the stated fixed target population.
**DEEPER ANSWER:** The analyses compare Coordinate_RF and controls by identical budget/trial keys, apply paired t and Wilcoxon tests, paired episode-bootstrap confidence intervals and effect sizes. Holm adjusts across 15 comparisons in each test family. These procedures do not measure between-city variation or remove historical selection bias.
**KEY NUMBERS/FACTS:** 200-shot ASTRA gain CI about [.015856,.016669]. [S14]
**COMMON MISTAKE TO AVOID:** Interpreting a tiny p-value as proof of generalization to any city.

#### Q33
**QUESTION:** What was Gate4 E2 good for if it missed the target?
**SHORT ANSWER:** It showed a reproducible small gain without satisfying the predefined practical success rule.
**DEEPER ANSWER:** At 25 shots the exact-reconstructed mean gain was .004953 and 10/10 pairs improved, but the required mean gain was .0100. Calling it inconclusive under that rule respects the original criterion; inventing a lower threshold after seeing results would undermine the test.
**KEY NUMBERS/FACTS:** E2 .603550 vs raw .598598; threshold +.0100. [S08]
**COMMON MISTAKE TO AVOID:** Relabelling E2 as successful because its p-value or win count looks favorable.

### 12. Leakage

#### Q34
**QUESTION:** Did you use the target test labels?
**SHORT ANSWER:** Current estimators use designated support labels; query truth is for evaluation, but historical research selection exposure is disclosed.
**DEEPER ANSWER:** The benchmark sampler uses labels for class-balanced support construction. A separate 800-label bank supports current selection. Historical ASTRA was audit-selected. The current inference API does not receive query truth, yet saying target labels were never used anywhere would be false, and the reference feature-builder deployment issue remains.
**KEY NUMBERS/FACTS:** 800 development labels; 4b episode support labels; historical audit exposure. [S03,S11,S12]
**COMMON MISTAKE TO AVOID:** Answering a blanket no without distinguishing fitting, sampling, selection and scoring.

#### Q35
**QUESTION:** Is using the entire unlabelled target pool cheating?
**SHORT ANSWER:** It is transductive learning; rule compliance depends on the organizer information contract.
**DEEPER ANSWER:** Means, covariance, pseudo-labels and graph structure use unlabelled target features/coordinates, not hidden query truth. This is a different privilege from inductive support-only adaptation. Our open-scope research assumes it, but the latest organizer message specifies deliverables, not permission for full-pool learning.
**KEY NUMBERS/FACTS:** Full ordered target pool required; permission not confirmed by submission email. [S06,S11,S16]
**COMMON MISTAKE TO AVOID:** Claiming coordinates/full-pool use is officially approved without evidence.

#### Q36
**QUESTION:** Can neighboring support predictions contaminate query predictions even without explicit labels?
**SHORT ANSWER:** They can transmit support-trained signal; that is spatial dependence, not automatically forbidden query-label use.
**DEEPER ANSWER:** The RF is trained on support labels and predicts the full pool. Smoothing averages those probabilities, including predictions at support locations. The absence of explicit truth anchoring narrows the leakage claim, but does not remove adjacency benefits. Whether that is allowed depends on the evaluation regime.
**KEY NUMBERS/FACTS:** Prediction-only Gaussian averaging; spatial stress reported. [S10,S13,S14]
**COMMON MISTAKE TO AVOID:** Saying prediction-only smoothing guarantees unbiased independent-pixel evaluation.

### 13. Reproducibility

#### Q37
**QUESTION:** What is the strongest replay evidence?
**SHORT ANSWER:** A fresh-source rebuild matched eight state arrays and 4,000 prediction arrays across 1,000 episodes.
**DEEPER ANSWER:** The existing original replay includes both inductive controls and the two RF methods. Later publication independently recalculated saved confusion/F1 records and verified fixed-reference calls. These are clean-process computational checks; they must not be described as a second human team or an independent organizer dataset.
**KEY NUMBERS/FACTS:** 4,000 arrays; 1,000 episodes; no expensive replay rerun in preparation. [S15]
**COMMON MISTAKE TO AVOID:** Confusing clean process with independent scientist or independent city.

#### Q38
**QUESTION:** Can someone reproduce the publication outside this workspace?
**SHORT ANSWER:** The existing extracted-archive test passed five reference predictions and byte-identical rebuilt CSVs.
**DEEPER ANSWER:** That ZIP contains the inference state, saved numeric evidence and preprocessed data under a defined allowlist. The organizer fallback ZIP is a different, smaller package and deliberately excludes target-truth data. Reproducible publication evidence is therefore not the same claim as a complete final notebook submission.
**KEY NUMBERS/FACTS:** Publication ZIP hash starts ed8ff94f; safety ZIP has its own seal. [S15,S16]
**COMMON MISTAKE TO AVOID:** Sending the large label-containing publication archive automatically as the minimal organizer deliverable.

#### Q39
**QUESTION:** What does your safety snapshot actually guarantee?
**SHORT ANSWER:** The 13 intended fallback files and ZIP have verified hashes and write protection; submission completeness remains explicitly unresolved.
**DEEPER ANSWER:** We preserved existing EXP-010 presentation/text, reference notebooks and minimal code/state. No final-method notebook was found. Seven background OneNote indexes appeared after sealing and were not deleted; the sealed ZIP excludes them. NTFS deny-write/delete and hashes protect/detect accidental changes, but owner/admin access is not WORM storage.
**KEY NUMBERS/FACTS:** 13 intended files; exact clean ZIP; no invented final notebook. [S16]
**COMMON MISTAKE TO AVOID:** Claiming a perfect current-model submission or silently ignoring post-seal directory additions.

### 14. Competitor comparison

#### Q40
**QUESTION:** Why is your score higher than the competitor?
**SHORT ANSWER:** The headline numbers use different protocols, so we do not claim that subtraction is a fair paired win.
**DEEPER ANSWER:** Our current .749299 excludes the fixed development bank and uses 200 trials/budget. Their locally recorded .7373 used 20 draws, another representation/configuration and earlier selection exposure. We can defend paired gains versus our current ASTRA/EXP-F/EXP-010 controls, not an exact comparison to an unavailable tuned competitor model.
**KEY NUMBERS/FACTS:** Current .749299; historical competitor claim .7373; not paired. [S10,S12]
**COMMON MISTAKE TO AVOID:** Saying we beat their exact best model by the difference of those means.

#### Q41
**QUESTION:** Did you copy competitor code or use their data?
**SHORT ANSWER:** No competitor payload is in our model implementation or safety snapshot; historical forensic execution was separate.
**DEEPER ANSWER:** Our own audits inspected their method and separately ran a labelled fallback mechanism with supplied data. The later candidate was independently implemented from this repository’s inputs and explicit formulas. Acknowledging mechanism inspiration is more accurate than pretending no comparison was studied. All forensic material remains outside the submission fallback.
**KEY NUMBERS/FACTS:** Own 60/120/62 representations; competitor tuned config unrecovered. [S10,S12,S16]
**COMMON MISTAKE TO AVOID:** Claiming no competitor code was ever executed anywhere in research, or claiming code originality proves conceptual novelty.

#### Q42
**QUESTION:** What was their latest update and was it a breakthrough?
**SHORT ANSWER:** Latest locally evidenced update is cf9af6c: distance-weighted smoothing, claimed .7373 at 200 shots.
**DEEPER ANSWER:** That update improved the earlier uniform-smoothing .7259 claim. It would be wrong to deny the reported improvement. We found no subsequently demonstrated local breakthrough beyond it, did not fetch new remote history in preparation, and still lack the winning configuration. Near reproduction is not exact winner reconstruction.
**KEY NUMBERS/FACTS:** cf9af6c, 2026-09-09 14:23:35 +02; .7259 to .7373. [S10]
**COMMON MISTAKE TO AVOID:** Turning lack of a newer local record into a claim that the competitor has made no progress anywhere.

### 15. Why not neural networks?

#### Q43
**QUESTION:** Why did you not use a neural network as the final model?
**SHORT ANSWER:** The frozen evidence supports the chosen tabular RF recipe; no validated neural-network advantage is recorded.
**DEEPER ANSWER:** The local adaptation sets are small and the inputs are structured spectral summaries. A neural model would require additional design, regularization and honest validation. We do not claim to have proved neural networks inferior, and this preparation task cannot authorize an untested neural search.
**KEY NUMBERS/FACTS:** Local support 20-800 labels; current RF 200 trees. [S12,S14]
**COMMON MISTAKE TO AVOID:** Inventing a neural-network experiment or saying neural networks always need millions of labels.

#### Q44
**QUESTION:** Could a pretrained sequence model use the annual satellite series better?
**SHORT ANSWER:** Possibly, but that is untested future work, not our result.
**DEEPER ANSWER:** A temporal model could preserve information lost in summaries, yet appropriate pretraining, source/target alignment, label availability and spatial splits would need careful handling. It might improve or worsen robustness. The rejected 94-feature experiment does not establish that all richer temporal representations are useless.
**KEY NUMBERS/FACTS:** Observed 42-year panels; frozen model consumes 60 summaries. [S03,S04]
**COMMON MISTAKE TO AVOID:** Presenting a plausible future architecture as an already demonstrated improvement.

#### Q45
**QUESTION:** Is the RF choice merely because of limited compute?
**SHORT ANSWER:** Compute and reproducibility matter, but the choice is grounded in the actual development evidence.
**DEEPER ANSWER:** The frozen RF approach was evaluated under a recorded support-development rule and replayed. We did not run a comprehensive equal-budget deep-learning comparison, so we cannot isolate compute as the causal reason or claim global model-family optimality. Presentation should emphasize evidence over fashionable architecture labels.
**KEY NUMBERS/FACTS:** Coordinate_RF selected before final scoring; no neural benchmark established. [S12]
**COMMON MISTAKE TO AVOID:** Claiming we searched every architecture or selected solely on the final score.

### 16. Why not another classifier?

#### Q46
**QUESTION:** Why not XGBoost or boosting?
**SHORT ANSWER:** There is no validated XGBoost result to claim; a histogram-boosted-tree alternative was explored but not selected.
**DEEPER ANSWER:** The autonomous report’s BoostedTrees arm uses sklearn HistGradientBoostingClassifier, not XGBoost. Its saved development mean was about .747317 in the reported support-CV comparison and it did not become the locked candidate. That is one operational comparison, not a universal theorem about boosting.
**KEY NUMBERS/FACTS:** BoostedTrees is sklearn histogram boosting, not XGBoost. [S12]
**COMMON MISTAKE TO AVOID:** Renaming the recorded algorithm to a more familiar library or claiming all boosting fails.

#### Q47
**QUESTION:** Why not ExtraTrees if it was competitive?
**SHORT ANSWER:** It was considered in the development selection but Coordinate_RF was the locked choice.
**DEEPER ANSWER:** ExtraTrees ranked among the strongest candidates and appears in the lock’s ranked options. The predeclared development rule included mean performance, paired wins, budget stability and geographic safeguards rather than one final-query number. We did not return to selection after seeing Coordinate_RF final results.
**KEY NUMBERS/FACTS:** Lock ranked Coordinate_RF and ExtraTrees; chosen config coord=true. [S12]
**COMMON MISTAKE TO AVOID:** Saying ExtraTrees was obviously poor or discarded because of the final audit.

#### Q48
**QUESTION:** Why not keep the simpler prototype model?
**SHORT ANSWER:** It remains a valuable inductive fallback, but the current richer recipe improves the stated random-pixel task.
**DEEPER ANSWER:** EXP-F showed that regularized prototype geometry helps, yet the nonlinear/transductive/spatial branch reached substantially higher internal scores. Its additional information privileges and complexity must be acknowledged. Under unavailable pool/coordinate access, a simpler frozen inductive model may be the more appropriate contract.
**KEY NUMBERS/FACTS:** Current matched EXP-F .657602; Coordinate_RF .749299 at 200. [S06,S12]
**COMMON MISTAKE TO AVOID:** Attributing the whole difference purely to classifier capacity when access and representation also change.

### 17. Why does performance improve with shots?

#### Q49
**QUESTION:** Why do more support labels generally help?
**SHORT ANSWER:** They improve estimation of target class structure and stabilize adaptation.
**DEEPER ANSWER:** A larger support set samples more target variability, gives more evidence for RF boundaries and reduces sensitivity to a few atypical pixels. The current geometry and source-prior weights also change by fixed formulas with budget. The curve is therefore the performance of a budget-adaptive procedure, not one identical fitted classifier receiving more data.
**KEY NUMBERS/FACTS:** Coordinate_RF .650253 at 5 to .749299 at 200. [S12]
**COMMON MISTAKE TO AVOID:** Claiming an individual episode must improve monotonically whenever support grows.

#### Q50
**QUESTION:** What changes in the source blend as shots increase?
**SHORT ANSWER:** The fixed source weight decreases from .5 at five shots to about .02439 at 200.
**DEEPER ANSWER:** The formula is alpha=20/(20+4b). It treats the source prior like a fixed pseudo-count relative to current support. This is a recorded heuristic, not a posterior probability derived from a proven probabilistic model and not a newly optimized lookup table for each final budget.
**KEY NUMBERS/FACTS:** alpha at 5=.5; at 200=20/820≈.02439. [S14]
**COMMON MISTAKE TO AVOID:** Calling alpha a learned confidence score or a calibrated Bayesian posterior.

#### Q51
**QUESTION:** What happens specifically at five shots?
**SHORT ANSWER:** The current model is already much stronger than its inductive controls, but adding local coordinates barely improves ASTRA.
**DEEPER ANSWER:** Coordinate_RF .650253 versus ASTRA .649964 yields only .000289 mean gain and 106/200 wins. Its paired gain interval includes zero. Most useful low-shot performance belongs to the inherited prior/geometry/spatial recipe rather than a clear extra benefit from the two local coordinate columns.
**KEY NUMBERS/FACTS:** Five-shot CI approximately [-.000077,.000667]. [S12,S14]
**COMMON MISTAKE TO AVOID:** Using the high-shot coordinate gain to claim coordinates strongly improve every budget.

### 18. Why does spatial performance vary?

#### Q52
**QUESTION:** Why can opposite directions give different results?
**SHORT ANSWER:** The two support regions and query regions have different feature/class/geographic distributions.
**DEEPER ANSWER:** A low-x support sample may cover relationships that do not hold in high-x queries, and reversing that direction changes both distributions. Coordinates are particularly sensitive to geographic extrapolation. The directional asymmetry is evidence of limited regional transfer, not something to average away without reporting the worst direction.
**KEY NUMBERS/FACTS:** High-x→low-x coordinate loss vs ASTRA about .028670. [S13]
**COMMON MISTAKE TO AVOID:** Treating x/y direction effects as random noise known to vanish with more trials.

#### Q53
**QUESTION:** Are spatial halves a fair matched comparison?
**SHORT ANSWER:** Methods are paired within a direction/trial; random-versus-spatial evaluations have different queries.
**DEEPER ANSWER:** All models in the spatial audit share its support and query keys, allowing matched model gains there. The random control shares budget and development exclusions but not query geography or composition, so its mean drop cannot be interpreted as an exact per-pixel causal effect of geography alone.
**KEY NUMBERS/FACTS:** 10 paired trials per direction; four directions. [S13]
**COMMON MISTAKE TO AVOID:** Calling random-versus-spatial bars an identical-query experiment.

#### Q54
**QUESTION:** Could you remove coordinates now to fix the spatial weakness?
**SHORT ANSWER:** Not in this frozen preparation task; changing the method would require separate predeclared evaluation.
**DEEPER ANSWER:** ASTRA already provides the matched no-local-coordinate control, and its directional mean is slightly stronger. We report that trade-off rather than select a post-audit hybrid or reverse the lock. A future deployment decision must match the intended geography and information contract.
**KEY NUMBERS/FACTS:** Coordinate_RF remains development-locked; ASTRA historical comparator retained. [S12,S13]
**COMMON MISTAKE TO AVOID:** Silently switching models after observing final spatial scores.

### 19. Why is macro-F1 used?

#### Q55
**QUESTION:** Why not report accuracy?
**SHORT ANSWER:** Macro F1 gives each class equal weight while balancing precision and recall.
**DEEPER ANSWER:** Class 2 dominates the data, so a classifier can look better under accuracy while doing poorly on minority eras. Macro averaging makes each class contribute one quarter of the score. Accuracy, per-class F1 and confusion can remain diagnostics, but must not be substituted for the organizer’s stated metric.
**KEY NUMBERS/FACTS:** Four-class arithmetic mean of class F1. [S01,S14]
**COMMON MISTAKE TO AVOID:** Calling F1 accuracy or reporting only the strongest class.

#### Q56
**QUESTION:** Is a row-normalized confusion diagonal the class F1?
**SHORT ANSWER:** No; it is recall for that true class.
**DEEPER ANSWER:** Row normalization divides by the number of true-class appearances. F1 also needs false positives from other rows and uses predicted-class totals as well. A pooled confusion matrix also weights repeated query appearances differently from an unweighted mean of per-episode class F1.
**KEY NUMBERS/FACTS:** Recall=TP/(TP+FN); F1=2TP/(2TP+FP+FN). [S14]
**COMMON MISTAKE TO AVOID:** Labelling a 75% confusion diagonal as 0.75 F1.

#### Q57
**QUESTION:** What does ±0.005716 mean in the headline?
**SHORT ANSWER:** Population SD of the 200 saved episode macro-F1 scores at 200 shots.
**DEEPER ANSWER:** It measures spread under the saved support-sampling regime with a fixed forest seed and target population. A confidence interval for the conditional mean is a different quantity; the paired gain bootstrap interval is narrower but also conditional. Neither describes uncertainty over all cities.
**KEY NUMBERS/FACTS:** ddof=0; 200 episodes/budget. [S12,S14]
**COMMON MISTAKE TO AVOID:** Saying 95% of unseen-city scores must fall within mean ±SD.

### 20. What would you do with more time?

#### Q58
**QUESTION:** What is the highest-priority next action?
**SHORT ANSWER:** Close the organizer-deliverable gap and verify the permitted inference information contract.
**DEEPER ANSWER:** The strongest research result already has publication/replay evidence, but the existing presentation is historical EXP-010 and no final-method notebook was found. Before another discovery sprint, independently prepare a correct final notebook/deck outside the frozen snapshot, clarify full-pool access, and verify the exact organizer-facing package.
**KEY NUMBERS/FACTS:** Email known; final-method notebook absent; snapshot remains frozen. [S16]
**COMMON MISTAKE TO AVOID:** Promising more optimization before a runnable, consistent required submission exists.

#### Q59
**QUESTION:** What scientific validation would matter most?
**SHORT ANSWER:** A genuinely untouched city or organizer-held-out geographic evaluation under predeclared rules.
**DEEPER ANSWER:** We would preserve current choices, define access to target covariates/coordinates, avoid post-hoc direction selection, and report failures as well as gains. More support draws on the same city would strengthen sampling precision but not answer the biggest deployment/generalization question.
**KEY NUMBERS/FACTS:** Current target population is Amsterdam only. [S12-S14]
**COMMON MISTAKE TO AVOID:** Saying 10,000 more random episodes would create independent-city evidence.

#### Q60
**QUESTION:** Would you pursue calibration or a new label-free feature pipeline?
**SHORT ANSWER:** Those are reasonable future engineering studies, not completed improvements.
**DEEPER ANSWER:** The current calibration figure is diagnostic, not a fitted calibrator. The accepted feature pipeline also needs a hidden-label-safe membership path. Any revised preprocessing or calibration changes predictions and must be separately developed and evaluated; it must not silently replace the frozen model or inherit its score.
**KEY NUMBERS/FACTS:** No calibration fitted; label-free v2 branch was rejected for the headline. [S03,S04,S14]
**COMMON MISTAKE TO AVOID:** Claiming calibration or deployment preprocessing is already solved because a figure or rejected branch exists.

### 21. What is the biggest weakness?

#### Q61
**QUESTION:** What is the biggest scientific weakness?
**SHORT ANSWER:** External validity: one historically explored target city with spatially dependent pixels.
**DEEPER ANSWER:** There is no organizer-held-out new population, and development labels plus historical audit exposure constrain generalization claims. The geographic audit shows the current coordinate addition is not uniformly better. Exact reproducibility is valuable, but it cannot replace data independence.
**KEY NUMBERS/FACTS:** Spatial mean .694216 vs ASTRA .696672. [S11-S15]
**COMMON MISTAKE TO AVOID:** Choosing only a minor runtime issue while omitting the main validity limitation.

#### Q62
**QUESTION:** What is the biggest submission risk?
**SHORT ANSWER:** The required final-method notebook is missing and the deck is not current Coordinate_RF.
**DEEPER ANSWER:** The safety snapshot truthfully preserves existing EXP-010 presentation/text and reference notebooks, with supporting code/state. It is a protected fallback, not a complete current-model submission. Its clean ZIP is intact; unsealed background OneNote files in the directory are separately reported.
**KEY NUMBERS/FACTS:** 13 intended snapshot files; final-method notebook requirement unresolved. [S16]
**COMMON MISTAKE TO AVOID:** Telling organizers a baseline notebook is the notebook for 0.749299.

#### Q63
**QUESTION:** What remains uncertain about historical provenance?
**SHORT ANSWER:** Baseline discrepancy causes, exact competitor tuned configuration and some human-review claims remain unresolved.
**DEEPER ANSWER:** Early notes sometimes state stronger causes/replication than later evidence permits. We use qualified audits and specific saved runs, not the most confident sentence. The competitor fallback near-matches a missing tuned model but does not reconstruct it; software clean processes do not establish independent-person review.
**KEY NUMBERS/FACTS:** Accepted data hash 51f11bc9…; competitor overnight_best.json unrecovered. [S03,S10,S15]
**COMMON MISTAKE TO AVOID:** Repeating an early causal story or attributing undocumented human work to balance team credit.

### 22. Strongest evidence the result is real

#### Q64
**QUESTION:** Why should we believe 0.7493?
**SHORT ANSWER:** It is the mean of a locked 200-shot protocol, backed by saved paired predictions, exact replay and metric reconstruction.
**DEEPER ANSWER:** The source/state rebuild and 4,000-array replay support implementation repeatability. Publication reconstructs all confusion/F1 records and excludes development/support from queries. Against matched ASTRA the high-shot gain is .016262 with 200/200 wins. This validates the stated internal result, not independent-city superiority.
**KEY NUMBERS/FACTS:** 0.749299 ±.005716; +.016262; 200/200. [S12,S15]
**COMMON MISTAKE TO AVOID:** Answering only with a p-value or presenting 0.7493 as organizer-scored.

#### Q65
**QUESTION:** How do you know it is not just a lucky episode?
**SHORT ANSWER:** The headline averages all 200 saved episodes at that budget, not a chosen best trial.
**DEEPER ANSWER:** We preserve the score distribution, paired wins/losses and conditional intervals. The 200-shot improvement appears across every matched ASTRA pair, whereas the five-shot coordinate difference is inconclusive. This makes a one-episode explanation implausible for the stated regime, but does not remove selection history or spatial limitations.
**KEY NUMBERS/FACTS:** 200-shot 200/200; five-shot 106/200. [S12,S14]
**COMMON MISTAKE TO AVOID:** Equating consistency across overlapping-query draws with universal generalization.

#### Q66
**QUESTION:** What failure would make you stop claiming the result?
**SHORT ANSWER:** An integrity/prediction mismatch or a violated evaluation contract would invalidate the affected claim until resolved.
**DEEPER ANSWER:** We distinguish byte changes, scientific metric reconstruction and organizer-rule compliance. If a replay fails, report and investigate without overwriting the reference; if pool privileges are disallowed, use a separately qualified inductive method rather than relabeling the transductive score. The snapshot/ZIP provide a preserved fallback, not a license to ignore missing deliverables.
**KEY NUMBERS/FACTS:** Freeze manifests; clean-reference arrays; explicit support/query boundaries. [S07-S16]
**COMMON MISTAKE TO AVOID:** Repairing or deleting inconvenient evidence and continuing to claim an unchanged validated result.


````````

</details>

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/PROJECT_NARRATIVE.md</summary>

````````text
# PROJECT MASTER GUIDE — StatsGeeks

> Team preparation, not a new experiment. Read the evidence-status language as carefully as the scores. This guide distinguishes the current **Coordinate_RF research incumbent**, the historical **ASTRA-AGF comparison**, the **EXP-010 organizer-facing fallback**, and the **reference notebooks**. They are not interchangeable.

## How to study this guide
1. Everybody: sections A, H–K and the numerical ledger; then `TONIGHT_REVISION.md`.
2. Presenter 1: problem, data, evaluation contract and opening/closing. Presenter 2: source transfer, prototypes, covariance and current architecture. Presenter 3: evidence, Gate4, spatial caveats and reproducibility.
3. Everybody: practice the question bank aloud. Give the short answer first; use the deeper answer only when asked. Say what is known, what is inferred, and what was not tested.
4. These are speaking assignments, not invented implementation credits. Exactly three member guides assign balanced coverage. Repository history documents Jaswin Chinthala and Ametor Buanyomi; a third presenter's personal contribution is not established by the records inspected.
5. The snapshot is frozen. Never update its deck or notebook while rehearsing. Draft future organizer revisions outside it under a separate task.

## Evidence map and precedence
All repository paths below are root-relative unless marked external. Bracketed IDs are source citations used throughout the study material.

| ID | Evidence | What it supports |
|---|---|---|
| S01 | `original/1-Introduction.ipynb`; `docs/building_age_transfer_learning_hackathon.md` | Task rationale and earlier organizer context; latest email instruction is supplied in the current task |
| S02 | `docs/member2_log.md`; commit `52c7357` | Original baseline execution narrative; later audits qualify several early causal/provenance claims |
| S03 | `working/member2_baseline_handoff.md`; `docs/member3_baseline_discrepancy_audit.md` | Accepted local scaler-shim artifact, notebook execution, unresolved baseline discrepancy |
| S04 | `docs/EXPERIMENT_LOG.md`; `candidate/artifacts/` | Early EXP-001–010 chronology and stored results; old “primary/ceiling” prose is historical |
| S05 | `candidate/artifacts/joint_sweep.json`; `candidate/exp010_predict.py` | Exact frozen EXP-010 numbers and deployed schedule |
| S06 | `candidate/experiments_2h/SPRINT_REPORT.md` | EXP-A–G controlled sprint, EXP-F positive result and low-shot spatial failure |
| S07 | `working/G4B-E1-001/REPORT.md` | E1 independently verified fixed-specification failure |
| S08 | `working/G4C-E2-008/EXECUTION_REPORT.md` | Latest completed E2; overrides earlier NOT_RUN/stop reports |
| S09 | `working/G4C-E3-002/EXECUTION_REPORT.md` | E3 production completed, coordinator FALSIFIED, independent validation blocked |
| S10 | Own external-quarantine `COMPARABILITY_AUDIT.md`, `FORENSIC_TRACE.md`, `SEARCH_SCOPE_ADDENDUM.md` | Competitor claim versus mechanism reproduction, missing configuration, latest locally evidenced update |
| S11 | `candidate/experiments_2h_v2/README.md`; `FINAL_SELECTION.json`; `final_100.json` | Historical ASTRA-AGF recipe and 100-trial protocol |
| S12 | `candidate/autonomous_runs/20260909_1727/SELECTION_LOCK.json`, `configuration.json`, `FINAL_REPORT.md`, `final_complete.json` | Current development lock, final 200-trial-per-budget results and disclosures |
| S13 | Same run's `spatial_complete.json`; `candidate/reports/SPATIAL_ANALYSIS.md` | Four-direction current geographic trade-off |
| S14 | `candidate/reports/METHODS.md`, `RESULTS.md`, `STATISTICAL_ANALYSIS.md`; `candidate/tables/` | Current publication definitions, conditional statistics and diagnostics |
| S15 | `candidate/reproducibility/final_validation.json`; `candidate/publication/distribution_test_receipt.json`; original `clean_replay/verification.json` | Protected files, exact numerical replay, isolated archive test |
| S16 | `candidate/team_preparation/SNAPSHOT_SEAL.json`, `SNAPSHOT_PROTECTION.json`, `INSPECTION_AND_SUBMISSION_DECISION.md` | Actual fallback contents, hashes, notebook gap and OneNote exception |
| S17 | Git history; `docs/member2_log.md`, `member3_log.md`, `member4_log.md` | Attribution; logs explicitly record one member covering several scopes |

Precedence rule: use specific validated run artifacts over an older “FINAL” filename; use later qualified audits over early confident explanations; use source code for algorithm details; never infer that a new seed means a new city. Earlier reports remain true descriptions of their point in the project, not current recommendations.

## Executive summary: what we can defend
We predict four construction-era classes for 30 m Landsat pixels, using labelled Madrid data and small class-balanced Amsterdam support sets. Our early work transferred Madrid feature relevance and class geometry into target prototypes. Later independently implemented research used a richer local classifier, unlabelled-target covariance, a contextual source prior and geographic smoothing. The current development-locked Coordinate_RF adds two standardized coordinate columns to ASTRA's 60-input local RF, while retaining its prior, adaptive covariance and Gaussian graph.

At 200 shots/class, Coordinate_RF has **0.749299 ± 0.005716 macro F1**, versus matched ASTRA **0.733037**; paired gain **+0.016262**, **200/200 wins**. This is strong conditional support-sampling evidence on the stated random-pixel target population. It is **not** an independent organizer-held-out city/test. At five shots the ASTRA difference is tiny and inconclusive. On spatial separation the coordinate model's four-direction mean is **worse**, 0.694216 versus 0.696672, and the worst direction is also worse.

Operational warning: the existing 17-slide presentation and written justification still describe EXP-010. No final candidate notebook exists in the inspected repository. The sealed fallback preserves that older coherent pair and explicitly labelled reference notebooks; it must not be sold as a complete current-model submission. [S05, S12–S16]

## Chronological reconstruction — do not confuse parallel branches with a single run

| Recorded period / milestone | What the evidence says | Source / caution |
|---|---|---|
| 8 September 2026 | Repository setup, reference preprocessing/modelling and the first source-learned candidate were recorded. | Git `165fe11`, `52c7357`, `f9dce46`; later local audits qualify historical input/version claims. |
| 8 September 2026 | Representation search, audit disclosure, reload checks and first presentation drafts followed. | `96435da`, `b6615dc`, `115e294`, `177f11c`; separate commit and execution clocks are not interchangeable. |
| 9 September, early development commits | Season/coverage features and fresh-draw support tests, then prototype shrinkage and joint k/lambda development. | `5f4cd4b`, `7faee9f`, `c53275c`; EXP-010 commit recorded 10:37:31 +02:00. |
| Parallel Gate4 line, before/around integration | Fixed E1/E2/E3 evaluations accumulated alongside infrastructure/provenance work. | E3-002 records 08:50:21–09:52:00 UTC; this overlaps the other branch's morning work, not a clean sequential experiment ladder. |
| 9 September integration | Baseline branch merge, documentation and Gate4 framework were committed. | `fc463e5`, `0179d59`, HEAD `7f012bb`; later autonomous artifacts remain uncommitted worktree evidence. |
| Later 9 September controlled sprint | EXP-A–F completed; EXP-G blocked; EXP-F retained for review without changing the EXP-010 presentation. | `experiments_2h/SPRINT_REPORT.md`; exact run identities, not guessed wall-clock ordering. |
| 9 September forensic / ASTRA research | Locally recorded competitor weighted-smoothing update, separate mechanism audit, independently implemented ASTRA and its locked 100-trial evaluation. | Competitor commit `cf9af6c` 14:23:35 +02:00; historical ASTRA evidence remains a different protocol. |
| Current autonomous lock | Coordinate_RF chosen under the support-development rule; lock records 2026-09-09 17:50:37 without an explicit timezone. Final query scoring followed the lock. | `autonomous_runs/20260909_1727/SELECTION_LOCK.json`; do not convert an unspecified local timestamp to UTC by assumption. |
| 9 September 18:39:47 UTC | Final publication ZIP sealed, later independently extracted for inference/evidence replay. | Existing distribution receipt; no model optimization in publication. |
| 9 September 19:08:50 UTC | This task created the pre-overnight fallback seal, then team-preparation guides. | `SNAPSHOT_SEAL.json`; no new model fitting/predictions; final-method notebook gap disclosed. |

The story below is organized by mechanisms so it can be presented coherently. That organization must not be mistaken for proof that all development, Gate4 and integration work happened serially or was personally implemented by one speaker.

## A. Problem definition
### What building-age prediction means
The target is a categorical construction-era label, not an exact year or a prediction for each individual roof. Each observation is a roughly 30 m satellite pixel, which can contain buildings from several periods plus vegetation, roads or water. A weighted mean construction year is converted into one of four city-specific classes. A mixed pixel's assigned class can summarize a collection of buildings rather than identify any one building exactly.

Building-age information can inform retrofit planning, energy-use understanding and urban development analysis where records are incomplete. This motivation is not evidence that the model is deployment-ready or fair across neighborhoods. The study is a benchmark on the supplied data. [S01, S03]

### Source city versus target city
Madrid is the labelled **source**: it supplies learning that should help elsewhere. Amsterdam is the **target**: an episode supplies only a small labelled support sample, and predictions are evaluated on other eligible pixels. Both cities have labels in the research data, but availability in a file is not permission to give them all to the estimator.

Different architecture, historical class cutoffs, land cover, sampling season and observation distributions create domain shift. A rule learned in Madrid may assign Amsterdam pixels incorrectly even if it performs well within Madrid. The project therefore needs adaptation, not merely a source score. [S01–S04]

### Why transfer and few-shot learning
Transfer means Madrid-supervised information actually enters Amsterdam prediction. Few-shot means each episode has b labels/class, for b in {5,25,50,100,200}; with four classes, total labelled support is 4b. Five shots means **20**, not five, target labels. Two hundred shots means **800**, not 200 total. The current method additionally used an **800-label fixed development bank** during research selection. That is separate supervision and must be disclosed rather than hidden behind the episode budget. [S12]

### Metric in plain language and equations
For a class, precision asks how often a predicted label is right; recall asks how many true members are found. F1 is their harmonic mean, `2TP/(2TP+FP+FN)`. Macro F1 averages the four class F1 values equally. It avoids letting the largest class dominate the summary as much as raw accuracy would, although it does not itself remove class imbalance or spatial dependence.

A row-normalized confusion diagonal is **recall**, not F1. The mean of episode macro F1 is not generally equal to macro F1 computed from one pooled confusion matrix. Population SD describes how scores vary across the episode draws; it is not automatically a confidence interval for an unknown-city performance mean. [S14]

## B. Starting point: what the baseline actually did
### Data and preprocessing
The accepted artifact has 76,263 Madrid pixels and 25,992 Amsterdam pixels, each with 60 ordered features. The raw panels contain roughly 3.17 million and 1.06 million pixel-year rows; these must not be called millions of independent buildings. Locally observed years are 1984–2025, 42 distinct years, despite earlier explanatory text saying 1984–2024.

The reference workflow selects QA-valid annual band values from available observation slots, screens extreme blue-band haze, interpolates missing annual observations, forms five spectral indices, aggregates temporal statistics and applies Madrid-fitted standardization. Six base bands are Blue, Green, Red, NIR, SWIR1 and SWIR2. The 60-column contract includes overall, early/late, annual-change and availability features. One availability column is constant in the observed data; “60 inputs” is the interface width, not a proof of 60 useful independent signals. Do not say the other 59 are all established as informative.

Class counts in Amsterdam are 7,568 / 8,802 / 6,745 / 2,877 for classes 1–4. Madrid counts are 13,794 / 27,152 / 18,672 / 16,645. Class 2 is the largest in both cities. Madrid's oldest-class division is 1960, Amsterdam's 1945, with later cutpoints 1984 and 2004. Exact boundary inclusion follows code, not casual interval notation. [S02, S03]

### Source RF, zero-shot and target-only prototypes
Notebook 4 trains a class-balanced 500-tree Random Forest on Madrid, evaluates repeated Madrid CV, and applies the source model directly to Amsterdam for zero-shot context. But its few-shot prototype path does **not** consume the trained RF. It computes Amsterdam support class means and uses nearest Euclidean distance. Madrid contributes scaling but not supervised feature relevance or learned class structure to that path. This is why a target-only prototype is the right equal-support control; outperforming zero-shot alone would not prove transfer.

Organizer-saved Madrid CV is **0.6179 ± 0.0043**, with Amsterdam zero-shot **0.3427**. Measured local reference-protocol values are **0.6281 ± 0.0043** and **0.4433**. The local prototype curve matches the saved reference at displayed precision: 0.5437 at five shots and about 0.6150 at 200, with intermediate 0.5986/0.6079/0.6129 at 25/50/100. These are a different episode protocol from the later EXP-010 and Coordinate_RF evaluations.

Early logs attributed the RF discrepancy too confidently to package versions. The later discrepancy audit says the precise cause is **not identifiable** from available historical input/package provenance. Stable repeated numbers in some early records are not sufficient to establish source/input equivalence on the later local shim artifact. Do not tell a judge “we proved it was sklearn.” [S02–S04]

### Baseline weaknesses worth understanding
- Label-dependent feature construction filters/groups using class metadata. This creates an unavailable-label deployment-path problem even though `age_class` is not an RF input column.
- Madrid scaling occurred before CV folds, so the reference CV preprocessing is not fold-safe.
- The reference notebook saved no deployable source RF or adaptation state by itself; recoverability needed separate work.
- Support draws were not stored/nested by the original starter in the way later matched candidate episodes were.
- Fine-grained building/parcel IDs were unavailable for a building-disjoint geographic audit.
- A plateau near 0.62 in the early prototype family was once interpreted as a possible ceiling. Later stronger transductive methods disprove treating **0.62 as a universal ceiling**. The early statement is a hypothesis that did not survive broader evidence. [S03, S04, S11, S12]

## C. EXP-010: how the frozen fallback was built
### Early representation work
Commit `f9dce46` introduced source-learned representations and matched episodes. `rfw` weighted inputs by square-root Madrid RF importance; initial audit gains were small but consistently positive. Subsequent representation search compared compact feature selection, within-class whitening, source probability/logit embeddings, LDA and RF-related representations. This did not establish that every sophisticated method was superior: a probability-space representation lost about 0.0611 mean macro F1 on the recorded selection comparison and won only 2/25 pairs. Compressing to source class outputs may discard target-relevant distinctions; that is a plausible interpretation, not a general theorem against dimensionality reduction.

Whitening showed budget dependence: `wcw10` changed from roughly −0.0218 at five shots to +0.0090 at 200 in the recorded comparison; whitening-plus-RF-weighting changed from −0.0131 to +0.0131. Small support sets make geometry/prototype estimation fragile. Another top-30 audit returned 19/25 wins, less than its selection promise. Repeated audit exposure was disclosed rather than treated as a pristine test. [S04]

### EXP-006–008 and the rejected feature expansion
A 94-feature seasonal/coverage branch measured median acquisition days 175 in Madrid versus 105 in Amsterdam—a 70-day difference. Its label-free builder separated label derivation from feature construction, an engineering improvement. But the broader feature set did not reliably improve F1: about +0.0001 selection mean and 8/25 audit wins, worse at four of five budgets. It was not adopted. “Feature dilution” is a possible mechanism; the outcome alone does not prove that causal account.

EXP-008 provided a fresh-episode supporting test of a fixed earlier representation, 19/25 wins. Those are fresh draws from the same target population, not a new city or exact independent replication of EXP-010, which was developed afterward. [S04]

### EXP-009 and EXP-010 mechanics
A source RF learns a feature ranking/importance vector on Madrid. Inputs are weighted by square-root feature importance so squared distances weight by the importance itself. The target support mean recenters source class offsets, helping separate transferable *relative class geometry* from an absolute city location shift.

Let `delta_c` be Madrid class-c mean minus Madrid overall mean in the selected weighted space. Let `m_s` be the Amsterdam support mean and `mu_c` its support class mean. The EXP-010 prototype is `m_s + lambda*delta_c + (1-lambda)*(mu_c-m_s)`. Predictions use squared Euclidean distance to these prototypes. At lambda zero this reduces to support-only class means—but the representation still transfers Madrid-supervised ranking/weights.

The frozen schedule is **k=30, lambda=0.6 at five shots** and **k=45, lambda=0 otherwise**. The RF has 500 trees at source learning; it is **not** a 500-tree local target classifier in EXP-010. Its small 6,221-byte adaptation artifact stores learned summaries, not the original full forest. The different legacy `stage1_madrid.pkl` must not be substituted. [S05]

### Exact historical EXP-010 result
Ten seed-31337 audit episodes/budget, mean ± population SD:

| Shots/class | EXP-010 | Matched full-feature target-only control | Gain | Wins |
|---:|---:|---:|---:|---:|
| 5 | 0.552428 ± 0.059539 | 0.515220 ± 0.070198 | +0.037208 | 7/10 |
| 25 | 0.612174 ± 0.013057 | 0.608872 ± 0.014539 | +0.003302 | 8/10 |
| 50 | 0.617273 ± 0.007839 | 0.613500 ± 0.008332 | +0.003773 | 10/10 |
| 100 | 0.619513 ± 0.004770 | 0.614502 ± 0.004810 | +0.005011 | 10/10 |
| 200 | 0.623982 ± 0.003646 | 0.618943 ± 0.003824 | +0.005040 | 10/10 |

Safe historical headline: **45/50 paired wins**. Do not use the provenance-limited “47/50” or “9.7%” comparison. Five selection trials and repeated target exposure limit selection claims; separate seed values do not make query pixels independent. Freezing protected a reproducible known result against more speculative changes and gave the team an explainable fallback. Later research did not retroactively change those arrays. [S04, S05]

## D. EXP-F and controlled alternatives
The first controlled sprint kept EXP-010 rather than automatically promoting its highest scoring new arm. EXP-A compared fixed source/local combinations; EXP-B crossed dimensions and shrinkage; EXP-C diagnosed class errors; EXP-D used spatial separation; EXP-E examined three temporal contrasts; EXP-F changed the support distance metric; EXP-G was blocked because full-pool privileges were not explicitly confirmed at that stage. Do not describe a blocked experiment as a failed model.

EXP-F uses compact Madrid-ranked/weighted inputs, support class means and a pooled within-support residual covariance `C=R.T R/(4b-4)`. Its inverse metric is based on `0.5 C + 0.5 trace(C)/k I + 1e-8 I`. This regularizes noisy correlations toward an isotropic distance. It does not use query-pool covariance or train a new local RF.

Historical reused-audit EXP-F at 200 shots: **0.658664 ± 0.004417**, gain +0.034681 over paired EXP-010, 10/10 wins. At 25: **0.638010 ± 0.014197**, gain +0.025835, 10/10 wins. But at five-shot spatial evaluation it scored **0.507618**, losing **0.025769** to the matched EXP-010 control. Its better random-pixel high-shot mean was therefore not a defensible all-budget promotion on its own. No new EXP-010-at-five/EXP-F-elsewhere hybrid was validated from that report. [S06]

Concrete lessons: correlation-aware metrics can help; diagonal-only normalization is not equivalent; low-shot covariance is unstable; source blending is not uniformly beneficial; class diagnostics guide interpretation, not permission to fit post-hoc class thresholds. The most difficult classes under one early low-shot protocol were not necessarily the same bottleneck under every later classifier.

## E. Gate4: experimental discipline, not a winning model name
### What the gates were for
Gate4 sought trustworthy fixed-specification tests with frozen episode manifests, constrained worker information, separate privileged scoring, immutable source state, exact hashes and clean-process teardown. These controls answer “was this exact experiment run under its stated boundary?” They do not answer “is this model superior?”

Different stopped/preflight identities remain in the tree. A filename like `G4C-FINAL-REPORT.md` reports an earlier NOT_RUN stop and must not override the later completed E2-008/E3-002 reports. Ten shots appears here as an extra diagnostic budget: 60 episodes means 10 trials at **six**, not five, budgets. [S07–S09]

### E1 — source within-class covariance geometry
E1 used 59 source-nonconstant dimensions and a fixed class-balanced within-class covariance shrunk as `0.9 W + 0.1 trace(W)/d I`. U0 was a total-source-covariance control; raw P0 and same-query frozen RF were retained. At the predeclared primary 25 shots, E1 scored **0.59008 ± 0.03214** versus raw **0.59860 ± 0.01764**, gain **−0.00852** and 4/10 positive pairs. It failed the +0.0100 threshold and class-regression safeguards despite beating the source zero-shot control. **FALSIFIED for that fixed specification**, independently reconstructed. High-shot gains could not move the goalposts. [S07]

### E2 — restrained source Fisher feature weighting
E2 estimated per-feature between-class/within-class variance ratios on Madrid, normalized/clipped them and mixed with identity weighting. Its fixed epsilon was 1e-6, clip [0.25,4.0], identity mixture 0.5. It classified by weighted support-prototype distances, not a target RF.

The latest complete identity E2-008 scored **0.603550 ± 0.015364** at 25 shots versus raw **0.598598 ± 0.017637**: **+0.004953**, 10/10 positive pairs and no mean per-class regression. That failed the preregistered **+0.0100** mean-gain requirement. Verdict: **INCONCLUSIVE / does not meet the success criterion**, not “promising” and not proof of a zero effect. Independent exact reconstruction passed all 60 records. A verifier-only advanced-indexing fix did not rerun or alter candidate predictions. [S08]

### E3 — target-support translation toward frozen source RF geometry
E3 computed source class means and a fixed support-derived translation on 58 continuous coordinates, leaving the two availability indicators unchanged, then used the frozen source RF. Production completed all 60 episodes. At 25 shots its coordinator reported **0.509079 ± 0.020012**, raw **0.598598**, delta **−0.089519**; all ten raw comparisons lost and class 1 suffered severely.

The frozen coordinator's verdict is **FALSIFIED**, but independent scientific validation stopped at **`Original tree dirty` before prediction/metric reconstruction**. Do not say “E3 was fully independently verified,” and do not claim the score itself was caused by an integrity failure. Execution/protocol/serialization checks and scientific reconstruction are separate layers. This is a negative production result with incomplete independent certification. E4/E5 were not subsequently run in the cited path. [S09]

### What survived Gate4
Useful outputs were not winning parameters: manifest binding, explicit class order, same-query controls, worker teardown, packet/hash checks, distinction between NPZ container bytes and array identity, and respect for stop conditions. A successful infrastructure certificate is not scientific superiority; a failed integrity gate is not automatically corruption of protected model bytes. The careful vocabulary protected the project from overstating its evidence.

## F. Competitor forensics: learn the comparison boundary, not a copied solution
### What is actually evidenced
Our own forensic audits identify the latest **locally evidenced** competitor branch commit as `cf9af6cffea292af9460bf572de33c32a10212d9`, dated 2026-09-09 14:23:35 +02:00. No remote fetch occurred in this preparation task. Therefore “latest” means latest recorded local evidence—not a live claim about what the other team has done since.

The recorded competitor progression was approximately **0.717 unsmoothed**, then **0.7259 ± 0.0049** with uniform smoothing, then a final claimed **0.7373 ± 0.0053** at **200 shots/class, 20 episodes** after distance weighting. The last update is a real reported improvement over the earlier uniform smoother; it would be inaccurate to say nothing changed. But there is **no locally demonstrated subsequent breakthrough beyond that claim**, and exact tuned-config reproducibility remains unresolved. [S10]

### Why headline subtraction is misleading
Frozen EXP-010 used 10 nested seed-31337 episodes and compact source-ranked features, without full-pool fitting. The competitor used 20 seed-42 draws with RNG reset per budget, support-complement queries, a different feature representation, full-target distribution information, pseudo-label alignment and spatial smoothing. The headline evaluates the full target population including earlier tuning regions; it is not an untouched half-test score. Same city, class labels, budget and metric are necessary but insufficient conditions for a fair paired comparison.

The reported winning `overnight_best.json` was missing from searched sources. A broad user-profile search timed out; that is limited search evidence, not proof the file exists nowhere. Our historical isolated original-code **fallback mechanism reproduction** reached **0.736392 ± 0.004722** using 108 features and a documented fallback configuration, not the unrecovered tuned winner. The literal 60-feature fallback already reached about **0.735655** at 200, so “48 extra features explain all of 0.73” is unsupported. Exact original raw-file provenance was also incomplete. [S10]

### What our comparison established—and what it did not
Historical ASTRA on the same 20-draw convention scored **0.737388** versus the reproduced fallback **0.736392**, a **+0.000995** mean difference and **13/20 wins**. It was worse at 5, 50 and 100 on that comparison. This is near parity at high shot count, not universal competitor dominance or an exact comparison to the missing tuned model.

Current Coordinate_RF's 0.749299 comes from a **different** 200-trial protocol excluding the development bank. Do not subtract 0.7373 and call the result a paired competitive advantage. We can discuss the method's own matched controls without needing a competition leaderboard claim. [S10–S12]

### What was learned and what was not copied
The investigation pointed to information regime, local nonlinear capacity, covariance geometry, pseudo-labelled source alignment and spatial processing as important mechanisms. Our subsequent candidate implementation uses the repository's own 60 inputs, a 120-input contextual source prior, one conditional alignment iteration, 200-tree forests, a dimension/support-ratio covariance schedule and Gaussian graph weights. It does not import the competitor implementation, reproduce its 108-feature list verbatim, or claim its unavailable tuned configuration.

Be honest about mechanism inspiration: **“independently implemented” does not mean “we never inspected another method.”** Historical forensic execution of original competitor code was separately recorded and quarantined. It is not part of our model implementation, current publication evidence or safety snapshot. No competitor figures, documentation, workflows, source code, predictions or data were copied into the organizer fallback. Absolute originality cannot be proved by a filename scan; the claim rests on reviewed own-source implementations and preserved provenance. [S10, S12, S16]

## G. ASTRA-AGF in three levels
### Ten-second explanation
“We adapted both the decision rule and the feature geometry to the target, reused a source prior, and averaged predictions locally without using query truth.”

### Plain-language stages
1. **Source prior:** use Madrid labels to provide an informed initial probability over the four target classes.
2. **Target geometry:** estimate how the unlabelled target features vary together so distances/axes are less dominated by redundant features.
3. **Budget adaptivity:** at tiny support counts, stay close to diagonal scaling; at larger counts permit more covariance structure.
4. **Support RF:** learn nonlinear target class boundaries from the current support labels rather than forcing every class into one prototype.
5. **Blend:** trust the source more when support is scarce and progressively less as support grows.
6. **Spatial smoothing:** aggregate neighboring predicted probabilities using coordinates; never clamp query labels or use ground-truth spatial anchors.

### Exact inherited recipe
Recover raw units from the saved scaler. Concatenate 60 raw features with their available 3×3 lattice-neighbour averages, yielding 120 contextual source-prior features. Globally transport source mean/covariance to the target, fit a balanced 200-tree RF with leaf size 2, pseudo-label target rows, then perform one class-conditional alignment/refit where the target pseudo-class is sufficiently populated. The resulting target prior is cached.

For b shots/class, local covariance shrinkage is `rho=min(1,60/(4b))`; use `(1-rho)C + rho diag(C) + 1e-7 I` to whiten the pool-centred 60 inputs. Fit a balanced 200-tree support RF, leaf size 1, square-root feature subsampling, seed 42. Blend with source weight `alpha=20/(20+4b)`. Apply one Gaussian averaging pass over self plus eight nearest lattice neighbors with sigma 1 key unit. The 120-context inputs belong to the source prior; the original local ASTRA head has 60—not 120—inputs. [S11, S12, S14]

### Why the method was interesting
It improved the much narrower prototype family while exposing its information advantages explicitly. Historical locked ASTRA reached **0.735239 ± 0.005406** at 200 under 100 newly seeded support trials/budget, seed 104729. That number stays historical. The inherited recipe was historically audit-selected; later locking and new seeds improve procedural clarity/repeatability but do not erase that exposure. [S11]

## H. Coordinate_RF: the current development-locked research incumbent
### The actual change
Append **two** standardized coordinate columns to the local RF inputs after adaptive whitening. Coordinates are centred and standardized using the full target pool, with standard deviations bounded below by one. The local head therefore has **62 inputs**. The contextual source prior remains 120-dimensional; forest settings, prior weighting and Gaussian graph remain unchanged. No new spectral features, query labels, class-specific thresholds or ground-truth geographic anchors were added. [S12, S14]

Coordinates were considered because nearby neighborhoods can share development history and spectra alone may not capture all regional structure. That hypothesis can work for random pixels yet fail under geographic extrapolation, exactly the distinction tested by the spatial audit. Coordinates are not proof of building identity or chronological causality.

### How selection was controlled
A fixed 800-label bank (200/class, seed 20260909) was used for support-only development. Initial five folds used 160 train/40 validation per class. Promising candidates underwent 20 repeated holdouts at 5/25/50/100/160 train shots and support-only directional safeguards. Final lock records Coordinate_RF and ExtraTrees as the top ranked options; Coordinate_RF's locked 160-shot repeated-holdout mean was **0.779338**, versus ASTRA **0.771304**, gain **0.008034**, 15/20 paired wins. These are development-support scores—not the final 200-shot query result.

The lock requires a 160-shot gain >0.002, at least 70% paired wins, no other budget worse by more than 0.005, and geographic mean/worst safeguards on the development bank. Passing that development check does not guarantee the later final spatial audit will improve. The rule/configuration were not changed after final-query scoring. [S12]

### Why call it incumbent carefully
Coordinate_RF is the **development-selected packaged research model** for the stated random-pixel/full-pool regime. It is not an officially scored organizer winner, not a universal spatial replacement for ASTRA, and not the model in the existing EXP-010 deck. Team members should always qualify “best” with protocol and scope. Model development is frozen in this preparation task.

## I. Current locked numerical ledger
Mean macro F1 ± population SD, **200 paired episodes per budget**, final seed **20260910**. All eligible final queries exclude the fixed development bank and current support. These values match the user-supplied target table and authoritative saved results; no stronger superseding validated result was found.

| Shots/class | Coordinate_RF | Gain vs matched ASTRA | Wins vs ASTRA |
|---:|---:|---:|---:|
| 5 | **0.650253 ± 0.011246** | +0.000289 | 106/200 |
| 25 | **0.687664 ± 0.012145** | +0.005045 | 171/200 |
| 50 | **0.708436 ± 0.011277** | +0.009213 | 193/200 |
| 100 | **0.729839 ± 0.008802** | +0.013803 | 200/200 |
| 200 | **0.749299 ± 0.005716** | **+0.016262** | **200/200** |

At 200: matched ASTRA **0.733037**; EXP-010 **0.622840**; EXP-F **0.657602**. Gains: **+0.016262 / +0.126459 / +0.091697** respectively. These comparisons are paired within the current run, not subtractions from old 0.735239/0.623982/0.658664 means.

The 200-shot paired-bootstrap 95% gain interval versus ASTRA is approximately **[0.015856, 0.016669]**. At five shots it is approximately **[-0.000077, 0.000667]**; paired t p≈0.125, Wilcoxon p≈0.255. The five-shot advantage is not statistically persuasive or practically substantial. Fifteen paired comparisons were analyzed, with Holm correction separately across the t-test and Wilcoxon families. Effect sizes are conditional: a large paired Cohen dz reflects small paired-difference variance, not an enormous transferable city-level effect. [S12, S14]

### Spatial ledger: memorize the exception, not just the win
At 200 shots, ten trials per direction, ten-key buffer:

| Diagnostic | Coordinate_RF | Matched ASTRA |
|---|---:|---:|
| x-half mean | 0.682326 | 0.687017 |
| y-half mean | 0.706106 | 0.706326 |
| worst directional mean | 0.644816 | 0.658183 |
| four-direction mean | **0.694216** | **0.696672** |

High-x support to low-x query loses about **0.028670** versus ASTRA. Do not describe Coordinate_RF as geographically robust without immediately giving the comparator/caveat. The random-pixel control has a different query geography; random-versus-spatial differences are not exact same-query paired effects. Lattice-key units are the authoritative buffer units; do not casually substitute metres without a verified mapping. [S13]

## J. Reproducibility: several claims, several levels
### Episodes and labels
The final harness constructs class-stratified support sets from eligible labels using seed 20260910, one permutation per class/trial with nested prefixes across budgets. Query is the eligible complement. It excludes all 800 development pixels from every final query. The 1,000 episodes are 200 trials × five budgets; 4,000 saved prediction arrays reflect four methods—not 4,000 independent experiments or cities.

Stratified episode construction uses labels to select the support samples; this is an evaluator function, not evidence that all those labels entered model fitting. Fitting receives Madrid source labels or current support labels only. Historical audit selection is a separate exposure that remains disclosed. The feature builder's label-dependence is yet another issue and cannot be waved away by saying the estimator has no query-label argument.

### Model and pool identity
Current model code SHA256: `26b2299ad50dcf935fb8bc1a89d4e79f82cf2c68881619a6eaf1330f813a7533`.

Current pool SHA256: `b975db430b4a00d1c90d59d10a76ef11a6c3727be42e22f41bec49a6f6c28007`.

Frozen EXP-010 state SHA256: `2f4dc0f7a84ea54e967d7a96573b349331e1777ddb0a4a46e4925cad7bd6d266`.

Accepted preprocessing SHA256: `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`.

The older preprocessing digest `f6f588c4…` in early member logs belongs to a different recorded artifact. Do not replace the accepted digest with it. Hashes bind bytes; they do not prove scientific correctness or make unknown pickle files safe to deserialize. [S03, S05, S12, S15]

### Clean replay evidence
The completed original fresh-source replay rebuilt eight state arrays and matched **4,000 prediction arrays across 1,000 episodes**. Publication later used ten fixed-reference ASTRA/Coordinate_RF calls for exact checks and observational runtime/importance diagnostics, recalculated all 4,000 confusion/F1 records, checked the 1,000 support/development exclusions, and verified 1,622 protected files in that publication freeze scope. Its distribution validator sealed 1,856 files after final additions.

The final publication ZIP was extracted outside the research repository, with no Git directory. Five packaged Coordinate_RF reference predictions passed and every rebuilt publication CSV was byte-identical. This is strong evidence of portable *inference/evidence replay under the tested environment*, not a claim that every Python version/platform will produce bit-identical bytes. Figure/PDF metadata and runtime measurements need not be byte-identical when regenerated.

This current preparation task performed **no new fitting or prediction**. It inspected those existing receipts and made read-only hash/static checks. Snapshot hash counts use a new, different scope: **13 intended files**, not the historical 1,622/1,856 counts. Explain the scope before quoting a count. [S15, S16]

### Runtime and interpretability boundaries
Current publication runtime instrumentation covered ten fixed-reference RF-method calls, not an optimized performance benchmark. Reported sampled peak RSS is not guaranteed OS high-water memory; local RF fit/predict timing excludes source-prior refit and does not account for all transform/smoothing time. All-model historical call times exist, but separate historical CPU/memory and fit/predict measurements do not.

Coordinate_RF impurity importance was observed from verification fits. The 60 whitened axes mix original features; they cannot be labelled as direct raw spectral feature importance. Coordinate split usage is not causal attribution. Calibration plots use existing probabilities for ASTRA/Coordinate_RF on one predeclared 200-shot episode; no calibrator was fitted and baseline hard predictions cannot yield probability calibration. Transfer-stage bars likewise show internal stages on one shared episode, not independently tuned causal interventions. [S14]

## K. Limitations we should volunteer
1. **No independent organizer-held-out city/test:** final data are the same Amsterdam population used throughout research.
2. **Historical selection exposure:** inherited ASTRA was audit-selected. The newer fixed bank/lock improves the protocol without erasing that history.
3. **Extra development supervision:** 800 labels beyond any one episode's budget were used during model selection.
4. **Spatial sensitivity:** coordinate gains under random pixels do not imply geographic extrapolation gains; our own spatial comparison is worse.
5. **Transductive assumption:** the full ordered target pool and coordinates are needed. Organizer approval for that privilege is not established by a message about submitting slides/notebooks.
6. **Deployment feature issue:** the accepted 60-feature preprocessing remains label-dependent; a rejected label-free feature branch does not automatically fix the current production path.
7. **Reference CV limitation:** scaling was fitted before source folds. Current target results should not be conflated with unbiased source CV.
8. **Label and unit semantics:** mixed building-age labels, city-specific old-era boundaries and unavailable building/parcel IDs limit interpretation.
9. **Competitor uncertainty:** missing tuned config, incomplete original data provenance and no new remote check prevent exact/current leaderboard claims.
10. **Reproducibility limits:** exact tested replay is not every-platform compatibility, independent human verification, raw-data permission or proof of absence of every conceivable leak.
11. **Optional source-rebuild archive dependency:** static inspection found the publication ZIP contains a preprocessing pickle referencing `working.minimal_standard_scaler` but not that module. Its optional `verify_source.py` therefore has an unresolved standalone import dependency. This does not undo the tested inference/evidence replay, which does not load that pickle; do not claim every optional source-rebuild command is self-contained.
12. **Submission readiness gap:** a model artifact and publication ZIP are not the requested final notebook. The safety fallback is preserved with explicit gaps.
13. **Snapshot directory metadata:** seven unsolicited OneNote indexes appeared after sealing. Intended files are unchanged; the protected ZIP is the exact clean fallback. Do not create a new ZIP from the whole directory and include those indexes. [S03, S10–S16]

## L. Concrete lessons from the journey
- **Transfer needs an information path.** Training a Madrid RF somewhere in a notebook is not enough if the target classifier ignores it.
- **Use an equal-support comparator.** Beating zero-shot with 800 target labels is not a clean proof of useful source transfer.
- **Few-shot geometry is fragile.** Whitening/source offsets help or hurt depending on the sample budget and representation; frozen formulas matter.
- **More columns are not automatically better.** The 94-feature negative result beat the intuition, not the original representation.
- **Do not promote a score without its access regime.** A pool-aware spatial RF and an inductive prototype have different privileges.
- **Coordinates encode useful structure and brittle shortcuts.** Both are compatible with the observed random/spatial trade-off.
- **A negative preregistered test is useful.** E1 failed despite beating RF; E2's consistent small gain still missed the predefined practical threshold.
- **Separate implementation validation from scientific validation.** E3 illustrates why a completed worker log is not a full independent scientific pass.
- **Preserve failures.** Numerical RF ties, verifier bugs, blocked runtime checks and missing configs should not be erased to make a clean story.
- **A hash is a contract about bytes.** Source code, pool state, feature order, episode indices and environment all matter; an unchanged seed alone is insufficient.
- **New seeds are not new data distributions.** More episodes can tighten conditional sampling estimates while leaving deployment uncertainty unchanged.
- **Stop when packaging is the bottleneck.** The current missing notebook is a more immediate organizer-delivery risk than an extra decimal point of F1.
- **Attribution and insight are different.** Everyone can understand and defend the method without claiming authorship of another member's code.
- **Scientific stories should update.** The old hypothesized 0.62 ceiling and categorical version-drift explanation are not current facts.

## M. Presentation strategy and rehearsal
### Choose the story before choosing the slides
There are two possible narratives, and mixing them is the main risk:
- **Immutable fallback:** existing EXP-010 deck/text, historically matched 45/50 result, plus explicitly reference notebooks. Do not announce 0.749299 while displaying that deck as if it implemented the result.
- **Current-research presentation plan:** a future separately approved deck/notebook package would explain Coordinate_RF, its development supervision and its spatial trade-off. The plan below is a rehearsal outline, not a claim that those slides already exist.

### Recommended current-research story arc (10 content slides, adjustable to organizer time)
| Slide | Purpose | Lead | One point to land |
|---|---|---|---|
| 1 | Problem and honest abstract | Member 1 | Building-era transfer with little target supervision |
| 2 | Data, source/target, budget and metric | Member 1 | Four classes; b/class; macro F1; one target city |
| 3 | Baseline flaw and EXP-010 bridge | Member 2 | Madrid-supervised ranking/geometry must actually reach target predictions |
| 4 | What experiments taught us | Member 2 | Covariance helps at some budgets; feature expansion and several hypotheses failed |
| 5 | ASTRA mechanism diagram | Member 2 | Prior + adaptive covariance + support RF + Gaussian smoothing |
| 6 | Coordinate_RF change and selection lock | Member 2 | Only two local coordinate columns; bank/lock before final scoring |
| 7 | Current paired learning curves | Member 3 | 0.749299 at 200; +0.016262 vs matched ASTRA; five-shot gain inconclusive |
| 8 | Spatial challenge | Member 3 | Four-direction mean is slightly worse than ASTRA |
| 9 | Trust evidence and limitations | Member 3 | Exact replay and exclusions, but no independent city/test |
| 10 | Takeaway, practical scope, next validation | Member 1 | Strong conditional result, explicitly limited deployment claim |

If time is short, move Gate4 details, full competitor discussion, covariance equations, class metrics and runtime to Q&A. Do not spend a third of the talk describing failed infrastructure. Show it only as evidence discipline when relevant. Keep one clear curve and one spatial plot rather than a wall of 32 figures.

### Existing 17-slide fallback: how to avoid stale claims
Slides 1–5 establish EXP-010's problem and method; 6–8 carry its historical results/schedule; 9–12 cover negative findings and caveats; 13 concludes; 14–17 are backup. The new member guides reassign those speaking sections among three presenters without altering the file. Read `CONSISTENCY_AUDIT.md` before rehearsal: it flags “official” wording, overlapping-pixel interpretation, causal seasonal prose and historical reproducibility statements.

### Explain concepts simply
- **Prototype:** a representative average for each class, estimated from support labels.
- **Shrinkage:** stabilize a noisy estimate by mixing it with a simpler or source-informed estimate.
- **Covariance:** how feature dimensions move together; it can reveal duplicated directions.
- **Whitening:** re-express features so correlated directions are decorrelated/scaled, with regularization to avoid unstable amplification.
- **Source prior:** a source-informed initial distribution over class labels, not a supplied target answer.
- **Pseudo-label:** the model's own guess, not newly acquired ground truth; errors can reinforce themselves.
- **Transduction:** use the unlabelled features of the actual prediction pool when adapting the model.
- **Spatial smoothing:** neighboring probability vectors vote with fixed distance-based weights.
- **Paired trial:** both models receive the same support and query; compare within that draw.
- **Population SD:** the observed spread across the benchmark episodes, not “plus/minus certainty.”

### Answer “Why did you do this?”
Use a four-step answer: **problem → hypothesis → controlled evidence → boundary**. Example: “Support prototypes ignore nonlinear class shape. We tested a richer support classifier under explicit pool access. The frozen RF-based recipe improved matched random-pixel scores. But it needs the full target pool and spatial generalization remains limited.” Do not reverse-engineer a just-so mechanism from a positive number.

### Answer “Why should we trust this?”
Lead with evidence and its limit: “We froze the choice, saved support/query sets, checked exclusions, replayed predictions and rebuilt all numerical tables. That makes the stated internal result reproducible. It does not make it an independent-city result.” Then give the 200-shot paired gain, its interval and the negative spatial comparison if asked.

### Team rehearsal protocol
Each member gives their 30-second area summary, then answers one question outside their own area. Correct vocabulary before speed. Practice saying “that is not established” without apologizing excessively. The designated evidence presenter checks whether a question concerns old EXP-010, historical ASTRA or current Coordinate_RF before answering. Never make an unsupported authorship claim to balance speaking time.

## N. Judge question bank
The following bank contains three questions in each of the 22 requested categories. Every answer has a short version, a deeper version, key facts and a common error to avoid. The source IDs above are factual anchors, not claims of independent verification by the speaker.

<!-- QUESTION_BANK_INSERTION -->

````````

</details>

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/PRESENTATION_QA.md</summary>

````````text
# Presentation Q&A — difficult questions, defensible answers

**Answer the question, then state the evidence boundary.** Current research model is Coordinate_RF; the immutable existing organizer fallback deck is EXP-010. Clarify which result a judge means before quoting a number.

## “Why should we believe 0.7493?”
It is 0.749299 ±0.005716 macro F1 over all 200 saved 200-shot episodes of the locked protocol, not the best episode. Existing source/state replay, 4,000 exact model prediction arrays, metric reconstruction and isolated publication replay support the calculation. This is credible internal evidence on Amsterdam, not an organizer-held-out new-city score.

## “How do you know this isn't overfitting?”
We cannot rule out target-population overfitting. The latest configuration was selected on a fixed development bank and locked before final scoring, but the inherited ASTRA recipe had historical audit exposure. We disclose the extra 800 development labels and the negative spatial comparison rather than treating new episode seeds as a fresh city.

## “Did you use the target test labels?”
Current estimator fitting uses only designated support labels; query truth is used for evaluation. Class-stratified episode construction uses labels in the evaluator, and an 800-label bank informed development. Historical ASTRA also used target audit feedback for selection. Those distinct uses matter; saying target labels were never read would be false. The raw reference feature builder's label-dependent membership path is an additional deployment limitation.

## “Did you use competitor data?”
No competitor data/predictions enter our current model or safety snapshot. Historical forensic work separately executed and analysed a labelled competitor fallback mechanism using supplied benchmark data; that material is quarantined. Our later implementation uses our repository's own input artifact and code. We acknowledge mechanism inspiration instead of pretending no investigation occurred.

## “Why is your score higher than the competitor?”
The two headline numbers are not an exact paired comparison. Their locally recorded .7373 used 20 episodes and a different information/selection protocol; our .749299 uses 200 episodes and excludes the development bank. The winning competitor configuration is unrecovered. Our strongest claim is the matched +.016262 over current ASTRA, not superiority inferred by subtracting unrelated means.

## “What was the competitor's latest breakthrough?”
Latest locally evidenced commit `cf9af6c` records distance-weighted smoothing and a .7373 claim, up from .7259 uniform smoothing. That is genuine reported progress. No subsequent breakthrough is demonstrated in the inspected local evidence, but we did not fetch new remote history in this task. The exact tuned configuration remains missing.

## “Why are coordinates allowed?”
They are supplied covariates used in the research's stated transductive regime, not hidden labels. That does **not** prove organizer permission. The instruction about emailing presentation/explanation/notebooks does not settle full-pool or coordinate rules. We would need the actual evaluation information contract before asserting eligibility under a different test setup.

## “Is using the entire unlabelled target pool cheating?”
It is transductive learning. Whether it is allowed depends on the task contract. We explicitly use full-pool means/covariances, pseudo-labels and spatial structure and compare them separately from inductive controls. We do not hide that extra information access or claim an organizer approval that is not recorded.

## “What information is available at inference?”
The current artifact is bound to the original ordered Amsterdam feature/coordinate pool, with a cached source prior. Each episode supplies its support indices and labels, budget and optional query indices. The model receives no query truth. A reordered/new pool requires the proper unchanged fitting path and a new evaluation; the Amsterdam artifact is not a generic unseen-city model.

## “Why Random Forest?”
It captures nonlinear interactions in tabular spectral summaries and has recorded development and exact replay evidence in this project. The final local model has 200 trees, balanced class weights, leaf size 1 and square-root feature subsampling. That is an evidence-based frozen choice, not proof that forests cannot overfit or always outperform other models.

## “Why not XGBoost or neural networks?”
No validated XGBoost/neural advantage is recorded. A sklearn histogram-boosting alternative was explored and not selected; that is not XGBoost. ExtraTrees was competitive in development. We will not invent a neural experiment or universal classifier ranking. New comparisons would require separate authorization and independent validation, not this preparation task.

## “What happens at 5 shots?”
Coordinate_RF scores .650253 ±.011246, but its gain over ASTRA is only .000289 with 106/200 wins. The paired gain interval includes zero. We do not claim a meaningful low-shot advantage from the two added local coordinate columns. Five shots/class means twenty support labels, not five total.

## “Why does spatial robustness matter?”
Random pixels can have neighbors with similar building histories and spectra, making prediction easier than transfer across regions. The buffered directional audit probes that issue. Coordinate_RF's four-direction mean is .694216 versus ASTRA .696672; worst directional mean is .644816 versus .658183. We show that limitation rather than cherry-picking directions.

## “Why retain a model that is worse spatially?”
It is the prelocked research choice for the specified random-pixel/full-pool use case, not a universal geographic replacement. No configuration was changed after the final audit. A deployment decision with a different geographic contract could favor another separately evaluated method, but we should not silently switch and inherit the same reported score.

## “What failed?”
The 94-feature expansion did not win. EXP-F helped larger budgets but regressed in five-shot spatial testing. Gate4 E1 failed its fixed primary rule; E2 was inconclusive because +.004953 was below the +.0100 practical threshold; E3 production was coordinator-falsified and lacked full independent scientific certification after the validator stopped. Blocked/unrun experiments are not scientific failures.

## “Was E3 falsified because the file tree was dirty?”
No. The coordinator's negative scores and frozen decision rule produced its falsified verdict; the dirty-tree gate separately prevented full independent scientific reconstruction. We report both facts and do not imply the validator reconstructed or independently endorsed those numbers.

## “Are your p-values exaggerated by spatial dependence?”
Their interpretation is conditional on this fixed target/support-sampling regime. We use paired episode analyses, bootstrap intervals and Holm adjustment, not independent-pixel tests. Those tools do not resolve between-city uncertainty or historical selection exposure. At five shots even that conditional coordinate difference is inconclusive.

## “What would you improve next?”
First complete a consistent final notebook/presentation package outside the frozen snapshot and clarify full-pool/coordinate access. Scientifically, obtain a genuinely untouched geographic/city evaluation and fix the raw hidden-label preprocessing path under a separate validated task. More optimization on the same explored city is not the highest-value answer to those gaps.

## “What is the biggest weakness?”
External validity: one historically explored target city, correlated pixels, extra development supervision and spatial sensitivity. Operationally, the requested final-method notebook is missing and the existing deck is still EXP-010. Reproducible code and a strong internal score do not remove either limitation.

## “What did each teammate actually do?”
Use the repository evidence, not equal-credit fiction. Git/logs support Jaswin's repository/integration role and Ametor's early baseline/representation/EXP-010/presentation work across multiple scopes. The third speaker's personal historical implementation is not established. All three can explain the full project while honestly distinguishing speaking responsibilities from code authorship and agent assistance.

## “Can we submit the snapshot exactly as it is?”
The sealed ZIP is a clean verified fallback of the 13 intended files, but it is not certified as a complete current-method organizer submission: no final-method notebook was found, and reference-notebook runtime data are external. Seven background OneNote indexes appeared in the directory after sealing; they were not deleted and are absent from the ZIP. Use the ZIP for the exact fallback, and never silently relabel baseline notebooks or historical slides.

## Emergency answer pattern
**Claim → evidence → limit → next check.**

Example: “The current random-pixel gain is +.016262 against matched ASTRA. It appears in 200/200 paired episodes and the existing replay reconstructs predictions. It does not establish independent-city improvement, and spatial means are slightly worse. The next decisive scientific check is a genuinely untouched geographic evaluation.”

````````

</details>

<details>
<summary>ARCHIVED SOURCE: candidate/team_preparation/TONIGHT_REVISION.md</summary>

````````text
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

````````

</details>

<details>
<summary>ARCHIVED SOURCE: archive/team_history/SPEAKER_1_setup.md</summary>

````````text
# Speaker 1 — The Setup and the Discovery

**Slides 1–4** · roughly **3 minutes** of a 10-minute talk
Your job: land the problem, then deliver the discovery that makes the whole talk work.

> **You have the best material in the deck.** Slide 4 is the moment the audience sits up. Do not rush to it and do not undersell it.

---

## Slide 1 — Title + Abstract *(~30 s)*

**Do not read the abstract aloud.** It is on the slide for the rubric; the judges can read.

Say something like:

> "We were asked to work out how old buildings are from satellite images — training on Madrid, then adapting to Amsterdam with almost no labels. What we found first was that the starter code we were given doesn't actually do the thing it says it does. That's where we'll start."

Then move on. Do not linger.

---

## Slide 2 — The problem *(~45 s)*

Key points, in your own words:

- Building age drives retrofit and energy policy — and the records are incomplete
- Each pixel is 30 m × 30 m of ground, seen once a year for 42 years
- Four eras. Train Madrid, adapt Amsterdam.
- **The hard constraint: as few as five labelled examples per class**

**Point at the "5" tile.** Say: *"Five. That's the whole problem."*

---

## Slide 3 — The data *(~45 s)*

- Six spectral bands, once a year, 1984–2025
- **Why this is even possible:** "A field becomes a roof. Concrete weathers. Old dense centres reflect differently from new suburbs. The trajectory carries a fingerprint."
- 42 years of readings collapse into 60 summary numbers per pixel

**Then the honest bit — the orange line:**

> "One pixel can hold a 1950s block and a 2010s block. The label is an area-weighted average, so it describes neither. There's a ceiling here well below a perfect score, and nobody knows where it is. That matters for how you read every number we show you."

---

## Slide 4 — The defect *(~60 s)* ← **your key slide**

Slow down here.

> "The starter pipeline trains a Random Forest on Madrid. Then it throws it away."

*(pause)*

> "The Amsterdam prototypes are built from Amsterdam data alone. Madrid contributes a scaler — the mean and variance used to normalise. Nothing else."

> "So when you see its learning curve go up as you add labels, that isn't transfer. That's an Amsterdam-only method getting more Amsterdam data. Nothing crosses between the cities."

**Then the turn — this is the line that earns you originality marks:**

> "And that flaw turned out to be the most useful instrument we had. Because that path never touches the tree code, it acted as a control. It's how we proved our data pipeline was identical to theirs, and isolated a scikit-learn version difference in the baseline numbers."

**Hand over:** *"So we built one that actually transfers. [Name] will take you through it."*

---

## If you have 30 seconds less

Cut slide 3's technical detail, keep the noisy-labels point. Never cut slide 4.

---

## Questions likely to come to you

**"Why four classes and not a regression on year?"**
> The organisers defined it as four classes with city-specific boundaries — Madrid splits at 1960, Amsterdam at 1945, reflecting different histories. We kept their definition. Changing it would have made our numbers incomparable to the baseline.

**"How do you know the labels are noisy?"**
> The label is `weighted_mean_year` — an area-weighted average of construction years for buildings in the pixel. That's the organisers' own construction. A mixed-age pixel gets a class that describes no building in it.

**"Isn't 30 m very coarse for a building?"**
> Yes, and that's the core difficulty. A 30 m pixel often contains several buildings of different ages. It's why we treat the ceiling as real rather than assuming more modelling would fix it.

**"Did you consider using higher-resolution imagery?"**
> We didn't — external data wasn't a confirmed permission in the brief, and the challenge is defined on this dataset. It would be the obvious next step if allowed.

````````

</details>

<details>
<summary>ARCHIVED SOURCE: archive/team_history/SPEAKER_2_method.md</summary>

````````text
# Speaker 2 — The Method and the Results

**Slides 5–7** · roughly **3 minutes**
Your job: explain what we actually transfer, then show it works.

> **The trap to avoid:** do not describe this as "we improved F1." The gain beyond five shots is ~1.5%. Your strength is *what* you transferred and *how* you proved it, not the size of the number.

---

## Slide 5 — Our method *(~75 s)*

Walk the four boxes left to right. Keep it plain:

> "Every method we tested is the same four steps. Learn a transform on Madrid only. Freeze it. Push Amsterdam through it. Then build a prototype for each class from the handful of labelled examples we're allowed, and each new pixel gets the class of its nearest prototype."

> "Only one thing changes between the methods we compared — the transform. That's what makes it a controlled experiment."

**Then the framing line:**

> "What we transfer is a *metric*, not a classifier. Madrid teaches us which of the 60 measurements matter for telling building ages apart. Amsterdam supplies the examples. Madrid supplies the sense of what 'similar' means."

**Then the two tiles:**

> "The forest we train is 244 megabytes. What we actually ship is 3 kilobytes. Everything that transfers fits in 3 KB — because the transfer is 60 numbers and a feature subset, not the model."

That line lands. Let it.

---

## Slide 6 — Results *(~60 s)*

> "Here's our method against the starter's actual method. Same pixels, same episodes, same environment. The only thing different is the method."

Walk the table briefly, then:

> "Better at every budget. 47 of 50 paired episodes won. And at five shots — the hard case — we're up nearly 10% relative."

**The critical honesty note — say it before anyone asks:**

> "We're deliberately not comparing to the organisers' published numbers. Different episodes and a different scikit-learn version. Our own reproduction of *their* method scores 0.5038 at five shots against their published 0.5437 — same code, different draws. Comparing across those would invent an improvement that isn't there."

---

## Slide 7 — Learning curve *(~45 s)*

> "The gain is concentrated where the data is scarcest. That's not an accident — it's the prediction. Once Amsterdam has 25 or more labels per class, it has enough of its own data and the help from Madrid falls away."

> "Five shots is the case that actually matters if you're deploying this to a city with no labelled stock. That's where we improve most."

**Hand over:** *"And when we looked at why, we found something we didn't expect. [Name]."*

---

## If you have 30 seconds less

Compress slide 7 into one sentence on slide 6 and skip the figure.

---

## Questions likely to come to you

**"Why nearest-prototype instead of a proper classifier?"**
> With five labelled examples per class, almost anything with parameters overfits. A prototype is one mean per class — four numbers-worth of estimation. We tested richer alternatives; they lost.

**"What exactly is `λ`?"** *(this will come up)*
> How much we trust Madrid versus Amsterdam when we build a class prototype. λ=0 ignores Madrid entirely — that's the starter's method. λ=0.6 means 60% Madrid, 40% Amsterdam. It's a blending weight, like a complementary filter between a stable-but-biased sensor and an accurate-but-noisy one.

**"And `k`?"**
> How many of the 60 features we keep, ranked by Madrid's importance. k=45 beat k=60 at every budget — 15 of the starter's features were actively hurting.

**"Isn't 3 KB suspiciously small for a transfer method?"**
> That's the point. The forest is the apparatus that derives the weights; adaptation only needs the weights themselves. It makes the artifact trivially portable and reload-testable.

**"Did you use the unlabelled Amsterdam data?"**
> No. Deliberately. The plan lists unlabelled query alignment as an unconfirmed permission, so we compute everything from the support set only. It would probably have helped, and we didn't do it.

**"How do you know the improvement isn't luck?"**
> Episodes are matched — every method sees identical support draws — so we compare paired differences. 47 of 50 paired wins, with 10/10 at three separate budgets, on an audit set we never selected on.

````````

</details>

<details>
<summary>ARCHIVED SOURCE: archive/team_history/SPEAKER_3_science.md</summary>

````````text
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

````````

</details>

<details>
<summary>ARCHIVED SOURCE: archive/team_history/member4_presentation_outline.md</summary>

````````text
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

````````

</details>

<details>
<summary>ARCHIVED SOURCE: archive/presentation_history/pre_final_sync/docs/judge/PRESENTATION_OUTLINE.md</summary>

````````text
# Presentation outline

The authoritative outline and speaker handoffs are in [presentation/README.md](../../presentation/README.md); the editable source is [build_judge_deck.py](../../presentation/build_judge_deck.py).

The ten-slide narrative covers abstract/problem, motivation/data, low-label challenge, pipeline, design contribution, learning curve, paired interpretation, spatial limitations, reproducibility and future work. It addresses all three rubric pillars without changing results.

The original sealed 16-slide deck remains unchanged. Use the [submission inventory](SUBMISSION_INVENTORY.md) to distinguish the live companion from the preserved package.

````````

</details>

<details>
<summary>ARCHIVED SOURCE: archive/presentation_history/pre_final_sync/presentation/README.md</summary>

````````text
# Coordinate-RF · judge presentation

**Use [Coordinate-RF_Judges.pdf](Coordinate-RF_Judges.pdf) or [Coordinate-RF_Judges.pptx](Coordinate-RF_Judges.pptx).** Ten slides, consistent typography and colour, numbered pages, source footers and speaker notes. Locked headline: **0.749299 macro-F1**.

| Slides | Story | Suggested speaker |
|---|---|---|
| 1–3 | Abstract, urban problem, dataset and low-label challenge | Member 1 |
| 4–5 | Source/local pipeline and design rationale | Member 2 |
| 6–8 | Learning curve, paired interpretation and spatial trade-off | Member 3 |
| 9–10 | Integrity, limitations, eligibility and next research | Member 4 |

Allow roughly 8–10 minutes as a rehearsal default, subject to organizer timing. Every speaker should answer questions on the 25-label regime, source-prior reuse, additional supervision and why spatial results limit the headline.

## Presentation-only rebuild

Using the already available presentation libraries:

```bash
python -B presentation/build_judge_deck.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File presentation/export_judge_deck.ps1
```

The builder reads the frozen learning-curve CSV; it never imports model code. Its log2-spaced chart is a new presentation view of existing means and population SD, not recomputed predictions or a replacement scientific figure. PowerPoint exports PDF and PNG slides, checks text bounds and updates only the companion hash manifest. Then rerun `python -B scripts/validate_release.py`. Desktop PowerPoint is required for that export; no cross-platform export claim is made. The scientific-package seal is never rewritten.

The scientific runtime requirements do not include presentation tooling. This release used existing `python-pptx`, Pillow, Matplotlib and desktop PowerPoint, without installing dependencies. Exact available versions are recorded in the release validation receipt when available.

## Preserved original presentation

`StatsGeeks_BuildingAge.pptx` / `.pdf` and the 16-slide deck inside `FINAL_SUBMISSION/` are preserved historical/sealed deliverables. Do not confuse them with the ten-slide companion. The stale EXP-010 builder was moved to `archive/release_history/presentation/`; it must not be used to rebuild the final Coordinate-RF deck.

[Upload checklist](../docs/judge/SUBMISSION_INVENTORY.md) · [judge overview](../docs/judge/START_HERE.md).

````````

</details>

<details>
<summary>EMBEDDED SLIDE TEXT AND NOTES: FINAL_SUBMISSION/presentation.pptx</summary>

````````text
SLIDE 1: STATSGEEKS  ·  CROSS-CITY BUILDING-AGE TRANSFER | Classifying building age in a city
with almost no local labels | Madrid teaches the model. Amsterdam gives it as few as 5 labelled pixels per class. |  | 4 | building-age classes |  | 60 | ordered spectral features |  | macro-F1 | equal weight, every class |  | WHAT MAKES IT HARD | Domain shift between cities, mixed-pixel class noise, and support sets as small as 5 examples per class. | WHAT SUCCESS MEANS | Strong, equally-weighted macro-F1 across every budget — reproducible, and honest about where it does not generalize. | 1 / 10

• We're adapting a building-age classifier from Madrid, where we have full labels, to Amsterdam, where we may have as few as 5 labelled pixels per class.
• Four age classes, 60 ordered spectral features per pixel — a fairly standard remote-sensing setup.
• The hard part is genuine: domain shift between cities, noisy mixed-pixel classes, and extreme label scarcity at the low end.
• Success is macro-F1 — every class matters equally — evaluated honestly across five support budgets.

Transition: So how do we actually move information from a labelled city to an almost-unlabelled one? That's the approach.
Target time: 45-55s

SLIDE 2: 02 · APPROACH | One pipeline, five stages | From two cities of spectral data to a single calibrated prediction — the whole workflow at a glance. |  |  | 1 | Data | Madrid source (labelled)
+ Amsterdam support | → |  |  | 2 | Source prior | Covariance-aligned
Random Forests | → |  |  | 3 | Local model | Whitened features
+ coordinates | → |  |  | 4 | Blend & smooth | Budget-weighted blend,
spatial smoothing | → |  |  | 5 | Prediction | Macro-F1
evaluation |  | The name: “Coordinate-RF” refers to stages 3–4 — a Random Forest trained on the small Amsterdam support set, with two standardized lattice coordinates appended so it can use local geography, then blended with the source-city prior. | 2 / 10

• Two labelled sources feed the pipeline: the full Madrid dataset, and a tiny Amsterdam support set.
• A source-side prior is built first — covariance-aligned Random Forests give us a probability estimate for Amsterdam before we've seen much of it.
• In parallel, a local model is fit directly on the Amsterdam support, with spatial coordinates added so it can lean on nearby geography.
• The two are blended — trusting the source more when support is tiny — then spatially smoothed, and evaluated with macro-F1.

Transition: Let's walk through what that data actually looks like, and why the protocol behind it is leak-free.
Target time: 45-55s

SLIDE 3: 03 · DATA | Two cities, one clean protocol |  | DATASET | Source: Madrid — fully labelled, 60 spectral features per pixel.
Target: Amsterdam — small, class-balanced support set.
Local model adds 2 standardized lattice coordinates (x, y).
Support budgets tested: 5, 25, 50, 100, 200 labelled pixels per class. |  | WHY THE PROTOCOL IS VALID — NO LEAKAGE | Pseudo-labels used for source alignment come only from the source model — the query set's true labels are never touched.
The final query population excludes both the current support set and a separate 800-label development bank.
Support and query pixels stay strictly separated through every stage of inference.
Every run is matched: 200 paired episodes per budget, same pixels seen by every method compared. | 3 / 10

• Madrid gives full supervision; Amsterdam gives only a small, class-balanced support set at each budget.
• The 60 spectral features are shared across cities; locally we also add two standardized coordinates.
• Leakage is the first thing judges will ask about — so we're explicit: pseudo-labels never see query truth, and query pixels exclude both the current support and a held-out 800-label development bank.
• Every comparison is a matched, paired episode — same pixels, same conditions, across all methods.

Transition: With clean data and a valid protocol established, here's the model we actually fit.
Target time: 50-60s

SLIDE 4: 04 · MODEL | Coordinate-RF: three design choices | Each choice targets the same constraint — very few Amsterdam labels. |  |  | 1 | Why Random Forest | A balanced, 200-tree forest fits reliably on support sets as small as 5 labels per class — no gradient tuning, minimal overfitting risk. |  |  | 2 | Why coordinates | Two standardized lattice coordinates are appended to the local model's inputs, letting splits exploit the fact that nearby pixels tend to share a building age. |  |  | 3 | Why blending helps | A source-trained probability prior fills the gap when local support is tiny. Its weight, 20/(20+4b), shrinks automatically as budget b grows. | Then: the blended probabilities are smoothed over 9 spatial neighbours with Gaussian weights, stabilizing predictions before evaluation. | 4 / 10

• Random Forest was chosen because it's stable at extremely small sample sizes — 5 labels per class is not enough data for most deep models.
• Coordinates matter because building age is spatially clustered — a forest can learn 'nearby pixels look similar' almost for free once coordinates are inputs.
• The blend is the key transfer mechanism: it leans heavily on Madrid-derived knowledge when Amsterdam support is tiny, and fades that out as real local evidence accumulates.
• A final spatial smoothing pass cleans up noisy pixel-level predictions.

Transition: Now let's talk about how we tested this, and how confident we can be in the numbers.
Target time: 50-60s

SLIDE 5: 05 · EXPERIMENTS | Five budgets, evaluated the same way every time |  |  | 5 |  | 25 |  | 50 |  | 100 |  | 200 | LABELLED PIXELS PER CLASS |  |  | 200 paired episodes | Every budget is evaluated across 200 matched episodes, with population SD reported alongside each score. |  |  | Macro-F1, equal weight | The four age classes are weighted equally — a rare class can't be ignored to inflate the score. |  |  | Same pixels, every method | Coordinate-RF, ASTRA, EXP-F and EXP-010 are all compared on identical, paired support/query splits. | 5 / 10

• We test five support budgets, from 5 up to 200 labelled pixels per class, to see how quickly the method improves as labels arrive.
• Every budget gets 200 paired episodes, so we can report a population standard deviation rather than a single lucky run.
• Macro-F1 is the scoring metric throughout — every class counts equally.
• Critically, every baseline we compare against sees exactly the same paired pixels — this is a matched, apples-to-apples comparison.

Transition: That protocol is what makes the results on the next slide meaningful — let's look at them.
Target time: 40-50s

SLIDE 6: 06 · RESULTS | 0.749299 macro-F1 — the best score at every budget |  | LOCKED RESULT · 200 SHOTS | 0.7493 | macro-F1  ±0.005716 population SD |  | Matched gains at 200 shots, all 200 paired episodes: | vs ASTRA | +0.0163 | 200/200 episodes won | vs EXP-F | +0.0917 | vs EXP-010 | +0.1265 | Why it matters: Coordinate-RF isn't just the best score at 200 shots — it's the top locked result at every budget tested, including the hardest, 5-shot regime. | 95% BOOTSTRAP CI · 200 SHOTS | [0.7485, 0.7501] macro-F1, resampled from the same 200 paired episodes — the headline number is not a single lucky draw. | 6 / 10

• The headline number: 0.749299 macro-F1 at 200 shots, with a tight population SD of 0.0057.
• But the more important story is in the table — this is the best locked score at every single budget we tested, not just the largest one.
• Against the strongest baseline, ASTRA, Coordinate-RF won all 200 matched episodes at 200 shots — that's a consistent, not a lucky, advantage.
• The gains over EXP-F and EXP-010 are much larger, showing how far the method has come since the earliest iterations.

Transition: Two figures make this trend and its boundaries concrete — the learning curve, and what the model actually learned.
Target time: 55-65s

SLIDE 7: 07 · ANALYSIS | Consistent gains as labels grow | Learning curve: macro-F1 rises smoothly from 5 to 200 shots, with Coordinate-RF (green) ahead of every baseline at every budget. | What the model learned: 71–83% correct per class, with confusion concentrated between adjacent age classes — the pattern we'd expect. | 7 / 10

• The learning curve is the clearest evidence for the method: Coordinate-RF's green line sits at or above every baseline at all five budgets.
• Even at 5 shots — the hardest regime — it ties the strongest baseline, ASTRA, and then pulls ahead as support grows.
• The confusion matrix shows what the model actually learned: strong diagonal performance, 71 to 83 percent per class, with most errors landing on the adjacent, visually-similar age class rather than being scattered randomly.
• That's a model that has learned a sensible, ordered representation of building age — not noise.

Transition: The honest next question is where this stops generalizing — that's the limitations slide.
Target time: 55-65s

SLIDE 8: 08 · LIMITATIONS | Where the method is honest about its limits | Spatial stress test: held-out on the opposite half of the city. Mean 0.6942 vs ASTRA's 0.6967; worst direction 0.6448 vs ASTRA's 0.6582 — coordinates help interpolation between nearby labels, not extrapolation far beyond them. |  | Transductive, not inductive | Full-pool, coordinate-aware inference bound to the supplied Amsterdam pool — not an unseen-city claim. |  | Pool-bound artifact | Excludes current support and an 800-label development bank; a new pool needs re-fitting on organizer data. |  | Future work | Extend beyond interpolation so the model holds up further from its labelled coordinates. | Also disclosed: the inherited ASTRA baseline recipe carries historical audit exposure; no independent organizer-held-out validation is claimed here, and protocol eligibility must still be confirmed against organizer rules. | 8 / 10

• We ran a deliberate stress test: holding out the opposite half of the city, in every direction, to see how far the model can extrapolate.
• Here Coordinate-RF is honest about a weakness — on both the mean and the worst direction, it's slightly behind ASTRA, unlike the random-pixel results.
• That tells us coordinates help the model interpolate between nearby labelled points, but don't grant real extrapolation power.
• This is why we describe the method as transductive and pool-bound rather than claiming it generalizes to any unseen city out of the box.

Transition: None of that changes why the result is still valuable — here's where it matters.
Target time: 55-65s

SLIDE 9: 09 · IMPACT | Why this is useful beyond one leaderboard score |  |  | Scales gracefully with labels | Macro-F1 climbs smoothly from 5 to 200 shots — useful whenever labelling a new city is slow or expensive, since even a handful of examples is workable. |  |  | Fully reproducible | Frozen configurations, hashes, label-free prediction replay and saved confusion matrices mean the result can be independently checked, not just trusted. |  |  | A transferable blueprint | Source prior + local coordinate-aware fit is a pattern that extends to other cross-city, low-label spectral classification problems within the same random-pixel, full-pool setting. | 9 / 10

• The practical value here is label efficiency — the curve shows useful performance even at 5 shots, which matters when a new city has almost no ground truth yet.
• Reproducibility is not an afterthought: every number on this deck traces back to a frozen, hashed, independently-replayable artifact.
• And the pattern itself — a source-city prior blended with a coordinate-aware local fit — isn't specific to Amsterdam or Madrid; it's a reusable recipe for this class of problem.
• That combination — real performance, full honesty about scope, and full reproducibility — is what we'd want judges to remember.

Transition: Let's close with the handful of points worth remembering.
Target time: 45-55s

SLIDE 10: 10 · KEY TAKEAWAYS | What to remember about Coordinate-RF |  | 0.749299 | Locked macro-F1 at 200 shots — the best result at every budget tested, 5 through 200. |  | 200 / 200 | Matched episodes where Coordinate-RF beat the strongest baseline, ASTRA, at 200 shots. |  | Zero leakage | Query truth never touches training, pseudo-labelling, or model selection — fully reproducible. |  | Honest scope | Transductive and pool-bound by design; coordinates aid interpolation, not extrapolation. | 10 / 10

• Four numbers to leave in judges' minds: 0.749299 as the locked, best-at-every-budget result.
• 200 out of 200 matched episodes beating the strongest prior baseline — a consistent, not lucky, win.
• Zero query-label leakage anywhere in the pipeline, with a fully reproducible, hashed artifact.
• And an honest scope: this is a transductive, pool-bound method that interpolates well and says so plainly about where it doesn't extrapolate.

Transition: Thank you — happy to take questions on the method, the protocol, or the limitations.
Target time: 40-50s
````````

</details>

<details>
<summary>EMBEDDED SLIDE TEXT AND NOTES: presentation/Coordinate-RF_Judges.pptx</summary>

````````text
SLIDE 1:  | STATSGEEKS · COORDINATE-RF | Building-age transfer with scarce labels | Frozen evidence: FINAL_SUBMISSION/results_summary/learning_curve.csv | 01 / 10 | Madrid → Amsterdam | We classify four building-construction eras from 30 m Landsat pixels. Coordinate-RF combines a Madrid-learned prior with a target-support random forest, whitened spectral features and spatial context. On the frozen Amsterdam random-pixel protocol it reaches 0.749299 macro-F1 at 200 labels per class. The method uses the full unlabelled target pool and an additional development label bank; spatial extrapolation remains a limitation. |  | 0.749299 | Locked macro-F1
200 labels/class
200 paired episodes

Speaker 1. First-slide abstract, under 150 words. Introduce the problem and the exact scope, not just the score.

SLIDE 2:  | 01 · PROBLEM & MOTIVATION | A useful urban signal, with imperfect labels | Data: organizer notebooks; docs/MASTER_PLAN.md dataset summary | 02 / 10 |  | Why age? | Retrofit planning
Energy-policy evidence
Incomplete records |  | What data? | Six spectral bands
1984–2025 imagery
30 m mixed pixels |  | What task? | Four construction eras
Madrid source city
Amsterdam target city | 76,263 source pixels  ·  25,992 target pixels  ·  60 spectral features

Speaker 1. Age supports retrofit and energy planning. Explain mixed-pixel labels and different oldest-era boundaries.

SLIDE 3:  | 02 · CHALLENGE UNDERSTANDING | Transfer must work when labels are scarce | Protocol: candidate/reports/METHODS.md; locked learning-curve CSV | 03 / 10 |  | Cross-city shift | Spectral and spatial patterns differ.
Source knowledge needs adaptation. |  | Few-label adaptation | 5 / 25 / 50 / 100 / 200 labels per class.
Only designated support labels fit the local RF. | 25 labels/class = 100 target support labels | The additional 800-label development bank is separate research supervision.

Speaker 1 → Speaker 2. The 25-shot result is important to the rubric. Macro-F1 gives each class equal weight.

SLIDE 4:  | 03 · PIPELINE | One source prior, one local adaptation branch | Method: candidate/reports/METHODS.md; frozen model configuration | 04 / 10 |  | Madrid source branch | Contextual spectral features
Covariance alignment + refinement
Frozen source probability prior |  | Amsterdam local branch | Full-pool adaptive whitening
Two standardized coordinates
Support-only 200-tree RF | ↓ | ↓ |  | Blend probabilities  →  nine-neighbour smoothing  →  classes

Speaker 2. Historical learning pipeline, not executed during release. Two source RFs produce the cached prior. Only support labels fit the target RF.

SLIDE 5:  | 04 · DESIGN RATIONALE & CREATIVITY | The contribution is the combination | Mechanism evidence: candidate/reports/RESULTS.md and METHODS.md | 05 / 10 |  | Source reuse | Source probability weight:
20 / (20 + 4b)
Less weight as support grows. |  | Local geometry | Adaptive whitening
Spectral + coordinate inputs
Balanced random forest |  | Spatial context | Label-free smoothing
Nine spatial neighbours
Full-pool access required | b = labels/class. Components interact; ablation bars are not additive causal effects.

Speaker 2. Explain rationale without presenting entangled ablations as additive causal effects. No novelty claim for RF itself.

SLIDE 6:  | 05 · LOCKED LEARNING CURVE | Performance improves as target support grows | Source: FINAL_SUBMISSION/results_summary/learning_curve.csv · no new predictions | 06 / 10 | 25 / class | 0.687664 | 200 / class | 0.749299 | SD is episode spread, not a confidence interval.

Speaker 3. Explain every budget and population SD. These are 200 paired episodes per budget on one fixed city. ASTRA, EXP-F and EXP-010 are historical comparison methods.

SLIDE 7:  | 06 · RESULT INTERPRETATION | A strong fixed-city result—not universal superiority | Paired evidence: candidate/reports/RESULTS.md and STATISTICAL_ANALYSIS.md | 07 / 10 |  | 200 labels/class | Coordinate-RF: 0.749299 ± 0.005716
Matched ASTRA: 0.733037
Mean gain: +0.016262 |  | What the evidence says | 200/200 paired wins at 200/class
Five-shot superiority is inconclusive
One shared target-city population | The 800-label development bank and current support are excluded from final queries.

Speaker 3. At 200/class, compare Coordinate-RF with ASTRA on matched episodes. Do not infer independent-city significance from the paired tests.

SLIDE 8:  | 07 · ANALYSIS & LIMITATIONS | Spatial extrapolation reveals the trade-off | Frozen spatial evidence: candidate/reports/SPATIAL_ANALYSIS.md | 08 / 10 |  | Four-direction mean | Coordinate-RF: 0.694216
Matched ASTRA: 0.696672 |  | Worst-direction mean | Coordinate-RF: 0.644816
Matched ASTRA: 0.658183 | Coordinates help within this pool; they do not establish transfer to new geography.

Speaker 3 → Speaker 4. Lower spatial means are material negative evidence. Different query geography prevents equating spatial and random-pixel scores.

SLIDE 9:  | 08 · ENGINEERING & INTEGRITY | Frozen evidence, explicit reproducibility boundaries | Verification: scripts/validate_release.py; FINAL_SUBMISSION/manifest.json | 09 / 10 |  | What is preserved | Model + configuration + ordered inputs
Notebook outputs + result tables
Manifest and SHA-256 checksums |  | What is not claimed | Fresh training or runtime replay here
A self-contained raw-data rebuild
Organizer-held-out validation | Safe audit: python -B scripts/validate_release.py

Speaker 4. Hash checks are safe; --verify is not just a checksum command and fits support RFs. Explain the pool-bound artifact and distinguish static checks from runtime reproduction.

SLIDE 10:  | 09 · CONCLUSION & FUTURE WORK | A clear result—and a clear next test | Start here: docs/judge/START_HERE.md · results remain locked | 10 / 10 | Coordinate-RF · macro-F1 0.749299 | 200 labels/class · fixed-city random-pixel evaluation |  | Before competition upload | Confirm full-pool, coordinate and
additional-supervision eligibility. |  | Next research—not run | Independent-city / spatial validation
Portable inference for new target pools

Speaker 4. Close with exact score and scope. Future work is proposed, not performed. All four speakers should rehearse handoffs. Take questions on source transfer, the 25-shot regime, extra supervision and spatial limitations.
````````

</details>

<details>
<summary>EMBEDDED SLIDE TEXT AND NOTES: presentation/StatsGeeks_BuildingAge.pptx</summary>

````````text
SLIDE 1:  | STATSGEEKS  ·  BUILDING-AGE TRANSFER LEARNING | Transfer that actually transfers | Building age drives urban retrofit and energy policy, but records are incomplete. We classify the construction era of buildings within 30-metre Landsat pixels into four classes, training on Madrid and adapting to Amsterdam with as few as five labelled examples per class.

The organiser baseline showed substantial source-target mismatch, motivating a representation-based transfer strategy. Madrid learns feature ranking and class geometry; Amsterdam support labels estimate target prototypes. At five shots we shrink noisy prototypes toward re-centred Madrid geometry. At larger budgets shrinkage switches off while dimensionality reduction remains useful. In frozen EXP-010 audit episodes, tuned macro F1 improves over the matched full-feature, target-only control at every budget, with 45 of 50 paired wins. The largest mean gain occurs at five shots per class—only 20 labelled Amsterdam samples total—where prototype estimation is hardest. | Abstract · ≤150 words

SLIDE 2:  | THE PROBLEM | How old are these buildings? |  | Four construction eras, per 30 m Landsat pixel |  | Train on Madrid  →  adapt to Amsterdam |  | As few as five labelled examples per class |  | Metric: four-class macro F1 |  | 76k | Madrid pixels |  | 26k | Amsterdam pixels |  | 42 | years of imagery |  | 5 | labels, worst case

SLIDE 3:  | THE DATA | Construction leaves a spectral fingerprint |  | Six spectral bands · once a year · 1984–2025 |  | A field becomes a roof.  Concrete weathers. |  | 42-year trajectory  →  60 summary features |  | Labels are area-weighted averages — noisy by construction |  | One pixel can hold a 1950s block and a 2010s block — and gets a label describing neither. | There is a ceiling below 1.0. Nobody knows where it is.

SLIDE 4:  | BASELINE CONTEXT | Source-target mismatch motivates transfer |  | Organiser reference path
Madrid-fitted scaling
Amsterdam-only prototypes |  | The reference path establishes a matched target-only control |  | It motivated reuse of supervised Madrid state |  | Our comparison holds episodes and classifier form fixed |  | Provenance limitation: local RF outputs differ from organiser-saved outputs. Incomplete package/input provenance means the cause remains unidentified.

SLIDE 5:  | OUR METHOD | Freeze Madrid knowledge; adapt prototypes |  | Madrid | labelled data | → |  | Frozen RF | ranking + geometry | → |  | Top-k | feature selection | → |  | Amsterdam | support set | → |  | Adapt | prototypes | → |  | Predict | query labels |  | 5 shots/class  →  k=30, λ=0.6
Shrink toward Madrid geometry |  | 25–200 shots/class  →  k=45, λ=0.0
Shrinkage switches off | Query labels are evaluation-only.

SLIDE 6:  | FROZEN EXP-010 AUDIT | Five shots is the practical anchor |  | shots/class | EXP-010 | control | gain | wins | 5 | 0.552 ± 0.060 | 0.515 ± 0.070 | +0.037 | 7/10 | 25 | 0.612 ± 0.013 | 0.609 ± 0.015 | +0.003 | 8/10 | 50 | 0.617 ± 0.008 | 0.614 ± 0.008 | +0.004 | 10/10 | 100 | 0.620 ± 0.005 | 0.615 ± 0.005 | +0.005 | 10/10 | 200 | 0.624 ± 0.004 | 0.619 ± 0.004 | +0.005 | 10/10 |  | +0.0372 | 5-shot macro F1 gain |  | 45 / 50 | paired audit wins | ± population SD across 10 audit episodes — not confidence intervals |  | SCIENTIFIC HEADLINE  ·  5/class = 20 labels total
0.552 ± 0.060 vs 0.515 ± 0.070 · 7/10 wins |  | OFFICIAL 25-SHOT RESULT
+0.0033 macro F1 · 8/10 paired wins

SLIDE 7:  | REQUIRED LEARNING CURVE | Transfer helps most in the lowest-data regime |  | 5 shots/class
High episode spread |  | 25+ shots/class
Prototypes stabilise | Empirical takeaway:
Transfer helps most when target prototypes are hardest to estimate. | Source-domain CV (documented local protocol):
Madrid 0.6281 ± 0.0043 macro F1

SLIDE 8:  | EMPIRICAL INTERPRETATION | More labels reduce prototype estimation error |  | shots | features (k) | shrinkage (λ) | 5 | 30 | 0.6 | 25 | 45 | 0.0 | 50 | 45 | 0.0 | 100 | 45 | 0.0 | 200 | 45 | 0.0 |  | λ — how much we trust Madrid over Amsterdam |  | k — how many features we keep |  | Less data → lean on Madrid, use fewer features |  | More data → trust Amsterdam, afford more features |  | In these experiments, the selected schedule |  | switches shrinkage off once labels increase.

SLIDE 9:  | WHAT WE LEARNED | Negative results clarify the mechanism |  | EXP-004 · WHITENING REVERSAL | Within-class whitening changed from harmful at low shot count to beneficial at high shot count. The same transform gave opposite outcomes as support grew. |  | EXP-007 · MORE FEATURES DID NOT HELP | The expanded 94-feature seasonal/coverage representation did not outperform the original 60 features. Extra dimensions can dilute few-shot prototype estimates. |  | Together, these outcomes support—without proving—the prototype estimation-error interpretation.

SLIDE 10:  | HONESTY | What we are not claiming |  | Gains beyond five shots are small in absolute macro F1 |  | Error bars are spreads, not confidence intervals |  | Confusion diagonals are recall, not F1 |  | Accuracy would have flattered us — we report macro F1 |  | We do not claim exact reproduction of organiser RF outputs |  | Why not? | Source-domain Madrid CV is 0.6281 ± 0.0043 under the documented local protocol; local zero-shot is 0.4433, versus organiser-saved 0.6179 and 0.3427. Package/input provenance is incomplete, so the cause remains unidentified and exact reproduction is not claimed.

SLIDE 11:  | STATED, NOT HIDDEN | Limitations |  | 1.   Features still built label-dependently — no hidden-test path yet |  | 2.   Scaling fitted before cross-validation — not fold-safe |  | 3.   λ schedule: five values from five selection trials — overfit risk |  | 4.   Optimal k moves once (30→45) — weak evidence for a trend |  | 5.   EXP-010 has not been independently replicated | No claims of worldwide portability. No claims of calibrated confidence.

SLIDE 12:  | CONTROLS AND PROVENANCE | Reproducible by design, limited by evidence |  | EVALUATION CONTROLS |  | Exact episode manifests + RNG binding |  | Support/query isolation |  | Frozen EXP-010 state |  | Matched episodes for tuned and control |  | Population SD over 10 audit episodes |  | EVIDENCE BOUNDARY |  | Madrid → Amsterdam only |  | No hidden-test claim |  | No independent EXP-010 replication |  | Local baseline provenance is incomplete |  | Controls support validity, not superiority

SLIDE 13:  | CONCLUSION | Madrid learns feature ranking and class geometry. | Amsterdam support labels estimate target prototypes. | EXP-010: positive mean gains, 45/50 paired wins. | A number without a mechanism is not a finding.

SLIDE 14:  | BACKUP | Reproducibility |  | requirements.txt pins the exact stack |  | Raw data + feature cache SHA256 recorded |  | Episode indices stored, not regenerated from a seed |  | EXP-010 package stores weights, k=30/45 offsets and schedule |  | Frozen artifacts include recorded SHA256 checksums |  | Cold-start reproduction: ~35 minutes

SLIDE 15:  | BACKUP | Why our baseline differs from the organiser's |  | All six prototype budgets match them to 4 decimal places |  | Both Random-Forest results differ: +0.0102 and +0.1006 |  | The prototype path does not consume fitted forest predictions |  | Determinism check: 0 of 25,992 predictions differed across two refits |  | Exact cause remains unidentified; no causal explanation is claimed

SLIDE 16:  | BACKUP | A 70-day seasonal offset between the cities |  | Madrid median day 175 · Amsterdam day 105 |  | June–August: 48.3% vs 20.5% |  | Part of the domain shift is phenology, not architecture |  | We rebuilt features to control for it |  | It did not help — dilution outweighed the correction |  | Reported as a measured finding with a negative test

SLIDE 17:  | BACKUP | The episode protocol |  | One permutation per class per trial; budgets read prefixes |  | So budgets are nested: support(5) ⊂ support(25) ⊂ … |  | Support and query disjoint, verified in code every episode |  | Selection and audit sets never overlap |  | Four independent seeds used across the project |  | Query set shrinks unevenly as budget grows — a stated limitation
````````

</details>

<details>
<summary>EMBEDDED SLIDE TEXT AND NOTES: archive/presentation_history/pre_final_sync/FINAL_SUBMISSION/presentation.pptx</summary>

````````text
SLIDE 1: StatsGeeks | Coordinate-RF | Building-age classification: Madrid → Amsterdam
Final selected incumbent; reproducible full-pool few-shot inference.
200-shot macro-F1: 0.749299 ± 0.005716.
Existing locked audit, not a new independent test.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Building-age classification: Madrid → Amsterdam
Final selected incumbent; reproducible full-pool few-shot inference.
200-shot macro-F1: 0.749299 ± 0.005716.
Existing locked audit, not a new independent test.

SLIDE 2: Problem and task | Four building-age classes; 60 ordered spectral features.
Labelled Madrid source; small balanced Amsterdam support.
Budgets: 5 / 25 / 50 / 100 / 200 labels per class.
Macro-F1 gives equal weight to each class.
Organizer data needed for raw training; pool-bound inference artifact supplied.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Four building-age classes; 60 ordered spectral features.
Labelled Madrid source; small balanced Amsterdam support.
Budgets: 5 / 25 / 50 / 100 / 200 labels per class.
Macro-F1 gives equal weight to each class.
Organizer data needed for raw training; pool-bound inference artifact supplied.

SLIDE 3: Starting point and experimental journey | EXP-010: source-selected weighted prototypes.
EXP-F: covariance-aware metric adaptation.
ASTRA: source prior, adaptive whitening, forest, graph.
Coordinate-RF: append standardized coordinates to local inputs.
Overnight discovery uses development support only; no query-driven selection.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. EXP-010: source-selected weighted prototypes.
EXP-F: covariance-aware metric adaptation.
ASTRA: source prior, adaptive whitening, forest, graph.
Coordinate-RF: append standardized coordinates to local inputs.
Overnight discovery uses development support only; no query-driven selection.

SLIDE 4: Challenges and failed approaches | Domain shift, scarce labels, noisy mixed-pixel age classes.
Historical support-only alternatives: ExtraTrees, boosted trees, covariance blends, wider graphs and ensembles.
They did not replace the development-locked Coordinate-RF under the documented gates.
Overnight results are exploratory, not new headline evidence.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Domain shift, scarce labels, noisy mixed-pixel age classes.
Historical support-only alternatives: ExtraTrees, boosted trees, covariance blends, wider graphs and ensembles.
They did not replace the development-locked Coordinate-RF under the documented gates.
Overnight results are exploratory, not new headline evidence.

SLIDE 5: Transfer-learning insight | Source information survives as an aligned probability prior.
120 contextual source features; covariance transport.
One pseudo-class refinement uses predictions, never target truth.
Two source RF200/leaf2 models; blend decreases as support grows.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Source information survives as an aligned probability prior.
120 contextual source features; covariance transport.
One pseudo-class refinement uses predictions, never target truth.
Two source RF200/leaf2 models; blend decreases as support grows.

SLIDE 6: Final method | Unlabelled-pool covariance → budget-adaptive diagonal shrinkage.
Whiten 60 inputs; append standardized lattice x/y.
Fit balanced RF200, leaf1, sqrt features, seed42 on support only.
Blend source prior: alpha=20/(20+4b).
Gaussian smoothing: 9 neighbours, sigma1, one step.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Unlabelled-pool covariance → budget-adaptive diagonal shrinkage.
Whiten 60 inputs; append standardized lattice x/y.
Fit balanced RF200, leaf1, sqrt features, seed42 on support only.
Blend source prior: alpha=20/(20+4b).
Gaussian smoothing: 9 neighbours, sigma1, one step.

SLIDE 7: Why it works — and assumptions | Spectral covariance adapts to target distribution.
Coordinates help interpolate local geography.
Source prior matters most when labels are scarce.
This is transductive/full-unlabelled-target inference.
Coordinates, pool membership and extra development supervision require organizer eligibility confirmation.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Spectral covariance adapts to target distribution.
Coordinates help interpolate local geography.
Source prior matters most when labels are scarce.
This is transductive/full-unlabelled-target inference.
Coordinates, pool membership and extra development supervision require organizer eligibility confirmation.

SLIDE 8: Locked learning curve | 5: 0.650253 ± 0.011246
25: 0.687664 ± 0.012145
50: 0.708436 ± 0.011277
100: 0.729839 ± 0.008802
200: 0.749299 ± 0.005716

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. 5: 0.650253 ± 0.011246
25: 0.687664 ± 0.012145
50: 0.708436 ± 0.011277
100: 0.729839 ± 0.008802
200: 0.749299 ± 0.005716

SLIDE 9: Matched comparisons at 200 shots | Coordinate-RF 0.749299; 200 episodes.
Gain vs ASTRA +0.016262; 200/200 wins.
Gain vs EXP-F +0.091697.
Gain vs EXP-010 +0.126459.
Inductive controls have different information access.
Five-shot advantage over ASTRA is negligible.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Coordinate-RF 0.749299; 200 episodes.
Gain vs ASTRA +0.016262; 200/200 wins.
Gain vs EXP-F +0.091697.
Gain vs EXP-010 +0.126459.
Inductive controls have different information access.
Five-shot advantage over ASTRA is negligible.

SLIDE 10: Paired gains and uncertainty | Matched support episodes on one fixed city.
Error bars/intervals quantify support sampling only.
Repeated query pixels imply correlated episodes.
No independent-city or organizer-test claim.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Matched support episodes on one fixed city.
Error bars/intervals quantify support sampling only.
Repeated query pixels imply correlated episodes.
No independent-city or organizer-test claim.

SLIDE 11: Class-level performance | Saved locked predictions/confusion matrices.
Macro-F1 is the mean of four class F1 values.
Pooled confusion is descriptive; not mean episode F1.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Saved locked predictions/confusion matrices.
Macro-F1 is the mean of four class F1 values.
Pooled confusion is descriptive; not mean episode F1.

SLIDE 12: Spatial stress: all directions | 200/class; opposite half; 10-key-unit buffer.
x-low .719836; x-high .644816.
y-low .669160; y-high .743052.
Mean .694216; worst .644816.
ASTRA mean .696672; worst .658183.
Coordinates improve interpolation, not all extrapolation.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. 200/class; opposite half; 10-key-unit buffer.
x-low .719836; x-high .644816.
y-low .669160; y-high .743052.
Mean .694216; worst .644816.
ASTRA mean .696672; worst .658183.
Coordinates improve interpolation, not all extrapolation.

SLIDE 13: Reproducibility | Existing clean source refit: 4000 exact prediction arrays / 1000 episodes.
Overnight fresh source refit: eight exact state arrays and five-budget replay.
Current package: clean-process five-budget cached replay.
Notebook executed sequentially in a fresh Python process.
Hashes, feature order, config, seeds and provenance included.
Query truth is absent from inference inputs.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Existing clean source refit: 4000 exact prediction arrays / 1000 episodes.
Overnight fresh source refit: eight exact state arrays and five-budget replay.
Current package: clean-process five-budget cached replay.
Notebook executed sequentially in a fresh Python process.
Hashes, feature order, config, seeds and provenance included.
Query truth is absent from inference inputs.

SLIDE 14: Limitations and conclusion | 0.80 not achieved on the locked audit.
No fresh untouched population exists locally for promotion.
Historical ASTRA audit exposure is disclosed.
Extra 800 research-development labels are beyond episode budgets.
Retain Coordinate-RF; do not force an unverified winner.
Competition eligibility remains conditional on organizer rules.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. 0.80 not achieved on the locked audit.
No fresh untouched population exists locally for promotion.
Historical ASTRA audit exposure is disclosed.
Extra 800 research-development labels are beyond episode budgets.
Retain Coordinate-RF; do not force an unverified winner.
Competition eligibility remains conditional on organizer rules.

SLIDE 15: Written explanation (1/2) | Coordinate-RF predicts four building-age classes for Amsterdam using labelled Madrid source data and a small class-balanced Amsterdam support set. The target is macro-F1, which weights each class equally. We evaluate 5, 25, 50, 100 and 200 support pixels per class.

Our source branch augments 60 spectral inputs with local 3-by-3 lattice averages, aligns source and unlabelled target covariance, and refines class-conditional alignment using source-model pseudo-labels, never query truth. Two source Random Forests produce a target probability prior. The local branch adaptively whitens 60 inputs using full unlabelled target covariance with budget-dependent diagonal shrinkage, appends two standardized lattice coordinates, and fits a 200-tree, balanced Random Forest to support labels only. Its probabilities are blended with the source prior using weight 20/(20+4b), then smoothed over nine spatial neighbours with Gaussian weights.

The locked random-pixel results, each from 200 paired episodes, are 0.650253, 0.687664, 0.708436, 0.729839 and 0.749299 macro-F1 across the five budgets. At 200 shots the population SD is 0.005716. Matched gains are 0.016262 over ASTRA, 0.091697 over EXP-F and 0.126459 over EXP-010. All 200 paired episodes beat ASTRA at that budget. The five-shot advantage is negligible.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. Coordinate-RF predicts four building-age classes for Amsterdam using labelled Madrid source data and a small class-balanced Amsterdam support set. The target is macro-F1, which weights each class equally. We evaluate 5, 25, 50, 100 and 200 support pixels per class.

Our source branch augments 60 spectral inputs with local 3-by-3 lattice averages, aligns source and unlabelled target covariance, and refines class-conditional alignment using source-model pseudo-labels, never query truth. Two source Random Forests produce a target probability prior. The local branch adaptively whitens 60 inputs using full unlabelled target covariance with budget-dependent diagonal shrinkage, appends two standardized lattice coordinates, and fits a 200-tree, balanced Random Forest to support labels only. Its probabilities are blended with the source prior using weight 20/(20+4b), then smoothed over nine spatial neighbours with Gaussian weights.

The locked random-pixel results, each from 200 paired episodes, are 0.650253, 0.687664, 0.708436, 0.729839 and 0.749299 macro-F1 across the five budgets. At 200 shots the population SD is 0.005716. Matched gains are 0.016262 over ASTRA, 0.091697 over EXP-F and 0.126459 over EXP-010. All 200 paired episodes beat ASTRA at that budget. The five-shot advantage is negligible.

SLIDE 16: Written explanation (2/2) | This is transductive, full-pool, coordinate-aware inference, not an inductive unseen-city claim. The packaged artifact is bound to the supplied ordered Amsterdam pool. Rebuilding for another pool requires organizer feature data, feature order, source-fitted scaling and matching lattice coordinates. The final query population excludes the designated 800-label development bank and current support. Development labels are additional research supervision beyond each episode budget; repeated episodes are correlated. The inherited ASTRA recipe has historical audit exposure. No independent organizer-held-out validation is claimed, and protocol eligibility must be confirmed against organizer rules.

Geographic extrapolation remains a limitation: the four-direction spatial mean is 0.694216 and the worst direction is 0.644816, versus ASTRA's 0.696672 and 0.658183. Coordinate-RF is therefore selected for the stated random-pixel/full-pool use case, not universal superiority. Frozen configurations, hashes, label-free prediction replay, support/query separation and saved confusion matrices support reproducibility. No competitor code, data or predictions are included. No overnight exploratory candidate replaces the incumbent without fresh-population validation.

Evidence: existing locked final_complete.json and spatial_complete.json. No independent organizer validation. This is transductive, full-pool, coordinate-aware inference, not an inductive unseen-city claim. The packaged artifact is bound to the supplied ordered Amsterdam pool. Rebuilding for another pool requires organizer feature data, feature order, source-fitted scaling and matching lattice coordinates. The final query population excludes the designated 800-label development bank and current support. Development labels are additional research supervision beyond each episode budget; repeated episodes are correlated. The inherited ASTRA recipe has historical audit exposure. No independent organizer-held-out validation is claimed, and protocol eligibility must be confirmed against organizer rules.

Geographic extrapolation remains a limitation: the four-direction spatial mean is 0.694216 and the worst direction is 0.644816, versus ASTRA's 0.696672 and 0.658183. Coordinate-RF is therefore selected for the stated random-pixel/full-pool use case, not universal superiority. Frozen configurations, hashes, label-free prediction replay, support/query separation and saved confusion matrices support reproducibility. No competitor code, data or predictions are included. No overnight exploratory candidate replaces the incumbent without fresh-population validation.
````````

</details>
