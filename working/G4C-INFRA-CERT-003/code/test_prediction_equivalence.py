"""Exact payload/provenance negative controls; saved arrays only, no inference."""
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile
import numpy as np
from prediction_equivalence import Artifact, EquivalenceError, MEMBERS, NAMES, compare_artifacts, compare_bytes

ROOT=Path(__file__).resolve().parents[3]
EP='G4A-B005-T01'


def pack(arrays):
    stream=io.BytesIO();np.savez_compressed(stream,**arrays);return stream.getvalue()


class PayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference=(ROOT/f'working/G4C-E3-001/predictions/{EP}.npz').read_bytes()
        with np.load(io.BytesIO(cls.reference),allow_pickle=False) as saved:
            cls.original={k:saved[k].copy() for k in saved.files}
    def arrays(self):return {k:a.copy() for k,a in self.original.items()}
    def rejects(self,arrays):
        with self.assertRaises((EquivalenceError,ValueError)):
            compare_bytes(self.reference,pack(arrays))
    def test_valid_exact_payload(self):
        r=compare_bytes(self.reference,pack(self.arrays()));self.assertEqual(r['payload_status'],'EXACT_MATCH')
    def test_change_prediction_value(self):
        a=self.arrays();a['candidate'][0]=a['candidate'][0]%4+1;self.rejects(a)
    def test_change_class_label(self):
        a=self.arrays();a['candidate'][0]=5;self.rejects(a)
    def test_class_mapping_permutation(self):
        a=self.arrays();a['candidate']=5-a['candidate'];self.rejects(a)
    def test_prediction_order(self):
        a=self.arrays();b=a['candidate'];i=int(np.flatnonzero(b!=b[0])[0]);b[0],b[i]=b[i],b[0];self.rejects(a)
    def test_example_identifier(self):
        a=self.arrays();a['query_ids'][0,0]+=1;self.rejects(a)
    def test_remove_array(self):
        a=self.arrays();del a['raw_prototype'];self.rejects(a)
    def test_extra_array(self):
        a=self.arrays();a['extra']=np.array([1]);self.rejects(a)
    def test_dtype(self):
        a=self.arrays();a['candidate']=a['candidate'].astype(np.int32);self.rejects(a)
    def test_endianness(self):
        a=self.arrays();a['candidate']=a['candidate'].astype('>i8');self.rejects(a)
    def test_shape(self):
        a=self.arrays();a['candidate']=a['candidate'][:,None];self.rejects(a)
    def test_all_example_order(self):
        self.rejects({k:a[::-1].copy() for k,a in self.arrays().items()})
    def test_member_order(self):
        a=self.arrays();self.rejects(dict(reversed(list(a.items()))))
    def test_npy_storage_order(self):
        a=self.arrays();a['query_ids']=np.asfortranarray(a['query_ids']);self.rejects(a)
    def test_nan(self):
        a=self.arrays();a['candidate']=a['candidate'].astype(float);a['candidate'][0]=np.nan;self.rejects(a)
    def test_inf(self):
        a=self.arrays();a['candidate']=a['candidate'].astype(float);a['candidate'][0]=np.inf;self.rejects(a)
    def test_pickle_object_array(self):
        a=self.arrays();a['candidate']=a['candidate'].astype(object);self.rejects(a)
    def test_duplicate_zip_member(self):
        target=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.reference)) as source,zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as out:
            for name in source.namelist():out.writestr(name,source.read(name))
            with warnings.catch_warnings():
                warnings.simplefilter('ignore');out.writestr(MEMBERS[0],source.read(MEMBERS[0]))
        with self.assertRaises(EquivalenceError):compare_bytes(self.reference,target.getvalue())
    def test_container_metadata_does_not_fake_file_identity(self):
        target=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.reference)) as source,zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as out:
            for name in source.namelist():
                info=zipfile.ZipInfo(name,date_time=(2001,2,3,4,5,6));info.compress_type=zipfile.ZIP_DEFLATED
                out.writestr(info,source.read(name))
        r=compare_bytes(self.reference,target.getvalue());self.assertFalse(r['archive_bytes_equal']);self.assertEqual(r['payload_status'],'EXACT_MATCH')
    def test_repeat_serialization_deterministic(self):
        self.assertEqual(pack(self.arrays()),pack(self.arrays()))
    def test_cross_run_substitution_even_identical_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp).resolve();ref=root/'reference';expected=root/'current';other=root/'other'
            for p in (ref,expected,other):p.mkdir();(p/(EP+'.npz')).write_bytes(self.reference)
            h=hashlib.sha256(self.reference).hexdigest()
            a=Artifact(ref,EP+'.npz',EP,h);b=Artifact(other,EP+'.npz',EP,h)
            with self.assertRaises(EquivalenceError):
                compare_artifacts(a,b,reference_owner=ref,candidate_owner=expected,episode_id=EP)
    def test_artifact_hash_remains_required(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp).resolve();(root/(EP+'.npz')).write_bytes(self.reference)
            a=Artifact(root,EP+'.npz',EP,hashlib.sha256(self.reference).hexdigest());bad=Artifact(root,EP+'.npz',EP,'0'*64)
            with self.assertRaises(EquivalenceError):
                compare_artifacts(a,bad,reference_owner=root,candidate_owner=root,episode_id=EP)
    def test_bound_episode_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp).resolve();(root/(EP+'.npz')).write_bytes(self.reference)
            h=hashlib.sha256(self.reference).hexdigest();a=Artifact(root,EP+'.npz',EP,h);b=Artifact(root,EP+'.npz','G4A-B005-T02',h)
            with self.assertRaises(EquivalenceError):compare_artifacts(a,b,reference_owner=root,candidate_owner=root,episode_id=EP)


if __name__=='__main__':unittest.main(verbosity=2)
