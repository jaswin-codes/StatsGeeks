# Member 2 — preprocessing baseline handoff

## Status
Notebook 3 completed: every code cell executed in order with Python and Matplotlib's headless Agg backend. Preprocessing validated. Notebook 4 was not run. No files in `original/` were edited by this work.

## Environment
Both requested commands exited 1:
- `python -c "import sklearn; print(sklearn.__version__)"`
- `python -c "from sklearn.preprocessing import StandardScaler; print(StandardScaler)"`

Both failed while loading SciPy in Python 3.14 with:
```
ImportError: DLL load failed while importing _rigid_transform_cy: An Application Control policy has blocked this file.
```
This is a confirmed Windows policy block, not a missing scaler import. No policy bypass attempted. Smallest environment fix: have the administrator approve the blocked SciPy binary or select an approved Python environment with working scikit-learn/SciPy.

Jupyter CLI/nbconvert was unavailable. An earlier direct run reported `Command aborted` at the plotting cell, without a Python traceback. The successful rerun used Agg; the expected non-interactive `plt.show()` warning is in the log. The runner executes all code, but does not capture notebook rich-display outputs or embed figures.

## Exact organiser-notebook deviations
Source comparison found only three changed cells:
1. Cell 2: import `working.minimal_standard_scaler.StandardScaler` instead of sklearn's scaler.
2. Cell 4: resolve input paths with `Path('data')`, falling back to `Path('../data')`.
3. Cell 19: save under `DATA_DIR / 'preprocessed'`, creating parents if necessary.

The local scaler supports only `fit`, `transform`, `fit_transform` and exposes `mean_`, `var_`, `scale_`, `n_features_in_`. It uses population variance (`ddof=0`), unit scale for zero-variance columns, and fits Madrid only. The actual notebook data passed sklearn's numerical constant-column criterion check. General sklearn API compatibility is not claimed; direct numerical comparison against imported sklearn remains unavailable because of the policy block. No feature engineering or preprocessing optimisation/redesign was performed.

## Validation
| City | Feature matrix | Labels |
|---|---|---|
| Madrid | (76263, 60) | (76263,) |
| Amsterdam | (25992, 60) | (25992,) |

Passed: finite features; labels in {1,2,3,4}; aligned pixel-ID dimensions; 60 unique ordered feature names matching feature groups; scaler type and all four attributes; fitted means/population variances/scales; Madrid zero means and unit nonconstant variances; both cities reproduced by scaler.transform; pickle array equality after reload. Separate fresh-process pickle reload also passed.

Full feature names and execution results: `working/member2_preprocessing_execution.log`.

## Artifacts
- `data/preprocessed/preprocessed_data.pkl` — 50,721,695 bytes (48.4 MiB).
- `working/minimal_standard_scaler.py` — required to unpickle the scaler.
- `working/3-Preprocessing_member2_baseline.ipynb` — working notebook.
- `working/3-Preprocessing_member2_baseline_executed.ipynb` — execution counts and text outputs.
- `working/run_member2_preprocessing.py` — reproducible headless runner and validation.
- `working/member2_preprocessing_execution.log` — complete successful run log.

Run/reload from the repository root so `working.minimal_standard_scaler` is importable. When loading from elsewhere, add the repository root to Python's import path. Ship the scaler module with the pickle.

## Remaining blockers
None for preprocessing. Scikit-learn remains blocked for downstream modelling; administrator approval or an approved environment is still needed. Original notebook SHA256 before/after the run: `86136f0ab901a4fd15f45e7545c5107f98fb17ed271e9c46c12d0d614b261175`.

## Suggested commits
- `fix(preprocessing): add minimal scaler for policy-blocked SciPy environment`
- `test(preprocessing): validate baseline artifact and document handoff`

Do not include unrelated workspace changes. Store the generated pickle according to the team's large-artifact policy. Stop here; Notebook 4 is outside this handoff.
