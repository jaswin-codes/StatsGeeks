# Written justification · Coordinate-RF

Coordinate-RF predicts four building-construction eras from Landsat pixels, transferring labelled Madrid knowledge to Amsterdam with scarce target labels. Macro-F1 weights the four classes equally.

## Model design and transfer

The source branch combines 60 spectral features with local lattice averages, aligns source and unlabelled-target covariance, and performs one prediction-based class-conditional refinement without query truth. Two source random forests produce the target probability prior.

The local branch adaptively whitens 60 features using full unlabelled-target covariance, appends two standardized coordinates, and fits a balanced 200-tree random forest using support labels only. The source probability weight, `20/(20+4b)`, decreases as the budget `b` grows. Nine-neighbour Gaussian smoothing incorporates spatial context without query labels. This combination addresses source-target mismatch and limited target supervision.

## Frozen results and interpretation

At 5, 25, 50, 100 and 200 labels/class, macro-F1 is respectively **0.650253, 0.687664, 0.708436, 0.729839 and 0.749299**. Population SD is respectively **0.011246, 0.012145, 0.011277, 0.008802 and 0.005716**, across 200 paired episodes per budget—not confidence intervals.

Performance improves with support size. At 200/class the matched gain over historical ASTRA is 0.016262, with 200/200 paired wins; five-shot superiority is inconclusive.

## Limitations

These are fixed-city random-pixel results, not organizer-held-out or unseen-city scores. Inference is transductive and bound to the original ordered Amsterdam pool. A separate 800-label development bank is excluded from final queries but remains additional research supervision.

Spatial extrapolation is weaker: Coordinate-RF's four-direction mean is 0.694216 versus matched ASTRA's 0.696672. Full-pool, coordinate and extra-supervision eligibility requires organizer confirmation. Future independent-city evaluation is proposed, not performed.

---

Presentation-only concise companion. [Frozen results](../../candidate/reports/RESULTS.md); the [original sealed explanation](../../FINAL_SUBMISSION/written_explanation/written_justification.txt) is preserved unchanged.
