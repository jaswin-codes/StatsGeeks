# E2 execution report - G4C-E2-008

## Status

- **Experiment status:** COMPLETED
- **Scientific verdict:** **INCONCLUSIVE / does not satisfy the predefined success criteria**
- **Episodes completed:** 60/60 (10 trials at each of 5, 10, 25, 50, 100, and 200 labels/class)
- **Validation status:** PASS (independent exact reload and reconstruction)
- **E3, E4, E5:** NOT RUN

## Final E2 metrics

Macro F1, mean +/- population SD (`ddof=0`):

| Labels/class | E2 | Frozen raw prototype | E2 - raw | Positive trials | Same-query frozen RF | E2 - RF |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 0.548537 +/- 0.034040 | 0.543686 +/- 0.032414 | +0.004851 | 8/10 | 0.443277 | +0.105261 |
| 10 | 0.567160 +/- 0.032958 | 0.564873 +/- 0.031178 | +0.002287 | 8/10 | 0.443272 | +0.123888 |
| **25** | **0.603550 +/- 0.015364** | **0.598598 +/- 0.017637** | **+0.004953** | **10/10** | **0.443265** | **+0.160285** |
| 50 | 0.609733 +/- 0.008129 | 0.607879 +/- 0.010059 | +0.001854 | 6/10 | 0.443144 | +0.166589 |
| 100 | 0.614526 +/- 0.007972 | 0.612898 +/- 0.009696 | +0.001628 | 7/10 | 0.442837 | +0.171689 |
| 200 | 0.616119 +/- 0.003516 | 0.614955 +/- 0.003558 | +0.001164 | 8/10 | 0.442582 | +0.173536 |

The predefined primary comparison is the matched 25-shot raw-prototype comparison. The all-target zero-shot baseline of 0.443273608786401 is contextual only; E2 uses support labels. The approved same-query frozen-RF comparison is shown above.

At 25 shots, E2 per-class mean F1 was `[0.653989, 0.558895, 0.619824, 0.581493]`; changes versus raw were `[+0.009064, +0.006474, +0.001553, +0.002720]` for classes 1-4. E2 also exceeded the U0 covariance control by +0.019931 mean macro F1 at 25 shots (7/10 positive trials).

## Success criteria (25 shots/class)

| Criterion | Result |
|---|---|
| Mean gain over raw >= +0.0100 | **FAIL** (+0.004953) |
| Positive raw gain in >=8/10 trials | PASS (10/10) |
| No mean per-class drop worse than -0.0200 | PASS (all changes positive) |
| Positive gain over same-query frozen RF | PASS (+0.160285) |

Because the required +0.0100 mean gain was not reached, E2 does **not** satisfy all predefined success criteria. Under the frozen verdict rule it is INCONCLUSIVE, not PROMISING.

## Validation and integrity

Independent verifier v2 passed all 60 records: exact source-state reconstruction, exact prediction reproduction, exact metrics/confusions, exact historical raw and U0 matches, RNG/manifest replay, query alignment, packet-hash reconstruction, worker teardown, 33 protected artifacts, and original-file cleanliness. Manifest SHA256 remained `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.

All 60 prediction NPZ files and per-episode worker/lifecycle evidence are preserved. Every worker teardown passed with no survivors. Candidate warnings: none. Candidate episode failures in the completed identity: none.

The initial verifier had an evaluator-only NumPy advanced-indexing error; it generated no candidate output and is preserved. A separately recorded v2 verifier corrected only that indexing expression and completed PASS without rerunning E2.

## Runtime and resources

- Prediction phase: 2570.396 s
- Primary coordinator total: 2570.845 s
- Independent verification: 141.810 s
- Peak worker RSS: 231,400 KiB (~226.0 MiB)
- Completed-run infrastructure status: all candidate workers and teardown checks passed

Earlier run identities 005-007 remain closed with their preflight/harness evidence and were not resumed or combined. The final complete identity had no worker infrastructure failure. No preprocessing, frozen data/model, manifest, runtime, algorithm, or hyperparameter was changed, and no E3-E5 execution occurred.
