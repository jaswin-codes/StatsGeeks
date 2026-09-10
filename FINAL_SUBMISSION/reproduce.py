"""Dispatch to the unchanged, hash-checking Coordinate-RF entry point.

WARNING: both --support and --verify fit support-set random forests. Do not
execute during a no-training audit. Output paths must not already exist.
"""
from pathlib import Path
import runpy


def main() -> None:
    """Resolve the artifact directory independently of the caller's cwd."""
    runner = Path(__file__).resolve().parent / "model" / "reproduce_best.py"
    runpy.run_path(str(runner), run_name="__main__")


if __name__ == "__main__":
    main()
