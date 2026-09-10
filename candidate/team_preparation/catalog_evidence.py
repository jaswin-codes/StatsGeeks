"""Read-only source inspection; writes only preparation catalog, never snapshot files."""
from pathlib import Path
import json,hashlib,subprocess,datetime,zipfile,xml.etree.ElementTree as ET,ast
R=Path(__file__).resolve().parents[2];T=R/'candidate/team_preparation'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(n,o):(T/n).write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding='utf-8')
def main():
    notebooks=[]
    for base in ['working','original']:
        for p in (R/base).glob('*.ipynb'):
            obj=json.loads(p.read_text(encoding='utf-8'));cells=obj['cells'];codes=[c for c in cells if c['cell_type']=='code'];text='\n'.join(''.join(c['source']) for c in cells);errors=[o for c in cells for o in c.get('outputs',[]) if o.get('output_type')=='error']
            notebooks.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size,modified_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),cells=len(cells),code_cells=len(codes),executed_code_cells=sum(c.get('execution_count') is not None for c in codes),stored_errors=len(errors),final_candidate_names_present=[n for n in ['Coordinate_RF','ASTRA','EXP-010'] if n in text],classification='organizer/reference; no final-candidate implementation',dependency_lines=[line for c in codes for line in ''.join(c['source']).splitlines() if any(k in line for k in ['import ','read_parquet','open(','DATA_DIR','output_dir'])]))
    save('NOTEBOOK_INVENTORY.json',notebooks)
    slides=[];ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    with zipfile.ZipFile(R/'presentation/StatsGeeks_BuildingAge.pptx') as z:
        names=sorted([n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')],key=lambda n:int(n.split('slide')[-1].split('.')[0]))
        for n in names:slides.append(dict(slide=int(n.split('slide')[-1].split('.')[0]),text='\n'.join(t.text or '' for t in ET.fromstring(z.read(n)).findall('.//a:t',ns))))
    save('EXISTING_PRESENTATION_TEXT.json',slides)
    log=subprocess.check_output(['git','log','--all','--reverse','--format=%h | %an | %ad | %s','--date=iso'],cwd=R,text=True)
    (T/'GIT_HISTORY_EVIDENCE.txt').write_text(log,encoding='utf-8')
    inventory=[]
    for base in ['candidate/best_model','candidate/reports','candidate/tables','candidate/figures/publication','candidate/publication','presentation','submission_dry_run']:
        for p in (R/base).rglob('*'):
            if p.is_file() and p.suffix!='.onetoc2' and '__pycache__' not in p.parts:inventory.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p),modified_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()))
    save('DELIVERABLE_INVENTORY.json',inventory)
    # Read only OUR existing audit documents; no competitor implementation/figures/text copied into deliverables.
    external=R.parent/(R.name+' - excluded_forensics_20260909_201729')
    save('FORENSIC_SOURCE_REFERENCES.json',dict(external_quarantine=str(external),competitor_repository='C:/Users/jaswi/JaswinHackathon',latest_locally_evidenced_commit='cf9af6cffea292af9460bf572de33c32a10212d9',no_fetch_or_competitor_execution=True,own_audits=[dict(path=str(p),sha256=sha(p)) for p in external.glob('*.md')],scope='Read-only factual synthesis of our own forensic audits; no copied competitor documentation/code/results payload'))
    print('Cataloged',len(notebooks),'notebooks,',len(slides),'slides and',len(inventory),'publication/deliverable files')
if __name__=='__main__':main()
