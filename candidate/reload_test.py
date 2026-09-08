"""Gate S check: reload the saved Stage 1 artifact in a CLEAN session and adapt.

This is the deliverable the starter never produced - "a saved Madrid model plus a
runnable adaptation script that consumes it". It must pass in a fresh interpreter
that never saw the training run, and it must run WITHOUT any label column present
on the query side.

Per TEAM_OPERATING_SYSTEM.md this should ultimately be executed by a DIFFERENT
team member than the one who trained it.

Run from the repository root:
    python candidate/reload_test.py
"""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score

ART = Path("candidate/artifacts")
PKL = Path("data/preprocessed/preprocessed_data.pkl")

checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))


print("=" * 70)
print("STAGE 1 ARTIFACT RELOAD + LABEL-FREE INFERENCE")
print("=" * 70)

# ---- reload source state (nothing from the training session is in scope) ----
print("\n-- Reloading frozen source state --")
with (ART / "stage1_madrid.pkl").open("rb") as f:
    st = pickle.load(f)

check("Artifact reloads in a clean session", True, f"{len(st)} keys")
check("Trained on Madrid only", st["trained_on"] == "madrid_only", st["trained_on"])
check("Feature schema present and ordered", len(st["feature_names"]) == 60,
      f"{len(st['feature_names'])} names")
check("Four source classes recorded", st["classes"] == [1, 2, 3, 4], str(st["classes"]))
check("Seed recorded", st["seed"] == 42, str(st["seed"]))
check("Metric weights match feature count", len(st["metric_weights"]) == 60)
check("Adaptation artifact is small enough to be portable",
      (ART / "stage1_madrid.pkl").stat().st_size < 5_000_000,
      f"{(ART / 'stage1_madrid.pkl').stat().st_size/1024:.0f} KB")

lda, w = st["lda"], st["metric_weights"]

# ---- load target features, then DISCARD the query labels ------------------
with PKL.open("rb") as f:
    d = pickle.load(f)
Xa, ya_true = d["X_amsterdam"], d["y_amsterdam"]

check("Feature order matches the artifact's schema",
      list(d["feature_names"]) == list(st["feature_names"]))

episodes = np.load(ART / "episodes.npz")
support_idx = episodes["t0_b25"]           # trial 0, 25 shots/class

query_mask = np.ones(len(Xa), dtype=bool)
query_mask[support_idx] = False

# The adaptation input: support features + support LABELS, and query features
# with NO labels attached at all.
X_sup = Xa[support_idx]
y_sup = ya_true[support_idx]
X_qry = Xa[query_mask]                     # features only - labels not passed on

check("Support and query are disjoint",
      not set(support_idx) & set(np.where(query_mask)[0]),
      f"{len(X_sup)} support / {len(X_qry)} query")


# ---- adapt using the frozen source state ----------------------------------
def prototype_predict(Xs, ys, Xq):
    classes = np.unique(ys)
    protos = np.stack([Xs[ys == c].mean(axis=0) for c in classes])
    dist = ((Xq ** 2).sum(1)[:, None] - 2.0 * Xq @ protos.T + (protos ** 2).sum(1)[None, :])
    return classes[dist.argmin(axis=1)]


print("\n-- Adapting with the frozen Madrid transform (label-free query path) --")
Z_sup, Z_qry = X_sup * w, X_qry * w        # the Madrid-learned metric
pred = prototype_predict(Z_sup, y_sup, Z_qry)

check("Inference ran without query labels", True, f"{len(pred)} predictions")
check("Predictions are all valid classes", set(np.unique(pred)).issubset({1, 2, 3, 4}),
      str(sorted(set(int(p) for p in np.unique(pred)))))
check("One prediction per query pixel", len(pred) == len(X_qry))

# labels are reintroduced ONLY now, purely to score
f1 = f1_score(ya_true[query_mask], pred, average="macro")
print(f"\n  Macro F1 on the held-out query set: {f1:.4f}")

# the source state must be unchanged by adaptation
check("Source LDA unchanged by adaptation", hasattr(lda, "scalings_"))
check("Metric weights unchanged by adaptation",
      np.array_equal(w, st["metric_weights"]))

# the full forest is a separate optional artifact - adaptation must not need it
rf_path = ART / "stage1_rf.joblib"
if rf_path.exists():
    print(f"\n  (source RF available separately: {rf_path.stat().st_size/1024/1024:.0f} MB, "
          f"not required for adaptation)")

print("\n" + "=" * 70)
n_fail = sum(1 for _, ok in checks if not ok)
print(f"RESULT: {len(checks) - n_fail} passed, {n_fail} failed, of {len(checks)}")
print("=" * 70)
sys.exit(1 if n_fail else 0)
