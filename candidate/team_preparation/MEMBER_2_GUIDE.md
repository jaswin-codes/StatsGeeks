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
