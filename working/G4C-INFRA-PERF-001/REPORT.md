# Infrastructure performance upgrade 001

## Status and scope

**Phase 1 implemented; Phase 2 non-worker benchmarks and offline checks PASS.**

**Full execution readiness is NOT certified.** No optimized coordinator/worker was executed. E3 generation is projected below the external limit, but E4/E5 worker time and candidate-specific validation have not been measured. The preparation utility binds the existing E3 coordinator only; it deliberately does not invent E4/E5 scientific coordinator/validator bindings.

Workers launched: **0**. Experiments started: **0**. Forest deserializations/fits: **0**. Partial E3 results scored: **0**.

Per the Phase 2 stop condition, no worker pool, altered orchestration, shortened validation, or resumable architecture was implemented. This is an offline infrastructure certificate, not a claim that E3/E4/E5 have completed or that their scientific conclusions are known.

## 1. Infrastructure changes

1. Replace the coordinator's `p.read_bytes()[:16].hex()` with a context-managed `stream.read(16).hex()` helper. All original hash/stat/attribute/inventory checks still run, twice per episode exactly as before. No memoized hash acceptance or mtime-only verification.
2. Stage the exact frozen RF on Linux-native storage. Creation uses a private temporary file, streamed copy, flush/fsync, full SHA256 verification, mode 0444, and atomic no-overwrite hard-link publication on the same filesystem. The cache is content-addressed. Existing corrupt entries fail closed; there is no automatic repair or overwrite.
3. The trusted supervisor uses the native copy as the existing exact-file RF mount. The supervisor hash check, worker hash check, read-only sandbox mount, environment, worker limits, and complete lifecycle/teardown logic remain unchanged. Cache reuse adds a full native SHA256 check; it does not skip existing checks.
4. Add cache path/hash/size/staging-duration evidence alongside, not instead of, the original boundary evidence. Packet bytes, worker input schema, prediction serialization, scoring, and scientific worker bytes remain unchanged.
5. Provide a preparation utility that never launches code. It pins source assets to closed historical inventories, rejects existing run identities, and requires a separately supplied execution approval before preparing a future E3 identity. Merely running `--inspect` creates no candidate run.

No model object is shared between workers. Every future episode still receives fresh process/namespace/adaptation state. No runtime image files are changed.

## 2. Files changed

No historical experiment, frozen dataset, model, manifest, runtime, worker, validator, or documentation file was edited.

New implementation files under `working/G4C-INFRA-PERF-001/code/`:

- `immutable_io.py`: bounded reads, native content-addressed artifact staging.
- `prepare_assets.py`: pinned preparation-only E3 coordinator/transport transformations; byte-for-byte worker/boundary copies.
- `benchmark_io.py`: RF hash/read measurements; no pickle loading.
- `benchmark_coordinator.py`: original-versus-bounded full integrity-scan benchmark; never calls coordinator main.
- `estimate_runtime.py`: explicit scenario calculations.
- `test_infrastructure.py`: synthetic and static tests; no worker execution.
- `audit_offline.py`: separate read-only historical artifact and archived E2 metric audit.

New Linux-native cache:

`/home/jaswin/.local/share/statsgeeks/frozen_rf/5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870.pkl`

The path is configurable in future preparation; it is not a change to the frozen runtime. The cache directory is not mounted into a worker: only the exact RF file is mounted at the original sandbox path `/app/rf_final.pkl`.

## 3. Performance benchmarks

Measured, three repetitions:

| Operation | Before | After |
|---|---:|---:|
| Full coordinator integrity scan | 7.18–7.71 s | 6.16–6.27 s |
| RF SHA256 (1,336,382,673 bytes) | 18.73–19.95 s via `/mnt/c` | 1.36–1.37 s native |
| Sequential RF read, no deserialization | 15.90–17.03 s via `/mnt/c` | 0.116–0.123 s native |

One-time native staging: **33.08 s**. Every copy/hash digest matches the frozen RF SHA256. Before/after integrity functions returned identical results on all three paired measurements.

Evidence:

- `evidence/native_io_benchmark.json`
- `evidence/coordinator_benchmark.json`
- `evidence/tests_linux_final.log`
- `evidence/independent_offline_audit.json`
- `evidence/runtime_estimates.json`

No fsync operations were removed. Forest-loading and inference time were not measured separately; raw sequential-read time is only an I/O proxy. Benchmarks are cache/load dependent and must not be presented as an optimized end-to-end run.

## 4. Runtime estimates and phase decision

The previous E3 trace had 52 workers totaling 2,176.69 s and mean inter-worker overhead 49.06 s. The original full generation projection was approximately 5,600–5,900 s.

| Experiment | Updated generation estimate | Expected under 5000 s? | Evidence strength |
|---|---:|---|---|
| E3 | Point ~2,600 s; conservative scenario ~4,331 s | **Expected yes for generation; not certified** | Saved E3 trace plus measured I/O substitutions |
| E4 | ~2,200–3,000 s | **Provisionally yes; not certified** | E2 timing proxy only; includes required separate zero-shot record conceptually |
| E5 | Not established | **Unknown** | No E5 worker measurements; no justified end-to-end estimate |

E3 conservative scenario: historical faster cross-filesystem hash (13.17 s), slowest measured native hash, minimum measured bounded-read saving, an added cache-verification hash, zero credit for unpickling I/O savings, and cold staging overhead. It leaves about **669 s / 13.4%** margin relative to 5000 s. This is a scenario, not a statistical confidence bound.

The point estimate credits both relocated hash passes and the measured sequential-read proxy. It is more optimistic and should not be used as a hard scheduling guarantee. E4 is an unmeasured proxy, not a transferred E2 scientific result.

For E5, a planning relationship is roughly `1500 + 60 * native_worker_seconds`; the unknown worker term prevents certification. The existing 180-second worker cap is unchanged and is not a measured E5 runtime.

Independent candidate validation durations are **unknown** and excluded from the table. Validation remains a separate, unchanged required phase; none of its checks may be removed to meet the budget.

**Phase 3 not triggered:** the E3 prediction-generation projection is below 5000 s with margin. Per the explicit stop condition, no further architecture was added. An unmeasured E5 is not evidence that optimized runtime still exceeds the limit.

## 5. Scientific equivalence verification

Verified offline:

- Exact unchanged hashes for source/episode/preflight worker bytes, approved boundary, runtime-check implementation, and lifecycle implementation.
- AST comparison: only `preexisting_integrity` gains the bounded signature helper; candidate loop, packet construction, metric functions, summary logic, criteria and verdict logic remain unchanged in the E3 coordinator transformation.
- Synthetic supervisor test: same packet, worker bytes, role, result and boundary evidence; only the host RF location and additional I/O provenance change. The boundary call was mocked; no worker was launched.
- All **33 protected artifacts** unchanged.
- All **216** inventoried E2 payloads and **184** inventoried closed E3 payloads unchanged.
- Independent recomputation of **300 archived E2 method/episode macro-F1, per-class-F1 and confusion records** from 60 saved episode files matched exactly.
- All 52 historical E3 prediction artifacts remained hash-identical; they were not evaluated.
- RF SHA256 remains `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870`.
- Episode manifest SHA256 remains `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.

Not verified under this authorization: newly generated optimized prediction bytes, candidate-specific end-to-end validation, actual E4/E5 runtime, or new scientific conclusions. No claim of fresh prediction reproduction is made from code inspection alone.

## 6. Resume protocol

See `RESUME_PROTOCOL.md`. Resumption was not implemented because the Phase 2 stop condition was reached. Historical closed identities remain closed. There is no signed episode ledger, restart switch, or filename-based resume heuristic in this upgrade. Atomic cache publication is not an episode checkpoint.

## 7. Independent audit and readiness boundary

See `INDEPENDENT_AUDIT.md` and `evidence/independent_offline_audit.json`. The audit is a separate implementation/process, not an independent human reviewer.

**Certified here:** offline infrastructure checks, native RF byte identity, unchanged scientific code/boundaries, bounded-read equivalence, archived artifact/metric preservation, and synthetic transport behavior.

**Not certified here:** production execution readiness for all three candidates. A separately authorized equivalence execution and E4/E5 coordinator/validator bindings remain necessary before that claim can be made. No experiment was started to bridge this evidence gap.

The frozen/inventoried `docs/MASTER_PLAN.md` was not edited because changing it would invalidate the current provenance checkpoint. This scoped report records the infrastructure status without silently changing frozen provenance.
