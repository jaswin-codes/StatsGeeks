# Authorized preserved dirty checkpoint

Execution authorized from preserved dirty starting state.
No cleanup, reset, restore, stash, commit, or provenance-altering
modification was performed.

The Team Lead explicitly accepts historical Git dirtiness; no reconciliation is required or attempted. HEAD/status/staged and unstaged binary diffs/index provenance are captured alongside hashes of all relevant pre-existing source/data/evidence files. New G4C evidence is the only provenance-related addition.

Frozen preflight: 33/33 protected hashes match; all inventoried working files in Gate 4A teardown and Gate 4B/E1 inventories match; original/ Git status empty; frozen manifest matches the authorized SHA256; no E2–E5 run directories exist. Historical Gate 4A and Gate 4B execution PASS and E1 FALSIFIED remain intact. Accepted raw 25-shot score remains .5986 ± .0176. Approved runtime tree matches all 4,355 files. See machine-readable checks and runtime verification.

New candidate code will be separately pinned, using the certified runtime and lifecycle without changing existing files. The 60 frozen episodes are the 6 budgets × 10 trials, not 3,600 independently sampled episodes. No Notebook 4 rerun, new draw identities, parameter tuning, or candidate access to evaluator labels/manifest is authorized.

The prior read-only `working/G4C-FINAL-REPORT.md` and `working/STOP_REASON.md` already exist. They will not be overwritten. Any continuation final/stop report will be created at a new evidence path and explicitly referenced to preserve the no-overwrite requirement.
