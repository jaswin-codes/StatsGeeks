# Gate 4C final report — BLOCKED BEFORE EXECUTION

## A. Authorization
User authorized sequential fixed E2–E5 with independent verification, strict isolation, and stop-on-integrity/infrastructure failure. A clean Git preflight was required.

## B. Starting state
HEAD `165fe11df8779eed514c75bd2852c2b9588a18a4`. Git is not clean: 14 tracked modifications plus untracked artifacts. Historical E1 dirty-diff provenance is not reproduced by either current plain or binary Git diff. See `STOP_REASON.md`; this is not proof of protected-file corruption.

## C. Gate 4A status
Historical PASS report reviewed: `G4A-TEARDOWN-002/REPORT.md`. Manifest hash matches the authorized value. No new isolation recertification was run.

## D. Gate 4B status
Historical execution PASS report and final audit reviewed: `G4B-E1-001/REPORT.md`, `final_audit.json`. No E1 rerun.

## E. E1 result
Historical fixed-specification FALSIFIED; 25-shot .5901 ± .0321 against raw .5986 ± .0176. Not retuned.

## F. E2 result
NOT_RUN; 0/60 episodes. 25-shot result unavailable.

## G. E3 result
NOT_RUN; 0/60 episodes. 25-shot result unavailable.

## H. E4 result
Both arms NOT_RUN; 25-shot result unavailable.

## I. E5 result
NOT_RUN; 0/60 episodes. 25-shot result unavailable.

## J. Cross-candidate comparison
Unavailable. No ranking or winner can be inferred.

## K. Primary 25-shot comparison
Accepted raw baseline .5986 ± .0176 (population SD). No E2–E5 paired deltas exist.

## L. Per-class comparison
No E2–E5 per-class results exist. Historical E1 results remain in its immutable report.

## M. Success/falsification criteria
Not evaluated. NOT_RUN is neither FALSIFIED nor scientifically INCONCLUSIVE. Do not conclude that all candidates failed.

## N. Reproducibility verification
All 33 protected hashes match the E1 entry. Current Git cleanliness requirement fails; dirty-diff provenance discrepancy remains unresolved. Candidate prediction reproduction was not attempted.

## O. Isolation verification
No candidate processes launched and no label packets constructed. No candidate exposure or worker leak occurred in this task. Historical isolation certificates are not presented as fresh candidate verification.

## P. Artifact hashes
Manifest: `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.

RF: `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870`.

Schema: `bea946aaf7d96e12370af5800f4e719bafe0f7b30fee4354278f7ef36e1f107a`.

Full protected expected/actual hashes: `G4C-PREFLIGHT-001/preflight.json`.

## Q. Resource/runtime results
Read-only approved WSL image comparison matched all 4,355 files. Python 3.14.4. No candidate runtime, peak RSS, numerical import probe, or execution timing exists. No alternate candidate environment used.

## R. Final scientific conclusion
Whether a qualifying E2–E5 candidate exists is **unknown**. Neither a qualifying-candidate claim nor a no-candidate-qualifies claim is supported. Team Lead method selection is not yet applicable. Further tuning is not justified; the already authorized fixed experiments remain scientifically unevaluated and may proceed only after the starting-state blocker is resolved.

## S. Recommended next action
Team Lead should preserve/reconcile current changes and supply a clean checkpoint, or explicitly approve this exact dirty checkpoint and resolve provenance. No automatic cleanup, commit, baseline modification, or protocol relaxation was performed.

## T. Exact extraction-ready artifacts
`working/G4C_EXTRACTION_READY/` was **not created**: its completion/verification prerequisites are unmet.

Stop evidence only:
- `working/STOP_REASON.md`
- `working/G4C-FINAL-REPORT.md`
- `working/G4C-PREFLIGHT-001/preflight.json`
- `working/G4C-PREFLIGHT-001/git_status.txt`
- `working/G4C-PREFLIGHT-001/git_diff.binary.patch`
- `working/G4C-PREFLIGHT-001/artifact_hash_manifest.json`

No original/baseline files modified; Notebook 4 not rerun; no authorized candidate run directory consumed.
