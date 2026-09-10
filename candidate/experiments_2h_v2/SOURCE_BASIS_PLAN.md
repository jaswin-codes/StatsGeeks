# Remaining low-shot gap: source alignment coordinate basis

The adaptive local candidate is now audited: .730028 at200, fresh-seed .729666, spatial .689830; exact clean-process source and local probabilities pass. At5 it remains .634935, below the reproduced competitor .661236 on matched episodes. Do not change the local model or smoothing further while testing this hypothesis.

The competitor aligns raw-unit source vectors. Our independently implemented source prior aligns Madrid-standardized120-feature vectors. CORAL's symmetric whitening/recolouring is not invariant to arbitrary diagonal changes of coordinates for a downstream axis-split forest; its absolute numerical ridge also changes relative scale. Our local-basis ablation already found small changes from this distinction.

One paired source-only ablation: recover physical units using the supplied Madrid scaler, append the SAME immediate-grid means, and run the SAME200-tree leaf2 source forest with global alignment and ONE pseudo-class alignment iteration. Keep local adaptive covariance, support-label budget schedule, probability blend and Gaussian smoothing exactly unchanged. Save raw-unit global and one-iteration priors; use existing immutable local probability fields to isolate the change. No new temporal features, no target labels for alignment, no copying a competitor tuned configuration.

This is exploration on reused audit episodes. If no clear transferable gain, retain the standardized source prior. If useful, exact source refit and fresh/spatial fields must pass before freezing. Deferred local leaf1 capacity control is lower priority than explaining the remaining low-shot source-prior gap.
