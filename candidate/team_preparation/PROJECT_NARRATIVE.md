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
