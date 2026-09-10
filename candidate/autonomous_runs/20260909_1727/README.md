# ASTRA-AGF + coordinate local forest

Development-selected random-pixel candidate: **0.749299 ± 0.005716** at 200 shots/class (200 paired episodes), versus matched ASTRA **0.733037 ± 0.006106**; 200/200 paired wins. All 4000 paired prediction arrays reproduce after a fresh source refit.

**Caveat:** worst spatial direction drops to 0.644816 versus ASTRA 0.658183. ASTRA remains the historical incumbent; this is not an official universal-winner promotion. Query labels were evaluation-only, never selection/fitting. A separate 800-label development-support bank was excluded from all final queries; this is not an independent-city test.

Read FINAL_REPORT.md and SELECTION_LOCK.json. Full session evidence: `candidate/autonomous_runs/20260909_1727/`. The compact `candidate/experiments_agf/` bundle is explicitly packaged for later submission integration; it does not modify the existing submission or EXP-010.

Install the pinned requirements with the tested Python 3.14 environment. The trusted pickle is bound to the original ordered 25,992-row target pool and 60 supplied feature columns. Rebuild with label-free target features/coordinates and labelled source data for any different target pool; do not reuse this artifact on arbitrary isolated query rows.

Inference: python -I -B reproduce_best.py --support support.npz --out NEW_DIRECTORY
Support NPZ: indices, labels, budget (scalar); full ordered target pool is bound to pool_state.pkl.

Verification: python -I -B reproduce_best.py --verify --out NEW_DIRECTORY
Requires repository benchmark data only for verification, not inference.
