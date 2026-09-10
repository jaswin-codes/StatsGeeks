"""FINAL AUDIT - run once, on the sealed trials, for the method already selected.

SELECTION DECISION (made on trials 0-4 only, before this file was run)
---------------------------------------------------------------------
`top30` - Madrid importance used to SELECT the 30 most informative features,
which are then weighted by that same importance.

Chosen on the 25-shot budget, which MASTER_PLAN.md names in advance as the
stability target ("Prioritise 25-shot stability"). That criterion was fixed
before any result was seen, so applying it is not a post-hoc choice.

HONEST CAVEAT, recorded before the audit runs
---------------------------------------------
On selection trials the top four methods are separated by 0.0012 mean macro F1
(top30 0.5978, leaf 0.5974, rfw 0.5966, wcw10_rfw 0.5952) across only 5 trials.
They are statistically indistinguishable. `top30` is not "the best method" -
it is the one the pre-stated 25-shot criterion picks. `rfw` is the most
consistent (beats control at every budget, 20/25 paired wins).

This file reports trials 5-9, which nothing has been selected on.

Run from the repository root:
    python candidate/final_audit.py
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score

PKL      = Path("data/preprocessed/preprocessed_data.pkl")
OUT      = Path("candidate/artifacts")
BUDGETS  = [5, 25, 50, 100, 200]
N_TRIALS, N_SELECT, SEED = 10, 5, 42
TOP_K    = 30
RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=SEED, n_jobs=-1)
OUT.mkdir(parents=True, exist_ok=True)


def build_episodes(y, budgets, n_trials, seed):
    rng = np.random.default_rng(seed)
    eps = {}
    for t in range(n_trials):
        perms = {int(c): rng.permutation(np.where(y == c)[0])[:max(budgets)]
                 for c in np.unique(y)}
        eps[t] = {b: np.concatenate([perms[int(c)][:b] for c in np.unique(y)])
                  for b in budgets}
    return eps


def proto_predict(Zs, ys, Zq):
    classes = np.unique(ys)
    protos = np.stack([Zs[ys == c].mean(axis=0) for c in classes])
    d = (Zq ** 2).sum(1)[:, None] - 2.0 * Zq @ protos.T + (protos ** 2).sum(1)[None, :]
    return classes[d.argmin(axis=1)]


def main():
    print("=" * 78)
    print("FINAL AUDIT - sealed trials 5-9, single run")
    print("=" * 78)

    with PKL.open("rb") as f:
        d = pickle.load(f)
    Xm, ym, Xa, ya = d["X_madrid"], d["y_madrid"], d["X_amsterdam"], d["y_amsterdam"]
    feat_names = list(d["feature_names"])

    print("\n-- Stage 1: Madrid only --")
    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS).fit(Xm, ym)
    imp = rf.feature_importances_
    w = np.sqrt(imp)
    sel_idx = np.sort(np.argsort(imp)[::-1][:TOP_K])
    zero_shot = f1_score(ya, rf.predict(Xa), average="macro")
    print(f"   RF ({time.time()-t0:.0f}s) | zero-shot {zero_shot:.4f}")
    print(f"   selected {TOP_K} of 60 features by Madrid importance")

    # frozen transforms
    T_cand = lambda X: X[:, sel_idx] * w[sel_idx]
    T_ctrl = lambda X: X

    Zc, Zr = np.ascontiguousarray(T_cand(Xa)), np.ascontiguousarray(T_ctrl(Xa))
    eps = build_episodes(ya, BUDGETS, N_TRIALS, SEED)
    n_all = len(ya)

    print("\n" + "=" * 78)
    print("AUDIT RESULTS  (trials 5-9, never used for selection)")
    print("=" * 78)
    print(f"{'shots':>7}{'control':>20}{'top30':>20}{'benefit':>11}{'wins':>8}")

    audit = {}
    for b in BUDGETS:
        rs, cs = [], []
        for t in range(N_SELECT, N_TRIALS):
            sup = eps[t][b]
            qm = np.ones(n_all, dtype=bool); qm[sup] = False
            ys, yq = ya[sup], ya[qm]
            rs.append(f1_score(yq, proto_predict(Zr[sup], ys, Zr[qm]), average="macro", zero_division=0))
            cs.append(f1_score(yq, proto_predict(Zc[sup], ys, Zc[qm]), average="macro", zero_division=0))
        rs, cs = np.array(rs), np.array(cs)
        diff = cs - rs
        audit[b] = {"control_mean": float(rs.mean()), "control_std": float(rs.std()),
                    "cand_mean": float(cs.mean()), "cand_std": float(cs.std()),
                    "benefit": float(diff.mean()), "wins": int((diff > 0).sum()),
                    "n": len(diff),
                    "control_trials": [float(x) for x in rs],
                    "cand_trials": [float(x) for x in cs]}
        print(f"{b:>7}{rs.mean():>13.4f} +/-{rs.std():.4f}"
              f"{cs.mean():>13.4f} +/-{cs.std():.4f}"
              f"{diff.mean():>+11.4f}{f'{int((diff>0).sum())}/{len(diff)}':>8}")

    print(f"\n   Zero-shot Madrid RF (no Amsterdam labels): {zero_shot:.4f}")
    print("   Beating zero-shot is NOT evidence of transfer. Beating the control is.")

    # per-class + confusion at the 25-shot target, first audit episode
    sup = eps[N_SELECT][25]
    qm = np.ones(n_all, dtype=bool); qm[sup] = False
    yq = ya[qm]
    pc = proto_predict(Zc[sup], ya[sup], Zc[qm])
    pr = proto_predict(Zr[sup], ya[sup], Zr[qm])
    f1c = f1_score(yq, pc, average=None, labels=[1, 2, 3, 4], zero_division=0)
    f1r = f1_score(yq, pr, average=None, labels=[1, 2, 3, 4], zero_division=0)

    print("\n" + "=" * 78)
    print("PER-CLASS F1 at 25 shots (first audit episode)")
    print("=" * 78)
    print(f"{'class':>7}{'control':>12}{'top30':>12}{'delta':>10}")
    for i, c in enumerate([1, 2, 3, 4]):
        print(f"{c:>7}{f1r[i]:>12.4f}{f1c[i]:>12.4f}{f1c[i]-f1r[i]:>+10.4f}")

    cm = confusion_matrix(yq, pc, labels=[1, 2, 3, 4])
    cmn = cm / cm.sum(axis=1, keepdims=True)
    print("\nConfusion matrix, top30, row-normalised (diagonal = recall):")
    print("         pred1   pred2   pred3   pred4")
    for i, c in enumerate([1, 2, 3, 4]):
        print(f"   true{c}" + "".join(f"{v:>8.3f}" for v in cmn[i]))

    # ---- save final artifacts ------------------------------------------------
    with (OUT / "stage1_madrid.pkl").open("wb") as f:
        pickle.dump({
            "method": "top30",
            "selected_feature_idx": sel_idx,
            "selected_feature_names": [feat_names[i] for i in sel_idx],
            "metric_weights": w,
            "feature_importances": imp,
            "feature_names": feat_names,
            "classes": [1, 2, 3, 4],
            "rf_params": RF_PARAMS, "seed": SEED,
            "trained_on": "madrid_only",
            "zero_shot_macro_f1": float(zero_shot),
            "note": "Stage 1 source state. Adaptation: X[:, selected_feature_idx] * "
                    "metric_weights[selected_feature_idx], then nearest class prototype "
                    "from support labels. Frozen; never refit on Amsterdam.",
        }, f)
    import joblib
    joblib.dump(rf, OUT / "stage1_rf.joblib", compress=3)
    np.savez_compressed(OUT / "episodes.npz",
                        **{f"t{t}_b{b}": eps[t][b] for t in eps for b in BUDGETS})
    (OUT / "final_audit.json").write_text(json.dumps({
        "method": "top30", "top_k": TOP_K, "seed": SEED,
        "selection_trials": [0, 1, 2, 3, 4], "audit_trials": [5, 6, 7, 8, 9],
        "zero_shot_macro_f1": float(zero_shot),
        "madrid_cv_reference": 0.6281,
        "audit": {str(b): audit[b] for b in BUDGETS},
        "per_class_25shot": {"control": [float(x) for x in f1r],
                             "candidate": [float(x) for x in f1c]},
        "confusion_25shot_rownorm": cmn.tolist(),
    }, indent=2))
    print(f"\nSaved -> {OUT}/stage1_madrid.pkl, stage1_rf.joblib, episodes.npz, final_audit.json")


if __name__ == "__main__":
    main()
