# Member 3 — Modelling Readiness Notes

Scope: downstream readiness only. No Random Forest redesign, no algorithm changes, and no Member 2 baseline preprocessing edits.

## 1. Notebook 4 modelling execution map

1. **Setup** (`original/4-Modelling.ipynb`, cells 3): imports NumPy/pandas/pickle/matplotlib/sklearn and defines class colours/labels.
2. **Load pickle** (cell 5): reads `../data/preprocessed/preprocessed_data.pkl` and binds all model inputs.
3. **Madrid model training / CV** (cell 7): runs `RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)` and fits a fresh `RandomForestClassifier(n_estimators=500, class_weight='balanced', random_state=42, n_jobs=-1)` per fold.
4. **Madrid CV evaluation/plots** (cells 7, 8, 11): calculates fold macro F1, stores out-of-fold predictions/probabilities/indices, plots fold scores, row-normalised confusion matrix, and spatial diagnostic maps.
5. **Final Madrid model training** (cell 14): fits `rf_final` on all Madrid rows using identical RF parameters. This is the Stage 1 in-memory source model.
6. **Feature importance** (cell 16): reads `rf_final.feature_importances_` and plots/prints top features.
7. **Amsterdam zero-shot evaluation** (cells 19, 20, 22): predicts Amsterdam with `rf_final`, calculates macro F1/classification report/confusion matrix, and maps probabilities/correctness.
8. **Amsterdam prototype evaluation** (cells 25, 26, 28, 30): samples Amsterdam support labels, computes class mean prototypes directly in Amsterdam feature space, predicts query rows by L2 distance, evaluates macro F1 and confusion/maps.

## 2. Required inputs from `preprocessed_data.pkl`

| Key | Used by | Expected object | Expected shape/content |
|---|---|---|---|
| `X_madrid` | Madrid CV; final RF training | numeric NumPy-like 2D array | `(76263, 60)`, finite, already standardised |
| `y_madrid` | Madrid CV; final RF training/evaluation | integer NumPy-like 1D array | `(76263,)`, classes exactly `{1,2,3,4}` |
| `X_amsterdam` | zero-shot; prototype support/query | numeric NumPy-like 2D array | `(25992, 60)`, finite, same feature order as Madrid |
| `y_amsterdam` | zero-shot evaluation; prototype sampling/evaluation | integer NumPy-like 1D array | `(25992,)`, classes exactly `{1,2,3,4}` |
| `feature_names` | feature-importance labels; schema checks | ordered list of strings | length `60`, unique, aligned to feature columns |
| `pixel_ids_madrid` | Madrid spatial maps | array-like integer coordinates | `(76263, 2)` containing `(px_key, py_key)`, aligned to rows |
| `pixel_ids_amsterdam` | Amsterdam spatial maps | array-like integer coordinates | `(25992, 2)` containing `(px_key, py_key)`, aligned to rows |
| `scaler` | not used in Notebook 4 after load, but required for artifact plan | fitted `StandardScaler` | fitted on Madrid by Notebook 3 |
| `feat_groups` | not used in Notebook 4, but required for schema metadata | dict of feature-name lists | groups: `overall`, `indices`, `early`, `late`, `yoy`, `indicators` |

## 3. Assumptions verified from notebooks/docs

- Notebook 4 is fully blocked until Member 2 creates the pickle.
- Notebook 4 does **not** read raw Parquets and does **not** depend on Notebook 2 outputs.
- Random Forest training occurs only in cells 7 and 14.
- Evaluation occurs in cells 7/8/11 for Madrid CV, cells 19/20/22 for zero-shot Amsterdam, and cells 25/26/28/30 for Amsterdam prototypes.
- Baseline Amsterdam prototypes do not consume `rf_final`; they use only Madrid-standardised Amsterdam feature vectors and Amsterdam support labels.
- The only persisted organiser artifact is the pickle from Notebook 3; Notebook 4 saves no model, metrics, splits, figures, prototypes, or predictions.
- Expected reference feature shapes are Madrid `(76263, 60)` and Amsterdam `(25992, 60)`.

## 4. Artifact saving plan

Suggested root: `models/member3_baseline_exports/` or Team-Lead-approved equivalent. Do not overwrite Member 2 artifacts.

| Artifact | Save after | Contents | Format |
|---|---|---|---|
| `preprocessed_validation.json` | pickle reload | shapes, class sets, finite checks, feature-name count, pickle checksum | JSON |
| `rf_final_source_bundle.pkl` | cell 14 final RF fit | fitted `rf_final`, ordered `feature_names`, RF params, seed, source city, class config, optional metrics | pickle |
| `madrid_cv_metrics.json` | cell 7/8 | fold F1 list, mean/std, raw and normalised confusion matrix, CV config | JSON |
| `amsterdam_zero_shot_metrics.json` | cells 19/20 | macro F1, classification report dict, confusion matrices | JSON |
| `amsterdam_prototype_metrics.json` | cell 25 | per-budget trial scores, mean/std, support/query seed/config | JSON |
| `episode_indices/*.npz` | prototype loop | exact support/query indices per budget/trial | compressed NumPy |
| `figures/*.png` | plot cells | CV curve, confusion matrices, learning curve, selected maps | PNG |
| `artifact_manifest.json` | end of run | paths, checksums, creation time, code/notebook path, seed/config summary | JSON |

Minimal helper functions now prepared in `working/member3_artifact_helpers.py` for: directory creation, pickle/json/CSV saving, figure saving, SHA256 checksums, pickle-contract validation, source-model bundling, and support/query-disjoint assertion.

## 5. Notebook dependency map

```text
original/1-Introduction.ipynb
  reference only

original/2-Reading_Data.ipynb
  raw parquet EDA only; no saved dependency

 data/madrid_train.parquet + data/amsterdam_data.parquet
        |
        v
 original/3-Preprocessing.ipynb or Member 2 baseline copy
        |
        v
 data/preprocessed/preprocessed_data.pkl
        |
        v
 original/4-Modelling.ipynb or downstream working copy
        |
        +--> Madrid CV metrics/figures
        +--> final Madrid RF source artifact
        +--> Amsterdam zero-shot metrics/figures
        +--> Amsterdam prototype metrics/episode records/figures
```

## 6. Validation checks before modelling starts

- [ ] Pickle path exists and reloads in a clean Python session.
- [ ] Required pickle keys are present.
- [ ] `X_madrid.shape == (76263, 60)` and `X_amsterdam.shape == (25992, 60)` unless Member 2 documents an accepted baseline deviation.
- [ ] Label lengths match feature row counts.
- [ ] Pixel-ID arrays are `(n_rows, 2)` and row-aligned.
- [ ] Classes are exactly `[1,2,3,4]` in both cities.
- [ ] Features are finite with no NaN/inf.
- [ ] `feature_names` length is 60, unique, and matches `feat_groups` membership.
- [ ] No `weighted_mean_year` or `age_class` appears in `feature_names`.
- [ ] RF params match baseline exactly for reproducibility: 500 trees, balanced class weight, seed 42.
- [ ] Amsterdam support/query indices are disjoint for every prototype episode.
- [ ] Query labels are used only inside metric calculation, never prototype fitting.
- [ ] Episode support indices and seeds are saved before interpreting metrics.
- [ ] Saved source bundle can be reloaded and used for Amsterdam prediction without refitting.

## 7. Minimal reproducibility improvements that do not change baseline behaviour

- Add project-relative configurable artifact paths; create directories with `parents=True`.
- Validate pickle schema before fitting.
- Persist exact RF params, CV config, budgets, seed, feature schema, and class labels.
- Save fold/trial scores and confusion matrices as machine-readable JSON.
- Save exact prototype support/query indices for every trial.
- Save figures with deterministic filenames rather than relying on notebook outputs.
- Save and reload-test `rf_final` after training.
- Record input pickle checksum and artifact checksums.
- Keep all changes in a separate working helper/export layer; do not alter baseline algorithms.

## 8. Recommended commits

1. `docs: add member3 modelling readiness map` — this document plus log update.
2. `model: add downstream artifact helper utilities` — `working/member3_artifact_helpers.py` only; no training output.
3. After Member 2 handoff only: `model: export baseline modelling artifacts` — save metrics/model/figures without changing RF/prototype logic.
4. If authorised later: `model: add source-state adaptation candidate` — separate candidate implementation, matched episodes, explicit source-state reuse.
