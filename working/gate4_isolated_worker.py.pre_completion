"""Label-free transport wrapper; executed only inside Bubblewrap."""
import importlib.util
import json
import sys

packet = json.load(sys.stdin)
spec = importlib.util.spec_from_file_location('episode_entry', '/app/entry.py')
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
result = entry.entry(packet)
sys.stdout.write(json.dumps(result, allow_nan=False, separators=(',', ':')))
