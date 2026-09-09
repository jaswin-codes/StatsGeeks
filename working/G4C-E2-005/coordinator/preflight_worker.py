"""Gate4B access preflight. Does not calculate model state or predictions."""
import sys;sys.path.insert(0,'/numeric')
import hashlib,json,os,gc
from pathlib import Path
for path in ['/mnt','/home','/run','/data','/working','/proc/1/root/mnt','/proc/1/root/home']:
 assert not Path(path).exists(),path
assert all('LABEL' not in k.upper() and 'EPISODE' not in k.upper() for k in os.environ)
for p in Path('/proc/self/fd').iterdir():
 try: target=os.readlink(p)
 except FileNotFoundError:continue
 assert int(p.name)<=2 and target.startswith('pipe:'),(p,target)
import numpy as np,scipy,sklearn,narwhals
assert (sys.version_info[:3],np.__version__,scipy.__version__,sklearn.__version__,narwhals.__version__)==((3,14,4),'2.4.6','1.17.1','1.9.0','2.25.0')
p=json.load(sys.stdin);sys.stdin.close()
assert set(p)=={'X_support','y_support','support_ids','X_query','query_ids','parameters'}
assert p['parameters']=={'mode':'preflight'}
assert len(p['X_support'])==len(p['y_support'])==len(p['support_ids']) and len(p['X_query'])==len(p['query_ids'])
for name in ('y_query','y_amsterdam','y_target','full_target_labels','other_episode_support_labels','evaluator','manifest'):
 assert name not in globals()
 for m in list(sys.modules.values()):
  if m is not None:assert name not in vars(m)
 for o in gc.get_objects():
  if type(o) is dict and name in o:assert type(o[name]) is str and o[name]==name
assert not Path('/tmp/prior_e1_state').exists();Path('/tmp/prior_e1_state').write_text(json.dumps(p['y_support']))
try:Path('/numeric/write').write_text('x');raise AssertionError('writable runtime')
except OSError:pass
q=hashlib.sha256(json.dumps(p['query_ids'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
print(json.dumps({'status':'PASS','query_fingerprint':q,'model_computation':False},separators=(',',':')))
