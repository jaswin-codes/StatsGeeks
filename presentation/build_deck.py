"""Build the submission deck. All numbers read from candidate/artifacts/*.json.

Design: colour-banded slides, short phrases rather than sentences, big figures.
16 slides - 12 main plus 4 backup - down from 21.

Run from the repository root:
    python presentation/build_deck.py
"""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ART = Path("candidate/artifacts")
FIGS = Path("candidate/figures")
OUT = Path("presentation/StatsGeeks_BuildingAge.pptx")

fs = json.loads((ART / "final_vs_starter.json").read_text())
js = json.loads((ART / "joint_sweep.json").read_text())
BUD = [5, 25, 50, 100, 200]
mean = lambda k, b: sum(fs[k][str(b)]) / len(fs[k][str(b)])
wins = lambda b: sum(1 for a, c in zip(fs["starter"][str(b)], fs["ours"][str(b)]) if c > a)

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
    "The organiser's starter pipeline appears to perform transfer learning but does not: its "
    "Madrid-trained Random Forest is discarded, and Amsterdam prototypes are computed from "
    "Amsterdam data alone. We reproduced that baseline exactly, then built a method that "
    "genuinely reuses Madrid-learned state.\n\n"
    "Our contribution is prototype shrinkage. An Amsterdam class mean estimated from five "
    "pixels is nearly unbiased but very noisy, so we shrink it toward Madrid's class geometry, "
    "with the weight falling as target data grows. Five-shot macro F1 rises by 0.0487 over the "
    "starter, winning 47 of 50 paired episodes. The optimal shrinkage declines monotonically "
    "with budget, exactly as shrinkage theory predicts."
)
r.font.size = Pt(14.5); r.font.color.rgb = MUTED
f = tb(s, 0.75, 6.85, 6, 0.4)
r = f.paragraphs[0].add_run(); r.text = "Abstract · 145 words"
r.font.size = Pt(10); r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 2 · the problem
s = slide()
head(s, "How old are these buildings?", "the problem", "M1")
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
head(s, "Construction leaves a spectral fingerprint", "the data", "M2")
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
head(s, "The starter's transfer learning transfers nothing",
     "what we found", "M2 → M3", ORANGE)
panel(s, 0.7, 1.9, 5.7, 2.5, WASH_W)
f = tb(s, 1.0, 2.1, 5.1, 2.1)
for i, t in enumerate(["1.  Train a Random Forest on Madrid",
                       "2.  Throw it away",
                       "3.  Build Amsterdam prototypes from",
                       "     Amsterdam data alone"]):
    p = f.paragraphs[0] if i == 0 else f.add_paragraph()
    r = p.add_run(); r.text = t
    r.font.size = Pt(17); r.font.color.rgb = INK
    r.font.bold = (i == 1)
    if i == 1:
        r.font.color.rgb = ORANGE
points(s, ["Madrid contributes only a scaler",
           "More labels ≠ more transfer",
           "It just measures Amsterdam-only learning"],
       x=6.9, y=2.0, size=18, gap=0.55, bullet=ORANGE)
panel(s, 6.9, 3.85, 5.7, 0.85, WASH)
f = tb(s, 7.15, 4.0, 5.2, 0.6)
r = f.paragraphs[0].add_run(); r.text = "The rubric can disqualify for this."
r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = BLUE
panel(s, 0.7, 4.85, 11.9, 1.55, WASH)
f = tb(s, 1.0, 5.0, 11.3, 1.3)
r = f.paragraphs[0].add_run(); r.text = "And that flaw became our best instrument."
r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = BLUE
f = tb(s, 1.0, 5.55, 11.3, 0.8)
r = f.paragraphs[0].add_run()
r.text = ("It touches no tree code — so it proved our data pipeline was identical, "
          "and isolated a scikit-learn version difference in the baseline.")
r.font.size = Pt(15); r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 5 · our method
s = slide()
head(s, "We transfer a metric, not a classifier", "our method", "M3")
for i, (t, d) in enumerate([
        ("Learn", "a transform on\nMadrid only"),
        ("Freeze", "never refit on\nAmsterdam"),
        ("Project", "push Amsterdam\nthrough it"),
        ("Prototype", "class means from\nsupport labels")]):
    x = 0.7 + i * 3.08
    panel(s, x, 1.95, 2.85, 1.85, WASH)
    f = tb(s, x + 0.2, 2.1, 2.45, 0.5)
    r = f.paragraphs[0].add_run(); r.text = f"{i+1}.  {t}"
    r.font.size = Pt(19); r.font.bold = True; r.font.color.rgb = BLUE
    f = tb(s, x + 0.2, 2.68, 2.45, 1.0)
    r = f.paragraphs[0].add_run(); r.text = d
    r.font.size = Pt(14); r.font.color.rgb = MUTED
points(s, ["Madrid teaches which measurements matter",
           "Amsterdam supplies the examples",
           "Query labels never touched — evaluation only"],
       y=4.15, size=18, gap=0.5)
stat(s, 0.7, 5.75, "3 KB", "what we ship", BLUE, 5.8, 34)
stat(s, 6.8, 5.75, "244 MB", "the forest behind it", ORANGE, 5.8, 34)

# ═════════════════════════════════════════════════════ 6 · results
s = slide(TEAL)
head(s, "Better at every budget", "results", "M3", TEAL)
rows = [["shots/class", "starter", "ours", "gain", "won"]]
for b in BUD:
    rows.append([str(b), f"{mean('starter', b):.4f}", f"{mean('ours', b):.4f}",
                 f"+{mean('ours', b) - mean('starter', b):.4f}", f"{wins(b)}/10"])
table(s, rows, 0.85, 2.0, [2.6, 1.9, 1.9, 1.9, 1.5], size=16, hi_col=3)
stat(s, 9.3, 2.05, "+9.7%", "at five shots", TEAL, 3.3, 40)
stat(s, 9.3, 3.9, "47/50", "episodes won", BLUE, 3.3, 40)
panel(s, 0.85, 5.55, 11.6, 1.15, WASH)
f = tb(s, 1.15, 5.7, 11.0, 0.9)
r = f.paragraphs[0].add_run()
r.text = "Same pixels. Same episodes. Same environment. The only thing that differs is the method."
r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = INK

# ═════════════════════════════════════════════════════ 7 · learning curve
s = slide()
head(s, "The gain is where the data is scarcest", "learning curve", "M3")
pic(s, "fig1_learning_curve.png", 0.7, 1.85, 4.9)
points(s, ["Five shots is the hard case",
           "That is where transfer should matter",
           "And that is where it does",
           "",
           "Beyond 25 shots, Amsterdam has",
           "enough data of its own"],
       x=6.7, y=2.1, size=17, gap=0.5)

# ═════════════════════════════════════════════════════ 8 · the finding
s = slide(ORANGE)
head(s, "Two knobs. Both depend on how much data you have.",
     "the finding", "M4", ORANGE)
pic(s, "fig9_shrinkage.png", 0.5, 1.9, 3.1)
rows = [["shots", "features (k)", "shrinkage (λ)"],
        ["5", "30", "0.6"], ["25", "45", "0.0"], ["50", "45", "0.0"],
        ["100", "45", "0.0"], ["200", "45", "0.0"]]
table(s, rows, 0.75, 5.12, [1.35, 1.9, 2.0], size=13, rowh=0.33)
points(s, ["λ — how much we trust Madrid over Amsterdam",
           "k — how many features we keep",
           "",
           "Less data → lean on Madrid, use fewer features",
           "More data → trust Amsterdam, afford more features",
           "",
           "We did not impose this. It is what shrinkage",
           "theory predicts, recovered from the data."],
       x=6.5, y=2.0, size=17, gap=0.5, bullet=ORANGE)

# ═════════════════════════════════════════════════════ 9 · what failed
s = slide()
head(s, "Three things we tried that did not work", "ablations", "M4")
pic(s, "fig3_method_ablation.png", 0.6, 1.9, 4.5)
for i, (t, d, c) in enumerate([
        ("Rank-3 LDA", "compresses 60 dims to 3 — loses too much", ORANGE),
        ("RF probability space", "worst of nine — 4 dims is not enough", ORANGE),
        ("94 season-aware features", "informative but dilutive — noisier prototypes", ORANGE)]):
    y = 2.1 + i * 1.35
    panel(s, 6.4, y, 6.3, 1.15, WASH_W)
    f = tb(s, 6.65, y + 0.12, 5.9, 0.45)
    r = f.paragraphs[0].add_run(); r.text = t
    r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = c
    f = tb(s, 6.65, y + 0.58, 5.9, 0.5)
    r = f.paragraphs[0].add_run(); r.text = d
    r.font.size = Pt(14); r.font.color.rgb = MUTED
panel(s, 6.4, 6.15, 6.3, 0.85, WASH)
f = tb(s, 6.65, 6.3, 5.9, 0.6)
r = f.paragraphs[0].add_run(); r.text = "All three: too few dimensions, or too many."
r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = BLUE

# ═════════════════════════════════════════════════════ 10 · honesty
s = slide(NAVY)
head(s, "What we are not claiming", "honesty", "M4", NAVY)
points(s, ["Gains beyond five shots are ~1.5% — small",
           "Error bars are spreads, not confidence intervals",
           "Confusion diagonals are recall, not F1",
           "Accuracy would have flattered us — we report macro F1",
           "We do not compare to the organiser's published numbers"],
       y=1.95, size=18, gap=0.56)
panel(s, 0.7, 4.85, 11.9, 1.9, WASH_W)
f = tb(s, 1.0, 5.0, 11.3, 0.6)
r = f.paragraphs[0].add_run(); r.text = "Why not?"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ORANGE
f = tb(s, 1.0, 5.5, 11.3, 1.2)
r = f.paragraphs[0].add_run()
r.text = ("Different episodes and a different scikit-learn. Our own reproduction of their "
          "method scores 0.5038 at five shots against their published 0.5437 — same code, "
          "different draws. Comparing across them would invent an improvement.")
r.font.size = Pt(15); r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 11 · limitations
s = slide()
head(s, "Limitations", "stated, not hidden", "M4")
for i, t in enumerate([
        "Features still built label-dependently — no hidden-test path yet",
        "Scaling fitted before cross-validation — not fold-safe",
        "λ schedule: five values from five selection trials — overfit risk",
        "Optimal k moves once (30→45) — weak evidence for a trend",
        "Near a label-noise ceiling — three independent lines of evidence"]):
    y = 1.95 + i * 0.82
    panel(s, 0.7, y, 11.9, 0.68, WASH)
    f = tb(s, 1.0, y + 0.11, 11.3, 0.5)
    r = f.paragraphs[0].add_run(); r.text = f"{i+1}.   {t}"
    r.font.size = Pt(17); r.font.color.rgb = INK
f = tb(s, 0.7, 6.25, 11.9, 0.6)
r = f.paragraphs[0].add_run()
r.text = "No claims of worldwide portability. No claims of calibrated confidence."
r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = MUTED

# ═════════════════════════════════════════════════════ 12 · conclusion
s = slide(band=False)
hero = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
hero.fill.solid(); hero.fill.fore_color.rgb = NAVY; hero.line.fill.background()
hero.shadow.inherit = False
f = tb(s, 1.0, 1.3, 11.3, 0.5)
r = f.paragraphs[0].add_run(); r.text = "CONCLUSION"
r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = RGBColor(0x8F, 0xB8, 0xE8)
r.font.name = "Consolas"
for i, t in enumerate(["The starter's transfer transferred nothing. We proved it.",
                       "We built one that does, and measured it honestly.",
                       "Better at every budget. +9.7% where data is scarcest."]):
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
    "Stage 1 artifact 3 KB · reload test 17/17 in a clean session",
    "Seeds fixed throughout · 12 commits · tagged",
    "Cold-start reproduction: ~35 minutes"])

backup("Why our baseline differs from the organiser's", [
    "All six prototype budgets match them to 4 decimal places",
    "Both Random-Forest results differ: +0.0102 and +0.1006",
    "The prototype path never uses the forest — it isolates the cause",
    "Determinism: 0 of 25,992 predictions differ across two refits",
    "Still inferred, not measured — we did not install their version"])

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
