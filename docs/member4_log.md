# Member 4 Log — Research & Presentation Engineer

**Name:** Ametor Humelo Buanyomi *(covering Member 4 scope from 2026-09-09, after a member left the team. Team Lead authorised working across roles on 2026-09-08.)*
**Role:** Evidence curation, rubric compliance, presentation and justification, run instructions, independent verification support.

## Daily entry

**Day/date:** Day 2 — 2026-09-09
**Branch/base commit:** `member2-baseline` @ `177f11c`
**Current status:** Deck built, inventory and run instructions complete. **Rehearsal and independent verification outstanding.**

### Daily Goals

- [x] Build the PowerPoint with a ≤150-word first-slide abstract
- [x] Draft the written justification covering all three required pillars
- [x] Produce the F1 vs log₂(budget) curve with error bars
- [x] Assemble the submission inventory and cold-start run instructions
- [x] Populate the lead documentation left empty by the departure
- [ ] Timed rehearsal
- [ ] Export PDF and confirm it opens offline
- [ ] Reallocate speaking roles

### Completed Tasks

- Built `presentation/build_deck.py` → **18 slides**, 412 KB. Every number is **read from `candidate/artifacts/*.json` at build time**, so the deck cannot drift from the evidence. Re-running the script after any result change regenerates it correctly.
- Abstract **144 words** (limit 150) and justification **287 words** — counted by script, not estimated. 287 satisfies both the 300-word Notebook 1 limit and the 500-word rubric limit, since that conflict is unresolved.
- Deck covers all three required pillars: model design, transfer strategy, F1 interpretation.
- Three backup slides: reproducibility, the version-drift diagnosis, the episode protocol.
- Wrote `docs/SUBMISSION_INVENTORY.md` — every deliverable, what is not in git, and a ≈35-minute cold-start reproduction path with the pickle checksum to verify features match.
- Populated `docs/DECISION_REGISTER.md` (DEC-001…014) and `docs/TEAM_LOG.md`, both previously blank templates.

### Important Decisions

- **DEC-013.** Installed `python-pptx` to generate the required PowerPoint. `pip --dry-run` first confirmed no existing package would be upgraded, so numpy/pandas/scikit-learn are untouched and every reported number stays reproducible. Verified after install.
- **DEC-014 (binding).** Model frozen. No further modelling before the presentation — the audit set has already informed two decisions and a third pass would compromise what can honestly be claimed.
- Deck is **generated, not hand-built**. A hand-typed deck drifts from the evidence the moment a number changes; a generated one cannot.

### Problems Encountered

- **A member left the team.** Speaking roles are still allocated M1–M4 in the deck and outline. **They must be reallocated before Thursday** — the rubric requires meaningful contributions and speaking roles from every remaining member, and the deck currently implies four speakers.
- **Gate S remains impossible to satisfy alone.** It explicitly requires the reload test to be run by someone other than its author. Recorded as an open gap on slide 14 and in the inventory rather than quietly dropped.
- **Nothing has been reviewed by a second person.** Gate M cannot pass as written either. This is disclosed, not concealed.

### AI Prompts Used (one-line summary only)

- Generate the submission deck from recorded results; allowed files limited to `presentation/`.
- Populate the decision register, team log, submission inventory and this log from existing evidence.

### Files Modified

- `presentation/build_deck.py`, `presentation/StatsGeeks_BuildingAge.pptx` — new
- `docs/DECISION_REGISTER.md`, `docs/TEAM_LOG.md` — were blank templates
- `docs/SUBMISSION_INVENTORY.md`, `docs/member4_log.md` — new
- `requirements.txt` — added python-pptx
- **Unchanged:** organiser originals, raw data, `working/` reference copies, all `candidate/` results

### Evidence Produced

| Deliverable | State |
|---|---|
| PowerPoint, 18 slides | ✅ abstract 144 w |
| Written justification | ✅ 287 w, three pillars |
| F1 vs log₂(budget) with error bars | ✅ `fig1_learning_curve.png` |
| Results table, all five budgets | ✅ on slide 9, from `final_audit.json` |
| Submission inventory + run instructions | ✅ ≈35 min cold start |
| Backup slides | ✅ three |

### Next Steps

1. Timed rehearsal once the organiser confirms the limit — built for 10 min, three slides marked cuttable for 5.
2. Export PDF; confirm it opens offline with no live dependency.
3. Reallocate speaking roles across the remaining members.
4. Back up the two large local files.
5. If a second person becomes available, have them run `python candidate/reload_test.py`.

### Reflection

- Generating the deck from the results JSON rather than typing it was the right call under time pressure. The numbers on the slides are the numbers in the artifacts by construction, so the class of error where a slide quietly disagrees with the evidence cannot happen.
- The honesty slides are load-bearing, not decoration. Under a rubric that can deduct 20 points for unsoundness, volunteering the two-audit disclosure and the small effect size before a judge finds them is worth more than the +0.007 itself.
- The limitation that matters most for Thursday is not technical: **no part of this work has been checked by another person.** Every gate in the team's own operating system assumes a second pair of eyes, and the departure removed that. It is stated on slide 14 rather than hidden.
