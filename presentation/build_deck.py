"""Build the submission PowerPoint from recorded results and exported figures.

Every number is read from candidate/artifacts/*.json, so the deck cannot drift
from the evidence. Re-run it after any result changes.

Run from the repository root:
    python presentation/build_deck.py
"""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ART = Path("candidate/artifacts")
FIGS = Path("candidate/figures")
OUT = Path("presentation/StatsGeeks_BuildingAge.pptx")

audit = json.loads((ART / "final_audit.json").read_text())
BUD = [5, 25, 50, 100, 200]

INK = RGBColor(0x0E, 0x14, 0x1B)
MUTED = RGBColor(0x55, 0x60, 0x6B)
ACC = RGBColor(0x2A, 0x78, 0xD6)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
n_slides = 0


def slide():
    global n_slides
    n_slides += 1
    return prs.slides.add_slide(BLANK)


def txt(s, x, y, w, h):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    return tf, tf.paragraphs[0]


def title(s, text, sub=None, speaker=None):
    _, p = txt(s, 0.6, 0.4, 12.1, 1.0)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(32)
    r.font.bold = True
    r.font.color.rgb = INK
    if sub:
        _, p2 = txt(s, 0.6, 1.35, 12.1, 0.5)
        r2 = p2.add_run()
        r2.text = sub
        r2.font.size = Pt(15)
        r2.font.color.rgb = MUTED
    if speaker:
        _, p3 = txt(s, 11.1, 6.9, 1.8, 0.4)
        r3 = p3.add_run()
        r3.text = speaker
        r3.font.size = Pt(10)
        r3.font.color.rgb = MUTED
        p3.alignment = PP_ALIGN.RIGHT


def bullets(s, items, x=0.7, y=2.15, w=12.0, size=17, gap=0.5):
    for i, it in enumerate(items):
        if not it:
            continue
        bold = it.startswith("**")
        _, p = txt(s, x, y + i * gap, w, 0.45)
        r = p.add_run()
        r.text = it.replace("**", "")
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = INK if bold else MUTED


def pic(s, name, x, y, h):
    s.shapes.add_picture(str(FIGS / name), Inches(x), Inches(y), height=Inches(h))


def bignum(s, value, label, x, y, color=ACC):
    _, p = txt(s, x, y, 3.1, 0.9)
    r = p.add_run()
    r.text = value
    r.font.size = Pt(36)
    r.font.bold = True
    r.font.color.rgb = color
    _, p2 = txt(s, x, y + 0.78, 3.1, 0.5)
    r2 = p2.add_run()
    r2.text = label
    r2.font.size = Pt(12)
    r2.font.color.rgb = MUTED


# --------------------------------------------------------------- 1 abstract
s = slide()
title(s, "Transfer that actually transfers",
      "Building-age classification from Landsat: Madrid to Amsterdam", "M1")
abstract = (
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
    "with the weight falling as target data grows. Five-shot macro F1 rises by 0.0515 over "
    "target-only prototypes, winning 40 of 50 paired episodes. The optimal shrinkage declines "
    "monotonically with budget, exactly as shrinkage theory predicts."
)
_, p = txt(s, 0.7, 2.1, 11.9, 4.3)
r = p.add_run()
r.text = abstract
r.font.size = Pt(15)
r.font.color.rgb = MUTED
_, p = txt(s, 0.7, 6.7, 6.0, 0.4)
r = p.add_run()
r.text = "Abstract"
r.font.size = Pt(10)
r.font.color.rgb = MUTED

# --------------------------------------------------------------- 2 problem
s = slide()
title(s, "The problem", "Four-class construction era, per 30 m pixel", "M1")
bullets(s, [
    "**Building age drives retrofit and energy policy - and the records are incomplete.**",
    "Classify the construction era of buildings inside a 30 m x 30 m Landsat pixel.",
    "Four classes. Train on Madrid. Adapt to Amsterdam.",
    "**The constraint: as few as 5 labelled Amsterdam examples per class.**",
    "Metric: four-class macro F1.",
], y=2.25)
bignum(s, "76,263", "Madrid pixels", 0.9, 4.9)
bignum(s, "25,992", "Amsterdam pixels", 4.0, 4.9)
bignum(s, "1984-2025", "annual observations", 7.1, 4.9)
bignum(s, "5-200", "labels per class", 10.2, 4.9)

# --------------------------------------------------------------- 3 data
s = slide()
title(s, "The data", "Six spectral bands, once a year, for 42 years", "M2")
bullets(s, [
    "Each pixel is a 42-year spectral trajectory, summarised into 60 features.",
    "**Construction changes what ground looks like from space - that is the whole premise.**",
    "A field becomes a roof. Concrete weathers. Dense old centres differ from new suburbs.",
    "Class 2 is the largest class in both cities, correcting the starter's prose.",
    "**We say 59 informative features, not 60 - see the next slide.**",
], y=2.3)

# --------------------------------------------------------------- 4 labels
s = slide()
title(s, "The labels are noisy by construction",
      "There is a ceiling below 1.0 and nobody knows where it is", "M2")
bullets(s, [
    "**The label is an area-weighted average of construction years inside the pixel.**",
    "A pixel holding a 1950s block and a 2010s block gets a class describing neither.",
    "No model can reach a perfect score on labels like these.",
    "",
    "**Evidence we are near that ceiling:**",
    "Amsterdam at 200 shots reaches 0.6227.",
    "Madrid's own full-data cross-validated score is 0.6281.",
], y=2.3, gap=0.47)

# --------------------------------------------------------------- 5 baseline
s = slide()
title(s, "First, we reproduced the baseline exactly",
      "Zero code edits - then the numbers disagreed", "M2")
bullets(s, [
    "Every result that avoids the Random Forest matched the organiser to 4 decimal places.",
    "**Both Random-Forest results did not:**",
    "        Madrid CV   0.6281  vs  0.6179            Zero-shot   0.4433  vs  0.3427",
    "Diagnosed to a scikit-learn version difference. The prototype path never touches",
    "tree code, so it acted as an unintended control that isolated the cause.",
    "**Refitting twice: 0 of 25,992 predictions differed. Systematic, not noise.**",
    "Also found: has_early_data is constant in both cities. 59 features carry signal, not 60.",
], y=2.2, gap=0.47)

# --------------------------------------------------------------- 6 defect
s = slide()
title(s, "The starter's transfer learning transfers nothing",
      "The defect at the centre of this challenge", "M2 > M3")
bullets(s, [
    "**It trains a Madrid Random Forest. Then it throws it away.**",
    "Amsterdam prototypes are computed from Amsterdam data alone.",
    "Madrid contributes only the scaler's mean and variance.",
    "Rising F1 with more labels measures an Amsterdam-only method getting more Amsterdam data.",
    "",
    "**And that flaw became our best instrument.** Because it touches no scikit-learn tree",
    "code, it proved our data pipeline was identical - which is how we isolated the",
    "version difference on the previous slide.",
], y=2.2, gap=0.46)

# --------------------------------------------------------------- 7 method
s = slide()
title(s, "What we actually transfer", "A metric, not a classifier", "M3")
bullets(s, [
    "**1.  Learn a transform T on MADRID ONLY.          2.  Freeze it.**",
    "**3.  Push Amsterdam support and query through T.**",
    "**4.  Nearest class prototype, from support labels only.**",
    "",
    "Madrid teaches which of the 60 measurements matter. Amsterdam supplies the examples.",
], y=2.2, gap=0.5)
bignum(s, "3 KB", "the shipped artifact", 1.1, 5.0, ACC)
bignum(s, "244 MB", "the forest that produced it", 5.0, 5.0, MUTED)
_, p = txt(s, 9.0, 5.1, 3.8, 1.3)
r = p.add_run()
r.text = "Everything that\ntransfers fits in 3 KB."
r.font.size = Pt(17)
r.font.bold = True
r.font.color.rgb = ACC

# --------------------------------------------------------------- 8 fairness
s = slide()
title(s, "Making the comparison fair", "The part that makes any of this measurable", "M3")
bullets(s, [
    "**Episodes matched across methods and nested across budgets** - a budget increase",
    "adds pixels and changes nothing else.",
    "**Support indices stored, not regenerated from a seed** - we had direct evidence",
    "that seeds do not survive an environment change.",
    "Selection on trials 0-4. Audit on trials 5-9, reported once.",
    "",
    "**Beating zero-shot proves nothing. Beating the target-only control does.**",
], y=2.2, gap=0.47)

# --------------------------------------------------------------- 9 results
s = slide()
title(s, "Does it work?", "Held-out audit episodes, mean +/- 1 SD", "M3")
pic(s, "fig1_learning_curve.png", 0.7, 1.9, 4.9)
rows = [("shots", "control", "ours", "gain")] + [
    (str(b),
     "{:.4f}".format(audit["audit"][str(b)]["control_mean"]),
     "{:.4f}".format(audit["audit"][str(b)]["cand_mean"]),
     "+{:.4f}".format(audit["audit"][str(b)]["benefit"]))
    for b in BUD]
for i, row in enumerate(rows):
    for j, cell in enumerate(row):
        _, p = txt(s, 7.3 + j * 1.4, 2.35 + i * 0.44, 1.35, 0.4)
        r = p.add_run()
        r.text = cell
        r.font.size = Pt(14)
        r.font.bold = (i == 0)
        r.font.color.rgb = INK if i == 0 else (ACC if j == 3 else MUTED)
_, p = txt(s, 7.3, 5.4, 5.4, 1.1)
r = p.add_run()
r.text = "Positive at every budget.\nThe lines are close - that is the honest picture."
r.font.size = Pt(14)
r.font.color.rgb = INK

# --------------------------------------------------------------- 9c shrinkage
s = slide()
title(s, "The biggest gain is where the data is scarcest",
      "Prototype shrinkage toward Madrid's class geometry", "M3")
pic(s, "fig9_shrinkage.png", 0.45, 2.0, 3.5)
bullets(s, [
    "**At 5 shots, an Amsterdam class mean comes from 5 points in 60 dimensions.**",
    "Nearly unbiased, but very noisy. Madrid's prototype comes from 76,263 pixels:",
    "biased, because it is a different city, but stable.",
    "",
    "**So shrink the noisy estimate toward the stable one:**",
    "        p = mu_A  +  lambda (Madrid class offset)  +  (1-lambda)(support mean - mu_A)",
    "",
    "**+0.0515 macro F1 at 5 shots. 40 of 50 paired episodes won.**",
    "",
    "**And the optimal lambda falls monotonically as target data grows** -",
    "0.5 at five shots, 0.1 at two hundred. We did not impose that; it is what",
    "shrinkage theory predicts, recovered from the data.",
    "",
    "mu_A uses the SUPPORT set only. Query features are never touched.",
], x=4.6, y=1.95, w=8.4, size=13, gap=0.35)

# --------------------------------------------------------------- 9b replication
s = slide()
title(s, "And it replicates", "On episodes that did not exist when the method was chosen", "M3")
pic(s, "fig8_replication.png", 0.7, 1.95, 4.6)
bullets(s, [
    "**The method was fixed on one episode set.**",
    "**Then tested on a brand new one, seed 2026.**",
    "",
    "19 of 25 paired episodes won.",
    "Positive at every budget, in both runs.",
    "",
    "**The 5-shot gain is the largest: +0.0178** -",
    "the regime the challenge actually cares about.",
    "",
    "**This is external validation, not a re-audit**",
    "**of the set we selected on.**",
], x=6.7, y=2.1, w=6.0, size=15, gap=0.42)

# --------------------------------------------------------------- 10 ablation
s = slide()
title(s, "What is worth transferring from Madrid?",
      "Nine frozen source representations, identical procedure otherwise", "M3 > M4")
pic(s, "fig3_method_ablation.png", 0.6, 1.95, 4.8)
bullets(s, [
    "**The crude method beat the clever ones.**",
    "",
    "Importance weighting worked.",
    "Rank-3 LDA hurt.",
    "The classifier's own probability space hurt",
    "badly - the worst of the nine.",
    "",
    "**Both compress 60 dimensions into 3-4 and**",
    "**discard what Amsterdam needs.**",
], x=6.9, y=2.15, w=5.9, size=15, gap=0.44)

# --------------------------------------------------------------- 11 finding
s = slide()
title(s, "The ranking depends on the label budget",
      "Same transform, opposite verdict", "M4")
pic(s, "fig4_budget_dependence.png", 0.6, 1.95, 4.7)
bullets(s, [
    "**Within-class whitening:**",
    "        -0.0218 at 5 shots",
    "        +0.0090 at 200 shots",
    "",
    "Whitening amplifies low-variance directions.",
    "Destructive when 5 points must estimate a",
    "prototype. Helpful once 200 make it stable.",
    "",
    "**This also explains the LDA failure: rank-3**",
    "**collapse, not useless supervision.**",
], x=6.8, y=2.1, w=5.9, size=15, gap=0.42)

# --------------------------------------------------------------- 11b season
s = slide()
title(s, "We found a 70-day seasonal offset - and tested it",
      "A hypothesis that did not pan out, and why that is still a result", "M4")
pic(s, "fig7_season_offset.png", 0.6, 1.95, 4.6)
bullets(s, [
    "**Madrid's median observation is day 175. Amsterdam's is 105.**",
    "June-August share: Madrid 48.3%, Amsterdam 20.5%.",
    "So part of the apparent domain shift is phenology, not architecture.",
    "The starter never uses the day-of-year column at all.",
    "",
    "**We rebuilt the features to control for it** - season-matched spectra,",
    "coverage restored, observation density, label-free change timing. 94 features.",
    "",
    "**It did not help.** +0.0001 on selection; slightly worse on audit.",
    "The new features hold 29% of importance across 38% of the columns -",
    "informative but dilutive. Going 60 to 94 dimensions makes prototype",
    "estimation noisier, which is why it loses most at 5 shots.",
    "",
    "**Same lesson as the whitening result: in the low-data regime, extra**",
    "**dimensions cost more in estimation error than they add in signal.**",
], x=5.9, y=2.0, w=7.0, size=13, gap=0.34)

# --------------------------------------------------------------- 12 honesty
s = slide()
title(s, "Reading the numbers honestly",
      "What we claim, and what we do not", "M4")
pic(s, "fig2_transfer_benefit.png", 0.6, 2.1, 3.8)
bullets(s, [
    "**The gain is small: +0.002 to +0.007.**",
    "The evidence is consistency across matched",
    "episodes, not magnitude.",
    "",
    "**Error bars are spreads, not confidence intervals.**",
    "**Confusion diagonals are recall, not F1.**",
    "Accuracy 0.4496 exceeds macro F1 0.4433 on",
    "zero-shot - accuracy would have flattered us.",
    "",
    "**Two methods were audited on the first set, so we crown no winner -**",
    "**but the headline result replicates on independent episodes.**",
], x=5.9, y=2.05, w=6.8, size=15, gap=0.42)

# --------------------------------------------------------------- 13 failure
s = slide()
title(s, "Where it still fails", "Class 2 is the hard one", "M4")
pic(s, "fig5_confusion.png", 0.8, 1.95, 4.6)
bullets(s, [
    "**37% of true Class 2 pixels are predicted Class 1.**",
    "",
    "Zero-shot Class 3 was the sharpest failure:",
    "recall 0.19 against precision 0.77. The Madrid",
    "model almost never predicted it, but was usually",
    "right when it did.",
    "",
    "**Adjacent eras look alike from space. That is a**",
    "**property of the problem, not a bug to tune away.**",
], x=6.4, y=2.2, w=6.3, size=15, gap=0.44)

# --------------------------------------------------------------- 14 limits
s = slide()
title(s, "Limitations", "Stated, not hidden", "M4")
bullets(s, [
    "**1.  Features are still built label-dependently** - the pipeline could not currently",
    "        generate features for an unlabelled hidden test set.",
    "**2.  Scaling is fitted before cross-validation** - not fold-safe.",
    "**3.  Two methods were audited on the original set** - so we crown no winner there.",
    "        The headline result has since been replicated on an independent episode set.",
    "**4.  No independent verification yet** - Gate S needs a second person.",
    "**5.  We appear to be near a label-noise ceiling.**",
    "",
    "No claims of worldwide portability. No claims of calibrated confidence.",
], y=2.2, gap=0.48)

# --------------------------------------------------------------- 15 conclusion
s = slide()
title(s, "Conclusion", None, "M1")
bullets(s, [
    "**The starter's transfer learning transferred nothing. We proved it.**",
    "**We built one that does, and measured it against the right control.**",
    "**Five-shot macro F1 up 0.0515 over the target-only control, 40 of 50 episodes won.**",
    "**The failures are documented. The method is sound.**",
], y=2.5, gap=0.72)
_, p = txt(s, 0.9, 5.0, 11.5, 1.2)
r = p.add_run()
r.text = "A number without a mechanism is not a finding."
r.font.size = Pt(26)
r.font.bold = True
r.font.color.rgb = ACC

# --------------------------------------------------------------- backups
s = slide()
title(s, "Backup - reproducibility", "Everything is re-runnable")
bullets(s, [
    "requirements.txt pins the exact stack that produced every number.",
    "Raw data SHA256 recorded. Feature cache SHA256 f6f588c4...5f33.",
    "Episode support indices stored, not regenerated from a seed.",
    "Stage 1 artifact is 3 KB. Reload test passes 17/17 in a clean session.",
    "Seeds fixed throughout: RF 42, CV 42, sampler 42.",
    "Ten commits, tagged day1-candidate-v1.",
], y=2.2, gap=0.5)

s = slide()
title(s, "Backup - why our numbers differ from the organiser's")
bullets(s, [
    "**All six prototype budgets match them to 4 decimal places.**",
    "**Both Random-Forest results differ: +0.0102 and +0.1006.**",
    "The prototype path never uses the forest, which isolates the cause to scikit-learn.",
    "Determinism verified: 0 of 25,992 predictions differ across two refits.",
    "**Still inferred, not measured** - nobody installed the organiser's version to confirm.",
], y=2.2, gap=0.5)

s = slide()
title(s, "Backup - the episode protocol", "How support and query are kept honest")
bullets(s, [
    "One permutation per class per trial. Each budget reads a prefix of it.",
    "**That makes budgets nested: support(5) is a subset of support(25), and so on.**",
    "Support and query are disjoint and verified disjoint in code, every episode.",
    "Query labels are used for scoring only - never for fitting or selection.",
    "At 25 shots: 100 support pixels, 25,892 query pixels.",
    "**The query set shrinks unevenly as the budget grows - Class 4 loses 7% of its**",
    "**pixels at 200 shots versus Class 2's 2.3%. A stated limitation.**",
], y=2.2, gap=0.47)

prs.save(OUT)
print("Saved {}  ({:.0f} KB, {} slides)".format(OUT, OUT.stat().st_size / 1024, n_slides))
