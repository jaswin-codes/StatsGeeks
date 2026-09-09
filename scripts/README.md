# `scripts/` — verification tools for the reproduced baseline

These check that the **organiser's baseline** reproduces correctly on this
machine. They do not train or modify anything, and they belong to Member 2's
baseline work — the transfer method lives in `candidate/`.

**Run all of them from the repository root**, not from inside `scripts/`.
They need `data/preprocessed/preprocessed_data.pkl` to exist first.

| Script | Runtime | What it answers |
|---|---|---|
| `validate_pickle.py` | ~5 s | Does the feature cache satisfy the contract? 24 checks in a **fresh interpreter**. |
| `determinism_check.py` | ~95 s | Does the Random Forest give the same answer twice? |
| `extract_results.py` | ~2 s | What did the reproduced run actually produce, versus the organiser's published numbers? |

---

## Why each one exists

### `validate_pickle.py`

Checks shapes `(76263, 60)` and `(25992, 60)`, the exact ordered 60-feature
schema, four classes per city, no non-finite values, pixel keys row-aligned and
unique, and scaler fit state. It reloads in a **fresh interpreter** because a
pickle that only works inside the kernel that made it is not a reusable artifact.

**This is what found the dead feature.** `has_early_data` is constant 1.0 for
every pixel in both cities — 60 features, but only **59 informative**. The
Random Forest independently agrees: it assigns that feature importance exactly
`0.000000`.

### `determinism_check.py`

Refits the final Madrid forest twice with the identical seed and compares every
prediction.

This mattered because our numbers differ from the organiser's published ones
(Madrid CV 0.6281 vs 0.6179; zero-shot 0.4433 vs 0.3427). A *systematic library
difference* and an *unrepeatable run* look identical from a single run, and have
opposite consequences: one leaves a usable reference, the other means the
baseline is worthless and every comparison built on it is meaningless.

Result: `0.4432736088` both times, **0 of 25,992 predictions differing**. The gap
is systematic and stable, so 0.6281 is a reliable datum.

> **Caveat — the script overstates its own conclusion.** Its printed message says
> the gap is "systematic (library version)". It tested no such thing. It rules
> out *randomness*. The library-version explanation comes from separate evidence:
> all six prototype budgets match the organiser exactly while both
> Random-Forest-dependent results differ, which isolates the divergence to
> scikit-learn. That remains **inferred, not measured** — nobody has installed
> the organiser's version and re-run.

### `extract_results.py`

Builds the comparison table. It **counts the individual `Fit N/25` output lines**
rather than trusting the summary — a shortened run would still print a plausible
mean, and the team's own timeline warns against unreported parameter reductions.
It also reports the Madrid CV difference as a multiple of the fold standard
deviation, so "close" is quantified rather than eyeballed.

---

## The number that matters to everyone else

**Benchmark Day 2 work against `0.6281` (Madrid CV) and `0.4433` (zero-shot) —
not the organiser's published `0.6179` and `0.3427`.**

A candidate compared against the published zero-shot would be credited with
roughly **+0.10 of improvement that is purely a library version difference**.

The prototype budgets are unaffected — those reproduce the organiser's numbers
exactly and can be compared against either source.

Full evidence: `docs/member2_log.md` and `docs/EXPERIMENT_LOG.md`.
