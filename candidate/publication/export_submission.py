"""Allowlisted self-contained evidence/inference ZIP; never mirrors research/forensics."""
from pathlib import Path
import sys,json,hashlib,zipfile,datetime,subprocess
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_package import sha

def main():
    out=R/'candidate/publication/submission_bundle.zip';assert not out.exists(),'Refusing to overwrite an earlier export'
    subprocess.run([sys.executable,'-B',str(R/'candidate/publication/validate_package.py')],check=True,cwd=R)
    selected=set()
    for base in ['candidate/best_model','candidate/tables','candidate/reports','candidate/figures/publication','candidate/presentation']:
        selected.update(p for p in (R/base).rglob('*') if p.is_file() and p.suffix!='.onetoc2' and '__pycache__' not in p.parts)
    names=['README.md','reproduce_best.py','requirements-repro.txt','CITATION.cff','.gitignore','data/preprocessed/preprocessed_data.pkl']
    names += ['candidate/publication/'+n for n in ['README.md','FIGURE_MANIFEST.json','EXPERIMENT_CATALOG.json','build_publication.py','verify_evidence.py','verify_source.py','validate_package.py','audit_and_seal.py','export_submission.py']]
    names += ['candidate/reproducibility/'+n for n in ['environment_summary.json','dataset_manifest.json','requirements-repro.txt','freeze_before.json','source_manifest.json','command_manifest.json','analysis_validation.json','final_validation.json','legacy_link_warnings.json','cleanup_actions.json','cleanup_deferred.json','excluded_historical_comparisons.json']]
    h='candidate/autonomous_runs/20260909_1727/'
    names += [h+n for n in ['final_complete.json','spatial_complete.json','ablation_complete.json','optimization_complete.json','SELECTION_LOCK.json','provenance.json','configuration.json','sealed_evaluation.npz','development_support.npz','clean_replay/verification.json','port_check.json','FINAL_REPORT.md','RUN_LOG.md']]
    # Include only independently produced numeric evidence, not research search drivers or forensic comparisons.
    for base in [h+'final',h+'spatial','candidate/reproducibility/verification']:
        selected.update(p for p in (R/base).rglob('*') if p.is_file() and p.suffix in ['.npz','.json'])
    selected.update(R/n for n in names)
    assert all(p.is_file() for p in selected)
    for p in selected:
        assert 'competitor' not in p.name.lower() and 'forensics' not in p.parts,p
    payload={p.relative_to(R).as_posix():p.read_bytes() for p in sorted(selected)}
    scope=dict(description='Allowlisted own-source publication, frozen inference, numeric evidence and preprocessed artifact; no external forensic payload',not_included=['competitor snapshot or outputs','historical forensic-comparison scripts/results','optimization drivers','raw parquet data','legacy workflow notebooks','Git metadata','caches'],data_permissions='Check organizer authorization before public redistribution; this local bundle does not grant data rights',scope_note='Historical provenance catalogs may reference files not distributed. Freeze baseline is historical; archive integrity uses this archive SHA256SUMS.json.')
    payload['SUBMISSION_SCOPE.json']=json.dumps(scope,indent=2).encode()
    hashes={n:hashlib.sha256(v).hexdigest() for n,v in payload.items()}
    artifacts=dict(scope='All allowlisted archive payload except circular manifests',files=[dict(path=n,bytes=len(payload[n]),sha256=h) for n,h in sorted(hashes.items())])
    payload['candidate/reproducibility/artifact_manifest.json']=json.dumps(artifacts,indent=2).encode()
    dirs={}
    for n in hashes:dirs.setdefault(str(Path(n).parent).replace('\\','/'),[]).append(n)
    directory=dict(algorithm='SHA256 sorted root-relative path + NUL + file SHA256 + LF; immediate directory files in archive subset',directories={d:dict(files=sorted(ns),sha256=hashlib.sha256(''.join(n+'\0'+hashes[n]+'\n' for n in sorted(ns)).encode()).hexdigest()) for d,ns in dirs.items()})
    payload['candidate/reproducibility/directory_hashes.json']=json.dumps(directory,indent=2).encode()
    hashes={n:hashlib.sha256(v).hexdigest() for n,v in payload.items()}
    payload['SHA256SUMS.json']=json.dumps(dict(algorithm='SHA256',scope='All allowlisted archive payload except this self-referential manifest',files=hashes),indent=2).encode()
    with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n,data in sorted(payload.items()):z.writestr(n,data)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for n,h in hashes.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
        assert not any('competitor' in n.lower() or 'forensics' in n.lower() for n in z.namelist())
    receipt=dict(path=out.relative_to(R).as_posix(),sha256=sha(out),bytes=out.stat().st_size,files=len(payload),archive_hashes_verified=True,allowlist_verified=True,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),note='Receipt/ZIP excluded from research seal to avoid circularity; archive has its own independent seal')
    (R/'candidate/publication/distribution_receipt.json').write_text(json.dumps(receipt,indent=2))
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
