# Repository Audit and Hackathon Plan

## Audit scope

I inspected **all 12 workspace files**:

- All **112 notebook cells**, including code, Markdown, saved text outputs, and **40 embedded plots**.
- All three Markdown documents.
- The Word rubric, including its complete scoring table and deduction rules.
- Both Parquet datasets: full-table schema, missingness, identifiers, labels, observation quality, and acquisition dates.
- The JPEG.
- The OneNote table-of-contents binary.

**Limitations:** The `.onetoc2` file contains no extractable readable text; I cannot establish whether it references additional OneNote content outside this workspace. No accompanying OneNote sections are present.

**No project files were modified and no training notebooks were executed.** Small inspection commands were used to decode documents and profile data; temporary inspection files and dependencies were kept outside the workspace. Model scores below are **saved starter-notebook results**, not independently reproduced training results.

There are **no PDFs, CSVs, standalone Python scripts, README, dependency manifest, evaluation script, hidden test files, or Git metadata** in this workspace.

---

# PART 1 — Executive Summary

## What problem are we solving?

We must predict the **construction-era class of buildings within a 30 m × 30 m satellite pixel**.

The important challenge is not merely classification within one city:

> **Learn from Madrid, then adapt that learned model to Amsterdam using very few labelled Amsterdam pixels.**

Each pixel has decades of Landsat observations across six spectral bands. These observations may reveal building materials, surrounding vegetation, land-use changes, and construction-related changes.

We predict **four classes**, not an exact construction year.

## Why does it matter?

Building-age records support:

- Urban planning.
- Infrastructure maintenance.
- Energy-efficiency policy.
- Risk assessment.

Many cities lack complete records. A model requiring only a small local labelling effort would be more useful than one requiring a new large training dataset for every city.

## What are we expected to submit?

The clearest requirements, in `1-Introduction.ipynb`, are:

1. A trained Madrid Stage 1 model.
2. Runnable, reproducible Amsterdam adaptation code with configurable labels per class.
3. A PowerPoint presentation with an abstract, results, and learning curve.
4. A short written justification.

Organisers intend to evaluate on **held-out Madrid and Amsterdam datasets not supplied here**.

## What does success look like?

A successful submission:

- Demonstrably transfers something learned from Madrid.
- Performs well at **25 Amsterdam labels per class**, particularly.
- Reports mean and standard deviation macro F1 across repeated evaluations.
- Uses a defensible, leakage-free protocol.
- Explains why the method works—or what a failed experiment teaches.
- Runs from a clean session.
- Gives all four team members meaningful contributions and speaking roles.

**There is no supported “winning F1 threshold.”** The starter’s approximately 0.60 Amsterdam macro F1 is a reference, not an organiser target.

### Most important findings

| Finding | Why it matters |
|---|---|
| Notebook 4’s Amsterdam prototypes do **not use the trained Madrid Random Forest** | Copying it unchanged may not satisfy the intended transfer-learning requirement |
| Actual scenes span many seasons, not just summer | Apparent building-age signals may partly reflect seasonal sampling |
| Preprocessing requires labels even to construct features | It is not ready for genuinely unlabelled hidden-test inference |
| Class boundaries use right-inclusive intervals | Thousands of boundary-year pixels can be mislabelled by an apparently harmless change |
| Submission documents conflict | We need written clarification before final packaging |
| Creativity carries **40/100 rubric points** | A justified original contribution matters substantially—not just leaderboard optimisation |

---

# PART 2 — Challenge Breakdown

## Inputs

### Stage 1: Madrid

- Multiyear Landsat spectral observations.
- Pixel metadata and building coverage.
- `weighted_mean_year`, used to derive training labels.

### Stage 2: Amsterdam

- The same input schema.
- A restricted labelled support sample:
  **5, 25, 50, 100, or 200 pixels per class**, according to Notebook 1.
- Remaining pixels used for evaluation under a controlled protocol.

For four classes, these budgets mean **20, 100, 200, 400, and 800 labelled pixels total**.

## Outputs

- One predicted integer **1–4 per geographic pixel**.
- Madrid macro F1 mean and standard deviation.
- Madrid confusion-matrix proportions.
- Amsterdam macro F1 mean and standard deviation at each required budget.
- A reusable trained model and adaptation procedure.

Probability outputs and maps are useful diagnostics, but are not explicitly mandatory submission files.

## Target definition

The notebooks derive `age_class` by binning `weighted_mean_year`.

**Actual implemented intervals:**

| Class | Madrid | Amsterdam |
|---|---|---|
| 1 | Year ≤ 1960 | Year ≤ 1945 |
| 2 | 1960 < year ≤ 1984 | 1945 < year ≤ 1984 |
| 3 | 1984 < year ≤ 2004 | 1984 < year ≤ 2004 |
| 4 | Year > 2004 | Year > 2004 |

This follows the default right-inclusive behaviour of `pd.cut()`.

**Important ambiguity:** Notebook 1 describes a “majority age class,” but the available label is an **area-weighted mean construction year**. Binning a mean is not mathematically equivalent to selecting the majority building-era class.

Use the supplied implementation provisionally; request confirmation.

## Evaluation metric

**Macro F1** averages the F1 score of each of the four classes equally.

Consequences:

- The largest class must not dominate model selection.
- Accuracy is not interchangeable with macro F1.
- Weighted F1 is not the requested metric.
- Confusion-matrix diagonals show class recall, not class F1.
- Four classes do not imply a universal random macro-F1 baseline of 0.25.

## Constraints and assumptions

### Confirmed or directly stated

- Madrid is the source city.
- Amsterdam is the adaptation target.
- Stage 1 must be trained entirely on Madrid.
- Adaptation must support configurable sample size per class.
- End-to-end execution must use a fixed seed.
- Hidden test sets are unavailable here.
- AI coding assistants are allowed.
- Spatial context is explicitly permitted in Notebook 1.
- Metric learning is optional, not mandatory.

### Not established

- Whether unlabelled target/query data may be used for distribution alignment.
- Whether Amsterdam labels may be used for hyperparameter development beyond episode support samples.
- Exact hidden-test splitting and sampling procedure.
- Whether multiple specialised models can be submitted.
- Official runtime and inference interface.
- GPU availability.

## Contradictions requiring attention

| Topic | Conflicting evidence | Safe provisional approach |
|---|---|---|
| Amsterdam budgets | Notebook 1 lists five; presentation text refers to four; Notebook 4 adds 10-shot | Implement all five stated budgets; treat 10-shot as diagnostic |
| Justification limit | Notebook 1: 300 words; rubric: 500 | Stay within **300 words** |
| Prizes | Notebook 1 lists four prizes; rubric mentions Best Overall | Prepare for both; ask which governs |
| Scoring | Lecture transcript says dry-run scoring was not planned | Do not treat that as overriding the rubric |
| Transfer direction | Metric-learning guide says Amsterdam → Madrid | Follow Madrid → Amsterdam |
| Number of classes | Metric-learning guide suggests five | Use four |
| Time span | Documentation says 1984–2024 | Actual files contain **1984–2025** |
| Season | Documentation says summer scenes | Actual acquisitions occur across the year |
| Class imbalance | Notebook 2 says Class 1 dominates | Actual largest class is **Class 2** in both cities |
| RF balancing | Notebook 4 says imbalance was not addressed | Code already uses `class_weight='balanced'` |
| Hardware/team size | Orientation discusses three people | Your plan uses four; confirm shared access |

## Things competitors may overlook

1. `pixel_id` includes acquisition year: it is a **pixel-year ID**, not a stable geographic ID.
2. Grouping should use `(city, px_key, py_key)` when cities are combined.
3. The three slots are ordered by acquisition date—not necessarily quality.
4. “First QA-valid” is not necessarily the most comparable observation across cities.
5. All Amsterdam labels being present does not make unrestricted use legitimate.
6. Construction-year-centred feature windows would leak the answer.
7. Hidden-test feature generation cannot require construction year.
8. Random pixel CV can overstate generalisation because nearby pixels share urban context.
9. Classes 1 and 2 have different historical meanings across cities.
10. Neither notebook saves a finished submission package.

---

# PART 3 — Deliverables

## Mandatory

| Deliverable | Required contents |
|---|---|
| **Madrid Stage 1 model** | Trained model; include necessary preprocessing and representation state |
| **Adaptation code** | Takes Stage 1 model and labelled Amsterdam support data; configurable `n`; fixed seed; runnable end-to-end |
| **Madrid evaluation** | Cross-validation macro F1 mean/std and confusion-matrix proportions |
| **Amsterdam evaluation** | Repeated evaluation at required support budgets; macro F1 mean/std |
| **PowerPoint** | First-slide abstract ≤150 words; design decisions; successes/failures; results table; error bars; F1 versus log2 sample size |
| **Written justification** | Model design, transfer strategy, F1 interpretation; keep ≤300 words pending clarification |

The rubric also expects evidence of collaboration and asks whether **all team members speak**.

## Recommended

- README with exact execution and inference instructions.
- Pinned dependency versions.
- Raw-data checksums.
- Saved feature schema and class-boundary configuration.
- Saved split IDs, support IDs, and seeds.
- Machine-readable experiment/result table.
- Label-free inference smoke test.
- Source-transfer versus target-only ablation.
- Spatial validation sensitivity analysis.
- Reproducible final figures.
- Backup presentation PDF.
- Local copy of the complete submission.

## Optional

- Saved adapted models for each budget, if useful or requested.
- Probability and uncertainty maps.
- A short demonstration.
- Embedding visualisations.
- Additional 10-shot analysis.
- Active learning or pseudo-labelling, **only if allowed**.

**No mandatory prediction CSV format is supplied.** Do not invent one and assume it is accepted.

---

# PART 4 — Scoring / Rubric

Source: `Evaluation Rubric Overview.docx`.

## Complete scoring-table content

The source table’s band headings contain apparent mistakes:

- **“> 50% Poor / Minimal”**
- **“50%–75% Satisfactory / Good”**
- **“<75% Exceptional”**

These inequalities appear reversed for poor and exceptional. They should be clarified rather than silently treated as valid thresholds.

| Dimension | Poor / Minimal | Satisfactory / Good | Exceptional | Points |
|---|---|---|---|---:|
| **Challenge Understanding & Transfer Strategy** | Misunderstands domain transfer or spectral data; justification ignores cross-city shift | Solid grasp of transfer learning; logical transfer strategy for cross-city domain shift; good understanding of limitations | Deep insight into spectral representations; elegant transfer strategy addressing cross-city domain shift; excellent F1 scores and/or insightful dissection of limitation; robust, reproducible workflow | 30 |
| **Originality & Solution Creativity** | Standard off-the-shelf model with zero customization or novel transfer techniques | Applied creative feature engineering, architecture adjustments, or domain adaptation tricks | Highly novel, elegant, or insightful approach to cross-city transfer; introduces unique ideas | 40 |
| **Presentation & Team Collaboration** | Disjointed presentation; uneven team contribution; fails to communicate key points | Clear presentation; well-structured pitch; all team members actively contributed; good interpretation of performance | Engaging storytelling; masterful interpretation of performance curves—F1, loss, etc.—across sample sizes; seamless team dynamic; articulate response to technical Q&A | 30 |

The table also has deduction and comments fields, and a **total /100**.

## 1. Challenge Understanding & Transfer Strategy — 30 points

The detailed rubric evaluates:

- **Model Design & Adaptation:** Does the model specifically address source/target distribution mismatch?
- **Spectral Representation:** Do features generalise across locations rather than memorise city-specific patterns?
- **Low-Data Mechanics:** Does the team understand why 25 samples/class requires different mechanics from full-data training?

**Likely full-mark evidence:**

- Explicit explanation of domain shift.
- A real source-learned representation used during adaptation.
- Clear support/query separation.
- Reproducible results and honest limitations.
- Evidence explaining why the method helps at 25-shot.

**Common mistakes:** Calling target-only fitting “transfer,” optimising only Madrid, or claiming worldwide generalisation from two cities.

## 2. Solution Originality & Creativity — 40 points

Detailed criteria:

- **Methodological Innovation:** Creative architecture, loss, or domain-adaptation technique.
- **Problem Framing:** A unique perspective on the cross-city spectral challenge.
- **Insightful Failure:** Valuable scientific interpretation when a bold approach performs poorly.

**Explicit judge note:** A team with lower F1 can win the **Best Overall Prize** if its method is novel, well-reasoned, or opens an exciting research path.

**Likely full-mark evidence:**

- One clear, problem-specific contribution.
- A falsifiable hypothesis.
- Controlled ablations demonstrating its effect.
- Insightful interpretation, including negative findings.

**Common mistakes:** Algorithm name-dropping, complexity without evidence, or presenting standard prototypes as a newly invented method.

## 3. Presentation & Team Collaboration — 30 points

Detailed criteria:

- **Abstract & Pitch:** Concise, accurate abstract aligned with presentation.
- **Cohesion:** Meaningful contributions from all members; all speak.
- **Communication:** Clear explanation within the time limit.

**Likely full-mark evidence:**

- A coherent problem → hypothesis → experiment → result story.
- Correct explanation of learning curves and uncertainty.
- Seamless speaking transitions.
- Strong technical Q&A.

**Common mistakes:** Notebook screenshots instead of a story, unsupported claims, unreadable plots, or one person presenting everything.

## Essential pillars and deductions

The written justification—**max 500 words according to this rubric**—and presentation must cover:

1. **Model Design:** Rationale for model and parameters.
2. **Transfer Strategy:** How learned representations adapt to Amsterdam.
3. **F1 Interpretation:** Performance trends across the stated scores/sample sizes.

**Deduct up to 5 points if:**

- The justification exceeds 500 words.
- The presentation or justification omits an essential pillar.

**Deduct up to 20 points, or disqualify the team or particular members, if:**

- The method is scientifically unsound, including leakage.
- The method is off-topic, including not performing transfer learning.
- Members behave unprofessionally.

The document does not specify detailed subcriterion allocations or whether deductions accumulate.

## Separate prize rules in Notebook 1

| Prize | Stated basis |
|---|---|
| Best average F1 | Mean F1 across all five Amsterdam models |
| Best peak F1 | Highest F1 among Amsterdam models |
| Best low-data F1 | F1 at 25 samples/class |
| Best originality | Abstract and presentation |

A team may win multiple categories.

**Strategic implication:** Prioritise scientific validity, a credible original idea, and presentation—not tiny metric gains at any cost.

---

# PART 5 — Repository Tour

## Every workspace file

“Yes” below means modify a **team-owned working copy**, preserving the supplied original.

| Filename | Purpose | Importance | Edit? | Notes |
|---|---|---|---|---|
| `1-Introduction.ipynb` | Task, labels, submissions, prizes, data background | High | No | Main challenge specification; contains inconsistencies |
| `2-Reading_Data.ipynb` | Data exploration and quality diagnostics | High | Yes | Fix paths; extend targeted QA; preserve baseline |
| `3-Preprocessing.ipynb` | Raw data → 60 features per pixel | High | Yes | Must become label-independent and fold-safe |
| `4-Modelling.ipynb` | RF CV, zero-shot test, prototype experiments, maps | High | Yes | Substantially redesign transfer and export |
| `amsterdam_data.parquet` | Labelled target-city adaptation/evaluation data | High | No | Keep immutable; control label access |
| `madrid_train.parquet` | Labelled source-city data | High | No | Keep immutable |
| `building_age_transfer_learning_hackathon.md` | Lecture transcript and logistics | High | No | Useful interpretation; some older requirements |
| `Evaluation Rubric Overview.docx` | Judging criteria and penalties | High | No | 30/40/30 scoring; major compliance source |
| `hackathon_computing_resources.md` | Server access, memory, package and backup instructions | High | No | 16 CPUs, 128 GB RAM, 200 GB disk stated |
| `METRIC_LEARNING_APPROACH.md` | Suggested triplet embedding and few-shot methods | Medium | No | Optional concept note; wrong task direction/classes |
| `Open Notebook.onetoc2` | OneNote table-of-contents binary | Low | No | No readable content extracted; no section files supplied |
| `WhatsApp Image 2026-09-07 at 14.51.21.jpeg` | Screenshot of colour-coded participant names | Low | No | No model/rubric information; colours have no supplied legend |

The JPEG groups **Ametor Humelo Buanyomi, Sibusiso Mathebula, Mzwandile Fuku, and Jaswin Chinthala** together visually. Confirm that this is your team before assigning names to responsibilities.

## Notebook 1 — `1-Introduction.ipynb`

**Purpose:** Understand the challenge before any execution.

**Inputs:** None.  
**Outputs:** Documentation only; no computation or saved artifacts.  
**Action:** Read and reference; do not treat all prose as internally consistent.

| Section | What it does |
|---|---|
| 1.1 Welcome | Introduces classification and four-notebook structure |
| 1.2 Challenge | Defines 30 m pixel inputs and integer class output |
| 1.3 Background | Explains urban applications and scarce-label motivation |
| 1.4 Age Classes | Defines four eras and derivation from weighted construction year |
| 1.5 Submission & Evaluation | Specifies CV, budgets, artifacts, presentation, word limits, prizes |
| 1.6 Dataset | Describes upstream scene selection, harmonisation, footprint linking, wide format |
| 1.7 Cities | Establishes Madrid source and Amsterdam target |
| 1.8 Next Steps | Directs users to exploratory and modelling notebooks |

## Notebook 2 — `2-Reading_Data.ipynb`

**Purpose:** Explore data structure, quality, class differences, and temporal signals.

**Inputs:** Both Parquet files via `../data`.  
**Outputs:** In-memory raw/flat tables, pixel statistics, printed summaries, and 25 saved plot outputs. **No persisted feature dataset.**  
**Action:** Use as an EDA reference and modify a copy for focused auditing.

| Section/block | What it does |
|---|---|
| 2.1 Setup | Imports NumPy, pandas, matplotlib; sets paths, bands, class boundaries |
| 2.2 Loading | Loads Madrid, derives classes, previews metadata and observation slots |
| Flat-view helpers | Selects first QA-valid observation per band; removes Blue >15,000 |
| Amsterdam loading | Applies equivalent processing and creates shared city iteration structure |
| 2.3 Columns | Documents metadata, bands, QA, dates, and identifiers |
| 2.4 Coverage | Prints coverage statistics; plots histogram and cumulative distribution |
| 2.5 Class distribution | Counts unique pixels per class and plots construction years |
| 2.6 Individual trajectories | Selects three spatially spread examples per class; plots Blue, NIR, SWIR1 histories |
| 2.7 Class-level trends | Plots annual class means with pixel-to-pixel standard-deviation shading |
| Pixel temporal statistics | Calculates means/stds and successive-observation differences |
| Histograms | Compares class distributions of level, variability, and change |
| Scatter grids | Examines overlap and relationships among temporal statistics |
| 2.8 Feature exploration | Band summaries, zero/saturation checks, correlation matrices |
| Summary | Suggests feature directions; contains stale class-dominance claims |

**Important issues:**

- Coverage histograms use pixel-year rows while labelling them “pixels.”
- Differences can span missing years; they are not always true one-year differences.
- Three selected trajectories are illustrative, not representative evidence.
- Suggested windows around **known construction year** must never become inference features.
- The cirrus-bit explanation for Landsat 7 needs sensor-specific verification.
- Saved quality checks report residual corrupt values despite “pre-cleaned” descriptions.

## Notebook 3 — `3-Preprocessing.ipynb`

**Purpose:** Produce one fixed-length feature vector per pixel.

**Inputs:** Both raw Parquets; class boundaries; fixed Blue threshold.  
**Outputs:** Standardised arrays, labels, IDs, scaler, feature names/groups, written to:

`../data/preprocessed/preprocessed_data.pkl`

The saved notebook reports approximately **48.4 MiB**. That file is **not currently present**.

**Action:** Modify substantially before production use.

| Section | What it does |
|---|---|
| 3.1 Setup | Defines bands, indices, class mapping, colours |
| 3.2 Load | Loads both datasets and reports dimensions |
| 3.3 Labels | Uses `pd.cut()` to derive four classes |
| 3.4 Flatten | Selects first valid observation; drops incomplete/hazy rows |
| Coverage indicators | Records whether original observations exist before/after 2004 |
| 3.5 Gap filling | Builds complete annual grid; interpolates interior gaps; fills edges |
| Second 3.5: indices | Computes NDVI, NDBI, UI, MNDWI, BSI |
| 3.6 Features | Aggregates overall, early, late, and change statistics |
| Class chart | Displays pixel-level class counts |
| 3.7 Standardisation | Fits `StandardScaler` on all Madrid features; transforms Amsterdam |
| 3.8 Save | Pickles features, labels, IDs, scaler, schema |
| 3.9 Summary | Documents preprocessing pipeline |

### The 60 starter features

| Feature group | Count |
|---|---:|
| Six bands: overall mean/std | 12 |
| Five indices: overall mean/std | 10 |
| Six bands: 1984–2003 mean/std | 12 |
| Six bands: 2004 onward mean/std | 12 |
| Six bands: annual-difference mean/std | 12 |
| Early/late availability flags | 2 |
| **Total** | **60** |

### Required fixes

- Feature generation filters/group-bys using `age_class` and carries `weighted_mean_year`. It needs a **label-free transform path**.
- Scaling before Madrid CV exposes validation-feature statistics. Fit learned transformations inside folds.
- `coverage` is dropped before feature engineering.
- Selected hazy observations are discarded without trying later valid slots.
- The annual horizon is derived from input data rather than a saved feature contract.
- `mkdir(exist_ok=True)` lacks `parents=True`; the absent expected directory hierarchy matters.
- No class resampling is implemented despite introductory references to balancing.

## Notebook 4 — `4-Modelling.ipynb`

**Purpose:** Demonstrate source classification, domain shift, few-shot prototypes, and spatial diagnostics.

**Inputs:** Notebook 3’s pickle.  
**Outputs:** In-memory models, predictions, scores, and plots.  
**Does not save:** Trained RF, adapted prototypes, submission predictions, or a final package.  
**Action:** Treat as an example; substantially replace the transfer/evaluation/export workflow.

| Section | What it does |
|---|---|
| 4.1 Setup | Imports Random Forest and evaluation utilities |
| 4.2 Load | Loads standardised arrays, labels, IDs, feature names |
| 4.3 Madrid CV | Runs 5 folds ×5 repeats, 500-tree balanced RF |
| CV plots | Displays fold scores and aggregated row-normalised OOF confusion matrix |
| 4.3a Spatial diagnostics | Maps class probabilities, entropy, true-class log loss, correct/incorrect predictions |
| 4.4 Final Madrid model | Fits RF on all Madrid; prints in-sample accuracy |
| 4.5 Importance | Plots impurity-based feature importance |
| 4.6 Zero-shot | Applies final Madrid RF directly to Amsterdam; reports performance and maps |
| 4.7 Few-shot | Samples support points; computes Amsterdam class means; predicts nearest prototype |
| Budget curve | Shows mean/std over 10 support draws at six budgets |
| Confusion examples | Shows separate 25- and 100-shot draws |
| Prototype probability maps | Uses softmax of negative distance for 25-shot visualisations |
| 4.8 Summary | Offers unverified improvement suggestions |

### Critical interpretation

The few-shot function receives **only Amsterdam feature vectors and labels**. It never receives `rf_final` or RF-derived embeddings.

Madrid contributes the feature scaling, but **Madrid supervised learning is absent from the adaptation path**.

Therefore:

> The notebook demonstrates useful few-shot classification, but does not establish that a Madrid-trained classifier or supervised representation transfers.

### Other issues

- Repeated CV scores are not statistically independent merely because splits change.
- Repeated OOF map entries overwrite the same pixel rather than average its probabilities.
- Prototype softmax scores are not automatically calibrated probabilities.
- True-class log loss requires labels; it is not deployable uncertainty.
- Grey map pixels mean absent/excluded pixels, not necessarily “no building.”
- The budget axis uses default logarithmic scaling, not explicitly base 2.
- Individual confusion matrices are single draws, not the trial-average result.
- In-sample RF accuracy of 1.0 is not generalisation evidence.

### Saved starter results

| Experiment | Macro F1 |
|---|---:|
| Madrid RF, 5×5 CV | **0.6179 ±0.0043** |
| Amsterdam zero-shot RF | **0.3427** |
| Amsterdam prototypes: 5/class | **0.5437 ±0.0324** |
| 10/class—extra diagnostic | **0.5649 ±0.0312** |
| 25/class | **0.5986 ±0.0176** |
| 50/class | **0.6079 ±0.0101** |
| 100/class | **0.6129 ±0.0097** |
| 200/class | **0.6150 ±0.0036** |

The strong prototype result makes this an essential baseline—but not sufficient evidence of supervised transfer.

---

# PART 6 — Data Understanding

## Source and provenance

The documentation describes:

- Landsat 5, 7, 8, and 9 observations.
- Building footprints linked to construction records.
- Area-weighted construction year per pixel.
- Cross-sensor spectral harmonisation.
- Coverage filtering at 15%.

Amsterdam’s labels are described as BAG-derived in Notebook 3. The exact Madrid source/version, processing implementation, licences, and full provenance are not supplied.

The upstream raw-processing notebooks are explicitly absent.

## Dataset sizes: independently verified

| Property | Madrid | Amsterdam |
|---|---:|---:|
| File | `madrid_train.parquet` | `amsterdam_data.parquet` |
| Disk size, decimal MB | 141.96 | 43.84 |
| Rows | 3,172,765 | 1,062,877 |
| Columns | 48 | 48 |
| Geographic pixels | 76,263 | 25,992 |
| Acquisition years | 1984–2025 | 1984–2025 |
| Distinct years | 42 | 42 |
| Mean rows per pixel | 41.60 | 40.89 |
| Minimum rows per pixel | 13 | 8 |
| Maximum rows per pixel | 42 | 42 |
| Construction-year range | 1850–2021 | 1850–2016 |
| Null cells | 0 | 0 |
| Duplicate pixel-year keys | 0 | 0 |
| Duplicate `pixel_id` | 0 | 0 |

**Combined:** 4,235,642 pixel-year rows representing **102,255 geographic pixels**.

The transcript’s 76,263 count refers to Madrid, not the combined dataset.

## All 48 columns

### Twelve metadata columns

| Columns | Meaning/use |
|---|---|
| `pixel_id` | String containing city, grid coordinates, acquisition year |
| `city` | Source/target identity |
| `year` | Acquisition year—not construction year |
| `px_key`, `py_key` | Stable geographic grid indices |
| `pixel_x`, `pixel_y` | Projected coordinates |
| `row`, `col` | Raster-position metadata; exact convention not documented |
| `coverage` | Building-footprint fraction |
| `usable_label` | Label-usability flag; **True for all supplied rows** |
| `weighted_mean_year` | Continuous label source; exclude from features |

### Twelve columns repeated for each slot N = 1, 2, 3

| Columns | Meaning |
|---|---|
| `Blue_N`, `Green_N`, `Red_N`, `NIR_N`, `SWIR1_N`, `SWIR2_N` | Six spectral measurements |
| `QA_PIXEL_N` | Pixel QA bitmask |
| `QA_RADSAT_N` | Radiometric/saturation QA bitmask |
| `doy_N` | Acquisition day of year |
| `scene_id_N` | Scene identity |
| `dataset_N` | Sensor/collection family |
| `qa_valid_N` | Provided validity flag |

That is **12 metadata +36 observation columns =48**.

## Class distribution

| Class | Madrid count | Madrid % | Amsterdam count | Amsterdam % |
|---|---:|---:|---:|---:|
| 1 | 13,794 | 18.1 | 7,568 | 29.1 |
| 2 | 27,152 | 35.6 | 8,802 | 33.9 |
| 3 | 18,672 | 24.5 | 6,745 | 26.0 |
| 4 | 16,645 | 21.8 | 2,877 | 11.1 |

Amsterdam Class 4 is particularly underrepresented.

### Boundary-year sensitivity

| Exact year | Madrid pixels | Amsterdam pixels |
|---|---:|---:|
| City event: 1960 /1945 | 2,227 | 2 |
| 1984 | 407 | 429 |
| 2004 | 1,107 | 188 |

The inclusion convention is therefore consequential, not cosmetic.

## Coverage and relationships

Verified per-geographic-pixel coverage:

| Statistic | Madrid | Amsterdam |
|---|---:|---:|
| Mean | 50.51% | 42.12% |
| Median | 46% | 37% |
| Range | 15%–100% | 15%–100% |

Within each geographic pixel, construction year, coverage, and coordinates are constant across years.

The cities share a schema but are **not matched observations of the same buildings**. There is no cross-city building correspondence.

Coverage is potentially useful because low-coverage pixels contain substantial non-building signal. It is not automatically leakage, but hidden-test availability and derivation should be confirmed.

## Missingness and quality

**No null values does not mean complete or clean observations.**

- Invalid observations remain as populated values with `qa_valid=False`.
- Entire pixel-year records can be absent.
- Invalid or extreme values can remain even after first-valid selection.

| Starter flattening outcome | Madrid | Amsterdam |
|---|---:|---:|
| Blue >15,000 rows removed | 34,845 | 12,917 |
| Retained pixel-year rows | 3,137,920 | 1,049,960 |
| Retained rows containing zero or exact 65535 | 23 | 7 |

Large values above 66,000 also remain in some non-Blue bands. Harmonisation complicates simplistic raw saturation thresholds; confirm processing conventions.

I also found nonzero `QA_RADSAT` in selected observations. This needs bit-level interpretation—not automatic blanket deletion.

### Recoverable observations

Among rows removed for selected-observation haze:

- **10,359 Madrid rows**
- **8,373 Amsterdam rows**

have an alternative QA-valid slot meeting the simple Blue threshold and positive-band check.

This does not prove those alternatives are perfectly clean, but it demonstrates that the starter unnecessarily discards potentially usable observations.

## Major discovery: seasonal mismatch

The “summer-only” description is inconsistent with actual dates.

Selected first-valid observations occur in **every month** in both cities.

Approximately:

- **49%** of selected Madrid observations are June–August.
- **30%** of selected Amsterdam observations are June–August.

Amsterdam is heavily represented in spring.

This matters because vegetation, moisture, illumination, and seasonal surface behaviour affect spectra. Some “city shift” or “age trend” may actually be acquisition-season shift.

**Feature priority:** Test season-aware observation selection before building a substantially more complex model.

## Feature opportunities

### Highest priority

1. Quality-aware slot selection with fallback.
2. More comparable acquisition seasons across cities.
3. Robust multiyear medians and variability.
4. Early-versus-late contrasts.
5. Label-free change timing and persistence.
6. Coverage and coverage interactions.
7. Observation counts, gap lengths, and seasonal availability.

### Secondary

- Per-decade summaries.
- Robust slopes.
- Cross-band agreement in change events.
- Relative temporal shape alongside absolute reflectance.
- Feature-group weighting to reduce redundant RGB/statistical contributions.

## Leakage risks

Exclude from predictive inputs:

- `weighted_mean_year`.
- `age_class`.
- Any transformation explicitly centred on the true construction year.
- Aggregates incorporating query labels.
- Spatial summaries of held-out true labels.

Coordinates and scene identities are not automatically label leakage, but can act as brittle city/neighbourhood shortcuts.

**A full historical trajectory is not itself leakage** when the task permits all observations to classify current buildings. It would become inappropriate for a historical forecasting task, which this repository does not specify.

## Derived and absent datasets

Notebook 3 creates:

- Madrid: **76,263 ×60** features.
- Amsterdam: **25,992 ×60** features.
- Labels, coordinates, feature groups, scaler.

That processed dataset is absent from the workspace.

Hidden Madrid and Amsterdam test sets are also absent; their dimensions and precise schema are unknown.

---

# PART 7 — Notebook Dependency Graph

## Reading order

**1 →2 →3 →4**

Read the rubric alongside Notebook 1.

## Actual execution dependencies

```text
1-Introduction.ipynb
    Documentation only

madrid_train.parquet ──┬──> 2-Reading_Data.ipynb
amsterdam_data.parquet ┘       EDA only; no saved dependency

madrid_train.parquet ──┬──> 3-Preprocessing.ipynb
amsterdam_data.parquet ┘                │
                                       ▼
                            preprocessed_data.pkl
                                       │
                                       ▼
                              4-Modelling.ipynb
                          Metrics and in-memory models
```

### What runs first?

- Notebook 1 does not need execution.
- Notebook 2 is the first exploratory notebook.
- For the computational pipeline, **Notebook 3 is the first required producer**.

### Does Notebook 3 depend on Notebook 2?

**No file dependency.** It repeats its own loading and helpers.

### Which are examples?

- Notebook 2: exploratory example.
- Notebook 3: suggested preprocessing.
- Notebook 4: baseline modelling/adaptation example.

### Which produces final outputs?

- Notebook 3 produces an intermediate pickle.
- Notebook 4 produces evaluation outputs but **does not export the final submission artifacts**.

### Immediate execution blocker

All executable notebooks assume a `notebooks/` and `../data/` hierarchy. Actual files are all in the workspace root.

Do not expect “Run All” to work unchanged.

---

# PART 8 — Winning Strategy

## Overall recommendation

> Build a reliable baseline first, then add one demonstrably source-learned, low-data transfer contribution, supported by season/quality-aware temporal features.

Avoid a broad algorithm sweep. The rubric rewards reasoning, originality, transfer mechanics, and collaboration.

## A. Modelling strategy

### Baseline ladder

Use identical evaluation episodes for:

1. Majority-class reference.
2. Madrid Random Forest → Amsterdam zero-shot.
3. Starter-style Amsterdam prototypes.
4. **Source-learned metric/embedding → Amsterdam prototypes.**

The fourth method must actually use a learned Madrid artifact.

### Main technical direction

A **compact source-supervised representation with a simple target prototype head** is well matched to:

- 60-dimensional starter features.
- Large Madrid source data.
- Very small Amsterdam support sets.
- Explicit low-data scoring.
- The repository’s prototype and metric-learning suggestions.

Train the representation on Madrid, then freeze it initially. For each Amsterdam episode:

1. Transform support and query features with the saved source pipeline.
2. Compute class prototypes from support labels only.
3. Predict query classes by distance.
4. Evaluate on query labels held outside model fitting.

At 25/class, freezing the representation reduces the temptation to fit a high-capacity target model to only 100 points.

**Lower-complexity fallback:** A Madrid-supervised feature-weighting/metric transformation with prototypes. This is preferable to an unfinished neural solution.

**Higher-budget extension:** Only test a regularised target head or limited fine-tuning after the frozen approach works.

### Original contribution worth testing

**Separate temporal change from static spectral appearance.**

- Classes 3/4 may contain an observable construction or redevelopment event.
- Classes 1/2 predate observation and rely more on persistent appearance/context.
- Season changes can masquerade as temporal construction signals.

Test a representation with separate static and temporal feature groups, including season-aware preprocessing. Compare it with the undifferentiated 60-feature baseline.

This is a repository-grounded hypothesis—not a claim that it will win.

### Prove that transfer helps

Compare:

- Raw-feature target prototypes.
- Source-learned representation +target prototypes.
- Equivalent untrained/unlearned representation where practical.

Without this comparison, improvement over zero-shot RF may simply reflect using Amsterdam labels and changing classifiers.

## B. Validation strategy

### Madrid

- Keep all years of a pixel together.
- Fit scaler, feature selection, and representation within each training fold.
- Use stratified pixel CV for starter comparability.
- Add spatial-block validation as a robustness check.
- Refit the final source pipeline on all Madrid only after selection.

### Amsterdam

Define:

- **Support:** labels adaptation may use.
- **Query:** labels evaluation may inspect only after prediction.

Use repeated episodes at all five official-looking budgets.

For development:

- Share fixed support/query episode definitions across competing methods.
- Prefer nested support budgets within a trial for cleaner learning-curve comparisons.
- Keep a separate final audit partition or final evaluation episodes unused for tuning.
- Add spatially separated support/query experiments where feasible.

Repeated support sampling is the starter protocol; it is not conventional k-fold CV. Ask organisers what they specifically expect.

### Label-budget discipline

- Sampling infrastructure may inspect labels to obtain `n` per class.
- The adaptation method receives only selected support labels.
- Hyperparameters must not be chosen by repeatedly inspecting the final query scores.
- Never use all Amsterdam construction years in feature generation.

### Error bars

Report explicitly:

- Mean macro F1.
- Standard deviation across folds or episodes.
- Number of folds/repeats/trials.
- What varied: support draw, fold, or model seed.

Do not label standard deviation as a confidence interval.

## C. Experimentation strategy

Keep a small hypothesis-driven matrix:

| Experiment | Question |
|---|---|
| Reproduced baseline | Can we trust our pipeline? |
| Slot fallback and improved QA | Are discarded/contaminated observations hurting us? |
| Season-aware selection | How much apparent domain shift is seasonal? |
| Coverage feature | Does footprint fraction help across cities? |
| Temporal contrasts/change features | Is construction-era information being preserved? |
| Source-supervised representation | Does Madrid supervision improve target few-shot learning? |
| Static/temporal separation | Do different era mechanisms deserve different feature treatment? |

Record each experiment’s:

- Commit.
- Feature version.
- Split/episode version.
- Seeds.
- Parameters.
- Per-budget scores and standard deviations.
- Per-class results.
- Runtime and memory.
- Decision and interpretation.

**Gate:** An experiment must improve reliable results or teach a clear scientific lesson to justify inclusion.

## D. Feature engineering priorities

1. Fix observation selection and quality.
2. Verify radiometric units before interpreting index formulas physically.
3. Account for season and sensor effects.
4. Preserve temporal change without using construction labels.
5. Add coverage if available at inference.
6. Reduce redundancy for distance models.
7. Add complexity only after ablation evidence.

Do not assume indices are physically correct just because ratios cancel multiplicative scaling: **additive offsets do not cancel**.

## E. Notebook organisation

Preserve the four originals.

Team working organisation should separate:

- Data audit.
- Label-free feature transformation.
- Source training.
- Target adaptation/evaluation.
- Final report figures.
- Clean inference/export demonstration.

Shared reusable logic should eventually live outside notebooks to prevent copy-pasted drift. That is an implementation recommendation, not something already present.

## F. Version control and compute

- Initialise a shared Git workflow.
- Assign one owner per notebook/module.
- Use short feature branches and reviewed merges.
- Keep datasets, large models, caches, and credentials out of ordinary Git.
- Save raw-data checksums and artifact locations.
- Tag a working baseline before experimentation.
- Limit concurrent CPU-heavy jobs; `n_jobs=-1` in several notebooks will oversubscribe the server.
- Run expensive preprocessing once and share versioned feature caches.
- Back up before the organiser server shuts down.

---

# PART 9 — Risk Assessment

| Severity | Risk | Mitigation |
|---|---|---|
| **Critical** | Target year/class leaks into features | Label-free feature API; explicit feature allowlist |
| **Critical** | Amsterdam query labels enter training or tuning | Enforced support/query separation and final audit set |
| **Critical** | No genuine Stage 1 transfer | Adaptation must consume source-learned state; prove by ablation |
| **Critical** | Hidden-test inference requires labels | Remove labels and successfully run inference before submission |
| **High** | Wrong class-boundary convention | Confirm intervals; test exact boundary years |
| **High** | Wrong metric or budget list | Use macro F1 over fixed four classes; configurable five budgets |
| **High** | Spatial dependence inflates validation | Pixel grouping and spatial sensitivity checks |
| **High** | Season effects mistaken for age | Date-aware diagnostics and season-aware ablation |
| **High** | Sensor artifacts mistaken for construction | Check sensor transitions and cross-band persistence |
| **High** | Incorrect band scaling/index interpretation | Confirm upstream radiometry; do not rescale blindly |
| **High** | Residual saturation/cloud/fill artifacts | Interpret QA masks; compare slot-level quality |
| **High** | Sparse target support overfits | Frozen source representation and regularised target mechanics |
| **High** | Adaptation overwrites source artifact | Immutable Stage 1 checkpoint and episode-local state |
| **High** | Wrong paths or absent processed file | Clean root-relative configuration and smoke test |
| **High** | Model never exported | Explicit save/load test by a different member |
| **High** | Submission limit/interface ambiguity | Obtain written organiser clarification |
| **High** | Server shutdown or lost work | Local and shared backups before final day |
| **Medium** | Pre-CV scaling contamination | Fit all learned transforms inside folds |
| **Medium** | Interpolation fabricates stability/change | Track missingness; assess long gaps and edge fills |
| **Medium** | Haze filtering discards useful slots | Attempt quality-controlled alternatives first |
| **Medium** | Feature horizon differs at inference | Save a fixed annual-window/schema contract |
| **Medium** | Redundant features dominate distances | Group weighting/reduction selected inside training |
| **Medium** | Class 2 bias and weak Class 4 | Macro-F1 selection; class-balanced source training; per-class analysis |
| **Medium** | Repeated-CV uncertainty overclaimed | Report descriptive spread and dependence honestly |
| **Medium** | Attractive but misleading maps | OOF/held-out maps; aggregate repeated predictions correctly |
| **Medium** | Confidence treated as correctness | Distinguish entropy, calibration, and labelled error |
| **Medium** | Full pairwise metric computations explode | Sample pairs/triplets; avoid all-pixel distance matrices |
| **Medium** | Shared CPU/RAM contention | One heavy job at a time; monitor kernels and memory |
| **Medium** | Different package versions change execution | Pin tested environment and rerun cleanly |
| **Medium** | Notebook merge conflicts/stale outputs | Ownership, shared helpers, clean final execution |
| **Medium** | Feature selection uses target audit labels | Restrict all selection to development protocol |
| **Medium** | Weighted mean treated as exact building age | Explain mixed-pixel label uncertainty |
| **Medium** | Claims of global portability exceed evidence | Describe two-city transfer as evidence, not proof |
| **Medium** | Presentation underweighted | Protect rehearsal and interpretation time |
| **Low** | Irrelevant files consume attention | Preserve roster/OneNote files; do not treat as technical specifications |

---

# PART 10 — Two-Day Execution Plan

## Roles

Use role labels until team membership and strengths are confirmed.

| Member | Responsibility |
|---|---|
| **A — Lead / evaluation owner** | Requirements, splits, metrics, leakage review, integration |
| **B — Data / features owner** | Raw QA, observation selection, feature pipeline, schema |
| **C — Model / transfer owner** | Source model, learned representation, target adaptation |
| **D — Reproducibility / communication owner** | Environment, experiment records, packaging, slides, independent reruns |

**Finish target:** A valid submission by **Day 1 evening**; final candidate frozen by **Day 2 early afternoon**.

## Build Day 1

| Time | A | B | C | D | Checkpoint / merge |
|---|---|---|---|---|---|
| 09:00–09:45 | Submit organiser questions; freeze provisional rules | Review data findings | Review baseline and transfer gap | Set repository structure and ownership | Everyone explains task and leakage risks |
| 09:45–11:00 | Define split/episode contract and metric reporting | Fix working-copy paths; design label-free transform | Define Stage 1/adaptation interface | Capture environment; establish result log and smoke-test checklist | **11:00:** Interfaces agreed |
| 11:00–12:30 | Verify grouping, label budget, boundaries | Generate baseline feature cache | Reproduce RF and raw-prototype baselines on development runs | Independently test clean loading; begin slide outline | **12:30 merge:** Baseline pipeline |
| 12:30–13:00 | All: review baseline discrepancies, blockers, compute schedule | | | | No new model work if baseline is broken |
| 13:00–15:00 | Compare matched episodes; create per-class diagnostics | Test QA fallback and season-aware candidate | Build compact source-learned representation +prototype adaptation | Track experiments; draft problem/data/validation slides | **15:00:** One real-transfer candidate runs |
| 15:00–16:30 | Conduct leakage and metric review | Compare feature variants; retain justified changes | Evaluate 5- and 25-shot first; then larger budgets | Run label-free inference and artifact reload checks | **16:30 merge:** Valid transferable pipeline |
| 16:30–17:30 | Evaluate candidate against target-only baseline | Freeze feature version 1 | Save source model and adaptation state/config | Assemble preliminary submission and backups | **17:30:** Submission-shaped package exists |
| 17:30–18:00 | All: results review, select at most two Day 2 experiments | | | | Tag Day 1 checkpoint |

### Day 1 expected outputs

- **A:** Written protocol, split/episode IDs, organiser issue log.
- **B:** Versioned feature cache and label-free transformation.
- **C:** Saved source model and working parameterised adaptation.
- **D:** Reproducible run instructions, results log, draft deck, backup package.

### Day 1 fallback

If the learned embedding is unstable:

- Retain a simpler Madrid-supervised metric/feature-weighting transfer.
- Stop architectural expansion.
- Preserve failed-approach diagnostics for the originality narrative.
- Do not submit an incomplete complex model merely because it sounds more novel.

## Build Day 2

| Time | A | B | C | D | Checkpoint / merge |
|---|---|---|---|---|---|
| 09:00–09:30 | Review overnight/final Day 1 results and organiser replies | Confirm features | Confirm model state | Check artifacts and backups | Freeze final experiment list |
| 09:30–11:00 | Paired comparison and spatial robustness | One targeted feature ablation | One targeted transfer ablation | Independent baseline/candidate rerun; refine figures | **11:00:** Select candidate |
| 11:00–12:30 | Lock evaluation protocol and launch final repeated runs | Freeze transform/schema | Refit final Madrid artifact after selection | Check runtime, environment, word counts, deliverable inventory | **12:30 merge:** Model/feature freeze |
| 12:30–13:30 | Audit final metrics and per-class behaviour | Validate unseen-input handling | Validate every support budget and serialization | Test full package from clean session | **13:30:** No remaining scientific changes |
| 13:30–15:00 | Write metric interpretation and limitations | Prepare data/season/feature explanation | Prepare model/transfer rationale | Finalise PowerPoint and ≤300-word justification | **15:00:** Submission-ready candidate |
| 15:00–16:00 | All: timed rehearsal; each presents their contribution | | | | Peer review against all rubric criteria |
| 16:00–17:00 | Final compliance sign-off | Verify feature artifact | Verify source/adaptation artifacts | Package, checksum, upload if permitted, back up | **17:00:** Submission frozen |
| 17:00–18:00 | All: Q&A rehearsal and contingency buffer | | | | No speculative last-minute changes |

## Day 3 — Presentation

- Confirm deck opens offline.
- Carry PowerPoint and PDF copies.
- Use saved figures rather than depend on a live training demo.
- All four speak:
  - **A:** Problem, evaluation, conclusions.
  - **B:** Data pitfalls and feature rationale.
  - **C:** Transfer method and ablation.
  - **D:** Results presentation, reproducibility, practical deployment.
- Divide time according to the organiser’s confirmed limit.
- Keep backup slides for leakage controls, class boundaries, support/query sampling, and negative results.

## Mandatory review gates

1. **Data gate:** Labels and geographic keys are correct.
2. **Inference gate:** Features work without target-year fields.
3. **Transfer gate:** Adaptation demonstrably uses source learning.
4. **Evaluation gate:** Support and query never overlap.
5. **Artifact gate:** Another member can reload and run it.
6. **Presentation gate:** All three rubric pillars and all four voices are included.

---

# PART 11 — Questions We Still Need Answered

## A. Can determine from the repository or local inspection

Already resolved:

- Actual shapes, columns, dates, labels, and duplicates.
- City direction.
- Starter feature count.
- Starter model and prototype implementation.
- Missing export artifacts.
- Path mismatch.
- Class imbalance.
- Non-summer observations.

Still locally determinable with further analysis:

- Which scenes dominate residual outliers?
- How many observations remain under sensor-correct QA rules?
- How strongly do day-of-year and sensor changes explain temporal jumps?
- How many pixels have long gaps after alternative quality filters?
- Whether nearby pixels share essentially identical spectral histories.
- Whether row/column and geographic-grid conventions differ in useful ways.
- Whether all observations for each slot are consistently date-ordered.
- Runtime and peak-memory characteristics of the final implementation.

## B. Need organiser clarification

1. Five Amsterdam budgets or four? Which exact list?
2. Is 10-shot only optional?
3. Is the justification cap 300 or 500 words?
4. Does the rubric supersede Notebook 1 prize descriptions?
5. Is there a Best Overall prize?
6. What are the correct rubric percentage bands?
7. What is the presentation time limit?
8. What are the final deadline and upload mechanism?
9. What model/artifact format and callable interface are required?
10. Are prediction files also required?
11. Are separate adapted models required, or only adaptation code?
12. Are class intervals right-inclusive as implemented?
13. Is the target explicitly binned weighted mean, rather than majority class?
14. Is 2025 data allowed and expected at inference?
15. What is the hidden-test schema?
16. Are hidden pixels geographically separated from supplied pixels?
17. Who draws the labelled support samples?
18. How many repeated trials/folds are required?
19. May unlabelled target/query data be used for alignment or pseudo-labelling?
20. How may Amsterdam labels be used during hyperparameter development?
21. Are external datasets or pretrained models permitted?
22. Are coverage and coordinates available and allowed at test time?
23. Does source-only scaling count as transfer, or is supervised source-state reuse required?
24. What radiometric scaling/offset and harmonisation were applied?
25. Can upstream processing notebooks and provenance be supplied?
26. Are the stated shared-server resources current, and is a GPU available?
27. Is four-person access supported?
28. When exactly is the server shut down?

## C. Need experimentation

- Does season-aware selection improve transfer without creating too much missingness?
- Does QA fallback improve downstream F1?
- Does coverage help at all budgets?
- Do robust temporal-change features survive spatial validation?
- Does learned source representation beat raw prototypes?
- How much source discrimination should be retained when city histories differ?
- Is frozen adaptation preferable to fine-tuning at 25-shot?
- Which method is stable at 5-shot?
- Is one prototype per class sufficient?
- Are gains consistent across classes or driven by one class?
- Does the candidate outperform simpler alternatives on final audit episodes?
- How sensitive are conclusions to support sampling and spatial separation?

## D. Need internet research or upstream documentation

Only after prioritising organiser answers:

- Sensor-specific Landsat QA bit definitions.
- Collection 2 radiometric scale/offset.
- Correct application of Roy et al. harmonisation.
- Original definitions and limitations of spectral indices.
- Landsat 7 acquisition artifacts and scan-line issues.
- Building-record provenance and licences.
- Prior work on few-shot cross-city spectral classification.
- Citations for any metric-learning or adaptation method used.

Do not spend scarce build time researching a large model zoo.

---

# PART 12 — Final Recommendations

## Top 20 things to do

1. Obtain written clarification of conflicting requirements.
2. Preserve all supplied files unchanged.
3. Establish a shared version-controlled working project.
4. Confirm exact label boundaries.
5. Use stable geographic-pixel identifiers.
6. Make preprocessing independent of labels.
7. Fix paths and create a clean execution contract.
8. Reproduce the starter baselines.
9. Freeze support/query episodes before comparing methods.
10. Report four-class macro F1 consistently.
11. Fit learned transformations inside validation folds.
12. Investigate seasonal sampling mismatch.
13. Improve slot selection and quality fallback.
14. Test coverage and robust temporal features.
15. Build an adaptation path that genuinely uses Madrid learning.
16. Prove transfer benefit against raw target prototypes.
17. Prioritise stable 25-shot performance.
18. Keep clear experiment and negative-result records.
19. Finish artifact reload/inference testing before polishing slides.
20. Protect rehearsal time and back up the final package.

## Top 20 mistakes to avoid

1. Training Amsterdam → Madrid by following the optional guide.
2. Changing the task to five classes or year regression.
3. Using construction year as an input feature.
4. Creating windows around the true construction date.
5. Splitting the same pixel’s years across folds.
6. Using all Amsterdam labels during adaptation.
7. Repeatedly tuning on the final query/audit set.
8. Calling raw Amsterdam prototypes supervised Madrid transfer.
9. Confusing accuracy, weighted F1, and macro F1.
10. Treating one lucky support draw as a result.
11. Assuming all observations are summer acquisitions.
12. Assuming QA-valid means artifact-free.
13. Applying unverified radiometric corrections.
14. Silently changing interval inclusivity.
15. Treating nearby pixels as fully independent evidence.
16. Claiming model confidence guarantees correctness.
17. Claiming global portability from two cities.
18. Launching uncontrolled heavy jobs on the shared server.
19. Discovering at submission time that the model was never saved.
20. Sacrificing a valid, explainable submission for last-minute complexity.

**Bottom line:** Our strongest opportunity is a scientifically credible low-data transfer method, backed by better observation handling and a convincing ablation—not merely a more powerful Madrid classifier.