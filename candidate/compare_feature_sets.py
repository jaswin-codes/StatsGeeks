"""Decisive test: do the v2 features beat the starter's v1 features?

FRESH EPISODES, NEW SEED (2026, not 42).
----------------------------------------
The Day-1 audit set had been used twice, which capped what we could honestly
claim (DEC-012). Building new features gives a legitimate reason to draw a brand
new episode set that nothing has ever been selected on, so this audit is clean.

Selection trials 0-4 choose the configuration. Audit trials 5-9 are reported once.

Both feature sets are evaluated on THE SAME PIXELS in THE SAME EPISODES, aligned
by (px_key, py_key), so the only thing differing is the feature representation.

Run from the repository root:
    python candidate/compare_feature_sets.py
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

V1 = Path("data/preprocessed/preprocessed_data.pkl")
V2 = Path("data/preprocessed/features_v2.pkl")
OUT = Path("candidate/artifacts")
BUDGETS = [5, 25, 50, 100, 200]
N_TRIALS, N_SELECT = 10, 5
EPISODE_SEED = 2026          # NEW - nothing has ever been selected on this
RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=42, n_jobs=-1)


def proto_predict(Zs, ys, Zq):
    classes = np.unique(ys)
    protos = np.stack([Zs[ys == c].mean(axis=0) for c in classes])
    d = (Zq ** 2).sum(1)[:, None] - 2.0 * Zq @ protos.T + (protos ** 2).sum(1)[None, :]
    return classes[d.argmin(axis=1)]


def build_episodes(y, seed):
    rng = np.random.default_rng(seed)
    eps = {}
    for t in range(N_TRIALS):
        perms = {int(c): rng.permutation(np.where(y == c)[0])[:max(BUDGETS)]
                 for c in np.unique(y)}
        eps[t] = {b: np.concatenate([perms[int(c)][:b] for c in np.unique(y)])
                  for b in BUDGETS}
    return eps


def load(p):
    with p.open("rb") as f:
        d = pickle.load(f)
    return d


print("=" * 78)
print("FEATURE SET COMPARISON - fresh episodes, seed", EPISODE_SEED)
print("=" * 78)

d1, d2 = load(V1), load(V2)
print(f"\nv1 (starter) : Madrid {d1['X_madrid'].shape}  Amsterdam {d1['X_amsterdam'].shape}")
print(f"v2 (ours)    : Madrid {d2['X_madrid'].shape}  Amsterdam {d2['X_amsterdam'].shape}")

# ---- align Amsterdam pixel order between the two feature sets --------------
k1 = pd.MultiIndex.from_arrays(np.asarray(d1["pixel_ids_amsterdam"]).T)
k2 = pd.MultiIndex.from_arrays(np.asarray(d2["pixel_ids_amsterdam"]).T)
order = pd.Series(np.arange(len(k2)), index=k2).reindex(k1).to_numpy()
assert not np.isnan(order).any(), "pixel key mismatch between feature sets"
order = order.astype(int)
Xa1, ya1 = d1["X_amsterdam"], d1["y_amsterdam"]
Xa2, ya2 = d2["X_amsterdam"][order], d2["y_amsterdam"][order]
assert np.array_equal(ya1, ya2), "labels disagree after alignment"
print(f"aligned on {len(k1):,} shared Amsterdam pixels; labels identical")

km1 = pd.MultiIndex.from_arrays(np.asarray(d1["pixel_ids_madrid"]).T)
km2 = pd.MultiIndex.from_arrays(np.asarray(d2["pixel_ids_madrid"]).T)
mo = pd.Series(np.arange(len(km2)), index=km2).reindex(km1).to_numpy().astype(int)
Xm1, ym1 = d1["X_madrid"], d1["y_madrid"]
Xm2, ym2 = d2["X_madrid"][mo], d2["y_madrid"][mo]
assert np.array_equal(ym1, ym2)

eps = build_episodes(ya1, EPISODE_SEED)
n_all = len(ya1)

# ---- Stage 1 per feature set ----------------------------------------------
SETS = {}
for tag, Xm, ym, Xa, names in [("v1", Xm1, ym1, Xa1, d1["feature_names"]),
                               ("v2", Xm2, ym2, Xa2, d2["feature_names"])]:
    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS).fit(Xm, ym)
    imp = rf.feature_importances_
    w = np.sqrt(imp)
    zs = f1_score(ya1, rf.predict(Xa), average="macro")
    n_top = min(30, Xa.shape[1])
    top = np.sort(np.argsort(imp)[::-1][:n_top])
    SETS[tag] = {"rf": rf, "imp": imp, "w": w, "Xa": Xa, "top": top,
                 "zero_shot": float(zs), "names": list(names)}
    print(f"\n{tag}: RF trained ({time.time()-t0:.0f}s)  zero-shot {zs:.4f}  "
          f"{Xa.shape[1]} features")
    o = np.argsort(imp)[::-1][:6]
    print("    top features: " + ", ".join(f"{names[i]}" for i in o))

# ---- evaluate --------------------------------------------------------------
METHODS = {
    "raw":   lambda S: S["Xa"],
    "rfw":   lambda S: S["Xa"] * S["w"],
    "topk":  lambda S: S["Xa"][:, S["top"]] * S["w"][S["top"]],
}

res = {f"{t}_{m}": {b: [] for b in BUDGETS} for t in SETS for m in METHODS}
Z = {f"{t}_{m}": np.ascontiguousarray(fn(SETS[t])) for t in SETS for m, fn in METHODS.items()}

print("\nevaluating...")
for t in range(N_TRIALS):
    for b in BUDGETS:
        sup = eps[t][b]
        qm = np.ones(n_all, bool); qm[sup] = False
        ys, yq = ya1[sup], ya1[qm]
        for k, M in Z.items():
            res[k][b].append(f1_score(yq, proto_predict(M[sup], ys, M[qm]),
                                      average="macro", zero_division=0))

sel, aud = slice(0, N_SELECT), slice(N_SELECT, N_TRIALS)
mean = lambda k, b, s: float(np.mean(res[k][b][s]))

print("\n" + "=" * 78)
print(f"SELECTION (trials 0-{N_SELECT-1})  - mean macro F1")
print("=" * 78)
print(f"{'config':<12}" + "".join(f"{b:>9}" for b in BUDGETS) + f"{'mean':>9}")
scores = {}
for k in res:
    ms = [mean(k, b, sel) for b in BUDGETS]
    scores[k] = float(np.mean(ms))
    print(f"{k:<12}" + "".join(f"{v:>9.4f}" for v in ms) + f"{scores[k]:>9.4f}")

best_v1 = max((k for k in res if k.startswith("v1")), key=lambda k: scores[k])
best_v2 = max((k for k in res if k.startswith("v2")), key=lambda k: scores[k])
print(f"\n   best v1 config: {best_v1}  ({scores[best_v1]:.4f})")
print(f"   best v2 config: {best_v2}  ({scores[best_v2]:.4f})")
print(f"   v2 - v1 on selection: {scores[best_v2]-scores[best_v1]:+.4f}")

print("\n" + "=" * 78)
print(f"FINAL AUDIT (trials {N_SELECT}-{N_TRIALS-1}, never selected on)")
print("=" * 78)
print(f"{'shots':>7}{'v1 best':>12}{'v2 best':>12}{'gain':>10}{'wins':>8}"
      f"{'  v2 vs v2-control':>20}")
audit_rows = {}
for b in BUDGETS:
    a = np.array(res[best_v1][b][aud])
    c = np.array(res[best_v2][b][aud])
    ctrl2 = np.array(res["v2_raw"][b][aud])
    d = c - a
    audit_rows[b] = {"v1_best": float(a.mean()), "v1_std": float(a.std()),
                     "v2_best": float(c.mean()), "v2_std": float(c.std()),
                     "gain": float(d.mean()), "wins": int((d > 0).sum()), "n": len(d),
                     "v2_transfer_benefit": float((c - ctrl2).mean())}
    print(f"{b:>7}{a.mean():>12.4f}{c.mean():>12.4f}{d.mean():>+10.4f}"
          f"{f'{int((d>0).sum())}/{len(d)}':>8}{(c-ctrl2).mean():>+20.4f}")

print(f"\n   v1 zero-shot {SETS['v1']['zero_shot']:.4f}   "
      f"v2 zero-shot {SETS['v2']['zero_shot']:.4f}   "
      f"({SETS['v2']['zero_shot']-SETS['v1']['zero_shot']:+.4f})")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "feature_comparison.json").write_text(json.dumps({
    "episode_seed": EPISODE_SEED,
    "note": "Fresh episode set - nothing was ever selected on seed 2026, so this "
            "audit is clean, unlike the Day-1 audit which had been used twice.",
    "best_v1": best_v1, "best_v2": best_v2,
    "zero_shot": {t: SETS[t]["zero_shot"] for t in SETS},
    "selection_means": scores,
    "audit": {str(b): audit_rows[b] for b in BUDGETS},
    "all_trials": {k: {str(b): [float(x) for x in res[k][b]] for b in BUDGETS} for k in res},
}, indent=2))
print(f"\nSaved -> {OUT}/feature_comparison.json")
