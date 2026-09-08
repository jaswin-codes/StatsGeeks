# Mission

You are Member 1: Team Lead / Integrator. Your purpose is to keep the team scientifically valid, reproducible, and mergeable. You maximise team output by reviewing, coordinating, accepting evidence, resolving blockers, and shaping the presentation narrative. Write as little production code as possible; your value is integration and judgement.

# Success Definition

By the end of Day 1, success means:

- Every member has clear ownership, a task branch, and no file conflicts.
- Original notebooks/raw data remain untouched.
- Baseline status is honestly recorded as reproduced, running, or blocked with evidence.
- All merges are reviewed against `docs/REVIEW_CHECKLIST.md`.
- `MASTER_PLAN.md`, `TEAM_LOG.md`, and important `DECISION_REGISTER.md` entries reflect actual progress only.
- The team has a defensible Day 2 plan, a submission-shaped inventory, and a presentation story with evidence placeholders or verified results.

# Read First

- `docs/AGENTS.md`
- `docs/MASTER_PLAN.md`
- `docs/BASELINE_EXECUTION_PLAN.md`
- `docs/TEAM_OPERATING_SYSTEM.md`
- `docs/DAY1_TIMELINE.md`
- `docs/REVIEW_CHECKLIST.md`

# Files They Own

You may edit:

- `docs/MASTER_PLAN.md`
- `docs/TEAM_LOG.md`
- `docs/DECISION_REGISTER.md`
- `docs/member1_log.md`
- Review/handoff records created under `docs/` if agreed by the team

# Files They May Read

You may inspect:

- All files listed in **Read First**
- Member handoffs/logs: `docs/member1_log.md`, `docs/member2_log.md`, `docs/member3_log.md`, `docs/member4_log.md`
- Proposed PR diffs and owned working-copy files submitted by teammates for review
- Result/evidence files referenced in handoffs

# Files They MUST NOT Modify

Do not modify:

- Organiser notebooks: `1-Introduction.ipynb`, `2-Reading_Data.ipynb`, `3-Preprocessing.ipynb`, `4-Modelling.ipynb`
- Raw data: `madrid_train.parquet`, `amsterdam_data.parquet`
- Historical audit: `docs/Hackathon_Analysis_Report.md`
- Teammates’ owned notebooks/modules unless explicitly taking over after a documented decision
- Large artifacts, model files, caches, environments, or credentials

# Morning Phase

## Objectives

- Start everyone immediately at 09:00 with non-overlapping work.
- Confirm provisional scientific rules: Madrid → Amsterdam, four classes, macro F1, right-inclusive boundaries, support/query separation.
- Assign file ownership and prevent duplicate heavy jobs.
- Prepare review, logging, and integration workflow before results arrive.

## Detailed step-by-step checklist

1. Confirm every member has cloned the agreed repository revision and created a task branch.
2. Re-state each member’s allowed files and forbidden files.
3. Assign Member 2 as the only baseline execution owner.
4. Ask Member 3 to prepare interface/leakage/artifact checks without editing Member 2’s files.
5. Ask Member 4 to prepare slide/evidence scaffolding with placeholders, not invented results.
6. Consolidate organiser questions from existing docs; do not invent new strategy questions.
7. Create or update a compute schedule so only one heavy run owns shared CPU/RAM.
8. Review any setup/path changes from Member 2 before execution.
9. At 11:00, run the interface gate: paths, originals protection, ownership, no algorithm changes.
10. At 12:00–12:30, record Gate L status: passed, blocked, or pending.

## Expected outputs

- Clear member task list and file ownership.
- Morning `TEAM_LOG.md` entry.
- Important provisional decisions in `DECISION_REGISTER.md` if needed.
- Updated `MASTER_PLAN.md` only for actual status changes.
- Review checklist template ready for first handoff.

## Validation checklist

- No two members are editing the same file.
- No original notebook/raw data modification is proposed.
- Baseline work remains faithful except approved path/parent-directory fixes.
- Any score is labelled starter reference, smoke/development, reproduced reference, or final audited.
- Compute status has one owner and a next checkpoint.

## Required documentation updates

- Update `docs/member1_log.md`.
- Integrate concise member updates into `docs/TEAM_LOG.md`.
- Update `docs/DECISION_REGISTER.md` only for consequential decisions.
- Update `docs/MASTER_PLAN.md` only for actual milestone/status changes.

## Git commit checkpoint

Suggested checkpoint: commit reviewed documentation/coordination updates only, e.g. `docs: record day 1 morning coordination`. Do not claim code is reproduced or merged unless reviewed evidence exists.

## Definition of done

Morning is done when all members are productive, file conflicts are prevented, baseline execution status is known, and Gate L is recorded honestly.

# Lunch Checkpoint

Show the Team Lead record itself:

- Who owns each active task and file.
- Whether preprocessing is complete, running, or blocked.
- Evidence location for any completed setup/run check.
- Current blockers and next checkpoint.

Evidence that must exist:

- Updated member logs or concise updates from all members.
- `TEAM_LOG.md` summary.
- Any important decision entries.
- Review status for any proposed merge.

Questions to answer before continuing:

- Is the baseline ready to continue to modelling?
- Is any member idle or duplicating work?
- Are any scientific rules at risk?
- Is candidate modelling authorised yet? If not, keep Member 3 on review/interface tasks.

# Afternoon Phase

## Objectives

- Accept or block baseline evidence using `REVIEW_CHECKLIST.md`.
- Approve candidate transfer work only after reference criteria and safety scope are clear.
- Keep presentation evidence aligned with actual results.
- End Day 1 with a stable checkpoint and Day 2 recovery/experiment plan.

## Step-by-step checklist

1. Review Member 2’s modelling evidence: 25 RF CV fits, final RF, zero-shot, prototype trials, or explicit blocker.
2. Compare outputs against `docs/BASELINE_EXECUTION_PLAN.md` success criteria.
3. Record known reference limitations: global pre-CV scaling, label-dependent features, target-only prototypes, missing exports.
4. If baseline is accepted, authorise exactly one scoped Member 3 candidate task from `MASTER_PLAN.md`.
5. If baseline is not accepted, keep focus on recovery; do not optimise.
6. Use `docs/REVIEW_CHECKLIST.md` for every PR/handoff.
7. Coordinate artifact locations/checksums through logs rather than committing large artifacts.
8. At 16:30, review leakage/inference/source-state evidence for any candidate work.
9. At 17:30, review submission-shaped inventory and missing items.
10. Select at most two Day 2 tasks based on actual evidence.

## Expected outputs

- Reviewed baseline acceptance or blocker record.
- Updated `MASTER_PLAN.md` priorities/status.
- Day 2 task list with dependencies.
- Presentation narrative outline: problem → protocol → baseline → transfer gap → candidate/evidence → limitations.

## Validation

- Reference reproduction is not misrepresented as submission-ready.
- Candidate code, if any, is separate from reference files.
- No query-label tuning, metric change, class-boundary change, or original-file edit is accepted.
- Every merge has a scope, evidence, and known limitations.

## Documentation updates

- `docs/member1_log.md`
- `docs/TEAM_LOG.md`
- `docs/DECISION_REGISTER.md` for important decisions
- `docs/MASTER_PLAN.md` for actual progress and Day 2 priorities
- `docs/EXPERIMENT_LOG.md` only if experiments/runs are reported

## Commit checkpoint

Suggested checkpoint: reviewed docs/integration commit and, only if justified, a clearly named Day 1 checkpoint tag. Do not tag “reproduced baseline” unless the full baseline criteria pass.

## Definition of done

Afternoon is done when main is stable, evidence is reviewed, unfinished checks are explicit, all logs are current, and Day 2 begins with named owners rather than a repository re-audit.

# If You Become Blocked

- If a teammate is blocked on execution: classify as path/data/environment/code/resource and pair for one small fix.
- If a scientific rule is unclear: stop the affected work, record a decision question, and use the provisional safe rule from `MASTER_PLAN.md`.
- If two people need the same file: stop one branch, decide ownership, and record handoff.
- If baseline is incomplete: do not authorise optimisation; keep M3/M4 on independent review/presentation tasks.
- If a merge is risky: request changes; do not merge to satisfy the clock.
- Ask another member when you need independent reload, artifact check, or domain explanation.
- Stop immediately for suspected leakage, original-file modification, data loss, hidden metric change, or uncontrolled heavy job.

# AI Prompt

```text
You are assisting Member 1, the Team Lead / Integrator. Read only the project documentation already assigned for this role: docs/AGENTS.md, docs/MASTER_PLAN.md, docs/BASELINE_EXECUTION_PLAN.md, docs/TEAM_OPERATING_SYSTEM.md, docs/DAY1_TIMELINE.md, and docs/REVIEW_CHECKLIST.md. Do not reread the repository, do not analyse notebooks, do not optimise the ML pipeline, and do not modify production code.

Role: integration, review, validation, logs, merge approval, and presentation narrative. Own only docs/MASTER_PLAN.md, docs/TEAM_LOG.md, docs/DECISION_REGISTER.md, docs/member1_log.md, and review/handoff records. Do not modify organiser notebooks, raw data, historical audit, teammates’ owned files, or large artifacts.

Implement the coordination/documentation updates needed for today: record actual checkpoint status, decisions, blockers, review outcomes, and Day 2 next actions. Use REVIEW_CHECKLIST.md for acceptance. Keep all claims evidence-based and label results as starter reference, smoke/development, reproduced reference, or final audited. Update EXPERIMENT_LOG.md only if a real run/experiment is reported. Suggest clear commit checkpoints, but do not claim a commit/merge happened unless there is evidence.
```