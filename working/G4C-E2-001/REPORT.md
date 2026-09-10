# G4C-E2-001 — stopped before modelling

The preserved dirty starting state was explicitly accepted and checkpointed. Dirtiness was **not** rejected again. No cleanup/reset/restore/stash/commit occurred.

The coordinator created the exclusive run directory, then its first integrity assertion detected a change to checkpointed pre-existing `working/Open Notebook.onetoc2`. It stopped before entry/config serialization, data loading, source fitting, packet construction, or worker launch. No experiment was attempted or retried. E3–E5 were not started.

## Exact discrepancy

| Field | Checkpoint | At independent stop audit |
|---|---|---|
| Bytes | 7,912 | 8,192 |
| SHA256 | `a5d62a10607923bc9f3bcd8df505ba2fac3fbf917d296a619532c55cfe9c8f75` | `e0a91560faa8fb0413d34cf1e7d982a000bf61297f8c61bb8fb4fc69b6ff66d1` |

This file is OneNote directory metadata, **not one of the 33 protected baseline files**. No assistant edit targeted it. Its modification mechanism was not independently established; an automatic metadata update is plausible but not proven. The fail-closed checkpoint checker covered all pre-existing top-level working files, including this metadata. No whitelist exemption, reset, or hash rebaselining was introduced after failure.

## Frozen integrity and outcomes

A separate read-only stop-audit process confirmed 33/33 protected hashes still match, `original/` remains Git-clean, and the frozen manifest hash matches. Before this attempt, Gate 4A/Gate 4B inventories matched and the approved runtime image matched all 4,355 files. No candidate runtime ran.

E2: 0/60 episodes, no 25-shot result, scientific verdict NOT_EVALUATED. E3/E4/E5: NOT_RUN. No candidate qualifies or is scientifically falsified on this evidence. Baseline remains .5986 ± .0176. Best candidate and improvement are unavailable.

No labels or manifest were exposed to candidate workers because no workers launched. No worker teardown was required. Candidate-independent verification was not run; `independent_stop_audit.json` is a frozen-file audit, not a prediction certificate.

Evidence: `STOP_REASON.md`, `independent_stop_audit.json`, `evidence/changed_file_1.bin`, `evidence/git_status_at_stop.txt`, `summary.json`, and `working/G4C-E2-execution.log`. New unexecuted candidate implementation files are preserved; they have only been syntax-checked and must not be represented as validated implementations.

The authorized run ID is consumed by stopped evidence and must not be overwritten or silently retried. Under the no-repair instruction, further execution requires a decision concerning the observed metadata mutation and a new run identity. No extraction-ready package was created.
