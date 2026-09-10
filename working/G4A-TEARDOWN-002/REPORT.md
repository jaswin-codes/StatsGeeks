# Gate 4A teardown repair and recertification — PASS

Run ID: **G4A-TEARDOWN-002**. Scope: infrastructure only. **No candidate modelling,
E1–E5, optimisation, scoring or Notebook 4 execution.** Stop for explicit Gate 4B/E1
authorization. Existing candidate-code guard remains probe-only.

## Diagnosis: what is proven, and the historical limit

The failed prior run captured namespace members 432/434 but no process state or
start-time identities. Their exact historical live/zombie states cannot now be
recovered, and PID reuse makes inspection of those numbers today invalid evidence.
The later empty scan was NOT used to declare the old attempt passing.

Three new observational reproductions captured the actual lifecycle race:

- Bubblewrap outer launcher becomes **Z (zombie)** after reporting worker success.
- Namespace init remains **S (sleeping)** and is reparented to WSL's supervisor.
- Detached episode child remains briefly **R (running)** during kernel namespace
  termination. Thus assuming that every remaining PID is already a zombie is unsafe.
- Waiting for the outer launcher alone is not a join/reap of the complete episode tree.

In the repaired certification, orphaned namespace init is adopted by the dedicated
runner. Its **Z** state, parent PID, original start ticks and namespace identity history
are recorded contemporaneously, followed by a successful `waitpid` and disappearance.
Normal worker return code is 0; the adopted namespace init's recorded termination
status is SIGKILL (-9), consistent with the observed Bubblewrap namespace shutdown.
No historical attempt was overwritten or retrospectively relabelled PASS.

Evidence: `lifecycle_diagnostic_1.json` through `_3.json`, and full timestamped
`lifecycle.events` in each certified `probe_*.json`.

## Exact lifecycle correction and boundedness

New `working/gate4_lifecycle.py`:

1. Require a dedicated supervisor with no pre-existing children.
2. Set Linux `PR_SET_CHILD_SUBREAPER` on that supervisor only; remember prior setting.
3. Track episode descendants using PID **and process start ticks**, ancestry and
   private PID namespace. Retain tracked processes after reparenting and namespace-
   link loss. **Zombies are not filtered or counted as clean.**
4. Record PID, PPID, state, command, process group/session, namespace PID chain,
   start ticks, exit status field, wall/monotonic timestamps, lifecycle transitions
   and launcher wait completion.
5. Following launcher exit, use **targeted nonblocking `waitpid`** only on tracked
   adopted children. `waitpid` itself verifies actual child ownership. Retain wait
   status/exit code evidence and verify no episode identities remain in `/proc`.
6. Poll the termination/reaping condition to a fixed **5-second deadline**. An empty
   tracked set and empty dedicated-supervisor child list are required. This is not
   an arbitrary sleep followed by presumed success. Failure raises and blocks output.
7. Restore the prior subreaper setting only after successful cleanup. Cleanup also
   executes on transport exceptions via `finally`.

No new broad killing was introduced. The existing controlled-abnormal path signals
only the runner-created launcher process group; kernel PID-namespace teardown kills
its detached descendants. The lifecycle addition itself sends **no signals**.
No OneNote, OneDrive or unrelated process was stopped. No dependency changed.

`finalize()` now rejects output from unsuccessful, interrupted or unreaped workers
before the prediction barrier. Candidate code remains restricted to the pinned
infrastructure probe; no production model was enabled by this certificate.

## Recertification results

Final evidence sets:

- `certification_v2/suite_001/`
- `independent_repeat/suite_001/` — separate fresh Linux verifier process

Each executes seven real-packet infrastructure probes: normal episode N, normal
N+1, controlled abnormal N with a ready marker after state creation/fork, fresh N+1
after abnormal cleanup, and three identical-packet comparator-role transports.
The last three roles are **routing probes**, not implementations or scores of raw
prototypes, RF or E1. All output integers are constant test status codes.

| Requirement | Result |
|---|---|
| Approved runtime integrity | PASS; independent 4,355-file reconstruction and all six wheel hashes |
| Real-episode numerical boundary | PASS; required imports, pinned module locations, small numerical solve |
| Query-label isolation | PASS within the documented trusted-host/kernel boundary; only source/current support labels transported |
| Cross-episode isolation | PASS; two distinct real packets, no previous memory/tmpfs/shared-state or keyring recovery |
| Fresh adaptation state | PASS, including the episode immediately following abnormal termination |
| Prediction finalisation | PASS; successful exit + complete reaping required; 16 negative input/output/barrier checks rejected |
| Normal teardown | PASS in 12 final real-packet probes, including detached children |
| Abnormal teardown | PASS twice; ready marker confirms state and detached child existed before controlled interruption |
| Reaping evidence | 14 adopted namespace-init zombies explicitly reaped; no final live/zombie attributable process |
| Sixty identities and RNG replay | PASS; exact prior-record agreement and independent reconstruction/replay of all 60 |
| Matched comparator routing | PASS; three named roles receive identical packet hashes/query order; no comparator model executed |
| Protected baseline files | 33/33 unchanged; independently checked before/after stages and manifest freeze |
| original/ | Git status/diff empty; original OneNote read-only flag remains set |
| Candidate modelling / Notebook 4 rerun | NO / NO |

A recertification-harness strengthening extends the keyring test's expiry from 15
to **300 seconds**. Fifteen seconds could expire during the next worker's numerical
startup and conceal persistence. The independent verifier checks recorded inter-
episode bounds remain below 300 seconds. No scientific/label-budget change occurred;
only current permitted support labels enter disposable sandbox test state. The prior
probe/code versions and initial passing suites remain preserved as intermediate evidence.

## Runtime and label-access boundary

Sandbox: Python **3.14.4**, NumPy **2.4.6**, SciPy **1.17.1**, scikit-learn **1.9.0**,
Narwhals **2.25.0**, joblib **1.5.3**, threadpoolctl **3.6.0**. One BLAS/OpenMP thread.
Host verifier remains Windows Python **3.11.9**; notebook tooling is host-only.
No downloads, installations, version substitutions or global-package fallback.

Runtime lock SHA256:
`cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514`

Runtime tree SHA256:
`b4e8c3f09000fd6764d8491ca963b8a3a246545e8a4a6244270db44a2d51b19f`

The privileged sampler/evaluator may hold full target labels, but serialized packets
were independently compared against Madrid source arrays and exactly the selected
current-episode supports. No full-target/query/other-episode labels leave that
boundary. Workers see a read-only pinned runtime, sealed probe code, private temporary
storage and one plain JSON packet; no project/evaluator/manifest mounts, inherited
label descriptors, label requests or scoring feedback. Query labels were not used
for scoring here because this task calculated no predictions from a model or scores.

Trust scope: audited unprivileged worker code under the approved Bubblewrap/WSL/Linux
boundary with trusted host controller/kernel. This is not a claim against malicious
host administration or kernel exploits. Future candidate bytes/source-state must be
separately approved and pinned; certificate does not authorize arbitrary code or
changes to mounts, runtime, packet contract or lifecycle. Source folds/model statistics
were not fit. Amsterdam remains development/reference-comparison data, not untouched
final-audit labels.

## Frozen manifest

Path: **`working/gate4_episode_manifest.json`**

SHA256:
**`9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`**

- Created only after required runtime, sampler, production, isolation and teardown
  evidence checks passed, with exclusive-create semantics.
- Contains exact 60 episode IDs, budgets/trials, ordered support row/pixel IDs,
  support/query and feature fingerprints, full before/after RNG records, sampler,
  schema/input fingerprints, code/runtime/evidence provenance and protected hashes.
- **Evaluator-only.** Full ordered support lists implicitly encode labels across
  episodes even without explicit label fields. This manifest must NEVER be mounted,
  transported or made available to a candidate. Workers receive only one packet.
- No query labels, query class counts or explicit support-label arrays are included.
- Independent verifier does not import builder/sampler/runner code. It reconstructs
  all draws using precomputed class pools and PCG64(42), replays each episode state,
  checks exact ordered fingerprints and revalidates contemporaneous reaping evidence.
- Independent pre-freeze check PASS, Windows `attrib +R`, then a separate fresh-process
  read/reconstruction/hash/read-only verification PASS. See
  `manifest_independent_verification.json` and `manifest_frozen_verification.json`.
- Read-only is the approved practical freeze mechanism, not an unchangeable filesystem
  guarantee against the owner. Future runs must verify the recorded SHA256 before use.
- `working/gate4_episode_manifest_validation.json` remains unchanged historical
  **BLOCKED evidence**, not the passing manifest.

## Files created/modified and next action

Created root-level working files:
- `gate4_lifecycle.py`
- `diagnose_gate4_teardown.py`
- `certify_gate4_manifest.py`
- `independently_verify_gate4_manifest.py`
- `gate4_teardown_runtime_rebuild_002.json`
- `gate4_teardown_sampler_002.json`
- `gate4_episode_manifest.json`

Modified:
- `working/gate4_production_boundary.py` — observation, bounded targeted reaping, finalisation barrier
- `working/gate4_production_probe.py` — longer keyring canary lifetime only
- `working/verify_gate4_production_suite.py` — recertification/output-barrier/routing evidence
- `working/gate4_readiness_audit.md` — latest-status pointer
- `working/gate4_episode_verification.md` — latest-status pointer

Created this run directory with entry snapshot, pre-repair/code snapshots, three
diagnostics, intermediate/final/independent suites, pre-manifest gate validation,
independent/frozen manifest validations, report, final checkpoint and artifact inventory.
**Every individual created/modified file and hash is listed in
`artifact_hash_manifest.json`** (the inventory excludes its own hash; its digest is
reported separately). No reference file, prior failed run artifact or runtime lock
was overwritten. No Git commit or protection removal.

**Remaining Gate 4A blocker: none.** Historical PID432/434 states remain unknowable,
but current certification has contemporaneous state/reaping evidence and does not
rely on that missing historical evidence.

**Exact next action: STOP for explicit Gate 4B/E1 authorization.** Do not execute E1
or any other candidate automatically. Preserve manifest/runtime/protected hashes and
apply the same isolated one-episode boundary to any subsequently approved code.
