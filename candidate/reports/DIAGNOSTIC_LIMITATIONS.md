# Diagnostic scope and unavailable evidence

- All four models: learning curves, distributions, confusion and per-class metrics use all saved locked episodes. Confusion images use 200 shots; CSV/Markdown cover every budget.
- Transfer: source-only, target-only and blended are observational probabilities from the fixed ASTRA replay before graph smoothing; final ASTRA/Coordinate_RF share its query. One predeclared episode, not new ablation trials or additive causal effects.
- RF importance: captured from the unmodified local Coordinate_RF verification fit. The 60 whitened axes mix original spectral inputs; do not relabel them as raw feature importance. Coordinate usage is split importance, not causal attribution.
- Covariance diagnostics: label-free saved population covariance and the exact frozen shrinkage equation. No covariance optimization.
- Calibration: ASTRA and Coordinate_RF probabilities from the first predeclared 200-shot replay, ten fixed bins. No post-hoc calibration. EXP-010 and EXP-F probability calibration is unavailable from saved hard predictions and was not invented.
- Historical four-model CPU/peak memory and separated fit/predict measurements are unavailable. Fresh instrumentation covers ASTRA and Coordinate_RF only. Sampled RSS is not exact peak allocation.
- Factorial mechanisms are operationally entangled; no additive contribution ladder is justified. All legacy exploratory outputs remain historical, with their original caveats.
