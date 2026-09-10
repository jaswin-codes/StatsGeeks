"""Build the submission deck. All numbers read from candidate/artifacts/*.json.

Design: colour-banded slides, short phrases rather than sentences, big figures.
16 slides - 12 main plus 4 backup - down from 21.

Run from the repository root:
    python presentation/build_deck.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ART = Path("candidate/artifacts")
FIGS = Path("candidate/figures")
OUT = Path("presentation/StatsGeeks_BuildingAge.pptx")
RESULTS_PLOT = Path("presentation/exp010_f1_log2.png")

js = json.loads((ART / "joint_sweep.json").read_text())
fc = json.loads((ART / "feature_comparison.json").read_text())
BUD = [5, 25, 50, 100, 200]
row = lambda b: js["audit"][str(b)]

# Frozen, audit-verified EXP-010 presentation values. These are not recomputed.
TUNED_SD = {5: 0.059539, 25: 0.013057, 50: 0.007839, 100: 0.004770, 200: 0.003646}
CONTROL_SD = {5: 0.070198, 25: 0.014539, 50: 0.008332, 100: 0.004810, 200: 0.003824}
MADRID_CV_MEAN = 0.6281
MADRID_CV_SD = 0.0043


def build_results_plot():
    """Render the rubric-required plot from frozen EXP-010 values only."""
    x = [math.log2(b) for b in BUD]
    tuned = [row(b)["tuned"] for b in BUD]
    control = [row(b)["control"] for b in BUD]
    tuned_sd = [TUNED_SD[b] for b in BUD]
    control_sd = [CONTROL_SD[b] for b in BUD]

    plt.rcParams.update({"font.family": "sans-serif", "font.size": 12})
    fig, ax = plt.subplots(figsize=(9.2, 5.4), dpi=180)
    ax.errorbar(x, tuned, yerr=tuned_sd, fmt="o-", color="#119d8f", lw=2.8,
                ms=7, capsize=5, capthick=1.7, label="EXP-010 tuned")
    ax.errorbar(x, control, yerr=control_sd, fmt="s--", color="#eb6834", lw=2.3,
                ms=6, capsize=5, capthick=1.7, label="Matched control")
    ax.set_xticks(x, [f"{v:.2f}\n({b} shots)" for v, b in zip(x, BUD)])
    ax.set_xlabel("log₂(shots/class)", fontweight="bold")
    ax.set_ylabel("Macro F1", fontweight="bold")
    ax.set_ylim(0.40, 0.66)
    ax.grid(axis="y", color="#dfe5ec", lw=0.9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Frozen EXP-010 audit · mean ± population SD (10 episodes)",
                 loc="left", fontweight="bold", fontsize=14)
    fig.tight_layout()
    fig.savefig(RESULTS_PLOT, bbox_inches="tight", facecolor="white")
    plt.close(fig)


build_results_plot()

# palette
NAVY = RGBColor(0x0E, 0x1C, 0x2B)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
TEAL = RGBColor(0x11, 0x9D, 0x8F)
INK = RGBColor(0x14, 0x1C, 0x24)
MUTED = RGBColor(0x63, 0x6E, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
WASH = RGBColor(0xEE, 0xF3, 0xF9)
WASH_W = RGBColor(0xFD, 0xF1, 0xEA)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
N = 0


def slide(accent=BLUE, band=True):
    global N
    N += 1
    s = prs.slides.add_slide(BLANK)
    if band:
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.13))
        bar.fill.solid(); bar.fill.fore_color.rgb = accent; bar.line.fill.background()
        bar.shadow.inherit = False
    return s


def tb(s, x, y, w, h):
    t = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    t.text_frame.word_wrap = True
    return t.text_frame


def head(s, title, kicker=None, speaker=None, accent=BLUE):
    if kicker:
        f = tb(s, 0.62, 0.34, 11.5, 0.35)
        r = f.paragraphs[0].add_run(); r.text = kicker.upper()
        r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = accent
        r.font.name = "Consolas"
    f = tb(s, 0.6, 0.66, 12.2, 1.0)
    r = f.paragraphs[0].add_run(); r.text = title
    r.font.size = Pt(33); r.font.bold = True; r.font.color.rgb = INK
    if speaker:
        f = tb(s, 11.2, 6.92, 1.7, 0.35)
        p = f.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
        r = p.add_run(); r.text = speaker
        r.font.size = Pt(10); r.font.color.rgb = MUTED


def points(s, items, x=0.7, y=1.85, size=19, gap=0.52, color=INK, bullet=BLUE):
    for i, it in enumerate(items):
        if not it:
            continue
        yy = y + i * gap
        dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(yy + 0.13),
                                 Inches(0.11), Inches(0.11))
        dot.fill.solid(); dot.fill.fore_color.rgb = bullet; dot.line.fill.background()
        dot.shadow.inherit = False
        f = tb(s, x + 0.32, yy, 12.0 - x, 0.45)
        r = f.paragraphs[0].add_run(); r.text = it
        r.font.size = Pt(size); r.font.color.rgb = color


def panel(s, x, y, w, h, fill=WASH, line=None):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line:
        sh.line.color.rgb = line; sh.line.width = Pt(1.5)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    sh.adjustments[0] = 0.06
    return sh


def stat(s, x, y, value, label, color=BLUE, w=2.9, vsize=44):
    panel(s, x, y, w, 1.65, WASH if color == BLUE else WASH_W)
    f = tb(s, x + 0.15, y + 0.16, w - 0.3, 0.85)
    p = f.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = value
    r.font.size = Pt(vsize); r.font.bold = True; r.font.color.rgb = color
    f = tb(s, x + 0.15, y + 1.06, w - 0.3, 0.5)
    p = f.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(12); r.font.color.rgb = MUTED


def pic(s, name, x, y, h):
    s.shapes.add_picture(str(FIGS / name), Inches(x), Inches(y), height=Inches(h))


def table(s, rows, x, y, colw, size=15, header=True, hi_col=None, rowh=0.42):
    for i, row in enumerate(rows):
        if header and i == 0:
            bg = panel(s, x - 0.12, y + i * rowh - 0.05, sum(colw) + 0.24, rowh, NAVY)
        for j, cell in enumerate(row):
            cx = x + sum(colw[:j])
            f = tb(s, cx, y + i * rowh - 0.04, colw[j], rowh)
            p = f.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if j else PP_ALIGN.LEFT
            r = p.add_run(); r.text = str(cell)
            r.font.size = Pt(size)
            if header and i == 0:
                r.font.bold = True; r.font.color.rgb = WHITE
            else:
                r.font.color.rgb = BLUE if (hi_col is not None and j == hi_col) else INK
                r.font.bold = bool(hi_col is not None and j == hi_col)


# ═════════════════════════════════════════════════════ 1 · title + abstract
s = slide(band=False)
hero = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(2.5))
hero.fill.solid(); hero.fill.fore_color.rgb = NAVY; hero.line.fill.background()
hero.shadow.inherit = False
f = tb(s, 0.75, 0.5, 11.8, 0.5)
r = f.paragraphs[0].add_run(); r.text = "STATSGEEKS  ·  BUILDING-AGE TRANSFER LEARNING"
r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = RGBColor(0x8F, 0xB8, 0xE8)
r.font.name = "Consolas"
f = tb(s, 0.75, 1.0, 11.8, 1.2)
r = f.paragraphs[0].add_run(); r.text = "Transfer that actually transfers"
r.font.size = Pt(44); r.font.bold = True; r.font.color.rgb = WHITE
f = tb(s, 0.75, 2.75, 11.8, 3.1)
r = f.paragraphs[0].add_run()
r.text = (
    "Building age drives urban retrofit and energy policy, but records are incomplete. We "
    "classify the construction era of buildings within 30-metre Landsat pixels into four "
    "classes, training on Madrid and adapting to Amsterdam with as few as five labelled "
    "examples per class.\n\n"
    "The organiser baseline showed substantial source-target mismatch, motivating a "
    "representation-based transfer strategy. Madrid learns feature ranking and class geometry; "
    "Amsterdam support labels estimate target prototypes. At five shots we shrink noisy "
    "prototypes toward re-centred Madrid geometry. At larger budgets shrinkage switches off "
    "while dimensionality reduction remains useful. In frozen EXP-010 audit episodes, tuned "
    "macro F1 improves over the matched full-feature, target-only control at every budget, "
    "with 45 of 50 paired wins. The largest mean gain occurs at five shots per class—only "
    "20 labelled Amsterdam samples total—where prototype estimation is hardest."
)
r.font.size = Pt(16); r.font.color.rgb = MUTED
f = tb(s, 0.75, 6.85, 6, 0.4)
r = f.paragraphs[0].add_run(); r.text = "Abstract · ≤150 words"
r.font.size = Pt(10); r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 2 · the problem
s = slide()
head(s, "How old are these buildings?", "the problem")
points(s, ["Four construction eras, per 30 m Landsat pixel",
           "Train on Madrid  →  adapt to Amsterdam",
           "As few as five labelled examples per class",
           "Metric: four-class macro F1"], y=1.9, size=20, gap=0.58)
stat(s, 0.7, 4.5, "76k", "Madrid pixels")
stat(s, 3.8, 4.5, "26k", "Amsterdam pixels")
stat(s, 6.9, 4.5, "42", "years of imagery", TEAL)
stat(s, 10.0, 4.5, "5", "labels, worst case", ORANGE)

# ═════════════════════════════════════════════════════ 3 · the data
s = slide()
head(s, "Construction leaves a spectral fingerprint", "the data")
points(s, ["Six spectral bands · once a year · 1984–2025",
           "A field becomes a roof.  Concrete weathers.",
           "42-year trajectory  →  60 summary features",
           "Labels are area-weighted averages — noisy by construction"],
       y=1.95, size=19, gap=0.55)
panel(s, 0.7, 4.55, 11.9, 1.5, WASH_W)
f = tb(s, 1.0, 4.72, 11.3, 1.2)
r = f.paragraphs[0].add_run()
r.text = "One pixel can hold a 1950s block and a 2010s block — and gets a label describing neither."
r.font.size = Pt(19); r.font.bold = True; r.font.color.rgb = INK
f = tb(s, 1.0, 5.32, 11.3, 0.6)
r = f.paragraphs[0].add_run()
r.text = "There is a ceiling below 1.0. Nobody knows where it is."
r.font.size = Pt(16); r.font.color.rgb = ORANGE

# ═════════════════════════════════════════════════════ 4 · the defect
s = slide(ORANGE)
head(s, "Source-target mismatch motivates transfer",
     "baseline context", None, ORANGE)
panel(s, 0.7, 1.9, 5.7, 2.6, WASH_W)
f = tb(s, 1.0, 2.15, 5.1, 1.9)
for i, t in enumerate(["Organiser reference path",
                       "Madrid-fitted scaling",
                       "Amsterdam-only prototypes"]):
    p = f.paragraphs[0] if i == 0 else f.add_paragraph()
    r = p.add_run(); r.text = t
    r.font.size = Pt(18); r.font.color.rgb = INK
    r.font.bold = (i == 0)
points(s, ["The reference path establishes a matched target-only control",
           "It motivated reuse of supervised Madrid state",
           "Our comparison holds episodes and classifier form fixed"],
       x=6.9, y=2.0, size=17, gap=0.72, bullet=ORANGE)
panel(s, 0.7, 4.9, 11.9, 1.45, WASH)
f = tb(s, 1.0, 5.1, 11.3, 1.0)
r = f.paragraphs[0].add_run()
r.text = ("Provenance limitation: local RF outputs differ from organiser-saved outputs. "
          "Incomplete package/input provenance means the cause remains unidentified.")
r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = BLUE

# ═════════════════════════════════════════════════════ 5 · our method
s = slide()
head(s, "Freeze Madrid knowledge; adapt prototypes", "our method")
steps = [
    ("Madrid", "labelled data"),
    ("Frozen RF", "ranking + geometry"),
    ("Top-k", "feature selection"),
    ("Amsterdam", "support set"),
    ("Adapt", "prototypes"),
    ("Predict", "query labels"),
]
for i, (t, d) in enumerate(steps):
    x = 0.55 + i * 2.12
    panel(s, x, 2.0, 1.78, 1.55, WASH_W if i in (0, 1, 4) else WASH)
    f = tb(s, x + 0.10, 2.18, 1.58, 0.45)
    p = f.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t
    r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = BLUE
    f = tb(s, x + 0.10, 2.72, 1.58, 0.55)
    p = f.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = d
    r.font.size = Pt(11.5); r.font.color.rgb = MUTED
    if i < len(steps) - 1:
        f = tb(s, x + 1.80, 2.50, 0.32, 0.4)
        r = f.paragraphs[0].add_run(); r.text = "→"
        r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = ORANGE
panel(s, 0.7, 4.15, 5.75, 1.45, WASH_W, ORANGE)
f = tb(s, 1.0, 4.38, 5.15, 0.9)
r = f.paragraphs[0].add_run(); r.text = "5 shots/class  →  k=30, λ=0.6\nShrink toward Madrid geometry"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ORANGE
panel(s, 6.85, 4.15, 5.75, 1.45, WASH, BLUE)
f = tb(s, 7.15, 4.38, 5.15, 0.9)
r = f.paragraphs[0].add_run(); r.text = "25–200 shots/class  →  k=45, λ=0.0\nShrinkage switches off"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = BLUE
f = tb(s, 0.8, 6.05, 11.7, 0.5)
p = f.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Query labels are evaluation-only."
r.font.size = Pt(15); r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 6 · results
s = slide(TEAL)
head(s, "Five shots is the practical anchor", "frozen EXP-010 audit", None, TEAL)
rows = [["shots/class", "EXP-010", "control", "gain", "wins"]]
for b in BUD:
    r = row(b)
    rows.append([str(b), f"{r['tuned']:.3f} ± {TUNED_SD[b]:.3f}",
                 f"{r['control']:.3f} ± {CONTROL_SD[b]:.3f}",
                 f"{r['gain']:+.3f}", f"{r['wins']}/10"])
table(s, rows, 0.70, 1.85, [1.30, 2.20, 2.20, 1.15, 1.05], size=15, hi_col=1, rowh=0.48)
stat(s, 9.05, 1.85, "+0.0372", "5-shot macro F1 gain", TEAL, 3.55, 32)
stat(s, 9.05, 3.65, "45 / 50", "paired audit wins", BLUE, 3.55, 38)
f = tb(s, 0.8, 4.85, 7.8, 0.38)
r = f.paragraphs[0].add_run(); r.text = "± population SD across 10 audit episodes — not confidence intervals"
r.font.size = Pt(11.5); r.font.color.rgb = MUTED
panel(s, 0.70, 5.35, 5.75, 1.10, WASH_W, ORANGE)
f = tb(s, 0.95, 5.55, 5.25, 0.7)
r = f.paragraphs[0].add_run(); r.text = "SCIENTIFIC HEADLINE  ·  5/class = 20 labels total\n0.552 ± 0.060 vs 0.515 ± 0.070 · 7/10 wins"
r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = ORANGE
panel(s, 6.85, 5.35, 5.75, 1.10, WASH, BLUE)
f = tb(s, 7.10, 5.55, 5.25, 0.7)
r = f.paragraphs[0].add_run(); r.text = "OFFICIAL 25-SHOT RESULT\n+0.0033 macro F1 · 8/10 paired wins"
r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = BLUE

# ═════════════════════════════════════════════════════ 7 · required learning curve
s = slide(TEAL)
head(s, "Transfer helps most in the lowest-data regime", "required learning curve", None, TEAL)
s.shapes.add_picture(str(RESULTS_PLOT), Inches(0.45), Inches(1.55), width=Inches(8.65))
panel(s, 9.35, 1.75, 3.45, 1.35, WASH_W, ORANGE)
f = tb(s, 9.60, 1.98, 2.95, 0.9)
r = f.paragraphs[0].add_run(); r.text = "5 shots/class\nHigh episode spread"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ORANGE
panel(s, 9.35, 3.30, 3.45, 1.35, WASH, BLUE)
f = tb(s, 9.60, 3.53, 2.95, 0.9)
r = f.paragraphs[0].add_run(); r.text = "25+ shots/class\nPrototypes stabilise"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = BLUE
f = tb(s, 9.42, 5.05, 3.25, 1.25)
r = f.paragraphs[0].add_run()
r.text = "Empirical takeaway:\nTransfer helps most when target prototypes are hardest to estimate."
r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = INK
f = tb(s, 9.42, 6.32, 3.25, 0.58)
r = f.paragraphs[0].add_run()
r.text = "Source-domain CV (documented local protocol):\nMadrid 0.6281 ± 0.0043 macro F1"
r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 8 · the finding
s = slide(ORANGE)
head(s, "More labels reduce prototype estimation error",
     "empirical interpretation", None, ORANGE)
rows = [["shots", "features (k)", "shrinkage (λ)"],
        ["5", "30", "0.6"], ["25", "45", "0.0"], ["50", "45", "0.0"],
        ["100", "45", "0.0"], ["200", "45", "0.0"]]
table(s, rows, 0.85, 2.1, [1.35, 1.9, 2.0], size=16, rowh=0.62)
points(s, ["λ — how much we trust Madrid over Amsterdam",
           "k — how many features we keep",
           "",
           "Less data → lean on Madrid, use fewer features",
           "More data → trust Amsterdam, afford more features",
           "",
           "In these experiments, the selected schedule",
           "switches shrinkage off once labels increase."],
       x=6.5, y=2.0, size=17, gap=0.5, bullet=ORANGE)

# ═════════════════════════════════════════════════════ 9 · what failed
s = slide()
head(s, "Negative results clarify the mechanism", "what we learned")
panel(s, 0.75, 1.85, 5.85, 3.35, WASH_W, ORANGE)
f = tb(s, 1.05, 2.15, 5.25, 0.55)
r = f.paragraphs[0].add_run(); r.text = "EXP-004 · WHITENING REVERSAL"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ORANGE
f = tb(s, 1.05, 2.85, 5.25, 1.75)
r = f.paragraphs[0].add_run()
r.text = ("Within-class whitening changed from harmful at low shot count to beneficial "
          "at high shot count. The same transform gave opposite outcomes as support grew.")
r.font.size = Pt(18); r.font.color.rgb = INK
panel(s, 6.75, 1.85, 5.85, 3.35, WASH, BLUE)
f = tb(s, 7.05, 2.15, 5.25, 0.55)
r = f.paragraphs[0].add_run(); r.text = "EXP-007 · MORE FEATURES DID NOT HELP"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = BLUE
f = tb(s, 7.05, 2.85, 5.25, 1.75)
r = f.paragraphs[0].add_run()
r.text = ("The expanded 94-feature seasonal/coverage representation did not outperform "
          "the original 60 features. Extra dimensions can dilute few-shot prototype estimates.")
r.font.size = Pt(18); r.font.color.rgb = INK
panel(s, 0.75, 5.55, 11.85, 0.90, WASH)
f = tb(s, 1.05, 5.73, 11.25, 0.55)
p = f.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Together, these outcomes support—without proving—the prototype estimation-error interpretation."
r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = INK

# ═════════════════════════════════════════════════════ 10 · honesty
s = slide(NAVY)
head(s, "What we are not claiming", "honesty", None, NAVY)
points(s, ["Gains beyond five shots are small in absolute macro F1",
           "Error bars are spreads, not confidence intervals",
           "Confusion diagonals are recall, not F1",
           "Accuracy would have flattered us — we report macro F1",
           "We do not claim exact reproduction of organiser RF outputs"],
       y=1.95, size=18, gap=0.56)
panel(s, 0.7, 4.85, 11.9, 1.9, WASH_W)
f = tb(s, 1.0, 5.0, 11.3, 0.6)
r = f.paragraphs[0].add_run(); r.text = "Why not?"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ORANGE
f = tb(s, 1.0, 5.5, 11.3, 1.2)
r = f.paragraphs[0].add_run()
r.text = ("Source-domain Madrid CV is 0.6281 ± 0.0043 under the documented local protocol; "
          "local zero-shot is 0.4433, versus organiser-saved 0.6179 and 0.3427. "
          "Package/input provenance is incomplete, so "
          "the cause remains unidentified and exact reproduction is not claimed.")
r.font.size = Pt(15); r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 11 · limitations
s = slide()
head(s, "Limitations", "stated, not hidden")
for i, t in enumerate([
        "Features still built label-dependently — no hidden-test path yet",
        "Scaling fitted before cross-validation — not fold-safe",
        "λ schedule: five values from five selection trials — overfit risk",
        "Optimal k moves once (30→45) — weak evidence for a trend",
        "EXP-010 has not been independently replicated"]):
    y = 1.95 + i * 0.82
    panel(s, 0.7, y, 11.9, 0.68, WASH)
    f = tb(s, 1.0, y + 0.11, 11.3, 0.5)
    r = f.paragraphs[0].add_run(); r.text = f"{i+1}.   {t}"
    r.font.size = Pt(17); r.font.color.rgb = INK
f = tb(s, 0.7, 6.25, 11.9, 0.6)
r = f.paragraphs[0].add_run()
r.text = "No claims of worldwide portability. No claims of calibrated confidence."
r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 12 · controls + contributions
s = slide()
head(s, "Reproducible by design, limited by evidence", "controls and provenance")
panel(s, 0.7, 1.9, 5.8, 4.7, WASH)
f = tb(s, 1.0, 2.1, 5.2, 0.5)
r = f.paragraphs[0].add_run(); r.text = "EVALUATION CONTROLS"
r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = BLUE
points(s, ["Exact episode manifests + RNG binding",
           "Support/query isolation",
           "Frozen EXP-010 state",
           "Matched episodes for tuned and control",
           "Population SD over 10 audit episodes"],
       x=1.0, y=2.75, size=14, gap=0.55)
panel(s, 6.8, 1.9, 5.8, 4.7, WASH_W)
f = tb(s, 7.1, 2.1, 5.2, 0.5)
r = f.paragraphs[0].add_run(); r.text = "EVIDENCE BOUNDARY"
r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = ORANGE
points(s, ["Madrid → Amsterdam only",
           "No hidden-test claim",
           "No independent EXP-010 replication",
           "Local baseline provenance is incomplete",
           "Controls support validity, not superiority"],
       x=7.1, y=2.75, size=14, gap=0.55, bullet=ORANGE)

# ═════════════════════════════════════════════════════ 13 · conclusion
s = slide(band=False)
hero = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
hero.fill.solid(); hero.fill.fore_color.rgb = NAVY; hero.line.fill.background()
hero.shadow.inherit = False
f = tb(s, 1.0, 1.3, 11.3, 0.5)
r = f.paragraphs[0].add_run(); r.text = "CONCLUSION"
r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = RGBColor(0x8F, 0xB8, 0xE8)
r.font.name = "Consolas"
for i, t in enumerate(["Madrid learns feature ranking and class geometry.",
                       "Amsterdam support labels estimate target prototypes.",
                       "EXP-010: positive mean gains, 45/50 paired wins."]):
    f = tb(s, 1.0, 2.0 + i * 0.75, 11.3, 0.7)
    r = f.paragraphs[0].add_run(); r.text = t
    r.font.size = Pt(26); r.font.bold = True; r.font.color.rgb = WHITE
f = tb(s, 1.0, 4.8, 11.3, 1.0)
r = f.paragraphs[0].add_run(); r.text = "A number without a mechanism is not a finding."
r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = RGBColor(0x6F, 0xA8, 0xE8)

# ═════════════════════════════════════════════════════ backups
def backup(title, items, fig=None):
    s = slide(MUTED)
    head(s, title, "backup", None, MUTED)
    if fig:
        pic(s, fig, 0.7, 1.9, 4.4)
        points(s, items, x=6.4, y=2.05, size=15, gap=0.46, bullet=MUTED)
    else:
        points(s, items, y=1.95, size=17, gap=0.52, bullet=MUTED)


backup("Reproducibility", [
    "requirements.txt pins the exact stack",
    "Raw data + feature cache SHA256 recorded",
    "Episode indices stored, not regenerated from a seed",
    "EXP-010 package stores weights, k=30/45 offsets and schedule",
    "Frozen artifacts include recorded SHA256 checksums",
    "Cold-start reproduction: ~35 minutes"])

backup("Why our baseline differs from the organiser's", [
    "All six prototype budgets match them to 4 decimal places",
    "Both Random-Forest results differ: +0.0102 and +0.1006",
    "The prototype path does not consume fitted forest predictions",
    "Determinism check: 0 of 25,992 predictions differed across two refits",
    "Exact cause remains unidentified; no causal explanation is claimed"])

backup("A 70-day seasonal offset between the cities", [
    "Madrid median day 175 · Amsterdam day 105",
    "June–August: 48.3% vs 20.5%",
    "Part of the domain shift is phenology, not architecture",
    "We rebuilt features to control for it",
    "It did not help — dilution outweighed the correction",
    "Reported as a measured finding with a negative test"],
    fig="fig7_season_offset.png")

backup("The episode protocol", [
    "One permutation per class per trial; budgets read prefixes",
    "So budgets are nested: support(5) ⊂ support(25) ⊂ …",
    "Support and query disjoint, verified in code every episode",
    "Selection and audit sets never overlap",
    "Four independent seeds used across the project",
    "Query set shrinks unevenly as budget grows — a stated limitation"])

prs.save(OUT)
print(f"Saved {OUT}  ({OUT.stat().st_size/1024:.0f} KB, {N} slides)")
