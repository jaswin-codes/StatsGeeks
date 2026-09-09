# E3 execution report — G4C-E3-002

## Final status

- **Execution: PASS — 60/60 fresh episodes completed.**
- **Independent validation: FAIL — stopped at the unchanged validator’s `Original tree dirty` gate.**
- **Protocol fidelity: PASS for production; validation stop honored. Full independent fidelity certification remains incomplete.**
- **Frozen coordinator scientific verdict: FALSIFIED; not independently validated.**
- Prior scientific run reused: **NO**. Protected artifact changed: **NO** (33/33 exact final hashes). E4/E5 run: **NO**.

## Identity, authorization and preservation

- Coordinator authorization UTC: `2026-09-09T08:50:21.743319+00:00`.
- Final report UTC: `2026-09-09T09:52:00.565707+00:00`.
- User explicitly accepted only the already-documented CERT-004 OneNote metadata hash and authorized proceeding after the prelaunch-only stop. CERT-004’s original NOT CERTIFIED report was not edited or relabelled.
- The initial failure report is preserved byte-for-byte as `checkpoint/PRELAUNCH_EXECUTION_REPORT.md`, bound by `checkpoint/infrastructure_preparation.json`.
- No E3-001 prediction or candidate state was consumed. Its frozen implementation was used through the existing approved asset generator; each new source/episode worker executed independently.

## Environment and production command

```bash
set -o pipefail; .venv_baseline/Scripts/python.exe -I -B working/G4C-E3-002/coordinator/execution_coordinator.py 2>&1 | tee working/G4C-E3-002/results/execution.log
```
- External bash-tool timeout: 5,000 seconds. One coordinator, no restart, no duplicate workers, no early termination.
- Windows producer: Python 3.14.6, NumPy 2.5.3, zlib `1.3.1.zlib-ng`; explicit `.venv_baseline/Scripts/python.exe`, `-I -B`, numerical thread variables set to 1.
- Approved Linux numerical runtime: Python 3.14.4, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.0, joblib 1.5.3, threadpoolctl 3.6.0, Narwhals 2.25.0. All 4,355 runtime files, wheel hashes and Bubblewrap hash checked.
- Runtime lock SHA256: `cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514`.
- Native RF: `/home/jaswin/.local/share/statsgeeks/frozen_rf/5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870.pkl`, 1,336,382,673 bytes, mode 0444, verified Linux-native filesystem. Every episode reports `created=false`; no Windows-backed model fallback.
- Coordinator assets match CERT-004 byte-for-byte except the authorized new run identity. E2-008 transport was the existing approved generator’s input. No performance change was implemented.

## Preflight

| Check | Result | Evidence |
|---|---|---|
| Historical preservation including accepted metadata exception | PASS: 1,151 files | `preflight_integrity.json` |
| Protected scientific artifacts | PASS: 33/33 | `preflight_integrity.json` |
| Host and approved runtime fingerprints | PASS | `checkpoint/data_host_preflight.json`, `checkpoint/runtime_preflight_native.json` |
| RF hash, native location, size and readonly mode | PASS | `checkpoint/runtime_preflight_native.json` |
| Frozen preprocessing, exact named feature order, arrays and identifiers | PASS | `checkpoint/data_host_preflight.json` |
| All 60 manifest bindings and RNG transitions | PASS | `checkpoint/data_host_preflight.json`, frozen run-local manifest |
| Fresh runtime/isolation probes | PASS | `evidence/preflight_*.json` |
| Frozen E3 parameters and scoring | PASS in production | Unchanged coordinator and worker hashes |

Budgets were 5, 10 (diagnostic), 25, 50, 100, 200 labels/class, ten trials each. This is five primary budgets plus one diagnostic budget, not five total. Seed 42/PCG64 advanced once through the exact frozen episode order. No preprocessing, forest, or hyperparameter refit occurred. Madrid class means were computed in a fresh source worker, then frozen. Target translation used only each episode’s selected support labels; indicators 58–59 remained unchanged. No new Madrid CV or target tuning was performed.

A preliminary shell-only runtime-check invocation was rejected because MSYS translated `/usr/bin/python3.14` into a Windows Git path. Both logs are preserved. Disabling shell argument conversion for the read-only WSL preflight restored the intended path; no worker launched in that failed invocation, no dependency changed, and production’s unchanged Python subprocess transport was unaffected.

## Execution and runtime

- Primary coordinator time: **3210.708326 s**; prediction/probe phase: **3210.280892 s**.
- Sum of 60 worker/supervisor boundary times: **982.790784 s**; including source and all three probes: **1011.433675 s**.
- Primary time outside those boundaries: **2199.274651 s**; includes integrity scans, WSL/JSON transport, packet construction, model staging verification, serialization, data loading and scoring. Not a pure coordinator CPU measurement.
- Production completed normally within the 5,000-second tool call. The recorded primary timer excludes its final integrity scan and console/report flush; the tool did not expose an exact full-call elapsed value. No exact full-call duration is invented.
- Peak episode worker RSS: **2,866,980 KiB**. Warnings: 0.
- Historical preflight audit: 6.865832 s. Immediate post-production audit and final audit are separately timed in `hashes/`. No extra timing instrumentation was added inside the episode loop.
- Independent validation stopped after **68.653303 s**. This is additional to production time.
- Every production output was verified before proceeding; all 60 NPZ outputs and per-worker transport/lifecycle evidence are retained. All predictions and workers finalized before query labels were attached for scoring.

| Episode | Budget | Trial | Boundary seconds | Worker | Teardown |
|---|---:|---:|---:|---|---|
| G4A-B005-T01 | 5 | 1 | 18.532263 | PASS | PASS |
| G4A-B005-T02 | 5 | 2 | 20.029681 | PASS | PASS |
| G4A-B005-T03 | 5 | 3 | 16.184327 | PASS | PASS |
| G4A-B005-T04 | 5 | 4 | 15.834993 | PASS | PASS |
| G4A-B005-T05 | 5 | 5 | 17.583302 | PASS | PASS |
| G4A-B005-T06 | 5 | 6 | 16.986091 | PASS | PASS |
| G4A-B005-T07 | 5 | 7 | 20.894552 | PASS | PASS |
| G4A-B005-T08 | 5 | 8 | 17.325407 | PASS | PASS |
| G4A-B005-T09 | 5 | 9 | 15.640827 | PASS | PASS |
| G4A-B005-T10 | 5 | 10 | 17.213174 | PASS | PASS |
| G4A-B010-T01 | 10 | 1 | 15.559466 | PASS | PASS |
| G4A-B010-T02 | 10 | 2 | 16.886951 | PASS | PASS |
| G4A-B010-T03 | 10 | 3 | 15.177742 | PASS | PASS |
| G4A-B010-T04 | 10 | 4 | 15.858939 | PASS | PASS |
| G4A-B010-T05 | 10 | 5 | 15.570914 | PASS | PASS |
| G4A-B010-T06 | 10 | 6 | 15.483753 | PASS | PASS |
| G4A-B010-T07 | 10 | 7 | 15.136897 | PASS | PASS |
| G4A-B010-T08 | 10 | 8 | 15.805811 | PASS | PASS |
| G4A-B010-T09 | 10 | 9 | 15.298385 | PASS | PASS |
| G4A-B010-T10 | 10 | 10 | 16.574635 | PASS | PASS |
| G4A-B025-T01 | 25 | 1 | 15.200694 | PASS | PASS |
| G4A-B025-T02 | 25 | 2 | 15.842689 | PASS | PASS |
| G4A-B025-T03 | 25 | 3 | 15.041146 | PASS | PASS |
| G4A-B025-T04 | 25 | 4 | 16.260790 | PASS | PASS |
| G4A-B025-T05 | 25 | 5 | 15.988502 | PASS | PASS |
| G4A-B025-T06 | 25 | 6 | 15.011739 | PASS | PASS |
| G4A-B025-T07 | 25 | 7 | 16.043301 | PASS | PASS |
| G4A-B025-T08 | 25 | 8 | 14.679256 | PASS | PASS |
| G4A-B025-T09 | 25 | 9 | 15.584558 | PASS | PASS |
| G4A-B025-T10 | 25 | 10 | 28.014861 | PASS | PASS |
| G4A-B050-T01 | 50 | 1 | 23.101231 | PASS | PASS |
| G4A-B050-T02 | 50 | 2 | 17.511966 | PASS | PASS |
| G4A-B050-T03 | 50 | 3 | 15.452001 | PASS | PASS |
| G4A-B050-T04 | 50 | 4 | 15.203302 | PASS | PASS |
| G4A-B050-T05 | 50 | 5 | 15.698339 | PASS | PASS |
| G4A-B050-T06 | 50 | 6 | 15.798184 | PASS | PASS |
| G4A-B050-T07 | 50 | 7 | 16.080288 | PASS | PASS |
| G4A-B050-T08 | 50 | 8 | 14.985332 | PASS | PASS |
| G4A-B050-T09 | 50 | 9 | 15.087116 | PASS | PASS |
| G4A-B050-T10 | 50 | 10 | 15.205514 | PASS | PASS |
| G4A-B100-T01 | 100 | 1 | 16.676386 | PASS | PASS |
| G4A-B100-T02 | 100 | 2 | 14.538068 | PASS | PASS |
| G4A-B100-T03 | 100 | 3 | 15.273861 | PASS | PASS |
| G4A-B100-T04 | 100 | 4 | 15.383812 | PASS | PASS |
| G4A-B100-T05 | 100 | 5 | 15.289609 | PASS | PASS |
| G4A-B100-T06 | 100 | 6 | 15.641727 | PASS | PASS |
| G4A-B100-T07 | 100 | 7 | 15.357390 | PASS | PASS |
| G4A-B100-T08 | 100 | 8 | 16.641037 | PASS | PASS |
| G4A-B100-T09 | 100 | 9 | 15.019709 | PASS | PASS |
| G4A-B100-T10 | 100 | 10 | 15.812610 | PASS | PASS |
| G4A-B200-T01 | 200 | 1 | 15.984140 | PASS | PASS |
| G4A-B200-T02 | 200 | 2 | 15.551351 | PASS | PASS |
| G4A-B200-T03 | 200 | 3 | 16.351185 | PASS | PASS |
| G4A-B200-T04 | 200 | 4 | 15.178197 | PASS | PASS |
| G4A-B200-T05 | 200 | 5 | 16.895527 | PASS | PASS |
| G4A-B200-T06 | 200 | 6 | 15.451888 | PASS | PASS |
| G4A-B200-T07 | 200 | 7 | 17.176874 | PASS | PASS |
| G4A-B200-T08 | 200 | 8 | 17.157228 | PASS | PASS |
| G4A-B200-T09 | 200 | 9 | 15.290184 | PASS | PASS |
| G4A-B200-T10 | 200 | 10 | 16.751079 | PASS | PASS |

## Frozen aggregate metrics

Macro F1 over classes [1,2,3,4], zero_division=0; mean and population SD (`ddof=0`). All ten trials included at every budget. These are coordinator results, not fully independently certified results. Full per-episode metrics, per-class precision/recall/F1, confusion matrices and paired deltas are in `results/per_episode_results.json`.

| Labels/class | E3 mean ± SD | Raw prototype | Same-query RF | E3 − raw | E3 − RF |
|---:|---:|---:|---:|---:|---:|
| 5 | 0.489854 ± 0.027567 | 0.543686 | 0.443277 | -0.053832 | +0.046577 |
| 10 | 0.510090 ± 0.029393 | 0.564873 | 0.443272 | -0.054783 | +0.066818 |
| 25 | 0.509079 ± 0.020012 | 0.598598 | 0.443265 | -0.089519 | +0.065813 |
| 50 | 0.513349 ± 0.006908 | 0.607879 | 0.443144 | -0.094530 | +0.070205 |
| 100 | 0.510743 ± 0.006692 | 0.612898 | 0.442837 | -0.102155 | +0.067906 |
| 200 | 0.513460 ± 0.004196 | 0.614955 | 0.442582 | -0.101495 | +0.070878 |

The frozen all-target zero-shot RF value 0.443273608786401 is contextual only, not a matched equal-information comparison. No new baseline was fitted.

### Frozen 25-shot decision rule

| Criterion | Result |
|---|---|
| mean_gain_over_raw_ge_0.0100 | FAIL |
| mean_gain_over_same_query_rf_ge_0.0100 | PASS |
| no_mean_per_class_raw_regression_worse_than_0.0200 | FAIL |
| no_mean_per_class_rf_regression_worse_than_0.0200 | FAIL |
| positive_raw_gain_ge_8_of_10 | FAIL |

- Mean per-class E3-minus-raw F1: `[-0.40261402186349426, 0.012423993735792838, 0.023852896208740315, 0.00826239327232059]`.
- Mean per-class E3-minus-RF F1: `[-0.1997486925176428, 0.08031232301131314, 0.3407824587769777, 0.04190737291885316]`.
- At 25 shots, all 10 raw-prototype paired gains were negative. Class-1 harm also violates the frozen safeguards. The unchanged decision rule returns **FALSIFIED**; improved mean F1 over RF alone does not make E3 successful. This is a development/reference-comparison result, not untouched final-audit evidence.

## Independent validation — mandatory stop

Command: `wsl -d Ubuntu --exec /usr/bin/python3.14 -I -B <run>/run_independent_validation.py` (via shell with MSYS path conversion disabled). The launcher used the unchanged bound validator SHA256 `02299fc780e624933255b5aa4e01192bb8d4e53d92c27fd0bcb0d12834a8828c` and verified the approved numerical runtime tree. It did not import candidate/coordinator code or launch candidate workers.

**Exact failure:** `e3_validator.production_context()` rejected Linux Git’s nonempty `git status --short -- original/` with `ValidationError: Original tree dirty`. This happened before `_validate` and before the complete independent 60-episode prediction/metric reconstruction. The validator was not changed, retried, or bypassed.

Windows Git reports original/ clean. Linux Git marks `original/1-Introduction.ipynb`, `original/2-Reading_Data.ipynb`, and `original/3-Preprocessing.ipynb` modified. Read-only comparison/configuration diagnostics are retained in `validation/git_discrepancy_diagnostics.json`. The final content-hash audit still passes. This distinguishes a Git-view discrepancy from evidence of modified protected bytes; it does not convert the failed gate to PASS.

| Category | Status |
|---|---|
| Protected and historical content-hash integrity | PASS — independent pre/post/final hash audits |
| Episode completeness/uniqueness and budget/trial coverage | PASS — production and separate serialization audit, 60/60 |
| Output bindings, query identifiers, shapes, dtypes, class values | PASS — separate strict serialization/worker-evidence audit |
| Exact archive member names/order and decompressed NPY bytes | PASS — 360 members |
| Unchanged Windows producer byte replay | PASS — 60/60 complete archive replays |
| Cross-compressor raw ZIP identity | Not required; scientific payload equality not relaxed |
| Native-worker versus original-RF independent reconstruction | NOT COMPLETED — validator stopped before this phase |
| Independent metric/confusion recomputation | NOT COMPLETED |
| Independent aggregate/verdict recomputation | NOT COMPLETED |
| Cross-run contamination checks | PASS in construction and separate output-path audit; full bound-validator phase not reached |
| Frozen manifest/RNG/hash binding | PASS preflight/production; full bound-validator phase not reached |
| Teardown | PASS — all 60 episodes, source, two initial probes and final probe; no recorded survivors |
| Unchanged complete independent validator | **FAIL — original-tree Git gate** |

## Protected state

Final audit: **PASS**, 33 scientific artifacts and 1,151 historical files unchanged from this run’s authorized starting state. The accepted OneNote metadata hash did not change again. `original/` content hashes remain unchanged. No historical experiment output was overwritten. Expected/observed hashes for every historical file are in `hashes/final_protected_audit.json`.

| Protected artifact | Expected SHA256 | Observed SHA256 | Result |
|---|---|---|---|
| `data/amsterdam_data.parquet` | `32388f3a9792b01d9831ca4d0fc4bfadba132a1c23c06e372d7a82e985be0719` | `32388f3a9792b01d9831ca4d0fc4bfadba132a1c23c06e372d7a82e985be0719` | PASS |
| `data/madrid_train.parquet` | `0e106a07044d867f8c68e77de8c36826c491d0f26692b8cde753d1046ce24c9c` | `0e106a07044d867f8c68e77de8c36826c491d0f26692b8cde753d1046ce24c9c` | PASS |
| `data/preprocessed/preprocessed_data.pkl` | `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe` | `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe` | PASS |
| `original/1-Introduction.ipynb` | `dd2b1e23eb8bc79d23ad5ac96d75ec99b15c28166e72db6d4f84f2e90afe640a` | `dd2b1e23eb8bc79d23ad5ac96d75ec99b15c28166e72db6d4f84f2e90afe640a` | PASS |
| `original/2-Reading_Data.ipynb` | `aa093cf5980e2218629e9dfe3a68ec20e8814b4bf4c33ae1bdb525532658ad9a` | `aa093cf5980e2218629e9dfe3a68ec20e8814b4bf4c33ae1bdb525532658ad9a` | PASS |
| `original/3-Preprocessing.ipynb` | `86136f0ab901a4fd15f45e7545c5107f98fb17ed271e9c46c12d0d614b261175` | `86136f0ab901a4fd15f45e7545c5107f98fb17ed271e9c46c12d0d614b261175` | PASS |
| `original/4-Modelling.ipynb` | `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae` | `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae` | PASS |
| `original/Open Notebook.onetoc2` | `a893d930d1d00f38b078bd96df08f6760dd8bbbf8bd7d2bdbf1b2a02239281fc` | `a893d930d1d00f38b078bd96df08f6760dd8bbbf8bd7d2bdbf1b2a02239281fc` | PASS |
| `working/3-Preprocessing_member2_baseline.ipynb` | `a97bf8f5b76fd3a3b852a3c1cf8b5a13efd697da62d44c85ed0c0ef9da50809b` | `a97bf8f5b76fd3a3b852a3c1cf8b5a13efd697da62d44c85ed0c0ef9da50809b` | PASS |
| `working/3-Preprocessing_member2_baseline_executed.ipynb` | `c6f7a50463f2785f10ff78a732fb655a29b282d89692b51d5baf4dbeb3fa3368` | `c6f7a50463f2785f10ff78a732fb655a29b282d89692b51d5baf4dbeb3fa3368` | PASS |
| `working/4-Modelling_member3_reference.ipynb` | `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae` | `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae` | PASS |
| `working/4-Modelling_member3_reference_executed.ipynb` | `37761873bc8d9ef57b13515b66ed636d400830b0b186cf25d55b41ccb3fc208e` | `37761873bc8d9ef57b13515b66ed636d400830b0b186cf25d55b41ccb3fc208e` | PASS |
| `working/baseline_artifacts/Open Notebook.onetoc2` | `989634ca4b3289918b3e47c07db4b5f2a22994b303f16025ee2f24700de1838c` | `989634ca4b3289918b3e47c07db4b5f2a22994b303f16025ee2f24700de1838c` | PASS |
| `working/baseline_artifacts/amsterdam_zero_shot.npz` | `e1d13830cc0d8d0f820aa0cc93a923b32117101b6ae1cea2c19c28ecb532523c` | `e1d13830cc0d8d0f820aa0cc93a923b32117101b6ae1cea2c19c28ecb532523c` | PASS |
| `working/baseline_artifacts/feature_schema.json` | `bea946aaf7d96e12370af5800f4e719bafe0f7b30fee4354278f7ef36e1f107a` | `bea946aaf7d96e12370af5800f4e719bafe0f7b30fee4354278f7ef36e1f107a` | PASS |
| `working/baseline_artifacts/madrid_cv_oof.npz` | `a52a7d721e505f3983fc470e1ef1785fac8ce7e6e4d59e0e09e663c425e2cbc5` | `a52a7d721e505f3983fc470e1ef1785fac8ce7e6e4d59e0e09e663c425e2cbc5` | PASS |
| `working/baseline_artifacts/prototype_trial_scores.npz` | `637631d7df4cf0d9f315424e9a3411744b26aeeea91b5c152da41ab7788c29ab` | `637631d7df4cf0d9f315424e9a3411744b26aeeea91b5c152da41ab7788c29ab` | PASS |
| `working/baseline_artifacts/recovery_manifest.json` | `01a6eb4b2e18f1eb99e06ddb84b6d2927d4992c0e999f7d9366f5af6ca26ff73` | `01a6eb4b2e18f1eb99e06ddb84b6d2927d4992c0e999f7d9366f5af6ca26ff73` | PASS |
| `working/baseline_artifacts/recovery_validation.json` | `f58c4ad5c99a0031eb5c2673905c53802484247a70874170e10f796fa15706f9` | `f58c4ad5c99a0031eb5c2673905c53802484247a70874170e10f796fa15706f9` | PASS |
| `working/baseline_artifacts/rf_final.pkl` | `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870` | `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870` | PASS |
| `working/freeze_member3_notebook4_outputs.py` | `6a16e84e05458bdad1667bfdbb0056a7a5100028a74a6c9d59177dabfee277d0` | `6a16e84e05458bdad1667bfdbb0056a7a5100028a74a6c9d59177dabfee277d0` | PASS |
| `working/member3_artifact_helpers.py` | `87fb7af733ede8a955b3ec6774588f7e32659a11b715566a4f6850d3cc251ab5` | `87fb7af733ede8a955b3ec6774588f7e32659a11b715566a4f6850d3cc251ab5` | PASS |
| `working/member3_baseline_frozen/Open Notebook.onetoc2` | `2064df45bbfbc846e222eead7c50942aba9df3266245fe3bb44dfffcc36d335f` | `2064df45bbfbc846e222eead7c50942aba9df3266245fe3bb44dfffcc36d335f` | PASS |
| `working/member3_baseline_frozen/amsterdam_prototype_results.json` | `8daf472e4a081dcd84344718436395746a19081b58b59ec83f0f047d5d530b6d` | `8daf472e4a081dcd84344718436395746a19081b58b59ec83f0f047d5d530b6d` | PASS |
| `working/member3_baseline_frozen/amsterdam_zero_shot_results.json` | `6b965f2a700c8d62eec9c79706d4950ef07dba78858e127edfe80f2835d3fa9a` | `6b965f2a700c8d62eec9c79706d4950ef07dba78858e127edfe80f2835d3fa9a` | PASS |
| `working/member3_baseline_frozen/artifact_manifest.json` | `c8541c570a702f7c2a616113d9c74269a83522af4b1ac6877f25d2b7dc51f435` | `c8541c570a702f7c2a616113d9c74269a83522af4b1ac6877f25d2b7dc51f435` | PASS |
| `working/member3_baseline_frozen/madrid_cv_results.json` | `6cff27f7448522ede547a7df835fefc19487105d56be40d2da880dae8fba7b5e` | `6cff27f7448522ede547a7df835fefc19487105d56be40d2da880dae8fba7b5e` | PASS |
| `working/member3_baseline_frozen/metadata.json` | `5fb0bada0c7bfd00f0c9c5a9274f8249640d538aa9cd12786ef23ee237c3c319` | `5fb0bada0c7bfd00f0c9c5a9274f8249640d538aa9cd12786ef23ee237c3c319` | PASS |
| `working/minimal_standard_scaler.py` | `c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111` | `c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111` | PASS |
| `working/run_member2_preprocessing.py` | `8ae69141c9fa5f04687d1237ce974f9c18d1bb76dbd8f7a338383e5084a0fe7d` | `8ae69141c9fa5f04687d1237ce974f9c18d1bb76dbd8f7a338383e5084a0fe7d` | PASS |
| `working/run_member3_notebook4_artifact_capture.py` | `41a4a9e7d4b5f66fbb06180fce1f0724258a32c1c1391074804ef1d2fb88612f` | `41a4a9e7d4b5f66fbb06180fce1f0724258a32c1c1391074804ef1d2fb88612f` | PASS |
| `working/run_member3_notebook4_reference.py` | `7ed22f17116d2690516db02c686396995074a3ec5a6bd84d63f1d9c5cc206bc6` | `7ed22f17116d2690516db02c686396995074a3ec5a6bd84d63f1d9c5cc206bc6` | PASS |
| `working/verify_gate4a_episodes.py` | `6ad66b3e0a8a287e1277c8e43c76759493f2fe9362cc5e685750c6ee30b51532` | `6ad66b3e0a8a287e1277c8e43c76759493f2fe9362cc5e685750c6ee30b51532` | PASS |

## Output hashes and report lifecycle

- `artifact_hash_manifest.json` is the immutable **prevalidation-phase** seal. Its report entry binds the prevalidation report preserved exactly at `checkpoint/PRIMARY_EXECUTION_REPORT_PREVALIDATION.md`; the original seal is not rewritten. Only this human-facing final report supersedes that report path, explicitly recorded in `validation/report_lifecycle.json`.
- `final_artifact_hash_manifest.json` binds the final reporting phase, including this report, the unchanged earlier seal, all scientific outputs, diagnostics, independent-validation failure and preserved reports. Its SHA256 is recorded in `final_artifact_hash_manifest.sha256`.
- Frozen episode manifest SHA256: `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.
- RF SHA256: `5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870`.
- Prevalidation seal SHA256: `561141c573ea27a4da5008e78745522e568564fdcde7249567b69cb3968110e2`.
- Source state canonical SHA256: `089eefb91d4df4f651905e3e7b602294411a5ced66590977bb50945d54ec768e`.

| Episode | Prediction artifact SHA256 |
|---|---|
| G4A-B005-T01 | `d3c7641cedf4fde41c6e709fc8ea9d214b710eaa09935ba4d31e96c73773d8b0` |
| G4A-B005-T02 | `b17b6d3e0f68ccd3cead0c24b15b7c1fb779e9e152d1a4d1f862b85b899897ac` |
| G4A-B005-T03 | `12de08fa2bd56a0849291a15b17970961ae36cf0f94c0858c04e5658595f406b` |
| G4A-B005-T04 | `f2fd273fee9630fd25e591f692225c1020ef6d97773f874eff73638f5d355892` |
| G4A-B005-T05 | `482fc4ec2550485daecb89cf19d50cec88a526f05c81ceecbb74d15eea2f9759` |
| G4A-B005-T06 | `bf15b94557ff96b0561ed3a67964abe2a8c6fa49f3c938ece16407241f618525` |
| G4A-B005-T07 | `31fb56f164e3a177ba59f081bf2fd522d0695a19951a3b5194980e7b23747b11` |
| G4A-B005-T08 | `c5f339feaca220237322755f73e2f0779f24937bf4c9b51f507a35aa071cbdec` |
| G4A-B005-T09 | `e16f23b82883cae975c82ccd56144d426ac64400615efa479481d6908ee692b7` |
| G4A-B005-T10 | `5fd513bdc2ab58aec5119c01100b107afba7dcb3fe09a69daa247ff15dfcf864` |
| G4A-B010-T01 | `645a37c940d0c237d322aa3d60222f77197eb1d8ca1e91c7d036cd68524f4ce2` |
| G4A-B010-T02 | `bb0b64962d55e8ea238a4edc737951e50d892c6e348525cff82630a866e6cc59` |
| G4A-B010-T03 | `1a56d017157f3c03e584475054725a6ac6084d7e143c90783b105c3dd2d5fd5c` |
| G4A-B010-T04 | `5c649a6106bd79ad2663d168e2b492332944595f7ba80d337bd00f737b770f35` |
| G4A-B010-T05 | `02183c222138ca5576fc1c4d985ad21c3ab66874164497a8ac2211f7970c2e3c` |
| G4A-B010-T06 | `1b32ba5b18753aa20d660ea9567e0c741558194b3061a651df1f72151a67edc8` |
| G4A-B010-T07 | `e378eb42ba924fc753b69a4b8355109a709f9a0f8fca184f85f7f065cff67ed8` |
| G4A-B010-T08 | `96a9d3b80f2288c3815352a97fa07adf9b0f516f051e6306fc0fe9579c084bde` |
| G4A-B010-T09 | `d55b77d553e4b5f9ed106f9f46d544338a31b5ec6233be83482f04a815a6c67d` |
| G4A-B010-T10 | `df8b96c17da52010e0a38d16ecbfb78b1fda9e94523da6932222952c13bc85fd` |
| G4A-B025-T01 | `a1c468e41f214cb7e620482525cc91da6ad3b1edb661aec1f42a0912ea0aac38` |
| G4A-B025-T02 | `65717915212775a03839200cd1e93f50d2b430457648652187b5ff7afa62bf0d` |
| G4A-B025-T03 | `6485136838d56343fb6bef6bb642c137acdeba15b04ff35409b16540c1ad89ea` |
| G4A-B025-T04 | `248140a952839214906809fd6fa9324ad59c9e53e1e81edb60c6f2efa7381663` |
| G4A-B025-T05 | `23dc35c33ee63ce5d3ce9037dd160ebd464cdd77c5b400177e97b13c4a6a7ea9` |
| G4A-B025-T06 | `8fe3bf0256b71b66157f1478f351d28fd7f285ff5a90c1c6faf30a50fd53f897` |
| G4A-B025-T07 | `424a0a7166f5dd262610447c73576d91ce6bbae20183ab82a8f179a5274d939c` |
| G4A-B025-T08 | `7081d401e7d25026b4ded7d24cacee0aecf4749f4481958e2b43d90da603911c` |
| G4A-B025-T09 | `de6243a6ab1ad93cd9e8111f1b96617a22a18c41fe847dc64d942914e4c4cbd7` |
| G4A-B025-T10 | `38097af96f3b816c07eae4e0ee67f5af1f8c1a6ea2bddb5036ff531065a7bc5e` |
| G4A-B050-T01 | `0ff980d5e35d8b0dc6fc1b671217530eef04ab5f43b7fc258f57d1f966719efb` |
| G4A-B050-T02 | `9bb38cd76eced1ad249cc48208b5b0a98447ac3e109829fae33860ff4a87fec9` |
| G4A-B050-T03 | `4b63359bf472dd38065ac42f2989903704d26376f38d23816ef7795a74884a81` |
| G4A-B050-T04 | `a353459e6b84fd422a0705997c8da4dbc6506ce6c86be1bc574a67b6c0f39f0d` |
| G4A-B050-T05 | `8bae9fc91b854ec33aa1f84e5e284919f4d9d05b335639a2abaa2d6cde3fec58` |
| G4A-B050-T06 | `213d7382f0085b101e6570cffa498548799ac355451c5739363e57eafe697817` |
| G4A-B050-T07 | `9e03ca9e941ad45a5da23d9f2e32f8f7d56114e758d7cd0f45856e229c9fb6d4` |
| G4A-B050-T08 | `4f11fdafe1776e345ffdf95dde1da686727d01a8b4d7062e63c1c9eec10f5040` |
| G4A-B050-T09 | `1352e593a06d2060cf81ceac8d8e9f3924642aca61251fbad1ee2faaaa15d270` |
| G4A-B050-T10 | `bb2ef13210a0614c7125e129ffdbc86ebcfe017e6a508f6078e6384315eef610` |
| G4A-B100-T01 | `5c3f698151e2c8c46455ee79ecb8af3678ac1fcb3dcd657aeec8a729c519ef02` |
| G4A-B100-T02 | `22338503fc6c033ec9cd81b1e63e858fabdacd2ae5a8d893f34acc8445d24f6d` |
| G4A-B100-T03 | `97aa8a31527bc99dbddc074d7342bafdbe29f42f0f2707305fdade3955672c00` |
| G4A-B100-T04 | `4b34376c8367e849aa81d7c391743fa3c0e1ecd3715772a29e95ab24e733bb00` |
| G4A-B100-T05 | `3cee8551884dc2df356a90f743eb1264817ee9baac0504fdfb18ed78a0ae312b` |
| G4A-B100-T06 | `8dd47b07db4f72efb1873064dda1c2cf1aaefb698f5a5280d4d5c4e3812aeaad` |
| G4A-B100-T07 | `1c7a14aaf08db3cb10ba33d751bc8349c0b13ce425b923bf95ef06d09f25abdf` |
| G4A-B100-T08 | `3e8cb7c6b1e3b738da1dd3c7dec9d2b4d080705cd2dd4d1076384eb2ab3ffa9d` |
| G4A-B100-T09 | `0040d27f2e6a98e5b9b8dcdb56d9f26e846c4322563c8fc82b24709a14204b41` |
| G4A-B100-T10 | `44bd1e69f10ff6c25f87c6727390697a01bbc1ac8f855680e4398cfef6c0398d` |
| G4A-B200-T01 | `8329b553ccea3822d39399609802acf0beb0473c21c9274356ae19c52d70f714` |
| G4A-B200-T02 | `ff8b81c345434f14abe085586c6f5d617c270b306ba038b5b9686070f3691737` |
| G4A-B200-T03 | `5c44b0b7859a356f55c8b929505df0c5f23e4787ba43a5a7265acb5362235cb1` |
| G4A-B200-T04 | `2890ad38c1b3dc03d33a1b3801a2e6d900c0486205a1c51a4b1e8bb3d38a48ba` |
| G4A-B200-T05 | `73f2559b8d92f8e08e550659b340c7470d2b2509f270000f187092e00493ecd7` |
| G4A-B200-T06 | `b460a8a5dc96624bbef0e52e7d6ed7d9e1425b870d7dfda9bb8859d2f78e7422` |
| G4A-B200-T07 | `3536a1b8447ac59764bed1774f0ed9e4e0072dfcbd580f14c4bb35df051adc95` |
| G4A-B200-T08 | `d6b200ba81a388e02289dfcf6fbe97b95a38c4f8e823469d57f7dbae99d179b3` |
| G4A-B200-T09 | `8baa0cbfbe023bbf9d1e56b96b8a48a91605cfa0eb29bfd731367685dca2c81d` |
| G4A-B200-T10 | `8fee29e348d9593b99b5f049e3e11ca14fdfd908c88bf3c493b678e494cd493d` |

## Stop disposition

No further scientific execution or validation recovery is authorized by this attempt. Preserve the failed validator and all outputs. A separately authorized resolution of the Windows/Linux Git clean-tree check is needed before a complete validation PASS can be issued. No E3 episode needs to be represented as missing, and no scientific success is claimed.
