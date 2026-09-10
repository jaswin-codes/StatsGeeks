# Gate 4A — existing Narwhals provenance investigation

## Decision

**Exact local wheel candidate recovered; intended pinned-runtime approval NOT established.**
Gate 4A remains **BLOCKED**. No package was downloaded, imported as a fallback,
staged or installed. No runtime/infrastructure/episode/model execution occurred.

The recovered candidate is **Narwhals 2.25.0**, original wheel filename
`narwhals-2.25.0-py3-none-any.whl`, **467,373 bytes**, SHA256:

`1f0f403e8c7e4463cde9bfe78b12fdd809e3ae3dda6d9b2f802934fb9c7a6a8f`

This is an existing artifact, not a version selected from the lower bound or a
new online lookup. Only one actual Narwhals wheel/version was found. Three
installed copies of that same version were also found; none was selected as a
runtime fallback.

## Exact local wheel provenance

Wheel bytes are preserved in their existing pip HTTP-cache location (not copied
or renamed):

```text
C:\Users\jaswi\AppData\Local\pip\Cache\http-v2\0\5\2\8\0\05280cda432a199e99befa1378983526a79ebfe8f09c7acb977a04c6.body
```

Evidence chain, all obtained offline:

1. The body is a ZIP wheel containing `narwhals-2.25.0.dist-info/METADATA`,
   `WHEEL` and `RECORD`. METADATA identifies version 2.25.0. WHEEL declares
   `py3-none-any` and `Generator: uv 0.12.5`.
2. The adjacent pip cache-response metadata identifies project `narwhals`, version
   `2.25.0`, content length 467373 and response date `Tue, 08 Sep 2026 08:29:37 GMT`.
   Response dates are provenance context, **not approval evidence**.
3. The existing compressed simple-index cache body below contains the exact
   filename, URL and SHA256 matching the actual cached wheel bytes:

```text
C:\Users\jaswi\AppData\Local\pip\Cache\http-v2\d\2\c\4\b\d2c4b2b07925b23b24c2df1f4d305788e1dfbc96ef47bf4aa54692f3.body
```

   Cached-index body SHA256:
   `d0d14544781e97a5535be8e87c04f3e8373dc66eb6239d289dc92593848b6127`.
   Its filename is therefore **recovered from existing metadata**, not merely
   synthesized from package version and compatibility tags. The cached URL is:

```text
https://files.pythonhosted.org/packages/eb/dc/55481808fd70ef1567cf13540ffd4702af3f74b112e35427564b03f79c2d/narwhals-2.25.0-py3-none-any.whl
```

   This URL was **not requested**. SHA224 of this existing URL equals the pip
   cache key `05280cda432a199e99befa1378983526a79ebfe8f09c7acb977a04c6`, independently
   connecting the cached response body to that filename/URL.
4. Wheel SHA256 was calculated with Python hashlib and independently recomputed
   using PowerShell `Get-FileHash`/.NET. Both equal the cached index's SHA256 above.

## Installed candidates and their relationship to the wheel

Each installation contains `narwhals-2.25.0.dist-info`, with `INSTALLER=pip` and no
`direct_url.json` or `REQUESTED` file. All **166 non-directory, non-RECORD wheel
members** match the installed bytes exactly in each location. All **167 hashed
installed RECORD entries** validate in each installation.

| Existing installation | Version | Installed RECORD SHA256 |
|---|---|---|
| `C:\Users\jaswi\AppData\Roaming\Python\Python311\site-packages` | 2.25.0 | `a7637a6a16988003b727b69e4c5c14e58a4980a339d00357f89982eb71a9c0f9` |
| `C:\Users\jaswi\AppData\Roaming\Python\Python314\site-packages` | 2.25.0 | `6fce1abbe586fdf43ab969093b27dbf04823130461613f89e21c7b1b4882ad26` |
| Project `.venv_baseline\Lib\site-packages` | 2.25.0 | `6fce1abbe586fdf43ab969093b27dbf04823130461613f89e21c7b1b4882ad26` |

Common METADATA SHA256:
`7fd4dedd283bf242b7d04fff6979e25ba9d98da1d3ee3703001908dc8f854a1b`.
Common WHEEL metadata SHA256:
`e0e2fa168aa79e9df1458e703248e0736e7f8b96090ba74ab02e8b3dc8ea1285`.

The common canonical installed member-tree SHA256 is
`0de98d382847d6ebbc73be8e9344d07d0849717d703bcc2e75cb29937b456bbc`.
Encoding: SHA256 of sorted-key compact JSON mapping sorted non-directory,
non-RECORD wheel member paths to their file SHA256 values. It is **not a wheel
hash**. No installed tree was repackaged into a purported original wheel.

All three installations also contain scikit-learn 1.9.0, whose existing metadata
requires `narwhals>=2.0.1`. Its METADATA SHA256 is
`ee61a579f42d3edabe3e483db483475e33fffec04d7f3e69c539527bd93eaca6`.

## What this does and does not prove

**Proven:** An exact wheel/version/hash exists locally, matches its cached index
record, and matches the current Narwhals contents in three environments including
the Windows Python 3.11 user site associated with the accepted baseline interpreter.

**Not proven:** That Narwhals 2.25.0 was explicitly selected/approved for the intended
Gate 4 Linux pinned environment, or that an immutable baseline-time record pinned
this exact dependency. Baseline manifests record Python/NumPy/SciPy/sklearn, but
not Narwhals. Current installation state and an earlier cache-response date are
not equivalent to an approved historical dependency lock.

The project `.venv_baseline` also records Python **3.14.6**, whereas accepted baseline
metadata names Python **3.11.9** and Gate 4's isolated interpreter is **3.14.4**.
Its name alone therefore cannot establish it as the accepted pinned runtime.
`Generator: uv 0.12.5` is wheel-build provenance; it does not prove a local Astral
installation selected/approved this package. Installed `INSTALLER` says pip.

The Gate 4 lock and provisioner still pin only NumPy, SciPy, scikit-learn, joblib
and threadpoolctl. Their `.pre_*` archives contain no exact Narwhals pin. Thus
**an exact approved Gate 4 Narwhals artifact cannot yet be established**. This
investigation must not silently add the recovered candidate to that lock.

## Search scope and limitations

- Repository documents, provisioning/validation logs, locks/manifests, `.pre_*`
  archives and all reachable Git history (one initial commit, including notebook
  text): no historical exact Narwhals approval found.
- Windows Python installations/user sites, project virtual environment, Downloads,
  pip HTTP/wheel caches, uv cache, `.cache/codex-runtimes`, and temporary download
  directories. Cached compressed simple-index responses were decoded **locally**.
- Existing WSL Gate 4 staging/cache trees, `/usr/lib/python3`, `/usr/local/lib`,
  `/opt`, and WSL user caches: no Narwhals artifact found; WSL pip/uv cache
  directories are absent.
- No additional Narwhals version/wheel was found in those accessible sources.
  The cached index includes historical release listings; these are not locally
  present wheel candidates and were not used to choose a version.
- One inaccessible Windows temporary directory and ten unrelated long-path WASM
  file-read failures in Codex's Node artifacts are recorded in the JSON log. This
  is not a claim to have exhaustively searched every protected machine directory.

## Protection and changes

Only these investigation logs were created/updated:
- `working/gate4_narwhals_provenance.json`
- `working/gate4_narwhals_provenance.md`

All **33 protected hashes** match before/after. original/ remains Git-clean;
`original/Open Notebook.onetoc2` retains `A R`. The pinned runtime's **4,188 files**
and its **five source wheels** still match the existing lock. No baseline,
package cache, runtime, package metadata, isolation code, sampler or episode
manifest was intentionally modified. No Narwhals import/fallback, package download,
staging/install, model execution, E1, real episode or Notebook 4 rerun occurred.

## Exact next decision

Team Lead must decide whether to approve the **recovered existing**
`narwhals-2.25.0-py3-none-any.whl` with SHA256
`1f0f403e8c7e4463cde9bfe78b12fdd809e3ae3dda6d9b2f802934fb9c7a6a8f`
for the intended pinned runtime, or provide stronger historical approval evidence.
No version has been selected on the lead's behalf. STOP; do not stage it under
this read-only investigation authorisation.
