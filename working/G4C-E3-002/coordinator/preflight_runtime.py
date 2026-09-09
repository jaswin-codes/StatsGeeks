"""Read-only native RF/runtime preflight using the unchanged production checker."""
import json,os,pathlib,platform,stat,sys
from gate4_production_boundary import runtime_check
from immutable_io import sha256,_native_directory,RF_SHA256
lock=runtime_check()
config=json.loads(pathlib.Path(__file__).with_name('native_cache.json').read_text())
p=pathlib.Path(config['directory'])/(RF_SHA256+'.pkl')
assert p.is_file() and not p.is_symlink() and not str(p).startswith('/mnt/')
_native_directory(p.parent)
assert sha256(p)==config['rf_sha256']==RF_SHA256
assert p.stat().st_size==1336382673 and stat.S_IMODE(p.stat().st_mode)==0o444
sys.path.insert(0,lock['image_path']+'/numeric')
import numpy, scipy, sklearn, joblib, threadpoolctl, narwhals
assert numpy.__version__=='2.4.6' and platform.python_version()=='3.14.4'
processes=[]
for entry in pathlib.Path('/proc').iterdir():
    if entry.name.isdecimal():
        try:
            cmd=(entry/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
            if any(s in cmd for s in ('/app/entry.py','g4c_linux_call.py','execution_coordinator.py')):processes.append({'pid':int(entry.name),'command':cmd})
        except (FileNotFoundError,PermissionError,ProcessLookupError):pass
assert not processes,processes
print(json.dumps({'status':'PASS','python':sys.version,'executable':sys.executable,'runtime_tree_files':len(lock['files']),'runtime_lock_sha256':'cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514','packages':{m.__name__:m.__version__ for m in (numpy,scipy,sklearn,joblib,threadpoolctl,narwhals)},'native_rf':{'path':str(p),'sha256':RF_SHA256,'bytes':p.stat().st_size,'mode':'0444','linux_native':True},'existing_production_processes':processes},indent=2))
