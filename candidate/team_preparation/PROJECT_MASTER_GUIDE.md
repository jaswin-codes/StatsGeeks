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

