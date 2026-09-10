"""Read-only verification of safety snapshot, prior artifacts and preparation consistency.
Writes reports ONLY in team_preparation. No model import, fit, prediction or optimization.
"""
from pathlib import Path
import json,hashlib,zipfile,tempfile,ast,datetime,collections,subprocess,re,os,stat
R=Path(__file__).resolve().parents[2];T=R/'candidate/team_preparation';S=R/'candidate/SUBMISSION_SAFETY_SNAPSHOT';Z=R/'candidate/SUBMISSION_SAFETY_SNAPSHOT.zip'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding='utf-8')
def main():
    seal=json.loads((T/'SNAPSHOT_SEAL.json').read_text());errors=[]
    for row in seal['files']:
        p=S/row['relative_path']
        if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['size']:errors.append('Snapshot mismatch: '+row['relative_path'])
    intended={r['relative_path'] for r in seal['files']};actual={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()};extra=sorted(actual-intended)
    unknown=[p for p in extra if not p.endswith('/Open Notebook.onetoc2') and p!='Open Notebook.onetoc2']
    if unknown:errors.append('Unexpected non-OneNote snapshot additions: '+str(unknown))
    for line in (S/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        h,n=line.split('  ',1)
        if sha(S/n)!=h:errors.append('Internal checksum mismatch: '+n)
    m=json.loads((S/'MANIFEST.json').read_text())
    for row in m['files']:
        if sha(S/row['relative_path'])!=row['sha256']:errors.append('Manifest mismatch: '+row['relative_path'])
    if sha(Z)!=seal['zip_sha256']:errors.append('ZIP changed')
    with zipfile.ZipFile(Z) as z:
        if z.testzip() is not None:errors.append('ZIP CRC failure')
        assert set(z.namelist())=={'SUBMISSION_SAFETY_SNAPSHOT/'+n for n in intended}
        for row in seal['files']:
            if hashlib.sha256(z.read('SUBMISSION_SAFETY_SNAPSHOT/'+row['relative_path'])).hexdigest()!=row['sha256']:errors.append('ZIP entry mismatch')
        assert not any(n.endswith(('.npz','.npy','.parquet','.onetoc2')) or 'competitor' in n.lower() or 'sealed_evaluation' in n.lower() for n in z.namelist())
        with tempfile.TemporaryDirectory(prefix='statsgeeks_safety_readonly_check_') as temp:
            z.extractall(temp);copy=Path(temp)/'SUBMISSION_SAFETY_SNAPSHOT'
            for row in seal['files']:assert sha(copy/row['relative_path'])==row['sha256']
            for p in copy.rglob('*.ipynb'):
                obj=json.loads(p.read_text(encoding='utf-8'));assert obj['nbformat']==4
                for c in obj['cells']:
                    if c['cell_type']=='code':ast.parse(''.join(c['source']))
                    assert not [o for o in c.get('outputs',[]) if o.get('output_type')=='error']
            for p in copy.rglob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    before=json.loads((T/'protected_before.json').read_text());changed=[]
    for n,h in before.items():
        if not (R/n).is_file() or sha(R/n)!=h:changed.append(n)
    if changed:errors.append('Pre-existing protected files changed: '+str(changed))
    # Arithmetic-only agreement with the locked evidence. No predictions are generated.
    final=json.loads((R/'candidate/autonomous_runs/20260909_1727/final_complete.json').read_text())
    expected={5:(.650253,.011246),25:(.687664,.012145),50:(.708436,.011277),100:(.729839,.008802),200:(.749299,.005716)}
    for b,(mean,sd) in expected.items():
        summary=final['summary'][str(b)]['Coordinate_RF'];assert round(summary['mean'],6)==mean and round(summary['population_sd'],6)==sd
        for name in ['PROJECT_MASTER_GUIDE.md','TONIGHT_REVISION.md']:
            text=(T/name).read_text(encoding='utf-8');assert f'{mean:.6f} ± {sd:.6f}' in text
    means=final['summary']['200'];deltas={n:round(means['Coordinate_RF']['mean']-means[n]['mean'],6) for n in ['ASTRA_AGF','EXP010','EXPF']}
    assert deltas==dict(ASTRA_AGF=.016262,EXP010=.126459,EXPF=.091697)
    assert len(list(T.glob('MEMBER_*_GUIDE.md')))==3
    bank=json.loads((T/'QUESTION_BANK.json').read_text());assert len(bank)==66
    groups=collections.Counter(q['category'] for q in bank);assert len(groups)==22 and set(groups.values())=={3}
    for q in bank:assert all(q[k] for k in ['question','short_answer','deeper_answer','key_numbers_facts','common_mistake_to_avoid'])
    required=['PROJECT_MASTER_GUIDE.md','MEMBER_1_GUIDE.md','MEMBER_2_GUIDE.md','MEMBER_3_GUIDE.md','TONIGHT_REVISION.md','PRESENTATION_QA.md','CONSISTENCY_AUDIT.md','INSPECTION_AND_SUBMISSION_DECISION.md']
    assert all((T/n).is_file() for n in required)
    words={n:len((T/n).read_text(encoding='utf-8').split()) for n in required};assert words['PROJECT_MASTER_GUIDE.md']==max(words.values())
    # Source-text chronology/ownership anchors and snapshot dependency exclusions are explicit.
    master=(T/'PROJECT_MASTER_GUIDE.md').read_text(encoding='utf-8')
    for token in ['FALSIFIED','INCONCLUSIVE','Original tree dirty','0.735239','0.733037','0.694216','0.696672','cf9af6c','overnight_best.json','working.minimal_standard_scaler','no final candidate notebook']:
        assert token.lower() in master.lower(),token
    broken_links=[]
    for p in T.glob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):continue
            if not (p.parent/target.split('#')[0]).exists():broken_links.append(dict(file=p.name,target=target))
    if broken_links:errors.append('Broken preparation links: '+str(broken_links))
    phases=dict(fitting=0,prediction=0,optimization=0,notebook_execution=0,source_refits=0,experiment_restarts=0,competitor_execution=0)
    report=dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),passed_payload_and_preservation=not errors,errors=errors,snapshot_intended_files=len(intended),snapshot_intended_hashes_valid=not any('Snapshot' in e or 'checksum' in e or 'Manifest' in e for e in errors),snapshot_directory_exact_membership=not extra,unsealed_background_files=extra,unsealed_files_deleted=False,clean_zip_hash=sha(Z),zip_integrity_and_external_extraction_pass=True,source_copy_hashes_preserved=True,read_only_ntfs_write_delete_protection='Applied to snapshot and ZIP; see SNAPSHOT_PROTECTION.json; no destructive write probe run',competitor_material_in_snapshot=False,development_or_sealed_truth_containers_in_snapshot=False,baseline_notebook_evaluation_displays_present=True,full_notebook_schema_validation='Unavailable due existing nbformat dependency-resource Unicode import error; JSON/AST checks pass; no dependency modifications',notebooks_current_model=False,notebooks_self_contained_runtime=False,notebook_external_dependencies=['authorized raw organizer Parquets','derived preprocessed pickle','compatible notebook/scientific environment'],exp010_unchanged=not any('exp010' in n.lower() for n in changed),protected_files_checked=len(before),protected_changes=changed,git_branch=m['git_branch'],git_commit=m['git_commit'],questions=len(bank),question_categories=len(groups),member_guides=3,broken_preparation_links=broken_links,word_counts=words,activity_counts=phases,submission_ready=False,isolated_future_work_preservation_ready=not errors,overnight_discovery_started=False,remaining_concerns=['Final-method notebook absent','Existing deck/text are historical EXP-010, not Coordinate_RF','Notebook runtime data excluded','Full-pool/coordinate organizer permission not confirmed','Human rendering/email delivery incomplete','Seven background OneNote indexes make directory membership non-pristine; clean ZIP authoritative','Optional source-rebuild publication archive lacks minimal scaler module; tested inference/evidence replay unaffected'])
    save(T/'FINAL_VALIDATION.json',report)
    # Fresh inventory outside the immutable snapshot; self-exclusion avoids circular hashing.
    files=[p for p in T.rglob('*') if p.is_file() and p.suffix!='.onetoc2' and p.name!='TEAM_PREPARATION_SHA256SUMS.json' and '__pycache__' not in p.parts]
    save(T/'TEAM_PREPARATION_SHA256SUMS.json',dict(algorithm='SHA256',scope='Preparation files except self, OneNote and bytecode; snapshot/ZIP bound separately by SNAPSHOT_SEAL.json',files={p.relative_to(T).as_posix():sha(p) for p in sorted(files)}))
    print(json.dumps({k:report[k] for k in ['passed_payload_and_preservation','snapshot_intended_files','snapshot_directory_exact_membership','clean_zip_hash','protected_files_checked','protected_changes','questions','question_categories','submission_ready','isolated_future_work_preservation_ready','overnight_discovery_started','errors']},indent=2))
    return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
