# TAES Regular Paper template receipt and layout feasibility audit

**Date:** 2026-11-18. **Disposition:** SELECTED CLASS COMPILES; FULL MANUSCRIPT/PUBLISHER GATE STILL HOLD.

## Artifact provenance and class identity

An author-uploaded ZIP named `IEEE_TAES_templates_latex(1).zip` was inspected in an isolated local workspace. ZIP SHA-256: `35f453d90866185dad95c99f8aff3e455b25e354eed7c8701897900db7215d45`. It contains **Regular Paper**, Correspondence and Letter templates (24 entries). No ZIP path traversal or symbolic-link entries were observed.

The appropriate Regular Paper subfolder supplies `IEEEtaes.cls`, `IEEEtaes.bst` and the sample `IEEE_TAES_regular_template_latex.tex`. Class SHA-256: `7b3e3d4553f4f871a3e9e3be13c063ea36b21f698a48f6584127b290f86dd7d4`. The class header identifies `2022/02/15 version V1.1`. This historical version has not been independently proven to be the most recent publisher release, as [TAES's primary author-information page](https://ieee-aess.org/publications/transactions-aes/author-information) has a direct template link returning HTTP 404 on 2026-11-18. The uploaded archive's provenance cannot be authenticated solely from its filename.

## Offline compilation and Table I layout proof

- User-supplied Regular Paper example: **pdflatex/latexmk completed with exit 0** using `-no-shell-escape`, producing a seven-page, US Letter example. This checks the template's local buildability, **not** the full TT&C manuscript.
- The class source hardcodes `textwidth=41pc` (492 TeX points), `columnsep=12pt` and native `tablefont=8.25pt`. A nominal column width of 240pt is ~3.32 inches, not the exact 3.45 inches/0.2-inch gutter stated on TAES's currently published [submission requirements](https://ieee-aess.org/publications/transactions-aes/author-information). Do not patch the class silently or state exact publisher geometry compliance before resolving this discrepancy.
- Independent full-width `table*` **feasibility fixture** compiled with the uploaded class and all 13 members / seven fields / complete evidence JSON from frozen `paper/tables/table-1-matched-family-outcomes.csv`. Source SHA-256 validated as `ef29a216b3de050a219e83a0e78c68e3f2f207160418bdafe0a3424a3b94a140`. This is a static presentation-only transformation, **not** rerunning Studies A-D.
- The resulting two-page PDF has Table I on page 2 with native `\\tablefont` approximately 8.25pt (PDF span check approximately 8.22pt), **zero LaTeX overfull-box diagnostics** and all 13 source member IDs displayed. CF-02 B1-01 and B1-05 remain separate rows within one analysis unit.
- The table proof is **not** a full manuscript compile: no integrated figures, equation/floats across the full body, publisher page estimate, bibliographic correctness, author metadata or release declaration is certified.

## Gate disposition

| Gate | Result |
|---|---|
| Correct template family and offline class compile | PASS, LOCAL SAMPLE ONLY |
| Full original seven-field Study A Table I in a wider, native-size float | PASS, ISOLATED LAYOUT FIXTURE ONLY |
| Latest class identity and exact TAES geometry | **HOLD** |
| Full current-manuscript build and visual review | **HOLD** |
| Final author, AI-use, funding/conflicts, copyright, originality and portal authorization | **HOLD** |

Do not commit the vendor's class/ZIP to this public repository or upload confidential author information. Source fixtures and PDFs are retained as author-local conversation artifacts, not publisher-facing submissions. This report does not change `taes_release_gates.json` and does not authorize publisher submission.
