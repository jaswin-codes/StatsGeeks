# Team Philosophy

**Purpose:** Help one experienced lead and three first-time hackathon participants deliver a valid, reproducible, well-explained submission over two build days, followed by Thursday's presentation. Everyone uses AI; humans own decisions, checks, and claims.

**Basis:** Only `docs/Hackathon_Analysis_Report.md`, `docs/MASTER_PLAN.md`, `docs/AGENTS.md`, and `docs/BASELINE_EXECUTION_PLAN.md`. This document defines team procedures, not new competition rules or a new ML strategy. No runs, implementations, merges, or organiser answers are asserted as completed.

1. **Reproduce before changing.** Follow the baseline execution plan without algorithm changes. Separate faithful reference reproduction from subsequent authorised correctness/transfer work.
2. **Protect the submission before chasing improvements.** Judging is 30 points understanding/transfer, 40 originality, and 30 presentation/collaboration. Evidence and insightful failures matter alongside macro F1.
3. **One owner, one small task, one verifiable handoff.** Beginners should never have to guess which file to edit or what success means.
4. **AI proposes; a named person verifies.** Nobody merges code they cannot explain. Never turn an AI prediction or saved starter score into a claimed run result.
5. **Keep the original safe.** Raw data and organiser notebooks are immutable. Existing user work and historical evidence are preserved.
6. **Say “blocked” early.** A documented problem is manageable; a hidden problem becomes an integration failure.
7. **All four contribute and speak.** Every member should explain the goal, their work, its evidence, and one limitation.
8. **Do not change the scientific contract silently.** Madrid → Amsterdam, four classes, macro F1, existing right-inclusive boundaries, controlled support/query labels, explicit seeds.

The master plan owns technical direction and current status. The baseline plan owns reference reproduction. `AGENTS.md` owns assistant safeguards. This operating system owns coordination. Conflicts go to the lead and `DECISION_REGISTER.md`; they are not silently resolved by an AI assistant.

# Repository Structure

## Documented layout and ownership

The historical audit/master plan describe a flat snapshot; the baseline execution plan describes `original/` and `data/`. Use the latter as the documented operating layout, without claiming a fresh filesystem inspection. Folder names marked **planned** are operating conventions to confirm before any authorised setup; this documentation task does not create, move, or inspect those folders.

| Folder/location | Purpose | Accountable owner | Boundaries |
|---|---|---|---|
| Repository root | GitHub integration point and portable project configuration | Team Lead | Everyone clones the same repository; lead approves shared configuration and dependency changes |
| `original/` | Four organiser notebooks | Team Lead, preservation custodian | Read-only for everyone, including AI; never rerun/save originals to change outputs |
| `data/` | `madrid_train.parquet`, `amsterdam_data.parquet` | Baseline Engineer, data custodian | Raw files immutable; a clone does not guarantee large data are available; use the lead-confirmed data-access procedure, not guessed downloads |
| `data/preprocessed/` | Reference `preprocessed_data.pkl` and documented feature artifacts | Baseline Engineer | Generated artifacts are not ordinary Git content; preserve baseline versions and label/schema alignment |
| `docs/` | Plans, rules, decisions, diary, member logs, handoffs, reviews | Team Lead for integration; each member for their own log | Historical audit remains unchanged; shared documents use the coordination contract below |
| `notebooks/` — planned working-copy location | Team copies of required Notebooks 3 and 4; optional EDA copy only if assigned | Baseline Engineer for reference copies; Modelling Engineer for separately named authorised candidates | Confirm location before copying; baseline and candidate must not overwrite each other; one named editor per file |
| Reusable helper location — planned, path not yet agreed | Shared transformation/training logic when authorised by master plan | Modelling Engineer; lead approves interfaces | No folder/framework invention during reference reproduction; record path before creation |
| Result/figure/model/submission locations — planned, paths not yet agreed | Versioned run evidence, saved models/preprocessing, final figures and deck | Producer owns run artifacts; Research & Presentation Engineer owns presentation package; lead owns release | Record actual paths in handoffs and run logs; no assumption these artifacts already exist; no large models/caches in ordinary Git |
| Local environment and backup locations — not shared source folders | Tested environment and safe copies of release artifacts | Each member locally; lead coordinates | Never commit environments, secrets, or credentials; confirm backup access before server shutdown |

No other folders can be established from the four source documents. If the cloned layout differs, report the specific path mismatch and let the lead update the living plan; do not reorganise the repository speculatively.

## Document ownership

- Lead owns `MASTER_PLAN.md`, `DECISION_REGISTER.md`, `TEAM_LOG.md`, gate acceptance, and shared schedule changes.
- Members own `member1_log.md` through `member4_log.md` respectively.
- Research & Presentation Engineer prepares concise shared-log/decision updates for lead acceptance and owns presentation evidence curation.
- The author fills a handoff and review request; the receiver/reviewer adds acceptance evidence.
- Do not have multiple AI sessions editing the same shared document at once. Submit a short proposed entry through the PR/handoff; the lead integrates it.

# Team Roles

## Member 1 — Team Lead

**Name:** ____________________

**Owns:** Integration, project management, evaluation contract, task assignments, scope control, organiser clarification, merge/release decisions, shared compute schedule.

**Responsibilities:**

- Give each beginner an allowed file list, expected output, validation checklist, timebox, and dependency owner.
- Resolve folder and environment assumptions after cloning; assign one heavy baseline run rather than four duplicate runs.
- Maintain fixed label/metric/split rules and distinguish baseline-reference defects from submission requirements.
- Review AI-generated changes and scientific claims; pair with a member on risky code rather than taking over all work.
- Record decisions, reserve final audit evaluation, approve transitions through quality gates, and package the release.

**Must not:** Silently rewrite a member's work, change class boundaries, hide failed checks, or approve own technical changes without another member checking evidence.

**Handoffs:** Accept baseline evidence from Member 2; assign authorised candidate work to Member 3; release verified results to Member 4.

**Presentation:** Problem, validation, integration, conclusions; facilitate Q&A.

## Member 2 — Baseline Engineer

**Name:** ____________________

**Owns:** Reference working copies of Notebooks 3 and 4, raw-data access checks, portable baseline execution, feature pickle, run evidence.

**Responsibilities:**

- Follow `BASELINE_EXECUTION_PLAN.md` exactly for the first reference run: only minimum path/parent-directory handling, recorded as deviations.
- Run preprocessing once when execution is authorised; verify 60-feature schema, pixel dimensions, labels, and reloadability.
- Run the unchanged reference modelling logic in a clean kernel: 25 RF CV fits, final source RF, zero-shot, and ten prototype trials at 5/10/25/50/100/200 shots.
- Capture output, versions, seeds, resource use, discrepancies, and known scientific limitations.
- Provide a reproducible handoff, not just “it worked.”

**Must not:** Tune RF parameters, add features, change QA/interpolation/scaling, fix methodological defects inside the reference experiment, or claim prototypes are genuine supervised transfer.

**Handoffs:** Feature contract and reference evidence to lead/Member 3; validated figures/results to Member 4. Later feature changes require an explicitly assigned separate candidate task.

**Presentation:** Data and baseline pipeline, reproducibility, observed limitations.

## Member 3 — Modelling Engineer

**Name:** ____________________

**Owns:** Candidate model/adaptation work only after authorisation; interface tests, explicit artifact saving/reloading, assigned correctness/transfer changes from the master plan.

**Responsibilities:**

- Before baseline acceptance, prepare the interface, leakage, inference, and artifact checklist from existing documentation; do not race the baseline owner or start an algorithm sweep.
- Use separate candidate copies and the approved versioned feature contract after handoff.
- Implement only the source-learned transfer direction already in the master plan, under a scoped lead-approved task.
- Keep support/query separation, fold-local learned transforms, saved source state, and label-free inference explicit.
- Record controlled comparisons, including raw target prototypes, and preserve failures.

**Must not:** Edit reference copies, raw data, class boundaries, shared evaluation splits, or dependencies without lead agreement; use query labels for fitting/tuning; optimise the baseline during reference reproduction.

**Handoffs:** Candidate artifacts, configuration, tests, and results to the lead; explanation and ablation evidence to Member 4.

**Presentation:** Existing approved model/transfer mechanics and evidence; no unsupported claims.

## Member 4 — Research & Presentation Engineer

**Name:** ____________________

**Owns:** Evidence curation, presentation/justification drafts, reproducibility instructions, rubric checklist, concise proposed shared-log updates.

**Responsibilities:**

- Extract unanswered organiser questions from the existing plan; send through the lead.
- Build the story and slide skeleton immediately, with placeholders rather than invented results.
- Track model design, transfer strategy, and F1 interpretation in both slides and justification.
- Help independently replay documented loading/inference checks when execution is authorised, without changing model logic.
- Ensure abstract ≤150 words, justification ≤300 words provisionally, results table/error bars, log2 budget curve, and all four speaking roles.
- Research only lead-approved clarification needs already listed in the plan; no new ML strategy or unapproved external data.

**Must not:** Select a model from query scores, alter metrics to fit a narrative, edit another member's notebook, or treat a screenshot without run provenance as final evidence.

**Handoffs:** Draft documentation and compliance findings to lead; requests for missing evidence to the responsible producer.

**Presentation:** Results interpretation, scientific lessons, reproducibility and practical limits.

# Daily Workflow

All times are local team planning targets, not organiser-confirmed deadlines. Use 09:00–18:00 build days from the existing schedule, lunch 12:30–13:00, and confirm Thursday's presentation time. A missed gate changes the plan; it never authorises skipping validation.

## Start-of-task routine for everyone

1. Begin from the agreed stable `main` revision in your clone; use your own task branch.
2. Read current master plan and agent rules; read only the assigned plan/files next.
3. State task, allowed files, expected evidence, and stop condition to your AI assistant.
4. Ask for small changes and an explanation; inspect the diff before any authorised execution.
5. Record result or blocker in your member log; request review using the handoff and review templates.
6. Never claim committed, tested, or merged status without the corresponding evidence.

## Day 1 — Morning Phase (before lunch, 09:00–12:30)

**Objectives**

- Confirm everyone has cloned GitHub, can identify originals versus working files, understands their branch, and has a named task.
- Agree paths, data access, environment, seeds, baseline deviation policy, and shared compute ownership.
- Start faithful preprocessing/reference execution; no feature or model optimisation.
- Build the review checklist, organiser question list, and slide skeleton in parallel.

**Deliverables**

- M1: task/file ownership, decision entries for provisional rules, compute schedule, evaluation checklist.
- M2: reference copies with documented minimum execution fixes; input/label/schema checks; reloadable pickle if run finishes.
- M3: candidate interface and leakage/inference review notes; independent review of feature contract, no premature modelling changes.
- M4: environment/evidence checklist, organiser questions, slide outline, morning contribution record.

**Validation checkpoint**

- 11:00: interfaces and responsibilities agreed; no conflicting editors or concurrent heavy jobs.
- 12:30: hold the lunch gate below. If full preprocessing/CV is still running, record it as pending with an owner, progress evidence, and next checkpoint. Do not compress 25 fits into an unreported smoke run or call an incomplete baseline reproduced.

**Merge strategy**

- Lead may merge reviewed documentation and portable setup changes independently of a still-running full baseline, provided their scoped checks pass.
- Merge preprocessing work as verified only after schema and reload evidence exists. No baseline-reproduced tag until full success criteria pass.

**Git commit strategy**

- Separate commits for working-copy/path setup, evidence metadata, and documentation.
- Do not commit raw data, environments, large pickle/model files, or credentials. Document their checksums/locations.

**Documentation updates**

- Every member updates their log before lunch.
- Lead adds chronological summary to `TEAM_LOG.md`, important decisions to `DECISION_REGISTER.md`, and actual milestone status to `MASTER_PLAN.md`.
- Mark every displayed score as starter reference, smoke/development, or reproduced evidence.

## Day 1 — Afternoon Phase (after lunch, 13:00–18:00)

**Objectives**

- Finish and independently review baseline reproduction before any algorithm changes.
- Preserve the reference checkpoint and document that it is not fold-safe, label-free, artifact-complete, or genuine supervised transfer.
- Only after acceptance, assign separate correctness/transfer implementation already specified by the master plan. This is not baseline optimisation.
- Aim for a valid submission-shaped package and draft narrative; maintain a recovery path if baseline execution is delayed.

**Deliverables**

- M2: full reference evidence, discrepancy analysis, versioned pickle handoff.
- M3: if authorised, separate candidate safety/transfer work with saved-state and label-free checks; otherwise reviewed task/interface notes.
- M1: accepted baseline checkpoint or explicit blocker, reviewed integration, final-audit/label-use controls, at most two proposed Day 2 experiments.
- M4: reproducibility instructions, baseline limitations, evidence-linked slides, draft justification and inventory.

**Validation checkpoint**

- 15:00: review full baseline completion or recovery status. Candidate implementation remains conditional, not a promised completed result.
- 16:30: inspect any candidate's leakage, inference, transfer-state, and artifact checks.
- 17:30: submission-shaped package review. If incomplete, list exact missing items and first Day 2 recovery task; do not mark it valid.

**Merge strategy**

- Merge completed reference evidence first; candidate PR depends on the accepted baseline contract.
- Use separate reviewed PRs for corrective implementation and experiments so the reference can always be recovered.
- Lead reviews scientific changes; another member checks lead-authored work.

**Git commit strategy**

- Commit coherent completed tasks with evidence links; tag reproduced baseline only after full reference acceptance.
- Preserve reference artifacts; tag a Day 1 checkpoint with an honest readiness note. No broken/unreviewed candidate enters `main` to satisfy the clock.

**Documentation updates**

- Record each run, deviation, failure, review, handoff, and keep/reject/defer decision.
- Update master-plan statuses and experiment tracker; use decision IDs rather than duplicating long explanations.
- End with each member's next task, dependency, and handoff recipient.

## Day 2 — Workflow (09:00–18:00)

| Phase | Objectives and deliverables | Validation and merge | Commits and documentation |
|---|---|---|---|
| 09:00–09:30 | M1 reviews organiser replies and Day 1 blockers; all confirm their tasks | No optimisation if baseline or submission-safety gate failed | Log decisions and revised schedule; synchronise accepted `main` |
| 09:30–11:00 | If gates pass, execute at most two authorised controlled experiments from the master plan; otherwise prioritise recovery/correctness. M4 independently checks evidence and drafts figures | Matched comparisons, fixed labels/metric/episodes, no final-audit tuning; select candidate by 11:00 target | One hypothesis/change per branch; record successes and failures; baseline stays immutable |
| 11:00–13:30 | Freeze selected feature/model contract; M1 owns final evaluation, M2 checks features, M3 refits/saves approved source state, M4 performs independent clean-session check | Model/feature freeze target 12:30; final audit, required budgets, label-free inference and reload target 13:30 | Merge only reviewed candidate; tag frozen candidate, update actual evidence and unresolved risks |
| 13:30–15:00 | M4 completes deck/justification; M1 interprets metrics; M2/M3 supply data/method explanations | Presentation evidence gate; all figures match frozen run | Commit documentation and lightweight result metadata; no speculative model changes |
| 15:00–16:00 | All four rehearse within confirmed limit and practise Q&A | Peer review all three rubric pillars and contributions | Log missing evidence, timing fixes, limitations |
| 16:00–17:00 | Lead coordinates release; M2 checks feature artifact, M3 model/adaptation artifact, M4 inventory/upload/backup readiness | Final submission gate; upload according to confirmed instructions | Stable release commit/tag and artifact locations/checksums; preserve receipt if submitted |
| 17:00–18:00 | Buffer, backup confirmation, final rehearsal | Only essential regression fixes, with review and affected revalidation | Log any changes; freeze again after approved fix |

## Thursday presentation workflow

- **Before the confirmed session:** Lead verifies submission status and organiser instructions; M4 checks offline PowerPoint and backup PDF; M2/M3 verify backup evidence locations. No live training dependency.
- **Final rehearsal:** Each person explains their contribution and one limitation; agree handoff phrases and who answers each technical topic. Use the confirmed time limit rather than inventing one.
- **During the talk:** M1 frames the problem/protocol; M2 explains data and reproducibility; M3 explains transfer mechanics and evidence; M4 interprets results/lessons. All four speak.
- **Q&A:** The relevant owner answers; the lead clarifies uncertainties. Never invent an organiser answer, completed experiment, or global-generalisation claim.
- **Afterward:** Record feedback and actual submission/presentation outcome in logs; confirm local backups before server shutdown. No retrospective editing of results to match the story.

# Communication Rules

## Ask for help early

Team convention: after about 15 minutes blocked or two unsuccessful AI fix attempts, stop looping and ask the lead. Escalate immediately for possible leakage, original-file edits, data loss, changed labels/metrics, environment conflicts, or shared memory pressure.

Use a compact help request: **task; file/branch; expected behaviour; actual error/evidence; what was tried; specific help needed.** Redact credentials and avoid pasting datasets or full AI transcripts.

## Escalation path

1. Task owner records blocker and tells the lead/dependency owner.
2. Lead classifies it: execution, scientific validity, integration, resource, or organiser ambiguity.
3. Pair-review one small fix; do not ask several AI sessions to rewrite the same file.
4. Only the lead consolidates organiser/support questions. Preserve the written answer and impact in the decision register.
5. Repeated/unresolved blockers cause a scoped recovery plan, not silent abandonment of required evaluation.

## Merge communication

- Submit a scoped PR with files, explanation, validation, experiment/decision IDs, and known issues.
- A chat message or an AI “looks correct” is not acceptance.
- Lead merges only after `REVIEW_CHECKLIST.md` is satisfied for the scope; final-readiness claims require the stricter submission gate.
- Shared interface changes require notifying every downstream owner before merging.

## AI review policy

- Review generated code before running it and again before merging it.
- Human author must explain inputs, outputs, fit/transform boundaries, label access, random state, and artifacts affected.
- Request lead review before executing a scientific-protocol change, dependency installation, costly job, or code touching another owner's scope.
- Log a one-line prompt summary and short change explanation; do not store private credentials or full sensitive prompts.
- If the author cannot explain a generated block, reduce its scope or pair-review it. Do not merge it on trust.

# Git Workflow

## Branch policy

- Every member works in their own clone and a short-lived task branch from agreed `main`.
- Example branch names: `baseline/path-setup`, `model/approved-task`, `docs/presentation-outline`, `integration/review-fix`. Names describe scope, not a new architecture.
- One owner per notebook; do not have two branches independently rework the same baseline file.
- `main` is the stable integration branch, not the team's experiment scratchpad.

## Commit policy

- Commit one coherent change with a clear purpose and linked evidence/decision where relevant.
- Separate execution compatibility, scientific corrections, experiments, and presentation edits.
- Inspect the diff and stage only intended files; never blanket-stage data/models/environments or unrelated user work.
- Save incomplete work on its branch with accurate status; do not call it tested, done, or merge-ready.

## Merge policy

- Use a review request/PR; the lead is integration owner.
- Require author explanation, scoped passing checks, documentation, experiment record where applicable, and committed changes.
- Reference reproduction can be merged as a clearly labelled reference with its known deficiencies; it cannot be promoted to submission-ready code.
- Resolve notebook conflicts with the file owner, preserving baseline evidence; do not accept an AI wholesale rewrite to resolve JSON conflicts.
- Merge in dependency order: setup → baseline features → reference results → separately authorised candidate changes → release evidence/presentation.
- Tag meaningful stable checkpoints only after evidence supports the tag's claim.

## Rollback policy

- Stop downstream use of suspect artifacts and notify owners.
- Lead identifies the last validated commit/tag and matching feature/model/configuration versions.
- Revert the offending change through a reviewed new commit; preserve failed branches, logs, and evidence.
- Do not force-push, hard-reset shared history, delete user work, or overwrite reference artifacts.
- Revalidate affected dependencies before resuming; record reason, impact, rollback commit, and recovery status.

# Documentation Contract

**Every important decision MUST be documented. Every experiment MUST be documented. Every AI-generated code change MUST have a short explanation.**

| Record | Required content | Owner and timing |
|---|---|---|
| `MASTER_PLAN.md` | Current priorities, actual milestone status, accepted direction, organiser clarifications, experiment summaries | Lead updates at phase reviews/major milestones |
| `DECISION_REGISTER.md` | Decision ID, time, owner, decision, reason, evidence, impact, status | Proposer supplies entry; lead accepts before consequential action |
| `TEAM_LOG.md` | Chronological seven-line task/result/decision/next-action/evidence entries | Lead integrates concise member updates at checkpoints |
| `memberN_log.md` | Daily goals, work, decisions, blockers, one-line AI prompt summaries, changed files, evidence, next steps, reflection | Each member before lunch, before handoff, and at day close |
| Experiment record + master-plan tracker | Hypothesis, changes, commit, config/seeds, data/feature/split versions, trial counts, per-budget mean/std, per-class diagnostics, runtime/memory, decision, limitations | Run owner records every run, including baseline, smoke test, failure, and abandoned attempt |
| Handoff | Status, completed/remaining work, files, issues, performed validation, exact next step | Sender before ownership changes; receiver acknowledges |
| Review request | Short AI-change explanation, allowed files, validation and known issues, links to records | Author before lead review |

Evidence should identify a commit and run/artifact location, not just “see notebook.” Use consistent IDs such as `DEC-001` and `EXP-001`; lead allocates shared IDs to avoid collisions. Time entries include date, local time, and timezone when ambiguity matters.

Label claims as **planned**, **starter reference**, **smoke/development**, **reproduced reference**, or **final audited**. No elapsed time or saved score proves completion. Append a correction rather than erasing a failed result or silently rewriting a decision. Supersede old decisions with a new linked entry.

# Quality Gates

The lead records each gate as **Pass**, **Blocked**, or **Pending**, with evidence and next owner. All checklists below are future execution requirements, not claims that they have been performed. Documentation-only requests never authorise running code.

## Gate L — Before moving to lunch

- Everyone has a clone, role, branch, allowed files, and next task; originals/raw data are protected.
- Paths/data access/environment assumptions are recorded; unresolved access issues have an owner.
- Baseline scope is unchanged except documented minimum execution compatibility fixes.
- Current preprocessing/model-run status has real evidence. Completed preprocessing includes schema/labels/pixel alignment and clean pickle reload; incomplete work is explicitly pending.
- One heavy job owns the shared compute slot; active runs have an operator and next checkpoint.
- Each member has updated their log; lead records morning decisions, blockers, and afternoon dependency order.

Lunch is not withheld when compute is slow. This gate authorises a safe phase handoff, **not** a claim of full baseline reproduction or permission to optimise.

## Gate O — Before moving to optimisation

- Full baseline success criteria from `BASELINE_EXECUTION_PLAN.md` pass: required feature contract/reload, 25 RF CV fits, final RF, zero-shot, and all reference prototype trials.
- Differences from saved reference scores and execution deviations are explained; baseline artifacts/results are preserved and tagged accurately.
- The known reference defects are recorded, not hidden or silently repaired inside reproduction.
- Separate authorised submission-safety work has passed: fold-local learned transforms, label-free inference, genuine source-state adaptation, support/query isolation, saved/reloadable state, and fixed metric/label contract.
- Final-audit separation, comparable episodes, required budgets, experiment logging, and resource limits are agreed; necessary data-use permissions are resolved or the method avoids them.
- Lead accepts the baseline/candidate handoff and approves a specific experiment already within the master plan. No baseline optimisation is authorised by this document alone.

## Gate M — Before merging code

- Correct scoped working files only; original notebooks and raw data unchanged.
- Human author explains AI-generated changes and downstream effects.
- Relevant code runs from a clean session with recorded seed/configuration; unfinished checks are not counted as passes.
- Labels, macro F1, pixel grouping, and support/query rules are unchanged or explicitly authorised; no new leakage introduced.
- Required artifacts reload and retain schema/order where affected.
- Documentation, decision/experiment records, and handoff are complete; changes committed and reviewed.
- Known reference-only limitations are clearly isolated; no false submission-ready claim.
- Lead approves merge; another member checks lead-authored changes. Use `REVIEW_CHECKLIST.md`.

## Gate P — Before preparing the final presentation

Slide outlines begin on Day 1. This gate applies to **final results and claims**, not early drafting.

- Candidate/version and evaluation protocol are frozen; every displayed metric/figure links to verified evidence.
- Madrid and required Amsterdam macro-F1 mean/std results are available with trial counts and correct labels.
- Model design, transfer strategy, and F1 interpretation are supported by evidence; failures and limitations are included honestly.
- First-slide abstract ≤150 words and justification ≤300 words provisionally; log2 sample-size curve and results table planned/completed.
- All four have a speaking role and a meaningful contribution; presentation time is confirmed or recorded as an urgent blocker.
- No claim of global portability, calibrated confidence, or genuine transfer exceeds the actual evidence.

## Gate S — Before final submission

- All master-plan required deliverables exist: saved Madrid model and required preprocessing/representation; runnable parameterised adaptation; Madrid CV/confusion proportions; required repeated Amsterdam scores; PowerPoint; written justification.
- Another member completes clean-session artifact reload and label-free inference; source-state reuse and leakage checks pass.
- Required budgets, word/time limits, final deadline, interface, upload mechanism, and any extra files are confirmed and satisfied.
- Slides/justification cover the three pillars; all four rehearse and can answer technical questions.
- Final code, configuration, metrics, and artifact versions agree and are committed/tagged; large artifacts have recorded locations/checksums.
- Offline deck/PDF and local artifact backups exist before shutdown; lead owns upload and records receipt/status.
- Any failed critical check blocks a submission-ready claim. Reduce optional scope, not scientific validity, to recover.
