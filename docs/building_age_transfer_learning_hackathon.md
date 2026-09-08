# Building Age Classification and Transfer Learning Hackathon Walkthrough

## Metadata
- Duration: ~1 hour 13 minutes
- Source: Video transcript (hackathon lecture on satellite-derived building age classification and transfer learning, followed by team logistics)
- Main Topics: Transfer learning motivation, hackathon deliverables, dataset structure (Madrid/Amsterdam satellite pixel data), exploratory data analysis, feature engineering, class imbalance, model training, confusion matrices, transfer learning results, Q&A, team login logistics

## Introduction and Motivation

In order to identify building age, you also need building age data to train your model — and this is difficult. So the main goal is to use existing data to create a **transferable model**. This is what was called "create model" in the presentation the previous day: a model that can be transferred from existing cities to new cities with minimal amounts of data. This is an example of transfer learning.

## Age Classes

> **[Visual reference omitted from transcript]**

The satellite data spans 40 years, from 1984 to 2024. There are:
- Two classes during the time of satellite observation.
- Two classes before the observation period, demarcated by a significant historical event specific to that city's history.

If this approach were applied to a different city, a different significant event would be chosen. The point is simply to be able to distinguish data into four classes — the four classes themselves could be arbitrary. If you get a new city, you retrain those four classes to be appropriate for that city.

## Submission Requirements

Participants will receive:
- **Madrid** data — for training.
- **Amsterdam** data — for transfer and validation, to see how well the created model works.

Workflow:
1. Use Madrid data to create a transferable model.
2. Evaluate the model using **cross-validation** (examples shown in Notebook 4). Much of the code in Notebook 4 can be reused rather than written from scratch.
3. From the Madrid model, develop a transfer procedure that uses a small number of labeled Amsterdam pixels to produce a model for Amsterdam (also demonstrated in Notebook 4).
4. Use the Amsterdam data to evaluate this transfer — not just once, but repeated many times to obtain a distribution, and find the mean and standard deviation of the transfer model's accuracy.

> **Note:** Participants may use AI coding assistants such as Claude, ChatGPT, Gemini, or Copilot to help write code. Claude in particular does a very good job of writing code.

### Deliverables

1. The trained model from stage one.
2. Training code that adapts the trained model to another city (Amsterdam).
3. A PowerPoint presentation.
4. Written justification.

Scoring was not planned for this session (this being a dry run to refine different aspects of the hackathon before the real event), though this may be revised.

## Dataset Overview

The dataset is provided as Parquet files (an efficient format for storing data), located in the notebook's data folder. Participants should read about how the data is formed, and background is given on the two cities, since the goal is a **city-portable model**.

### Reading the Data (Notebook: "Reading Data")

The data will "run out of the box" on the provided platform. Some notebooks may take a while to run.

**Key data facts:**
- The dataset has approximately 3 million rows.
- This does *not* mean 3 million pixels — each pixel has 40 years of data, so the number of rows must be divided by roughly 40 to get the actual number of data points (one row per pixel per year).
- The count is not perfectly divisible by 40 because some years have missing data.
- There are **76,263 unique data pixels** total.
- There are believed to be **three satellite images per year** in the original dataset.

**Data screening:** During preliminary analysis, one outlier image was found and manually removed — it resulted from cloud cover that wasn't detected by the original filter. This illustrates the importance of always trying to represent data graphically to understand it and catch problems.

**Data fields per pixel per image include:**
- City
- Complete ID
- Pixel location (x, y)
- Coverage (fraction of the pixel actually covered by buildings)
- Year (mean year/date of construction of buildings in that pixel)
- Spectral values (including visible light bands)
- A pixel/image quality measure
- Satellite identifying information

> The original raw processing notebooks (used to prepare this dataset) are not part of the hackathon materials, but could be made available on request (e.g., zipped and shared via chat).

### Comparing Madrid and Amsterdam

- Amsterdam has somewhat less data than Madrid, which is fine since Amsterdam isn't used for training — only for adaptation/retraining.
- The "flat view" takes one reflectance value per row (each row has three years of observations, but only one is selected).

**Building coverage distribution:**
- X-axis: 0 to 1 (0 = no coverage, 1 = total coverage).
- Y-axis: percentage of pixels (a histogram; bars sum to 100%).
- A pixel with a value of 1 means it is entirely covered with buildings; a value of 0.2 means only 20% is covered (the rest might be yard, water, parking lot, etc.).
- Only pixels with a minimum building fraction of about 15% were retained; pixels below this threshold appear as gray in later maps.
- The median (50% below, 50% above) and mean (average) are marked on the distribution.

**Madrid vs. Amsterdam building density:**
- Madrid is significantly more densely packed with buildings than Amsterdam.
- Mean coverage: Madrid ≈ 50%, Amsterdam ≈ 42% (an ~8 percentage point difference).
- This isn't directly relevant for classification, but confirms the data is reasonable and shows the two cities have different characteristics.

### Class Distribution and Imbalance

Class distributions were shown for both cities, again revealing **class imbalance** — Class 2 has significantly more data than the other classes (almost twice as much as Class 1), especially in the Madrid data.

> **Note:** There is no need to use all the data. For example, an equal amount of data could be sampled from each class. There is plenty of data, but this class imbalance causes significant problems for the estimator later on.

A year-based histogram also showed a spike in construction just before 1984.

## Exploring Pixel Time Series by Class

The goal is to trace one pixel over time and discover, from changes in its reflectance values, which class it belongs to. Each year, a pixel has a different reflectance value, and the aim is to identify features that distinguish the four classes.

**Example: "Blue over time" plots**
- Each plot shows the blue reflectance value over time for three example pixels from a single class.
- Dotted lines on some plots indicate the actual year of construction for a given pixel.

**Observations discussed:**
- Class 2 appeared more variable (more spikes) than Class 1.
- Class 2 pixels appeared slightly higher on average than Class 1 pixels (though based on only three examples, so only suggestive).
- Near the year of construction, some pixels showed a sharp increase in reflectance, followed by a downward trend — a possibly distinguishing feature.
- Overall, distinguishing classes by eye from a single time series is very difficult — "if you give me one of these lines and say which class, I can't tell." This shows the classification task asks the algorithm to do something humans themselves cannot easily do.
- A participant pointed out that the coverage fraction might also be a useful distinguishing feature — noted as a good point not initially considered.

### Mean Reflectance by Year and Class

Plots of mean reflectance per year for each class (Class 1 = blue, Class 2 = green, Class 3 = orange, Class 4 = red) showed:
- For earlier years, classes were nearly identical; for later years, values diverged — this is more encouraging for classification.
- Shaded regions around each line represent ±1 standard deviation for that year, showing within-year variation.
- Class 4 had both the highest mean and the highest variability.
- A similar pattern was observed in Amsterdam, though examined for a different spectral band (NIR vs. blue).

### Overall Distributions and Year-on-Year Change

- Distributions of reflectance averaged over all years again showed higher variability for the "red" class (Class 4), which is encouraging, since it suggests there may be ways to separate the classes across different spectral bands.
- **Year-on-year change** was also examined: the difference between consecutive years' values (e.g., 1985 value minus 1984 value), averaged — another potentially useful feature.
- A mean-vs-standard-deviation plot was used to explore relationships between features.
- Of the six spectral/radiation bands measured, blue, green, and red carry largely similar information, while they differ substantially from SWIR1 and SWIR2.

## Data Preparation for Modeling (Notebook 3)

Goal: construct **one data vector per pixel** (rather than one data vector per pixel per year), in order to predict the class for each pixel.

Steps performed:
1. Imports and data loading.
2. Assign classes to each pixel.
3. Simplify to one observation per year.
4. Fill in missing years' data using near-interpolation (e.g., a gap between 1992 and 1996 gets interpolated).
5. Derive additional index features from the raw spectral values, based on the literature — these indices are known from urban-planning literature to relate to vegetation, buildup intensity, urban areas, etc.
6. Collapse each pixel's time series (up to 40 annual observations) into a single vector for prediction — described as the most important section, since it captures how the spectrum changes over time.
7. Standardize all pixel values onto the same scale to allow comparison across years.
8. Save the processed data so the notebook doesn't need to be rerun each time.

> **Note:** Participants are not required to use this exact feature vector — they may modify it, drop features, or add different ones. It is provided as a starting point, not a requirement.

## Model Training and Transfer Learning (Notebook 4)

This notebook provides an example model that participants are expected to substantially rewrite or replace with their own technique.

**Workflow steps demonstrated:**

1. **Train on Madrid** — train a standard classifier (Random Forest was used as an example; SVM, XGBoost, or others could be substituted) on the Madrid data.
2. **Zero-shot transfer** — apply the exact same Madrid-trained model directly to Amsterdam with no adaptation, purely for comparison purposes. Poor performance is expected here since Amsterdam should differ from Madrid.
3. **Transfer learning (few-shot transfer)** — make small adjustments to the Madrid model using a limited number of labeled Amsterdam points, described analogously to a driver used to left-hand-side steering wheels adapting to a right-hand-side steering wheel: not a complete relearning, but some adjustment is needed.

### Cross-Validation

Because machine learning training involves random variability (e.g., one run might yield 60% accuracy, another 55%), cross-validation is used to estimate accuracy reliably:
- **n_folds**: number of different subsets trained on (5 folds used).
- **n_repeats**: number of times training is repeated.

Example results: Macro F1 scores clustered around 61–62%, with a summary value of approximately 61.79% ± 0.43% — showing the estimate is quite stable. (Macro F1 is described as very similar to accuracy for this purpose.)

### Confusion Matrix

A confusion matrix was used to evaluate the classifier in detail. Key points covered:

- Each cell represents: given the *actual* class, what's the *probability* the classifier predicts each class.
- Example: given an actual Class 3 pixel, there was a 0.33 (33%) probability it was misclassified as Class 2.
- Conversely, given an actual Class 2 pixel, there was only a 0.08 (8%) probability of misclassification as Class 3 — much less confusion in that direction.
- Class 1 was correctly predicted 39% of the time.
- **Diagonal entries** (correct classifications) are particularly important.
- Class 2 (the largest class) was classified best — described as *not* a coincidence but a **problem**: the classifier favors the biggest class, and other classes are often mistaken for it. This indicates the imbalanced classes should be balanced before training.
- Confusion between Class 1 and Class 2 was considered unsurprising, since there is genuinely little change between these classes during the observation period; balancing Class 2 might help.
- Overall accuracy exceeded 50% across four classes — considered encouraging, since random chance would give 25% accuracy (i.e., a value of 0.25 in every cell of a random classifier's confusion matrix).

### Zero-Shot Transfer to Amsterdam

Applying the Madrid-trained model directly to Amsterdam (no retraining) performed very poorly — the model predicted nearly every pixel as Class 2.

### Spatial Visualization of Predictions

A geographic/pixel-map visualization technique was described:
- Each of the four classes is assigned a color: Class 1 = red, Class 2 = blue, Class 3 = green, Class 4 = black (as used in this specific visualization; note the class-to-color mapping was described contextually and may differ from the class-to-color scheme used in the mean-reflectance plots above).
- The classifier assigns a probability to each class per pixel; these probabilities are combined to set the RGB-like intensity of each pixel — e.g., probabilities of 0.5 / 0.15 / 0.22 / (implied remainder ≈ 0.13) produce a pixel that looks predominantly red-ish, reflecting the dominant predicted class.
- **Worked example on probabilities:** given three known class probabilities (e.g., 0.5, 0.15, 0.22), the fourth is found by subtracting their sum from 1.
- Gray pixels in these maps represent excluded pixels (insufficient building coverage, water, etc.) — only colored pixels (green, red, blue, black) are relevant.
- In the **true class** map, pixels are shown in one pure color corresponding to their actual class; distinct, largely single-colored neighborhoods are visible (e.g., an "old quarter" appearing almost entirely one color for Class 1).
- In the **predicted class** map (Madrid), the colors matched the true map reasonably well, capturing the general spatial pattern, though with some mixing/errors (e.g., red mixed into blue regions) — considered an encouraging result.
- A **certainty/confidence map** was also shown: brighter pixels indicate the classifier is more confident in its prediction; darker pixels indicate more uncertainty. Two versions of this uncertainty measure were shown, described as two different ways of measuring the same underlying uncertainty.
- A **correct/incorrect map** was shown, with black marking correctly classified pixels and red marking incorrectly classified pixels — errors were scattered throughout the image, with some regions performing much better than others.
- A **feature importance** visualization was also shown, indicating which features in the data vector contributed most to the classifier's decisions (participants were directed to the notebook for feature details).

### Few-Shot Transfer Learning Results (Amsterdam)

- Applying the Madrid model with zero retraining to Amsterdam performed very poorly (as above).
- With **few-shot transfer** — retraining using only a small number of labeled Amsterdam points per class — results improved substantially:
  - With just 5 points per class, there was a large accuracy improvement over no retraining.
  - Accuracy continued to improve up to about 25 points per class, reaching close to 60%.
  - With 50 points per class, accuracy was close to the best achieved result.
- **Comparison to full training:** Madrid training used over 3,000 points per class, while the Amsterdam transfer achieved comparable accuracy (~60%, matching what Madrid achieved with 10,000 points per class) using only 50 points per class (200 pixels total across 4 classes) — roughly **200× less data** required.
- The Amsterdam confusion matrix again showed the same two classes highly confused with each other, and Class 2 again over-predicted — described as an area for participants to improve upon.
- Corresponding spatial plots (true class, predicted class, confidence, correct/incorrect) were also shown for Amsterdam.

## Q&A Note

A participant asked about class selection/exclusion criteria; the presenter clarified they had not additionally screened by the remaining coverage fraction, and acknowledged this as a good point they hadn't considered (the coverage fraction might be a useful additional feature or filter).

## Closing Remarks

The presenter noted running slightly over time (about 2 minutes over) but wanted to leave participants time to work, offering to go around and answer individual questions during the working session.

## Team Login and Logistics (Post-Lecture)

Following the lecture, there was a live session to organize team logins:

- Teams were instructed to sit together (in groups, e.g., Group 1, 2, 3, 4) and verify they were all logged into the same server/session.
- A roll call was conducted to confirm representation from teams/regions including Iraq, Ethiopia, Nigeria, and Tanzania.
- It was clarified that only **one representative per team** (typically the team lead, or a stand-in if the lead was unavailable) needed to join the coordination call — in this case, Ali was noted as replacing "Salah" for Iraq.
- Representatives were asked to provide their email addresses in the chat so that login details for the virtual machines could be sent to them.
- A separate Zoom link was to be created for just the one representative from each team.
- There was a wait while missing team representatives (Ethiopia, Nigeria, Tanzania) were followed up with, since other teams had already started working.
- Login details, including a link to a different Zoom meeting, were eventually sent to the Iraq and (apparently) Ethiopia representatives ("Ali and Yona").
- The original Zoom call was then closed, with instructions that only team leads needed to remain present; a final request was made for someone from the Nigeria team to email organizers to confirm hackathon participation.
