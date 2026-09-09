"""Preserve validation failure, audit protected state, and report without recovery."""
import datetime,hashlib,json,pathlib,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[2];RUN=ROOT/'working/G4C-E3-002'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,o):
    with p.open('x',encoding='utf8') as f:json.dump(o,f,indent=2)
def command(args):
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    return {'command':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
linux_root='/mnt/'+ROOT.as_posix()[0].lower()+ROOT.as_posix()[2:]
win=['git','--no-optional-locks'];lin=['wsl','-d','Ubuntu','--exec','git','--no-optional-locks','-C',linux_root]
diag={'windows_status':command(win+['status','--short','--','original/']),'linux_status':command(lin+['status','--short','--','original/']),'windows_autocrlf':command(win+['config','--show-origin','--get','core.autocrlf']),'linux_autocrlf':command(lin+['config','--show-origin','--get','core.autocrlf']),'linux_numstat':command(lin+['diff','--numstat','--','original/']),'linux_ignore_eol_diff':command(lin+['diff','--ignore-space-at-eol','--exit-code','--','original/']),'linux_processes':command(['wsl','-d','Ubuntu','--exec','ps','-eo','pid,ppid,args'])}
save(RUN/'validation/git_discrepancy_diagnostics.json',diag)
start=time.perf_counter();before=json.loads((RUN/'preflight_integrity.json').read_text());checks=[]
for c in before['historical_checks']:
    p=ROOT/c['path'];v={'sha256':sha(p),'bytes':p.stat().st_size} if p.is_file() else None
    checks.append({'path':c['path'],'expected':c['observed'],'observed':v,'pass':v==c['observed']})
protected=[{'path':c['path'],'expected_sha256':c['expected_sha256'],'observed_sha256':sha(ROOT/c['path']),'pass':sha(ROOT/c['path'])==c['expected_sha256']} for c in before['protected_checks']]
audit={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(c['pass'] for c in checks+protected) else 'FAIL','historical_checks':checks,'protected_checks':protected,'seconds':time.perf_counter()-start}
save(RUN/'hashes/final_protected_audit.json',audit)
summary=json.loads((RUN/'results/execution_summary.json').read_text());rows=json.loads((RUN/'results/per_episode_results.json').read_text());auth=json.loads((RUN/'checkpoint/execution_authorization.json').read_text());failure=json.loads((RUN/'validation/INDEPENDENT_VALIDATION_FAILURE.json').read_text())
assert failure['status']=='FAIL' and len(rows)==summary['episodes_completed']==60
# Preserve the deterministic pre-validation report and its seal, without changing scientific outputs.
primary=RUN/'EXECUTION_REPORT.md';snapshot=RUN/'checkpoint/PRIMARY_EXECUTION_REPORT_PREVALIDATION.md'
with snapshot.open('xb') as f:f.write(primary.read_bytes())
original_report_hash=sha(primary);assert sha(snapshot)==original_report_hash
seal=RUN/'artifact_hash_manifest.json';assert json.loads(seal.read_text())['files']['EXECUTION_REPORT.md']['sha256']==original_report_hash
save(RUN/'validation/report_lifecycle.json',{'original_seal':'artifact_hash_manifest.json','original_seal_sha256':sha(seal),'prevalidation_report_original_path':'EXECUTION_REPORT.md','prevalidation_report_preserved_path':snapshot.relative_to(RUN).as_posix(),'prevalidation_report_sha256':original_report_hash,'final_report_path':'EXECUTION_REPORT.md','reason':'Replace only prevalidation human report with required final failure disclosure. Scientific outputs and original seal remain unchanged. Original seal describes prevalidation phase; final manifest will bind final reporting phase.','independent_validation_status':'FAIL','validation_retried':False})
worker=sum(r['worker_seconds'] for r in rows)
all_boundary=0.0
for label in ['preflight_1','preflight_2','source_worker','post_candidate_probe']:
    all_boundary+=json.loads((RUN/'evidence'/f'{label}.json').read_text())['boundary_evidence']['elapsed_seconds']
all_boundary+=worker
lines=['# E3 execution report — G4C-E3-002','',
'## Final status','',
'- **Execution: PASS — 60/60 fresh episodes completed.**',
'- **Independent validation: FAIL — stopped at the unchanged validator’s `Original tree dirty` gate.**',
'- **Protocol fidelity: PASS for production; validation stop honored. Full independent fidelity certification remains incomplete.**',
'- **Frozen coordinator scientific verdict: FALSIFIED; not independently validated.**',
'- Prior scientific run reused: **NO**. Protected artifact changed: **NO** (33/33 exact final hashes). E4/E5 run: **NO**.',
'', '## Identity, authorization and preservation','',
f"- Coordinator authorization UTC: `{auth['timestamp_utc']}`.",
f"- Final report UTC: `{datetime.datetime.now(datetime.timezone.utc).isoformat()}`.",
'- User explicitly accepted only the already-documented CERT-004 OneNote metadata hash and authorized proceeding after the prelaunch-only stop. CERT-004’s original NOT CERTIFIED report was not edited or relabelled.',
'- The initial failure report is preserved byte-for-byte as `checkpoint/PRELAUNCH_EXECUTION_REPORT.md`, bound by `checkpoint/infrastructure_preparation.json`.',
'- No E3-001 prediction or candidate state was consumed. Its frozen implementation was used through the existing approved asset generator; each new source/episode worker executed independently.',
'', '## Environment and production command','',
'```bash',
'set -o pipefail; .venv_baseline/Scripts/python.exe -I -B working/G4C-E3-002/coordinator/execution_coordinator.py 2>&1 | tee working/G4C-E3-002/results/execution.log',
'```',
'- External bash-tool timeout: 5,000 seconds. One coordinator, no restart, no duplicate workers, no early termination.',
'- Windows producer: Python 3.14.6, NumPy 2.5.3, zlib `1.3.1.zlib-ng`; explicit `.venv_baseline/Scripts/python.exe`, `-I -B`, numerical thread variables set to 1.',
'- Approved Linux numerical runtime: Python 3.14.4, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.0, joblib 1.5.3, threadpoolctl 3.6.0, Narwhals 2.25.0. All 4,355 runtime files, wheel hashes and Bubblewrap hash checked.',
'- Runtime lock SHA256: `cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514`.',
'- Native RF: `/home/jaswin/.local/share/statsgeeks/frozen_rf/5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870.pkl`, 1,336,382,673 bytes, mode 0444, verified Linux-native filesystem. Every episode reports `created=false`; no Windows-backed model fallback.',
'- Coordinator assets match CERT-004 byte-for-byte except the authorized new run identity. E2-008 transport was the existing approved generator’s input. No performance change was implemented.',
'', '## Preflight','',
'| Check | Result | Evidence |','|---|---|---|',
'| Historical preservation including accepted metadata exception | PASS: 1,151 files | `preflight_integrity.json` |',
'| Protected scientific artifacts | PASS: 33/33 | `preflight_integrity.json` |',
'| Host and approved runtime fingerprints | PASS | `checkpoint/data_host_preflight.json`, `checkpoint/runtime_preflight_native.json` |',
'| RF hash, native location, size and readonly mode | PASS | `checkpoint/runtime_preflight_native.json` |',
'| Frozen preprocessing, exact named feature order, arrays and identifiers | PASS | `checkpoint/data_host_preflight.json` |',
'| All 60 manifest bindings and RNG transitions | PASS | `checkpoint/data_host_preflight.json`, frozen run-local manifest |',
'| Fresh runtime/isolation probes | PASS | `evidence/preflight_*.json` |',
'| Frozen E3 parameters and scoring | PASS in production | Unchanged coordinator and worker hashes |',
'',
'Budgets were 5, 10 (diagnostic), 25, 50, 100, 200 labels/class, ten trials each. This is five primary budgets plus one diagnostic budget, not five total. Seed 42/PCG64 advanced once through the exact frozen episode order. No preprocessing, forest, or hyperparameter refit occurred. Madrid class means were computed in a fresh source worker, then frozen. Target translation used only each episode’s selected support labels; indicators 58–59 remained unchanged. No new Madrid CV or target tuning was performed.',
'',
'A preliminary shell-only runtime-check invocation was rejected because MSYS translated `/usr/bin/python3.14` into a Windows Git path. Both logs are preserved. Disabling shell argument conversion for the read-only WSL preflight restored the intended path; no worker launched in that failed invocation, no dependency changed, and production’s unchanged Python subprocess transport was unaffected.',
'', '## Execution and runtime','',
f"- Primary coordinator time: **{summary['total_primary_seconds']:.6f} s**; prediction/probe phase: **{summary['prediction_phase_seconds']:.6f} s**.",
f'- Sum of 60 worker/supervisor boundary times: **{worker:.6f} s**; including source and all three probes: **{all_boundary:.6f} s**.',
f"- Primary time outside those boundaries: **{summary['total_primary_seconds']-all_boundary:.6f} s**; includes integrity scans, WSL/JSON transport, packet construction, model staging verification, serialization, data loading and scoring. Not a pure coordinator CPU measurement.",
'- Production completed normally within the 5,000-second tool call. The recorded primary timer excludes its final integrity scan and console/report flush; the tool did not expose an exact full-call elapsed value. No exact full-call duration is invented.',
f"- Peak episode worker RSS: **{summary['peak_worker_rss_kib']:,} KiB**. Warnings: {len(summary['warnings'])}.",
f"- Historical preflight audit: {before['seconds']:.6f} s. Immediate post-production audit and final audit are separately timed in `hashes/`. No extra timing instrumentation was added inside the episode loop.",
f"- Independent validation stopped after **{failure['seconds']:.6f} s**. This is additional to production time.",
'- Every production output was verified before proceeding; all 60 NPZ outputs and per-worker transport/lifecycle evidence are retained. All predictions and workers finalized before query labels were attached for scoring.',
'', '| Episode | Budget | Trial | Boundary seconds | Worker | Teardown |','|---|---:|---:|---:|---|---|']
for r in rows:lines.append(f"| {r['episode_id']} | {r['budget']} | {r['trial']} | {r['worker_seconds']:.6f} | PASS | PASS |")
lines += ['', '## Frozen aggregate metrics','',
'Macro F1 over classes [1,2,3,4], zero_division=0; mean and population SD (`ddof=0`). All ten trials included at every budget. These are coordinator results, not fully independently certified results. Full per-episode metrics, per-class precision/recall/F1, confusion matrices and paired deltas are in `results/per_episode_results.json`.',
'', '| Labels/class | E3 mean ± SD | Raw prototype | Same-query RF | E3 − raw | E3 − RF |','|---:|---:|---:|---:|---:|---:|']
for b in ('5','10','25','50','100','200'):
    s=summary['summary'][b];lines.append(f"| {b} | {s['candidate']['mean']:.6f} ± {s['candidate']['std_ddof0']:.6f} | {s['raw_prototype']['mean']:.6f} | {s['frozen_rf']['mean']:.6f} | {s['candidate_minus_raw']['mean']:+.6f} | {s['candidate_minus_rf']['mean']:+.6f} |")
lines += ['', 'The frozen all-target zero-shot RF value 0.443273608786401 is contextual only, not a matched equal-information comparison. No new baseline was fitted.', '', '### Frozen 25-shot decision rule','', '| Criterion | Result |','|---|---|']
for k,val in summary['success_criteria'].items():lines.append(f"| {k} | {'PASS' if val else 'FAIL'} |")
lines += ['',f"- Mean per-class E3-minus-raw F1: `{summary['primary_per_class_delta_candidate_minus_raw']}`.",f"- Mean per-class E3-minus-RF F1: `{summary['primary_per_class_delta_candidate_minus_rf']}`.",
'- At 25 shots, all 10 raw-prototype paired gains were negative. Class-1 harm also violates the frozen safeguards. The unchanged decision rule returns **FALSIFIED**; improved mean F1 over RF alone does not make E3 successful. This is a development/reference-comparison result, not untouched final-audit evidence.',
'', '## Independent validation — mandatory stop','',
'Command: `wsl -d Ubuntu --exec /usr/bin/python3.14 -I -B <run>/run_independent_validation.py` (via shell with MSYS path conversion disabled). The launcher used the unchanged bound validator SHA256 `02299fc780e624933255b5aa4e01192bb8d4e53d92c27fd0bcb0d12834a8828c` and verified the approved numerical runtime tree. It did not import candidate/coordinator code or launch candidate workers.',
'',
'**Exact failure:** `e3_validator.production_context()` rejected Linux Git’s nonempty `git status --short -- original/` with `ValidationError: Original tree dirty`. This happened before `_validate` and before the complete independent 60-episode prediction/metric reconstruction. The validator was not changed, retried, or bypassed.',
'',
'Windows Git reports original/ clean. Linux Git marks `original/1-Introduction.ipynb`, `original/2-Reading_Data.ipynb`, and `original/3-Preprocessing.ipynb` modified. Read-only comparison/configuration diagnostics are retained in `validation/git_discrepancy_diagnostics.json`. The final content-hash audit still passes. This distinguishes a Git-view discrepancy from evidence of modified protected bytes; it does not convert the failed gate to PASS.',
'', '| Category | Status |','|---|---|',
'| Protected and historical content-hash integrity | PASS — independent pre/post/final hash audits |',
'| Episode completeness/uniqueness and budget/trial coverage | PASS — production and separate serialization audit, 60/60 |',
'| Output bindings, query identifiers, shapes, dtypes, class values | PASS — separate strict serialization/worker-evidence audit |',
'| Exact archive member names/order and decompressed NPY bytes | PASS — 360 members |',
'| Unchanged Windows producer byte replay | PASS — 60/60 complete archive replays |',
'| Cross-compressor raw ZIP identity | Not required; scientific payload equality not relaxed |',
'| Native-worker versus original-RF independent reconstruction | NOT COMPLETED — validator stopped before this phase |',
'| Independent metric/confusion recomputation | NOT COMPLETED |',
'| Independent aggregate/verdict recomputation | NOT COMPLETED |',
'| Cross-run contamination checks | PASS in construction and separate output-path audit; full bound-validator phase not reached |',
'| Frozen manifest/RNG/hash binding | PASS preflight/production; full bound-validator phase not reached |',
'| Teardown | PASS — all 60 episodes, source, two initial probes and final probe; no recorded survivors |',
'| Unchanged complete independent validator | **FAIL — original-tree Git gate** |',
'', '## Protected state','',
f"Final audit: **{audit['status']}**, 33 scientific artifacts and 1,151 historical files unchanged from this run’s authorized starting state. The accepted OneNote metadata hash did not change again. `original/` content hashes remain unchanged. No historical experiment output was overwritten. Expected/observed hashes for every historical file are in `hashes/final_protected_audit.json`.",
'', '| Protected artifact | Expected SHA256 | Observed SHA256 | Result |','|---|---|---|---|']
for c in protected:lines.append(f"| `{c['path']}` | `{c['expected_sha256']}` | `{c['observed_sha256']}` | {'PASS' if c['pass'] else 'FAIL'} |")
lines += ['', '## Output hashes and report lifecycle','',
'- `artifact_hash_manifest.json` is the immutable **prevalidation-phase** seal. Its report entry binds the prevalidation report preserved exactly at `checkpoint/PRIMARY_EXECUTION_REPORT_PREVALIDATION.md`; the original seal is not rewritten. Only this human-facing final report supersedes that report path, explicitly recorded in `validation/report_lifecycle.json`.',
'- `final_artifact_hash_manifest.json` binds the final reporting phase, including this report, the unchanged earlier seal, all scientific outputs, diagnostics, independent-validation failure and preserved reports. Its SHA256 is recorded in `final_artifact_hash_manifest.sha256`.',
f"- Frozen episode manifest SHA256: `{auth['manifest_hash']}`.",f"- RF SHA256: `{auth['rf_hash']}`.",f"- Prevalidation seal SHA256: `{sha(seal)}`.",f"- Source state canonical SHA256: `{summary['source_state_sha256']}`.",
'', '| Episode | Prediction artifact SHA256 |','|---|---|']
for r in rows:lines.append(f"| {r['episode_id']} | `{r['prediction_sha256']}` |")
lines += ['', '## Stop disposition','',
'No further scientific execution or validation recovery is authorized by this attempt. Preserve the failed validator and all outputs. A separately authorized resolution of the Windows/Linux Git clean-tree check is needed before a complete validation PASS can be issued. No E3 episode needs to be represented as missing, and no scientific success is claimed.', '']
primary.write_text('\n'.join(lines),encoding='utf8')
final={'run_id':RUN.name,'candidate':'E3','execution':'PASS','validation':'FAIL','protocol_fidelity':'PASS (production and mandatory validation stop; full independent certification incomplete)','scientific_verdict':summary['scientific_verdict'],'scientific_verdict_independently_validated':False,'episodes':60,'runtime_primary_seconds':summary['total_primary_seconds'],'prior_run_reused':False,'protected_artifact_changed':not all(c['pass'] for c in protected),'E4_E5_run':False,'files':{}}
for p in sorted(RUN.rglob('*')):
    if p.is_file():final['files'][p.relative_to(RUN).as_posix()]={'bytes':p.stat().st_size,'sha256':sha(p)}
save(RUN/'final_artifact_hash_manifest.json',final)
with (RUN/'final_artifact_hash_manifest.sha256').open('x') as f:f.write(sha(RUN/'final_artifact_hash_manifest.json')+'  final_artifact_hash_manifest.json\n')
print(json.dumps({'execution':'PASS','validation':'FAIL','episodes':60,'protected_audit':audit['status'],'runtime_primary_seconds':summary['total_primary_seconds'],'scientific_verdict':summary['scientific_verdict'],'final_manifest_sha256':sha(RUN/'final_artifact_hash_manifest.json'),'windows_git':diag['windows_status'],'linux_git':diag['linux_status'],'ignore_eol_exit':diag['linux_ignore_eol_diff']['returncode']},indent=2))
