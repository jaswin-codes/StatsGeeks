# Gate 4A isolation repair — BLOCKED

Date: 2026-09-08. Scope: isolation and sampler diagnostics only. No candidate model,
E1, fitting, inference, tuning, performance calculation, or Notebook 4 execution.

## Outcome

**Partial implementation, not an enforceable production deployment. STOP; no freeze.**

A diagnostic Bubblewrap boundary was implemented and tested under WSL2 Ubuntu.
The approved numerical workload cannot currently execute there: sandbox Python
cannot import NumPy (`ModuleNotFoundError`). No numerical environment or immutable
source-state mount has been provisioned/approved. Timeout descendant teardown and
resource containment are also unverified. The timeout handler must not be assumed
to kill the entire WSL sandbox merely because the Windows client exits. Output is
validated after collection, not bounded while streaming; this is another deployment
hardening requirement. These omissions prevent certification of a usable evaluator/
candidate execution boundary, even though the tested namespace/file checks pass.

`working/gate4_isolation.py::run_episode` **always raises BLOCKED**. Its separate
`run_isolation_probe` accepts only a fixed synthetic packet with negative dummy IDs.
No real support or query data were sent into any sandbox. Do not repurpose the probe
interface for models or remove the production stop guard.

## Mechanism implemented, and its limits

- Fresh Bubblewrap process with `--unshare-all --unshare-user --disable-userns`,
  dropped capabilities, new session, cleared environment, private PID/network/IPC
  namespaces, temporary root and `/tmp`, read-only `/usr`, isolated `/proc` and `/dev`.
- Only the label-free wrapper and synthetic probe source are mounted from the host.
  No project directory, preprocessing pickle, baseline artifacts, full manifest,
  home directory, prior worker directory, or evaluator object is mounted.
- One JSON packet on stdin; no shared Python objects, pickle, evaluator callback,
  label-request service, or score-feedback channel.
- After process completion, stdout bytes are parsed into an exact-length integer
  list with values 1–4, then copied into a tuple. Arbitrary object graphs, extra fields,
  booleans, extra rows and label requests are rejected. Test integers are status
  codes only, not predictions from a model.
- Source hashes are checked before launch, but a complete production solution also
  needs immutable staged code/runtime/source-state ownership, not just mutable-host
  file hashes checked before mounting. No all-episode ordered support IDs may be
  admitted as candidate code, source state or metadata: their class blocks reveal labels.

Runtime observed: Windows evaluator Python 3.11.9 / NumPy 2.4.6; WSL kernel
`6.18.33.2-microsoft-standard-WSL2`, Bubblewrap 0.11.1, sandbox Python 3.14.4,
**no NumPy**. No packages were installed, security policies relaxed, or baseline
files/ACLs changed. This is not a claim that WSL cannot support a complete solution;
it is a statement that this prototype has not established one.

## Negative-access and fresh-process evidence

`working/verify_gate4_isolation_repair.py` launched two independent Windows verifier
processes. Each launched two fresh sandboxes for state/access checks, four malformed
output probes and one numerical-runtime import probe. No candidate model was used.

| Check | Observed result | Certification limit |
|---|---|---|
| `y_amsterdam`, full labels, other/prior support labels, evaluator, adaptation state in globals/module dictionaries | No matching references | Synthetic probe, not deployed numerical worker |
| Hidden named references in GC-tracked dictionaries | No label-bearing references | Name-to-identical-string intern-table entries excluded; not exhaustive object-graph proof |
| Open known full-label pickle/NPZ, full diagnostic/manifest paths | Denied/not found; no bytes read | Only explicitly tested paths |
| Parent `/proc/1/root` route to host labels and host home | Denied/not found | No host evaluator object mounted |
| Previous `/tmp` sentinel | Absent in next worker | Normal successful exits only |
| Write into `/usr` | Rejected | Does not certify every possible kernel channel |
| Cross-worker Linux user-keyring sentinel | **Not recovered** | Explicit new user namespaces isolate the tested keyrings |
| Hidden-label object, label RPC request, extra output row, boolean output | All rejected | No actual scoring; resource limits/abnormal teardown pending |
| Numerical runtime import | **FAIL: NumPy unavailable** in both independent runs | Deployment blocked |

### Corrections retained for independent review

An early capability probe could access a user keyring. That alone did **not** prove
cross-episode persistence. Fresh-worker testing showed different keyrings and no
sentinel recovery; **there is no demonstrated keyring label leak**. Synthetic keys
in the final test have a 60-second expiry; no actual labels were written to keys.
An initial GC name-only test matched interned strings rather than labelled arrays;
the corrected test excludes only exact name-to-identical-string entries.
Initial launcher checks also caught the requirement for explicit `--unshare-user`
and Windows-path quoting; these were corrected before the recorded verification.
No failed attempt emitted a passing manifest, and no label-access convention was
substituted for OS isolation.

## Sampler and matched identities — PASS, unchanged

The existing `working/verify_gate4a_episodes.py` was **not edited**. It ran in a fresh
approved interpreter and its complete 60-episode diagnostic fingerprint list was
compared exactly with the previous Gate 4A evidence. All support/query row and pixel
ID fingerprints, ordering, budgets, trial numbering, before/after RNG states, seed,
PCG64 policy, schema and sampler source hash agree. Deterministic regeneration,
independent sampler agreement, RNG replay, support/query disjointness, matched
packets, and query-reordering/truncation rejection pass.

Raw prototypes, frozen RF saved predictions, and future E1 can be routed to identical
support/query identities under the verified packet contract. **This is feasibility
of identities, not successful deployment of three model adapters.** No model was run,
no RF was unpickled by this repair, and no score was calculated. A numerical worker
runtime is still needed for the agreed prototype/E1 implementation.

## Manifest and preservation

- `working/gate4_episode_manifest.json`: **not created**.
- Existing `working/gate4_episode_manifest_validation.json` and
  `working/gate4_episode_verification.md`: **preserved unchanged** as blocked evidence.
- New failure evidence: `working/gate4_isolation_repair_validation.json`, SHA256
  `a57077095aede63c5db7fdd0c21e1861b9175a4ec2c78f60827622dec3b2b4a3`.
- New sampler evidence: `working/gate4_isolation_sampler_reverification.json`, SHA256
  `f82fd3824c8a8906363c88e816198806c45c0b2ded0d0fd85cae656c6bb4e3bf`.
- Prior validation SHA256 still
  `4214973bee738306b6df4cacb9d3859398028dfcb42b8aee40692cc3be6979ca`.
- All **33** files in the prior protected hash map (32 protected reference/input
  files plus the accepted sampler verifier) match before and after this task.
  Includes raw Parquets, preprocessing pickle, original notebooks, RF and both
  frozen artifact directories. `original/` remains Git-clean.
- Existing dirty user work was neither reverted nor staged. No commit made.

Reproduction command (exclusive output creation; existing evidence is not overwritten):

```text
C:\Users\jaswi\AppData\Local\Programs\Python\Python311\python.exe -B working/verify_gate4_isolation_repair.py
```

Environment: `PYTHONDONTWRITEBYTECODE=1`, `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`.
To repeat synthetic isolation checks without rewriting reports, use `--child`.

## Independent self-review

A. **Can a candidate receive query labels directly or indirectly?** Production
execution is disabled. Synthetic direct/file/object tests found no labels, but a
complete numerical deployment is not certified. Do not claim a production guarantee.

B. **Can a candidate recover another episode's labels?** No recovery was observed
in the tested namespace/file/keyring probes. Full manifests remain host-only.
Production guarantee remains unverified; approved real-episode execution is blocked.

C. **Can adaptation state carry labels across episodes?** Ordinary process memory
and tmpfs are fresh in tests; no keyring sentinel crossed. Abnormal process-tree
teardown and the final immutable runtime/source-state policy remain unverified.
Therefore absence of all carry-over channels is not certified.

D. **Can the evaluator score without exposing labels?** The post-exit plain-output
architecture permits it, and malformed label-bearing outputs/requests are rejected.
No actual score was calculated; the complete scoring deployment was not certified.

E. **Are all exact 60 identities unchanged? YES.** Full diagnostic list and protocol
fields compare equal to the prior accepted sampler evidence.

F. **Can raw prototypes, frozen RF and E1 consume identical identities? YES at the
verified data-routing level.** Numerical worker deployment is still incomplete.

G. **Is E1 now fairly evaluable under the contract? NO.** Isolation/runtime
certification and a passing frozen manifest are absent; this is not E1 authorisation.

## Exact next action

STOP and hand this blocked partial-repair package to Team Lead. Request a narrowly
scoped continuation to provision/pin a label-free numerical sandbox, enforce immutable
code/source-state staging and bounded output/whole-process-tree teardown, then repeat
fresh-process negative-access and unchanged-identity checks. Freeze only after all
checks pass. Do not run E1, any candidate model, or Notebook 4.
