"""Read-only result packaging and final integrity checks; never selects a new model."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,csv,hashlib,datetime,pickle
import numpy as np
from sklearn.metrics import f1_score
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];F=R/'candidate/competitor_forensics';sys.path[:0]=[str(H),str(R)]
from candidate.experiments_2h.run import setup,save,sha
from astra_agf import adapt_and_predict
B=[5,25,50,100,200]
def read(p):return json.loads(p.read_text())
def pair(a,b):
 d=np.asarray(a)-np.asarray(b)
 return {'mean_delta':float(d.mean()),'sd_delta':float(d.std()),'wins':int((d>1e-12).sum()),'losses':int((d< -1e-12).sum()),'ties':int((np.abs(d)<=1e-12).sum())}
def vals(obj,b,m=None):return [r['f1']for r in obj['records']if r['budget']==b and(m is None or r.get('method')==m)]
def fmt(r):return f"{r['mean']:.6f} ± {r['sd']:.6f}"
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|',*['| '+' | '.join(map(str,r))+' |'for r in rows]])

def main():
 report=F/'FINAL_GAP_ANALYSIS.md';assert not report.exists(),'Never overwrite a packaged report'
 final=read(H/'final_100.json');audit=read(H/'capacity_leaf1_audit.json');fresh=read(H/'capacity_leaf1_fresh.json');spatial=read(H/'capacity_leaf1_spatial.json');ys=read(H/'final_yspatial.json');old=read(H/'audit.json');old_sp=read(H/'spatial.json');proto=read(H/'final_competitor_protocol.json');comp=read(F/'reproduction_both.json');comp60=read(F/'reproduction_fallback.json');comp_audit=read(F/'paired_audit.json');comp_sp=read(F/'paired_spatial.json');cfg=read(H/'FINAL_SELECTION.json');prox=read(F/'proximity_extended.json')
 checks=['physical_source_reproduction','source_basis_audit_reproducibility','capacity_leaf1_audit_reproducibility','candidate_interface','candidate_interface_reload','final_100_reproducibility','final_yspatial_reproducibility','final_competitor_protocol_reproducibility','h_interface_reproduction']
 for n in checks:assert read(H/(n+'.json'))['pass'],n
 clean=read(H/'locked_clean_replay/run.json');assert clean['pass'] and clean['source_trained_from_scratch'] and clean['reference_arrays_exact']==1500 and clean['trials_per_budget']==100
 for p,h in cfg['files_sha256'].items():assert sha(H/p)==h,p
 protected=read(F/'protected_before.json');changed=[p for p,h in protected.items()if sha(R/p)!=h]
 frozen_core=[p for p in changed if not p.endswith('.onetoc2')];assert not frozen_core,frozen_core
 # Exact canonical protocol replay, not just agreement after six-decimal rounding.
 canonical=read(R/'candidate/artifacts/joint_sweep.json')
 for b in B:np.testing.assert_allclose(vals(old,b,'EXP010'),canonical['audit'][str(b)]['tuned_trials'],rtol=0,atol=1e-12)
 with np.load(R/'candidate/experiments_2h/expF_covariance/predictions.npz')as previous,np.load(H/'audit.npz')as current:
  for b in B:
   for t in range(10):np.testing.assert_array_equal(previous[f'b{b}_t{t}_regularized'],current[f'b{b}_t{t}_EXPF'])
 # Test the pinned, non-experimental wrapper against an existing exact episode.
 _,d=setup()
 with(H/'astra_pool_state.pkl').open('rb')as f:state=pickle.load(f)
 data=np.load(H/'capacity_leaf1_audit.npz');s=data['b5_t0_s'];q=data['b5_t0_q'];p=adapt_and_predict(state,s,d['y_amsterdam'][s],5);np.testing.assert_array_equal(p[q],data['b5_t0_pred'])
 comparisons={}
 for b in B:
  comparisons[b]={'final100_vs_'+m:pair(vals(final,b,'ASTRA_AGF'),vals(final,b,m))for m in ['EXP010','EXPF','EXPH']}
  comparisons[b].update({'audit_vs_EXP010':pair(vals(audit,b),vals(old,b,'EXP010')),'audit_vs_EXPF':pair(vals(audit,b),vals(old,b,'EXPF')),'audit_vs_competitor_mechanism':pair(vals(audit,b),vals(comp_audit,b)),'spatial_x_vs_EXP010':pair(vals(spatial,b),vals(old_sp,b,'EXP010')),'spatial_x_vs_EXPF':pair(vals(spatial,b),vals(old_sp,b,'EXPF')),'spatial_x_vs_competitor_mechanism':pair(vals(spatial,b),vals(comp_sp,b))})
 save(H/'PAIRED_COMPARISONS.json',comparisons)
 # Machine-readable catalogue: all methods, including negative arms and original failed repeat.
 rows=[];episode_count=0
 for path in sorted(H.glob('*.json')):
  obj=read(path)
  if not isinstance(obj,dict)or'records'not in obj:continue
  records=obj['records'];episode_count+=len(records)
  for b in sorted({r['budget']for r in records}):
   for m in sorted({r.get('method','ASTRA_AGF')for r in records if r['budget']==b}):
    rr=[r for r in records if r['budget']==b and r.get('method','ASTRA_AGF')==m];v=np.array([r['f1']for r in rr]);rows.append({'file':path.name,'method':m,'budget':b,'episodes':len(v),'mean':float(v.mean()),'population_sd':float(v.std()),'repeat':('_repeat'in path.stem)})
 with(H/'ALL_RESULTS.csv').open('x',newline='')as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 # Final class diagnostics, no classifier changes.
 diagnostics={'final100':{},'source_priors':{}}
 for b in B:
  diagnostics['final100'][b]={m:{'mean_class_f1':final['summary'][str(b)][m]['class_f1_mean'],'summed_confusion':np.sum([r['cm']for r in final['records']if r['budget']==b and r['method']==m],axis=0).tolist()}for m in ['ASTRA_AGF','EXP010','EXPF','EXPH']}
 for file in ['conditional_priors.npz','source_context_priors.npz','physical_source_priors.npz']:
  with np.load(H/file)as ar:
   diagnostics['source_priors'][file]={k:f1_score(d['y_amsterdam'],ar[k].argmax(1)+1,labels=[1,2,3,4],average=None,zero_division=0).tolist()for k in ar.files}
 save(H/'FINAL_CLASS_DIAGNOSTICS.json',diagnostics)
 finaltable=table(['Shots/class','ASTRA-AGF:100 new episodes','EXP-010','EXP-F','EXP-H','Wins vs010/F/H'],[[b,fmt(final['summary'][str(b)]['ASTRA_AGF']),fmt(final['summary'][str(b)]['EXP010']),fmt(final['summary'][str(b)]['EXPF']),fmt(final['summary'][str(b)]['EXPH']),'/'.join(str(comparisons[b]['final100_vs_'+m]['wins'])for m in ['EXP010','EXPF','EXPH'])+' of100']for b in B])
 audittable=table(['Shots','ASTRA audit10','Delta vs frozen010','Delta vs EXP-F','Wins vs010/F'],[[b,fmt(audit['summary'][str(b)]),f"{comparisons[b]['audit_vs_EXP010']['mean_delta']:+.6f}",f"{comparisons[b]['audit_vs_EXPF']['mean_delta']:+.6f}",f"{comparisons[b]['audit_vs_EXP010']['wins']}/{comparisons[b]['audit_vs_EXPF']['wins']} of10"]for b in B])
 comptable=table(['Shots','Latest competitor CLAIM','Original-code108 fallback20','Our LOCKED method,same20 draws','Our delta vs reproduced','Paired W/L'],[[b,{'5':'.6622 ±.0028','25':'.6769 ±.0055','50':'.7035 ±.0089','100':'.7207 ±.0074','200':'.7373 ±.0053'}[str(b)],fmt(comp['budgets'][str(b)]),fmt(proto['summary'][str(b)]),f"{proto['summary'][str(b)]['delta_vs_competitor']:+.6f}",f"{proto['summary'][str(b)]['paired_competitor_wins']}/{proto['summary'][str(b)]['paired_competitor_losses']}"]for b in B])
 spatialtable=table(['Shots','ASTRA x-half10','EXP-010 x','EXP-F x','Competitor fallback x','ASTRA y-half10','EXP-010 y','EXP-F y'],[[b,fmt(spatial['summary'][str(b)]),fmt(old_sp['summary'][str(b)]['EXP010']),fmt(old_sp['summary'][str(b)]['EXPF']),fmt(comp_sp['summary'][str(b)]),fmt(ys['summary'][str(b)]['ASTRA_AGF']),fmt(ys['summary'][str(b)]['EXP010']),fmt(ys['summary'][str(b)]['EXPF'])]for b in B])
 htable=table(['Shots','EXP-F','H covariance:k','H covariance:4k','H covariance:1/2','H +shrunk means','Hmean wins vsF'],[[b,fmt(old['summary'][str(b)]['EXPF']),fmt(old['summary'][str(b)]['H_k']),fmt(old['summary'][str(b)]['H_4k']),fmt(old['summary'][str(b)]['H_half']),fmt(old['summary'][str(b)]['H_mean']),pair(vals(old,b,'H_mean'),vals(old,b,'EXPF'))['wins']]for b in B])
 blendtable=table(['Source alpha',*map(str,B)],[[a,*[f"{old['summary'][str(b)][f'blend_{a:.2f}']['mean']:.6f}"for b in B]]for a in [0,.25,.5,.75,1]])
 classrows=[[m,*[f'{v:.6f}'for v in final['summary']['200'][m]['class_f1_mean']]]for m in ['EXP010','EXPF','EXPH','ASTRA_AGF']]
 text=f'''# Executive Verdict

**PROMOTE ASTRA-AGF for the open-scope, full-unlabelled-pool regime.** Keep frozen EXP-010 intact and EXP-H as an explicitly inductive backup. Do not silently run a transductive artifact on isolated queries without the required pool/coordinates.

We closed the headline high-shot gap: the independently implemented method scores **{fmt(proto['summary']['200'])}** on the competitor's exact20-episode convention, versus **{fmt(comp['budgets']['200'])}** for the independently executed108-feature fallback mechanism. Paired difference **{proto['summary']['200']['delta_vs_competitor']:+.6f}**,13/20 wins. It numerically matches the claimed .7373, but this tiny difference is **not evidence of superiority to the unrecovered tuned pipeline**.

The locked method then scores **{fmt(final['summary']['200']['ASTRA_AGF'])}** across **100 newly seeded episodes**, with gains **{comparisons[200]['final100_vs_EXP010']['mean_delta']:+.6f}** versus EXP-010 and **{comparisons[200]['final100_vs_EXPF']['mean_delta']:+.6f}** versus EXP-F on exactly those episodes. These are support-sampling stability checks on the SAME target population, not an independent organizer test or a new-population holdout. No model changes followed the final lock.

## 1. What produced the competitor's ~0.73?

Repository `C:/Users/jaswi/JaswinHackathon`, remote `ubayd-hattas/Data_Science_Hackathon`, branch `israel-transfer-pipeline`, SHA **cf9af6cffea292af9460bf572de33c32a10212d9**. Main branch was NOT this method. See `FORENSIC_TRACE.md` and the detached snapshot.

Actual path: raw Landsat annual panels →108 temporal/context features → globally CORAL-aligned Madrid RF →two pseudo-class alignment iterations →full-target budget-shrunk ZCA, optional config-dependent PCA →support-only local RF →source/local probability blend →inverse-distance spatial probability smoothing →support-complement macro F1.

**The headline is a200-shot/class MEAN over20 episodes.** Earlier .73 was .7259±.0049 with uniform smoothing. The latest notebook/table is .7373±.0053 after distance weighting, not a best episode, an across-budget average, or an untouched test-half result. All100 final episodes means20 at EACH of five budgets. The final full-pool report includes the earlier tuning half; later refinements also used target evaluations.

`results/overnight_best.json` is missing. The unmodified polish script fails on exactly that missing file; original raw data equivalents exist locally. The winning forest had500 trees according to git history, but its complete config is not recoverable. Our250-tree explicit fallback executes the original feature/alignment/evaluation functions and nearly reproduces the headline; it is NOT falsely labelled an exact tuned-config reproduction. Literal60-feature fallback already reaches **{fmt(comp60['budgets']['200'])}** at200. The extra48 features are not necessary for approximately .73 at high budget.

## 2. Is it comparable to our result?

**PARTIALLY COMPARABLE** to frozen EXP-010/EXP-F: same pixel population/classes/budgets/metric/query-complement task, but different information regime, features, spatial processing, episode RNG/count and selection history. Both cities' pixel IDs/order and labels match exactly in our reconstructed inputs; original competitor raw-file hashes are unavailable. Our subsequent comparison to the reproduced mechanism uses the SAME episodes and transductive access regime.

{comptable}

The final competitor20 convention resets default_rng(42) per budget, samples each class without replacement, and queries every remaining pixel. Ours initially used10 nested permutation-prefix episodes, seed31337. All report SDs are population SD (ddof0). Forest seed42 is fixed across trials; SD principally reflects support sampling, not refitting random source seeds. RF's internal bootstrap replacement is separate from the without-replacement support sampling.

Our final method is slightly better than the fallback mean at25 and200, and worse at5/50/100 under this common20-draw convention. Do not report universal competitor dominance. Exact comparability scorecard and ten explicit audit answers: `COMPARABILITY_AUDIT.md`, `FORENSIC_TRACE.md`.

## 3. What explains the gap?

It is **not just an episode-count effect or hidden target ground-truth labels**. Changing episode convention shifts the common60-feature pool-RF+uniform-smoothing200 mean .722616→.725606, whereas its paired gain over EXP-010 under that convention is .100396.

The strongest explanation is moving from a compact shared-covariance prototype family to a richer local classifier plus transductive distribution and spatial information. On our original episodes, RF60 alone gives .689729 versus EXP-F .658664; this comparison changes classifier AND effective dimensionality, so it is not a pure capacity causal estimate. The same60-feature LR gives .683275. The subsequent RF60→pool-RF60→uniform smoothing sequence, holding other settings fixed, gives .689729→.694923→.722616. This isolates the latter two gains more cleanly.

A one-iteration physical-unit class-conditional source alignment lifts its global prior .558601→.629725 zero-shot; no true target labels enter that update. Better priors mainly help low budgets; local learning and smoothing explain most high-budget gain. Extra target-only context features help an unsmoothed RF but add little once smoothing is present, so they were not retained in the local head.

## 4. Which competitor ideas transferred successfully?

- Full-target covariance geometry, explicitly transductive.
- Nonlinear support-only RF in the provided60-feature representation.
- Source/local probability blending with a smooth effective-sample-size weight.
- Class-conditional source alignment from model-generated pseudo-labels.
- Spatial context in the source prior, and prediction-only weighted smoothing.
- Budget-aware local decorrelation: suppress rotations when labels are fewer than features, gradually allow them as support grows.

Our code imports no competitor implementation. We use120 source-prior features derived from existing60+coordinates, ONE conditional alignment iteration, a dimension/sample-ratio covariance schedule,200 trees, and a Gaussian graph—not their108 raw-derived feature list, target-tuned shrinkage/blend schedule, unknown500-tree config, or inverse-distance formula.

## 5. Which did not?

Pure target-pool prototype whitening harms5-shot performance (.499901 vs EXP-F .552745). Covariance-only EXP-H borrowing hurts low shots; adding shrinking source mean geometry repairs it but does not approach the nonlinear/spatial branch at high shots. Larger source covariance weights are not consistently beneficial. A stronger source probability weight hurts high budgets. A second conditional iteration increased zero-shot F1 in the initial60-feature source experiment but hurt the blended/spatial method; the final method uses one iteration. Immediate-grid-only uniform smoothing did not beat the weighted field. Doubling target-local features to120 did not materially improve the already smoothed classifier and was rejected. Alternative ZCA frames/schedules produced modest, budget-dependent changes, not a magic .1 gain.

The initial omnibus clean repeat failed on12 non-headline arrays, each differing by one prediction. Affected RF top-two probabilities differed at approximately5.55e-17; serial aggregation fixes this numerical tie sensitivity. All failures and diagnostic logs remain. The final recipe/source fits/public interface/complete new100-episode suite have exact clean-process reproduction checks.

### EXP-H adaptive covariance investigation

Three predeclared metric settings: source pseudo-count k,4k, or fixed1/2; source covariance trace matched to support covariance, then the existing half-identity regularization. A separate mean-transfer arm uses .6*k/(k+N_support) of centred source offsets. No query covariance for these H arms.

{htable}

The locked100-episode H results appear in section7. `h_predict.py` is a separate inductive interface, with30 exact episode-array checks and20 query-batch invariance checks. H is a modest improvement, not the explanation for .73.

### Exactly requested source/local alpha control

Raw60 local RF; global source prior; means on10 shared original episodes. Pooled-local variants also retained in ALL_RESULTS.csv.

{blendtable}

Point-estimate best raw alpha is .50 at5, .25 at25–100, and0 at200. These are audit-exploratory point estimates, not independent validation. Final alpha=20/(20+4*n) is a predetermined continuous pseudo-count heuristic, not a post-selected per-budget lookup table.

## 6. Best new method

**ASTRA-AGF: adaptive-geometry forest with transductive source prior and Gaussian spatial smoothing.**

1. Recover physical units from the existing Madrid scaler; no additional raw feature engineering is required.
2. Build120 source-prior features:60 originals plus immediate-grid averages, separately within each city.
3. Globally match source/target covariances and means; fit a balanced200-tree source RF (leaf2); perform one pseudo-class alignment/refit.
4. Keep local input at60. Use target covariance `(1-rho)*C + rho*diag(C) +1e-7*I`, rho=min(1,60/(4*n)), and symmetric whitening.
5. Fit a200-tree support-only RF, default leaf1, seed42. A final leaf1-versus-leaf2 control improved all five audit means without changing source training.
6. Blend with source weight20/(20+4*n); Gaussian-smooth self+8 nearest pool predictions, unit grid-key length scale. No true-label anchors.

Fixed source alignment jitter is a numerical PSD safeguard, not a target-tuned search parameter. Raw-versus-standardized alignment also changes the ridge's relative scale; observed frame effects cannot be attributed to rotation alone. Inverse covariance square roots are not PCA compression: dimensions remain120/60.

Pinned public entry point: `astra_agf.py`. Experimental `candidate_predict.py` exposes alternatives for the archived ablation, so use the pinned wrapper or the saved final pool state, not an omitted experimental default. The wrapper itself is checked against an exact stored prediction array.

## 7. Exact results

### Primary: locked recipe,100 new support-sampling trials per budget

Seed104729,500 total episodes, nested support/complement query, no discarded trials. No tuning after lock. Wins are against the corresponding100 paired controls, not against historical means.

{finaltable}

### Original10 shared audit trials (seed31337)

{audittable}

The separate10-trial seed8675309 check gives (5→200): {', '.join(fmt(fresh['summary'][str(b)])for b in B)}. These, the100 new draws, and the competitor-protocol draws all reuse the SAME target population; no untouched organizer test score is claimed.

## 8. Spatial robustness

Both half-split protocols exclude query pixels within10 grid-key units of the split boundary; support comes from the other half. X-axis uses the historical31337 setup; additional Y-axis uses104729. Each has10 trials alternating sides. These are two geographic partition diagnostics, NOT20 independent cities or building-disjoint cohorts. Unlabelled pool statistics still include both halves, consistently with the transductive regime.

{spatialtable}

At200, ASTRA falls from random100-trial .735239 to x-half .689672 and y-half .705083: substantial spatial sensitivity remains, but both are materially above paired EXP-010/EXP-F. The reconstructed competitor108 fallback also falls, .735582→.692119 on our random10 versus x-half10 convention. Thus its headline benefits from spatial assumptions, but the improvement is not solely immediate support adjacency.

The published competitor orthogonal-neighbour audit is independently reproduced (81.0/79.1/80.1/79.5/78.4% of SUPPORT pixels touching query). It used a continuous RNG across budgets, unlike the final notebook reset. In our200-shot episodes, about7.78% of QUERY pixels are within a Moore neighbourhood of support, not80%. No duplicate coordinate or full-feature rows were found. Across the examined support/query pairs, RMS feature distance below.05 source SD units was absent; below.1 was rare. These descriptive thresholds do not identify buildings/roofs/parcels. No such IDs are available for a same-building exclusion audit.

Classification: **valid random-pixel evaluation, spatially autocorrelated, transductive**. No actual query-label fitting found. Prediction-only smoothing still uses in-sample support predictions, so the competitor docstring's claim that it cannot benefit from adjacency is too strong. Gaussian weights in the buffered Y split connect to support only at distances at least11 keys, making direct nearby-label influence negligible; geographic generalization is still not proven universally.

## 9. Information-access regime

Source: all76263 labelled Madrid rows and their supplied coordinates. Target: all25992 unlabelled feature vectors and coordinates; only4*n true target labels per episode. The final source context is derived from these inputs, not hidden raw data. Target means/covariances, pseudo-label class partitions and their moments, neighbour features and probability graph are fitted over support+unlabelled query pool. Local supervised fitting receives support labels only. Target class ground-truth frequencies are NOT used for prediction.

This is not interchangeable with frozen EXP-010's inductive API. On a new target population, rebuild the pool-bound state; do not reuse Amsterdam's alignment or a subset pretending it is the same full pool. If pool/coordinate access is unavailable, retain the inductive EXP-H/EXP-010 branch and label it separately. Open-scope modelling is assumed permitted as directed by the user; availability of an organizer's future hidden-test pool is not verified.

Audit labels influenced model selection across experiments. **QUERY-LABEL LEAKAGE PASS means no query ground-truth values entered fitting/prediction; it does not mean target labels were never used in research selection/evaluation.**

## 10. Reproducibility

- Exact immutable competitor SHA and executable path: FORENSIC_TRACE.md/provenance.json.
- Original tuned config missing; original-code fallback20 results and failed script attempt retained.
- Our source priors refitted in clean processes and matched exactly; public API rebuilt source training independently again and matched the prior and predictions.
- Final100-episode suite exact repeat:3000 arrays; candidate20-draw competitor protocol exact repeat:300 arrays; Y-spatial exact repeat:300 arrays; initial final-candidate audit exact repeat:150 arrays.
- Standalone locked_clean_replay rebuilds all ASTRA source/local models from scratch, without their cached models, and matches the source prior plus1500 support/query/candidate-prediction arrays over100 trials per budget.
- Public inference artifact saved/reloaded,10 exact prediction-array checks per process; invalid-support tests and probability normalization pass. No target-truth argument in pool fitting.
- Frozen recipe SHA checks, original protected hashes and data/artifact SHA checks pass. The only initial omnibus failure was retained and repaired by stable tree-order prediction summation before the final recipe.
- Environment: Python3.14.6, NumPy2.5.3, SciPy1.18.1, sklearn1.9.0, Windows11. See environment.json and README.md for commands. Cross-version/platform byte equivalence is not asserted.

## 11. Recommended final hackathon method

**PROMOTE ASTRA-AGF**, conditional on the explicitly assumed full-unlabelled-pool/coordinate regime. It gives large reproducible gains at every budget over EXP-010/EXP-F, closes the200-shot competitor gap on matched protocol, survives both spatial diagnostics, requires no new raw-feature builder, and has a staged, explainable implementation. Its complexity is higher than a prototype but lower in data dependencies than the competitor's raw108-feature pipeline. Keep EXP-010 immutable; EXP-H remains an inductive contingency. Presentation files were NOT modified.

Do not claim statistical superiority to the missing tuned competitor model, do not present the best single episode, and do not suppress the worse5/50/100 matched-competitor results.

## 12. Remaining limitations

One target city; same label population used throughout exploratory selection; new seeds are not a new test population. No organizer-held-out test. Two spatial cuts are not parcel-disjoint validation. Raw benchmark membership itself presumes labelled building pixels. Source/target oldest-class date boundaries differ (1960 vs1945). Source pseudo-label errors may reinforce themselves. Gaussian scale is tied to unit grid keys, not arbitrary coordinates. Source alignment must be refitted for a genuinely new target pool. Large source-model evidence files and target-bound artifacts need deliberate packaging. Original competitor winner/PCA/complete settings remain unavailable. Mid-budget competitor fallback remains ahead on matched trials. These limitations remain despite excellent reproducibility.

## 13. Future generalized pipeline ideas

Separate label-free feature construction from benchmark label assignment; declare inductive versus transductive interfaces at the API level; retain raw feature/scaler/coordinate provenance and full episode manifests. Use building/parcel-disjoint and multi-city validation when IDs/data become available. Prefer budget-adaptive geometry and source-prior strength over per-budget lookup tuning. Study confidence-aware conditional alignment on a genuinely separate development domain, with confirmation-bias controls, rather than increasing iterations on this audit. Learn or justify spatial scales from physical sampling geometry and source-only evidence. Investigate multimodal class models and temporal source features only as isolated ablations. Keep deterministic prediction aggregation and mandatory artifact reload tests.

### Class diagnostics

Mean per-episode class F1 on the locked100-trial200-shot evaluation:

{table(['Method','C1','C2','C3','C4'],classrows)}

The largest gains over the prototype family concentrate in old classes1/2, though all four improve. On the locked200-shot100-trial confusion matrices, C2→C1 errors drop32.18%→16.16% versus EXP-010 (30.23% under EXP-F), and C1→C2 drops19.49%→12.87%. Not every confusion improves: versus EXP-F, C3→C4 rises8.65%→10.49%; class4 recall rises68.37%→82.51% but precision remains a limitation. This is consistent with neighbourhood construction-era coherence and nonlinear feature interactions, not proof of same-building identity. No class-specific thresholds were tuned after observing these diagnostics. Full per-class vectors, confusion matrices and episode scores are retained in FINAL_CLASS_DIAGNOSTICS.json and the underlying result files.

### Evidence inventory

`ALL_RESULTS.csv` contains every packaged result family, including negative arms and the original failed-repeat output. It contains method-evaluation records, not that many independent populations. `PAIRED_COMPARISONS.json` holds full-precision paired deltas/wins. `FINAL_SELECTION.json` proves the recipe was locked before seed104729 results. `final_verification.json` records integrity/reproduction status. Competitor claims/slide text/commit-table generations: claim_evidence.json. The data-adapter and parallel-probability failures remain in their original logs.
'''
 report.write_text(text,encoding='utf-8')
 # Append final scorecard to the already written comparability audit without erasing forensic history.
 auditfile=F/'COMPARABILITY_AUDIT.md';oldtext=auditfile.read_text(encoding='utf-8');assert '## Locked final candidate addendum'not in oldtext
 auditfile.write_text(oldtext+'\n\n## Locked final candidate addendum\n\n'+comptable+'\n\nASTRA-AGF has100 new seed104729 episodes/class budget after locking: '+', '.join(fmt(final['summary'][str(b)]['ASTRA_AGF'])for b in B)+'. These are the primary sampling-stability results, not an independent target population. On the SAME20 competitor episodes,200-shot ASTRA is .737388 versus fallback108 .736392 (13/20 paired wins; +.000995). This matches the .7373 claim numerically but does not establish superiority to the missing tuned model. On our original10 episodes ASTRA .733731 versus reproduced competitor .735582, so the exact gap depends on the stated episode convention.\n\nThe matched x-half comparator is .689672 for ASTRA versus .692119 for competitor fallback; additional ASTRA y-half is .705083. Full information regimes and limitations remain as above. Presentation untouched; frozen EXP-010 intact.\n',encoding='utf-8')
 verification={'pass':True,'frozen_EXP010_integrity':not frozen_core,'protected_file_count':len(protected),'protected_changed_files':changed,'query_label_fitting_or_prediction_leakage':False,'audit_based_model_selection':True,'information_regime':'transductive','clean_process_reproduction':True,'checks':checks,'standalone_source_and_500_episode_rebuild':True,'standalone_reference_arrays_exact':clean['reference_arrays_exact'],'pinned_wrapper_exact':True,'canonical_EXP010_50_episode_scores_exact':True,'historical_EXPF_50_prediction_arrays_exact':True,'recipe_files_sha256':cfg['files_sha256'],'state_sha256':sha(H/'astra_pool_state.pkl'),'packaged_result_rows':len(rows),'method_episode_records_including_repeats':episode_count,'competition_presentation_modified_by_this_session':False,'competitor_exact_tuned_reproduction':False,'competitor_mechanism_reproduction':True}
 save(H/'final_verification.json',verification)
 manifest={str(p.relative_to(R)):sha(p)for p in list(H.glob('*.py'))+list(H.glob('*.md'))+list(H.glob('*.csv'))+[H/'FINAL_SELECTION.json',H/'astra_pool_state.pkl',F/'FINAL_GAP_ANALYSIS.md',F/'COMPARABILITY_AUDIT.md',F/'FORENSIC_TRACE.md']};save(H/'FINAL_SHA256SUMS.json',manifest)
 save(H/'DECISION_SUMMARY.json',{'recommendation':'PROMOTE ASTRA-AGF','primary_final100':{b:final['summary'][str(b)]['ASTRA_AGF']for b in B},'paired_comparisons':comparisons,'competitor_protocol':proto['summary'],'spatial_x':spatial['summary'],'spatial_y':{b:ys['summary'][str(b)]['ASTRA_AGF']for b in B},'competitor_claim_200':.7373,'competitor_reproduced_200':comp['budgets']['200'],'integrity_pass':True,'query_label_prediction_leakage_pass':True,'clean_process_pass':True})
 print('PACKAGED',len(rows),'rows;',episode_count,'method-episode records (including repeats); frozen integrity PASS',flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
