"""Prove the DEFLATE stream origin independently from NumPy array writing."""
import hashlib
import inspect
import io
import json
from pathlib import Path
import struct
import sys
import zipfile
import zlib

CERT=Path(__file__).resolve().parents[1]
platform='windows' if sys.platform=='win32' else 'linux'
path=CERT/'evidence'/f'reserialized_{platform}_1.npz'
raw=path.read_bytes();results=[]
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    for member in archive.infolist():
        payload=archive.read(member)
        compressor=zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION,zlib.DEFLATED,-15)
        independently_compressed=compressor.compress(payload)+compressor.flush()
        n,e=struct.unpack_from('<HH',raw,member.header_offset+26)
        start=member.header_offset+30+n+e
        recorded=raw[start:start+member.compress_size]
        results.append({'member':member.filename,'npy_sha256':hashlib.sha256(payload).hexdigest(),
            'raw_deflate_sha256':hashlib.sha256(recorded).hexdigest(),
            'independent_compression_sha256':hashlib.sha256(independently_compressed).hexdigest(),
            'exact_stream_match':recorded==independently_compressed})
assert all(r['exact_stream_match'] for r in results),'Compression settings require further diagnosis'
record={'platform':platform,'zlib_compile':zlib.ZLIB_VERSION,'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,
        'compression_level':zlib.Z_DEFAULT_COMPRESSION,'method':zlib.DEFLATED,'wbits':-15,
        'zipfile_default_compressor_source':inspect.getsource(zipfile._get_compressor),
        'members':results,'status':'EXACT_DEFLATE_STREAM_REPRODUCTION_PASS'}
with (CERT/'evidence'/f'compression_proof_{platform}.json').open('x',encoding='utf8') as f:json.dump(record,f,indent=2);f.write('\n')
print(platform,record['status'],len(results),'members',zlib.ZLIB_RUNTIME_VERSION)
