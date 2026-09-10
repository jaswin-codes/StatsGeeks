# FAQ

**Which model is final?** Coordinate-RF. `Coordinate_RF` is the frozen machine ID, not another method.

**Where should a judge begin?** [Start here](START_HERE.md), then the [approved final PDF](../../FINAL_SUBMISSION/presentation.pdf) and [written explanation](WRITTEN_JUSTIFICATION.md).

**What is the score?** At 25/class: 0.687664 ± 0.012145. At 200/class: **0.749299 ± 0.005716** macro-F1. Each uses 200 paired fixed-city episodes; deviations are population SD, not confidence intervals.

**Why preserve old notebooks and duplicate artifacts?** They are evidence, backups or hash-bound copies. Removing them would risk provenance or runtime paths. Superseded editable reports are archived; research evidence remains in place and outside the main judge route.

**Can I run `--verify` during a no-fitting audit?** No. It fits support RFs. From `FINAL_SUBMISSION/`, use `sha256sum -c checksums.sha256` for byte checks instead. The older release validator targets the previous presentation layout.

**Does the notebook rebuild from raw data?** No. It uses a trusted preprocessed pool. Fresh raw-data reproduction is not certified by this release.

**Which presentation is current?** Only `FINAL_SUBMISSION/presentation.pptx` and its matching PDF. Earlier decks and sealed candidate packages are historical, not alternate upload targets. [Upload guidance](SUBMISSION_INVENTORY.md) records approved source provenance and remaining checks.

**Is the result universally better?** No. Five-shot superiority is inconclusive; Coordinate-RF's spatial mean is below the matched historical comparison. One target city does not establish unseen-city generalization.

**What remains conditional?** Organizer eligibility, exact upload requirements, source-model export expectations, redistribution rights and runtime portability. No new experiment was run to resolve these questions.
