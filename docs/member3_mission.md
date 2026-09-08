# Mission

You are Member 3: Modelling Engineer. Your purpose is to build the authorised transfer candidate after the reference baseline is accepted or explicitly handed off. Before that, you keep moving by preparing interface, leakage, inference, artifact, and validation checks. Your work must prove genuine Madrid source-state reuse, not just Amsterdam target-only fitting.

# Success Definition

By the end of Day 1, success means:

- You have not interfered with Member 2’s baseline files.
- You have a clear candidate interface/checklist ready before lunch.
- If authorised after baseline handoff, you have a separate candidate implementation or work-in-progress with explicit source-state path, support/query separation, and artifact/reload plan.
- Any experiment is logged with hypothesis, configuration, seeds, evidence, and limitations.
- If candidate implementation is not authorised, you have still contributed review evidence and a Day 2 implementation plan.

# Read First

- `docs/AGENTS.md`
- `docs/MASTER_PLAN.md`
- `docs/BASELINE_EXECUTION_PLAN.md`
- `docs/TEAM_OPERATING_SYSTEM.md`
- `docs/DAY1_TIMELINE.md`
- `docs/REVIEW_CHECKLIST.md`

# Files They Own

You may edit only after Team Lead confirmation:

- `docs/member3_log.md`
- Your candidate modelling/adaptation working copy or helper files at Team-Lead-approved paths
- Candidate experiment records assigned to you
- Candidate artifact configuration metadata assigned to you

# Files They May Read

You may inspect:

- All files listed in **Read First**
- Member 2 handoff/evidence after Team Lead shares it
- Approved feature schema/artifact metadata
- Your own candidate files and review comments
- Result logs needed for matched comparison

# Files They MUST NOT Modify

Do not modify:

- Organiser notebooks or raw data
- Member 2 reference baseline working copies
- `docs/MASTER_PLAN.md`, `docs/TEAM_LOG.md`, or `docs/DECISION_REGISTER.md` directly unless assigned by the Team Lead
- Member 4 presentation/deck files unless asked for a small text contribution
- Shared split/episode definitions, labels, class boundaries, metric, budgets, dependencies, or feature contract without Team Lead decision

# Morning Phase

## Objectives

- Stay productive while baseline runs.
- Define how a valid transfer candidate must consume Madrid-learned state.
- Prepare checks that prevent leakage and artifact failures.

## Detailed step-by-step checklist

1. Create/update `docs/member3_log.md` with your branch, task, and stop conditions.
2. Read the baseline plan and identify what Member 2 must hand off before candidate work starts.
3. Draft an interface checklist:
   - source artifact input,
   - feature schema input,
   - support features/labels input,
   - query features without labels,
   - configurable budget and seed,
   - prediction output,
   - evaluation output separated from adaptation.
4. Draft leakage checks:
   - no `weighted_mean_year` or `age_class` in predictive inputs,
   - no query labels in fitting/tuning,
   - support/query IDs disjoint,
   - source state immutable during adaptation,
   - fold-local learned transforms for candidate/submission code.
5. Draft artifact checks:
   - save source preprocessing/representation/model,
   - save ordered feature schema, class config, horizon, seeds,
   - reload and run inference without label fields.
6. Review Member 2’s feature contract when available, but do not edit their files.
7. Prepare a scoped candidate task proposal for Team Lead approval.
8. Do not start model optimisation before explicit authorisation.

## Expected outputs

- Candidate interface/leakage/artifact checklist.
- Short candidate task proposal grounded in `MASTER_PLAN.md`.
- `docs/member3_log.md` update.
- Questions/blockers for Team Lead.

## Validation checklist

- No reference files modified.
- Candidate proposal compares against raw target prototypes and uses matched episodes.
- Candidate is simple enough for Day 1/Day 2 integration.
- No unapproved dependencies or external data.

## Required documentation updates

- Update `docs/member3_log.md`.
- Send concise status to Team Lead for `TEAM_LOG.md`.
- Send important decision request to Team Lead if candidate scope needs approval.

## Git commit checkpoint

Suggested checkpoint: `docs: add modelling interface checklist` if the Team Lead assigns a docs file. Otherwise keep notes in your member log and do not commit unassigned files.

## Definition of done

Morning is done when you can immediately implement a safe candidate after handoff, without waiting to rediscover requirements.

# Lunch Checkpoint

Show the Team Lead:

- Your interface checklist.
- Your leakage/artifact checklist.
- Exact baseline handoff items you need from Member 2.
- Candidate task proposal and stop conditions.

Evidence that must exist:

- `docs/member3_log.md` update.
- A written checklist or handoff request.
- No modifications to Member 2 reference files.

Questions to answer before continuing:

- Has the baseline contract been accepted or is it still pending?
- Are you authorised to implement candidate code now?
- Which exact files do you own for candidate implementation?
- What comparison baseline and episodes must be reused?

# Afternoon Phase

## Objectives

- If authorised, implement a separate, minimal valid transfer candidate.
- If not authorised, support baseline recovery and review without editing reference files.
- Produce evidence for judging: genuine transfer mechanics, controlled comparison, limitations.

## Step-by-step checklist

1. Wait for Team Lead authorisation and exact owned file paths.
2. Start from accepted feature/schema handoff; do not alter baseline artifacts.
3. Implement or prepare candidate path that:
   - trains source representation/model on Madrid only,
   - freezes source state for Amsterdam episodes,
   - computes Amsterdam support prototypes or simple target head using support labels only,
   - predicts query labels without query-label access,
   - supports budgets 5, 25, 50, 100, 200 per class.
4. Keep raw target prototypes as the required comparison.
5. Use deterministic seeds and matched episode IDs where available.
6. Save configuration and source artifact metadata; do not overwrite source artifact during adaptation.
7. Validate label-free inference path where implemented.
8. Run only approved smoke/development checks if full experiments are not authorised.
9. Record failures as useful evidence, not hidden mistakes.
10. Request Team Lead review using `docs/REVIEW_CHECKLIST.md`.

## Expected outputs

Depending on authorisation:

- Candidate implementation/checkpoint in owned files, or
- Reviewed interface/recovery support notes.

If experiments run:

- Per-budget macro F1 mean/std with trial counts.
- Comparison to raw target prototypes.
- Source-state/reload/inference evidence.

## Validation

- Madrid-only source training.
- Amsterdam adaptation uses only support labels.
- Query labels are evaluation-only.
- Feature schema/order preserved.
- Source artifact immutable.
- No hidden metric/budget/class changes.
- Failures and pending checks clearly labelled.

## Documentation updates

- `docs/member3_log.md`
- Experiment record if any run occurs
- Proposed `TEAM_LOG.md` update to Team Lead
- Decision request if candidate scope or protocol changes
- Handoff to Member 4 explaining model design, transfer strategy, and limitations

## Commit checkpoint

Suggested checkpoint after scoped validation: `model: add source-state adaptation candidate` or `docs: record modelling candidate blocker`. Commit only owned files and lightweight metadata; exclude large models/artifacts.

## Definition of done

Afternoon is done when your candidate/review contribution is safe to integrate or explicitly blocked, with evidence and next action clear.

# If You Become Blocked

- Missing baseline handoff: do not improvise; ask Team Lead and continue documentation/review tasks.
- Unsure if query labels are being used: stop and ask Team Lead immediately.
- Candidate needs new dependency: stop and request approval with reason and fallback.
- Feature schema mismatch: stop downstream modelling; ask Member 2 and Team Lead.
- Results look good but validation is incomplete: label them smoke/development only.
- Ask Member 2 for feature contract clarification.
- Ask Member 4 for presentation wording/evidence needs.
- Stop if you would need to edit reference files, change labels/metrics/budgets, or tune on final query scores.

# AI Prompt

```text
You are assisting Member 3, the Modelling Engineer. Read only the assigned documentation: docs/AGENTS.md, docs/MASTER_PLAN.md, docs/BASELINE_EXECUTION_PLAN.md, docs/TEAM_OPERATING_SYSTEM.md, docs/DAY1_TIMELINE.md, and docs/REVIEW_CHECKLIST.md. Do not reread the repository, do not analyse notebooks again, do not modify original notebooks/raw data, and do not optimise the baseline pipeline.

Role: implement only Team-Lead-authorised candidate modelling/adaptation in owned candidate files, or prepare interface/leakage/artifact checks if candidate coding is not yet authorised. Do not edit Member 2 reference files. Preserve four classes, Madrid to Amsterdam direction, macro F1, right-inclusive boundaries, fixed seeds, required budgets, and support/query separation.

Implementation goal when authorised: create a minimal valid source-learned transfer path. Train source state on Madrid only, freeze it, adapt to Amsterdam using support labels only, predict query data without query labels, compare against raw target prototypes on matched episodes, save/reload source state/config/schema metadata where affected, and validate label-free inference. Update docs/member3_log.md and experiment records for any run. Suggest a scoped commit only after validation; do not commit large artifacts.
```