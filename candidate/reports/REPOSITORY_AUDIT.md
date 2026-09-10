# Repository audit

## Changes made
- Replaced root README; preserved its predecessor under `archive/publication_cleanup/`.
- Added an immutable inference copy, publication scripts, 32 figure sets, tables, slide variants, methods/results and reproducibility bundle.
- No model implementation or original scientific run changed. No optimization executed.
- Archived root scratch diffs and normalized the Windows-reserved `nul` artifact. No experimental evidence deleted.
- Extended .gitignore for environments, bytecode, OneNote/editor files, forensic reintroduction and generated ZIPs; explicitly allowed the 36-MB frozen inference state. Existing tracked user files were not untracked.
- Preserved Git history, index and pre-existing user changes; recorded dirty worktree and pre-publication diff.
- Sidecar catalogs index original configuration, results, logs, metadata and hashes without adding files inside frozen experiments.

## Archived / moved / renamed
- `core_diff.txt` → `archive/publication_cleanup/core_diff.txt`: Scratch output archived; timestamps preserved
- `integration_diff.txt` → `archive/publication_cleanup/integration_diff.txt`: Scratch output archived; timestamps preserved
- `member2_vs_integration.txt` → `archive/publication_cleanup/member2_vs_integration.txt`: Scratch output archived; timestamps preserved
- `nul` → `archive/publication_cleanup/windows_reserved_nul.txt`: Reserved Windows filename normalized using Git Bash
- `candidate/competitor_forensics` → `C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy - excluded_forensics_20260909_201729`: External quarantine, not submission material
- `candidate/publication/submission_bundle.zip (initial verified export)` → `archive/publication_cleanup/exports/submission_bundle_pre_final_audit.zip`: Preserved initial tested export before final documentation/ignore-rule audit; one canonical current ZIP

## Removed files
None permanently deleted. Competitor forensics were moved intact to external quarantine, not copied into the submission.

## Canonicalization
New publication figures have one canonical opaque/vector set in `candidate/figures/publication/`; slide-specific transparent variants are separate derived assets. Historical figure duplicates remain unchanged because they form prior run evidence. Large experimental trees stay in place to avoid invalidating hardcoded paths/hashes; the final export is an allowlist, not a mirror of the research tree.

## Health and remaining warnings
- 35 experiment directories indexed; missing metadata categories are marked in `EXPERIMENT_CATALOG.json`, not fabricated.
- 0 local Markdown link warnings in historical/research documents are inventoried in `candidate/reproducibility/legacy_link_warnings.json`. Active publication links are separately required to pass.
- Own historical competitor-protocol comparisons in `candidate/experiments_2h_v2/` remain protected historical evidence. They depend on quarantined forensic material and are deliberately not runnable or included in the final export. They are not publication evidence.
- Caches, OneNote files, old notebooks, failed logs and manifests are excluded from export, not deleted blindly; provenance dependencies make safe removal uncertain.
- Orphan check is conservative: all generated artifacts are referenced by figure/table/artifact manifests. Legacy unreferenced artifacts and unused manifests are retained because archival provenance is itself a valid use; no claim of complete semantic reference inference.
- No automated scan can prove independent authorship. The export uses reviewed own-source allowlists, inference dependency checks and the existing provenance declaration; no competitor snapshot/code/data/figures/workflows are included.
- Initial staging stopped on the Windows reserved filename `nul`; Git Bash moved it to `windows_reserved_nul.txt`. Staging records were recovered without repeating scientific computation.
- Raw datasets/large artifacts are historically Git-ignored. Local self-contained evidence export does not establish data redistribution rights or complete reproducibility of raw preprocessing.
- A prior full fresh-source replay is preserved. This phase verified ten reference arrays and recalculated all saved metrics, not another expensive full replay.

## Validation scope
Frozen baseline checks, packaged source hashes, 4,000 confusion/F1 reconstructions, 1,000 exclusion checks, required outputs, image formats/DPI, active links and final SHA256 seals are checked. The distribution validator is read-only. Legacy warnings do not become scientific success claims.
