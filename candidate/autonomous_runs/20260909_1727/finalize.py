"""Evidence-only reports/figures/packaging after the immutable selection lock."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from sprint import *
import shutil,subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn,scipy

def main():
    report()
    result=json.loads((H/'FINAL_RESULTS.json').read_text());best=result['best_new_candidate'];records=result['results']['records'];sp=result['spatial']['records'];ss=result['results']['summary'];lock=result['selection_lock'];fig=H/'figures';fig.mkdir(exist_ok=False)
    methods=['EXP010','EXPF','ASTRA_AGF',best];colors=['#777777','#cc7a00','#2676b5','#169b69'];labels=['EXP-010 (inductive)','EXP-F (inductive)','ASTRA-AGF', 'ASTRA-AGF + coordinates']
    plt.rcParams.update({'font.size':10,'figure.dpi':120,'savefig.dpi':170,'axes.spines.top':False,'axes.spines.right':False})
    figure_paths=[]
    def export(name,figure):
        figure.tight_layout()
        for ext in ('png','svg'):
            p=fig/f'{name}.{ext}';figure.savefig(p,bbox_inches='tight');figure_paths.append(str(p.relative_to(H)))
        plt.close(figure)
    f,ax=plt.subplots(figsize=(8,5))
    for n,c,l in zip(methods,colors,labels):
        means=[ss[str(b)][n]['mean'] for b in BUDGETS];sd=[ss[str(b)][n]['population_sd'] for b in BUDGETS]
        ax.errorbar(range(5),means,yerr=sd,color=c,label=l,marker='o',capsize=3)
    ax.set(xticks=range(5),xticklabels=BUDGETS,xlabel='Shots per class',ylabel='Macro F1 (mean ± population SD)',title='Locked evaluation: 200 paired episodes per budget');ax.legend();ax.grid(alpha=.2);f.text(.5,-.015,'One target city; excludes fixed development bank. SD is not a confidence interval.',ha='center',fontsize=8);export('01_budget_performance',f)
    f,ax=plt.subplots(figsize=(8,4))
    gains=[]
    for b in BUDGETS:
        vals={n:[r['f1'] for r in records if r['method']==n and r['budget']==b] for n in ('ASTRA_AGF',best)};gains.append(np.array(vals[best])-vals['ASTRA_AGF'])
    ax.boxplot(gains,tick_labels=BUDGETS,showfliers=False);ax.axhline(0,color='black',lw=1);ax.set(xlabel='Shots per class',ylabel='Paired macro-F1 gain vs ASTRA',title='Coordinate variant: all paired gains, no query-based selection');export('02_paired_gains',f)
    f,ax=plt.subplots(figsize=(10,5));x=np.arange(4)
    spatial_details={}
    for j,(n,c,l) in enumerate(zip(methods,colors,labels)):
        vals=[np.array([r['f1'] for r in sp if r['method']==n and r['axis']==a and r['support_side']==s]) for a in (0,1) for s in (0,1)];means=[v.mean() for v in vals];sd=[v.std() for v in vals]
        spatial_details[n]=dict(directions=[dict(axis=a,support_side=s,mean=float(means[a*2+s]),population_sd=float(sd[a*2+s])) for a in (0,1) for s in (0,1)],x_half=float(np.mean(means[:2])),y_half=float(np.mean(means[2:])),worst_direction=float(min(means)),mean=float(np.mean(means)))
        ax.bar(x+(j-1.5)*.19,means,.19,yerr=sd,color=c,label=l,capsize=2)
    ax.set(xticks=x,xticklabels=['Low x → high x','High x → low x','Low y → high y','High y → low y'],ylim=(.48,.82),ylabel='Macro F1 ± population SD',title='Spatial audit: every direction, 10 trials each, 200 shots/class');ax.legend(fontsize=8,ncol=2);export('03_spatial_directions',f)
    ab=json.loads((H/'ablation_complete.json').read_text())['summary']['160'];order=['EXPF','A','A+B','A+C','A+D','A+B+C','A+B+D','A+C+D','A+B+C+D','ASTRA_AGF'];f,ax=plt.subplots(figsize=(9,5));ax.barh(order,[ab[n]['mean'] for n in order],xerr=[ab[n]['population_sd'] for n in order],color='#2676b5');ax.set(xlabel='Held-out SUPPORT macro F1 ± population SD (not query score)',title='Operational ablation: 160 training / 40 validation per class',xlim=(.5,.82));f.text(.5,-.015,'A=RF; B=pool covariance; C=spatial graph; D=adaptive covariance. Prior off except ASTRA.',ha='center',fontsize=8);export('04_support_ablation',f)
    f,axes=plt.subplots(1,2,figsize=(11,4.5));matrices={}
    for ax,n,l in zip(axes,['ASTRA_AGF',best],['ASTRA-AGF','ASTRA-AGF + coordinates']):
        cm=np.sum([r['confusion'] for r in records if r['method']==n and r['budget']==200],axis=0);norm=cm/cm.sum(1,keepdims=True);matrices[n]=norm.tolist();im=ax.imshow(norm,vmin=0,vmax=1,cmap='Blues')
        for i in range(4):
            for j in range(4):ax.text(j,i,f'{norm[i,j]:.1%}',ha='center',va='center',color='white' if norm[i,j]>.5 else 'black')
        ax.set(xticks=range(4),xticklabels=CLASSES,yticks=range(4),yticklabels=CLASSES,xlabel='Predicted class',ylabel='True query class',title=l)
    f.suptitle('200-shot aggregate row-normalized confusion (evaluation only)');export('05_confusion_matrices',f)
    f,ax=plt.subplots(figsize=(8,4));x=np.arange(4)
    for j,(n,c,l) in enumerate(zip(methods,colors,labels)):ax.bar(x+(j-1.5)*.2,ss['200'][n]['class_f1'],.2,color=c,label=l)
    ax.set(xticks=x,xticklabels=CLASSES,xlabel='Class',ylabel='Mean per-episode class F1',title='200-shot class diagnostics');ax.legend(fontsize=8,ncol=2);export('06_per_class_f1',f)
    state=load_state();ref=np.load(H/'final/b200_t0.npz');q=ref['query'];xy=state['coords'][q];f,axes=plt.subplots(1,2,figsize=(11,5))
    for ax,n,l in zip(axes,['ASTRA_AGF',best],['ASTRA-AGF','ASTRA-AGF + coordinates']):
        im=ax.scatter(xy[:,0],xy[:,1],c=ref[n],cmap='viridis',vmin=1,vmax=4,s=1,rasterized=True);ax.set(title=l,xlabel='x lattice key',ylabel='y lattice key',aspect='equal')
    f.suptitle('First predeclared 200-shot episode: query predictions (not best episode)');export('07_prediction_maps',f)
    save('FIGURE_MANIFEST.json',dict(files=figure_paths,source_results_sha256=sha(H/'final_complete.json'),spatial_results_sha256=sha(H/'spatial_complete.json'),selection_used=False,query_truth_usage='confusion and F1 diagnostics only'))
    result.update(spatial_direction_summary=spatial_details,aggregate_confusion_proportions=matrices,figures=figure_paths,official_incumbent='ASTRA_AGF historical',promotion_status='Development-selected random-pixel candidate packaged; no official universal-winner promotion',geographic_caveat='Coordinate variant worsens high-x to low-x and high-y to low-y directions. No post-audit configuration changes.',reproducibility=json.loads((H/'clean_replay/verification.json').read_text()))
    save('FINAL_RESULTS.json',result)
    text=(H/'FINAL_REPORT.md').read_text(encoding='utf-8')
    text+='\n## Headline and geographic trade-off\n\nThe prelocked coordinate variant scores **0.749299 ± 0.005716** at 200 shots/class, versus paired ASTRA **0.733037 ± 0.006106**, gain **+0.016262**, **200/200 wins**. The full independent source refit and replay matches **4000 prediction arrays across 1000 episodes**, including both inductive controls.\n\nThis is a robust support-sampling gain on the stated random-pixel population, NOT independent-city superiority. Five-shot gain is tiny (+0.000289; 106/200 wins), so no meaningful low-budget superiority is claimed. No recipe changes or candidate reselection followed audit scores.\n\nCoordinate-RF spatial x-half = **0.682326**, y-half = **0.706106**, worst direction = **0.644816**, four-direction mean = **0.694216**. Matched ASTRA: x-half **0.687017**, y-half **0.706326**, worst **0.658183**, mean **0.696672**. In particular high-x → low-x loses approximately **0.028670**. Thus the coordinate variant is NOT an automatic universal replacement. ASTRA remains the historical incumbent; the development-locked coordinate variant is packaged for the explicitly stated random-pixel/full-pool use case. Official submission promotion remains unclaimed.\n\n## Figures\n\n'
    text+='\n'.join('- '+p for p in figure_paths if p.endswith('.png'))+'\n'
    text+='\n## Compute and failure accounting\n\nCompleted: fresh source rebuild; 50-episode baseline; 8 factorial RF arms plus controls; 12 first-pass alternatives; 7 refinements; 400 budget-stability support evaluations; support-only four-direction safeguards; 1000 locked paired final episodes; 40 spatial episodes; fresh source rebuild and exact 1000-episode replay. No model-fit exceptions occurred in this session. The network/pause interval was resumed without restarting completed stages. Source models use 200 trees except explicitly archived 600-tree experiments. The experiment named Confidence_prior is a stronger fixed pseudo-count prior (60), NOT an implemented confidence gate. No true confidence-gated adaptation was tested.\n\nNo query truth was used for model fitting, hyperparameter selection, candidate selection, adaptation, or stopping. Query labels were read only for scoring/figures and class-stratified benchmark episode construction. Development-support labels are research supervision, not an organizer-held-out test.\n'
    (H/'FINAL_REPORT.md').write_text(text,encoding='utf-8')
    board=json.loads((H/'LEADERBOARD.json').read_text())
    for row in board:
        n=row['candidate'];row.update(query_labels_used_for_selection=False,query_labels_used_for_evaluation=n in methods)
        if n in spatial_details:row['spatial']=spatial_details[n]
    # Preserve factorial rows rather than dropping completed ablations from the leaderboard.
    for n,v in ab.items():
        if n=='ASTRA_AGF':continue
        cfg=json.loads((H/'ablation_complete.json').read_text())['configurations'].get(n)
        board.append(dict(candidate='ablation:'+n,development_support_cv=v,config=cfg,status='diagnostic',query_label_usage=False,query_labels_used_for_selection=False,query_labels_used_for_evaluation=False,information_regime='inductive' if n=='EXPF' or not cfg.get('pool',True) and not cfg.get('spatial',True) else 'transductive',reproducibility='not separately replayed'))
    save('LEADERBOARD.json',board);save('AUTONOMOUS_LEADERBOARD.json',board)
    latest=json.loads((H/'LATEST_BEST.json').read_text());latest.update(BEST_SCORE=ss['200'][best]['mean'],score_type='locked evaluation macro F1 at 200 shots/class; not selection metric',BEST_RESULTS='FINAL_RESULTS.json',BEST_ARTIFACT='pool_state.pkl',BEST_CONFIG=lock['config'],selection_support_score=lock['support_cv']['mean'],population_sd=ss['200'][best]['population_sd'],status='verified development-selected candidate; historical ASTRA incumbent retained',reproducibility='fresh source rebuild and 4000 exact prediction arrays',spatial=spatial_details[best],official_promotion=False);save('LATEST_BEST.json',latest)
    req=f'numpy=={np.__version__}\nscipy=={scipy.__version__}\nscikit-learn=={sklearn.__version__}\nthreadpoolctl=='+__import__('threadpoolctl').__version__+'\n'
    (H/'requirements-repro.txt').write_text(req)
    inputs=H/'verification_inputs';inputs.mkdir(exist_ok=False)
    for b in BUDGETS:
        ref=np.load(H/f'final/b{b}_t0.npz');np.savez_compressed(inputs/f'b{b}.npz',support=ref['support'],support_labels=ref['support_labels'],query=ref['query'],expected=ref[best])
    save('INFERENCE_MANIFEST.json',dict(files={name:sha(H/name) for name in ('agf_model.py','pool_state.pkl','SELECTION_LOCK.json')},feature_names=state['feature_names'],pool_rows=len(state['raw']),input_contract='Original target pool row order. Support indices and support labels only. Lattice coordinate units.'))
    log('Figures and final inference bundle prepared')

if __name__=='__main__':
    with threadpool_limits(limits=1):main()
