# Review Checklist

For the Team Lead before accepting code. Complete a review record for each PR/handoff; an empty checkbox is not a pass. Scope the review as **reference reproduction**, **authorised corrective implementation**, **candidate experiment**, or **documentation**. Use `TEAM_OPERATING_SYSTEM.md` gates and the baseline plan for the relevant scope.

**Author / reviewer:** ____________________  
**Task and scope:** ____________________  
**Branch / commit / PR:** ____________________  
**Evidence / EXP-ID / DEC-ID:** ____________________  
**Review time:** ____________________

## ✓ Correct files modified

- [ ] Diff includes only assigned working copies/helpers/documents; no unrelated edits or user work overwritten.
- [ ] File owners reviewed shared-interface changes; no competing notebook edits remain.
- [ ] Every AI-generated code change has a short explanation; the author can explain its inputs, outputs, label access, state, and effects.
- [ ] New dependencies, configuration, and portable paths are documented and approved.

## ✓ Original notebooks untouched

- [ ] `original/` organiser notebooks are unchanged, including outputs/metadata.
- [ ] Raw Parquets and historical audit are unchanged; no original was reformatted or edited for a path fix.
- [ ] Reference reproduction changes are limited to recorded minimum execution compatibility fixes; no hidden optimisation or method change.

## ✓ Code runs

- [ ] Relevant working code runs cleanly from the documented environment/kernel and start point.
- [ ] Required input/artifact availability and execution order are explicit; no hidden notebook state.
- [ ] Results, failures, and warnings have actual run evidence; smoke tests are not presented as full evaluations.
- [ ] Artifact load, schema, shape, feature-order, and label/pixel alignment checks pass where affected.
- [ ] Full reference acceptance, if claimed, includes 60 features, pickle reload, 25 RF CV fits, final RF, zero-shot, and ten prototype trials at all reference budgets.

## ✓ Reproducible

- [ ] Commit, environment versions, input checksums/locations, configuration, seeds, feature version, and split/episode IDs are recorded as applicable.
- [ ] No silent changes to four classes, right-inclusive boundaries, macro F1, horizon, requested budgets, or trial counts.
- [ ] Candidate models/preprocessing/schema/configuration are explicitly saved and reload-tested where affected.
- [ ] Comparisons use approved matched episodes and report per-budget mean/std and variation source; standard deviation is not labelled a confidence interval.
- [ ] Another member can follow the handoff; final release requires independent clean-session reload and label-free inference.

## ✓ No obvious leakage

- [ ] Predictive features exclude construction year, class, true-year-centred windows, and held-out-label aggregates.
- [ ] All years of a geographic pixel stay together; correct city/pixel keys are used.
- [ ] Support/query IDs are disjoint; query labels are evaluation-only; final audit is not used for tuning.
- [ ] Learned transformations are fitted within training folds for submission/candidate code.
- [ ] Genuine source-learned state is reused during adaptation for submission/candidate code; source artifact remains immutable.
- [ ] Unconfirmed target-feature/label privileges or external resources were not introduced.
- [ ] Label-free inference passes for submission/candidate code; spatial dependence and other known limitations are disclosed.

**Reference-only exception handling:** Faithful reference reproduction retains documented global pre-CV scaling and label-dependent feature construction; its target prototypes do not reuse the fitted RF. Do not falsely check these deficiencies as fixed. Record them below and merge only as an isolated, clearly labelled reference under the baseline plan, with no new leakage. This exception never satisfies the optimisation/submission-safety gate.

## ✓ Documentation updated

- [ ] Member log and concise team-log update are supplied.
- [ ] Important decisions have DEC-IDs, reasons, evidence, impact, and status.
- [ ] Master-plan changes reflect actual milestone progress; no fabricated run/merge completion.
- [ ] Handoff lists files, completed/remaining work, validation, known issues, and exact next action.
- [ ] Claims distinguish starter references, smoke/development, reproduced reference, and final audited evidence.

## ✓ Experiment logged

- [ ] Every affected experiment/run, including failed/reference runs, has an ID and evidence record.
- [ ] Hypothesis, changes, parameters/seeds, feature/split versions, scores or failure, trial counts, resource observations, decision, and limitations are recorded.
- [ ] Master-plan experiment summary and detailed record agree; no cherry-picked lucky draw or hidden failed experiment.
- [ ] If no experiment applies, record an explicit reason rather than fabricating an entry.

## ✓ Git committed

- [ ] Intended changes are committed on the task branch with a clear message and reviewed diff.
- [ ] No raw datasets, large caches/models, environments, credentials, or unrelated work are staged/committed.
- [ ] Review evidence identifies the exact commit; uncommitted or untested changes are not included in the acceptance claim.

## ✓ Ready to merge

- [ ] All applicable scoped checks pass; failed/pending checks have not been counted as passes.
- [ ] Dependencies and downstream owners are ready; baseline/candidate artifacts cannot overwrite each other.
- [ ] Lead approves, with a second member reviewing lead-authored technical changes.
- [ ] A recovery commit/tag and corresponding artifact versions are known for consequential changes.
- [ ] Required post-merge/master-plan updates have a named owner.

## Review outcome

**Decision:** [Approved for scoped merge / Changes requested / Blocked]  
**Known limitations or justified N/A checks:** ____________________  
**Unperformed validation:** ____________________  
**Required follow-up / owner / checkpoint:** ____________________  
**Reviewer and evidence:** ____________________  
**Actual merge commit, after merge only:** ____________________

Documentation-only requests do not authorise code execution or Git operations. Mark execution checks not applicable to a pure document change, and state any pending commit honestly. Do not use this scoped acceptance to claim an implementation or final submission is complete.
