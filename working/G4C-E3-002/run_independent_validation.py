"""Launch unchanged bound validator in the approved Linux numerical environment.
Privileged evaluator only; no candidate/coordinator import or worker launch.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import hashlib,json,pathlib,sys,time,traceback
ROOT=pathlib.Path(__file__).resolve().parents[2];RUN=ROOT/'working/G4C-E3-002'
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
start=time.perf_counter()
try:
    lockpath=ROOT/'working/gate4_runtime_narwhals_lock.json'
    assert sha(lockpath)=='cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514'
    lock=json.loads(lockpath.read_text());image=pathlib.Path(lock['image_path'])
    assert {p.relative_to(image).as_posix():sha(p) for p in sorted(image.rglob('*')) if p.is_file()}==lock['files']
    for item in lock['wheels'].values():assert sha(item['source'])==item['sha256']
    assert sha('/usr/bin/bwrap')==lock['bwrap_sha256']
    sys.path.insert(0,lock['image_path']+'/numeric');sys.path.insert(0,str(RUN/'coordinator'))
    import e3_validator
    assert sha(e3_validator.__file__)=='02299fc780e624933255b5aa4e01192bb8d4e53d92c27fd0bcb0d12834a8828c'
    result=e3_validator.validate_e3_run(RUN)
    result['launcher_wall_seconds']=time.perf_counter()-start
    result['runtime_tree_files_verified']=len(lock['files'])
    result['execution_mode']='privileged independent evaluator, original frozen RF reconstruction versus new Linux-native worker predictions; no worker launch'
    destination=RUN/'validation/independent_validation.json'
except BaseException:
    result={'status':'FAIL','seconds':time.perf_counter()-start,'traceback':traceback.format_exc()}
    destination=RUN/'validation/INDEPENDENT_VALIDATION_FAILURE.json'
with destination.open('x') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
if result['status']!='PASS':raise SystemExit(1)
