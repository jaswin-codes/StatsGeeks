# Coordinate-RF · judge presentation

**Use [Coordinate-RF_Judges.pdf](Coordinate-RF_Judges.pdf) or [Coordinate-RF_Judges.pptx](Coordinate-RF_Judges.pptx).** Ten slides, consistent typography and colour, numbered pages, source footers and speaker notes. Locked headline: **0.749299 macro-F1**.

| Slides | Story | Suggested speaker |
|---|---|---|
| 1–3 | Abstract, urban problem, dataset and low-label challenge | Member 1 |
| 4–5 | Source/local pipeline and design rationale | Member 2 |
| 6–8 | Learning curve, paired interpretation and spatial trade-off | Member 3 |
| 9–10 | Integrity, limitations, eligibility and next research | Member 4 |

Allow roughly 8–10 minutes as a rehearsal default, subject to organizer timing. Every speaker should answer questions on the 25-label regime, source-prior reuse, additional supervision and why spatial results limit the headline.

## Presentation-only rebuild

Using the already available presentation libraries:

```bash
python -B presentation/build_judge_deck.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File presentation/export_judge_deck.ps1
```

The builder reads the frozen learning-curve CSV; it never imports model code. Its log2-spaced chart is a new presentation view of existing means and population SD, not recomputed predictions or a replacement scientific figure. PowerPoint exports PDF and PNG slides, checks text bounds and updates only the companion hash manifest. Then rerun `python -B scripts/validate_release.py`. Desktop PowerPoint is required for that export; no cross-platform export claim is made. The scientific-package seal is never rewritten.

The scientific runtime requirements do not include presentation tooling. This release used existing `python-pptx`, Pillow, Matplotlib and desktop PowerPoint, without installing dependencies. Exact available versions are recorded in the release validation receipt when available.

## Preserved original presentation

`StatsGeeks_BuildingAge.pptx` / `.pdf` and the 16-slide deck inside `FINAL_SUBMISSION/` are preserved historical/sealed deliverables. Do not confuse them with the ten-slide companion. The stale EXP-010 builder was moved to `archive/release_history/presentation/`; it must not be used to rebuild the final Coordinate-RF deck.

[Upload checklist](../docs/judge/SUBMISSION_INVENTORY.md) · [judge overview](../docs/judge/START_HERE.md).
