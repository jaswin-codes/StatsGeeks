# Spatial robustness

Grid keys are rounded UTM/30m (organiser Notebook2 section2.3). Fixed median east/west split with 10-key (~300m) query exclusion; alternating support side. Query regions differ from random evaluation, so protocol drops combine region shift, class composition and geographic separation. No buffer tuning. Two regions only, not general spatial CV.

| Method | Shots | Random F1 | Spatial F1 | Spatial minus random | Spatial gain vs EXP010 |
|---|---:|---:|---:|---:|---:|
| EXP010 | 5 | 0.552428 | 0.533387 | -0.019041 | +0.000000 |
| alpha_0.50 | 5 | 0.542596 | 0.517747 | -0.024850 | -0.015641 |
| euclidean | 5 | 0.523169 | 0.485336 | -0.037834 | -0.048052 |
| diagonal | 5 | 0.538866 | 0.482127 | -0.056739 | -0.051260 |
| regularized | 5 | 0.552745 | 0.507618 | -0.045127 | -0.025769 |
| EXP010 | 25 | 0.612174 | 0.584138 | -0.028036 | +0.000000 |
| alpha_0.50 | 25 | 0.614121 | 0.603008 | -0.011112 | +0.018871 |
| euclidean | 25 | 0.612174 | 0.584138 | -0.028036 | +0.000000 |
| diagonal | 25 | 0.617635 | 0.590307 | -0.027328 | +0.006169 |
| regularized | 25 | 0.638010 | 0.613639 | -0.024371 | +0.029501 |
| EXP010 | 50 | 0.617273 | 0.614244 | -0.003029 | +0.000000 |
| alpha_0.50 | 50 | 0.614479 | 0.612943 | -0.001535 | -0.001300 |
| euclidean | 50 | 0.617273 | 0.614244 | -0.003029 | +0.000000 |
| diagonal | 50 | 0.623267 | 0.607392 | -0.015876 | -0.006852 |
| regularized | 50 | 0.649538 | 0.629634 | -0.019904 | +0.015390 |
| EXP010 | 100 | 0.619513 | 0.616810 | -0.002703 | +0.000000 |
| alpha_0.50 | 100 | 0.615650 | 0.613629 | -0.002021 | -0.003180 |
| euclidean | 100 | 0.619513 | 0.616810 | -0.002703 | +0.000000 |
| diagonal | 100 | 0.621612 | 0.616246 | -0.005366 | -0.000564 |
| regularized | 100 | 0.653269 | 0.635870 | -0.017399 | +0.019061 |
| EXP010 | 200 | 0.623982 | 0.617758 | -0.006224 | +0.000000 |
| alpha_0.50 | 200 | 0.619562 | 0.616061 | -0.003501 | -0.001697 |
| euclidean | 200 | 0.623982 | 0.617758 | -0.006224 | +0.000000 |
| diagonal | 200 | 0.625714 | 0.617888 | -0.007826 | +0.000130 |
| regularized | 200 | 0.658664 | 0.636970 | -0.021694 | +0.019212 |
