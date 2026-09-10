"""Coordinate-RF: hash-checked pool-bound inference. No query labels accepted."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1]/'model/reproduce_best.py'),run_name='__main__')
