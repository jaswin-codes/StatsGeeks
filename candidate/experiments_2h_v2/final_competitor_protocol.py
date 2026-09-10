"""Locked ASTRA candidate under the competitor's exact20-trial RNG convention."""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json,pickle
import numpy as np
from sklearn.metrics import f1_score,confusion_matrix
from threadpoolctl import threadpool_limits
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from candidate_predict import adapt_and_predict,BUDGETS
from candidate.experiments_2h.run import setup,save,sha
from candidate.exp010_predict import adapt_and_predict as baseline

def main():
 repeat='--repeat'in sys.argv;tag='final_competitor_protocol'+('_repeat'if repeat else'');out=H/(tag+'.json');assert not out.exists();st,d=setup();cfg=json.loads((H/'FINAL_SELECTION.json').read_text())
 for f,h in cfg['files_sha256'].items():assert sha(H/f)==h
 with(H/'astra_pool_state.pkl').open('rb')as f:state=pickle.load(f)
 competitor=json.loads((R/'candidate/competitor_forensics/reproduction_both.json').read_text());old_protocol=json.loads((H/'competitor_protocol.json').read_text());y=d['y_amsterdam'];records=[];payload={}
 for b in BUDGETS:
  rng=np.random.default_rng(42)
  for t in range(20):
   s=np.concatenate([rng.choice(np.flatnonzero(y==c),b,False)for c in [1,2,3,4]]);q=np.setdiff1d(np.arange(len(y)),s);ys=y[s].copy();p=adapt_and_predict(state,s,ys,b)[q];basep=baseline(st,d['X_amsterdam'][s],ys,d['X_amsterdam'][q],b,42);pc=f1_score(y[q],p,labels=[1,2,3,4],average=None,zero_division=0);v=float(pc.mean());base=float(f1_score(y[q],basep,average='macro'));ref=next(r['f1']for r in old_protocol['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010');assert abs(base-ref)<1e-12;comp=competitor['budgets'][str(b)]['scores'][t]
   records.append({'budget':b,'trial':t,'f1':v,'EXP010':base,'competitor_fallback108':comp,'delta_vs_EXP010':v-base,'delta_vs_competitor':v-comp,'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=[1,2,3,4]).tolist()});payload[f'{b}_{t}_s']=s;payload[f'{b}_{t}_q']=q;payload[f'{b}_{t}_pred']=p
  print('budget',b,flush=True)
 summary={}
 for b in BUDGETS:
  rr=[r for r in records if r['budget']==b];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta_vs_competitor']for r in rr]);summary[b]={'mean':float(v.mean()),'sd':float(v.std()),'delta_vs_EXP010':float(np.mean([r['delta_vs_EXP010']for r in rr])),'delta_vs_competitor':float(dv.mean()),'paired_competitor_wins':int((dv>1e-12).sum()),'paired_competitor_losses':int((dv< -1e-12).sum()),'paired_competitor_ties':int((np.abs(dv)<=1e-12).sum())}
 save(out,{'records':records,'summary':summary,'seed':42,'n_trials':20,'rng':'reset per budget; stratified choice without replacement, support complement query','selection':'locked final method, no tuning','competitor_reference':'original-code fallback108; not the missing tuned config','baseline_existing_protocol_exact':True});np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((H/'final_competitor_protocol.json').read_text());assert old['records']==records
  with np.load(H/'final_competitor_protocol.npz')as a:
   for k,v in payload.items():np.testing.assert_array_equal(v,a[k])
  save(H/'final_competitor_protocol_reproducibility.json',{'pass':True,'arrays_exact':len(payload)})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
