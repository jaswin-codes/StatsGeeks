"""Minimal local replacement for sklearn.preprocessing.StandardScaler.

Used only because this Windows environment blocks a SciPy DLL required by
scikit-learn import. Implements the subset needed by Notebook 3.
"""

import numpy as np


class StandardScaler:
    """Minimal StandardScaler supporting fit, transform, and fit_transform."""

    def fit(self, X):
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2:
            raise ValueError("Expected 2D array")
        self.mean_ = np.mean(X, axis=0)
        self.var_ = np.var(X, axis=0)
        self.scale_ = np.sqrt(self.var_)
        self.scale_ = np.where(self.scale_ == 0.0, 1.0, self.scale_)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2:
            raise ValueError("Expected 2D array")
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"X has {X.shape[1]} features, expected {self.n_features_in_}")
        return (X - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)
