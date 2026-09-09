# G4A-PRODUCTION-001 — BLOCKED at normal teardown

## Decision

**Gate 4A BLOCKED. No passing episode manifest created or frozen. E1–E5 not executed.**
The current Team Lead authorization permits the fixed candidate sequence only after
all gates pass. Execution stopped at the first failing sequential-suite teardown
check. Candidate parameters, labels, sampler and baseline were not changed.

## Completed checks

- Entry: all 33 protected hashes match; original/ has empty Git status and diff.
- Fresh independent runtime reconstruction: all 4,355 files and all six wheels
  match the existing approved lock; no downloads, installs or host fallback.
- Approved numerical sandbox: Python 3.14.4, NumPy 2.4.6, SciPy 1.17.1,
  scikit-learn 1.9.0, Narwhals 2.25.0, joblib 1.5.3, threadpoolctl 3.6.0.
  Required RF/CV imports and a small linear solve passed in real-packet probes.
- Host remains Python 3.11.9. Jupyter/nbconvert are host-only: the inspected
  transport/probe components are Python programs and import neither package.
  Their absence from the sandbox is no longer a blocker under current approval.
- The unchanged protected sampler ran in a fresh Windows process. All 60
  support/query row and pixel fingerprints, exact before/after RNG states, class
  balance, ordering, budgets, disjointness, seed, schema and sampler source hash
  match the previously retained records exactly. Its BLOCKED wrapper status is
  the intentional historical shared-runtime isolation warning, not a sampler failure.
- A real first-episode packet was built from the accepted input and sent to the
  staged numerical sandbox. Only Madrid X/y and the current Amsterdam support
  X/y/IDs, query X/IDs and fixed probe parameters were supplied. A second-episode
  packet was prepared evaluator-side but the sequential suite stopped before
  executing it. Neither packet contains query labels or other episodes' labels.

## Production boundary implemented (not certified for candidate use)

New Linux supervisor: `working/gate4_production_boundary.py`.

- Fresh Bubblewrap user/PID/network/IPC namespaces, disabled nested user namespaces,
  dropped capabilities, cleared environment, read-only pinned runtime root.
- Only sealed anonymous-memory code bytes mounted in a private read-only `/app`;
  no project directory, label artifact, evaluator manifest, home or host package mount.
- One JSON packet on a pipe; no pickle, Python object sharing, label RPC or scoring
  feedback. Source and support labels are allowed, not described as label-free.
- Private tmpfs and bounded streamed stdout/stderr; process-specific wall/CPU/address
  space/file-size/descriptor limits. No unrelated user process was terminated.
- Strict prediction-only sanitizer implemented, with ordered query fingerprint and
  exact class/count/type checks. Full negative-output test matrix was NOT reached.
- Test code checks import-time paths/environment/descriptors, named globals/module/
  GC references, built-in-only transport, numerical imports, private temp/shared-
  memory sentinels, read-only runtime and user-keyring non-recovery.
- Probe writes only current allowed support labels into disposable sandbox state
  to test persistence. Its constant integer status output is not a classifier and
  was not scored. No candidate source statistics or transforms were fitted.

These checks passed in `probe_normal_attempt5.json` and inside the subsequent
suite's first worker. They are bounded empirical/access-control checks, not proof
against arbitrary kernel exploits. Cross-episode and abnormal-state guarantees
remain unverified because the sequential suite stopped at its first teardown.

## Exact failure / preserved evidence

`working/G4A-PRODUCTION-001/suite_001/probe_1.json` reports:

```text
worker returncode: 0
stderr: empty
elapsed: 12.066675126999996 seconds
recorded PID namespace: pid:[4026532231]
initial namespace member: 432
observed namespace survivors after launcher wait: [432, 434]
teardown_pass: false
status: BLOCKED
```

The worker deliberately forked a detached child using `setsid()` before returning.
The supervisor's immediate post-wait namespace scan did not establish an empty
namespace. This fails the required teardown certification even though an earlier
individual launch had an empty scan. No second suite episode, controlled-interrupt
case, post-abnormal freshness case or negative-output matrix ran after this failure.

A later **read-only** namespace scan found no matching processes. It did not capture
the failed scan's process states and cannot distinguish transient zombie reaping
from briefly live descendants. PID/namespace IDs may also be reused. Therefore:

- Do NOT claim that label-bearing live memory definitely survived.
- Do NOT claim that the failed teardown was safe merely because a later scan is empty.
- Do NOT convert this attempt to PASS or erase it.

The missing evidence is contemporaneous process state/start identity, namespace
lifetime, bounded reaping completion and fresh-state success after normal/abnormal
termination. The supervisor needs that engineering repair and a new complete
certification run before candidate execution can resume.

## Earlier setup repairs, not scientific deviations

All failed attempts remain under this run directory:

1. Bubblewrap could not create `/app/entry.py` on the read-only image. Fixed by a
   private `/app` tmpfs, sealed code bind, then read-only remount; runtime unchanged.
2. Environment allowlist omitted Bubblewrap's generated `PWD=/tmp`. Diagnostic
   retry identified it; exact `/tmp` is now checked. No host environment inherited.
3. Descriptor probe ran after importing ctypes, which opened pinned `libffi.so.8`.
   Moved ctypes import after the inherited-descriptor check, retaining the strict
   initial pipe-only FD check. This was not an evaluator descriptor/label leak.
4. The latest user preprocessing-hash text differs from the prior accepted and
   repository record. As instructed, existing repository specifications were used:
   `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`.
   All 33 recorded hashes agree. No file or accepted hash record was corrected.

## Required result status

| Item | Result |
|---|---|
| Gate 4A | BLOCKED |
| Manifest | Not created; `working/gate4_episode_manifest.json` absent; SHA256 N/A |
| Production isolation certification | FAIL / incomplete at teardown |
| Label-access audit | No forbidden target labels supplied or observed; full cross-episode certification incomplete |
| Fresh state | Within-worker checks passed; sequential/cross-episode and post-abnormal tests not completed |
| Normal teardown | FAIL certification: nonempty immediate namespace scan |
| Abnormal teardown | Not run |
| Prediction finalisation | Positive output validated in individual probe; full rejection matrix not run |
| 60-episode replay | PASS, exact prior-record agreement |
| Matched comparators | Sampler identity-routing PASS; no production comparator models run |
| E1 | Not executed; primary score/SD/P0/RF/U0/paired gain all N/A; hypothesis not evaluated |
| E2–E5 | Not executed |
| Best fixed candidate | None established |
| Accepted baseline | Unchanged |
| Notebook 4 rerun | No |
| original/ / protected files | Final checks recorded in `final_checkpoint.json` |

The Amsterdam benchmark remains development/reference-comparison data, NOT
untouched final-audit labels. No performance, causal or source-label benefit claim
is made. No selection, tuning, additional draws or new model was introduced.

## Runtime anchors

Runtime lock SHA256:
`cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514`

Runtime tree SHA256:
`b4e8c3f09000fd6764d8491ca963b8a3a246545e8a4a6244270db44a2d51b19f`

Narwhals wheel `narwhals-2.25.0-py3-none-any.whl` SHA256:
`1f0f403e8c7e4463cde9bfe78b12fdd809e3ae3dda6d9b2f802934fb9c7a6a8f`

Exact six wheel hashes, baseline hashes, final code hashes and every run artifact's
hash/size are retained in `final_checkpoint.json` and `artifact_hash_manifest.json`.
Neither JSON is a passing episode manifest.

## Files changed / safe next action

Created four infrastructure/probe scripts under working/, a fresh runtime rebuild
report, fresh sampler report and this uniquely named run directory with packets,
entry/attempt/failure evidence and final audit. Modified the independent runtime
verifier only to support an exclusive new output path; updated readiness pointer.
No commits, deletions of evidence, dependency installations, reference writes or
OneNote protection changes. Exact suite code is preserved in `code_at_stop/`.
After the stop, the working boundary was restricted to the pinned infrastructure
probe hash: arbitrary candidate code is rejected while Gate 4A remains blocked.

**Next safe action after review of this stop:** repair the Linux supervisor's
teardown observation/reaping mechanism using bounded waits and contemporaneous
process identity/state evidence; do not kill unrelated processes. Repeat normal,
detached-child, controlled abnormal, post-abnormal, cross-episode and output-boundary
certification in a new run. Recheck protected/runtime/sampler identities. Only after
all gates pass may the evaluator-only manifest be frozen and the conditionally
authorized fixed E1 sequence begin. Existing run evidence must remain unchanged.
