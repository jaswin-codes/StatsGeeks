# EXP-F

See ../PLAN.md for the predeclared method and information-access boundaries.

Run: `python -I -B candidate/experiments_2h/run.py F`; clean repeat: append `--repeat`.
Existing results are never overwritten. To rerun elsewhere copy the sprint code without generated outputs.

| Budget | Method | Mean | Population SD | Delta vs EXP010 | W/L/T |
|---|---|---:|---:|---:|---|
| 5 | EXP010 | 0.552428 | 0.059539 | +0.000000 | 0/0/10 |
| 5 | euclidean | 0.523169 | 0.068765 | -0.029259 | 2/8/0 |
| 5 | diagonal | 0.538866 | 0.033340 | -0.013562 | 3/7/0 |
| 5 | regularized | 0.552745 | 0.036466 | +0.000317 | 6/4/0 |
| 25 | EXP010 | 0.612174 | 0.013057 | +0.000000 | 0/0/10 |
| 25 | euclidean | 0.612174 | 0.013057 | +0.000000 | 0/0/10 |
| 25 | diagonal | 0.617635 | 0.011268 | +0.005461 | 9/1/0 |
| 25 | regularized | 0.638010 | 0.014197 | +0.025835 | 10/0/0 |
| 50 | EXP010 | 0.617273 | 0.007839 | +0.000000 | 0/0/10 |
| 50 | euclidean | 0.617273 | 0.007839 | +0.000000 | 0/0/10 |
| 50 | diagonal | 0.623267 | 0.010389 | +0.005994 | 9/1/0 |
| 50 | regularized | 0.649538 | 0.009417 | +0.032265 | 10/0/0 |
| 100 | EXP010 | 0.619513 | 0.004770 | +0.000000 | 0/0/10 |
| 100 | euclidean | 0.619513 | 0.004770 | +0.000000 | 0/0/10 |
| 100 | diagonal | 0.621612 | 0.006166 | +0.002099 | 8/2/0 |
| 100 | regularized | 0.653269 | 0.005811 | +0.033757 | 10/0/0 |
| 200 | EXP010 | 0.623982 | 0.003646 | +0.000000 | 0/0/10 |
| 200 | euclidean | 0.623982 | 0.003646 | +0.000000 | 0/0/10 |
| 200 | diagonal | 0.625714 | 0.005272 | +0.001731 | 7/3/0 |
| 200 | regularized | 0.658664 | 0.004417 | +0.034681 | 10/0/0 |
