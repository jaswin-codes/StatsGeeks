# Final predeclared smoothing ablation (after source-context stage)

Competitor's move from uniform to inverse-distance smoothing added about .011. Our exact immediate-grid cutoff did not match that gain, though spatial-half high-shot behavior improved. This suggests weighting/self-preservation rather than extra neighbour count deserves a controlled test.

Use saved full-pool probability fields, unchanged models/supports/features/prior weight. Compare:
1. existing uniform nine-nearest smoothing (control);
2. lazy diffusion: 1/2 original +1/2 uniform neighbour-smoothed field (a fixed conservative Markov-step convention);
3. Gaussian heat kernel over the same self+8 nearest points, exp(-distance^2/2), normalized rowwise. Unit lattice spacing is a physical one-pixel length scale, NOT a fitted bandwidth. No kernel sweep and no competitor inverse-distance formula copied.

Each kernel gets an explicit no-source and fixed-source comparison. No truth anchoring. Whole-pool probabilities, not hard labels, are smoothed. If this passes .73, stop further optimization and validate exact clean-process fields + fresh seeds + spatial split. Selection remains audit-based and must be disclosed.
