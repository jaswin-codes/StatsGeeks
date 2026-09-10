# ASTRA-AGF — locked, independently implemented gap-closing candidate

Repository root: `C:/Users/jaswi/Downloads/Hackathon3_StatsGeeks - Copy`.

**Recommendation: PROMOTE ASTRA-AGF for the full-unlabelled-pool/coordinate regime.** This does not change frozen EXP-010 or the presentation. EXP-H is a separate inductive backup.

## Verified headline

Four-class macro F1, population SD, support-complement query. Final recipe locked before100 new seed104729 episodes per budget:

| Shots/class | ASTRA-AGF mean ±SD |
|---:|---:|
|5|0.652903 ±0.011410|
|25|0.683153 ±0.013056|
|50|0.701560 ±0.009799|
|100|0.719199 ±0.007682|
|200|0.735239 ±0.005406|

On the competitor's exact20-draw seed42 convention,200-shot **0.737388 ±0.006339**, versus independently executed competitor108-feature fallback **0.736392 ±0.004722** (13/20 paired wins). This is numerical parity/near-parity, not proof of superiority to the missing tuned configuration. Competitor fallback remains better at5/50/100 on that convention.

Spatial200-shot: x-half **0.689672**, additional y-half **0.705083**; both above matched EXP-010/EXP-F. All these runs use the same city population, so new seeds do not constitute independent population validation.

## Read first

- `../competitor_forensics/FINAL_GAP_ANALYSIS.md`: decision, exact results, ablations, caveats.
- `../competitor_forensics/COMPARABILITY_AUDIT.md`: competitor claims versus reproduced mechanisms versus ours.
- `../competitor_forensics/FORENSIC_TRACE.md`: all ten audit questions, executable path, missing config, SHA.
- `FINAL_SELECTION.md` / `.json`: frozen recipe and predeclared verification plan.
- `ALL_RESULTS.csv`: every packaged result family, including negative arms and the initial failed-repeat result.
- `PAIRED_COMPARISONS.json`, `FINAL_CLASS_DIAGNOSTICS.json`, `final_verification.json`: full-precision evidence.

## Pinned inference API

Use **`astra_agf.py`**, not experimental defaults in `candidate_predict.py`. The wrapper pins physical-unit source alignment and local leaf1. Experimental defaults remain preserved for forensic replay of the leaf2 control.

```python
from pathlib import Path
import sys, pickle

root = Path(r"C:/Users/jaswi/Downloads/Hackathon3_StatsGeeks - Copy")
code = root / "candidate/experiments_2h_v2"
sys.path.insert(0, str(code))
from astra_agf import adapt_and_predict

# Only load a trusted local artifact; check FINAL_SHA256SUMS.json.
with (code / "astra_pool_state.pkl").open("rb") as f:
    state = pickle.load(f)

# support_indices index the ORIGINAL full Amsterdam pool row order.
# support_labels contains exactly n true labels per class, no query truth.
pred_all = adapt_and_predict(state, support_indices, support_labels, budget=n)
pred_query = pred_all[query_indices]  # query must exclude support
```

The artifact is bound to the exact25992-row pool and row ordering. Preserve support ordering for seeded-forest reproduction. No true-label anchoring is applied to support predictions.

For a new target pool, call `astra_agf.fit_pool(source_features, source_labels, source_coords, target_features, target_coords, source_mean, source_scale)`. Inputs are the original60 source-standardized columns in the supplied feature order; the source scaler is provided separately so physical units can be recovered. Source and target coordinates are **integer unit-lattice pixel keys**, not arbitrary metres/latitude/longitude. Source fitting receives NO target labels. It performs target-aware CORAL, so the state must be rebuilt for a different pool; it is not an inductive pointwise model.

If full unlabelled target covariates/coordinates are unavailable, use `h_predict.py` or keep EXP-010. Do not silently reuse Amsterdam's pool statistics for a different test distribution.

## Clean reproduction without ASTRA model caches

From the repository root, using the existing environment:

```text
.venv_baseline/Scripts/python.exe -I -B candidate/experiments_2h_v2/reproduce_locked.py --outdir candidate/astra_replay_001
```

Choose a **new output directory** on every invocation. Default:100 trials per budget, seed104729. `--trials 2` is a quick prefix smoke test; it is not the headline evaluation. The driver recomputes all ASTRA source/local fitting rather than loading their cached models. It retains the original repository's data-provenance validator, which needs `candidate/artifacts/exp010_stage1_madrid.pkl` and `data/preprocessed/preprocessed_data.pkl`; that frozen artifact's model is not used for ASTRA prediction. The direct pinned `fit_pool` API does not require an EXP-010 model.

The completed `locked_clean_replay/` run uses this standalone path. It checks its source prior and all matching support/query/prediction arrays against the frozen100-episode reference. `final_100_reproducibility.json` additionally covers all four paired methods,3000 arrays. Public source rebuild and artifact reload tests are in `candidate_interface*.json`.

Historical experiment scripts intentionally refuse output overwrites. Their `--repeat` paths have already been executed; do not delete inconvenient results to rerun them. Use the standalone driver with a new output directory, or reconstruct a new isolated evidence directory with the same original inputs.

## Recipe in six operations

1. Existing60 inputs plus immediate-grid means form120 source-prior features, separately in each city.
2. Global source-to-target CORAL; balanced200-tree source RF, leaf2, seed42.
3. One model-pseudo-class alignment/refit; no true target labels.
4. Local60-feature target covariance: rho=min(1,60/(4*n)) toward diagonal; ZCA with numerical ridge1e-7.
5. Support-only200-tree RF, leaf1, seed42; source weight20/(20+4*n).
6. Gaussian probability smoothing, self+8 nearest, exp(-distance²/2); no true-label anchors.

Forest tree fitting uses4 workers; prediction aggregation and BLAS are serial for deterministic floating-point behavior. `environment.json` records exact tested package versions. Cross-version/platform bit identity is not promised.

## Scientific limitations

**Transductive, audit-selected exploration**, not an untouched organizer test. True query labels were used for scoring/research selection, never fitting/prediction. Full unlabelled pool statistics, pseudo-labels and spatial context enter the model. Spatially autocorrelated random-pixel evaluation is not automatically leakage; neither does prediction-only smoothing eliminate adjacency benefits. Same-building/parcel separation cannot be established without IDs.

Original competitor tuned `overnight_best.json` is missing. Our original-code fallback reproduction is explicitly labelled, not substituted for their exact claim. Source/target oldest-class boundaries differ. Mid-budget competitor differences remain. Per-class diagnostics include worsening C3→C4 confusion despite overall improvement; no post-hoc class thresholds were applied.

## Failure and artifact retention

- Initial competitor script fails on missing `overnight_best.json`; log retained.
- Initial data audit called an unavailable method on the project's minimal scaler shim; affine inverse used in the retained successful retry.
- Initial stage1 omnibus repeat differs by one prediction in12 arrays at machine-epsilon forest ties. Failed result/log retained; stable serial prediction aggregation introduced before final selection. Every final headline check passes.
- Large historical source model `.pkl` files and prediction `.npz` files are deliberate evidence. Do not unintentionally commit the entire multi-GB experiment directory. Operational inference needs the four small modules (`astra_agf.py`, `candidate_predict.py`, `stage2_models.py`, `models.py`), compatible dependencies, and the target-bound `astra_pool_state.pkl`. New-pool fitting additionally needs the source data/scaler/coordinates, not the historical experimental model files.
- Presentation and frozen EXP-010 remain unchanged.
