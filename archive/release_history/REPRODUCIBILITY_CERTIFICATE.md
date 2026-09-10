# Reproducibility Certificate

## Certification level

**STATIC AND HISTORICAL-RECEIPT VERIFIED; RUNTIME REPLAY NOT EXECUTED IN THIS PASS.** This certificate does not claim fresh validation or independent organizer testing. Running either inference mode fits a support-set Random Forest and was prohibited.

## Verified controls

| Control | Evidence | Status |
|---|---|---|
| Selected implementation | `model/SELECTION_LOCK.json`: `Coordinate_RF`, `coord: true` | Pass |
| Query labels excluded from fitting API | `agf_model.fit_pool` accepts source labels only; `probabilities` accepts support indices/labels only | Pass, static |
| Support/query separation | Inference wrapper validates unique indices and rejects query/support overlap | Pass, static |
| No query-label selection | Selection lock says support-only selection; final audit marked not selection | Pass, documented |
| Transfer pipeline | Source contextual prior + target covariance + support RF + blend + smoothing | Pass, static |
| Coordinate usage | Two standardized coordinate columns; coordinate-neighbour smoothing | Pass, static |
| Feature order | 60 names sealed in `INFERENCE_MANIFEST.json` and checked after load | Pass |
| Dependency list | Exact inference pins and notebook additions provided | Pass |
| Notebook structure | nbformat 4.5, 9 cells, 4 code cells, all code compiles | Pass |
| Inference entry point | Root dispatcher resolves package-relative frozen wrapper | Pass, static |
| Manifest/checksums | 30/30 scoped files; 31/31 checksum entries pass | Pass |
| Protected hashes | Three provenance-protected files and three inference files match | Pass |
| Saved metric arithmetic | 4,000 confusion matrices/F1 records and all means/SDs recomputed | Pass |
| Prediction stability | Existing exact-replay receipts/hashes unchanged | Pass, historical receipt |

## Leakage assessment

No construction-year/query-label field appears in the final prediction API. Full target features, covariance, coordinates and topology are used transductively; this is explicitly disclosed and is not label leakage under the stated protocol. Support labels alone fit the target RF. Saved source-refit evidence notes that a historical cache containing target truth was deserialized and the truth field immediately discarded without value access; the fitting API cannot receive it.

## Reproduction contract

The package reproduces inference only for the bound 25,992-row Amsterdam pool in original order. A support NPZ must contain unique integer `indices`, labels 1–4 with exactly `budget` rows per class, and a supported integer budget. Optional query indices must be valid, unique and disjoint. Output directories must be new. Trusted hashes must be verified before pickle loading.

## Limitations

- No clean installation or runtime command was performed in this no-retraining pass.
- The notebook starts from a trusted preprocessed pool artifact; raw-data training is not self-contained.
- A compatible Jupyter frontend/kernel is not pinned.
- Portability beyond the observed Python 3.14.6 Windows environment is not certified.
- Organizer approval of transductive pool access, coordinates and extra development supervision is unresolved.

Subject to those limits, the package is internally reproducible and integrity-sealed.
