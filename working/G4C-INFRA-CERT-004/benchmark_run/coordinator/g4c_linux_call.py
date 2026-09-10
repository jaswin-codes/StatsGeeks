"""Fresh trusted Linux supervisor; preserves failure evidence without retries."""
import argparse,json,traceback
from pathlib import Path
from g4c_boundary import run
from immutable_io import RF_SHA256, stage_frozen_file
p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('worker',type=Path);p.add_argument('role');p.add_argument('output',type=Path);p.add_argument('--rf',type=Path);a=p.parse_args()
assert not a.output.exists()
try:
    packet=json.loads(a.packet.read_text())
    native_record=None
    if a.rf is not None:
        if a.role!='episode' or packet['parameters']['candidate'] not in ('E3','E5'):
            raise RuntimeError('RF supplied to an unauthorized worker role')
        config=json.loads(Path(__file__).with_name('native_cache.json').read_text())
        if set(config)!={'directory','rf_sha256'} or config['rf_sha256']!=RF_SHA256:
            raise RuntimeError('Invalid native cache configuration')
        native_record=stage_frozen_file(a.rf,Path(config['directory']),RF_SHA256)
        a.rf=Path(native_record['path'])
    raw,evidence=run(packet,a.worker.read_bytes(),a.role,rf_path=a.rf)
    result={'result':json.loads(raw),'boundary_evidence':evidence,'infrastructure_io':native_record}
    with a.output.open('x') as f:json.dump(result,f,separators=(',',':'));f.write('\n')
    print(json.dumps({'status':'PASS','role':a.role,'elapsed_seconds':evidence['elapsed_seconds']}))
except BaseException:
    with a.output.open('x') as f:json.dump({'status':'FAIL','traceback':traceback.format_exc()},f,indent=2)
    raise
