# Speaker 2 — The Method and the Results

**Slides 5–7** · roughly **3 minutes**
Your job: explain what we actually transfer, then show it works.

> **The trap to avoid:** do not describe this as "we improved F1." The gain beyond five shots is ~1.5%. Your strength is *what* you transferred and *how* you proved it, not the size of the number.

---

## Slide 5 — Our method *(~75 s)*

Walk the four boxes left to right. Keep it plain:

> "Every method we tested is the same four steps. Learn a transform on Madrid only. Freeze it. Push Amsterdam through it. Then build a prototype for each class from the handful of labelled examples we're allowed, and each new pixel gets the class of its nearest prototype."

> "Only one thing changes between the methods we compared — the transform. That's what makes it a controlled experiment."

**Then the framing line:**

> "What we transfer is a *metric*, not a classifier. Madrid teaches us which of the 60 measurements matter for telling building ages apart. Amsterdam supplies the examples. Madrid supplies the sense of what 'similar' means."

**Then the two tiles:**

> "The forest we train is 244 megabytes. What we actually ship is 3 kilobytes. Everything that transfers fits in 3 KB — because the transfer is 60 numbers and a feature subset, not the model."

That line lands. Let it.

---

## Slide 6 — Results *(~60 s)*

> "Here's our method against the starter's actual method. Same pixels, same episodes, same environment. The only thing different is the method."

Walk the table briefly, then:

> "Better at every budget. 47 of 50 paired episodes won. And at five shots — the hard case — we're up nearly 10% relative."

**The critical honesty note — say it before anyone asks:**

> "We're deliberately not comparing to the organisers' published numbers. Different episodes and a different scikit-learn version. Our own reproduction of *their* method scores 0.5038 at five shots against their published 0.5437 — same code, different draws. Comparing across those would invent an improvement that isn't there."

---

## Slide 7 — Learning curve *(~45 s)*

> "The gain is concentrated where the data is scarcest. That's not an accident — it's the prediction. Once Amsterdam has 25 or more labels per class, it has enough of its own data and the help from Madrid falls away."

> "Five shots is the case that actually matters if you're deploying this to a city with no labelled stock. That's where we improve most."

**Hand over:** *"And when we looked at why, we found something we didn't expect. [Name]."*

---

## If you have 30 seconds less

Compress slide 7 into one sentence on slide 6 and skip the figure.

---

## Questions likely to come to you

**"Why nearest-prototype instead of a proper classifier?"**
> With five labelled examples per class, almost anything with parameters overfits. A prototype is one mean per class — four numbers-worth of estimation. We tested richer alternatives; they lost.

**"What exactly is `λ`?"** *(this will come up)*
> How much we trust Madrid versus Amsterdam when we build a class prototype. λ=0 ignores Madrid entirely — that's the starter's method. λ=0.6 means 60% Madrid, 40% Amsterdam. It's a blending weight, like a complementary filter between a stable-but-biased sensor and an accurate-but-noisy one.

**"And `k`?"**
> How many of the 60 features we keep, ranked by Madrid's importance. k=45 beat k=60 at every budget — 15 of the starter's features were actively hurting.

**"Isn't 3 KB suspiciously small for a transfer method?"**
> That's the point. The forest is the apparatus that derives the weights; adaptation only needs the weights themselves. It makes the artifact trivially portable and reload-testable.

**"Did you use the unlabelled Amsterdam data?"**
> No. Deliberately. The plan lists unlabelled query alignment as an unconfirmed permission, so we compute everything from the support set only. It would probably have helped, and we didn't do it.

**"How do you know the improvement isn't luck?"**
> Episodes are matched — every method sees identical support draws — so we compare paired differences. 47 of 50 paired wins, with 10/10 at three separate budgets, on an audit set we never selected on.
