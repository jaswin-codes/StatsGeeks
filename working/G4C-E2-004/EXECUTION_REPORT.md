# G4C-E2-004 execution report — STOPPED

## Experiment status

**STOPPED_INFRASTRUCTURE_FAILURE_FIRST_EPISODE**

E2 did not complete. The fixed Madrid-only E2 source state was fitted after two successful isolated preflight workers, but the first target episode worker terminated before parsing its packet or generating predictions. No retry or worker-code repair was performed. E3–E5 and follow-up analyses were not started.

## Completion

| Item | Result |
|---|---:|
| Planned episodes | 60 |
| Completed episodes | **0** |
| Successful preflight workers | 2 |
| Successful Madrid source worker | 1 |
| Failed episode workers | 1 |
| Total workers launched | 4 |
| Candidate predictions | 0 |
| Prediction NPZ artifacts | 0 |
| Episode metrics/confusions | 0 |

## Exact execution issue

The first episode used the frozen identity `B005-T01`. The sealed worker started inside the approved Bubblewrap/runtime boundary but failed at its inherited-file-descriptor assertion:

```text
AssertionError: ('/proc/self/fd/3', '/usr/lib/x86_64-linux-gnu/libffi.so.8')
```

The worker code requires every descriptor observed at that point to be stdin/stdout/stderr pipes (`fd <= 2`). Descriptor 3 referenced the approved runtime's `libffi.so.8`, so the worker returned 1 before `json.load(sys.stdin)` and before any E2 prototype/distance operation. Worker stdout was empty.

This is an infrastructure/isolation-check runtime failure, not an E2 score or scientific falsification. Changing the descriptor policy or worker import order would require a newly authorized infrastructure task and new run identity; neither was attempted here.

## Information boundary and teardown

The failed packet contained only the permitted fields:

- current support X/y/IDs;
- current query X/IDs without query labels;
- frozen Madrid source state;
- fixed current episode parameters.

No manifest, query labels, full Amsterdam label vector, or other-episode labels was in the packet. The worker failed before deserializing it.

The captured lifecycle record reports:

- worker return code 1;
- teardown PASS;
- adopted namespace process reaped;
- final survivors empty;
- no candidate stdout/prediction finalized.

The source worker received Madrid source X/y only, reported zero target rows, fitted the fixed E2 weights, exited successfully, and was fully reaped. Its partial source state and all failure evidence are preserved.

## Fixed configuration

No parameters changed:

- epsilon `1e-6`;
- normalized Fisher ratio;
- clipping `[0.25, 4.0]`;
- identity mixture `0.50`;
- classes `[1,2,3,4]`;
- frozen seed/episode ordering and comparator protocol.

No tuning, sweep, preprocessing change, RF change, manifest change, or Notebook 4 rerun occurred.

## Metrics

No predictions exist, so all requested scientific metrics are unavailable:

- E2 macro F1: N/A;
- paired delta versus raw: N/A;
- U0 comparison: N/A;
- per-class F1/confusion: N/A;
- predefined success criteria: **NOT EVALUATED**.

The accepted raw 25-shot baseline remains `.5986 ± .0176`, but no E2 comparison is valid.

## Validation status

**NOT COMPLETED.** There were no prediction outputs to independently reproduce. Two verifier-only stop-audit attempts failed in evidence parsing/assertion logic and are retained in `results/stop_audit_attempt1_failure.json` and `stop_audit_attempt2_failure.json`. They did not rerun or alter any candidate worker, source state, packet, or output. Consequently, no independent validation PASS is claimed.

Primary frozen-anchor checks performed during execution remained passing: protected artifacts, manifest, RF, historical run inventories, and `original/`. The failed worker's own lifecycle evidence is retained verbatim. The run is closed as an infrastructure stop.

## Preserved artifacts

- fixed source state: `candidate_state/source_state.json`;
- successful preflight/source lifecycle evidence: `evidence/`;
- exact failed first-episode input and failure evidence: `evidence/worker_01*`;
- execution traceback: `results/execution.log`;
- stop reason: `results/EXECUTION_STOP_REASON.md`;
- machine-readable status: `results/summary.json`;
- artifact inventory: `artifact_hash_manifest.json`.

## Final disposition

The success response `EXPERIMENT COMPLETE` is not applicable. E2 remains scientifically unevaluated. Do not continue to another candidate or rerun this identity. A separate infrastructure authorization is required before any new attempt.
