"""EXP-010: joint sweep of dimensionality (k) and shrinkage (lambda) per budget.

THE THESIS
----------
Every result so far has been the same phenomenon in disguise: in the few-shot
regime, performance is limited by ESTIMATION ERROR in the class prototypes, not
by the classifier.

  EXP-004  whitening flips sign with budget  (amplifies noisy directions)
  EXP-007  94 features lose to 60            (dilution)
  EXP-009  shrinkage helps most at 5 shots   (borrowing a stable estimate)

If that is the right frame, then the optimal NUMBER OF FEATURES should also
depend on the budget: few dimensions when you have 5 labels, more when you have
200. Each dimension you keep must earn its estimation cost.

This tests both knobs together, which is also the mentor's suggestion #3 -
strip away what is not carrying weight, rather than adding more.

  k       how many Madrid-ranked features to keep
  lambda  how hard to shrink the support prototype toward Madrid's class geometry

PROTOCOL
--------
(k, lambda) chosen per budget on the seed-2026 SELECTION trials only.
Audited once on seed 31337, a fourth episode set never used for anything.

Run from the repository root:
    python candidate/joint_sweep.py
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

PKL = Path("data/preprocessed/preprocessed_data.pkl")
OUT = Path("candidate/artifacts")
BUDGETS = [5, 25, 50, 100, 200]
KS = [5, 10, 15, 20, 30, 45, 60]
LAMS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
SELECT_SEED, AUDIT_SEED = 2026, 31337
RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=42, n_jobs=-1)


def episodes(y, seed, n):
    rng = np.random.default_rng(seed)
    eps = {}
    for t in range(n):
        perms = {int(c): rng.permutation(np.where(y == c)[0])[:max(BUDGETS)]
                 for c in np.unique(y)}
        eps[t] = {b: np.concatenate([perms[int(c)][:b] for c in np.unique(y)])
                  for b in BUDGETS}
    return eps


def main():
    print("=" * 78)
    print("EXP-010  joint (k, lambda) sweep - is optimal dimensionality also")
    print("         budget-dependent?")
    print("=" * 78)

    with PKL.open("rb") as f:
        d = pickle.load(f)
    Xm, ym = d["X_madrid"], d["y_madrid"]
    Xa, ya = d["X_amsterdam"], d["y_amsterdam"]
    cls = np.unique(ya)

    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS).fit(Xm, ym)
    imp = rf.feature_importances_
    w = np.sqrt(imp)
    rank = np.argsort(imp)[::-1]
    print(f"Stage 1 RF ({time.time()-t0:.0f}s)")

    # per-k frozen representation plus Madrid class offsets in that space
    REP = {}
    for k in KS:
        sel = np.sort(rank[:k])
        Zm = Xm[:, sel] * w[sel]
        mu = Zm.mean(axis=0)
        REP[k] = {"Za": np.ascontiguousarray(Xa[:, sel] * w[sel]),
                  "delta": np.stack([Zm[ym == c].mean(axis=0) - mu for c in cls])}
    print(f"built {len(KS)} representations: k = {KS}")

    def score(k, lam, sup, qm, ys, yq):
        Za, delta = REP[k]["Za"], REP[k]["delta"]
        Zs, Zq = Za[sup], Za[qm]
        mu_a = Zs.mean(axis=0)                       # support only
        P = np.stack([mu_a + lam * delta[i] + (1 - lam) * (Zs[ys == c].mean(axis=0) - mu_a)
                      for i, c in enumerate(cls)])
        dd = (Zq ** 2).sum(1)[:, None] - 2 * Zq @ P.T + (P ** 2).sum(1)[None, :]
        return f1_score(yq, cls[dd.argmin(1)], average="macro", zero_division=0)

    def sweep(eps, n_tr):
        acc = {}
        n = len(ya)
        for t in range(n_tr):
            for b in BUDGETS:
                sup = eps[t][b]
                qm = np.ones(n, bool); qm[sup] = False
                ys, yq = ya[sup], ya[qm]
                for k in KS:
                    for lam in LAMS:
                        acc.setdefault((b, k, lam), []).append(score(k, lam, sup, qm, ys, yq))
        return acc

    print(f"\nSELECTION sweep on seed {SELECT_SEED}, trials 0-4 "
          f"({len(KS)*len(LAMS)} configs x {len(BUDGETS)} budgets)...")
    t0 = time.time()
    sel = sweep(episodes(ya, SELECT_SEED, 5), 5)
    print(f"   done ({time.time()-t0:.0f}s)")

    best = {}
    print(f"\n{'budget':>7}{'best k':>8}{'best lam':>10}{'selection F1':>14}"
          f"{'  vs k=60,lam=0':>17}")
    for b in BUDGETS:
        bk, bl = max(((k, l) for k in KS for l in LAMS),
                     key=lambda kl: np.mean(sel[(b, kl[0], kl[1])]))
        base = float(np.mean(sel[(b, 60, 0.0)]))
        best[b] = (bk, bl)
        print(f"{b:>7}{bk:>8}{bl:>10.1f}{np.mean(sel[(b,bk,bl)]):>14.4f}"
              f"{np.mean(sel[(b,bk,bl)])-base:>+17.4f}")

    # does optimal k rise with budget?
    ks = [best[b][0] for b in BUDGETS]
    lams = [best[b][1] for b in BUDGETS]
    print(f"\n   optimal k      by budget: {ks}")
    print(f"   optimal lambda by budget: {lams}")
    print(f"   k non-decreasing with budget?      {all(x <= y for x, y in zip(ks, ks[1:]))}")
    print(f"   lambda non-increasing with budget? {all(x >= y for x, y in zip(lams, lams[1:]))}")

    # ---- audit on a fourth, untouched set ---------------------------------
    print(f"\nFINAL AUDIT on seed {AUDIT_SEED} - never used for anything")
    eps_a = episodes(ya, AUDIT_SEED, 10)
    n = len(ya)
    rows = {}
    print(f"\n{'shots':>7}{'control':>11}{'tuned':>11}{'gain':>10}{'wins':>9}"
          f"{'   (k, lam)':>13}")
    tot = 0
    for b in BUDGETS:
        bk, bl = best[b]
        c0, c1 = [], []
        for t in range(10):
            sup = eps_a[t][b]
            qm = np.ones(n, bool); qm[sup] = False
            ys, yq = ya[sup], ya[qm]
            c0.append(score(60, 0.0, sup, qm, ys, yq))    # full-dim, no shrinkage
            c1.append(score(bk, bl, sup, qm, ys, yq))
        c0, c1 = np.array(c0), np.array(c1)
        g = c1 - c0
        tot += int((g > 0).sum())
        rows[b] = {"control": float(c0.mean()), "tuned": float(c1.mean()),
                   "gain": float(g.mean()), "wins": int((g > 0).sum()),
                   "k": int(bk), "lambda": float(bl),
                   "control_trials": [float(x) for x in c0],
                   "tuned_trials": [float(x) for x in c1]}
        print(f"{b:>7}{c0.mean():>11.4f}{c1.mean():>11.4f}{g.mean():>+10.4f}"
              f"{f'{int((g>0).sum())}/10':>9}{f'({bk}, {bl})':>13}")
    print(f"\n   total paired wins: {tot}/50")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "joint_sweep.json").write_text(json.dumps({
        "select_seed": SELECT_SEED, "audit_seed": AUDIT_SEED,
        "ks": KS, "lambdas": LAMS,
        "best_per_budget": {str(b): {"k": best[b][0], "lambda": best[b][1]} for b in BUDGETS},
        "selection_grid": {f"{b}|{k}|{l}": float(np.mean(sel[(b, k, l)]))
                           for b in BUDGETS for k in KS for l in LAMS},
        "audit": {str(b): rows[b] for b in BUDGETS},
    }, indent=2))
    print(f"\nSaved -> {OUT}/joint_sweep.json")


if __name__ == "__main__":
    main()
