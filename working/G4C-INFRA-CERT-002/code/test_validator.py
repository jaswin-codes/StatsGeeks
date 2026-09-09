"""Offline synthetic validation tests. No RF loading, fitting, or worker processes."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import numpy as np
import e3_validator as v


def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf8')


def inventory(run):
    files = {p.relative_to(run).as_posix(): {'sha256': v.sha(p), 'bytes': p.stat().st_size}
             for p in run.rglob('*') if p.is_file() and p.name != 'artifact_hash_manifest.json'}
    write(run/'artifact_hash_manifest.json', {'run_id':run.name, 'files':files})


class SyntheticForest:
    """Test double; deliberately not a RandomForest and inaccessible from public CLI."""
    def predict(self, x):
        return np.argmax(x[:, :4],axis=1)+1


def transport(run,label,role,packet):
    cmd=['wsl','-d','Ubuntu','--exec','/usr/bin/python3','-B',v.linux_path(run/'coordinator/g4c_linux_call.py'),
         v.linux_path(run/f'evidence/{label}.input.json'),v.linux_path(run/'coordinator'/({'episode':'episode_worker.py','source':'source_worker.py','preflight':'preflight_worker.py'}[role])),
         role,v.linux_path(run/f'evidence/{label}.json')]
    if role=='episode':cmd += ['--rf',v.linux_path(run.parent/'baseline_artifacts/rf_final.pkl')]
    raw=(json.dumps(packet,indent=2,sort_keys=True,allow_nan=False)+'\n').replace('\n','\r\n').encode()
    return {'command':cmd,'returncode':0,'stderr':'','stdout':'synthetic fixture','input_sha256':hashlib.sha256(raw).hexdigest()}


def boundary(role,code,packet,out):
    return {'result':out,'boundary_evidence':{'role':role,'code_sha256':code,'packet_sha256':v.digest(packet),
        'teardown_pass':True,'returncode':0,'reason':None,'stderr':'','elapsed_seconds':1.0,'namespace':'pid:[synthetic]',
        'runtime_lock_sha256':'synthetic-runtime','lifecycle':{'pass_':True,'subreaper_enabled':True,'final_survivors':[]}}}


def fixture(run):
    generator=np.random.default_rng(812)
    X=generator.normal(size=(24,60));X[:,-1]=0;Y=np.repeat([1,2,3,4],6)
    x=generator.normal(size=(820,60));x[:,-1]=0;y=np.repeat([1,2,3,4],205)
    ids=np.column_stack([np.arange(len(y)),np.arange(len(y))+1000])
    means=np.stack([X[Y==c].mean(0) for c in [1,2,3,4]])
    state={'parameters':v.PARAMS,'source_means':means.tolist(),'active_indices':np.flatnonzero(X.var(0)>0).tolist()}
    sh=v.digest(state);forest=SyntheticForest();rf=forest.predict(x);rng=np.random.default_rng(42)
    episodes=[];rows=[];raw={b:[] for b in v.BUDGETS};code_hashes={}
    for name in ['episode_worker.py','source_worker.py','preflight_worker.py','g4c_linux_call.py']:
        p=run/'coordinator'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'SYNTHETIC NEVER EXECUTED '+name.encode());code_hashes[name]=v.sha(p)
    (run/'coordinator/e3_validator.py').write_bytes(Path(v.__file__).read_bytes())
    for i in range(60):
        b=v.BUDGETS[i//10];before=copy.deepcopy(rng.bit_generator.state)
        s=np.concatenate([rng.choice(np.flatnonzero(y==c),b,replace=False) for c in [1,2,3,4]])
        q=np.setdiff1d(np.arange(len(y)),s)
        e={'episode_id':f'G4A-B{b:03d}-T{i%10+1:02d}','budget':b,'trial':i%10+1,'rng_before':before,
           'rng_after':copy.deepcopy(rng.bit_generator.state),'support_row_indices':s.tolist(),'support_pixel_ids':ids[s].tolist()}
        for key,a in [('support_row_indices_sha256',s),('query_row_indices_sha256',q),('support_pixel_ids_sha256',ids[s]),
                      ('query_pixel_ids_sha256',ids[q]),('X_support_sha256',x[s]),('X_query_sha256',x[q])]:e[key]=v.array_hash(a)
        episodes.append(e)
        centers=np.stack([x[s][y[s]==c].mean(0) for c in [1,2,3,4]])
        delta=(centers-means).mean(0);delta[58:]=0
        preds={'candidate':forest.predict(x[q]-delta),'raw_prototype':np.argmin(((x[q,None,:]-centers[None,:,:])**2).sum(2),axis=1)+1,
               'rf_reproduced':forest.predict(x[q])}
        packet={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),
                'query_ids':ids[q].tolist(),'source_state':state,'parameters':{'episode_id':e['episode_id'],'budget':b,'trial':i%10+1,'classes':[1,2,3,4],'candidate':'E3'}}
        out={'predictions':{k:a.tolist() for k,a in preds.items()},'source_state_sha256':sh,'fresh_state_probe':True,
             'label_access':{'source_state_only':True,'current_support_labels':len(s),'query_labels':0,'other_episode_labels':0},
             'query_fingerprint':v.digest(ids[q].tolist()),'adaptation_state':{'prototypes':centers.tolist(),'translation':delta.tolist()},
             'descriptor_audit':{'before':{'forbidden':[]},'after':{'forbidden':[]}},'peak_rss_kib':100,'warnings':[]}
        label=f'worker_{i+1:02d}';ep=run/f'evidence/{label}.json';write(ep,boundary('episode',code_hashes['episode_worker.py'],packet,out));write(run/f'evidence/{label}.transport.json',transport(run,label,'episode',packet))
        preds['frozen_rf']=rf[q];p=run/'predictions'/f"{e['episode_id']}.npz";p.parent.mkdir(exist_ok=True)
        np.savez_compressed(p,query_indices=q,query_ids=ids[q],**preds)
        metrics={k:v.score(y[q],a) for k,a in preds.items()};raw[b].append(metrics['raw_prototype']['macro_f1'])
        row={k:e[k] for k in ['episode_id','budget','trial','support_row_indices_sha256','query_row_indices_sha256','query_pixel_ids_sha256']}
        row.update(prediction_artifact=f'working/{run.name}/predictions/{p.name}',prediction_sha256=v.sha(p),worker_evidence=f'evidence/{label}.json',worker_output_sha256=v.sha(ep),
                   worker_seconds=1.0,peak_rss_kib=100,warnings=[],worker_teardown=True,metrics=metrics,
                   confusion_sha256={k:v.digest(m['confusion']) for k,m in metrics.items()},
                   paired_deltas={'candidate_minus_raw':metrics['candidate']['macro_f1']-metrics['raw_prototype']['macro_f1'],
                                  'candidate_minus_rf':metrics['candidate']['macro_f1']-metrics['frozen_rf']['macro_f1']})
        rows.append(row)
    manifest={'gate4a':'PASS','episodes':episodes};mp=run/'checkpoint/episode_manifest.json';write(mp,manifest);mh=v.sha(mp)
    prep=run/'checkpoint/infrastructure_preparation.json';write(prep,{'authorization':{'run_id':run.name,'candidate':'E3','scope':'execution'},'code_hashes':code_hashes})
    write(run/'checkpoint/validation_binding.json',{'run_id':run.name,'candidate':'E3','manifest_sha256':mh,'rf_sha256':'synthetic-rf',
          'preparation_sha256':v.sha(prep),'validator_sha256':v.sha(run/'coordinator/e3_validator.py')})
    write(run/'checkpoint/execution_authorization.json',{'run_id':run.name,'candidate':'E3 only','parameters':v.PARAMS,'E4_E5':False,'notebook4_rerun':False,'manifest_hash':mh,'rf_hash':'synthetic-rf'})
    write(run/'candidate_state/source_state.json',{'source_state':state,'source_state_sha256':sh})
    s=np.asarray(episodes[0]['support_row_indices']);q=np.setdiff1d(np.arange(len(y)),s)
    probe={'X_support':x[s].tolist(),'y_support':y[s].tolist(),'support_ids':ids[s].tolist(),'X_query':x[q].tolist(),'query_ids':ids[q].tolist(),'parameters':{'mode':'preflight'}}
    for label in ['preflight_1','preflight_2','post_candidate_probe']:
        write(run/f'evidence/{label}.json',boundary('preflight',code_hashes['preflight_worker.py'],probe,{'status':'PASS','model_computation':False}))
        write(run/f'evidence/{label}.transport.json',transport(run,label,'preflight',probe))
    sp={'X_source':X.tolist(),'y_source':Y.tolist(),'parameters':v.PARAMS}
    write(run/'evidence/source_worker.json',boundary('source',code_hashes['source_worker.py'],sp,{'source_state':state,'source_state_sha256':sh,'target_rows_received':0,'fit_scope':'Madrid only'}))
    write(run/'evidence/source_worker.transport.json',transport(run,'source_worker','source',sp))
    summary={}
    for b in v.BUDGETS:
        group=[r for r in rows if r['budget']==b];summary[str(b)]={}
        for name in v.METHODS:
            vals=np.array([r['metrics'][name]['macro_f1'] for r in group]);summary[str(b)][name]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'values':vals.tolist(),'per_class_mean':np.mean([r['metrics'][name]['per_class_f1'] for r in group],0).tolist()}
        for name in ['candidate_minus_raw','candidate_minus_rf']:
            vals=np.array([r['paired_deltas'][name] for r in group]);summary[str(b)][name]={'mean':float(vals.mean()),'std_ddof0':float(vals.std()),'values':vals.tolist(),'positive_trials':int((vals>0).sum())}
    p=summary['25'];rr=np.array(p['candidate']['per_class_mean'])-p['raw_prototype']['per_class_mean'];fr=np.array(p['candidate']['per_class_mean'])-p['frozen_rf']['per_class_mean']
    criteria={'mean_gain_over_raw_ge_0.0100':p['candidate_minus_raw']['mean']>=.01,'positive_raw_gain_ge_8_of_10':p['candidate_minus_raw']['positive_trials']>=8,
              'no_mean_per_class_raw_regression_worse_than_0.0200':bool(np.all(rr>=-.02)),'mean_gain_over_same_query_rf_ge_0.0100':p['candidate_minus_rf']['mean']>=.01,
              'no_mean_per_class_rf_regression_worse_than_0.0200':bool(np.all(fr>=-.02))}
    verdict='PROMISING' if all(criteria.values()) else ('FALSIFIED' if p['candidate_minus_rf']['mean']<=0 or np.any(fr<-.02) or p['candidate_minus_raw']['mean']<=0 or np.any(rr<-.02) else 'INCONCLUSIVE')
    result={'run_id':run.name,'parameters':v.PARAMS,'execution_status':'COMPLETED_PENDING_INDEPENDENT_VERIFICATION','episodes_completed':60,
            'all_predictions_finalized_before_scoring':True,'E4_E5_run':False,'notebook4_rerun':False,'source_state_sha256':sh,
            'summary':summary,'success_criteria':criteria,'scientific_verdict':verdict,'primary_per_class_delta_candidate_minus_raw':rr.tolist(),
            'primary_per_class_delta_candidate_minus_rf':fr.tolist(),'peak_worker_rss_kib':100,'warnings':[]}
    write(run/'results/per_episode_results.json',rows);write(run/'results/execution_summary.json',result)
    (run/'EXECUTION_REPORT.md').write_text(v.report_text(result),encoding='utf8')
    inventory(run)
    return {'synthetic':True,'X':X,'Y':Y,'x':x,'y':y,'ids':ids,'forest':forest,'rf_predictions':rf,'historical_raw':raw,
            'manifest_hash':mh,'rf_hash':'synthetic-rf','runtime_hash':'synthetic-runtime','worker_hashes':{n:code_hashes[n] for n in ['episode_worker.py','source_worker.py','preflight_worker.py']}}


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name).resolve();cls.target=cls.root/'working/G4C-E3-900'
        cls.context=fixture(cls.target)
        cls.backup=cls.root/'fixture_backup';shutil.copytree(cls.target,cls.backup)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        shutil.rmtree(self.target);shutil.copytree(self.backup,self.target)
    def rows(self):return v.load(self.target/'results/per_episode_results.json')
    def change_rows(self,rows):write(self.target/'results/per_episode_results.json',rows);inventory(self.target)
    def rejects(self):
        with self.assertRaises((v.ValidationError,FileNotFoundError,ValueError,KeyError)):
            v._validate(self.target,self.context)
    def test_A_valid_complete_layout(self):
        result=v._validate(self.target,self.context);self.assertEqual(result['status'],'SYNTHETIC_TEST_PASS');self.assertEqual(result['exact_prediction_records'],60)
    def test_B_wrong_run_id(self):
        p=self.target/'checkpoint/execution_authorization.json';a=v.load(p);a['run_id']='G4C-E3-901';write(p,a);inventory(self.target);self.rejects()
    def test_C_historical_path_substitution(self):
        rows=self.rows();rows[0]['prediction_artifact']='working/G4C-E3-001/predictions/'+Path(rows[0]['prediction_artifact']).name;self.change_rows(rows);self.rejects()
    def test_D_missing_prediction(self):
        next((self.target/'predictions').glob('*.npz')).unlink();self.rejects()
    def test_E_modified_prediction_even_rehashed(self):
        rows=self.rows();p=v.local_path(self.target,rows[0]['prediction_artifact'])
        with np.load(p) as a:arrays={k:a[k].copy() for k in a.files}
        arrays['candidate'][0]=arrays['candidate'][0]%4+1;np.savez_compressed(p,**arrays);rows[0]['prediction_sha256']=v.sha(p);self.change_rows(rows);self.rejects()
    def test_F_wrong_manifest(self):
        p=self.target/'checkpoint/episode_manifest.json';m=v.load(p);m['episodes'].reverse();write(p,m);inventory(self.target);self.rejects()
    def test_G_duplicate_episode(self):
        rows=self.rows();rows[-1]=copy.deepcopy(rows[0]);self.change_rows(rows);self.rejects()
    def test_H_wrong_episode_identity(self):
        rows=self.rows();rows[0]['episode_id']='G4A-B005-T99';self.change_rows(rows);self.rejects()
    def test_I_missing_evidence(self):
        (self.target/'evidence/worker_01.json').unlink();self.rejects()
    def test_J_cross_run_evidence_reference(self):
        rows=self.rows();rows[0]['worker_evidence']='working/G4C-E3-901/evidence/worker_01.json';self.change_rows(rows);self.rejects()
    def test_K_corrupt_report_even_rehashed(self):
        p=self.target/'EXECUTION_REPORT.md';p.write_text(p.read_text(encoding='utf8')+'false success\n',encoding='utf8');inventory(self.target);self.rejects()
    def test_L_inspect_real_closed_history_without_PASS(self):
        root=Path(__file__).resolve().parents[3];result=v.inspect_closed_run(root/'working/G4C-E3-001')
        self.assertEqual(result['status'],'HISTORICAL_EVIDENCE_ONLY')
        with self.assertRaises(v.ValidationError):v.validate_e3_run(root/'working/G4C-E3-001')
    def test_M_fake_fixture_cannot_receive_production_PASS(self):
        with self.assertRaises((v.ValidationError,FileNotFoundError)):v.validate_e3_run(self.target)
    def test_N_traversal(self):
        rows=self.rows();rows[0]['prediction_artifact']='../G4C-E3-901/predictions/x.npz';self.change_rows(rows);self.rejects()
    def test_O_wrong_metric_even_rehashed(self):
        rows=self.rows();rows[0]['metrics']['candidate']['macro_f1']+=.01;self.change_rows(rows);self.rejects()
    def test_P_failed_teardown_even_rehashed(self):
        rows=self.rows();p=self.target/'evidence/worker_01.json';a=v.load(p);a['boundary_evidence']['lifecycle']['final_survivors']=[123];write(p,a);rows[0]['worker_output_sha256']=v.sha(p);self.change_rows(rows);self.rejects()
    def test_Q_wrong_summary_verdict_even_rehashed(self):
        p=self.target/'results/execution_summary.json';a=v.load(p);a['scientific_verdict']='invented';write(p,a);inventory(self.target);self.rejects()
    def test_R_closed_run_binding_refused(self):
        from bind_e3_validation import bind_e3_validation
        with self.assertRaises(v.ValidationError):bind_e3_validation(self.target)
    def test_S_known_metric_case(self):
        a=v.score(np.array([1,2,3,4]),np.array([1,2,4,3]));self.assertEqual(a['macro_f1'],.5);self.assertEqual(a['per_class_f1'],[1.,1.,0.,0.])


if __name__=='__main__':unittest.main(verbosity=2)
