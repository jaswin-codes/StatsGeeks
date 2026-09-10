"""Search over frozen Madrid source representations. Hypothesis-driven, not a sweep.

Every method is the SAME procedure - freeze a transform learned on Madrid only,
take Amsterdam class prototypes from support labels in that space. Only the
representation changes, so differences are attributable to the representation.

HYPOTHESES UNDER TEST
---------------------
H1 raw     No Madrid learning at all.                        THE CONTROL.
H2 rfw     Madrid says WHICH features matter -> weight them.
H3 lda     Madrid's supervised directions -> project onto them.
           (already known to fail: rank-3 collapse discards too much)
H4 proba   Madrid classifier's output space.
           (already known to fail badly: 4 dims discards too much)
H5 wcw     Madrid says which DIRECTIONS are within-class noise -> whiten them
           out. This is LDA's metric WITHOUT LDA's rank-3 projection, so it
           keeps all 60 dimensions. If H3 failed only because of the rank
           collapse, this should succeed where LDA did not.
H6 wcw+rfw Whiten, then weight. Do the two source signals compose?
H7 topk    Madrid importance used to SELECT rather than weight. Fewer, better
           dimensions should help most in the low-shot regime.
H8 leaf    Madrid's learned PARTITION itself: two pixels are similar if the
           forest's trees put them in the same leaves. The deepest use of the
           source model available - the full tree structure, not a summary.

Audit trials are NOT touched here. Selection only.

Run from the repository root:
    python candidate/search_representations.py
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

PKL      = Path("data/preprocessed/preprocessed_data.pkl")
OUT      = Path("candidate/artifacts")
BUDGETS  = [5, 25, 50, 100, 200]
N_TRIALS = 10
N_SELECT = 5
SEED     = 42
RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=SEED, n_jobs=-1)
OUT.mkdir(parents=True, exist_ok=True)


def build_episodes(y, budgets, n_trials, seed):
    rng = np.random.default_rng(seed)
    classes = np.unique(y)
    max_b = max(budgets)
    eps = {}
    for t in range(n_trials):
        perms = {int(c): rng.permutation(np.where(y == c)[0])[:max_b] for c in classes}
        eps[t] = {b: np.concatenate([perms[int(c)][:b] for c in classes]) for b in budgets}
    return eps


def proto_predict(Zs, ys, Zq):
    classes = np.unique(ys)
    protos = np.stack([Zs[ys == c].mean(axis=0) for c in classes])
    d = (Zq ** 2).sum(1)[:, None] - 2.0 * Zq @ protos.T + (protos ** 2).sum(1)[None, :]
    return classes[d.argmin(axis=1)]


def within_class_whitener(X, y, shrink):
    """Sw^{-1/2} from Madrid's pooled within-class scatter, with shrinkage.

    Euclidean distance after this transform == Mahalanobis distance under the
    source's within-class covariance. It encodes 'directions that vary a lot
    WITHIN a class are not evidence about the class'.
    """
    d = X.shape[1]
    Sw = np.zeros((d, d))
    for c in np.unique(y):
        Xc = X[y == c]
        Xc = Xc - Xc.mean(0)
        Sw += Xc.T @ Xc
    Sw /= len(X)
    Sw = (1.0 - shrink) * Sw + shrink * (np.trace(Sw) / d) * np.eye(d)
    vals, vecs = np.linalg.eigh(Sw)
    vals = np.maximum(vals, 1e-10)
    return vecs @ np.diag(vals ** -0.5) @ vecs.T


def leaf_predict(rf, leaves_all, sup, ys, qmask):
    """RF-proximity prototypes: similarity = fraction of trees sharing a leaf.

    Uses the forest's actual learned partition rather than any summary of it.
    """
    Ls, Lq = leaves_all[sup], leaves_all[qmask]
    classes = np.unique(ys)
    score = np.zeros((Lq.shape[0], len(classes)))
    n_trees = Ls.shape[1]
    for t in range(n_trees):
        col_s, col_q = Ls[:, t], Lq[:, t]
        size = int(max(col_s.max(), col_q.max())) + 1
        for ci, c in enumerate(classes):
            counts = np.bincount(col_s[ys == c], minlength=size)
            score[:, ci] += counts[col_q] / max(int((ys == c).sum()), 1)
    return classes[score.argmax(axis=1)]      # highest proximity wins


def main():
    print("=" * 80)
    print("REPRESENTATION SEARCH  (selection trials only - audit stays sealed)")
    print("=" * 80)

    with PKL.open("rb") as f:
        d = pickle.load(f)
    Xm, ym, Xa, ya = d["X_madrid"], d["y_madrid"], d["X_amsterdam"], d["y_amsterdam"]
    feat_names = list(d["feature_names"])

    print("\n-- Stage 1: Madrid only --")
    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS).fit(Xm, ym)
    print(f"   RF ({time.time()-t0:.0f}s)")
    lda = LinearDiscriminantAnalysis().fit(Xm, ym)
    imp = rf.feature_importances_
    w = np.sqrt(imp)

    t0 = time.time()
    W10 = within_class_whitener(Xm, ym, 0.10)
    W30 = within_class_whitener(Xm, ym, 0.30)
    print(f"   within-class whiteners ({time.time()-t0:.1f}s)")

    top20 = np.argsort(imp)[::-1][:20]
    top30 = np.argsort(imp)[::-1][:30]

    METHODS = {
        "raw":       ("H1 control - no Madrid learning",        lambda X: X),
        "rfw":       ("H2 importance weighting",                lambda X: X * w),
        "lda":       ("H3 supervised projection (rank 3)",      lambda X: lda.transform(X)),
        "proba":     ("H4 classifier output space",             lambda X: rf.predict_proba(X)),
        "wcw10":     ("H5 within-class whitening, shrink 0.10", lambda X: X @ W10),
        "wcw30":     ("H5 within-class whitening, shrink 0.30", lambda X: X @ W30),
        "wcw10_rfw": ("H6 whiten then weight",                  lambda X: (X @ W10) * w),
        "top20":     ("H7 top-20 features, weighted",           lambda X: X[:, top20] * w[top20]),
        "top30":     ("H7 top-30 features, weighted",           lambda X: X[:, top30] * w[top30]),
    }

    print("\n-- Transforming Amsterdam through each frozen state --")
    Za = {}
    for k, (_, fn) in METHODS.items():
        Za[k] = np.ascontiguousarray(fn(Xa), dtype=np.float64)
        print(f"   {k:11s} {Za[k].shape[1]:3d} dims")

    print("   leaf        (RF partition, computed per episode)")
    t0 = time.time()
    leaves_all = rf.apply(Xa)
    print(f"   rf.apply -> {leaves_all.shape}  ({time.time()-t0:.0f}s)")

    eps = build_episodes(ya, BUDGETS, N_TRIALS, SEED)
    n_all = len(ya)
    names = list(METHODS) + ["leaf"]
    res = {k: {b: [] for b in BUDGETS} for k in names}

    print(f"\n-- Evaluating on selection trials 0-{N_SELECT-1} --")
    for t in range(N_SELECT):
        for b in BUDGETS:
            sup = eps[t][b]
            qmask = np.ones(n_all, dtype=bool)
            qmask[sup] = False
            ys, yq = ya[sup], ya[qmask]
            for k in METHODS:
                Z = Za[k]
                res[k][b].append(f1_score(yq, proto_predict(Z[sup], ys, Z[qmask]),
                                          average="macro", zero_division=0))
            res["leaf"][b].append(
                f1_score(yq, leaf_predict(rf, leaves_all, sup, ys, qmask),
                         average="macro", zero_division=0))
        print(f"   trial {t} done")

    print("\n" + "=" * 80)
    print("SELECTION RESULTS - macro F1 (mean over 5 selection trials)")
    print("=" * 80)
    print(f"{'method':<12}" + "".join(f"{b:>10}" for b in BUDGETS) + f"{'mean':>10}")
    order = sorted(names, key=lambda k: -np.mean([np.mean(res[k][b]) for b in BUDGETS]))
    for k in order:
        means = [np.mean(res[k][b]) for b in BUDGETS]
        print(f"{k:<12}" + "".join(f"{v:>10.4f}" for v in means) + f"{np.mean(means):>10.4f}")

    print("\n" + "=" * 80)
    print("BENEFIT vs CONTROL  (paired, same episodes)")
    print("=" * 80)
    print(f"{'method':<12}" + "".join(f"{b:>10}" for b in BUDGETS) + f"{'wins':>10}")
    for k in order:
        if k == "raw":
            continue
        row, wins, tot = f"{k:<12}", 0, 0
        for b in BUDGETS:
            diff = np.array(res[k][b]) - np.array(res["raw"][b])
            row += f"{diff.mean():>+10.4f}"
            wins += int((diff > 0).sum()); tot += len(diff)
        print(row + f"{f'{wins}/{tot}':>10}")

    best = max((k for k in names if k != "raw"),
               key=lambda k: np.mean([np.mean(res[k][b]) for b in BUDGETS]))
    print(f"\n   BEST ON SELECTION: '{best}'  ({dict(METHODS).get(best, ('RF partition proximity',))[0] if best in METHODS else 'H8 RF partition proximity'})")
    print("   Audit trials remain untouched. Confirm with a single audit run.")

    (OUT / "search_selection.json").write_text(json.dumps({
        "note": "SELECTION TRIALS ONLY (0-4). Audit trials 5-9 not touched.",
        "budgets": BUDGETS, "n_select": N_SELECT, "seed": SEED, "best_on_selection": best,
        "results": {k: {str(b): [float(x) for x in res[k][b]] for b in BUDGETS} for k in names},
    }, indent=2))
    print(f"\nSaved -> {OUT}/search_selection.json")


if __name__ == "__main__":
    main()
