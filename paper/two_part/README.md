# paper/two_part: Part II (Study E) material, kept outside the checksum-locked Part I files

Status: DRAFT. Nothing here is submitted. Part I (Studies A-D) is frozen and is not edited from this folder.

## Why a separate folder
- `artifacts/manifests/repository-v0.1.1.sha256` locks Part I sources by hash: every file in `paper/manuscript/`, `references/bibliography.bib`, `paper/figures/` and the TAES workflow files.
- `.github/workflows/taes-s1-publication-hygiene.yml` regenerates `paper/manuscript/manuscript.md` and requires a byte-identical result, and requires the abstract to be exactly 250 words.
- Editing any of those files (including `introduction.md`, `conclusion.md` or the builder) would fail CI until the manifest and workflow are changed, which is the author's decision.

## Files
- `part-ii-study-e.md`: Part II text in pandoc markdown (cites keys from `bibliography_study_e.bib`).
- `bibliography_study_e.bib`: six entries (CosmicDancePro, WetLinks, Starlink ping dataset, SatNOGS API, CCSDS 354.0-M-1, Ledin et al. accepted version). Keys do not collide with `references/bibliography.bib`.
- `FRAMING_TEXT_PROPOSAL_v1_2026-11-19.md`: proposed abstract, introduction and conclusion changes, with author decision points.

## Open items before any assembly
1. Author decision on the combined abstract (250-word rule) and the introduction and conclusion edits.
2. Author decision whether to change the Part I locks (manifest, 250-word CI assertion) or build the two-part paper with a separate builder that reads Part I files read-only.
3. Last step before any pull request: refresh the tracked-file manifest, because 57 Study E files on this branch are not in it yet.
4. Ledin et al. final proceedings details (DOI, pages) unverified; recheck before submission.
