# Author-only action packet (prepared 2026-11-21; nothing here has been executed)

Each item below needs your own decision. I prepared inputs only. Your standing rules block me from submitting, publishing data, paying, approving declarations, running NOS3/CryptoLib, or merging, so none of these was done.

## 1. Third-party timestamp and deposit (publishes data: yours to do)
What exists: tags `study-e-prereg-v1` and `study-f-plan-v1`, frozen Part I manifest (358 entries), Study G protocol hash.
Why it matters: the pre-registration is currently author-frozen only. A third-party timestamp is what turns "declared before the run" into something a reviewer can check.
Options (cheapest and least reversible first thing to decide):
- Hash-only timestamp (OpenTimestamps or similar): publishes only a SHA-256, no data. Low risk, free. Needs the tag commit SHA and the file hash list.
- Zenodo (GitHub release integration) or OSF registration: publishes content. A public Zenodo record cannot be deleted, and an OSF public registration cannot be withdrawn without a permanent tombstone. Decide first whether the repo contents are releasable (no restricted material, licence chosen).
Before doing it: confirm licence file, confirm no restricted spacecraft or vendor material in the bundle, confirm author name/ORCID metadata, and decide embargo.
Devil's advocate: a timestamp made after Studies A-D ran proves nothing about Part I, only that the Part II/Study F declarations were frozen at the stated time. State it that way.

## 2. Independent human re-implementation (needs another person)
Brief to give them: written spec only (system and threat model, T1 rules, Study B schedule rule, outcome vocabulary), not the code or results. They freeze their code and outputs, then compare against `paper/tables/table-2-deterministic-t1.csv`.
Acceptance: agreement on outcome, alignment, security_state, availability_state and verification_complete for the 40 Study B schedules; list every spec ambiguity found. The AI agent's run (docs/study_g/AI_REIMPLEMENTATION_REPORT_2026-11-21.md) already lists the known ambiguities: duplicate and stale-replay counter attribution, whether a rejection stops retries, STATUS opportunity after a lost TEST, and the Part II restart rules.
Fixing those spec gaps before handing it over would make the exercise cleaner.
Cost: their time; any payment is yours to decide.

## 3. Submission, fees, overlength
Current manuscript: 19 pages. From the earlier check of the official AESS page: $200 per printed page beyond 10 for accepted regular papers, so about $1,800 at 19 pages. Confirm on the IEEE/AESS page at submission time; fees and limits change.
Options: accept the charge; cut toward the page limit (each cut costs claims or evidence); or move Part II to a separate paper (rejected earlier in favour of one paper). I have not submitted or paid anything. PUBLISHER_SUBMISSION_AUTHORIZED stays false.

## 4. Author declarations and AI-use statement
Draft material is in the Project doc `AUTHOR_DECLARATIONS_2026-11-21.md`. Facts only you can state: funding, conflicts of interest, data availability intent, the degree of AI assistance in design, code and prose (Studies F, G and the re-implementation were AI-assisted), and corresponding-author details. I did not complete or approve any of these.

## 5. NOS3 / CryptoLib (F1-F4 runtime, HOLD)
Not run. Conditions I would want before proposing a run: written approval from you, an isolated container with no network, no flight hardware or vendor-restricted images, pinned commits recorded, and a report that says what was and was not exercised. Until then the manuscript's no-conformance statement stands.

## 6. PR #31: ready-for-review and merge gates
Checklist (all must be yours): manifest regenerated and committed; ROUND10 PDF reviewed by you; abstract v9 approved; items 1-4 decided; confirm no restricted material in the diff; mark ready; merge.
I leave the PR as a draft.

## Done by me this round (non-restricted)
Citation audit (DOIs verified via Crossref for 9 records; Gray, Skeen, Alwen and Cohn-Gordon completed; access dates added to web sources), SECURE_DEGRADED shown as `LOCKOUT` in the text only, Part II regime map (Supplementary Figure S8).
