# E3 validator identity/path map

## Root cause

`working/verify_g4c_candidate.py::main(method)` constructs `ROOT / 'working' / f'G4C-{method}-001'`. Its failure handler independently repeats that construction. Selecting E3 therefore selects the closed `G4C-E3-001` directory, regardless of the current authorization.

The optimized preparer emits a different coordinator layout and does not emit a validator. The legacy validator cannot be made compatible merely by substituting the experiment string.

## Inspected path and schema assumptions

| Legacy assumption | Current explicit binding |
|---|---|
| Repository `ROOT` derived from verifier placement | Repository derived from the one canonical `project/working/<run_id>` argument |
| `G4C-{method}-001` in main and failure handler | Target directory argument; identity checked against preparation, execution authorization, binding, summary and inventory |
| `entry.json` | `checkpoint/infrastructure_preparation.json`, `checkpoint/execution_authorization.json`, `checkpoint/validation_binding.json` |
| `parameters.json` | Exact frozen E3 parameters independently compared across authorization, saved state and execution summary |
| `source_state.json` | `candidate_state/source_state.json` |
| `per_episode_results.json` | `results/per_episode_results.json` |
| `summary.json` | `results/execution_summary.json` |
| `code/<name>` and global `working/<name>` | Current `coordinator/<name>` checked against preparation hashes and approved worker hashes |
| `ROOT / row['prediction_artifact']` | Strict current-run resolver; producer-style `working/<CURRENT_ID>/predictions/...` is accepted, other identities/absolute/traversal/symlink references rejected |
| `run / row['worker_evidence']` | Same resolver; requires exact expected `evidence/worker_NN.json` for its ordinal |
| `row['worker_sha256']` | Producer's `row['worker_output_sha256']`; same hash check retained |
| `evidence/preflight_1.json`, `preflight_2.json`, `post_candidate_probe.json` | Same paths relative to the explicit target; all three substantive checks retained |
| `evidence/source_worker.json` | Same path relative to the explicit target; source packet/state reconstruction retained |
| Legacy root-level verification result/STOP path | API returns a result for the explicit target; CLI prints it without writing any historical directory |
| No substantive execution-report check | Current `EXECUTION_REPORT.md` must exactly render the current execution summary and be inventoried |
| Global frozen episode manifest | Global frozen anchor checked plus byte-identical current-run `checkpoint/episode_manifest.json`; no sampler change |
| `working/baseline_artifacts/rf_final.pkl` | Same frozen reference, hash pinned; never treated as another run's candidate output |
| `data/preprocessed/preprocessed_data.pkl` | Same protected frozen input; exact pinned pickle dependency |
| `working/baseline_artifacts/amsterdam_zero_shot.npz` | Same frozen RF reference; target labels/IDs aligned independently |
| `working/baseline_artifacts/prototype_trial_scores.npz` | Same frozen raw comparator, all 60 trial scores checked |
| Old `G4C-PROVENANCE-CHECKPOINT/input_artifact_hashes.json` | Already-approved coordinator checkpoint 002, with its existing exact-path external-metadata exception; all other input hashes retained |
| `original/` Git check | Same clean-original check at the explicit repository |
| Legacy `delta_*` summary fields and `verdict` | Current `candidate_minus_raw`, `candidate_minus_rf`, `scientific_verdict`; underlying exact paired comparisons preserved |
| Shared legacy criteria field names | Exact current frozen E3 criteria field names; includes E3's RF gain/per-class safeguards as already implemented in the E3 coordinator |

Historical paths remain only frozen reference/provenance sources. They are never fallback sources for missing current predictions, evidence, state, authorization, report or summary.

## Binding sequence (implemented, not exercised on a real new experiment)

1. Use the unchanged optimized preparer after a separate execution authorization to create a new E3 run.
2. `bind_e3_validation.py bind RUN_DIR` attaches the independent validator, current-run manifest snapshot, and hash-bound validation contract **before execution starts**. It rejects finalized/closed/running targets and never launches code.
3. The unchanged coordinator produces all 60 predictions and the current result schema.
4. `bind_e3_validation.py seal-report RUN_DIR` renders existing primary results (no new metric calculation), hashes current payloads, and marks the bundle pending independent validation.
5. `e3_validator.py RUN_DIR` independently validates the target. It takes exactly one target, with no historical/default run argument. Failure is returned, not rewritten into another run.

No actual E3 identity was created, bound, executed, sealed or validated as a completed experiment during this task.
