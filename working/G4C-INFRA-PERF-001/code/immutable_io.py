"""Infrastructure-only I/O; never imports scientific libraries or launches workers."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import stat
import tempfile
import time

RF_SHA256 = "5ffdd11f300532a14b3c2957a1ac77b748aa91c0a4d1a88f1ff0a3735dc75870"


def sha256(path: Path) -> str:
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def signature_hex(path: Path) -> str:
    """Exactly the original first-16-byte signature, without a full-file allocation."""
    with Path(path).open("rb") as stream:
        return stream.read(16).hex()


def _regular(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Not a regular, non-symlink file: {path}")


def _sync_directory(directory: Path) -> None:
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _native_directory(directory: Path) -> None:
    """Fail closed unless the resolved Linux mount is a local native filesystem."""
    if os.name != "posix" or not Path("/proc/self/mountinfo").exists():
        raise RuntimeError("Native artifact staging requires Linux")
    resolved = str(directory.resolve())
    mounts = []
    for line in Path("/proc/self/mountinfo").read_text().splitlines():
        left, right = line.split(" - ", 1)
        mount = left.split()[4]
        for encoded, decoded in [(r"\040", " "), (r"\011", "\t"), (r"\134", "\\")]:
            mount = mount.replace(encoded, decoded)
        if resolved == mount or resolved.startswith(mount.rstrip("/") + "/"):
            mounts.append((len(mount), right.split()[0]))
    if not mounts or max(mounts)[1] not in {"ext4", "xfs", "btrfs", "tmpfs"}:
        raise RuntimeError(f"Not an approved Linux-native filesystem: {directory}")


def stage_frozen_file(source: Path, directory: Path, expected: str) -> dict:
    """Atomic content-addressed copy. Never rewrites a corrupt existing cache.

    Existing caches are fully rehashed, not trusted by timestamps or readonly mode.
    The caller still performs all original source/worker/runtime integrity checks.
    No model deserialization, prediction, mount, or worker creation occurs here.
    """
    if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError("Invalid SHA256")
    source, directory = Path(source), Path(directory)
    _regular(source)
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    _native_directory(directory)
    destination = directory / (expected + ".pkl")
    started = time.perf_counter()
    if destination.exists() or destination.is_symlink():
        _regular(destination)
        if sha256(destination) != expected:
            raise RuntimeError("Existing frozen cache hash mismatch; no automatic repair")
        return {"path": str(destination), "sha256": expected, "bytes": destination.stat().st_size,
                "created": False, "seconds": time.perf_counter() - started}
    before = source.stat()
    fd, temporary = tempfile.mkstemp(prefix=".stage-", dir=directory)
    temporary = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as output, source.open("rb") as input_stream:
            shutil.copyfileobj(input_stream, output, length=1024 * 1024)
            output.flush()
            os.fsync(output.fileno())
        after = source.stat()
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise RuntimeError("Source changed during staging")
        if sha256(temporary) != expected:
            raise RuntimeError("Staged bytes disagree with frozen digest")
        os.chmod(temporary, 0o444)
        # link is atomic, same-filesystem, and refuses to overwrite another publisher.
        try:
            os.link(temporary, destination)
        except FileExistsError:
            _regular(destination)
            if sha256(destination) != expected:
                raise RuntimeError("Concurrent publisher produced invalid bytes")
        _sync_directory(directory)
    finally:
        temporary.unlink(missing_ok=True)
    return {"path": str(destination), "sha256": expected, "bytes": destination.stat().st_size,
            "created": True, "seconds": time.perf_counter() - started}
