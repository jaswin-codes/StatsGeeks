"""One-time preparation only: copy reviewed organizer deliverables, seal, never edit again.
No model code is imported or executed. Refuses any existing snapshot or ZIP.
"""
from pathlib import Path
import json,hashlib,shutil,datetime,subprocess,zipfile,os,stat,ast
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];T=R/'candidate/team_preparation';S=R/'candidate/SUBMISSION_SAFETY_SNAPSHOT';Z=R/'candidate/SUBMISSION_SAFETY_SNAPSHOT.zip'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
def main():
    assert not S.exists() and not Z.exists(),'Immutable snapshot already exists; refusing all writes'
    now=datetime.datetime.now(datetime.timezone.utc);stamp=now.strftime('%Y%m%dT%H%M%SZ');branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip();commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
    status=subprocess.check_output(['git','status','--short'],cwd=R,text=True)
    (T/'git_status_at_snapshot.txt').write_text(status,encoding='utf-8')
    # Protect all pre-existing scientific material, not transient OneNote/bytecode files.
    before={}
    for name in ['candidate','docs','working','original','data','models','presentation','submission','submission_dry_run','archive']:
        for p in (R/name).rglob('*'):
            if p.is_file() and 'team_preparation' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.onetoc2':before[p.relative_to(R).as_posix()]=sha(p)
    for name in ['README.md','.gitignore','requirements.txt','requirements-repro.txt','reproduce_best.py','SHA256SUMS.json','CITATION.cff']:before[name]=sha(R/name)
    save(T/'protected_before.json',before)
    mappings=[
      ('presentation/StatsGeeks_BuildingAge.pptx','presentation/StatsGeeks_BuildingAge.pptx','Organizer-requested presentation; strongest existing deck, frozen EXP-010 historical result'),
      ('presentation/StatsGeeks_BuildingAge.pdf','presentation/StatsGeeks_BuildingAge.pdf','Static viewing alternative for the same presentation'),
      ('submission_dry_run/justification/written_justification.txt','justification/written_justification.txt','Existing submission-ready standalone approach explanation; matches EXP-010 deck'),
      ('working/3-Preprocessing_member2_baseline_executed.ipynb','working/3-Preprocessing_member2_baseline_executed.ipynb','Strongest audited executed preprocessing notebook for accepted local artifact; REFERENCE, not a final candidate notebook'),
      ('working/4-Modelling_member3_reference_executed.ipynb','working/4-Modelling_member3_reference_executed.ipynb','Strongest audited executed modelling notebook; REFERENCE BASELINE ONLY, not EXP-010/Coordinate_RF'),
      ('working/minimal_standard_scaler.py','working/minimal_standard_scaler.py','Required import for the selected preprocessing notebook and its produced pickle'),
      ('candidate/exp010_predict.py','code/exp010_predict.py','Frozen EXP-010 adaptation implementation corresponding to the presentation; Python, not a notebook substitute'),
      ('candidate/artifacts/exp010_stage1_madrid.pkl','model/exp010_stage1_madrid.pkl','Small source-only learned adaptation state required by the frozen EXP-010 inference code'),
      ('submission_dry_run/requirements.txt','requirements.txt','Existing minimal dependency file for the EXP-010 inference CLI; not the full notebook environment')]
    for src,_,_ in mappings:assert (R/src).is_file(),src
    assert sha(R/'candidate/artifacts/exp010_stage1_madrid.pkl')=='2f4dc0f7a84ea54e967d7a96573b349331e1777ddb0a4a46e4925cad7bd6d266'
    for src,_,_ in mappings:
        if src.endswith('.ipynb'):
            nb=json.loads((R/src).read_text(encoding='utf-8'));assert nb['nbformat']==4 and isinstance(nb['cells'],list)
            assert not [o for c in nb['cells'] for o in c.get('outputs',[]) if o.get('output_type')=='error']
            for cell in nb['cells']:
                assert cell['cell_type'] in ('code','markdown','raw')
                if cell['cell_type']=='code':ast.parse(''.join(cell['source']))
        if src.endswith('.py'):ast.parse((R/src).read_text(encoding='utf-8'))
        if src.endswith('.pptx'):
            with zipfile.ZipFile(R/src) as z:
                assert z.testzip() is None
                for n in z.namelist():
                    if n.endswith('.xml'):ET.fromstring(z.read(n))
        if src.endswith('.pdf'):
            raw=(R/src).read_bytes();assert raw.startswith(b'%PDF-') and b'%%EOF' in raw[-100:]
    # Build entirely in staging; only atomic rename creates the final immutable path.
    staging=T/('_snapshot_staging_'+stamp);staging.mkdir(exist_ok=False);prefix='deliverables_'+stamp;rows=[]
    for src,dest,reason in mappings:
        out=staging/prefix/dest;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/src,out)
        assert sha(out)==sha(R/src)
        rows.append(dict(relative_path=prefix+'/'+dest,file_type=out.suffix.lstrip('.'),size=out.stat().st_size,sha256=sha(out),source_path=src,source_modified_utc=datetime.datetime.fromtimestamp((R/src).stat().st_mtime,datetime.timezone.utc).isoformat(),reason=reason))
    readme=f'''# PRE-OVERNIGHT SUBMISSION SAFETY SNAPSHOT — FROZEN

Created UTC: {now.isoformat()} · timestamped deliverables directory: `{prefix}/`.
Git branch: `{branch}`. Git HEAD: `{commit}`. Working tree was dirty; the commit alone does not identify this snapshot. The manifest and hashes do.

**DO NOT overwrite, edit, regenerate, add experiments, or optimize using this directory.** This is the currently safest known *existing organizer-facing fallback*, not a certification that the required final-method notebook already exists. Later optimization must never overwrite it. Work only on new copies outside the snapshot. File read-only flags are accidental-write protection, not administrator-proof immutability; an externally recorded seal and ZIP detect changes.

## Organizer instructions currently known
The operative instruction supplied for this task is: “The presentation, their written explanation of their approach, and their final notebook solutions. This is what you need to submit; the written explanation of your approach should be included in your presentation. And send everything to: uctstatsgeekssociety@uct.ac.za”. No email is sent by this task. Deadline, size limits, notebook count, presentation duration and full-target-pool/coordinate permission are not established by this message. Older rubric/word-limit notes are historical, not a new confirmation.

## Exactly what this fallback represents
The presentation (17 slides) and standalone written justification describe **frozen EXP-010**, seed-31337 audit, ten paired episodes/budget: 5=0.552428 ±0.059539; 25=0.612174 ±0.013057; 50=0.617273 ±0.007839; 100=0.619513 ±0.004770; 200=0.623982 ±0.003646. The matched full-feature target-only control gives 45/50 paired wins overall. Deviations are population SD, not confidence intervals. This is not the current Coordinate_RF learning curve.

Current development-locked research model (NOT the model in this deck): Coordinate_RF, 0.749299 ±0.005716 at 200 shots; matched ASTRA gain +0.016262, 200/200 wins. The validated publication bundle stays outside this minimal organizer snapshot: it is not a substitute for the requested final notebooks. No research/sealed evaluation data was copied here.

## Critical completeness warning
**No final notebook implementing EXP-010, ASTRA or Coordinate_RF was found.** The two included executed notebooks are the strongest audited *reference preprocessing/modelling evidence*, not invented or relabelled final solutions. They do not reproduce the EXP-010 or Coordinate_RF headlines. The matching frozen EXP-010 Python interface and source-only artifact are included as minimal operational support, but do not satisfy a notebook-only requirement. Therefore this folder is a protected fallback with an explicitly unresolved organizer deliverable; do not represent it as a fully compliant current-model submission.

## Contents and dependency boundary
Open the PPTX/PDF and text explanation directly; these are portable static files. The approach explanation is embedded across presentation slides 1/5/8/9 and the result interpretation in 6/10/11; the standalone text is not promised verbatim inside the deck.

The two notebooks retain their original bytes and embedded outputs. Preprocessing requires organizer `data/madrid_train.parquet` and `data/amsterdam_data.parquet`; modelling reads `../data/preprocessed/preprocessed_data.pkl` relative to its `working/` notebook directory. Raw data and the label-containing preprocessed pickle are intentionally **not distributed** here. If independently authorized to reproduce the reference, copy the *deliverables directory* elsewhere, obtain the organizer data, and keep `data/` beside `working/`. The local scaler module must be importable with that copied directory on PYTHONPATH. Notebook libraries: NumPy, pandas, Matplotlib, scikit-learn, SciPy, PyArrow plus a Jupyter environment. Historical Notebook 4 kernel was Python 3.11.9; exact historical in-kernel package provenance is incomplete. No notebook execution is requested as part of snapshot verification. Executing notebooks in this frozen directory would overwrite outputs/data and is forbidden; use an external working copy only.

The EXP-010 CLI requires already Madrid-standardized ordered 60-feature inputs. From an *external copy* of `{prefix}/`, inference syntax is:

`python code/exp010_predict.py --artifact model/exp010_stage1_madrid.pkl --support support.npz --query query.npz --shots 5 --seed 31337 --output predictions.npy`

Support NPZ: `X`, `y`, `feature_names`; query NPZ: `X`, `feature_names`, no labels. Exactly budget support labels/class, IDs 1–4. `requirements.txt` covers this CLI only. No support/query NPZ or target truth is included. Only load trusted, hash-verified pickle files.

## Known caveats preserved rather than silently repaired
- Deck/text are an older EXP-010 submission narrative. Their “primary result” is historical; the research incumbent is now Coordinate_RF.
- Deck slide 17 says selection/audit “sets never overlap”; this must not be read as pixel- or city-disjoint held-out validation. Historical episode sets share the target population.
- Slide 6's “OFFICIAL 25-SHOT RESULT” is an internally computed audit result, not evidence of organizer scoring.
- Slide 16's causal-sounding “dilution outweighed correction” is a hypothesis, not a proven explanation. Slide 3's performance ceiling below 1 is not quantified.
- Slide 14 says exact stack/cold start ~35 minutes; those historical statements are not a newly verified execution contract, particularly with the selected scaler-shim reference notebooks.
- Historical text says EXP-010 lacks independent replication. Later clean-process paired replay exists on the changed query population; neither is independent-city validation or a second-person attestation of the original audit.
- Baseline notebooks use label-dependent feature construction and non-fold-safe pre-CV scaling. These weaknesses are disclosed and not fixed here.
- Reference preprocessing uses a documented minimal scaler shim. It is not universal sklearn API equivalence. Some embedded reference prose contains text-encoding artifacts.

## Seal definition
MANIFEST.json indexes every payload and generated README/checklist file, with size/type/hash/source/reason. SHA256SUMS.txt covers those files plus MANIFEST.json. A file cannot contain a conventional SHA256 of its own final bytes; self-referential control-file hashes are therefore recorded in an **external seal receipt** under `candidate/team_preparation/`. That receipt hashes every final snapshot file, including both manifest files, and the sibling ZIP. No content changes occur after the atomic directory rename/seal.
'''
    (staging/'README.md').write_text(readme,encoding='utf-8')
    bydest={Path(row['relative_path']).name:row for row in rows}
    check=['# Final submission checklist — immutable fallback','','Organizer destination: `uctstatsgeekssociety@uct.ac.za`. **Integrity ready; final-method notebook requirement unresolved.**','','| Organizer requirement | Required file | Present? | Exact filename | SHA256 | Validated? | Notes / remaining concern |','|---|---|---|---|---|---|---|']
    for name,req,note in [('StatsGeeks_BuildingAge.pptx','Presentation including approach explanation','17-slide EXP-010 historical fallback; no Coordinate_RF deck'),('StatsGeeks_BuildingAge.pdf','Portable presentation viewing copy','Existing PDF container; no fresh rendering certification'),('written_justification.txt','Written explanation','Existing EXP-010 explanation; also described in slides'),('3-Preprocessing_member2_baseline_executed.ipynb','Notebook preprocessing solution','Reference only; organizer data excluded; scaler shim required'),('4-Modelling_member3_reference_executed.ipynb','Notebook modelling solution','Reference only; NOT a final EXP-010/Coordinate_RF notebook')]:
        v=bydest[name];check.append(f"| {req} | {name} | Yes (existing version) | `{v['relative_path']}` | `{v['sha256']}` | Hash and structural checks; historical execution where recorded | {note} |")
    check += ['| Current/frozen-method final notebook | No valid existing final notebook located | **NO** | — | — | **NOT SATISFIED** | Do not substitute a baseline notebook without disclosure |','| Supporting frozen EXP-010 inference | Python interface + source-only state | Yes | See MANIFEST.json | See MANIFEST.json | Byte-identical to protected originals | CLI is not a notebook |','| Notebook runtime data | Authorized organizer data / derived preprocessing | External prerequisite | Not included | Input hashes in team inspection | Not rerun | Intentional exclusion of label-containing data; not self-contained execution |','| Email submission | Presentation + explanation + final notebooks | Not sent | — | — | Not performed | Deadline, size limits and final-method notebook gap remain |','','PPTX is ZIP/XML-checked; notebooks pass JSON structure and code-AST checks with no stored error outputs. Full nbformat schema validation was unavailable: an existing environment metadata file caused a UTF-8 import error; no environment repair was attempted. No fitting or inference ran. PDF has valid header/end marker; visual fidelity across viewers remains a human check. Source provenance and full per-file hashes are in MANIFEST.json.']
    (staging/'FINAL_SUBMISSION_CHECKLIST.md').write_text('\n'.join(check)+'\n',encoding='utf-8')
    for name in ['README.md','FINAL_SUBMISSION_CHECKLIST.md']:
        p=staging/name;rows.append(dict(relative_path=name,file_type='md',size=p.stat().st_size,sha256=sha(p),source_path='generated from inspected repository evidence and operative user-supplied organizer instruction',source_modified_utc=now.isoformat(),reason='Required submission cover/checklist; exposes scope and gaps without changing original deliverables'))
    save(staging/'MANIFEST.json',dict(created_utc=now.isoformat(),timestamp_id=stamp,git_branch=branch,git_commit=commit,worktree_dirty=True,model_in_presentation='EXP-010 historical fallback',current_research_model='Coordinate_RF development-locked (not the deck)',organizer_email='uctstatsgeekssociety@uct.ac.za',submission_ready=False,blocker='Final-method notebook absent; included notebooks are reference evidence only',files=rows,control_files=[dict(relative_path='MANIFEST.json',file_type='json',source_path='generated snapshot metadata',reason='Indexes all deliverables; its hash/size recorded in SHA256SUMS.txt and external seal to avoid self-hash paradox'),dict(relative_path='SHA256SUMS.txt',file_type='txt',source_path='generated snapshot seal',reason='Hashes payload and manifest; its own hash/size recorded in external seal')]))
    paths=sorted(p for p in staging.rglob('*') if p.is_file());(staging/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(staging).as_posix()+'\n' for p in paths),encoding='utf-8')
    for line in (staging/'SHA256SUMS.txt').read_text().splitlines():h,n=line.split('  ',1);assert sha(staging/n)==h
    # No target truth containers or forensic payload; only one known source-only pickle is allowed.
    assert [p.name for p in staging.rglob('*.pkl')]==['exp010_stage1_madrid.pkl']
    assert not list(staging.rglob('*.npz')) and not list(staging.rglob('*.parquet'))
    for p in staging.rglob('*'):
        if p.is_file():assert 'competitor' not in p.name.lower() and 'sealed_evaluation' not in p.name.lower()
    staging.rename(S)  # Creation boundary: no file content inside S is changed after this line.
    final=[]
    for p in sorted(S.rglob('*')):
        if p.is_file():
            info=next((x for x in rows if x['relative_path']==p.relative_to(S).as_posix()),None)
            final.append(dict(relative_path=p.relative_to(S).as_posix(),file_type=p.suffix.lstrip('.'),size=p.stat().st_size,sha256=sha(p),source_path=info['source_path'] if info else 'generated snapshot seal',timestamp_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),reason=info['reason'] if info else 'Required immutable metadata/control file'))
            p.chmod(stat.S_IREAD)
    with zipfile.ZipFile(Z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(S.rglob('*')):
            if p.is_file():z.write(p,'SUBMISSION_SAFETY_SNAPSHOT/'+p.relative_to(S).as_posix())
    with zipfile.ZipFile(Z) as z:
        assert z.testzip() is None
        for row in final:assert hashlib.sha256(z.read('SUBMISSION_SAFETY_SNAPSHOT/'+row['relative_path'])).hexdigest()==row['sha256']
    Z.chmod(stat.S_IREAD)
    save(T/'SNAPSHOT_SEAL.json',dict(created_utc=now.isoformat(),snapshot=str(S),zip=str(Z),zip_sha256=sha(Z),zip_bytes=Z.stat().st_size,git_commit=commit,git_branch=branch,files=final,all_hashes_verified=True,read_only_files=True,submission_complete=False,competitor_payload=False,target_truth_containers=False,exp010_unchanged=True,immutability_limit='Read-only file flags + external hash seal; not WORM storage or protection against privileged deletion'))
    print(json.dumps(dict(snapshot=str(S),zip=str(Z),files=len(final),verified=True,branch=branch,commit=commit,submission_complete=False),indent=2))
if __name__=='__main__':main()
