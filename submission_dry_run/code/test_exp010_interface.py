"""Cheap software smoke test for the frozen EXP-010 prediction interface.

Uses synthetic feature matrices only. It does not train, score, sample real
episodes, or create a scientific result.
"""
from __future__ import annotations

import inspect
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
# Isolated mode omits the script directory from sys.path; add only this packaged
# code directory so the smoke test cannot import repository/global project state.
sys.path.insert(0, str(HERE))

from exp010_predict import (
    SUPPORTED_SCHEDULE,
    adapt_and_predict,
    load_stage1_artifact,
)

# Support both repository layout and the judge-facing dry-run package layout.
if (HERE.parent / "model" / "exp010_stage1_madrid.pkl").is_file():
    ROOT = HERE.parent
    SCRIPT = HERE / "exp010_predict.py"
    ARTIFACT = ROOT / "model" / "exp010_stage1_madrid.pkl"
else:
    ROOT = HERE.parents[0]
    SCRIPT = HERE / "exp010_predict.py"
    ARTIFACT = ROOT / "candidate" / "artifacts" / "exp010_stage1_madrid.pkl"
EXPECTED = {
    5: (30, 0.6),
    25: (45, 0.0),
    50: (45, 0.0),
    100: (45, 0.0),
    200: (45, 0.0),
}
SEED = 31337


def synthetic_inputs(stage1: dict, shots: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Deterministic, non-scientific matrices satisfying the feature contract."""
    width = len(stage1["feature_names"])
    classes = np.asarray(stage1["classes"])
    support_y = np.repeat(classes, shots)
    support_X = np.zeros((len(support_y), width), dtype=float)
    for row, label in enumerate(support_y):
        support_X[row] = float(label) + (row % shots) * 1e-4
    query_X = np.stack([
        np.full(width, 1.25),
        np.full(width, 2.25),
        np.full(width, 3.25),
        np.full(width, 4.25),
    ])
    return support_X, support_y, query_X


def main() -> None:
    assert SUPPORTED_SCHEDULE == EXPECTED
    assert "query_y" not in inspect.signature(adapt_and_predict).parameters
    stage1 = load_stage1_artifact(ARTIFACT)
    assert {int(b): (int(v["k"]), float(v["lambda"]))
            for b, v in stage1["schedule"].items()} == EXPECTED

    for shots, (k, shrinkage) in EXPECTED.items():
        support_X, support_y, query_X = synthetic_inputs(stage1, shots)
        predictions = adapt_and_predict(
            stage1, support_X, support_y, query_X, shots, SEED
        )
        assert predictions.shape == (len(query_X),)
        assert set(predictions.tolist()) <= set(stage1["classes"])
        print(f"PASS budget {shots}: k={k}, lambda={shrinkage}, "
              f"predictions={len(predictions)}")

    try:
        support_X, support_y, query_X = synthetic_inputs(stage1, 5)
        adapt_and_predict(stage1, support_X, support_y, query_X, 10, SEED)
    except ValueError as exc:
        assert "Unsupported budget" in str(exc)
    else:
        raise AssertionError("Unsupported budget 10 was not rejected")

    # Exercise the public CLI in a new isolated Python process. The query NPZ
    # deliberately has no labels, so successful prediction proves none are needed.
    with tempfile.TemporaryDirectory(prefix="exp010_smoke_") as directory:
        tmp = Path(directory)
        support_X, support_y, query_X = synthetic_inputs(stage1, 5)
        names = np.asarray(stage1["feature_names"])
        support_path, query_path, output_path = (
            tmp / "support.npz", tmp / "query.npz", tmp / "predictions.npy"
        )
        np.savez_compressed(support_path, X=support_X, y=support_y, feature_names=names)
        np.savez_compressed(query_path, X=query_X, feature_names=names)
        command = [
            sys.executable, "-I", "-B", str(SCRIPT),
            "--artifact", str(ARTIFACT), "--support", str(support_path),
            "--query", str(query_path), "--shots", "5", "--seed", str(SEED),
            "--output", str(output_path),
        ]
        completed = subprocess.run(command, cwd=ROOT, check=True, text=True,
                                   capture_output=True)
        cli_predictions = np.load(output_path, allow_pickle=False)
        assert cli_predictions.shape == (len(query_X),)
        print(completed.stdout.strip())

    print("PASS: clean-process artifact reload, support adaptation, and label-free query prediction")
    print("NOTE: synthetic smoke output is not a scientific metric or result")


if __name__ == "__main__":
    main()
