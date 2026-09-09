"""Trusted Linux call adapter; candidate sees only stdin packet inside Bubblewrap."""
import argparse,json
from pathlib import Path
from gate4b_boundary import run

def main():
 p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('worker',type=Path);p.add_argument('role');p.add_argument('output',type=Path);a=p.parse_args();assert not a.output.exists()
 raw,evidence=run(json.loads(a.packet.read_text()),a.worker.read_bytes(),a.role)
 result=json.loads(raw)
 with a.output.open('x') as f:json.dump({'result':result,'boundary_evidence':evidence},f,separators=(',',':'));f.write('\n')
 print(json.dumps({'status':'PASS','role':a.role,'output':str(a.output),'elapsed_seconds':evidence['elapsed_seconds']}))
if __name__=='__main__':main()
