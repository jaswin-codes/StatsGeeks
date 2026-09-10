# Gate 4 — Candidate modelling readiness audit

> Latest certification: [G4A-TEARDOWN-002 — PASS](G4A-TEARDOWN-002/REPORT.md).
> Bounded subreaper repair passed normal/abnormal teardown, fresh-state, isolation and matched-routing checks in two fresh processes.
> All 60 episode identities/RNG records independently verified; evaluator-only manifest frozen at `working/gate4_episode_manifest.json`.
> SHA256: `9d493d99f60098cb22fd781c51e2d2907d6831df72cb2524700293aa1a1bbf32`.
> No candidate modelling or Notebook 4 rerun. STOP for new explicit Gate 4B/E1 authorization; current entry remains probe-only.
> The historical audit below is preserved and predates this certification.

**ID:** G4-AUDIT-001 · **Date:** 2026-09-08 · **Owner:** Member 3 / modelling-research agent

## Decision

**GATE 4 READINESS: BLOCKED for candidate execution.** The read-only research/design package is ready for Team Lead review. This is **not** a rejection of the accepted baseline and does **not** call for rerunning Notebook 4.

The most important unresolved issue is the **target-label development/final-audit contract combined with absent matched episode IDs**. The frozen zero-shot score covers all target pixels, while few-shot scores exclude supports. Full-target labels have already been evaluated and, under this task's express authorisation, used for diagnostic error/class-conditional summaries. Future candidate fitting, selection, and final-audit claims need explicit boundaries; missing episode IDs prevent exact-query paired claims today.

Supporting documents:
- [Measured baseline diagnostics](gate4_baseline_error_analysis.md)
- [Five fixed candidate specifications and experiment matrix](gate4_candidate_experiment_plan.md)

No candidate is approved by this document. The Team Lead owns approval, shared IDs, scientific exceptions, resources, and integration.

## Evidence status convention

- **FACT:** inspected code, current user handoff, or measurements from hashed artifacts.
- **INFERENCE:** defensible interpretation, not a proven cause.
- **HYPOTHESIS:** proposed fixed intervention; no executed candidate results.
- **UNKNOWN:** absent evidence; not silently converted into pass/fail or filled with guesses.

## Gate checklist

| Check | Finding | Status / narrowly scoped follow-up |
|---|---|---|
| Reference execution/protocol acceptance | User handoff says PASS; recovered metadata and notebook sources support the measured reference, not numerical replication of historical starter outputs | PASS for this audit; no baseline rerun |
| Original preservation | `original/` Git-clean; Notebook 4 SHA256 remains `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae`; OneNote read-only still active | PASS; leave protection unchanged |
| Raw/cache/reference immutability | Pre-audit hashes of raw Parquets, input pickle, reference sources/helpers, frozen evidence taken; no writes to them authorised | PASS at entry; final hash comparison recorded below |
| Artifact reload/integrity | Manifest hashes pass; NPZs/pickles/schema load; OOF/target labels and IDs agree with input; saved RF attributes inspect correctly | PASS; distinguish current inspection from prior reload-inference validation |
| Baseline numbers | Madrid .6281±.0043; Amsterdam .4433; prototype 5/10/25/50/100/200 measured values retained | PASS; older starter RF values are not current comparators |
| Recomputable CV/zero-shot F1 | All 25 folds recalculated from saved OOF predictions; target F1 recomputed from saved predictions | PASS; no fit/predict needed |
| Prototype per-trial recalculation | Ten scores per budget retained; indices/predictions absent | UNKNOWN at episode level; retain gap, do not fabricate per-class prototype metrics |
| Matched candidate episodes | None retained; candidate/P0/frozen-RF query alignment not yet established | BLOCKER before paired candidate claims; lead approves isolated deterministic sampler/comparator task, not Notebook 4 rerun |
| Target query-label policy / untouched final audit | Docs leave permissions unresolved; full target set already seen in baseline evaluation/EDA | BLOCKER before candidate selection/final-audit claims; lead records development scope and genuinely independent final route or honest limitation |
| Label-free raw inference | Notebook 3 requires construction year/class metadata and filters/groups on age_class | BLOCKER to submission-safety/Gate O; separate candidate-only safety task; do not alter reference |
| Fold-local new transforms | Reference cache is scaled globally before CV; no candidate pipeline exists | BLOCKER before new Madrid-CV claims; approve fold-local candidate layer preserving seed/folds/features |
| Genuine source-supervised transfer | Frozen raw target prototypes do not reuse RF or learned label-derived geometry | NOT IMPLEMENTED; E1 is proposed work, not an existing gate pass |
| Candidate execution permission | Current task explicitly prohibits model execution; existing DEC-001 covers reference only | BLOCKED until a new scoped approval |
| Resource/environment readiness | RF is 1.336 GB on disk; earlier policy blocks transient; recovery environment identified | Pending fresh imports/resource slot on any future run; no installations or policy bypass |
| Experiment registry / immutable run paths | `docs/EXPERIMENT_LOG.md` contains only `/`; master tracker empty; no shared candidate IDs/paths approved | Lead to allocate IDs/paths and approve append-only records; not fixed here |
| Git integration | `main` is dirty; baseline files/helpers/recovery metadata uncommitted; no tag/commit identifies complete accepted baseline | BLOCKER to reproducible merge, not to these read-only diagnostics; lead stages narrow reviewed files and logs artifact locations/hashes |
| Presentation/lead records | Master phase still says Notebook 4 next, decision/team logs only Phase 1; Member 4 evidence placeholders say no results | Documentation reconciliation required by owners before candidate launch/claims; baseline authority is current user handoff plus recovery evidence |

## 1. What is solid now — FACT

- Input hash `.pkl`: `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`.
- Madrid X/y `(76263,60)/(76263,)`; Amsterdam `(25992,60)/(25992,)`; 60 ordered feature names.
- Saved Madrid OOF arrays have 381,315 appearances and four-column probability vectors; five occurrences per source pixel. Shape and semantic row alignment checked against accepted y/IDs.
- Saved zero-shot arrays have 25,992 predictions/four-column probability vectors; score `.443273608786401` independently recalculable without calling the model.
- Prototype arrays contain 60 trial scores total. Their means/SD reproduce accepted summaries but not per-class trial errors.
- Saved RF has 500 trees, classes `[1,2,3,4]`, 60 features, balanced class weights, seed 42. Full parameters in recovery metadata match inspected state.
- Original and unexecuted working Notebook 4 are byte-identical; accepted working Notebook 3 source changes remain cells 2/4/19 only. Source comparisons are rechecked at final safety verification.
- The scaler's local module is required to unpickle preprocessing. It is an environment compatibility deviation, not an improvement. No new implementation or broader sklearn compatibility is asserted.

## 2. Artifact gaps: contain them, do not rerun

| Missing item | Consequence | Safe next handling |
|---|---|---|
| Individual CV forests | Cannot derive new fold-local RF leaf embeddings from saved OOF probabilities | Do not substitute full-Madrid forest into OOF evaluation; Amsterdam-only use of full-source RF is valid. Any new source CV task requires separate approval |
| Prototype support/query IDs and query predictions | Cannot compute paired comparisons, episode confusion, or verify each trial F1 from source evidence | Ask for deterministic isolated sampler/comparator verification with fixed protocol; until then label all episode identity claims unverified |
| Final Madrid in-sample predictions | Cannot independently reconstruct recorded in-sample accuracy from stored predictions | Not decision-critical; in-sample fit is not generalisation. Do not rerun for this |
| Capture-run notebook/kernel telemetry | Some execution provenance is incomplete despite recovered model/arrays | Keep recovery metadata's validation-process provenance qualifier. Matching four-decimal summaries does not prove full-precision equality to the first run |

The earlier text-only freeze and subsequent recovered payloads are different stages of evidence. Old logs claiming arrays unavailable are historical, not current. Preserve those histories; new lead summary should point to the recovered manifest and explicitly retain its remaining gaps.

## 3. Scientific risks and requested decisions

### Target-label access is the central issue

**FACT:** Authorised diagnostic class means are not valid adaptation state. Audit code used full target labels for error reporting/conditional-shift diagnosis only and generated no classifier output.

**Required lead decision:** What target data are permitted for development, how many candidate looks are allowed, and what will support a final-audit claim? The same pixels cannot become completely unseen merely by new seeds, masks, or filenames. If independent organiser-held-out evaluation is the only untouched route, say so. Do not use full-target statistics from this report as transformation parameters or feature-selection scores.

**Required comparison decision:** Preserve the frozen full-target zero-shot value `.4433`. For few-shot candidates report exact-query RF scores from the saved predictions and matched same-budget P0; do not present a few-shot vs all-target zero-shot subtraction as an equal-condition algorithm gain. No new split/evaluation is created here.

### Source-validation and raw-inference safety

The reference's source scaling before CV is a disclosed reference defect, not a candidate safety pass. Affine positive rescaling is often theoretically immaterial to tree thresholds, but numerical implementation and non-tree metrics need honest fold-local treatment. A candidate layer may use approximate inverse scaling to reconstruct raw feature units and refit inside existing source folds; it must be separately tested and recorded. This does not recover a label-free raw spectral feature function.

A new metric can be tested on cached features only if the lead explicitly approves that limited development scope and does not misrepresent it as passing all submission-safety gates. The operating system's Gate O also requires genuine source adaptation, inference safety, and fixed evaluation contracts; simple baseline acceptance is insufficient permission for optimisation.

### Scientific interpretation risks

- RF class weighting is **already balanced**, despite contradictory organiser prose. Do not propose enabling it as an innovation.
- Madrid repeats are correlated; 25 fold scores are not independent replications and SD is not a confidence interval.
- C1/C2 labels are semantically city-specific. Neither class-centre equality nor pure prior shift is established.
- In-place global target normalisation, query-feature CORAL, and pseudo-label learning require privileges not confirmed in project docs.
- Source impurity importance is not target causal importance; using high source importance alone as proof of transfer robustness is unwarranted.
- The diagram/draft abstract in Member 4's pack describes label-free extraction and source representation as if implemented. They are scaffold aspirations, not verified reference behaviour; request correction before presentation, without modifying that owner's file here.

## 4. Engineering risks from helper/source inspection

**FACT:** `working/member3_artifact_helpers.py` is useful scaffolding, not a complete safety boundary:

- `save_pickle`/`save_json` write in overwrite mode; `ensure_dir` permits existing directories. Candidate runs need approved exclusive creation/manifest semantics to protect immutable state.
- `validate_preprocessed_data` checks dimensions/finite values/class sets, but after collecting a ndim error it still accesses `shape[1]`, which can raise an uncontrolled IndexError on a 1-D input. It does not enforce the exact ordered schema, forbidden label columns, ID uniqueness/content alignment, scaler state, or exact one-dimensional y shape.
- `assert_support_query_disjoint` checks set overlap only; it does not enforce valid index bounds, uniqueness, exhaustiveness, class budgets, or correct city and pixel identities.
- CSV field names are taken from each new row without checking existing header/order; schema drift could silently corrupt a run ledger.
- Source-model bundle does not itself guarantee that scaler/representation/horizon/label intervals are persisted; they must be explicit configuration/state fields.
- Feature-schema JSON was written with sorted dictionary keys. `feature_names` is authoritative; do not concatenate `feat_groups.values()` in incidental JSON key order to infer the 60-column model order.
- The capture runner remains executable and its sidecar writes into frozen baseline paths. No execution occurred here. Future candidate entry points must not import/run its main path or reuse its output directory.

**Narrow recommendation:** Member 3 proposes a separate candidate-only validation/export patch and tests; lead reviews before any candidate run. Do not change helper/reference code during this documentation task.

## 5. Reproducibility and working-tree risks

**FACT:** Audit began on dirty `main` at `165fe11df8779eed514c75bd2852c2b9588a18a4`, with pre-existing Member 1–4 docs, working notebooks/helpers, frozen artifacts, several OneNote indices, and untracked `nul`. No cleanup/staging/commit was performed. Existing whitespace warnings in `docs/member3_log.md` are Markdown hard-break spaces predating the appended audit entry; not cleaned up.

`*.pkl` is ignored; `.npz`/JSON files under the untracked baseline directory may still be stageable. Never `git add .`. Lead should commit narrow code/docs/metadata, preserve large artifacts outside ordinary Git, and capture dirty-code hashes if execution precedes a clean reviewed commit. Read-only attribute protection is local Windows metadata and is not carried by a Git clone; run instructions must mention verification on each machine. The exact external OneNote writer was never conclusively attributed and no process was terminated; do not claim OneDrive/OneNote definitively caused a specific write.

Recommended narrow owner actions (not performed here):

1. **Lead:** Record accepted Notebook 4/recovery milestone in master/decision/team records, current metrics and manifest hashes; preserve historical starter values only as historical.
2. **Lead/evaluation owner:** Decide label-use/development/final-audit and cached-feature safety scope; approve unchanged episode/comparator verification and unique run IDs.
3. **Member 3:** After approval only, implement isolated sampler/validation infrastructure, then request review; never rerun Notebook 4 to fill missing artifacts.
4. **Member 2/3:** Separate candidate-only label-free feature/inference and fold-local scaler safety task, leaving accepted preprocessing untouched.
5. **Member 4:** Update evidence inventory and scaffold claims from lead-approved measured baseline, not starter/current placeholders.
6. **Lead:** Allocate one fixed E1 experiment, allowed files, resource slot and stop rule; backups remain proposals. No autonomous sweep.

## 6. Audit operations and safety

This audit only read existing pickles/NPZs/JSON/notebook sources and computed descriptive confusion, probability, feature-distribution, class-conditional and source-importance summaries. It did not call estimator `.fit`, `.predict`, `.predict_proba`, or `.apply`; did not draw supports or modify seeds; did not install packages, disable security, or remove read-only protection.

Proposed repository changes are limited to:
- `working/gate4_baseline_error_analysis.md` (new)
- `working/gate4_candidate_experiment_plan.md` (new)
- `working/gate4_readiness_audit.md` (new)
- `docs/member3_log.md` (append only)

Temporary text extractions, hash snapshot, audit-only Python calculations and JSON diagnostics reside in the OS temp directory `statsgeeks_gate4_audit/`, not in reference/model code. They contain baseline diagnostics only; they are not candidate metrics or deployment artifacts.

### Final preservation verification

**PASS:** Post-analysis SHA256 comparison found **zero changes among all 32 protected files**, including every frozen baseline payload/manifest and both artifact-directory OneNote indices, all organiser notebooks, raw Parquets, accepted pickle, working reference notebooks, and existing Python helpers/runners. Notebook 4 working/executed cell counts, types, and sources match the organiser; Notebook 3 deviations remain exactly `[2,4,19]`.

`git status --short -- original/` was empty at t=0 and every second through t=10; `git diff --quiet -- original/` passed at every check. Final `git diff -- original/` was empty. `attrib original/Open Notebook.onetoc2` still reports `A R`. No protection was removed or reapplied.

Compared with entry Git status, the only new entries are the three proposed Gate 4 Markdown files; the already-dirty Member 3 log was appended. No candidate code/model/prediction/metric files were created in the repository. Existing unrelated modifications were not restored, cleaned, staged, or committed. No estimator fitting/inference, prototype episode execution, tuning, or reference-runner execution occurred. These preservation checks do not remove the scientific readiness blockers above.

## 7. Exact next authorised action

**Team Lead reviews this documentation package and resolves the explicit readiness decisions.** The next possible implementation authorisation should be a narrow episode/comparator and safety-contract task, followed by one fixed E1 proposal if reviewed. At the end of this audit the modelling agent must STOP: no candidate modelling, tuning, baseline rerun, Notebook 4 execution, or Gate 4 execution is authorised.
