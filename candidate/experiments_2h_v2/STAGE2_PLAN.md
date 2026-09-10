# Conditional second-stage plan (written after stage-1 audit, before stage-2 scores)

Stage 1 found >.70 at 100/200 from RF probability smoothing on unchanged 60 features. Optimization pauses until clean repeat, fresh-seed and spatial checks complete. This file does not authorize running until those checks are available.

Hypothesis 1: distant nearest-neighbour averaging blurs true construction boundaries. Replace uniform nine nearest pixels with **only immediate grid neighbours**, Chebyshev separation <=1 (coordinate keys form a unit lattice). Self included, uniform averaging, no tunable bandwidth. Compare this single change on raw and pool-whitened RF. This is NOT competitor's inverse-distance kernel.

Hypothesis 2: class-conditional target alignment improves the weak global prior. Independently refit globally aligned Madrid to predicted target class clouds; evaluate after one and two iterations. No true target labels in alignment or pseudo-label construction. Explicit covariance ridge in existing standardized 60-space, existing 200-tree RF. Stop after these two specified iterations, preserve both results.

Hypothesis 3 (only after 1/2 ablations): unify low-shot prior and high-shot support classifier with alpha=20/(20+4*budget). Twenty total prior-equivalent observations is the smallest complete 5/class episode. This is a predetermined smooth effective-sample-size heuristic, NOT per-budget alpha selection. Compare global versus class-conditional prior, local raw versus pool-whitened RF, then immediate-grid smoothing. Audit-based exploration, not independent validation.

Only if residual gap remains and time permits: independent context-feature augmentation by averaging **all** existing 60 covariates over immediate grid neighbours, retaining original 60 (120 total). Single representation hypothesis, fixed same RF, no imported competitor features/code. Raw temporal augmentation remains a separate optional branch, not silently stacked.

Fresh seed checks on the already accessed target population quantify sampling stability only. Final promotion must weigh the spatial-half split, not random-pixel F1 alone.
