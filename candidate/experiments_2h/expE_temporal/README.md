# EXP-E

See ../PLAN.md for the predeclared method and information-access boundaries.

Run: `python -I -B candidate/experiments_2h/run.py E`; clean repeat: append `--repeat`.
Existing results are never overwritten. To rerun elsewhere copy the sprint code without generated outputs.

| Budget | Method | Mean | Population SD | Delta vs EXP010 | W/L/T |
|---|---|---:|---:|---:|---|
| 5 | EXP010 | 0.552428 | 0.059539 | +0.000000 | 0/0/10 |
| 5 | temporal3 | 0.560998 | 0.061231 | +0.008570 | 9/1/0 |
| 25 | EXP010 | 0.612174 | 0.013057 | +0.000000 | 0/0/10 |
| 25 | temporal3 | 0.613456 | 0.013229 | +0.001282 | 8/2/0 |
| 200 | EXP010 | 0.623982 | 0.003646 | +0.000000 | 0/0/10 |
| 200 | temporal3 | 0.625755 | 0.003445 | +0.001773 | 10/0/0 |
