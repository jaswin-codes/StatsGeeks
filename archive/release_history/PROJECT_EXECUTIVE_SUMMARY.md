# StatsGeeks — five-minute research summary

## Problem and dataset
Predict four building-construction eras for 30 m Landsat pixels. Madrid supplies
labelled source learning; Amsterdam supplies sparse support labels. Historical
data documentation records 76,263 Madrid / 25,992 Amsterdam pixels, 1984–2025,
with six spectral bands. City-specific first age cutoffs are 1960 and 1945.

## Transfer strategy and Coordinate-RF
A source-learned, context-aware probability prior is transferred to the full
unlabelled Amsterdam pool. A support-only, 200-tree RF uses 60 adaptively whitened
features plus two standardized coordinates. Blend probabilities with source weight
`20/(20+4b)` and apply nine-neighbour Gaussian smoothing. The source knowledge is
reused; it is not merely a target-only RF. Implementation ID: `Coordinate_RF`.

## Why it can work
Spectral summaries encode urban context; local coordinates help interpolate
spatially coherent construction eras. A source prior offers information when
support is scarce. This is a rationale consistent with the frozen evidence,
not a causal explanation or proof of universal transfer.

## Locked results
| Labels/class | Macro F1 | Population SD | Episodes |
|---:|---:|---:|---:|
| 5 | 0.650253 | 0.011246 | 200 |
| 25 | 0.687664 | 0.012145 | 200 |
| 50 | 0.708436 | 0.011277 | 200 |
| 100 | 0.729839 | 0.008802 | 200 |
| 200 | 0.749299 | 0.005716 | 200 |

Population SD across 200 paired fixed-city random-pixel episodes per budget.
At 200/class, ASTRA is 0.733037. Coordinate-RF is not spatially superior:
four-direction mean 0.694216 vs 0.696672; worst 0.644816 vs 0.658183.
Five-shot benefit is negligible. No new scientific work occurred during polish.

## Lessons and future work
Spatial interpolation and geographic extrapolation are different objectives.
Repeated support draws do not replace a fresh city. Full-pool target access,
800 additional development labels and historical audit exposure must be disclosed.
Future work, not performed here: independent geographic validation, approved
protocol clarification and a portable raw-data inference contract.

## Competition strengths and readiness
Strengths: explicit source-state reuse, locked five-budget evidence, matched
comparisons, honest spatial tradeoffs, readable notebook and traceable artifacts.
Unresolved: organizer eligibility, explanation limit, rights/license, independent
validation and clean-environment/runtime/visual sign-off. The package is prepared
for review, not falsely certified for unconditional upload.

Start with [the package](../../FINAL_SUBMISSION/README.md),
[validation](DELIVERABLE_VALIDATION.md) and [pre-flight](FINAL_PRE_FLIGHT.md).
