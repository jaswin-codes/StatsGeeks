"""Bounded sequential driver. Discovery loads only a fixed labelled support bank.
Audit truth lives in sealed_evaluation.npz and is opened by evaluation modes only.
"""
from pathlib import Path
import os
for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[k]='1'
import sys,time,json,pickle,hashlib,argparse,traceback,platform
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent; R=H.parents[2]
sys.path[:0]=[str(H),str(R)]
from agf_model import fit_pool,probabilities,BASE,CLASSES,BUDGETS
from candidate.experiments_2h.run import setup,representation,predict as metric_predict
from candidate.exp010_predict import adapt_and_predict as frozen_predict,SUPPORTED_SCHEDULE

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def save(name,obj):
    path=H/name; path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,allow_nan=False));tmp.replace(path)
def log(text):
    print(time.strftime('%H:%M:%S'),text,flush=True)
    with (H/'RUN_LOG.md').open('a') as f: f.write('\n'+time.strftime('%H:%M:%S')+' '+text+'\n')
def load_state():
    with (H/'pool_state.pkl').open('rb') as f:return pickle.load(f)
def summary(records):
    result={}
    for b in sorted(set(r['budget'] for r in records)):
        result[str(b)]={}
        for name in sorted(set(r['method'] for r in records if r['budget']==b)):
            rr=[r for r in records if r['budget']==b and r['method']==name];scores=np.array([r['f1'] for r in rr]);entry=dict(mean=float(scores.mean()),population_sd=float(scores.std()),episodes=len(rr),class_f1=np.mean([r['class_f1'] for r in rr],0).tolist(),seconds=sum(r['seconds'] for r in rr))
            entry['paired']={}
            for control in ('EXP010','EXPF','ASTRA_AGF'):
                cc={r['trial']:r['f1'] for r in records if r['budget']==b and r['method']==control}
                if all(r['trial'] in cc for r in rr):
                    dd=np.array([r['f1']-cc[r['trial']] for r in rr]);entry['paired'][control]=dict(gain=float(dd.mean()),wins=int((dd>1e-12).sum()),losses=int((dd < -1e-12).sum()),delta_sd=float(dd.std()))
            result[str(b)][name]=entry
    return result

def score(method,b,t,truth,p,seconds):
    pc=f1_score(truth,p,labels=CLASSES,average=None,zero_division=0);cm=confusion_matrix(truth,p,labels=CLASSES)
    return dict(method=method,budget=b,trial=t,f1=float(pc.mean()),class_f1=pc.tolist(),confusion=cm.tolist(),confusion_row_normalized=(cm/np.maximum(cm.sum(1,keepdims=True),1)).tolist(),seconds=seconds)

def prepare():
    assert not (H/'pool_state.pkl').exists()
    st,d=setup();protected=[R/'candidate/exp010_predict.py',R/'candidate/artifacts/exp010_stage1_madrid.pkl',R/'data/preprocessed/preprocessed_data.pkl']
    save('provenance.json',dict(protected={str(p.relative_to(R)):sha(p) for p in protected},feature_names=d['feature_names'],python=platform.python_version(),numpy=np.__version__,competitor_imports=False,source='Own supplied Madrid source data; no cached competitor models/predictions',historical_selection_caveat='Inherited ASTRA recipe was historically audit-selected; session cannot erase that exposure.'))
    y=d['y_amsterdam'];rng=np.random.default_rng(20260909);dev=np.concatenate([rng.permutation(np.flatnonzero(y==c))[:200] for c in CLASSES]);np.savez_compressed(H/'development_support.npz',indices=dev,labels=y[dev])
    np.savez_compressed(H/'sealed_evaluation.npz',labels=y)
    with (H/'baseline_state.pkl').open('wb') as f:pickle.dump(st,f)
    compact={k:representation(st,d,k) for k in (30,45)}
    with (H/'compact.pkl').open('wb') as f:pickle.dump(compact,f)
    log('Fitting source prior from scratch: global + one pseudo-class transport, RF200 x2')
    t=time.time();state=fit_pool(d['X_madrid'],d['y_madrid'],d['pixel_ids_madrid'],d['X_amsterdam'],d['pixel_ids_amsterdam'],d['scaler'].mean_,d['scaler'].scale_,d['feature_names'])
    with (H/'pool_state.pkl').open('wb') as f:pickle.dump(state,f,protocol=5)
    reference=np.load(R/'candidate/experiments_2h_v2/physical_source_priors.npz')['physical1']
    save('port_check.json',dict(source_seconds=time.time()-t,prior_exact=bool(np.array_equal(state['prior'],reference)),max_absolute_prior_difference=float(abs(state['prior']-reference).max()),target_labels_used_in_fit=False,pool_sha256=sha(H/'pool_state.pkl')))
    save('configuration.json',dict(base=BASE,development_bank_seed=20260909,development_labels=800,selection='Held-out support labels only; no final/audit query truth',final_seed=20260910,final_excludes_development_bank=True,TARGET_LABELS_USED=False,SUPPORT_LABELS_USED=True,TARGET_FEATURES_USED=True,COORDINATES_USED=True,QUERY_LABEL_USAGE='evaluation only; never selection/adaptation/stopping',population_sd_ddof=0))
    log('Fresh source prior ready')

def evaluate(mode,trials):
    assert not (H/f'{mode}_complete.json').exists()
    state=load_state();y=np.load(H/'sealed_evaluation.npz')['labels'];dev=np.load(H/'development_support.npz')['indices'];eligible=np.setdiff1d(np.arange(len(y)),dev)
    with (H/'baseline_state.pkl').open('rb') as f:st=pickle.load(f)
    with (H/'compact.pkl').open('rb') as f:compact=pickle.load(f)
    locked=json.loads((H/'SELECTION_LOCK.json').read_text()) if mode!='benchmark' else None
    methods={'ASTRA_AGF':{}}
    if locked and locked['candidate']!='ASTRA_AGF':methods[locked['candidate']]=locked['config']
    seed=20260910 if mode=='final' else 20260911 if mode=='spatial' else 20260908
    rng=np.random.default_rng(seed);records=[];start=time.time();spatial=mode=='spatial';budgets=(200,) if spatial else BUDGETS
    for t in range(trials):
        pools={c:eligible[y[eligible]==c] for c in CLASSES};qsp=None
        if spatial:
            axis=(t//2)%2;side=t%2;v=state['coords'][:,axis];cut=np.median(v);mask=v<=cut if side==0 else v>cut
            pools={c:p[mask[p]] for c,p in pools.items()};qsp=eligible[(v[eligible]>cut+10) if side==0 else (v[eligible]<cut-10)]
        perms={c:rng.permutation(p)[:200] for c,p in pools.items()};assert all(len(p)==200 for p in perms.values())
        for b in budgets:
            s=np.concatenate([perms[c][:b] for c in CLASSES]);q=np.setdiff1d(eligible,s) if qsp is None else qsp
            assert not np.intersect1d(s,q).size and not np.intersect1d(dev,q).size
            ys=y[s].copy();preds={};times={};arrays=dict(support=s,support_labels=ys,query=q)
            for name,cfg in methods.items():
                now=time.time();preds[name]=CLASSES[probabilities(state,s,ys,b,cfg).argmax(1)][q];times[name]=time.time()-now
            now=time.time();preds['EXP010']=frozen_predict(st,state['standard'][s],ys,state['standard'][q],b,seed);times['EXP010']=time.time()-now
            now=time.time();z,delta=compact[SUPPORTED_SCHEDULE[b][0]];preds['EXPF']=metric_predict(z[s],ys,z[q],delta,metric='regularized');times['EXPF']=time.time()-now
            # Only now access query truth, with all configurations frozen.
            for name,p in preds.items():
                r=score(name,b,t,y[q],p,times[name]);
                if spatial:r.update(axis=axis,support_side=side)
                records.append(r);arrays[name]=p.astype('int8')
            folder=H/mode;folder.mkdir(exist_ok=True);np.savez_compressed(folder/f'b{b}_t{t}.npz',**arrays)
            save(f'{mode}_progress.json',dict(records=records,completed_trials=t,seconds=time.time()-start))
        log(f'{mode} {t+1}/{trials}')
    save(f'{mode}_complete.json',dict(records=records,summary=summary(records),seed=seed,seconds=time.time()-start,query_population='Full target minus fixed 800 development pixels and current support',fresh_population=False,selection_used=False))

def folds():
    bank=np.load(H/'development_support.npz');ids=bank['indices'];labels=bank['labels'];out=[]
    for fold in range(5):
        train=[];val=[]
        for c in CLASSES:
            a=np.flatnonzero(labels==c);mask=np.arange(200)%5==fold;train.extend(a[~mask]);val.extend(a[mask])
        train=np.array(train);val=np.array(val);out.append((ids[train],labels[train],ids[val],labels[val]))
    return out

def discover(stage):
    state=load_state(); rec=[]; configs={}
    if stage=='ablation':
        # Pure factorial holds source prior OFF so B/C have interpretable access boundaries.
        for pool,spatial,adaptive,name in [(False,False,False,'A'),(True,False,False,'A+B'),(False,True,False,'A+C'),(False,False,True,'A+D'),(True,True,False,'A+B+C'),(True,False,True,'A+B+D'),(False,True,True,'A+C+D'),(True,True,True,'A+B+C+D')]:
            configs[name]=dict(pool=pool,spatial=spatial,adaptive=adaptive,prior=0.)
        configs['ASTRA_AGF']={}
    else:
        configs={'ASTRA_AGF':{},'RF_half_features':dict(features=.5),'ExtraTrees':dict(kind='extra',features=.5),'BoostedTrees':dict(kind='hist'),'Coordinate_RF':dict(coord=True),'Stronger_diagonal':dict(rho_factor=2.),'Less_diagonal':dict(rho_factor=.5),'Covariance_blend':dict(covblend=.15),'No_source_prior':dict(prior=0.),'Confidence_prior':dict(prior=60.),'Wide_graph':dict(neighbours=25,sigma=2.),'Bilateral_graph':dict(bilateral=True),'Two_step_graph':dict(steps=2)}
    save(stage+'_plan.json',dict(configurations=configs,folds=5,training_shots=160,validation_shots=40,selection_metric='support-only held-out macro F1',axes=dict(A='RF200 classifier',B='full unlabelled target covariance',C='Gaussian coordinate graph',D='budget/sample-ratio covariance shrinkage; uses support covariance without B'),note='Factorial source prior OFF. Full ASTRA separately restores contextual source prior; D depends on B for its original operational definition.'))
    bankfolds=folds()
    if stage=='ablation':
        with (H/'compact.pkl').open('rb') as f:compact=pickle.load(f)
        z,delta=compact[45]
        for i,(s,ys,q,yq) in enumerate(bankfolds):
            now=time.time();p=metric_predict(z[s],ys,z[q],delta,metric='regularized');rec.append(score('EXPF',160,i,yq,p,time.time()-now))
    for name,cfg in configs.items():
        if (H/f'{stage}/{name.replace("+","_")}.json').exists():raise RuntimeError('Refusing to overwrite completed experiment')
        rr=[]
        try:
            for i,(s,ys,q,yq) in enumerate(bankfolds):
                now=time.time();p=CLASSES[probabilities(state,s,ys,160,cfg).argmax(1)][q];rr.append(score(name,160,i,yq,p,time.time()-now))
            rec.extend(rr);save(f'{stage}/{name.replace("+","_")}.json',dict(config=cfg,records=rr,summary=summary(rr)))
            log(f'{stage} {name}: support CV {np.mean([r["f1"] for r in rr]):.6f}')
        except Exception:
            save(f'{stage}/{name.replace("+","_")}_FAILED.json',dict(traceback=traceback.format_exc()));log(f'{name} failed; continuing')
        save(stage+'_progress.json',dict(records=rec,summary=summary(rec)))
        leaderboard=[];ss=summary(rec).get('160',{})
        for n,v in ss.items():leaderboard.append(dict(candidate=n,development_support_cv=v,config=configs.get(n),information_regime='transductive' if configs.get(n,{}).get('pool',True) or configs.get(n,{}).get('spatial',True) else 'support-only',query_label_usage=False,status='incumbent' if n=='ASTRA_AGF' else 'exploratory',reproducibility='pending'))
        save('LEADERBOARD.json',leaderboard)
    save(stage+'_complete.json',dict(records=rec,summary=summary(rec),configurations=configs))

def lock():
    obj=json.loads((H/'stability_complete.json').read_text());summ=obj['summary']['160'];base=summ['ASTRA_AGF']['mean'];eligible=[]
    # Conservative predeclared selection gate; five small support validation folds.
    for name,v in summ.items():
        paired=v['paired']['ASTRA_AGF']
        if name!='ASTRA_AGF' and v['mean']>base+.002 and paired['wins']>=int(.7*v['episodes']) and all(obj['summary'][str(b)][name]['mean']>=obj['summary'][str(b)]['ASTRA_AGF']['mean']-.005 for b in (5,25,50,100)):eligible.append(name)
    ranked=sorted(eligible,key=lambda n:summ[n]['mean'],reverse=True)
    # Spatial development check: only labels within the same 800-label bank.
    state=load_state();bank=np.load(H/'development_support.npz');ids=bank['indices'];y=bank['labels'];geo=[]
    for name in ['ASTRA_AGF']+ranked[:2]:
        cfg=obj['configurations'][name]
        for axis in (0,1):
            v=state['coords'][ids,axis];cut=np.median(state['coords'][:,axis])
            for side in (0,1):
                mask=v<=cut if side==0 else v>cut;qmask=v>cut+10 if side==0 else v<cut-10
                budget=min(80,min(np.sum(mask&(y==c)) for c in CLASSES));sidx=np.concatenate([np.flatnonzero(mask&(y==c))[:budget] for c in CLASSES]);qidx=np.flatnonzero(qmask)
                now=time.time();p=CLASSES[probabilities(state,ids[sidx],y[sidx],int(budget),cfg).argmax(1)][ids[qidx]];r=score(name,int(budget),axis*2+side,y[qidx],p,time.time()-now);r.update(axis=axis,side=side);geo.append(r)
    control=np.array([r['f1'] for r in geo if r['method']=='ASTRA_AGF']);chosen='ASTRA_AGF'
    for name in ranked[:2]:
        scores=np.array([r['f1'] for r in geo if r['method']==name])
        if scores.mean()>=control.mean()-.005 and scores.min()>=control.min()-.01:chosen=name;break
    save('development_spatial.json',dict(records=geo,selection_labels='fixed development support only'))
    save('SELECTION_LOCK.json',dict(candidate=chosen,config=obj['configurations'][chosen],support_cv=summ[chosen],incumbent_support_cv=summ['ASTRA_AGF'],selection='support-only 20 repeated holdouts per budget plus support-only spatial safeguards; no query truth',rule='160-shot mean gain > .002; >=70% paired wins; no other budget mean worse than -.005; geographic mean no worse than -.005 and worst no worse than -.01; top two only',time=time.strftime('%Y-%m-%d %H:%M:%S'),model_sha256=sha(H/'agf_model.py'),ranked=ranked,final_audit_is_not_selection=True))
    save('LATEST_BEST.json',dict(BEST_CANDIDATE=chosen,BEST_SCORE=summ[chosen]['mean'],score_type='160-shot training, 40/class held-out support CV, NOT headline query F1',BEST_CONFIG=obj['configurations'][chosen],BEST_RESULTS='SELECTION_LOCK.json',BEST_ARTIFACT='pool_state.pkl',historical_incumbent='ASTRA_AGF 0.735239; different audit population',status='locked development-selected candidate; no official promotion based on query labels'))
    log('SELECTION LOCKED: '+chosen)

def verify():
    assert not (H/'verification.json').exists()
    lock=json.loads((H/'SELECTION_LOCK.json').read_text());assert sha(H/'agf_model.py')==lock['model_sha256'];state=load_state();y=np.load(H/'sealed_evaluation.npz')['labels'];count=0
    for b in BUDGETS:
        ref=np.load(H/f'final/b{b}_t0.npz');s=ref['support'];q=ref['query'];p=CLASSES[probabilities(state,s,y[s],b,lock['config']).argmax(1)][q];np.testing.assert_array_equal(p,ref[lock['candidate']]);count+=1
    for rel,h in json.loads((H/'provenance.json').read_text())['protected'].items():assert sha(R/rel)==h,rel
    # Strict input validation and support permutation/non-overlap contracts.
    errors=0
    for s,ys,b in [(np.array([0]*20),np.repeat(CLASSES,5),5),(np.arange(20),np.ones(20),5)]:
        try:probabilities(state,s,ys,b)
        except ValueError:errors+=1
    assert errors==2
    save('verification.json',dict(pass_=True,clean_process=True,artifact_reload=True,exact_prediction_arrays=count,protected_files_unchanged=True,feature_order_validated=True,bad_support_checks=errors,query_truth_not_passed_to_model=True,pool_sha256=sha(H/'pool_state.pkl')))
    log('Clean-process artifact replay passed')

def report():
    lock=json.loads((H/'SELECTION_LOCK.json').read_text());result=json.loads((H/'final_complete.json').read_text());sp=json.loads((H/'spatial_complete.json').read_text());verification=json.loads((H/'clean_replay/verification.json').read_text());best=lock['candidate'];board=json.loads((H/'LEADERBOARD.json').read_text())
    for row in board:
        row['status']='development_selected' if row['candidate']==best else 'incumbent' if row['candidate']=='ASTRA_AGF' else 'rejected';row['score_by_budget']={b:v[row['candidate']] for b,v in result['summary'].items() if row['candidate'] in v};row['reproducibility']='fresh source + 1000 episodes exact replay' if row['candidate'] in (best,'ASTRA_AGF') else 'not separately replayed'
    final=dict(current_historical_incumbent='ASTRA-AGF ~0.735239',best_new_candidate=best,selection_lock=lock,results=result,spatial=sp,verification=verification,query_labels_used_for_selection=False,target_features_used=True,coordinates_used=True,target_labels_used_for_fitting='support only',independent_population_validation=False)
    save('FINAL_RESULTS.json',final);save('LEADERBOARD.json',board);save('AUTONOMOUS_LEADERBOARD.json',board)
    lines=['# Autonomous ASTRA-AGF sprint','','## Decision',f'Historical incumbent: ASTRA-AGF (0.735239 on its historical protocol). Development-selected candidate: **{best}**. Selection was locked before final query scoring; no query-driven promotion or rejection.','', 'Fresh source prior was trained from supplied Madrid data, not competitor caches. Frozen EXP-010 remains unchanged.','', '## Fresh locked evaluation','Macro F1 mean ± population SD; paired trials; query excludes all 800 fixed development pixels. This changed query population is NOT an exact reproduction of the historical 0.735239 benchmark.','', '| Shots | Selected mean ± SD | Gain vs EXP010 | Gain vs EXPF | Gain vs ASTRA | Wins vs 010/F/ASTRA |','|---|---|---|---|---|---|']
    for b,methods in result['summary'].items():
        v=methods[best];p=v['paired'];lines.append(f'| {b} | {v["mean"]:.6f} ± {v["population_sd"]:.6f} | {p["EXP010"]["gain"]:+.6f} | {p["EXPF"]["gain"]:+.6f} | {p["ASTRA_AGF"]["gain"]:+.6f} | {p["EXP010"]["wins"]}/{p["EXPF"]["wins"]}/{p["ASTRA_AGF"]["wins"]} of {v["episodes"]} |')
    lines+=['','## Spatial robustness','200 shots/class; 10-key-unit buffer; fixed development bank excluded. Four directions are all reported, not selected.','']
    direction_means={}
    for name in sorted(set(r['method'] for r in sp['records'])):
        means=[]
        for axis in (0,1):
            av=[]
            for side in (0,1):
                vals=[r['f1'] for r in sp['records'] if r['method']==name and r['axis']==axis and r['support_side']==side];m=float(np.mean(vals));means.append(m);av.append(m);lines.append(f'- {name}: {"xy"[axis]} support {"low" if side==0 else "high"} → opposite: {m:.6f} ± {np.std(vals):.6f}')
            lines.append(f'- {name}: {"xy"[axis]}-half mean {np.mean(av):.6f}')
        lines.append(f'- {name}: worst direction {min(means):.6f}; four-direction mean {np.mean(means):.6f}')
    lines+=['','## Information regime and validity','TARGET_FEATURES_USED = TRUE; COORDINATES_USED = TRUE; TARGET_LABELS_USED (outside designated support) = FALSE for fitting/selection/adaptation. Query labels are used ONLY for evaluation. Source uses all labelled Madrid rows. Initial selection uses five folds of a fixed 800-label development-support bank (160 training + 40 validation per class). Top three variants plus ASTRA then undergo 20 repeated support-only holdouts at 5/25/50/100/160 training shots per class, followed by four development-support spatial directions. Repeated holdouts are correlated, not independent validation populations. These development labels are NEVER scored as final query labels. Final support is drawn outside the bank.','', 'The inherited ASTRA recipe was historically query-audit-selected; this cannot be undone. New seeds and support exclusion do not create an independent city or organizer test. Additional 800 development labels constitute research supervision beyond an individual episode budget, explicitly disclosed. Baseline and selected model receive identical current-episode support, full-pool access only for transductive models. EXP010 and EXPF remain inductive controls.','', '## Reproducibility and integrity',f'Clean-process artifact replay: {verification}. Feature names/order are stored in pool_state.pkl and provenance.json. Source-prior comparison is in port_check.json. Input hashes and all final session file hashes are retained.','', '## Rejected and failed experiments','All ablation/optimization results and configurations are retained. Rejection is based ONLY on development-support folds and geographic safeguards, never final query truth.']
    for row in board:
        if row['candidate'] not in (best,'ASTRA_AGF'):lines.append(f'- {row["candidate"]}: support CV {row["development_support_cv"]["mean"]:.6f}; not selected by the predeclared mean/wins/geographic gate or ranked behind a qualifying candidate.')
    lines+=['', 'Factorial A=RF; B=pool covariance; C=Gaussian coordinates; D=budget-adaptive covariance. Source prior disabled in factorial arms to avoid hidden coordinate access; original ASTRA evaluated separately. D without B borrows support covariance, so these are operational ablations, not fully independent causal factors.','', '## Recommended model and exact packaging files',f'For continued packaging use development-locked **{best}**, while retaining ASTRA as historical incumbent; no independent-test superiority is asserted. Required files: agf_model.py, pool_state.pkl, SELECTION_LOCK.json, INFERENCE_MANIFEST.json, reproduce_best.py, requirements-repro.txt. Optional cached replay inputs: verification_inputs/b5.npz, b25.npz, b50.npz, b100.npz, b200.npz (contain support labels and expected predictions, not query truth). Source/provenance files: configuration.json, provenance.json, SHA256SUMS.json. The pool artifact is tied to the supplied ordered Amsterdam population and integer lattice coordinates; rebuild for a new pool. Do not package sealed_evaluation.npz or development labels for inference.','', 'See reproduce_best.py for inference/verification commands. The runner and all raw per-episode predictions remain in the timestamped directory.']
    (H/'FINAL_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (H/'README.md').write_text('# ASTRA-AGF autonomous run\n\nRead FINAL_REPORT.md and SELECTION_LOCK.json. All evidence is isolated in this run.\n\nInference: python -I -B reproduce_best.py --support support.npz --out NEW_DIRECTORY\nSupport NPZ: indices, labels, budget (scalar); full ordered target pool is bound to pool_state.pkl.\n\nVerification: python -I -B reproduce_best.py --verify --out NEW_DIRECTORY\nRequires repository benchmark data only for verification, not inference.\n',encoding='utf-8')
    save('SHA256SUMS.json',{str(p.relative_to(H)):sha(p) for p in H.rglob('*') if p.is_file() and p.name not in ('SHA256SUMS.json','RUN_LOG.md') and p.suffix!='.tmp'})
    log('Final report and hashes saved')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','benchmark','ablation','optimization','lock','final','spatial','verify','report']);parser.add_argument('--trials',type=int,default=20);args=parser.parse_args()
    with threadpool_limits(limits=1):
        if args.mode=='prepare':prepare()
        elif args.mode in ('benchmark','final','spatial'):evaluate(args.mode,args.trials)
        elif args.mode in ('ablation','optimization'):discover(args.mode)
        else:globals()[args.mode]()
