# Day 1 Timeline

**Planning window:** 09:00–18:00 local team time, following the existing two-day plan. Lunch is planned for 12:30–13:00. These are team targets, not a confirmed organiser closing time. The Team Lead records any revised deadline or schedule in the decision register and master plan.

**Scope:** Faithful baseline first. No new ML strategy and no baseline optimisation. Later correctness/transfer tasks require separate lead authorisation under the existing master plan. This schedule describes future work; no execution or completion is asserted.

## Members

- **M1 — Team Lead:** experienced integrator/project manager; evaluation, review, organiser clarification.
- **M2 — Baseline Engineer:** reference execution and feature/artifact evidence.
- **M3 — Modelling Engineer:** interface/safety review first; separately authorised candidate work after reference acceptance.
- **M4 — Research & Presentation Engineer:** evidence, documentation, rubric, slides, independent verification support.

All members clone the GitHub repository before starting. Each works on a task branch; one named person owns each notebook. Only the designated operator launches the heavy baseline job on shared resources.

## Hour-by-hour schedule

| Time | Responsible member | Objective | Expected deliverable | Validation checkpoint | Merge point | Dependencies |
|---|---|---|---|---|---|---|
| 09:00–10:00 | M1 coordinates; all four | Confirm clone/base revision, ownership, allowed files, data access, paths and environment. M1 consolidates organiser questions; M2 plans reference execution; M3 drafts safety/interface checklist; M4 drafts evidence/slide outline | Named task cards and branches; explicit working-copy location; provisional rules and compute operator; one-line daily goals per member | Everyone can explain Madrid → Amsterdam, four-class macro F1, originals protection, and their task. No assumption that cloning includes large data | Review documentation/setup proposal only; lead approves scope before copying/editing in a later authorised execution task | Four project documents, GitHub access, lead-confirmed data-access procedure; missing data/access becomes a blocker |
| 10:00–11:00 | M2 implements authorised execution setup; M1 reviews; M3/M4 assist without editing M2 files | Prepare team copies of Notebooks 3 and 4 with minimum portable path/parent handling only; record versions, seeds, inputs and horizon. M3 reviews contracts; M4 records baseline/reference limitations | Scoped setup diff and deviation list; reproducible run instructions; source/target feature expectations; initial presentation skeleton | 11:00 interface gate: paths/inputs resolve, no original changes, no algorithm/QA/feature/scaling changes, one heavy-run slot agreed | Lead may merge reviewed path/setup/documentation changes once their scoped tests pass; do not tag baseline reproduced | 09:00 agreements; access to raw data and compatible environment |
| 11:00–12:00 | M2 runs authorised preprocessing; M1 monitors; M3 reviews handoff expectations; M4 curates evidence | Execute reference Notebook 3 copy once; retain preprocessing output and resource observations. Other members work on independent documentation/review tasks | Pickle if complete; otherwise honest run progress/error evidence. Feature/schema checklist and baseline limitation notes | When complete: 60 ordered features; expected Madrid (76263,60), Amsterdam (25992,60); label/pixel alignment; finite outputs; reloadable pickle | Preprocessing acceptance only after actual checks; long run remains pending, not merged as a completed result | Scoped setup passed; shared CPU/RAM available; input/schema checks |
| 12:00–12:30 | M1 +M2, with M3 independent review and M4 documentation | Review preprocessing/reload or blocker; start reference modelling only if ready. Summarise morning progress and afternoon dependencies | Gate L record; artifact handoff or recovery task; updated member logs; initial team-log/decision entries | Lunch gate: owners, originals protection, run state/evidence, resource operator and next checkpoint all clear | Merge only independently validated scoped work; no optimisation permission implied | Pickle or explicit blocker; reviewer available |
| 12:30–13:00 | All; M2 remains designated operator for any continuing job | Lunch and safe handover; do not launch duplicate work or disguise unfinished compute as completion | Brief availability/run-status note and next checkpoint | Active work has an owner; pending full runs stay pending | No forced merge or milestone tag | Gate L phase handoff; actual completion is not required to take a break |
| 13:00–14:00 | M2 runs reference Notebook 4 copy; M1 checks scope; M3/M4 document and review | Continue/launch clean-kernel 25-fit RF CV, final source RF, zero-shot, ten-trial prototype evaluation with unchanged reference settings | Run log/output capture, seeds/config/environment; actual completed counts. M3 prepares approved candidate task outline; M4 fills non-result slides | Track all required fits/trials; preserve 10-shot diagnostic; stop on real errors. No unreported parameter reductions to meet schedule | Evidence/docs PR may progress; full baseline acceptance waits for completion | Validated pickle; CPU/RAM coordination; minimum compatibility fixes only |
| 14:00–15:00 | M1 +M2 review; M3 verifies interfaces; M4 checks claims | Compare completed reference results with saved starter outputs and explain deviations; document global scaling, label dependence, target-only prototypes, and missing exports | Full baseline acceptance record if criteria pass; otherwise explicit remaining fits/errors, recovery owner and new checkpoint | Reference success requires actual clean run, 25 fits, final RF, zero-shot and all prototype trials; references are not proof of execution or hidden-test scores | Lead merges accepted reference evidence and tags reproduced baseline only if justified; no fake completion at 15:00 | Completed reference run and evidence; baseline-plan validation checklist |
| 15:00–16:00 | M3 only on authorised separate candidate task; M2 provides stable feature handoff; M1 supervises; M4 drafts instructions/justification | If reference accepted, begin the existing master-plan correctness/transfer work in separate copies. If not, M2/M1 recover baseline while M3/M4 finish review/docs | Candidate work-in-progress and scoped tests, or documented recovery progress; reference remains immutable | Check no query-label fitting, unchanged labels/metric, explicit source-state path and label-free interface where implemented. Incomplete checks stay pending | Small candidate PR only when its scoped checks pass; not baseline optimisation and not final-readiness acceptance | Accepted baseline contract plus explicit lead authorisation; otherwise recovery branch of schedule |
| 16:00–17:00 | M1 reviews; M2/M3 validate their artifacts; M4 independently follows run/inference instructions when authorised | Target 16:30 integration review: assess actual candidate safety, saved-state/reload, reference comparison, and required remaining work | Reviewed handoffs and artifact inventory; leakage/inference/transfer review evidence if complete; result-linked slide draft | Gate M for each PR. Gate O cannot pass until genuine transfer, fold-safe fitting, label-free inference, saved state, and evaluation controls pass separately from reference | Merge only reviewed working code; preserve reference tag/artifacts; unready code stays on branch | Actual completed candidate checks; independent reviewer; artifact/configuration availability |
| 17:00–18:00 | All; M1 accepts status and plans Day 2; M4 assembles package | Target 17:30 submission-shaped package review; back up outputs; each member explains one contribution/limitation. Choose at most two Day 2 experiments only if gates allow | Package/inventory or exact missing-item list; updated master plan, team/member logs, decisions, handoffs; backups; Day 2 task list | No submission-ready claim unless required safety/artifact/evaluation checks pass. Failed gates trigger Day 2 recovery, not skipped validation | Commit reviewed documentation/evidence; tag Day 1 checkpoint with honest readiness status; do not call incomplete work a reproduced/final milestone | Reviewed changes and evidence; confirmed backup destination; current organiser answers |

## Critical dependencies

1. Portable working-copy setup → reference preprocessing → validated/reloaded feature pickle → clean reference modelling → baseline acceptance.
2. Baseline acceptance → explicit lead approval → separate corrective/transfer candidate work from the master plan.
3. Candidate safety and reproducibility gates → permission to optimise through controlled existing-plan experiments.
4. Verified run evidence → final numerical slide claims. Slide outline and rubric work do not wait for training.
5. Reviewed commit +matching artifacts → handoff and stable milestone; a notebook kernel alone is not an artifact handoff.

## Delay and escalation policy

- If blocked for approximately 15 minutes or after two unsuccessful AI fixes, ask the lead with branch/file, expected/actual behaviour, error evidence, and attempted fixes.
- Escalate suspected leakage, original edits, changed labels/metrics, data loss, or memory pressure immediately.
- If full baseline execution outlasts a slot, retain the baseline settings and extend its schedule. A smaller smoke run may be labelled separately only with approval; it cannot satisfy full reproduction.
- Do not run four full baselines merely because there are four clones. Share immutable artifact locations/checksums and lightweight evidence; independent checks remain targeted.
- At a missed checkpoint, record status, evidence, remaining work, owner, and next review. Keep M3/M4 productive on interfaces, documentation, and presentation rather than unapproved model work.
- At day close, save progress and identify whether any continuing job is explicitly authorised with an operator and resource plan. Do not imply overnight results exist.

## Day 1 exit targets

- [ ] Reference reproduced and evidenced, or precisely documented recovery work assigned.
- [ ] Original notebooks and raw data preserved; no baseline optimisation performed.
- [ ] Shared state committed/reviewed appropriately; large artifact locations and versions documented.
- [ ] Any candidate work is separate, authorised, and honestly labelled by validation status.
- [ ] Every member log is current; shared diary and decision entries integrated by lead.
- [ ] Slide skeleton, rubric checklist, and concise scientific limitations exist.
- [ ] Submission-shaped package readiness and gaps recorded, with local backups.
- [ ] Day 2 begins with named tasks, dependencies, and gate conditions rather than another repository re-audit.
