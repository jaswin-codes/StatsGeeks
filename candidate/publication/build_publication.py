"""Evidence-only publication build. Reads saved predictions; does not import model code.
Run from repository root: python -B candidate/publication/build_publication.py
"""
from pathlib import Path
import json,hashlib,pickle,platform,subprocess,sys,os,datetime,importlib.metadata,re
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import psutil
R=Path(__file__).resolve().parents[2]; H=R/'candidate/autonomous_runs/20260909_1727'
T=R/'candidate/tables'; F=R/'candidate/figures/publication'; D=R/'candidate/reports'; E=R/'candidate/reproducibility'; P=R/'candidate/presentation'
MODELS=['EXP010','EXPF','ASTRA_AGF','Coordinate_RF']; LABEL={'EXP010':'EXP-010','EXPF':'EXP-F','ASTRA_AGF':'ASTRA','Coordinate_RF':'Coordinate_RF'}
COLORS=dict(zip(MODELS,['#737373','#D89000','#377EB8','#009E73'])); BUDGETS=[5,25,50,100,200]; SEED=20260911
rng=np.random.default_rng(SEED); figure_manifest=[]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,obj):p.write_text(json.dumps(obj,indent=2,allow_nan=False),encoding='utf-8')
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def git_commit():
    try:return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True,stderr=subprocess.DEVNULL).strip()
    except (OSError,subprocess.CalledProcessError):return load(E/'environment_summary.json').get('git_commit','unavailable in extracted archive')
def md(df):
    def fmt(v):
        if isinstance(v,(float,np.floating)):return '' if np.isnan(v) else f'{v:.6g}'
        return str(v).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(map(str,df.columns))+' |\n|'+'|'.join(['---']*len(df.columns))+'|\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))+'\n'
def table(name,rows):
    df=rows if isinstance(rows,pd.DataFrame) else pd.DataFrame(rows)
    df.to_csv(T/(name+'.csv'),index=False);(T/(name+'.md')).write_text(md(df),encoding='utf-8');return df

def export(name,fig,caption):
    fig.tight_layout()
    for ext in ('png','svg','pdf'):fig.savefig(F/f'{name}.{ext}',dpi=350,bbox_inches='tight',metadata={'Creator':'StatsGeeks publication build'} if ext=='pdf' else None)
    fig.savefig(P/f'{name}_transparent.png',dpi=350,bbox_inches='tight',transparent=True)
    # Canonical opaque files are referenced, not redundantly copied; transparent tight crops are slide-specific.
    figure_manifest.append(dict(name=name,caption=caption,files=[f'candidate/figures/publication/{name}.{e}' for e in ('png','svg','pdf')],transparent=f'candidate/presentation/{name}_transparent.png',dpi=350))
    plt.close(fig)

def main():
    for p in (T,F,D,E,P):p.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.figsize':(9,5),'savefig.dpi':350,'svg.fonttype':'none','pdf.fonttype':42})
    final=load(H/'final_complete.json'); rec=pd.DataFrame(final['records']); spatial=pd.DataFrame(load(H/'spatial_complete.json')['records'])
    assert len(rec)==4000 and not rec.duplicated(['method','budget','trial']).any()
    scores=rec.pivot(index=['budget','trial'],columns='method',values='f1').sort_index();assert not scores.isna().any().any()
    # Confusion-derived F1 and saved labels/predictions independently agree; labels used only here for evaluation.
    truth=np.load(H/'sealed_evaluation.npz')['labels'];dev=np.load(H/'development_support.npz')['indices'];audit_count=0
    indexed=rec.set_index(['budget','trial','method']);support_hashes=[]
    for b in BUDGETS:
        for t in range(200):
            with np.load(H/f'final/b{b}_t{t}.npz') as a:
                s,q=a['support'],a['query'];assert not np.intersect1d(s,q).size and not np.intersect1d(dev,q).size
                assert len(np.unique(s))==4*b and len(np.unique(q))==len(q)
                np.testing.assert_array_equal(truth[s],a['support_labels'])
                assert set(q)==set(range(len(truth)))-set(dev)-set(s)
                support_hashes.append(dict(budget=b,trial=t,support_sha256=hashlib.sha256(s.tobytes()).hexdigest(),query_sha256=hashlib.sha256(q.tobytes()).hexdigest()))
                for n in MODELS:
                    cm=np.bincount((truth[q]-1)*4+(a[n]-1),minlength=16).reshape(4,4)
                    np.testing.assert_array_equal(cm,indexed.loc[(b,t,n),'confusion'])
                    den=cm.sum(0)+cm.sum(1);f1=np.divide(2*np.diag(cm),den,out=np.zeros(4),where=den!=0)
                    np.testing.assert_allclose(f1.mean(),indexed.loc[(b,t,n),'f1'],atol=1e-14);audit_count+=1
    table('episode_manifest',support_hashes)
    summary=[]
    for b in BUDGETS:
        for n in MODELS:
            x=scores.loc[b,n].to_numpy();lo,hi=np.quantile(x[rng.integers(len(x),size=(10000,len(x)))].mean(1),[.025,.975])
            summary.append(dict(method=n,budget=b,episodes=len(x),mean=x.mean(),population_sd=x.std(ddof=0),bootstrap_mean_ci_low=lo,bootstrap_mean_ci_high=hi,protocol='locked random-pixel; fixed target; development bank excluded'))
    curve=table('learning_curve',summary);table('leaderboard',curve[curve.budget==200].sort_values('mean',ascending=False));table('episode_scores',rec[['method','budget','trial','f1','seconds']])
    fig,ax=plt.subplots()
    for n in MODELS:
        d=curve[curve.method==n];ax.errorbar(range(5),d['mean'],yerr=d.population_sd,label=LABEL[n],color=COLORS[n],marker='o',capsize=3)
    ax.set(xticks=range(5),xticklabels=BUDGETS,xlabel='Shots per class',ylabel='Macro F1 ± population SD',title='Frozen-model learning curves · 200 paired episodes/budget');ax.legend(ncol=2);ax.grid(alpha=.2)
    export('learning_curve',fig,'Error bars: population SD (ddof=0), not CI. Conditional bootstrap mean intervals in learning_curve.csv.')
    fig,ax=plt.subplots();x=np.arange(5)
    for j,n in enumerate(MODELS):
        d=curve[curve.method==n];ax.bar(x+(j-1.5)*.2,d['mean'],.2,yerr=d.population_sd,color=COLORS[n],label=LABEL[n],capsize=2)
    ax.set(xticks=x,xticklabels=BUDGETS,xlabel='Shots per class',ylabel='Macro F1 ± population SD',ylim=(0,.85));ax.legend(ncol=2);export('budget_comparison',fig,'All five budgets, same locked evaluation population.')
    sig=[];gains=[]
    for b in BUDGETS:
        for n in MODELS[:-1]:
            a=scores.loc[b,'Coordinate_RF'].to_numpy();z=scores.loc[b,n].to_numpy();d=a-z
            ci=np.quantile(d[rng.integers(len(d),size=(20000,len(d)))].mean(1),[.025,.975]);tt=stats.ttest_rel(a,z);ww=stats.wilcoxon(d,zero_method='wilcox',alternative='two-sided',method='auto')
            # dz is the paired standardized mean difference. Cliff delta is explicitly marginal, not paired.
            cliff=np.sign(a[:,None]-z[None,:]).mean();nonzero=d[d!=0];ranks=stats.rankdata(abs(nonzero));rbc=(ranks*np.sign(nonzero)).sum()/ranks.sum() if len(nonzero) else 0.
            sig.append(dict(comparison='Coordinate_RF vs '+n,budget=b,n_pairs=len(d),mean_gain=d.mean(),population_sd_gain=d.std(),bootstrap_ci_low=ci[0],bootstrap_ci_high=ci[1],paired_t=tt.statistic,t_p=tt.pvalue,wilcoxon_W=ww.statistic,wilcoxon_p=ww.pvalue,cohen_dz=d.mean()/d.std(ddof=1),paired_rank_biserial=rbc,cliff_delta_marginal=cliff,wins=int((d>0).sum()),ties=int((d==0).sum()),losses=int((d<0).sum())))
            gains.extend(dict(budget=b,trial=t,comparison=n,gain=v) for t,v in enumerate(d))
    sig=pd.DataFrame(sig)
    for col in ('t_p','wilcoxon_p'):
        order=np.argsort(sig[col].values);adjusted=np.maximum.accumulate(sig[col].values[order]*(len(sig)-np.arange(len(sig))));sig[col+'_holm']=0.;sig.loc[order,col+'_holm']=np.minimum(adjusted,1)
    table('significance',sig);table('paired_gains',gains)
    fig,axes=plt.subplots(1,3,figsize=(14,4.5),sharey=True)
    for ax,n in zip(axes,MODELS[:-1]):
        ax.boxplot([scores.loc[b,'Coordinate_RF'].values-scores.loc[b,n].values for b in BUDGETS],tick_labels=BUDGETS,showfliers=False);ax.axhline(0,color='gray',ls='--');ax.set(title='vs '+LABEL[n],xlabel='Shots/class')
    axes[0].set_ylabel('Paired macro-F1 gain');export('paired_gain',fig,'Matched by budget and trial; boxes summarize paired differences, not independent-city uncertainty.')
    for kind in ('wins','gain'):
        fig,axes=plt.subplots(1,3,figsize=(14,4.5))
        for ax,n in zip(axes,MODELS[:-1]):
            for b in BUDGETS:
                d=scores.loc[b,'Coordinate_RF'].values-scores.loc[b,n].values;ax.plot(np.arange(1,201),np.cumsum(d>0 if kind=='wins' else d),label=str(b))
            ax.set(title='Coordinate_RF vs '+LABEL[n],xlabel='Episode in saved order',ylabel='Cumulative '+('paired wins' if kind=='wins' else 'macro-F1 gain'));ax.legend(title='Shots',fontsize=8)
        export('cumulative_'+kind,fig,'Saved episode order is arbitrary; cumulative trends do not represent learning or sequential inference.')
    perclass=[];conf=[];predsum=[]
    for b in BUDGETS:
        for n in MODELS:
            rows=rec[(rec.budget==b)&(rec.method==n)];cm=np.sum(rows.confusion.tolist(),axis=0);support=cm.sum(1);predicted=cm.sum(0);tp=np.diag(cm)
            precision=np.divide(tp,predicted,out=np.zeros(4),where=predicted!=0);recall=tp/support;f1=2*tp/(support+predicted)
            for i in range(4):
                perclass.append(dict(method=n,budget=b,class_id=i+1,precision=precision[i],recall=recall[i],f1=f1[i],support=int(support[i]),mean_episode_class_f1=np.mean(rows.class_f1.tolist(),axis=0)[i],unit='pooled query appearances; repeated pixels'))
                predsum.append(dict(method=n,budget=b,class_id=i+1,predicted_count=int(predicted[i]),true_count=int(support[i]),query_appearances=int(cm.sum())))
                for j in range(4):conf.append(dict(method=n,budget=b,true_class=i+1,predicted_class=j+1,count=int(cm[i,j]),row_normalized=cm[i,j]/support[i]))
            if b==200:
                for norm in (False,True):
                    values=cm/support[:,None] if norm else cm;fig,ax=plt.subplots(figsize=(6,5));im=ax.imshow(values,cmap='Blues',vmin=0,vmax=1 if norm else None)
                    for i in range(4):
                        for j in range(4):ax.text(j,i,f'{values[i,j]:.1%}' if norm else f'{values[i,j]:,}',ha='center',va='center',fontsize=9,color='white' if values[i,j]>values.max()*.55 else 'black')
                    ax.set(xticks=range(4),xticklabels=range(1,5),yticks=range(4),yticklabels=range(1,5),xlabel='Predicted class',ylabel='True class',title=LABEL[n]+' · '+('row-normalized' if norm else 'pooled counts'));fig.colorbar(im,ax=ax)
                    export('confusion_'+n+('_normalized' if norm else '_raw'),fig,'200 shots/class, 200 episodes. Counts are repeated query appearances, not unique independent pixels.')
    pc=table('per_class',perclass);table('confusion',conf);table('prediction_summary',predsum)
    fig,axes=plt.subplots(1,3,figsize=(14,4.5))
    for ax,metric in zip(axes,['precision','recall','f1']):
        for j,n in enumerate(MODELS):ax.bar(np.arange(4)+(j-1.5)*.2,pc[(pc.method==n)&(pc.budget==200)][metric],.2,color=COLORS[n],label=LABEL[n])
        ax.set(xticks=range(4),xticklabels=range(1,5),xlabel='Class ID',ylabel=metric.title(),ylim=(0,1));ax.legend(fontsize=8)
    export('per_class',fig,'Pooled precision/recall/F1 at 200 shots. Mean per-episode class F1 is separately tabulated.')
    for n in MODELS:
        view=pc[(pc.method==n)&(pc.budget==200)][['class_id','precision','recall','f1','support']]
        fig,ax=plt.subplots(figsize=(8,3));ax.axis('off');ax.set_title(LABEL[n]+' · 200 shots/class');tbl=ax.table(cellText=[[str(int(row[0])),*[f'{v:.4f}' for v in row[1:4]],f'{int(row[4]):,}'] for row in view.to_numpy()],colLabels=view.columns,loc='center');tbl.auto_set_font_size(False);tbl.set_fontsize(11);tbl.scale(1,1.7)
        export('per_class_'+n,fig,'Pooled class metrics; support counts repeated query appearances.')
    # Spatial directions remain separate; random controls are contextual, not matched query geography.
    sp=[]
    for n in MODELS:
        means=[]
        for axis in (0,1):
            for side in (0,1):
                v=spatial[(spatial.method==n)&(spatial.axis==axis)&(spatial.support_side==side)].f1.to_numpy();means.append(v.mean());sp.append(dict(method=n,diagnostic=('x' if axis==0 else 'y')+('_low_to_high' if side==0 else '_high_to_low'),mean=v.mean(),population_sd=v.std(),episodes=len(v),protocol='spatial buffered; paired within direction'))
        for label,val in [('x_half',np.mean(means[:2])),('y_half',np.mean(means[2:])),('worst_direction',min(means)),('four_direction_mean',np.mean(means))]:sp.append(dict(method=n,diagnostic=label,mean=val,population_sd=None,episodes=40 if label=='four_direction_mean' else None,protocol='summary of directional means; no synthetic SD'))
        v=scores.loc[200,n].values;sp.append(dict(method=n,diagnostic='random_pixel_control',mean=v.mean(),population_sd=v.std(),episodes=len(v),protocol='same budget/population exclusions; different query geography'))
    sdf=table('spatial',sp);spgain=[]
    for axis in (0,1):
        for side in (0,1):
            pair=spatial[(spatial.axis==axis)&(spatial.support_side==side)].pivot(index='trial',columns='method',values='f1')
            for n in MODELS[:-1]:
                d=pair.Coordinate_RF-pair[n];spgain.append(dict(axis=axis,support_side=side,control=n,n_pairs=len(d),mean_gain=d.mean(),population_sd=d.std(ddof=0)))
    table('spatial_matched_control',spgain)
    for name,keys in [('spatial',['x_low_to_high','x_high_to_low','y_low_to_high','y_high_to_low']),('spatial_summary',['x_half','y_half','worst_direction','four_direction_mean','random_pixel_control'])]:
        fig,ax=plt.subplots(figsize=(11,5))
        for j,n in enumerate(MODELS):
            d=sdf[sdf.method==n].set_index('diagnostic').loc[keys];ax.bar(np.arange(len(keys))+(j-1.5)*.2,d['mean'],.2,yerr=d.population_sd.fillna(0),capsize=2,color=COLORS[n],label=LABEL[n])
        ax.set(xticks=range(len(keys)),xticklabels=[k.replace('_','\n') for k in keys],ylabel='Macro F1',ylim=(.45,.85));ax.legend(ncol=2);export(name,fig,'10 paired trials per spatial direction, 10-key-unit buffer; 200 shots. Summary bars have no fabricated SD. Random control has different geography.')
    ab=load(H/'ablation_complete.json');opt=load(H/'optimization_complete.json');abl=[]
    for origin,obj in [('factorial',ab),('mechanism',opt)]:
        names=list(obj['summary']['160']) if origin=='factorial' else ['No_source_prior','Coordinate_RF']
        for n in names:
            v=obj['summary']['160'][n];abl.append(dict(method=n,origin=origin,shots=160,mean=v['mean'],population_sd=v['population_sd'],episodes=v['episodes'],configuration=json.dumps(obj['configurations'].get(n,{}),sort_keys=True),protocol='five development folds; 160 train/40 validation per class'))
    adf=table('ablation',abl);fig,ax=plt.subplots(figsize=(10,7));ax.barh(adf.method,adf['mean'],xerr=adf.population_sd,color=['#009E73' if n=='Coordinate_RF' else '#377EB8' for n in adf.method]);ax.set(xlabel='Development-support macro F1 ± population SD',xlim=(.45,.86),title='Saved operational ablations · not final-query results');export('ablation',fig,'A=RF, B=pool covariance, C=Gaussian graph, D=adaptive shrinkage; factorial prior disabled. Mechanism rows use full ASTRA recipe. Not an additive causal ladder.')
    # Distribution plots show every budget and model.
    for kind in ('histogram','boxplot','violin','density'):
        fig,axes=plt.subplots(1,5,figsize=(18,4),sharey=kind in ('boxplot','violin'))
        for ax,b in zip(axes,BUDGETS):
            vals=[scores.loc[b,n].values for n in MODELS]
            if kind=='boxplot':ax.boxplot(vals,tick_labels=[LABEL[n] for n in MODELS],showfliers=True)
            elif kind=='violin':
                parts=ax.violinplot(vals,showmedians=True)
                for body,n in zip(parts['bodies'],MODELS):body.set_facecolor(COLORS[n])
                ax.set(xticks=range(1,5),xticklabels=[LABEL[n] for n in MODELS])
            else:
                for v,n in zip(vals,MODELS):
                    if kind=='histogram':ax.hist(v,bins=15,alpha=.4,label=LABEL[n],color=COLORS[n])
                    else:
                        xx=np.linspace(v.min()-.01,v.max()+.01,200);ax.plot(xx,stats.gaussian_kde(v)(xx),label=LABEL[n],color=COLORS[n])
                ax.set_xlabel('Macro F1')
            ax.set_title(f'{b} shots/class')
            if kind in ('boxplot','violin'):ax.tick_params(axis='x',labelrotation=60)
        axes[0].set_ylabel('Macro F1' if kind in ('boxplot','violin') else 'Episodes' if kind=='histogram' else 'Density');
        if kind in ('histogram','density'):axes[-1].legend(fontsize=7)
        export(kind,fig,'200 episodes per model/budget on one fixed city; density uses Gaussian KDE with default Scott bandwidth.')
    runtime=load(E/'verification/runtime.json');rd=table('runtime',runtime)
    old=[]
    for (n,b),group in rec.groupby(['method','budget']):old.append(dict(method=n,budget=b,episodes=len(group),mean_wall_seconds=group.seconds.mean(),population_sd=group.seconds.std(ddof=0),episodes_per_second=len(group)/group.seconds.sum(),scope='historical combined per-call fit/predict; cached source; no CPU or RSS instrumentation'))
    hist=table('runtime_historical',old);fig,axes=plt.subplots(1,2,figsize=(12,5))
    for n in MODELS:
        d=hist[hist.method==n];axes[0].plot(d.budget,d.mean_wall_seconds,'o-',color=COLORS[n],label=LABEL[n])
    axes[0].set(xlabel='Shots/class',ylabel='Historical call wall seconds',yscale='log');axes[0].legend(fontsize=8)
    for n in ['ASTRA_AGF','Coordinate_RF']:
        d=rd[rd.method==n];axes[1].plot(d.budget,d.wall_seconds,'o-',label=LABEL[n]+' wall');axes[1].plot(d.budget,d.cpu_seconds,'--',label=LABEL[n]+' CPU')
    axes[1].set(xlabel='Shots/class',ylabel='Verification seconds (profiled)');axes[1].legend(fontsize=8);export('runtime',fig,'Historical episode timings and single fixed-reference profiled replays are distinct regimes. No source refit; memory and RF fit/predict times in runtime.csv.')
    # Trusted pool is hash-checked before reading; covariance diagnostics are label-free.
    manifest=load(R/'candidate/best_model/INFERENCE_MANIFEST.json');assert digest(R/'candidate/best_model/pool_state.pkl')==manifest['files']['pool_state.pkl']
    with open(R/'candidate/best_model/pool_state.pkl','rb') as f:state=pickle.load(f)
    fi=table('feature_importance',load(E/'verification/feature_importance.json'));top=fi[fi.budget==200].nlargest(15,'importance').sort_values('importance');fig,ax=plt.subplots(figsize=(9,6));ax.barh(top.feature,top.importance,color=['#D89000' if n.startswith('coordinate') else '#009E73' for n in top.feature]);ax.set(xlabel='RF impurity importance',title='Coordinate_RF · first predeclared 200-shot episode');export('feature_importance',fig,'Captured from verification fit; transformed covariance axes are not raw spectral features. Impurity importance is biased and not causal.')
    coord=fi[fi.feature.str.startswith('coordinate')];table('coordinate_influence',coord);fig,ax=plt.subplots()
    for key in ('coordinate_x','coordinate_y'):
        v=coord[coord.feature==key];ax.plot(v.budget,v.importance,'o-',label=key)
    ax.set(xlabel='Shots/class',ylabel='Impurity importance',title='Coordinate split usage · first predeclared episodes');ax.legend();export('coordinate_influence',fig,'Descriptive split usage, not a perturbation or feature-selection experiment; geographic trade-off reported separately.')
    cov=state['cov'];eig=np.linalg.eigvalsh(cov);eigrows=[];fig,axes=plt.subplots(1,2,figsize=(12,5));axes[0].semilogy(range(1,61),np.maximum(eig[::-1],1e-12),label='Unshrunk pool')
    for b in BUDGETS:
        rho=min(1,60/(4*b));shr=(1-rho)*cov+rho*np.diag(np.diag(cov))+1e-7*np.eye(60);v=np.linalg.eigvalsh(shr)[::-1];axes[0].semilogy(range(1,61),v,label=f'{b} shots; ρ={rho:.3g}')
        eigrows.extend(dict(budget=b,rank=i+1,eigenvalue=float(value),raw_eigenvalue=float(eig[::-1][i]),rho=rho) for i,value in enumerate(v))
    axes[0].set(xlabel='Eigenvalue rank',ylabel='Covariance eigenvalue (log)');axes[0].legend(fontsize=8);axes[1].plot(BUDGETS,[min(1,60/(4*b)) for b in BUDGETS],'o-');axes[1].set(xlabel='Shots/class',ylabel='Diagonal shrinkage weight ρ',ylim=(0,1.05));table('covariance_eigenvalues',eigrows);export('covariance_spectrum',fig,'Exact frozen shrinkage formula; full-pool covariance is label-free. Units are mixed raw feature units.')
    fig,axes=plt.subplots(1,2,figsize=(11,5));scale=np.sqrt(np.maximum(np.diag(cov),1e-20));rho=60/800
    for ax,v,title in zip(axes,[cov,(1-rho)*cov+rho*np.diag(np.diag(cov))],['Original covariance (scaled)','200-shot shrunk covariance (scaled)']):
        im=ax.imshow(v/scale[:,None]/scale[None,:],cmap='RdBu_r',vmin=-1,vmax=1);ax.set(title=title,xlabel='Feature index',ylabel='Feature index')
    fig.colorbar(im,ax=axes[-1]);export('covariance_shrinkage',fig,'Covariance divided by original feature standard deviations for display. Visualization does not change model inputs.')
    calibration=[];transfer=[];b=200
    for n in ['ASTRA_AGF','Coordinate_RF']:
        with np.load(E/f'verification/{n}_b{b}.npz') as a:
            q=a['query'];y=truth[q];prob=a['probability'];confid=prob.max(1);correct=(prob.argmax(1)+1)==y
            for lo in np.arange(0,1,.1):
                mask=(confid>=lo)&(confid<lo+.1 if lo<.9 else confid<=1);calibration.append(dict(method=n,budget=b,trial=0,bin_low=lo,bin_high=min(1,lo+.1),count=int(mask.sum()),mean_confidence=float(confid[mask].mean()) if mask.any() else None,accuracy=float(correct[mask].mean()) if mask.any() else None))
            from sklearn.metrics import f1_score,log_loss
            if n=='ASTRA_AGF':
                for label,pp in [('Source only',state['prior'][q]),('Target only (pre-blend)',a['local_probability']),('Blended (pre-graph)',a['blended_probability'])]:transfer.append(dict(stage=label,macro_f1=f1_score(y,pp.argmax(1)+1,average='macro'),budget=200,trial=0,protocol='same query; observational internal ASTRA stages; not separately tuned controls'))
            transfer.append(dict(stage=LABEL[n],macro_f1=f1_score(y,prob.argmax(1)+1,average='macro'),budget=200,trial=0,protocol='fixed-reference final predictions'))
    cal=table('calibration',calibration);fig,ax=plt.subplots();ax.plot([0,1],[0,1],'--',color='gray')
    for n in ['ASTRA_AGF','Coordinate_RF']:
        d=cal[(cal.method==n)&(cal['count']>0)];ax.plot(d.mean_confidence,d.accuracy,'o-',color=COLORS[n],label=LABEL[n])
    ax.set(xlabel='Mean maximum probability',ylabel='Observed accuracy',xlim=(0,1),ylim=(0,1),title='Reliability · first predeclared 200-shot episode');ax.legend();export('calibration',fig,'Evaluation only; no calibrator fitted. Ten fixed equal-width confidence bins. Spatially dependent pixels; no binomial independence intervals.')
    tr=table('transfer',transfer);fig,ax=plt.subplots(figsize=(10,5));ax.bar(range(len(tr)),tr.macro_f1,color=['#737373','#D89000','#984EA3','#377EB8','#009E73']);ax.set(xticks=range(len(tr)),xticklabels=[s.replace(' (','\n(') for s in tr.stage],ylabel='Macro F1',title='Observed transfer stages · first 200-shot episode');export('transfer',fig,'Source-only uses saved contextual prior; target-only and blend are internal ASTRA probabilities before graph smoothing. No additive/causal claim; one fixed episode, no error bars.')
    save(E/'analysis_validation.json',dict(prediction_arrays_checked=audit_count,support_query_disjoint=True,development_query_disjoint=True,confusion_and_macro_f1_agree=True,pair_keys_unique=True,query_labels_used_only_for_evaluation=True))
    save(R/'candidate/publication/FIGURE_MANIFEST.json',figure_manifest)
    env=dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,executable=sys.executable,os=platform.platform(),machine=platform.machine(),cpu=platform.processor(),logical_cpus=psutil.cpu_count(),physical_cpus=psutil.cpu_count(logical=False),ram_bytes=psutil.virtual_memory().total,git_commit=git_commit(),git_dirty=True,packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},environment_variables={k:os.environ.get(k,'<unset>') for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONHASHSEED','CUDA_VISIBLE_DEVICES']},seeds=dict(publication_bootstrap=SEED,bootstrap_replicates_gain=20000,bootstrap_replicates_mean=10000,**load(H/'configuration.json')))
    save(E/'environment_summary.json',env)
    packages=['numpy','scipy','scikit-learn','matplotlib','pandas','psutil','threadpoolctl','pillow']
    req='\n'.join(n+'=='+importlib.metadata.version(n) for n in packages)+'\n';(R/'requirements-repro.txt').write_text(req);(E/'requirements-repro.txt').write_text(req)
    source_names=['final_complete.json','spatial_complete.json','ablation_complete.json','optimization_complete.json','SELECTION_LOCK.json','provenance.json','configuration.json','clean_replay/verification.json']
    save(E/'source_manifest.json',{(H/n).relative_to(R).as_posix():digest(H/n) for n in source_names})
    (P/'README.md').write_text('# PowerPoint assets\n\nTransparent, tightly cropped 350-DPI PNGs are in this directory. Canonical opaque PNGs, editable SVGs and vector PDFs are in [../figures/publication/](../figures/publication/). Insert those directly; no redundant copies. See [figure manifest](../publication/FIGURE_MANIFEST.json) for captions. All plots use DejaVu Sans and a consistent palette. Prior slide decks remain historical.\n',encoding='utf-8')
    (D/'STATISTICAL_ANALYSIS.md').write_text('''# Statistical analysis

All 15 comparisons (three controls × five budgets) were paired on saved budget/trial keys, with 200 pairs each. Reported: two-sided paired t-test, Wilcoxon signed-rank (SciPy auto method; zero differences discarded), 20,000 paired percentile-bootstrap 95% intervals for the mean gain, paired Cohen dz (sample SD of differences), paired rank-biserial effect and marginal Cliff delta. Holm correction is applied over 15 comparisons separately for each test family. Marginal Cliff delta ignores matching and is supplementary. Mean-score CIs use 10,000 bootstrap resamples; figure error bars are population SD, not CIs. Seed: 20260911.

These are conditional support-sampling analyses on a fixed target city with heavily overlapping query pixels. They do not measure city-level generalization, erase historical audit selection, or support independent-pixel significance. Bootstrap resamples episodes, never individual pixels. Normality/symmetry assumptions of t/Wilcoxon tests may fail; agreement across tests does not resolve geographic dependence or development selection. No causal or universal superiority claim is made. The tiny five-shot difference is not a meaningful practical gain. See [significance table](../tables/significance.md).
''',encoding='utf-8')
    (D/'RUNTIME_REPORT.md').write_text('''# Runtime evidence

[runtime.csv](../tables/runtime.csv) measures ten fixed-reference calls (one episode per budget for Coordinate_RF and ASTRA), not a timing search. Calls exactly matched saved predictions. Wall time uses perf_counter; CPU uses process_time (process-wide CPU, excluding profiler sampling thread waiting); RF fit and predict_proba durations use observational sys.setprofile. Five-millisecond psutil sampling reports absolute process RSS before/after and sampled peak, not a guaranteed OS high-water mark or model-only allocation. It can miss short peaks. Calls include instrumentation overhead, label-free transforms, forest fitting, full-pool prediction, blending and graph smoothing. They exclude artifact loading and source-prior training. Predictions/sec uses either full pool or query count explicitly. Training/prediction columns cover the local RF only; they do not sum to full wall time.

[Historical timings](../tables/runtime_historical.csv) summarize existing 200-episode combined fit/predict calls per budget for all four models. Historical CPU, separated fit/predict and memory were not recorded and cannot be reconstructed. Source training timing is retained in the historical port_check.json; source fitting was not repeated. Single verification timings lack uncertainty estimates and should not be ranked as rigorous performance benchmarks. Environment and hardware are recorded in the reproducibility bundle.
''',encoding='utf-8')
    (D/'SPATIAL_ANALYSIS.md').write_text('''# Geographic robustness

At 200 shots/class, saved audits use a 10-lattice-key buffer and 10 episodes in each of four directions. All methods share direction/trial support and query sets. [Matched gains](../tables/spatial_matched_control.md) use those keys. The random-pixel control has the same budget and development exclusion, but a different query geography; it is not an exact matched spatial control.

Coordinate_RF: x-half 0.682326, y-half 0.706106, worst direction 0.644816, four-direction mean 0.694216. ASTRA: 0.687017, 0.706326, 0.658183, 0.696672 respectively. Coordinate_RF loses about 0.028670 on high-x → low-x. Random-pixel gains therefore coexist with worse geographic extrapolation. Coordinates can exploit local structure without guaranteeing transfer beyond observed support regions. No model selection or changes followed this audit. New cities and geographically blocked organizer tests remain necessary.
''',encoding='utf-8')
    (D/'DIAGNOSTIC_LIMITATIONS.md').write_text('''# Diagnostic scope and unavailable evidence

- All four models: learning curves, distributions, confusion and per-class metrics use all saved locked episodes. Confusion images use 200 shots; CSV/Markdown cover every budget.
- Transfer: source-only, target-only and blended are observational probabilities from the fixed ASTRA replay before graph smoothing; final ASTRA/Coordinate_RF share its query. One predeclared episode, not new ablation trials or additive causal effects.
- RF importance: captured from the unmodified local Coordinate_RF verification fit. The 60 whitened axes mix original spectral inputs; do not relabel them as raw feature importance. Coordinate usage is split importance, not causal attribution.
- Covariance diagnostics: label-free saved population covariance and the exact frozen shrinkage equation. No covariance optimization.
- Calibration: ASTRA and Coordinate_RF probabilities from the first predeclared 200-shot replay, ten fixed bins. No post-hoc calibration. EXP-010 and EXP-F probability calibration is unavailable from saved hard predictions and was not invented.
- Historical four-model CPU/peak memory and separated fit/predict measurements are unavailable. Fresh instrumentation covers ASTRA and Coordinate_RF only. Sampled RSS is not exact peak allocation.
- Factorial mechanisms are operationally entangled; no additive contribution ladder is justified. All legacy exploratory outputs remain historical, with their original caveats.
''',encoding='utf-8')
    print('Built',len(figure_manifest),'figure sets; validated',audit_count,'prediction arrays')
if __name__=='__main__':main()
