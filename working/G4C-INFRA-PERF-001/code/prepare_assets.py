"""Prepare new execution assets; NEVER execute a coordinator or worker.

Only the bounded signature read, run identity, and trusted RF transport change.
Scientific worker bytes, runtime boundary, and lifecycle code are copied verbatim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROVEN = ROOT / "working/G4C-E3-001/coordinator"
TRANSPORT_SOURCE = ROOT / "working/G4C-E2-008/coordinator/g4c_linux_call.py"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bounded_coordinator(source: bytes) -> bytes:
    old = b"p.read_bytes()[:16].hex()"
    if source.count(old) != 1:
        raise ValueError("Expected exactly one frozen signature-read expression")
    newline = b"\r\n" if b"\r\n" in source else b"\n"
    helper = newline.join([
        b"def signature_hex(path):",
        b" with pathlib.Path(path).open('rb') as stream:return stream.read(16).hex()",
        b"",
    ])
    marker = b"def preexisting_integrity():"
    if source.count(marker) != 1:
        raise ValueError("Unsupported coordinator; integration requires explicit review")
    result = source.replace(marker, helper + marker).replace(old, b"signature_hex(p)")
    compile(result, "bounded_coordinator.py", "exec")
    return result


def native_transport(source: bytes) -> bytes:
    """Keep original output/error handling and boundary.run; add native RF staging."""
    newline = b"\r\n" if b"\r\n" in source else b"\n"
    marker = b"from g4c_boundary import run"
    imports = newline.join([
        marker,
        b"from immutable_io import RF_SHA256, stage_frozen_file",
    ])
    if source.count(marker) != 1:
        raise ValueError("Unrecognized proven transport")
    old = b"packet=json.loads(a.packet.read_text());raw,evidence=run(packet,a.worker.read_bytes(),a.role,rf_path=a.rf)"
    replacement = newline.join([
        b"packet=json.loads(a.packet.read_text())",
        b"    native_record=None",
        b"    if a.rf is not None:",
        b"        if a.role!='episode' or packet['parameters']['candidate'] not in ('E3','E5'):",
        b"            raise RuntimeError('RF supplied to an unauthorized worker role')",
        b"        config=json.loads(Path(__file__).with_name('native_cache.json').read_text())",
        b"        if set(config)!={'directory','rf_sha256'} or config['rf_sha256']!=RF_SHA256:",
        b"            raise RuntimeError('Invalid native cache configuration')",
        b"        native_record=stage_frozen_file(a.rf,Path(config['directory']),RF_SHA256)",
        b"        a.rf=Path(native_record['path'])",
        b"    raw,evidence=run(packet,a.worker.read_bytes(),a.role,rf_path=a.rf)",
    ])
    if source.count(old) != 1:
        raise ValueError("Unrecognized run invocation")
    result = source.replace(marker, imports).replace(old, replacement)
    result = result.replace(b"'boundary_evidence':evidence}",
                            b"'boundary_evidence':evidence,'infrastructure_io':native_record}")
    compile(result, "g4c_linux_call.py", "exec")
    return result


def asset_bytes() -> dict[str, bytes]:
    # Pin source code to closed historical inventories, not just current filenames.
    anchors = {
        "G4C-E3-001": "60d74b21be8825af89917895b45cc64e7bf1021b7321042345383686152454a8",
        "G4C-E2-008": "6bab2d294b291cda113b471921299224051d390dfbe5c9a58e42df8ba42570bd",
    }
    inventories = {}
    for identity, expected in anchors.items():
        manifest = ROOT / "working" / identity / "artifact_hash_manifest.json"
        raw = manifest.read_bytes()
        if digest(raw) != expected:
            raise RuntimeError("Historical manifest anchor mismatch")
        inventories[identity] = json.loads(raw)["files"]
    for path in list(PROVEN.glob("*.py")) + [TRANSPORT_SOURCE]:
        identity = path.parent.parent.name
        relative = path.relative_to(ROOT).as_posix()
        if digest(path.read_bytes()) != inventories[identity][relative]["sha256"]:
            raise RuntimeError(f"Historical source code mutated: {relative}")
    files = {}
    for name in ("episode_worker.py", "source_worker.py", "preflight_worker.py",
                 "g4c_boundary.py", "gate4_lifecycle.py", "gate4_production_boundary.py"):
        files[name] = (PROVEN / name).read_bytes()
    files["execution_coordinator.py"] = bounded_coordinator(
        (PROVEN / "execution_coordinator.py").read_bytes())
    files["g4c_linux_call.py"] = native_transport(TRANSPORT_SOURCE.read_bytes())
    files["immutable_io.py"] = (HERE / "immutable_io.py").read_bytes()
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect", action="store_true", help="Print hashes only; no files created")
    parser.add_argument("--new-run-id", help="Future separately authorized E3 identity")
    parser.add_argument("--native-cache", help="Absolute Linux-native cache directory")
    parser.add_argument("--authorization", type=Path, help="Externally supplied approval record")
    args = parser.parse_args()
    files = asset_bytes()
    if args.inspect:
        print(json.dumps({name: digest(data) for name, data in files.items()}, indent=2))
        return
    # E4/E5 transport works unchanged, but no unapproved scientific coordinator is invented.
    if not args.new_run_id or not re.fullmatch(r"G4C-E3-\d{3}", args.new_run_id):
        parser.error("Only the frozen E3 coordinator is integrated; E4/E5 require approved coordinator bindings")
    if not args.native_cache or not args.native_cache.startswith("/") or not args.authorization:
        parser.error("Native path and separate execution approval are required")
    approval = json.loads(args.authorization.read_text())
    if (approval.get("run_id") != args.new_run_id or approval.get("candidate") != "E3"
            or approval.get("scope") != "execution"):
        parser.error("Approval must bind the exact new E3 run and execution scope")
    run = ROOT / "working" / args.new_run_id
    run.mkdir(exist_ok=False)
    for directory in ("coordinator", "checkpoint", "candidate_state", "evidence", "predictions", "results"):
        (run / directory).mkdir()
    files["execution_coordinator.py"] = files["execution_coordinator.py"].replace(
        b"G4C-E3-001", args.new_run_id.encode("ascii"))
    files["native_cache.json"] = (json.dumps({"directory": args.native_cache,
        "rf_sha256": "5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870"}, indent=2) + "\n").encode()
    for name, data in files.items():
        with (run / "coordinator" / name).open("xb") as stream:
            stream.write(data)
    record = {"authorization": approval, "source": str(PROVEN.relative_to(ROOT)),
              "changes": ["bounded 16-byte signature read", "native hash-verified RF transport", "new run identity"],
              "code_hashes": {name: digest(data) for name, data in files.items()},
              "experiments_launched": 0}
    with (run / "checkpoint/infrastructure_preparation.json").open("x", encoding="utf8") as stream:
        json.dump(record, stream, indent=2)
    print(f"Prepared only: {run}. No worker or coordinator was launched.")


if __name__ == "__main__":
    main()
