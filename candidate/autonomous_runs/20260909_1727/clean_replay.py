"""Clean-process source refit and complete paired replay; no scoring or selection."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from sprint import *

def main():
    out=H/'clean_replay';out.mkdir(exist_ok=False)
    lock=json.loads((H/'SELECTION_LOCK.json').read_text());assert sha(H/'agf_model.py')==lock['model_sha256']
    st,d=setup();start=time.time()
    # y_amsterdam is retained only inside this benchmark episode-generator harness.
    # The pool fitting function receives source y, never target y.
    fresh=fit_pool(d['X_madrid'],d['y_madrid'],d['pixel_ids_madrid'],d['X_amsterdam'],d['pixel_ids_amsterdam'],d['scaler'].mean_,d['scaler'].scale_,d['feature_names'])
    old=load_state();checked_state=[]
    for key in ('raw','standard','coords','prior','cov','nn','dist','classes'):
        np.testing.assert_array_equal(fresh[key],old[key]);checked_state.append(key)
    assert fresh['feature_names']==old['feature_names']==d['feature_names']
    with (out/'rebuilt_pool_state.pkl').open('wb') as f:pickle.dump(fresh,f,protocol=5)
    log('Clean replay: independently rebuilt pool state exact')
    compact={k:representation(st,d,k) for k in (30,45)}
    y=d['y_amsterdam'];dev=np.load(H/'development_support.npz')['indices'];eligible=np.setdiff1d(np.arange(len(y)),dev);rng=np.random.default_rng(20260910)
    count=0;episodes=0
    for t in range(200):
        perms={c:rng.permutation(eligible[y[eligible]==c])[:200] for c in CLASSES}
        for b in BUDGETS:
            ref=np.load(H/f'final/b{b}_t{t}.npz');s=np.concatenate([perms[c][:b] for c in CLASSES]);q=np.setdiff1d(eligible,s);ys=y[s]
            np.testing.assert_array_equal(s,ref['support']);np.testing.assert_array_equal(q,ref['query']);np.testing.assert_array_equal(ys,ref['support_labels'])
            assert not np.intersect1d(s,q).size and not np.intersect1d(dev,q).size
            for name,cfg in [('ASTRA_AGF',{}),(lock['candidate'],lock['config'])]:
                p=CLASSES[probabilities(fresh,s,ys,b,cfg).argmax(1)][q];np.testing.assert_array_equal(p,ref[name]);count+=1
            p=frozen_predict(st,fresh['standard'][s],ys,fresh['standard'][q],b,20260910);np.testing.assert_array_equal(p,ref['EXP010']);count+=1
            z,delta=compact[SUPPORTED_SCHEDULE[b][0]];p=metric_predict(z[s],ys,z[q],delta,metric='regularized');np.testing.assert_array_equal(p,ref['EXPF']);count+=1;episodes+=1
        save('clean_replay/progress.json',dict(exact_prediction_arrays=count,episodes=episodes,completed_trials=t+1,seconds=time.time()-start))
        if (t+1)%10==0:log(f'Clean paired replay {t+1}/200')
    for rel,h in json.loads((H/'provenance.json').read_text())['protected'].items():assert sha(R/rel)==h,rel
    save('clean_replay/verification.json',dict(pass_=True,source_refitted_from_scratch=True,exact_state_arrays=checked_state,exact_prediction_arrays=count,episodes=episodes,trials_per_budget=200,seed_regenerated_exactly=20260910,support_query_disjoint=True,development_query_disjoint=True,query_labels_used_for_scoring_or_selection=False,frozen_files_unchanged=True,seconds=time.time()-start,model_sha256=sha(H/'agf_model.py'),rebuilt_pool_sha256=sha(out/'rebuilt_pool_state.pkl')))

if __name__=='__main__':
    with threadpool_limits(limits=1):main()
