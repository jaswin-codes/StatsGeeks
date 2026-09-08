# StatsGeeks Data Science Hackathon 2026

> Team repository for the StatsGeeks Hackathon. This repository contains the organiser baseline, project documentation, working copies, and team workflow.

---

# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/jaswin-codes/StatsGeeks.git
cd StatsGeeks
```

---

## 2. Obtain the datasets

The organiser datasets are **not included** in this repository because GitHub limits file sizes to 100 MB.

Copy the following files into the `data/` directory:

```
data/
├── madrid_train.parquet
└── amsterdam_data.parquet
```

These files are available from the hackathon VM (IDIA) provided by the organisers.

---

## 3. Read the documentation

Everyone should read:

```
docs/TEAM_OPERATING_SYSTEM.md
```

Then read **only your assigned mission**:

```
docs/member1_mission.md
docs/member2_mission.md
docs/member3_mission.md
docs/member4_mission.md
```

---

## 4. Create your branch

```
git checkout -b memberX-feature
```

Examples:

```
member2-baseline
member3-modelling
member4-research
```

---

## 5. Start working

- Do **NOT** modify anything inside `original/`
- Work only inside the assigned folders/files.
- Follow your mission document.
- Update your member log throughout the day.
- Commit regularly with meaningful messages.

---

# Repository Structure

```
.
├── data/                  # Local datasets (not tracked by Git)
├── docs/                  # Project documentation
├── original/              # Original organiser notebooks (read-only)
├── working/               # Team working copies
└── README.md
```

---

# Documentation

| Document | Purpose |
|----------|---------|
| TEAM_OPERATING_SYSTEM.md | Team workflow |
| MASTER_PLAN.md | Overall project strategy |
| BASELINE_EXECUTION_PLAN.md | Baseline implementation plan |
| PARALLEL_EXECUTION_MAP.md | Team execution timeline |
| REVIEW_CHECKLIST.md | Code review checklist |
| TEAM_LOG.md | Team project diary |
| DECISION_REGISTER.md | Important project decisions |
| EXPERIMENT_LOG.md | Experiment tracking |

---

# Rules

✅ Preserve all files in `original/`

✅ Work from assigned copies only

✅ Document important decisions

✅ Record experiments

✅ Keep commits small and descriptive

❌ Never overwrite another member's work

❌ Never commit datasets or generated artifacts

❌ Never claim results that have not been reproduced

---

# Team Workflow

1. Clone repository
2. Read the Team Operating System
3. Read your mission
4. Create your branch
5. Implement your assigned work
6. Update documentation
7. Commit changes
8. Submit for Team Lead review
9. Merge after approval

---

# Notes

This repository is structured to prioritise:

- Reproducibility
- Parallel development
- Minimal merge conflicts
- Clear documentation
- Strong presentation evidence

The goal is not only to build a good solution, but also to produce a solution that the team can confidently explain, reproduce, and defend during judging.
