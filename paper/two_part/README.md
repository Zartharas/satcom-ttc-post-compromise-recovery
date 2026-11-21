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

## Build
```
python3 -I paper/two_part/build_two_part_manuscript.py --compact --trim
bash paper/two_part/latex_build/build.sh <dir with IEEEtaes.cls and IEEEtaes.bst> <empty work dir outside the repo> trim
```
Reads Part I read-only, refuses to run if `paper/manuscript/manuscript.md` or `references/bibliography.bib` differ from the manifest, applies output-only edits from `safe_trims.py`, `review_fixes.py` and `review_fixes_r9.py`, and writes the generated manuscript, bibliography and supplementary tables to `paper/two_part/out/` (git-ignored). The IEEE class files are not stored in the repository and must be obtained from IEEE. `paper/supplement/SUPPLEMENTARY_TABLES_S2_S7.md` is a committed copy of the generated Supplementary Tables S2 to S7 (S2 to S6 derived read-only from frozen Part I inputs, S7 from the Study F run); regenerate it with the builder.

- `abstract_candidate_250w.md`: combined abstract (candidate; author decision pending).
- `reanalysis/`: read-only post hoc reanalysis of retained Part I records and an exploratory Part II exposure measure.
- Part I source files and frozen results are not modified by any of these steps.

## Open items before any assembly
1. Author decision on the combined abstract (250-word rule) and the introduction and conclusion edits.
2. Author decision whether to change the Part I locks (manifest, 250-word CI assertion) or build the two-part paper with a separate builder that reads Part I files read-only.
3. Last step before any pull request: refresh the tracked-file manifest, because 57 Study E files on this branch are not in it yet.
4. Ledin et al. final proceedings details (DOI, pages) unverified; recheck before submission.

### Supplementary Figure S8 (regime map)
`paper/two_part/reanalysis/regime_map.py` computes exact masses from the frozen Part II model (read-only import) for one slice (B = 8, L = 3) and writes `paper/two_part/figures_ieee/figS8_regime_map.{pdf,png,csv}`; copies are in `paper/supplement/`. It is illustrative and not a pre-registered test.

### Display label
In the manuscript text the raw enum `SECURE_DEGRADED` is shown as `LOCKOUT` (output-only patch in `review_fixes_r9.py`). Frozen data and supplement tables keep the raw label.
