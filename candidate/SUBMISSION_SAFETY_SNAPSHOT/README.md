# PRE-OVERNIGHT SUBMISSION SAFETY SNAPSHOT — FROZEN

Created UTC: 2026-09-09T19:08:50.620710+00:00 · timestamped deliverables directory: `deliverables_20260909T190850Z/`.
Git branch: `integration`. Git HEAD: `7f012bba90b4c04305bcaebe24b53de59f0ca170`. Working tree was dirty; the commit alone does not identify this snapshot. The manifest and hashes do.

**DO NOT overwrite, edit, regenerate, add experiments, or optimize using this directory.** This is the currently safest known *existing organizer-facing fallback*, not a certification that the required final-method notebook already exists. Later optimization must never overwrite it. Work only on new copies outside the snapshot. File read-only flags are accidental-write protection, not administrator-proof immutability; an externally recorded seal and ZIP detect changes.

## Organizer instructions currently known
The operative instruction supplied for this task is: “The presentation, their written explanation of their approach, and their final notebook solutions. This is what you need to submit; the written explanation of your approach should be included in your presentation. And send everything to: uctstatsgeekssociety@uct.ac.za”. No email is sent by this task. Deadline, size limits, notebook count, presentation duration and full-target-pool/coordinate permission are not established by this message. Older rubric/word-limit notes are historical, not a new confirmation.

## Exactly what this fallback represents
The presentation (17 slides) and standalone written justification describe **frozen EXP-010**, seed-31337 audit, ten paired episodes/budget: 5=0.552428 ±0.059539; 25=0.612174 ±0.013057; 50=0.617273 ±0.007839; 100=0.619513 ±0.004770; 200=0.623982 ±0.003646. The matched full-feature target-only control gives 45/50 paired wins overall. Deviations are population SD, not confidence intervals. This is not the current Coordinate_RF learning curve.

Current development-locked research model (NOT the model in this deck): Coordinate_RF, 0.749299 ±0.005716 at 200 shots; matched ASTRA gain +0.016262, 200/200 wins. The validated publication bundle stays outside this minimal organizer snapshot: it is not a substitute for the requested final notebooks. No research/sealed evaluation data was copied here.

## Critical completeness warning
**No final notebook implementing EXP-010, ASTRA or Coordinate_RF was found.** The two included executed notebooks are the strongest audited *reference preprocessing/modelling evidence*, not invented or relabelled final solutions. They do not reproduce the EXP-010 or Coordinate_RF headlines. The matching frozen EXP-010 Python interface and source-only artifact are included as minimal operational support, but do not satisfy a notebook-only requirement. Therefore this folder is a protected fallback with an explicitly unresolved organizer deliverable; do not represent it as a fully compliant current-model submission.

## Contents and dependency boundary
Open the PPTX/PDF and text explanation directly; these are portable static files. The approach explanation is embedded across presentation slides 1/5/8/9 and the result interpretation in 6/10/11; the standalone text is not promised verbatim inside the deck.

The two notebooks retain their original bytes and embedded outputs. Preprocessing requires organizer `data/madrid_train.parquet` and `data/amsterdam_data.parquet`; modelling reads `../data/preprocessed/preprocessed_data.pkl` relative to its `working/` notebook directory. Raw data and the label-containing preprocessed pickle are intentionally **not distributed** here. If independently authorized to reproduce the reference, copy the *deliverables directory* elsewhere, obtain the organizer data, and keep `data/` beside `working/`. The local scaler module must be importable with that copied directory on PYTHONPATH. Notebook libraries: NumPy, pandas, Matplotlib, scikit-learn, SciPy, PyArrow plus a Jupyter environment. Historical Notebook 4 kernel was Python 3.11.9; exact historical in-kernel package provenance is incomplete. No notebook execution is requested as part of snapshot verification. Executing notebooks in this frozen directory would overwrite outputs/data and is forbidden; use an external working copy only.

The EXP-010 CLI requires already Madrid-standardized ordered 60-feature inputs. From an *external copy* of `deliverables_20260909T190850Z/`, inference syntax is:

`python code/exp010_predict.py --artifact model/exp010_stage1_madrid.pkl --support support.npz --query query.npz --shots 5 --seed 31337 --output predictions.npy`

Support NPZ: `X`, `y`, `feature_names`; query NPZ: `X`, `feature_names`, no labels. Exactly budget support labels/class, IDs 1–4. `requirements.txt` covers this CLI only. No support/query NPZ or target truth is included. Only load trusted, hash-verified pickle files.

## Known caveats preserved rather than silently repaired
- Deck/text are an older EXP-010 submission narrative. Their “primary result” is historical; the research incumbent is now Coordinate_RF.
- Deck slide 17 says selection/audit “sets never overlap”; this must not be read as pixel- or city-disjoint held-out validation. Historical episode sets share the target population.
- Slide 6's “OFFICIAL 25-SHOT RESULT” is an internally computed audit result, not evidence of organizer scoring.
- Slide 16's causal-sounding “dilution outweighed correction” is a hypothesis, not a proven explanation. Slide 3's performance ceiling below 1 is not quantified.
- Slide 14 says exact stack/cold start ~35 minutes; those historical statements are not a newly verified execution contract, particularly with the selected scaler-shim reference notebooks.
- Historical text says EXP-010 lacks independent replication. Later clean-process paired replay exists on the changed query population; neither is independent-city validation or a second-person attestation of the original audit.
- Baseline notebooks use label-dependent feature construction and non-fold-safe pre-CV scaling. These weaknesses are disclosed and not fixed here.
- Reference preprocessing uses a documented minimal scaler shim. It is not universal sklearn API equivalence. Some embedded reference prose contains text-encoding artifacts.

## Seal definition
MANIFEST.json indexes every payload and generated README/checklist file, with size/type/hash/source/reason. SHA256SUMS.txt covers those files plus MANIFEST.json. A file cannot contain a conventional SHA256 of its own final bytes; self-referential control-file hashes are therefore recorded in an **external seal receipt** under `candidate/team_preparation/`. That receipt hashes every final snapshot file, including both manifest files, and the sibling ZIP. No content changes occur after the atomic directory rename/seal.
