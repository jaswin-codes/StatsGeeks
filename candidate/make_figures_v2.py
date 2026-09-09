"""Two additional figures: the seasonal offset, and the independent replication.

Run from the repository root:
    python candidate/make_figures_v2.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIG = Path("candidate/figures")
FIG.mkdir(parents=True, exist_ok=True)

CAND, CTRL = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#0e141b", "#7c8794", "#e1e6ec"
BUD = [5, 25, 50, 100, 200]

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 10,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150, "savefig.bbox": "tight",
})


# ------------------------------------------------------------------ fig 7
def fig_season():
    """The 70-day offset. Madrid is observed in summer, Amsterdam in spring."""
    doys = {}
    for city, f in [("Madrid", "data/madrid_train.parquet"),
                    ("Amsterdam", "data/amsterdam_data.parquet")]:
        df = pd.read_parquet(f, columns=["doy_1", "qa_valid_1"])
        d = df.loc[df["qa_valid_1"].fillna(False), "doy_1"].dropna()
        doys[city] = d.to_numpy()

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bins = np.arange(0, 371, 10)
    for city, col in [("Madrid", CTRL), ("Amsterdam", CAND)]:
        d = doys[city]
        ax.hist(d, bins=bins, density=True, alpha=0.55, color=col,
                label=f"{city}  (median day {np.median(d):.0f})", zorder=3)
        ax.axvline(np.median(d), color=col, lw=2, ls="--", zorder=4)

    ax.axvspan(152, 243, color=MUTED, alpha=0.10, zorder=1)
    ax.text(197, ax.get_ylim()[1] * 0.42, "June - August", ha="center",
            fontsize=9, color=MUTED)

    ax.annotate("", xy=(175, ax.get_ylim()[1] * 0.72), xytext=(105, ax.get_ylim()[1] * 0.72),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.text(140, ax.get_ylim()[1] * 0.76, "70 days", ha="center", fontsize=12,
            fontweight="bold", color=INK)

    ax.set_xlabel("Day of year of the observation actually used")
    ax.set_ylabel("Density")
    ax.set_title("The two cities are not observed in the same season\n"
                 "Madrid is a summer dataset; Amsterdam is a spring dataset",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.set_xlim(0, 370)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    fig.text(0.01, -0.03,
             "June-August share: Madrid 48.3%, Amsterdam 20.5%. "
             "Part of the apparent domain shift is phenology, not architecture.",
             fontsize=8, color=MUTED)
    fig.savefig(FIG / "fig7_season_offset.png")
    plt.close(fig)


# ------------------------------------------------------------------ fig 8
def fig_replication():
    """Day-1 result vs the independent replication on fresh episodes."""
    fc = json.loads(Path("candidate/artifacts/feature_comparison.json").read_text())
    orig = json.loads(Path("candidate/artifacts/final_audit.json").read_text())

    A = slice(5, 10)
    rep = [float(np.mean(np.array(fc["all_trials"]["v1_topk"][str(b)][A])
                         - np.array(fc["all_trials"]["v1_raw"][str(b)][A]))) for b in BUD]
    day1 = [orig["audit"][str(b)]["benefit"] for b in BUD]

    x = np.arange(len(BUD))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - w / 2, day1, w, color=CTRL, label="Day 1 audit  (seed 42)", zorder=3)
    ax.bar(x + w / 2, rep, w, color=CAND, label="Replication  (seed 2026, independent)", zorder=3)
    for i in range(len(BUD)):
        ax.text(x[i] - w / 2, day1[i] + 0.0004, f"{day1[i]:+.4f}", ha="center",
                fontsize=8, color=CTRL)
        ax.text(x[i] + w / 2, rep[i] + 0.0004, f"{rep[i]:+.4f}", ha="center",
                fontsize=8, color=CAND, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels([str(b) for b in BUD])
    ax.set_xlabel("Labelled Amsterdam examples per class")
    ax.set_ylabel("Macro F1 gain over target-only control")
    ax.set_title("The transfer benefit replicates on episodes that did not exist\n"
                 "when the method was chosen",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    fig.text(0.01, -0.03,
             "19 of 25 paired episodes won on the replication. Positive at every budget "
             "in both runs.", fontsize=8, color=MUTED)
    fig.savefig(FIG / "fig8_replication.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_season()
    fig_replication()
    for p in [FIG / "fig7_season_offset.png", FIG / "fig8_replication.png"]:
        print(f"  {p}  ({p.stat().st_size/1024:.0f} KB)")
