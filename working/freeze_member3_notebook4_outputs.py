"""Freeze recoverable Notebook 4 reference outputs without rerunning any cells."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import nbformat
import numpy as np
import scipy
import sklearn

ROOT = Path(__file__).resolve().parents[1]
EXECUTED = ROOT / "working" / "4-Modelling_member3_reference_executed.ipynb"
SOURCE = ROOT / "working" / "4-Modelling_member3_reference.ipynb"
ORIGINAL = ROOT / "original" / "4-Modelling.ipynb"
PICKLE = ROOT / "data" / "preprocessed" / "preprocessed_data.pkl"
OUT = ROOT / "working" / "member3_baseline_frozen"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_text(cell: object) -> str:
    return "".join(
        output.get("text", "")
        for output in cell.outputs
        if output.output_type == "stream"
    )


def save_json(name: str, payload: dict) -> Path:
    path = OUT / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    notebook = nbformat.read(EXECUTED, as_version=4)
    cv_text = output_text(notebook.cells[6])
    zero_text = output_text(notebook.cells[18])
    prototype_text = output_text(notebook.cells[24])

    cv_scores = [float(value) for value in re.findall(r"macro-F1 = ([0-9.]+)", cv_text)]
    zero_match = re.search(r"Macro F1: ([0-9.]+)", zero_text)
    prototype_matches = re.findall(
        r"^\s*(\d+) shots/class: macro-F1 = ([0-9.]+) \+/- ([0-9.]+)$",
        prototype_text,
        flags=re.MULTILINE,
    )
    if len(cv_scores) != 25 or zero_match is None or len(prototype_matches) != 6:
        raise RuntimeError("Executed notebook outputs do not match the expected reference result contract")

    cv_payload = {
        "artifact_type": "recovered_notebook_output_summary",
        "source_executed_notebook": str(EXECUTED.relative_to(ROOT)),
        "source_executed_notebook_sha256": sha256(EXECUTED),
        "fold_macro_f1": cv_scores,
        "mean_macro_f1": float(np.mean(cv_scores)),
        "std_macro_f1_ddof0": float(np.std(cv_scores)),
        "printed_mean_macro_f1": 0.6281,
        "printed_std_macro_f1": 0.0043,
        "cv_config": {"n_splits": 5, "n_repeats": 5, "random_state": 42},
    }
    zero_payload = {
        "artifact_type": "recovered_notebook_output_summary",
        "source_executed_notebook": str(EXECUTED.relative_to(ROOT)),
        "source_executed_notebook_sha256": sha256(EXECUTED),
        "macro_f1": float(zero_match.group(1)),
        "classification_report_text": zero_text,
        "prediction_arrays_available": False,
        "note": "Notebook output stores metrics/report text only; y_ams_pred_zero was kernel memory and is unavailable after shutdown.",
    }
    prototype_payload = {
        "artifact_type": "recovered_notebook_output_summary",
        "source_executed_notebook": str(EXECUTED.relative_to(ROOT)),
        "source_executed_notebook_sha256": sha256(EXECUTED),
        "results": {
            shots: {"mean_macro_f1": float(mean), "std_macro_f1_ddof0": float(std), "n_trials": 10}
            for shots, mean, std in prototype_matches
        },
        "shots_per_class": [5, 10, 25, 50, 100, 200],
        "rng": "np.random.default_rng(42), one advancing generator across all budgets/trials",
        "support_indices_available": False,
        "note": "Notebook output stores summaries only; per-trial scores/prototypes/support indices were kernel memory and are unavailable after shutdown.",
    }
    metadata = {
        "artifact_type": "notebook4_reference_baseline_freeze",
        "freeze_scope": "Recoverable outputs from completed reference execution only; no cells rerun.",
        "source_notebook": str(ORIGINAL.relative_to(ROOT)),
        "source_notebook_sha256": sha256(ORIGINAL),
        "working_notebook": str(SOURCE.relative_to(ROOT)),
        "working_notebook_sha256": sha256(SOURCE),
        "executed_notebook": str(EXECUTED.relative_to(ROOT)),
        "executed_notebook_sha256": sha256(EXECUTED),
        "input_pickle": str(PICKLE.relative_to(ROOT)),
        "input_pickle_sha256": sha256(PICKLE),
        "environment": {
            "python": sys.version.replace("\n", " "),
            "executable": sys.executable,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "rf_params": {"n_estimators": 500, "class_weight": "balanced", "random_state": 42, "n_jobs": -1},
        "cv_params": {"n_splits": 5, "n_repeats": 5, "random_state": 42},
        "zero_shot_procedure": "Fresh RF fit on all Madrid X/y, then rf_final.predict(X_amsterdam), then macro F1 against y_amsterdam.",
        "unavailable_after_kernel_shutdown": [
            "rf_final fitted model",
            "CV fitted forests and OOF prediction/probability arrays",
            "y_ams_pred_zero and proba_amsterdam_zero",
            "prototype per-trial scores, support/query indices, prototypes, and query predictions",
        ],
        "rerun_performed": False,
    }

    paths = [
        save_json("madrid_cv_results.json", cv_payload),
        save_json("amsterdam_zero_shot_results.json", zero_payload),
        save_json("amsterdam_prototype_results.json", prototype_payload),
        save_json("metadata.json", metadata),
    ]
    manifest = {
        "artifact_type": "manifest",
        "files": {path.name: {"sha256": sha256(path), "bytes": path.stat().st_size} for path in paths},
        "source_executed_notebook_sha256": sha256(EXECUTED),
        "input_pickle_sha256": sha256(PICKLE),
        "rerun_performed": False,
    }
    save_json("artifact_manifest.json", manifest)
    print("FROZEN", OUT)


if __name__ == "__main__":
    main()
