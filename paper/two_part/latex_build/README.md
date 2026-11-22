# paper/two_part/latex_build: local PDF build in the IEEE TAES template (DRAFT)

Builds a review PDF of the compact two-part manuscript. Nothing here is submitted, and the output is not a final TAES file.

```
python3 -I paper/two_part/build_two_part_manuscript.py --compact
paper/two_part/latex_build/build.sh <dir with IEEEtaes.cls and IEEEtaes.bst> <empty work dir outside the repo>
```
- The IEEE class and style files come from the TAES template package and are NOT stored in this repo.
- Author, affiliation, funding and first-page footnote are placeholders (author declarations are on hold).
- Section numbers in the text are the manuscript's own ("Section 7.10"), so headings are unnumbered in LaTeX. The Part II sections are labelled II.1-II.5, which can be confused with the template's Roman-numeral sections; decide before submission.
- Figure 1 and 2 are page-wide (figure*), Figure 3 is one column; the 40-row matrix is in the supplement (supplement_S1_deterministic_matrix.md).
- Page count in the private build (2026-11-21): 21 pages for the compact output; 20 pages with the opt-in trim (`build_two_part_manuscript.py --compact --trim`, then `build.sh <template dir> <work dir> trim`). The trim condenses the Conclusion's results recap and drops the Introduction's study-inventory sentence; no number or caveat is lost. IEEE's final proof decides the real count.
