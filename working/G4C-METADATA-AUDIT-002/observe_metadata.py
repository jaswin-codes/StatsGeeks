"""Read-only passive metadata/process observation. No models or candidate workers."""
from pathlib import Path
import ctypes as C
from ctypes import wintypes as W
import datetime, hashlib, json, os, subprocess, time
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
TARGET=ROOT/'working/Open Notebook.onetoc2'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sample():
    with TARGET.open('rb') as f:
        s=os.fstat(f.fileno());h=hashlib.file_digest(f,'sha256').hexdigest();end=os.fstat(f.fileno())
    return dict(utc=stamp(),sha256=h,bytes=s.st_size,mtime_ns=s.st_mtime_ns,creation_time_ns=s.st_ctime_ns,attributes=s.st_file_attributes,stable_during_read=(s.st_size,s.st_mtime_ns)==(end.st_size,end.st_mtime_ns))
class UniqueProcess(C.Structure):_fields_=[('pid',W.DWORD),('start',W.FILETIME)]
class ProcessInfo(C.Structure):_fields_=[('process',UniqueProcess),('app_name',W.WCHAR*256),('service_name',W.WCHAR*64),('app_type',C.c_int),('status',W.ULONG),('terminal_session',W.DWORD),('restartable',W.BOOL)]
def owners():
    # Register/query/end only. Never invoke RmShutdown/RmRestart or process signals.
    dll=C.WinDLL('rstrtmgr');handle=W.DWORD();key=C.create_unicode_buffer(33)
    rc=dll.RmStartSession(C.byref(handle),0,key)
    if rc:return {'utc':stamp(),'start_error':rc}
    try:
        resources=(W.LPCWSTR*1)(str(TARGET));rc=dll.RmRegisterResources(handle,1,resources,0,None,0,None)
        if rc:return {'utc':stamp(),'register_error':rc}
        needed=W.UINT();count=W.UINT();reason=W.DWORD()
        rc=dll.RmGetList(handle,C.byref(needed),C.byref(count),None,C.byref(reason))
        if rc not in (0,234):return {'utc':stamp(),'list_error':rc}
        if not needed.value:return {'utc':stamp(),'owners':[],'note':'No reported registered resource users; not proof of no transient writer.'}
        buf=(ProcessInfo*needed.value)();count.value=needed.value
        rc=dll.RmGetList(handle,C.byref(needed),C.byref(count),buf,C.byref(reason))
        if rc:return {'utc':stamp(),'list_error':rc}
        return {'utc':stamp(),'owners':[{'pid':p.process.pid,'name':p.app_name,'service':p.service_name,'app_type':p.app_type,'restartable':bool(p.restartable),'process_start_filetime':(p.process.start.dwHighDateTime<<32)+p.process.start.dwLowDateTime} for p in buf[:count.value]],'note':'Resource-user ownership is not write-event attribution.'}
    finally:dll.RmEndSession(handle)
def processes():
    command="$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(ONENOTE|OneDrive|python.*|pythonw.*|wsl.*|bwrap|WindowsTerminal|powershell)\\.exe$' } | Select-Object Name,ProcessId,ParentProcessId,ExecutablePath,CommandLine,CreationDate | ConvertTo-Json -Depth 3"
    p=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',command],capture_output=True,text=True,timeout=30)
    return {'utc':stamp(),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def main():
    assert not (OUT/'observations.json').exists()
    observations=[];ownership=[];snapshots=[];start=time.monotonic()
    for i in range(37):
        if i:time.sleep(max(0,start+i*5-time.monotonic()))
        observations.append(sample())
        if i in [0,12,24,36]:ownership.append(owners());snapshots.append(processes())
    result={'method':'Passive read-only samples every 5 seconds for 180 seconds; no write/rename/attribute/process termination operations on target. Resource users queried by Windows Restart Manager without shutdown/restart.','started_utc':observations[0]['utc'],'ended_utc':observations[-1]['utc'],'elapsed_seconds':time.monotonic()-start,'samples':observations,'resource_users':ownership,'process_snapshots':snapshots,'unique_hashes':sorted(set(x['sha256'] for x in observations))}
    with (OUT/'observations.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'samples':len(observations),'unique_hashes':result['unique_hashes'],'owners':ownership,'elapsed_seconds':result['elapsed_seconds']},indent=2))
if __name__=='__main__':main()
