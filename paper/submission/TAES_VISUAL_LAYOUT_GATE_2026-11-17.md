# TAES figure geometry correction and full-width display gate

**Date:** 2026-11-17  
**Status:** SVG source corrections and CI sizing contract; **not** a new PDF layout validation or publisher-ready manuscript.  
**Source:** `paper/figures/render_publication_figures.py` and three regenerated SVGs.  
**Science:** study data CSVs, counts, trial populations and results unchanged.

## Verified failure in prior layout-only PDF

The existing 18-page 10pt two-column **measurement** PDF (not a final TAES PDF) placed Figure 1, Figure 2 and Figure 3 at `\\columnwidth`. The Figure 1 box labels were about 3 pt. Figure 2's y-axis annotation was clipped by the left margin, and Figure 3's horizontal candidate-lifetime annotation collided with matrix labels. Table I was about 4.9 pt; its fix is a **separate pending task**.

The renderer fixes two overlapping axes by rotating each y-axis label 90 degrees (Figures 2/3) and raises four small Figure 1 labels from 15/16 to 17 raw SVG units. These are visual source-only corrections. The embedded numerical chart content remains unchanged.

## Physical print-size gate

At TAES's approximate full two-column text width (7.1 in = 511.2 typographic points), the minimum SVG glyph font sizes are:

| SVG | Intrinsic width | Smallest raw font size | At 511.2 pt full-width display |
|---|---:|---:|---:|
| Figure 1 | 1400 px | 17 | 6.21 pt |
| Figure 2 | 1100 px | 14 | 6.51 pt |
| Figure 3 | 920 px | 14 | 7.78 pt |

**These are nominal geometric sizes**; final visual inspection and PDF font/render metrics remain mandatory. The same graphics scaled to a 3.45-inch column would be too small. The paper's PDF build must place all three graphics as `figure*` environments with `\\includegraphics[width=\\textwidth]`, and should not shrink them further than these conditions without re-evaluation.

## Separate, still-unresolved items

1. Reformat Table I's 13 qualified-family member rows to readable physical type while preserving every authorized-field tuple and the CF-02 B1 shared-analysis-unit rule. The existing source CSV cannot be abbreviated silently.
2. Keep the full 40-row Study B matrix in `paper/supplement/SUPPLEMENTARY_TABLE_S1.md` (committed by PR #21); preserve all 10 columns and `SECURE_DEGRADED / security_state=UNSAFE`. Generate a separately paginated supplement PDF after readability review.
3. Keep the T1 PREPARE/RESPONSE/COMMIT/CONFIRM display together across column boundaries; avoid full-document `clearpage` solely to move bibliography.
4. Recompile a complete IEEE two-column draft after this figure-source change and inspect every float, heading, axis label, reference and page break. The 18-page measurement count is historical, not guaranteed for the revised layout.
5. Confirm acknowledgments/AI-use and funding/COI declarations, author details, bibliography metadata, and controlled access to the raw archive before journal submission.

## Scope and originality

No other satellite project was touched. There is no new dataset, experiment execution, CCSDS conformance assessment, flight/ground deployment, raw archive release or TAES publisher submission.
