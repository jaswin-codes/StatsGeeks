"""Minimal downstream artifact helpers for Notebook 4 / candidate modelling.

These helpers do not change baseline algorithms. They only standardise validation and
saving of models, metrics, episode metadata, and figures once Member 2's
preprocessed_data.pkl exists.
"""

from __future__ import annotations

import csv
import hashlib
import json
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

REQUIRED_PREPROCESSED_KEYS = (
    "X_madrid",
    "y_madrid",
    "X_amsterdam",
    "y_amsterdam",
    "feature_names",
    "scaler",
    "pixel_ids_madrid",
    "pixel_ids_amsterdam",
    "feat_groups",
)

EXPECTED_CLASSES = np.array([1, 2, 3, 4])


def ensure_dir(path: str | Path) -> Path:
    """Create and return an artifact directory."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_sha256(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Return SHA256 checksum for an artifact or input file."""
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_timestamp() -> str:
    """Filesystem-safe UTC timestamp."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_pickle(path: str | Path) -> Any:
    with Path(path).open("rb") as f:
        return pickle.load(f)


def save_pickle(obj: Any, path: str | Path) -> Path:
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    return path


def save_json(data: Mapping[str, Any], path: str | Path) -> Path:
    """Save JSON metadata/metrics, converting NumPy scalars/arrays safely."""
    def default(obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.generic):
            return obj.item()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serialisable")

    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, default=default)
        f.write("\n")
    return path


def append_metrics_csv(row: Mapping[str, Any], path: str | Path) -> Path:
    """Append one flat metric/config row to CSV, writing a header if needed."""
    path = Path(path)
    ensure_dir(path.parent)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)
    return path


def save_figure(fig: Any, path: str | Path, *, dpi: int = 150) -> Path:
    """Save a matplotlib figure with consistent bbox handling."""
    path = Path(path)
    ensure_dir(path.parent)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def validate_preprocessed_data(
    data: Mapping[str, Any],
    *,
    expected_n_features: int = 60,
    expected_madrid_rows: int | None = 76263,
    expected_amsterdam_rows: int | None = 25992,
) -> dict[str, Any]:
    """Validate Notebook 4's expected pickle contract without fitting anything."""
    missing = [k for k in REQUIRED_PREPROCESSED_KEYS if k not in data]
    if missing:
        raise ValueError(f"Missing required preprocessed_data keys: {missing}")

    X_mad = np.asarray(data["X_madrid"])
    y_mad = np.asarray(data["y_madrid"])
    X_ams = np.asarray(data["X_amsterdam"])
    y_ams = np.asarray(data["y_amsterdam"])
    pid_mad = np.asarray(data["pixel_ids_madrid"])
    pid_ams = np.asarray(data["pixel_ids_amsterdam"])
    feature_names = list(data["feature_names"])

    checks = {
        "X_madrid_shape": tuple(X_mad.shape),
        "X_amsterdam_shape": tuple(X_ams.shape),
        "y_madrid_shape": tuple(y_mad.shape),
        "y_amsterdam_shape": tuple(y_ams.shape),
        "pixel_ids_madrid_shape": tuple(pid_mad.shape),
        "pixel_ids_amsterdam_shape": tuple(pid_ams.shape),
        "n_feature_names": len(feature_names),
        "madrid_classes": sorted(np.unique(y_mad).tolist()),
        "amsterdam_classes": sorted(np.unique(y_ams).tolist()),
        "X_madrid_all_finite": bool(np.isfinite(X_mad).all()),
        "X_amsterdam_all_finite": bool(np.isfinite(X_ams).all()),
        "feature_names_unique": len(feature_names) == len(set(feature_names)),
    }

    errors: list[str] = []
    if X_mad.ndim != 2 or X_ams.ndim != 2:
        errors.append("X_madrid and X_amsterdam must be 2D arrays")
    if X_mad.shape[1] != expected_n_features or X_ams.shape[1] != expected_n_features:
        errors.append(f"Expected {expected_n_features} features for both cities")
    if len(feature_names) != expected_n_features:
        errors.append(f"Expected {expected_n_features} ordered feature names")
    if expected_madrid_rows is not None and X_mad.shape[0] != expected_madrid_rows:
        errors.append(f"Expected Madrid rows {expected_madrid_rows}, got {X_mad.shape[0]}")
    if expected_amsterdam_rows is not None and X_ams.shape[0] != expected_amsterdam_rows:
        errors.append(f"Expected Amsterdam rows {expected_amsterdam_rows}, got {X_ams.shape[0]}")
    if y_mad.shape[0] != X_mad.shape[0] or y_ams.shape[0] != X_ams.shape[0]:
        errors.append("Label vector lengths must match feature row counts")
    if pid_mad.shape != (X_mad.shape[0], 2) or pid_ams.shape != (X_ams.shape[0], 2):
        errors.append("Pixel ID arrays must be (n_rows, 2) and aligned to X rows")
    if not np.array_equal(np.unique(y_mad), EXPECTED_CLASSES):
        errors.append("Madrid labels must contain exactly classes 1,2,3,4")
    if not np.array_equal(np.unique(y_ams), EXPECTED_CLASSES):
        errors.append("Amsterdam labels must contain exactly classes 1,2,3,4")
    if not checks["X_madrid_all_finite"] or not checks["X_amsterdam_all_finite"]:
        errors.append("Feature matrices must contain only finite values")
    if not checks["feature_names_unique"]:
        errors.append("Feature names must be unique and ordered")

    checks["ok"] = not errors
    checks["errors"] = errors
    if errors:
        raise ValueError("Preprocessed data validation failed: " + "; ".join(errors))
    return checks


def build_source_model_bundle(
    *,
    model: Any,
    feature_names: Sequence[str],
    config: Mapping[str, Any],
    metrics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Package a fitted source model with schema/config metadata for reload tests."""
    return {
        "model": model,
        "feature_names": list(feature_names),
        "config": dict(config),
        "metrics": dict(metrics or {}),
        "created_utc": utc_timestamp(),
        "artifact_type": "source_model_bundle",
    }


def assert_support_query_disjoint(support_idx: Sequence[int], query_idx: Sequence[int]) -> None:
    """Fail fast if any Amsterdam support pixel is also in the query set."""
    overlap = set(map(int, support_idx)).intersection(map(int, query_idx))
    if overlap:
        raise ValueError(f"Support/query overlap detected: {len(overlap)} shared indices")
