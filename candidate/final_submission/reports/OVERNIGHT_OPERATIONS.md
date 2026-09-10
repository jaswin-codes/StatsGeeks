# Operational notes

## Live execution

The detached driver was launched at 2026-09-09T20:11:26Z. `LAUNCH.json` records Windows launcher PIDs; `.venv_baseline` launchers spawn real Python child processes, so `STATUS.json` records the actual worker PID. This is expected, not a second search. The watchdog validates the owned command line and handles descendants before forced finalization. It requests a bounded Windows system-awake state without changing persistent power settings. Reboot, power loss, or termination can still interrupt the run.

Discovery deadline: 2026-09-10T02:00:15Z. The normal worker then performs one-time development-support spatial diagnostics and finalist replay, followed by final package generation. If it has not completed by 03:00:15Z, the independent watchdog stops only the owned worker tree and attempts finalization, reserving time before 04:00:15Z. A tested incumbent package already exists independently of this future finalization.

## Scientific boundary

The already-designated 800-label development-support bank is the only target supervision used by discovery. New resampling seeds do not make a fresh population. No unseen organizer target pool is available locally. Thus all new candidates are exploratory and cannot pass the requested fresh-population promotion gate, regardless of development scores. This preserves rather than weakens the user's absolute ban on query-driven model selection. The incumbent's published audit numbers are reporting-only.

The new source rebuild is a separate reproduction check of the existing locked model, not candidate selection. Its historical trusted preprocessing pickle contains target labels; that field was immediately discarded, never indexed or passed to fitting. `fit_pool` accepts Madrid labels and unlabelled Amsterdam features/coordinates only. Its eight state arrays and serialized pool artifact match exactly. Five-budget predictions also match.

## Failures and fixes

1. Importing installed `nbformat` failed because `jsonschema_specifications` attempted to decode non-UTF8 data in its package schema tree. No shared dependency files were changed. A standard-library nbformat-4 serializer was written inside this run root; the actual notebook code cells were executed sequentially in a fresh Python process and their real outputs saved. This is not mislabelled as Jupyter-kernel execution.
2. The first new source-refit attempt rejected an obsolete hash quoted by `candidate/README.md`. The authoritative locked-run provenance instead binds the accepted cache to `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`. The script now verifies that frozen provenance, not a relaxed assertion. The fresh rebuild then passed, including byte-identical artifact SHA256 `b975db430b4a00d1c90d59d10a76ef11a6c3727be42e22f41bec49a6f6c28007`.
3. PDF rendering was initially unverified. PDFium was installed only under this run's `local_deps/`, then independently rendered all sixteen native-PowerPoint-exported PDF pages. PPTX was opened and all sixteen slides rendered by native PowerPoint. Representative learning-curve and written-explanation slide images were visually inspected and readable.
4. SVC emits a future-deprecation warning for probability fitting. This is not a fit failure; the installed API is used with a fixed seed and bounded iterations. Warnings are retained in `worker.log`.

## Remaining gaps

No new independent-city/organizer validation can be claimed. The driver's preliminary geographic diagnostic uses designated development-support labels only. After discovery ends and the finalist is frozen, a separate one-time reporting-only evaluator is scheduled for 50 new support draws at every budget and the established full 200-shot opposite-half spatial framework (all four directions, ten trials each). It writes FIXED_FINALIST_AUDIT.json and never changes the winner or feeds further optimization. These draws still reuse the exposed city, so they do not satisfy fresh-population promotion. Failure/timeout cannot prevent incumbent packaging. Organizer eligibility of full-pool coordinates, historical preprocessing membership and extra research supervision remains unconfirmed. The notebook supports actual artifact-bound inference and explains external rebuild inputs, but is not self-contained raw-data training.
