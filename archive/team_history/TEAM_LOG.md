# Team Log

Master chronological project diary. Entries are appended in date order; corrections are appended rather than rewritten.

> **Team status.** One member left the team during Day 2. Ametor Buanyomi covered Member 2, Member 3 and Member 4 scope under Team Lead authorisation. Work is labelled by the scope it belongs to, not by who happened to execute it. **Nothing below has been independently reviewed**, and that gap is itself recorded.

---

**Time:** 2026-09-08, morning (SAST)
**Owner:** M2 — Baseline Engineer
**Task:** Reproduce the organiser baseline faithfully
**Result:** Notebooks 3 and 4 executed with **zero code edits**. Notebook 3 13m28s, Notebook 4 16m15s, both exit 0, 25/25 CV fits verified by counting output lines.
**Decision:** DEC-001, DEC-002
**Evidence:** commit `52c7357`; `docs/member2_log.md`; pickle SHA256 `f6f588c4…5f33`
**Status:** reproduced reference
**Next:** compare against the organiser's published outputs

---

**Time:** 2026-09-08, late morning
**Owner:** M2
**Task:** Explain why reproduced numbers differ from the organiser's
**Result:** All six prototype budgets match to 4 dp; both Random-Forest results differ (Madrid CV +0.0102, zero-shot +0.1006). The prototype path never uses the forest, so it acted as an unintended control isolating the cause to scikit-learn. Determinism verified: **0 of 25,992 predictions differ** across two refits.
**Decision:** DEC-003, DEC-006
**Evidence:** EXP-001, EXP-002; `scripts/determinism_check.py`
**Status:** reproduced reference
**Next:** warn all downstream work to benchmark against 0.6281 / 0.4433

---

**Time:** 2026-09-08, midday
**Owner:** M2
**Task:** Validate the feature contract
**Result:** 24/24 clean-interpreter checks pass. **New finding:** `has_early_data` is constant in both cities — 59 informative features, not 60. The Random Forest independently assigns it importance exactly 0.000000.
**Decision:** DEC-005
**Evidence:** `scripts/validate_pickle.py`
**Status:** reproduced reference
**Next:** flag as a free ablation candidate

---

**Time:** 2026-09-08, afternoon
**Owner:** M3 scope
**Task:** Build a genuinely source-learned transfer path
**Result:** Frozen Madrid transform + Amsterdam prototypes from support labels only. Matched, nested episodes with stored indices; selection trials 0–4, audit 5–9. `rfw` audited at 25/25 paired wins.
**Decision:** DEC-007 … DEC-011
**Evidence:** EXP-003; commit `f9dce46`
**Status:** smoke/development
**Next:** search a wider set of source representations

---

**Time:** 2026-09-08, late afternoon
**Owner:** M3 scope
**Task:** Representation search and final audit
**Result:** Nine representations, eight hypotheses. Top four separated by 0.0012 — **not distinguishable**. `top30` audited: +0.0018 to +0.0072, 19/25 paired wins. Main finding: **the ranking depends on the label budget** — whitening is −0.0218 at 5 shots and +0.0090 at 200. Three negative results recorded.
**Decision:** DEC-012 (binding — no winner claimed)
**Evidence:** EXP-004, EXP-005; commit `96435da`
**Status:** smoke/development
**Next:** validity checks and documentation

---

**Time:** 2026-09-08, evening
**Owner:** M2 / M4 scope
**Task:** Validity checks, figures, documentation
**Result:** Label boundaries confirmed right-closed. Spatial blocking made scores **higher** (mean −0.0160), so no evidence of proximity inflation. Six figures exported. `EXPERIMENT_LOG.md`, member logs, READMEs, `requirements.txt`, presentation outline with abstract (144 w) and justification (287 w).
**Evidence:** commits `115e294`, `4308d0a`, `177f11c`; tag `day1-candidate-v1`
**Status:** reproduced reference / smoke-development as labelled
**Next:** presentation build

---

**Time:** 2026-09-09, morning
**Owner:** M4 scope
**Task:** Build the submission deck; complete lead documentation after a member left
**Result:** 18-slide PowerPoint generated **from the recorded results**, so it cannot drift from the evidence. Decision register populated (DEC-001…014), this log written, submission inventory prepared.
**Decision:** DEC-013, DEC-014 (model frozen)
**Evidence:** `presentation/StatsGeeks_BuildingAge.pptx`
**Status:** planned → in progress
**Next:** rehearsal; Gate S still needs a second person

---

**Time:** Final scientific freeze and packaging
**Owner:** Team scope
**Task:** Inspect, verify provenance, package the frozen EXP-010 state, and align submission materials
**Result:** `joint_sweep.json` arithmetic independently confirms all five tuned/control means, gains and **45/50** paired wins. `final_vs_starter.json` and `shrinkage_chain.json` are partially verified and demoted from headline use. Legacy `stage1_madrid.pkl` was identified as top-30 only; a separate EXP-010 package was created and interface-checked without fitting or prediction. E1/E3 are FALSIFIED and E2 INCONCLUSIVE; E3's independent validator limitation is preserved. Earlier attribution of the local/organiser RF baseline gap is superseded: package/input provenance is incomplete, so the cause remains unidentified and exact organiser reproduction is not claimed.
**Decision:** DEC-015…017
**Status:** final scientific freeze
**Next:** human confirmation of organiser packaging requirements, deck opening, and speaking roles

---

## Standing risks

| Risk | Impact | Owner |
|---|---|---|
| **EXP-010 has not been independently replicated** | Claims must remain limited to the frozen stored audit and arithmetic verification | Team Lead |
| **Gate S needs a different member to run the reload test** | Submission-readiness claim is incomplete | any remaining member |
| Team is short one member | Speaking roles must be reallocated before Thursday | Team Lead |
| Organiser answers missing: time limit, word limit, upload mechanism | Deck timing and packaging unconfirmed | Team Lead |
| Feature generation still label-dependent | Could not serve an unlabelled hidden test set | deferred, documented |
