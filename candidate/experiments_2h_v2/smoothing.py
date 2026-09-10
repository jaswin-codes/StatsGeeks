"""Final weighting ablation on immutable source-context probability fields.
No fitting or target truth enters smoothing. All configurations are specified in SMOOTHING_PLAN.md.
"""
from pathlib import Path
import os
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
import sys,json
import numpy as np
from scipy.spatial import cKDTree
from sklearn.metrics import f1_score,confusion_matrix
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R)]
from models import C
from candidate.experiments_2h.run import setup,save,sha

def main():
 mode=sys.argv[1];repeat='--repeat'in sys.argv;tag='smoothing_'+mode+('_repeat'if repeat else '');out=H/(tag+'.json');assert not out.exists();st,d=setup();y=d['y_amsterdam'];dist,ids=cKDTree(d['pixel_ids_amsterdam']).query(d['pixel_ids_amsterdam'],k=9);weights=np.exp(-dist**2/2);weights/=weights.sum(1,keepdims=True)
 priors=dict(np.load(H/'source_context_priors.npz'));priors['cc1']=np.load(H/'conditional_priors.npz')['cc1'];priors['none']=None
 suffix='_repeat'if repeat else '';arrays=np.load(H/('source_context_'+mode+suffix+'.npz'));fields=np.load(H/('source_context_'+mode+suffix+'_fields.npz'));control=json.loads((H/f'stage2_{mode}.json').read_text());rec=[];payload={}
 for t in range(10):
  for b in [5,25,50,100,200]:
   tag0=f'b{b}_t{t}';s=arrays[tag0+'_s'];q=arrays[tag0+'_q'];base=next(r['f1']for r in control['records']if r['budget']==b and r['trial']==t and r['method']=='EXP010');predictions={}
   for basis in ['raw','pool']:
    P=fields[tag0+'_'+basis];alpha=20/(20+len(s))
    for priorname,prior in priors.items():
     field=P if prior is None else (1-alpha)*P+alpha*prior;mean=field[ids].mean(1);kernels={'uniform':mean,'lazy':.5*field+.5*mean,'gaussian':np.sum(field[ids]*weights[:,:,None],axis=1)}
     for kernel,prob in kernels.items():predictions['_'.join([basis,priorname,kernel])]=C[prob[q].argmax(1)]
   for name,p in predictions.items():
    pc=f1_score(y[q],p,labels=C,average=None,zero_division=0);rec.append({'budget':b,'trial':t,'method':name,'f1':float(pc.mean()),'delta':float(pc.mean()-base),'class_f1':pc.tolist(),'cm':confusion_matrix(y[q],p,labels=C).tolist()});payload[tag0+'_'+name]=p
   payload[tag0+'_s']=s;payload[tag0+'_q']=q
 summary={}
 for b in [5,25,50,100,200]:
  summary[b]={}
  for name in predictions:
   rr=[r for r in rec if r['budget']==b and r['method']==name];v=np.array([r['f1']for r in rr]);dv=np.array([r['delta']for r in rr]);summary[b][name]={'mean':float(v.mean()),'sd':float(v.std()),'delta':float(dv.mean()),'wins':int((dv>1e-12).sum()),'class_f1_mean':np.mean([r['class_f1']for r in rr],axis=0).tolist()}
 save(out,{'records':rec,'summary':summary,'mode':mode,'selection':'final three-kernel controlled ablation on saved probability fields, audit exploration','script_sha':sha(Path(__file__))});np.savez_compressed(H/(tag+'.npz'),**payload)
 if repeat:
  old=json.loads((H/('smoothing_'+mode+'.json')).read_text());assert old['records']==rec
  with np.load(H/('smoothing_'+mode+'.npz'))as data:
   for k,v in payload.items():np.testing.assert_array_equal(v,data[k])
  save(H/('smoothing_'+mode+'_reproducibility.json'),{'pass':True,'arrays_exact':len(payload),'upstream':'source_context_audit_repeat_fields.npz from source+local clean refits'})
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
