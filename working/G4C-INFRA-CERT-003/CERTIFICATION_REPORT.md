# Infrastructure certification 003 — NPZ equivalence resolution

## Final decision

**CERTIFICATION FAILED — remaining blocker: production runtime readiness is not independently certified.**

The NPZ failure is resolved without changing prediction generation or the production writer. Validator tests, artifact preservation, exact payload equivalence, and producer-side whole-file byte replay pass. No full E3 experiment or candidate worker was launched.

| Gate | Result |
|---|---|
| Validator correctness | PASS: existing 19-test offline suite |
| Artifact/provenance integrity | PASS: historical snapshots, frozen hashes, current bound artifact checks |
| Prediction equivalence | PASS: exact arrays, decompressed NPY bytes, metrics, RNG/identifiers, and producer-side NPZ bytes |
| Runtime readiness | NOT CERTIFIED: no end-to-end optimized coordinator timing/bound |
| Overall readiness for E3 execution | BLOCKED by runtime certification; no scientific divergence found |

## 1. Original failure and preserved evidence

Certification 002 used:

`working/G4C-E3-001/predictions/G4A-B005-T01.npz`

It reconstructed predictions in a Linux privileged verifier, wrote an NPZ to an in-memory `BytesIO` with `np.savez_compressed`, then compared that Linux-generated container's SHA256 with the Windows coordinator's archived NPZ.

The failed 002 in-memory buffer was not retained and its generated size/hash were not logged. Its exact historical buffer hash cannot be recovered from those records. This report does **not** invent it. Certification 003 preserves fresh reproductions, including an actual original-RF reconstruction with the same archived inputs.

## 2. Exact NPZ evidence

### G4A-B005-T01

| Artifact | Bytes | SHA256 |
|---|---:|---|
| Historical original | 139,993 | `d3c7641cedf4fde41c6e709fc8ea9d214b710eaa09935ba4d31e96c73773d8b0` |
| Windows saved-array reserialization, repeats 1 and 2 | 139,993 | `d3c7641cedf4fde41c6e709fc8ea9d214b710eaa09935ba4d31e96c73773d8b0` |
| Linux saved-array reserialization, repeats 1 and 2 | 120,669 | `a5627620b69059b42aa837081ea14f55cc3778dbe0404362c111f65e2bb169d6` |
| Fresh original-RF reconstruction, Linux container | 120,669 | `a5627620b69059b42aa837081ea14f55cc3778dbe0404362c111f65e2bb169d6` |
| Fresh optimized-native RF reconstruction, Linux container | 120,669 | `a5627620b69059b42aa837081ea14f55cc3778dbe0404362c111f65e2bb169d6` |
| Both reconstructions replayed on original Windows producer | 139,993 | `d3c7641cedf4fde41c6e709fc8ea9d214b710eaa09935ba4d31e96c73773d8b0` |

New artifacts are under `evidence/reserialized_*`, `evidence/reconstructed/{original,optimized_native}/`, and `evidence/producer_replay/{original,optimized_native}/{1,2}/`. Historical artifacts were not rewritten.

### Members, order and payloads

All archives have exactly this order:

| Member | dtype | shape | Uncompressed NPY bytes |
|---|---|---|---:|
| `query_indices.npy` | `<i8` | `(25972,)` | 207,904 |
| `query_ids.npy` | `<i4` | `(25972, 2)` | 207,904 |
| `raw_prototype.npy` | `<i8` | `(25972,)` | 207,904 |
| `rf_reproduced.npy` | `<i8` | `(25972,)` | 207,904 |
| `candidate.npy` | `<i8` | `(25972,)` | 207,904 |
| `frozen_rf.npy` | `<i8` | `(25972,)` | 207,904 |

Every decompressed `.npy` member is **byte-identical**, including its 128-byte NPY 1.0 header, dtype, shape, `fortran_order=False`, padding, and actual array bytes. Each member's raw NPY/data SHA256 and header hex are recorded in `evidence/npz_forensics_{windows,linux}.json`. All example order, identifier and categorical label arrays are identical.

### Compression and ZIP metadata

Both writers use `np.savez_compressed`, ZIP method 8 (DEFLATE), default compression level `-1`, and raw DEFLATE `wbits=-15`. No explicit compression level or timestamp override exists in the producer call.

Measured environments:

| Component | Windows producer-compatible replay | Linux verifier |
|---|---|---|
| Python | 3.14.6 | 3.14.4 |
| NumPy | 2.5.3 | 2.4.6 |
| zlib compile/runtime | `1.3.1.zlib-ng` | `1.3.1` |
| ZIP creator system | 0 (DOS/Windows) | 3 (Unix) |

The historical E3 authorization did not record the exact host serializer library versions. The Windows version information above is freshly measured; its output reproduces the historical archive exactly. It is not a fabricated historical environment record.

The DEFLATE streams differ for all six members. Independently compressing each identical raw NPY member using each platform's `zlib.compressobj(-1, DEFLATED, -15)` reproduced that platform's stored compressed stream **exactly**, 6/6 in each environment. This isolates the compressor implementation difference from prediction generation and NumPy array formatting.

| Member | Historical/Windows compressed bytes | Linux compressed bytes |
|---|---:|---:|
| query_indices | 39,427 | 39,427 |
| query_ids | 63,990 | 44,293 |
| raw_prototype | 9,477 | 9,574 |
| rf_reproduced | 8,944 | 9,028 |
| candidate | 8,433 | 8,541 |
| frozen_rf | 8,944 | 9,028 |

The total Linux archive is 19,324 bytes smaller. At corresponding positions up to the shorter length, 119,857 bytes differ; the offset-by-offset evidence is retained. Different compressed sizes also move later member/central-directory offsets.

Identical metadata: all six timestamps are **1980-01-01 00:00:00**; create/extract versions are 45; flags, volume and internal attributes are 0; external attributes are 25,165,824 (`0o600 << 16`); CRCs and uncompressed sizes match; central-directory extra fields/member comments/archive comments are empty. Creator-system metadata differs as shown above. This is **not timestamp nondeterminism**.

Both environments produce identical bytes on repeated writes within the same environment. Byte identity across different compressor implementations/ZIP creator systems is not implied by equal NumPy arrays.

### Root cause

**The certification harness compared different serialization environments.** It confused the Linux verifier's reserialization with the Windows coordinator's artifact generation. Differences are lossless compression/container representation only, not prediction values or scientific data. No scientifically consumed metadata differs.

## 3. Contract and equivalence invariant

The existing frozen plan requires every payload's size/SHA256 for provenance and independent prediction/metric reproduction. The original coordinator records the saved NPZ's SHA256, then scores named arrays reloaded with `allow_pickle=False`. The legacy independent verifier checks each saved file against its recorded hash and separately checks reconstructed predictions with `np.array_equal`; it does not recompress an NPZ in another runtime and demand the same archive hash.

Concrete sources:

- `working/gate4_candidate_experiment_plan.md`, reproducibility contract and sign-off checks: payload size/SHA256, saved predictions, independent reload and F1 reproduction.
- `working/G4C-E3-001/coordinator/execution_coordinator.py`: `np.savez_compressed`, per-file `prediction_sha256`, named-array reload and scoring.
- `working/verify_g4c_candidate.py`: immutable archive SHA256 check plus independent array equality and metric/confusion reconstruction.

The concepts are distinct:

- **A — artifact identity:** full NPZ bytes and SHA256. Required for immutable artifact/provenance verification. Also retained as an explicit stronger producer-replay certification gate here.
- **B — serialized payload identity:** exact member names/order, dtype, shape, values, example order, identifiers and decompressed NPY bytes. No tolerance, coercion, sorting or dropped fields.
- **C — scientific prediction identity:** exact categorical predictions aligned to the same examples, yielding identical metrics.

**A was not replaced with B or C.** Certification now enforces all of them at the appropriate boundary:

1. Every historical and generated archive is verified against its own bound run/episode/path/hash record.
2. Original and optimized inference paths must satisfy exact B and C.
3. Their outputs are replayed through the unchanged original Windows producer serializer, twice each. Each resulting archive must be byte-for-byte identical to the historical archive and to the other inference path's archive. The complete SHA256 assertion remains mandatory.

Linux-container hashes remain recorded rather than normalized away. No production serializer, model, prediction operation, seed, preprocessing, scoring, criterion, isolation or teardown code was changed. No new deterministic writer was needed: the actual producer is already deterministic for these payloads.

## 4. Minimal certification-only changes

New `code/prediction_equivalence.py` performs exact payload and explicit provenance checks. `code/offline_equivalence.py` is a copy of certification 002 with only its equivalence/evidence boundary amended: it preserves reconstructed files, checks their bound payloads, and leaves full archive identity pending producer replay. `code/producer_byte_replay.py` enforces that full byte gate on Windows.

The validator, binding tool and existing 19-test suite are byte-for-byte copies of certification 002. All historical files are unchanged. `changes.patch` records the certification harness change and new checker/replay modules.

## 5. Tests and negative controls

- Existing offline validator/binding suite: **19/19 PASS**.
- Targeted payload/provenance suite: **23/23 PASS**, comprising 20 rejection controls and 3 positive/regression cases.
- Direct DEFLATE-stream reconstruction: **6/6 members per platform PASS**.
- Same-payload repeat serialization: PASS in both environments.
- Full original-Windows byte replay of the reconstructed subset: **12/12 PASS** (3 episodes × 2 RF locations × 2 writes).

Targeted rejection controls include: one changed prediction; invalid class label; class mapping permutation; prediction order; changed identifier; missing/extra array; dtype; endianness; shape; complete example reorder; ZIP member reorder; NPY storage order; NaN; Inf; object array; duplicate ZIP member; wrong artifact hash; wrong bound episode; and a different run's file even when its bytes are identical.

Container-only metadata variation passes B but is explicitly reported as not passing A; a changed artifact still fails its provenance hash. This test does not bypass the producer byte gate.

An initial forensic inspection used a NumPy private header-reader attribute unavailable in the installed version. It was replaced with the public NPY 1.0/2.0 readers before completing diagnosis. No scientific operation or historical artifact was changed; the already-created raw reserialization evidence was retained.

## 6. Fixed-subset prediction results

Subset remains the previously fixed ordinals **1, 21, 51**:

| Episode | Query predictions per method | Archived/producer NPZ bytes | SHA256 |
|---|---:|---:|---|
| G4A-B005-T01 | 25,972 | 139,993 | `d3c7641cedf4fde41c6e709fc8ea9d214b710eaa09935ba4d31e96c73773d8b0` |
| G4A-B025-T01 | 25,892 | 138,761 | `a1c468e41f214cb7e620482525cc91da6ad3b1edb661aec1f42a0912ea0aac38` |
| G4A-B200-T01 | 25,192 | 136,137 | `8329b553ccea3822d39399609802acf0beb0473c21c9274356ae19c52d70f714` |

For each inference path:

- Candidate predictions compared: **77,056** episode/query outputs.
- All four prediction methods compared: **308,224** categorical outputs.
- Six stored arrays including identifiers: **539,392** scalar elements per comparison.
- Mismatches: **0**. Maximum absolute difference: **0**.
- Dtypes, shapes, member order, example order, identifiers and class labels: **exactly equal**.
- Every stored array is integer-valued; no floating-point tolerance is permitted or used for prediction equivalence.
- Selected metrics match exactly across both paths and an independent read-only audit.
- All 60 manifest RNG transitions replayed identically as identity checks, not 60 episode executions.

The pre-existing source-mean/translation reconstruction checks retain their original legacy tolerance; this tolerance is not applied to stored prediction arrays or metrics. No statistical methodology was changed and no full E3 scientific verdict was computed.

A separate audit implementation imported neither the payload checker nor the candidate/coordinator implementations. It independently compared ZIP/NPY bytes, arrays, metrics, identifiers, RNG replay and the 12 producer replays. Result: **PASS**.

## 7. Performance evidence and limitation

Historical optimization evidence remains unchanged and valid as historical measurements:

- bounded signature reads retain the same full integrity checks;
- the Linux-native RF has the same frozen SHA256;
- protected worker/scoring/isolation/teardown code remains unchanged;
- previous integrity scan benchmark: 7.18–7.71 s → 6.16–6.27 s;
- previous RF hash benchmark: 18.73–19.95 s → 1.36–1.37 s;
- previous raw RF read benchmark: 15.90–17.03 s → 0.116–0.123 s.

Fresh bounded offline reconstruction measurements:

| Component | Original RF location | Native RF location |
|---|---:|---:|
| One full RF hash | 17.22 s | 6.13 s |
| One RF unpickle/load | 22.06 s | 8.89 s |
| Each selected prediction reconstruction | 1.31–1.48 s | 1.70–2.19 s |

The live runtime tree check matched all **4,355** files, approved wheel hashes and Bubblewrap hash. These were read-only package checks, not fresh sandbox worker launches.

The fresh native hash cost differs materially from the earlier microbenchmark. This demonstrates why the prior **2,600–4,331 s** generation estimate and **669 s** nominal conservative margin must not be promoted to a runtime certificate. The offline verifier loads one forest per path and does not measure the fresh-worker launch, repeated coordinator scans, packet transport, per-episode model loading, or teardown costs of an end-to-end run.

**Runtime readiness remains uncertified.** There is no independently measured end-to-end optimized coordinator duration or proven bound below 5,000 seconds, including sufficient margin. Independent full E3 validation time is also unmeasured. No full E3 execution was proposed or performed to bridge this gap.

## 8. Protected state

Before/after checks cover **1,072 existing files**, including all previously protected historical material and certification 002. No changes were found. All **33 protected artifacts** remain unchanged. Historical E2/E3 NPZs, frozen RF, preprocessing, manifest, worker/scoring/isolation/teardown code, optimized package and earlier certifications are preserved.

All changes are new files under `working/G4C-INFRA-CERT-003/`. No candidate run identity or candidate worker was created/launched. The subset computations were privileged offline reconstructions only.

## 9. Independent audit and final decision

See `INDEPENDENT_AUDIT.md`, `evidence/independent_audit.json`, `evidence/producer_byte_equivalence.json`, forensic JSON records, test logs and the final artifact manifest.

The NPZ mismatch is fully explained and resolved at the correct serialization boundary. File identity, payload identity and scientific prediction identity are all retained and demonstrated for the fixed subset.

**CERTIFICATION FAILED — runtime readiness remains the exact outstanding gate.**
