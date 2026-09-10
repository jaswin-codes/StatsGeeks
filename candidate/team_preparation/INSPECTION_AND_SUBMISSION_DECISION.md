# Inspection and submission decision

## Scope and operative instruction
Preparation/archive only. No model optimization, model fitting, inference, notebook execution, experiment regeneration, competitor execution, repository cleanup or Git-history modification was performed. Initial inspection was read-only; subsequent writes were confined to new preparation/snapshot artifacts and their protection metadata.

Organizer message supplied in this task: **presentation, written explanation, final notebook solutions; include the approach explanation in the presentation; email everything to uctstatsgeekssociety@uct.ac.za**. This supersedes earlier uncertainty about the delivery channel. It does not establish the deadline, duration, attachment limit, full-pool permission or acceptance of Python instead of a notebook. No email was sent.

## Phase-0 inventory
1. **Branch:** `integration`.
2. **Status:** dirty before this task; tracked changes include README, docs, presentation and OneNote metadata; many research artifacts are untracked. Full status: `git_status_at_snapshot.txt`.
3. **HEAD:** `7f012bba90b4c04305bcaebe24b53de59f0ca170`. Snapshot UTC: `2026-09-09T19:08:50Z`. Commit identity is not worktree identity.
4. **Structure:** `original/`, `working/`, `data/`, `models/`, `docs/`, `presentation/`, `submission/`, `submission_dry_run/`, `candidate/`, `archive/`. No reorganization.
5. **Submission artifacts:** `submission/` has no substantive final submission; `submission_dry_run/` contains an EXP-010 CLI/state, deck and justification, but no notebook.
6. **Frozen EXP-010:** `candidate/exp010_predict.py`, `candidate/artifacts/exp010_stage1_madrid.pkl`, `candidate/artifacts/joint_sweep.json`. The legacy `stage1_madrid.pkl` is a different older state and was not substituted.
7. **Current RF artifacts:** `candidate/best_model/` is the current Coordinate_RF inference package; `candidate/experiments_agf/` its prior package; `candidate/experiments_2h_v2/` holds historical ASTRA-AGF. Existing implementations remain unchanged.
8. **Presentation:** the only substantive existing deck is `presentation/StatsGeeks_BuildingAge.pptx`, 17 slides, and its PDF. The dry-run PPTX is byte-identical. It is an EXP-010 deck, despite later research results.
9. **Written justification:** `docs/WRITTEN_JUSTIFICATION.md` and the dry-run `justification/written_justification.txt` describe EXP-010. The staged text was selected. Current Coordinate_RF methods/results exist as publication reports, not an integrated organizer presentation/notebook trio.
10. **Notebooks:** ten across `original/` and `working/`; no notebook implements EXP-010, ASTRA or Coordinate_RF. The selected executed local preprocessing and modelling references have documented validation, execution counts and no saved error outputs. They are explicitly NOT final candidate notebooks. `NOTEBOOK_INVENTORY.json` records every variant and dependency.
11. **Publication bundle:** `candidate/publication/submission_bundle.zip`, SHA256 `ed8ff94f54c8f90738a3f5c577f099148f8554e151be845c1928b92662f9fd10`. Existing distribution receipt records isolated extraction, five reference predictions and byte-identical rebuilt CSVs. It contains evaluation data and is deliberately not copied into the organizer fallback.
12. **Reports/figures/tables/reproducibility:** `candidate/reports/`, `candidate/figures/publication/`, `candidate/tables/`, `candidate/reproducibility/`, `candidate/presentation/`. The prior read-only publication validator passed 1,856 sealed files and 32 figure sets at inspection. No publication artifact was regenerated.
13. **Competitor forensics:** snapshot/code outputs remain in external sibling quarantine `Hackathon3_StatsGeeks - Copy - excluded_forensics_20260909_201729`; historical own-protocol comparisons remain under `candidate/experiments_2h_v2/`. The competitor repository at `C:/Users/jaswi/JaswinHackathon` was not changed or fetched. Only local history and our own forensic audits were consulted for factual study notes. No forensic payload entered the safety snapshot.
14. **Autonomous outputs:** one timestamped run, `candidate/autonomous_runs/20260909_1727/`, with development, lock, final 1,000-episode evidence, spatial audit and prior clean replay. Its contents were not changed.

## Selection decision
There is **no fully current, validated organizer-deliverable trio**. Renaming a baseline notebook would not repair that gap. We therefore preserve the strongest existing coherent *presentation/justification* pair—EXP-010—plus the strongest audited existing reference notebooks and minimal matching EXP-010 support files. We do not invent a notebook, update a deck, or insert Coordinate_RF scores into an EXP-010 narrative.

The exact selection is in `SNAPSHOT_SEAL.json`. Its timestamped payload folder is `deliverables_20260909T190850Z/`, inside the fixed requested snapshot path. Root README/checklist expose all gaps. The current research incumbent is still Coordinate_RF; choosing an older organizer-facing fallback is a packaging decision, not research-model demotion or optimization.

## Dependencies and portability
- PPTX/PDF/text open without the live research tree. The approach is explained across deck slides 1, 5, 8 and 9; written text is not reproduced verbatim inside the deck.
- The chosen preprocessing notebook needs the supplied raw Parquets and `working/minimal_standard_scaler.py`; the latter is included. Modelling needs the derived pickle. Both notebooks must be used only in an external copy if later execution is authorized.
- Raw Parquets, preprocessed target-truth pickle, sealed evaluation truth, development labels, episode prediction NPZs and competitor data are not included. External organizer data remain necessary for reference-notebook execution.
- The EXP-010 CLI/state are portable for the documented preprocessed-input contract. They cannot manufacture missing feature inputs or satisfy a notebook requirement by themselves.
- Existing notebook JSON and code ASTs passed static checks. Full nbformat validation could not import because an existing JSON-schema package resource triggered a UnicodeDecodeError. We did not repair dependencies or rerun notebooks. PDF header/end marker and PPTX ZIP/XML integrity are checked; manual offline rendering remains outstanding.

## Snapshot immutability and background metadata exception
All **13 intended files** and their ZIP were hashed and verified, then read-only-protected. The directory was created via atomic rename after all content generation. No intended file was modified afterward. SHA self-reference is avoided: the manifest inventories payload/README/checklist; SHA256SUMS covers those plus the manifest; the external seal hashes **every** final intended file, including SHA256SUMS itself.

A background OneNote process subsequently added **seven `Open Notebook.onetoc2` index files**. They were not created by the preparation scripts, are not submission deliverables, and are absent from the already-sealed ZIP. To obey the no-change-after-freeze rule, we did **not** delete or rewrite them. Granular inherited NTFS deny-write/delete permissions were then applied to the snapshot and ZIP. Generic W/D permissions initially blocked directory reads and were replaced with granular permissions; only ACL metadata changed, not snapshot content. Owner/admin access can reverse ACLs; this is not WORM storage.

**Use the verified sibling ZIP as the exact clean fallback.** The directory's 13-file payload is intact, but directory membership is not an exact pristine match because of those unsealed background indexes. `SNAPSHOT_PROTECTION.json` inventories this issue; final verification must report it rather than silently ignore it.

## Remaining organizer-facing blockers
1. Missing final-method notebook (both EXP-010 and Coordinate_RF).
2. Existing presentation/justification describe historical EXP-010, not current Coordinate_RF.
3. Reference notebook runtime data intentionally excluded; external reproduction prerequisites remain.
4. Historical slide wording/provenance issues are listed in `CONSISTENCY_AUDIT.md`; snapshot is never silently corrected.
5. Full-target-pool/coordinate permission, deadline, size limits and three-person speaking allocation are not confirmed by the operative message.
6. Human offline rendering and actual email delivery remain unperformed.
7. Background metadata means the sealed ZIP—not a new whole-folder zip—is the clean exact distribution.

**Decision:** research is protected for a separately authorized future task, but a complete organizer-ready current-model submission is **not certified**. Fixing presentation/notebook readiness should precede prioritizing more model discovery. This preparation task does not authorize or start that discovery.
