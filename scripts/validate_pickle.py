"""Clean-session validation of the reference preprocessed pickle.

Run from the repository root with a FRESH interpreter (no notebook kernel state):
    python validate_pickle.py

Checks the Member 2 feature contract from docs/member2_mission.md and the
validation checklist in docs/BASELINE_EXECUTION_PLAN.md. Read-only: it never
writes to the pickle or the raw data.
"""

import hashlib
import pickle
import sys
from pathlib import Path

import numpy as np

PKL = Path("data/preprocessed/preprocessed_data.pkl")

EXPECTED_MADRID = (76263, 60)
EXPECTED_AMSTERDAM = (25992, 60)
EXPECTED_N_FEATURES = 60

BASE_BANDS = ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]
INDEX_COLS = ["NDVI", "NDBI", "UI", "MNDWI", "BSI"]

# The exact ordered schema Notebook 3 builds: 12 overall + 10 indices
# + 12 early + 12 late + 12 yoy + 2 indicators.
EXPECTED_FEATURES = (
    [f"{b}_mean" for b in BASE_BANDS]
    + [f"{b}_std" for b in BASE_BANDS]
    + [f"{i}_mean" for i in INDEX_COLS]
    + [f"{i}_std" for i in INDEX_COLS]
    + [f"{b}_early_mean" for b in BASE_BANDS]
    + [f"{b}_early_std" for b in BASE_BANDS]
    + [f"{b}_late_mean" for b in BASE_BANDS]
    + [f"{b}_late_std" for b in BASE_BANDS]
    + [f"d_{b}_mean" for b in BASE_BANDS]
    + [f"d_{b}_std" for b in BASE_BANDS]
    + ["has_early_data", "has_late_data"]
)

results = []


def check(name, passed, detail=""):
    results.append((name, bool(passed), detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


print("=" * 72)
print("REFERENCE PICKLE VALIDATION (clean session)")
print("=" * 72)

if not PKL.exists():
    print(f"FATAL: {PKL} does not exist. Notebook 3 has not produced it.")
    sys.exit(2)

size_mb = PKL.stat().st_size / 1024 / 1024
h = hashlib.sha256()
with PKL.open("rb") as fh:
    for chunk in iter(lambda: fh.read(1024 * 1024), b""):
        h.update(chunk)
print(f"\nArtifact : {PKL}")
print(f"Size     : {size_mb:.1f} MB")
print(f"SHA256   : {h.hexdigest()}\n")

print("Reloading in this clean interpreter...")
with PKL.open("rb") as f:
    data = pickle.load(f)
check("Pickle reloads in a clean session", True, f"{len(data)} top-level keys")

print("\n-- Keys --")
expected_keys = {
    "X_madrid", "y_madrid", "X_amsterdam", "y_amsterdam",
    "feature_names", "scaler", "pixel_ids_madrid", "pixel_ids_amsterdam",
    "feat_groups",
}
missing = expected_keys - set(data)
check("All expected keys present", not missing, f"missing={sorted(missing)}" if missing else "")

Xm, ym = data["X_madrid"], data["y_madrid"]
Xa, ya = data["X_amsterdam"], data["y_amsterdam"]
feats = list(data["feature_names"])

print("\n-- Shapes --")
check("Madrid X shape", Xm.shape == EXPECTED_MADRID, f"got {Xm.shape}, expected {EXPECTED_MADRID}")
check("Amsterdam X shape", Xa.shape == EXPECTED_AMSTERDAM, f"got {Xa.shape}, expected {EXPECTED_AMSTERDAM}")
check("Madrid y length matches X rows", len(ym) == Xm.shape[0], f"y={len(ym)} X={Xm.shape[0]}")
check("Amsterdam y length matches X rows", len(ya) == Xa.shape[0], f"y={len(ya)} X={Xa.shape[0]}")

print("\n-- Feature schema --")
check("Feature count is 60", len(feats) == EXPECTED_N_FEATURES, f"got {len(feats)}")
check("Feature order matches expected schema", feats == EXPECTED_FEATURES,
      "exact ordered match" if feats == EXPECTED_FEATURES else "ORDER OR NAMES DIFFER")
if feats != EXPECTED_FEATURES:
    for i, (got, exp) in enumerate(zip(feats, EXPECTED_FEATURES)):
        if got != exp:
            print(f"        first mismatch at index {i}: got {got!r}, expected {exp!r}")
            break
check("feature_names length matches X columns", len(feats) == Xm.shape[1],
      f"names={len(feats)} cols={Xm.shape[1]}")

groups = data["feat_groups"]
flat_groups = [f for g in ["overall", "indices", "early", "late", "yoy", "indicators"] for f in groups[g]]
check("feat_groups concatenate to the full ordered schema", flat_groups == feats,
      f"{len(flat_groups)} grouped vs {len(feats)} named")

print("\n-- Labels --")
um, ua = np.unique(ym), np.unique(ya)
check("Madrid has exactly 4 classes", list(um) == [1, 2, 3, 4], f"got {list(um)}")
check("Amsterdam has exactly 4 classes", list(ua) == [1, 2, 3, 4], f"got {list(ua)}")
print("      Madrid    counts:", {int(c): int((ym == c).sum()) for c in um})
print("      Amsterdam counts:", {int(c): int((ya == c).sum()) for c in ua})

print("\n-- Finiteness --")
check("Madrid features all finite (no NaN/inf)", bool(np.isfinite(Xm).all()),
      f"{int((~np.isfinite(Xm)).sum())} non-finite cells")
check("Amsterdam features all finite (no NaN/inf)", bool(np.isfinite(Xa).all()),
      f"{int((~np.isfinite(Xa)).sum())} non-finite cells")

print("\n-- Pixel key alignment --")
pm, pa = data["pixel_ids_madrid"], data["pixel_ids_amsterdam"]
check("Madrid pixel_ids rows align with X rows", pm.shape[0] == Xm.shape[0], f"{pm.shape} vs {Xm.shape}")
check("Amsterdam pixel_ids rows align with X rows", pa.shape[0] == Xa.shape[0], f"{pa.shape} vs {Xa.shape}")
check("Madrid pixel keys are unique (one row per geographic pixel)",
      len(np.unique(pm, axis=0)) == len(pm), f"{len(np.unique(pm, axis=0))} unique of {len(pm)}")
check("Amsterdam pixel keys are unique (one row per geographic pixel)",
      len(np.unique(pa, axis=0)) == len(pa), f"{len(np.unique(pa, axis=0))} unique of {len(pa)}")

print("\n-- Scaler --")
scaler = data["scaler"]
check("Scaler is fitted (has mean_)", hasattr(scaler, "mean_"), type(scaler).__name__)
check("Scaler was fitted on 60 features", getattr(scaler, "n_features_in_", None) == 60,
      f"n_features_in_={getattr(scaler, 'n_features_in_', None)}")
check("Scaler fitted on Madrid row count", getattr(scaler, "n_samples_seen_", None) == EXPECTED_MADRID[0],
      f"n_samples_seen_={getattr(scaler, 'n_samples_seen_', None)}")
# Madrid was fit_transform'd, so its columns should be ~zero mean / unit variance.
# EXCEPTION: StandardScaler documents that a zero-variance column is left alone
# (scale_ = 1), so a constant feature stays constant instead of becoming unit-std.
# Excluding those from the std check is correct; they are reported separately below.
const_mask = scaler.var_ == 0
n_const = int(const_mask.sum())
mad_mean = float(np.abs(Xm.mean(axis=0)).max())
nonconst_std = np.abs(Xm[:, ~const_mask].std(axis=0) - 1)
mad_std = float(nonconst_std.max()) if nonconst_std.size else 0.0
check("Madrid is standardised (mean~0)", mad_mean < 1e-8, f"max |mean| = {mad_mean:.2e}")
check("Madrid is standardised (std~1, excluding constant columns)", mad_std < 1e-6,
      f"max |std-1| = {mad_std:.2e} over {int((~const_mask).sum())} non-constant columns")
check("Constant columns behave as StandardScaler documents (scale_=1)",
      bool(np.all(scaler.scale_[const_mask] == 1)) if n_const else True,
      f"{n_const} constant column(s)")

if n_const:
    print(f"\n  NOTE — {n_const} of 60 features carry NO information in Madrid:")
    for i in np.flatnonzero(const_mask):
        raw_a = Xa[:, i] * scaler.scale_[i] + scaler.mean_[i]
        ua = np.unique(raw_a.round(6))
        also_const = " (also constant in Amsterdam)" if ua.size == 1 else ""
        print(f"      [{i}] {feats[i]} = {scaler.mean_[i]:g} for all Madrid rows{also_const}")
    print(f"      Effective informative feature count: {60 - n_const}, not 60.")
# Amsterdam is only transformed, so it should NOT be centred — that is the documented
# Madrid-scaled feature space the prototypes live in.
ams_mean = float(np.abs(Xa.mean(axis=0)).max())
print(f"      Amsterdam max |column mean| in Madrid-scaled space = {ams_mean:.3f}")
print("      (non-zero is EXPECTED and is exactly the domain shift the task is about)")

print("\n" + "=" * 72)
n_pass = sum(1 for _, p, _ in results if p)
n_fail = len(results) - n_pass
print(f"RESULT: {n_pass} passed, {n_fail} failed, of {len(results)} checks")
if n_fail:
    print("\nFAILED CHECKS:")
    for name, passed, detail in results:
        if not passed:
            print(f"  - {name}: {detail}")
print("=" * 72)
sys.exit(1 if n_fail else 0)
