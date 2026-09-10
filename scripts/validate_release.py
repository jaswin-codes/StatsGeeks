"""Static release checks: no model imports, pickle loads, fitting or predictions.

Run from any directory with Python 3.10+: python -B scripts/validate_release.py
Writes only reproducibility/release/{validation.json,inventory.csv,duplicates.json}.
Historical/protected link or wording findings are warnings, not silently repaired.
"""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import shutil
import statistics
import subprocess
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reproducibility/release'
PACKAGE = ROOT / 'FINAL_SUBMISSION'
EXPECTED = {
    5: ('0.650253', '0.011246'), 25: ('0.687664', '0.012145'),
    50: ('0.708436', '0.011277'), 100: ('0.729839', '0.008802'),
    200: ('0.749299', '0.005716'),
}
# Only these pre-existing documentation files may be rewritten by this release.
EDITABLE = {
    'README.md', 'docs/MASTER_PLAN.md', 'deliverables/README.md', '.gitignore',
    'scripts/README.md',
}
IMMUTABLE_DOCS = {'docs/AGENTS.md', 'docs/Hackathon_Analysis_Report.md',
                  'docs/building_age_transfer_learning_hackathon.md',
                  'docs/hackathon_computing_resources.md', 'docs/METRIC_LEARNING_APPROACH.md'}


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for b in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def active_doc(n):
    return (n == 'README.md' or n in {'presentation/README.md', 'deliverables/README.md',
                                    'scripts/README.md', 'archive/README.md', 'docs/README.md'}
            or n.startswith(('docs/judge/', 'docs/methodology/', 'docs/reproducibility/', 'docs/release/')))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    checks, details = [], {}
    def check(name, ok, detail=None, warning=False):
        checks.append({'name': name, 'status': 'PASS' if ok else ('WARNING' if warning else 'FAIL'), 'detail': detail})

    baseline = json.loads((OUT / 'baseline.json').read_text())['files']
    moves = json.loads((OUT / 'moves.json').read_text())
    hashes, missing, forbidden, edited, sidecars = {}, [], [], [], []
    inventory, groups = [], defaultdict(list)
    for old, entry in baseline.items():
        new = moves.get(old, old)
        p = ROOT / new
        allowed = (old in EDITABLE or (old in moves and old.endswith('.md')))
        if old in IMMUTABLE_DOCS:
            allowed = False
        if not p.is_file():
            missing.append(old)
        else:
            hashes[new] = digest(p)
            if hashes[new] != entry['sha256']:
                if old.endswith('.onetoc2'):
                    sidecars.append(old)
                else:
                    (edited if allowed else forbidden).append(old)
        groups[entry['sha256']].append(old)
        if old in moves:
            status = 'ARCHIVE' if new.startswith('archive/') else 'MOVE'
            reason = 'Superseded documentation/sidecar' if status == 'ARCHIVE' else 'Organized active documentation'
        else:
            status = 'KEEP'
            reason = 'Frozen or historical evidence; retain original paths and bytes'
            if old in EDITABLE:
                reason = 'Editable high-level release documentation'
        inventory.append([old, new, status, reason, entry['bytes'], entry['sha256']])
    check('preexisting_files_preserved_or_documented_moves', not missing, missing)
    check('all_scientific_and_other_protected_bytes_unchanged', not forbidden, {'violations': forbidden, 'editable_changes': edited})
    check('local_onenote_sidecar_bytes', not sidecars, {'changed': sidecars, 'note': 'Non-scientific OneNote navigation sidecars changed during folder relocation; retained locally. No model/data/result exception.'}, warning=True)
    details['preservation'] = {'baseline_files': len(baseline), 'baseline_bytes': sum(v['bytes'] for v in baseline.values()),
                               'byte_identical_files': len(baseline)-len(edited)-len(sidecars)-len(forbidden)-len(missing), 'moves': len(moves)}
    with (OUT/'inventory.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream); writer.writerow(['original_path', 'current_path', 'status', 'reason', 'bytes_before', 'sha256_before']); writer.writerows(inventory)
    duplicates = [v for v in groups.values() if len(v)>1]
    (OUT/'duplicates.json').write_text(json.dumps({'policy': 'Identical evidence/backups retained, not deduplicated destructively.', 'groups': duplicates}, indent=2))
    details['duplicate_groups'] = len(duplicates)
    details['dispositions'] = dict(Counter(row[2] for row in inventory))
    details['excluded_local_state'] = {'KEEP': 'Git internals and local environments; not release content',
                                      'REMOVE_recommended_only': 'Bytecode caches, notebook checkpoints, editor scratch files; no scientific evidence deleted'}
    def sha(p):
        n = p.relative_to(ROOT).as_posix()
        return hashes[n] if n in hashes else digest(p)

    manifest = json.loads((PACKAGE/'manifest.json').read_text())
    actual = {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()}
    check('sealed_package_membership', actual == set(manifest['files']) | {'manifest.json','checksums.sha256'})
    bad = [n for n,e in manifest['files'].items() if not (PACKAGE/n).is_file() or sha(PACKAGE/n)!=e['sha256'] or (PACKAGE/n).stat().st_size!=e['bytes']]
    check('sealed_package_manifest_hashes', not bad, bad)
    sums = dict((line.split('  ',1)[1], line.split('  ',1)[0]) for line in (PACKAGE/'checksums.sha256').read_text().splitlines() if line)
    check('sealed_checksum_coverage', set(sums) == actual-{'checksums.sha256'})
    bad = [n for n,h in sums.items() if not (PACKAGE/n).is_file() or sha(PACKAGE/n)!=h]
    check('sealed_checksums', not bad, bad)
    inference = json.loads((PACKAGE/'model/INFERENCE_MANIFEST.json').read_text())
    check('inference_hashes', all(sha(PACKAGE/'model'/n)==h for n,h in inference['files'].items()))
    lock = json.loads((PACKAGE/'model/SELECTION_LOCK.json').read_text())
    check('model_selection_and_pool_contract', lock['candidate']=='Coordinate_RF' and inference['pool_rows']==25992 and len(inference['feature_names'])==60)

    evidence = json.loads((PACKAGE/'model/evidence/final_complete.json').read_text())
    arithmetic_bad, grouped = [], defaultdict(list)
    for i, r in enumerate(evidence['records']):
        cm = r['confusion']
        values = []
        for c in range(4):
            denominator = sum(cm[c]) + sum(row[c] for row in cm)
            values.append(2*cm[c][c]/denominator if denominator else 0.0)
        if not math.isclose(sum(values)/4, r['f1'], abs_tol=1e-12, rel_tol=0): arithmetic_bad.append(i)
        grouped[(str(r['budget']),r['method'])].append(r['f1'])
    check('frozen_confusion_f1_arithmetic', not arithmetic_bad, {'records': len(evidence['records']), 'errors': arithmetic_bad})
    bad = []
    for (b,m), values in grouped.items():
        r = evidence['summary'][b][m]
        if not (len(values)==r['episodes'] and math.isclose(statistics.mean(values),r['mean'],abs_tol=1e-12,rel_tol=0)
                and math.isclose(statistics.pstdev(values),r['population_sd'],abs_tol=1e-12,rel_tol=0)): bad.append([b,m])
    check('frozen_summary_arithmetic', not bad, bad)
    bad = []
    for folder in [PACKAGE/'results_summary', ROOT/'candidate/tables', ROOT/'candidate/final_submission/tables']:
        with (folder/'learning_curve.csv').open(encoding='utf-8',newline='') as stream:
            for r in csv.DictReader(stream):
                ref = evidence['summary'][r['budget']][r['method']]
                if not all(math.isclose(float(r[k]),ref[k],abs_tol=1e-12,rel_tol=0) for k in ['mean','population_sd','episodes']): bad.append([str(folder),r['budget'],r['method']])
    check('all_learning_curve_copies_match_evidence', not bad, bad)
    check('locked_five_budget_values', all(tuple(f"{evidence['summary'][str(b)]['Coordinate_RF'][k]:.6f}" for k in ['mean','population_sd'])==v for b,v in EXPECTED.items()))

    notebook = json.loads((PACKAGE/'solution_notebook.ipynb').read_text())
    notebook_errors = []
    for i,c in enumerate(notebook['cells']):
        source = ''.join(c['source']) if isinstance(c['source'],list) else c['source']
        if c['cell_type']=='code':
            try: ast.parse(source)
            except SyntaxError as e: notebook_errors.append([i,str(e)])
            for target in re.findall(r"ROOT\s*/\s*['\"]([^'\"]+)['\"]",source):
                if not (PACKAGE/target).exists(): notebook_errors.append([i,target])
    check('notebook_structure_syntax_and_input_paths', notebook['nbformat']==4 and not notebook_errors, notebook_errors)
    try:
        # Read installed schema directly; do not import notebook execution machinery.
        import fastjsonschema
        import importlib.util
        schema = Path(importlib.util.find_spec('nbformat').origin).parent/'v4/nbformat.v4.5.schema.json'
        fastjsonschema.compile(json.loads(schema.read_text()))(notebook)
        check('notebook_full_schema',True)
    except Exception as e:
        check('notebook_full_schema',False,str(e),warning=True)
    zip_bad, xml_bad = [], []
    for p in PACKAGE.rglob('*'):
        if p.suffix in {'.pptx','.npz'}:
            with zipfile.ZipFile(p) as z:
                if z.testzip(): zip_bad.append(p.name)
                for n in z.namelist():
                    if n.endswith(('.xml','.rels')):
                        try: ET.fromstring(z.read(n))
                        except ET.ParseError: xml_bad.append([p.name,n])
    check('sealed_zip_xml_and_npz_crc',not zip_bad and not xml_bad,zip_bad+xml_bad)

    ns = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    ppt = ROOT/'presentation/Coordinate-RF_Judges.pptx'
    slide_text, bounds = [], []
    with zipfile.ZipFile(ppt) as z:
        check('companion_pptx_zip_integrity',z.testzip() is None)
        presentation = ET.fromstring(z.read('ppt/presentation.xml'))
        size = presentation.find('p:sldSz',ns); width,height = int(size.attrib['cx']),int(size.attrib['cy'])
        slides = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)),key=lambda n:int(re.search(r'slide(\d+)',n).group(1)))
        check('companion_exactly_ten_slides',len(slides)==10,len(slides))
        for n in slides:
            node=ET.fromstring(z.read(n));slide_text.append(' '.join(t.text or '' for t in node.findall('.//a:t',ns)))
            for transform in node.findall('.//a:xfrm',ns):
                off,ext=transform.find('a:off',ns),transform.find('a:ext',ns)
                if off is not None and ext is not None:
                    x,y,cx,cy=map(int,[off.attrib['x'],off.attrib['y'],ext.attrib['cx'],ext.attrib['cy']])
                    if min(x,y)<0 or x+cx>width+2 or y+cy>height+2:bounds.append(n)
    check('companion_slide_shape_bounds',not bounds,bounds)
    check('companion_score_and_name',all('0.749299' in slide_text[i] for i in [0,5,6,9]) and 'Coordinate-RF' in '\n'.join(slide_text))
    companion = json.loads((OUT/'companion_manifest.json').read_text())
    companion_bad = [n for n, h in companion['files'].items() if not (ROOT/n).is_file() or sha(ROOT/n) != h]
    check('presentation_companion_hashes', not companion_bad, companion_bad)
    layout = OUT/'powerpoint_layout.json'
    flags = json.loads(layout.read_text(encoding='utf-8-sig')) if layout.exists() else ['No native PowerPoint measurement']
    check('native_powerpoint_text_bounds',not flags,flags)
    pdf = ROOT/'presentation/Coordinate-RF_Judges.pdf'
    check('companion_pdf_container',pdf.is_file() and pdf.read_bytes().startswith(b'%PDF-') and b'%%EOF' in pdf.read_bytes()[-2048:])
    if shutil.which('pdftotext'):
        proc = subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True)
        pdftext=proc.stdout.decode('utf-8',errors='replace')
        check('companion_pdf_pages_and_results',proc.returncode==0 and pdftext.count('\f')==10 and all(v in pdftext for v in ['0.749299','0.687664','0.694216','0.696672']), {'pages':pdftext.count('\f')})
    else:check('companion_pdf_text_extraction',False,'pdftotext not installed',warning=True)

    justification=(ROOT/'docs/judge/WRITTEN_JUSTIFICATION.md').read_text().split('\n---')[0]
    word_count=len(re.findall(r'\S+',re.sub(r'^#+.*$','',justification,flags=re.M)))
    check('concise_explanation_under_300_words',word_count<=300,word_count)
    for n in ['README.md','docs/methodology/METHOD.md','docs/judge/WRITTEN_JUSTIFICATION.md']:
        t=(ROOT/n).read_text()
        check('all_budget_mean_sd_tokens:'+n,all(v in t for pair in EXPECTED.values() for v in pair))

    broken_active,broken_historical,wording_active,wording_historical=[],[],[],[]
    scanned, empty_dirs, large = 0, [], []
    pattern=re.compile(r'competitor|copied implementation|borrowed method|competitor[- ](?:inspired|workflow|pipeline)',re.I)
    for directory,children,files in os.walk(ROOT):
        children[:]=[n for n in children if n not in {'.git','__pycache__'} and not n.startswith('.venv')]
        d=Path(directory)
        if not children and not files:empty_dirs.append(d.relative_to(ROOT).as_posix())
        for name in files:
            p=d/name;n=p.relative_to(ROOT).as_posix()
            if n.startswith('reproducibility/release/'):continue
            if p.stat().st_size>100_000_000:large.append({'path':n,'bytes':p.stat().st_size})
            if p.suffix.lower() not in {'.md','.txt','.json','.py','.ipynb','.csv','.html','.log','.patch','.yaml','.yml'}:continue
            try:t=p.read_text(encoding='utf-8')
            except UnicodeError:continue
            scanned+=1
            for i,line in enumerate(t.splitlines(),1):
                if pattern.search(line):
                    (wording_active if active_doc(n) else wording_historical).append({'file':n,'line':i})
            if p.suffix != '.md':continue
            t=re.sub(r'```.*?```','',t,flags=re.S)
            for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',t):
                raw=target.split(' "')[0].strip('<>')
                if re.match(r'^[a-zA-Z][\w+.-]*:',raw) or raw.startswith('#'):continue
                local=unquote(raw.split('#')[0])
                if local and not (p.parent/local).exists():
                    (broken_active if active_doc(n) else broken_historical).append({'file':n,'target':raw})
    check('active_document_local_links_and_images',not broken_active,broken_active)
    check('historical_protected_local_links',not broken_historical,broken_historical,warning=True)
    check('active_document_wording',not wording_active,wording_active)
    check('protected_historical_wording_exceptions',not wording_historical,{'hits':len(wording_historical),'locations':wording_historical},warning=True)
    details['scan_scope']='All project text files of listed source/document/evidence types; Git internals/environments/cache excluded. Binary wording not certified; frozen binary bytes preserved.'
    details['text_files_scanned']=scanned;details['empty_directories']=empty_dirs;details['large_files_over_100MB']=sorted(large,key=lambda r:r['bytes'],reverse=True)
    details['link_scope']='Inline relative Markdown links/images; external URLs and heading anchors not certified.'

    versions={}
    for name in ['numpy','scipy','scikit-learn','pandas','matplotlib','python-pptx','Pillow','nbformat','fastjsonschema']:
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:versions[name]=None
    details['environment']={'python':sys.version,'installed_versions':versions,'clean_install_tested':False}
    check('git_index_untouched',subprocess.check_output(['git','ls-files','--stage'],cwd=ROOT,text=True)==(OUT/'git_index_before.txt').read_text())
    syntax_errors = []
    for n in ['scripts/validate_release.py', 'scripts/organize_release.py', 'presentation/build_judge_deck.py']:
        try: ast.parse((ROOT/n).read_text(encoding='utf-8'))
        except SyntaxError as exc: syntax_errors.append([n, str(exc)])
    check('release_script_syntax', not syntax_errors, syntax_errors)
    details['not_executed']=['training','optimization','hyperparameter search','support fitting','prediction regeneration','notebook cells','pickle deserialization','package installation','git add/commit/push']
    failures=sum(c['status']=='FAIL' for c in checks)
    payload={'checks':checks,'details':details,'failures':failures,'warnings':sum(c['status']=='WARNING' for c in checks),'scope':'Static validation and arithmetic on saved confusion matrices only'}
    (OUT/'validation.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps({'checks':len(checks),'failures':failures,'warnings':payload['warnings'],'dispositions':details['dispositions']},indent=2))
    for c in checks:
        if c['status']=='FAIL':print(c['name'],str(c['detail'])[:3000])
    return int(bool(failures))

if __name__=='__main__':
    raise SystemExit(main())
