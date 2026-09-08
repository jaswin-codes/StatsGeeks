# Mission

You are Member 2: Baseline Engineer. Your purpose is to produce faithful, reproducible baseline evidence and a clean handoff for downstream modelling. You do not optimise. You protect the reference path so the team can compare future work fairly and explain what is reproduced versus only starter-reference output.

# Success Definition

By the end of Day 1, success means:

- Working-copy baseline setup is reviewed and uses only minimum path/parent-directory fixes.
- Original notebooks and raw data remain unchanged.
- Preprocessing status is evidenced: feature pickle complete/reloadable or blocker documented.
- Modelling status is evidenced: full reference run complete or exact remaining work documented.
- Feature/schema/label/pixel alignment checks are recorded.
- Baseline limitations are documented without trying to fix them inside the reference run.

# Read First

- `docs/AGENTS.md`
- `docs/MASTER_PLAN.md`
- `docs/BASELINE_EXECUTION_PLAN.md`
- `docs/TEAM_OPERATING_SYSTEM.md`
- `docs/DAY1_TIMELINE.md`
- `docs/REVIEW_CHECKLIST.md`

# Files They Own

You may edit only files assigned by the Team Lead, expected to include:

- `docs/member2_log.md`
- Your reference working-copy Notebook 3, with the exact path confirmed by the Team Lead
- Your reference working-copy Notebook 4, with the exact path confirmed by the Team Lead
- Baseline run/evidence notes under `docs/` if assigned

# Files They May Read

You may inspect:

- All files listed in **Read First**
- Organiser notebooks as read-only references
- Raw Parquet files only through the authorised baseline execution path
- Your own generated baseline artifacts and logs
- Team Lead review comments and handoff requests

# Files They MUST NOT Modify

Do not modify:

- Organiser notebooks: `1-Introduction.ipynb`, `2-Reading_Data.ipynb`, `3-Preprocessing.ipynb`, `4-Modelling.ipynb`
- Raw data: `madrid_train.parquet`, `amsterdam_data.parquet`
- `docs/MASTER_PLAN.md`, `docs/TEAM_LOG.md`, or `docs/DECISION_REGISTER.md` directly unless the Team Lead explicitly assigns a small entry
- Member 3 candidate files or Member 4 presentation files
- Model hyperparameters, features, QA logic, scaling protocol, labels, metrics, budgets, or trial counts during reference reproduction

# Morning Phase

## Objectives

- Prepare the faithful baseline run without method changes.
- Verify inputs, paths, labels, feature schema, and reloadability.
- Give the Team Lead clear evidence, not vague “works for me” status.

## Detailed step-by-step checklist

1. Start from the agreed branch and confirm your owned working-copy paths with the Team Lead.
2. Copy or use only lead-approved working copies; never save over organiser originals.
3. Apply only minimum portable path and parent-directory handling needed to run the reference baseline.
4. Record every deviation from the organiser notebooks.
5. Confirm raw input paths resolve through the approved procedure.
6. Run preprocessing only when the Team Lead confirms resource ownership.
7. Validate expected feature contract if preprocessing completes:
   - 60 ordered features.
   - Madrid `(76263, 60)` expected reference shape.
   - Amsterdam `(25992, 60)` expected reference shape.
   - Four classes in each label vector.
   - Pixel keys align with rows.
   - Feature matrices finite/no NaNs.
   - Pickle reloads in a clean session.
8. Capture environment/package versions, seed settings, runtime notes, and artifact location.
9. If preprocessing is still running or blocked, record exact progress/error evidence.
10. Prepare a handoff note for Member 3 and Member 4 through the Team Lead.

## Expected outputs

- Reviewed baseline setup diff.
- Deviation list.
- Preprocessing artifact location or blocker.
- Schema/reload validation evidence.
- `docs/member2_log.md` update.

## Validation checklist

- No algorithm/QA/feature/scaling/model changes.
- Original files untouched.
- Artifact is not committed if large; location/checksum recorded instead.
- Any run status is labelled correctly: pending, smoke/development, or reproduced reference.

## Required documentation updates

- Update `docs/member2_log.md`.
- Send concise TEAM_LOG text to the Team Lead.
- Send decision-worthy issues to the Team Lead for `DECISION_REGISTER.md`.
- Create/update `docs/EXPERIMENT_LOG.md` only if the Team Lead assigns baseline run logging there.

## Git commit checkpoint

Suggested checkpoint after review: `baseline: add portable reference setup` or `docs: record baseline preprocessing evidence`. Do not commit raw data, generated pickle, environments, or large outputs.

## Definition of done

Morning is done when preprocessing is either validated/reloadable or honestly blocked/running, with evidence and next action clear.

# Lunch Checkpoint

Show the Team Lead:

- Your branch and files changed.
- Exact deviations from reference notebooks.
- Preprocessing artifact path/checksum if complete.
- Feature/schema/reload checklist results.
- Any errors, warnings, runtime/memory observations.

Evidence that must exist:

- Setup diff or explanation.
- Log entry in `docs/member2_log.md`.
- Artifact/reload evidence or error trace/status note.

Questions to answer before continuing:

- Is Notebook 4 ready to run from a clean start?
- Are all baseline settings still faithful?
- Is any output large and therefore excluded from Git?
- What does Member 3 need from your handoff?

# Afternoon Phase

## Objectives

- Run or continue the faithful reference modelling workflow.
- Capture Madrid CV, final RF, zero-shot, and prototype baseline evidence.
- Compare reproduced results to starter references without hiding discrepancies.
- Preserve a stable reference for future candidate comparisons.

## Step-by-step checklist

1. Launch Notebook 4 reference copy only after validated pickle exists.
2. Use unchanged reference settings:
   - 500-tree balanced RF.
   - 5 folds × 5 repeats Madrid CV.
   - Final Madrid RF.
   - Amsterdam zero-shot.
   - Prototype trials at 5, 10 diagnostic, 25, 50, 100, 200 shots/class.
3. Capture actual completed fit/trial counts.
4. Do not reduce parameters secretly to finish faster.
5. Compare outputs to starter-reference values from the plan.
6. Document discrepancies, seeds, versions, and warnings.
7. Explicitly record known reference deficiencies:
   - scaling fitted before CV,
   - label-dependent feature construction,
   - prototypes are target-only in Madrid-scaled raw feature space,
   - no saved final RF/adaptation artifact.
8. Provide feature/result handoff to Team Lead, Member 3, and Member 4.
9. Request review using `docs/REVIEW_CHECKLIST.md`.
10. If blocked, record exact recovery task for Day 2.

## Expected outputs

- Baseline modelling evidence or precise blocker.
- Reference score table if completed.
- Run configuration/version/seed record.
- Handoff for feature contract and result interpretation.

## Validation

- Full baseline acceptance requires actual clean run completion, not notebook screenshots alone.
- Macro F1 remains the metric.
- Support/query masks are disjoint in prototype evaluation.
- 10-shot is clearly labelled diagnostic.
- Results are not claimed as hidden-test or final audited evidence.

## Documentation updates

- `docs/member2_log.md`
- Proposed concise `TEAM_LOG.md` update to Team Lead
- Experiment/run entry if assigned
- Handoff notes with artifact paths/checksums and limitations

## Commit checkpoint

Suggested checkpoint after review: `baseline: record reproduced reference evidence` only if the full run passes. Otherwise commit as `docs: record baseline blocker` or keep work pending honestly.

## Definition of done

Afternoon is done when the baseline is accepted or blocked with exact evidence, and downstream members know what is safe to use.

# If You Become Blocked

- Path/data missing: stop, record exact path/error, ask Team Lead.
- Environment/package error: record versions/error, ask Team Lead before installing anything.
- Runtime too long: report progress; do not downsize the run without approval.
- Notebook wants to modify an original: stop immediately.
- Any temptation to fix QA/features/model protocol: stop; that belongs to a later authorised task.
- Ask Member 3 only for interface/checklist review, not for edits to your reference files.
- Ask Member 4 for evidence packaging support, not result interpretation beyond verified outputs.
- Stop immediately for suspected leakage changes, metric changes, class-boundary changes, or data/artifact overwrite risk.

# AI Prompt

```text
You are assisting Member 2, the Baseline Engineer. Read only the assigned documentation: docs/AGENTS.md, docs/MASTER_PLAN.md, docs/BASELINE_EXECUTION_PLAN.md, docs/TEAM_OPERATING_SYSTEM.md, docs/DAY1_TIMELINE.md, and docs/REVIEW_CHECKLIST.md. Do not reread the full repository, do not analyse notebooks beyond the assigned working copies, do not optimise the ML pipeline, and do not modify original organiser notebooks or raw data.

Role: faithful baseline reproduction and evidence. Own only docs/member2_log.md and the Team-Lead-approved reference working copies of Notebook 3 and Notebook 4. Allowed implementation: minimum portable path/parent-directory fixes required to run the reference baseline. Forbidden: changing features, labels, QA logic, interpolation, scaling protocol, model hyperparameters, budgets, metric, trial counts, or candidate transfer code.

Implement the requested baseline setup/run support in the owned working copies only. Record deviations, seeds, environment, artifact paths, and validation results. Validate 60-feature schema, expected shapes, labels/classes, pixel alignment, finite features, pickle reload, and full Notebook 4 reference outputs if run. Update docs/member2_log.md and prepare a concise handoff for the Team Lead. Do not commit large data/artifacts; suggest a commit only for reviewed code/docs.
```