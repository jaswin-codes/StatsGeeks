"""Export presentation figures from the recorded results. No model is re-run.

Reads candidate/artifacts/*.json and writes PNGs to candidate/figures/.
Colours are the two-slot categorical pair validated for colour-vision
deficiency (CVD dE 24.7 light): #2a78d6 candidate, #eb6834 control.

Run from the repository root:
    python candidate/make_figures.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ART = Path("candidate/artifacts")
FIG = Path("candidate/figures")
FIG.mkdir(parents=True, exist_ok=True)

CAND, CTRL = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#0e141b", "#7c8794", "#e1e6ec"
BUDGETS = [5, 25, 50, 100, 200]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

audit = json.loads((ART / "final_audit.json").read_text())
search = json.loads((ART / "search_selection.json").read_text())
ZERO = audit["zero_shot_macro_f1"]
MADRID_CV = audit["madrid_cv_reference"]


# ---------------------------------------------------------------- Figure 1
# THE REQUIRED DELIVERABLE: macro F1 with error bars vs log2(sample size)
def fig_learning_curve():
    fig, ax = plt.subplots(figsize=(8, 5))
    cm = [audit["audit"][str(b)]["cand_mean"] for b in BUDGETS]
    cs = [audit["audit"][str(b)]["cand_std"] for b in BUDGETS]
    rm = [audit["audit"][str(b)]["control_mean"] for b in BUDGETS]
    rs = [audit["audit"][str(b)]["control_std"] for b in BUDGETS]

    ax.axhline(MADRID_CV, color=MUTED, ls="--", lw=1.3, zorder=1)
    ax.text(5.2, MADRID_CV + 0.004, f"Madrid CV (full data) = {MADRID_CV:.4f}",
            fontsize=8.5, color=MUTED)
    ax.axhline(ZERO, color=MUTED, ls=":", lw=1.3, zorder=1)
    ax.text(5.2, ZERO + 0.004, f"Zero-shot, no Amsterdam labels = {ZERO:.4f}",
            fontsize=8.5, color=MUTED)

    ax.errorbar(BUDGETS, rm, yerr=rs, fmt="s--", color=CTRL, lw=1.8, ms=6,
                capsize=4, label="Target-only prototypes (control)", zorder=3)
    ax.errorbar(BUDGETS, cm, yerr=cs, fmt="o-", color=CAND, lw=2.2, ms=7,
                capsize=4, label="Madrid-learned transfer (top30)", zorder=4)

    ax.set_xscale("log", base=2)
    ax.set_xticks(BUDGETS)
    ax.set_xticklabels([str(b) for b in BUDGETS])
    ax.set_xlabel("Labelled Amsterdam examples per class  (log$_2$ scale)")
    ax.set_ylabel("Macro F1  (four classes)")
    ax.set_title("Few-shot transfer to Amsterdam\nHeld-out audit episodes, mean ± 1 SD over 5 matched draws",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.set_ylim(0.40, 0.66)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.text(0.01, -0.03,
             "Error bars are spreads across episodes, not confidence intervals.",
             fontsize=8, color=MUTED)
    fig.savefig(FIG / "fig1_learning_curve.png")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 2
def fig_transfer_benefit():
    """The comparison that actually demonstrates transfer."""
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ben = [audit["audit"][str(b)]["benefit"] for b in BUDGETS]
    wins = [audit["audit"][str(b)]["wins"] for b in BUDGETS]
    x = np.arange(len(BUDGETS))
    bars = ax.bar(x, ben, width=0.55, color=CAND, zorder=3)
    for i, (bx, bv, wn) in enumerate(zip(x, ben, wins)):
        ax.text(bx, bv + 0.00025, f"+{bv:.4f}", ha="center", fontsize=9,
                fontweight="bold", color=CAND)
        ax.text(bx, -0.0006, f"{wn}/5 episodes", ha="center", fontsize=8, color=MUTED)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{b}" for b in BUDGETS])
    ax.set_xlabel("Labelled Amsterdam examples per class")
    ax.set_ylabel("Macro F1 gain over control")
    ax.set_title("Transfer benefit: Madrid-learned metric vs target-only prototypes\n"
                 "Paired on identical episodes — positive at every budget",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.set_ylim(-0.0015, max(ben) * 1.35)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    fig.savefig(FIG / "fig2_transfer_benefit.png")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3
def fig_method_ablation():
    """Nine representations, ranked. The control is highlighted."""
    names = list(search["results"].keys())
    means = {k: np.mean([np.mean(search["results"][k][str(b)]) for b in BUDGETS])
             for k in names}
    order = sorted(names, key=lambda k: means[k])
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(order))
    colors = [CTRL if k == "raw" else CAND for k in order]
    ax.barh(y, [means[k] for k in order], color=colors, height=0.62, zorder=3)
    ax.axvline(means["raw"], color=CTRL, ls="--", lw=1.3, zorder=4)
    for i, k in enumerate(order):
        ax.text(means[k] + 0.0015, i, f"{means[k]:.4f}", va="center",
                fontsize=8.5, color=INK)
    labels = {"raw": "raw  (control — no Madrid learning)",
              "proba": "proba  (RF output space)",
              "lda": "lda  (rank-3 projection)",
              "wcw10": "wcw10  (within-class whitening)",
              "top20": "top20  (top 20 features)",
              "wcw30": "wcw30  (whitening, more shrinkage)",
              "wcw10_rfw": "wcw10_rfw  (whiten + weight)",
              "rfw": "rfw  (importance weighting)",
              "leaf": "leaf  (RF partition proximity)",
              "top30": "top30  (top 30 features, weighted)"}
    ax.set_yticks(y)
    ax.set_yticklabels([labels.get(k, k) for k in order], fontsize=9)
    ax.set_xlim(0.52, 0.605)
    ax.set_xlabel("Mean macro F1 across all five budgets  (selection trials only)")
    ax.set_title("What is worth transferring from Madrid?\n"
                 "Nine frozen source representations, identical procedure otherwise",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    fig.text(0.01, -0.02,
             "The top four are separated by 0.0012 across 5 trials and are not "
             "statistically distinguishable.", fontsize=8, color=MUTED)
    fig.savefig(FIG / "fig3_method_ablation.png")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 4
def fig_budget_dependence():
    """The main scientific finding: method ranking flips with label budget."""
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for k, col, lab in [("wcw10", CAND, "Within-class whitening"),
                        ("wcw10_rfw", CTRL, "Whitening + importance weighting")]:
        d = [np.mean(search["results"][k][str(b)]) - np.mean(search["results"]["raw"][str(b)])
             for b in BUDGETS]
        ax.plot(BUDGETS, d, "o-", color=col, lw=2.2, ms=7, label=lab, zorder=3)
        ax.annotate(f"{d[0]:+.4f}", (BUDGETS[0], d[0]), textcoords="offset points",
                    xytext=(6, -12), fontsize=8.5, color=col, fontweight="bold")
        ax.annotate(f"{d[-1]:+.4f}", (BUDGETS[-1], d[-1]), textcoords="offset points",
                    xytext=(-14, 8), fontsize=8.5, color=col, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.3)
    ax.text(5.4, 0.0016, "target-only control", fontsize=8.5, color=MUTED)
    ax.set_xscale("log", base=2)
    ax.set_xticks(BUDGETS)
    ax.set_xticklabels([str(b) for b in BUDGETS])
    ax.set_xlabel("Labelled Amsterdam examples per class  (log$_2$ scale)")
    ax.set_ylabel("Macro F1 gain over control")
    ax.set_title("The ranking depends on the label budget\n"
                 "Whitening hurts at 5 shots and helps at 200 — the same transform, opposite verdict",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.savefig(FIG / "fig4_budget_dependence.png")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 5
def fig_confusion():
    cm = np.array(audit["confusion_25shot_rownorm"])
    labs = ["C1\npre-1945", "C2\n1945–84", "C3\n1984–2004", "C4\n2004+"]
    fig, ax = plt.subplots(figsize=(5.6, 5))
    im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=1)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{cm[i,j]:.2f}", ha="center", va="center", fontsize=10,
                    color="white" if cm[i, j] > 0.55 else INK)
    ax.set_xticks(range(4)); ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_yticks(range(4)); ax.set_yticklabels(labs, fontsize=8.5)
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title("Where the transfer still fails\n25 shots/class, row-normalised (diagonal = recall)",
                 fontweight="bold", fontsize=11, loc="left")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.text(0.01, -0.02,
             "Class 2 is hardest: 37% of true C2 pixels are predicted C1.",
             fontsize=8, color=MUTED)
    fig.savefig(FIG / "fig5_confusion.png")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 6
def fig_per_class():
    pc = audit["per_class_25shot"]
    ctrl, cand = pc["control"], pc["candidate"]
    x = np.arange(4); w = 0.36
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.bar(x - w/2, ctrl, w, color=CTRL, label="Target-only control", zorder=3)
    ax.bar(x + w/2, cand, w, color=CAND, label="Madrid-learned transfer", zorder=3)
    for i in range(4):
        ax.text(x[i]-w/2, ctrl[i]+0.008, f"{ctrl[i]:.3f}", ha="center", fontsize=8, color=CTRL)
        ax.text(x[i]+w/2, cand[i]+0.008, f"{cand[i]:.3f}", ha="center", fontsize=8, color=CAND)
    ax.set_xticks(x)
    ax.set_xticklabels(["C1\npre-1945", "C2\n1945–84", "C3\n1984–2004", "C4\n2004+"], fontsize=9)
    ax.set_ylabel("Per-class F1")
    ax.set_ylim(0, 0.80)
    ax.set_title("Per-class performance at 25 shots\nGains concentrate in the oldest and newest classes",
                 fontweight="bold", fontsize=11.5, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.savefig(FIG / "fig6_per_class.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_learning_curve()
    fig_transfer_benefit()
    fig_method_ablation()
    fig_budget_dependence()
    fig_confusion()
    fig_per_class()
    for p in sorted(FIG.glob("*.png")):
        print(f"  {p}  ({p.stat().st_size/1024:.0f} KB)")
    print(f"\n{len(list(FIG.glob('*.png')))} figures written to {FIG}/")
