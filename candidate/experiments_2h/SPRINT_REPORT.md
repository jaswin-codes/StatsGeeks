# ASTRA controlled sprint report

## Executive result

**Final recommendation: KEEP EXP-010**

Frozen EXP-010: **0.5524 / 0.6122 / 0.6173 / 0.6195 / 0.6240** at5/25/50/100/200 shots per class. Five shots means20 labelled Amsterdam samples total.

Strongest new scientific signal: **EXP-F regularized support-covariance prototypes**, fixed before scoring. At200 shots: **0.658664 ± 0.004417**, gain **+0.034681**,10/10 paired wins. At25 shots: **0.638010 ± 0.014197**, gain **+0.025835**,10/10 wins. It improves all ten random episodes at each budget25–200, and improves spatial means at those budgets. However, its5-shot spatial performance is materially worse than frozen EXP-010. No replacement, hybrid schedule, submission update or promotion was performed.

These are predeclared comparisons on the **reused seed31337 audit pool**, not newly independent confirmation. Descriptive ranking is not model selection. Selecting the best-looking arm for deployment from this report would be **EXPLORATORY — AUDIT-SET SELECTION**. No such selection was made.

### All branches, including negative/blocked outcomes

“Best result” below highlights the most informative new positive signal, not a fitted budget-specific schedule. SD is population SD; all exact episode-level values are preserved.

| Experiment | Best result | Budget/class | Gain vs EXP-010 | Reproducible | Promote? |
|---|---:|---:|---:|---|---|
| A source/local |0.559415 ±0.036110 (alpha1)|5|+0.006987|Exact repeat|No:5/10 wins; source endpoint, not a blending victory|
| B dimension × shrinkage |0.612891 ±0.009887 (compact,lambda0.4)|25|+0.000717|Exact repeat|No: marginal; larger-budget shrinkage hurts|
| C class diagnostics |Classes2+3 explain83.8% of5-shot macro variance|5|Diagnostic, not a candidate|Exact repeat|No safeguard fitted|
| D spatial, A alpha0.5 |0.603008 ±0.024135|25|+0.018871 vs spatial EXP010; random gain+0.001947|Exact repeat|No: fixed alpha0.5 loses random at4/5 budgets|
| E temporal3 |0.560998 ±0.061231|5|+0.008570|Exact repeat|No: higher5-shot SD; gains at25/200 only+0.001282/+0.001773|
| F regularized covariance |0.658664 ±0.004417|200|+0.034681|Exact repeat plus label-free CLI|No automatic promotion; strongest review candidate|
| G transductive |BLOCKED|N/A|N/A|Not run|No explicit target-pool permission|

## EXP-F results and spatial stress

| Shots/class | Random F1 ± population SD | Random gain | Random W/L/T | Spatial F1 ± population SD | Spatial gain | Spatial W/L/T |
|---:|---:|---:|---|---:|---:|---|
|5|0.552745 ±0.036466|+0.000317|6/4/0|0.507618 ±0.051281|-0.025769|3/7/0|
|25|0.638010 ±0.014197|+0.025835|10/0/0|0.613639 ±0.024090|+0.029501|8/2/0|
|50|0.649538 ±0.009417|+0.032265|10/0/0|0.629634 ±0.013783|+0.015390|8/2/0|
|100|0.653269 ±0.005811|+0.033757|10/0/0|0.635870 ±0.013664|+0.019061|9/1/0|
|200|0.658664 ±0.004417|+0.034681|10/0/0|0.636970 ±0.013747|+0.019212|10/0/0|

Random paired wins:46/50. No claim that50 highly overlapping query episodes are50 independent datasets.

Metric: source-standardized, Madrid-importance-weighted compact features; labelled-support class means; pooled within-class support covariance C=R.T@R/(4*shots−4); distance uses inverse(0.5*C +0.5*trace(C)/k*I +1e−8*I). Fixed k30 at5, k45 otherwise. No source prototype shrinkage, query covariance, metric search or new RF fitting. Compared with Euclidean support prototypes this tests the distance metric directly. At5 shots the EXP010 comparison additionally includes its source prototype shrinkage, so do not attribute that difference solely to covariance.

## Scientific findings

1. **Does source/local blending improve transfer?** Slightly at25 shots: alpha0.5 gives0.614121 versus0.612174,7/10 wins. At5 shots the source-geometry endpoint wins the grid rather than a mixture; alpha0.75 gives0.558754, only+0.006326. Fixed alpha0.5 loses against EXP010 at four budgets. No credible overall blending promotion.

2. **Does source reliance decrease as labels increase?** **Yes descriptively in this grid**, with best-looking alphas1.0/0.5/0/0/0. This was not selected or rerun as a schedule and is not independently validated optimal reliance. Historical development seed2026 uses the same labelled Amsterdam pool, so it cannot supply label-disjoint confirmation. Source probabilities use the frozen Madrid offsets recentered using support; they are not a zero-shot RF or the full EXP010 endpoint. Both endpoints share source-derived representation; the local classifier itself fits only labelled support.

3. **Does dimension reduction interact with shrinkage?** A small positive interaction appears at all budgets: +0.001145/+0.002485/+0.003315/+0.002672/+0.003437 for the lambda0/0.4 factorial. At5 shots compact selection alone contributes+0.007949 versus all60/no shrinkage, while lambda0.4 contributes+0.017080 within compact space. At50–200 shrinkage remains harmful despite the positive interaction. Frozen lambda0.6 at5 matches exactly. Detailed paired interaction effects are saved; no large sweep occurred.

4. **Which class limits low-shot performance?** Class2 has the weakest mean F1 (0.474917); class3 contributes42.7% of macro-F1 variance and class2 contributes41.2%. Their class-F1 SDs are0.122255 and0.118206 versus class1 SD0.032462. Dominant confusion by count is1↔2, with normalized direction2→1. Class1 is not the main variance source. Poor5-shot trials are4 and7 under the predeclared mean−SD diagnostic. EXP010 improves mean F1 for all four classes at5 shots versus the joint control, but wins per class are8/7/5/8 of10, not uniformly positive. Against compact-local (isolating source shrinkage), gains are+0.027528/+0.004139/+0.082072/+0.003296 with wins8/6/8/4; class4 often loses slightly. At25 shots class3 loses0.000259 against the joint control; later budgets show small average gains for all classes. No defensible class-specific safeguard was established or implemented.

5. **Does the candidate survive spatial separation?** EXP-F retains positive mean gains at25–200, including+0.029501 at25 and+0.019212 at200. At200 spatial retains about55% of the random gain; at50 about48%, so robustness is partial, not complete. **At5 shots it is fragile**, losing0.025769 versus EXP010. The spatial evaluator uses geographic grid IDs from the cached data; organiser Notebook2 §2.3 identifies them as rounded UTM/30m. Fixed median east/west split, alternating support side, query opposite side with10-key (~300m) exclusion. No model receives pool statistics. This combines regional shift, class-composition shift and separation; two regions are not comprehensive spatial CV. Random-vs-spatial drops are not paired on identical queries. Spatial evidence does not replace official results.

6. **Did temporal features help?** Three Madrid-standardized late−early contrasts (NIR/SWIR1/SWIR2) gave+0.008570/+0.001282/+0.001773 at5/25/200, with9/8/10 wins. The5-shot SD increased from0.059539 to0.061231. This is a small deterministic re-expression/reweighting of existing temporal information, not a new information source. Stopped at the initial three budgets: no audit-triggered expansion or broad feature rebuild.

7. **Did covariance regularization help?** Yes, substantially at25–200, unlike diagonal-only normalization. Full regularization accounts for feature correlations while shrinking unstable support estimates toward an isotropic metric. No need for a large metric-learning system. The5-shot spatial weakness cautions against replacing the entire frozen system.

8. **Was transductive alignment permitted?** Not explicitly in the locally available organiser instructions. Notebook1 §1.5/§1.7 describes small-labelled-support adaptation; docs/MASTER_PLAN.md line74 records target-pool privileges as unresolved. **EXP-G BLOCKED — competition information-access rules unclear.** No alignment executed.

9. **Strongest scientifically defensible new candidate?** The fixed EXP-F regularized support-covariance arm, **for review**, especially25–200 shots. No audit-selected alpha schedule, covariance sweep, class safeguard or EXP010/F hybrid was created. Ranking completed arms is descriptive; there is no independent winner confirmation.

## Reproducibility and integrity

- Frozen artifact SHA256: `2f4dc0f7a84ea54e967d7a96573b349331e1777ddb0a4a46e4925cad7bd6d266`.
- Data SHA256 matched the frozen artifact: `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`.
- Every random baseline episode matches frozen joint_sweep.json to1e−12, using the official frozen prediction interface, not a separately refitted RF.
- Seed31337, trials0–9; original nested support sampler and non-support query complement. Class order1–4. All arms predict before the scorer slices episode query labels. Sampler uses labels only to construct the original stratified supports; predictors have no query-label parameter. No query-label fitting or configuration selection.
- Exact predictions, support/query indices, macro/class F1, confusion counts/proportions, class counts, population SD, paired differences and wins/losses/ties saved. Numerical tie threshold1e−12. Configuration includes code/plan/data/artifact hashes and library versions.
- All six computational branches plus the fixed spatial F follow-up repeated with `python -I -B`; every prediction array and episode score matched exactly. BLAS threads fixed to1.
- Additional five independent EXP-F CLI processes reproduce full-query trial0 at every budget from feature-only query NPZ. Query label keys explicitly rejected. Test processes run outside the repository root. See `expF_covariance/interface_test/verification.json`.
- Initial isolated pickle load required an explicit repository path for the trusted existing `working.*` class. No environment repair or preprocessing change was made. Read-only imports only; bytecode disabled.
- Protected before/after hashes: **1,579 files checked; zero changed or missing**. Existing dirty Git state was preserved. Includes frozen evidence, Gate4 working evidence, data, notebooks, presentation and submission dry-run. No original artifacts or historical results rewritten.

**FROZEN EXP-010 INTEGRITY: PASS**

**NO QUERY-LABEL SELECTION: PASS** — configurations fixed before scores; no winner/schedule adopted. Audit tables and diagnostic rankings remain exploratory, not independent confirmation.

**CLEAN-PROCESS REPRODUCIBILITY: PASS**

## Execution, limits and deviations

Order: A → clean repeat → B → clean repeat → C → clean repeat → D → clean repeat → F → clean repeat → E → clean repeat → fixed-rule spatial follow-up of all F arms → synthesis. Class metrics were produced during C; narrative interpretation was assembled in final synthesis.

The nominal two hours was treated as a ceiling, not a requirement to keep tuning. All primary runs took about3–19 seconds each using frozen source state and a single-threaded small-matrix pipeline. Packaging completed14.3 minutes after the protection snapshot, plus preliminary inspection and final synthesis. Exact wall/process times are in timing.json and results files. No experiment approached its cap. Work ended early rather than exhausting time with new audit-driven configurations.

Predeclared A alpha0.5 was used for D because A/B had no promotion-quality candidate; no best-alpha selection. Strong F results motivated a separately documented spatial follow-up of **all three** unchanged F metrics using the already fixed D rule. This is explicitly exploratory and does not create a new holdout. E used a fixed three-feature append rather than replacing ranked features; interpretation and scope documented before scoring. G was blocked without disrupting safe inductive branches.

## Files created

All outputs are under `candidate/experiments_2h/`:

- `PLAN.md`, `run.py`, `preflight.py`, `summarize.py`, `spatial_f.py`, `package.py`, this report.
- `expA_source_local/`, `expB_dim_shrink/`, `expC_class_diagnostic/`, `expD_spatial/`, `expE_temporal/`, `expF_covariance/`: local script entrypoint, configuration, original/repeat raw episode results, compressed predictions and indices, method notes/tables, exact reproducibility checks.
- Additional A findings, B factorial effects, C full class diagnostics, D random/spatial contrasts, F metric effects and spatial raw/repeat evidence.
- `expF_covariance/candidate_predict.py`, `test_candidate.py`, `CANDIDATE.md`, `SPATIAL_ADDENDUM.md`, `interface_test/`: unpromoted clean-process review package, not a submission replacement.
- `expG_transductive/README.md`: blocked-rule rationale.
- `protected_before.json`, `integrity.json`, `git_status_before.txt`, `environment.txt`, `start.json`, `timing.json`, execution logs.

## Final recommendation

**KEEP EXP-010**

EXP-F is a strong, reproducible, inductive improvement signal at25–200 shots, worthy of review and genuinely independent validation. It is not yet a scientifically safer all-budget replacement:5-shot spatial robustness regresses, and the winner was identified descriptively on an already reused audit pool. Do not combine EXP010 at5 with EXP-F above5 based on this audit; that would create an unvalidated selected schedule. No submission, presentation, written justification, official result or frozen artifact was changed.
