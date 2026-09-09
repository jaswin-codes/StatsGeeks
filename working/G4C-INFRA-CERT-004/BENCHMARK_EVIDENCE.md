# Benchmark evidence — runtime certification only

## Scope

This was a **NON-SCIENTIFIC / RUNTIME-CERTIFICATION ONLY** execution. It did not run the 60-episode experiment, attach query labels, score candidate outputs, or create a candidate verdict.

The successful measurement ran the production startup sequence (startup integrity check, five-second metadata settle, frozen data/comparator load, complete 60-entry RNG replay, two isolated preflights and the isolated Madrid source worker), followed by fixed manifest ordinals 1, 21, 31, 41 and 51: `G4A-B005-T01`, `G4A-B025-T01`, `G4A-B050-T01`, `G4A-B100-T01`, and `G4A-B200-T01`.

## Production-path identity

The harness used generated assets from `G4C-INFRA-PERF-001/code/prepare_assets.py`:

- unchanged episode worker SHA256: `b3cf5ab28ccbac2506c8ed7398a3b25254b24c86d8e58e5f1de742577660c350`
- unchanged source worker: `c00c31624c9e107ce5aba2024c9c834648ff92f816acb390127846a2b3938d30`
- unchanged preflight worker: `bb5a3114ebfaa4cf0716d9cf4f4467c6682924c95ffd7fa631b40ca4b513e2f6`
- optimized coordinator: `4aae65bfd53bafef7d10856a50922fd0b25f55fea3795a4f6d09e7ed5be09adb`
- optimized transport: `6ca48dea6a3bf49c3ed629ba120eb5093d0e4afd48b651a424594f7584a7f6e3`

Every episode used a fresh WSL transport, fresh Bubblewrap namespace, unchanged runtime scan, real RF mount/load, prediction production, lifecycle observation and teardown. All five return codes were zero, all teardown checks passed, all final-survivor lists were empty, and no warnings occurred. Generated prediction archives exactly matched the corresponding historical producer hashes.

## Wall-clock results

| Episode | Budget | Full cycle | Boundary worker/supervisor | Call outside boundary | Native cache verification | Predispatch scan | In-call scan |
|---|---:|---:|---:|---:|---:|---:|---:|
| G4A-B005-T01 | 5 | 54.045 s | 18.678 s | 28.651 s | 3.237 s | 6.484 s | 6.472 s |
| G4A-B025-T01 | 25 | 54.216 s | 16.226 s | 29.671 s | 2.824 s | 8.132 s | 6.711 s |
| G4A-B050-T01 | 50 | 51.816 s | 16.153 s | 27.448 s | 2.681 s | 8.034 s | 7.090 s |
| G4A-B100-T01 | 100 | 49.069 s | 15.123 s | 25.932 s | 2.406 s | 7.771 s | 6.495 s |
| G4A-B200-T01 | 200 | 51.600 s | 16.464 s | 27.255 s | 2.580 s | 7.694 s | 6.797 s |

Episode-cycle mean was **52.149 s**, median **51.816 s**, maximum **54.216 s**. Inter-episode delay was 0.000–0.0023 s. Packet construction was 0.128–0.190 s and NPZ serialization 0.043–0.058 s. Total benchmark wall time was **371.581 s**; observed startup/non-episode time was **110.835 s**.

Startup details: initial coordinator integrity 6.502 s; required metadata settle 5.001 s; data/comparator load 0.051 s; RNG replay 0.036 s. Preflight wall/boundary times were 28.547/6.862 s and 22.687/7.032 s. Source wall/boundary time was 45.992/8.850 s.

Lifecycle observations measured launch-to-namespace at 0.020–0.047 s. For four episodes, end-of-stream through completed teardown was 0.005–0.007 s; episode 51 exited too quickly for the pre-wait observation, and its recorded launcher-wait-complete to teardown-complete lower bound was 0.006 s. Complete lifecycle records are retained.

The unchanged worker deliberately combines its internal RF hash, pickle load, two RF predictions and JSON output without phase markers. Splitting those operations would require modifying the approved worker and would cease to be the production path. They are therefore reported honestly as part of the directly measured 15.123–18.678 s boundary interval. The stronger relevant measurement—the complete external episode cycle—is measured directly.

## RF path and repeated work

Every transport record reports:

`/home/jaswin/.local/share/statsgeeks/frozen_rf/5ffdd11f...75870.pkl`

Independent path evidence shows SHA256 `5ffdd11f...75870`, 1,336,382,673 bytes, mode 0444, filesystem **ext4** (`/dev/sdd`), and `WINDOWS_BACKED=false`. Bubblewrap lifecycle commands show that exact native path mounted read-only as `/app/rf_final.pkl`. There was no `/mnt/c` RF fallback.

The unchanged integrity protocol intentionally performs duplicate work: two full coordinator integrity scans per episode; one native-cache full hash; one supervisor RF hash before launch; and one worker RF hash before unpickling. The benchmark did not remove them. The production code contains no retry loop, and evidence shows one transport, one Bubblewrap supervisor chain and one isolated scientific worker per successful episode. No fallback interpreter was used: lifecycle commands identify `/usr/bin/python3.14 -I -B /app/entry.py` in the approved image.

## Evidence files

- `evidence/runtime_measurements.json` — timestamps and all phase measurements
- `evidence/forecast_and_lifecycle.json` — reproducible forecast and teardown extraction
- `evidence/native_rf_path_verification.txt` — native path/hash/filesystem proof
- `evidence/benchmark_worker_*.{json,transport.json}` — worker and transport evidence
- `predictions/NON_SCIENTIFIC_*.npz` — benchmark-only prediction replay artifacts
- `hashes/protected_before.json`, `hashes/protected_after.json` — state gate

Three retained setup diagnostics preceded the successful measurement. Two failed before any transport; one reached transport validation but failed before Bubblewrap/worker launch because the temporary nested path resolved the runtime lock incorrectly. The successful measurement used direct production-depth layout and did not reuse those failed records. They are disclosed rather than deleted.
