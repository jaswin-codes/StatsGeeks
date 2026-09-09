"""NPZ serialization forensics from saved arrays only. No prediction generation."""
import hashlib
import io
import json
from pathlib import Path
import platform
import struct
import sys
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[3]
CERT=Path(__file__).resolve().parents[1]
if sys.platform=='linux':
    lock=json.loads((ROOT/'working/gate4_runtime_narwhals_lock.json').read_text())
    sys.path.insert(0,lock['image_path']+'/numeric')
import numpy as np


def digest(raw):return hashlib.sha256(raw).hexdigest()


def describe(path):
    raw=Path(path).read_bytes();members=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for item in archive.infolist():
            payload=archive.read(item)
            stream=io.BytesIO(payload)
            version=np.lib.format.read_magic(stream)
            if version == (1, 0):
                shape,fortran,dtype=np.lib.format.read_array_header_1_0(stream)
            elif version == (2, 0):
                shape,fortran,dtype=np.lib.format.read_array_header_2_0(stream)
            else:
                raise ValueError('Unsupported NPY format: '+repr(version))
            offset=stream.tell();array_raw=stream.read()
            array=np.load(io.BytesIO(payload),allow_pickle=False)
            header=raw[item.header_offset:item.header_offset+30]
            name_len,extra_len=struct.unpack_from('<HH',header,26)
            data_start=item.header_offset+30+name_len+extra_len
            compressed=raw[data_start:data_start+item.compress_size]
            members.append({'name':item.filename,'npy_sha256':digest(payload),'npy_header_hex':payload[:offset].hex(),
                'npy_version':version,'fortran_order':fortran,'dtype':dtype.str,'shape':shape,
                'array_data_sha256':digest(array_raw),'array_data_bytes':len(array_raw),
                'array_c_order_sha256':digest(array.tobytes(order='C')),
                'zip':{key:getattr(item,key) for key in ['date_time','compress_type','compress_size','file_size','CRC','create_system',
                    'create_version','extract_version','reserved','flag_bits','volume','internal_attr','external_attr','header_offset']},
                'zip_extra_hex':item.extra.hex(),'zip_comment_hex':item.comment.hex(),
                'compressed_data_sha256':digest(compressed),'compressed_data_offset':data_start})
        comment=archive.comment.hex()
    return {'path':str(path),'bytes':len(raw),'sha256':digest(raw),'member_order':[m['name'] for m in members],
            'zip_comment_hex':comment,'members':members}


def main():
    original=ROOT/'working/G4C-E3-001/predictions/G4A-B005-T01.npz'
    platform_name='linux' if sys.platform=='linux' else 'windows'
    with np.load(original,allow_pickle=False) as saved:
        arrays={key:saved[key].copy(order='K') for key in saved.files}
    paths=[]
    for i in (1,2):
        target=CERT/'evidence'/f'reserialized_{platform_name}_{i}.npz'
        if not target.exists():
            with target.open('xb') as stream:np.savez_compressed(stream,**arrays)
        paths.append(target)
    descriptions=[describe(original)]+[describe(p) for p in paths]
    reference=original.read_bytes();repacked=paths[0].read_bytes()
    offsets=[i for i,(a,b) in enumerate(zip(reference,repacked)) if a!=b]
    record={'platform':platform.platform(),'python':sys.version,'numpy':np.__version__,
            'zlib_compile':zlib.ZLIB_VERSION,'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,
            'writer':'np.savez_compressed(file_object, **ordered_arrays)',
            'numpy_writer_source_sha256':digest(Path(np.lib._npyio_impl.__file__).read_bytes()),
            'zipfile_source_sha256':digest(Path(zipfile.__file__).read_bytes()),
            'descriptions':descriptions,'length_difference':len(repacked)-len(reference),
            'byte_differences':[{'offset':i,'original':reference[i],'reserialized':repacked[i]} for i in offsets],
            'repeat_byte_identity':paths[0].read_bytes()==paths[1].read_bytes(),
            'models_loaded':0,'workers_launched':0,'predictions_computed':0}
    with (CERT/'evidence'/f'npz_forensics_{platform_name}.json').open('x',encoding='utf8') as f:
        json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps({'platform':platform_name,'archives':[{k:d[k] for k in ('path','bytes','sha256')} for d in descriptions],
                      'changed_bytes':record['byte_differences'],'repeat_identical':record['repeat_byte_identity']},indent=2))


if __name__=='__main__':main()
