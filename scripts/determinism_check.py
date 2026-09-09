"""Is the reference Random Forest deterministic ON THIS MACHINE?

This distinguishes two very different explanations for why our reproduced
RF numbers differ from the organiser's saved outputs:

  (A) systematic  — a different scikit-learn builds different trees from the
                    same seed. Our number is then a stable, trustworthy datum.
  (B) nondeterministic — the run is not repeatable here (thread scheduling,
                    unstable seeding). Our number would then be worthless as a
                    reference and the whole baseline claim collapses.

We refit the final Madrid RF twice with the identical seed and compare the
predictions and the zero-shot Amsterdam score exactly. Read-only.
"""

import pickle
import time

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=42, n_jobs=-1)

with open("data/preprocessed/preprocessed_data.pkl", "rb") as f:
    d = pickle.load(f)
Xm, ym = d["X_madrid"], d["y_madrid"]
Xa, ya = d["X_amsterdam"], d["y_amsterdam"]

print("Refitting the final Madrid RF twice with identical settings (seed 42)...")
preds, f1s, probas = [], [], []
for run in (1, 2):
    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS)
    rf.fit(Xm, ym)
    p = rf.predict(Xa)
    pr = rf.predict_proba(Xa)
    f1 = f1_score(ya, p, average="macro")
    preds.append(p)
    probas.append(pr)
    f1s.append(f1)
    print(f"  run {run}: zero-shot macro F1 = {f1:.10f}   ({time.time()-t0:.0f}s)")

same_pred = bool(np.array_equal(preds[0], preds[1]))
same_proba = bool(np.array_equal(probas[0], probas[1]))
n_diff = int((preds[0] != preds[1]).sum())

print()
print(f"  Identical predictions : {same_pred}  ({n_diff} of {len(ya)} differ)")
print(f"  Identical probabilities: {same_proba}")
print(f"  Identical macro F1     : {f1s[0] == f1s[1]}  (delta = {f1s[0]-f1s[1]:.2e})")
print()
if same_pred and f1s[0] == f1s[1]:
    print("  => DETERMINISTIC on this machine. The gap versus the organiser's saved")
    print("     outputs is SYSTEMATIC (library version), not run-to-run noise.")
    print("     The reproduced number is usable as a stable reference datum.")
else:
    print("  => NOT deterministic. Escalate immediately: a reference that does not")
    print("     repeat cannot serve as a baseline for any later comparison.")

print(f"\n  Zero-shot reproduced here: {f1s[0]:.4f}   |  organiser saved: 0.3427")
print(f"  Notebook 4 run reported  : 0.4433  (agreement with this refit: "
      f"{abs(f1s[0]-0.4433) < 5e-5})")
