# Start here · two minutes

## What we built

**Coordinate-RF** estimates four building-construction eras from Landsat pixels. It transfers a Madrid-learned probability prior to Amsterdam, then combines scarce support labels with spectral and spatial context.

## What to remember

- **0.749299 macro-F1** at 200 labels/class; population SD **0.005716**, 200 paired episodes.
- **0.687664 macro-F1** at 25 labels/class—the low-data rubric anchor.
- A fixed-city, random-pixel result, not an independent held-out-city result.
- Full unlabelled-target access, coordinates and an extra 800-label development bank are disclosed; eligibility needs organizer confirmation.
- Spatial extrapolation is weaker than random-pixel performance. We do not claim universal superiority.

## Review route

1. [10-slide PDF](../../presentation/Coordinate-RF_Judges.pdf) or [editable PowerPoint](../../presentation/Coordinate-RF_Judges.pptx).
2. [Written explanation](WRITTEN_JUSTIFICATION.md): model design, transfer strategy and F1 interpretation.
3. [Locked results](../../candidate/reports/RESULTS.md), [learning-curve CSV](../../FINAL_SUBMISSION/results_summary/learning_curve.csv) and [method](../methodology/METHOD.md).
4. [Safe verification](../reproducibility/REPRODUCIBILITY.md); inspect the [notebook](../../FINAL_SUBMISSION/solution_notebook.ipynb) without running it.

The notebook and sealed scientific bundle retain their original evidence. The concise deck is a new presentation-only companion; [submission navigation](SUBMISSION_INVENTORY.md) distinguishes it from the original sealed deck.

## Judging rubric

**Understanding (30):** cross-city domain shift, source-state reuse and few-label adaptation. **Creativity (40):** a context-aware transfer combination, with explicit negative spatial evidence. **Communication/teamwork (30):** concise visual narrative and four-person handoffs; see [speaker guidance](../../presentation/README.md).
