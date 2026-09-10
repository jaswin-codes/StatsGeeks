# Scientific Consistency Report

## Verdict

**PASS for the locked scientific bytes and active final narrative; CONDITIONAL for release.** Coordinate-RF (`Coordinate_RF`) remains selected. No training, optimization, prediction generation or scientific-artifact edit was performed.

## Locked result verification

Arithmetic was recomputed read-only from all 4,000 records and confusion matrices in `FINAL_SUBMISSION/model/evidence/final_complete.json`.

| Labels/class | Mean macro-F1 | Population SD | Episodes | Result |
|---:|---:|---:|---:|---|
| 5 | 0.650253 | 0.011246 | 200 | Match |
| 25 | 0.687664 | 0.012145 | 200 | Match |
| 50 | 0.708436 | 0.011277 | 200 | Match |
| 100 | 0.729839 | 0.008802 | 200 | Match |
| 200 | **0.749299** | **0.005716** | 200 | Match |

Checks performed:

- 4 methods × 5 budgets × 200 episodes = 4,000 records.
- Every saved row-normalized confusion matrix matches its raw confusion matrix.
- Every saved class-F1 vector and macro-F1 matches confusion-matrix arithmetic.
- Every method/budget mean and population SD matches the saved summary.
- `results_summary/learning_curve.csv`, `leaderboard.csv`, `LOCKED_REPORT.md`, package README, notebook outputs, written explanation, PPTX text and PDF text agree on the Coordinate-RF headline.
- The spatial values agree: Coordinate-RF mean/worst 0.694216/0.644816; matched ASTRA 0.696672/0.658183.

## Artifact consistency

- All 31 entries in `FINAL_SUBMISSION/checksums.sha256` pass.
- All 30 manifest-scoped files exist, have the listed size/hash, and there are no extra or missing scoped files.
- Frozen protected files in `model/provenance.json` match: `candidate/exp010_predict.py`, `candidate/artifacts/exp010_stage1_madrid.pkl`, and `data/preprocessed/preprocessed_data.pkl`.
- The inference manifest hashes for `agf_model.py`, `pool_state.pkl`, and `SELECTION_LOCK.json` pass.
- Final PPTX, PDF, written explanation and model are byte-identical to their canonical `candidate/final_submission/` sources.
- Predictions were not regenerated or changed. Existing prediction/reference integrity is supported by unchanged hashes and the sealed preflight receipts.

## Tables, figures and deliverables

The locked report, notebook, README, written explanation, slides and embedded result figures all identify Coordinate-RF. The 16-page PDF has a corresponding 16-slide PPTX and previously rendered 16-page evidence. Existing rendered pages were visually inspected; no visible text clipping was found. One slide-11 image shape extends 0.427 inches beyond the formal slide boundary, although the supplied PDF render appears complete. This is a manual PowerPoint review item, not a scientific discrepancy.

## Documentation synchronization applied

Documentation-only stale EXP-010 positioning was replaced in:

- `docs/PROJECT_SUMMARY.md`
- `docs/WRITTEN_JUSTIFICATION.md`
- `docs/PRESENTATION_OUTLINE.md`
- `docs/SUBMISSION_INVENTORY.md`

Historical experiment logs, archived evidence and frozen package bytes retain historical values by design. Those values are not stale final claims and were not altered.

## Exceptions requiring human review

1. The sealed deck has 16 slides, not the preferred 8–10; slides 15–16 contain the full written explanation.
2. Organizer eligibility for transductive full-pool access, coordinates and the extra 800-label development bank is unconfirmed.
3. The 340-word explanation may exceed a conservative 300-word limit.
4. No independent organizer-held-out result exists.
5. Raw-data end-to-end reconstruction is not self-contained.
