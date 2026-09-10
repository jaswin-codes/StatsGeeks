"""Feature builder v2 - season-controlled, coverage-aware, and LABEL-FREE.

WHY THIS EXISTS
---------------
All nine transfer representations tested on the starter's features landed
between 0.5870 and 0.5978 - a spread of 0.011 around a control of 0.5926. Nine
different ways of using Madrid's learning barely moved the result. That is the
signature of a FEATURE bottleneck, not a method bottleneck.

Three signals the starter throws away:

1. SEASON.  Madrid's median observation is day-of-year 175 (late June);
   Amsterdam's is 105 (mid April). A 70-day offset. Vegetation phenology alone
   moves NDVI enormously between those dates, so part of what a model reads as
   "Madrid looks different from Amsterdam" is really "late June looks different
   from mid April". `doy` is present in the raw data and never used.

2. COVERAGE.  Building fraction per pixel - mean 0.505 Madrid, 0.421 Amsterdam.
   A 20%-building pixel and a 100%-building pixel look nothing alike regardless
   of construction era. The starter drops the column during feature generation.

3. OBSERVATION DENSITY.  Gap-filling manufactures complete trajectories, but the
   number of real observations behind each one is never recorded, so a
   well-observed pixel and a mostly-interpolated one are indistinguishable.

STRUCTURAL FIX - LABEL INDEPENDENCE
-----------------------------------
The starter's `build_pixel_features` filters on `age_class.notna()` and groups by
`age_class`, so it CANNOT generate features for unlabelled pixels. That is
MASTER_PLAN priorities #10 and #11, still open.

Here, `build_features()` never sees a label. Labels are derived separately and
joined by pixel key afterwards. The same function would run unchanged on a
hidden test set with no label column present.

Run from the repository root:
    python candidate/build_features_v2.py
"""

from __future__ import annotations

import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("data")
OUT = DATA / "preprocessed" / "features_v2.pkl"

BANDS = ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]
INDICES = ["NDVI", "NDBI", "UI", "MNDWI", "BSI"]
BLUE_MAX = 15_000
PID = ["px_key", "py_key"]

EARLY_END = 2003          # 1984-2003
LATE_START = 2004         # 2004+
WARM_LO, WARM_HI = 121, 273   # May-Sep: wide enough that both cities have data
CLASS_EVENTS = {"Amsterdam": 1945, "Madrid": 1960}


# ----------------------------------------------------------------- flattening
def best_obs(df, col_base, qa):
    """First QA-valid slot per column, same policy as the starter."""
    out = np.full(len(df), np.nan)
    for slot in (1, 2, 3):
        c, q = f"{col_base}_{slot}", f"{qa}_{slot}"
        if c not in df.columns:
            continue
        valid = df[q].fillna(False).values
        out = np.where(np.isnan(out) & valid, df[c].astype(float).values, out)
    return out


def flatten(df):
    """One row per pixel-year: six bands, the day-of-year they came from, coverage.

    NOTE: carries NO label column. `coverage` is a per-pixel constant supplied by
    the organisers and is an input, not a label.
    """
    keep = [c for c in ["city", "year", "px_key", "py_key", "coverage"] if c in df.columns]
    out = df[keep].copy()
    for b in BANDS:
        out[b] = best_obs(df, b, "qa_valid")
    out["doy"] = best_obs(df, "doy", "qa_valid")
    out = out.dropna(subset=BANDS)
    n0 = len(out)
    out = out[out["Blue"] <= BLUE_MAX].copy()
    print(f"    removed {n0-len(out):,} haze rows (Blue > {BLUE_MAX:,})")
    return out


def add_indices(d):
    B, G, R = d["Blue"], d["Green"], d["Red"]
    N, S1, S2 = d["NIR"], d["SWIR1"], d["SWIR2"]
    e = 1e-6
    d["NDVI"] = (N - R) / (N + R + e)
    d["NDBI"] = (S1 - N) / (S1 + N + e)
    d["UI"] = (S2 - N) / (S2 + N + e)
    d["MNDWI"] = (G - S1) / (G + S1 + e)
    d["BSI"] = ((S1 + R) - (N + B)) / ((S1 + R) + (N + B) + e)
    return d


# ----------------------------------------------------------------- gap filling
def fill_wide(flat, pixels, years, col, interpolate=True):
    """Pivot to (pixel x year); optionally interpolate along the year axis.

    Much faster than the starter's per-group transform, which made ~450k
    Python-level calls. Same interpolation policy: linear interior, nearest edges.

    interpolate=False returns the RAW grid with NaN where no observation exists -
    needed to count real observations, since after interpolation nothing is NaN.
    """
    w = flat.pivot_table(index=PID, columns="year", values=col, aggfunc="mean")
    w = w.reindex(index=pixels, columns=years)
    if interpolate:
        w = w.interpolate(axis=1, limit_direction="both")
    return w.to_numpy(dtype=np.float64)


# ----------------------------------------------------------------- features
def build_features(df, city_name):
    """Raw pixel-year frame -> one feature row per pixel. NEVER sees a label."""
    t0 = time.time()
    print(f"  [{city_name}] flattening...")
    flat = add_indices(flatten(df))

    years = sorted(flat["year"].unique())
    pixels = pd.MultiIndex.from_frame(
        flat[PID].drop_duplicates().sort_values(PID)).set_names(PID)
    n_pix, n_yr = len(pixels), len(years)
    print(f"    {len(flat):,} valid pixel-years -> {n_pix:,} pixels x {n_yr} years")

    yr = np.asarray(years)
    early_m, late_m = yr <= EARLY_END, yr >= LATE_START

    # observed-value matrices before gap filling, to count real observations
    obs_mask = ~np.isnan(
        fill_wide(flat.assign(_o=1.0), pixels, years, "_o", interpolate=False))

    feats, names = [], []

    def push(mat, label):
        feats.append(mat.astype(np.float64))
        names.append(label)

    # ---- spectral trajectories, gap-filled --------------------------------
    print(f"  [{city_name}] gap-filling {len(BANDS)+len(INDICES)} channels...")
    filled = {}
    for c in BANDS + INDICES:
        filled[c] = fill_wide(flat, pixels, years, c)

    for c in BANDS + INDICES:
        M = filled[c]
        push(np.nanmean(M, axis=1), f"{c}_mean")
        push(np.nanstd(M, axis=1), f"{c}_std")

    # ---- early / late period contrasts (bands only, as in the starter) ----
    for c in BANDS:
        M = filled[c]
        push(np.nanmean(M[:, early_m], axis=1), f"{c}_early_mean")
        push(np.nanstd(M[:, early_m], axis=1), f"{c}_early_std")
        push(np.nanmean(M[:, late_m], axis=1), f"{c}_late_mean")
        push(np.nanstd(M[:, late_m], axis=1), f"{c}_late_std")
        push(np.nanmean(M[:, late_m], axis=1) - np.nanmean(M[:, early_m], axis=1),
             f"{c}_late_minus_early")          # NEW: explicit change magnitude

    # ---- year-on-year change ----------------------------------------------
    for c in BANDS:
        D = np.diff(filled[c], axis=1)
        push(np.nanmean(D, axis=1), f"d_{c}_mean")
        push(np.nanstd(D, axis=1), f"d_{c}_std")
        push(np.nanmax(np.abs(D), axis=1), f"d_{c}_absmax")      # NEW
        # NEW, label-free change timing: WHEN was the largest jump?
        push(yr[1:][np.nanargmax(np.abs(D), axis=1)].astype(float), f"d_{c}_argmax_year")

    # ---- NEW: season ------------------------------------------------------
    print(f"  [{city_name}] season, coverage, observation density...")
    doy_w = fill_wide(flat, pixels, years, "doy")
    push(np.nanmean(doy_w, axis=1), "doy_mean")
    push(np.nanstd(doy_w, axis=1), "doy_std")

    warm_rows = flat[(flat["doy"] >= WARM_LO) & (flat["doy"] <= WARM_HI)]
    warm_frac = (flat.assign(_w=((flat["doy"] >= WARM_LO) & (flat["doy"] <= WARM_HI)).astype(float))
                 .groupby(PID)["_w"].mean().reindex(pixels).to_numpy())
    push(np.nan_to_num(warm_frac), "warm_frac")

    # season-controlled spectra: statistics computed ONLY from May-Sep
    # observations, so Madrid and Amsterdam are compared on comparable phenology.
    for c in BANDS + ["NDVI", "NDBI"]:
        g = warm_rows.groupby(PID)[c]
        mu = g.mean().reindex(pixels).to_numpy()
        # fall back to the all-season mean where a pixel has no warm observation
        allm = np.nanmean(filled[c], axis=1)
        push(np.where(np.isnan(mu), allm, mu), f"{c}_warm_mean")
    push(np.isnan(warm_rows.groupby(PID)["NDVI"].mean().reindex(pixels).to_numpy()).astype(float),
         "warm_missing")

    # ---- NEW: coverage ----------------------------------------------------
    cov = flat.groupby(PID)["coverage"].first().reindex(pixels).to_numpy()
    push(np.nan_to_num(cov, nan=float(np.nanmean(cov))), "coverage")

    # ---- NEW: observation density -----------------------------------------
    n_obs = obs_mask.sum(axis=1).astype(float)
    push(n_obs, "n_obs")
    push(n_obs / n_yr, "obs_frac")
    push(obs_mask[:, early_m].sum(axis=1).astype(float), "n_obs_early")
    push(obs_mask[:, late_m].sum(axis=1).astype(float), "n_obs_late")
    gaps = np.zeros(n_pix)
    for i in range(n_pix):
        idx = np.flatnonzero(obs_mask[i])
        gaps[i] = np.max(np.diff(idx)) if idx.size > 1 else float(n_yr)
    push(gaps, "max_gap_years")

    X = np.column_stack(feats)
    keys = np.array([[a, b] for a, b in pixels])
    print(f"  [{city_name}] {X.shape[1]} features x {X.shape[0]:,} pixels "
          f"({time.time()-t0:.0f}s)")
    return X, names, keys


def derive_labels(df, city):
    """Labels, derived SEPARATELY from features and joined by pixel key."""
    ev = CLASS_EVENTS[city]
    p = df[PID + ["weighted_mean_year"]].drop_duplicates(PID).sort_values(PID)
    lab = pd.cut(p["weighted_mean_year"], bins=[-np.inf, ev, 1984, 2004, np.inf],
                 labels=[1, 2, 3, 4]).astype("Int64")
    return p[PID].to_numpy(), lab.to_numpy()


def main():
    out = {}
    for city, fn in [("Madrid", "madrid_train.parquet"),
                     ("Amsterdam", "amsterdam_data.parquet")]:
        print(f"\n=== {city} ===")
        df = pd.read_parquet(DATA / fn)
        X, names, keys = build_features(df, city)          # label-free
        lkeys, labels = derive_labels(df, city)            # labels, separately

        # join labels to feature rows by pixel key
        fi = pd.MultiIndex.from_arrays(keys.T)
        li = pd.MultiIndex.from_arrays(lkeys.T)
        y = pd.Series(labels, index=li).reindex(fi).to_numpy()
        keep = ~pd.isna(y)
        print(f"  {int(keep.sum()):,} of {len(y):,} pixels have a label")
        out[city] = {"X": X[keep], "y": y[keep].astype(int), "keys": keys[keep]}

    names_ref = names
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    Xm = sc.fit_transform(out["Madrid"]["X"])
    Xa = sc.transform(out["Amsterdam"]["X"])

    const = int((sc.var_ == 0).sum())
    print(f"\nfeatures: {len(names_ref)}   constant (zero-variance): {const}")
    if const:
        for i in np.flatnonzero(sc.var_ == 0):
            print(f"   dead: {names_ref[i]}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("wb") as f:
        pickle.dump({
            "X_madrid": Xm, "y_madrid": out["Madrid"]["y"],
            "X_amsterdam": Xa, "y_amsterdam": out["Amsterdam"]["y"],
            "feature_names": names_ref, "scaler": sc,
            "pixel_ids_madrid": out["Madrid"]["keys"],
            "pixel_ids_amsterdam": out["Amsterdam"]["keys"],
            "version": "v2-season-coverage-labelfree",
            "note": "Features generated WITHOUT any label column; labels joined by "
                    "pixel key afterwards. Adds season control (May-Sep statistics, "
                    "doy summaries), coverage, observation density, and label-free "
                    "change-timing features.",
        }, f)
    print(f"\nMadrid {Xm.shape}   Amsterdam {Xa.shape}")
    print(f"Saved -> {OUT}  ({OUT.stat().st_size/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
