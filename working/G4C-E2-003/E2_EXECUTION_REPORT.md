# G4C-E2-003 E2 execution report — infrastructure STOP before workers

## Executive decision

- **Experiment status:** `STOPPED_INFRASTRUCTURE_FAILURE_BEFORE_WORKER_LAUNCH`
- **Validation status:** `NOT RUN — no predictions or candidate state exist`
- **E2 predefined success criteria:** `NOT EVALUATED`
- **Scientific verdict:** none; this is neither FALSIFIED nor PROMISING
- **Recommend E3 authorization:** **NO**

The authorized fixed E2 scientific experiment did not begin in a candidate worker. Per the no-repair/no-retry integrity protocol, execution stopped immediately and E2 was not retried. E3–E5 were not executed.

## Failure point and root cause

The preparation-only `G4C-E2-003` coordinator had passed its no-worker preflight. Under the subsequent explicit E2-only authorization, a new execution entrypoint was created in the same run namespace. It preserved fixed E2 parameters and passed initial protected/provenance checks. It then attempted to deserialize the accepted frozen preprocessing artifact in the privileged host controller:

```python
with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:
    d = pickle.load(f)
```

Host Python was deliberately run with `-I -B`. Deserialization failed with:

```text
ModuleNotFoundError: No module named 'working'
```

The pickle contains the exact global reference:

```text
working.minimal_standard_scaler.StandardScaler
```

at byte offset 49,901,669. Isolated mode excluded the repository root, so the pickle could not resolve that project module. This is a privileged-controller packaging/deserialization failure, not an approved-runtime failure and not an E2 numerical/scientific result.

### Minimum future change—not applied

A separately authorized new attempt would need a narrowly pinned import mechanism for exactly `working.minimal_standard_scaler` before deserializing the accepted pickle, while retaining isolated execution and preventing broad environment fallback. No path injection, module alias, retry, or repair was performed after observing this failure.

## Execution boundary at stop

| Item | Result |
|---|---:|
| Candidate workers launched | 0 |
| Worker evidence JSONs | 0 |
| Source-state fits | 0 |
| Episode adaptations | 0/60 |
| Prediction NPZs | 0 |
| Candidate predictions | 0 |
| Confusion matrices/scores | 0 |
| Independent candidate validation | Not possible; no outputs |
| E3/E4/E5 execution | No |
| Notebook 4 rerun | No |

No manifest was provided to a worker because no worker existed. No Amsterdam query labels entered fitting, adaptation, or prediction. The privileged pickle load did not return or assign `d`. Because failure occurred late in the pickle stream, preceding members—including potentially arrays—may have been reconstructed transiently inside the unpickler before the unresolved scaler global; the evidence therefore does **not** overclaim that no host-side transient deserialization occurred. No reconstructed object was made available to candidate code, and no modelling computation followed.

## Fixed E2 configuration at attempted start

- Candidate: bounded diagonal Fisher weighting plus target prototypes
- Source fitting: Madrid labels only
- epsilon: `1e-6`
- clipping: `[0.25, 4.0]`
- identity mixture: `0.50`
- classes: `[1,2,3,4]`
- frozen episodes/RNG/budgets/trials: unchanged
- hyperparameter tuning/sweeps: none

These parameters were recorded but never fitted.

## Integrity and provenance at stop

An independent stop-audit process confirmed:

- protected files: **33/33 PASS**;
- frozen manifest SHA256: unchanged;
- frozen RF SHA256: unchanged;
- `original/`: Git-clean;
- closed `G4C-E2-001`: inventory PASS, unchanged;
- blocked preparation `G4C-E2-002`: inventory PASS, unchanged;
- prediction artifacts: none;
- candidate-state payloads: none;
- worker processes/teardown: not applicable (zero launches).

The exact root metadata change remained governed by the path-specific `working/Open Notebook.onetoc2` exception. No other historical artifact was changed. Existing preparation evidence was not overwritten.

## E2 criteria and requested comparisons

All values are unavailable because zero episodes produced predictions:

| Predefined requirement | Result |
|---|---|
| 25-shot E2 macro F1 | N/A |
| Mean matched gain over raw ≥ +.0100 | NOT EVALUATED |
| Positive raw gain in ≥8/10 trials | NOT EVALUATED |
| No per-class regression worse than .0200 | NOT EVALUATED |
| Positive same-query RF gain | NOT EVALUATED |
| Comparison with U0 | NOT EVALUATED |
| Independent reload/hash/prediction reproduction | NOT RUN; no outputs |

The frozen raw 25-shot baseline remains **0.5986 ± 0.0176**, but no subtraction or scientific inference is valid.

## Final recommendation

Do **not** authorize E3 as a scientific continuation from this result. The suite encountered an infrastructure failure rather than a clean E2 falsification/completion. Under the sequential protocol, the pipeline remains stopped. Team Lead must separately decide whether to authorize a new E2 run identity with only the narrowly scoped pickle-module packaging correction. E2 must not be reported as failed scientifically, tuned, or silently rerun under `G4C-E2-003`.

## Evidence

- `results/execution.log`
- `results/EXECUTION_STOP_REASON.md`
- `results/independent_stop_audit.json`
- `checkpoint/execution_authorization.json`
- `coordinator/execution_coordinator.py`
- `artifact_hash_manifest.json`
