# G4C infrastructure certification 004 — runtime readiness

## Final decision

**RUNTIME NOT CERTIFIED — DO NOT RUN E3.**

The measured optimized production path itself supports a sub-5000-second forecast with a meaningful calculated margin. Certification nevertheless fails because the mandatory protected-state post-check detected an unexpected change to one of the 1,072 historical files. The instruction requires any such change to be an immediate STOP; runtime evidence cannot override that gate.

## 1. Exact 5000-second enforcement

The limit came from the **pi coding-agent `bash` tool call**, not from the shell, Python coordinator, worker, or an OS `timeout` command.

The original pi session transcript records tool call line 96 with arguments:

```json
{
  "command": "set -o pipefail; .venv_baseline/Scripts/python.exe -I -B working/G4C-E3-001/coordinator/execution_coordinator.py 2>&1 | tee working/G4C-E3-001/results/execution.log",
  "timeout": 5000
}
```

The shell command contains no `timeout 5000s`. The coordinator has only a 300-second timeout on each WSL subprocess; the Linux boundary has a 180-second per-worker timeout. Neither imposes a 5000-second global deadline. See `evidence/timeout_enforcement.json`, which binds the transcript path and SHA256.

## 2. Bounded benchmark design

No full E3 was run. A dedicated, explicitly non-scientific harness exercised:

1. optimized coordinator startup and unchanged integrity validation;
2. the production five-second metadata settle;
3. real frozen data/comparator loading and all 60 frozen RNG transitions;
4. two real isolated preflight workers;
5. the real isolated Madrid source worker;
6. five fixed trial-1 manifest episodes spanning budgets 5, 25, 50, 100 and 200;
7. fresh WSL transport, approved runtime scan, native RF staging verification, Bubblewrap isolation, real RF mount/hash/load, unchanged E3 predictions, output transport and complete teardown;
8. normal prediction verification and NPZ serialization.

No query labels crossed the candidate boundary and no query labels were scored. The five outputs are marked `NON_SCIENTIFIC_*`; no scientific verdict was created.

Measured episodes were manifest ordinals 1, 21, 31, 41 and 51: `G4A-B005-T01`, `G4A-B025-T01`, `G4A-B050-T01`, `G4A-B100-T01`, and `G4A-B200-T01`.

## 3. Actual timings

- Total bounded benchmark: **371.581 s**
- Observed startup/non-episode portion: **110.835 s**
- Episode full-cycle mean: **52.149 s**
- Episode median: **51.816 s**
- Episode maximum: **54.216 s**
- Episode range: **49.069–54.216 s**
- Boundary worker/supervisor range: **15.123–18.678 s**
- Native cache verification: **2.406–3.237 s**
- Predispatch integrity scan: **6.484–8.132 s**
- In-call integrity scan: **6.472–7.090 s**
- Packet construction: **0.128–0.190 s**
- Prediction serialization: **0.043–0.058 s**
- Inter-episode delay: effectively zero, maximum **0.0023 s**
- Observed teardown completion after end-of-stream/wait: approximately **0.005–0.007 s**, with no survivors

The worker's RF hash, pickle load and prediction calls are not separately timestamped by the unchanged approved worker. Instrumenting them would change its bytes and invalidate the production-path measurement. They remain included in the directly measured complete boundary and external cycle times rather than being represented by a synthetic estimate.

## 4. RF access and optimized-path verification

All five episode transports used the content-addressed Linux path:

`/home/jaswin/.local/share/statsgeeks/frozen_rf/5ffdd11f...75870.pkl`

It is 1,336,382,673 bytes, mode 0444, has the frozen SHA256, and resides on `/dev/sdd` **ext4**. It is not under `/mnt/c`. Lifecycle evidence confirms this exact file was mounted read-only inside Bubblewrap as `/app/rf_final.pkl`. `native_rf_created=false` for every episode, so there was no copy or Windows-backed fallback.

## 5. Duplication and fallback check

No hidden retry, second worker, second supervisor, or fallback Python environment was observed. Each successful episode has one transport record and one isolated worker chain; `/usr/bin/python3.14 -I -B` from the approved image was used.

Existing intentional duplicate integrity work remains:

- two coordinator integrity scans per episode;
- one full native-cache RF hash in staging verification;
- one supervisor RF hash before mounting;
- one worker RF hash before pickle load.

The benchmark retained all of these checks. Large JSON packet serialization/transport is included in `call_outside_boundary_seconds` (25.932–29.671 s together with the in-call integrity scan, WSL startup, runtime scan and supervisor pre-launch work). Nothing was silently optimized away.

## 6. Sixty-episode forecast

The forecast includes the measured startup, 60 complete episode cycles, a conservative post-prediction probe/scoring/final-integrity allowance, and explicit safety treatment:

| Forecast | Seconds | Margin to 5000 s |
|---|---:|---:|
| Mean-cycle forecast | 3,278.334 | 1,721.666 |
| Every episode at observed maximum | 3,402.331 | 1,597.669 |
| Conservative: add 33.08 s cold-stage allowance, then 20% contingency | **4,122.493** | **877.507 (17.55%)** |

This is not a 4,800-second borderline claim. On runtime evidence alone, the optimized path has a meaningful conservative margin and would support runtime readiness.

## 7. Protected-state verification and mandatory stop

Before benchmarking, all **1,072/1,072** historical files matched certification 003, all **33/33** protected artifacts matched, and `original/` was clean.

After benchmarking:

- the 33 protected artifacts and `original/` remained unchanged;
- RF, manifest, data, workers, scoring, validation and teardown code remained unchanged;
- however, historical file `working/G4C-INFRA-PERF-001/code/Open Notebook.onetoc2` changed from 5,040 bytes / SHA256 `f2a5477d...28ecd` to 6,160 bytes / SHA256 `e2e685e8...904025`.

This appears to be external OneNote directory metadata, not scientific code, but the requirement says **any unexpected historical-file change is an immediate STOP**. It is therefore reported without repair, deletion or normalization. See `hashes/protected_after.json`.

## 8. Changes and scope

Only new certification files under `working/G4C-INFRA-CERT-004/` were intentionally created. No full E3, E4 or E5 run was launched; no experiment definition or scientific result was changed. Failed harness-layout diagnostics were preserved. `changes.patch` records the dedicated harness and optimized infrastructure differences.

## Certification

The timing result is favorable, but the protected-state gate failed. Certifying despite that failure would violate the explicit protocol.

**RUNTIME NOT CERTIFIED — DO NOT RUN E3**
