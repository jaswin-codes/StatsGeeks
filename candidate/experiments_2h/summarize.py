"""Arithmetic-only summaries; no fitting, selection or changes to raw results."""
from pathlib import Path
import json,time
import numpy as np
O=Path(__file__).resolve().parent
D={'A':'expA_source_local','B':'expB_dim_shrink','C':'expC_class_diagnostic','D':'expD_spatial','E':'expE_temporal','F':'expF_covariance'}
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2))
def rows(result,b,m):return sorted([x for x in result['episodes'] if x['budget']==b and x['method']==m],key=lambda x:x['trial'])
R={k:load(O/v/'results.json') for k,v in D.items()}; S=load(O/'expF_covariance/spatial/results.json'); B=[5,25,50,100,200]
# Full class diagnostics relative to both controls.
diagnostics={}
lines=['# Class-level findings','', 'Class order: 1,2,3,4. Repeated query pixels mean episodes are not independent samples.','']
for b in B:
 rr=rows(R['C'],b,'EXP010'); pc=np.array([x['class_f1'] for x in rr]); macro=pc.mean(1)
 cov=((pc-pc.mean(0))*(macro-macro.mean())[:,None]).mean(0)/4
 cm=np.sum([x['confusion'] for x in rr],axis=0); off=cm.copy(); np.fill_diagonal(off,0)
 directed=np.unravel_index(off.argmax(),off.shape); pair=max([(i,j) for i in range(4) for j in range(i+1,4)],key=lambda ij:off[ij]+off[ij[::-1]])
 norm=cm/cm.sum(1,keepdims=True); no=norm.copy();np.fill_diagonal(no,0); norm_pair=np.unravel_index(no.argmax(),no.shape)
 gains={}
 for control in ['joint_control','compact_local']:
  delta=pc-np.array([x['class_f1'] for x in rows(R['C'],b,control)])
  gains[control]={'mean_per_class':delta.mean(0).tolist(),'episode_deltas':delta.tolist(),'wins':(delta>1e-12).sum(0).tolist(),'losses':(delta< -1e-12).sum(0).tolist(),'ties':(abs(delta)<=1e-12).sum(0).tolist()}
 diagnostics[b]={'per_class_mean':pc.mean(0).tolist(),'per_class_population_sd':pc.std(0).tolist(),'macro_variance_contribution':cov.tolist(),'variance_fraction':(cov/macro.var()).tolist(),'aggregate_confusion':cm.tolist(),'aggregate_confusion_row_normalized':norm.tolist(),'dominant_directed_count_pair':[int(v+1) for v in directed],'dominant_bidirectional_count_pair':[int(v+1) for v in pair],'dominant_normalized_direction':[int(v+1) for v in norm_pair],'poor_episodes_below_mean_minus_sd':[{'trial':x['trial'],'macro_f1':x['macro_f1'],'class_f1':x['class_f1']} for x in rr if x['macro_f1']<macro.mean()-macro.std()],'transfer_gains':gains}
 lines += [f'## {b} shots',f'- Mean class F1: {np.round(pc.mean(0),6).tolist()}',f'- Class SD: {np.round(pc.std(0),6).tolist()}',f'- Macro-variance fractions (including covariance): {np.round(cov/macro.var(),4).tolist()}',f'- Dominant bidirectional confusion by count: {pair[0]+1} <-> {pair[1]+1}; normalized directed: {norm_pair[0]+1} -> {norm_pair[1]+1}.',f'- Gain vs joint control: {np.round(gains["joint_control"]["mean_per_class"],6).tolist()}',f'- Gain vs compact local: {np.round(gains["compact_local"]["mean_per_class"],6).tolist()}',f'- Poor episodes: {[x["trial"] for x in diagnostics[b]["poor_episodes_below_mean_minus_sd"]]}','']
q=diagnostics[5]; dominant=int(np.argmax(q['variance_fraction']))+1; weakest=int(np.argmin(q['per_class_mean']))+1
lines += ['## Answers',f'Largest low-shot macro-variance contributor: class {dominant}; weakest mean F1: class {weakest}.', 'The variance decomposition allocates correlated class changes via cov(class F1, macro F1)/4; it is descriptive, not causal.',f'Largest contributor accounts for {max(q["variance_fraction"]):.1%}, so do not attribute all 5-shot SD to one class.', 'Per-class wins/losses/ties and every episode gain are in diagnostic.json. Source geometry alone is isolated by compact_local; joint_control also includes dimension changes. No class-specific safeguard is justified by ten highly overlapping episodes. None implemented.']
save(O/D['C']/'diagnostic.json',diagnostics);(O/D['C']/'FINDINGS.md').write_text('\n'.join(lines)+'\n')
# Factorial effects with episode pairing.
effects={}; lines=['# Dimension x shrinkage interaction','', '| Shots | Dimension effect at lambda0 | Shrinkage effect all60 | Shrinkage effect compact | Interaction | Interaction W/L/T |','|---|---:|---:|---:|---:|---|']
for b in B:
 v={m:np.array([x['macro_f1'] for x in rows(R['B'],b,m)]) for m in ['all60_l0','compact_l0','all60_l04','compact_l04']}
 dim=v['compact_l0']-v['all60_l0']; shrinkall=v['all60_l04']-v['all60_l0']; shrinkcompact=v['compact_l04']-v['compact_l0']; interaction=shrinkcompact-shrinkall
 effects[b]={name:{'episode_deltas':a.tolist(),'mean':float(a.mean()),'population_sd':float(a.std()),'wins':int((a>1e-12).sum()),'losses':int((a< -1e-12).sum()),'ties':int((abs(a)<=1e-12).sum())} for name,a in [('dimension',dim),('shrinkage_all',shrinkall),('shrinkage_compact',shrinkcompact),('interaction',interaction)]}
 z=effects[b]['interaction'];lines.append(f'| {b} | {dim.mean():+.6f} | {shrinkall.mean():+.6f} | {shrinkcompact.mean():+.6f} | {interaction.mean():+.6f} | {z["wins"]}/{z["losses"]}/{z["ties"]} |')
lines+=['','Positive interactions are small: compact features reduce the harm of shrinkage at larger budgets, but do not make it beneficial there. k changes by budget, so cross-budget changes are not a pure k effect.']
save(O/D['B']/'factorial_effects.json',effects);(O/D['B']/'FINDINGS.md').write_text('\n'.join(lines)+'\n')
# Spatial contrasts, not paired estimates across protocols.
lines=['# Spatial robustness','', 'Grid keys are rounded UTM/30m (organiser Notebook2 section2.3). Fixed median east/west split with 10-key (~300m) query exclusion; alternating support side. Query regions differ from random evaluation, so protocol drops combine region shift, class composition and geographic separation. No buffer tuning. Two regions only, not general spatial CV.','', '| Method | Shots | Random F1 | Spatial F1 | Spatial minus random | Spatial gain vs EXP010 |','|---|---:|---:|---:|---:|---:|']
for b in B:
 for name,random,spatial in [('EXP010',R['A'],R['D']),('alpha_0.50',R['A'],R['D']),('euclidean',R['F'],S),('diagonal',R['F'],S),('regularized',R['F'],S)]:
  a=random['summary'][str(b)][name]; s=spatial['summary'][str(b)][name]
  lines.append(f'| {name} | {b} | {a["mean"]:.6f} | {s["mean"]:.6f} | {s["mean"]-a["mean"]:+.6f} | {s["mean_delta"]:+.6f} |')
(O/D['D']/'FINDINGS.md').write_text('\n'.join(lines)+'\n')
# A descriptive maxima: no schedule selected or run.
best_alpha={b:max([m for m in R['A']['summary'][str(b)] if m!='EXP010'],key=lambda m:R['A']['summary'][str(b)][m]['mean']) for b in B}
(O/D['A']/'FINDINGS.md').write_text('# Source reliance\n\nDescriptive audit maxima (not a selected/validated schedule): '+str(best_alpha)+'\n\nYes, best-looking source reliance decreases with labels in this grid: 1.0, 0.5, 0, 0, 0. This is exploratory, not evidence of an independently validated optimal schedule. At 5 shots the source-only-geometry endpoint beats all probability mixtures, so blending itself does not beat both endpoints there. At 25 shots alpha0.5 exceeds both endpoints by a small amount. The fixed alpha0.5 candidate loses at four of five budgets versus EXP010. No further alpha tuning or promotion.\n')
# Metrics vs euclidean isolate distance choice.
metric_effects={}
for b in B:
 base=np.array([x['macro_f1'] for x in rows(R['F'],b,'euclidean')]);metric_effects[b]={}
 for m in ['diagonal','regularized']:
  delta=np.array([x['macro_f1'] for x in rows(R['F'],b,m)])-base
  metric_effects[b][m]={'episode_deltas':delta.tolist(),'mean':float(delta.mean()),'population_sd':float(delta.std()),'wins':int((delta>1e-12).sum()),'losses':int((delta< -1e-12).sum()),'ties':int((abs(delta)<=1e-12).sum())}
save(O/D['F']/'metric_effects.json',metric_effects)
print(json.dumps({'low_shot_diagnostic':q,'spatial_regularized':{b:S['summary'][str(b)]['regularized'] for b in B}},indent=2))
