# Mission

You are Member 4: Research & Presentation Engineer. Your purpose is to turn the team’s technical work into reproducible evidence and a judging-ready story. You make sure the team can explain model design, transfer strategy, macro-F1 interpretation, collaboration, limitations, and artifact reproducibility. You do not invent results or change modelling logic.

# Success Definition

By the end of Day 1, success means:

- Slide skeleton exists with placeholders for verified metrics.
- Evidence inventory and reproducibility checklist are current.
- Organiser questions from existing docs are summarised for the Team Lead.
- Baseline/candidate claims are correctly labelled by evidence status.
- Draft abstract/justification structure covers all three rubric pillars.
- Each member has a speaking role and contribution evidence.

# Read First

- `docs/AGENTS.md`
- `docs/MASTER_PLAN.md`
- `docs/Hackathon_Analysis_Report.md`
- `docs/BASELINE_EXECUTION_PLAN.md`
- `docs/TEAM_OPERATING_SYSTEM.md`
- `docs/DAY1_TIMELINE.md`
- `docs/REVIEW_CHECKLIST.md`

# Files They Own

You may edit after Team Lead confirms paths:

- `docs/member4_log.md`
- Presentation outline/draft files assigned to you
- Reproducibility/run-instruction draft files assigned to you
- Evidence inventory/checklist files assigned to you
- Proposed concise shared-log text for Team Lead integration

# Files They May Read

You may inspect:

- All files listed in **Read First**
- Member handoffs/log summaries shared by the Team Lead
- Verified run evidence, result tables, figures, and artifact metadata
- Review outcomes needed for presentation claims

# Files They MUST NOT Modify

Do not modify:

- Organiser notebooks or raw data
- Member 2 baseline working copies
- Member 3 candidate implementation files
- `docs/MASTER_PLAN.md`, `docs/TEAM_LOG.md`, or `docs/DECISION_REGISTER.md` directly unless Team Lead assigns a specific entry
- Metrics, model outputs, experiment logs, or result files produced by others except by reviewed handoff
- Any slide/justification claim that contradicts verified evidence

# Morning Phase

## Objectives

- Build presentation and reproducibility scaffolding while technical runs proceed.
- Prepare judge-facing evidence without depending on results being ready.
- Keep documentation honest and beginner-friendly.

## Detailed step-by-step checklist

1. Create/update `docs/member4_log.md` with goals and allowed files.
2. Extract organiser clarification questions already listed in the docs and summarise for the Team Lead.
3. Create a slide skeleton with sections:
   - problem and urban relevance,
   - data/classes/domain shift,
   - baseline protocol,
   - transfer gap,
   - candidate method placeholder,
   - results table placeholder,
   - F1 versus log2 sample size placeholder,
   - limitations and reproducibility,
   - team contributions.
4. Draft first-slide abstract placeholder ≤150 words, clearly marked draft.
5. Draft written-justification outline ≤300 words target with three pillars:
   - model design,
   - transfer strategy,
   - F1 interpretation.
6. Build evidence inventory template:
   - result source,
   - evidence status,
   - commit/branch,
   - artifact path/checksum,
   - owner,
   - reviewer,
   - limitations.
7. Prepare clean-session/reload checklist to support Team Lead review.
8. Do not add final numbers unless handed off as verified.
9. Record open evidence requests for Member 2 and Member 3.

## Expected outputs

- Slide skeleton or outline.
- Evidence inventory template.
- Organiser question summary for Team Lead.
- Draft abstract/justification outline.
- `docs/member4_log.md` update.

## Validation checklist

- No invented results.
- Starter-reference scores are labelled as starter reference unless reproduced.
- The deck covers 30/40/30 rubric priorities.
- All four members have planned speaking roles.
- Limitations and leakage controls are included.

## Required documentation updates

- Update `docs/member4_log.md`.
- Send concise summary to Team Lead for `TEAM_LOG.md`.
- Send important organiser/decision questions to Team Lead.
- Do not update `EXPERIMENT_LOG.md` unless helping format verified run information from the run owner.

## Git commit checkpoint

Suggested checkpoint: `docs: add presentation and evidence scaffold` if files are assigned and reviewed. Do not commit generated decks if the Team Lead wants another storage location.

## Definition of done

Morning is done when presentation/reproducibility work can absorb verified results immediately without waiting for new planning.

# Lunch Checkpoint

Show the Team Lead:

- Slide skeleton.
- Evidence inventory template.
- Abstract/justification draft structure.
- Organiser question summary.
- Missing evidence list for Members 2 and 3.

Evidence that must exist:

- `docs/member4_log.md` update.
- Draft files or outline at assigned paths.
- Clear labels for placeholders versus verified evidence.

Questions to answer before continuing:

- Which baseline evidence is verified, pending, or blocked?
- What candidate story is authorised, if any?
- What exact results/figures are needed by 17:30?
- Who will speak to each slide section?

# Afternoon Phase

## Objectives

- Convert verified technical outputs into presentation evidence.
- Support independent reproducibility checks without modifying model logic.
- Prepare submission-shaped package inventory and Day 2 presentation priorities.

## Step-by-step checklist

1. Receive verified baseline/candidate evidence only through Team Lead or owner handoff.
2. Update slide placeholders with verified status labels.
3. Prepare results table structure for:
   - Madrid CV macro F1 mean/std,
   - Amsterdam budgets 5, 25, 50, 100, 200,
   - optional 10-shot diagnostic clearly labelled.
4. Prepare learning-curve figure specification: macro F1 vs log2 support size, mean/std, trial counts.
5. Draft narrative for baseline limitations:
   - reference prototypes are target-only,
   - label-free inference and saved source-state checks are required for submission,
   - support/query separation matters.
6. If authorised, independently follow reload/inference instructions and record pass/fail without changing code.
7. Maintain submission inventory: models, preprocessing, adaptation code, results, deck, justification, backups.
8. Ensure all four members can explain their contribution and one limitation.
9. Produce concise missing-item list for the Team Lead at 17:30.
10. Do not polish false claims; use honest pending/blocker language.

## Expected outputs

- Evidence-linked slide draft.
- Draft justification text or bullet outline.
- Submission inventory with missing items.
- Reproducibility checklist status.
- Speaking-role plan.

## Validation

- Every number in slides links to verified evidence or is marked placeholder/reference.
- Standard deviation is not called confidence interval.
- Confusion-matrix rows are not described as F1.
- Presentation includes originality/insightful-failure angle without overclaiming.
- Offline/back-up requirements are tracked.

## Documentation updates

- `docs/member4_log.md`
- Proposed `TEAM_LOG.md` update to Team Lead
- Evidence inventory
- Presentation/justification drafts
- Experiment-log formatting only when based on run-owner evidence

## Commit checkpoint

Suggested checkpoint: `docs: draft day 1 presentation evidence` or assigned deck commit. Commit only reviewed lightweight docs unless the Team Lead instructs otherwise.

## Definition of done

Afternoon is done when the team has a clear evidence-based story, a package inventory, and a Day 2 list of missing presentation/reproducibility items.

# If You Become Blocked

- Missing results: keep placeholders; ask the responsible owner through Team Lead.
- Conflicting numbers: stop using them; ask Team Lead to resolve evidence status.
- Unclear organiser requirement: use existing question list and ask Team Lead to escalate.
- Asked to edit model/baseline files: decline and request a handoff/review role instead.
- Deck too crowded: prioritise problem, transfer, macro F1 curve, reproducibility, limitations, team roles.
- Ask Member 2 for baseline evidence and limitations.
- Ask Member 3 for transfer-method explanation and artifact status.
- Stop immediately if a presentation claim would imply unverified results, hidden-test performance, or global portability.

# AI Prompt

```text
You are assisting Member 4, the Research & Presentation Engineer. Read only the assigned documentation: docs/AGENTS.md, docs/MASTER_PLAN.md, docs/Hackathon_Analysis_Report.md, docs/BASELINE_EXECUTION_PLAN.md, docs/TEAM_OPERATING_SYSTEM.md, docs/DAY1_TIMELINE.md, and docs/REVIEW_CHECKLIST.md. Do not reread the repository, do not analyse notebooks again, do not modify project code, and do not optimise the ML pipeline.

Role: create presentation/reproducibility/evidence materials in assigned files only. Own docs/member4_log.md and Team-Lead-approved presentation, justification, evidence-inventory, and run-instruction drafts. Do not modify organiser notebooks, raw data, baseline/candidate implementation files, shared logs directly unless assigned, or any metrics generated by others.

Implement documentation/presentation outputs now: slide skeleton, evidence inventory, organiser-question summary, reproducibility checklist, abstract/justification draft structure, speaking-role plan, and missing-evidence list. Use placeholders for unverified results. Label all claims as starter reference, smoke/development, reproduced reference, or final audited. Validate word limits, rubric pillars, macro-F1 interpretation, standard deviation wording, and all-four-member contribution evidence. Suggest a docs commit only after review.
```