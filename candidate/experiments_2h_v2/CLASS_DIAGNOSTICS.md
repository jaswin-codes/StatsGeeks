# Class diagnostics: stage1

Class order1/2/3/4. Values are means of per-episode class F1, not F1 of pooled confusion counts. Full confusion matrices and episode records are in audit.json, fresh.json and spatial.json.

|200-shot method|C1|C2|C3|C4|
|---|---:|---:|---:|---:|
|EXP-010|.6702|.5815|.6528|.5914|
|EXP-F|.6795|.6034|.6953|.6564|
|H_mean|.6803|.6062|.6951|.6547|
|RF60|.7312|.6500|.7211|.6566|
|RF60 uniform smoothing|.7809|.7006|.7203|.6750|
|Pool-whitened RF60 uniform smoothing|.7851|.7039|.7220|.6795|

The gap is concentrated in **two old classes,1 and2**, not just the newest construction class. Their construction predates the Landsat record: richer jump timing alone cannot reveal their building date. Neighbourhood construction-era coherence is a plausible mechanism, but no building IDs establish same-building membership. Spatial-half tests are needed to distinguish useful regional signal from immediate support adjacency.

At5 shots, the .50 source/local blend raises C2/C3/C4 materially while C1 remains weaker than EXP-010. This supports a source prior for low-data local classifiers; it does not justify hand-tuning one class's thresholds using query truth.

Simplest class-relevant intervention: improve the locality of the probability smoother (immediate grid only) rather than training separate ad-hoc classifiers or using class-specific thresholds. This is tested independently in STAGE2_PLAN.md. No class-specific target-label fitting beyond support.
