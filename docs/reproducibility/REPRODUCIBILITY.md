# Reproducibility and evidence boundaries

## Safe verification now

Use the current distribution byte check below. The older `scripts/validate_release.py` targets the previous release layout and baseline; it is historical, not the final synchronization verdict. It was not rerun and its receipts were not overwritten. Current static checks are recorded in [final synchronization validation](../../reproducibility/final_sync/validation.json).

For an independent shell checksum check:

```bash
cd FINAL_SUBMISSION
sha256sum -c checksums.sha256
```

Hashes prove byte consistency, not authenticity. Obtain artifacts and checksum references from a trusted source.

## What is and is not reproducible

| Level | Status and boundary |
|---|---|
| Frozen artifact integrity | Before/after SHA-256 verification; model, input, data, notebook and result bytes retained |
| Static package structure | Manifest membership, checksums, ZIP/XML, notebook source syntax, result-table values and documentation paths checked without execution |
| Saved scientific results | Historical outputs and receipts exist; no experiment rerun in release preparation |
| Fixed-reference runtime replay | Historical receipts only; not rerun here; also fits support RFs |
| Fresh raw-data reproduction | Not certified by this release; requires authorized data, preprocessing/source-state provenance and the recorded environment |
| Clean installation / portability | Not verified; Python 3.14.6 on Windows was the observed scientific environment |
| Organizer-held-out evaluation | Not supplied or claimed; competition eligibility remains conditional |

The frozen model is bound to **25,992 ordered Amsterdam rows**. Arbitrary pools are not supported. Query labels are evaluation-only; the separate 800-label development bank is excluded from final queries but remains extra research supervision.

## Installation and runtime workflow — not release checks

Use the [sealed package README](../../FINAL_SUBMISSION/README.md) for support NPZ schema, exact commands and required working directory. `FINAL_SUBMISSION/requirements.txt` pins that package; root `requirements-repro.txt` describes publication inference. Root `requirements.txt` belongs to the older baseline and must not be substituted.

Both `reproduce.py --verify` and `reproduce.py --support` **fit support-set random forests**. Run neither under a no-fitting/no-prediction-regeneration restriction. No packages were installed and no notebook cells executed during this release. A clone alone may omit ignored data/models; verify the actual transferred bundle before use.

## Evidence locations

- [Earlier release baseline and inventory](../../reproducibility/release/): every pre-existing project file except Git internals, environments and bytecode caches.
- [Earlier static validation receipts](../../reproducibility/repository_polish/): historical packaging checks; not proof of current runtime execution.
- [Frozen scientific reproduction guide](../../candidate/reports/REPRODUCIBILITY.md): original seeds, environment and historical commands.
- [Distribution manifest](../../FINAL_SUBMISSION/manifest.json): current package membership. Presentation, justification, logo and README entries alone were refreshed; scientific entries retain their original values.
- [Final synchronization receipt](../../reproducibility/final_sync/validation.json): byte preservation, approved-file copy provenance, PDF text and active-navigation checks.

The approved ten-slide deck and matching PowerPoint PDF are now inside `FINAL_SUBMISSION/`. The old presentation and distribution seal are archived under `archive/presentation_history/pre_final_sync/`. Scientific hash files were neither rewritten nor regenerated. Before/after digest comparisons are read-only integrity verification, not regenerated scientific manifests. Presentation export does not execute model code.
