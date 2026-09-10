"""Five clean label-free inference subprocesses, exact predictions vs saved trials."""
from pathlib import Path
import sys,subprocess,json,hashlib,time
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import run

def main():
 t0=time.perf_counter();st,d=run.setup();folder=HERE/'interface_test';folder.mkdir(exist_ok=True)
 checks=[]
 with np.load(HERE/'predictions.npz') as evidence:
  for b in run.BUD:
   tag=f'b{b}_t0';s=evidence[tag+'_support'];q=evidence[tag+'_query']
   support=folder/f'support_{b}.npz';query=folder/f'query_{b}.npz';output=folder/f'predictions_{b}.npy'
   assert not support.exists() and not query.exists()
   np.savez_compressed(support,X=d['X_amsterdam'][s],y=d['y_amsterdam'][s],feature_names=np.array(st['feature_names']))
   np.savez_compressed(query,X=d['X_amsterdam'][q],feature_names=np.array(st['feature_names']))
   command=[sys.executable,'-I','-B',str(HERE/'candidate_predict.py'),'--artifact',str(run.ROOT/'candidate/artifacts/exp010_stage1_madrid.pkl'),'--support',str(support),'--query',str(query),'--shots',str(b),'--output',str(output)]
   result=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=120)
   assert result.returncode==0,result.stderr
   pred=np.load(output);assert np.array_equal(pred,evidence[tag+'_regularized'])
   checks.append({'budget':b,'trial':0,'pass':True,'query_labels_present':False,'query_rows':len(q),'exact_prediction_equality':True,'prediction_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'command':command})
 # Negative check: a query label key must be rejected before prediction.
 bad=folder/'invalid_query_labels.npz';np.savez_compressed(bad,X=d['X_amsterdam'][q[:1]],feature_names=np.array(st['feature_names']),y=np.array([-999]))
 command[command.index('--query')+1]=str(bad);command[command.index('--output')+1]=str(folder/'must_not_exist.npy')
 rejected=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=120)
 assert rejected.returncode!=0 and not (folder/'must_not_exist.npy').exists()
 run.save(folder/'verification.json',{'pass':True,'checks':checks,'query_label_key_rejected':True,'runtime_seconds':time.perf_counter()-t0,'candidate_code_sha256':run.sha(HERE/'candidate_predict.py')})
 print('PASS: five clean feature-only query subprocesses reproduce full-query predictions exactly; query label key rejected.')
if __name__=='__main__':main()
