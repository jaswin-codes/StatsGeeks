# Repository audit — preservation-first

## Scope and evidence
Before changes: **5,214 files, 6.318 GB**,
excluding Git internals, `.venv_baseline`, named virtual environments and bytecode
caches. Inventory includes the newly introduced inventory script itself. No file
is deemed unused merely because it is old, duplicated or large. Every action
recommendation below is explicitly KEEP, MOVE, ARCHIVE or IGNORE.

Baseline: [baseline.json](../../reproducibility/repository_polish/baseline.json).
Exact duplicates, notebooks, temporary candidates, scripts and largest files:
[inventory_summary.json](../../reproducibility/repository_polish/inventory_summary.json).
The initial working tree was already dirty; it was neither reverted nor staged.

## Current structure at entry
| Directory | Files | Decimal MB |
|---|---:|---:|
| `(root files)` | 9 | 0.30 |
| `archive` | 10 | 129.60 |
| `candidate` | 3656 | 3977.00 |
| `data` | 6 | 236.53 |
| `docs` | 38 | 0.46 |
| `models` | 1 | 0.01 |
| `original` | 5 | 13.95 |
| `presentation` | 5 | 0.79 |
| `scripts` | 6 | 0.03 |
| `submission` | 1 | 0.01 |
| `submission_dry_run` | 9 | 0.70 |
| `working` | 1468 | 1958.73 |

## Findings and disposition
| Area | Finding | Recommendation |
|---|---|---|
| Current science | `candidate/final_submission/` and `candidate/best_model/` contain frozen Coordinate-RF artifacts | KEEP — authoritative sources at current paths |
| Historical runs | `working/`, `candidate/autonomous_runs/`, `candidate/autonomous_ml_overnight/`, `experiments_2h*`, `experiments_agf/` | KEEP — research provenance, excluded from judge package |
| Apparently unused folders | Root `models/` and `submission/` each contain only a OneNote index; no model/submission payload | IGNORE — dormant historical scaffolding; do not populate with duplicate models |
| Organizer assets | `original/`, `data/` and source challenge documents | KEEP — never edit or redistribute without approval |
| Draft presentations | Root `presentation/StatsGeeks_BuildingAge.*` differs in role from `candidate/final_submission/presentation/*FINAL*` | KEEP — historical; route judges only to final copies |
| Old exports | Prior ZIPs in `archive/`, `candidate/publication/`, overnight runs and safety snapshots | KEEP — backups are evidence, not disposable clutter |
| Temporary candidates | 378 `.onetoc2`, `.pre_completion`, `.pre_dependency_repair`, `.tmp`/`.bak` candidates | IGNORE active OneNote metadata; KEEP pre-repair files as audit evidence |
| Auto-generated sidecars | OneNote index files appeared in new folders; root/archive indices changed during this pass | ARCHIVE only new distribution sidecars when encountered; do not rewrite original indices or claim global byte invariance |
| Old figures | Legacy plots and transparent slide assets coexist with canonical publication figures | KEEP — archive provenance; exclude from minimal package except embedded final assets |
| Duplicate notebooks | Four byte-identical groups found (below) | KEEP — originals, executed references and safety copies have different provenance roles |
| Duplicate reports | 9 identical Markdown groups within 321 duplicate groups across all types | KEEP — versioned evidence; use a single judge entry point, not deletion |
| Orphan scripts | 351 Python files inventoried; dynamic notebook/CLI usage prevents reliable automatic orphan proof | KEEP — no proven-dead script removed; `scripts/README.md` documents baseline tools |
| Unsafe audit commands | Legacy `scripts/README.md` says tools do not train, but documents Madrid RF refits; candidate replay also fits support RFs | KEEP original text; use the new no-model-execution validator only |
| Names | `Coordinate_RF` machine ID, Coordinate-RF prose, ASTRA_AGF, EXP010/EXP-010 and EXPF/EXP-F coexist | KEEP frozen IDs; use Coordinate-RF consistently in new prose and document aliases |
| Root README | Frozen in `SHA256SUMS.json`; valid headline but not a complete final judge guide | KEEP bytes; MOVE judge reading flow to `docs/README_SUBMISSION.md` and new package README |
| Historical master plan | Still describes planning-era status | KEEP original; add `docs/MASTER_PLAN_POLISH_ADDENDUM.md` rather than rewriting history |
| Requirements | Legacy baseline Python 3.13.15 / NumPy 2.5.1 differs from final Python 3.14.6 / NumPy 2.5.3 | KEEP both historical environments; use only new package requirements for its contract |
| Environment health | All six new package pins match installed metadata, but nbformat import fails on a non-UTF-8 schema-resource entry | KEEP failure evidence; clean environment repair requires a separate authorized task |
| License | No root LICENSE or confirmed organizer redistribution grant | KEEP notices; defer a license grant pending rights-holder approval |
| Structural organization | Artificial root `src/`, `notebook/`, `tables/` duplication would increase confusion and threaten imports | KEEP existing module paths; use additive `docs/`, `deliverables/`, `figures/`, `reproducibility/`, `FINAL_SUBMISSION/` |

## Duplicate notebooks (exact SHA-256 identity)
- KEEP — byte-identical group: `candidate/SUBMISSION_SAFETY_SNAPSHOT/deliverables_20260909T190850Z/working/3-Preprocessing_member2_baseline_executed.ipynb`; `working/3-Preprocessing_member2_baseline_executed.ipynb`
- KEEP — byte-identical group: `candidate/SUBMISSION_SAFETY_SNAPSHOT/deliverables_20260909T190850Z/working/4-Modelling_member3_reference_executed.ipynb`; `working/4-Modelling_member3_reference_executed.ipynb`
- KEEP — byte-identical group: `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/notebook/FINAL_NOTEBOOK.ipynb`; `candidate/final_submission/notebook/FINAL_NOTEBOOK.ipynb`
- KEEP — byte-identical group: `original/4-Modelling.ipynb`; `working/4-Modelling_member3_reference.ipynb`

## Representative duplicate reports
- KEEP — `candidate/SUBMISSION_SAFETY_SNAPSHOT/deliverables_20260909T190850Z/justification/written_justification.txt`; `docs/WRITTEN_JUSTIFICATION.md`; `submission_dry_run/justification/written_justification.txt`
- KEEP — `candidate/autonomous_ml_overnight/20260909T200015Z/OPERATIONAL_NOTES.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260910T041854/reports/OVERNIGHT_OPERATIONS.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/reports/OVERNIGHT_OPERATIONS.md`; `candidate/final_submission/reports/OVERNIGHT_OPERATIONS.md`
- KEEP — `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T221222/README.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T221903/README.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T222158/README.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T222533/README.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260910T041854/README.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/README.md`; `candidate/final_submission/README.md`
- KEEP — `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T221222/reports/METHODS.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T221903/reports/METHODS.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T222158/reports/METHODS.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T222533/reports/METHODS.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260910T041854/reports/METHODS.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/reports/METHODS.md`; `candidate/final_submission/reports/METHODS.md`
- KEEP — `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260909T222533/reports/FINAL_REPORT.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/previous_final_20260910T041854/reports/FINAL_REPORT.md`; `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/reports/FINAL_REPORT.md`; `candidate/final_submission/reports/FINAL_REPORT.md`
- KEEP — `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/reports/EXPLORATORY_FINALIST_AUDIT.md`; `candidate/final_submission/reports/EXPLORATORY_FINALIST_AUDIT.md`
- KEEP — `candidate/autonomous_ml_overnight/20260909T200015Z/submission_build/reports/REPRODUCIBILITY.md`; `candidate/final_submission/reports/REPRODUCIBILITY.md`
- KEEP — `candidate/autonomous_runs/20260909_1727/FINAL_REPORT.md`; `candidate/experiments_agf/FINAL_REPORT.md`

## Large artifacts — usage not presumed absent
| Artifact | Decimal MB | Action |
|---|---:|---|
| `working/baseline_artifacts/rf_final.pkl` | 1336.38 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/experiments_2h_v2/conditional_source_models.pkl` | 736.69 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/experiments_2h_v2/physical_source_models.pkl` | 592.14 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/experiments_2h_v2/source_context_models.pkl` | 565.95 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `data/madrid_train.parquet` | 141.96 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/publication/submission_bundle.zip` | 129.47 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `archive/publication_cleanup/exports/submission_bundle_pre_final_audit.zip` | 129.47 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `working/G4A-PRODUCTION-001/current_packet.json` | 120.22 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `working/G4A-PRODUCTION-001/second_packet.json` | 120.22 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/autonomous_ml_overnight/20260909T200015Z/SEARCH_RESULTS.json` | 110.49 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/experiments_2h_v2/astra_pool_state.pkl` | 66.96 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |
| `candidate/final_submission.zip` | 51.60 | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |

## Broken links and reference scope
KEEP — the explicit-inline-link scan reports one historical missing target:
`README.ijg` from the vendored pypdfium2 libjpeg-turbo license documentation.
It is outside the final package; do not edit third-party notices. New guide links
are checked after report creation. External URLs, Markdown anchors, dynamic code
paths and arbitrary prose references are not exhaustively certified.

KEEP — historical manifests and reports retain original relative paths, explained
in the new package README. No global claim of “no stale numbers anywhere” is
possible while preserving old experiment evidence. Current five-budget values
match across the selected table, slides, PDF, report, notebook and new guides.

## Archival outcome
ARCHIVE — documentation snapshots under `archive/repository_polish/snapshots/`.
ARCHIVE — this pass's first package and diagram drafts; no pre-existing scientific
file moved. The first build stopped safely on an exclusive-create filename
collision. The first package was then preserved before correcting UTF-8 notebook
reading and schematic labels. Failed validation attempts remain visible.
