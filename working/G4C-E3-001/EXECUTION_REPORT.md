# E3 execution report - G4C-E3-001

## Experiment status

**STOPPED - EXTERNAL EXECUTION HARNESS TIMEOUT**

The authorized E3 run was externally terminated after 52 of 60 frozen episodes completed. The timeout occurred while the coordinator was preparing episode `G4A-B200-T03` (episode 53). Its input packet was preserved, but no worker output or prediction was produced for that episode. The run was not resumed or retried.

## Completion and preservation

- Planned episodes: 60
- Completed episodes: **52**
- Preserved prediction artifacts: **52**
- Uncompleted episodes: 8 (200-shot trials 3-10)
- Completed worker teardowns: 52/52 PASS; no survivors
- Peak completed-worker RSS: **2,866,656 KiB**
- Candidate warnings: none
- E4/E5: not executed

The 52 completed artifacts are partial failure evidence only. They were not combined with another identity or selectively scored.

## Metrics and validation

The frozen protocol requires every candidate prediction to be finalized and every worker reaped before evaluator labels are attached. Because only 52/60 predictions completed, evaluator scoring did not begin.

- Primary 25-shot macro F1: N/A
- Paired improvement over raw prototype: N/A
- Improvement over frozen RF: N/A
- E3 success criteria: NOT EVALUATED
- Independent full-output validation: NOT RUN (incomplete run)
- Scientific verdict: **NOT EVALUATED**

This is an infrastructure/harness stop, not scientific falsification of E3. The frozen datasets, preprocessing, Random Forest, episode manifest, parameters, worker algorithm, isolation policy, and completed prediction evidence were not modified.

## Failure

The external execution command reached its 5000-second harness limit after completing episode 52. No candidate process remained afterward. Exact logs and the incomplete episode input are preserved under `results/` and `evidence/`.

A new run identity and separate authorization are required for any further E3 attempt. `G4C-E3-001` must not be resumed or overwritten.
