# Decision Register

Record important technical, evaluation, scope, ownership, resource, and organiser-rule decisions before acting. The proposer supplies the entry; the Team Lead assigns the ID and accepts shared decisions.

Status options: Proposed, Accepted, Blocked, Rejected, Superseded. Preserve history: a replacement receives a new ID and links to the superseded entry.

> **Note on authorship.** Entries DEC-001 to DEC-014 were proposed by Ametor Buanyomi covering Member 2, 3 and part of Member 4 scope, under Team Lead authorisation on 2026-09-08 after the baseline finished early. One member has since left the team. **Most entries remain Proposed rather than Accepted** — they have not been independently reviewed. Do not read "Proposed" as "agreed".

| ID | Date | Owner | Decision | Reason | Evidence | Impact | Status |
|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-09-08 | M2 | Reference working copies live in `working/`, run with CWD `working/` | The notebooks hardcode `DATA_DIR='../data'`; running from `working/` resolves it, so **zero path edits** are needed | commit `52c7357` | No code deviation from the organiser baseline | Proposed |
| DEC-002 | 2026-09-08 | M2 | Execute working copies in place, so each becomes its own run evidence | `original/` retains the starter's saved outputs as the untouched reference | `working/*.ipynb` | Reference outputs preserved separately | Proposed |
| DEC-003 | 2026-09-08 | M2 | Treat library version drift as a known discrepancy source, flagged **before** any comparison | pandas 3.0.5 / numpy 2.5.1 / sklearn 1.9.0 are far newer than the organiser's; RF results shift across versions even with a fixed seed | `docs/EXPERIMENT_LOG.md` EXP-001 | All later comparisons must use our numbers, not the published ones | Accepted (evidence-backed) |
| DEC-004 | 2026-09-08 | M2 | Do **not** install seaborn | Repository-wide search shows no notebook imports it. `pip --dry-run` confirmed the install was safe, so this was bookkeeping, not risk: `AGENTS.md` forbids dependencies without a documented purpose | `docs/member2_log.md` | Dependency record stays minimal | Accepted |
| DEC-005 | 2026-09-08 | M2 | Leave the constant `has_early_data` feature in place | It is inert (zero variance in both cities, RF importance exactly 0.000000). Removing it would break faithful reproduction | `scripts/validate_pickle.py` | Quote **59 informative features**, not 60, in all outputs | Proposed |
| DEC-006 | 2026-09-08 | M2 | Accept this machine's values as the team datum rather than pinning the organiser's scikit-learn | Comparisons are internal and matched; pinning an old sklearn risks the pandas 3.0 stack that currently reproduces the data path exactly | EXP-001, EXP-002 | Benchmark against **0.6281 / 0.4433** | Proposed |
| DEC-007 | 2026-09-08 | M3 | Candidate work lives in `candidate/`, entirely separate from `working/` | One owner per file; the reference must stay recoverable | commit `f9dce46` | No reference file modified | Proposed |
| DEC-008 | 2026-09-08 | M3 | Store episode support **indices**, not a seed | A seed only reproduces in an identical environment — EXP-001 is direct evidence that this fails | `candidate/artifacts/episodes.npz` | Episodes reproducible across machines and library versions | Proposed |
| DEC-009 | 2026-09-08 | M3 | Budgets are **nested**: support(5) is a subset of support(25), etc. | A budget increase then adds pixels and changes nothing else, so gains are attributable to data volume rather than draw luck | `candidate/transfer_candidate.py` | Accepted cost: curve points are correlated, not independent | Proposed |
| DEC-010 | 2026-09-08 | M3 | The comparison baseline is **target-only prototypes on identical episodes**, not zero-shot | Beating zero-shot demonstrates nothing about transfer | EXP-003 | The claim rests on the right control | Proposed |
| DEC-011 | 2026-09-08 | M3 | Exclude the 244 MB source RF from the adaptation artifact | Adaptation needs only the 60 importance weights and the selected subset; the shipped artifact is 3 KB | `candidate/artifacts/stage1_madrid.pkl` | Artifact is portable and committable | Proposed |
| DEC-012 | 2026-09-08 | M3 | **Do not claim any single representation is best** | Two methods were audited (`rfw`, `top30`). Each cycle was individually clean, but choosing between them on audit scores would be selection on audit data | EXP-005 | The reported claim is deliberately the weaker, defensible one | **Accepted — binding** |
| DEC-013 | 2026-09-09 | M2 | Install `python-pptx` to generate the required PowerPoint | PowerPoint is an explicit deliverable and a member has left. `pip --dry-run` confirmed no existing package is upgraded, so the reproducibility stack is untouched | `requirements.txt`, `presentation/build_deck.py` | Deck generated from recorded results, cannot drift from evidence | Proposed |
| DEC-014 | 2026-09-09 | M2 | Freeze the model. No further modelling before the presentation | The audit set has already informed two decisions; a third selection pass would compromise what can honestly be claimed | DEC-012, EXP-005 | Day 2 is presentation and rehearsal only | **Accepted — binding** |

## Open decisions requiring organiser input

| Topic | Question | Provisional handling |
|---|---|---|
| Presentation | Time limit? | Built for 10 minutes; three slides marked cuttable for 5 |
| ~~Justification word limit~~ | **RESOLVED 2026-09-09: 500 words.** | Submission version is 467 words. A 269-word fallback is retained if a shorter limit is ever imposed. |
| Submission | Upload mechanism, deadline, required artifact formats? | Inventory prepared in `docs/SUBMISSION_INVENTORY.md`; do not invent requirements |
