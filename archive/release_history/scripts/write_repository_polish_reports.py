"""Write additive human review reports from measured static audit receipts.

This is editorial scoring, not an official competition judgment. Reports refuse
replacement and never alter scientific evidence, configuration or model code.
"""
from __future__ import annotations

import json
from pathlib import Path

from repository_polish_audit import ROOT

BASE = ROOT/'reproducibility/repository_polish'
BASELINE = json.loads((BASE/'baseline.json').read_text())['files']
SUMMARY = json.loads((BASE/'inventory_summary.json').read_text())
VALIDATION = json.loads((BASE/'validation_attempt_05/validation.json').read_text())


def put(name: str, text: str) -> None:
    path = ROOT/name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text.rstrip()+'\n')


def main() -> None:
    folders = '\n'.join(f"| `{name}` | {row['files']} | {row['bytes']/1e6:.2f} |" for name, row in SUMMARY['folders'].items())
    large = '\n'.join(f"| `{name}` | {BASELINE[name]['bytes']/1e6:.2f} | KEEP — historical model, dataset or audit evidence; not a minimal-package dependency |" for name in SUMMARY['largest_files'][:12])
    duplicates = SUMMARY['duplicate_groups']
    notebook_groups = [g for g in duplicates if any(n.endswith('.ipynb') for n in g)]
    notebook_text = '\n'.join('- KEEP — byte-identical group: '+ '; '.join(f'`{n}`' for n in group) for group in notebook_groups)
    report_groups = [g for g in duplicates if any(n.endswith('.md') for n in g)]
    report_text = '\n'.join('- KEEP — '+ '; '.join(f'`{n}`' for n in group) for group in report_groups[:8])
    put('REPOSITORY_AUDIT.md', f'''# Repository audit — preservation-first

## Scope and evidence
Before changes: **{len(BASELINE):,} files, {sum(v['bytes'] for v in BASELINE.values())/1e9:.3f} GB**,
excluding Git internals, `.venv_baseline`, named virtual environments and bytecode
caches. Inventory includes the newly introduced inventory script itself. No file
is deemed unused merely because it is old, duplicated or large. Every action
recommendation below is explicitly KEEP, MOVE, ARCHIVE or IGNORE.

Baseline: [baseline.json](reproducibility/repository_polish/baseline.json).
Exact duplicates, notebooks, temporary candidates, scripts and largest files:
[inventory_summary.json](reproducibility/repository_polish/inventory_summary.json).
The initial working tree was already dirty; it was neither reverted nor staged.

## Current structure at entry
| Directory | Files | Decimal MB |
|---|---:|---:|
{folders}

## Findings and disposition
| Area | Finding | Recommendation |
|---|---|---|
| Current science | `candidate/final_submission/` and `candidate/best_model/` contain frozen Coordinate-RF artifacts | KEEP — authoritative sources at current paths |
| Historical runs | `working/`, `candidate/autonomous_runs/`, `candidate/autonomous_ml_overnight/`, `experiments_2h*`, `experiments_agf/` | KEEP — research provenance, excluded from judge package |
| Apparently unused folders | Root `models/` and `submission/` each contain only a OneNote index; no model/submission payload | IGNORE — dormant historical scaffolding; do not populate with duplicate models |
| Organizer assets | `original/`, `data/` and source challenge documents | KEEP — never edit or redistribute without approval |
| Draft presentations | Root `presentation/StatsGeeks_BuildingAge.*` differs in role from `candidate/final_submission/presentation/*FINAL*` | KEEP — historical; route judges only to final copies |
| Old exports | Prior ZIPs in `archive/`, `candidate/publication/`, overnight runs and safety snapshots | KEEP — backups are evidence, not disposable clutter |
| Temporary candidates | {len(SUMMARY['temporary_candidates'])} `.onetoc2`, `.pre_completion`, `.pre_dependency_repair`, `.tmp`/`.bak` candidates | IGNORE active OneNote metadata; KEEP pre-repair files as audit evidence |
| Auto-generated sidecars | OneNote index files appeared in new folders; root/archive indices changed during this pass | ARCHIVE only new distribution sidecars when encountered; do not rewrite original indices or claim global byte invariance |
| Old figures | Legacy plots and transparent slide assets coexist with canonical publication figures | KEEP — archive provenance; exclude from minimal package except embedded final assets |
| Duplicate notebooks | Four byte-identical groups found (below) | KEEP — originals, executed references and safety copies have different provenance roles |
| Duplicate reports | {len(report_groups)} identical Markdown groups within {len(duplicates)} duplicate groups across all types | KEEP — versioned evidence; use a single judge entry point, not deletion |
| Orphan scripts | {len(SUMMARY['python_scripts'])} Python files inventoried; dynamic notebook/CLI usage prevents reliable automatic orphan proof | KEEP — no proven-dead script removed; `scripts/README.md` documents baseline tools |
| Unsafe audit commands | Legacy `scripts/README.md` says tools do not train, but documents Madrid RF refits; candidate replay also fits support RFs | KEEP original text; use the new no-model-execution validator only |
| Names | `Coordinate_RF` machine ID, Coordinate-RF prose, ASTRA_AGF, EXP010/EXP-010 and EXPF/EXP-F coexist | KEEP frozen IDs; use Coordinate-RF consistently in new prose and document aliases |
| Root README | Frozen in `SHA256SUMS.json`; valid headline but not a complete final judge guide | KEEP bytes; MOVE judge reading flow to `docs/README_SUBMISSION.md` and new package README |
| Historical master plan | Still describes planning-era status | KEEP original; add `docs/MASTER_PLAN_POLISH_ADDENDUM.md` rather than rewriting history |
| Requirements | Legacy baseline Python 3.13.15 / NumPy 2.5.1 differs from final Python 3.14.6 / NumPy 2.5.3 | KEEP both historical environments; use only new package requirements for its contract |
| Environment health | All six new package pins match installed metadata, but nbformat import fails on a non-UTF-8 schema-resource entry | KEEP failure evidence; clean environment repair requires a separate authorized task |
| License | No root LICENSE or confirmed organizer redistribution grant | KEEP notices; defer a license grant pending rights-holder approval |
| Structural organization | Artificial root `src/`, `notebook/`, `tables/` duplication would increase confusion and threaten imports | KEEP existing module paths; use additive `docs/`, `deliverables/`, `figures/`, `reproducibility/`, `FINAL_SUBMISSION/` |

## Duplicate notebooks (exact SHA-256 identity)
{notebook_text}

## Representative duplicate reports
{report_text or 'No exact duplicate Markdown groups.'}

## Large artifacts — usage not presumed absent
| Artifact | Decimal MB | Action |
|---|---:|---|
{large}

## Broken links and reference scope
KEEP — the explicit-inline-link scan reports one historical missing target:
`README.ijg` from the vendored pypdfium2 libjpeg-turbo license documentation.
It is outside the final package; do not edit third-party notices. New guide links
are checked after report creation. External URLs, Markdown anchors, dynamic code
paths and arbitrary prose references are not exhaustively certified.

KEEP — historical manifests and reports retain original relative paths, explained
in the new package README. No global claim of “no stale numbers anywhere” is
possible while preserving old experiment evidence. Current five-budget values
match across the selected table, slides, PDF, report, notebook and new guides.

## Archival outcome
ARCHIVE — documentation snapshots under `archive/repository_polish/snapshots/`.
ARCHIVE — this pass's first package and diagram drafts; no pre-existing scientific
file moved. The first build stopped safely on an exclusive-create filename
collision. The first package was then preserved before correcting UTF-8 notebook
reading and schematic labels. Failed validation attempts remain visible.
''')
    put('docs/VALIDATION_ADDENDUM.md', '''# Validation addendum — later checks in the same polish pass

This document qualifies the earlier build-time statements in the new guides and
sealed package README; it does not change their files or historical receipts.

- The current PDF was freshly rendered with the existing local pypdfium2 library:
  16 pages, two contact sheets, with no installation or model execution.
- Contact sheets for all pages and full-resolution page 11 were inspected. Page
  11 clips the bottom of the confusion-matrix plot; do not claim visual readiness.
- PowerPoint ZIP/XML parsing passed; no fresh PowerPoint application render occurred.
- Full notebook v4.5 schema validation passed using fastjsonschema and the installed
  bundled schema directly. The normal nbformat import remains environment-blocked
  by a non-UTF-8 resource entry; this is not a successful notebook runtime test.
- The five embedded slide PNGs match existing canonical assets by hash. This proves
  asset identity, not that every plotted coordinate has been independently rebuilt.
- Two original OneNote indices changed during the audit. No audit command wrote
  them; background indexing is suspected, not forensically proven. All original
  non-OneNote files and every entry in the frozen root manifest remain unchanged.

See [deliverable validation](../DELIVERABLE_VALIDATION.md) and the final validator
receipt for measured scope. No source or support model was trained.
''')
    checks = '\n'.join(f"| `{c['name']}` | {c['status']} |" for c in VALIDATION['checks'] if c['name'] != 'new_explicit_local_markdown_links')
    put('DELIVERABLE_VALIDATION.md', f'''# Deliverable validation

**Conditional review package, not an unconditional submission certificate.**
Scientific training/inference was prohibited. No source fit, support RF fit,
prediction generation, model deserialization or notebook execution was performed.

## Deliverables
| Deliverable | Check performed | Outcome / remaining gate |
|---|---|---|
| Presentation | ZIP CRC, XML, embedded-image decoding, python-pptx open, text and shape bounds | 16 slides; original bytes preserved; slide 11 picture extends below canvas |
| PDF | Header/EOF, successful pdftotext, 16-page count; fresh PDFium render | All 16 pages render; page 11 bottom-axis clipping confirmed visually |
| Notebook | JSON, complete v4.5 bundled schema via fastjsonschema, AST syntax, literal dependencies | PASS; outputs/metadata identical and only permitted path changes; execution NOT RUN |
| Written explanation | UTF-8 open, exact slide-body match, scores and whitespace word count | 340 words; below 500, above conservative 300 limit |
| First slide | Text extraction, whitespace count | 28 words including title; under 150, but completeness is a judging question |
| Model | Frozen SHA-256, selection ID, 60-feature/25,992-row manifest, pickle opcode parsing | PASS structurally; deserialization and functionality NOT RUN |
| Reference inputs | Five safe NPZ loads, balanced support, disjoint valid queries, class ranges | PASS; no reference prediction regenerated |
| Inference | Original runner byte identity, new wrapper syntax and path resolution | Static PASS; both --support and --verify fit RFs, therefore not executed |
| Requirements | PEP 508 parsing and installed metadata comparison | Six pins match; nbformat import environment BLOCKED; clean install NOT RUN |
| Manifest/checksums | Exact membership, byte lengths, SHA-256 and original-copy comparisons | PASS for the sealed clean package; check again after background applications stop |
| Scientific metrics | F1 from 4,000 saved confusion matrices, means/SD, all three learning-curve copies | PASS within absolute 1e-12; no scientific value written |
| Figures | Five embedded slide PNG hashes match existing assets; SVG/PNG schematics parse | PASS for identity/formats; no independent regeneration of scientific plots |
| Frozen evidence | Existing root SHA256SUMS.json and all original non-OneNote bytes | PASS; zero frozen-manifest mismatches |
| All original files | Before/after inventory including OneNote metadata | FAIL: two original `.onetoc2` indices changed, none missing; not concealed |

## Recorded check detail before final document-link sweep
{checks}

The intermediate missing-new-document links were expected while these reports
were not yet created. The final receipt is
`reproducibility/repository_polish/validation_final/validation.json`.
All failed attempts are retained; attempt 01 hit the nbformat import issue,
attempt 02 exposed an explicit UTF-8 handling error in the new validator, and
attempt 03 detected sidecar contamination and the first notebook derivative's
encoding issue. That entire derived package was archived before rebuilding.
No original notebook or output was repaired or overwritten.

## Visual and semantic review
Fresh renders: `reproducibility/repository_polish/visual_review/`.
All pages inspected as contact sheets; page 11 also inspected at full resolution.
The plot extends beyond the page bottom, hiding its x-axis label and clipping
its tick labels. Small figure text and dense explanation slides warrant a real
presentation-screen review. Existing scientific graphics and slides were not
modified to mask these issues.

Score tokens match at six displayed decimals across new README, executive summary,
method guide, locked report, saved notebook, PowerPoint and PDF. The five means
match the written explanation. This is a scoped consistency check, not a claim
that every historical document contains only current results. Historical report
and slide replay claims refer to their original package, not new execution here.

## Acceptance decision
Do not certify immediate upload until organizer eligibility, official word limit,
source-artifact/interface requirements, rights, clean runtime and slide clipping
are resolved through explicitly authorized follow-up. See FINAL_PRE_FLIGHT.md.
''')
    put('JUDGE_REVIEW.md', '''# Mock judge review

Editorial scores out of 10, not official rubric scores or predictions of a prize.
The scientific solution remains Coordinate-RF. No metric optimization is proposed.

| Dimension | Score | Deductions |
|---|---:|---|
| Scientific quality | 7.5 | Fixed-city audit, historical exposure, extra development supervision and eligibility ambiguity |
| Novelty | 7.0 | Context/prior/coordinate integration is useful; familiar building blocks and limited independent transfer evidence |
| Presentation | 7.0 | Coherent story and honest limitations; slide 11 clipping, small plots, dense explanation appendix |
| Documentation | 9.0 | Clear new judge path and provenance; frozen root README cannot be redirected and historical context remains complex |
| Repository quality | 8.0 | Minimal allowlisted distribution; large dirty research tree and active index-file contamination remain |
| Reproducibility | 7.0 | Strong hashes and exact saved-evidence checks; no permitted runtime replay, clean install or raw-data reconstruction |
| Professionalism | 8.0 | Transparent negative results and blockers; license/eligibility/word-limit decisions unresolved |
| Code quality | 7.0 | Explicit frozen contract and hash guard; dense legacy code, dynamic dispatch and environment fragility |
| Maintainability | 7.5 | Existing imports protected and new tooling documented; pool binding and duplicated historical entry points persist |

**Strengths:** five-budget locked evidence, population-SD clarity, explicit source
state reuse, honest spatial tradeoffs, exact artifact provenance and safe packaging.

**Major review questions:** Are transductive target access and the extra 800 research
labels allowed? Does a pool-bound source prior satisfy the required Madrid artifact?
Which explanation limit governs? Can another member run the notebook in a clean,
trusted environment after authorization? Is there independent organizer validation?

**Recommendation:** review the prepared distribution, but withhold unconditional
submission approval. Better-looking documentation cannot resolve protocol rights,
scientific independence or a clipped frozen slide. Do not replace Coordinate-RF or
rerun model selection to answer these questions.
''')
    put('COMMIT_CHECKLIST.md', '''# Commit checklist — no commit performed

## Preservation and scope
- [x] Saved initial Git HEAD and dirty status without staging/reverting user changes.
- [x] Existing model, predictions, results, frozen hashes and scientific code unchanged.
- [x] Existing root README and requirements preserved; professional alternatives added.
- [x] New notebook has path-only derivation; original outputs and metadata preserved.
- [x] Old drafts/evidence retained; this pass's failed artifacts archived.
- [ ] Investigate active OneNote metadata changes; do not silently restore or stage them.

## Review before staging
- [ ] Run `git diff --check` and inspect pre-existing warnings separately.
- [ ] Stage only explicitly reviewed new guides/scripts/manifests, never `git add .`.
- [ ] Review large model/PDF/PPTX/NPZ distribution artifacts for release storage or LFS;
      the requested final package intentionally duplicates only necessary deliverables.
- [ ] Keep environments, raw data, caches, generated OneNote files, replay outputs and
      historical safety ZIPs out of ordinary Git history without deleting local evidence.
- [ ] Do not stage `archive/` wholesale; it contains preserved package binaries.
- [ ] Review new documentation and audit receipts for identifying local-path details.
- [ ] Obtain rights-holder licensing and organizer data-sharing approval.
- [ ] Have another member verify checksums and review the exact final upload allowlist.
- [ ] Confirm HEAD/tag aligns with approved release; current repository is already dirty.

Suggested logical commit (pending approval):
`docs: add preservation-first judge package and static audit guides`

The root `.gitignore` is frozen; it was not rewritten. Use explicit staging or a
separately authorized Git policy change. No automatic commit, tag or broad cleanup.
''')
    put('FINAL_PRE_FLIGHT.md', '''# Final pre-flight — conditional, not ready for unconditional upload

## Requested phases and disposition
| Phase | Status | Evidence / restriction |
|---|---|---|
| 1 Audit | Complete | REPOSITORY_AUDIT.md and full inventory |
| 2 Structure | Additive complete | Existing imports retained; new judge/documentation layer |
| 3 README | Preservation-safe alternative | Frozen root README kept; professional new package README and companion |
| 4 Documentation | Complete | Method, pipeline, reproducibility, limitations, FAQ, addenda |
| 5 Diagrams | Complete | Four new SVG/PNG pairs, non-scientific schematics |
| 6 Deliverables | Reviewed; blockers recorded | Structural checks, PDF rendering, no model execution |
| 7 Judge review | Complete | JUDGE_REVIEW.md, subjective scores and deductions |
| 8 Code cleanup | Safe scope complete | New documented tooling/wrapper only; no frozen code formatting |
| 9 Archive | Preservation-safe complete | Original evidence left in place; snapshots and new drafts archived |
| 10 Minimal package | Created | FINAL_SUBMISSION, allowlist and checksums; monitor index sidecars |
| 11 Consistency | Scoped checks complete | Five-budget metric tokens/arrays/tables; slide clipping remains |
| 12 Git readiness | Checklist prepared, commit pending | Dirty user state preserved; no staging |
| 13 Executive summary | Complete | PROJECT_EXECUTIVE_SUMMARY.md |

## Passed within scope
- [x] Coordinate-RF retained; no training, optimization or prediction replay.
- [x] All existing non-OneNote files and every frozen root-manifest entry unchanged.
- [x] All five budget results and SDs match selected deliverables at displayed precision.
- [x] 4,000 saved confusion matrices agree with recorded F1; summary/table arithmetic agrees.
- [x] Package copies, manifest, checksums, NPZ schemas and notebook schema/syntax verified.
- [x] Current PDF freshly renders all 16 pages; visual clipping detected, not hidden.
- [x] Final documentation and traceable archival records prepared.

## Blocking gates — cannot be completed without authorization/decisions
- [ ] Organizer: approve full-pool target features, coordinates and extra development supervision.
- [ ] Organizer: confirm official explanation limit (original is 340 words), upload format,
      deadline and whether a reusable source model rather than a cached prior is required.
- [ ] Rights holder: approve code license and artifact/data redistribution terms.
- [ ] Presentation owner: authorize a derived layout-only repair of slide 11 and new PDF
      export; do not change the locked originals or scientific plot data.
- [ ] Runtime owner: resolve nbformat's resource-import failure in a separate clean
      environment; independently reload/replay only when support-model fitting is allowed.
- [ ] Workspace owner: stop background OneNote indexing and recheck the upload folder;
      two original index files changed during audit and newly generated sidecars appeared.
- [ ] Team: perform final PowerPoint-app/offline review and four-person timed rehearsal.
- [ ] Team: approve explicit staging and a release commit/tag after reviewing user changes.

## Final safe checks
```bash
python -B scripts/validate_repository_polish.py --out NEW_FINAL_CHECK_DIRECTORY
cd FINAL_SUBMISSION
sha256sum -c checksums.sha256
```
The validator intentionally returns nonzero for real preservation/layout failures;
do not weaken checks to manufacture a green result. A hash match is not a license,
scientific eligibility decision, model safety guarantee or clean-runtime certificate.
''')
    put('FINAL_CONSISTENCY_AUDIT.md', '''# Final consistency audit

| Relationship | Evidence | Verdict |
|---|---|---|
| New README → slides | Five macro-F1 means and population SDs, six displayed decimals | PASS |
| Slides → report | Same selected model, locked five-budget tokens and spatial limitations | PASS within extracted text |
| Report → notebook | Same locked results and explanation; notebook metadata/outputs preserved | PASS within audited fields |
| Notebook → inference | Same hash-locked implementation/configuration; resolved package paths | Static PASS; execution prohibited |
| Results → tables | 4,000 saved confusion-matrix calculations and 20 method/budget summaries | PASS at absolute tolerance 1e-12 |
| Tables → figures | Existing figure identities retained, embedded PNG hashes matched; plots visually reviewed | Identity PASS; no full plot-data regeneration |
| Figures → report | Learning-curve values and spatial tradeoff consistent; no new scientific graphs | Scoped PASS; slide 11 clips the plot bottom |
| Naming | Coordinate-RF prose; Coordinate_RF immutable machine identifier | Alias documented, not renamed |
| Historical numbers | Old experiments retain old metrics and scopes | Preserved, not falsely called stale-free |
| References | New explicit local Markdown file links checked; historical vendor warning retained | Scoped, not all URLs/anchors/prose |
| Screenshots | Final PDF rendered freshly and all-page contact sheets inspected | Not stale screenshots; clipping remains |

Historical slide/report statements about clean replay/source refit are inherited
claims with original receipts. They are not claims of new execution in this pass.
No notebook cell ran. No scientific prediction, CSV, configuration, hash or result
was changed. Original OneNote metadata is the only detected before/after exception.

See DELIVERABLE_VALIDATION.md and the final machine-readable receipt. “Identical
macro F1 everywhere” means the same method/budget/protocol at the same precision,
not forcing different baselines or historical protocols to share one number.
''')
    put('FINAL_REPOSITORY_REPORT.md', '''# Final repository report

## Executive decision
**Prepared for judge review; not certified for immediate unconditional submission.**
The no-overwrite and frozen-evidence rules were prioritized over cosmetic changes.
Coordinate-RF, all scientific artifacts, prediction CSVs and frozen hashes remain
unchanged. No source training, support RF fitting, optimization or inference replay.

## Editorial scores /100
| Dimension | Score |
|---|---:|
| Repository | 82 |
| Submission readiness | 68 |
| Documentation | 90 |
| Code quality | 72 |
| Research quality | 75 |
| Professionalism | 82 |
| Judge friendliness | 84 |
| Reproducibility | 72 |

These are qualitative reviewer estimates, not official competition scores or
empirical software benchmarks. Deductions reflect unresolved eligibility/rights,
runtime environment failure, clipped slide, no clean execution and historical
complexity; documentation cannot erase those constraints.

## Files changed
- No pre-existing scientific file, root README, requirement file, model code,
  prediction, submission artifact, protected hash or evidence record was edited.
- Before/after inventory detected changes to root `Open Notebook.onetoc2` and
  `archive/Open Notebook.onetoc2`; no audit command wrote them. Background indexing
  is suspected. They were not reverted, deleted or concealed.
- Only newly introduced audit/build/validation code was corrected during this pass.
  The derived notebook changes dependency paths only; all saved outputs remain exact.

## Files archived
- Byte-identical README, legacy requirements and master-plan snapshots under
  `archive/repository_polish/snapshots/`; originals remain in place.
- The first new package at `archive/repository_polish/package_draft_01/`, before
  correcting UTF-8 handling and excluding generated OneNote sidecars.
- First schematic exports at `archive/repository_polish/diagram_draft_01/`.
- No old scientific experiment, organizer original, prediction or evidence moved.
  Existing archive folders and safety snapshots were retained.

## Files created
- Requested top-level audit, validation, judge review, commit/pre-flight, executive
  summary and final-report documents, plus FINAL_CONSISTENCY_AUDIT.md.
- `docs/README_SUBMISSION.md`, METHOD.md, PIPELINE.md, REPRODUCIBILITY.md,
  LIMITATIONS.md, FAQ.md, LICENSE_STATUS.md and preservation/validation addenda.
- `deliverables/README.md`; four SVG/PNG schematic pairs under
  `figures/repository_polish/`.
- `FINAL_SUBMISSION/`: professional README, unchanged PPTX/PDF/explanation,
  path-only notebook derivative, requirements, wrapper, frozen model and notebook
  dependencies, results summary, provenance manifest and checksums. No raw datasets,
  experiments, caches or development logs belong in the sealed package.
- Audit/build/validation/report scripts under `scripts/`; baseline, inventory,
  interrupted-attempt evidence, PDF renders and validation receipts under
  `reproducibility/repository_polish/`.

The exact new-file index is `reproducibility/repository_polish/final_file_index.json`.
Per-copy provenance is in build_receipt_02.json and FINAL_SUBMISSION/manifest.json.
Package drafts and necessary distribution copies are intentional duplication;
this task does not claim the entire historical research tree is deduplicated.

## Verification
- Original non-OneNote files and frozen root manifest: unchanged, zero mismatches.
- Saved F1 arithmetic: all 4,000 confusion records and corresponding summaries pass.
- Five-budget tables, slide/report/notebook/new-guide values agree.
- New package manifest/checksum membership and canonical copies pass.
- Full notebook v4.5 schema and AST/dependencies pass without executing cells.
- Five reference NPZ schemas and support/query separation pass without model fitting.
- PPTX/XML/images parse; 16-page PDF freshly renders. Slide 11 clipping is confirmed.
- All six requirement pins match installed metadata; nbformat import still fails.
- New local Markdown targets receive a final link sweep; one historical vendored
  license-document link remains outside the judge package.

Final measured results: `reproducibility/repository_polish/validation_final/validation.json`.
The validator must remain nonzero for genuine slide-bounds and original-index
preservation failures. Full nbformat import is separately BLOCKED despite successful
schema validation. No success claim relies on an unexecuted model test.

## Remaining issues and final recommendation
1. Obtain organizer approval of transductive access, coordinates and development labels.
2. Confirm 300/500-word limit, upload/interface rules and required source-model export.
3. Resolve license and redistribution rights without inventing permission.
4. Authorize a separate presentation-layout revision; slide 11 is visibly clipped.
5. Resolve environment import contamination and authorize independent support fitting
   before clean-runtime certification; no retraining is undertaken here.
6. Stop background index generation, verify the final folder again and review Git
   changes explicitly. No automatic commit, staging, tag or process termination.

Use PROJECT_EXECUTIVE_SUMMARY.md for the five-minute judge tour and FINAL_PRE_FLIGHT.md
for the release gates. The repository-only pass is complete within the safe scope;
claiming immediate competition readiness while these gates remain would be false.
''')
    put('reproducibility/repository_polish/validation_attempt_01/INTERRUPTION.md', '''# Preserved interruption
The first validator attempt stopped at nbformat import: UnicodeDecodeError in
jsonschema_specifications._schemas reading a non-UTF-8 resource. No model loaded.
The environment was not modified. Subsequent receipts record the import as BLOCKED
and validate the notebook using the exact installed v4.5 schema via fastjsonschema.
''')
    put('reproducibility/repository_polish/validation_attempt_02/INTERRUPTION.md', '''# Preserved interruption
The second validator attempt stopped on a cp1252 decoding error while reading the
new UTF-8 notebook. The new validator was corrected to request UTF-8 explicitly.
No original scientific file or environment was modified. Later checks exposed a
similar build-time derivative issue; the full first package was archived before
rebuilding from the original notebook using UTF-8.
''')
    print('Review reports created exclusively; no scientific edits.')


if __name__ == '__main__':
    main()
