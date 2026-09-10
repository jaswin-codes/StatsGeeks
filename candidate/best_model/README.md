# Frozen Coordinate_RF inference bundle

Byte-identical implementation, source-prior pool state, configuration and development lock from `candidate/autonomous_runs/20260909_1727`. This is the only current model package; prior packages remain historical.

Run from repository root: `python -I -B reproduce_best.py --verify --out replay_new`. See [reproduction guide](../reports/REPRODUCIBILITY.md). Support inputs must preserve original pool row order. Full target features/coordinates are used, but no query truth or development-label bank is included here. Reference inputs contain designated support labels and expected predictions only.
