"""Convenience entrypoint; shared implementation ../run.py."""
from pathlib import Path
import subprocess,sys
if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable,"-I","-B",str(Path(__file__).resolve().parents[1]/"run.py"),'E',*sys.argv[1:]]))
