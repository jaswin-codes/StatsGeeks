# StatsGeeks — Coordinate-RF

**Four-class building-construction-era classification · Madrid → Amsterdam**

## Competition and problem
Classify 30 m × 30 m Landsat pixels into four construction-era classes.
Learn from labelled Madrid data and adapt using 5, 25, 50, 100 or 200 labelled
Amsterdam pixels per class. Macro F1 weights the four classes equally.

**Status: frozen scientific solution; submission eligibility remains conditional.**
No new training, tuning, predictions or model replacement occurred during packaging.

## Approach and transfer
```text
Madrid spectral features → contextual source learning → frozen probability prior
                                                               ↓
Amsterdam full unlabelled pool → whitening + coordinates → support RF
                                                               ↓
                                     blend + spatial smoothing → predictions
```
Coordinate-RF combines source-learned probabilities with a 200-tree target-support
random forest on 60 whitened features plus two standardized coordinates. The source
prior weight is `20/(20+4b)`, where `b` is labels/class. Nine-neighbour Gaussian
smoothing uses coordinates, not query labels. This is transductive and pool-bound,
not an inductive unseen-city model. The machine identifier `Coordinate_RF` means
**Coordinate-RF**; it is not a different model.

## Locked results
| Labels/class | Macro F1 | Population SD | Episodes |
|---:|---:|---:|---:|
| 5 | 0.650253 | 0.011246 | 200 |
| 25 | 0.687664 | 0.012145 | 200 |
| 50 | 0.708436 | 0.011277 | 200 |
| 100 | 0.729839 | 0.008802 | 200 |
| 200 | 0.749299 | 0.005716 | 200 |

Each row uses 200 paired, fixed-city random-pixel episodes. Population SD is not
a confidence interval. The 800-label development bank is excluded from final
queries but constitutes additional research supervision. At 200/class, paired
ASTRA scores 0.733037; Coordinate-RF's spatial mean is 0.694216 versus ASTRA's
0.696672. These are existing audit results, not organizer-held-out scores.

## Repository structure and deliverables
| Path | Purpose |
|---|---|
| `presentation.pptx`, `presentation.pdf` | Original final slides, unchanged |
| `written_explanation/` | Original explanation, unchanged |
| `solution_notebook.ipynb` | Original notebook with dependency paths relocated only |
| `model/` | Frozen state, inference implementation and notebook evidence dependencies |
| `results_summary/` | Locked CSV tables, report and concise summary |
| `requirements.txt`, `reproduce.py` | Environment specification and inference dispatcher |
| `manifest.json`, `checksums.sha256` | Package membership, provenance and byte integrity |

## Quick start: safe inspection
Open the PDF, then [results summary](results_summary/README.md). Read the notebook
without running its cells. Check all package bytes from this directory:
```bash
sha256sum -c checksums.sha256
```
Checksums establish consistency, not authenticity; obtain them from a trusted source.
The checksum file excludes itself and covers the manifest; the manifest excludes
itself and the checksum file to avoid circular hashes.

## How to run inference / reproduce (not run during this audit)
Observed environment: Python 3.14.6 on Windows. A Git clone is not guaranteed to
include ignored large artifacts; use this complete folder. Only load trusted pickles.
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# POSIX: source .venv/bin/activate
python -m pip install -r requirements.txt
python -I -B reproduce.py --support support.npz --out NEW_OUTPUT_DIRECTORY
# Optional fixed-reference replay (also fits support RFs):
python -I -B reproduce.py --verify --out NEW_REPLAY_DIRECTORY
```
**Both commands fit support-set RFs. They are not permitted in a no-retraining audit.**
Support NPZ fields: `indices` (unique integer pool rows), `labels` (1–4), and
`budget` (integer scalar, supported values above). Supply exactly `budget` labels
per class. Optional `query` indices must be unique, valid and disjoint from support.
The pool contains 25,992 rows in its original order; arbitrary new pools are not
supported. Never pass query truth to adaptation. Output paths must be new.

For notebook use, start a compatible Jupyter kernel in this folder. Saved outputs
are inherited, not newly executed here. Raw-data training is not self-contained:
organizer data, Madrid-fitted preprocessing and ordered coordinates are external.
See [methods](model/reports/METHODS.md). Historical receipts and the historical
SHA256SUMS under `model/evidence/` describe the original source package, not the
relocated package; use the root manifest and checksums for this folder.

## Limitations and submission gates
Organizer approval of full-pool target features, coordinates and additional
research supervision is unconfirmed. The original explanation exceeds the
conservative 300-word interpretation; confirm the official limit before upload.
There is one target city, historical audit exposure and no independent organizer
held-out validation. Clean installation, new inference execution and fresh visual
rendering are not certified by this packaging pass. Source-trained reusable model
export requirements versus a cached source probability prior also need confirmation.

## Acknowledgements and license
StatsGeeks acknowledges the organizers for data and notebooks and the open-source
scientific Python community. No competitor material is added. No repository license
or raw-data redistribution grant has been established; no new license is asserted.
Obtain rights-holder approval before public redistribution.
