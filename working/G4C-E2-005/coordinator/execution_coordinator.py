"""Authorized fixed E2 execution for G4C-E2-003; privileged evaluator/controller.
Candidate workers never receive manifest or query labels. All 60 predictions finalize
and workers reap before this process attaches evaluator labels for scoring.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k]='1'
import datetime,hashlib,importlib.util,json,pathlib,pickle,platform,subprocess,sys,tempfile,time,traceback,types
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[3];RUN=ROOT/'working/G4C-E2-005'
MANIFEST=ROOT/'working/gate4_episode_manifest.json';MH='9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32'
RFH='5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870';CLASSES=np.array([1,2,3,4])
PARAMS={'candidate':'E2','epsilon':1e-6,'clip':[.25,4.0],'identity_mixture':.5}
WORKERS={'source':'source_worker.py','episode':'episode_worker.py','preflight':'preflight_worker.py'}
STATIC=[]

def sha(p):
 with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def save(path,obj):
 path=pathlib.Path(path)
 with path.open('x',encoding='utf8') as f:json.dump(obj,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def linux(p):
 s=pathlib.Path(p).resolve().as_posix();return '/mnt/'+s[0].lower()+s[2:]
def attrs_readonly(path):subprocess.run(['attrib','+R',str(pathlib.Path(path).resolve())],check=True,capture_output=True)
def metric(y,p):
 cm=np.bincount(4*(y-1)+(p-1),minlength=16).reshape(4,4);tp=np.diag(cm);den=cm.sum(0)+cm.sum(1)
 f=np.divide(2*tp,den,out=np.zeros(4),where=den>0);precision=np.divide(tp,cm.sum(0),out=np.zeros(4),where=cm.sum(0)>0);recall=np.divide(tp,cm.sum(1),out=np.zeros(4),where=cm.sum(1)>0)
 return {'macro_f1':float(f.mean()),'per_class_f1':f.tolist(),'precision':precision.tolist(),'recall':recall.tolist(),'accuracy':float(tp.sum()/cm.sum()),'confusion':cm.tolist()}
def install_pickle_dependency():
 path=ROOT/'working/minimal_standard_scaler.py';expected='c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111';assert sha(path)==expected
 assert 'working' not in sys.modules and 'working.minimal_standard_scaler' not in sys.modules
 package=types.ModuleType('working');package.__package__='working';package.__path__=[];package.__file__=None
 spec=importlib.util.spec_from_file_location('working.minimal_standard_scaler',path);assert spec and spec.loader
 module=importlib.util.module_from_spec(spec);sys.modules['working']=package;sys.modules['working.minimal_standard_scaler']=module;setattr(package,'minimal_standard_scaler',module);before=list(sys.path);spec.loader.exec_module(module);assert list(sys.path)==before and module.StandardScaler.__module__=='working.minimal_standard_scaler'
def original_clean():
 return not subprocess.check_output(['git','status','--short','--','original/'],cwd=ROOT) and not subprocess.check_output(['git','diff','--','original/'],cwd=ROOT)
def preexisting_integrity():
 cp=json.loads((ROOT/'working/G4C-PROVENANCE-CHECKPOINT-002/file_fingerprints.json').read_text())
 bad=[];metadata=[]
 for rel,v in cp.items():
  p=ROOT/rel;s=p.stat();cur={'sha256':sha(p),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'file_id':s.st_ino,'attributes':s.st_file_attributes,'signature_hex':p.read_bytes()[:16].hex(),'regular':p.is_file(),'links':s.st_nlink}
  if cur!=v:
   if rel=='working/Open Notebook.onetoc2' and all(cur[k]==v[k] for k in ('file_id','attributes','signature_hex','regular','links')) and cur['signature_hex']=='a12fff43d9ef764c9ee210ea5722765f':metadata.append({'before':v,'after':cur})
   else:bad.append(rel)
 if bad:raise RuntimeError('Pre-existing integrity failure '+repr(bad))
 entry=json.loads((ROOT/'working/G4B-E1-001/entry.json').read_text());assert len(entry['protected_hashes'])==33
 assert all(sha(ROOT/p)==h for p,h in entry['protected_hashes'].items());assert sha(MANIFEST)==MH;assert sha(ROOT/'working/baseline_artifacts/rf_final.pkl')==RFH;assert original_clean()
 for path,anchor in [(ROOT/'working/G4C-E2-001/artifact_hash_manifest.json','46cdbabcd98754f9b879250090359d29a8a64861b32887ae8e7b24b423007436'),(ROOT/'working/G4C-E2-002/checkpoint/artifact_hash_manifest.json','72d5a082443b5f5e6e4eb7879d9e17c860163079b62f0af2ebd2eee959b9e302'),(ROOT/'working/G4C-E2-003/artifact_hash_manifest.json','bb88bb5093e33da774023d8e31b280e4e67ea399d6556d03c3d642fd1f3e2d7f'),(ROOT/'working/G4C-INFRA-PICKLE-001/artifact_hash_manifest.json','0c2ae198299c454809947ddb4329c09a4e63708c9ffd1dea7a6fab8059b8e22f'),(ROOT/'working/G4C-E2-004/artifact_hash_manifest.json','df81100c96e51704012bbae90cb846357e163c69937803f13fbb47cf14e30859'),(ROOT/'working/G4C-INFRA-FD-001/artifact_hash_manifest.json','32b6cd7f916e967586f4f7a67c3c5c9a593775afcce207a7dfbb1e152863d27a')]:
  assert sha(path)==anchor;inv=json.loads(path.read_text());assert all(sha(ROOT/p)==v['sha256'] for p,v in inv['files'].items())
 return metadata
def static_integrity():
 for item in STATIC:
  p=ROOT/item['path'];assert p.is_file() and sha(p)==item['sha256'] and p.stat().st_size==item['bytes'],item['path']
 preexisting_integrity()
def call(packet,role,label):
 static_integrity();temp=RUN/'evidence'/f'{label}.input.json';save(temp,packet);out=RUN/'evidence'/f'{label}.json';transport=RUN/'evidence'/f'{label}.transport.json'
 cmd=['wsl','-d','Ubuntu','--exec','/usr/bin/python3','-B',linux(RUN/'coordinator/g4c_linux_call.py'),linux(temp),linux(RUN/'coordinator'/WORKERS[role]),role,linux(out)]
 proc=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
 save(transport,{'command':cmd,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'input_sha256':sha(temp)})
 if proc.returncode:raise RuntimeError(label+' transport failed '+proc.stderr)
 z=json.loads(out.read_text());ev=z['boundary_evidence'];assert ev['packet_sha256']==hashlib.sha256(canonical(packet)).hexdigest();assert ev['teardown_pass'] and ev['lifecycle']['pass_'] and not ev['lifecycle']['final_survivors'] and not ev['stderr'] and ev['returncode']==0 and ev['reason'] is None
 temp.unlink();return z

def main():
 global STATIC
 assert not (RUN/'results/execution_summary.json').exists() and not (RUN/'candidate_state/source_state.json').exists()
 started=time.perf_counter();metadata_start=preexisting_integrity()
 authorization={'run_id':'G4C-E2-005','authorization':'Explicit Team Lead E2-only execution authorization in current user message','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'E2 only','E3_E5':False,'parameters':PARAMS,'manifest_hash':MH,'rf_hash':RFH,'preparation_preflight_G4C_E2_003':sha(ROOT/'working/G4C-E2-003/checkpoint/preflight.json'),'metadata_events_at_start':metadata_start,'notebook4_rerun':False}
 save(RUN/'checkpoint/execution_authorization.json',authorization)
 # Allow external OneNote directory metadata to observe already-declared directories/files,
 # then freeze every run-local file (no run-local metadata exception).
 time.sleep(5)
 fixed=[]
 for p in sorted(RUN.rglob('*')):
  if p.is_file() and not any(part in ('evidence','predictions','candidate_state','results') for part in p.relative_to(RUN).parts):fixed.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
 STATIC=fixed
 # Privileged evaluator loads accepted arrays; no candidate packet contains target query labels or manifest.
 install_pickle_dependency()
 m=json.loads(MANIFEST.read_text());assert m['gate4a']=='PASS' and len(m['episodes'])==60
 with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:d=pickle.load(f)
 x,y,ids=d['X_amsterdam'],d['y_amsterdam'],d['pixel_ids_amsterdam'];xm,ym=d['X_madrid'],d['y_madrid']
 with np.load(ROOT/'working/baseline_artifacts/amsterdam_zero_shot.npz',allow_pickle=False) as a:
  rf=a['y_ams_pred_zero'].copy();assert np.array_equal(a['y_amsterdam'],y) and np.array_equal(a['pixel_ids_amsterdam'],ids)
 # Independent authoritative RNG replay before packet construction.
 rng=np.random.default_rng(42)
 for i,e in enumerate(m['episodes']):
  assert (e['budget'],e['trial'])==([5,10,25,50,100,200][i//10],i%10+1);assert rng.bit_generator.state==e['rng_before']
  s=np.concatenate([rng.choice(np.flatnonzero(y==c),e['budget'],replace=False) for c in CLASSES]);assert np.array_equal(s,e['support_row_indices']);assert rng.bit_generator.state==e['rng_after']
 e=m['episodes'][0];s=np.asarray(e['support_row_indices']);q=np.setdiff1d(np.arange(len(y)),s)
 probe={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'parameters':{'mode':'preflight'}}
 for n in (1,2):
  z=call(probe,'preflight',f'preflight_{n}');assert z['result']['status']=='PASS' and not z['result']['model_computation']
 source_packet={'X_source':xm.tolist(),'y_source':ym.tolist(),'parameters':PARAMS};z=call(source_packet,'source','source_worker');state=z['result']['source_state'];state_hash=z['result']['source_state_sha256'];assert z['result']['target_rows_received']==0 and z['result']['fit_scope']=='Madrid only'
 save(RUN/'candidate_state/source_state.json',{'source_state':state,'source_state_sha256':state_hash,'worker_peak_rss_kib':z['result']['peak_rss_kib']})
 rows=[]
 for index,e in enumerate(m['episodes']):
  static_integrity();s=np.asarray(e['support_row_indices'],dtype=np.int64);q=np.setdiff1d(np.arange(len(y)),s,assume_unique=True);assert np.array_equal(ids[s],np.asarray(e['support_pixel_ids']))
  packet={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'source_state':state,'parameters':{'episode_id':e['episode_id'],'budget':e['budget'],'trial':e['trial'],'classes':[1,2,3,4],'candidate':'E2'}}
  z=call(packet,'episode',f'worker_{index+1:02d}');r=z['result'];assert r['label_access']=={'source_state_only':True,'current_support_labels':len(s),'query_labels':0,'other_episode_labels':0};assert r['fresh_state_probe'] and r['source_state_sha256']==state_hash
  pred={k:np.asarray(v,dtype=np.int64) for k,v in r['predictions'].items()};pred['frozen_rf']=rf[q]
  with np.load(ROOT/'working/G4B-E1-001/predictions'/f"{e['episode_id']}.npz",allow_pickle=False) as old:
   assert np.array_equal(old['query_indices'],q) and np.array_equal(old['query_ids'],ids[q]);pred['unsupervised_covariance']=old['unsupervised_covariance'].copy();assert np.array_equal(old['raw_prototype'],pred['raw_prototype'])
  path=RUN/'predictions'/f"{e['episode_id']}.npz"
  with path.open('xb') as f:np.savez_compressed(f,query_indices=q,query_ids=ids[q],**pred)
  row={'episode_id':e['episode_id'],'budget':e['budget'],'trial':e['trial'],'support_row_indices_sha256':e['support_row_indices_sha256'],'query_row_indices_sha256':e['query_row_indices_sha256'],'query_pixel_ids_sha256':e['query_pixel_ids_sha256'],'prediction_artifact':path.relative_to(ROOT).as_posix(),'prediction_sha256':sha(path),'worker_evidence':f'evidence/worker_{index+1:02d}.json','worker_output_sha256':sha(RUN/'evidence'/f'worker_{index+1:02d}.json'),'worker_seconds':z['boundary_evidence']['elapsed_seconds'],'peak_rss_kib':r['peak_rss_kib'],'warnings':r['warnings'],'worker_teardown':True}
  rows.append(row);print(index+1,e['episode_id'],row['worker_seconds'],flush=True)
 # Fresh-state probe and teardown before privileged evaluator attaches query labels.
 z=call(probe,'preflight','post_candidate_probe');assert z['result']['status']=='PASS';prediction_phase_seconds=time.perf_counter()-started
 # Evaluator-only scoring starts after every candidate prediction and worker is finalized/reaped.
 for row in rows:
  with np.load(ROOT/row['prediction_artifact'],allow_pickle=False) as a:
   q=a['query_indices'];yt=y[q];row['metrics']={name:metric(yt,a[name]) for name in ('candidate','raw_prototype','all_ones_active','unsupervised_covariance','frozen_rf')}
   c=row['metrics']['candidate']['macro_f1'];row['paired_deltas']={'candidate_minus_raw':c-row['metrics']['raw_prototype']['macro_f1'],'candidate_minus_u0':c-row['metrics']['unsupervised_covariance']['macro_f1'],'candidate_minus_rf':c-row['metrics']['frozen_rf']['macro_f1']};row['confusion_sha256']={k:hashlib.sha256(canonical(v['confusion'])).hexdigest() for k,v in row['metrics'].items()}
 save(RUN/'results/per_episode_results.json',rows)
 summary={}
 for b in (5,10,25,50,100,200):
  group=[r for r in rows if r['budget']==b];summary[str(b)]={}
  for name in ('candidate','raw_prototype','all_ones_active','unsupervised_covariance','frozen_rf'):
   vals=np.array([r['metrics'][name]['macro_f1'] for r in group]);pcs=np.array([r['metrics'][name]['per_class_f1'] for r in group]);summary[str(b)][name]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'values':vals.tolist(),'per_class_mean':pcs.mean(0).tolist()}
  for name in ('candidate_minus_raw','candidate_minus_u0','candidate_minus_rf'):
   vals=np.array([r['paired_deltas'][name] for r in group]);summary[str(b)][name]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'positive_trials':int((vals>0).sum()),'values':vals.tolist()}
 p=summary['25'];reg=(np.asarray(p['candidate']['per_class_mean'])-p['raw_prototype']['per_class_mean']).tolist();criteria={'mean_gain_over_raw_ge_0.0100':p['candidate_minus_raw']['mean']>=.01,'positive_raw_gain_ge_8_of_10':p['candidate_minus_raw']['positive_trials']>=8,'no_mean_per_class_regression_worse_than_0.0200':bool(np.all(np.asarray(reg)>=-.02)),'positive_gain_over_same_query_rf':p['candidate_minus_rf']['mean']>0}
 verdict='PROMISING' if all(criteria.values()) else ('FALSIFIED' if p['candidate_minus_raw']['mean']<=0 or not criteria['no_mean_per_class_regression_worse_than_0.0200'] else 'INCONCLUSIVE')
 result={'run_id':'G4C-E2-005','execution_status':'COMPLETED_PENDING_INDEPENDENT_VERIFICATION','scientific_verdict':verdict,'episodes_completed':60,'parameters':PARAMS,'summary':summary,'success_criteria':criteria,'primary_per_class_delta_candidate_minus_raw':reg,'source_state_sha256':state_hash,'prediction_phase_seconds':prediction_phase_seconds,'total_primary_seconds':time.perf_counter()-started,'peak_worker_rss_kib':max(r['peak_rss_kib'] for r in rows),'warnings':[{'episode_id':r['episode_id'],'warnings':r['warnings']} for r in rows if r['warnings']],'metadata_events':preexisting_integrity(),'candidate_label_boundary':'Madrid source labels in source worker; current target support labels only per episode; query/full-target/other-episode labels never transported','all_predictions_finalized_before_scoring':True,'E3_E5_run':False,'notebook4_rerun':False}
 save(RUN/'results/execution_summary.json',result);static_integrity();print(json.dumps({'status':verdict,'criteria':criteria,'primary':p},indent=2),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException:
  p=RUN/'results/EXECUTION_STOP_REASON.md'
  if not p.exists():
   with p.open('x',encoding='utf8') as f:f.write('# E2 execution STOP — no retry\n\n```\n'+traceback.format_exc()+'\n```\n')
  raise
