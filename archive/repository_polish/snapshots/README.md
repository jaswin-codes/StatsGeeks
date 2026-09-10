# StatsGeeks — Building-age transfer learning

Publication and reproducibility package for four-class Landsat building-age classification, transferring from Madrid to Amsterdam.

**Model frozen:** Coordinate_RF is the development-locked packaged model. ASTRA remains a historical comparison; EXP-F and frozen EXP-010 are unchanged. No publication-phase tuning was performed.

## Results
At 200 shots/class, Coordinate_RF achieves **0.749299 ± 0.005716 macro F1** (population SD; 200 paired episodes), versus paired ASTRA **0.733037**. This is a fixed-city, random-pixel result—not independent-city superiority. Coordinate_RF is slightly worse on the four-direction spatial mean, and its five-shot gain is inconclusive. An additional 800-label development bank was excluded from final queries.

[Results](candidate/reports/RESULTS.md) · [Methods](candidate/reports/METHODS.md) · [Statistical evidence](candidate/reports/STATISTICAL_ANALYSIS.md) · [Final report](candidate/reports/FINAL_REPORT.md)

## Installation and reproduction
The observed environment is Python **3.14.6** on Windows 11. Exact versions are pinned; portability to other environments is not yet certified.

```bash
python -m venv .venv-publication
# Windows: .venv-publication\Scripts\activate
# Linux/macOS: source .venv-publication/bin/activate
python -m pip install -r requirements-repro.txt
python -B candidate/publication/validate_package.py
python -I -B reproduce_best.py --verify --out replay_new
```

The replay destination must not already exist. It checks five fixed-reference Coordinate_RF episodes without loading query truth. Only load trusted, hash-verified pickle artifacts.

[Reproduction guide](candidate/reports/REPRODUCIBILITY.md) includes evidence rebuilding, seeds, hardware, commands and hashes. Local data and large artifacts have historically been Git-ignored: a Git clone alone is **not** guaranteed to contain them. Use the manifest-verified submission bundle or obtain authorized data. The inference bundle already contains the bound target pool.

## Method
A contextual source prior is blended with a target-support random forest using adaptively whitened features and two standardized coordinate columns, followed by label-free spatial probability averaging. Full target features/coordinates are used transductively; only designated support labels enter episode fitting. The pool's original row order is part of the input contract.

## Repository layout
```text
candidate/
  best_model/          Frozen inference code, state, lock, reference inputs
  publication/         Evidence-only build, validation and export scripts
  figures/publication/ Canonical 350-DPI PNG + vector SVG/PDF figures
  tables/              CSV and Markdown evidence
  reports/             Methods, results, reproducibility and audit
  reproducibility/     Environment, manifests and verification outputs
  presentation/        Transparent, tightly cropped slide assets
  autonomous_runs/     Immutable original research evidence
archive/               Preserved root scratch files and previous README
```

[Detailed directory structure](candidate/reports/DIRECTORY_STRUCTURE.md) · [Repository audit](candidate/reports/REPOSITORY_AUDIT.md)

Legacy `docs/`, `working/`, `submission/`, `presentation/` and earlier experiment directories preserve historical provenance and are **not** the current final package. Competitor forensics were quarantined outside this repository. The allowlisted submission export excludes all forensic comparisons, legacy workflows, caches and unrelated research.

## Figures and presentation
[Figure gallery](candidate/publication/README.md) · [Slide-ready assets](candidate/presentation/README.md) · [Tables](candidate/tables/leaderboard.md)

Every publication figure has PNG, SVG and PDF exports. Transparent PNG variants are provided without duplicating canonical vector assets.

## Citation and acknowledgements
Cite this repository's team, title and the commit recorded in [environment_summary.json](candidate/reproducibility/environment_summary.json); see [CITATION.cff](CITATION.cff). No DOI or peer-reviewed publication is claimed. We acknowledge the hackathon organizers for supplied data/notebooks and NumPy, SciPy, scikit-learn, pandas and Matplotlib. No competitor material is included in the final export.

## Limitations
One target city; spatially correlated pixels; historical audit exposure; extra development supervision; pool-bound coordinates; uncertain raw-data redistribution rights. See the methods and audit before reusing results. Frozen implementations and predictions must not be modified as part of publication maintenance.
