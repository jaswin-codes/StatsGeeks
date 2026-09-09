"""EXP-009: prototype shrinkage toward Madrid's class geometry.

THE IDEA
--------
Everything we have transferred so far is a feature RANKING - 60 importance
weights. A fair criticism is that this is the weakest form of transfer that
still qualifies. This module transfers the CLASS GEOMETRY instead.

At 5 shots, an Amsterdam class mean is estimated from 5 points in 60 dimensions:
nearly unbiased but very high variance. Madrid's class prototype is estimated
from 76,263 pixels: low variance, but biased, because it is a different city.

That is a textbook James-Stein / empirical-Bayes situation. Shrink the noisy
target estimate toward the stable source estimate:

    delta_c = mu_madrid_c - mu_madrid          (Madrid class OFFSET from its own mean)
    m_c     = support mean of class c          (noisy Amsterdam estimate)
    mu_A    = pooled mean of the SUPPORT set    (Amsterdam location, support only)

    p_c(lambda) = mu_A + lambda * delta_c + (1 - lambda) * (m_c - mu_A)

lambda = 0 is exactly the target-only control.
lambda = 1 is pure Madrid class structure, re-centred on Amsterdam.

Subtracting each city's own mean before transferring the offsets is a
first-order domain-shift correction: it moves the class geometry without
importing Madrid's absolute location in feature space.

DATA-USE DISCIPLINE
-------------------
mu_A is computed from the SUPPORT SET ONLY. Query features are never touched.
MASTER_PLAN.md lists unlabelled query alignment as an UNCONFIRMED permission, so
we do not use it, even though it would be easy and would probably help.

AUDIT HYGIENE
-------------
lambda is chosen on seed-2026 selection trials 0-4. The audit uses a THIRD,
brand-new episode set (seed 7777) that has never been used for anything.

Run from the repository root:
    python candidate/shrinkage_transfer.py
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
SELECT_SEED, AUDIT_SEED = 2026, 7777
N_TRIALS = 10
LAMBDAS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
RF_PARAMS = dict(n_estimators=500, class_weight="balanced", random_state=42, n_jobs=-1)


def episodes(y, seed, n=N_TRIALS):
    rng = np.random.default_rng(seed)
    eps = {}
    for t in range(n):
        perms = {int(c): rng.permutation(np.where(y == c)[0])[:max(BUDGETS)]
                 for c in np.unique(y)}
        eps[t] = {b: np.concatenate([perms[int(c)][:b] for c in np.unique(y)])
                  for b in BUDGETS}
    return eps


def assign(protos, classes, Zq):
    d = (Zq ** 2).sum(1)[:, None] - 2.0 * Zq @ protos.T + (protos ** 2).sum(1)[None, :]
    return classes[d.argmin(axis=1)]


def shrunk_prototypes(delta, Zs, ys, classes, lam):
    """Blend the Madrid class offsets with the Amsterdam support means."""
    mu_a = Zs.mean(axis=0)                       # support only - never the query
    out = np.empty((len(classes), Zs.shape[1]))
    for i, c in enumerate(classes):
        m_c = Zs[ys == c].mean(axis=0)
        out[i] = mu_a + lam * delta[i] + (1.0 - lam) * (m_c - mu_a)
    return out


def main():
    print("=" * 78)
    print("EXP-009  prototype shrinkage toward Madrid class geometry")
    print("=" * 78)

    with PKL.open("rb") as f:
        d = pickle.load(f)
    Xm, ym = d["X_madrid"], d["y_madrid"]
    Xa, ya = d["X_amsterdam"], d["y_amsterdam"]

    t0 = time.time()
    rf = RandomForestClassifier(**RF_PARAMS).fit(Xm, ym)
    w = np.sqrt(rf.feature_importances_)
    top = np.sort(np.argsort(rf.feature_importances_)[::-1][:30])
    print(f"Stage 1 RF trained ({time.time()-t0:.0f}s)")

    # two frozen representations, both Madrid-learned
    REPS = {
        "topk": (lambda X: X[:, top] * w[top]),
        "rfw":  (lambda X: X * w),
    }

    classes = np.unique(ya)
    state = {}
    for name, fn in REPS.items():
        Zm, Za = fn(Xm), np.ascontiguousarray(fn(Xa))
        mu_m = Zm.mean(axis=0)
        delta = np.stack([Zm[ym == c].mean(axis=0) - mu_m for c in classes])
        state[name] = {"Za": Za, "delta": delta}
        print(f"  {name}: {Za.shape[1]} dims, Madrid class offsets computed")

    def run(eps, n_tr):
        res = {}
        n_all = len(ya)
        for t in range(n_tr):
            for b in BUDGETS:
                sup = eps[t][b]
                qm = np.ones(n_all, bool)
                qm[sup] = False
                ys, yq = ya[sup], ya[qm]
                for rep in REPS:
                    Za, delta = state[rep]["Za"], state[rep]["delta"]
                    Zs, Zq = Za[sup], Za[qm]
                    for lam in LAMBDAS:
                        P = shrunk_prototypes(delta, Zs, ys, classes, lam)
                        f1 = f1_score(yq, assign(P, classes, Zq),
                                      average="macro", zero_division=0)
                        res.setdefault((rep, lam), {}).setdefault(b, []).append(f1)
        return res

    # ---- selection ---------------------------------------------------------
    print(f"\nSELECTION on seed {SELECT_SEED}, trials 0-4")
    sel = run(episodes(ya, SELECT_SEED), 5)
    print(f"\n{'lambda':>8}" + "".join(f"{b:>9}" for b in BUDGETS) + f"{'mean':>9}")
    for rep in REPS:
        print(f"  -- {rep} --")
        for lam in LAMBDAS:
            ms = [float(np.mean(sel[(rep, lam)][b])) for b in BUDGETS]
            star = "  <- control" if lam == 0.0 else ""
            print(f"{lam:>8.1f}" + "".join(f"{v:>9.4f}" for v in ms)
                  + f"{np.mean(ms):>9.4f}{star}")

    best = max(sel, key=lambda k: np.mean([np.mean(sel[k][b]) for b in BUDGETS]))
    base = ("topk", 0.0)
    print(f"\n   best on selection: rep={best[0]}  lambda={best[1]}")
    print(f"   vs lambda=0 control: "
          f"{np.mean([np.mean(sel[best][b]) for b in BUDGETS]) - np.mean([np.mean(sel[base][b]) for b in BUDGETS]):+.4f}")

    # per-budget best lambda, to see whether it varies with data volume
    print("\n   best lambda per budget (topk):")
    for b in BUDGETS:
        bl = max(LAMBDAS, key=lambda L: np.mean(sel[("topk", L)][b]))
        print(f"      {b:>4} shots -> lambda {bl}")

    # ---- audit on a THIRD, untouched episode set ---------------------------
    print(f"\nFINAL AUDIT on seed {AUDIT_SEED} - never used for anything")
    aud = run(episodes(ya, AUDIT_SEED), N_TRIALS)
    print(f"\n{'shots':>7}{'control':>11}{'shrunk':>11}{'gain':>10}{'wins':>9}")
    rows = {}
    for b in BUDGETS:
        c0 = np.array(aud[(best[0], 0.0)][b])
        cs = np.array(aud[best][b])
        g = cs - c0
        rows[b] = {"control": float(c0.mean()), "shrunk": float(cs.mean()),
                   "gain": float(g.mean()), "wins": int((g > 0).sum()), "n": len(g)}
        print(f"{b:>7}{c0.mean():>11.4f}{cs.mean():>11.4f}{g.mean():>+10.4f}"
              f"{f'{int((g>0).sum())}/{len(g)}':>9}")
    tot = sum(r["wins"] for r in rows.values())
    n = sum(r["n"] for r in rows.values())
    print(f"\n   total paired wins: {tot}/{n}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "shrinkage.json").write_text(json.dumps({
        "select_seed": SELECT_SEED, "audit_seed": AUDIT_SEED,
        "lambdas": LAMBDAS, "best_rep": best[0], "best_lambda": best[1],
        "selection": {f"{r}|{l}": {str(b): float(np.mean(sel[(r, l)][b])) for b in BUDGETS}
                      for (r, l) in sel},
        "audit": {str(b): rows[b] for b in BUDGETS},
        "audit_trials": {f"{r}|{l}": {str(b): [float(x) for x in aud[(r, l)][b]] for b in BUDGETS}
                         for (r, l) in aud},
    }, indent=2))
    print(f"\nSaved -> {OUT}/shrinkage.json")


if __name__ == "__main__":
    main()
