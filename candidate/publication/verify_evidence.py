"""Fixed-reference verification and observational profiling; never searches or tunes."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'): os.environ[k]='1'
from pathlib import Path
import sys,json,pickle,time,hashlib,threading
import numpy as np
import psutil
from threadpoolctl import threadpool_limits
R=Path(__file__).resolve().parents[2]
H=R/'candidate/best_model'
O=R/'candidate/reproducibility/verification'
def sha(p): return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def main():
    O.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((H/'INFERENCE_MANIFEST.json').read_text())
    for n,v in manifest['files'].items(): assert sha(H/n)==v,n
    sys.path.insert(0,str(H))
    import agf_model as m
    with open(H/'pool_state.pkl','rb') as f: state=pickle.load(f)
    cfg=json.loads((H/'SELECTION_LOCK.json').read_text())['config']
    proc=psutil.Process(); rows=[]; importance=[]; process_peak=0
    for b in m.BUDGETS:
        with np.load(H/f'verification_inputs/b{b}.npz') as ref:
            for name,config in [('Coordinate_RF',cfg),('ASTRA_AGF',{})]:
                captured={}; clocks={}; durations={'training_seconds':0.,'prediction_seconds':0.}
                def profile(frame,event,arg):
                    code=frame.f_code; fn=code.co_name
                    if '_forest.py' in code.co_filename and fn in ('fit','predict_proba'):
                        if event=='call': clocks[id(frame)]=time.perf_counter()
                        elif event=='return' and id(frame) in clocks:
                            durations['training_seconds' if fn=='fit' else 'prediction_seconds']+=time.perf_counter()-clocks.pop(id(frame))
                    if event=='return' and code is m.stable_probability.__code__:
                        captured['local_probability']=arg.copy()
                    if event=='return' and code is m.probabilities.__code__:
                        captured['importance']=frame.f_locals['model'].feature_importances_.copy()
                stop=threading.Event(); rss=[proc.memory_info().rss]
                def sample():
                    while not stop.wait(.005): rss.append(proc.memory_info().rss)
                th=threading.Thread(target=sample,daemon=True); th.start()
                wall=time.perf_counter(); cpu=time.process_time(); sys.setprofile(profile)
                try:
                    with threadpool_limits(limits=1): p=m.probabilities(state,ref['support'],ref['support_labels'],b,config)
                finally: sys.setprofile(None); stop.set(); th.join()
                elapsed=time.perf_counter()-wall; cpu=time.process_time()-cpu; rss.append(proc.memory_info().rss)
                pred=m.CLASSES[p.argmax(1)]; q=ref['query']
                if name=='Coordinate_RF': expected=ref['expected']
                else:
                    with np.load(R/f'candidate/autonomous_runs/20260909_1727/final/b{b}_t0.npz') as original: expected=original[name]
                np.testing.assert_array_equal(pred[q],expected)
                alpha=20/(20+len(ref['support']))
                np.savez_compressed(O/f'{name}_b{b}.npz',query=q,probability=p[q],prediction=pred[q],local_probability=captured['local_probability'][q],blended_probability=((1-alpha)*captured['local_probability']+alpha*state['prior'])[q])
                rows.append(dict(method=name,budget=b,trial=0,wall_seconds=elapsed,cpu_seconds=cpu,**durations,rss_before_bytes=rss[0],rss_after_bytes=rss[-1],sampled_peak_rss_bytes=max(rss),episodes_per_second=1/elapsed,pool_predictions_per_second=len(p)/elapsed,query_predictions_per_second=len(q)/elapsed,exact_predictions=True,scope='fixed-reference replay; source prior cached; profiler overhead included; RF-only fit/predict times'))
                if name=='Coordinate_RF':
                    for i,v in enumerate(captured['importance']): importance.append(dict(budget=b,trial=0,feature=f'whitened_component_{i+1:02}' if i<60 else ['coordinate_x','coordinate_y'][i-60],importance=float(v),kind='impurity; transformed axes, not raw spectral features'))
    (O/'runtime.json').write_text(json.dumps(rows,indent=2))
    (O/'feature_importance.json').write_text(json.dumps(importance,indent=2))
    (O/'validation.json').write_text(json.dumps(dict(exact_arrays=10,passed=True,query_truth_loaded=False,model_modified=False,optimization=False),indent=2))
    print('Verified 10 fixed-reference arrays. No query truth loaded by inference.')
if __name__=='__main__':main()
