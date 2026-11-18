# TAES originality, reviewer-package and release-readiness gate

**Snapshot:** 2026-11-18. **Disposition:** AUTHOR-SIGNOFF HOLD; this is an internal review aid, not a publisher-ready manuscript, independent originality clearance, or permission to submit.

**Scope:** `Zartharas/satcom-ttc-post-compromise-recovery` at `main` commit `1bda511862f104e82bddcbf95db1ee97702e6c02`. Existing Studies A-D and retained experiments are frozen. This document makes no change to their results, author identities, data access, or published claims. The machine-readable companion is `paper/submission/taes_release_gates.json`; `python3 paper/submission/check_taes_release_gates.py` checks the fail-closed state.

## Current primary-policy basis

- [IEEE AESS TAES author instructions](https://ieee-aess.org/publications/transactions-aes/author-information) (consulted 2026-11-18): original work only, no simultaneous submission of the same article, citation and clear differentiation of prior *published* related work, author approval, PDF submission, single-anonymous review, and author responsibility for rights/consents. The rules require disclosure and earlier correspondence where the **same manuscript** was previously reviewed and rejected; a prior rejection of a **different** paper must not be misrepresented as this paper's submission history.
- [IEEE AESS AI-content policy](https://ieee-aess.org/using-ai-generated-content-ieee-article-and-its-review) (consulted 2026-11-18): substantive AI-generated text, figures or code must be identified by system, article section and extent in acknowledgments. Grammar-only help is treated separately. A specific factual contribution inventory must come from the author; do not infer it from tool usage or past papers.
- Current [TAES reference/bibliography audit](TAES_INTEGRITY_AND_DISCLOSURE_AUDIT_2026-11-18.md) finds 13 resolved in-text references, but not a sentence-by-sentence claim verification. The uncited `singh_dissertation` BibTeX item is a decision point, not automatically required or proof of omission.

## Originality boundary, based on read-only public repository evidence

| Work | `main` observed SHA | Distinct primary question and lineage | Clearance still required |
|---|---|---|---|
| [This TT&C recovery study](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery) | `1bda511862f104e82bddcbf95db1ee97702e6c02` | Frozen deterministic Studies A-D model post-compromise resynchronization, endpoint activation, verification evidence, restart and retry outcomes; abstract cryptographic core, no flight implementation. | Confirm no duplicate current submission, prior manuscript history, text/figure reuse and author declaration. |
| [Mission-aware satellite cyber-recovery](https://github.com/Zartharas/mission-aware-satellite-cyber-recovery) | `7fd87eb1bbfb5ec811bb1f8ec29b4532ac5ff425` | Separate mission-response decision/evidence studies (Studies 1-9 and extensions); includes contact proxies and software integration work that **must not** be imported as new TT&C evidence. Public README records multiple separate publication lines, including a previously rejected TAES **Paper 2** and its subsequent CEAS route. | Compare exact overlap in claims, source data, figures, methods and submissions; distinguish the earlier Paper 2 decision from this manuscript. Author must confirm related-work disclosures. |
| [Verifiable spacecraft lifecycle](https://github.com/Zartharas/verifiable-spacecraft-lifecycle) | `f0a26d2edd974827741a53c566b6c79ca2ebdd0b` | S0-S5 spacecraft software supply-chain pipeline and tamper/rollback/attestation testing; `STATUS.md` records JSSE revision preparation. Do not repackage its software integrity outcomes as TT&C key recovery validation. | Check manuscript text, evidence and author rights for reused or closely related material. |

This is a **scope-screen**, not a plagiarism-detection score or a legal/publisher originality certification. Cross-project repo heads are observations at this date, not locks on those other projects. The upstream CCSDS 350.5-G-2 Recovery SA / segregated durable-context concept is explicit prior art, **not** an invention of the TT&C treatment; the manuscript already states this limitation. The prospective NOS3/CryptoLib F1-F4 extension remains on its independent safety **HOLD** and is not submission evidence. See `paper/extension/TTCSIL_NONOVERLAP_GATE_2026-11-16.md` and `paper/extension/ttcsil_integration/INTEGRATED_RECOVERY_GATE_AND_EVIDENCE_CONTRACT_2026-11-17.md`.

## Pending release gates and exact completion evidence

| Gate | State | Required evidence / action |
|---|---|---|
| Publisher-specific layout | **HOLD** | Acquire official TAES template package (the journal's earlier direct archive link was unavailable); compile **the complete manuscript** against the approved template; inspect final PDF layout, figure sizes, full bibliography and page breaks. The prior 19-page IEEEtran **measurement** is not an approved final template compile. |
| Table I readability | **HOLD** | Correct the approximately 4.9-point Table I typesetting observed in the earlier draft; retain all 13 source members, seven source fields and CF-02 shared analysis-unit semantics. No silent aggregation or source mutation. |
| Reviewer S0 and S1 | **HOLD** | Confirm draft PR #26's PDF renderer and source-lock checks, inspect the final reviewer PDFs, and confirm files/README are actually available to reviewers in the journal portal. Local draft PDFs or a public repository link alone do not prove portal access. |
| Claim-level citation support | **HOLD** | Independently check every consequential standards/cryptography/empirical claim against the relevant original text; the key/metadata reconciliation is not sufficient. Resolve the uncited dissertation only if it materially informs this article. |
| Authorship / ORCID / contact metadata | **HOLD** | Author privately approves exact name, affiliation, correspondent identity, ORCID, contributions and version. Never commit personal email, private correspondence or portal credentials to public Git. |
| AI-content disclosure | **HOLD** | Author inventories all actual AI systems and specific text/figure/code sections plus substantive level; review IEEE-compliant acknowledgment wording before inclusion. Never copy a generic AI disclaimer or declarations from unrelated papers. |
| Funding / conflicts / employment rights | **HOLD** | Author confirms all direct and indirect support, competing interests and any employer/client intellectual-property permissions that apply specifically to this study. No presumed "none" statement. |
| Same-author related work / submissions | **HOLD** | Author confirms no concurrent submission of the same article; review citation/overlap and prior rejection history of **this exact manuscript**. Prior TAES Paper 2 rejection in the other repo is not presumed to be this manuscript. |
| Raw evidence access and rights | **HOLD** | Verify controlled reviewer access, any third-party rights, retention identity, archival license and redistribution permission. No public raw-data upload or invented archival DOI. |
| Author final signoff / publisher action | **HOLD** | Obtain explicit approval of the *final* PDF, declarations, supplements and portal metadata before any submission. No autonomous upload, final publication assertion or fee commitment. |

## Fail-closed review rules

1. All holds remain unresolved in `taes_release_gates.json`; its values record **unverified publication readiness**, not a checklist that authorless automation can approve.
2. The static checker returns zero only if the registry still enforces `publisher_submission_authorized=false`, `author_approval_documented=false` and the ten exact HOLD gates. The `--require-ready` mode returns nonzero until a separately reviewed and explicitly authorized release procedure exists.
3. No frozen study CSV, experiment trace, science conclusion, author identity, public licensing status, integration runtime or manuscript text is modified by this review artifact.
4. Final author declarations and any evidence containing confidential information belong in a private author-controlled location, **not** this public repository or the CI logs.
5. The next release decision requires specific proof of each gate; a green CI status indicates only *correctly maintained holds*, never publication readiness.

**No submission, external email, public data release, template-compilation certification or integrated satellite experiment is authorized by this document.**
