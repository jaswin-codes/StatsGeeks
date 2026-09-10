# Judge Walkthrough

## Ten-minute route

1. **0:00–1:00 — repository root:** read `PROJECT_EXECUTIVE_SUMMARY.md` for task, method, locked score and caveats.
2. **1:00–2:00 — package guide:** open `FINAL_SUBMISSION/README.md`; confirm Coordinate-RF, transductive scope and package map.
3. **2:00–6:00 — presentation:** use slides 1–2, 5–9 and 12–14. Treat slides 15–16 as appendix.
4. **6:00–8:00 — notebook:** inspect `solution_notebook.ipynb` for path setup, support-only adaptation, prediction replay and confusion-matrix arithmetic.
5. **8:00–9:00 — evidence:** open `results_summary/README.md`, `learning_curve.csv` and `leaderboard.csv`.
6. **9:00–10:00 — integrity:** run `sha256sum -c checksums.sha256` from the package directory; read limitations before judging generalization.

## What is clear

- Coordinate-RF is unambiguously the locked model.
- The 0.749299 ± 0.005716 headline is easy to find and consistently qualified.
- The transfer mechanism, support/query boundary and coordinate use are explained.
- Negative results and spatial limitations are not hidden.
- The package README clearly warns that runtime commands fit support RFs.

## Friction for a first-time reviewer

- The root research tree is large, with many historical experiments, reports and duplicate exports. A judge should stay in `FINAL_SUBMISSION/`.
- The authoritative deck has 16 slides despite an 8–10-slide preference; two dense appendix slides reproduce the explanation.
- `Coordinate_RF` (machine ID) and Coordinate-RF (display name) may look different until the README explains them.
- The model filename `agf_model.py` reflects ancestry while the selected configuration is Coordinate-RF; the lock file is authoritative.
- Official eligibility, word limit, filenames and package-category rules are still unknown.
- Raw-data training cannot be reproduced from the minimal package alone.

## Documentation improvements applied

`docs/PROJECT_SUMMARY.md`, `docs/WRITTEN_JUSTIFICATION.md`, `docs/PRESENTATION_OUTLINE.md` and `docs/SUBMISSION_INVENTORY.md` now identify Coordinate-RF and the locked five-budget evidence. They explicitly direct judges to the minimal package and distinguish historical experiments from the final model.

## Judge recommendation

Review the package rather than the entire research tree. Scientifically, reward the transparent controls and limitations. Administratively, withhold acceptance until organizer eligibility and presentation constraints are confirmed.
