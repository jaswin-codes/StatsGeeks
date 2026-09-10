# Team preparation and submission safety

**Preparation only. No ML fitting, prediction, optimization or notebook execution.**

## Read in this order
1. [Tonight revision](TONIGHT_REVISION.md) — quick shared facts and 20 likely questions.
2. [Project master guide](PROJECT_MASTER_GUIDE.md) — approximately 13,000 words, complete evidence narrative and 66 structured questions across 22 categories.
3. Exactly three role-specific packs: [Member 1](MEMBER_1_GUIDE.md), [Member 2](MEMBER_2_GUIDE.md), [Member 3](MEMBER_3_GUIDE.md).
4. [Presentation Q&A](PRESENTATION_QA.md) — hard questions with defensible short answers.
5. [Consistency audit](CONSISTENCY_AUDIT.md) — stale claims, protocol differences and unresolved issues.

Speaking coverage is balanced; implementation credit is not fabricated. Member 1 is integration/problem scope, Member 2 method scope, Member 3 evaluation scope. The third presenter's personal contribution is not identified in the inspected records.

## Immutable fallback
- [Snapshot directory](../SUBMISSION_SAFETY_SNAPSHOT/README.md)
- [Clean sealed ZIP](../SUBMISSION_SAFETY_SNAPSHOT.zip)
- [Full external seal](SNAPSHOT_SEAL.json)
- [Protection / background metadata exception](SNAPSHOT_PROTECTION.json)
- [Inspection and selection decision](INSPECTION_AND_SUBMISSION_DECISION.md)
- [Final validation](FINAL_VALIDATION.json)

The **13 intended files and clean ZIP are protected and verified**. A background OneNote process added seven index files to the directory after sealing; they were not deleted or incorporated into a new seal. The original ZIP excludes them. Read-only flags plus granular NTFS deny-write/delete permissions protect the snapshot/ZIP; owner/admin privileges can reverse this, so it is not WORM storage.

**Submission-readiness gap:** the existing presentation/justification describe EXP-010; the included notebooks are audited references, not final EXP-010/Coordinate_RF notebooks. No final-method notebook was found or invented. Current Coordinate_RF remains the research incumbent, not the method in that old deck. The organizer asks for presentation, explanation included in the presentation, and final notebooks, emailed to **uctstatsgeekssociety@uct.ac.za**. Nothing was emailed by this task.

## Evidence catalogs
[Notebook inventory](NOTEBOOK_INVENTORY.json), [deliverable inventory](DELIVERABLE_INVENTORY.json), [existing slide text](EXISTING_PRESENTATION_TEXT.json), [Git history](GIT_HISTORY_EVIDENCE.txt), [forensic-source references](FORENSIC_SOURCE_REFERENCES.json), [question bank](QUESTION_BANK.json).

`PROJECT_NARRATIVE.md` and `question_bank.py` are authored source material assembled into the master by `build_master_guide.py`; they are not additional member packs. `create_safety_snapshot.py` is a one-time builder that now refuses to run because the snapshot exists. Never delete the snapshot to rerun it.

## Read-only verification
From the repository root:

```bash
python -B candidate/team_preparation/verify_preparation.py
```

This reads hashes, validates ZIP extraction/static notebook syntax and checks guide coverage/numbers. It writes reports only here, never inside the snapshot. It does not run model code or notebooks. Full nbformat schema validation was unavailable due an existing dependency-resource import error; no package repair was attempted.

[Future-work guardrails](NEXT_TASK_GUARDRAILS.md) explain the preserved boundaries. This task stops at preparation; it does not start overnight discovery.
