"""Source-learned transfer candidate: frozen Madrid representation + Amsterdam prototypes.

WHAT THIS FIXES IN THE STARTER
------------------------------
The organiser's few-shot path computes Amsterdam class prototypes directly from
raw Amsterdam features. The Madrid-trained Random Forest is never used, so Madrid
contributes only the scaler's mean/variance. That is target-only fitting, not
supervised transfer.

Here every method is the same procedure:

    represent Amsterdam through a transform T learned on MADRID ONLY,
    then take class prototypes from the SUPPORT pixels in T-space.

Methods differ ONLY in T, so the comparison is a controlled experiment:

    raw    T(x) = x                          <- no Madrid learning. THE CONTROL.
    rfw    T(x) = x * sqrt(importances)      <- Madrid-learned feature weighting
    lda    T(x) = LDA.transform(x)           <- Madrid-learned supervised projection
    proba  T(x) = RF.predict_proba(x)        <- Madrid classifier's own output space
    logit  T(x) = log(RF.predict_proba(x))   <- same, log-odds scaled

`proba` is the interesting one. Zero-shot fails on Amsterdam largely because
Madrid's classes map onto Amsterdam's differently (Class 3 recall was 0.19).
Taking prototypes in the Madrid classifier's OUTPUT space lets a handful of
Amsterdam labels re-learn that mapping, while every decision boundary the
forest learned stays frozen.

Beating zero-shot proves nothing. Beating `raw` on matched episodes is the
evidence that Madrid supervision helped.

PROTOCOL GUARANTEES
-------------------
* Madrid-only training. Amsterdam labels never touch T.
* Support/query strictly disjoint; query labels used for scoring only.
* Episodes MATCHED across methods and NESTED across budgets.
* Episode indices STORED, not regenerated from a seed.
* FINAL-AUDIT SEPARATION: trials 0-4 select the method, trials 5-9 are held back
  and reported once. The winner is never chosen using audit trials.
* T fitted once, frozen, reused for every episode. Never refit on target.
* Label-free inference: T never sees a label.

Run from the repository root:
    python candidate/transfer_candidate.py
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score

PKL      = Path("data/preprocessed/preprocessed_data.pkl")
OUT      = Path("candidate/artifacts")
BUDGETS  = [5, 25, 50, 100, 200]
N_TRIALS = 10
N_SELECT = 5          # trials 0-4 select; trials 5-9 are the held-out audit
SEED     = 42
RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=SEED, n_jobs=-1)

OUT.mkdir(parents=True, exist_ok=True)


def build_episodes(y, budgets, n_trials, seed):
    """Matched, nested support draws. Each budget reads a prefix of one permutation."""
    rng = np.random.default_rng(seed)
    classes = np.unique(y)
    max_b = max(budgets)
    for c in classes:
        if int((y == c).sum()) < max_b:
            raise ValueError(f"class {c} smaller than max budget {max_b}")
    episodes = {}
    for t in range(n_trials):
        perms = {int(c): rng.permutation(np.where(y == c)[0])[:max_b] for c in classes}
        episodes[t] = {b: np.concatenate([perms[int(c)][:b] for c in classes]) for b in budgets}
    return episodes


def prototype_predict(Xs, ys, Xq):
    """Nearest-class-prototype. Support labels only; never sees query labels."""
    classes = np.unique(ys)
    protos = np.stack([Xs[ys == c].mean(axis=0) for c in classes])
    d = (Xq ** 2).sum(1)[:, None] - 2.0 * Xq @ protos.T + (protos ** 2).sum(1)[None, :]
    return classes[d.argmin(axis=1)]


def main():
    print("=" * 78)
    print("SOURCE-LEARNED TRANSFER CANDIDATE")
    print("=" * 78)

    with PKL.open("rb") as f:
        data = pickle.load(f)
    Xm, ym = data["X_madrid"], data["y_madrid"]
    Xa, ya = data["X_amsterdam"], data["y_amsterdam"]
    feat_names = list(data["feature_names"])
    print(f"\nMadrid {Xm.shape}   Amsterdam {Xa.shape}   features {len(feat_names)}")

    # ---- Stage 1: Madrid only -------------------------------------------------
    print("\n-- Stage 1: fitting source state on Madrid only --")
    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS)
    rf.fit(Xm, ym)
    print(f"   RF trained ({time.time() - t0:.0f}s)")
    lda = LinearDiscriminantAnalysis().fit(Xm, ym)
    print(f"   LDA fitted -> {lda.transform(Xm[:1]).shape[1]} components")

    importances = rf.feature_importances_
    w = np.sqrt(importances)
    EPS = 1e-9

    TRANSFORMS = {
        "raw":   ("target-only prototypes (control, no Madrid learning)", lambda X: X),
        "rfw":   ("Madrid RF importance-weighted metric",                 lambda X: X * w),
        "lda":   ("Madrid supervised LDA projection",                     lambda X: lda.transform(X)),
        "proba": ("Madrid RF probability space",                          lambda X: rf.predict_proba(X)),
        "logit": ("Madrid RF log-probability space",                      lambda X: np.log(rf.predict_proba(X) + EPS)),
    }

    zero_shot = f1_score(ya, rf.predict(Xa), average="macro")
    print(f"   Madrid RF zero-shot on Amsterdam: {zero_shot:.4f}")

    # ---- Episodes -------------------------------------------------------------
    print(f"\n-- Episodes: {N_TRIALS} trials x {len(BUDGETS)} budgets, matched + nested --")
    episodes = build_episodes(ya, BUDGETS, N_TRIALS, SEED)
    nested_ok = all(
        set(episodes[t][BUDGETS[i]]).issubset(set(episodes[t][BUDGETS[i + 1]]))
        for t in episodes for i in range(len(BUDGETS) - 1)
    )
    print(f"   nesting verified: {nested_ok}")
    print(f"   selection trials 0-{N_SELECT-1} | HELD-OUT AUDIT trials {N_SELECT}-{N_TRIALS-1}")

    print("\n-- Transforming Amsterdam through each frozen source state --")
    Xa_t = {}
    for k, (_, fn) in TRANSFORMS.items():
        t1 = time.time()
        Xa_t[k] = np.ascontiguousarray(fn(Xa), dtype=np.float64)
        print(f"   {k:6s} -> {Xa_t[k].shape[1]:3d} dims  ({time.time()-t1:.1f}s)")

    # ---- Evaluate -------------------------------------------------------------
    results = {k: {b: [] for b in BUDGETS} for k in TRANSFORMS}
    n_all = len(ya)
    for t in range(N_TRIALS):
        for b in BUDGETS:
            sup = episodes[t][b]
            qmask = np.ones(n_all, dtype=bool)
            qmask[sup] = False
            y_sup, y_qry = ya[sup], ya[qmask]
            for k in TRANSFORMS:
                Z = Xa_t[k]
                pred = prototype_predict(Z[sup], y_sup, Z[qmask])
                results[k][b].append(f1_score(y_qry, pred, average="macro", zero_division=0))

    sel = slice(0, N_SELECT)
    aud = slice(N_SELECT, N_TRIALS)

    def m(k, b, sl):
        return float(np.mean(results[k][b][sl]))

    # ---- Selection ------------------------------------------------------------
    print("\n" + "=" * 78)
    print(f"SELECTION PHASE  (trials 0-{N_SELECT-1} only)   benefit vs the 'raw' control")
    print("=" * 78)
    print(f"{'shots':>7}" + "".join(f"{k:>14}" for k in TRANSFORMS if k != "raw"))
    for b in BUDGETS:
        row = f"{b:>7}"
        for k in TRANSFORMS:
            if k == "raw":
                continue
            row += f"{m(k,b,sel) - m('raw',b,sel):>+14.4f}"
        print(row)

    # pick the winner on 25-shot selection performance (the stability target)
    cands = [k for k in TRANSFORMS if k != "raw"]
    winner = max(cands, key=lambda k: m(k, 25, sel))
    print(f"\n   Selected on 25-shot selection trials: '{winner}' "
          f"({TRANSFORMS[winner][0]})")

    # ---- Audit ----------------------------------------------------------------
    print("\n" + "=" * 78)
    print(f"FINAL AUDIT  (held-out trials {N_SELECT}-{N_TRIALS-1}, never used for selection)")
    print("=" * 78)
    print(f"{'shots':>7}{'control (raw)':>22}{'  ' + winner:>22}{'benefit':>12}{'wins':>8}")
    for b in BUDGETS:
        r = np.array(results["raw"][b][aud])
        c = np.array(results[winner][b][aud])
        d = c - r
        print(f"{b:>7}{r.mean():>13.4f} +/-{r.std():.4f}"
              f"{c.mean():>13.4f} +/-{c.std():.4f}"
              f"{d.mean():>+12.4f}{int((d>0).sum())}/{len(d):>4}")

    print(f"\n   Zero-shot Madrid RF (no Amsterdam labels): {zero_shot:.4f}")
    print("   Beating zero-shot is NOT evidence of transfer. Beating 'raw' is.")

    # ---- Per-class evidence for the winner at 25 shots ------------------------
    sup = episodes[N_SELECT][25]
    qmask = np.ones(n_all, dtype=bool)
    qmask[sup] = False
    Zw = Xa_t[winner]
    pred_w = prototype_predict(Zw[sup], ya[sup], Zw[qmask])
    Zr = Xa_t["raw"]
    pred_r = prototype_predict(Zr[sup], ya[sup], Zr[qmask])
    yq = ya[qmask]

    print("\n" + "=" * 78)
    print(f"PER-CLASS F1 at 25 shots  (first audit episode)")
    print("=" * 78)
    f1_w = f1_score(yq, pred_w, average=None, labels=[1, 2, 3, 4], zero_division=0)
    f1_r = f1_score(yq, pred_r, average=None, labels=[1, 2, 3, 4], zero_division=0)
    print(f"{'class':>7}{'control':>12}{'  '+winner:>12}{'delta':>10}")
    for i, c in enumerate([1, 2, 3, 4]):
        print(f"{c:>7}{f1_r[i]:>12.4f}{f1_w[i]:>12.4f}{f1_w[i]-f1_r[i]:>+10.4f}")

    cm = confusion_matrix(yq, pred_w, labels=[1, 2, 3, 4])
    cm_n = cm / cm.sum(axis=1, keepdims=True)
    print(f"\nConfusion matrix, {winner}, row-normalised (diagonal = recall):")
    print("        pred1   pred2   pred3   pred4")
    for i, c in enumerate([1, 2, 3, 4]):
        print(f"  true{c}" + "".join(f"{v:>8.3f}" for v in cm_n[i]))

    # ---- Save -----------------------------------------------------------------
    with (OUT / "stage1_madrid.pkl").open("wb") as f:
        pickle.dump(
            {
                "lda": lda,
                "feature_importances": importances,
                "metric_weights": w,
                "feature_names": feat_names,
                "classes": [1, 2, 3, 4],
                "rf_params": RF_PARAMS,
                "seed": SEED,
                "trained_on": "madrid_only",
                "zero_shot_macro_f1": float(zero_shot),
                "selected_method": winner,
                "note": "Stage 1 source state for adaptation. Frozen; never refit on Amsterdam. "
                        "'proba'/'logit' methods additionally require stage1_rf.joblib.",
            },
            f,
        )
    import joblib
    joblib.dump(rf, OUT / "stage1_rf.joblib", compress=3)
    np.savez_compressed(
        OUT / "episodes.npz",
        **{f"t{t}_b{b}": episodes[t][b] for t in episodes for b in BUDGETS},
    )
    (OUT / "results.json").write_text(json.dumps({
        "zero_shot_macro_f1": float(zero_shot),
        "budgets": BUDGETS, "n_trials": N_TRIALS, "n_select": N_SELECT, "seed": SEED,
        "selected_method": winner,
        "methods": {k: v[0] for k, v in TRANSFORMS.items()},
        "selection": {k: {str(b): m(k, b, sel) for b in BUDGETS} for k in TRANSFORMS},
        "audit": {k: {str(b): {"mean": m(k, b, aud),
                               "std": float(np.std(results[k][b][aud])),
                               "trials": [float(x) for x in results[k][b][aud]]}
                      for b in BUDGETS} for k in TRANSFORMS},
        "all_trials": {k: {str(b): [float(x) for x in results[k][b]] for b in BUDGETS}
                       for k in TRANSFORMS},
    }, indent=2))
    print(f"\nSaved -> {OUT}/  (stage1_madrid.pkl, stage1_rf.joblib, episodes.npz, results.json)")


if __name__ == "__main__":
    main()
