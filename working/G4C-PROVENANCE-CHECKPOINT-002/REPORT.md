# Checkpoint 002 — metadata-scoped dry-run PASS

Open Notebook.onetoc2 is explicitly treated as external mutable
metadata under a path-specific integrity exception. All other
pre-existing experiment files remain immutable.

Exact path: `working/Open Notebook.onetoc2`. This does not exempt other `.onetoc2` files, directories, code, configuration, data, models, predictions, manifest or runtime. Same-file/type/attribute safeguards and full logging apply.

The preserved dirty Git state is intentional. No reset, restore, checkout, clean, stash, commit or pre-existing project modification was performed. Only new audit/checkpoint artifacts were created; target metadata updates were externally observed, not written by Astra.

431 checkpointed files were independently rehashed; zero non-allowlisted changes. Protected 33/33, Gate 4A/Gate 4B inventories, closed G4C-E2-001, original/, frozen RF/manifest and the approved runtime remain intact. The 180-second passive dry-run had 37 stable metadata samples. Independent policy tests passed 22/22. Exact writer PID is unproven; the evidence establishes file type and external mutability without inventing ownership.

Full report: `working/G4C-METADATA-AUDIT-002/REPORT.md`.

Recommended future identity: **G4C-E2-002**. No run directory was created and no candidate worker or modelling data was loaded. Existing runners remain untouched and must not be used to rerun the closed attempt. Candidate execution requires a new pinned coordinator using this checkpoint/policy and separate execution authorization.

This checkpoint is hash-inventoried. Previously captured files are not attribute-modified merely to freeze new evidence, since that would itself change recorded fingerprints. Hashes, exclusive creation and retained historical inventories provide auditable preservation; no claim of owner-proof filesystem immutability is made.
