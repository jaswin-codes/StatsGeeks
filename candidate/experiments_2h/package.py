"""Create convenience entrypoints and record completion metadata; no experiments."""
from pathlib import Path
import json,time,subprocess,sys
O=Path(__file__).resolve().parent
folders={'A':'expA_source_local','B':'expB_dim_shrink','C':'expC_class_diagnostic','D':'expD_spatial','E':'expE_temporal','F':'expF_covariance'}
for branch,folder in folders.items():
 p=O/folder/'script.py';assert not p.exists()
 p.write_text('"""Convenience entrypoint; shared implementation ../run.py."""\nfrom pathlib import Path\nimport subprocess,sys\nif __name__ == "__main__":\n    raise SystemExit(subprocess.call([sys.executable,"-I","-B",str(Path(__file__).resolve().parents[1]/"run.py"),'+repr(branch)+',*sys.argv[1:]]))\n')
(O/'environment.txt').write_bytes(subprocess.check_output([sys.executable,'-I','-B','-m','pip','freeze']))
start=json.loads((O/'start.json').read_text()); runs={}
for p in O.rglob('results*.json'):
 r=json.loads(p.read_text());runs[p.relative_to(O).as_posix()]=r['runtime_seconds']
(O/'timing.json').write_text(json.dumps({'start':start,'completed_local_time':time.strftime('%Y-%m-%d %H:%M:%S'),'elapsed_minutes_since_protection_snapshot':(time.time()-start['unix_time'])/60,'note':'Finished early after completing all bounded grids and clean repeats. No extra tuning to consume the nominal two-hour ceiling. Preliminary inspection preceded snapshot.','run_seconds':runs},indent=2))
print('Packaging complete')
