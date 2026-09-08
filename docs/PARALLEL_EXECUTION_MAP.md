# Parallel Execution Map

Purpose: coordinate Day 1 so all four members start at 09:00, avoid merge conflicts, minimise idle time, and give the Team Lead clean integration points.

## Timeline

| Time | Member 1 — Lead | Member 2 — Baseline | Member 3 — Modelling | Member 4 — Research/Presentation | Validation point |
|---|---|---|---|---|---|
| 09:00–10:00 | Assign ownership, branches, compute schedule, provisional rules | Confirm owned reference files and baseline setup needs | Draft interface/leakage/artifact checklist | Draft slide/evidence scaffold and organiser-question summary | Everyone knows allowed files and stop conditions |
| 10:00–11:00 | Review setup scope; prevent conflicts | Apply minimum path/parent fixes in working copies only | Review expected feature/model contracts; no reference edits | Build evidence inventory and abstract/justification outline | 11:00 interface gate |
| 11:00–12:30 | Monitor Gate L, logs, decisions | Run/validate preprocessing or record blocker | Prepare candidate task proposal awaiting handoff | Prepare reproducibility checklist and missing-evidence list | Lunch Gate L |
| 12:30–13:00 | Safe lunch handoff | Keep any authorised run owned; no duplicate launch | Stay on review tasks | Keep placeholders; no invented results | Active work has owner/next checkpoint |
| 13:00–15:00 | Review baseline progress against execution plan | Run/continue reference modelling | Verify handoff; candidate only if authorised | Add verified baseline evidence or pending labels | Baseline acceptance/recovery point |
| 15:00–16:30 | Approve or block candidate work; run review checklist | Handoff stable feature/result evidence | Implement separate scoped transfer candidate if authorised | Convert verified evidence into slides/inventory | Candidate leakage/artifact review |
| 16:30–17:30 | Integration review and package gap assessment | Validate artifacts/handoff | Validate source-state/adaptation checks or record blocker | Assemble submission-shaped inventory | Submission-shaped package review |
| 17:30–18:00 | Update master/team logs; Day 2 plan | Update member log/handoff | Update member log/handoff | Update member log/slides gap list | Honest Day 1 checkpoint |

## Dependency Graph

```text
M1 ownership/protocol decisions
    ├──> M2 reference setup
    │       └──> M2 preprocessing artifact/reload evidence
    │               └──> M2 reference modelling evidence
    │                       ├──> M1 baseline acceptance/recovery decision
    │                       ├──> M3 candidate handoff/comparison baseline
    │                       └──> M4 verified baseline slide evidence
    ├──> M3 interface/leakage checklist
    │       └──> M3 authorised candidate work after baseline handoff
    │               └──> M1 candidate review
    │                       └──> M4 transfer-method evidence
    └──> M4 presentation/evidence scaffold
            └──> M4 submission-shaped inventory and speaking plan
```

## Merge Points

1. **Setup/documentation merge** — after M1 reviews ownership, paths, and no original-file edits.
2. **Preprocessing evidence merge** — after M2 validates schema, labels, pixel alignment, finite features, and reload.
3. **Reference baseline merge/tag** — only after full baseline criteria pass; otherwise merge blocker documentation only.
4. **Candidate merge** — only after explicit M1 authorisation, separate files, leakage checks, source-state evidence, and reload/inference validation where affected.
5. **Presentation/docs merge** — after M4 labels all claims by evidence status and M1 checks consistency with `MASTER_PLAN.md`.
6. **Day 1 checkpoint tag** — honest readiness note; not called final unless final gates actually pass.

## Validation Points

- **09:30 ownership check:** no two people edit the same file.
- **11:00 interface gate:** originals protected; baseline setup only; compute owner assigned.
- **12:30 Lunch Gate L:** run status and evidence recorded; incomplete work labelled pending.
- **15:00 baseline/recovery review:** full baseline accepted only with actual evidence.
- **16:30 candidate safety review:** no query-label fitting; source-state path clear; artifacts/reload checked where applicable.
- **17:30 package review:** deliverables, gaps, backups, and Day 2 tasks listed.

## Critical Path

The critical path for technical integration is:

```text
M1 protocol/ownership
→ M2 baseline setup
→ M2 preprocessing/reload
→ M2 reference modelling
→ M1 baseline acceptance
→ M3 authorised transfer candidate
→ M1 review/integration
→ M4 evidence-linked presentation
```

If M2 baseline execution is delayed, M3 and M4 remain productive on checklists, interface design, reproducibility, and presentation scaffolding. Candidate implementation must not bypass the baseline acceptance decision unless the Team Lead explicitly records a recovery decision.

## Parallel Tasks

Can run in parallel immediately at 09:00:

- M1: ownership, review workflow, organiser questions, logs.
- M2: baseline working-copy setup and later single authorised heavy run.
- M3: interface/leakage/artifact checklist and candidate proposal.
- M4: presentation skeleton, evidence inventory, reproducibility checklist.

Can run in parallel after baseline handoff:

- M1: review and update master/team logs.
- M2: package baseline evidence and answer feature-contract questions.
- M3: implement authorised candidate in separate owned files.
- M4: prepare slides/justification with verified or placeholder evidence.

Must not run in parallel:

- Two full baseline runs competing for CPU/RAM.
- Two people editing the same notebook/helper/document.
- Candidate code editing reference baseline files.
- Presentation claiming results before evidence handoff.

## Expected Completion Order

1. M1 ownership/protocol setup.
2. M4 slide/evidence scaffold.
3. M3 interface/leakage checklist.
4. M2 preprocessing setup and artifact validation.
5. M2 reference modelling evidence.
6. M1 baseline acceptance or recovery decision.
7. M3 authorised candidate checkpoint, if allowed.
8. M4 evidence-linked presentation package.
9. M1 Day 1 checkpoint and Day 2 plan.

## Risk Mitigation Strategy

| Risk | Mitigation |
|---|---|
| Merge conflicts | One owner per file; Team Lead approves shared-interface edits; candidate files separate from reference files |
| Idle beginners | M3 and M4 have independent checklist/presentation tasks before baseline finishes |
| False reproducibility claims | Every result labelled by evidence status; baseline acceptance requires `BASELINE_EXECUTION_PLAN.md` criteria |
| Scientific leakage | M1 review checklist; M3 leakage checklist; stop immediately for query-label fitting or label-feature contamination |
| Compute contention | M2 is sole heavy baseline operator; no duplicate full runs; resource status logged |
| Presentation lag | M4 starts at 09:00 with placeholders; verified evidence drops into prepared structure |
| Over-optimisation | No candidate work until Team Lead authorises; at most two Day 2 experiments |
| Artifact loss | Record artifact paths/checksums; do not commit large files; backup inventory by 17:30 |
| Requirement ambiguity | Use safe provisional rules from `MASTER_PLAN.md`; record organiser questions through Team Lead |
| Integration failure | Review at 11:00, 12:30, 15:00, 16:30, and 17:30; unfinished checks become Day 2 recovery tasks |
