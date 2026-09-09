# Gate 4A approved Narwhals repair — BLOCKED

## Outcome

The exact newly approved Narwhals wheel was hash-verified before staging and added
ONLY to a separate copy of the existing isolated runtime. No other package was
installed/downloaded, no host fallback was used, and v3 and its lock remain unchanged.
Gate 4A is **BLOCKED**; Gate 4B is **NOT READY / NOT AUTHORIZED**.

## Runtime evidence

Two fresh Bubblewrap runs imported the six staged distributions from `/numeric`:

| Component | Isolated version |
|---|---|
| Python | 3.14.4 (existing interpreter, unchanged) |
| NumPy | 2.4.6 |
| SciPy | 1.17.1 |
| scikit-learn | 1.9.0 |
| joblib | 1.5.3 |
| threadpoolctl | 3.6.0 |
| Narwhals | 2.25.0 |

`RandomForestClassifier` and `RepeatedStratifiedKFold`: **PASS**, both runs.
No estimator was instantiated, fitted, or used for inference.
Jupyter, jupyter_core, nbconvert, nbclient: **ABSENT inside isolation**.

The approved Windows route separately reports Python 3.11.9, NumPy 2.4.6,
SciPy 1.17.1, scikit-learn 1.9.0, Narwhals 2.25.0, jupyter_core 5.9.1,
nbconvert 7.17.1, nbclient 0.11.0. These host versions are NOT sandbox evidence
and were not used as a fallback.

Wheel: `narwhals-2.25.0-py3-none-any.whl`  
SHA256: `1f0f403e8c7e4463cde9bfe78b12fdd809e3ae3dda6d9b2f802934fb9c7a6a8f`

The wheel was independently hashed again with Windows Python. An independent
WSL verifier reconstructed the entire 4,355-file runtime from six exact wheels,
existing stdlib/interpreter and recorded native sources. It matched the new lock
exactly, checked the six-distribution inventory and verified that all reported
native mappings belong to the lock. Temporary reconstruction storage was removed.
This is runtime provenance verification, NOT production label-isolation certification.

New image: `/home/jaswin/.local/share/gate4a/runtime_v4_narwhals/image`  
Files/directories staged read-only; no production launcher switch made.  
Lock: `working/gate4_runtime_narwhals_lock.json`  
Lock SHA256: `cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514`  
Tree SHA256: `b4e8c3f09000fd6764d8491ca963b8a3a246545e8a4a6244270db44a2d51b19f`

## Required gate status

| Requirement | Status |
|---|---|
| Real-episode transport/isolation | NOT RUN |
| Query-label isolation | NOT RUN in production |
| Cross-episode isolation | NOT RUN in production |
| Fresh adaptation state | NOT RUN in production |
| Prediction finalisation | NOT RUN in production |
| Normal teardown | NOT RUN as production certification; smoke processes returned normally |
| Abnormal teardown | NOT RUN |
| 60-episode identities/RNG | Prior PASS retained; no new replay after dependency stop |
| Matched comparator routing | Prior sampler four-consumer routing PASS retained; production NOT RUN |
| Manifest | NOT CREATED; `working/gate4_episode_manifest.json` remains absent; no hash/freeze |
| Candidate modelling / E1 | NO |
| Notebook 4 rerun | NO |
| Protected files | All 33 hashes match at entry and after runtime staging |
| original/ | Empty Git status and diff; OneNote retains `A R` |

All historical episode records, protected artifacts and accepted baseline scores
are unchanged. No target data was loaded or transported during this repair.
Future raw prototypes, frozen RF and candidates still require identical ordered
queries/supports per budget/trial, with paired deltas; full-target zero-shot must
not be treated as a same-query comparator. Candidate execution stays fail-closed.

## Exact remaining decision and next action

Section 10 requests Jupyter/nbconvert availability in the staged runtime, but the
existing locked image has neither. Section 8 permits adding only the approved
Narwhals wheel and requires stopping on another missing dependency. Installing
notebook tooling would require additional approved exact artifacts; mounting the
host would violate isolation. No such change was made.

Team Lead must clarify whether Jupyter/nbconvert are required only in the approved
Windows orchestration environment (where available), or approve an exact offline
sandbox tooling dependency set. Also explicitly confirm that the existing Linux
Python **3.14.4** is the intended isolated interpreter, distinct from the accepted
Windows reference **3.11.9**; neither interpreter was changed here.

After that decision, the next infrastructure task is production launcher/teardown
repair and real-episode isolation certification against the unchanged 60 records.
Only after every check passes may a manifest be created, independently verified,
hashed and frozen. E1 still requires a separate subsequent Team Lead authorization.

## Files created/modified by this task

Created:
- `working/stage_gate4_approved_narwhals.py`
- `working/verify_gate4_approved_runtime_tree.py`
- `working/gate4_runtime_narwhals_lock.json`
- `working/gate4_approved_runtime_validation.json`
- `working/gate4_approved_runtime_tree_validation.json`
- `working/gate4_approved_runtime_report.md`
- `working/gate4_approved_runtime_checkpoint.json` (final integrity/evidence inventory)

Modified: `working/gate4_readiness_audit.md` (latest-status pointer only).
External creation: `runtime_v4_narwhals/` image and exact wheel; original v3 untouched.
Existing unrelated dirty Git state was preserved. No passing evidence overwritten.
