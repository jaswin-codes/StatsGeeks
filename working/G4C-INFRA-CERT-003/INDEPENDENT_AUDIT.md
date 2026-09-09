# Independent audit — certification 003

## Scope and independence

`code/independent_audit.py` is a separate verification implementation/process. It imports neither the candidate/coordinator implementations nor the new payload-comparison helper. It reads archived and certification NPZs and independently computes hashes, ZIP/NPY byte equality, exact NumPy equality, query alignment, RNG replay and metrics. This is not an independent human reviewer signature.

No model is loaded and no worker is launched by this audit. The only predictions checked are the three fixed certification episodes already reconstructed by the offline verifier.

## Findings

### Artifact identity

The historical first-episode archive is 139,993 bytes with SHA256:

`d3c7641cedf4fde41c6e709fc8ea9d214b710eaa09935ba4d31e96c73773d8b0`

The Linux reserialization is 120,669 bytes with SHA256:

`a5627620b69059b42aa837081ea14f55cc3778dbe0404362c111f65e2bb169d6`

Both files are preserved independently. Each artifact's own SHA256 and bound owner/episode/path remains mandatory. No hash is rewritten to conceal the difference.

All 12 replay archives produced by the existing Windows serialization environment match their corresponding historical files byte-for-byte, not just by decoded contents or hash alone. Thus the stricter whole-file certification condition is satisfied at the actual producer boundary.

### Root-cause proof

All six decompressed NPY members are byte-identical. Raw array bytes, NPY headers, names, ordering, dtypes and shapes match. DEFLATE compression differs between the measured `1.3.1.zlib-ng` and `1.3.1` implementations, and ZIP creator system differs between Windows/DOS and Unix. Each platform's compressed streams were independently recreated exactly from the same NPY bytes with default raw-DEFLATE settings. Timestamps are fixed at 1980-01-01 in both, not randomly generated.

This is lossless serialization variation. No scoring-consumed metadata or prediction value differs. The exact failed buffer from certification 002 was not preserved; this audit does not invent that buffer's hash.

### Scientific payload identity

For manifest ordinals 1, 21 and 51, both the original RF and hash-identical native-staged RF reconstructions match the archive exactly. Checked per comparison:

- 77,056 candidate predictions;
- 308,224 prediction values across four methods;
- 539,392 scalar elements including query rows and two-column identifiers;
- zero mismatches and maximum absolute difference zero;
- six exact serialized NPY members per episode;
- unchanged dtype, shape, label set, member ordering and example ordering.

The audit independently recomputes the selected macro-F1, per-class precision/recall/F1, accuracy and confusion arrays with a different counting implementation. Their canonical metric digests match both inference paths. It independently replays the 60 fixed manifest RNG transitions but does not execute 60 episodes.

### Validation strength

The original 19 tests are unchanged and pass. The new exact payload checker adds 23 targeted tests, including 20 negative controls. Changed predictions, labels, dtype/endian/shape, identifiers, ordering, missing/extra/duplicate members, NaN/Inf/object arrays, corrupted hashes, wrong episodes and cross-run references are rejected.

A container-metadata-only change can satisfy payload identity B but is explicitly marked as failing file identity A. It still requires its own correct provenance hash, and it cannot satisfy the separately enforced producer byte-replay gate unless the bytes actually match.

No floating-point tolerance is used for prediction equivalence. Stored prediction/identifier arrays are integral. Existing legacy source-state tolerance is not reused as permission to tolerate prediction differences.

### Historical preservation

The independent audit rehashed 1,072 pre-existing files and found zero modifications. The protected 33-artifact registry, historical E2/E3 archives, frozen preprocessing/RF/manifest and prior certification/optimization files remain unchanged. The final protected-state check is recorded separately as well.

## Runtime limitation and decision

The current offline verifier loaded each forest once and reconstructed three episodes outside the worker orchestration. Its timings are not an end-to-end coordinator benchmark. The prior performance estimates remain estimates, and observed native hashing varied from prior microbenchmarks. No proven upper bound or measured full optimized coordinator duration with safe margin to 5,000 seconds exists.

**Validator correctness, artifact identity and fixed-subset scientific prediction equivalence: PASS.**

**Overall certification: FAILED — production runtime readiness remains uncertified.**

No E3 experiment was launched or proposed as part of resolving this gap.
