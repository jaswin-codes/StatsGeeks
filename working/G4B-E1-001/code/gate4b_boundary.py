"""Gate 4B approved-code JSON boundary using certified runtime/lifecycle."""
import fcntl, hashlib, json, os, resource, selectors, signal, subprocess, time
from pathlib import Path
from gate4_lifecycle import Lifecycle
from gate4_production_boundary import runtime_check, canonical

APPROVED = {
    'preflight': 'bb5a3114ebfaa4cf0716d9cf4f4467c6682924c95ffd7fa631b40ca4b513e2f6',
    'source': '1d4eb63496d5161b953cd54deec6c1c2c506a703d0dcf2e8b8638d954aa0c03d',
    'episode': '05dcde156dfaf0fef67a6ac9f7e07f61801dee5496ded765a364abef7751524a',
}


def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0)); resource.setrlimit(resource.RLIMIT_AS,(6*1024**3,6*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(180,180)); resource.setrlimit(resource.RLIMIT_FSIZE,(64*1024**2,64*1024**2)); resource.setrlimit(resource.RLIMIT_NOFILE,(128,128))


def run(packet, code, role, output_limit=20_000_000, timeout=180):
    digest=hashlib.sha256(code).hexdigest()
    if APPROVED.get(role)!=digest: raise RuntimeError('Unapproved worker bytes')
    payload=canonical(packet); lock=runtime_check()
    fd=os.memfd_create('gate4b-approved-code',os.MFD_ALLOW_SEALING|os.MFD_CLOEXEC)
    os.write(fd,code);os.lseek(fd,0,0);fcntl.fcntl(fd,fcntl.F_ADD_SEALS,fcntl.F_SEAL_WRITE|fcntl.F_SEAL_GROW|fcntl.F_SEAL_SHRINK|fcntl.F_SEAL_SEAL)
    ir,iw=os.pipe(); cmd=['/usr/bin/bwrap','--unshare-all','--unshare-user','--disable-userns','--die-with-parent','--new-session','--cap-drop','ALL','--ro-bind',lock['image_path'],'/','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--chdir','/tmp','--clearenv','--tmpfs','/app','--ro-bind-data',str(fd),'/app/entry.py','--remount-ro','/app','--info-fd',str(iw)]
    for k,v in lock['sandbox_environment'].items():cmd += ['--setenv',k,v]
    cmd += ['--',lock['interpreter_path'],'-I','-B','/app/entry.py']
    lifecycle=Lifecycle(reap=True);started=time.monotonic();p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,pass_fds=(fd,iw),close_fds=True,start_new_session=True,preexec_fn=limits);lifecycle.attach(p.pid);os.close(fd);os.close(iw)
    sel=selectors.DefaultSelector(); streams=[(p.stdin,selectors.EVENT_WRITE,'in'),(p.stdout,selectors.EVENT_READ,'out'),(p.stderr,selectors.EVENT_READ,'err'),(ir,selectors.EVENT_READ,'info')]
    for s,e,n in streams:os.set_blocking(s if isinstance(s,int) else s.fileno(),False);sel.register(s,e,n)
    b={'out':bytearray(),'err':bytearray(),'info':bytearray()};offset=0;namespace=None;reason=None
    try:
      while sel.get_map():
        lifecycle.observe('streaming'); elapsed=time.monotonic()-started
        if reason is None and elapsed>timeout:
          reason='timeout'
          try:os.killpg(p.pid,signal.SIGKILL)
          except ProcessLookupError:pass
        if reason and elapsed>timeout+15:raise RuntimeError('Transport teardown deadline')
        for key,_ in sel.select(.05):
          s,n=key.fileobj,key.data;fileno=s if isinstance(s,int) else s.fileno()
          if n=='in':
            try:w=os.write(fileno,payload[offset:offset+65536]);offset+=w
            except BrokenPipeError:offset=len(payload)
            if offset==len(payload):sel.unregister(s);s.close()
          else:
            data=os.read(fileno,65536)
            if not data:
              sel.unregister(s);os.close(fileno) if isinstance(s,int) else s.close()
            else:
              b[n].extend(data)
              if n=='out' and len(b[n])>output_limit:
                reason='output_limit';os.killpg(p.pid,signal.SIGKILL)
              if n=='err' and len(b[n])>65536:
                reason='stderr_limit';os.killpg(p.pid,signal.SIGKILL)
              if n=='info' and namespace is None:
                try:
                  child=json.loads(b[n])['child-pid'];namespace=os.readlink(f'/proc/{child}/ns/pid');lifecycle.namespace=namespace;lifecycle.observe('namespace_created')
                except (ValueError,FileNotFoundError):pass
      lifecycle.observe('before_launcher_wait');rc=p.wait(timeout=10)
    finally:
      if p.poll() is None:
        try:os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        p.wait(timeout=10)
      for key in list(sel.get_map().values()):
        try:os.close(key.fd)
        except OSError:pass
      sel.close(); life=lifecycle.finish(p.returncode)
    evidence={'role':role,'code_sha256':digest,'packet_sha256':hashlib.sha256(payload).hexdigest(),'stdout_sha256':hashlib.sha256(b['out']).hexdigest(),'returncode':rc,'reason':reason,'stderr':b['err'].decode(errors='replace'),'elapsed_seconds':time.monotonic()-started,'namespace':namespace,'lifecycle':life,'teardown_pass':life['pass_'],'runtime_lock_sha256':'cbebbda8f2a2a470d3d639e51fdf63b24afa7c950044bbf6b35a81dc9c21b514'}
    if rc or reason or evidence['stderr'] or not life['pass_']:raise RuntimeError('Worker failed: '+json.dumps(evidence))
    return bytes(b['out']),evidence
