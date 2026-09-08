# Handoff Template

Use whenever a task, artifact, or file changes hands. Fill this template in the handoff/PR record; keep the reusable template available. A chat message without evidence is not acceptance. No completed work is pre-filled.

**Time:** [date/local time]  
**From / To:** [names and roles]  
**Task / experiment / decision IDs:** [IDs or none]  
**Branch / commit / PR:** [exact references]  
**Scope and allowed files:** [ownership boundary]

## Current status

[Planned / in progress / blocked / ready for review / accepted. State whether this is reference reproduction, authorised corrective work, candidate experiment, or documentation.]

## Completed work

- [Actual completed step, output, evidence location]
- [Short explanation of AI-generated changes and human review]

## Remaining work

- [Unfinished step, owner, dependency, next checkpoint]
- [Required but unperformed tests, runs, exports, documentation, or commits]

## Files touched

| Path | Change/purpose | Source or generated artifact | Next owner |
|---|---|---|---|
| | | | |

[Confirm originals/raw data unchanged. Identify external/ignored artifact locations and checksums where recorded; do not assume a Git clone contains large data or models.]

## Known issues

- [Error/limitation and impact; reproduction steps or evidence]
- [Unresolved organiser assumptions and DEC-ID]
- [Any baseline-only methodological deficiencies; do not claim submission readiness]

## Validation performed

| Check | Actual result | Evidence / command or run reference |
|---|---|---|
| Clean execution or scoped test | [pass/fail/not run/not applicable] | |
| Seed/config/environment and feature/split version | | |
| Labels, feature order, pixel alignment, support/query separation | | |
| Fold-local fitting and source-state reuse, where applicable | | |
| Artifact save/load and label-free inference, where applicable | | |
| Documentation, experiment record, Git status | | |

[Do not run code when the task forbids it. Record checks as not run, never inferred passes. Reference reproduction and final submission have different acceptance gates.]

## Recommended next action

[One concrete first step, precise input/artifact, responsible person, acceptance evidence, required approval, and resource slot if execution is involved.]

**Receiver acknowledgement:** [name/time; accepted or blocked; reproduced/opened evidence; remaining question]  
**Lead review / gate decision:** [review reference, status, next checkpoint]  
**Documentation links:** [member log, TEAM_LOG entry, DEC-ID, EXP-ID/master-plan tracker]
