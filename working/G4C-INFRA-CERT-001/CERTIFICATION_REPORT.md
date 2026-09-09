# Optimized infrastructure certification — FAIL

## Part 1 — Certification decision

**FAIL: `VALIDATION_BINDING_MISSING`.**

The optimized package does not provide a compatible, bound independent E3 validation pipeline for a new run identity. Therefore the required validation/readiness condition fails before prediction-subset execution.

This is a production validation integration failure, not evidence of changed model predictions, preprocessing corruption, or scientific falsification. No claim of complete scientific equivalence is made.

As required, certification stopped at this failure. No repair, further optimization, deterministic-subset worker, full experiment, or new E3 run was started. Historical closed runs remain unchanged.

## Part 2 — Infrastructure verification

Fresh checks completed during this certification:

| Check | Result |
|---|---|
| Optimized package manifest anchor and 22 payload hashes/sizes | PASS |
| Validated E2 manifest anchor and 216 payload hashes/sizes | PASS |
| Closed E3 manifest anchor and 184 payload hashes/sizes | PASS |
| Protected artifacts | 33/33 PASS |
| Frozen original RF hash | PASS |
| Episode manifest hash | PASS |
| Source/episode/preflight worker bytes | Identical |
| Boundary, runtime-check implementation and teardown implementation bytes | Identical |
| Original and optimized full coordinator integrity checks | PASS; identical results |
| Bounded-read transformation | Only the expected signature-read helper/integrity function changed |
| E3 coordinator main, packet-call function and metric function AST | Unchanged |
| Compatible independent E3 validator for a new identity | **FAIL — absent** |
| Live Linux-native cache and runtime-tree checks | NOT RUN after preflight failure |
| Fresh isolation/teardown worker checks | NOT RUN after preflight failure |

RF SHA256:

`5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870`

Episode manifest SHA256:

`9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`

Historical native-staging hash-equivalence and runtime evidence remains preserved in `working/G4C-INFRA-PERF-001/`. It is not presented as a fresh live runtime/cache check in this failed certification.

### Exact validation defect

`working/G4C-INFRA-PERF-001/code/prepare_assets.py::asset_bytes()` produces nine implementation assets, none of which is an independent E3 validator. Its preparation path likewise does not configure a verifier for the new run identity.

The prepared coordinator writes:

- `candidate_state/source_state.json`
- `results/per_episode_results.json`
- `results/execution_summary.json`
- execution assets under `coordinator/`

It ends with status `COMPLETED_PENDING_INDEPENDENT_VERIFICATION`; it does not itself complete independent validation.

The available legacy `working/verify_g4c_candidate.py` instead:

- fixes its target to `G4C-{method}-001`, which would target the closed E3 directory;
- expects root-level `entry.json`, `source_state.json`, `per_episode_results.json`, `summary.json`, and `parameters.json`;
- expects execution code under `code/`;
- uses the older result/summary field contract.

It cannot validate the prepared new-run outputs unchanged. Merely finding an E3 algorithm branch in that legacy verifier does not establish compatible production validation. The optimized package's `audit_offline.py` checks archived E2 outputs and hashes closed E3 artifacts; it is not a new E3 result verifier.

## Part 3 — Prediction equivalence

**NOT RUN.** A deterministic verification subset was authorized only within successful certification progression; the mandatory production-validation preflight failed first. The explicit stop-on-any-failure condition was followed.

No byte-identical optimized prediction result is claimed. Identical worker/scientific-code bytes are supporting static evidence, not a substitute for the requested empirical subset comparison.

## Part 4 — Runtime estimate

Previously recorded estimates, not fresh certification timings:

- E3 prediction generation point estimate: approximately **2,600 seconds**.
- Conservative scenario: approximately **4,331 seconds**.
- Nominal margin to 5,000 seconds: approximately **669 seconds (13.4%)**.

These estimates exclude unmeasured independent E3 validation and are not an end-to-end guarantee. Runtime readiness and the absence of remaining bottlenecks are **not certified** by this attempt.

## Part 5 — Execution disposition

- New E3 run created: **No**.
- Candidate workers launched: **0**.
- Prediction-subset episodes executed: **0**.
- Full E3 episodes executed: **0**.
- E4/E5 executed: **No**.
- Infrastructure/scientific files repaired or modified: **No**.

The next prerequisite is a separately reviewed independent E3 verifier binding to the new identity and existing output schema, preserving all frozen prediction/metric/manifest/isolation/teardown checks. It must be in place before repeating certification. No implementation of that repair occurred here.

## Evidence

- `certify_preflight.py`: certification-only checks; no candidate-launch path.
- `certification.json`: machine-readable decision, hashes, code comparisons, and exact failure.
- `preflight.log`: captured certification output.
- `artifact_hash_manifest.json`: inventory of this certification evidence.

CERTIFICATION FAILED
