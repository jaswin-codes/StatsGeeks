"""Infrastructure-only synthetic worker launcher."""
import argparse,json,traceback
from pathlib import Path
from infra_boundary import run
p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('worker',type=Path);p.add_argument('role');p.add_argument('output',type=Path);a=p.parse_args();assert not a.output.exists()
try:
 raw,evidence=run(json.loads(a.packet.read_text()),a.worker.read_bytes(),a.role);result={'result':json.loads(raw),'boundary_evidence':evidence}
 with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
except BaseException:
 with a.output.open('x') as f:json.dump({'status':'FAIL','traceback':traceback.format_exc()},f,indent=2)
 raise
