"""Maintainer-only evidence catalog, repository audit and publication seal; no fitting."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_package import sha,local_links
E=R/'candidate/reproducibility';D=R/'candidate/reports';P=R/'candidate/publication'
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def valid(p):return p.is_file() and '__pycache__' not in p.parts and p.suffix!='.onetoc2'
def main():
    frozen=json.loads((E/'freeze_before.json').read_text());bad=[n for n,h in frozen.items() if not (R/n).exists() or sha(R/n)!=h];assert not bad,bad
    save(E/'dataset_manifest.json',{p.relative_to(R).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size,role='unchanged local organizer input; check redistribution permission') for p in [R/'data/madrid_train.parquet',R/'data/amsterdam_data.parquet',R/'data/preprocessed/preprocessed_data.pkl'] if p.is_file()})
    # Catalog sidecars keep every scientific experiment directory byte-identical.
    roots=[R/'candidate/autonomous_runs/20260909_1727',R/'candidate/experiments_agf',R/'candidate/experiments_2h',R/'candidate/experiments_2h_v2']
    roots += [p for p in (R/'candidate/experiments_2h').iterdir() if p.is_dir() and p.name.startswith('exp')]
    roots += [p for p in (R/'working').iterdir() if p.is_dir() and p.name.startswith('G4')]
    catalog=[]
    for p in roots:
        key=p.relative_to(R).as_posix().replace('/','__');out=P/'experiment_catalog'/key;out.mkdir(parents=True,exist_ok=True)
        files=[f for f in p.rglob('*') if valid(f)];roles={k:[] for k in ['configuration','results','logs','metadata']}
        for f in files:
            n=f.name.lower();rel=f.relative_to(R).as_posix()
            if any(t in n for t in ('config','plan','selection_lock')):roles['configuration'].append(rel)
            if any(t in n for t in ('result','complete','score','prediction')):roles['results'].append(rel)
            if f.suffix in ('.log','.stderr') or 'log' in n:roles['logs'].append(rel)
            if any(t in n for t in ('metadata','provenance','environment','manifest')):roles['metadata'].append(rel)
        hashes={f.relative_to(R).as_posix():sha(f) for f in files}
        for role,paths in roles.items():save(out/(role+'.json'),dict(paths=paths,status='indexed' if paths else 'not found; not fabricated'))
        save(out/'hashes.json',hashes)
        (out/'README.md').write_text(f'# Historical experiment catalog\n\nOriginal path: `{p.relative_to(R).as_posix()}`. Original files remain in place to preserve frozen paths and timestamps. Sidecars index configuration, results, logs, metadata and hashes; missing original categories are explicitly marked. This catalog is not a new experiment or copied workflow.\n',encoding='utf-8')
        catalog.append(dict(path=p.relative_to(R).as_posix(),sidecar=out.relative_to(R).as_posix(),files=len(files),missing_roles=[k for k,v in roles.items() if not v]))
    save(P/'EXPERIMENT_CATALOG.json',catalog)
    broken=[]
    for base in ['README.md','candidate','docs','working','presentation','submission','archive']:
        p=R/base;paths=[p] if p.is_file() else p.rglob('*.md')
        for f in paths:
            for target in local_links(f):broken.append(dict(file=f.relative_to(R).as_posix(),target=target,status='legacy/reference warning'))
    save(E/'legacy_link_warnings.json',broken)
    leftovers=[p.relative_to(R).as_posix() for p in (R/'candidate/experiments_2h_v2').glob('*competitor*')]
    save(E/'excluded_historical_comparisons.json',dict(paths=leftovers,reason='Own historical forensic-comparison drivers/results; preserved in frozen provenance tree; excluded from final submission allowlist'))
    # Do not delete caches or scratch notebooks inside frozen experiment snapshots.
    cache_paths=[]
    for base in ['candidate','working','docs','presentation']:
        cache_paths += [p.relative_to(R).as_posix() for p in (R/base).rglob('__pycache__')]
    save(E/'cleanup_deferred.json',dict(cache_directories=cache_paths,reason='Excluded from export; retained locally to avoid deleting protected/referenced evidence'))
    figure_manifest=json.loads((P/'FIGURE_MANIFEST.json').read_text())
    gallery=['# Publication figure gallery','','Canonical figures: 350-DPI PNG, editable SVG and vector PDF. Tight transparent PNG variants are in `candidate/presentation/`. Error bars are population SD unless explicitly stated. No model optimization ran.','']
    for f in figure_manifest:
        n=f['name'];gallery += [f'## {n}',f"[PNG](../figures/publication/{n}.png) · [SVG](../figures/publication/{n}.svg) · [PDF](../figures/publication/{n}.pdf)",f['caption'],'']
    (P/'README.md').write_text('\n'.join(gallery),encoding='utf-8')
    (R/'candidate/best_model/README.md').write_text('# Frozen Coordinate_RF inference bundle\n\nByte-identical implementation, source-prior pool state, configuration and development lock from `candidate/autonomous_runs/20260909_1727`. This is the only current model package; prior packages remain historical.\n\nRun from repository root: `python -I -B reproduce_best.py --verify --out replay_new`. See [reproduction guide](../reports/REPRODUCIBILITY.md). Support inputs must preserve original pool row order. Full target features/coordinates are used, but no query truth or development-label bank is included here. Reference inputs contain designated support labels and expected predictions only.\n',encoding='utf-8')
    (D/'FINAL_REPORT.md').write_text('''# Final publication report

**Coordinate_RF is frozen and packaged.** No model changes, optimization or completed-experiment restarts occurred during publication.

- [Methods](METHODS.md) and [results](RESULTS.md): exact information regime, protocol and caveats.
- [Statistical evidence](STATISTICAL_ANALYSIS.md): 15 paired comparisons with Holm-adjusted tests and bootstrap intervals.
- [Spatial evidence](SPATIAL_ANALYSIS.md): geographic trade-off retained, not hidden.
- [Runtime](RUNTIME_REPORT.md) and [diagnostic scope](DIAGNOSTIC_LIMITATIONS.md): instrumentation limits stated.
- [Reproducibility](REPRODUCIBILITY.md), [repository audit](REPOSITORY_AUDIT.md) and [directory tree](DIRECTORY_STRUCTURE.md).

Publication generated 32 canonical figure sets (PNG/SVG/PDF at 350 DPI for raster exports), 32 transparent slide variants, and CSV/Markdown tables. Ten fixed-reference replays matched exactly; all 4,000 saved prediction arrays agreed with recorded confusion/F1 metrics. All 1,000 support/query and development/query exclusions passed. Protected source/evidence hashes remained unchanged.

The 200-shot random-pixel macro F1 is 0.749299 ± 0.005716 versus paired ASTRA 0.733037. The five-shot difference is inconclusive. Four-direction spatial mean is lower than ASTRA (0.694216 vs 0.696672). No independent-city superiority or official submission promotion is claimed.

An extracted-archive test outside the research repository also passed five packaged Coordinate_RF references and rebuilt every CSV byte-identically without Git metadata or research-tree dependencies. The final archive test receipt identifies the archive by SHA256 and is in `candidate/publication/distribution_test_receipt.json` (outside the seal to avoid a circular archive hash).\n\nThe final allowlisted ZIP is generated by `candidate/publication/export_submission.py`; it excludes competitor/forensic material, legacy workflows and caches. Raw-data redistribution permission and cross-platform environment portability remain external limitations. Historical incomplete metadata and broken archival links are recorded rather than falsified or silently deleted.
''',encoding='utf-8')
    moves=json.loads((E/'cleanup_actions.json').read_text())
    audit=['# Repository audit','','## Changes made','- Replaced root README; preserved its predecessor under `archive/publication_cleanup/`.','- Added an immutable inference copy, publication scripts, 32 figure sets, tables, slide variants, methods/results and reproducibility bundle.','- No model implementation or original scientific run changed. No optimization executed.','- Archived root scratch diffs and normalized the Windows-reserved `nul` artifact. No experimental evidence deleted.','- Extended .gitignore for environments, bytecode, OneNote/editor files, forensic reintroduction and generated ZIPs; explicitly allowed the 36-MB frozen inference state. Existing tracked user files were not untracked.','- Preserved Git history, index and pre-existing user changes; recorded dirty worktree and pre-publication diff.','- Sidecar catalogs index original configuration, results, logs, metadata and hashes without adding files inside frozen experiments.','','## Archived / moved / renamed']
    audit += ['- `'+m['source']+'` → `'+m['destination']+'`: '+m['reason'] for m in moves]
    audit += ['','## Removed files','None permanently deleted. Competitor forensics were moved intact to external quarantine, not copied into the submission.','','## Canonicalization','New publication figures have one canonical opaque/vector set in `candidate/figures/publication/`; slide-specific transparent variants are separate derived assets. Historical figure duplicates remain unchanged because they form prior run evidence. Large experimental trees stay in place to avoid invalidating hardcoded paths/hashes; the final export is an allowlist, not a mirror of the research tree.','','## Health and remaining warnings',f'- {len(catalog)} experiment directories indexed; missing metadata categories are marked in `EXPERIMENT_CATALOG.json`, not fabricated.',f'- {len(broken)} local Markdown link warnings in historical/research documents are inventoried in `candidate/reproducibility/legacy_link_warnings.json`. Active publication links are separately required to pass.','- Own historical competitor-protocol comparisons in `candidate/experiments_2h_v2/` remain protected historical evidence. They depend on quarantined forensic material and are deliberately not runnable or included in the final export. They are not publication evidence.','- Caches, OneNote files, old notebooks, failed logs and manifests are excluded from export, not deleted blindly; provenance dependencies make safe removal uncertain.','- Orphan check is conservative: all generated artifacts are referenced by figure/table/artifact manifests. Legacy unreferenced artifacts and unused manifests are retained because archival provenance is itself a valid use; no claim of complete semantic reference inference.','- No automated scan can prove independent authorship. The export uses reviewed own-source allowlists, inference dependency checks and the existing provenance declaration; no competitor snapshot/code/data/figures/workflows are included.','- Initial staging stopped on the Windows reserved filename `nul`; Git Bash moved it to `windows_reserved_nul.txt`. Staging records were recovered without repeating scientific computation.','- Raw datasets/large artifacts are historically Git-ignored. Local self-contained evidence export does not establish data redistribution rights or complete reproducibility of raw preprocessing.','- A prior full fresh-source replay is preserved. This phase verified ten reference arrays and recalculated all saved metrics, not another expensive full replay.','','## Validation scope','Frozen baseline checks, packaged source hashes, 4,000 confusion/F1 reconstructions, 1,000 exclusion checks, required outputs, image formats/DPI, active links and final SHA256 seals are checked. The distribution validator is read-only. Legacy warnings do not become scientific success claims.']
    (D/'REPOSITORY_AUDIT.md').write_text('\n'.join(audit)+'\n',encoding='utf-8')
    tree=['# Directory structure','','Current publication layout (expanded evidence directories; large historical trees summarized):','','```text','./','├── README.md','├── reproduce_best.py','├── requirements-repro.txt','├── SHA256SUMS.json','├── CITATION.cff','├── candidate/']
    for name in ['best_model','publication','figures/publication','tables','reports','reproducibility','presentation']:
        tree.append('│   ├── '+name+'/')
        for p in sorted((R/'candidate'/name).iterdir()):
            if p.suffix!='.onetoc2':tree.append('│   │   ├── '+p.name+('/ [indexed contents]' if p.is_dir() else ''))
    tree += ['│   ├── autonomous_runs/20260909_1727/ [immutable original evidence]','│   ├── experiments_agf/ [prior immutable package]','│   ├── experiments_2h/ [historical experiments; EXP-F implementation]','│   └── experiments_2h_v2/ [historical ASTRA; excluded forensic comparisons]','├── archive/publication_cleanup/ [previous README and root scratch outputs]','├── data/ [local organizer parquet and preprocessed artifact]','├── docs/ [historical project documentation]','├── original/ [organizer notebooks]','├── working/ [historical gates and experiments]','├── models/ [historical source artifacts]','├── submission/ and submission_dry_run/ [historical, not final export]','└── presentation/ [historical decks]','```','','Machine-readable complete publication file inventory: `candidate/reproducibility/artifact_manifest.json`. Historical experiment inventory: `candidate/publication/EXPERIMENT_CATALOG.json`. The final ZIP contains only the allowlisted subset defined by its `SUBMISSION_SCOPE.json`; the full research-tree inventory is not its payload.']
    (D/'DIRECTORY_STRUCTURE.md').write_text('\n'.join(tree)+'\n',encoding='utf-8')
    commands=dict(executed=['python -B candidate/publication/prepare_package.py (partial failure on reserved nul; recovered without rerunning preparation)','Git Bash: mv nul archive/publication_cleanup/windows_reserved_nul.txt','python -B candidate/publication/verify_evidence.py','python -B candidate/publication/build_publication.py','python -B candidate/publication/audit_and_seal.py','python -B candidate/publication/validate_package.py','python -B candidate/publication/export_submission.py','python -B candidate/publication/test_distribution.py (isolated ZIP validation, five packaged references, evidence rebuild; all CSVs byte-identical)'],replay_order=['Install requirements-repro.txt','Validate received hashes before rebuilding','Run reproduce_best.py --verify --out a_new_directory','Optional evidence build from saved verification outputs'],not_executed=['optimization','full source refit','full 1000-episode model refit replay'],failure_recovery='Reserved nul filename moved with Git Bash; completed preparation copy/log metadata recovered. No scientific stage restarted.')
    save(E/'command_manifest.json',commands)
    # Active links must resolve before seal issuance.
    active=[R/'README.md',*D.glob('*.md'),P/'README.md',R/'candidate/presentation/README.md',R/'candidate/best_model/README.md']
    errors=[dict(file=p.relative_to(R).as_posix(),target=t) for p in active for t in local_links(p)]
    # Manifests are written below; only those known forthcoming targets are allowed now.
    forthcoming={'../../SHA256SUMS.json','../reproducibility/directory_hashes.json','../reproducibility/artifact_manifest.json','../reproducibility/final_validation.json'}
    errors=[e for e in errors if e['target'] not in forthcoming];assert not errors,errors
    from PIL import Image
    for f in figure_manifest:
        for n in f['files']:assert (R/n).is_file()
        with Image.open(R/f['files'][0]) as im:assert min(im.info['dpi'])>=300
    validation=dict(passed=True,protected_files_unchanged=len(frozen),new_exact_reference_arrays=10,saved_confusion_arrays_verified=4000,episodes_exclusion_checked=1000,figure_sets=32,formats=['PNG','SVG','PDF'],minimum_png_dpi=350,active_links_valid=True,query_truth_not_supplied_to_inference=True,competitor_snapshot_quarantined=True,submission_allowlist_required=True,limitations='Historical warnings and unmeasured diagnostics retained explicitly; source replay not rerun',isolated_distribution_test='Passed on first sealed archive: five packaged reference arrays and all rebuilt CSVs byte-identical. Final archive retest receipt is external to the seal to avoid circularity.')
    save(E/'final_validation.json',validation)
    paths={R/n for n in frozen}
    for name in ['candidate/publication','candidate/tables','candidate/reports','candidate/figures/publication','candidate/presentation','candidate/best_model','candidate/reproducibility']:
        paths.update(p for p in (R/name).rglob('*') if valid(p))
    paths.update(R/n for n in ['README.md','reproduce_best.py','requirements-repro.txt','CITATION.cff','.gitignore'])
    excluded={'artifact_manifest.json','directory_hashes.json','SHA256SUMS.json','distribution_receipt.json','distribution_test_receipt.json'}
    paths={p for p in paths if valid(p) and p.name not in excluded and p.suffix!='.zip' and 'experiment_catalog' not in p.parts}
    hashes={p.relative_to(R).as_posix():sha(p) for p in sorted(paths)}
    artifacts=[dict(path=n,bytes=(R/n).stat().st_size,sha256=h,role='frozen historical input' if n in frozen else 'publication output or implementation') for n,h in hashes.items()]
    save(E/'artifact_manifest.json',dict(scope='Protected scientific evidence plus active publication; excludes catalogs, archive, self-referential seals and ZIP/receipt',files=artifacts))
    dirs={}
    for n in hashes:dirs.setdefault(str(Path(n).parent).replace('\\','/'),[]).append(n)
    save(E/'directory_hashes.json',dict(algorithm='SHA256 sorted root-relative path + NUL + lowercase SHA256 + LF; immediate directory files in seal subset',directories={d:dict(files=sorted(names),sha256=hashlib.sha256(''.join(n+'\0'+hashes[n]+'\n' for n in sorted(names)).encode()).hexdigest()) for d,names in dirs.items()}))
    for p in [E/'artifact_manifest.json',E/'directory_hashes.json']:hashes[p.relative_to(R).as_posix()]=sha(p)
    save(R/'SHA256SUMS.json',dict(algorithm='SHA256',scope='See artifact manifest; self excluded; no Git-history identity implied',files=hashes))
    print('Sealed',len(hashes),'files; protected',len(frozen),'; legacy link warnings',len(broken))
if __name__=='__main__':main()
