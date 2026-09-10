"""G4C-E2-002 exact-path integrity policy (standard library only).

This module does not import numerical/model packages and never opens datasets,
the manifest as JSON, model pickle, target labels, or episode records.
"""
from pathlib import Path
import hashlib, os, stat

RUN_ID = "G4C-E2-002"
ROOT_MUTABLE_METADATA = "working/Open Notebook.onetoc2"
TOC_SIGNATURE_HEX = "a12fff43d9ef764c9ee210ea5722765f"
REPARSE_ATTRIBUTE = 0x400


def _under(path, prefix):
    return path == prefix or path.startswith(prefix.rstrip("/") + "/")


def normalized_relative(root, path):
    root = Path(root).resolve(strict=True)
    path = Path(path)
    absolute = path.resolve(strict=True)
    relative = absolute.relative_to(root).as_posix()
    if absolute != root.joinpath(*relative.split("/")).absolute():
        raise RuntimeError(f"Non-canonical or substitute path: {path}")
    if any(part in ("", ".", "..") for part in relative.split("/")):
        raise RuntimeError(f"Unsafe relative path: {relative}")
    return relative


def fingerprint(root, relative):
    """Race-aware fingerprint with file identity/type/link safeguards."""
    root = Path(root).resolve(strict=True)
    relative = relative.replace("\\", "/")
    path = root.joinpath(*relative.split("/"))
    if normalized_relative(root, path) != relative:
        raise RuntimeError(f"Path alias rejected: {relative}")
    before = path.lstat()
    attrs = getattr(before, "st_file_attributes", 0)
    if not stat.S_ISREG(before.st_mode) or attrs & REPARSE_ATTRIBUTE:
        raise RuntimeError(f"Nonregular/reparse file rejected: {relative}")
    if before.st_nlink != 1:
        raise RuntimeError(f"Hard-linked file rejected: {relative}")
    with path.open("rb") as handle:
        signature = handle.read(16).hex()
        handle.seek(0)
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
        opened = os.fstat(handle.fileno())
    after = path.lstat()
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, attrs)
    identity_open = (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns,
                     getattr(opened, "st_file_attributes", 0))
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                      getattr(after, "st_file_attributes", 0))
    if identity_before != identity_open or identity_open != identity_after:
        raise RuntimeError(f"File changed or was replaced while hashing: {relative}")
    return {"sha256": digest, "bytes": after.st_size, "mtime_ns": after.st_mtime_ns,
            "file_id": after.st_ino,
            "attributes": getattr(after, "st_file_attributes", 0),
            "signature_hex": signature, "regular": True, "links": after.st_nlink}


def compare_checkpoint(checkpoint, current):
    """Default deny: exactly one path may drift, under stricter identity checks."""
    failures, metadata_events = [], []
    if set(checkpoint) != set(current):
        for path in sorted(set(checkpoint) - set(current)):
            failures.append({"path": path, "reason": "checkpoint path missing"})
        for path in sorted(set(current) - set(checkpoint)):
            failures.append({"path": path, "reason": "undeclared path injected into checkpoint set"})
    for path in sorted(set(checkpoint) & set(current)):
        before, after = checkpoint[path], current[path]
        if before == after:
            continue
        if path != ROOT_MUTABLE_METADATA:
            failures.append({"path": path, "reason": "non-allowlisted pre-existing file changed",
                             "before": before, "after": after})
            continue
        immutable_keys = ("file_id", "attributes", "signature_hex", "regular", "links")
        keys = tuple(k for k in immutable_keys if k in before)
        invalid = [k for k in keys if before[k] != after[k]]
        if (after["signature_hex"] != TOC_SIGNATURE_HEX or not after["regular"] or
                after["links"] != 1 or after["attributes"] & REPARSE_ATTRIBUTE):
            invalid.append("OneNote TOC type/link/reparse safeguard")
        if invalid:
            failures.append({"path": path, "reason": "allowlisted metadata identity/type changed",
                             "invalid": sorted(set(invalid)), "before": before, "after": after})
        else:
            metadata_events.append({"classification": "EXPECTED_EXTERNAL_METADATA_MUTATION",
                                    "path": path, "before": before, "after": after})
    return {"pass": not failures, "failures": failures,
            "metadata_events": metadata_events,
            "allowed_mutable_paths": [ROOT_MUTABLE_METADATA]}


def classify_new_paths(paths):
    """New paths are allowed only inside this run namespace and by declared phase."""
    failures = []
    for relative, owner in paths.items():
        if not _under(relative, f"working/{RUN_ID}"):
            failures.append({"path": relative, "reason": "new path outside run namespace"})
        if owner not in ("COORDINATOR", "CANDIDATE"):
            failures.append({"path": relative, "reason": "unknown artifact owner"})
        if relative.endswith(".onetoc2") and relative != ROOT_MUTABLE_METADATA:
            # A newly observed run-local TOC can be recorded as coordinator-created,
            # but receives no mutable exception after its first fingerprint.
            if owner != "COORDINATOR":
                failures.append({"path": relative, "reason": "TOC cannot be candidate output"})
    return {"pass": not failures, "failures": failures}
