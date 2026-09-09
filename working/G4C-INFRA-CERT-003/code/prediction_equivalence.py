"""Strict E3 NPZ scientific-payload identity PLUS explicit artifact provenance.

No tolerant comparison, pickle loading, prediction generation, or scoring changes.
Complete archive SHA256 checks remain mandatory against each artifact's own bound
record. Cross-implementation ZIP identity is an additional, separately reported
check; producer-side replay in this certification must also satisfy it.
"""
from dataclasses import dataclass
import hashlib
import io
from pathlib import Path
import zipfile
import numpy as np

NAMES = ('query_indices', 'query_ids', 'raw_prototype', 'rf_reproduced', 'candidate', 'frozen_rf')
MEMBERS = tuple(name+'.npy' for name in NAMES)


class EquivalenceError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise EquivalenceError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Artifact:
    owner_root: Path
    relative_path: str
    episode_id: str
    sha256: str


def artifact_bytes(artifact, expected_owner, episode_id):
    root = Path(artifact.owner_root).absolute()
    need(root == Path(expected_owner).absolute(), 'Cross-run owner reference')
    need(root.resolve() == root and not root.is_symlink(), 'Noncanonical owner root')
    need(artifact.episode_id == episode_id, 'Wrong bound episode identity')
    relative = Path(artifact.relative_path)
    need(not relative.is_absolute() and '..' not in relative.parts and ':' not in artifact.relative_path,
         'Unsafe artifact reference')
    path = root
    for part in relative.parts:
        path = path/part
        need(not path.is_symlink(), 'Symlink artifact forbidden')
    need(path.resolve().is_relative_to(root) and path.name == episode_id+'.npz', 'Wrong bound prediction path')
    raw = path.read_bytes()
    need(sha(raw) == artifact.sha256, 'Artifact/provenance SHA256 mismatch')
    return raw


def payload(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = archive.infolist()
        need(tuple(m.filename for m in members) == MEMBERS, 'Missing/extra/reordered/duplicate NPZ members')
        arrays, serialized = {}, {}
        for name, member in zip(NAMES, members):
            need(not member.is_dir() and not member.flag_bits & 1, 'Invalid encrypted/directory member')
            data = archive.read(member)  # ZIP CRC is checked on read.
            stream = io.BytesIO(data)
            array = np.load(stream, allow_pickle=False)
            need(isinstance(array, np.ndarray) and not array.dtype.hasobject, 'Unsafe NPY payload')
            need(stream.tell() == len(data), 'Trailing data in NPY member')
            required_dtype = '<i4' if name == 'query_ids' else '<i8'
            need(array.dtype.str == required_dtype, 'Changed/non-protocol dtype: '+name)
            arrays[name], serialized[name] = array, data
    count = len(arrays['query_indices'])
    need(arrays['query_indices'].shape == (count,), 'Invalid query-index shape')
    need(arrays['query_ids'].shape == (count, 2), 'Invalid identifier shape')
    need(len(np.unique(arrays['query_indices'])) == count, 'Duplicate example row')
    need(len(np.unique(arrays['query_ids'], axis=0)) == count, 'Duplicate example identifier')
    for name in NAMES[2:]:
        need(arrays[name].shape == (count,), 'Changed prediction shape: '+name)
        need(np.isin(arrays[name], [1,2,3,4]).all(), 'Invalid class label: '+name)
    return arrays, serialized


def compare_bytes(reference_raw, candidate_raw):
    """Exact value/dtype/shape/order AND decompressed NPY-byte comparisons."""
    reference, ref_npy = payload(reference_raw)
    candidate, cand_npy = payload(candidate_raw)
    details = {}
    for name in NAMES:
        a, b = reference[name], candidate[name]
        need(a.dtype.str == b.dtype.str, 'Dtype disagreement: '+name)
        need(a.shape == b.shape, 'Shape disagreement: '+name)
        need(np.array_equal(a, b), 'Exact value/example-order disagreement: '+name)
        need(a.tobytes(order='C') == b.tobytes(order='C'), 'Array byte disagreement: '+name)
        need(ref_npy[name] == cand_npy[name], 'Serialized NPY metadata/order disagreement: '+name)
        details[name] = {'dtype': a.dtype.str, 'shape': list(a.shape), 'values_compared': int(a.size),
                         'mismatches': 0, 'maximum_absolute_difference': 0,
                         'dtype_equal': True, 'shape_equal': True, 'order_equal': True,
                         'serialized_npy_sha256': sha(ref_npy[name]),
                         'array_bytes_sha256': sha(a.tobytes(order='C'))}
    return {'payload_status': 'EXACT_MATCH', 'archive_bytes_equal': reference_raw == candidate_raw,
            'reference_archive_sha256': sha(reference_raw), 'candidate_archive_sha256': sha(candidate_raw),
            'member_order_equal': True, 'identifiers_equal': True, 'class_labels_equal': True,
            'prediction_elements_compared': sum(reference[n].size for n in NAMES[2:]),
            'candidate_predictions_compared': int(reference['candidate'].size), 'arrays': details}


def compare_artifacts(reference, candidate, *, reference_owner, candidate_owner, episode_id):
    a = artifact_bytes(reference, reference_owner, episode_id)
    b = artifact_bytes(candidate, candidate_owner, episode_id)
    result = compare_bytes(a, b)
    result.update(episode_id=episode_id, provenance_status='BOUND_HASHES_AND_OWNERS_VERIFIED')
    return result
