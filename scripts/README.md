# Scripts

## Final synchronization

Use `cd FINAL_SUBMISSION` then `sha256sum -c checksums.sha256` for the current package. See the [final synchronization report](../docs/release/FINAL_SYNC_REPORT.md). Existing release scripts below target historical layouts/baselines; do not rerun migration/build scripts or overwrite historical receipts to certify this approved revision. No script implementation was changed.

## Historical static release validation

```bash
python -B scripts/validate_release.py
```

Standard-library core; optional installed notebook schema validation and PDF text extraction are reported separately. Checks byte preservation, frozen package seals, saved confusion/F1 arithmetic, documentation links, notebook source syntax, slide bounds and the locked Coordinate-RF score. No model imports, fitting or prediction generation.

`organize_release.py` is the one-time documentation migration used for this release. It refuses existing destinations and is not part of reproduction; do not rerun it on an organized tree.

## Presentation tooling

See [presentation/README.md](../presentation/README.md) for the approved final deck. The ten-slide builder and export script retained here describe an earlier companion and must not rebuild the current human-reviewed deck. Earlier release generators and validators were moved to `archive/release_history/scripts/`: their path assumptions and readiness checks are historical.

## Historical research utilities

`determinism_check.py`, `extract_results.py` and `validate_pickle.py` retain their original behaviour. Their names do not imply that execution is permitted under a no-fitting/no-deserialization release audit. Inspect their source before any later authorized research use; they were not run during release preparation.
