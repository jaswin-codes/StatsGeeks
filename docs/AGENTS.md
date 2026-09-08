# Project Goal

Build a reproducible four-class building-construction-era classifier for 30 m × 30 m Landsat pixels. Train entirely on Madrid, then adapt learned source state to Amsterdam using very few labelled pixels. Evaluate four-class macro F1, especially at 25 labels per class, while demonstrating scientific validity, originality, and team collaboration.

Read `MASTER_PLAN.md` for current status, priorities, provisional requirements, and owners. `Hackathon_Analysis_Report.md` is the historical audit, not evidence that training has been reproduced. These instructions derive from that report and the team's documentation workflow; coding conventions below are team standards, not additional organiser rules.

# Absolute Rules

## Preserve source materials and user work

- NEVER modify the original organiser notebooks: `1-Introduction.ipynb`, `2-Reading_Data.ipynb`, `3-Preprocessing.ipynb`, and `4-Modelling.ipynb`.
- ALWAYS work on clearly identified team-owned copies. Preserve original data, supplied challenge documents, and the historical audit.
- Never overwrite user work without explaining the intended change. Do not revert unrelated edits.
- Never remove existing functionality without explaining why and documenting its replacement or consequences.
- Prefer incremental, reviewable changes over whole-notebook rewrites.
- Respect the current request's scope. A documentation-only task does not authorise training, package installation, or code changes.

## Protect the scientific protocol

- Madrid is the source and Amsterdam the target. Do not reverse them based on the optional metric-learning guide.
- Predict four classes, not five classes or construction-year regression unless explicitly instructed to change the task.
- Never alter class boundaries or interval inclusivity unless explicitly instructed. Record any approved change and its consequences in `MASTER_PLAN.md`.
- Current intervals are Madrid: ≤1960, (1960,1984], (1984,2004], >2004; Amsterdam: ≤1945, (1945,1984], (1984,2004], >2004.
- Keep preprocessing and feature generation label-independent. `weighted_mean_year` may derive labels but must not become a predictive input. Exclude `age_class`, true-construction-year-centred windows, and aggregates of held-out labels.
- Never use Amsterdam query labels during training, representation fitting, adaptation, feature selection, or final-audit tuning. Query labels are evaluation-only.
- Sampling infrastructure may inspect labels to choose balanced support sets; adaptation receives only selected support labels. Do not infer that all available Amsterdam labels are permitted for development.
- Keep support/query IDs disjoint. Reserve final audit evaluation from hyperparameter selection.
- Keep all years of each geographic pixel in one split. Use `(city, px_key, py_key)` across cities; `pixel_id` is a pixel-year identifier.
- Fit learned scalers, feature selection, and representations inside training folds. Refit on all Madrid only after model selection.
- Adaptation must consume genuinely source-learned state. Raw Amsterdam prototypes in Madrid-standardised feature space do not establish supervised transfer.
- Preserve the source artifact; use separate adaptation state for each episode.
- Do not silently change evaluation metrics. Primary reporting is macro F1 over classes 1–4, not accuracy or weighted F1.
- Support provisional budgets 5, 25, 50, 100, 200 per class until clarified. Treat 10-shot as optional diagnostic.
- Do not use unconfirmed permissions for unlabelled query alignment, pseudo-labelling, external data, pretrained models, or unrestricted target-label tuning. Ask for clarification.
- Do not assume summer-only observations, artifact-free QA flags, or verified spectral scaling. Document and justify any sensor/season/QA correction.

## Preserve reproducibility and deliverability

- Always preserve explicit deterministic seeds for splits, support draws, training, and comparisons. Record any unavoidable nondeterminism.
- Keep notebooks runnable top-to-bottom from a clean environment without hidden kernel state.
- Never hardcode machine-specific absolute paths. Use configurable project-relative paths and document artifact locations.
- Save models explicitly. Save preprocessing, learned representations, ordered feature schemas, annual horizons, class configuration, and seeds explicitly.
- Validate save/load round trips and inference with label fields absent.
- Document assumptions, new dependencies, versions, and important architectural decisions.
- Keep Markdown documentation current with major changes and milestone evidence.
- Never describe saved starter outputs, unexecuted code, or proposed experiments as independently verified results.
- Coordinate heavy jobs on shared resources; avoid uncontrolled parallel `n_jobs=-1` workloads and full all-pixel pairwise distance matrices.
- Back up artifacts before server shutdown. Do not put credentials, raw datasets, large caches, or models into ordinary Git history.

# Coding Standards

## Python style

- Use readable, consistent Python with four-space indentation and PEP 8-style naming.
- Prefer small, single-purpose functions and reusable helpers over copied notebook logic.
- Use explicit inputs/outputs for feature transformation, source training, adaptation, prediction, and evaluation. Keep labels separate from feature matrices.
- Add type hints and concise docstrings to public pipeline interfaces, specifying shapes, pixel keys, expected columns, and fitted state where relevant.
- Keep paths, seeds, budgets, horizons, feature lists, and model parameters in explicit configuration rather than scattered literals.
- Validate schema, feature order, class labels, finite outputs, and support/query separation at pipeline boundaries.
- Prefer clear errors for invalid budgets or missing classes over silently changing the intended experiment.
- Avoid introducing a new framework or dependency unless it serves a documented task-specific purpose.

## Notebook style

- Edit only working copies. Assign one owner per notebook or shared component to limit conflicts.
- Organise notebooks into setup/configuration, inputs, transformations, training/adaptation, evaluation, and export sections as applicable.
- Put methodological rationale and assumptions in Markdown; keep reusable computation in helpers when practical.
- Do not rely on variables from another notebook's kernel. Dependencies must be explicit saved artifacts or imports.
- Distinguish EDA using known labels from inference-safe feature generation.
- Preserve reference outputs as references; clear or regenerate stale working-copy outputs before calling a run final.
- Keep figures readable and label city, budget, metric, evaluation protocol, and uncertainty correctly.
- Use held-out or OOF diagnostic maps; aggregate repeated pixel probabilities rather than overwrite duplicates.

## Documentation style

- Write concise Markdown with clear headings, file paths, ordered actions, and actionable checklists.
- Separate verified facts, saved reference outputs, reproduced results, hypotheses, and organiser-dependent assumptions.
- Explain why consequential changes were made, what they affect, how they were tested, and unresolved limitations.
- Update `MASTER_PLAN.md` for decisions, owners, task status, experiment outcomes, blockers, and major milestones. Do not mark a milestone complete without evidence.
- Keep the historical audit unchanged; record subsequent corrections and organiser clarifications in the living plan with source/date.
- Do not claim global portability, calibrated confidence, independent repeated-CV scores, or causal construction effects beyond evidence.

## Naming conventions

- Use `snake_case` for Python functions, variables, modules, and new working-file names; `PascalCase` for classes; `UPPER_SNAKE_CASE` for constants.
- Use explicit `madrid`, `amsterdam`, `support`, and `query` names where ambiguity could affect label handling.
- Give experiments unique, stable IDs such as `EXP-001`; identify feature, split/episode, and artifact versions in their records.
- Distinguish organiser originals, team working copies, reference results, and final artifacts in names and documented locations.
- Never infer feature order or class order from incidental file ordering; save both explicitly.

## Reproducibility standards

- Record commit, environment/package versions, raw-data checksums, configuration, feature version, split/episode IDs, support IDs, and seeds for each reported run.
- Use matched episodes and seeds for method comparisons; nested support budgets are preferred for controlled learning curves.
- Save per-trial scores and summarise mean/std with fold/repeat/trial counts and variation source.
- Standard deviation is not a confidence interval; confusion-matrix diagonals are recall, not F1.
- Document clean-run and inference commands when implementation exists. Do not claim a run happened if execution was prohibited or unavailable.
- Have another member independently reload final artifacts and reproduce inference before submission.

# Git Workflow

- The audit found no Git metadata. Establish Git only as part of an authorised implementation/setup task; do not assume it already exists.
- Keep `main` as the stable integration branch. Use short-lived task/feature branches and review changes before merging.
- Make small, coherent commits with clear messages explaining purpose, such as a preprocessing safety fix or one experiment's configuration/results.
- Never edit organiser originals directly, including during formatting, path fixes, or notebook output cleanup.
- Review the diff and working-tree changes before committing; do not stage unrelated user work.
- Keep datasets, large artifacts/caches, environments, and credentials out of ordinary Git. Track checksums, configurations, and artifact locations instead.
- Tag stable milestones: reproduced baseline, valid transfer pipeline, Day 1 package, and final submission.
- Preserve user changes and history; do not use destructive resets, broad cleanup, or force pushes without explicit authorisation.
- Suggest commits at logical milestones. Follow current user authorisation for committing; if a commit cannot be made, report it as pending rather than claiming the task is fully done.

# Experiment Rules

1. Start from a reproduced baseline. Saved starter scores are comparison references, not team-run evidence.
2. State a falsifiable hypothesis before changing preprocessing or models. Priorities from the audit are quality-aware fallback, season comparability, coverage, robust temporal features, source-supervised representation, and static/temporal separation.
3. Prefer one controlled change per comparison; avoid random algorithm sweeps.
4. Use the same feature/split contract and support/query episodes across compared methods unless the hypothesis explicitly requires a documented difference.
5. Evaluate the baseline ladder: majority reference, Madrid RF zero-shot, raw-feature target prototypes, and genuine source-learned transfer.
6. Prove source-learning benefit against target-only prototypes; compare an unlearned representation where practical. Improvement over zero-shot RF alone is not proof of transfer.
7. Start with a compact frozen source representation and simple target prototypes. Use simpler source-supervised weighting/metric transfer if a more complex embedding is unstable.
8. Prioritise 25-shot stability, test all required budgets, and report per-class behaviour and spatial sensitivity. Do not choose a model from one lucky draw.
9. Keep final audit query evaluation out of tuning. Do not change class definitions, label budgets, or metric to improve a result silently.
10. Record experiment ID, hypothesis, changes, commit, parameters, seeds, feature/split versions, trial counts, per-budget mean/std, per-class diagnostics, runtime, memory, and decision. Add a summary row to the Experiment Tracker in `MASTER_PLAN.md`.
11. Record failures with the attempted method, observed result/error, evidence, suspected explanation distinguished from fact, and keep/reject/defer decision. Negative scientific results are useful; do not hide them or manufacture a success narrative.
12. Label smoke tests, development results, final-audit results, and unexecuted proposals distinctly.
13. Keep expensive preprocessing cached and versioned. Coordinate CPU/RAM use and stop architectural expansion early enough to package, independently test, and rehearse.
14. Do not start internet research, external-data integration, or new dependencies merely for novelty; prioritise confirmed requirements and the current task.

# Definition of Done

An implementation task is complete only when:

- [ ] Requested functionality is implemented without unrelated changes or edits to originals.
- [ ] Code runs from a clean documented environment; relevant checks pass.
- [ ] Results are reproducible with recorded configuration, versions, IDs, and seeds.
- [ ] No label leakage or support/query overlap is introduced; learned transforms respect folds.
- [ ] Relevant inference works without label columns and preserves the feature contract.
- [ ] Models/preprocessing are explicitly saved and reload-tested when the task affects artifacts.
- [ ] Changes, assumptions, dependencies, results, and limitations are documented; `MASTER_PLAN.md` is updated as appropriate.
- [ ] Changes are reviewed and committed to Git under the authorised workflow.

If execution, Git, or data access is unavailable or prohibited, state which checks remain pending; do not falsely declare implementation complete. For documentation-only tasks, do not execute code to satisfy this checklist: completion means the requested documents are accurate and saved within scope, with any applicable commit status reported honestly.

Final-submission readiness additionally requires all deliverables, all required macro-F1 budgets, the abstract/justification limits, the three rubric pillars, clean artifact reload, four-person presentation preparation, and backups listed in `MASTER_PLAN.md`.

# AI Behaviour

Every future Codex session should:

1. Read `MASTER_PLAN.md` first.
2. Read `AGENTS.md` second; if this file was automatically loaded first, still read the current master plan before planning work.
3. Read only the files necessary for the requested task. Consult relevant audit sections for background rather than rediscovering established facts.
4. Avoid rereading or re-auditing the full repository unless required by the task or a material change.
5. Minimise token usage and unnecessary tool calls.
6. Produce concise reasoning and summaries unless detailed explanations are requested.
7. Update `MASTER_PLAN.md` whenever major milestones are completed, with evidence, status, decisions, and remaining blockers; respect a request that explicitly limits documentation edits.
8. Never overwrite user work without explanation or undo unrelated changes.
9. Suggest Git commits at logical milestones and clearly distinguish suggested, pending, and completed commits.
10. Prefer improving existing working-copy code over rewriting entire notebooks.

Before acting, distinguish the requested task from the broader plan. Ask for clarification when an unresolved organiser rule affects scientific validity or submission compatibility. Explain important architectural decisions briefly, preserve incremental progress, and report exactly what changed and what was actually verified. Do not invent implementation progress, organiser answers, benchmark results, or file contents.
