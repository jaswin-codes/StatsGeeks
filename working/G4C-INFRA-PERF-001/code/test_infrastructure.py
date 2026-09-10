"""No-worker tests. Uses synthetic bytes and compilation/static inspection only."""
import ast
import hashlib
import os
from pathlib import Path
import tempfile
import unittest

from immutable_io import sha256, signature_hex, stage_frozen_file
from prepare_assets import PROVEN, TRANSPORT_SOURCE, asset_bytes, bounded_coordinator, native_transport


class InfrastructureTests(unittest.TestCase):
    def test_signature_equivalence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input"
            for data in [b"", b"a", bytes(range(16)), bytes(range(256)) * 8192]:
                path.write_bytes(data)
                self.assertEqual(signature_hex(path), path.read_bytes()[:16].hex())

    def test_signature_reads_only_sixteen(self):
        import io
        from unittest.mock import patch
        stream = io.BytesIO(bytes(range(100)))
        class Tracked(io.BytesIO):
            def read(self, size=-1):
                if size != 16:
                    raise AssertionError("Unbounded signature read")
                return super().read(size)
        with patch.object(Path, "open", return_value=Tracked(stream.getvalue())):
            self.assertEqual(signature_hex(Path("unused")), bytes(range(16)).hex())

    def test_only_signature_function_changes(self):
        original = (PROVEN / "execution_coordinator.py").read_bytes()
        changed = bounded_coordinator(original)
        before, after = ast.parse(original), ast.parse(changed)
        b = {n.name: ast.dump(n) for n in before.body if isinstance(n, ast.FunctionDef)}
        a = {n.name: ast.dump(n) for n in after.body if isinstance(n, ast.FunctionDef)}
        self.assertEqual(set(a) - set(b), {"signature_hex"})
        self.assertEqual([name for name in b if b[name] != a[name]], ["preexisting_integrity"])
        self.assertIn(b"stream.read(16)", changed)

    def test_workers_and_boundaries_exact(self):
        assets = asset_bytes()
        for name in ("episode_worker.py", "source_worker.py", "preflight_worker.py",
                     "g4c_boundary.py", "gate4_lifecycle.py", "gate4_production_boundary.py"):
            self.assertEqual(assets[name], (PROVEN / name).read_bytes(), name)

    def test_transport_keeps_boundary_and_errors(self):
        new = native_transport(TRANSPORT_SOURCE.read_bytes()).decode()
        self.assertIn("run(packet,a.worker.read_bytes(),a.role,rf_path=a.rf)", new)
        self.assertIn("except BaseException:", new)
        self.assertIn("assert not a.output.exists()", new)
        self.assertIn("'boundary_evidence':evidence", new)
        self.assertIn("'infrastructure_io':native_record", new)
        self.assertNotIn("pickle.load", new)

    def test_transport_payload_equivalence_without_worker(self):
        import contextlib
        import io
        import json
        import sys
        import types
        from unittest.mock import patch
        from immutable_io import RF_SHA256
        calls = []
        boundary = types.ModuleType('g4c_boundary')
        def fake_run(packet, code, role, rf_path=None):
            calls.append((packet, code, role, rf_path))
            return b'{"synthetic":true}', {'teardown_pass': True, 'elapsed_seconds': 0.0}
        boundary.run = fake_run
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entry = root / 'g4c_linux_call.py'
            code = native_transport(TRANSPORT_SOURCE.read_bytes())
            packet_path, worker_path, output = root/'packet', root/'worker', root/'output'
            packet = {'parameters': {'candidate': 'E3'}, 'synthetic': True}
            packet_path.write_text(json.dumps(packet))
            worker_path.write_bytes(b'synthetic-worker-bytes-NOT-EXECUTED')
            (root/'native_cache.json').write_text(json.dumps({'directory': '/native/cache', 'rf_sha256': RF_SHA256}))
            argv = [str(entry), str(packet_path), str(worker_path), 'episode', str(output), '--rf', '/original/rf.pkl']
            with patch.dict(sys.modules, {'g4c_boundary': boundary}), patch.object(sys, 'argv', argv), \
                    patch('immutable_io.stage_frozen_file', return_value={'path': '/native/rf.pkl', 'sha256': RF_SHA256}) as stage, \
                    contextlib.redirect_stdout(io.StringIO()):
                exec(compile(code, str(entry), 'exec'), {'__name__': 'synthetic_transport_test', '__file__': str(entry)})
            self.assertEqual(calls, [(packet, worker_path.read_bytes(), 'episode', Path('/native/rf.pkl'))])
            self.assertEqual(json.loads(output.read_text())['result'], {'synthetic': True})
            self.assertEqual(stage.call_count, 1)

    def test_unknown_coordinator_rejected(self):
        with self.assertRaises(ValueError):
            bounded_coordinator(b"print('not approved')")

    @unittest.skipUnless(os.name == "posix", "Linux-native staging test")
    def test_native_atomic_staging_and_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.write_bytes(b"synthetic frozen bytes" * 4096)
            expected = sha256(source)
            result = stage_frozen_file(source, root / "cache", expected)
            destination = Path(result["path"])
            self.assertTrue(result["created"])
            self.assertEqual(destination.read_bytes(), source.read_bytes())
            self.assertFalse(stage_frozen_file(source, root / "cache", expected)["created"])
            self.assertFalse(destination.stat().st_mode & 0o222)
            self.assertFalse(list((root / "cache").glob(".stage-*")))

    @unittest.skipUnless(os.name == "posix", "Linux-native staging test")
    def test_corrupt_cache_fails_without_repair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.write_bytes(b"frozen")
            expected = sha256(source)
            result = stage_frozen_file(source, root / "cache", expected)
            destination = Path(result["path"])
            destination.chmod(0o600)
            destination.write_bytes(b"corrupt")
            with self.assertRaises(RuntimeError):
                stage_frozen_file(source, root / "cache", expected)
            self.assertEqual(destination.read_bytes(), b"corrupt")

    @unittest.skipUnless(os.name == "posix", "Linux-native staging test")
    def test_bad_source_never_published(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.write_bytes(b"wrong bytes")
            with self.assertRaises(RuntimeError):
                stage_frozen_file(source, root / "cache", hashlib.sha256(b"expected").hexdigest())
            self.assertFalse(list((root / "cache").glob("*.pkl")))

    @unittest.skipUnless(os.name == "posix", "Linux-native staging test")
    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.write_bytes(b"x")
            link = root / "link"
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                stage_frozen_file(link, root / "cache", sha256(target))


if __name__ == "__main__":
    unittest.main(verbosity=2)
