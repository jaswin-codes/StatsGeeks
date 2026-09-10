# Independence Audit

## Scope and result

Repository-wide text and filename searches covered competitor/team-reference terms and phrases such as “inspired by,” “based on,” “adapted from,” “borrowed,” and “derived from.” Binary scientific artifacts were not deserialized for authorship analysis. **No submission-facing claim says Coordinate-RF was copied, borrowed, adapted from, or based on another team's implementation. No obvious plagiarism indicator was found.**

## Removed references

None. The documentation corrections in this pass removed obsolete EXP-010 final-model positioning, not third-party attribution. Removing text from frozen evidence or resealing deliverables was prohibited.

## Remaining references in `FINAL_SUBMISSION/`

- `README.md`: states that no competitor material was added.
- `written_explanation/written_justification.txt`: states that no competitor code, data or predictions are included.
- `model/provenance.json`: records `competitor_imports: false` and own-data provenance.
- `model/evidence/PREFLIGHT.json` and `results_summary/LOCKED_REPORT.md`: record that a competitor repository was not accessed.

These are independence/provenance declarations, not implementation dependencies or acknowledgements of borrowing. They remain because the files are checksummed and some are protected evidence.

## Historical research references outside the judge package

`candidate/experiments_2h_v2/` contains protected historical files named `competitor_protocol*` and comparison fields. Other research reports describe quarantine/exclusion controls. These are explicitly excluded from `FINAL_SUBMISSION/`, are not imported by the frozen inference wrapper, and were not modified because doing so would alter historical scientific/provenance evidence.

## Dependency audit

`FINAL_SUBMISSION/model/agf_model.py` imports only NumPy, SciPy and scikit-learn. `reproduce_best.py` uses local `agf_model.py` plus standard/pinned dependencies. The inference manifest references only the local implementation, model state and selection lock. No competitor repository path, code, prediction file, figure or notebook is required by the final package.

## Qualification

A text scan cannot prove independent authorship. The evidence supports implementation independence and package isolation, but human code review remains the final plagiarism check.
