# E3 validator binding repair and certification 002

## Final decision

**CERTIFICATION FAILED.**

The run-ID/path binding repair and 19 offline validator tests passed. The subsequent deterministic offline equivalence test stopped at its first selected episode because a regenerated prediction NPZ file did not match the archived file's SHA256. Prediction arrays had matched elementwise before that file-level check.

Per the explicit stop condition, no equivalence retry, serializer repair, further certification benchmark, candidate worker, or full E3 experiment followed. This is **not evidence of an E3 scientific failure or an original-versus-optimized prediction difference**: failure occurred on the original-RF reference reconstruction before the optimized-native comparison was reached.

## 1. Root cause of the old binding failure

The generic legacy validator hard-codes `G4C-{method}-001` in both normal and exception paths and expects an older root-level layout (`entry.json`, `parameters.json`, `source_state.json`, `per_episode_results.json`, `summary.json`, `code/`). The optimized coordinator uses `checkpoint/`, `candidate_state/`, `results/`, and `coordinator/` and does not install a compatible validator.

`PATH_BINDING_MAP.md` records the inspected path assumptions and exact path/schema mappings. No historical target is used as a fallback.

## 2. Files changed

Only new files under `working/G4C-INFRA-CERT-002/` were created:

- `code/e3_validator.py`: explicit-target independent E3 validator and historical hash-only inspection interface.
- `code/bind_e3_validation.py`: preparation-time validator/manifest binding and completion-time report/inventory sealing; neither operation launches code.
- `code/test_validator.py`: synthetic full-layout and negative tests.
- `code/offline_equivalence.py`: bounded privileged archived-output reconstruction, not a candidate worker.
- Certification evidence and reports in this directory.

The optimized package, previous certification, closed E3 run, all historical files, preprocessing, RF, manifests, algorithms and runtime were not modified. No real new E3 run directory was created.

## 3. Exact validator design

Public interface: `validate_e3_run(run_dir)`; CLI takes exactly one directory.

The validator checks canonical target location, E3 identity, current preparation approval, current execution authorization, current source state, current manifest snapshot, current predictions, current evidence, current inventory, current summary and current execution report. Absolute, traversal, symlink and cross-run candidate-output references are rejected. The producer's project-relative paths are accepted only when their embedded run ID equals the explicit target.

Frozen baseline inputs remain independently hash-pinned references. They are not substitute candidate outputs. Historical inspection returns `HISTORICAL_EVIDENCE_ONLY`, never a fresh-run validation PASS.

The binding operation is permitted only before execution and refuses historical/finalized targets. The report renderer echoes the existing full primary summary deterministically; it does not change scores or success criteria. The independent validation result remains separate from primary output.

## 4. Validation semantics preserved

The dedicated E3 validator independently reconstructs the legacy scientific checks:

- full-source class means and active mask;
- fixed class-balanced translation and unchanged indicator columns;
- immutable forest loading and unchanged reference predictions;
- all 60 frozen episode identities/order and advancing seed-42 RNG replay;
- exact support/query and pixel identities, disjointness and manifest array hashes;
- source-state, packet, code, prediction, evidence and confusion hashes;
- prediction NPZ reload and independent prediction reconstruction;
- all per-episode macro-F1, per-class precision/recall/F1, confusion and accuracy;
- exact historical raw baseline trial scores;
- paired raw/RF deltas, budget means, population SDs and positive-trial counts;
- current frozen E3 criteria and verdict, with only layout/field-name mapping;
- source worker and three preflight/fresh-state records;
- isolation labels, descriptor evidence, namespace, runtime lock and successful complete teardown;
- transport commands bound to the target run rather than another run;
- report content consistent with the current summary and full artifact inventory;
- protected inputs and approved provenance checks.

It does not import a candidate or coordinator implementation. The full public validator cannot accept the test double context. No completed E3 output exists yet, so no fresh full-run validation PASS is claimed.

## 5–6. Tests and results

**19 offline tests passed**, including all requested cases:

| Case | Result |
|---|---|
| A: valid complete synthetic 60-episode layout | Accepted by substantive validation core; explicitly `SYNTHETIC_TEST_PASS`, not production PASS |
| B: wrong run identity | Rejected |
| C: historical prediction path substituted | Rejected |
| D: missing prediction | Rejected |
| E: modified prediction, even after rehashing metadata | Rejected |
| F: changed manifest | Rejected |
| G: duplicate episode | Rejected |
| H: wrong episode identity | Rejected |
| I: missing evidence | Rejected |
| J: cross-run evidence reference | Rejected |
| K: corrupted report, even after rehashing | Rejected |
| L: real closed historical evidence | Read-only hash inspection accepted; production validation rejected |
| M: synthetic fixture through production API | Rejected |
| N: path traversal | Rejected |
| O: modified metric after rehashing | Rejected |
| P: failed teardown after rehashing | Rejected |
| Q: invented scientific verdict | Rejected |
| R: binding a finalized target | Rejected |
| S: independently known macro-F1/per-class example | Matched |

The fixture uses synthetic arrays and a deliberately non-RF test double; no scientific experiment or worker executes. Production loading is not replaced with the test double. The synthetic acceptance test runs the actual independent reconstruction/metric/identity/hash checks over 60 synthetic entries, not merely existence checks.

An initial test harness attempt incorrectly shadowed `unittest.TestCase.run` with a path and failed before tests ran. The test-only attribute name was corrected; both attempt logs remain preserved. No candidate was retried.

## 7. Prediction-equivalence result

The deterministic subset was fixed before reading results: manifest ordinals **1, 21, 51**, spanning 5, 25 and 200 labels/class. The offline script uses the same saved source state and fixed input packets, reconstructs predictions with the pinned RF, then compares both original and native-staged RF paths against archived predictions.

Actual progress:

1. Live runtime-tree, wheel and Bubblewrap hash assertions completed without error.
2. Native RF staging/reuse verified the frozen digest.
3. All 60 manifest RNG transitions were replayed as identity checks, without executing 60 predictions.
4. Original-RF reconstruction of `G4A-B005-T01` matched archived query identity, packet hash and all four prediction arrays elementwise.
5. Repacking those arrays using `np.savez_compressed` in archived member order produced an NPZ SHA256 different from the original archived NPZ.
6. The script stopped at `offline_equivalence.py`'s `NPZ byte divergence: G4A-B005-T01` assertion.

The optimized-native prediction reconstruction, the other selected episodes, and metric-digest comparisons were **not reached**. The failed regenerated archive was held in memory and not retained, so no byte-offset or header/compression root cause is asserted. Cross-platform container serialization is a possible explanation, not a verified diagnosis. The preserved failure record and traceback establish the exact failed check.

No serializer normalization, reference overwrite, tolerance relaxation or repeat was performed after failure.

## 8. Runtime evidence

Production runtime readiness is **NOT certified**.

The prior optimized package's estimates were approximately **2,600 seconds point / 4,331 seconds conservative** for 60-episode generation, with a nominal 669-second margin. They remain estimates and are not promoted to PASS here.

The new offline test failed before its successful timing/equivalence result was finalized. No fresh complete before/after runtime range or reliable production margin can be claimed from it. Independent full E3 validation time remains unmeasured. The previously successful native I/O benchmarks remain historical evidence only.

## 9–10. Protected state and historical preservation

Before/after comparison: **1,055 existing files checked; zero changed files**.

- Protected artifacts: **33/33 unchanged**.
- Original Git subtree: clean.
- Frozen preprocessing, RF and episode manifest: unchanged.
- Historical E2/E3 runs: unchanged.
- Optimized package and certification 001: unchanged.
- No actual new E3 identity or candidate worker: created/launched.

Evidence: `evidence/protected_before.json` and `evidence/protected_after.json`.

## 11. Remaining risks and certification boundary

- File-byte prediction equivalence has not passed, even though the first original-reference prediction arrays matched.
- End-to-end optimized transport/isolation was not exercised because candidate workers were prohibited. Code/hash evidence does not invent a fresh worker isolation test.
- Full fresh-run E3 validation and runtime readiness are not yet demonstrated.
- The new validator/binder remains unapproved for production sign-off until the failed equivalence check is resolved and certification is repeated under appropriate authorization.
- The public validator has no historical fallback. The test-only context cannot certify a real run.

## 12. Decision

Binding and offline rejection/reproduction tests: **PASS**.

Protected-state preservation: **PASS**.

Required prediction archive byte-equivalence: **FAIL**.

Optimized prediction comparison and runtime readiness: **NOT COMPLETED**.

**CERTIFICATION FAILED**
