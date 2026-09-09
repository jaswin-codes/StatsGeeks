# Repository cleanup and preservation audit — PROPOSAL ONLY

**Audit date:** 2026-09-09 UTC. **Checkout:** `Hackathon3_StatsGeeks - Copy`, local branch `main`.

## 1. Scope and safety

This is an inventory and preservation proposal, **not authorization to clean or stage files**. The only new project file created by this audit is this report, which did not previously exist. No existing file was edited, deleted, moved, renamed, staged, committed, reset, checked out, merged or pushed. No experiment, model load, training, prediction, E4 or E5 execution occurred. Python was used only for read-only enumeration, JSON/notebook inspection and hashing, with `-I -B`. Git queries used `--no-optional-locks`.

The inventory traversed the entire current checkout, including hidden `.git/` and `.venv_baseline/`, without following directory symlinks. No enumeration errors or directory symlinks were found. Installed packages were inventoried by path/size, not reviewed as project source. External WSL images, wheel caches and native RF storage are outside the directory-size totals; they remain important preservation dependencies. This is not a fresh scientific validation, remote-branch synchronization, exhaustive secret scan or disk-allocation measurement.

**Classification meanings:**

- **A — preserve and version-control:** project source, methodology, required notebooks, compact reproducibility records and durable results documentation.
- **B — preserve locally and in a checksum-verified backup/artifact store, not ordinary Git:** generated bulk evidence, model/data binaries, environments and machine-local state. B does **not** mean disposable.
- **C — genuinely disposable candidate:** explicitly enumerated below; no removal performed or authorized.
- **D — human review:** retain untouched until ownership, provenance or publishing suitability is resolved.

For mixed directories, the specific file rules below override the directory default. The entire original experiment archive must remain intact locally even when selected A files are eventually committed. Ignoring an artifact is not archiving it.

## 2. Executive findings

1. Before creating this report, the checkout contained **27,589 files, 2,804,583,764 logical bytes (approximately 2.61 GiB)**, including Git internals and the Windows environment.
2. `working/baseline_artifacts/rf_final.pkl` alone is **1,336,382,673 bytes**, approximately 1.24 GiB. It must be preserved, not committed to ordinary Git or regenerated as a cleanup operation.
3. `working/G4C-E3-002/` is **22,242,779 bytes / 21.212 MiB**. Preserve every byte. Its production completed 60 episodes; independent validation failed at the Windows/Linux Git clean-tree discrepancy. The frozen coordinator verdict is FALSIFIED, not independently validated. Cleanup must not relabel this a validated experiment.
4. All G4 experiment/certification/checkpoint directories together occupy **579,273,463 bytes**, approximately 552.44 MiB. Failed attempts, interrupted packets, certification diagnostics and code snapshots are evidence, not junk.
5. Fresh read-only checks matched **33/33 protected artifact hashes**, **1,151/1,151 historical file hashes**, and **242/242 E3-002 final-manifest payloads**. E3-002's only files outside that manifest's payload list are the final manifest itself and its checksum sidecar, as expected.
6. The only clear C candidates are the empty root `nul` and three standalone, regenerable `.pyc` files outside experiment directories: **19,483 bytes total**. There is no meaningful safe space recovery from deleting scientific evidence.
7. The working reference Notebook 4 is byte-identical to its organiser source, but has a separate required/protected path. It is **not** a deletion candidate.
8. `models/`, `presentation/` and `submission/` contain only OneNote table-of-contents files. No actual packaged model, slide deck or submission bundle was found there.
9. The master plan and some global status reports lag the preserved experiments. Reconcile status through a separately authorized documentation update; do not rewrite historical reports.

### Preservation checks recorded by this audit

- Protected registry: `working/G4B-E1-001/entry.json`, 33 paths, all current SHA256 values match.
- Historical comparison: `working/G4C-E3-002/hashes/final_protected_audit.json`, 1,151 paths, all current SHA256 values match its recorded observed hashes.
- E3-002 final manifest: `working/G4C-E3-002/final_artifact_hash_manifest.json`.
- Its SHA256: `82bed334430ef5d6bd6f4a40928f3e1995a430a36524336f408fcf5f8ae99aa4`.
- No E3-002 payload was changed or written by this audit. These are content-integrity findings, not a new independent prediction-validation PASS.

## 3. Git starting state

- Local `main`: `165fe11df8779eed514c75bd2852c2b9588a18a4`, “Initial hackathon repository”.
- Local `member2-baseline`, `member3-modelling`, `member4-research` and their cached origin tracking refs point to the same commit in this clone.
- **No fetch was performed.** This does not establish the current remote server state or the contents of a separate member's checkout.
- There are **38 tracked files**, **14 tracked modifications**, numerous untracked working artifacts, and no staged changes.
- Seven modified tracked documents are `docs/DECISION_REGISTER.md`, `docs/MASTER_PLAN.md`, `docs/TEAM_LOG.md`, and `docs/member1_log.md` through `docs/member4_log.md`. These are user/team work to preserve.
- The other seven tracked modifications are OneNote metadata at the root and under `data/`, `docs/`, `models/`, `presentation/`, `submission/`, and `working/`.
- `.venv_baseline/` is currently hidden by its **own** generated `.gitignore` containing `*`; the root ignore file does not explicitly cover this environment name.
- Untracked artifacts are not automatically “on member2's branch” or protected by a branch name. The current working tree has not been captured by the initial commit.

**Do not use `git add .`, `git clean`, a reset or a branch checkout as a cleanup shortcut.** A later change to `.gitignore` will neither untrack existing OneNote files nor make the seven modified scientific/project documents clean.

## 4. Directory sizes

Logical bytes, not allocated disk blocks; MiB = 1,048,576 bytes. Parent totals include children, so do not sum both levels. Measurements exclude this newly created report.

| Directory | Bytes | MiB |
|---|---:|---:|
| `.git/` | 10,898,126 | 10.393 |
| `.venv_baseline/` | 591,004,278 | 563.626 |
| `data/` | 236,533,025 | 225.575 |
| `docs/` | 417,594 | 0.398 |
| `models/` | 5,040 | 0.005 |
| `original/` | 13,952,574 | 13.306 |
| `presentation/` | 5,040 | 0.005 |
| `submission/` | 5,040 | 0.005 |
| `working/` | 1,951,754,568 | 1861.338 |
| `working/baseline_artifacts/` | 1,340,338,730 | 1278.247 |
| `working/member3_baseline_frozen/` | 10,880 | 0.010 |
| `working/__pycache__/` | 24,523 | 0.023 |

### Every G4 experiment/infrastructure directory

**All rows are B archive-default, with the A source/report/compact-record exceptions in section 5.** No entire row is C. This is a preservation classification, not a fresh certification of each historical run.

| Directory under `working/` | Bytes | MiB | Preservation significance |
|---|---:|---:|---|
| `G4A-PRODUCTION-001/` | 240,517,161 | 229.375 | Isolation/probe history; two large input packets and code-at-stop evidence |
| `G4A-TEARDOWN-002/` | 788,454 | 0.752 | Teardown certification, pre-repair and certified code |
| `G4B-E1-001/` | 17,691,805 | 16.872 | E1 baseline comparison, protected registry, 60 predictions and audits |
| `G4C-E2-001/` | 50,594 | 0.048 | Closed preflight/stop evidence |
| `G4C-E2-002/` | 54,984 | 0.052 | Preparation and binding history |
| `G4C-E2-003/` | 112,180 | 0.107 | Preparation/execution failure and coordinator history |
| `G4C-E2-004/` | 44,443,214 | 42.384 | Failed execution evidence including retained input |
| `G4C-E2-005/` | 44,393,925 | 42.337 | Preflight failure evidence including retained input |
| `G4C-E2-006/` | 7,205,637 | 6.872 | Interrupted attempt, including 22 NPZ artifacts |
| `G4C-E2-007/` | 44,390,625 | 42.334 | Preflight failure evidence including retained input |
| `G4C-E2-008/` | 19,694,435 | 18.782 | Complete E2; reported independent verification PASS; preserve both verifier versions |
| `G4C-E3-001/` | 66,421,554 | 63.345 | Closed 52/60 timeout; episode-53 packet is evidence, not resumable state |
| `G4C-E3-002/` | 22,242,779 | 21.212 | Complete 60-episode production; independent validation stopped; immutable preservation |
| `G4C-INFRA-CERT-001/` | 23,260 | 0.022 | Historical certification attempt |
| `G4C-INFRA-CERT-002/` | 284,295 | 0.271 | Validator/binding and initial equivalence investigation |
| `G4C-INFRA-CERT-003/` | 23,711,300 | 22.613 | Exact NPZ payload/producer equivalence, tests and independent audit |
| `G4C-INFRA-CERT-004/` | 46,351,358 | 44.204 | Optimized-path benchmark and documented historical metadata stop |
| `G4C-INFRA-FD-001/` | 79,180 | 0.076 | File-descriptor isolation diagnosis/validation |
| `G4C-INFRA-PERF-001/` | 97,500 | 0.093 | Existing optimized asset generator, I/O helpers, tests and no-resume policy |
| `G4C-INFRA-PICKLE-001/` | 17,328 | 0.017 | Deserialization/provenance investigation |
| `G4C-METADATA-AUDIT-002/` | 196,126 | 0.187 | Explicit metadata policy and observations |
| `G4C-PREFLIGHT-001/` | 89,208 | 0.085 | Starting-state and Git-diff evidence |
| `G4C-PROVENANCE-CHECKPOINT/` | 151,958 | 0.145 | Original authorization/hash/Git checkpoint |
| `G4C-PROVENANCE-CHECKPOINT-002/` | 264,603 | 0.252 | Subsequent bound checkpoint and file fingerprints |

### Largest individual project files

| File | Bytes | Class / reason |
|---|---:|---|
| `working/baseline_artifacts/rf_final.pkl` | 1,336,382,673 | B — exact frozen RF; mandatory external backup |
| `data/madrid_train.parquet` | 141,959,981 | B — immutable organiser data |
| `working/G4A-PRODUCTION-001/current_packet.json` | 120,218,908 | B — isolation evidence |
| `working/G4A-PRODUCTION-001/second_packet.json` | 120,218,908 | B — separate historical packet; equal size is not permission to discard |
| `data/preprocessed/preprocessed_data.pkl` | 50,721,695 | B — accepted preprocessing artifact |
| `working/G4C-E3-001/evidence/worker_53.input.json` | 44,293,287 | B — exact timeout checkpoint evidence |
| `working/G4C-E2-004/evidence/worker_01.input.json` | 44,291,161 | B — failure evidence |
| `working/G4C-INFRA-CERT-004/benchmark_run/evidence/benchmark_preflight_1.input.json` | 44,278,067 | B — benchmark setup failure evidence |
| `working/G4C-E2-007/evidence/preflight_1.input.json` | 44,278,067 | B — failure evidence |
| `working/G4C-E2-005/evidence/preflight_1.input.json` | 44,278,067 | B — failure evidence |
| `data/amsterdam_data.parquet` | 43,840,149 | B — immutable organiser data |
| `working/gate4_approved_runtime_validation.json` | 14,619,946 | B — verbose runtime evidence |
| `working/G4C-INFRA-CERT-003/evidence/npz_forensics_linux.json` | 10,149,890 | B — forensic payload evidence |
| `working/G4C-INFRA-CERT-003/evidence/npz_forensics_linux_final.log` | 10,118,577 | B — forensic log; not disposable because similar to JSON |
| `original/2-Reading_Data.ipynb` | 7,187,442 | A — immutable original notebook, including saved output |
| `working/4-Modelling_member3_reference_executed.ipynb` | 6,946,149 | B — protected executed reference; retain exact bytes |
| `original/4-Modelling.ipynb` | 6,668,714 | A — immutable original notebook |
| `working/4-Modelling_member3_reference.ipynb` | 6,668,714 | A — required separately named source reference |
| `working/baseline_artifacts/madrid_cv_oof.npz` | 3,716,888 | B — baseline OOF evidence |

Largest environment files include `pyarrow/arrow.dll` (21,993,984 bytes), NumPy's OpenBLAS DLL (20,589,056), SciPy's OpenBLAS DLL (20,262,912), and `pyarrow/arrow_flight.dll` (14,660,096). All are B as part of the intact environment, not candidates for selective DLL deletion. Git objects are repository history, not cleanup targets.

## 5. Exhaustive classification rules for the current inventory

The following path rules cover the current relevant files without printing 25,966 individual environment paths or every generated episode payload. A specific named exception takes precedence over a wildcard/default.

### A — must preserve / proposed version-controlled material

| Paths | Rationale / caveat |
|---|---|
| `.gitignore`; this proposed report | Repository policy and review record; no ignore edit performed |
| `original/1-Introduction.ipynb`, `2-Reading_Data.ipynb`, `3-Preprocessing.ipynb`, `4-Modelling.ipynb` | Original project plan and scientific reference; retain all bytes, outputs and paths |
| All `docs/*.md` | Instructions, MASTER_PLAN, decisions, team logs/missions, operating process, scientific methodology, audit and presentation preparation; preserve existing and untracked work |
| `docs/Evaluation Rubric Overview.docx` | Supplied governing document; a binary extension does not make it generated/disposable |
| `working/3-Preprocessing_member2_baseline.ipynb` | Member 2's protected, documented three-cell-deviation reference source |
| `working/4-Modelling_member3_reference.ipynb` | Member 3's protected source reference and required reproducibility path, despite equality with the original |
| All `working/*.py` | Project-owned runners, artifact helpers, isolation boundaries, lifecycle code, protocol validators and diagnostics; preserve source history, not an assertion every root script is the current production entrypoint |
| All `working/*.md` | Handoff, methodology, baseline error analysis, candidate plan, runtime/isolation provenance and historical stop reports; dated scope must be understood before quoting as current status |
| `working/gate4_episode_manifest.json` | Frozen 60-episode identities/RNG/array bindings; not a disposable generated cache |
| `working/gate4_runtime_lock.json`, `working/gate4_runtime_narwhals_lock.json` | Exact historical runtime configuration/hash provenance; absolute paths must not be silently rewritten |
| Other current `working/*.json`, except the B verbose/sampler cases below | Compact readiness, repair, completion and verification records supporting reproducibility |
| `working/baseline_artifacts/feature_schema.json`, `recovery_manifest.json`, `recovery_validation.json` | Feature order and artifact reconstruction/integrity anchors |
| All five `working/member3_baseline_frozen/*.json` | Only about 5.8 KB combined; frozen baseline scores, metadata and artifact manifest; distinct from the recovered model directory |
| Every G4 archive's `*.py` source, including nested `coordinator/`, `code/`, `certified_code/`, `code_at_stop/`, `pre_repair_code/` and `final_certification/code/` | Small exact implementation/validator/test snapshots. Keep old versions as historical evidence; do not deduplicate or execute them as cleanup |
| Every G4 archive's `*.md`; `NON_SCIENTIFIC_RUNTIME_ONLY.txt` | Durable execution/failure/certification reports and scope markers, including E3-002's two preserved prior reports |
| Every G4 archive's `artifact_hash_manifest.json`; E3-002 `final_artifact_hash_manifest.json` and `.sha256`; `changes.patch` | Compact durable archive/hash/source-change provenance; review patches for machine details before publication |
| G4 run `entry.json`, `environment_manifest.json`, `certification.json`; checkpoint `contract.json`, `execution_authorization.json`, `infrastructure_preparation.json`, `validation_binding.json`, `episode_manifest.json`, `file_fingerprints.json`, `checkpoint.json`, `metadata_exception_policy.json`; coordinator `native_cache.json` | Exact identity, authorization and reproducibility bindings; matching names only where they exist |
| G4 root `summary.json`, `independent_verification.json`, `final_audit.json`, `validation_summary.json`; run results `execution_summary.json`, `per_episode_results.json`, `independent_verification_v2.json` | Durable compact scientific/result-validation records; carry failed or incomplete status honestly, not only successful results |
| E3-002 `validation/INDEPENDENT_VALIDATION_FAILURE.json`, `git_discrepancy_diagnostics.json`, `report_lifecycle.json`, `serialization_validation.json`; `checkpoint/data_host_preflight.json`, `runtime_preflight_native.json` | Essential failure, environment, report-lifecycle and strict payload-validation context. Version-control suitability does not permit editing E3-002 |

The source-code rule includes `minimal_standard_scaler.py`, `member3_artifact_helpers.py`, the `run_member2_*`/`run_member3_*` runners, `freeze_member3_notebook4_outputs.py`, `g4c_*`, `gate4*`, `run_g4c_candidate.py`, `run_gate4b_e1.py`, `verify_*`, `certify_gate4_manifest.py`, `independently_verify_gate4_manifest.py`, `diagnose_gate4_teardown.py`, `provision_gate4_runtime.py`, and `stage_gate4_approved_narwhals.py`. None should be lost in a broad `working/` ignore/delete operation.

**A does not mean “stage immediately.”** Review scientific claims, privacy and exact-byte Git handling first. Unselected artifact metadata defaults to B, not C. There is no recommendation to make historical path-bound scripts a new public API or refactor them in this task.

### B — preserve locally and back up; keep out of ordinary Git

| Paths / rule | Why preserve and why exclude |
|---|---|
| `.git/**` | Local repository history/index/configuration; never stage as a nested project artifact or delete as generated output |
| `.venv_baseline/**` | 563.626 MiB of interpreter environment/packages; preserve until approved reproducibility and replacement are established |
| `data/*.parquet` | Immutable supplied source/target data, large and subject to distribution permissions |
| `data/preprocessed/preprocessed_data.pkl` | Exact 50.7 MB accepted cache/scaler/arrays, protected and required downstream |
| `working/baseline_artifacts/rf_final.pkl` and all `*.npz` there | Exact frozen RF, zero-shot predictions, OOF records and trial scores; loss would defeat scientific auditability |
| `working/3-Preprocessing_member2_baseline_executed.ipynb`, `working/4-Modelling_member3_reference_executed.ipynb` | Execution evidence, protected hashes, embedded output; preserve exact originals externally rather than strip outputs |
| All G4 archive files not specifically A or D | Preserve intact runs, including packets, predictions, source/adaptation states, lifecycle evidence, benchmark outputs and raw diagnostics |
| All G4 `predictions/**`, raw `evidence/**`, generated `candidate_state/**`, verbose `hashes/**` except named A records | Generated scientific/audit payloads, often identifiers or local system information; keep local and in the bound archive |
| All current `working/*.log` and run `*.log`, `*.stderr`, raw diagnostic `.txt` / `.bin` | Successful and failed execution evidence, not mere expendable terminal scratch |
| `working/gate4_approved_runtime_validation.json` | 14.6 MB runtime trace; archive rather than ordinary Git |
| `working/gate4_autonomous_sampler_001.json`, `gate4_teardown_sampler_002.json`, `gate4_isolation_sampler_reverification.json` | Generated sampler revalidation evidence; keep outside the source checkout's committed payloads |
| `working/*.pre_completion`, `working/*.pre_dependency_repair` | Explicit prior versions of code/reports/manifests supporting repair history; not presumed editor backups |
| G4 `git_diff*.patch`, `git_status.txt`, `git_index.txt`, `git_ls_files_stage.txt`, `git_HEAD.txt`, raw process/metadata snapshots unless explicitly A | Historical machine/Git-state evidence, sometimes binary-embedded or privacy-sensitive; preserve without presenting as portable configuration |
| `working/G4C-INFRA-PERF-001/code/__pycache__/prepare_assets.cpython-314.pyc` | Technically regenerable but inside a historical certification directory; conservatively preserve the archive intact |

**External dependencies, B:** the existing Linux-native RF under `/home/jaswin/.local/share/statsgeeks/frozen_rf/`, the approved WSL runtime image and source wheels referenced by the runtime locks, and approved interpreter installations outside this repository. They were not resized or modified. A Git commit without these artifacts or verified retrieval instructions is not a complete reproducibility backup.

### C — the complete genuinely disposable candidate list

| Exact path | Bytes | Why C |
|---|---:|---|
| `nul` | 0 | Untracked, empty accidental Windows-reserved-name file; no content to preserve and absent from the inspected protected/historical inventories |
| `working/__pycache__/member3_artifact_helpers.cpython-314.pyc` | 14,375 | Regenerable bytecode; its project `.py` source is present and protected; not in the inspected bound inventories |
| `working/__pycache__/minimal_standard_scaler.cpython-311.pyc` | 2,527 | Regenerable interpreter-specific cache; source is present/protected; not a model/scaler artifact |
| `working/__pycache__/minimal_standard_scaler.cpython-314.pyc` | 2,581 | Same reasoning, distinct Python version |

**Total: 19,483 bytes. Nothing was removed.** Do not remove `working/__pycache__/` wholesale: it also contains a OneNote file classified D. Do not expand this list to all `.pyc` files, the virtual environment, or any experiment directory. Recheck bindings immediately before any separately authorized future removal.

### D — the complete human-review classes and reasons

| Exact file or exhaustive path rule | Why human review is required / preserve-first disposition |
|---|---|
| Every `Open Notebook.onetoc2` anywhere in the project tree outside `.git/` and `.venv_baseline/` | User/tool-owned OneNote metadata, not proven empty placeholders. Multiple files are already tracked; some are explicitly protected or inventoried. Deleting or normalizing them caused prior integrity-gate issues. Future Git publishing treatment needs owner approval, but local preservation is mandatory now |
| `docs/WhatsApp Image 2026-09-07 at 14.51.21.jpeg` | Tracked participant/team reference image, 42,240 bytes. Ownership, consent/privacy and continuing presentation relevance must be reviewed; not classed as garbage merely because of its name |
| Any future/unrecognized path not matched by the rules above | Importance not established; do not auto-delete or auto-stage. No additional unexplained non-environment payload family was found in this inventory |

The OneNote rule explicitly includes root `Open Notebook.onetoc2`; the files in `data/`, `data/preprocessed/`, `docs/`, `models/`, `original/`, `presentation/`, `submission/`, `working/`, both baseline directories, both discovered `__pycache__/` directories, and **all** nested G4 run/checkpoint/code/evidence/result directories. The same explanation applies to each member of this set. In particular, `original/Open Notebook.onetoc2`, `working/baseline_artifacts/Open Notebook.onetoc2`, and `working/member3_baseline_frozen/Open Notebook.onetoc2` occur in the 33-path protected registry. The accepted CERT-004 exception was specific historical evidence, not a general metadata-deletion permission.

## 6. Special preservation decisions

### E3-002 — no changes, no cleanup

| Subdirectory | Bytes | Treatment |
|---|---:|---|
| `candidate_state/` | 14,018 | B: freshly learned source state and local metadata |
| `checkpoint/` | 1,306,622 | Mixed: A named contracts/manifests/preserved reports; B remaining generated material; D OneNote |
| `coordinator/` | 99,877 | A source/runtime bindings; D OneNote |
| `evidence/` | 10,502,325 | B raw 60-worker/probe/transport evidence |
| `hashes/` | 913,178 | B complete protected-state audit payloads; retain all |
| `predictions/` | 8,329,308 | B all 60 prediction archives |
| `results/` | 364,062 | A compact results/summary; B execution log; D OneNote |
| `validation/` | 116,144 | A named validation/failure/lifecycle records; B raw log; D OneNote |

The prevalidation `artifact_hash_manifest.json` and final manifest are **different reporting phases**, not duplicate manifests to consolidate. The final report documents the preserved prevalidation report path. Retain both manifests, both historical report snapshots, the final report, and `report_lifecycle.json`. Keep the failed unchanged validator and the successful serialization audit together; do not cherry-pick the PASS evidence.

### Baseline directories are not substitutes

- `baseline_artifacts/` contains the recovered RF/prediction/OOF payloads, schema and recovery evidence.
- `member3_baseline_frozen/` contains five compact JSON files recording recovered notebook scores, hashes, environment and the limitations of that earlier freeze.
- `metadata.json` describes its historical stage, including objects unavailable after that kernel shutdown; the later recovery does not make that file obsolete or a license to overwrite it.

### Reference notebooks

Read-only comparisons found:

- `original/4-Modelling.ipynb` and `working/4-Modelling_member3_reference.ipynb` are byte-identical, SHA256 `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae`.
- Both member2 source/executed notebooks have identical cell types/source, but different bytes and execution output.
- Both member3 source/executed notebooks likewise have identical cell types/source, but different bytes and execution output.

This supports keeping source notebooks in A and executed artifacts in B. It does **not** support deleting required paths, removing stored outputs in-place, or treating the original notebook as a safe target for future edits.

### Models, presentation and submission

Each currently contains only `Open Notebook.onetoc2`. Preserve the directories and metadata pending owner review. Their names do not prove that deliverables have been assembled. Future human-authored slide decks, abstracts, submission code and documentation should normally be A; large model/data bundles should be B with a release/artifact-store pointer. No future file is claimed to exist today.

## 7. Proposed commit to main — after separate approval

Stage only an explicit reviewed list, in small commits, after preservation and exact-byte policies are agreed:

1. **Project documents:** the seven modified Markdown documents; five untracked `docs/member3_baseline_discrepancy_audit.md`, `member3_modelling_readiness.md`, `member4_evidence_inventory.md`, `member4_phase1_judging_pack.md`, `member4_presentation_outline.md`; this report. Retain already-tracked project instructions, organiser notebooks and supplied rubric.
2. **Reference source:** the two unexecuted working notebooks, all current root `working/*.py`, `working/member2_baseline_handoff.md`, and root methodology/audit Markdown. Preserve protected bytes exactly.
3. **Compact baseline/protocol records:** the three named `baseline_artifacts/*.json`, all five `member3_baseline_frozen/*.json`, episode manifest, runtime locks and selected compact root validation/provenance JSON per section 5.
4. **Historical reproducibility record:** run-local Python source/test snapshots, reports, manifests, contracts and selected result/validation JSON specifically designated A. Preserve run identities and failed-attempt reports. Committing only the newest coordinator loses the historical code/hash relationship.
5. **Repository policy:** a reviewed `.gitignore` revision and an explicit future byte-preservation/line-ending policy. Neither was changed here.

This is a proposed set, not a ready-to-run staging command. Source snapshots contain machine/run-bound paths; inspect before publication. Original data and generated runs need an external backup plan even if a small Git evidence index is committed. No merge with `member2-baseline` is proposed at this stage.

## 8. Proposed keep-local / no-Git set

- `.venv_baseline/`, Git internals and external WSL runtime/model caches.
- Raw Parquets, accepted preprocessing pickle, exact RF and baseline prediction/OOF/trial NPZs.
- Both executed member2/member3 reference notebooks, with their current protected hashes.
- Complete G4 archives locally, excluding only the selected A files from the **Git exclusion**, not from the local archive.
- All episode predictions, worker packets, lifecycle details, source/adaptation outputs, failure inputs, forensic dumps, logs and metadata snapshots.
- Repair-version backups `*.pre_completion` and `*.pre_dependency_repair`.
- OneNote metadata and the participant image pending human publishing review; do not untrack existing files during this audit.

Use a verified backup/artifact store, not “only this laptop,” for B scientific evidence. Record relative paths, original sizes, SHA256 values, access controls and retrieval instructions. Do not alter payload bytes or move the active archives as part of this proposal.

## 9. `.gitignore` review and proposed revision

### Current file

```gitignore
# Large datasets
data/*.parquet

# Generated files
data/preprocessed/
*.pkl

# Python
__pycache__/
.ipynb_checkpoints/
.venv/
```

Gaps: no root rule for `.venv_baseline/`; no project-level exclusion for bulk G4 packets/predictions/logs; no explicit executed-reference-notebook rule; no metadata policy. Conversely, ignoring all of `working/`, all JSON, all Markdown, all notebooks, or all of `models/`/`presentation/`/`submission/` would hide important A material. Retain the large-model/pickle rule while version-controlling schema/hash/retrieval documentation.

### Proposed policy text — NOT applied

This conservative allowlist preserves reviewable source/reports/manifests while excluding generated runs by default. Paths not explicitly re-included remain local. Additional A JSON may be added only by reviewed literal path; do not force-add whole archives.

```gitignore
# Python environments and regenerable caches
/.venv/
/.venv_baseline/
/venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Large immutable data/model payloads: retain outside ordinary Git
/data/*.parquet
/data/preprocessed/**
*.pkl
*.pickle
*.joblib
*.npz
*.npy

# Protected executed notebooks: preserve exact local/archive originals
/working/3-Preprocessing_member2_baseline_executed.ipynb
/working/4-Modelling_member3_reference_executed.ipynb

# Raw execution/diagnostic output
/working/**/*.log
/working/**/*.stderr
/working/*.pre_completion
/working/*.pre_dependency_repair
/working/gate4_approved_runtime_validation.json
/working/gate4_autonomous_sampler_001.json
/working/gate4_teardown_sampler_002.json
/working/gate4_isolation_sampler_reverification.json

# Historical G4 archive payloads default to local-only.
# Re-open directories so exact source/document exceptions can be traversed.
/working/G4*/**
!/working/G4*/**/
!/working/G4*/**/*.py
!/working/G4*/**/*.md
!/working/G4*/**/artifact_hash_manifest.json
!/working/G4*/**/changes.patch
!/working/G4*/**/NON_SCIENTIFIC_RUNTIME_ONLY.txt
!/working/G4*/**/entry.json
!/working/G4*/**/environment_manifest.json
!/working/G4*/**/certification.json
!/working/G4*/**/summary.json
!/working/G4*/**/independent_verification.json
!/working/G4*/**/final_audit.json
!/working/G4*/**/validation_summary.json
!/working/G4*/checkpoint/contract.json
!/working/G4*/checkpoint/execution_authorization.json
!/working/G4*/checkpoint/infrastructure_preparation.json
!/working/G4*/checkpoint/validation_binding.json
!/working/G4*/checkpoint/episode_manifest.json
!/working/G4*/checkpoint/file_fingerprints.json
!/working/G4*/checkpoint/checkpoint.json
!/working/G4*/checkpoint/metadata_exception_policy.json
!/working/G4*/coordinator/native_cache.json
!/working/G4*/results/execution_summary.json
!/working/G4*/results/per_episode_results.json
!/working/G4*/results/independent_verification_v2.json
!/working/G4C-PROVENANCE-CHECKPOINT-002/file_fingerprints.json
!/working/G4C-PROVENANCE-CHECKPOINT-002/checkpoint.json
!/working/G4C-PROVENANCE-CHECKPOINT-002/metadata_exception_policy.json

# E3-002 final reporting/validation context, no payload rewriting
!/working/G4C-E3-002/final_artifact_hash_manifest.json
!/working/G4C-E3-002/final_artifact_hash_manifest.sha256
!/working/G4C-E3-002/validation/INDEPENDENT_VALIDATION_FAILURE.json
!/working/G4C-E3-002/validation/git_discrepancy_diagnostics.json
!/working/G4C-E3-002/validation/report_lifecycle.json
!/working/G4C-E3-002/validation/serialization_validation.json
!/working/G4C-E3-002/checkpoint/data_host_preflight.json
!/working/G4C-E3-002/checkpoint/runtime_preflight_native.json

# Machine/user metadata: no implied deletion or untracking approval
*.onetoc2
.DS_Store
Thumbs.db
/nul

# Keep cache contents ignored even inside re-opened archive directories
__pycache__/
*.py[cod]

# Local credentials/configuration, if introduced later
.env
.env.*
!.env.example
```

**Important limitations:** this is proposed text, not a tested/applied policy. Validate it with read-only ignore queries against representative A/B paths before a separately authorized edit/staging operation. Existing tracked `.onetoc2` files and the participant image remain tracked regardless of new ignore patterns. No `git rm --cached` or history rewrite is authorized. The baseline JSON records are intentionally not blanket-ignored. A final model required for submission can be distributed as an external release/artifact with its exact hash; ignoring `.pkl` is not permission to omit the model from the delivered bundle.

## 10. Conflicts, gaps and decisions needed before canonical main

1. **Stale master-plan status:** `docs/MASTER_PLAN.md` still says Notebook 4 has not run and candidate implementation is unapproved, while dated experiment evidence exists through E3-002. Preserve the plan as A; later update its current-status section and decision links with explicit authorization history. Do not erase older stages.
2. **Stale global final/stop report:** `working/G4C-FINAL-REPORT.md` and `working/STOP_REASON.md` describe a specific earlier preflight with E2/E3 NOT_RUN. They remain A historical evidence, but cannot serve as today's global status. A new current index is preferable to rewriting them.
3. **Git does not replace scientific preservation:** the plan requires saved models/scalers/predictions and backups. Keeping generated binaries out of Git is compatible only if their exact artifacts and retrieval instructions are preserved elsewhere.
4. **Notebook duplication versus provenance:** deduplicating Notebook 4, clearing original outputs, removing executed copies or replacing preprocessing would violate required paths and protected hashes. No such optimization is proposed.
5. **OneNote metadata versus clean Git:** metadata is already tracked and sometimes explicitly protected. Ignoring it later will not produce a clean index or resolve an old integrity exception. Any ownership/untracking policy must be separately authorized and preserve the bytes.
6. **Line endings and protected content:** this Windows Git warns of LF-to-CRLF transformations. E3-002's preserved diagnostics show Windows `core.autocrlf=true`, no corresponding Linux setting, Linux dirty status for three original notebooks, and no Linux diff when end-of-line whitespace is ignored. Do not run normalization, `git add --renormalize`, or rewrite `.gitattributes` now. A later policy must preserve protected source/notebook bytes and distinguish Git's clean-tree interpretation from content hashes. Do not assert this audit resolves E3 validation.
7. **Canonical code selection:** root `working/` scripts and run-local certified versions are not all the same generation. Preserve them as A historical source; identify approved entrypoints and runtime bindings before exposing any as canonical runnable commands. Do not merge code by filename or delete older verifier versions.
8. **Final deliverables are missing from their named directories:** the plan requires models, slides, justification and runnable submission material, but `models/`, `presentation/`, `submission/` contain metadata only. Documentation under `docs/member4_*` is preparatory evidence, not a completed submission.
9. **Branch state is local only:** all inspected refs point at the initial commit. No remote refresh or member2 comparison/merge happened. Capture reviewed current work before any later branch operation; do not assume a branch switch will organize untracked changes.
10. **No negative-result cleanup:** E1/E2/E3 reports, failed infrastructure attempts, incomplete E3-001 and E3-002's failed independent validation must all remain available. Neither failed status nor large size establishes disposability.

## 11. Recommended next step

**Approve an immutable, checksum-verified backup of all B scientific artifacts and the current A/D working files first**, including the external native RF and runtime dependencies. Then separately review the explicit A staging list, exact-byte/line-ending policy, and proposed ignore rules. Only after those decisions should an authorized, selective preservation commit to `main` be considered.

Resolve E3-002's independent-validation Git-view discrepancy in a separate authorized task, without rerunning episodes or editing protected evidence. Defer any member2-baseline comparison/merge until the preservation checkpoint and actual branch provenance are established.

**No deletion is needed to prepare a scientifically defensible main branch.** The C list saves less than 20 KB; the priority is preserving and documenting the uncommitted work, not reclaiming space.
