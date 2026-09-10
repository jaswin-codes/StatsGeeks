# G4C infrastructure FD isolation validation 001 — PASS

## Status

**WORKER ISOLATION VERIFIED**  
**READY FOR E2 EXECUTION**

This was infrastructure-only validation. No E2 episode, candidate worker, model fit, prediction, or metric was executed.

## Exact source of descriptor 3

A synthetic isolated diagnostic worker sampled `/proc/self/fd` at controlled import stages:

| Stage | Persistent fd > 2 | Relevant modules |
|---|---|---|
| Entry after `os/json/hashlib` | None; scan fd vanished | no `ctypes`, no NumPy |
| After `pathlib` | None | no `ctypes`, no NumPy |
| After `resource` | None | no `ctypes`, no NumPy |
| After `pickle/warnings` | None | no `ctypes`, no NumPy |
| Immediately after NumPy import | fd 3 → `libffi.so.8` | NumPy and `ctypes` loaded |
| 20 samples over 200 ms | same fd 3 | same |
| After synthetic packet parse | same fd 3 | same |

`/proc/self/maps` simultaneously showed the approved `libffi.so.8` mappings. Therefore fd 3 was **not inherited from Bubblewrap** and was **not present at Python startup**. It was opened inside the worker during NumPy import: NumPy loads Python's `ctypes` support, and the ELF dynamic-loading path maps its libffi dependency.

Exact target:

```text
/usr/lib/x86_64-linux-gnu/libffi.so.8
```

SHA256:

```text
1a0dc86f787f73e025a6e521056360afcbe70f2a82cd808132fefc2b4ee95daa
```

This exactly matches the declared native source in the frozen approved runtime inventory. Descriptor flags were octal `02100000`: access mode `O_RDONLY` with `O_CLOEXEC`; position was zero. It was not a socket, pipe, writable project file, packet file, label channel, or external mount.

## Safety decision

The descriptor is legitimate approved-runtime state. Accepting it does not create an information path because acceptance requires all of:

1. exact absolute sandbox target path;
2. exact frozen SHA256;
3. regular file;
4. read-only access mode;
5. stable descriptor identity while inspected.

The file is inside the read-only approved runtime image and already covered by the runtime lock. A descriptor matching only its number is **not** accepted.

## Exact validation-policy change

Old rule:

```text
Every descriptor number greater than 2 is forbidden.
```

New narrowly scoped rule:

```text
Descriptors 0–2 remain expected standard streams.
For fd > 2:
  - tolerate and log a descriptor that vanished because /proc/self/fd was itself scanned;
  - accept only the exact hash-pinned, regular, O_RDONLY approved libffi path above;
  - reject every other persistent descriptor.
```

There is no directory prefix, runtime-wide wildcard, library-extension rule, arbitrary read-only-file exception, or fd-number exception. The policy is implemented only in the new validation worker. Historical candidate workers and failed runs were not edited.

## Preflight and validation workers

### Diagnostic preflight

- Synthetic packet only.
- NumPy import reproduced fd 3.
- Packet parsing reached successfully while fd 3 was present.
- Project/data mounts absent from the sandbox.
- Return code 0.
- Teardown PASS; final survivors empty.

### Single policy-validation worker

- One synthetic validation worker launched after implementing the policy.
- Synthetic packet parsed successfully.
- Forbidden descriptors before parse: none.
- Forbidden descriptors after parse: none.
- `/proc/self/fd` scan entries that vanished were logged, not confused with inherited handles.
- Project/data mounts absent.
- Return code 0.
- Teardown PASS; adopted namespace process reaped; final survivors empty.

The validation worker did not import NumPy, so its accepted-libffi list was empty. The separate diagnostic preflight exercised the real NumPy/libffi descriptor and its recorded path/hash/flags satisfy the exact policy predicate. No claim is made that an E2 worker was launched.

## Isolation guarantees

Unchanged:

- approved runtime and Bubblewrap namespace;
- no project/data/manifest mounts;
- sealed worker code;
- synthetic stdin packet only;
- clear environment and private tmpfs;
- dedicated subreaper and PID/start-tick tracking;
- zombies count as survivors;
- successful return and complete reaping required before output finalization;
- all non-allowlisted descriptors remain fatal.

The policy changes descriptor validation only; it does not alter candidate packets, labels, model definitions, parameters, runtime versions, preprocessing, frozen RF, episode manifest, or prediction finalization.

## Scientific non-execution and integrity

| Item | Result |
|---|---:|
| Infrastructure workers | 2 (diagnostic + validation) |
| Candidate workers | 0 |
| Experiment episodes | 0 |
| Candidate data processed | No |
| Models fitted | 0 |
| Predictions generated | 0 |
| Metrics generated | 0 |
| Protected files | 33/33 unchanged |
| Frozen manifest/RF | unchanged |
| `original/` | clean |
| G4C-E2-004 evidence | hash inventory unchanged |

An initial infrastructure-launcher attempt had a generated string-literal syntax error and launched no worker. The malformed newline was corrected only in the newly created infrastructure launcher; the failure is retained in `evidence/launcher_attempt1_failure.json`. No candidate or historical file was repaired or retried.

## Artifacts

- `code/diagnostic_preflight_worker.py`
- `code/validation_worker.py`
- `code/infra_boundary.py`
- `code/infra_call.py`
- `evidence/diagnostic_result.json`
- `evidence/validation_result.json`
- `validation_summary.json`
- `artifact_hash_manifest.json`

A future E2 execution requires a new run identity and separately pinned episode-worker bytes incorporating this exact descriptor predicate. This task grants no experiment execution.
