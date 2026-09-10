"""Artifact-consuming prediction interface for the frozen EXP-010 method.

This module performs no model fitting, episode sampling, tuning, or scoring. Input
matrices must already follow the 60-feature, Madrid-fitted preprocessing contract
recorded in the Stage 1 artifact. Query labels are neither accepted nor loaded.
"""
from __future__ import annotations

import argparse
import pickle
from pathlib import Path
from typing import Any

import numpy as np

SUPPORTED_SCHEDULE = {
    5: (30, 0.6),
    25: (45, 0.0),
    50: (45, 0.0),
    100: (45, 0.0),
    200: (45, 0.0),
}
REQUIRED_KEYS = {
    "format", "experiment", "trained_on", "classes", "feature_names",
    "feature_importances", "metric_weights", "schedule", "representations",
    "source_artifact_sha256", "source_data_sha256",
}


def _schedule_from_artifact(stage1: dict[str, Any]) -> dict[int, tuple[int, float]]:
    try:
        return {
            int(budget): (int(config["k"]), float(config["lambda"]))
            for budget, config in stage1["schedule"].items()
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid EXP-010 schedule in Stage 1 artifact") from exc


def validate_stage1_artifact(stage1: Any) -> dict[str, Any]:
    """Validate and return an EXP-010 Stage 1 artifact loaded in memory."""
    if not isinstance(stage1, dict):
        raise TypeError("Stage 1 artifact must be a dictionary")
    missing = REQUIRED_KEYS - stage1.keys()
    if missing:
        raise ValueError(f"Stage 1 artifact is missing keys: {sorted(missing)}")
    if stage1["format"] != "statsgeeks.exp010.stage1.v1":
        raise ValueError(f"Unsupported artifact format: {stage1['format']!r}")
    if stage1["experiment"] != "EXP-010" or stage1["trained_on"] != "madrid_only":
        raise ValueError("Artifact is not the frozen Madrid-only EXP-010 state")

    classes = np.asarray(stage1["classes"])
    names = list(stage1["feature_names"])
    weights = np.asarray(stage1["metric_weights"], dtype=float)
    importances = np.asarray(stage1["feature_importances"], dtype=float)
    if classes.tolist() != [1, 2, 3, 4]:
        raise ValueError(f"Expected classes [1, 2, 3, 4], got {classes.tolist()}")
    if len(names) != 60 or len(set(names)) != 60:
        raise ValueError("Artifact must contain 60 unique, ordered feature names")
    if weights.shape != (60,) or importances.shape != (60,):
        raise ValueError("Artifact weights/importances must each have shape (60,)")
    if not np.isfinite(weights).all() or not np.isfinite(importances).all():
        raise ValueError("Artifact weights/importances contain non-finite values")
    if not np.array_equal(weights, np.sqrt(importances)):
        raise ValueError("Artifact metric weights do not equal sqrt(feature importances)")
    if _schedule_from_artifact(stage1) != SUPPORTED_SCHEDULE:
        raise ValueError("Artifact schedule does not equal the frozen EXP-010 schedule")

    rank = np.argsort(importances)[::-1]
    for k in (30, 45):
        try:
            rep = stage1["representations"][str(k)]
            selected = np.asarray(rep["selected_feature_idx"])
            offsets = np.asarray(rep["madrid_class_offsets"], dtype=float)
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Artifact is missing the k={k} representation") from exc
        if not np.array_equal(selected, np.sort(rank[:k])):
            raise ValueError(f"Stored k={k} feature indices do not match Madrid ranking")
        if offsets.shape != (4, k) or not np.isfinite(offsets).all():
            raise ValueError(f"Madrid class offsets must have finite shape (4, {k})")
    return stage1


def load_stage1_artifact(path: str | Path) -> dict[str, Any]:
    """Load and validate the frozen Madrid Stage 1 state."""
    with Path(path).open("rb") as handle:
        return validate_stage1_artifact(pickle.load(handle))


def _feature_matrix(name: str, value: Any, width: int) -> np.ndarray:
    matrix = np.asarray(value)
    if matrix.ndim != 2 or matrix.shape[1] != width:
        raise ValueError(f"{name} must have shape (n_rows, {width}); got {matrix.shape}")
    if matrix.shape[0] == 0:
        raise ValueError(f"{name} must contain at least one row")
    if not np.issubdtype(matrix.dtype, np.number):
        raise TypeError(f"{name} must be numeric")
    matrix = np.asarray(matrix, dtype=float)
    if not np.isfinite(matrix).all():
        raise ValueError(f"{name} contains NaN or infinity")
    return matrix


def adapt_and_predict(
    stage1: dict[str, Any],
    support_X: Any,
    support_y: Any,
    query_X: Any,
    n_shots_per_class: int,
    seed: int,
) -> np.ndarray:
    """Apply the exact frozen EXP-010 support adaptation and predict query rows.

    ``seed`` is validated and recorded at the interface boundary, but no random
    sampling occurs here: callers provide the already-selected support rows.
    """
    stage1 = validate_stage1_artifact(stage1)
    try:
        shots = int(n_shots_per_class)
    except (TypeError, ValueError) as exc:
        raise ValueError("n_shots_per_class must be an integer") from exc
    if shots not in SUPPORTED_SCHEDULE or shots != n_shots_per_class:
        raise ValueError(f"Unsupported budget {n_shots_per_class!r}; use {sorted(SUPPORTED_SCHEDULE)}")
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)):
        raise TypeError("seed must be an integer")

    width = len(stage1["feature_names"])
    Xs = _feature_matrix("support_X", support_X, width)
    Xq = _feature_matrix("query_X", query_X, width)
    ys = np.asarray(support_y)
    if ys.ndim != 1 or len(ys) != len(Xs):
        raise ValueError("support_y must be one-dimensional with one label per support row")

    classes = np.asarray(stage1["classes"])
    if not np.isin(ys, classes).all():
        raise ValueError(f"support_y may contain only classes {classes.tolist()}")
    counts = {int(c): int(np.count_nonzero(ys == c)) for c in classes}
    if any(count != shots for count in counts.values()):
        raise ValueError(f"Expected exactly {shots} support rows per class; got {counts}")

    k, shrinkage = SUPPORTED_SCHEDULE[shots]
    rep = stage1["representations"][str(k)]
    selected = np.asarray(rep["selected_feature_idx"], dtype=int)
    weights = np.asarray(stage1["metric_weights"], dtype=float)[selected]
    madrid_offsets = np.asarray(rep["madrid_class_offsets"], dtype=float)

    # Exact EXP-010 equations from candidate/joint_sweep.py. Every target-side
    # quantity below is calculated from support data only.
    Zs = Xs[:, selected] * weights
    Zq = Xq[:, selected] * weights
    support_centre = Zs.mean(axis=0)
    prototypes = np.stack([
        support_centre
        + shrinkage * madrid_offsets[i]
        + (1.0 - shrinkage) * (Zs[ys == c].mean(axis=0) - support_centre)
        for i, c in enumerate(classes)
    ])
    distances = (
        (Zq ** 2).sum(axis=1)[:, None]
        - 2.0 * Zq @ prototypes.T
        + (prototypes ** 2).sum(axis=1)[None, :]
    )
    return classes[distances.argmin(axis=1)]


def _load_cli_npz(path: Path, *, labels: bool) -> tuple[np.ndarray, np.ndarray | None, list[str]]:
    with np.load(path, allow_pickle=False) as payload:
        required = {"X", "feature_names"} | ({"y"} if labels else set())
        missing = required - set(payload.files)
        if missing:
            raise ValueError(f"{path} is missing NPZ keys: {sorted(missing)}")
        X = np.array(payload["X"], copy=True)
        y = np.array(payload["y"], copy=True) if labels else None
        names = [str(name) for name in payload["feature_names"].tolist()]
    return X, y, names


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--support", type=Path, required=True,
                        help="NPZ containing X, y, and ordered feature_names")
    parser.add_argument("--query", type=Path, required=True,
                        help="NPZ containing X and ordered feature_names; no label key is read")
    parser.add_argument("--shots", type=int, required=True, choices=sorted(SUPPORTED_SCHEDULE))
    parser.add_argument("--seed", type=int, required=True,
                        help="Fixed run identifier; adaptation itself is deterministic")
    parser.add_argument("--output", type=Path, required=True, help="Output .npy prediction path")
    args = parser.parse_args()

    stage1 = load_stage1_artifact(args.artifact)
    support_X, support_y, support_names = _load_cli_npz(args.support, labels=True)
    query_X, _, query_names = _load_cli_npz(args.query, labels=False)
    expected_names = list(stage1["feature_names"])
    if support_names != expected_names or query_names != expected_names:
        raise ValueError("Input feature_names do not exactly match the artifact's ordered schema")
    predictions = adapt_and_predict(
        stage1, support_X, support_y, query_X, args.shots, args.seed
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.output, predictions, allow_pickle=False)
    print(f"EXP-010 prediction complete: {len(predictions)} query rows -> {args.output}")
    print(f"Frozen configuration: k={SUPPORTED_SCHEDULE[args.shots][0]}, "
          f"lambda={SUPPORTED_SCHEDULE[args.shots][1]}; seed={args.seed}")


if __name__ == "__main__":
    main()
