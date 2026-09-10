"""Synthetic packet parser with exact approved inherited-FD policy; no modelling."""
import sys
sys.path.insert(0,'/numeric')
import hashlib,json,os,stat,time
from pathlib import Path
APPROVED_TRANSIENT={
 '/usr/lib/x86_64-linux-gnu/libffi.so.8':'1a0dc86f787f73e025a6e521056360afcbe70f2a82cd808132fefc2b4ee95daa'
}
def sha(path):
 with open(path,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def audit(stage):
 accepted=[];forbidden=[];vanished=[]
 for name in os.listdir('/proc/self/fd'):
  fd=int(name)
  if fd<=2:continue
  try:
   target=os.readlink('/proc/self/fd/'+name);before=os.fstat(fd);info=Path('/proc/self/fdinfo/'+name).read_text();after=os.fstat(fd)
  except (FileNotFoundError,OSError):vanished.append(fd);continue
  if (before.st_dev,before.st_ino)!=(after.st_dev,after.st_ino):forbidden.append({'fd':fd,'reason':'identity changed during audit'});continue
  expected=APPROVED_TRANSIENT.get(target)
  flags=int(next(line.split()[1] for line in info.splitlines() if line.startswith('flags:')),8)
  access_mode=flags & os.O_ACCMODE
  if expected and stat.S_ISREG(before.st_mode) and access_mode==os.O_RDONLY and sha(target)==expected:
   accepted.append({'fd':fd,'target':target,'sha256':expected,'access':'O_RDONLY','stage':stage})
  else:forbidden.append({'fd':fd,'target':target,'flags_octal':oct(flags),'stage':stage})
 if forbidden:raise AssertionError({'forbidden_descriptors':forbidden,'accepted':accepted,'vanished_scan_entries':vanished})
 return {'accepted_approved_runtime_descriptors':accepted,'vanished_scan_entries':vanished,'forbidden':[]}
before=audit('before_packet_parse')
packet=json.load(sys.stdin);sys.stdin.close();assert packet=={'mode':'fd_policy_validation','synthetic':True,'no_candidate_data':True}
after=audit('after_packet_parse')
print(json.dumps({'status':'PASS','packet_parsed':True,'before':before,'after':after,'exact_allowlist':APPROVED_TRANSIENT,'project_mount_absent':not Path('/working').exists() and not Path('/data').exists() and not Path('/mnt').exists(),'models_fit':0,'predictions':0,'candidate_data':False},separators=(',',':')))
