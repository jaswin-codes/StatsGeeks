# EXP-C

See ../PLAN.md for the predeclared method and information-access boundaries.

Run: `python -I -B candidate/experiments_2h/run.py C`; clean repeat: append `--repeat`.
Existing results are never overwritten. To rerun elsewhere copy the sprint code without generated outputs.

| Budget | Method | Mean | Population SD | Delta vs EXP010 | W/L/T |
|---|---|---:|---:|---:|---|
| 5 | EXP010 | 0.552428 | 0.059539 | +0.000000 | 0/0/10 |
| 5 | joint_control | 0.515220 | 0.070198 | -0.037208 | 3/7/0 |
| 5 | compact_local | 0.523169 | 0.068765 | -0.029259 | 2/8/0 |
| 25 | EXP010 | 0.612174 | 0.013057 | +0.000000 | 0/0/10 |
| 25 | joint_control | 0.608872 | 0.014539 | -0.003302 | 2/8/0 |
| 25 | compact_local | 0.612174 | 0.013057 | +0.000000 | 0/0/10 |
| 50 | EXP010 | 0.617273 | 0.007839 | +0.000000 | 0/0/10 |
| 50 | joint_control | 0.613500 | 0.008332 | -0.003773 | 0/10/0 |
| 50 | compact_local | 0.617273 | 0.007839 | +0.000000 | 0/0/10 |
| 100 | EXP010 | 0.619513 | 0.004770 | +0.000000 | 0/0/10 |
| 100 | joint_control | 0.614502 | 0.004810 | -0.005011 | 0/10/0 |
| 100 | compact_local | 0.619513 | 0.004770 | +0.000000 | 0/0/10 |
| 200 | EXP010 | 0.623982 | 0.003646 | +0.000000 | 0/0/10 |
| 200 | joint_control | 0.618943 | 0.003824 | -0.005040 | 0/10/0 |
| 200 | compact_local | 0.623982 | 0.003646 | +0.000000 | 0/0/10 |
