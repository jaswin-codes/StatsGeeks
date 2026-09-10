# Source-context hypothesis (predeclared)

The independent target-only120-feature context ablation raised raw RF200 from .689729 to .711043, but little remains after probability smoothing; context_pool_cc1_grid200=.723504 versus60-feature .723562. Do NOT blindly promote higher dimensionality.

Competitor's reproduced108-feature class-conditional source prior improved zero-shot .608341→.652704 compared with its60-feature fallback, while200-shot results were almost identical. This suggests feature context belongs primarily in the **source prior at low shots**, not necessarily a larger support classifier.

Test one new hypothesis: build immediate-grid averages of all60 source and target covariates (independent120-feature representation), globally align source, then one pseudo-class alignment iteration. Keep our already tested60-feature local heads, source-weight formula, and smoothing unchanged. Save global and one-iteration priors. No second-round tuning: stage2 found one round more useful for the final blend/spatial behavior despite the higher zero-shot score at round2.

This branch may train after the whitening-coordinate audit is recorded. All settings fixed; evaluate on10 original episodes, then exact clean repeat, seed8675309 and spatial split for any candidate to be promoted. Target-only context branch remains a separate negative/limited ablation.
