# Final pre-flight — conditional, not ready for unconditional upload

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
