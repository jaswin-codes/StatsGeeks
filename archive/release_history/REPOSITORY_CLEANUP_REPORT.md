# Repository Cleanup Report

## Actions completed

- Removed all discovered `__pycache__` directories and `.pyc` cache files outside the ignored baseline virtual environment.
- Confirmed `FINAL_SUBMISSION/` contains no OneNote sidecars, cache files, logs, editor backups or temporary exports.
- Replaced four stale active documentation files with Coordinate-RF-aligned narratives.
- Removed the temporary visual-audit contact sheet after inspection.

## Files archived

None in this pass. Existing `archive/` content was left intact. Moving or deleting research runs, historical logs, duplicate prediction evidence, safety snapshots or old package exports could invalidate paths/hashes or destroy provenance; safety took precedence over cosmetic cleanup.

## Retained clutter and rationale

- Historical OneNote sidecars exist outside `FINAL_SUBMISSION/`; they are ignored by `.gitignore`, and several pre-existing tracked sidecars are already modified. Human Git cleanup is still needed.
- Historical logs and `.pre_*` files under `working/` are scientific/protocol evidence, not disposable application logs.
- `candidate/final_submission.zip`, `candidate/SUBMISSION_SAFETY_SNAPSHOT.zip` and other large exports remain because their archival/protection status cannot be safely changed in a no-evidence-modification pass.
- Legacy `presentation/`, `working/`, `original/`, `submission/` and experiment trees remain for provenance and are excluded from the judge package.
- `.venv_baseline/` remains locally present but Git-ignored.

## Result

The judge package is clean. The full research repository is not minimal and the working tree is not clean; indiscriminate deletion would be unsafe. Use an explicit human-reviewed Git allowlist rather than bulk staging.
