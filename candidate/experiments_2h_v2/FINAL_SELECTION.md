# Final candidate lock — ASTRA-AGF

**No more optimization after this lock.** Subsequent runs are reproduction, new-episode stability checks, protocol/spatial audits and packaging only.

Selected recipe:
- Original provided60-feature input; source-fitted scaler inverted to physical feature units.
- Source prior representation120: original60 +immediate-grid averages of those60, in each city's own unlabelled geography.
- Source RF200 trees, balanced, leaf2, sqrt features, seed42. Global CORAL followed by ONE pseudo-class alignment/refit. No true target labels in either step.
- Local representation remains60. Full-target covariance shrunk toward its diagonal by rho=min(1,60/(4*n)); symmetric inverse square root, numerical ridge1e-7.
- Support-only local RF200 trees, default leaf1, balanced, sqrt features, seed42. Local leaf1 versus conservative leaf2 was the final predeclared capacity control; it improved all five audit means without changing the source model.
- Source probability weight20/(20+4*n); no budget-specific tuning table.
- Gaussian spatial smoothing on self+8 nearest pool pixels, exp(-distance^2/2), normalized. Unit pixel-key length scale, no true-label anchoring.
- Stable serial probability aggregation, parallel tree fitting; BLAS thread limit1.

Selection rationale: balances low-shot strength, high-shot growth, clear staged ablations, availability from current data, and simplicity versus adding raw temporal data or fitting multiple source-basis ensembles. Both source and local alignment use the same physical coordinate frame. This is an internal **audit-selected transductive candidate**, not an untouched organizer test result.

Locked ten-episode audit means (5→200):
.651044 / .688937 / .700289 / .716997 / .733731.
All50 paired comparisons beat EXP-010. Spatial/fresh leaf1 checks are still required; their results must not trigger recipe tuning. If they fail materially, recommend the already tested conservative recipe or keep the frozen method, not an unreported retry.

Final verification plan fixed now:
1. Exact clean-process leaf1 replay and source refit already separately covered; public API reconstruction test.
2. Existing seed8675309 and buffered x-half diagnostic on this exact recipe.
3. **100 new nested trials per budget, seed104729**, evaluated once with EXP-010, EXP-F and inductive EXP-H controls on identical supports/queries. Same city population: episode stability, NOT independent population validation. Do not tune on these results.
4. Additional10-trial buffered y-half spatial protocol, seed104729, geometry-only partition with10-key-unit buffer; no episode discard. Check class availability explicitly.
5. Query-label access/interface, probability normalization, frozen file hashes and exact query/support separation checks.

Inductive fallback: `h_predict.py` EXP-H_mean. Do not silently use this transductive artifact when the evaluator supplies only isolated query rows or lacks target coordinates. Rebuild target-bound state for a new full pool.
