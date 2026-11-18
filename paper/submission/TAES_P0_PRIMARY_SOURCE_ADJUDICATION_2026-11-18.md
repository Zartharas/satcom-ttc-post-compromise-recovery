# TAES P0 primary-source adjudication: scope of three verified claim groups

**Date:** 2026-11-18. **Status:** claim-limited primary-source verification, not a complete citation audit, originality clearance, or publisher approval. Frozen Studies A-D unchanged.

| Source | Inspected original location | Supported claim | Claim-level disposition |
|---|---|---|---|
| CCSDS 350.5-G-2, January 2024 | Sec. 3.5.1.2, p. 3-25; Sec. 4.5.6, p. 4-14 | Recovery SA already exists as a segregated last-resort TC concept; the Green Book discusses counter desynchronization, lost telemetry, damaged key storage and non-volatile protected recovery context. | PASS for this **prior-art boundary only**. Informational report, not implementation conformance. |
| Christoph Bader, SpaceSec 2024 | Introduction and Sec. V, p. 8 | All-frame first-contact protection; SDLS Extended Procedures alone do not meet his post-compromise key-management requirements; re-establishing a secure key after lost synchronization while retaining strong PCS is described as an open problem. | PASS for the source's stated concern. Current simulation's opaque cryptographic core cannot solve or claim the cryptographic open problem. |
| Andreas Huelsing, Tanja Lange and Fiona Johanna Weber, CANS 2025 (published 2026) | Accepted manuscript pp. 3-4 and 7 | Independent Triple-KEM SDLS key update delivers key material after handshake completion and uses key confirmation. The authors explicitly note that loss or reordering of fragments requires a separate handling layer or a dropped connection. | PASS for the explicit limitation. The source did **not** ignore delivery faults; project-defined activation, retry and verified commandability remain separate. |

## Original publication links

- CCSDS 350.5-G-2: https://ccsds.org/Pubs/350x5g2.pdf
- Bader original: https://www.ndss-symposium.org/wp-content/uploads/spacesec2024-53-paper.pdf
- Huelsing/Lange/Weber author accepted version: https://pure.tue.nl/ws/portalfiles/portal/375669792/llncs.pdf ; final record DOI https://doi.org/10.1007/978-981-95-4434-9_29

## Manuscript change and unresolved reviews

This audit supports two narrowly scoped source clarifications in `paper/manuscript/background-related-work.md`, mirrored verbatim by the generated integrated manuscript. It does not introduce new references, modify abstract population counts, alter data tables, rerun experiments or approve any stronger security/flight claims.

The other 15 citation-bearing manuscript blocks still require individual technical-claim assessment, with appropriate source passages and scope notes. An existing citation-key checksum gate is not equivalent to full scientific fact-checking. The author retains responsibility for the uncited dissertation decision, originality disclosures, final formatted PDF and any publisher-facing declarations. All submission holds remain in force.
