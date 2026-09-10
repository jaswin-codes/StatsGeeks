# Final Validation Report

## Organizer-style verdict

**CONDITIONAL FAIL — do not upload without manual rule/format review.** Scientific consistency and byte integrity pass. Submission policy and presentation-format gates remain unresolved.

## Strict validator checklist

| Check | Result | Evidence / issue |
|---|---|---|
| Required core files exist | Pass | PPTX, PDF, explanation, notebook, requirements, README, manifest, checksums, model and wrapper present |
| Filenames correct | Conditional | Names are clear, but official organizer naming rules were not supplied |
| PPTX opens structurally | Pass | Valid Office ZIP; 16 slide XML parts |
| PDF opens/renders | Pass | Valid PDF 1.7, 16 pages; existing page renders visually inspected |
| Notebook valid | Pass | nbformat 4.5; JSON parses; all four code cells compile |
| Report internally consistent | Pass | Coordinate-RF and 0.749299 ± 0.005716 consistent |
| README complete | Pass | Method, run contract, limits, structure and integrity instructions included |
| Figures/tables present | Pass/conditional | Tables are package files; figures are embedded in slides rather than separately packaged |
| Confusion matrices | Pass | 4,000 raw/normalized matrices and F1 arithmetic match |
| Hashes/checksums | Pass | 31/31 checksum entries; protected and inference hashes pass |
| Manifest | Pass | 30 listed = 30 actual scoped files; no missing/extra scoped files |
| Package structure | Conditional fail | `results_summary/` is useful but is not named in the user's Phase-8 exclusive category list |
| Competitor references | Conditional | No dependency/borrowing; negative provenance declarations remain in sealed files |
| Obvious plagiarism | Pass, static | No suggestive attribution phrase or competitor implementation dependency found |
| Local documentation links | Pass | 15 current judge/package documents checked; no broken links |
| Missing images | Pass | PPTX/PDF assets resolve and render |
| Slide clipping | Conditional | No visible clipping in supplied renders; slide-11 image shape extends 0.427 inches below slide bounds |
| Formatting | Conditional fail | Deck has 16 slides rather than preferred 8–10; slides 15–16 are dense explanation pages; slide numbering is absent |
| First-time reviewer navigation | Pass | Executive summary and package README give clear entry points |
| Runtime inference | Not run | Prohibited because both modes fit support RFs |
| Clean-environment install | Not verified | Existing preflight only; no fresh install in this pass |

## Rubric review and deductions

| Area | Score | Deduction and exact file | Documentation-only action |
|---|---:|---|---|
| Technical quality | 91/100 | Transductive eligibility unresolved in `FINAL_SUBMISSION/README.md` | Already disclosed |
| Innovation | 88/100 | Coordinate benefit is use-case-specific; spatial stress underperforms ASTRA in `results_summary/LOCKED_REPORT.md` | Already disclosed |
| Scientific reasoning | 93/100 | No independent city/organizer test | Cannot fix without new science |
| Presentation | 72/100 | 16 slides, dense slides 15–16, small chart labels, no slide numbers in `presentation.pptx` | Logged; sealed binary not modified |
| Reproducibility | 86/100 | Pool-bound artifact; raw rebuild and clean install not self-contained | Already documented |
| Communication | 86/100 | Full caveat set is accurate but heavy for a short judging window | Active docs simplified |
| Repository quality | 68/100 | Large historical tree and highly dirty Git status | Package entry points clarified |
| Judge friendliness | 84/100 | Minimal package is clear; unresolved official limits create hesitation | Inventory and outline synchronized |

## Exact remaining actions

1. Obtain organizer approval for full-pool target features, coordinates and additional development supervision.
2. Confirm slide count/time and whether 16 slides are accepted; if not, authorize a 9–10-slide rebuild and reseal all hashes.
3. Confirm whether 340 words satisfy the official explanation limit.
4. Open the PPTX on the presentation machine and inspect slide 11 plus font substitution.
5. Confirm official filenames, allowed package categories and redistribution/license terms.
