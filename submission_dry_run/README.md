# StatsGeeks EXP-010 — judge dry-run package

> **Staging package only.** The organiser's upload mechanism, archive name, and exact directory structure are not specified in the local materials.

## What is this?

The frozen EXP-010 transfer solution for Madrid → Amsterdam building-age classification.

## Included

- `model/exp010_stage1_madrid.pkl` — frozen Madrid Stage 1 state
- `code/exp010_predict.py` — Amsterdam support adaptation and query prediction CLI
- `code/test_exp010_interface.py` — synthetic, non-scientific interface smoke test
- `evidence/SHA256SUMS.txt` — package checksums
- `presentation/StatsGeeks_BuildingAge.pptx` and `.pdf`
- `justification/written_justification.txt` — written justification (404 words)

Dependency: Python 3.10+ and NumPy (`python -m pip install -r requirements.txt`).

## Run

Prepare `support.npz` with keys `X`, `y`, `feature_names`, and `query.npz` with keys `X`, `feature_names`. The query file needs no labels. Then run, for example:

```bash
python code/exp010_predict.py --artifact model/exp010_stage1_madrid.pkl --support support.npz --query query.npz --shots 5 --seed 31337 --output predictions.npy
```

The output is a one-dimensional NumPy `.npy` array of predicted integer classes 1–4. Run the software-only smoke test with:

```bash
python code/test_exp010_interface.py
```

## Input contract

- Support `X`: shape `(4 × shots, 60)`, finite numeric values, with exactly `shots` rows for each class.
- Support `y`: one-dimensional labels 1–4 corresponding to support rows.
- Query `X`: shape `(n_query, 60)`, finite numeric values; no query labels are accepted or required.
- Both NPZ files must include `feature_names` in the exact order below.
- The 60 features must already have the Madrid-fitted preprocessing used by EXP-010 applied.

Exact feature order:

```text
Blue_mean, Green_mean, Red_mean, NIR_mean, SWIR1_mean, SWIR2_mean,
Blue_std, Green_std, Red_std, NIR_std, SWIR1_std, SWIR2_std,
NDVI_mean, NDBI_mean, UI_mean, MNDWI_mean, BSI_mean,
NDVI_std, NDBI_std, UI_std, MNDWI_std, BSI_std,
Blue_early_mean, Green_early_mean, Red_early_mean, NIR_early_mean,
SWIR1_early_mean, SWIR2_early_mean,
Blue_early_std, Green_early_std, Red_early_std, NIR_early_std,
SWIR1_early_std, SWIR2_early_std,
Blue_late_mean, Green_late_mean, Red_late_mean, NIR_late_mean,
SWIR1_late_mean, SWIR2_late_mean,
Blue_late_std, Green_late_std, Red_late_std, NIR_late_std,
SWIR1_late_std, SWIR2_late_std,
d_Blue_mean, d_Green_mean, d_Red_mean, d_NIR_mean,
d_SWIR1_mean, d_SWIR2_mean,
d_Blue_std, d_Green_std, d_Red_std, d_NIR_std,
d_SWIR1_std, d_SWIR2_std,
has_early_data, has_late_data
```

## Supported budgets and frozen schedule

| Shots/class | k | λ |
|---:|---:|---:|
| 5 | 30 | 0.6 |
| 25 | 45 | 0.0 |
| 50 | 45 | 0.0 |
| 100 | 45 | 0.0 |
| 200 | 45 | 0.0 |

## Important limitation

Raw Parquet → 60-feature construction is **not provided** because the legacy feature builder remains label-dependent. This package is runnable only when inputs satisfying the preprocessed 60-feature contract are supplied.
