# IEEE-ready figure copies for the two-part paper

The Part I figures (`paper/figures/rendered/*.svg`) are checksum-locked and are NOT changed.
These are separate, redrawn copies prepared against the IEEE TAES template rules (checked 2026-11-19):

| File | Size | Why |
|---|---|---|
| `fig1.pdf` | 7.16 in (page-wide) | architecture diagram; text is 8 pt or larger at this size |
| `fig2.pdf` | 7.16 in (page-wide) | outcome distribution (values from `paper/figures/figure-2-outcome-distribution-source.csv`) |
| `fig3.pdf` | 3.5 in (one column) | retry/retention grid (values from `paper/figures/figure-3-sensitivity-source.csv`) |

Differences from the Part I figures: physical size fixed to the template widths; all text at least 8 pt as printed;
no "Figure N." title inside the image (IEEE: captions are not part of the figure); the two descriptive notes that sat
inside Figures 2 and 3 are added to their captions by `paper/two_part/build_two_part_manuscript.py`.
Vector PDF is an IEEE-accepted format; `*.png` are 600 dpi line-art copies; `*.svg` are the sources.

Regenerate: `python3 -I paper/two_part/figures_ieee/make_ieee_figures.py` (needs `cairosvg` for PDF/PNG; without it only SVG is written).
The script reads the Part I CSVs read-only and writes only into this folder.

For the final LaTeX files, place Figures 1 and 2 as page-wide (`figure*`) and Figure 3 in one column.
Not yet done: author review of the redrawn figures.
