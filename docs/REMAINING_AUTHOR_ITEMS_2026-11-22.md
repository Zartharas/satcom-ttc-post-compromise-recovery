# Remaining author items, status and gates (2026-11-22; nothing below has been submitted, published, paid, signed or merged)

Review PDF to read: paper/two_part/out/two_part_compact_trim_review_ROUND11.pdf (git-ignored; 19 pages, fonts embedded, sha256 f8b864af75a49932ec8f8a39a2ac19fdb75af4d5bddf38055b7b4ce63278ae3f). Branch head at build time: 1c01383 plus the files in this commit. Overlength fee: excluded from this round by the author.

## 1. Third-party timestamp / deposit  (prepared; needs your go/no-go)
Inputs: docs/timestamp/ANCHOR_2026-11-22.txt and docs/timestamp/README.md (commit, tree and tar hashes of study-e-prereg-v1, study-e-analysis-script-v1, study-f-plan-v1; all three tags are on GitHub). Decision needed: Option A hash-only OpenTimestamps (free, reveals only a hash) or Option B Zenodo release (public, not deletable). Suggested order: A now, B only after you decide on a release licence/embargo and spot-check docs/f1_f4_software_only/. Commands are in the README; I did not run them because they contact third parties.

## 2. Independent human re-implementation  (prepared; needs a person)
docs/independent_reimplementation/BRIEF_FOR_IMPLEMENTER.md (what to give, what to withhold, freeze protocol, acceptance) and compare_study_b.py (self-test on the reference table gives 40/40, 31/31). You choose the person and any terms. Before sending, grep the files you hand over for result numbers.

## 3. Submission (excluding the fee)  (checklist; PUBLISHER_SUBMISSION_AUTHORIZED stays false)
Ready: PDF, ORCID (public), declarations (docs in the Project: AUTHOR_DECLARATIONS), data-availability text, cover-letter text. Before you submit: (a) decide the Acknowledgment change in item 4; (b) re-hash the retained raw Part I bundle against the SHA-256 in Section 9.2; (c) confirm the page-fee rate on the live AESS/IEEE pages; (d) enter the same name form as the ORCID; (e) say in the cover letter whether the repository, Study E/F/G tags and any timestamp exist and when they were made; (f) mention TAES-2026-4182 only if asked.

## 4. Author declarations / AI-use statement  (one proposed change; needs your approval)
The published Acknowledgment does not yet mention work done since: Study G, the Part II/Part I reconciliation, the regime-map figure, the software-only CryptoLib restart harness and Docker kit, and the AI-agent re-implementation. All were written by Claude Sonnet 5.5 and none was reviewed line by line by you unless you say so. Proposed replacement for the second sentence of the Acknowledgment (your words to confirm; the review sentence must reflect what you actually did):
"Claude Sonnet 5.5 edited the Part I text, drafted Part II, and wrote the software, tests and build scripts for Studies E, F and G, the Part I/Part II reconciliation, the Part II regime-map figure and the software-only restart harness; an AI agent also re-implemented the Study B specification (not an independent party)."
Then the review sentence: "The author ran the tests, reviewed [the Study E code, tests and Part I text line by line, and read the rest in full] and takes responsibility for all content." Edit the bracket to what is true. I did not change the manuscript; applying this needs your approval because it is your declaration.

## 5. PR #31  (marked ready; do not merge until)
Gates: you have read ROUND11; items 3-4 decided; CI green on the head you intend to merge (it has been at every push so far); no restricted material (scan done, see timestamp README); frozen Part I files untouched (CI job "Preserve frozen results" passes). Merging is yours.

## 6. Full read of the PDF and sign-off  (yours)
Read-through list: abstract v9 (246 words) against Sections 5.12, 7.10, 8.10; every number in the abstract and Section 7 against the CSV in results/ or study_*_out; Table I security-state column and "TEST COMMAND" vs "TEST_COMMAND" spelling (known open from the memo); Supplementary Figure S8 caption says illustrative, not pre-registered; the two bracketed claims in Section 8.10 (F1-F4 software-only; no conformance claim); figures legible on pages 7 and 11.
