# G4C mutable metadata audit 002 — PASS; STOP BEFORE MODELLING

## Decision summary (A–E)

**A. Is it definitely external mutable metadata?** Its identity as a Microsoft OneNote table-of-contents file and its externally observed mutability are established. The exact writer process is **not** established. Do not equate a running OneNote process with proven write-event ownership.

**B. Can it safely be excluded?** Yes, narrowly: `working/Open Notebook.onetoc2` may have logged content/size/mtime changes under the same-file/type safeguards below. It is unrelated to modelling inputs and cannot enter the audited candidate packet/mount boundary. It is not exempt from observation.

**C. Exact next-run rule:** permit and log only that exact path's content/size/mtime changes. Every other pre-existing experiment file remains immutable. No wildcard/suffix/directory exemption. All protected hashes, original/ cleanliness and membership, frozen manifest and full runtime/dependency hashes remain mandatory. Missing files, non-allowlisted changes, redirection or unapproved additions stop execution.

**D. Is a new E2 attempt now safe?** The **metadata-provenance gate is ready**: independent policy tests and checkpoint dry-run PASS. This is not a candidate execution/reproducibility certificate or authorization. The existing runner is untouched, still targets the closed run/checkpoint, and must NOT be invoked. A future separately pinned coordinator must adopt checkpoint 002 and this exact policy, preserve all episode/isolation checks, use a new run identity and pass candidate-specific preflight under new execution authorization.

**E. Recommended new ID:** `G4C-E2-002` (not created or executed). `G4C-E2-001` remains permanently closed and unchanged.

## Scope and prohibitions observed

Only read-only provenance/integrity analysis, passive observation, synthetic policy tests and new audit/checkpoint artifacts were performed. No candidate workers, candidate data loading, model fitting, predictions, Notebook 4 execution, Git cleanup/reset/restore/checkout/stash/commit, process termination, or edits to pre-existing code/data/evidence occurred. No integrity checks were disabled or installed into the old runner.

Historical dirty state was intentionally preserved. The metadata was never opened for writing, replaced, renamed, or attribute-modified by Astra. Necessary creation of the authorized audit/checkpoint directories was not a forced edit to the metadata; updates correlated with those new directory names appearing in its contents.

## File identity and provenance

- Exact path: `working/Open Notebook.onetoc2`.
- Windows association: `.onetoc2` → `OneNote.TableOfContents.12` → **Microsoft OneNote Table Of Contents**.
- Registered opener: `C:\Program Files\Microsoft Office\Root\Office16\ONENOTE.EXE /navigate "%1"`.
- Binary first GUID: `43ff2fa1-efd9-4c76-9ee2-10ea5722765f`, consistent with OneNote TOC storage. The independently queried Windows association and UTF-16 directory-name contents corroborate the type; the extension alone was not used as proof.
- Initial size: 8,192 bytes; final checkpoint size: 9,544 bytes.
- Creation time reported by Windows: 2026-09-08 08:12:37.455044 UTC. Initial mtime: 18:20:28.708562 UTC; latest observed mtime: 18:41:32.540667 UTC. Complete nanosecond timestamps and attributes are retained.
- Git tracked, mode `100644`, stage 0 index blob `b5013052a1f9c94f897041e42b4be1f5bd24505c`; status ` M` means an unstaged working-tree modification, not a staged replacement. HEAD remains `165fe11df8779eed514c75bd2852c2b9588a18a4`.
- Regular, single-link, non-reparse file, attributes 32; file identity unchanged across the second update.

### References and experiment relevance

The file **is referenced by provenance inventories/Git-status evidence**. Claiming it has no manifest references would be wrong. Its prior broad checkpoint hash was the cause of the stopped preflight.

Static text review found no metadata reference in candidate source/episode workers or the candidate boundary. The coordinator loads its broad hash inventory and therefore hashes the file indirectly; that is an integrity dependency, not a modelling dependency. Candidate packets contain only explicit source or current support/query feature fields, IDs, parameters and source state. Sandbox mounts expose only the approved runtime, sealed worker code, and—where needed—the exact frozen RF file; no project/metadata directory is exposed.

Accepted Notebook 4 source names the preprocessed pickle directly; static review did not find a OneNote input or directory glob. It was not executed. The metadata stores directory names such as baseline/Gate 4 evidence directories, not feature vectors, labels, forest state, episode identities, scores or predictions. All 33 accepted protected artifacts retained their hashes before and after this task. The metadata has no demonstrated effect on baseline or E2–E5 numerical inputs; it affects only the over-broad historical provenance comparison.

## Passive mutation evidence

| Read/interval | UTC | Bytes | SHA256 |
|---|---|---:|---|
| Initial read, before audit directory creation | 18:31:59.974012 | 8,192 | `e0a91560faa8fb0413d34cf1e7d982a000bf61297f8c61bb8fb4fc69b6ff66d1` |
| First repeated sample | 18:33:06.423545 | 9,368 | `bf5daa01690f85533703d0ebad9192bdb3d54c8797626148d51b613ad63c5a8a` |
| End initial 180-second interval | 18:36:06.421817 | 9,368 | same |
| Checkpoint 002, after its necessary directory creation | 18:41:45.644759 | 9,544 | `516003e09e847ddeccff55a466b8a917a83f05791b7136c781ecdf2cfa62f608` |
| End checkpoint dry-run | 18:44:45.724773 | 9,544 | same |

Date: 2026-09-08. First change's OS mtime was 18:32:05.673876; second was 18:41:32.540667. Metadata gained the audit directory name. Both updates occurred without Astra writing the target file.

There were **37 samples at 5-second intervals in each of two 180-second waits**. Neither wait itself captured an additional content transition: changes were detected across the initial-read/start interval and around checkpoint creation. We do not claim continuous write-event tracing or manufacture a mutation during the dry-run.

### Attribution limits

Windows process snapshots show `ONENOTE.EXE` PID 35804 and OneDrive PIDs 3148/43684 running. Windows Restart Manager was queried four times using register/get-list/end only: it reported **no resource users**. No shutdown/restart API or unrelated process termination was used. This neither identifies the writer nor excludes a transient open/close writer. No confident OneNote-versus-OneDrive PID attribution is available.

Windows snapshots showed audit Python and editor tooling, not project experiment runners. A later WSL process listing showed system services and the read-only listing, not candidate/bwrap workers. No candidate was launched by this task. Point-in-time observations do not prove absence of every possible external transient process between samples.

## Exact integrity policy and independent tests

Allowlist: **only `working/Open Notebook.onetoc2`**. Content hash, byte length and mtime may change and must be reported. It must retain the same file identity/attributes, regular single-link non-reparse status and OneNote TOC signature. Deletion, replacement, redirection, changed attributes or invalid type stops. These safeguards are intentionally stricter than a generic mutable-file exemption.

The default denylist covers all other pre-existing working files, candidate code/configuration, datasets, baseline/model artifacts, source/adaptation state, episode manifest, prediction/evaluation evidence, original/ and runtime files. Other `.onetoc2` paths are explicitly tested as forbidden changes. Newly authorized audit/run artifacts are exclusively created and separately inventoried; no pre-existing evidence is overwritten. Unexpected additions outside declared new evidence destinations stop.

An independent process justified the exception from recorded type/mutation evidence and static input/mount review. **22 synthetic tests PASS**, including code/config/data/RF/manifest/prediction/runtime mutations, other OneNote metadata paths, and invalid allowed-file identity/type changes. Tests changed dictionaries only, never project artifacts. The reference policy resides under this audit directory only.

## New checkpoint and dry-run

New checkpoint: **`working/G4C-PROVENANCE-CHECKPOINT-002/`**. Historical checkpoint and reports were untouched. It contains HEAD/status/full staged and unstaged binary diffs/index, 431 file fingerprints, protected hashes, manifest/RF hashes, runtime hashes, metadata state, exact exception, timestamp and authorization.

> Open Notebook.onetoc2 is explicitly treated as external mutable
> metadata under a path-specific integrity exception. All other
> pre-existing experiment files remain immutable.

Dry-run and independent reload results:

| Requirement | Result |
|---|---|
| Gate 4A teardown/isolation inventory | PASS, hashes unchanged |
| Gate 4B/E1 inventory and outcome | PASS / fixed E1 FALSIFIED |
| Raw baseline 25-shot | .5986 ± .0176, unchanged |
| Protected files | 33/33 unchanged |
| Manifest | Authorized SHA256 unchanged |
| RF | Authorized SHA256 unchanged |
| original/ | Git-clean; checkpoint files and membership unchanged |
| Runtime | 4,355 files, all six wheels and Bubblewrap match before/after |
| Closed G4C-E2-001 | Inventoried evidence unchanged |
| All checkpointed files | 431 independently rehashed; zero non-allowlisted changes |
| Passive checkpoint wait | 180 seconds, 37 samples; zero changes during wait |
| Negative policy tests | 22/22 PASS; non-allowlisted mutations STOP |
| Candidate launches / data loads / fits | 0 / 0 / 0 |

The dry-run PASS demonstrates a stable checkpoint and fail-closed policy behavior; a live allowed-file change occurred around checkpoint creation and was separately verified against the same-file safeguards. It does not imply future metadata changes are guaranteed or that scientific candidates will succeed.

## Remaining risks and next action

1. Writer PID/mechanism remains unattributed. External mutable metadata status does not require guessing that PID; the evidence and limits are explicit.
2. Future metadata replacement/type/attribute changes or any other file changes still stop. Do not broaden the exception after a failure.
3. Existing runner still points at the old checkpoint/run ID and has not been repaired or invoked. A new pinned coordinator must implement the exact policy; this audit-only reference is not silently integrated.
4. Candidate isolation/execution and prediction reproducibility remain untested for E2–E5. They require separate execution authorization and candidate-specific preflight.
5. This is preserved dirty-state provenance, not a claim of a clean Git tree.

**STOP here. Recommend `G4C-E2-002` for a separately authorized attempt. No experiment execution is authorized or performed by this audit.**

## Artifact guide

- `initial_metadata.json`, `metadata_after_observation.json`, `metadata_timeline.json`
- `windows_file_association.json`, `observations.json`, `linux_process_snapshot.json`
- `static_reference_audit.json`, `baseline_source_reference_review.json`
- `exception_policy.json`, `allowlist_denylist.md`, `integrity_policy.py`
- `independent_policy_verification.json` (22 tests)
- `dry_run_results.json`, `frozen_postflight.json`, `runtime_verification_after.json`
- `independent_dryrun_verification.json`
- New checkpoint 002 and its artifact inventory
- `artifact_hash_manifest.json` inventories all audit files except itself
