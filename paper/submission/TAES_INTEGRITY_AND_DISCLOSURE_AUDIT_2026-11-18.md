# IEEE TAES regular-paper integrity, bibliography, and disclosure audit

**Date:** 2026-11-18. **Status:** PRE-SUBMISSION GATE; not a submitted, author-approved or publisher-format-verified paper.  
**Science:** Studies A–D and raw evidence remain frozen; no numerical outcome changed.  
**Reference basis:** Current `paper/manuscript/manuscript.md`, `references/bibliography.bib`, Supplementary S0/S1, and the author's uploaded v2 19-page **measurement** PDF/LaTeX log.  
**Automated check:** `python3 paper/submission/check_taes_citations_and_supplements.py`.

## 1. Authoritative TAES instructions (rechecked 2026-11-18)

- [IEEE AESS TAES author page](https://ieee-aess.org/publications/transactions-aes/author-information): Regular Paper submissions require a **10-point, two-column, single-spaced PDF**, approximately 1-in top/bottom, 0.7-in side margins, 3.45-in column width and 0.2-in gap. There is **no formal submission page limit**; paper length can influence editorial decisions, and published pages beyond 10 cost **US$200 per page**.
- [IEEE AESS AI content guidance](https://ieee-aess.org/using-ai-generated-content-ieee-article-and-its-review): AI-generated content (including text, figures and code) requires a statement in acknowledgments naming the system, sections and extent. Grammar-only assistance is generally outside the mandatory rule, with disclosure encouraged. Actual human/AI contributions must be confirmed by the author.
- TAES uses **single-anonymous** review; author identities are visible to reviewers. Final author names, affiliation and ORCID still require author approval; the measurement PDF intentionally uses a placeholder and is not a submission artifact.
- TAES permits supplementary code/data/PDF but requires **reviewer-accessible supplemental files, references in the manuscript and a README**; public repository references alone do not prove accessibility to reviewers.
- Submission of the *same previously rejected manuscript* requires disclosure and correspondence; an unrelated prior rejection is not automatically a rejection of the current paper. Same-author related submissions/publications nevertheless require an originality/overlap check.
- TAES's explicit LaTeX template link (the web asset `TAES+Template.zip`) returned HTTP **404** during this audit. The installed `IEEEtran` class and manually matched geometry are a valid **measurement approximation**, not independent confirmation that the exact TAES template package was compiled. Obtain the journal-specific package through [IEEE Template Selector](https://template-selector.ieee.org/) or the editorial office before declaring this gate passed.

## 2. Evidence and citation reconciliation

The uploaded v2 compile reported **19 pages**, zero overfull hboxes/vboxes, no undefined citations, a **250-word abstract**, and full-width Figures 1–3. The TeX input was `IEEEtran` in journal/two-column/10-point mode with the above margins. This verifies geometry and float behavior **only**, not final publisher-template, content-integrity, author-information or disclosure approval.

There are **13 distinct in-text citation keys, 13 bibliography entries actually printed, and 14 BibTeX library records**. All 13 cited keys resolve; one extra library entry, `singh_dissertation`, is **uncited/unprinted**. This is not a missing manuscript reference or proof of self-citation omission: decide whether the dissertation materially underlies this TT&C study, and cite/disclose only if appropriate.

### Reference verification register

External pages were consulted on 2026-11-18. “Verified metadata” is not the same as independent verification of *every* claim in the manuscript or every source's full text. DOIs are listed for identity, not reproduced as new research evidence.

| Key / group | Current source / identifier | Verification |
|---|---|---|
| `ccsds_sdls_355_0_b_2` | [CCSDS 355.0-B-2, Aug. 2022](https://ccsds.org/publications/bluebooks/) | Number, title, edition/date checked against CCSDS list |
| `ccsds_sdls_ep_355_1_b_1` | [CCSDS 355.1-B-1, Feb. 2020](https://ccsds.org/Pubs/355x1b1.pdf) | Number/title/date verified; any catalog display ambiguity should be checked against CCSDS |
| `ccsds_sdls_rationale_350_5_g_2` | [CCSDS 350.5-G-2, Jan. 2024](https://ccsds.org/Pubs/350x5g2.pdf) | Green Book context and Recovery SA prior-art limitation already recorded |
| `ccsds_sdls_ep_rationale_350_11_g_1` | [CCSDS 350.11-G-1, Jul. 2024](https://ccsds.org/Pubs/350x11g1e1.pdf) | Number/date verified against CCSDS SLS catalog |
| `nist_fips203` | [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), DOI 10.6028/NIST.FIPS.203 | Primary NIST standard metadata |
| `nist_sp800_227` | [NIST SP 800-227](https://csrc.nist.gov/pubs/sp/800/227/final), DOI 10.6028/NIST.SP.800-227 | 2025 date/author list confirmed by NIST |
| `bader_ttc_key_management` | [Bader, SpaceSec 2024 original](https://www.ndss-symposium.org/wp-content/uploads/spacesec2024-53-paper.pdf), DOI 10.14722/spacesec.2024.23053 | Title, author, workshop, date and abstract reviewed; all-frame protection and PCS framing supported |
| `hulsing_lange_weber_sdls_key_update` | [University of Eindhoven record](https://research.tue.nl/en/publications/a-key-update-mechanism-for-the-space-data-link-security-protocol/), DOI 10.1007/978-981-95-4434-9_29 | Authors, CANS 2025 proceedings published 2026, LNCS 16351, pp. 602–611 and abstract checked |
| `dowling_hale_tian_wimalasiri_space_key` | [arXiv:2503.06785](https://arxiv.org/abs/2503.06785) | Four authors, title/ID and **preprint** status corroborated; not peer-reviewed proceedings |
| `poettering_roesler_bidirectional_rke` | [Royal Holloway bibliographic record](https://pure.royalholloway.ac.uk/en/publications/towards-bidirectional-ratcheted-key-exchange/), DOI 10.1007/978-3-319-96884-1_1 | Authors, CRYPTO 2018, pp. 3–32 and abstract checked |
| `poettering_roesler_async_rke` | [IACR ePrint 2018/296](https://eprint.iacr.org/2018/296) | Report identity and two authors corroborated; no peer-reviewed status inferred |
| `idan_aegissat` | [NDSS SpaceSec 2025 paper](https://www.ndss-symposium.org/wp-content/uploads/spacesec25-final69.pdf), DOI 10.14722/spacesec.2025.23069 | Title, author list, original workshop/date and abstract checked. Confirm unusual surname/transliteration against publisher if editing |
| `castanon_remy_space_testbed` | [NDSS SpaceSec 2025 paper](https://www.ndss-symposium.org/wp-content/uploads/spacesec25-final42.pdf), DOI 10.14722/spacesec.2025.23042 | Four authors, workshop date and seven-attribute fidelity framework verified from original paper |

## 3. Hard gates and outstanding integrity risks

| Gate | Disposition | Smallest remaining action |
|---|---|---|
| Current source/bibliography citation-key reconciliation | **PASS** | No key change justified; keep source-integrity CI |
| Reference identity sample and standards currency | **PARTIAL** | 13 identities screened, selected claims compared with original abstracts; full sentence-by-sentence citation support and retraction checks still require scholarly review |
| Abstract and Study A–D count integrity | **PASS in prior CI** | Preserve 250 words and frozen source rows |
| Supplementary S0/S1 evidence | **PASS for source equality; packaging PENDING** | Validate S0/S1 with their builders, generate legible reviewer PDFs, upload both and README |
| 19-page two-column layout | **PASS as preview** | Obtain *exact* journal template and visually inspect final source; no automatic 10-page limit |
| Author information / ORCID | **UNVERIFIED** | Author confirms exact public name, affiliation, email/ORCID and authorship; **do not guess or commit private contacts** |
| AI-use declaration | **HOLD** | Author confirms each actual AI system, contribution level and affected text/figure/code sections; provide disclosure in acknowledgments if applicable |
| Funding and competing interests | **HOLD** | Author supplies accurate statements specific to TT&C work; never import unrelated manuscript declarations without verification |
| Originality, preprints, previous reviews | **HOLD** | Compare related same-author studies, disclose related published/submitted works as requested; if this *same* manuscript was rejected elsewhere, disclose correspondence |
| Raw research archive and rights | **HOLD** | Raw retained external bundle not publicly archived; no fabricated DOI, no unauthorized release |
| Technical novelty and applicability | **REVIEW REQUIRED** | Maintain explicit CCSDS Recovery SA prior-art boundary, synthetic-only interpretation and aerospace commandability consequence |
| Submission authority | **NOT AUTHORIZED** | Author approves final artifact and all declarations before any portal submission |

**No technical journal submission or external message was sent.** This audit deliberately does not add guessed acknowledgments, new author names, grant claims, conflicts, IRB decisions or a permanent archive link. Confirm and incorporate all relevant facts privately before inserting them in a publisher-facing manuscript.

## 4. Author-only disclosure worksheet (keep private; not in public Git)

**A. Authorship:** Author/public affiliation, ORCID, correspondence address, author approval.  
**B. Funding/COI:** All direct/indirect support, employer/client IP restrictions, actual competing interests and none-if-true statements.  
**C. AI-use:** Which system(s) were used? Distinguish language-only proofreading from substantive drafts, code/figure creation, search/synthesis and analytic work; name affected article sections and scope. Review and independently verify all technical assertions.  
**D. Provenance:** Any material based on doctoral dissertation or prior submitted papers? List overlaps and distinct claims; any prior rejection of *this exact paper*?  
**E. Reproducibility:** Retained bundle access for reviewers, archive rights, public vs controlled release, DOI only if actual deposit exists.

These statements require the author's factual confirmation; no related-paper memory or previous declarations substitute for approval.
