# Methods

## Task and data
We study four-class building-age classification from Landsat spectral trajectories, transferring labelled Madrid data to Amsterdam. The supplied preprocessing artifact contains 76,263 Madrid rows, 25,992 Amsterdam rows, 60 ordered features, a Madrid-fitted scaler and integer lattice-coordinate keys. These are pixel-level observations, not independent buildings. Feature groups include six bands, five spectral indices, temporal means/standard deviations, early/late summaries, differences and availability indicators. The exact feature order is recorded in the inference manifest. We consume the existing preprocessing artifact unchanged; no features were engineered in publication phase.

Class IDs 1–4 correspond to city-specific age intervals: Madrid pre-1960, 1960–1984, 1984–2004, 2004–2024; Amsterdam pre-1945, 1945–1984, 1984–2004, 2004–2024. Boundary handling and preprocessing remain defined by the original preprocessing notebook and hashed artifact, not by these shorthand interval labels. Raw datasets are locally present but historically Git-ignored; redistribution permissions are not established by this repository.

## Frozen Coordinate_RF
The packaged implementation is an exact copy of `candidate/autonomous_runs/20260909_1727/agf_model.py`, with the development lock `{"coord": true}` applied to its unchanged BASE configuration. It is a pool-bound, transductive method: all ordered target features and coordinates are available, but target labels are supplied only for the designated support set.

### Contextual source prior
Madrid-standardized inputs are restored to raw feature units using the saved source scaler. For each city, 60 raw inputs are concatenated with their 3×3 available-lattice-neighbour averages, yielding 120 contextual inputs. Source features undergo global covariance transport to the unlabelled target distribution: source centring, regularized inverse-square-root source covariance, target square-root covariance and target mean. A 200-tree, class-balanced random forest (leaf size 2, seed 42) generates target pseudo-labels. Source class blocks are transported once more toward pseudo-labelled target blocks where the latter contain more than 120 rows. A second identical forest supplies the fixed four-class target prior. No target truth enters either forest. This source fit was completed previously and was not repeated for publication.

### Episode adaptation
For budget b, the episode provides b labels in each of four classes. Pool covariance C of the 60 raw inputs is shrunk as

`C_b = (1-rho) C + rho diag(diag(C)) + 1e-7 I`, with `rho = min(1, 60/(4b))`.

Pool-centred inputs are multiplied by `C_b^(-1/2)`, using the frozen eigendecomposition/eigenvalue-floor implementation. Two coordinate columns, centred and scaled on the full pool (standard deviations bounded below by 1), are appended. The local classifier is a 200-tree random forest with balanced class weights, leaf size 1, square-root feature subsampling, seed 42 and four fit workers. The inference implementation serializes probability aggregation to preserve deterministic results.

Local probabilities are blended with the fixed contextual prior using `alpha = 20/(20+4b)`. One Gaussian graph averaging step uses nine nearest coordinate neighbours and sigma 1 in lattice-key units. No support-truth clamping or query-label anchors are used. The class with largest final probability is returned. The artifact is tied to target row order and is not a generic unseen-city estimator.

## Frozen controls and historical comparison
- **ASTRA / ASTRA_AGF:** the same contextual prior, local RF, adaptive covariance and Gaussian graph, without the two local coordinate columns. Historical ASTRA's reported 0.735239 belongs to an earlier audit population and must not be combined with the current paired scores.
- **EXP-010:** Madrid-only 500-tree RF feature ranking/weights; top 30 features at five shots, top 45 otherwise, weighted by square-root source importance. Support class prototypes shrink toward recentered Madrid class offsets with weight 0.6 at five shots and zero otherwise. Classification uses squared Euclidean distance. Its source artifact and interface remain unchanged.
- **EXP-F:** the same compact source-ranked representation, target support class means, and a pooled within-support residual covariance regularized by 50% isotropic trace shrinkage plus `1e-8 I`. Classification uses the corresponding Mahalanobis distance; no target-pool covariance or coordinate graph is used.

Controls are operational comparisons, not equally supervised causal interventions. In particular transductive methods use full-pool features/coordinates, whereas EXP-010 and EXP-F are inductive support-adaptation controls.

## Development and freeze protocol
A fixed stratified bank of 800 target development labels (200/class; seed 20260909) supported five-fold development diagnostics (160 training/40 validation per class). Preselected candidates also underwent repeated support-only holdouts across budgets and four support-only spatial safeguards. The archived selection lock records the actual predeclared mean/wins/geographic rule and chosen configuration. These additional development labels are research supervision beyond any one episode's stated budget. Historical ASTRA was audit-selected; subsequent support-only selection cannot undo that exposure.

No optimization, model changes, candidate reselection, or source refitting occurred during publication. Ten fixed-reference verification calls (five budgets each for Coordinate_RF and ASTRA) were used solely for exact prediction checks and observational diagnostics.

## Evaluation and uncertainty
The locked random-pixel evaluation uses seed 20260910, 200 paired trials and budgets 5, 25, 50, 100 and 200. Support sets are class-stratified, nested across budgets within trial, and sampled outside the fixed development bank. Query sets exclude both the entire development bank and current support. All four methods share the saved support/query sets. Query truth is used only to score predictions and evaluate diagnostics. Benchmark stratification necessarily uses labels to construct support episodes; this is explicitly separate from estimator fitting and adaptation.

Macro F1 averages class F1 equally. Learning-curve error bars are population SD across 200 episodes (`ddof=0`). Confusion counts aggregate query appearances, including repeated pixels; pooled F1 therefore differs from mean per-episode F1. Paired tests, episode-bootstrap intervals and effect sizes are defined in [STATISTICAL_ANALYSIS.md](STATISTICAL_ANALYSIS.md). They describe conditional support-sampling uncertainty, not independent cities or pixels.

The spatial audit uses 200 shots/class and ten trials per direction (low/high x and low/high y support, opposite-side query), a median cut and a ten-key-unit buffer. Coordinates are lattice keys, not assumed metres. We report both axis means, worst directional mean and four-direction mean; no favourable direction is selected.

## Leakage safeguards and reproducibility
Inference receives source labels and designated episode support labels, never query truth. Saved support/query and development/query disjointness and all 4,000 prediction-derived confusion matrices were checked during publication. The inference-only bundle excludes sealed evaluation truth and development labels. Local trusted pickle artifacts are SHA256-checked before loading; hashes establish integrity, not security for arbitrary untrusted pickle files. Freeze manifests verify protected implementations and evidence byte-for-byte. The earlier fresh-source replay matched 4,000 prediction arrays; publication performed only ten fixed-reference replays and evidence recomputation, not another expensive full refit.

## Limitations and future work
One target city, spatial autocorrelation, historical audit exposure, 800 extra development labels, coordinate dependence and city-specific age boundaries limit external claims. Coordinate_RF is worse on some geographic directions despite random-pixel gains. RF impurity importance on whitened axes is descriptive and biased; transfer-stage plots are not additive causal ablations. Calibration is evaluated, not fitted. Future work should obtain genuinely unseen-city and organizer-held-out evidence under predeclared protocols and clarify data licensing. These are recommendations, not experiments conducted here.
