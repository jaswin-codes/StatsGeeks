# Commit checklist — no commit performed

## Preservation and scope
- [x] Saved initial Git HEAD and dirty status without staging/reverting user changes.
- [x] Existing model, predictions, results, frozen hashes and scientific code unchanged.
- [x] Existing root README and requirements preserved; professional alternatives added.
- [x] New notebook has path-only derivation; original outputs and metadata preserved.
- [x] Old drafts/evidence retained; this pass's failed artifacts archived.
- [ ] Investigate active OneNote metadata changes; do not silently restore or stage them.

## Review before staging
- [ ] Run `git diff --check` and inspect pre-existing warnings separately.
- [ ] Stage only explicitly reviewed new guides/scripts/manifests, never `git add .`.
- [ ] Review large model/PDF/PPTX/NPZ distribution artifacts for release storage or LFS;
      the requested final package intentionally duplicates only necessary deliverables.
- [ ] Keep environments, raw data, caches, generated OneNote files, replay outputs and
      historical safety ZIPs out of ordinary Git history without deleting local evidence.
- [ ] Do not stage `archive/` wholesale; it contains preserved package binaries.
- [ ] Review new documentation and audit receipts for identifying local-path details.
- [ ] Obtain rights-holder licensing and organizer data-sharing approval.
- [ ] Have another member verify checksums and review the exact final upload allowlist.
- [ ] Confirm HEAD/tag aligns with approved release; current repository is already dirty.

Suggested logical commit (pending approval):
`docs: add preservation-first judge package and static audit guides`

The root `.gitignore` is frozen; it was not rewritten. Use explicit staging or a
separately authorized Git policy change. No automatic commit, tag or broad cleanup.
