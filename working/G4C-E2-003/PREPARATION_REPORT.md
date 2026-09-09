# G4C-E2-003 coordinator preparation report

## Final status

**PREPARED FOR MODELLING**

The new coordinator's isolated, no-worker preflight completed successfully with status:

`READY FOR TEAM LEAD EXECUTION AUTHORIZATION`

This is preparation readiness only. E2 was not executed. A separate explicit modelling authorization is still required.

## 1. Preserved history and new identity

- New preparation identity: **G4C-E2-003**.
- `G4C-E2-001` remains closed, hash-verified, unchanged and unused.
- `G4C-E2-002` and its failed-import evidence remain hash-verified, unchanged and unused.
- Metadata Audit 002 and Provenance Checkpoint 002 inventories match their frozen anchors.
- No historical artifact was overwritten, repaired, reset, restored, checked out, cleaned, stashed or committed.
- All new files are confined to `working/G4C-E2-003/`.

## 2. Root-cause diagnosis

The G4C-E2-002 command used host Python isolated mode:

```text
python.exe -I -B working/G4C-E2-002/coordinator/coordinator.py --dry-run-preflight
```

The exact failing import was:

```python
from integrity_policy import ...
```

Traceback root:

```text
ModuleNotFoundError: No module named 'integrity_policy'
```

There was no missing third-party dependency. Python `-I` intentionally excludes the script's sibling directory from the normal import search path in this invocation. Consequently, execution stopped at line 10 before `dry_run()`, anchor checks, modelling-data access or worker operations.

Dependency chain:

```text
coordinator.py
  -> sibling integrity_policy.py
  -> Python standard library only: pathlib, hashlib, os, stat
```

## 3. Minimum packaging fix

Only the coordinator packaging/import path was changed. Before importing the sibling module, G4C-E2-003 now adds exactly its resolved coordinator directory:

```python
COORDINATOR_MODULE_DIR = Path(__file__).resolve(strict=True).parent
sys.path.insert(0, str(COORDINATOR_MODULE_DIR))
```

It does **not** add the repository root, current working directory, user site, global environment or arbitrary module path. Python `-I -B` remains in force.

Other revision-only changes were the required new identity (`G4C-E2-003`) and anchored preservation checks for blocked G4C-E2-002. No experiment definition, worker implementation, model parameter, baseline, data, RF, manifest, runtime or protected file was changed.

## 4. Successful no-worker preflight

Command:

```text
C:/Users/jaswi/AppData/Local/Programs/Python/Python311/python.exe -I -B \
  working/G4C-E2-003/coordinator/coordinator.py --dry-run-preflight
```

Result:

```json
{
  "status": "READY FOR TEAM LEAD EXECUTION AUTHORIZATION",
  "workers_launched": 0,
  "model_data_loaded": false,
  "metadata_events": 1
}
```

Authoritative machine-readable output: `checkpoint/preflight.json`.

## 5. Integrity results

| Check | Result |
|---|---|
| Protected files | **33/33 PASS** |
| Frozen manifest | Hash-only PASS: `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32` |
| Manifest contents | **Not loaded** |
| Frozen RF | Hash-only PASS: `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870` |
| RF deserialization | **Not performed** |
| Runtime lock | PASS |
| Approved runtime tree | **4,355 files PASS** |
| Approved wheels | **6/6 PASS** |
| Bubblewrap | PASS |
| `original/` | Git status/diff empty; 5 checkpoint files intact |
| Metadata Audit 002 inventory | 23 files PASS |
| Provenance Checkpoint 002 inventory | 14 files PASS |
| G4C-E2-001 inventory | 18 files PASS |
| G4C-E2-002 inventory | 11 files PASS |
| Candidate state/output roots | Absent |
| Git cleanup/provenance-altering operations | None |

The root `working/Open Notebook.onetoc2` changed from the checkpoint state and was classified/logged as `EXPECTED_EXTERNAL_METADATA_MUTATION`. Its file identity, attributes, regular/single-link/non-reparse status and OneNote TOC signature remained valid.

## 6. Metadata and provenance enforcement

The only mutable pre-existing path is exactly:

`working/Open Notebook.onetoc2`

There is no extension, basename, prefix, glob or directory exception. Every other pre-existing path defaults to `DENY_MUTATION`, including all code, configuration, datasets, baseline/model artifacts, manifest, predictions, runtime files, `original/`, and every other `.onetoc2` file.

New paths must be canonical, non-substitute paths under `working/G4C-E2-003/` and assigned an explicit `COORDINATOR` or future `CANDIDATE` owner. Run-local `.onetoc2` files were recorded as coordinator-created and receive no mutable exception after fingerprinting. Candidate output roots remain absent.

## 7. Isolation, teardown and label policy

No worker was launched, as required. Static contract checks all passed for the pinned future boundary:

- exact source packet and episode packet fields;
- project and evaluator manifest not mounted;
- query/full-target/other-episode labels forbidden;
- source worker receives Madrid source state inputs only;
- episode worker receives only frozen source state, current support labels/features/IDs, query features/IDs and fixed episode metadata;
- fresh private namespace and tmpfs;
- dedicated subreaper;
- PID plus process-start-tick identity tracking;
- zombies remain teardown survivors;
- empty final-survivor requirement;
- prediction finalization only after successful worker exit and complete reaping;
- approved runtime checked before packet execution;
- fixed E2 epsilon `1e-6`, clipping `[0.25,4]`, and identity mixture `0.50` present.

These are static pre-execution checks, not a claim that live candidate isolation or predictions were run in this task.

## 8. Scientific non-modification

- Candidate workers launched: **0**.
- Modelling data loaded: **no**.
- Amsterdam query labels loaded: **no**.
- Episode manifest contents loaded: **no**.
- Support/query episode contents loaded: **no**.
- Models fitted: **0**.
- Predictions generated: **0**.
- Notebook 4 rerun: **no**.
- Baseline/experiment definitions changed: **no**.

The coordinator is deliberately preparation-only: its execution path raises an authorization error. It cannot automatically continue into E2.

## 9. Deviations and limitations

1. Live worker isolation and teardown were not exercised because worker launch was prohibited; only pinned-source static checks were performed.
2. The OneNote writer PID remains unattributed, consistent with Metadata Audit 002.
3. A post-pass, optional inline verification helper completed its substantive assertions but then raised `NameError: name 'sys' is not defined` while constructing an isolated-path diagnostic. It wrote no artifact, launched no worker, accessed no modelling data, and did not affect the already successful coordinator preflight. It was not retried after the instruction to stop on a passing preflight. This is transparently recorded but is not a coordinator-preflight failure.

## 10. Required authorization

The exact next authorization must explicitly permit **G4C-E2-003 E2 modelling execution** under the frozen E2 specification, Metadata Audit 002 exact-path exception, Provenance Checkpoint 002, and the pinned worker/isolation contract.

That later authorization must not permit parameter tuning, historical artifact modification, execution under G4C-E2-001/G4C-E2-002, or automatic continuation to another candidate. This preparation task itself grants no modelling authority.
