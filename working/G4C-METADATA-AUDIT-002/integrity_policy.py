"""Audit-only reference policy; never imports candidate code or loads modelling data.
Not installed in any experiment runner. Exact allowlist, not extension filtering.
"""
from pathlib import Path
import hashlib, stat
MUTABLE_PATH='working/Open Notebook.onetoc2'
TOC_SIGNATURE=bytes.fromhex('a12fff43d9ef764c9ee210ea5722765f')
def fingerprint(root,relative):
    p=Path(root)/relative
    before=p.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_file_attributes & 0x400:
        raise ValueError('Nonregular/reparse path: '+relative)
    if before.st_nlink!=1:raise ValueError('Hard-linked file: '+relative)
    with p.open('rb') as f:
        signature=f.read(16);f.seek(0);digest=hashlib.file_digest(f,'sha256').hexdigest()
    after=p.lstat()
    if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
        raise ValueError('File changed during hash: '+relative)
    return {'sha256':digest,'bytes':after.st_size,'mtime_ns':after.st_mtime_ns,'file_id':after.st_ino,'attributes':after.st_file_attributes,'signature_hex':signature.hex(),'regular':True,'links':after.st_nlink}
def classify(before,after):
    """Compare supplied maps; caller must enumerate ALL checkpoint paths, not a filter."""
    failures=[];allowed=[]
    for p,old in before.items():
        new=after.get(p)
        if new is None:failures.append({'path':p,'reason':'missing checkpoint file'});continue
        if old==new:continue
        if p!=MUTABLE_PATH:
            failures.append({'path':p,'reason':'non-allowlisted fingerprint change'});continue
        if not new.get('regular') or new.get('links')!=1 or new.get('attributes',0)&0x400:
            failures.append({'path':p,'reason':'metadata type/link violation'});continue
        if new.get('signature_hex')!=TOC_SIGNATURE.hex():
            failures.append({'path':p,'reason':'metadata signature changed'});continue
        if new.get('attributes')!=old.get('attributes') or new.get('file_id')!=old.get('file_id'):
            failures.append({'path':p,'reason':'metadata identity/attribute changed'});continue
        allowed.append({'path':p,'before':old,'after':new})
    return {'pass':not failures,'failures':failures,'allowed_metadata_changes':allowed}
