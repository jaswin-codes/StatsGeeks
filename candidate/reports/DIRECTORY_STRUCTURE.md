# Directory structure

Current publication layout (expanded evidence directories; large historical trees summarized):

```text
./
├── README.md
├── reproduce_best.py
├── requirements-repro.txt
├── SHA256SUMS.json
├── CITATION.cff
├── candidate/
│   ├── best_model/
│   │   ├── agf_model.py
│   │   ├── configuration.json
│   │   ├── INFERENCE_MANIFEST.json
│   │   ├── pool_state.pkl
│   │   ├── provenance.json
│   │   ├── README.md
│   │   ├── reproduce_best.py
│   │   ├── requirements-repro.txt
│   │   ├── SELECTION_LOCK.json
│   │   ├── verification_inputs/ [indexed contents]
│   ├── publication/
│   │   ├── audit_and_seal.py
│   │   ├── build_publication.py
│   │   ├── distribution_receipt.json
│   │   ├── experiment_catalog/ [indexed contents]
│   │   ├── EXPERIMENT_CATALOG.json
│   │   ├── export_submission.py
│   │   ├── FIGURE_MANIFEST.json
│   │   ├── prepare_package.py
│   │   ├── README.md
│   │   ├── test_distribution.py
│   │   ├── validate_package.py
│   │   ├── verify_evidence.py
│   │   ├── verify_source.py
│   ├── figures/publication/
│   │   ├── ablation.pdf
│   │   ├── ablation.png
│   │   ├── ablation.svg
│   │   ├── boxplot.pdf
│   │   ├── boxplot.png
│   │   ├── boxplot.svg
│   │   ├── budget_comparison.pdf
│   │   ├── budget_comparison.png
│   │   ├── budget_comparison.svg
│   │   ├── calibration.pdf
│   │   ├── calibration.png
│   │   ├── calibration.svg
│   │   ├── confusion_ASTRA_AGF_normalized.pdf
│   │   ├── confusion_ASTRA_AGF_normalized.png
│   │   ├── confusion_ASTRA_AGF_normalized.svg
│   │   ├── confusion_ASTRA_AGF_raw.pdf
│   │   ├── confusion_ASTRA_AGF_raw.png
│   │   ├── confusion_ASTRA_AGF_raw.svg
│   │   ├── confusion_Coordinate_RF_normalized.pdf
│   │   ├── confusion_Coordinate_RF_normalized.png
│   │   ├── confusion_Coordinate_RF_normalized.svg
│   │   ├── confusion_Coordinate_RF_raw.pdf
│   │   ├── confusion_Coordinate_RF_raw.png
│   │   ├── confusion_Coordinate_RF_raw.svg
│   │   ├── confusion_EXP010_normalized.pdf
│   │   ├── confusion_EXP010_normalized.png
│   │   ├── confusion_EXP010_normalized.svg
│   │   ├── confusion_EXP010_raw.pdf
│   │   ├── confusion_EXP010_raw.png
│   │   ├── confusion_EXP010_raw.svg
│   │   ├── confusion_EXPF_normalized.pdf
│   │   ├── confusion_EXPF_normalized.png
│   │   ├── confusion_EXPF_normalized.svg
│   │   ├── confusion_EXPF_raw.pdf
│   │   ├── confusion_EXPF_raw.png
│   │   ├── confusion_EXPF_raw.svg
│   │   ├── coordinate_influence.pdf
│   │   ├── coordinate_influence.png
│   │   ├── coordinate_influence.svg
│   │   ├── covariance_shrinkage.pdf
│   │   ├── covariance_shrinkage.png
│   │   ├── covariance_shrinkage.svg
│   │   ├── covariance_spectrum.pdf
│   │   ├── covariance_spectrum.png
│   │   ├── covariance_spectrum.svg
│   │   ├── cumulative_gain.pdf
│   │   ├── cumulative_gain.png
│   │   ├── cumulative_gain.svg
│   │   ├── cumulative_wins.pdf
│   │   ├── cumulative_wins.png
│   │   ├── cumulative_wins.svg
│   │   ├── density.pdf
│   │   ├── density.png
│   │   ├── density.svg
│   │   ├── feature_importance.pdf
│   │   ├── feature_importance.png
│   │   ├── feature_importance.svg
│   │   ├── histogram.pdf
│   │   ├── histogram.png
│   │   ├── histogram.svg
│   │   ├── learning_curve.pdf
│   │   ├── learning_curve.png
│   │   ├── learning_curve.svg
│   │   ├── paired_gain.pdf
│   │   ├── paired_gain.png
│   │   ├── paired_gain.svg
│   │   ├── per_class.pdf
│   │   ├── per_class.png
│   │   ├── per_class.svg
│   │   ├── per_class_ASTRA_AGF.pdf
│   │   ├── per_class_ASTRA_AGF.png
│   │   ├── per_class_ASTRA_AGF.svg
│   │   ├── per_class_Coordinate_RF.pdf
│   │   ├── per_class_Coordinate_RF.png
│   │   ├── per_class_Coordinate_RF.svg
│   │   ├── per_class_EXP010.pdf
│   │   ├── per_class_EXP010.png
│   │   ├── per_class_EXP010.svg
│   │   ├── per_class_EXPF.pdf
│   │   ├── per_class_EXPF.png
│   │   ├── per_class_EXPF.svg
│   │   ├── runtime.pdf
│   │   ├── runtime.png
│   │   ├── runtime.svg
│   │   ├── spatial.pdf
│   │   ├── spatial.png
│   │   ├── spatial.svg
│   │   ├── spatial_summary.pdf
│   │   ├── spatial_summary.png
│   │   ├── spatial_summary.svg
│   │   ├── transfer.pdf
│   │   ├── transfer.png
│   │   ├── transfer.svg
│   │   ├── violin.pdf
│   │   ├── violin.png
│   │   ├── violin.svg
│   ├── tables/
│   │   ├── ablation.csv
│   │   ├── ablation.md
│   │   ├── calibration.csv
│   │   ├── calibration.md
│   │   ├── confusion.csv
│   │   ├── confusion.md
│   │   ├── coordinate_influence.csv
│   │   ├── coordinate_influence.md
│   │   ├── covariance_eigenvalues.csv
│   │   ├── covariance_eigenvalues.md
│   │   ├── episode_manifest.csv
│   │   ├── episode_manifest.md
│   │   ├── episode_scores.csv
│   │   ├── episode_scores.md
│   │   ├── feature_importance.csv
│   │   ├── feature_importance.md
│   │   ├── leaderboard.csv
│   │   ├── leaderboard.md
│   │   ├── learning_curve.csv
│   │   ├── learning_curve.md
│   │   ├── paired_gains.csv
│   │   ├── paired_gains.md
│   │   ├── per_class.csv
│   │   ├── per_class.md
│   │   ├── prediction_summary.csv
│   │   ├── prediction_summary.md
│   │   ├── runtime.csv
│   │   ├── runtime.md
│   │   ├── runtime_historical.csv
│   │   ├── runtime_historical.md
│   │   ├── significance.csv
│   │   ├── significance.md
│   │   ├── spatial.csv
│   │   ├── spatial.md
│   │   ├── spatial_matched_control.csv
│   │   ├── spatial_matched_control.md
│   │   ├── transfer.csv
│   │   ├── transfer.md
│   ├── reports/
│   │   ├── DIAGNOSTIC_LIMITATIONS.md
│   │   ├── DIRECTORY_STRUCTURE.md
│   │   ├── FINAL_REPORT.md
│   │   ├── METHODS.md
│   │   ├── REPOSITORY_AUDIT.md
│   │   ├── REPRODUCIBILITY.md
│   │   ├── RESULTS.md
│   │   ├── RUNTIME_REPORT.md
│   │   ├── SPATIAL_ANALYSIS.md
│   │   ├── STATISTICAL_ANALYSIS.md
│   ├── reproducibility/
│   │   ├── analysis_validation.json
│   │   ├── artifact_manifest.json
│   │   ├── cleanup_actions.json
│   │   ├── cleanup_deferred.json
│   │   ├── command_manifest.json
│   │   ├── dataset_manifest.json
│   │   ├── directory_hashes.json
│   │   ├── distribution_test.json
│   │   ├── environment_summary.json
│   │   ├── excluded_historical_comparisons.json
│   │   ├── final_validation.json
│   │   ├── freeze_before.json
│   │   ├── git_diff_before.patch
│   │   ├── git_status_before.txt
│   │   ├── legacy_link_warnings.json
│   │   ├── requirements-repro.txt
│   │   ├── source_manifest.json
│   │   ├── verification/ [indexed contents]
│   ├── presentation/
│   │   ├── ablation_transparent.png
│   │   ├── boxplot_transparent.png
│   │   ├── budget_comparison_transparent.png
│   │   ├── calibration_transparent.png
│   │   ├── confusion_ASTRA_AGF_normalized_transparent.png
│   │   ├── confusion_ASTRA_AGF_raw_transparent.png
│   │   ├── confusion_Coordinate_RF_normalized_transparent.png
│   │   ├── confusion_Coordinate_RF_raw_transparent.png
│   │   ├── confusion_EXP010_normalized_transparent.png
│   │   ├── confusion_EXP010_raw_transparent.png
│   │   ├── confusion_EXPF_normalized_transparent.png
│   │   ├── confusion_EXPF_raw_transparent.png
│   │   ├── coordinate_influence_transparent.png
│   │   ├── covariance_shrinkage_transparent.png
│   │   ├── covariance_spectrum_transparent.png
│   │   ├── cumulative_gain_transparent.png
│   │   ├── cumulative_wins_transparent.png
│   │   ├── density_transparent.png
│   │   ├── feature_importance_transparent.png
│   │   ├── histogram_transparent.png
│   │   ├── learning_curve_transparent.png
│   │   ├── paired_gain_transparent.png
│   │   ├── per_class_ASTRA_AGF_transparent.png
│   │   ├── per_class_Coordinate_RF_transparent.png
│   │   ├── per_class_EXP010_transparent.png
│   │   ├── per_class_EXPF_transparent.png
│   │   ├── per_class_transparent.png
│   │   ├── README.md
│   │   ├── runtime_transparent.png
│   │   ├── spatial_summary_transparent.png
│   │   ├── spatial_transparent.png
│   │   ├── transfer_transparent.png
│   │   ├── violin_transparent.png
│   ├── autonomous_runs/20260909_1727/ [immutable original evidence]
│   ├── experiments_agf/ [prior immutable package]
│   ├── experiments_2h/ [historical experiments; EXP-F implementation]
│   └── experiments_2h_v2/ [historical ASTRA; excluded forensic comparisons]
├── archive/publication_cleanup/ [previous README and root scratch outputs]
├── data/ [local organizer parquet and preprocessed artifact]
├── docs/ [historical project documentation]
├── original/ [organizer notebooks]
├── working/ [historical gates and experiments]
├── models/ [historical source artifacts]
├── submission/ and submission_dry_run/ [historical, not final export]
└── presentation/ [historical decks]
```

Machine-readable complete publication file inventory: `candidate/reproducibility/artifact_manifest.json`. Historical experiment inventory: `candidate/publication/EXPERIMENT_CATALOG.json`. The final ZIP contains only the allowlisted subset defined by its `SUBMISSION_SCOPE.json`; the full research-tree inventory is not its payload.
