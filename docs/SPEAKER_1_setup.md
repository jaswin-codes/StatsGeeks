# Speaker 1 — The Setup and the Discovery

**Slides 1–4** · roughly **3 minutes** of a 10-minute talk
Your job: land the problem, then deliver the discovery that makes the whole talk work.

> **You have the best material in the deck.** Slide 4 is the moment the audience sits up. Do not rush to it and do not undersell it.

---

## Slide 1 — Title + Abstract *(~30 s)*

**Do not read the abstract aloud.** It is on the slide for the rubric; the judges can read.

Say something like:

> "We were asked to work out how old buildings are from satellite images — training on Madrid, then adapting to Amsterdam with almost no labels. What we found first was that the starter code we were given doesn't actually do the thing it says it does. That's where we'll start."

Then move on. Do not linger.

---

## Slide 2 — The problem *(~45 s)*

Key points, in your own words:

- Building age drives retrofit and energy policy — and the records are incomplete
- Each pixel is 30 m × 30 m of ground, seen once a year for 42 years
- Four eras. Train Madrid, adapt Amsterdam.
- **The hard constraint: as few as five labelled examples per class**

**Point at the "5" tile.** Say: *"Five. That's the whole problem."*

---

## Slide 3 — The data *(~45 s)*

- Six spectral bands, once a year, 1984–2025
- **Why this is even possible:** "A field becomes a roof. Concrete weathers. Old dense centres reflect differently from new suburbs. The trajectory carries a fingerprint."
- 42 years of readings collapse into 60 summary numbers per pixel

**Then the honest bit — the orange line:**

> "One pixel can hold a 1950s block and a 2010s block. The label is an area-weighted average, so it describes neither. There's a ceiling here well below a perfect score, and nobody knows where it is. That matters for how you read every number we show you."

---

## Slide 4 — The defect *(~60 s)* ← **your key slide**

Slow down here.

> "The starter pipeline trains a Random Forest on Madrid. Then it throws it away."

*(pause)*

> "The Amsterdam prototypes are built from Amsterdam data alone. Madrid contributes a scaler — the mean and variance used to normalise. Nothing else."

> "So when you see its learning curve go up as you add labels, that isn't transfer. That's an Amsterdam-only method getting more Amsterdam data. Nothing crosses between the cities."

**Then the turn — this is the line that earns you originality marks:**

> "And that flaw turned out to be the most useful instrument we had. Because that path never touches the tree code, it acted as a control. It's how we proved our data pipeline was identical to theirs, and isolated a scikit-learn version difference in the baseline numbers."

**Hand over:** *"So we built one that actually transfers. [Name] will take you through it."*

---

## If you have 30 seconds less

Cut slide 3's technical detail, keep the noisy-labels point. Never cut slide 4.

---

## Questions likely to come to you

**"Why four classes and not a regression on year?"**
> The organisers defined it as four classes with city-specific boundaries — Madrid splits at 1960, Amsterdam at 1945, reflecting different histories. We kept their definition. Changing it would have made our numbers incomparable to the baseline.

**"How do you know the labels are noisy?"**
> The label is `weighted_mean_year` — an area-weighted average of construction years for buildings in the pixel. That's the organisers' own construction. A mixed-age pixel gets a class that describes no building in it.

**"Isn't 30 m very coarse for a building?"**
> Yes, and that's the core difficulty. A 30 m pixel often contains several buildings of different ages. It's why we treat the ceiling as real rather than assuming more modelling would fix it.

**"Did you consider using higher-resolution imagery?"**
> We didn't — external data wasn't a confirmed permission in the brief, and the challenge is defined on this dataset. It would be the obvious next step if allowed.
