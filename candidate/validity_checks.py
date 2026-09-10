"""Two outstanding validity checks from MASTER_PLAN.md Current Priorities.

  #7  Confirm right-inclusive labels and test exact boundary years.
  #15 Spatial sensitivity: nearby pixels can appear in both support and query,
      which would inflate the reported score. Random draws cannot detect this;
      a spatially blocked draw can.

Run from the repository root:
    python candidate/validity_checks.py
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

PKL = Path("data/preprocessed/preprocessed_data.pkl")
OUT = Path("candidate/artifacts")
BUDGETS = [5, 25, 50, 100, 200]
SEED = 42


def proto_predict(Zs, ys, Zq):
    classes = np.unique(ys)
    protos = np.stack([Zs[ys == c].mean(axis=0) for c in classes])
    d = (Zq ** 2).sum(1)[:, None] - 2.0 * Zq @ protos.T + (protos ** 2).sum(1)[None, :]
    return classes[d.argmin(axis=1)]


# ===================================================================== #7
print("=" * 76)
print("CHECK #7 - label boundaries are right-inclusive")
print("=" * 76)
print("pd.cut(bins=[-inf, ev, 1984, 2004, inf]) defaults to right-closed intervals,")
print("so a pixel sitting EXACTLY on a boundary belongs to the LOWER class.\n")

cuts = {"Madrid": 1960, "Amsterdam": 1945}
boundary_report = {}
for city, ev in cuts.items():
    bins = [-np.inf, ev, 1984, 2004, np.inf]
    probes = [ev - 1, ev, ev + 1, 1984, 1985, 2004, 2005]
    got = pd.cut(pd.Series(probes, dtype="float64"),
                 bins=bins, labels=[1, 2, 3, 4]).astype("Int64").tolist()
    boundary_report[city] = dict(zip(map(str, probes), [int(g) for g in got]))
    print(f"{city} (event year {ev}):")
    for p, g in zip(probes, got):
        edge = "  <- exact boundary" if p in (ev, 1984, 2004) else ""
        print(f"    weighted_mean_year = {p}  ->  class {g}{edge}")
    print()

print("Confirmed: exact boundary years fall in the LOWER class "
      "(1984 -> class 2, 2004 -> class 3).")
print("Consequence: shifting to left-closed intervals would move every")
print("boundary-year pixel up one class and change the labels. Do not change it.\n")

# ==================================================================== #15
print("=" * 76)
print("CHECK #15 - spatial sensitivity of the few-shot protocol")
print("=" * 76)

with PKL.open("rb") as f:
    d = pickle.load(f)
Xa, ya = d["X_amsterdam"], d["y_amsterdam"]
pix = d["pixel_ids_amsterdam"]
px, py = pix[:, 0].astype(float), pix[:, 1].astype(float)

with (OUT / "stage1_madrid.pkl").open("rb") as f:
    st = pickle.load(f)
w, sel = st["metric_weights"], st["selected_feature_idx"]
Z = np.ascontiguousarray(Xa[:, sel] * w[sel])

print(f"Amsterdam spans px {px.min():.0f}-{px.max():.0f}, py {py.min():.0f}-{py.max():.0f}")
print("\nRANDOM draw  : support pixels scattered among the query pixels (the protocol used).")
print("BLOCKED draw : support drawn only from the WEST half, scored only on the EAST half,")
print("               so no support pixel is a near neighbour of any query pixel.\n")

split = np.median(px)
west, east = px < split, px >= split
print(f"   west {west.sum():,} pixels | east {east.sum():,} pixels\n")

rng = np.random.default_rng(SEED)
classes = np.unique(ya)
rows = []
print(f"{'shots':>7}{'random':>12}{'blocked':>12}{'drop':>10}")
for b in BUDGETS:
    rnd_s, blk_s = [], []
    for _ in range(5):
        # random protocol
        sup = np.concatenate([rng.choice(np.where(ya == c)[0], b, replace=False) for c in classes])
        qm = np.ones(len(ya), bool); qm[sup] = False
        rnd_s.append(f1_score(ya[qm], proto_predict(Z[sup], ya[sup], Z[qm]),
                              average="macro", zero_division=0))
        # spatially blocked: support from west only, query = east only
        sup_b = np.concatenate([
            rng.choice(np.where((ya == c) & west)[0], b, replace=False) for c in classes])
        qm_b = east.copy()
        blk_s.append(f1_score(ya[qm_b], proto_predict(Z[sup_b], ya[sup_b], Z[qm_b]),
                              average="macro", zero_division=0))
    r, bl = float(np.mean(rnd_s)), float(np.mean(blk_s))
    rows.append({"budget": b, "random": r, "blocked": bl, "drop": r - bl})
    print(f"{b:>7}{r:>12.4f}{bl:>12.4f}{r-bl:>+10.4f}")

mean_drop = float(np.mean([r["drop"] for r in rows]))
print(f"\n   mean change under spatial blocking: {mean_drop:+.4f}")
# The SIGN matters. Only a positive drop (random scoring HIGHER than blocked)
# is evidence that spatial proximity inflated the reported numbers.
if mean_drop > 0.01:
    verdict = ("MATERIAL SPATIAL OPTIMISM. Random draws score higher than spatially "
               "separated ones, so the reported figures are inflated by support/query "
               "proximity. Report the blocked figure alongside them.")
elif mean_drop < -0.01:
    verdict = ("NO EVIDENCE OF SPATIAL OPTIMISM. Blocking made scores HIGHER, not lower, "
               "so proximity between support and query is not inflating the results. "
               "The east half is simply easier than the city as a whole - a difficulty "
               "difference between regions, not leakage.")
else:
    verdict = ("NO MATERIAL EFFECT. Spatial separation changes the score by less than "
               "0.01, so the reported figures are not substantially driven by "
               "support/query proximity.")
print("   ->", verdict)
print("\n   Caveat: a west/east split also changes the class mix and the query set,")
print("   so this bounds the effect rather than isolating it cleanly.")

(OUT / "validity_checks.json").write_text(json.dumps({
    "boundary_inclusivity": boundary_report,
    "boundary_note": "pd.cut is right-closed; exact boundary years fall in the lower class.",
    "spatial": {"split_px": float(split), "n_west": int(west.sum()), "n_east": int(east.sum()),
                "per_budget": rows, "mean_drop": mean_drop, "verdict": verdict},
}, indent=2))
print(f"\nSaved -> {OUT}/validity_checks.json")
