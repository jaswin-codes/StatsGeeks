"""Real-packet isolation probe ONLY. Constant status codes are not model predictions."""
import sys
sys.path.insert(0, '/numeric')
import gc
import hashlib
import json
import os
from pathlib import Path
import time

# Import-time access probes, before packet decoding.
for path in ['/mnt', '/home', '/run', '/data', '/working', '/proc/1/root/mnt', '/proc/1/root/home']:
    assert not Path(path).exists(), ('host path visible', path)
assert set(os.environ) <= {'LD_LIBRARY_PATH', 'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'HOME', 'PATH', 'LC_CTYPE', 'PWD'}, dict(os.environ)
assert os.environ.get('PWD') == '/tmp'
assert all('LABEL' not in k.upper() and 'EPISODE' not in k.upper() for k in os.environ)
for p in Path('/proc/self/fd').iterdir():
    try:
        target = os.readlink(p)
    except FileNotFoundError:
        continue
    assert int(p.name) <= 2, ('inherited descriptor', p.name, target)
    assert target.startswith('pipe:'), ('unexpected descriptor', target)

import ctypes
import numpy as np
import scipy
import sklearn
import narwhals
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
assert (np.__version__, scipy.__version__, sklearn.__version__, narwhals.__version__) == ('2.4.6', '1.17.1', '1.9.0', '2.25.0')
assert sys.version_info[:3] == (3, 14, 4)
assert all(m.__file__.startswith('/numeric/') for m in (np, scipy, sklearn, narwhals))
assert np.allclose(np.linalg.solve([[2., 0.], [0., 3.]], [4., 9.]), [2., 3.])

packet = json.load(sys.stdin)
sys.stdin.close()
assert set(packet) == {'X_source', 'y_source', 'X_support', 'y_support', 'support_ids', 'X_query', 'query_ids', 'parameters'}
assert np.asarray(packet['X_source']).shape == (76263, 60)
assert np.asarray(packet['y_source']).shape == (76263,)
assert np.asarray(packet['X_support']).shape == (len(packet['y_support']), 60)
assert np.asarray(packet['X_query']).shape == (len(packet['query_ids']), 60)
assert len(packet['y_support']) + len(packet['query_ids']) == 25992
assert all(isinstance(x, int) and x in (1, 2, 3, 4) for x in packet['y_support'])
# JSON produces builtins only: no executable pickle/reference graph crosses boundary.
def plain(x):
    if type(x) is dict:
        return all(type(k) is str and plain(v) for k, v in x.items())
    if type(x) is list:
        return all(plain(v) for v in x)
    return type(x) in (str, int, float, bool, type(None))
assert plain(packet)
for name in ('y_amsterdam', 'y_target', 'y_query', 'full_target_labels', 'other_episode_support_labels', 'evaluator'):
    assert name not in globals()
    for module in list(sys.modules.values()):
        if module is not None:
            assert name not in vars(module)
    for obj in gc.get_objects():
        if type(obj) is dict and name in obj:
            assert type(obj[name]) is str and obj[name] == name, 'Forbidden object reference'
for path in ['/tmp/gate4_prior_support', '/dev/shm/gate4_prior_support']:
    assert not Path(path).exists(), 'Persistent labelled state entered worker'
Path('/tmp/gate4_prior_support').write_text(json.dumps(packet['y_support']))
if Path('/dev/shm').is_dir():
    Path('/dev/shm/gate4_prior_support').write_text(json.dumps(packet['y_support']))
try:
    Path('/numeric/gate4_write_probe').write_text('x')
    raise AssertionError('Runtime writable')
except OSError:
    pass
# Same key description in all episodes: a previous support state must not recover.
libc = ctypes.CDLL(None, use_errno=True)
libc.syscall.restype = ctypes.c_long
keyring = libc.syscall(250, 0, -4, 1)
description = ctypes.c_char_p(b'gate4-production-probe-prior-support-v1')
if keyring >= 0:
    found = libc.syscall(250, 10, keyring, ctypes.c_char_p(b'user'), description, 0)
    assert found < 0, 'Cross-episode keyring state recovered'
    value = json.dumps(packet['y_support']).encode()
    added = libc.syscall(248, ctypes.c_char_p(b'user'), description, ctypes.c_char_p(value), len(value), keyring)
    if added >= 0:
        assert libc.syscall(250, 15, added, 15) == 0
# Exercise detached descendants: kernel PID namespace teardown must remove them.
if packet['parameters'].get('teardown_child'):
    pid = os.fork()
    if pid == 0:
        os.setsid()
        while True:
            time.sleep(1)
    time.sleep(.5)
if packet['parameters'].get('interrupt'):
    sys.stderr.write('GATE4_PROBE_READY\n')
    sys.stderr.flush()
    while True:
        time.sleep(1)
result = {'query_fingerprint': hashlib.sha256(json.dumps(packet['query_ids'], sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
          'predictions': [1] * len(packet['query_ids'])}
sys.stdout.write(json.dumps(result, separators=(',', ':')))
