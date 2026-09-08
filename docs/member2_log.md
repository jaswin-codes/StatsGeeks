# Member 2 Log — Baseline Engineer

**Name:** Ametor Humelo Buanyomi  
**Role:** Faithful reference execution, baseline working copies, feature contract, data-access checks, reproducibility evidence.

Own this log. Duplicate the daily section for Day 1, Day 2, and Thursday. Update before lunch, handoffs, and day close. Do not optimise baseline logic or edit originals. Record every minimum execution deviation and distinguish reference reproduction from later authorised candidate work. Keep bullets concise and do not record credentials or full AI transcripts.

## Daily entry

**Day/date:** Day 1 — 2026-09-08  
**Branch/base commit:** `member2-baseline` @ `165fe11df8779eed514c75bd2852c2b9588a18a4`  
**Current status:** **BASELINE EXECUTION COMPLETE.** Notebook 3 reproduced and validated (13m 28s, 24/24 clean-session checks). Notebook 4 reproduced (16m 15s, 25/25 CV fits, exit 0, 14 figures). Every execution success criterion in `BASELINE_EXECUTION_PLAN.md` passes. **Values match the starter exactly on all non-RF results and differ systematically on all RF results** — cause isolated and proven deterministic (see RUN-M2-002). Awaiting Team Lead review.

### Daily Goals

- [x] Confirm working-copy location and compute-slot ownership with Team Lead
- [x] Verify raw data access and record checksums
- [x] Create/verify faithful working copies of Notebooks 3 and 4
- [x] Record environment, versions, seeds, machine limits
- [x] Run reference Notebook 3; validate 60-feature schema, shapes, labels, pickle reload
- [x] Run reference Notebook 4 in a clean kernel; capture CV / zero-shot / prototype evidence
- [x] Compare reproduced values against starter references and explain any discrepancy

### Completed Tasks

- Confirmed `working/` as the agreed reference working-copy location (Team Lead approved 2026-09-08).
- Confirmed both raw Parquets present in `data/` and readable; recorded sizes and SHA256 (see Evidence).
- Verified `working/3-Preprocessing.ipynb` and `working/4-Modelling.ipynb` are **byte-identical** copies of the `original/` notebooks (SHA256 match) before any edit.
- Verified `original/` is unchanged versus git HEAD (`git status --porcelain original/` empty).
- Captured Python/package versions, CPU count, and platform.
- Cleared stale organiser outputs from both working copies so run evidence is unambiguous (Notebook 4 dropped 6.6 MB → 41 KB; all embedded reference figures removed). Originals retain the starter reference outputs.
- Launched reference Notebook 3 execution via `jupyter nbconvert --execute` with CWD = `working/`. **Completed successfully:** 10:21:20 → 10:34:48 (+02:00), **13m 28s**, exit code 0, 10/10 code cells executed, **zero errors**, peak kernel RSS ≈ 3.6 GB.
- Validated the resulting pickle in a **fresh interpreter** (not the notebook kernel): **24 of 24 checks pass**.
- Launched reference Notebook 4 execution in a clean kernel (nbconvert starts a new kernel per run, so the clean-session requirement is satisfied by construction). **Running at time of writing.**

### Important Decisions

- **DEC-M2-01 (proposed):** Reference working copies live in `working/`, not the `notebooks/` folder assumed by `BASELINE_EXECUTION_PLAN.md`. Rationale: notebooks hardcode `DATA_DIR = '../data'`; running with CWD = `working/` makes `../data` resolve to the repository-root `data/` folder, so **zero path edits are required**. Status: Team Lead approved the location; awaiting formal register entry.
- **DEC-M2-02 (proposed):** Working copies executed in place, so each working copy becomes its own reproduced-run evidence. `original/` remains the untouched starter reference. Status: pending Team Lead confirmation.
- **DEC-M2-03 (escalate):** Installed environment is materially newer than the starter's likely environment (pandas 3.0.5, numpy 2.5.1, scikit-learn 1.9.0). Exact reproduction of starter float values is therefore **not guaranteed**; RF results in particular can shift across scikit-learn versions even with a fixed `random_state`. Status: flagged to Team Lead as a known discrepancy source **before** any comparison is made.
- **DEC-M2-04 (resolved):** `seaborn` will **not** be installed. Team Lead initially approved the install, then approved skipping it once evidence showed it was unnecessary. Rationale: a case-insensitive search for `seaborn`/`sns.` across the entire repository returns zero hits in any notebook — Notebooks 2, 3 and 4 all use plain `matplotlib`. `pip install --dry-run` confirmed the install would have been safe (`Would install seaborn-0.13.2`, every dependency already satisfied, no numpy/pandas/matplotlib change), so this was a bookkeeping decision, not a risk one: per `AGENTS.md`, a dependency without a documented task-specific purpose should not enter the environment or the submission's dependency record. Environment recorded above stands unchanged.

- **DEC-M2-05 (escalate):** Feature `has_early_data` is constant across both cities and carries no information (full detail under Known reference deficiencies). Decision needed: leave the reference untouched (my recommendation — it is inert and removing it would break faithful reproduction) while flagging it to Member 3 as a free feature-ablation candidate, and correcting "60 features" to "59 informative + 1 dead" wherever the count is quoted in slides or the justification. Status: awaiting Team Lead.
- **DEC-M2-06 (resolved by evidence):** Reproduced RF-path values differ from the organiser's published figures. Established by control and by a two-run determinism test that the difference is **systematic and stable**, not a failed reproduction — see RUN-M2-002. Consequence: this machine's values become the team's comparison datum. Status: recorded; Team Lead to confirm the environment policy (see Open questions).

### Problems Encountered

- **BLOCKER (open) — cannot push to origin; no write access to the team repository.** `git push origin member2-baseline` fails with:
  > `remote: Permission to jaswin-codes/StatsGeeks.git denied to BuanyomiAmetor.`
  > `fatal: unable to access 'https://github.com/jaswin-codes/StatsGeeks.git/': The requested URL returned error: 403`

  The remote is Jaswin's personal repository. Git authenticated correctly as `BuanyomiAmetor`; that account simply lacks write permission. Note `origin/member2-baseline` already exists at `165fe11`, so the branch was created for me but collaborator access was never granted.
  - **Impact:** commit `eab0bf1` is safe locally and the branch is 1 ahead of origin — no work is at risk — but the Team Lead **cannot review the baseline evidence** and the Member 3 / Member 4 handoffs are blocked until this is resolved.
  - **Fix required (repo owner only):** Jaswin adds `BuanyomiAmetor` as a collaborator with **Write** access (repo → Settings → Collaborators → Add people), then I retry the push.
  - **Escalated to Team Lead.** Recommend checking whether Members 3 and 4 have the same problem — if the repo was set up from one account, they are likely blocked too and may not have discovered it yet. Worth resolving now rather than at the Day 1 merge checkpoint.

- `seaborn` is not installed. **Impact: none.** Verified by repository-wide search that no notebook imports it — Notebooks 3 and 4 use only `numpy`, `pandas`, `matplotlib`, `sklearn`, `pickle`, `pathlib`, and Notebook 2 (EDA, not in the reference execution path) does not use it either. Deliberately left uninstalled — see DEC-M2-04.
- `data/Open Notebook.onetoc2` was showing as modified; it is a OneNote index file that OneDrive rewrites in the background (binary, zero real content change). Restored to the committed version to keep the working tree clean. No project impact.
- Benign warnings during kernel start (zmq Proactor event-loop `RuntimeWarning`; IPKernelApp plain-TCP notice). Recorded for completeness; neither affects computation.

### AI Prompts Used (one-line summary only)

- Recover prior-session project context and read the six assigned "Read First" documents; no files modified.
- Capture environment/version/checksum evidence and verify working copies match originals; read-only inspection plus this log.
- Clear stale outputs and launch the reference Notebook 3 run with unchanged baseline logic; allowed files limited to `working/3-Preprocessing.ipynb`, `working/4-Modelling.ipynb`, `docs/member2_log.md`.

### Files Modified

- `working/3-Preprocessing.ipynb` — outputs cleared, then executed in place. **No source-code changes; no path edits.**
- `working/4-Modelling.ipynb` — outputs cleared. Execution pending. **No source-code changes.**
- `docs/member2_log.md` — this log.
- `data/Open Notebook.onetoc2` — restored to committed state (OneDrive churn, not a project edit).
- Originals in `original/` and both raw Parquets: **unchanged and verified unchanged.**

### Evidence Produced

**Deviation list from the organiser notebooks: ZERO code deviations.** The only execution-compatibility measure was choosing the working directory (`working/`), which required no edit. Outputs were cleared, which does not alter logic.

Raw input checksums:

| File | Bytes | SHA256 |
|---|---:|---|
| `data/madrid_train.parquet` | 141,959,981 | `0e106a07044d867f8c68e77de8c36826c491d0f26692b8cde753d1046ce24c9c` |
| `data/amsterdam_data.parquet` | 43,840,149 | `32388f3a9792b01d9831ca4d0fc4bfadba132a1c23c06e372d7a82e985be0719` |

Working-copy provenance (pre-execution, verified identical to `original/`):

| Notebook | SHA256 (prefix) |
|---|---|
| `3-Preprocessing.ipynb` | `86136f0ab901a4fd…` |
| `4-Modelling.ipynb` | `3a279782c6e03e8a…` |

Environment:

| Item | Value |
|---|---|
| Python | 3.13.15 (`C:\Users\range\AppData\Local\Python\pythoncore-3.13-64\python.exe`) |
| numpy / pandas / scikit-learn | 2.5.1 / 3.0.5 / 1.9.0 |
| scipy / pyarrow / matplotlib / joblib | 1.18.1 / 25.0.1 / 3.11.1 / 1.6.0 |
| nbconvert / nbformat / jupyter_core | 7.17.1 / 5.11.1 / 5.9.1 |
| seaborn | not installed (unused by Notebooks 3–4) |
| Platform / CPU | Windows-11-10.0.26200-SP0 / 16 logical CPUs |

Seeds and settings fixed by the reference code (unchanged): `RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)`; `RandomForestClassifier(n_estimators=500, class_weight='balanced', random_state=42, n_jobs=-1)`; prototype sampler `np.random.default_rng(42)`, 10 trials at 5/10/25/50/100/200 shots per class.

**Status labels:** the setup evidence above, plus the Notebook 3 evidence below, is **reproduced reference**. All Notebook 4 scores (Madrid CV 0.6179 ±0.0043; Amsterdam zero-shot 0.3427; prototypes 0.5437 / 0.5649 / 0.5986 / 0.6079 / 0.6129 / 0.6150) remain **starter reference only** until that run completes.

#### RUN-M2-001 — Notebook 3 reference preprocessing — REPRODUCED

Config: `working/3-Preprocessing.ipynb`, CWD `working/`, unmodified organiser logic, commit `165fe11`, environment as tabled above. Preprocessing contains no RNG, so it is deterministic and an exact match is the correct expectation.

Output artifact (**not committed** — `.gitignore` excludes `data/preprocessed/` and `*.pkl`):

| Field | Value |
|---|---|
| Path | `data/preprocessed/preprocessed_data.pkl` |
| Size | 50,721,885 bytes (48.4 MB) — matches the starter's saved "48.4 MB" |
| SHA256 | `f6f588c4e3cfa2e0793354bc7772228bd4c749b39fce67bde5302f4c63955f33` |
| Runtime | 13m 28s |

Reproduced values versus the audit's documented dataset facts — **every figure matches exactly**:

| Quantity | Reproduced | Audit reference | Match |
|---|---|---|---|
| Madrid raw rows × cols | 3,172,765 × 48 | 3,172,765 × 48 | ✔ |
| Amsterdam raw rows × cols | 1,062,877 × 48 | 1,062,877 × 48 | ✔ |
| Madrid / Amsterdam pixels | 76,263 / 25,992 | 76,263 / 25,992 | ✔ |
| Acquisition years | 1984–2025 (42) | 1984–2025 (42) | ✔ (confirms data runs to **2025**, not 2024) |
| Madrid classes 1/2/3/4 | 13,794 / 27,152 / 18,672 / 16,645 | same | ✔ |
| Amsterdam classes 1/2/3/4 | 7,568 / 8,802 / 6,745 / 2,877 | same | ✔ |
| Madrid / Amsterdam X shape | (76263, 60) / (25992, 60) | same | ✔ |

Also reproduced: Blue > 15,000 haze filter removed **34,845** Madrid and **12,917** Amsterdam pixel-year rows; gap-fill produced 3,203,046 Madrid and 1,091,664 Amsterdam rows (42 years × pixels, complete); 0 pixels lacking early data and 163 Madrid / 7 Amsterdam lacking late data; NaN check OK for both cities. **Class 2 is the largest class in both cities**, confirming the audit's correction to the starter's stale prose.

Clean-session validation (fresh interpreter, `validate_pickle.py`, 24/24 pass): all 9 pickle keys present; exact ordered 60-feature schema; `feat_groups` concatenate to the same ordered list; exactly 4 classes per city; zero non-finite cells; pixel-key arrays row-aligned and unique (76,263 / 25,992 distinct keys); scaler fitted on 60 features and 76,263 Madrid samples; Madrid standardised to mean 1.4e-15 and unit std across all 59 non-constant columns.

#### RUN-M2-002 — Notebook 4 reference modelling — REPRODUCED, with a systematic RF-path difference

Config: `working/4-Modelling.ipynb`, clean kernel (nbconvert starts a fresh kernel per run), CWD `working/`, unmodified organiser logic, input = the RUN-M2-001 pickle above. Executed 10:36:55 → 10:53:10 (+02:00), **16m 15s**, exit 0, 14/14 code cells, **zero errors**, 14 figures rendered, ~15× parallelism across 16 cores.

**Completion evidence (not just the summary line):** the individual `Fit N/25` output lines were counted — **25 of 25 present**, per-fit macro F1 spanning 0.6205–0.6363. No parameter was reduced to save time; all six prototype budgets ran at 10 trials each.

| Result | Reproduced (this machine) | Starter reference | Delta |
|---|---|---|---|
| Madrid CV macro F1 | **0.6281 ±0.0043** | 0.6179 ±0.0043 | +0.0102 (2.37× the fold std) |
| Final RF in-sample accuracy | 0.9999 | ~1.0 expected | ✔ |
| Amsterdam zero-shot | **0.4433** | 0.3427 | +0.1006 |
| Prototypes 5/class | 0.5437 ±0.0324 | 0.5437 ±0.0324 | **0.0000** |
| Prototypes 10/class (diagnostic) | 0.5649 ±0.0312 | 0.5649 ±0.0312 | **0.0000** |
| Prototypes 25/class | 0.5986 ±0.0176 | 0.5986 ±0.0176 | **0.0000** |
| Prototypes 50/class | 0.6079 ±0.0101 | 0.6079 ±0.0101 | **0.0000** |
| Prototypes 100/class | 0.6129 ±0.0097 | 0.6129 ±0.0097 | **0.0000** |
| Prototypes 200/class | 0.6150 ±0.0036 | 0.6150 ±0.0036 | **0.0000** |

**The discrepancy is isolated, not diffuse.** Every result that touches the Random Forest differs; every result that does not touch it matches the starter to four decimal places in both mean and standard deviation, across all six budgets.

That split is itself the diagnostic. The prototype path — precisely because of the documented defect that it never uses the fitted RF — acts as an unintended **control variable**: it exercises the entire data pipeline (parquet load, labelling, QA filter, gap-fill, all 60 features, the Madrid-fitted scaler) and the numpy seed-42 support sampler, while touching zero scikit-learn tree code. Its exact match is positive evidence that the data path and RNG are bit-identical to the organiser's, which leaves **scikit-learn's Random Forest implementation as the only remaining source of divergence**. This confirms DEC-M2-03, which was raised *before* any number was seen.

**Determinism proof (`determinism_check.py`).** A difference that does not repeat would make 0.6281 noise rather than a reference. The final Madrid RF was refitted twice from a separate process with identical settings:

- run 1 zero-shot macro F1 = `0.4432736088`; run 2 = `0.4432736088`
- **0 of 25,992 predictions differ**; probability matrices bit-identical; F1 delta exactly `0.00e+00`
- Independently reproduces the notebook's 0.4433 from a separate process — a third confirmation

**Conclusion: the RF gap is systematic and stable, not run-to-run noise.** The reproduced values are therefore usable as a fixed reference datum on this hardware.

Zero-shot per-class detail (reproduced), showing the domain-shift signature:

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| 1 (Pre-1945) | 0.4635 | 0.4223 | 0.4420 | 7,568 |
| 2 (1945–1984) | 0.3862 | 0.6489 | 0.4843 | 8,802 |
| 3 (1984–2004) | **0.7741** | **0.1870** | 0.3012 | 6,745 |
| 4 (2004–2024) | 0.5659 | 0.5269 | 0.5457 | 2,877 |

Class 3 is the clearest failure: the Madrid model almost never predicts it in Amsterdam (recall 0.19) but is usually right when it does (precision 0.77), while Class 2 is over-predicted (recall 0.65 on precision 0.39). The Madrid-trained forest dumps Amsterdam pixels into Class 2. Note also that accuracy (0.4496) exceeds macro F1 (0.4433) — reporting accuracy here would flatter the result.

Top RF features (reproduced): `NIR_early_mean` (0.0387), `Red_late_std` (0.0304), `NIR_mean` (0.0284), `UI_mean` (0.0263), `Red_std` (0.0259). No single feature exceeds 4% importance, so the signal is broadly distributed rather than carried by one band.

### Known reference deficiencies (recorded, deliberately NOT fixed inside the reference run)

Confirmed present by direct code reading of `working/3-Preprocessing.ipynb` and `working/4-Modelling.ipynb`:

- **Global scaling before CV.** `StandardScaler` is fitted on all Madrid rows in Notebook 3, before Notebook 4 creates CV folds. Not fold-safe.
- **Label-dependent feature construction.** `build_pixel_features` filters on `age_class.notna()` and includes `age_class` in the `groupby` key, so features cannot currently be generated for unlabelled/hidden-test pixels.
- **Target-only prototypes.** `prototype_predict` computes class means directly from Amsterdam support vectors; `rf_final` is never used in that path. Madrid contributes feature scaling only. **This is not genuine supervised transfer** and must not be described as such.
- **No saved artifacts.** Notebook 4 saves no final RF, no predictions, no scores, no adaptation state. Only `data/preprocessed/preprocessed_data.pkl` persists.
- **Sampler quirks.** One advancing RNG across budgets and trials, so episodes are neither recorded nor nested/matched across budgets; `min(n_shots, len(cls_idx))` would silently shrink a budget (not triggered here — smallest Amsterdam class has 2,877 pixels).
- **Map overwrite.** Madrid OOF spatial maps write 5 repeats' worth of predictions into one grid; duplicate pixels overwrite rather than average.

- **NEW FINDING (not in the team audit) — the feature set is effectively 59 features, not 60.** Feature index 58, `has_early_data`, is **constant 1.0 for every pixel in both cities** (76,263/76,263 Madrid and 25,992/25,992 Amsterdam). It has zero variance, so it carries no information anywhere and cannot contribute to any model. `StandardScaler` leaves zero-variance columns untouched (`scale_ = 1`), so it survives standardisation as a constant column rather than being flagged. Its companion `has_late_data` is *nearly* constant too: only **163 Madrid (0.21%)** and **7 Amsterdam (0.03%)** pixels take the value 0.
  - **Cause:** both indicators are computed correctly *before* gap-filling, but every retained pixel happens to have at least one real observation in 1984–2003, so the early indicator can only ever be 1. The starter's own diagnostic prints `has_early_data=0: 0 pixels` for both cities and moves on without noticing the feature is therefore dead.
  - **Impact on the reference run: none.** A constant column cannot change a Random Forest's splits or a Euclidean prototype distance. It does **not** invalidate any baseline number, and it must **not** be removed from the reference.
  - **Why it matters anyway:** the "60 features" figure appears in the plan and will appear in slides; the honest number is **59 informative + 1 dead**. It is also a ready-made, evidence-backed feature-ablation candidate for Member 3 under a separate authorised task, and a concrete example of the kind of unexamined assumption the audit warned about. Escalated to Team Lead for the decision register.

### HANDOFF — read before any Day 2 comparison

> **⚠ Benchmark against 0.6281 and 0.4433, NOT the organiser's 0.6179 and 0.3427.**
>
> On this hardware and environment the reference baseline is **Madrid CV 0.6281 ±0.0043** and **Amsterdam zero-shot 0.4433**. The organiser's published figures were produced on a different scikit-learn and are ~0.010 and ~0.101 lower respectively.
>
> A candidate benchmarked against the published numbers would be credited with roughly **+0.10 of zero-shot "improvement" that is purely a library difference**. That would put a false claim in the submission and is exactly the kind of unsound comparison the rubric penalises. The prototype budgets are unaffected — those match the starter exactly and can be compared against either source.

**Feature contract for Member 3** (frozen, from RUN-M2-001): 60 ordered features in the exact order stored in `feature_names`; Madrid `(76263, 60)`, Amsterdam `(25992, 60)`; labels 1–4 in both; `pixel_ids_*` row-aligned and unique; no NaN/inf; Madrid-fitted `StandardScaler` included. Artifact `data/preprocessed/preprocessed_data.pkl`, SHA256 `f6f588c4…5f33`, 48.4 MB, **not in Git** — regenerate with Notebook 3 (13m 28s) or copy from this machine. Caveat: `has_early_data` is constant and carries no information; treat the usable width as 59.

### Next Steps

1. Request Team Lead review of RUN-M2-001 and RUN-M2-002 via `docs/REVIEW_CHECKLIST.md`, scope = **reference reproduction**.
2. Send DEC-M2-01…05 to Team Lead for `DECISION_REGISTER.md` (this log is the evidence).
3. Commit reviewed working copies and this log. Do **not** commit the pickle or figures.
4. Ask Team Lead to record in `MASTER_PLAN.md` that priorities 1–4 are now evidenced, and that the environment-drift caveat governs all later comparisons.
5. Hand the feature contract to Member 3 and the results/figures to Member 4 for evidence packaging.
6. **Not started and explicitly out of scope for this task:** any correctness or transfer work. Gate O has not been assessed and no optimisation is authorised by this run.

### Open questions for the Team Lead

- Should the team pin an environment (e.g. the organiser's scikit-learn) to reproduce the published numbers exactly, or accept this machine's values as the team datum and document the drift? **Recommendation: accept and document.** The published numbers are not required to be matched, all comparisons will be internal and matched-episode, and pinning an old scikit-learn risks breaking the pandas 3.0 / numpy 2.5 stack that the data path currently reproduces exactly.
- Does the constant `has_early_data` feature (DEC-M2-05) warrant a Member 3 ablation, given it is free evidence of an unexamined starter assumption?

### Reflection

- The reference pipeline's biggest trap is that it *looks* like transfer learning while doing none: Madrid supplies only the scaler's mean/variance, and the Amsterdam prototypes are fitted from Amsterdam data alone. The Madrid Random Forest is trained, evaluated, used zero-shot — and then abandoned. Rising F1 with more Amsterdam labels measures the target-only prototype learner getting more data, not knowledge moving between cities.
- The limitation that must not be mistaken for a completed submission: **nothing in this baseline is saved or reloadable except the preprocessed pickle.** There is no Stage 1 artifact, so the deliverable "saved Madrid model consumed by an adaptation script" does not yet exist in any form.
- Reproduction discipline note: the environment here is much newer than the starter's, so matching numbers was a hypothesis to test, not an expectation. That turned out to be the day's main finding.
- **What I learned about the reference pipeline.** The most useful evidence came from the starter's own worst defect. Because the prototype path never touches the Random Forest, it functioned as a control: it exercised the whole data pipeline and the RNG while avoiding scikit-learn's trees, and its exact match to the starter proved the divergence was confined to the forest. A flaw in the code under test became the instrument that diagnosed it. I would not have designed that experiment deliberately — it was available only because the defect had already been documented carefully.
- **On not stopping at a plausible story.** Once the RF-versus-non-RF split appeared, "it's the scikit-learn version" was a satisfying explanation and I could have written it up there. But a systematic version difference and an unrepeatable run produce the *same* symptom, and they have opposite consequences: one leaves a usable datum, the other means the baseline is worthless and every Day-2 comparison built on it is meaningless. Refitting twice cost about 95 seconds and converted a plausible story into a checked one. The habit worth keeping is asking what *else* would produce this same evidence.
- **The mistake I made and what it cost.** My first validator failed a check because a standardised column had zero variance. I had encoded my expectation ("all columns end up unit-variance") rather than the tool's documented behaviour (`StandardScaler` leaves zero-variance columns alone). The fix was to correct the check, not the data — but the false alarm is what exposed the constant `has_early_data` feature, which no one had noticed. Worth remembering that a check failing does not establish which of the check and the thing checked is wrong.
