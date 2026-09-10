"""Arithmetic-only verification of frozen EXP-010 and provenance comparisons.

Loads existing JSON arrays. It does not train, predict, sample episodes, or write
scientific artifacts.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ART = Path(__file__).parent / "artifacts"
BUDGETS = (5, 25, 50, 100, 200)
EXPECTED = {
    5: (0.552428, 0.059539, 0.515220, 0.070198, 0.037208, 7),
    25: (0.612174, 0.013057, 0.608872, 0.014539, 0.003302, 8),
    50: (0.617273, 0.007839, 0.613500, 0.008332, 0.003773, 10),
    100: (0.619513, 0.004770, 0.614502, 0.004810, 0.005011, 10),
    200: (0.623982, 0.003646, 0.618943, 0.003824, 0.005040, 10),
}

joint = json.loads((ART / "joint_sweep.json").read_text())
comparison = json.loads((ART / "final_vs_starter.json").read_text())
total = 0
for budget in BUDGETS:
    row = joint["audit"][str(budget)]
    tuned = np.asarray(row["tuned_trials"], dtype=float)
    control = np.asarray(row["control_trials"], dtype=float)
    actual = (tuned.mean(), tuned.std(ddof=0), control.mean(), control.std(ddof=0),
              (tuned - control).mean(), int((tuned > control).sum()))
    assert np.allclose(actual[:5], EXPECTED[budget][:5], atol=5e-7, rtol=0)
    assert actual[5] == EXPECTED[budget][5]
    assert np.allclose((actual[0], actual[2], actual[4]),
                       (row["tuned"], row["control"], row["gain"]), atol=1e-15)
    assert actual[5] == row["wins"]
    assert comparison["ours"][str(budget)] == row["tuned_trials"]
    total += actual[5]
    print(f"{budget}: tuned={actual[0]:.6f} ± {actual[1]:.6f} "
          f"control={actual[2]:.6f} ± {actual[3]:.6f} "
          f"gain={actual[4]:+.6f} wins={actual[5]}/10")
assert total == 45
print("total paired wins: 45/50")
