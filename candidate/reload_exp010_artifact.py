"""Lightweight interface check for the packaged, frozen EXP-010 source state.

No model is fitted and no episode predictions or metrics are generated.
"""
from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "candidate" / "artifacts"
with (ART / "exp010_stage1_madrid.pkl").open("rb") as fh:
    state = pickle.load(fh)
with (ART / "stage1_madrid.pkl").open("rb") as fh:
    legacy = pickle.load(fh)
joint = json.loads((ART / "joint_sweep.json").read_text())

required = {"format", "experiment", "trained_on", "classes", "feature_names",
            "feature_importances", "metric_weights", "schedule", "representations",
            "source_artifact_sha256", "source_data_sha256"}
assert required <= state.keys()
assert state["experiment"] == "EXP-010" and state["trained_on"] == "madrid_only"
assert state["classes"] == [1, 2, 3, 4]
assert np.array_equal(state["feature_importances"], legacy["feature_importances"])
assert np.array_equal(state["metric_weights"], np.sqrt(state["feature_importances"]))
rank = np.argsort(state["feature_importances"])[::-1]
for budget, config in joint["best_per_budget"].items():
    packed = state["schedule"][budget]
    assert packed == {"k": config["k"], "lambda": config["lambda"]}
    rep = state["representations"][str(config["k"])]
    assert np.array_equal(rep["selected_feature_idx"], np.sort(rank[:config["k"]]))
    assert rep["madrid_class_offsets"].shape == (4, config["k"])
print("PASS: EXP-010 artifact reload, keys, weights, feature indices, class offsets, and schedule")
