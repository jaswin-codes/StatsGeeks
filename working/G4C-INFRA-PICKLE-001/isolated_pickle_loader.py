"""Infrastructure-only isolated loader for the frozen preprocessing artifact.

No repository path is added to sys.path. Only the exact hash-pinned module required
by the pickle is registered under its historical fully qualified module name.
"""
import datetime
import hashlib
import importlib.util
import json
import pathlib
import pickle
import sys
import types

RUN = pathlib.Path(__file__).resolve(strict=True).parent
ROOT = RUN.parents[1]
PICKLE = ROOT / "data/preprocessed/preprocessed_data.pkl"
MODULE = ROOT / "working/minimal_standard_scaler.py"
RECEIPT = RUN / "deserialization_receipt.json"
EXPECTED_PICKLE_SHA256 = "51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe"
EXPECTED_MODULE_SHA256 = "c15ccb5f40b6c9f062f3a332ce523a1021daad65ec1f122394d388d715e2d111"
QUALIFIED_MODULE = "working.minimal_standard_scaler"


def sha256(path):
    with pathlib.Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def install_exact_pickle_dependency():
    """Register one exact module without broadening isolated import search paths."""
    if sha256(MODULE) != EXPECTED_MODULE_SHA256:
        raise RuntimeError("Pinned minimal_standard_scaler source hash mismatch")
    if "working" in sys.modules or QUALIFIED_MODULE in sys.modules:
        raise RuntimeError("Historical pickle module names unexpectedly preloaded")

    package = types.ModuleType("working")
    package.__package__ = "working"
    package.__path__ = []
    package.__file__ = None
    spec = importlib.util.spec_from_file_location(QUALIFIED_MODULE, MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot construct exact module specification")
    module = importlib.util.module_from_spec(spec)
    sys.modules["working"] = package
    sys.modules[QUALIFIED_MODULE] = module
    setattr(package, "minimal_standard_scaler", module)
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(QUALIFIED_MODULE, None)
        sys.modules.pop("working", None)
        raise
    if module.__file__ != str(MODULE) or module.StandardScaler.__module__ != QUALIFIED_MODULE:
        raise RuntimeError("Exact pickle dependency identity mismatch")
    return module


def main():
    if RECEIPT.exists():
        raise RuntimeError("Refuse to overwrite deserialization receipt")
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        raise RuntimeError("Require Python isolated mode (-I) and no bytecode (-B)")
    if sha256(PICKLE) != EXPECTED_PICKLE_SHA256:
        raise RuntimeError("Frozen preprocessing pickle hash mismatch")

    initial_path = list(sys.path)
    module = install_exact_pickle_dependency()
    if list(sys.path) != initial_path:
        raise RuntimeError("Import search path was broadened")

    # The sole authorized operation: deserialize the existing immutable artifact.
    with PICKLE.open("rb") as handle:
        loaded = pickle.load(handle)

    # Do not inspect arrays, labels, scaler fields, or invoke any method. Record only
    # that pickle.load returned and the top-level Python type needed for auditability.
    receipt = {
        "status": "PASS",
        "run_id": "G4C-INFRA-PICKLE-001",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "isolated_mode": bool(sys.flags.isolated),
        "dont_write_bytecode": bool(sys.dont_write_bytecode),
        "sys_path_unchanged": list(sys.path) == initial_path,
        "broad_repository_path_added": False,
        "registered_package": "working",
        "registered_exact_module": QUALIFIED_MODULE,
        "module_source": MODULE.relative_to(ROOT).as_posix(),
        "module_sha256": sha256(MODULE),
        "pickle_path": PICKLE.relative_to(ROOT).as_posix(),
        "pickle_sha256": sha256(PICKLE),
        "pickle_load_returned": True,
        "top_level_type": f"{type(loaded).__module__}.{type(loaded).__qualname__}",
        "payload_inspected": False,
        "methods_invoked": [],
        "models_fit": 0,
        "predictions_generated": 0,
        "workers_launched": 0,
        "scientific_state_changed": False
    }
    with RECEIPT.open("x", encoding="utf8") as handle:
        json.dump(receipt, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": "PASS", "pickle_load_returned": True,
                      "workers_launched": 0, "models_fit": 0,
                      "predictions_generated": 0}))


if __name__ == "__main__":
    main()
