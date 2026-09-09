# Resume protocol disposition

## Current implementation

**No episode resumption was implemented or enabled.** Phase 2 projects E3 prediction generation below 5000 seconds; the user explicitly requires stopping architectural work at that point.

- No closed experiment can be continued by this package.
- Never rerun or overwrite `G4C-E3-001` or any closed E2 identity.
- No episode is inferred complete from an NPZ filename.
- No signing key was generated and no episode ledger is claimed to exist.
- Native-cache atomic publication concerns identical immutable RF bytes only. It is not a scientific progress checkpoint.
- Preparation requires a new identity and separate authorization. It does not launch an experiment.

## Deferred design if a later authorized measurement triggers Phase 3

This is documentation, not an implementation or current capability.

1. One logical new run, explicit ordered manifest entries, and bounded invocation IDs. Preserve the 60-episode order, RNG states, and E4's separate zero-shot record. Store frozen input, preprocessing, schema, RF, source state, worker/runtime/validator code hashes in a run contract.
2. A single coordinator lease plus a signed append-only ledger. Use a real authenticated scheme (for example an externally provisioned Ed25519 signing key and separately pinned public key); a bare hash chain is not a signature. Archive ledger-head receipts externally if rollback/truncation detection against an owner-level adversary is required.
3. Publish `DISPATCHED` before launch. After successful worker exit and verified teardown, preserve predictions, adaptation state, all transport/lifecycle evidence, runtime, peak memory, warnings, packet hash, episode index, RNG-before/after, and manifest position. Flush/fsync temporary payloads, publish atomically without overwriting, then publish a signed `COMMITTED` entry last. Retain the original prediction serializer and bytes.
4. On restart verify the signature chain, invocation provenance, every committed artifact, frozen anchors, source-state hash, and the ledger-to-manifest ordering. Continue only the next `PENDING` episode. Never rerun `COMMITTED` episodes; never assemble completion from filenames alone.
5. On an uncertain `DISPATCHED` entry, do not auto-rerun. Recover only a fully durable valid result plus successful teardown evidence. Otherwise stop for explicit resolution. Exactly-once execution cannot be promised for arbitrary mid-worker host failure using a ledger alone.
6. Use a conservative deadline reserve large enough for the complete next dispatch/worker/teardown/commit cycle. Stop gracefully between episodes; do not deliberately rely on the 5000-second killer. Preserve the current worker timeout/resource caps.
7. Do not attach evaluator query labels or score until all required predictions and teardown/probe evidence are committed. Then run the same metric/criteria logic and independent verifier, preserving all per-episode checks and final aggregate validation.
8. Fault-injection tests must cover lost writes, rename interruptions, concurrent coordinators, invalid signatures, changed frozen inputs, stale ledger heads, orphan outputs, uncertain dispatch, wrong RNG/manifest position, and failure after teardown but before commit. Compare uninterrupted and interrupted synthetic executions byte-for-byte before any candidate authorization.

No part of this deferred design authorizes worker reuse, retained cross-episode support labels, missing validation checks, duplicated episodes, or new scientific choices.
