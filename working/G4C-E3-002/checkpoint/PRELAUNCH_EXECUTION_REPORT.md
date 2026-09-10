# E3 execution report — G4C-E3-002

- Recorded UTC: 2026-09-09T08:41:51Z
- Execution: FAIL — blocked in Phase 0; production never launched.
- Episodes: 0/60.
- Validation: FAIL — certification prerequisite failed; production validation not performed.
- Protocol fidelity: PASS — mandatory stop honored; no scientific definitions changed.
- Scientific verdict: NOT EVALUATED. No predictions were scored.
- Production runtime: 0 seconds. Inspection/report time is not production runtime.

## Exact stop reason

The request states that runtime certification passed in `working/G4C-INFRA-CERT-004/`. The actual governing report, `RUNTIME_CERTIFICATION_REPORT.md`, explicitly concludes **RUNTIME NOT CERTIFIED — DO NOT RUN E3**. Its favorable runtime forecast is expressly insufficient to override its failed historical-state gate.

`working/G4C-INFRA-CERT-004/hashes/protected_after.json` records `status: FAIL`, 1,072 historical files checked, and this change:

| Historical artifact | Expected SHA256 | Observed SHA256 in CERT-004 | Status |
|---|---|---|---|
| `working/G4C-INFRA-PERF-001/code/Open Notebook.onetoc2` | `f2a5477d4cef70fe707f91402d66296435919ad0ee24577d0e3b027d20828ecd` | `e2e685e8b6be61f2d70f5e33191a4629a1b92d1516f1f6c1738ace9a75904025` | FAIL |

Recorded size changed from 5,040 to 6,160 bytes. These are historical certification observations, not a fresh E3 hash audit. CERT-004 reports that its 33 protected scientific artifacts and organiser originals remained unchanged.

This contradicts the required certification prerequisite and activates the explicit immediate-stop rule. No metadata exception, repair, recertification, alternative path, or scientific improvisation was attempted.

## Evidence binding

SHA256 observed during this inspection:

- `working/G4C-INFRA-CERT-004/RUNTIME_CERTIFICATION_REPORT.md`: `37996c2eb667ca4784b895b5e674842c970e2346b4ad5738ac62bdb867a5f3c1`
- `working/G4C-INFRA-CERT-004/hashes/protected_after.json`: `3c72fe42c542a67cba9064ff3a8a1b6aed95ea257248c88e99c36f03b85186ba`

Also read project instructions, the candidate experiment plan, and the execution reports of E2-008 and E3-001. E2 reports 60/60 and independent validation PASS; E3-001 reports an external timeout at 52/60 and is explicitly non-resumable. Neither supplies the missing successful CERT-004 gate.

## Unperformed phases

Exact production-command/environment reconciliation and the remaining source, runtime, RF, preprocessing, episode, isolation and time preflight checks were not completed because the certification failure required an immediate stop. No production command was selected or executed.

No coordinator, source worker, episode worker, packet, prediction, episode metric, aggregate, or baseline comparison was generated. No worker timing, teardown evidence, peak memory, integrity overhead or coordinator overhead exists. Teardown is not applicable: no workers were launched.

Independent artifact, episode, binding, identifier, shape, dtype, class, metric, aggregate, contamination, manifest, teardown and prediction-equivalence validation was not performed. No raw NPZ-byte or decompressed-member equivalence claims are made. A complete new protected-state post-audit was not performed; no blanket current-hash PASS is claimed.

## Preservation and scope

Only this fresh run directory and its execution report were created. No prior-run state or predictions were reused. No prior output or protected artifact was intentionally modified by this attempt. The pre-existing historical modification documented above remains unresolved; it was not repaired or normalized. E4/E5 were not run.

Execution completion is not scientific success. The frozen E3 decision rule cannot be evaluated without a complete validated run. A successful authoritative certification resolving this contradiction is required before any newly authorized production attempt.
