# Gate 4B E1 — completed, fixed E1 FALSIFIED

Run ID **G4B-E1-001**. Gate 4B execution status **PASS**: exactly the authorized
E1 plus P0/U0/saved-RF controls completed on all 60 frozen episodes. Scientific
verdict **FALSIFIED** under the preregistered primary rule. No tuning or E2–E5.

## Method and boundary

Source worker received Madrid X/y only. On 59 source-nonconstant dimensions it fit
the class-balanced population within-class covariance and fixed
`0.9 W + 0.1 trace(W)/d I`; U0 used population total Madrid covariance with identical
shrinkage. Both inverse metrics were saved in `source_state.json`. Every target
worker was fresh and received only immutable source state, current support X/y/IDs,
current query X/IDs, and fixed episode metadata. It emitted P0/U0/E1 predictions,
then exited and was fully reaped. All 60 workers finalized before the privileged
evaluator attached query labels. Frozen RF predictions were subset to the same Q;
the 1.336 GB RF was not retrained or invoked.

Two actual-code preflights passed before source fitting: approved runtime, no project/
manifest/label mounts, no inherited label descriptors/references, private temporary
state, read-only runtime, prediction lifecycle. Gate4A manifest was never supplied
to a worker. No scoring feedback entered later workers.

## Results (macro F1, mean ± population SD over 10 trials)

| shots/class | E1 | Raw P0 | U0 | same-Q frozen RF | E1−P0 | E1−U0 | E1−RF |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | .51023±.03858 | .54369±.03240 | .50073±.03849 | .44328±.00012 | −.03346 | +.00949 | +.06695 |
| 10 | .52823±.03208 | .56487±.03119 | .51963±.03287 | .44327±.00020 | −.03664 | +.00861 | +.08496 |
| **25** | **.59008±.03214** | **.59860±.01764** | **.58362±.03425** | **.44327±.00031** | **−.00852** | **+.00646** | **+.14681** |
| 50 | .60567±.02057 | .60788±.01012 | .60040±.02193 | .44314±.00033 | −.00221 | +.00528 | +.16253 |
| 100 | .62525±.00889 | .61290±.00974 | .62109±.00889 | .44284±.00045 | +.01235 | +.00415 | +.18241 |
| 200 | .62411±.00701 | .61495±.00360 | .62102±.00728 | .44258±.00054 | +.00915 | +.00309 | +.18153 |

Raw matched trial scores exactly reproduce all 60 frozen historical prototype scores.
Full-target RF `.443273608786401` remains contextual; table RF values are proper
support-excluded same-Q scores.

### Primary 25-shot per-class mean F1

| class | E1 | Raw P0 | U0 | same-Q RF | E1−P0 |
|---:|---:|---:|---:|---:|---:|
| 1 | .62306 | .64492 | .61269 | .44206 | −.02187 |
| 2 | .56198 | .55242 | .55552 | .48453 | +.00956 |
| 3 | .58448 | .61827 | .58179 | .30134 | −.03379 |
| 4 | .59080 | .57877 | .58448 | .54513 | +.01202 |

### Fixed success rule

- Mean E1−P0 ≥+.0100: **FAIL** (−.00852).
- Positive E1−P0 in ≥8/10: **FAIL** (4/10).
- No class regression worse than .0200: **FAIL** (C1 −.02187, C3 −.03379).
- Positive E1−same-Q RF: **PASS** (+.14681).
- Beat U0: **PASS** (+.00646), but this does not rescue failure versus P0.

Verdict: **FALSIFIED for this fixed specification on this development/reference
benchmark.** Better high-budget values do not supersede the preregistered 25-shot
criterion. No causal/general transfer claim; trials share heavily overlapping queries.

## Reproducibility and independent verification

- Frozen evaluator manifest SHA256:
  `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.
- Source-state SHA256:
  `33973edd974f6703cd869b6d1460304ee2b3cfa37dd3173694a1021b7c79997c`.
- Runtime lock SHA256:
  `cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514`.
- Runtime: Python 3.14.4; NumPy 2.4.6; SciPy 1.17.1; sklearn 1.9.0;
  Narwhals 2.25.0; joblib 1.5.3; threadpoolctl 3.6.0; BLAS/OpenMP threads 1.
- Episode-worker wall-time sum: 784.663 s. Resource ceiling 6 GiB/worker;
  measured peak RSS was not captured and is reported unavailable, not estimated.
- Independent privileged implementation refit W/U0 from Madrid, reloaded all 60
  prediction NPZs, reproduced every prediction exactly, recalculated every confusion,
  per-class/macro score, aggregate and paired delta, and matched all historical P0
  trial values exactly. Windows/Linux metric matrices agreed within 2e−14; exact
  predictions were the decisive verification.
- Two verifier attempts are retained: missing repository import path, then overly
  strict cross-platform eigensolver matrix tolerance. Repairs affected verifier only;
  candidate artifacts, parameters and results were not rerun or changed.

`summary.json`, `per_episode_results.json`, `source_state.json`, every prediction
NPZ and worker lifecycle record are authoritative machine-readable evidence.
`artifact_hash_manifest.json` inventories every run/code artifact and baseline anchor.

Final checks: frozen manifest unchanged/read-only; all 33 protected hashes unchanged;
`original/` Git status and diff empty; original OneNote remains read-only. Notebook 4
was not rerun. No baseline, raw, preprocessing, reference or manifest file modified.

**Next action:** stop. Team Lead may accept the negative E1 finding and separately
decide whether to authorize one preregistered backup. Do not tune E1 or automatically
run E2–E5.
