# Deferred target-whitening coordinate-basis hypothesis

Our fixed half-identity metric on Madrid-standardized columns is not the competitor's raw-unit, diagonal-shrunk ZCA. ZCA is a particular whitening orientation, and RF axis splits are not rotation-invariant. Consequently changing raw/source-scaled coordinates before ZCA can change a forest even when ideal Mahalanobis distances would be equivalent.

A future small ablation should compare one budget-derived shrinkage rho=d/(d+4*n) toward the target covariance diagonal, once in source-scaled coordinates and once in recovered raw physical units. This is a degrees-of-freedom heuristic, not their target-tuned shrinkage formula. Controls must hold forest/episodes/features/prior/smoothing fixed. Do not assume all CORAL/whitening implementations are equivalent for RF.

Not counted as an executed experiment until results actually exist. Representation/context and source-prior ablations have priority; do not stack untested whitening with them.
