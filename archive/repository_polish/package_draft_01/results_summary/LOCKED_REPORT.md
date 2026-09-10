# Final selection: Coordinate-RF

5: 0.650253 ± 0.011246
25: 0.687664 ± 0.012145
50: 0.708436 ± 0.011277
100: 0.729839 ± 0.008802
200: 0.749299 ± 0.005716

# Coordinate-RF methods and limitations

Input: 60 ordered source-standardized features; labelled Madrid rows; integer 2D lattice coordinates for both cities. `fit_pool` in model/agf_model.py implements source transfer and unlabelled-pool preprocessing. Its signature never accepts target labels. It reverses source scaling, constructs 120 contextual features (60 raw plus 60 local averages), performs covariance transport, fits RF200/leaf2, and performs one pseudo-class refinement and RF200/leaf2 refit. No query truth anchors are used.

Local adaptation: rho=min(1,60/(4*b)); covariance=(1-rho)*full_pool_cov+rho*diagonal_cov+1e-7*I. Apply inverse square root whitening; append full-pool standardized x,y. RF200, leaf1, sqrt features, balanced weights, seed42. Blend prior with alpha=20/(20+4*b). Gaussian coordinate smoothing: k=9, sigma=1, one step, cKDTree tie convention. Probability columns map to classes [1,2,3,4]. Full configuration is in model/agf_model.py and SELECTION_LOCK.json.

EXP-010 and EXP-F are inductive controls; ASTRA and Coordinate-RF are transductive. Matched comparison does not equal matched information access. All numbers are from the existing prelocked audit, not new overnight independent validation. Source-only raw preprocessing rebuild requires organizer data and original source-fitted scaler; the inference notebook starts from a trusted preprocessed pool artifact, not invented external data. This is not self-contained training from raw data.

Additional 800 labelled development pixels were used for historical support-only selection; they never enter final query scoring. Target pool membership and inherited preprocessing have historical label-availability filtering. Prior ASTRA research had audit exposure. Organizer eligibility of full-pool coordinates and research supervision is unconfirmed. No independently held-out city exists locally.

Spatial: medians define x/y halves; support low/high predicts opposite side with 10-key-unit buffer. 200/class, ten trials per direction. Coordinate-RF means: x-low .719836, x-high .644816, y-low .669160, y-high .743052; mean .694216, worst .644816. ASTRA mean .696672, worst .658183. Do not conceal this tradeoff. Statistical intervals describe support sampling conditional on this fixed city, not geographic generalization.


Software preflight:
```json
{
  "model": "Coordinate-RF",
  "fresh_source_refit": true,
  "rebuilt_artifact_byte_identical": true,
  "notebook_executed": true,
  "notebook_execution": "fresh Python sequential code-cell execution; not Jupyter kernel UI",
  "inference_works": true,
  "artifact_loads": true,
  "exact_replay_arrays": 5,
  "explanation_words": 340,
  "presentation_opens": true,
  "pptx_renders": true,
  "pdf_created": true,
  "pdf_render_checked": true,
  "pptx_structural_open": true,
  "safety_snapshot_unchanged": true,
  "all_protected_evidence_unchanged": true,
  "query_labels_used_for_selection": false,
  "competitor_repository_accessed": false,
  "independent_organizer_test": false,
  "spatial_limitations_documented": true,
  "organizer_protocol_eligibility": "UNCONFIRMED",
  "submission_ready_unconditionally": false,
  "public_support_inference_checked": true,
  "learning_curve_table_matches_locked_results": true,
  "all_five_budgets_match": true,
  "macro_f1_arithmetic_checked_records": 4000,
  "written_explanation_in_slides": true
}
```
