"""Read-only integrity/health validation. Never fits or changes a model."""
from pathlib import Path
import json,hashlib,re,sys
from urllib.parse import unquote
R=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def local_links(path):
    text=path.read_text(encoding='utf-8',errors='replace')
    for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text):
        if '://' in target or target.startswith(('mailto:','#','data:')):continue
        target=unquote(target.split('#')[0]);dest=path.parent/target.replace('\\','/')
        if not dest.exists():yield target

def main():
    errors=[];manifest=json.loads((R/'SHA256SUMS.json').read_text())
    for name,expected in manifest['files'].items():
        p=R/name
        if not p.is_file():errors.append('Missing: '+name)
        elif sha(p)!=expected:errors.append('Hash mismatch: '+name)
    export=(R/'SUBMISSION_SCOPE.json').exists()
    if not export:
        for name,expected in json.loads((R/'candidate/reproducibility/freeze_before.json').read_text()).items():
            if not (R/name).is_file() or sha(R/name)!=expected:errors.append('Frozen file changed: '+name)
    for p in [R/'README.md',*list((R/'candidate/reports').glob('*.md')),R/'candidate/publication/README.md',R/'candidate/presentation/README.md',R/'candidate/best_model/README.md']:
        if p.exists():errors.extend(f'Broken link {p.relative_to(R)}: {link}' for link in local_links(p))
    figs=json.loads((R/'candidate/publication/FIGURE_MANIFEST.json').read_text())
    for fig in figs:
        for name in [*fig['files'],fig['transparent']]:
            if not (R/name).is_file():errors.append('Missing figure: '+name)
    for name in ['leaderboard','per_class','runtime','significance','ablation','spatial','learning_curve','prediction_summary','feature_importance']:
        for ext in ['csv','md']:
            if not (R/f'candidate/tables/{name}.{ext}').is_file():errors.append('Missing table: '+name)
    inference=json.loads((R/'candidate/best_model/INFERENCE_MANIFEST.json').read_text())
    for name,h in inference['files'].items():
        if sha(R/'candidate/best_model'/name)!=h:errors.append('Inference manifest mismatch: '+name)
    # Cross-check directory seals against the exact manifest-defined subset, not arbitrary current files.
    dirs=json.loads((R/'candidate/reproducibility/directory_hashes.json').read_text())
    for directory,record in dirs['directories'].items():
        entries=record['files'];payload=''.join(n+'\0'+manifest['files'][n]+'\n' for n in sorted(entries))
        if hashlib.sha256(payload.encode()).hexdigest()!=record['sha256']:errors.append('Directory hash mismatch: '+directory)
    print(json.dumps(dict(passed=not errors,files_checked=len(manifest['files']),figure_sets=len(figs),export_scope=export,errors=errors),indent=2))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
