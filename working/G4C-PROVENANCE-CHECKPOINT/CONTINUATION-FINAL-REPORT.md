# Gate 4C continuation final report — STOPPED

## Authorization and preserved starting state

Execution authorized from preserved dirty starting state.
No cleanup, reset, restore, stash, commit, or provenance-altering
modification was performed.

Historical project changes were intentionally preserved under explicit Team Lead authorization. The checkpoint includes HEAD, status, diff stat, complete staged/unstaged binary diffs, Git index records, input hashes, runtime verification and authorization. Git dirtiness was accepted, not used as a blocker again.

## Frozen preflight

- Gate 4A PASS and teardown/isolation inventory: matching hashes.
- Gate 4B/E1 inventory/report: matching hashes; E1 remains FALSIFIED, .5901 ± .0321 at 25 shots.
- Manifest: `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.
- RF: `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870`.
- Protected files: 33/33 matched at checkpoint and independent stop audit.
- original/: clean, unchanged protected hashes.
- Approved runtime: 4,355-file tree match; no runtime substitution.
- No E2–E5 run directory existed before this attempt.

## Execution and stop

New candidate/coordinator/verifier files were created separately without editing existing infrastructure. Syntax checks passed. `G4C-E2-001` was exclusively created, but its first integrity assertion detected that pre-existing checkpointed `working/Open Notebook.onetoc2` had changed. It stopped before any data loading, candidate source fitting, packet construction or worker launch. No E2 episode or E3/E4/E5 run occurred.

The metadata file changed from 7,912 to 8,192 bytes. Checkpoint hash: `a5d62a10607923bc9f3bcd8df505ba2fac3fbf917d296a619532c55cfe9c8f75`; stop-audit hash: `e0a91560faa8fb0413d34cf1e7d982a000bf61297f8c61bb8fb4fc69b6ff66d1`. This is not a baseline/protected-33 failure. The checker covered all pre-existing working files, including OneNote metadata. No assistant write targeted it; the external modification mechanism is unproven. No repair, exception, overwrite, or retry followed the integrity failure.

## Results and method decision

| Candidate | Execution | 25-shot | Qualification |
|---|---|---|---|
| E2 | Stopped before modelling; 0/60 | N/A | Not evaluated |
| E3 | Not run | N/A | Not evaluated |
| E4, both arms | Not run | N/A | Not evaluated |
| E5 | Not run | N/A | Not evaluated |

Baseline 25-shot: **.5986 ± .0176** (ddof=0). Best candidate and improvement: unavailable. No conclusion that a candidate qualifies or that all candidates fail is supported. No ranking, per-class comparison, tuning, or threshold change occurred. Further tuning is not justified; the fixed suite remains unevaluated.

## Verification, isolation, resources

Independent read-only stop audit confirmed frozen file anchors and the metadata discrepancy. No independent candidate prediction verification occurred. No worker received labels or manifest, no adaptation state was created, and no worker teardown was necessary. Candidate timing/peak RSS: unavailable. Notebook 4 was not rerun.

## Deviations and next action

The no-overwrite requirement conflicts with reusing the already-existing read-only `working/G4C-FINAL-REPORT.md` and `working/STOP_REASON.md`. Those historical artifacts remain untouched; this new continuation report and `working/G4C-E2-001/STOP_REASON.md` provide the current disposition.

Stop evidence for `G4C-E2-001` is retained; that run ID must not be overwritten. A Team Lead decision is required on stabilizing or explicitly scoping mutable directory metadata and authorizing a new attempt/run identity. No accepted project file was modified to clean provenance or bypass the failure.

## Exact artifacts

- Checkpoint: `working/G4C-PROVENANCE-CHECKPOINT/`
- Current report: `working/G4C-PROVENANCE-CHECKPOINT/CONTINUATION-FINAL-REPORT.md`
- Current stop: `working/G4C-E2-001/STOP_REASON.md`
- Detailed result: `working/G4C-E2-001/REPORT.md`, `summary.json`
- Independent stop audit: `working/G4C-E2-001/independent_stop_audit.json`
- Execution traceback: `working/G4C-E2-execution.log`
- Extraction-ready directory: **NOT CREATED**; completion/verification requirements unmet.
