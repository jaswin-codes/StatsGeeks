# Deliverable validation

**Conditional review package, not an unconditional submission certificate.**
Scientific training/inference was prohibited. No source fit, support RF fit,
prediction generation, model deserialization or notebook execution was performed.

## Deliverables
| Deliverable | Check performed | Outcome / remaining gate |
|---|---|---|
| Presentation | ZIP CRC, XML, embedded-image decoding, python-pptx open, text and shape bounds | 16 slides; original bytes preserved; slide 11 picture extends below canvas |
| PDF | Header/EOF, successful pdftotext, 16-page count; fresh PDFium render | All 16 pages render; page 11 bottom-axis clipping confirmed visually |
| Notebook | JSON, complete v4.5 bundled schema via fastjsonschema, AST syntax, literal dependencies | PASS; outputs/metadata identical and only permitted path changes; execution NOT RUN |
| Written explanation | UTF-8 open, exact slide-body match, scores and whitespace word count | 340 words; below 500, above conservative 300 limit |
| First slide | Text extraction, whitespace count | 28 words including title; under 150, but completeness is a judging question |
| Model | Frozen SHA-256, selection ID, 60-feature/25,992-row manifest, pickle opcode parsing | PASS structurally; deserialization and functionality NOT RUN |
| Reference inputs | Five safe NPZ loads, balanced support, disjoint valid queries, class ranges | PASS; no reference prediction regenerated |
| Inference | Original runner byte identity, new wrapper syntax and path resolution | Static PASS; both --support and --verify fit RFs, therefore not executed |
| Requirements | PEP 508 parsing and installed metadata comparison | Six pins match; nbformat import environment BLOCKED; clean install NOT RUN |
| Manifest/checksums | Exact membership, byte lengths, SHA-256 and original-copy comparisons | PASS for the sealed clean package; check again after background applications stop |
| Scientific metrics | F1 from 4,000 saved confusion matrices, means/SD, all three learning-curve copies | PASS within absolute 1e-12; no scientific value written |
| Figures | Five embedded slide PNG hashes match existing assets; SVG/PNG schematics parse | PASS for identity/formats; no independent regeneration of scientific plots |
| Frozen evidence | Existing root SHA256SUMS.json and all original non-OneNote bytes | PASS; zero frozen-manifest mismatches |
| All original files | Before/after inventory including OneNote metadata | FAIL: two original `.onetoc2` indices changed, none missing; not concealed |

## Recorded check detail before final document-link sweep
| `nbformat_import_environment` | BLOCKED |
| `package_membership` | PASS |
| `package_manifest_hashes` | PASS |
| `checksum_coverage` | PASS |
| `package_checksums` | PASS |
| `canonical_copies_byte_identical` | PASS |
| `top_level_allowlist` | PASS |
| `frozen_model_hashes` | PASS |
| `feature_contract` | PASS |
| `selected_model_unchanged` | PASS |
| `all_package_files_structurally_open` | PASS |
| `full_notebook_v4_5_schema` | PASS |
| `notebook_exact_path_only_derivation` | PASS |
| `notebook_literal_runtime_paths` | PASS |
| `five_reference_episode_schemas` | PASS |
| `locked_confusion_f1_arithmetic` | PASS |
| `locked_summary_arithmetic` | PASS |
| `learning_curve_tables_match_locked_summary` | PASS |
| `slide_shapes_within_canvas` | FAIL |
| `embedded_slide_figures_match_existing_assets` | PASS |
| `pdf_text_extraction` | PASS |
| `pdf_slide_page_count` | PASS |
| `all_five_mean_sd_tokens_in_current_materials` | PASS |
| `explanation_five_means_match` | PASS |
| `explanation_embedded_in_slides` | PASS |
| `installed_package_pins` | PASS |
| `new_diagram_formats` | PASS |
| `all_original_files_preserved` | FAIL |
| `all_original_non_onenote_files_preserved` | PASS |

The intermediate missing-new-document links were expected while these reports
were not yet created. The final receipt is
`reproducibility/repository_polish/validation_final/validation.json`.
All failed attempts are retained; attempt 01 hit the nbformat import issue,
attempt 02 exposed an explicit UTF-8 handling error in the new validator, and
attempt 03 detected sidecar contamination and the first notebook derivative's
encoding issue. That entire derived package was archived before rebuilding.
No original notebook or output was repaired or overwritten.

## Visual and semantic review
Fresh renders: `reproducibility/repository_polish/visual_review/`.
All pages inspected as contact sheets; page 11 also inspected at full resolution.
The plot extends beyond the page bottom, hiding its x-axis label and clipping
its tick labels. Small figure text and dense explanation slides warrant a real
presentation-screen review. Existing scientific graphics and slides were not
modified to mask these issues.

Score tokens match at six displayed decimals across new README, executive summary,
method guide, locked report, saved notebook, PowerPoint and PDF. The five means
match the written explanation. This is a scoped consistency check, not a claim
that every historical document contains only current results. Historical report
and slide replay claims refer to their original package, not new execution here.

## Acceptance decision
Do not certify immediate upload until organizer eligibility, official word limit,
source-artifact/interface requirements, rights, clean runtime and slide clipping
are resolved through explicitly authorized follow-up. See FINAL_PRE_FLIGHT.md.
