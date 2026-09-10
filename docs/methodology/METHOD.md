# Method — Coordinate-RF

## Task and data
Madrid is the labelled source; Amsterdam is the few-shot target. Predict four
construction-era classes per 30 m Landsat pixel. Historical dataset documentation
records 76,263 Madrid and 25,992 Amsterdam pixels over 1984–2025; raw row counts
are not independent sample counts. Madrid class boundaries: ≤1960, (1960,1984],
(1984,2004], >2004. Amsterdam differs only at the first cutoff, 1945.
Construction-year labels are not predictive features.

## Source transfer
The saved recipe constructs 120 contextual columns from 60 spectral summaries
and their local lattice averages. Covariance alignment and one pseudo-class
refinement produce source-learned probabilities for the target pool. Target query
truth is not an input. Packaging consumes saved source state; it does not refit it.

## Few-shot branch
For budget `b`, shrink covariance toward its diagonal with
`rho=min(1,60/(4b))` and ridge `1e-7 I`. Whiten the 60 inputs, append two full-pool
standardized lattice coordinates, and fit a balanced RF with 200 trees, leaf size
1, sqrt feature sampling and seed 42 on support labels. Blend the source prior
with weight `20/(20+4b)`. Apply one Gaussian smoothing step, nine neighbours,
sigma 1. Frozen implementation and tie handling remain authoritative.

## Evaluation and interpretation
| Labels/class | Macro F1 | Population SD | Episodes |
|---:|---:|---:|---:|
| 5 | 0.650253 | 0.011246 | 200 |
| 25 | 0.687664 | 0.012145 | 200 |
| 50 | 0.708436 | 0.011277 | 200 |
| 100 | 0.729839 | 0.008802 | 200 |
| 200 | 0.749299 | 0.005716 | 200 |

Macro F1 averages class-wise F1 over classes 1–4. Variation is population SD over
200 paired support draws, conditional on one city. Extra 800-label development
supervision and historical audit exposure limit independence claims. Spatial
mean/worst 0.694216 / 0.644816 do not beat matched ASTRA (0.696672 / 0.658183).

Sources: [locked report](../../candidate/final_submission/reports/FINAL_REPORT.md),
[implementation](../../candidate/final_submission/model/agf_model.py),
[selection lock](../../candidate/final_submission/model/SELECTION_LOCK.json).
Coordinate-RF is the display name; `Coordinate_RF` is the unchanged machine ID.
