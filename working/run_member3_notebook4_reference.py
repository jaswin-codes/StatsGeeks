"""Execute the untouched Notebook 4 working copy with the authorised Python 3.11 kernel.

This wrapper supplies only the kernel command/cwd needed because no local Jupyter
kernelspec is installed. Notebook cell source, parameters, seeds, and execution
order are not changed.
"""
from __future__ import annotations

import hashlib
import os
import sys
import time
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
WORKING = ROOT / "working"
SOURCE = WORKING / "4-Modelling_member3_reference.ipynb"
OUTPUT = WORKING / "4-Modelling_member3_reference_executed.ipynb"
LOG = WORKING / "member3_notebook4_reference_execution.log"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    started = time.perf_counter()
    # The accepted pickle references working.minimal_standard_scaler. The
    # repository root must be on the kernel import path while the notebook runs
    # from working/ so its original ../data path resolves unchanged.
    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")

    notebook = nbformat.read(SOURCE, as_version=4)
    kernel_command = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    kernel_manager = KernelManager(kernel_cmd=kernel_command)
    client = NotebookClient(
        notebook,
        km=kernel_manager,
        timeout=None,
        resources={"metadata": {"path": str(WORKING)}},
        record_timing=True,
    )

    try:
        client.execute(cwd=str(WORKING))
    except Exception as exc:
        elapsed = time.perf_counter() - started
        LOG.write_text(
            "STATUS: FAIL\n"
            f"SOURCE: {SOURCE}\n"
            f"SOURCE_SHA256: {sha256(SOURCE)}\n"
            f"PYTHON: {sys.executable}\n"
            f"ELAPSED_SECONDS: {elapsed:.3f}\n"
            f"ERROR_TYPE: {type(exc).__name__}\n"
            f"ERROR: {exc}\n",
            encoding="utf-8",
        )
        raise

    nbformat.write(notebook, OUTPUT)
    elapsed = time.perf_counter() - started
    LOG.write_text(
        "STATUS: PASS\n"
        f"SOURCE: {SOURCE}\n"
        f"SOURCE_SHA256: {sha256(SOURCE)}\n"
        f"OUTPUT: {OUTPUT}\n"
        f"OUTPUT_SHA256: {sha256(OUTPUT)}\n"
        f"PYTHON: {sys.executable}\n"
        f"KERNEL_COMMAND: {kernel_command}\n"
        f"CWD: {WORKING}\n"
        f"ELAPSED_SECONDS: {elapsed:.3f}\n",
        encoding="utf-8",
    )
    print(f"Notebook 4 reference execution PASS in {elapsed:.1f} seconds")


if __name__ == "__main__":
    main()
