# StatsGeeks final solution — Coordinate-RF

Selected incumbent: **0.749299 ± 0.005716 macro-F1 at 200 shots/class** (200 existing locked episodes; population SD). No claim of a new overnight or independent organizer test. 0.80 was not reached on the locked audit.

Open notebook/FINAL_NOTEBOOK.ipynb. It executes pool-bound inference, support/query separation, saved-prediction replay and macro-F1 arithmetic. The trusted local pickle and feature schema are included. Raw organizer data are NOT included; a new-pool source refit needs the 60-column source-standardized Madrid and Amsterdam feature matrices, source labels, their ordered lattice coordinates, and Madrid scaler mean/scale. Read reports/METHODS.md before presenting.

Python dependencies are model/requirements-repro.txt; notebook additionally uses nbformat, numpy and pandas. Install matching pinned inference versions in your environment. Only load trusted pickle artifacts.

Inference from package root:
```
python -I -B code/final_inference.py --support support.npz --out NEW_OUTPUT
python -I -B code/final_inference.py --verify --out NEW_REPLAY
```
Support NPZ: indices (unique pool integer indices), labels (1..4), budget (integer: 5/25/50/100/200); optional disjoint query indices. Exactly budget labels per class. Output probabilities and predicted classes. Pool order must not change. No query labels are accepted.

The presentation contains the <=500-word explanation. Tables and figures are existing locked audit evidence, not development results; the separate overnight_development_leaderboard is explicitly exploratory.

**Competition readiness remains conditional:** organizers must allow full-unlabelled-target access, coordinates and additional research-development supervision. No independent organizer-held-out validation. Consult evidence/PREFLIGHT.json for actual software checks; opening a file structurally is not the same as rendering it. The immutable safety snapshot remains separate and unchanged.
