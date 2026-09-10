"""Build additive judge documentation and a minimal, dependency-complete package.

No existing file is overwritten. No model module is imported or executed.
Frozen scientific files are copied byte-for-byte. The derived notebook changes
only dependency paths, retaining all scientific code, metadata and outputs.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil

from repository_polish_audit import ROOT, sha256

SOURCE = ROOT / 'candidate/final_submission'
PACKAGE = ROOT / 'FINAL_SUBMISSION'
COPIES: dict[str, str] = {}
CREATED: list[str] = []
AUDIT = json.loads((SOURCE / 'evidence/final_complete.json').read_text())
BUDGETS = [5, 25, 50, 100, 200]


def put(name: str, text: str) -> None:
    """Write a new UTF-8 document, refusing replacement."""
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text.rstrip() + '\n')
    CREATED.append(name)


def copy(source: Path, destination: Path) -> None:
    """Copy exclusively and record the original path as provenance."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open('rb') as src, destination.open('xb') as dst:
        shutil.copyfileobj(src, dst)
    assert sha256(source) == sha256(destination)
    name = destination.relative_to(ROOT).as_posix()
    COPIES[name] = source.relative_to(ROOT).as_posix()
    CREATED.append(name)


def result_table() -> str:
    lines = ['| Labels/class | Macro F1 | Population SD | Episodes |', '|---:|---:|---:|---:|']
    for budget in BUDGETS:
        row = AUDIT['summary'][str(budget)]['Coordinate_RF']
        lines.append(f"| {budget} | {row['mean']:.6f} | {row['population_sd']:.6f} | {row['episodes']} |")
    return '\n'.join(lines)


def diagrams() -> None:
    """Draw process-only diagrams, never regenerate scientific figures."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    flows = {
        'method': ('Coordinate-RF: Madrid to Amsterdam', [
            'Madrid + Amsterdam\nSource / target inputs', 'Feature engineering\nContext + alignment',
            'Target features\nWhitening + coordinates', 'Coordinate-RF\nSupport RF + source prior',
            'Amsterdam predictions\nSpatial smoothing'],
            'Method schematic only. Full unlabelled target pool is used; query labels are not predictive inputs.'),
        'repository_architecture': ('Repository architecture: evidence stays in place', [
            'Original + data\nOrganizer inputs', 'candidate/\nFrozen research evidence',
            'docs/ + reproducibility/\nJudge guides and audit', 'FINAL_SUBMISSION/\nAllowlisted copies',
            'archive/\nPreserved historical material'],
            'Reading order, not import dependencies. Existing paths and original bytes remain unchanged.'),
        'inference': ('Pool-bound inference contract', [
            'Trusted artifact\nVerify hashes first', 'Support NPZ\nIndices, labels, budget',
            'Frozen recipe\nSupport RF fitting required', 'Probability blend\nLabel-free smoothing',
            'New output directory\nQuery classes + probabilities'],
            'Execution was NOT performed in this polish pass: adaptation fits a model and is prohibited here.'),
        'evaluation': ('Evidence-only evaluation audit', [
            'Locked confusion matrices\nRead saved evidence', 'Check F1 arithmetic\nNo new predictions',
            'Check mean + population SD\n200 episodes per budget', 'Match tables + documents\nFixed-city interpretation',
            'Preservation receipt\nOriginal SHA-256 unchanged'],
            'Query truth remains evaluation-only. Repeated support draws are not independent cities.'),
    }
    for name, (title, labels, note) in flows.items():
        fig, ax = plt.subplots(figsize=(14, 3.2))
        fig.patch.set_facecolor('white')
        ax.set(xlim=(0, 14), ylim=(0, 3.2))
        ax.axis('off')
        ax.text(0.2, 2.85, title, fontsize=17, weight='bold', color='#16324f')
        for index, label in enumerate(labels):
            x = 0.18 + index * 2.79
            box = FancyBboxPatch((x, 1.05), 2.42, 1.2, boxstyle='round,pad=0.06',
                                 facecolor='#edf4fa', edgecolor='#236b8e', linewidth=1.4)
            ax.add_patch(box)
            ax.text(x + 1.21, 1.65, label, ha='center', va='center', fontsize=10, color='#16324f')
            if index < len(labels) - 1:
                ax.annotate('', xy=(x + 2.71, 1.65), xytext=(x + 2.49, 1.65),
                            arrowprops={'arrowstyle': '->', 'color': '#236b8e', 'lw': 1.5})
        ax.text(0.18, 0.40, note, fontsize=9, color='#435466')
        for extension in ('svg', 'png'):
            destination = ROOT / f'figures/repository_polish/{name}.{extension}'
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb') as stream:
                fig.savefig(stream, format=extension, dpi=300, bbox_inches='tight',
                            metadata={'Date': None} if extension == 'svg' else None)
            CREATED.append(destination.relative_to(ROOT).as_posix())
        plt.close(fig)


def build_package() -> None:
    """Preserve scientific contents while resolving the flat notebook layout."""
    PACKAGE.mkdir(exist_ok=False)
    copy(SOURCE / 'presentation/StatsGeeks_BuildingAge_FINAL.pptx', PACKAGE / 'presentation.pptx')
    copy(SOURCE / 'presentation/StatsGeeks_BuildingAge_FINAL.pdf', PACKAGE / 'presentation.pdf')
    copy(SOURCE / 'justification/written_justification.txt', PACKAGE / 'written_explanation/written_justification.txt')
    for path in sorted((SOURCE / 'model').rglob('*')):
        if path.is_file() and path.suffix != '.onetoc2':
            copy(path, PACKAGE / 'model' / path.relative_to(SOURCE / 'model'))
    # Include only dependencies referenced by the preserved notebook, not replay outputs.
    for name in ('final_complete.json', 'SOURCE_REFIT.json', 'PREFLIGHT.json', 'SHA256SUMS.txt'):
        copy(SOURCE / 'evidence' / name, PACKAGE / 'model/evidence' / name)
    copy(SOURCE / 'tables/spatial.csv', PACKAGE / 'model/tables/spatial.csv')
    copy(SOURCE / 'reports/METHODS.md', PACKAGE / 'model/reports/METHODS.md')
    for name in ('learning_curve.csv', 'leaderboard.csv'):
        copy(SOURCE / 'tables' / name, PACKAGE / 'results_summary' / name)
    copy(SOURCE / 'reports/FINAL_REPORT.md', PACKAGE / 'results_summary/LOCKED_REPORT.md')
    notebook = json.loads((SOURCE / 'notebook/FINAL_NOTEBOOK.ipynb').read_text(encoding='utf-8'))
    for cell in notebook['cells']:
        source = cell['source']
        is_list = isinstance(source, list)
        text = ''.join(source) if is_list else source
        text = text.replace("ROOT/'evidence/", "ROOT/'model/evidence/").replace("ROOT/'tables/", "ROOT/'model/tables/")
        if cell['cell_type'] == 'markdown':
            text = text.replace('evidence/SOURCE_REFIT.json', 'model/evidence/SOURCE_REFIT.json')
            text = text.replace('evidence/PREFLIGHT.json', 'model/evidence/PREFLIGHT.json')
            text = text.replace('evidence/SHA256SUMS.txt', 'model/evidence/SHA256SUMS.txt')
            text = text.replace('reports/METHODS.md', 'model/reports/METHODS.md')
        cell['source'] = text.splitlines(keepends=True) if is_list else text
    put('FINAL_SUBMISSION/solution_notebook.ipynb', json.dumps(notebook, indent=1, ensure_ascii=False))
    put('FINAL_SUBMISSION/reproduce.py', '''"""Dispatch to the unchanged, hash-checking Coordinate-RF entry point.

WARNING: both --support and --verify fit support-set random forests. Do not
execute during a no-training audit. Output paths must not already exist.
"""
from pathlib import Path
import runpy


def main() -> None:
    """Resolve the artifact directory independently of the caller's cwd."""
    runner = Path(__file__).resolve().parent / "model" / "reproduce_best.py"
    runpy.run_path(str(runner), run_name="__main__")


if __name__ == "__main__":
    main()
''')
    put('FINAL_SUBMISSION/requirements.txt', '''# Frozen inference pins copied from model/requirements-repro.txt.
# pandas is required by the notebook; nbformat supports structural validation.
# Python 3.14.6 observed. Clean installation was not attempted in this audit.
numpy==2.5.3
scipy==1.18.1
scikit-learn==1.9.0
threadpoolctl==3.6.0
pandas==3.0.5
nbformat==5.11.1
# A compatible Jupyter frontend/kernel is optional and not certified here.
''')
    put('FINAL_SUBMISSION/README.md', f'''# StatsGeeks — Coordinate-RF

**Four-class building-construction-era classification · Madrid → Amsterdam**

## Competition and problem
Classify 30 m × 30 m Landsat pixels into four construction-era classes.
Learn from labelled Madrid data and adapt using 5, 25, 50, 100 or 200 labelled
Amsterdam pixels per class. Macro F1 weights the four classes equally.

**Status: frozen scientific solution; submission eligibility remains conditional.**
No new training, tuning, predictions or model replacement occurred during packaging.

## Approach and transfer
```text
Madrid spectral features → contextual source learning → frozen probability prior
                                                               ↓
Amsterdam full unlabelled pool → whitening + coordinates → support RF
                                                               ↓
                                     blend + spatial smoothing → predictions
```
Coordinate-RF combines source-learned probabilities with a 200-tree target-support
random forest on 60 whitened features plus two standardized coordinates. The source
prior weight is `20/(20+4b)`, where `b` is labels/class. Nine-neighbour Gaussian
smoothing uses coordinates, not query labels. This is transductive and pool-bound,
not an inductive unseen-city model. The machine identifier `Coordinate_RF` means
**Coordinate-RF**; it is not a different model.

## Locked results
{result_table()}

Each row uses 200 paired, fixed-city random-pixel episodes. Population SD is not
a confidence interval. The 800-label development bank is excluded from final
queries but constitutes additional research supervision. At 200/class, paired
ASTRA scores 0.733037; Coordinate-RF's spatial mean is 0.694216 versus ASTRA's
0.696672. These are existing audit results, not organizer-held-out scores.

## Repository structure and deliverables
| Path | Purpose |
|---|---|
| `presentation.pptx`, `presentation.pdf` | Original final slides, unchanged |
| `written_explanation/` | Original explanation, unchanged |
| `solution_notebook.ipynb` | Original notebook with dependency paths relocated only |
| `model/` | Frozen state, inference implementation and notebook evidence dependencies |
| `results_summary/` | Locked CSV tables, report and concise summary |
| `requirements.txt`, `reproduce.py` | Environment specification and inference dispatcher |
| `manifest.json`, `checksums.sha256` | Package membership, provenance and byte integrity |

## Quick start: safe inspection
Open the PDF, then [results summary](results_summary/README.md). Read the notebook
without running its cells. Check all package bytes from this directory:
```bash
sha256sum -c checksums.sha256
```
Checksums establish consistency, not authenticity; obtain them from a trusted source.
The checksum file excludes itself and covers the manifest; the manifest excludes
itself and the checksum file to avoid circular hashes.

## How to run inference / reproduce (not run during this audit)
Observed environment: Python 3.14.6 on Windows. A Git clone is not guaranteed to
include ignored large artifacts; use this complete folder. Only load trusted pickles.
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# POSIX: source .venv/bin/activate
python -m pip install -r requirements.txt
python -I -B reproduce.py --support support.npz --out NEW_OUTPUT_DIRECTORY
# Optional fixed-reference replay (also fits support RFs):
python -I -B reproduce.py --verify --out NEW_REPLAY_DIRECTORY
```
**Both commands fit support-set RFs. They are not permitted in a no-retraining audit.**
Support NPZ fields: `indices` (unique integer pool rows), `labels` (1–4), and
`budget` (integer scalar, supported values above). Supply exactly `budget` labels
per class. Optional `query` indices must be unique, valid and disjoint from support.
The pool contains 25,992 rows in its original order; arbitrary new pools are not
supported. Never pass query truth to adaptation. Output paths must be new.

For notebook use, start a compatible Jupyter kernel in this folder. Saved outputs
are inherited, not newly executed here. Raw-data training is not self-contained:
organizer data, Madrid-fitted preprocessing and ordered coordinates are external.
See [methods](model/reports/METHODS.md). Historical receipts and the historical
SHA256SUMS under `model/evidence/` describe the original source package, not the
relocated package; use the root manifest and checksums for this folder.

## Limitations and submission gates
Organizer approval of full-pool target features, coordinates and additional
research supervision is unconfirmed. The original explanation exceeds the
conservative 300-word interpretation; confirm the official limit before upload.
There is one target city, historical audit exposure and no independent organizer
held-out validation. Clean installation, new inference execution and fresh visual
rendering are not certified by this packaging pass. Source-trained reusable model
export requirements versus a cached source probability prior also need confirmation.

## Acknowledgements and license
StatsGeeks acknowledges the organizers for data and notebooks and the open-source
scientific Python community. No competitor material is added. No repository license
or raw-data redistribution grant has been established; no new license is asserted.
Obtain rights-holder approval before public redistribution.
''')
    put('FINAL_SUBMISSION/results_summary/README.md', f'''# Locked results summary

Selected model: **Coordinate-RF** (`Coordinate_RF` in frozen machine files).

{result_table()}

Source: `model/evidence/final_complete.json` (relative to package root).
Values are formatted to six decimals without altering saved scientific precision.
See `learning_curve.csv` for all matched methods and full stored precision.
200 paired episodes per budget; population SD; fixed Amsterdam query population
with development-bank and current-support exclusions. No new scientific run.
Spatial mean/worst: 0.694216 / 0.644816; matched ASTRA: 0.696672 / 0.658183.
The unchanged `LOCKED_REPORT.md` preserves historical preflight claims; they are
not fresh validation of this relocation. Its short relative paths refer to the
original canonical package. New-package evidence is under `model/evidence/`.
''')


def documents() -> None:
    """Add concise navigation without touching any frozen README or master plan."""
    put('docs/README_SUBMISSION.md', '''# StatsGeeks — judge entry point

The existing root README is listed in the frozen SHA256SUMS.json and is preserved.
This is its additive, current companion rather than an unauthorized overwrite.

1. [Five-minute executive summary](../PROJECT_EXECUTIVE_SUMMARY.md)
2. [Professional package README](../FINAL_SUBMISSION/README.md)
3. [Method](METHOD.md) · [Pipeline](PIPELINE.md) · [Reproducibility](REPRODUCIBILITY.md)
4. [Limitations](LIMITATIONS.md) · [FAQ](FAQ.md)
5. [Deliverable validation](../DELIVERABLE_VALIDATION.md)
6. [Final pre-flight](../FINAL_PRE_FLIGHT.md)

Use `candidate/final_submission/` as the existing canonical scientific source.
`FINAL_SUBMISSION/` is a new, minimal judge distribution with traceable copies.
Historical research remains in place. Do not confuse old experiment metrics with
current locked Coordinate-RF scores. No model work is authorized by these guides.
''')
    put('docs/METHOD.md', f'''# Method — Coordinate-RF

## Task and data
Madrid is the labelled source; Amsterdam is the few-shot target. Predict four
construction-era classes per 30 m Landsat pixel. Historical dataset documentation
records 76,263 Madrid and 25,992 Amsterdam pixels over 1984–2025; raw row counts
are not independent sample counts. Madrid class boundaries: ≤1960, (1960,1984],
(1984,2004], >2004. Amsterdam differs only at the first cutoff, 1945.
Construction-year labels are not predictive features.

## Source transfer
The saved recipe constructs 120 contextual columns from 60 spectral summaries
and their local lattice averages. Covariance alignment and one pseudo-class
refinement produce source-learned probabilities for the target pool. Target query
truth is not an input. Packaging consumes saved source state; it does not refit it.

## Few-shot branch
For budget `b`, shrink covariance toward its diagonal with
`rho=min(1,60/(4b))` and ridge `1e-7 I`. Whiten the 60 inputs, append two full-pool
standardized lattice coordinates, and fit a balanced RF with 200 trees, leaf size
1, sqrt feature sampling and seed 42 on support labels. Blend the source prior
with weight `20/(20+4b)`. Apply one Gaussian smoothing step, nine neighbours,
sigma 1. Frozen implementation and tie handling remain authoritative.

## Evaluation and interpretation
{result_table()}

Macro F1 averages class-wise F1 over classes 1–4. Variation is population SD over
200 paired support draws, conditional on one city. Extra 800-label development
supervision and historical audit exposure limit independence claims. Spatial
mean/worst 0.694216 / 0.644816 do not beat matched ASTRA (0.696672 / 0.658183).

Sources: [locked report](../candidate/final_submission/reports/FINAL_REPORT.md),
[implementation](../candidate/final_submission/model/agf_model.py),
[selection lock](../candidate/final_submission/model/SELECTION_LOCK.json).
Coordinate-RF is the display name; `Coordinate_RF` is the unchanged machine ID.
''')
    put('docs/PIPELINE.md', '''# Pipeline and repository architecture

![Method](../figures/repository_polish/method.svg)

| Boundary | Inputs | Contract |
|---|---|---|
| Source learning (historical) | Madrid features, labels, coordinates | No target query truth |
| Pool binding (historical) | Ordered Amsterdam features and coordinates | Full-pool transductive preprocessing |
| Adaptation (not run here) | Frozen state, support rows and labels, budget | Fits a support RF; disjoint queries |
| Prediction (not run here) | Adapted branch + source prior | Four probability columns, classes 1–4 |
| Evidence audit (this pass) | Saved matrices, summaries and files | Read-only arithmetic and integrity checks |

![Inference](../figures/repository_polish/inference.svg)
![Evaluation](../figures/repository_polish/evaluation.svg)
![Architecture](../figures/repository_polish/repository_architecture.svg)

## Layout policy
Keep existing `candidate/`, `working/`, `original/`, `data/`, `presentation/` and
`archive/` paths intact to protect imports and hash manifests. Do not introduce
empty `src/`, `models/`, `tables/` or `autonomous_runs/` duplicates for appearance.
Current implementations, models, tables and runs already live under `candidate/`.
The new `FINAL_SUBMISSION/` has only requested deliverable categories; notebook
runtime dependencies live under its `model/` directory. New schematic SVG/PNG
assets live under `figures/repository_polish/`, separate from locked result figures.
''')
    put('docs/REPRODUCIBILITY.md', '''# Reproducibility without disturbing evidence

## Levels of assurance
1. **Byte preservation:** compare every inventoried original against the before
   SHA-256 snapshot; report missing/changed files. Environments/Git internals and
   bytecode are explicitly outside that snapshot.
2. **Static package validation:** manifest coverage, copied bytes, ZIP/XML/PNG/NPZ,
   notebook schema/syntax, dependency paths, pins and saved metric arithmetic.
3. **Runtime reproduction:** historical receipts exist; this pass does not rerun
   them. Both `--verify` and `--support` fit RFs, so are prohibited by this task.
4. **Fresh scientific reproduction:** raw preprocessing/source fitting and new
   validation are outside scope. Do not claim organizer-independent results.

## Safe checks
From the repository root:
```bash
python -B scripts/validate_repository_polish.py --out NEW_AUDIT_DIRECTORY
cd FINAL_SUBMISSION
sha256sum -c checksums.sha256
```
The validator never imports model code or loads a pickle. Its output directory
must not exist. It computes F1 arithmetic from frozen confusion matrices, not new
predictions. Baseline and later receipts live in `reproducibility/repository_polish/`.

## Environment and execution contract
Observed scientific Python: 3.14.6, Windows. The legacy root `requirements.txt`
describes a different baseline (Python 3.13.15; NumPy 2.5.1). For the new package
use its requirements (NumPy 2.5.3), not the legacy file. The package adds notebook
pandas/nbformat pins without changing inference pins. No packages were installed.
Jupyter frontend/kernel and clean offline installation remain unverified.

Runtime commands and the support NPZ schema are in the
[package README](../FINAL_SUBMISSION/README.md). Only execute later with explicit
permission to fit support models. Use a fresh output directory. Trust provenance
before deserialization: hashes detect mismatch but are not signatures.

## Relocation and historical evidence
The new notebook retains all outputs and metadata. Only two code dependency
prefixes and Markdown reference paths change; the validator checks these exact
allowed transformations against the original. Historical manifest paths/receipts
remain historical, while the new package manifest seals the relocated assets.
A clone alone may lack ignored models/data. Raw organizer redistribution rights
and standalone source-model requirements need confirmation.
''')
    put('docs/LIMITATIONS.md', '''# Limitations and submission gates

- **Eligibility:** full unlabelled target-pool access, coordinates and additional
  research-development labels require organizer approval. Do not infer approval.
- **Generalization:** one Amsterdam pool, spatial correlation, historical audit
  exposure and 800 extra development labels; 200 support draws are not 200 cities.
- **Spatial tradeoff:** Coordinate-RF mean/worst 0.694216 / 0.644816 versus ASTRA
  0.696672 / 0.658183. Random-pixel gains are not geographic superiority.
- **Deployment:** 25,992-row bound pool, exact order, schema and lattice units.
  This is not raw-input prediction for arbitrary cities. The cached source prior
  does not automatically satisfy an organizer requirement for a reusable Madrid
  trained-model export.
- **Protocol:** inherited label-availability filtering affects population
  membership; historical audit exposure limits independent-validation language.
- **Artifacts:** pickle requires trust. A byte hash is not proof of model safety.
  Large ignored artifacts and external raw data prevent clone-only reproduction.
- **Submission:** original explanation exceeds the conservative 300-word limit;
  official limits and upload/interface requirements remain unresolved.
- **Verification:** no training, support RF fitting, notebook execution, clean
  install or fresh slide rendering in this pass. Structural opening is not visual
  review. Existing historical rendering receipts are not newly certified.
- **Rights:** no repository license or organizer data redistribution permission
  has been established. Do not invent an open-source license for others' work.

All limitations are preserved rather than masked by cosmetic cleanup.
''')
    put('docs/FAQ.md', '''# FAQ

**Which model is final?** Coordinate-RF. `Coordinate_RF` is its frozen machine ID.
ASTRA, EXP-F and EXP-010 remain comparisons, not replacements.

**What should a judge read first?** The executive summary, then
`FINAL_SUBMISSION/README.md`, the PDF and the limitations.

**What is the key score?** 25/class: 0.687664 ± 0.012145; 200/class:
0.749299 ± 0.005716 macro F1. Both are 200 paired fixed-city episodes,
with population SD. They are not new or independent organizer test results.

**Why not rewrite the root README?** It is listed in a frozen hash manifest.
The no-overwrite/preservation rule wins; `docs/README_SUBMISSION.md` and the new
package README supply the professional entry points.

**Why keep old experiments and duplicate notebooks?** They are evidence or
backups. Reorganizing them could break imports, provenance or frozen paths.
They are excluded from the minimal distribution, not deleted.

**Can I run --verify during this audit?** No. It fits support RFs. Read-only
hash, schema, syntax and arithmetic checks are the allowed substitute.

**Does the notebook train from raw data?** No. It consumes a trusted preprocessed
pool. Raw organizer inputs and source-fitted preprocessing are external.

**Are these new results?** No. Saved scientific bytes and metrics are preserved.
New diagrams explain architecture, not scientific performance.

**Is this ready to upload unconditionally?** No. Organizer eligibility, official
limits, licensing, runtime portability and final human visual review remain gates.
''')
    put('docs/LICENSE_STATUS.md', '''# License status — not a license grant

No root LICENSE was present at inspection. The team has not authorized a specific
license, and organizer data rights are unresolved. This document grants no rights
and must not be presented as an OSI license. KEEP all existing notices. KEEP raw
data out of the judge distribution. MOVE a team-approved license decision into a
future dedicated licensing change only after rights-holder approval; do not alter
frozen evidence or silently license organizer materials.
''')
    put('docs/MASTER_PLAN_POLISH_ADDENDUM.md', '''# Master-plan addendum: repository-only pass

This additive status record supersedes no scientific evidence. The historical
`MASTER_PLAN.md` is preserved under the current no-overwrite instruction; its
planning-era claims are not the current experiment status.

Scope: new judge guides, diagrams, a minimal allowlisted package, static validation
and preservation receipts. Existing root documentation, experiments, models,
predictions, manifests and submissions remain unchanged. No optimization,
source training, support RF fitting or inference replay is performed.

Evidence and open gates: see `FINAL_REPOSITORY_REPORT.md`, `DELIVERABLE_VALIDATION.md`
and `FINAL_PRE_FLIGHT.md` at repository root. No milestone of unconditional
competition readiness or fresh model reproduction is claimed. Commit pending user
review; the pre-existing dirty working tree is not staged or reverted.
''')
    put('PROJECT_EXECUTIVE_SUMMARY.md', f'''# StatsGeeks — five-minute research summary

## Problem and dataset
Predict four building-construction eras for 30 m Landsat pixels. Madrid supplies
labelled source learning; Amsterdam supplies sparse support labels. Historical
data documentation records 76,263 Madrid / 25,992 Amsterdam pixels, 1984–2025,
with six spectral bands. City-specific first age cutoffs are 1960 and 1945.

## Transfer strategy and Coordinate-RF
A source-learned, context-aware probability prior is transferred to the full
unlabelled Amsterdam pool. A support-only, 200-tree RF uses 60 adaptively whitened
features plus two standardized coordinates. Blend probabilities with source weight
`20/(20+4b)` and apply nine-neighbour Gaussian smoothing. The source knowledge is
reused; it is not merely a target-only RF. Implementation ID: `Coordinate_RF`.

## Why it can work
Spectral summaries encode urban context; local coordinates help interpolate
spatially coherent construction eras. A source prior offers information when
support is scarce. This is a rationale consistent with the frozen evidence,
not a causal explanation or proof of universal transfer.

## Locked results
{result_table()}

Population SD across 200 paired fixed-city random-pixel episodes per budget.
At 200/class, ASTRA is 0.733037. Coordinate-RF is not spatially superior:
four-direction mean 0.694216 vs 0.696672; worst 0.644816 vs 0.658183.
Five-shot benefit is negligible. No new scientific work occurred during polish.

## Lessons and future work
Spatial interpolation and geographic extrapolation are different objectives.
Repeated support draws do not replace a fresh city. Full-pool target access,
800 additional development labels and historical audit exposure must be disclosed.
Future work, not performed here: independent geographic validation, approved
protocol clarification and a portable raw-data inference contract.

## Competition strengths and readiness
Strengths: explicit source-state reuse, locked five-budget evidence, matched
comparisons, honest spatial tradeoffs, readable notebook and traceable artifacts.
Unresolved: organizer eligibility, explanation limit, rights/license, independent
validation and clean-environment/runtime/visual sign-off. The package is prepared
for review, not falsely certified for unconditional upload.

Start with [the package](FINAL_SUBMISSION/README.md),
[validation](DELIVERABLE_VALIDATION.md) and [pre-flight](FINAL_PRE_FLIGHT.md).
''')
    put('archive/repository_polish/README.md', '''# Preservation archive — repository polish

These are byte-identical documentation snapshots, not replacements. Originals
remain at their existing paths so frozen manifests and imports remain valid.
No research evidence, draft, prediction, model or old experiment was deleted or
moved. Existing scratch/export archives are retained. Additional archival moves
are deferred because file age, duplication and naming do not prove obsolescence.
''')
    for name in ('README.md', 'requirements.txt', 'docs/MASTER_PLAN.md'):
        copy(ROOT / name, ROOT / 'archive/repository_polish/snapshots' / name)
    put('deliverables/README.md', '''# Deliverable index

Use [FINAL_SUBMISSION](../FINAL_SUBMISSION/README.md) for the clean judge package.
The canonical existing scientific source remains `candidate/final_submission/`.
Validation: [DELIVERABLE_VALIDATION.md](../DELIVERABLE_VALIDATION.md).
This folder is navigation only; binary assets are not duplicated here.
''')


def seal() -> None:
    """Seal only the new package; frozen historical checksums remain untouched."""
    files = {}
    for path in sorted(PACKAGE.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(PACKAGE).as_posix()
        name = path.relative_to(ROOT).as_posix()
        files[relative] = {'sha256': sha256(path), 'bytes': path.stat().st_size,
                           'source': COPIES.get(name, 'new documentation, wrapper, requirements or path-only notebook derivative')}
    put('FINAL_SUBMISSION/manifest.json', json.dumps({
        'schema_version': 1, 'model_display_name': 'Coordinate-RF', 'frozen_model_id': 'Coordinate_RF',
        'source_package': 'candidate/final_submission', 'training_executed': False,
        'scope': 'Every package file except manifest.json and checksums.sha256. Checksums cover manifest; self excluded.',
        'notebook_derivation': 'Dependency prefixes evidence/ and tables/ moved under model/; Markdown references updated only. Outputs and metadata unchanged.',
        'historical_receipts': 'model/evidence receipts and SHA256SUMS describe the original package, not this relocation.',
        'files': files,
    }, indent=2))
    sums = [f'{sha256(p)}  {p.relative_to(PACKAGE).as_posix()}' for p in sorted(PACKAGE.rglob('*')) if p.is_file()]
    put('FINAL_SUBMISSION/checksums.sha256', '\n'.join(sums))


def main() -> None:
    """Build only into new paths; a second run deliberately refuses replacement."""
    build_package()
    documents()
    diagrams()
    seal()
    put('reproducibility/repository_polish/build_receipt.json', json.dumps({'created': CREATED.copy(), 'byte_identical_copies': COPIES}, indent=2))
    print(f'Created {len(CREATED)} files; {len(COPIES)} byte-identical copies. No model execution.')


if __name__ == '__main__':
    main()
