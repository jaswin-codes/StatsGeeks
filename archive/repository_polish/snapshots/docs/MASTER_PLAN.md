# Hackathon Overview

**Living project document — single source of truth for team progress and decisions.**

Source: `Hackathon_Analysis_Report.md`. This plan summarises that audit; it does not represent a new repository inspection or completed implementation. Update status, owners, evidence, and organiser decisions as work progresses. Preserve the audit as the historical reference. Operational instructions for AI assistants are in `AGENTS.md`.

**Current phase:** Planning and context handover. Baseline reproduction and implementation are not yet recorded as completed.

## Problem statement

Classify the construction era of buildings within a 30 m × 30 m Landsat pixel into four classes using multiyear observations across Blue, Green, Red, NIR, SWIR1, and SWIR2.

## Goal

Train a transferable model entirely on Madrid, then adapt its learned representation to Amsterdam using few labelled pixels. Prioritise defensible, reproducible transfer and stable performance at 25 labels per class, rather than only improving Madrid classification.

## Final deliverables

1. Saved Madrid Stage 1 model, including necessary preprocessing and representation state.
2. Runnable Amsterdam adaptation notebook or script consuming Stage 1 state and labelled support data, with configurable samples per class and fixed seeds.
3. Madrid cross-validation macro F1 mean/std and confusion-matrix proportions.
4. Repeated Amsterdam evaluation with macro F1 mean/std at the required label budgets.
5. PowerPoint with first-slide abstract, design decisions, results, and learning curve.
6. Written justification covering model design, transfer strategy, and F1 interpretation.

Also prepare reproducible run instructions, dependency versions, artifact reload tests, and backups. Prediction-file format and whether adapted models must be submitted remain unconfirmed.

## Evaluation metric

- **Four-class macro F1** is the primary metric; do not substitute accuracy or weighted F1.
- Predictions are integers 1–4 per geographic pixel.
- Provisional Amsterdam budgets: **5, 25, 50, 100, 200 labels per class**, or 20, 100, 200, 400, 800 labels total.
- Report mean, standard deviation, trial/fold counts, and what varied. Standard deviation is not a confidence interval.
- Hidden Madrid and Amsterdam test sets are not supplied. There is no documented winning F1 threshold.

## Judging criteria

| Dimension | Points | Evidence to prepare |
|---|---:|---|
| Challenge understanding and transfer strategy | 30 | Domain-shift explanation, genuine source-state reuse, low-data mechanics, reproducibility, limitations |
| Originality and solution creativity | 40 | Problem-specific hypothesis, justified contribution, controlled ablations, insightful failures |
| Presentation and team collaboration | 30 | Clear abstract and storytelling, correct results interpretation, meaningful contributions and speaking roles for all four members |

The rubric permits a lower-F1 but novel and insightful method to win Best Overall. Notebook 1 separately describes best average Amsterdam F1, best peak F1, best 25-shot F1, and best originality prizes; their relationship requires clarification.

The presentation and justification must each cover model design, transfer strategy, and F1 interpretation. The rubric allows up to 5 points deducted for word-limit/pillar omissions and up to 20 points deducted or disqualification for scientific unsoundness, off-topic methods, or unprofessional conduct.

## Important constraints

- Preserve all organiser notebooks and raw datasets unchanged; work on copies.
- Source city is Madrid; target city is Amsterdam. Use four classes, not regression or five classes.
- Keep features independent of labels. `weighted_mean_year` is for label derivation only; `age_class` and true-construction-year-centred features must never enter predictive inputs.
- Amsterdam adaptation uses support labels only. Query labels are evaluation-only.
- Keep every year's observations for one geographic pixel in the same split. Use `(city, px_key, py_key)` when combining cities; `pixel_id` includes acquisition year.
- Fit learned preprocessing, feature selection, and representations within training folds.
- Adaptation must demonstrably consume source-learned state, not merely replace the source classifier with target-only fitting.
- Keep fixed seeds and runnable clean-session workflows; explicitly save and reload models and preprocessing.
- Spatial context and AI assistants are stated as allowed; metric learning is optional.
- Stated shared resources are 16 CPUs, 128 GB RAM, and 200 GB disk. Confirm access and GPU availability; coordinate heavy jobs and back up before shutdown.

## Known ambiguities requiring organiser clarification

All items remain open unless an answer is recorded here with its source and date.

| Topic | Question | Provisional handling |
|---|---|---|
| Label budgets | Five or four Amsterdam budgets? Is 10-shot optional? | Support 5, 25, 50, 100, 200; treat 10 as diagnostic |
| Justification | 300-word notebook limit or 500-word rubric limit? | Stay within 300 words |
| Judging | Which prize rules govern? Is there Best Overall? Are rubric percentage inequalities reversed? | Prepare for 30/40/30 rubric and stated metric prizes; do not interpret malformed bands as valid thresholds |
| Presentation/submission | Time limit, deadline, upload mechanism, model format, callable interface, prediction files, adapted-model artifacts? | Do not invent official requirements |
| Labels | Right-inclusive intervals? Binned weighted mean or majority age class? | Preserve implemented intervals below |
| Observation horizon | Is 2025 allowed and expected at inference? | Record actual 1984–2025 data; keep horizon configurable and versioned |
| Hidden evaluation | Schema, geographic separation, support sampler, required folds/trials? | Use explicit pixel-level support/query protocol with spatial sensitivity checks |
| Target data use | Are unlabelled query alignment, pseudo-labels, or broader Amsterdam development labels permitted? | Do not use unconfirmed target-data privileges |
| External resources | External data/pretrained models permitted? | Do not introduce without clarification |
| Input availability | Coverage and coordinates allowed/available at test time? | Treat additional features as conditional |
| Transfer eligibility | Does source-only scaling count, or is supervised source reuse required? | Require genuine source-supervised state reuse |
| Radiometry/provenance | Scale, offset, harmonisation, QA conventions, upstream notebooks, record sources/licences? | Do not apply unverified corrections |
| Compute/logistics | Current resources, GPU, four-person access, exact shutdown? | Coordinate shared resources and keep local backups |

# Current Repository Status

## Current project structure

The audit records a flat workspace, not the `notebooks/` and `../data/` hierarchy expected by the starter code.

| Files | Role |
|---|---|
| `1-Introduction.ipynb`, `2-Reading_Data.ipynb`, `3-Preprocessing.ipynb`, `4-Modelling.ipynb` | Immutable organiser notebooks |
| `madrid_train.parquet`, `amsterdam_data.parquet` | Immutable raw source and target datasets |
| `building_age_transfer_learning_hackathon.md` | Lecture transcript and logistics |
| `Evaluation Rubric Overview.docx` | Scoring and deduction rules |
| `hackathon_computing_resources.md` | Server, memory, package, and backup guidance |
| `METRIC_LEARNING_APPROACH.md` | Optional concept guide; reverses city direction and suggests incompatible five-class framing |
| `Open Notebook.onetoc2` | Binary table of contents; no readable content extracted in audit |
| `WhatsApp Image 2026-09-07 at 14.51.21.jpeg` | Participant roster screenshot; no technical requirements |
| `Hackathon_Analysis_Report.md` | Historical comprehensive audit |
| `MASTER_PLAN.md`, `AGENTS.md` | Living plan and permanent assistant instructions |

At audit time there was no Git metadata, README, dependency manifest, standalone Python code, evaluation script, processed pickle, saved final model, or hidden test data. No implementation progress beyond the audit is asserted here.

## Important notebooks

| Notebook | Purpose and dependency | Team action |
|---|---|---|
| 1 — Introduction | Documentation only: task, labels, requirements, prizes | Reference original; track contradictions in this plan |
| 2 — Reading Data | Loads both Parquets; EDA, quality checks, trajectories, distributions; saves no pipeline input | Work on a copy for targeted diagnostics |
| 3 — Preprocessing | Loads raw files; creates 60 features per pixel, standardises, writes `../data/preprocessed/preprocessed_data.pkl` | Copy and make label-independent, fold-safe, configurable, and reproducible |
| 4 — Modelling | Reads the pickle; RF CV, zero-shot, target prototypes, maps; models remain in memory | Copy; correct transfer path, evaluation, and explicit export |

Reading order is 1 → 2 → 3 → 4. Execution dependency is raw Parquets → Notebook 3 → processed pickle → Notebook 4. Notebook 2 is not a computational prerequisite for Notebook 3.

## Dataset summary

These are audit-verified facts, not new measurements.

| Property | Madrid | Amsterdam |
|---|---:|---:|
| Raw rows | 3,172,765 | 1,062,877 |
| Columns | 48 | 48 |
| Geographic pixels | 76,263 | 25,992 |
| Acquisition years | 1984–2025 (42) | 1984–2025 (42) |
| Construction-year range | 1850–2021 | 1850–2016 |
| Disk size, decimal MB | 141.96 | 43.84 |
| Null cells / duplicate pixel-year keys | 0 / 0 | 0 / 0 |
| Mean building coverage | 50.51% | 42.12% |
| Class 1 / 2 / 3 / 4 counts | 13,794 / 27,152 / 18,672 / 16,645 | 7,568 / 8,802 / 6,745 / 2,877 |

Each row is a pixel-year with three observation slots, each containing six bands, QA flags, acquisition day, scene, and sensor metadata. Twelve metadata columns plus 36 observation columns give 48 columns. Combined data represent 102,255 geographic pixels, not millions of independent examples.

Preserve current right-inclusive label intervals until explicitly instructed otherwise:

| Class | Madrid weighted construction year | Amsterdam weighted construction year |
|---|---|---|
| 1 | ≤1960 | ≤1945 |
| 2 | >1960 and ≤1984 | >1945 and ≤1984 |
| 3 | >1984 and ≤2004 | >1984 and ≤2004 |
| 4 | >2004 | >2004 |

The starter feature vector contains 12 overall band statistics, 10 index statistics, 12 early-period statistics, 12 late-period statistics, 12 annual-change statistics, and two period-availability flags. Expected processed dimensions are Madrid 76,263 ×60 and Amsterdam 25,992 ×60, but the processed file is absent at audit time.

## Current baseline results

**Saved starter outputs only — not independently reproduced by the team or audit.**

| Experiment | Macro F1 |
|---|---:|
| Madrid balanced 500-tree RF, 5 folds ×5 repeats | 0.6179 ±0.0043 |
| Amsterdam zero-shot Madrid RF | 0.3427 |
| Amsterdam raw-feature prototypes, 5/class | 0.5437 ±0.0324 |
| 10/class, optional diagnostic | 0.5649 ±0.0312 |
| 25/class | 0.5986 ±0.0176 |
| 50/class | 0.6079 ±0.0101 |
| 100/class | 0.6129 ±0.0097 |
| 200/class | 0.6150 ±0.0036 |

Prototype results use ten support draws. Madrid contributes scaling, but its trained RF is not used in the prototype adaptation path. These results do not prove supervised transfer.

## Existing risks

- **Critical:** label leakage, query-label reuse, no genuine Stage 1 transfer, label-dependent hidden-test inference.
- **High:** incorrect labels/metrics/budgets, optimistic spatial validation, season/sensor confounding, unverified radiometry, sparse-support overfitting, missing exports, submission ambiguity, lost server work.
- **Medium:** interpolation artifacts, redundant features, overclaimed uncertainty, misleading maps, shared-resource contention, stale notebook outputs, merge conflicts, package drift, unsupported global-portability claims.

## Known issues

- Starter paths do not match the flat workspace; processed-file parent creation is fragile.
- Feature construction depends on `age_class` and carries construction year; an inference path without labels is missing.
- Scaling is fitted on all Madrid before CV, exposing validation-feature statistics.
- Notebook 4 never exports the final RF or submission package.
- QA-valid observations can still contain artifacts. Starter filtering leaves 23 Madrid and seven Amsterdam rows with zero or exact 65535 values, plus other extreme values.
- First-valid selection discards hazy observations without trying potentially usable alternate slots. The audit identified 10,359 Madrid and 8,373 Amsterdam potentially recoverable rows under simple checks, not guaranteed-clean replacements.
- Acquisitions occur across all months. Only approximately 49% of selected Madrid and 30% of selected Amsterdam observations are June–August.
- Coverage is dropped by starter feature generation; long gaps and input-derived horizons need explicit handling.
- Class 2, not Class 1, is largest in both cities; RF already uses `class_weight='balanced'` despite stale prose.
- Repeated CV does not imply independent scores; repeated map entries overwrite pixels instead of averaging predictions.
- Prototype softmax is not calibrated confidence; true-class log loss needs labels.
- Starter learning curve is not explicitly base-2 logarithmic; example confusion matrices are single draws.

## Current assumptions

- Follow Madrid → Amsterdam, four classes, and current implemented boundaries pending written clarification.
- Support all five stated budgets and keep the justification ≤300 words.
- Treat source-supervised representation plus target prototypes as the initial technical direction, not a proven winning method or an already implemented decision.
- Use only confirmed data permissions; do not assume query-feature alignment or unrestricted target-label tuning is allowed.
- Keep source artifact immutable during adaptation and reserve final audit evaluation from tuning.
- Retain full historical trajectories for current-building classification; confirm the permitted 2025 horizon.
- Keep two-city claims proportionate to evidence. Novelty, validity, and presentation matter alongside F1.

# Technical Strategy

## Preprocessing strategy

1. Reproduce starter behaviour on working copies before changing observation handling; record any safety-related deviations.
2. Separate label derivation from a label-free transformation of raw spectra and metadata.
3. Use stable geographic keys, explicit feature allowlists, a saved annual horizon, and a fixed feature order.
4. Fit learned transforms within source training folds, then refit on full Madrid after selection.
5. Test QA-aware alternate-slot selection, season comparability, and robust gap handling. Interpret sensor-specific QA and radiometry before changing corrections.
6. Preserve missingness/observation-count indicators. Version feature caches and avoid repeated expensive preprocessing.
7. Test robust temporal summaries, early/late contrasts, label-free change timing, and coverage if available at inference. Never centre features on the true construction year.

## Modelling strategy

Use a controlled ladder: majority-class reference → Madrid RF and zero-shot transfer → raw-feature Amsterdam prototypes → source-supervised metric/embedding with target prototypes. Use matched episodes for comparison.

Start with a compact representation and a simple target head. If an embedding is unstable, retain a simpler Madrid-supervised feature-weighting/metric transformation. Consider regularised target heads or limited fine-tuning only after the frozen approach is reliable. Do not launch an arbitrary algorithm sweep.

## Transfer learning strategy

Train the representation entirely on Madrid. Freeze it initially; transform Amsterdam support and query features through saved source state, calculate class prototypes from support labels only, and classify queries by distance.

Prove source-learning benefit against raw-feature target prototypes and an untrained/unlearned representation where practical. Prioritise 25-shot stability, while evaluating every required budget. Test static-appearance versus temporal-change feature groups as a problem-specific hypothesis, accounting for seasonal confounding.

## Validation strategy

- Madrid: stratified pixel CV for baseline comparability, all years grouped, learned transforms inside folds, plus spatial-block robustness checks.
- Amsterdam: fixed, disjoint support/query episodes; configurable per-class budgets; repeated draws; matched episode IDs across methods; preferably nested budgets within each trial.
- Sampling infrastructure may inspect labels to draw balanced support; the adaptation model receives only selected support labels.
- Keep a separate final audit partition or final episodes unused for hyperparameter selection. Clarify broader target-label development permissions before use.
- Report four-class macro F1 mean/std, per-class diagnostics, trial counts, and the source of variation. Confusion-matrix diagonals are recall, not F1.
- Check spatial separation sensitivity and label-free inference before model selection is finalised.

## Experimentation philosophy

Every experiment needs a hypothesis, controlled change, reproducible configuration, and recorded outcome. Keep improvements only when reliable or scientifically informative. Document failed experiments rather than hiding them. Prioritise QA/season handling, coverage, temporal contrasts, and demonstrated transfer benefit. Stop architecture expansion early enough to package and rehearse.

# Project Architecture

**Planned pipeline; not an assertion that these components already exist.**

```text
Raw data
    ↓
Preprocessing
    ↓
Feature engineering
    ↓
Madrid training
    ↓
Amsterdam adaptation
    ↓
Evaluation
    ↓
Presentation
```

| Stage | Contract and outputs |
|---|---|
| Raw data | Immutable Parquets, checksums, city/pixel identifiers; isolate labels from predictive inputs |
| Preprocessing | Configurable paths, QA/slot policy, observation horizon, missingness handling; label-free transforms |
| Feature engineering | One row per geographic pixel, versioned unscaled features/schema and group metadata; labels stored separately |
| Madrid training | Fold-local learned preprocessing and model fitting; validation evidence; final saved scaler/representation/classifier and configuration |
| Amsterdam adaptation | Explicit Stage 1 artifact +support features/labels +budget/seed; independent episode state; no query labels |
| Evaluation | Held-out query predictions, four-class macro F1, repeated-run tables, confusion proportions, spatial checks, immutable final audit results |
| Presentation | Reproducible figures, results table, log2 budget curve, abstract, justification, PowerPoint, backup package |

Madrid CV runs before the final full-Madrid fit. Evaluation is independent of training and adaptation: query labels never flow backwards. Shared feature/training logic should eventually live in reusable helpers, with notebooks orchestrating analysis and reporting. Save and reload all required inference objects explicitly.

# Team Plan

Owner fields are intentionally blank. All tasks are pending unless updated with evidence.

## Member A — Lead and evaluation

**Current owner:**

**Current task:** Resolve requirements and define the label, split, support/query, and metric contracts.

**Status:** Not started; planning complete in the audit.

**Deliverables:** Organiser decision log; split/episode IDs; reproducible metric reporting; leakage review; final results sign-off.

**Notes:** Own integration and comparison fairness. Day 1: baseline protocol and evaluation; Day 2: candidate selection, final audit, compliance. Presentation: problem, evaluation, conclusions.

## Member B — Data and features

**Current owner:**

**Current task:** Prepare working-copy, label-free preprocessing and a versioned baseline feature cache.

**Status:** Not started.

**Deliverables:** Feature transformation, schema/horizon contract, QA and season diagnostics, controlled feature ablations, input validation.

**Notes:** Coordinate expensive preprocessing. Day 1: baseline features and targeted QA/season candidate; Day 2: one feature ablation and feature freeze. Presentation: data pitfalls and feature rationale.

## Member C — Model and transfer

**Current owner:**

**Current task:** Reproduce source RF and target prototype baselines, then establish genuine source-state reuse.

**Status:** Not started.

**Deliverables:** Saved Madrid model/representation; parameterised Amsterdam adaptation; transfer ablations; reproducible configurations; reloadable artifacts.

**Notes:** Start frozen and simple; protect source state. Day 1: valid transfer candidate; Day 2: one targeted model ablation, final fit and export. Presentation: method, transfer mechanics, ablation.

## Member D — Reproducibility and communication

**Current owner:**

**Current task:** Establish environment/run instructions, experiment records, packaging tests, and slide outline.

**Status:** Not started.

**Deliverables:** Dependency record; independent clean-session rerun; experiment log; PowerPoint; justification; submission inventory and backups.

**Notes:** Day 1: submission-shaped package and draft deck; Day 2: independent verification, final figures, word-count checks, packaging. Presentation: results, reproducibility, deployment.

## Checkpoints and merge points

| Target | Checkpoint |
|---|---|
| Day 1, 11:00 | Interfaces, responsibilities, and evaluation contract agreed |
| Day 1, 12:30 | Baseline pipeline merged and discrepancies reviewed |
| Day 1, 15:00 | At least one genuine transfer candidate runs |
| Day 1, 16:30 | Leakage and inference review; valid pipeline merged |
| Day 1, 17:30 | Submission-shaped package and backup exist |
| Day 1 close | Stable tag; select at most two Day 2 experiments |
| Day 2, 11:00 | Final candidate selected from matched comparisons |
| Day 2, 12:30–13:30 | Model/features frozen; final audit and clean-session checks |
| Day 2, 15:00 | Submission-ready deck, justification, artifacts |
| Day 2, 15:00–16:00 | Timed four-person rehearsal and rubric review |
| Day 2, 17:00 | Submission frozen, packaged, and backed up |
| Day 3 | Offline presentation checks, all four speak, technical Q&A |

# Experiment Tracker

Populate only with actual planned or executed experiments; do not turn saved starter scores into reproduced results. Each row should link to a record containing commit, feature/split versions, seeds, parameters, per-budget mean/std, per-class diagnostics, trial counts, runtime, memory, and interpretation.

| Experiment ID | Hypothesis | Changes | Result | Decision | Notes |
|---|---|---|---|---|---|

# Current Priorities

Ordered checklist. Baseline reproduction includes the minimum path/environment setup needed in working copies; do not begin optimisation while baseline or safety gates are unresolved.

1. ☐ Preserve original notebooks
2. ☐ Create working copies
3. ☐ Reproduce baseline
4. ☐ Record baseline provenance, seeds, deviations, and results; distinguish saved outputs from reproduced runs
5. ☐ Establish shared Git workflow, file ownership, dependency versions, and portable paths
6. ☐ Obtain written organiser clarification and update provisional requirements
7. ☐ Confirm right-inclusive labels and test exact boundary years
8. ☐ Define stable geographic keys and freeze source folds and target episodes
9. ☐ Separate labels from features and enforce support/query isolation
10. ☐ Make feature generation work without construction-year or class columns
11. ☐ Move learned transforms inside source training folds
12. ☐ Save a fixed horizon, ordered feature schema, and versioned baseline cache
13. ☐ Establish four-class macro F1 reporting at all five provisional budgets
14. ☐ Implement a real source-learned adaptation path and target-only comparison
15. ☐ Reserve final audit evaluation and establish spatial sensitivity checks
16. ☐ Save and independently reload model, preprocessing, and adaptation configuration
17. ☐ Pass clean-session, label-free inference, metric, and leakage checks
18. ☐ Establish experiment logging and a coordinated CPU/RAM schedule
19. ☐ Tag a validated baseline and create a preliminary submission package with backups
20. ☐ Begin controlled QA/season, temporal-feature, and transfer optimisation only after the above gates pass

# Final Submission Checklist

## Required deliverables and compliance

- [ ] Madrid Stage 1 model trained entirely on source data and explicitly saved.
- [ ] Required scaler, preprocessing, representation, feature schema, horizon, labels configuration, and model state saved.
- [ ] Runnable adaptation notebook/script consumes Stage 1 state and labelled Amsterdam support data.
- [ ] Samples per class are configurable; all five provisional budgets supported unless organisers confirm otherwise.
- [ ] End-to-end deterministic seeds and reproducible run instructions supplied.
- [ ] Madrid CV macro F1 mean/std and confusion-matrix proportions included.
- [ ] Amsterdam repeated-evaluation macro F1 mean/std included for every required budget.
- [ ] Trial/fold counts and error-bar meaning stated.
- [ ] PowerPoint completed with first-slide abstract ≤150 words.
- [ ] Results table includes Madrid and all required Amsterdam scores with uncertainty.
- [ ] F1 with error bars versus log2(sample size) plot included.
- [ ] Written justification covers model design, transfer strategy, and F1 interpretation; ≤300 words pending clarification.
- [ ] Exact official upload, deadline, artifact/interface requirements confirmed; any requested prediction or adapted-model files supplied.

## Readiness and recommended supporting artifacts

- [ ] A different member can reload artifacts and run from a clean session.
- [ ] Inference succeeds without construction-year/class fields.
- [ ] No support/query overlap, query-label fitting, or final-audit tuning.
- [ ] Stage 1 transfer benefit is tested against target-only baseline.
- [ ] Environment/dependency versions, raw-data checksums, configurations, feature/split versions, and seeds recorded.
- [ ] Machine-readable results and reproducible figures preserved.
- [ ] Final artifacts and documentation correspond to the same stable commit/tag.
- [ ] Local backup and presentation PDF created before server shutdown.

# Presentation Checklist

- [ ] First-slide abstract is ≤150 words, accurate, and consistent with the talk.
- [ ] Explain the urban relevance, pixel-level task, Madrid source, and few-shot Amsterdam target.
- [ ] Explain four classes, mixed-pixel weighted-mean labels, and class imbalance.
- [ ] Explain seasonal/sensor domain shift without making unsupported causal claims.
- [ ] Cover essential pillar 1: model choice, parameters, and rationale.
- [ ] Cover essential pillar 2: genuine reuse of Madrid learning and low-data adaptation mechanics.
- [ ] Cover essential pillar 3: macro F1 trends across support budgets and their interpretation.
- [ ] Show Madrid and all required Amsterdam mean/std results and a base-2 budget curve.
- [ ] Distinguish accuracy, F1, recall, standard deviation, confidence intervals, and model confidence.
- [ ] Demonstrate originality through a problem-specific hypothesis and controlled ablation.
- [ ] Explain what worked, what failed, why, and remaining limitations.
- [ ] Explain support/query separation, fold-local transformations, spatial robustness, and clean inference.
- [ ] Do not claim worldwide portability or calibrated confidence beyond evidence.
- [ ] All four members contribute meaningfully and speak with planned transitions.
- [ ] Rehearse within the confirmed time limit and prepare technical Q&A.
- [ ] Keep backup slides for labels, leakage, sampling, reproducibility, and negative results.
- [ ] Confirm PowerPoint/PDF opens offline; do not depend on live training.
- [ ] Maintain professional conduct and consistency between slides, justification, and final artifacts.

# Lessons Learned
