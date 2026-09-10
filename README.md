# Project

**Building-age transfer learning · Madrid → Amsterdam.** We classify 30 m Landsat pixels into four construction-era classes using Madrid source knowledge and a small labelled Amsterdam support set.

# Final Result

**Coordinate-RF — macro-F1: 0.749299 ± 0.005716.**

Locked at **200 labels/class**, across 200 paired, fixed-city random-pixel episodes. The ± value is population SD, not a confidence interval. This is a transductive, full-pool result—not an organizer-held-out or unseen-city score.

# Quick Start

Judges: follow this order; no execution is needed.

1. **[FINAL_SUBMISSION/](FINAL_SUBMISSION/README.md)** — the complete current submission.
2. **Presentation:** [PDF](FINAL_SUBMISSION/presentation.pdf) · [PowerPoint](FINAL_SUBMISSION/presentation.pptx).
3. **[Written justification](FINAL_SUBMISSION/written_explanation/written_justification.txt)** — approved revised explanation.
4. **[Notebook](FINAL_SUBMISSION/solution_notebook.ipynb)** — inspect saved outputs without running cells.
5. **[Model](FINAL_SUBMISSION/model/)** — frozen state, configuration and inference interface.
6. **[Results](FINAL_SUBMISSION/results_summary/README.md)** — locked tables and report.
7. **[Repository documentation](docs/README.md)** — methods, limitations, reproducibility and presentation guide.

# Repository Structure

| Folder | Purpose |
|---|---|
| `FINAL_SUBMISSION/` | Authoritative current presentation, PDF, justification, logo and unchanged scientific payload |
| `docs/` | Judge navigation, methodology, reproducibility and one active presentation guide |
| `presentation/` | Navigation to the final deck; older decks/tooling are historical, not upload targets |
| `FINAL_SUBMISSION/results_summary/` | Submitted results; there is no root `results/` folder |
| `FINAL_SUBMISSION/model/` | Submitted model; there is no root `model/` folder |
| `candidate/` | Canonical scientific reports, models, predictions and experiment history |
| `reproducibility/` | Integrity records and historical release receipts |
| `figures/` | Existing figures; canonical scientific figures also remain under `candidate/` |
| `scripts/` | Existing maintenance and validation utilities; older release checks target older layouts |
| `data/`, `original/`, `working/` | Supplied data, original notebooks and preserved research work |
| `archive/` | Superseded presentation materials and historical documentation; not current submission |

# Final Deliverables

| Deliverable | Exact location |
|---|---|
| Presentation | [FINAL_SUBMISSION/presentation.pptx](FINAL_SUBMISSION/presentation.pptx) |
| PDF | [FINAL_SUBMISSION/presentation.pdf](FINAL_SUBMISSION/presentation.pdf) |
| Written justification | [FINAL_SUBMISSION/written_explanation/written_justification.txt](FINAL_SUBMISSION/written_explanation/written_justification.txt) |
| Notebook | [FINAL_SUBMISSION/solution_notebook.ipynb](FINAL_SUBMISSION/solution_notebook.ipynb) |
| Model | [FINAL_SUBMISSION/model/pool_state.pkl](FINAL_SUBMISSION/model/pool_state.pkl) + [configuration](FINAL_SUBMISSION/model/configuration.json) |
| Submission README | [FINAL_SUBMISSION/README.md](FINAL_SUBMISSION/README.md) |
| Requirements | [FINAL_SUBMISSION/requirements.txt](FINAL_SUBMISSION/requirements.txt) |

# Reproducibility

Scientific artifacts are **frozen**: models, predictions, notebooks, evidence, reports, CSVs, methodology and scientific hash files are unchanged by final synchronization. Saved outputs, locked configurations and existing replay evidence document the submitted work.

Safe byte check: from `FINAL_SUBMISSION/`, run `sha256sum -c checksums.sha256`. Only documentation/presentation entries in the distribution manifest were updated. No training, inference or notebook execution was performed. Runtime reproduction is documented in the [submission README](FINAL_SUBMISSION/README.md); it fits support forests and is **not** a release-audit step. Large ignored binaries may be missing from a Git clone—verify the actual upload.

The artifact requires the original ordered Amsterdam pool. The additional 800-label development bank, historical audit exposure, weaker spatial results and unresolved organizer eligibility are disclosed in the [justification](FINAL_SUBMISSION/written_explanation/written_justification.txt). See the [inventory and remaining checks](docs/judge/SUBMISSION_INVENTORY.md).

# Team

**Pixel Prophets**

<img src="FINAL_SUBMISSION/assets/pixel_prophets_logo.png" alt="Pixel Prophets team logo" width="180">

[Presentation guide](docs/presentation/PRESENTATION_GUIDE.md) · [License and redistribution status](docs/reproducibility/LICENSE_STATUS.md)
