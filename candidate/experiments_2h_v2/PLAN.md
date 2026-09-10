# Predeclared v2 gap attack

Frozen EXP-010 and historical evidence are read-only (SHA256 manifest in ../competitor_forensics).
No independent target development population exists. All new arms are audit-based exploration, NOT independent validation. Fresh seeds are episode stability checks on the SAME population, not new geography.

## First stage (before seeing v2 scores)
- Matched ten seed-31337 nested EXP-010 episodes, budgets 5/25/50/100/200, full support-complement query, four-class macro F1, population SD.
- Controls EXP-010 and EXP-F, exact historical prediction implementation.
- EXP-H: within-class source/support covariances normalized to matched trace; mix source with effective pseudocount k or 4k or fixed 1/2, then EXP-F's 1/2 identity regularization. Local class means stay unchanged. Separate mean-transfer arm adds 0.6*source_weight of centred Madrid class offsets. This isolates metric and mean changes.
- Target pool metric: unlabeled target total covariance, half identity ridge, applied to local prototypes (global); separately whiten representation then estimate support residual covariance (global+F); global+H follows same source/support mixing after whitening.
- Simple classifier capacity control: all-60 support multinomial logistic regression C=1, and support RF (200 trees, balanced classes, leaf minimum 2, sqrt columns; fixed regularization, not competitor's tuned config).
- Global CORAL: independently match source mean/covariance to full target pool on Madrid-scaled 60 features, train the same RF. Source/local RF probability blending alpha exactly {0,.25,.5,.75,1}, both with/without pool-whitened local RF. No class-conditional alignment until a useful global effect is measured.
- Spatial prediction smoothing: independent uniform immediate grid ring (up to eight closest neighbours plus self) as simplest clean spatial mechanism; compare logistic/RF predictions before/after. No true-label anchoring. Geometry-only smoothing uses pool coordinates; it is transductive and spatially autocorrelated, not query-label leakage.

## Validation trigger
Any mean >.70 triggers audit before further optimization: exact clean-process predictions, fresh seed 8675309, historical x-half split with 10-key-unit buffer, same features, saved confusion/per-class scores, data-ID correspondence, proximity, feature provenance and model-selection caveats. No promotion from a single best episode.

Competitor source is executed only in the separate forensics harness. Our candidate implementation does not import or copy their code. Missing tuned configuration must never be guessed and called exact reproduction.
