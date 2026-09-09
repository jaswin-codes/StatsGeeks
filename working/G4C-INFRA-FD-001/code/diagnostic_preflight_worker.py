"""Infrastructure-only FD origin diagnostic; synthetic packet, no modelling."""
import sys,os,json,time,hashlib
sys.path.insert(0,'/numeric')

def snapshot(stage):
    entries=os.listdir('/proc/self/fd');rows=[]
    for name in entries:
        try:
            target=os.readlink('/proc/self/fd/'+name);info=open('/proc/self/fdinfo/'+name).read()
            rows.append({'fd':int(name),'target':target,'fdinfo':info})
        except FileNotFoundError:rows.append({'fd':int(name),'target':'VANISHED_SCAN_DESCRIPTOR'})
    return {'stage':stage,'rows':rows,'modules':{k:True for k in ['ctypes','numpy','resource','pickle','warnings'] if k in sys.modules}}
records=[snapshot('entry_after_os_json_hashlib')]
import pathlib
records.append(snapshot('after_pathlib'))
import resource
records.append(snapshot('after_resource'))
import pickle,warnings
records.append(snapshot('after_pickle_warnings'))
import numpy as np
records.append(snapshot('immediately_after_numpy'))
for i in range(20):
    records.append(snapshot('numpy_settle_'+str(i)));time.sleep(.01)
packet=json.load(sys.stdin);sys.stdin.close();assert packet=={'mode':'fd_diagnostic_preflight','synthetic':True}
records.append(snapshot('after_packet_parse'))
maps=open('/proc/self/maps').read();libffi_maps=[line for line in maps.splitlines() if 'libffi' in line]
print(json.dumps({'status':'PASS','packet_parsed':True,'records':records,'libffi_maps':libffi_maps,'candidate_data':False,'models_fit':0,'predictions':0},separators=(',',':')))
