"""Fresh trusted Linux supervisor; preserves failure evidence without retries."""
import argparse,json,traceback
from pathlib import Path
from g4c_boundary import run
p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('worker',type=Path);p.add_argument('role');p.add_argument('output',type=Path);p.add_argument('--rf',type=Path);a=p.parse_args()
assert not a.output.exists()
try:
    packet=json.loads(a.packet.read_text());raw,evidence=run(packet,a.worker.read_bytes(),a.role,rf_path=a.rf)
    result={'result':json.loads(raw),'boundary_evidence':evidence}
    with a.output.open('x') as f:json.dump(result,f,separators=(',',':'));f.write('\n')
    print(json.dumps({'status':'PASS','role':a.role,'elapsed_seconds':evidence['elapsed_seconds']}))
except BaseException:
    with a.output.open('x') as f:json.dump({'status':'FAIL','traceback':traceback.format_exc()},f,indent=2)
    raise
