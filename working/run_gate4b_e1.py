"""Privileged Windows evaluator for fixed G4B-E1-001; query labels score only after all workers exit."""
import datetime,hashlib,json,os,pathlib,pickle,platform,subprocess,sys,tempfile,time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];RUN=ROOT/'working/G4B-E1-001';MANIFEST=ROOT/'working/gate4_episode_manifest.json'
PY=r'C:/Users/jaswi/AppData/Local/Programs/Python/Python311/python.exe';CLASSES=np.array([1,2,3,4]);MANIFEST_HASH='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def linux(p):
 p=pathlib.Path(p).resolve().as_posix();return '/mnt/'+p[0].lower()+p[2:]
def call(packet,worker,role,out):
 with tempfile.NamedTemporaryFile('w',suffix='.json',prefix='g4b_packet_',delete=False,dir=RUN,encoding='utf8') as f:json.dump(packet,f,separators=(',',':'),allow_nan=False);tmp=pathlib.Path(f.name)
 try:
  cmd=['wsl','-d','Ubuntu','--exec','/usr/bin/python3','-B',linux(ROOT/'working/gate4b_linux_call.py'),linux(tmp),linux(ROOT/'working'/worker),role,linux(out)]
  return subprocess.check_output(cmd,text=True,timeout=300)
 finally:tmp.unlink()
def fmetrics(y,p):
 cm=np.bincount(4*(y-1)+(p-1),minlength=16).reshape(4,4);den=cm.sum(0)+cm.sum(1);f=np.divide(2*np.diag(cm),den,out=np.zeros(4),where=den!=0);return cm,f,float(f.mean())
def integrity():
 pins=json.load(open(ROOT/'working/gate4_dependency_repair_entry.json'))['protected_input_hashes']
 assert all(sha(ROOT/p)==h for p,h in pins.items());assert sha(MANIFEST)==MANIFEST_HASH;assert MANIFEST.stat().st_file_attributes&1
 assert not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT);assert not subprocess.check_output(['git','diff','--','original/'],cwd=ROOT);return pins
def main():
 pins=integrity();m=json.loads(MANIFEST.read_text());assert len(m['episodes'])==60 and m['gate4a']=='PASS'
 sys.path.insert(0,str(ROOT));
 with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:d=pickle.load(f)
 x,y,ids=d['X_amsterdam'],d['y_amsterdam'],d['pixel_ids_amsterdam'];xm,ym=d['X_madrid'],d['y_madrid']
 with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as a:
  rf=a['y_ams_pred_zero'];assert np.array_equal(a['y_amsterdam'],y) and np.array_equal(a['pixel_ids_amsterdam'],ids)
 # Preflight uses real first episode packet but does no modelling.
 e=m['episodes'][0];s=np.array(e['support_row_indices']);mask=np.ones(len(y),bool);mask[s]=False;q=np.flatnonzero(mask)
 pre={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'parameters':{'mode':'preflight'}}
 for i in range(2):call(pre,'gate4b_preflight_worker.py','preflight',RUN/'evidence'/f'preflight_{i+1}.json')
 # Independently ensure preflight output and lifecycle before first E1 operation.
 for p in sorted((RUN/'evidence').glob('preflight_*.json')):
  z=json.loads(p.read_text());assert z['result']['status']=='PASS' and not z['result']['model_computation'];assert z['boundary_evidence']['teardown_pass']
 preflight={'status':'PASS','runs':2,'manifest_not_mounted':True,'query_labels_not_transported':True,'model_computation':False,'protected_33':'PASS'}
 with (RUN/'preflight.json').open('x') as f:json.dump(preflight,f,indent=2)
 # Source state: first authorized E1 computation, Madrid only.
 source={'X_source':xm.tolist(),'y_source':ym.tolist(),'parameters':{'classes':[1,2,3,4],'shrinkage':0.1,'covariance_ddof':0}}
 call(source,'gate4b_source_worker.py','source',RUN/'source_worker_output.json');z=json.loads((RUN/'source_worker_output.json').read_text());state=z['result']['source_state'];state_hash=z['result']['source_state_sha256'];assert z['result']['target_rows_received']==0 and z['boundary_evidence']['teardown_pass']
 with (RUN/'source_state.json').open('x') as f:json.dump({'source_state':state,'source_state_sha256':state_hash},f,separators=(',',':'));f.write('\n')
 results=[];started=time.perf_counter()
 for index,e in enumerate(m['episodes']):
  s=np.array(e['support_row_indices'],dtype=np.int64);mask=np.ones(len(y),bool);mask[s]=False;q=np.flatnonzero(mask)
  assert sha(MANIFEST)==MANIFEST_HASH and np.array_equal(ids[s],np.array(e['support_pixel_ids']))
  packet={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'source_state':state,'parameters':{'episode_id':e['episode_id'],'budget':e['budget'],'trial':e['trial'],'classes':[1,2,3,4]}}
  out=RUN/'evidence'/f"worker_{index+1:02d}.json";call(packet,'gate4b_episode_worker.py','episode',out)
  ev=json.loads(out.read_text());assert ev['boundary_evidence']['teardown_pass'];r=ev['result'];assert r['label_access']=={'source_state_only':True,'current_support_labels':len(s),'query_labels':0,'other_episode_labels':0}
  pred={k:np.array(v,dtype=np.int64) for k,v in r['predictions'].items()};pred['frozen_rf']=rf[q].astype(np.int64)
  assert all(len(v)==len(q) for v in pred.values())
  npz=RUN/'predictions'/f"{e['episode_id']}.npz";np.savez_compressed(npz,query_indices=q,query_ids=ids[q],**pred)
  results.append({'episode_id':e['episode_id'],'budget':e['budget'],'trial':e['trial'],'support_row_indices_sha256':e['support_row_indices_sha256'],'query_row_indices_sha256':e['query_row_indices_sha256'],'query_pixel_ids_sha256':e['query_pixel_ids_sha256'],'worker_packet_sha256':ev['boundary_evidence']['packet_sha256'],'worker_output_sha256':sha(out),'prediction_artifact':npz.relative_to(ROOT).as_posix(),'prediction_sha256':sha(npz),'adaptation_state':r['adaptation_state'],'worker_seconds':ev['boundary_evidence']['elapsed_seconds'],'worker_teardown':True})
  print(index+1,e['episode_id'],ev['boundary_evidence']['elapsed_seconds'],flush=True)
 # Only now, after all 60 outputs finalized and workers reaped, attach evaluator labels.
 for row in results:
  with np.load(ROOT/row['prediction_artifact'],allow_pickle=False) as a:
   q=a['query_indices'];yt=y[q]
   row['scores']={};row['confusion_matrices']={};row['per_class_f1']={}
   for method in ['raw_prototype','unsupervised_covariance','e1','frozen_rf']:
    cm,pc,score=fmetrics(yt,a[method]);row['scores'][method]=score;row['confusion_matrices'][method]=cm.tolist();row['per_class_f1'][method]=pc.tolist()
   row['paired_deltas']={'e1_minus_raw':row['scores']['e1']-row['scores']['raw_prototype'],'e1_minus_u0':row['scores']['e1']-row['scores']['unsupervised_covariance'],'e1_minus_rf':row['scores']['e1']-row['scores']['frozen_rf']}
 with (RUN/'per_episode_results.json').open('x') as f:json.dump(results,f,indent=2);f.write('\n')
 summary={}
 for b in [5,10,25,50,100,200]:
  rows=[r for r in results if r['budget']==b];summary[str(b)]={}
  for method in ['raw_prototype','unsupervised_covariance','e1','frozen_rf']:
   vals=np.array([r['scores'][method] for r in rows]);pcs=np.array([r['per_class_f1'][method] for r in rows]);summary[str(b)][method]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'per_class_mean':pcs.mean(0).tolist()}
  for delta in ['e1_minus_raw','e1_minus_u0','e1_minus_rf']:
   vals=np.array([r['paired_deltas'][delta] for r in rows]);summary[str(b)][delta]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'positive_trials':int((vals>0).sum()),'values':vals.tolist()}
 primary=summary['25'];reg=np.array(primary['e1']['per_class_mean'])-np.array(primary['raw_prototype']['per_class_mean'])
 criteria={'mean_gain_raw_at_least_0.0100':primary['e1_minus_raw']['mean']>=.01,'positive_raw_gain_at_least_8_of_10':primary['e1_minus_raw']['positive_trials']>=8,'no_mean_per_class_regression_over_0.0200':bool(np.all(reg>=-.02)),'positive_gain_over_same_query_rf':primary['e1_minus_rf']['mean']>0,'beats_unsupervised_covariance':primary['e1_minus_u0']['mean']>0}
 verdict='PROMISING' if all(criteria.values()) else ('FALSIFIED' if primary['e1_minus_raw']['mean']<=0 or not criteria['no_mean_per_class_regression_over_0.0200'] else 'INCONCLUSIVE')
 report={'run_id':'G4B-E1-001','status':'PASS','verdict':verdict,'episodes_completed':60,'parameters':{'e1':'class-balanced population within-class covariance; shrinkage 0.1; inverse metric','u0':'population total source covariance; shrinkage 0.1; inverse metric','classes':[1,2,3,4],'tie_break':'ascending class via numpy argmin','primary_budget':25,'std_ddof':0},'summary':summary,'success_criteria':criteria,'primary_per_class_delta_e1_minus_raw':reg.tolist(),'source_state_sha256':state_hash,'manifest_sha256':MANIFEST_HASH,'wall_seconds_episode_workers':time.perf_counter()-started,'label_access':'Workers never receive query/full-target/other-episode labels; all 60 finalized before evaluator scoring','baseline_hashes':pins,'candidate_models':['E1 only'],'backup_candidates_run':False,'notebook4_rerun':False}
 with (RUN/'summary.json').open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 integrity();print(json.dumps({'verdict':verdict,'criteria':criteria,'primary':primary},indent=2))
if __name__=='__main__':main()
