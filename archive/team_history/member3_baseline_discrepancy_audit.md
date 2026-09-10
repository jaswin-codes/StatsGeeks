# Notebook 4 baseline discrepancy audit

## Conclusion

**YES: evidence supports faithful execution of the current Notebook 4 source on the accepted preprocessing artifact.** Accept 0.6281 ± 0.0043 and 0.4433 as measured local reference-protocol results, not as exact replication of the starter outputs. Exact cause of the score discrepancy is **not identifiable from the available provenance**. Independent deterministic repetition is not verified. No training was performed in this audit.

## Source and input evidence

- Original and unexecuted working notebook SHA256: `709fa081f33186253715e1cd525b5d2a7c8b7a05259855fc72f137c9233551ae`.
- Every executed-notebook cell source equals the corresponding original cell source, including Markdown.
- Executed artifact: `working/4-Modelling_member3_reference_executed.ipynb`; recorded SHA256 `37761873bc8d9ef57b13515b66ed636d400830b0b186cf25d55b41ccb3fc208e`.
- Accepted input `data/preprocessed/preprocessed_data.pkl` SHA256 rechecked: `51f11bc9025b5d4ffe2f9e03a8c76b70e4cfd0e91cb36876a9d021181e8ccdbe`. Original cell 5 loads `../data/preprocessed/preprocessed_data.pkl`; runner cwd is `working/`, resolving to this file.
- Madrid: X `(76263,60)` float64, y `(76263,)` int64; classes 1–4 counts 13794, 27152, 18672, 16645.
- Amsterdam: X `(25992,60)` float64, y `(25992,)` int64; counts 7568, 8802, 6745, 2877.
- Both X matrices finite; pixel keys unique and lexicographically ordered `(px_key, py_key)`; no Notebook 4 row sorting or label remapping before fitting. Row alignment relies on the accepted producer contract; dimensions alone cannot prove semantic alignment.
- The accepted pickle contains `working.minimal_standard_scaler.StandardScaler`, a documented preprocessing compatibility deviation, not sklearn's scaler. Notebook 4 consumes the already-scaled arrays without refitting/scaling. Numerical identity to the unavailable starter pickle cannot be established by shape or matching rounded prototype scores.

## Protocol audit (one-based cell numbers)

- Cell 7: `RandomForestClassifier(n_estimators=500, class_weight='balanced', random_state=42, n_jobs=-1)`; all other parameters default. Current defaults include criterion gini, max_features sqrt, bootstrap True, max_depth None, min_samples_split 2, min_samples_leaf 1, max_samples None, ccp_alpha 0, warm_start False.
- CV: `RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)`. Fresh RF per split, unmodified indexed train/validation rows. F1 uses `average='macro'`; aggregate uses `np.mean` and `np.std` (ddof=0) over 25 scores.
- Cell 14: creates a fresh RF using the same parameters and fits **all Madrid** X/y. It is not the last CV forest. No Amsterdam fitting precedes zero-shot prediction. Measured in-sample accuracy 0.9999.
- Cell 19: `rf_final.predict(X_amsterdam)` followed by `f1_score(y_amsterdam, y_ams_pred_zero, average='macro')`. No thresholding/remapping. Class names are display strings only. Labels remain integers 1–4.
- Cell 25: shots `[5,10,25,50,100,200]`, ten trials, one advancing `default_rng(42)` across budgets/trials; class means and nearest L2 prototype, support sampled without replacement, query is the support complement. No change to methodology or seeds.
- Confusion/map diagnostics use sorted class order; map probability indexing assumes columns correspond to 1–4. They do not change the zero-shot score.

## Version/provenance limits and launcher correction

- Local preflight: Python 3.11.9, NumPy 2.4.6, SciPy 1.17.1, sklearn 1.9.0. Executed notebook kernel metadata reports Python 3.11.9.
- Original notebook metadata reports Python 3.11.15 (`landsat` display name). It does not record NumPy/SciPy/sklearn versions or the checksum of its original input pickle. Therefore package/default/implementation differences cannot be isolated as the cause. Fixed seeds do not promise identical results across different library versions and inputs.
- Correction to earlier execution explanation: installed `KernelManager` has **no `kernel_cmd` trait**. It resolves a Python kernel spec from `C:\Users\jaswi\AppData\Roaming\Python\share\jupyter\kernels\python3`, whose argv begins `python -m ipykernel_launcher`. `format_kernel_cmd` substitutes the manager process's `sys.executable`, currently the authorised Python 3.11 path. Thus the claim that no kernelspec existed was incorrect; the wrapper logged its intended command rather than capturing the launched command. Executed kernel metadata supports the intended Python version. Package versions were recorded in preflight, not inside the executing kernel.
- This is a provenance/reporting weakness, not evidence of a changed RF protocol. No wrapper or notebook code was changed in this audit.

## Starter versus measured results

Original saved cell 7 explicitly prints 0.6179 ± 0.0043; original saved cell 19 prints 0.3427. They are genuine saved starter outputs, not guaranteed targets. `docs/BASELINE_EXECUTION_PLAN.md` Success Criteria identifies them as saved organiser references and requires recording discrepancies rather than adjusting the protocol.

The executed corresponding cells print 0.6281 ± 0.0043 and 0.4433. Differences are +0.0102 and +0.1006 at displayed precision. Matching six prototype summaries at displayed precision supports consistency of that path, but does not prove identical RF inputs, source ordering, or historical library behaviour. No specific cause is proven.

## Deterministic reproduction check

The saved notebook can be reloaded to recover the printed **0.4433**, but that is not an independent deterministic reproduction. Notebook 4 saves neither `rf_final` nor raw prediction arrays. The kernel exited after execution. Consequently the score cannot be independently recalculated from a saved model/prediction artifact currently available. A same-environment, same-input, unchanged-protocol rerun would be needed to test repeatability; none was performed in this audit. Rounded classification-report values also cannot reconstruct exact predictions/F1.

## Preservation and recommendation

- `git status --short -- original` clean; OneNote file retains `A R` read-only protection.
- No datasets, notebook sources, seeds, model parameters, or evaluation logic changed.
- Team Lead may accept these as the measured local baseline while retaining unresolved historical discrepancy and repeatability qualifications. Acceptance of exact starter reproduction is not justified.
- Candidate modelling remains **not authorised**. Await Team Lead review and any separately scoped repeatability/provenance task.
