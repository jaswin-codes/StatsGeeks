"""G4C-E2-003 preparation coordinator revision.

Only --dry-run-preflight exists in this preparation version. It uses stdlib hashes
and static contract inspection; it cannot load modelling data or launch workers.
Candidate execution intentionally raises until a separately authorized, immutable
execution entrypoint is added as a NEW run artifact without changing this file.
"""
import argparse, datetime, hashlib, json, os, platform, stat, subprocess, sys
from pathlib import Path

# Python -I intentionally omits the script directory from sys.path. Add only the
# resolved, fixed sibling-module directory; do not add the repository or environment.
COORDINATOR_MODULE_DIR = Path(__file__).resolve(strict=True).parent
sys.path.insert(0, str(COORDINATOR_MODULE_DIR))
from integrity_policy import (RUN_ID, ROOT_MUTABLE_METADATA, classify_new_paths,
                              compare_checkpoint, fingerprint)

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "working" / RUN_ID
CHECKPOINT = ROOT / "working/G4C-PROVENANCE-CHECKPOINT-002"
AUDIT = ROOT / "working/G4C-METADATA-AUDIT-002"
OUT = RUN / "checkpoint/preflight.json"
ANCHORS = {
    "git_head": "165fe11df8779eed514c75bd2852c2b9588a18a4",
    "manifest_sha256": "9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32",
    "rf_sha256": "5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870",
    "runtime_lock_sha256": "cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514",
    "checkpoint_fingerprints_sha256": "e1e1d8bda427d15f41ee06ed1ff5e391d6210ab2637b950cd4ac5158f9fd1a2a",
    "metadata_audit_inventory_sha256": "d95669f5ee16674f2fa8938c979d73635e3d0ac09cca3fa194b559b5e67bc0e9",
    "checkpoint_inventory_sha256": "1406deaab5b2781845f4e3ce05dbc7495a5d55fd323b6029ea827fddd223bfc5",
    "closed_e2_001_inventory_sha256": "46cdbabcd98754f9b879250090359d29a8a64861b32887ae8e7b24b423007436",
    "blocked_e2_002_inventory_sha256": "72d5a082443b5f5e6e4eb7879d9e17c860163079b62f0af2ebd2eee959b9e302",
    "metadata_policy_sha256": "8946c08a9e3baa1fa6166196d2e6f21ef7086922323d7e4d44e598da0c7b7f43",
}
FORBIDDEN_IMPORTS = {"numpy", "scipy", "sklearn", "pandas", "joblib", "pickle"}
CANDIDATE_OUTPUT_ROOTS = ("predictions", "evidence", "candidate_state", "results")


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf8"))


def inventory_verify(path, anchor, prefix=None):
    if sha(path) != anchor:
        raise RuntimeError(f"Inventory anchor changed: {path}")
    inventory = load_json(path)
    failures = []
    for relative, expected in inventory["files"].items():
        if prefix is not None and not relative.startswith(prefix):
            continue
        actual = sha(ROOT / relative) if (ROOT / relative).is_file() else None
        if actual != expected["sha256"]:
            failures.append({"path": relative, "expected": expected["sha256"], "actual": actual})
    if failures:
        raise RuntimeError(f"Inventory mismatch: {failures}")
    return {"inventory": str(path.relative_to(ROOT)), "files_checked": len(inventory["files"]),
            "inventory_sha256": anchor}


def all_project_files():
    result = set()
    for top in ("working", "data", "original"):
        result.update(p.relative_to(ROOT).as_posix() for p in (ROOT / top).rglob("*") if p.is_file())
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    result.update(p for p in tracked if p and (ROOT / p).is_file())
    return result


def runtime_verify():
    """Hash approved runtime; no interpreter or worker launched inside it."""
    lock_path = ROOT / "working/gate4_runtime_narwhals_lock.json"
    if sha(lock_path) != ANCHORS["runtime_lock_sha256"]:
        raise RuntimeError("Runtime lock changed")
    lock = load_json(lock_path)
    # Windows cannot traverse the Linux path; use WSL only as a read-only hash host.
    linux_root = "/mnt/" + ROOT.as_posix()[0].lower() + ROOT.as_posix()[2:]
    code = r'''import hashlib,json,pathlib,sys
def sha(p):
 with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
root=pathlib.Path(sys.argv[1]); lock=json.loads((root/'working/gate4_runtime_narwhals_lock.json').read_text()); image=pathlib.Path(lock['image_path'])
actual={p.relative_to(image).as_posix():sha(p) for p in sorted(image.rglob('*')) if p.is_file()}
result={'tree_match':actual==lock['files'],'files':len(actual),'wheel_matches':{n:sha(v['source'])==v['sha256'] for n,v in lock['wheels'].items()},'bwrap_match':sha('/usr/bin/bwrap')==lock['bwrap_sha256'],'python':sys.version}
print(json.dumps(result,separators=(',',':')))
'''
    proc = subprocess.run(["wsl", "-d", "Ubuntu", "--exec", "/usr/bin/python3", "-B", "-c", code,
                           linux_root], capture_output=True, text=True, timeout=180)
    if proc.returncode or proc.stderr:
        raise RuntimeError(f"Runtime hash host failed: {proc.returncode} {proc.stderr}")
    result = json.loads(proc.stdout)
    if not result["tree_match"] or result["files"] != 4355 or not result["bwrap_match"] or not all(result["wheel_matches"].values()):
        raise RuntimeError(f"Runtime mismatch: {result}")
    result["worker_launched"] = False
    return result


def static_boundary_contract():
    """Inspect text/bytes only; never import or invoke workers/boundary."""
    files = {name: ROOT / "working" / name for name in (
        "g4c_boundary.py", "g4c_linux_call.py", "g4c_source_worker.py",
        "g4c_episode_worker.py", "gate4_lifecycle.py", "gate4_production_boundary.py")}
    text = {name: path.read_text(encoding="utf8") for name, path in files.items()}
    checks = {
        "manifest_not_mounted": "gate4_episode_manifest" not in text["g4c_boundary.py"] and
                                "'/working'" in text["g4c_episode_worker.py"] and
                                "'/mnt'" in text["g4c_episode_worker.py"],
        "project_not_mounted": "--ro-bind',lock['image_path'],'/'" in text["g4c_boundary.py"] and
                               "--ro-bind',str(rf_path),'/app/rf_final.pkl'" in text["g4c_boundary.py"],
        "episode_packet_exact_fields": "assert set(p)=={'X_support','y_support','support_ids','X_query','query_ids','source_state','parameters'}" in text["g4c_episode_worker.py"],
        "source_packet_exact_fields": "assert set(p)=={'X_source','y_source','parameters'}" in text["g4c_source_worker.py"],
        "query_and_cross_episode_labels_forbidden": all(token in text["g4c_episode_worker.py"] for token in
            ("'y_query'", "'full_target_labels'", "'other_episode_support_labels'")),
        "fresh_private_tmpfs": "--tmpfs','/tmp'" in text["g4c_boundary.py"] and
                               "assert not Path('/tmp/g4c_prior_state').exists()" in text["g4c_episode_worker.py"],
        "dedicated_reaping": "Lifecycle(reap=True)" in text["g4c_boundary.py"] and
                             "Subreaper requires a dedicated child-free supervisor" in text["gate4_lifecycle.py"],
        "zombies_not_clean": "Zombies are retained, never filtered out" in text["gate4_lifecycle.py"],
        "final_survivors_required_empty": "final_survivors" in text["gate4_lifecycle.py"] and
                                          "not life['pass_']" in text["g4c_boundary.py"],
        "prediction_finalization_barrier": "if rc or reason or evidence['stderr'] or not life['pass_']" in text["g4c_boundary.py"],
        "approved_runtime_check": "payload=canonical(packet); lock=runtime_check()" in text["g4c_boundary.py"],
        "e2_fixed_parameters_present": "'epsilon':1e-6" in text["g4c_source_worker.py"] and
                                       "'clip':[.25,4.0]" in text["g4c_source_worker.py"] and
                                       "'identity_mixture':.5" in text["g4c_source_worker.py"],
    }
    if not all(checks.values()):
        raise RuntimeError(f"Static boundary contract failure: {checks}")
    return {"status": "STATIC_PASS_NOT_EXECUTED", "checks": checks,
            "files": {name: {"sha256": sha(path), "bytes": path.stat().st_size} for name, path in files.items()},
            "limitation": "Static inspection does not recertify live isolation/teardown or candidate predictions."}


def verify_original(checkpoint):
    expected = {p for p in checkpoint if p.startswith("original/")}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "original").rglob("*") if p.is_file()}
    status = subprocess.check_output(["git", "status", "--short", "--", "original/"], cwd=ROOT)
    diff = subprocess.check_output(["git", "diff", "--", "original/"], cwd=ROOT)
    if expected != actual or status or diff:
        raise RuntimeError("original/ membership or Git state changed")
    return {"clean": True, "files": len(actual)}


def dry_run():
    if RUN.name != RUN_ID or OUT.exists():
        raise RuntimeError("Wrong/reused run identity or preflight output exists")
    if any((RUN / name).exists() for name in CANDIDATE_OUTPUT_ROOTS):
        raise RuntimeError("Existing candidate state/output detected in new namespace")
    if any(name in sys.modules for name in FORBIDDEN_IMPORTS):
        raise RuntimeError("Modelling dependency unexpectedly imported")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != ANCHORS["git_head"]:
        raise RuntimeError("Git HEAD changed")
    checkpoint_path = CHECKPOINT / "file_fingerprints.json"
    if sha(checkpoint_path) != ANCHORS["checkpoint_fingerprints_sha256"]:
        raise RuntimeError("Checkpoint fingerprint anchor changed")
    checkpoint = load_json(checkpoint_path)
    current = {relative: fingerprint(ROOT, relative) for relative in checkpoint}
    comparison = compare_checkpoint(checkpoint, current)
    if not comparison["pass"]:
        raise RuntimeError(f"Checkpoint integrity failed: {comparison['failures']}")
    histories = [
        inventory_verify(AUDIT / "artifact_hash_manifest.json", ANCHORS["metadata_audit_inventory_sha256"]),
        inventory_verify(CHECKPOINT / "artifact_hash_manifest.json", ANCHORS["checkpoint_inventory_sha256"]),
        inventory_verify(ROOT / "working/G4C-E2-001/artifact_hash_manifest.json", ANCHORS["closed_e2_001_inventory_sha256"]),
        inventory_verify(ROOT / "working/G4C-E2-002/checkpoint/artifact_hash_manifest.json", ANCHORS["blocked_e2_002_inventory_sha256"]),
    ]
    # Protected hashes are inventory metadata only; no datasets/models are deserialized.
    e1_entry = load_json(ROOT / "working/G4B-E1-001/entry.json")
    protected = {path: sha(ROOT / path) == expected for path, expected in e1_entry["protected_hashes"].items()}
    if len(protected) != 33 or not all(protected.values()):
        raise RuntimeError("Protected-file mismatch")
    if sha(ROOT / "working/gate4_episode_manifest.json") != ANCHORS["manifest_sha256"]:
        raise RuntimeError("Frozen manifest hash mismatch")
    if sha(ROOT / "working/baseline_artifacts/rf_final.pkl") != ANCHORS["rf_sha256"]:
        raise RuntimeError("Frozen RF hash mismatch")
    # Closed run must have no contamination relationship with this exclusive namespace.
    if (ROOT / "working/G4C-E2-001").resolve() == RUN.resolve() or not (ROOT / "working/G4C-E2-001/STOP_REASON.md").is_file():
        raise RuntimeError("Closed E2-001 identity contamination")
    if (ROOT / "working/G4C-E2-002").resolve() == RUN.resolve() or not (ROOT / "working/G4C-E2-002/checkpoint/preflight_attempt_1_failure.json").is_file():
        raise RuntimeError("Blocked E2-002 identity contamination")
    known = set(checkpoint)
    for inv in (AUDIT / "artifact_hash_manifest.json", CHECKPOINT / "artifact_hash_manifest.json",
                ROOT / "working/G4C-E2-002/checkpoint/artifact_hash_manifest.json"):
        known.update(load_json(inv)["files"])
        known.add(inv.relative_to(ROOT).as_posix())
    current_paths = all_project_files()
    additions = sorted(current_paths - known)
    ownership = {}
    for path in additions:
        if path.startswith(f"working/{RUN_ID}/"):
            ownership[path] = "COORDINATOR"
        else:
            raise RuntimeError(f"Unexpected post-checkpoint path outside new namespace: {path}")
    path_policy = classify_new_paths(ownership)
    if not path_policy["pass"]:
        raise RuntimeError(f"New-path policy failed: {path_policy['failures']}")
    boundary = static_boundary_contract()
    runtime = runtime_verify()
    report = {
        "status": "READY FOR TEAM LEAD EXECUTION AUTHORIZATION",
        "run_id": RUN_ID,
        "mode": "DRY_RUN_PREFLIGHT_ONLY",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "coordinator_integrated": True,
        "execution_available_in_this_task": False,
        "authorization_gate": "Candidate execution is absent/disabled; a separate explicit Team Lead execution authorization is required.",
        "metadata_policy": comparison,
        "exact_mutable_path": ROOT_MUTABLE_METADATA,
        "all_other_preexisting_paths_default": "DENY_MUTATION",
        "protected_33": {"status": "PASS", "files": protected},
        "manifest": {"status": "HASH_ONLY_PASS", "sha256": ANCHORS["manifest_sha256"], "contents_loaded": False},
        "rf": {"status": "HASH_ONLY_PASS", "sha256": ANCHORS["rf_sha256"], "deserialized": False},
        "runtime": runtime,
        "original": verify_original(checkpoint),
        "historical_inventories": histories,
        "closed_G4C_E2_001": "UNCHANGED_AND_NOT_REUSED",
        "blocked_G4C_E2_002": "UNCHANGED_AND_NOT_REUSED",
        "new_namespace": {"owned_paths": ownership, "candidate_state_present": False,
                          "candidate_artifact_roots_absent": list(CANDIDATE_OUTPUT_ROOTS)},
        "isolation_teardown_finalization_policy": boundary,
        "model_data_loaded": False,
        "target_labels_loaded": False,
        "episode_manifest_contents_loaded": False,
        "episode_or_support_query_contents_loaded": False,
        "workers_launched": 0,
        "models_fit": 0,
        "predictions_constructed": 0,
        "git_cleanup_actions": [],
        "deviations": ["Live worker isolation/teardown is statically checked only because worker launch is prohibited.",
                       "OneNote writer PID remains unattributed as documented by Metadata Audit 002."],
        "host_python": platform.python_version(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("x", encoding="utf8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "workers_launched": 0,
                      "model_data_loaded": False, "metadata_events": len(comparison["metadata_events"])}, indent=2))


def execute():
    raise RuntimeError("EXECUTION NOT AUTHORIZED OR IMPLEMENTED IN THIS PREPARATION ENTRYPOINT")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run-preflight", action="store_true")
    args = parser.parse_args()
    if not args.dry_run_preflight:
        execute()
    dry_run()
