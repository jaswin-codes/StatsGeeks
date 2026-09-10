"""Support-only sequential refinement; this file never loads audit truth."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from sprint import *

def refine():
    state=load_state();obj=json.loads((H/'optimization_complete.json').read_text());rec=list(obj['records']);cfgs=dict(obj['configurations'])
    more={'Extra_sqrt':dict(kind='extra'),'Extra_coordinates':dict(kind='extra',features=.5,coord=True),'Forest_ensemble':dict(ensemble=True),'Coordinate_ensemble':dict(ensemble=True,coord=True),'RF600':dict(trees=600),'Extra600':dict(kind='extra',features=.5,trees=600),'Extra_leaf2':dict(kind='extra',features=.5,leaf=2)}
    save('refinement_plan.json',dict(configurations=more,rationale='ExtraTrees and coordinate RF had positive support-only gains; test diversity/variance reduction, not large grids.'))
    for name,cfg in more.items():
        rr=[]
        try:
            for i,(s,ys,q,yq) in enumerate(folds()):
                now=time.time();p=CLASSES[probabilities(state,s,ys,160,cfg).argmax(1)][q];rr.append(score(name,160,i,yq,p,time.time()-now))
            rec.extend(rr);cfgs[name]=cfg;save(f'refinement/{name}.json',dict(records=rr,config=cfg));log(f'refinement {name}: support CV {np.mean([r["f1"] for r in rr]):.6f}')
        except Exception:save(f'refinement/{name}_FAILED.json',dict(traceback=traceback.format_exc()))
    save('refinement_complete.json',dict(records=rec,summary=summary(rec),configurations=cfgs))

def stability():
    obj=json.loads((H/'refinement_complete.json').read_text());summ=obj['summary']['160'];rank=sorted((n for n in summ if n!='ASTRA_AGF'),key=lambda n:summ[n]['mean'],reverse=True)
    # Top three mechanism refinements plus incumbent, fixed before repeated holdouts.
    names=['ASTRA_AGF']+rank[:3];cfgs={n:obj['configurations'][n] for n in names}
    save('stability_plan.json',dict(configurations=cfgs,trials=20,budgets=[5,25,50,100,160],seed=20260912,selection_rule='160-shot gain >.002; >=70% paired wins; no budget >.005 worse; support-only geographic safeguard',caveat='Repeated splits reuse the same 800 development labels, not independent samples. Balanced development validation differs from imbalanced full query F1.'))
    state=load_state();bank=np.load(H/'development_support.npz');ids=bank['indices'];y=bank['labels'];rng=np.random.default_rng(20260912);rec=[]
    for t in range(20):
        perms={c:rng.permutation(np.flatnonzero(y==c)) for c in CLASSES}
        for b in (5,25,50,100,160):
            ii=np.concatenate([perms[c][:b] for c in CLASSES]);vv=np.concatenate([perms[c][b:] for c in CLASSES]);s=ids[ii];ys=y[ii];q=ids[vv];yq=y[vv]
            for name,cfg in cfgs.items():
                now=time.time();p=CLASSES[probabilities(state,s,ys,b,cfg).argmax(1)][q];rec.append(score(name,b,t,yq,p,time.time()-now))
            save('stability_progress.json',dict(records=rec,summary=summary(rec)))
        log(f'support stability {t+1}/20')
    save('stability_complete.json',dict(records=rec,summary=summary(rec),configurations=cfgs))
    board=json.loads((H/'LEADERBOARD.json').read_text());known={r['candidate'] for r in board}
    for name,v in obj['summary']['160'].items():
        if name not in known:board.append(dict(candidate=name,development_support_cv=v,config=obj['configurations'][name],query_label_usage=False,information_regime='transductive',status='exploratory',reproducibility='pending'))
    for row in board:
        if row['candidate'] in names:row['stability_by_budget']={b:v[row['candidate']] for b,v in summary(rec).items()}
    save('LEADERBOARD.json',board)

if __name__=='__main__':
    with threadpool_limits(limits=1):globals()[sys.argv[1]]()
