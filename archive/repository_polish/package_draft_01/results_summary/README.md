# Locked results summary

Selected model: **Coordinate-RF** (`Coordinate_RF` in frozen machine files).

| Labels/class | Macro F1 | Population SD | Episodes |
|---:|---:|---:|---:|
| 5 | 0.650253 | 0.011246 | 200 |
| 25 | 0.687664 | 0.012145 | 200 |
| 50 | 0.708436 | 0.011277 | 200 |
| 100 | 0.729839 | 0.008802 | 200 |
| 200 | 0.749299 | 0.005716 | 200 |

Source: `model/evidence/final_complete.json` (relative to package root).
Values are formatted to six decimals without altering saved scientific precision.
See `learning_curve.csv` for all matched methods and full stored precision.
200 paired episodes per budget; population SD; fixed Amsterdam query population
with development-bank and current-support exclusions. No new scientific run.
Spatial mean/worst: 0.694216 / 0.644816; matched ASTRA: 0.696672 / 0.658183.
The unchanged `LOCKED_REPORT.md` preserves historical preflight claims; they are
not fresh validation of this relocation. Its short relative paths refer to the
original canonical package. New-package evidence is under `model/evidence/`.
