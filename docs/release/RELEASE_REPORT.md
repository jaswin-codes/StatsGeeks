# Final release report

**Coordinate-RF remains selected. Locked macro-F1: 0.749299.**

## PASS — engineering and judge experience

- Root report clutter has been archived; methodology, judge guidance and reproducibility are organized under `docs/`. One current release report replaces overlapping status reports.
- README now explains the problem, data, pipeline, all five budgets, limitations, repository map and safe checks. The judge route starts at `docs/judge/START_HERE.md`.
- A new ten-slide Coordinate-RF companion deck replaces the stale builder in the active presentation workflow. It includes a first-slide abstract, log2-spaced learning curve, spatial limitations, four-speaker notes and slide numbering. Native PowerPoint exported the PDF/PNG views; measured text bounds have no overflow flags.
- The concise written explanation covers all three rubric pillars within the conservative 300-word limit. Original sealed documents remain unchanged.
- No training, tuning, support fitting, prediction regeneration, model deserialization or notebook execution occurred. Nothing was staged, committed or pushed.

## Validation

Run `python -B scripts/validate_release.py`; the machine-readable receipt is `reproducibility/release/validation.json`. The same folder contains the pre-edit hash baseline, per-file KEEP/MOVE/ARCHIVE dispositions, duplicate groups and exact move map. Environments, Git internals and bytecode caches are explicitly outside the scientific inventory.

**34 checks: 31 PASS, 3 WARNING, 0 FAIL.** Scientific/data/model/result bytes and the complete existing submission package pass preservation checks. All 31 entries in the package's shell checksum list also pass independently.

- Inventory: **5,389 files / 6.41 GB**, with **5,322 KEEP, 57 ARCHIVE, 10 MOVE** dispositions; **332 duplicate groups** retained as evidence/backups.
- Root: **eight files**, including Git hygiene configuration; no root audit-report pile. Active documentation: **zero broken inline local links/images** and no flagged wording.
- Scientific consistency: **4,000 frozen confusion/F1 records**, summary arithmetic and all three learning-curve CSV copies agree; five-budget mean/SD values remain unchanged.
- Deliverables: ten PPTX slides, ten PDF pages, valid notebook schema/source paths, unchanged model/pool contract, no out-of-slide shapes or native text overflow. Concise explanation: **235 words**.
- Broader inspection: **2,311 text files**, **23 document/archive containers**, **1,087 text members** and **114 PDFs** scanned. Binary extraction had no errors; protected wording exceptions remain. No nested-archive recursion, OCR, external-URL availability or heading-anchor certification is claimed.
- `git diff --check` passes and the Git index matches the pre-edit snapshot. The staging plan contains **122 explicit paths**, not a bulk directory allowlist.

## WARNING — preservation and submission boundaries

- The existing `FINAL_SUBMISSION/` seal retains the original 16-slide deck and explanation. The new ten-slide deck and concise explanation are outside that seal. Use the companions for live judging; confirm single-archive upload requirements before preparing a presentation-only derivative. Do not silently overwrite sealed files.
- **Warning 1:** Eight non-scientific OneNote navigation sidecars changed bytes during folder reorganization. They remain retained locally; review tracked sidecars separately. No scientific artifact receives this exception.
- **Warning 2:** Thirteen historical/protected inline links remain stale (twelve in a preserved README snapshot; one in a vendored dependency license).
- **Warning 3:** Some historical/protected evidence retains unwanted external-comparison wording and stale links. It was not rewritten or deleted to manufacture an independence claim. Editable judge-facing documentation does not rely on those references. A repository-wide zero-reference guarantee would conflict with preserving frozen provenance/notebooks.
- Frozen research paths and duplicate scientific artifacts stay in place. Large models, raw data, saved predictions and historical experiment outputs are not disposable clutter.
- The root historical `SHA256SUMS.json` is not a new whole-repository release seal. It describes an earlier tree; the unchanged package seal and this release's before/after inventory have distinct scopes.
- Runtime replay, clean installation, portability and organizer-held-out evaluation were not performed or newly certified.

## Remaining manual tasks

1. Confirm organizer eligibility for full unlabelled-target access, coordinates and the additional 800-label development bank; clarify any separate source-model export requirement.
2. Confirm upload filenames/categories and whether presentation companions can be uploaded separately. Rehearse the four-speaker deck on the actual presentation machine.
3. Verify the transferred submission contains the ignored model binary and passes checksums; a Git clone alone may be incomplete.
4. Confirm repository/data redistribution rights; no license grant has been invented.
5. Review the pre-existing dirty working tree, large files and tracked OneNote sidecars. Use the explicit release-only staging allowlist, not bulk staging.

## Git readiness

- **Staging allowlist:** `reproducibility/release/staging_allowlist.txt` lists exact repository paths for review, including old paths for recorded moves. It is a plan, not a staged index.
- **Line-ending protection:** `.gitattributes` disables text conversion for scientific/evidence paths and normalizes only editable release documentation. Do not run `git add --renormalize` on scientific files; verify hashes of any future exported checkout.
- **Exclude from this commit:** data/model binaries, scientific result changes, untouched experiment directories, submission ZIPs, virtual environments, local render PNGs, caches and all unrelated pre-existing modifications. Existing `.gitignore` rules protect most of these; do not add a blanket rule that hides research evidence.
- **Archived:** exact paths in `reproducibility/release/moves.json`; old release reports, team drafts, stale presentation/packaging builders and local sidecars. Sidecars remain local/manual-review items, not ordinary release content.
- **Commit message:** `docs(release): organize judge materials and add frozen-evidence Coordinate-RF deck`
- **Recommended tag:** `v1.0.0-coordinate-rf` after upload/package gates are resolved.
- **Release notes:** “Organized documentation and archived superseded reports; added a ten-slide judge presentation, concise justification and static integrity validator. Coordinate-RF and macro-F1 0.749299 remain unchanged. Existing scientific artifacts and submission seal preserved; runtime reproduction not rerun.”

## Estimated readiness

**Engineering: PASS for the scoped documentation/presentation release. Scientific consistency and static integrity: PASS. Competition upload: WARNING / conditional on organizer and packaging gates.** Repository professionalism and judge navigation are substantially improved; the frozen evidence tree intentionally remains large. No defensible competition rank or numerical readiness percentage is inferred from this audit.

**FAIL: none in completed safe validation.** The requested repository-wide zero-reference condition is not achieved because removing protected provenance wording would violate preservation requirements.
