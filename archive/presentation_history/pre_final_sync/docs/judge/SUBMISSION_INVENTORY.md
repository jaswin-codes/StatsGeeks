# Submission contents and upload checklist

## Recommended judge-facing materials

| Deliverable | Path | Status |
|---|---|---|
| Concise presentation | [10-slide PPTX](../../presentation/Coordinate-RF_Judges.pptx) / [PDF](../../presentation/Coordinate-RF_Judges.pdf) | New presentation-only companion; same locked science |
| Written explanation | [Concise justification](WRITTEN_JUSTIFICATION.md) | Under conservative 300-word limit, excluding navigation footer |
| Notebook | [solution_notebook.ipynb](../../FINAL_SUBMISSION/solution_notebook.ipynb) | Frozen saved outputs; do not execute for release audit |
| Model and configuration | [model/](../../FINAL_SUBMISSION/model/) | Unchanged scientific bytes, full ordered pool required |
| Results | [results_summary/](../../FINAL_SUBMISSION/results_summary/) | Unchanged tables and locked report |
| Environment and interface | [requirements](../../FINAL_SUBMISSION/requirements.txt) / [dispatcher](../../FINAL_SUBMISSION/reproduce.py) | Runtime use fits support RFs; not run here |
| Integrity | [manifest](../../FINAL_SUBMISSION/manifest.json) / [checksums](../../FINAL_SUBMISSION/checksums.sha256) | Existing scientific package seal unchanged |

## Important packaging distinction

`FINAL_SUBMISSION/` is the existing sealed bundle, **not a newly rebuilt release export**. It retains its original 16-slide presentation and original explanation. The polished ten-slide presentation and concise explanation live outside that seal to respect preservation requirements. They report the same Coordinate-RF result: **0.749299 macro-F1**.

The companion's own [hash manifest](../../reproducibility/release/companion_manifest.json) covers its PPTX, PDF, chart, builder, export script, concise explanation and unchanged source CSV. It does not replace the original scientific-package seal.

Use the new deck for the live judge presentation. If uploads accept separate presentation and explanation files, upload the companions alongside the unchanged scientific bundle. If organizers require one self-contained archive with exactly one deck, prepare a separate presentation-only derivative and new distribution manifest after confirming the required layout; do not silently replace sealed bytes. No new scientific experiment is needed.

## Final human tasks

- Confirm eligibility of unlabelled full-pool access, coordinates and the extra 800-label development bank.
- Confirm official upload mechanism, filenames, package categories and presentation duration.
- Use the conservative 300-word explanation; the supplied rubric says 500, while notebook-derived guidance says 300.
- Open the new PDF/PPTX on the presentation machine and rehearse four-person handoffs.
- Verify the actual uploaded model binary is present; a Git clone may omit ignored large files.
- Confirm any separate reusable source-model export requirement: the bundle includes a cached source probability prior.
- Confirm repository/data redistribution rights before public release.

The scientific package, notebook, source results, original slides and explanation are all retained. See the [single release report](../release/RELEASE_REPORT.md) for test results and the Git allowlist.
