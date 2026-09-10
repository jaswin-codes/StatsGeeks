# Member 4 Final Judging Pack

**Frozen headline:** EXP-010, 45/50 paired wins.  
**Claim:** Madrid-supervised feature selection combined with budget-dependent prototype shrinkage improves few-shot transfer from Madrid to Amsterdam, with the largest benefit when only 5 labels per class are available. As target labels increase, dimensionality reduction remains beneficial while shrinkage becomes unnecessary.

## Judge-facing evidence map

| Topic | Evidence | Qualification |
|---|---|---|
| Main result | `candidate/artifacts/joint_sweep.json` | Raw arrays independently re-aggregated; 45/50 |
| Method source | `candidate/joint_sweep.py` | Frozen; do not rerun |
| Arithmetic check | `candidate/verify_frozen_results.py` | No fitting/prediction |
| Packaged source state | `candidate/artifacts/exp010_stage1_madrid.pkl` | Reload/interface checked; legacy pickle is older top-30 |
| Fresh feature evidence | EXP-008 / `feature_comparison.json` | Supporting evidence, not EXP-010 replication |
| Shrinkage foundation | EXP-009 / `shrinkage.json` | Method development |
| Mechanism | EXP-004 | Whitening harmful low-budget, useful high-budget |
| Negative ablation | EXP-007 | Expanded season/coverage features did not improve v1 |

## Main result

| shots | tuned | control | gain | wins |
|---:|---:|---:|---:|---:|
| 5 | 0.552428 ± 0.059539 | 0.515220 ± 0.070198 | +0.037208 | 7/10 |
| 25 | 0.612174 ± 0.013057 | 0.608872 ± 0.014539 | +0.003302 | 8/10 |
| 50 | 0.617273 ± 0.007839 | 0.613500 ± 0.008332 | +0.003773 | 10/10 |
| 100 | 0.619513 ± 0.004770 | 0.614502 ± 0.004810 | +0.005011 | 10/10 |
| 200 | 0.623982 ± 0.003646 | 0.618943 ± 0.003824 | +0.005040 | 10/10 |

Control is `k=60, lambda=0`. Tuned schedule is `(30, 0.6)` at five shots and `(45, 0)` thereafter. Deviations are population standard deviations across episodes, not confidence intervals.

## Provenance limits

`final_vs_starter.json` is partially verified: its tuned arrays equal EXP-010 and arithmetic checks, but starter-array provenance is incomplete. `shrinkage_chain.json` is partially verified: top-k and shrunk arrays trace to `shrinkage.json`; raw arrays do not. Neither supplies the headline. Do not say 47/50 or 9.7%.

The unchanged local baseline gave Madrid CV `0.6281 ± 0.0043` and Amsterdam zero-shot `0.4433`; organiser-saved values are `0.6179 ± 0.0043` and `0.3427`. The cause is unidentified because package/input provenance is incomplete. This is a limitation, not exact reproduction.

## Gate4

- E1: **FALSIFIED**.
- E2: **INCONCLUSIVE**; +0.004953 at 25 shots did not meet +0.0100.
- E3: **FALSIFIED**, not successful.
- E3 execution/protocol/serialization checks passed, but full independent scientific validation stopped at `Original tree dirty` before prediction/metric reconstruction.

Keep infrastructure evidence—manifests, RNG binding, isolation, immutable-state checks, fresh workers, teardown, hashes, protected-state audits, NPZ validation, and scientific-payload identity—out of the central superiority claim.

## Required presentation sequence

Problem → few-shot domain shift → baseline → hypothesis → Madrid feature selection → prototype estimation → shrinkage → EXP-010 → EXP-008 support → negative results → reproducibility → limitations → conclusion → contributions.

## Claims prohibited

Universal superiority; perfect transfer; global generalisation; exact organiser reproduction; E3 success; independent EXP-010 replication; 47/50; 9.7% relative gain.

## Human checks

Confirm organiser upload/deadline/format/time limit, team names and speaking roles, and offline PPTX/PDF opening.
