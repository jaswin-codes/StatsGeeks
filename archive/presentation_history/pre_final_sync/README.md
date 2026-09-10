# StatsGeeks · Building-age transfer learning

**Coordinate-RF · Madrid → Amsterdam · four construction-era classes**

We estimate building construction era from 30 m Landsat pixels where complete building records are unavailable. The goal is useful cross-city transfer with few labelled target examples—not simply high source-city accuracy.

> **Locked result: macro-F1 = 0.749299** at 200 labels/class.
> Population SD **0.005716** across 200 paired, fixed-city random-pixel episodes. This is not an organizer-held-out or unseen-city score.

## Start here

- **Judges:** [two-minute overview](docs/judge/START_HERE.md) → [10-slide presentation](presentation/Coordinate-RF_Judges.pdf) → [written explanation](docs/judge/WRITTEN_JUSTIFICATION.md).
- **Reviewers:** [methods](docs/methodology/METHOD.md) · [locked results](candidate/reports/RESULTS.md) · [limitations](docs/methodology/LIMITATIONS.md).
- **Release team:** [safe verification](docs/reproducibility/REPRODUCIBILITY.md) · [submission contents](docs/judge/SUBMISSION_INVENTORY.md) · [release report and commit plan](docs/release/RELEASE_REPORT.md).

## Dataset and motivation

The organizer-supplied data contain six spectral bands over 1984–2025: **76,263 Madrid pixels** and **25,992 Amsterdam pixels**. Multiyear observations are summarized into 60 spectral features. Construction-era labels describe mixed 30 m pixels, not individual buildings. The oldest class boundary differs by city; [data documentation](data/README.md) and [methods](candidate/reports/METHODS.md) explain the input contract.

Building age informs retrofit planning and energy policy. Domain shift between cities and scarce target labels make direct source-only classification insufficient.

## Method and pipeline

```text
Labelled Madrid → contextual source learning → frozen probability prior
                                                       ↓
Unlabelled Amsterdam pool → whitening + coordinates → support-label RF
                                                       ↓
                                   probability blend → spatial smoothing
```

Coordinate-RF combines a source-learned prior with a balanced 200-tree target-support random forest on 60 whitened features and two standardized coordinates. The source weight is `20/(20+4b)`, where `b` is labels/class; a nine-neighbour Gaussian step smooths probabilities without query labels. The contribution is a problem-specific combination of source transfer, low-data adaptation and spatial context—not a claim to have invented random forests.

This is **transductive, full-pool, coordinate-aware inference**. The frozen artifact requires the original ordered Amsterdam pool. `Coordinate_RF` is the machine identifier for Coordinate-RF.

## Frozen results

| Labels/class | Total support labels | Macro-F1 | Population SD |
|---:|---:|---:|---:|
| 5 | 20 | 0.650253 | 0.011246 |
| 25 | 100 | 0.687664 | 0.012145 |
| 50 | 200 | 0.708436 | 0.011277 |
| 100 | 400 | 0.729839 | 0.008802 |
| 200 | 800 | **0.749299** | 0.005716 |

Each budget has 200 paired episodes. SD measures support-sampling spread, not a confidence interval. The additional 800-label development bank is excluded from final queries but remains additional research supervision. [Authoritative CSV](FINAL_SUBMISSION/results_summary/learning_curve.csv) · [comparison table](candidate/tables/leaderboard.md).

## Safe reproducibility

From the repository root, using the Python standard library:

```bash
python -B scripts/validate_release.py
```

This checks hashes, package membership, documentation links and frozen result values. It does **not** load models, fit support sets or regenerate predictions. For the sealed package alone: `cd FINAL_SUBMISSION` then `sha256sum -c checksums.sha256`.

Observed scientific environment: Python 3.14.6 on Windows, with [pinned inference requirements](requirements-repro.txt). The root `requirements.txt` belongs to the historical baseline. A Git clone alone may lack ignored data and model binaries. Runtime reproduction is documented separately and **both `--verify` and `--support` fit support RFs**; neither is a safe release-audit command. [Assurance levels and installation limits](docs/reproducibility/REPRODUCIBILITY.md).

## Repository map

| Directory | Purpose |
|---|---|
| `docs/` | Judge guide, methodology, reproducibility and one current release report |
| `presentation/` | Concise judge deck, editable builder and speaker guidance |
| `FINAL_SUBMISSION/` | Existing sealed scientific bundle: notebook, model, tables, original slides and explanation |
| `candidate/` | Canonical frozen models, results, figures and original experiment evidence |
| `scripts/` | Static validation and maintenance utilities |
| `data/`, `original/` | Supplied data and unchanged organizer notebooks |
| `working/`, `models/`, `submission/` | Historical research/runtime paths retained for provenance |
| `archive/` | Superseded reports, team drafts and preserved local sidecars |
| `reproducibility/` | Before/after hashes, inventory and validation receipts |

Scientific directories stay at their original paths to preserve manifests and runtime contracts. [Full navigation](docs/README.md).

## Submission, limitations and future work

The sealed [submission bundle](FINAL_SUBMISSION/README.md) contains the frozen model, saved-output notebook, result tables, original 16-slide PPTX/PDF, explanation, requirements and checksums. The new **10-slide judge deck** is a presentation-only companion; it does not replace bytes inside that seal. See the [upload checklist](docs/judge/SUBMISSION_INVENTORY.md) before choosing the presentation to upload.

The four-direction spatial mean is **0.694216**, below the matched historical comparison's **0.696672**. Five-shot superiority is inconclusive. Results from one spatially correlated city do not establish geographic generalization. Organizer eligibility for full-pool features, coordinates and extra development supervision remains unconfirmed.

Future work, **not performed for this release**: independent-city evaluation, spatially separated validation and a portable inference contract for new pools. No retraining, optimization or prediction regeneration was performed during release preparation.

## License and acknowledgements

No repository license has been granted; do not assume open-source reuse or raw-data redistribution permission. See [license status](docs/reproducibility/LICENSE_STATUS.md). We thank the hackathon organizers for the data and starter notebooks, and the NumPy, SciPy, scikit-learn, pandas and Matplotlib communities. Citation metadata: [CITATION.cff](CITATION.cff).
