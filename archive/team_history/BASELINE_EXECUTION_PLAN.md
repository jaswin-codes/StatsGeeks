# Overview

The organiser baseline is a four-class, one-row-per-geographic-pixel workflow from **Madrid** to **Amsterdam**. Notebook 3 derives labels from `weighted_mean_year`, converts each raw pixel-year record into a complete annual spectral trajectory, aggregates that trajectory into 60 features, standardises with a scaler fitted on all Madrid pixels, and serialises the resulting arrays. Notebook 4 uses those arrays to:

- estimate Madrid Random Forest performance with 5-fold × 5-repeat stratified CV;
- fit a 500-tree, class-balanced Random Forest on all Madrid data;
- apply that forest zero-shot to Amsterdam; and
- run Amsterdam target-only nearest-class-prototype experiments using labelled support pixels.

The prototype path uses Madrid-fitted feature scaling but **does not use the fitted Madrid Random Forest or a learned Madrid representation**. It is therefore the organiser's reference pipeline, not evidence of genuine supervised transfer.

Notebook 2 is exploratory only. It reads both raw files, derives labels for EDA, makes diagnostics/plots, and creates no input consumed by Notebook 3 or 4.

# Notebook Execution Order

1. **`original/1-Introduction.ipynb` — reference only**
   - States the four-class task, Madrid source/Amsterdam target direction, macro-F1 reporting, support budgets (5, 25, 50, 100, 200 per class), and intended deliverables.
   - Does not create computational artefacts.

2. **`original/2-Reading_Data.ipynb` — optional EDA, before or independently of preprocessing**
   - Reads `../data/madrid_train.parquet`, then `../data/amsterdam_data.parquet`.
   - Derives `age_class`, flattens first QA-valid observations, applies the Blue > 15,000 outlier rule, and produces quality, coverage, time-series, distribution, and plot diagnostics.
   - It has no saved pipeline output and is **not** an execution dependency of Notebook 3.

3. **`original/3-Preprocessing.ipynb` — required**
   - Reads the two raw Parquets.
   - Builds scaled 60-feature Madrid and Amsterdam matrices plus labels, pixel keys, feature metadata, and the fitted scaler.
   - Writes `../data/preprocessed/preprocessed_data.pkl`.

4. **`original/4-Modelling.ipynb` — required after Notebook 3**
   - Reads `../data/preprocessed/preprocessed_data.pkl`.
   - Runs Madrid CV, fits the final Madrid RF in memory, evaluates zero-shot Amsterdam predictions, and evaluates repeated Amsterdam prototype episodes.
   - Produces notebook displays/printed results only; it does not save a model, predictions, scores, or submission file.

**Computational dependency:**

`madrid_train.parquet` + `amsterdam_data.parquet` → Notebook 3 → `preprocessed_data.pkl` → Notebook 4

# Pipeline Diagram

```text
Input
  madrid_train.parquet + amsterdam_data.parquet
  (pixel-year rows; three observation slots; metadata and weighted_mean_year)
        ↓
Preprocessing
  derive city-specific age_class; select first QA-valid slot per band;
  drop incomplete band rows; remove Blue > 15,000; record early/late coverage;
  complete annual pixel trajectories by interpolation and edge fill
        ↓
Feature Generation
  compute five indices; aggregate each pixel into ordered 60 features;
  StandardScaler fit on all Madrid features and applied to Amsterdam
        ↓
Training
  Madrid 5×5 repeated stratified CV of a 500-tree balanced Random Forest;
  then fit the same RF on all Madrid features
        ↓
Prediction
  RF Madrid validation predictions; final-RF zero-shot Amsterdam predictions;
  target-only Amsterdam nearest-prototype predictions from per-episode support means
        ↓
Evaluation
  macro F1; row-normalised confusion matrices (recall); classification report;
  displayed feature-importance, uncertainty, accuracy, and learning-curve plots
        ↓
Outputs
  preprocessed_data.pkl plus in-memory objects and notebook-only displays
```

# Files Created

| Expected file | Created by | Contents |
|---|---|---|
| `../data/preprocessed/preprocessed_data.pkl` | Notebook 3 | Dictionary containing `X_madrid`, `y_madrid`, `X_amsterdam`, `y_amsterdam`, ordered `feature_names`, Madrid-fitted `scaler`, per-city `(px_key, py_key)` arrays, and feature-group lists. |

No other file is written by the organiser notebooks. In particular, Notebook 4 does **not** save `rf_final`, CV folds/scores, support indices, prototypes, predictions, figures, a submission, or an adaptation artefact. Its model, result dictionaries, confusion matrices, and plots are kernel/notebook-output state only.

# Potential Failure Points

1. **Path/layout mismatch.** The notebooks expect to run from a sibling `notebooks/` directory and use `../data`; this repository stores notebooks in `original/` and data in `data/`. The expected parent directory may not exist. `output_dir.mkdir(exist_ok=True)` lacks `parents=True`.
2. **Required pickle is absent initially.** Notebook 4 cannot start until Notebook 3 has completed and produced the pickle.
3. **Raw input/schema assumptions.** The baseline requires both Parquets, the listed metadata, all six `*_1..3` bands, and `qa_valid_1..3`. It assumes stable pixel identity is `(px_key, py_key)` and a shared 1984–2025 annual horizon.
4. **Label-dependent feature construction.** Notebook 3 carries `weighted_mean_year` and `age_class` through flattening/gap filling and filters feature rows with `age_class.notna()`. It cannot directly generate hidden-test/unlabelled inference features without labels, even though those fields are excluded from `FEATURE_COLS`.
5. **Boundary sensitivity.** `pd.cut` defaults to right-inclusive intervals: Madrid ≤1960, (1960,1984], (1984,2004], >2004; Amsterdam ≤1945, (1945,1984], (1984,2004], >2004. Changing inclusivity changes labels.
6. **Observation-selection limitations.** It chooses the first QA-valid slot independently per band, not one coherent scene/slot, and does not try later slots when a selected valid observation is spectrally implausible. It drops any row lacking any of the six selected bands.
7. **Unverified data-quality assumptions.** The sole added spectral filter is `Blue <= 15,000`; QA-valid rows may still contain zero, saturated, extreme, haze, sensor, or seasonal artefacts. The documented summer-only assumption conflicts with recorded all-month acquisitions.
8. **Interpolation artefacts.** Missing annual values are linearly interpolated, while leading/trailing gaps are filled with the nearest observation. This makes every trajectory complete but can manufacture flat/change signals and makes period statistics depend on data availability. Coverage flags are retained, but observation counts/gap lengths are not features.
9. **Temporal leakage risk by design.** Features use the full 1984–2025 trajectory, including signals surrounding the true construction period. This is the starter baseline behaviour; suitability for a hidden inference horizon must be confirmed before reproduction is claimed beyond the supplied data.
10. **Global scaling before CV.** Standardisation is fitted on all Madrid pixels in Notebook 3 before Notebook 4 splits CV folds. This exposes validation-fold feature distribution statistics to training and is not fold-safe.
11. **CV protocol is not spatial.** `RepeatedStratifiedKFold` splits pixel rows rather than spatial blocks. One pixel is already collapsed to one row, so years do not split, but nearby pixels can appear in training and validation. Repeated-fold scores are correlated despite notebook prose suggesting repeats are independent.
12. **Resource pressure/nondeterministic scheduling.** Madrid CV fits 25 forests with 500 trees and `n_jobs=-1`, potentially monopolising shared CPUs/RAM. The RF seed is fixed, but uncontrolled parallelism and package versions can still affect runtime/reproducibility.
13. **Prototype evaluation uses target labels broadly.** The sampler sees all Amsterdam labels to draw supports and scores on all remaining labels. This is valid only as a controlled reference episode protocol; support draws, episode IDs, and final-audit separation are not saved.
14. **Prototype budget/sampling quirks.** It includes organiser-unstated 10-shot diagnostics; uses one advancing RNG across budgets/trials, so episodes are neither explicitly recorded nor nested/matched across budgets; and silently reduces a requested support count with `min(n_shots, len(cls_idx))`.
15. **No genuine source-trained adaptation state.** Amsterdam prototypes are computed directly from Amsterdam support vectors in Madrid-standardised raw feature space. The trained `rf_final` is unused in that path.
16. **Metric/reporting interpretation.** Macro F1 is correct, but displayed confusion-matrix rows are recall proportions, not per-class F1. Zero-shot and prototype evaluation use known Amsterdam labels, so their printed values are reference results, not hidden-test predictions.
17. **Loss of results/artifacts.** Final RF, scaler contract details such as horizon/configuration, figures, maps, predictions, and scores are not explicitly exported/reload-tested. Restarting the kernel loses Notebook 4 state.

# Validation Checklist

## Inputs and preprocessing

- [ ] Both raw files resolve at the configured paths and have the expected columns.
- [ ] Label counts reflect the stated four right-inclusive city-specific intervals.
- [ ] Flattened data have six selected finite bands per retained pixel-year and the Blue filter is applied.
- [ ] Early/late indicators are calculated before gap filling.
- [ ] Gap-filled series contain every annual year in the chosen horizon for every retained pixel.
- [ ] Five indices are finite after calculation; all 60 ordered feature columns exist and contain no NaNs.
- [ ] Feature matrices have one row per geographic pixel: expected reference shapes are Madrid `(76263, 60)` and Amsterdam `(25992, 60)`.
- [ ] The scaler is fitted on Madrid and transforms Amsterdam; pickle keys, feature order, group lists, labels, and pixel-key alignment are present after reload.

## Training and prediction

- [ ] Notebook 4 loads the pickle and finds exactly four classes in each label vector.
- [ ] Madrid CV performs 25 fits with `n_estimators=500`, `class_weight='balanced'`, and seed 42.
- [ ] Every CV fold reports macro F1 and the aggregate is mean/std over 25 fold scores.
- [ ] The final RF fits all Madrid rows and returns a four-class prediction vector for Madrid and Amsterdam.
- [ ] Each prototype episode selects the configured number of distinct support pixels per class; support and query masks are disjoint and exhaustive.
- [ ] Prototype predictions are made only from support features/labels and query features.

## Evaluation/output checks

- [ ] Macro F1 uses all classes 1–4; confusion matrices are row-normalised only after raw counts are computed.
- [ ] Amsterdam reference experiments report 10 trials at 5, 10, 25, 50, 100, and 200 shots/class, with 10-shot explicitly labelled diagnostic.
- [ ] `../data/preprocessed/preprocessed_data.pkl` exists and can be loaded in a clean session.
- [ ] Any displayed figures/results are treated as notebook output, not saved deliverables.

# Success Criteria

A successfully reproduced organiser baseline means, without altering organiser notebooks or algorithms:

1. Notebook 3 runs from the configured working-copy location and creates a reloadable pickle with the stated 60-feature contract and reference pixel dimensions.
2. Notebook 4 runs from that pickle in a clean kernel, completes the Madrid 25-fit CV, final Madrid RF, Amsterdam zero-shot evaluation, and 10-trial prototype loop.
3. Reported values are identified as **reproduced baseline evidence** only after execution. Until then, the saved organiser references are approximately Madrid CV macro F1 `0.6179 ± 0.0043`, Amsterdam RF zero-shot `0.3427`, and prototype macro F1s `0.5437 ± 0.0324` (5), `0.5649 ± 0.0312` (10 diagnostic), `0.5986 ± 0.0176` (25), `0.6079 ± 0.0101` (50), `0.6129 ± 0.0097` (100), and `0.6150 ± 0.0036` (200).
4. The only persisted organiser pipeline artefact is the preprocessed pickle; absence of saved RF/adaptation/submission files is documented rather than misrepresented as a complete submission pipeline.

# Next Actions

1. Preserve `original/` notebooks and raw `data/*.parquet` unchanged.
2. Confirm the intended working-copy directory and configure project-relative paths before copying anything.
3. Record the raw-file checksums, Python/package versions, machine limits, and expected 1984–2025 horizon.
4. Create clearly named team-owned copies of Notebooks 3 and 4 only; do not change their baseline logic for the first run.
5. Add only the minimum portable path/parent-directory handling needed to execute those copies, and record every deviation.
6. Run the preprocessing copy once under coordinated resource limits; verify and reload `preprocessed_data.pkl`.
7. Run the modelling copy in a clean kernel; retain the printed CV, zero-shot, and per-trial prototype outputs as baseline evidence.
8. Compare reproduced outputs with the saved references, record discrepancies/seeds/versions, and do not call them reproduced if they differ without explanation.
9. Document that the baseline is not fold-safe, label-free, artifact-complete, or genuine supervised transfer before planning any authorised corrective implementation.
10. Obtain organiser clarification on hidden-test schema/horizon, target-label protocol, submission format, and whether source-scaling-only prototypes meet transfer requirements.
