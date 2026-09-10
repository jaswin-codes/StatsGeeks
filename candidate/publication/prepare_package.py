"""One-time additive publication staging; preserves all prior scientific runs."""
from pathlib import Path
import hashlib,json,shutil,subprocess,datetime
R=Path(__file__).resolve().parents[2]; H=R/'candidate/autonomous_runs/20260909_1727'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    for n in ('tables','reports','best_model','reproducibility','presentation'): (R/'candidate'/n).mkdir(exist_ok=True)
    out=R/'candidate/reproducibility'
    assert not (out/'freeze_before.json').exists(),'Already prepared; do not overwrite'
    protected={}
    for base in ('candidate/autonomous_runs/20260909_1727','candidate/experiments_agf','candidate/experiments_2h','candidate/experiments_2h_v2','candidate/artifacts'):
        for p in (R/base).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.onetoc2': protected[p.relative_to(R).as_posix()]=sha(p)
    for p in (R/'candidate').glob('*.py'):protected[p.relative_to(R).as_posix()]=sha(p)
    for n,v in json.loads((H/'provenance.json').read_text())['protected'].items():
        p=R/n.replace('\\','/');assert sha(p)==v,n;protected[p.relative_to(R).as_posix()]=v
    (out/'freeze_before.json').write_text(json.dumps(protected,indent=2))
    (out/'git_status_before.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=R))
    (out/'git_diff_before.patch').write_bytes(subprocess.check_output(['git','diff','--binary'],cwd=R))
    B=R/'candidate/best_model'
    for n in ('agf_model.py','pool_state.pkl','SELECTION_LOCK.json','INFERENCE_MANIFEST.json','reproduce_best.py','requirements-repro.txt','configuration.json','provenance.json'):
        assert not (B/n).exists();shutil.copy2(H/n,B/n)
    shutil.copytree(H/'verification_inputs',B/'verification_inputs')
    moves=[]; stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # Historical forensic material is retained OUTSIDE the submission repository.
    p=R/'candidate/competitor_forensics'
    if p.exists():
        dest=R.parent/(R.name+' - excluded_forensics_'+stamp);shutil.move(str(p),str(dest));moves.append(dict(source='candidate/competitor_forensics',destination=str(dest),reason='Excluded third-party forensic material; preserved externally'))
    for n in ('core_diff.txt','integration_diff.txt','member2_vs_integration.txt'):
        p=R/n
        if p.exists():
            d=R/'archive/publication_cleanup'/n;d.parent.mkdir(parents=True,exist_ok=True);assert not d.exists();shutil.move(str(p),str(d));moves.append(dict(source=n,destination=d.relative_to(R).as_posix(),reason='Root scratch material; timestamps preserved'))
    d=R/'archive/publication_cleanup/README.before_publication.md';shutil.copy2(R/'README.md',d)
    (out/'cleanup_actions.json').write_text(json.dumps(moves,indent=2))
    print('Prepared immutable package and freeze baseline:',len(protected),'files')
if __name__=='__main__':main()
