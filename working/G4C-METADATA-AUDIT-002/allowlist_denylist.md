# Exact integrity scope

## Allowlist — one path only

`working/Open Notebook.onetoc2`

Only content/size/mtime drift of the same regular single-link non-reparse OneNote TOC file is allowed and logged. Removal, changed identity/attributes, redirection or invalid TOC signature stops. No glob, suffix, basename, or working-directory exemption exists.

## Denylist — all other pre-existing files

This is a default-deny complement, not an incomplete list of special protected names. It includes:

| Category | Examples outside exception |
|---|---|
| Candidate source and coordinator | `working/g4c_episode_worker.py`, `working/g4c_source_worker.py`, `working/run_g4c_candidate.py` |
| Candidate config/state | Future `working/G4C-E2-002/parameters.json`, source/adaptation state once created and finalized |
| Data | `data/preprocessed/preprocessed_data.pkl`, accepted parquet files |
| Baseline/model | Everything under `working/baseline_artifacts/` and `working/member3_baseline_frozen/`, including their `.onetoc2` files |
| Episode identities | `working/gate4_episode_manifest.json` |
| Predictions/evidence | Closed `working/G4C-E2-001/`, Gate 4A/Gate 4B runs, future finalized predictions |
| Isolation infrastructure | `working/gate4_lifecycle.py`, `working/gate4_production_boundary.py`, `working/g4c_boundary.py` |
| Runtime | Approved Linux runtime files, dependency wheels, Bubblewrap, runtime lock files |
| Original | Every file and directory membership under `original/`, including its `.onetoc2` |
| Other metadata | `working/nested/Open Notebook.onetoc2`, `working/another.onetoc2`, every other pre-existing `.onetoc2` |

New audit/run artifacts require exclusive creation in a separately declared write set. That permission does not relax any pre-existing-file comparison. Unknown additions outside the declared new evidence destinations stop.

The independent verifier exercised 22 synthetic allowed/forbidden changes without changing any real project file. All tests passed. This policy is not installed in the historical runner; its future adoption requires a newly identified coordinator/attempt without overwriting prior code or evidence.
