# Submission Inventory & Run Instructions

Everything in the submission, where it lives, and how to reproduce it from nothing.

**Commit:** `member2-baseline`, tag `day1-candidate-v1`
**Status:** smoke/development. **Not independently reviewed.**

> ⚠️ **Upload mechanism, deadline and required artifact formats are still unconfirmed by the organisers.** This inventory lists what exists; it does not assume what they will ask for.

---

## 1. Required deliverables

| # | Deliverable | Where | State |
|---|---|---|---|
| 1 | Saved Madrid Stage 1 model | `candidate/artifacts/stage1_madrid.pkl` (3 KB) | ✅ in git |
| 1b | Source Random Forest | `candidate/artifacts/stage1_rf.joblib` (244 MB) | ⚠️ **not in git** — local only |
| 2 | Runnable adaptation consuming Stage 1 | `candidate/reload_test.py` | ✅ 17/17 pass |
| 3 | Madrid CV macro F1 + confusion proportions | `docs/member2_log.md`; `working/4-Modelling.ipynb` | ✅ 0.6281 ±0.0043 |
| 4 | Amsterdam repeated evaluation, all budgets | `candidate/artifacts/final_audit.json` | ✅ 5 budgets × 5 audit episodes |
| 5 | PowerPoint with ≤150-word first-slide abstract | `presentation/StatsGeeks_BuildingAge.pptx` | ✅ 18 slides, abstract 144 w |
| 6 | Written justification | `docs/PRESENTATION_OUTLINE.md` | ✅ 287 words |
| — | F1 vs log₂(budget) curve with error bars | `candidate/figures/fig1_learning_curve.png` | ✅ |

## 2. Supporting evidence

| Item | Where |
|---|---|
| Experiment records EXP-001…005 | `docs/EXPERIMENT_LOG.md` |
| Decisions DEC-001…014 | `docs/DECISION_REGISTER.md` |
| Chronological diary | `docs/TEAM_LOG.md` |
| Member logs | `docs/member2_log.md`, `docs/member3_log.md`, `docs/member4_log.md` |
| Pinned environment | `requirements.txt` |
| Verification scripts | `scripts/` (3), `candidate/` (6) |
| Figures | `candidate/figures/` (6 PNGs) |

## 3. Not in Git — obtain or regenerate

| File | Size | How to get it |
|---|---|---|
| `data/madrid_train.parquet` | 142 MB | Organisers / hackathon VM |
| `data/amsterdam_data.parquet` | 44 MB | Organisers / hackathon VM |
| `data/preprocessed/preprocessed_data.pkl` | 48 MB | Regenerate, 13½ min — see below |
| `candidate/artifacts/stage1_rf.joblib` | 244 MB | Regenerate, ~50 s — see below |

---

## 4. Reproduce from nothing

```bash
git clone https://github.com/jaswin-codes/StatsGeeks.git
cd StatsGeeks
git checkout member2-baseline
pip install -r requirements.txt

# place the two parquet files in data/ first, then:

# 1. Features  (~13.5 min)
cd working
jupyter nbconvert --to notebook --execute --inplace 3-Preprocessing.ipynb
cd ..

# verify the features match ours before trusting any comparison
python scripts/validate_pickle.py        # expect 24/24

# 2. Baseline reference  (~16 min)
cd working
jupyter nbconvert --to notebook --execute --inplace 4-Modelling.ipynb
cd ..
python scripts/extract_results.py

# 3. Transfer candidate  (~2 min each)
python candidate/search_representations.py   # selection trials only
python candidate/final_audit.py              # sealed trials, single run
python candidate/reload_test.py              # Gate S, expect 17/17
python candidate/validity_checks.py
python candidate/make_figures.py

# 4. Deck
python presentation/build_deck.py
```

**The pickle must have SHA256 `f6f588c4e3cfa2e0793354bc7772228bd4c749b39fce67bde5302f4c63955f33`.** If it differs, your features differ from the ones every reported number was computed on, and no comparison against our results is valid.

Total cold-start time: **≈35 minutes**.

---

## 5. Numbers a reader should be able to check

| Quantity | Value | Source |
|---|---|---|
| Madrid CV macro F1 | 0.6281 ±0.0043 | our run, **not** the organiser's 0.6179 |
| Amsterdam zero-shot | 0.4433 | **not** the organiser's 0.3427 |
| Candidate, 25 shots/class | 0.6028 | audit trials |
| Control, 25 shots/class | 0.5956 | audit trials |
| Transfer benefit | +0.002 to +0.007 | positive at every budget |
| Informative features | 59 of 60 | `has_early_data` is constant |

---

## 6. Known gaps — disclose, do not conceal

1. **Nothing has been independently reviewed.** Gate M and Gate S both require a second person; the team is now short a member.
2. **Feature generation is label-dependent** — could not serve an unlabelled hidden test set as it stands.
3. **Scaling is fitted before cross-validation** — not fold-safe.
4. **The audit set informed two decisions**, so no single representation is claimed best (DEC-012, binding).
5. **The scikit-learn explanation is inferred, not measured** — nobody installed the organiser's version to confirm.

## 7. Before submitting

- [ ] Confirm the upload mechanism and deadline with organisers
- [ ] Confirm presentation time limit
- [ ] Export the deck to **PDF** and confirm it opens offline
- [ ] Back up `stage1_rf.joblib` and `preprocessed_data.pkl` off this machine
- [ ] Reallocate speaking roles after the member departure
- [ ] If a second person becomes available: `python candidate/reload_test.py`
