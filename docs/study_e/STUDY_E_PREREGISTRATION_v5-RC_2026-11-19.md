# Study E pre-registration, FREEZE CANDIDATE v5-RC (NOT FROZEN; no pre-registered run executed)
Status: development draft against code v0.6.0-dev (v0.5.0-dev + `anchors.py`; exchange model unchanged; Dockerfile pinned by digest). Freezing needs the author's separate explicit approval (commit hash recorded before any pre-registered execution). Studies A-D immutable, not rerun/pooled/reinterpreted. No CCSDS conformance claim. PCS labels are not verified cryptography.

## Question
When SDLS key activation or ratchet state is disrupted by loss, restart and short contact windows, how often does an automated exchange finish, diverge, or stall, and how much do persistence, retry and resumability choices change that? The standards read (CCSDS 355.1-B-1, 354.0-M-1) define activation and verification but leave recovery out of scope (354.0-M-1 3.1.2); SDLS-DR (Ledin et al., RISC 2026) specifies state persistence and Recovery-association re-provisioning but reports no evaluation of contact windows, handover or delay.

## Model (code: study_e v0.6.0-dev)
- Exchange: 6-message project abstraction of activation + verification (A1); K slots/contact, budget B, lifetime L; i.i.d. loss p or Gilbert-Elliott channel (sensitivity); spacecraft restart r at contact boundaries; persistence volatile/commit/journal; activation local/gated.
- Run: horizon H contacts; EXPIRED_OLD retries; divergence ends the exchange; INDETERMINATE = option (a) operator-handled (reported) and option (b) resumable verification (sensitivity, `resume=True`, assumption outside the standards).
- R0: after divergence, detection delay `detect`, then re-bootstrap chain (n_msgs, B0, L0) over a static Recovery SA (parameters are model assumptions; SDLS-DR gives none).
- R2: bounded skipped-key cache desynchronisation, `cmax` a model parameter (frame level only; deliberately NOT coupled to the exchange, reported separately).

## Endpoints
P(SUCCESS), P(RECOVERED), P(UNRECOVERED_DIVERGED), P(INDETERMINATE), P(EXPIRED_OLD), expected attempts, expected contacts; P(desync) for R2 reported separately.

## Hypotheses
- H-E1: exact DP equals exhaustive enumeration (exact rationals) and TLC reachability support, on the validation grid.
- H-E2a: SUCCESS non-decreasing in B, K, L, H, non-increasing in p. Divergence reported, not assumed monotone (witness: P(S-ahead) = P(exactly 3 successes) rises with B).
- H-E2b: gated activation: more durable persistence never increases ground-ahead divergence.
- H-E2c: journal persistence makes outcomes invariant to r; volatile fallback-required probability non-decreasing in r.
- H-E3: with EXPIRED_OLD-only retry, raising H changes SUCCESS by less than the INDETERMINATE mass; resumable completion (b) is the dominant lever (development values at the single point p=0.3, K=3, B=8, L=3, r=0.1: 0.49-0.59 -> 0.77-0.95; not a grid-wide range).
- H-E4: with a static Recovery SA and a long horizon, divergence is almost always recoverable; the cost is contacts and loss of forward secrecy on that association (not measured here). Shorter horizons and heavier loss are needed for detection delay to matter.
- H-E5: bursty loss at equal stationary loss changes outcomes but not in a fixed direction (witness exists in both directions).

## Validation (must pass before any pre-registered run)
Exact==enumeration; closed forms (binomial, total loss, one-contact geometric, cmax=0 desync); Monte Carlo within 4.5 SE (seeds 20261201..); mutation tests kill seeded bugs; TLC support check (432 and 2,592 configurations; the specification does NOT cover the resume option or the Gilbert-Elliott channel); frozen-record guard vs SHA-256 manifest; all on the author's Mac and in Docker. Verified 2026-11-19 on v0.6.0-dev: container 88 OK (2 skipped by design); author's Mac, Python 3.11.7: 88 OK, 0 skipped; Docker (no-cache rebuild): 88 OK, 1 skipped (trace file not in image) in default and full modes; anchor report JSON byte-identical on the Mac. Re-verify after the digest pin.

## Grid design (AUTHOR-APPROVED in chat 2026-11-19, item 1; still unfrozen)
- Exchange grid, full factorial, checked exhaustively (no sampling): p {0.05,0.1,0.2,0.3,0.5} x K {2,3,4,6} x B {4,6,8,12} x L {1..4} x r {0,0.01,0.05,0.1} x persistence x3 x activation x2 = 7,680 configurations. Supports H-E1, H-E2a/b/c, H-E5. p = 0.3 and 0.5 are stress points and are labelled so in every table.
- Composite grid (H-E3, H-E4): H {4,8,20} x policy {expired-only, restart-indeterminate, resume} x detect {1,3,5} on the FULL exchange grid (2.1e5 points; author-approved in chat 2026-11-19; no subset is chosen). Exact-rational checks stay on a small validation grid.
- With the full composite grid the whole 2.1e5 candidate grid is covered; any later extra points are exploratory with no hypothesis attached.
- Sizing note (re-timed in the container 2026-11-19): float about 0.0004 s per random point, at most about 0.002 s at a heavy corner (p=0.5, K=6, B=12, L=4, H=20); EXACT-rational arithmetic about 0.01 s at the same corner. The whole 2.1e5 grid is therefore minutes in float and well under an hour in exact arithmetic on one core, so the confirmatory run can be done in exact rationals and cost is not a reason for any subset.
- Disclosure: development numbers were seen at ONE illustrative point (p=0.3, K=3, B=8, L=3, r=0.1; H=12 or 20; docs/MULTI_ATTEMPT_RULES.md): automatic EXPIRED_OLD retry adds only a few points of success (0.458 to 0.485 volatile/local), and resumable verification raises success from 0.49-0.59 to 0.77-0.95 with a 4-message recovery. They are single-point development values, not grid-wide ranges, and not pre-registered results. The grid was not chosen from them, but the author and tool were not blind to them.

## Real-data anchors (v4; descriptive only, see ANCHORS_REPORT.md)
No open measured TT&C uplink-loss dataset was found. The study is therefore PARAMETRIC, anchored to proxies, each labelled:
- DOWNLINK / observation timing: SatNOGS POP-002 trace from Study 8E (476 scheduled windows, 20 satellite-station pairs, SHA-256 6f80a44f...a8e verified byte-identical on re-materialization). Window duration median 277 s (range 180-771 s). These are scheduled observation windows, not contacts, and say nothing about loss or commanding. First-page records only; not representative. Reuse follows Study 8E's claim boundary: no pooling, no inference to uplink. SatNOGS data is CC BY-SA 4.0: any published derived data needs attribution and share-alike.
- BROADBAND (not TT&C): Starlink ping bursts (Zenodo 14987305, 12 days, 91,580 usable bursts, 10 packets per 10 s). Mean loss 2.16%; 8.79% of bursts lossy; 520 total-loss bursts; P(lossy | previous lossy) 0.137 vs 0.078 after a clean burst; lossy runs mostly 1 burst (max 7). Shows mild persistence at 10 s resolution; cannot resolve packet-level sojourns. 74 blank rows excluded, never counted as loss.
- PUBLISHED RANGES (broadband/downlink, cited from the papers, not re-measured): baseline loss up to about 2% (CosmicDancePro); WetLinks mean ~1% with 22-25% of samples showing loss and maxima above 80%; NPS CubeSat pass-quality counts (547 passes; 179 with no communication). The upper half of the p grid (0.3, 0.5) is a stress range, not an observed one.
- MODELED (not measured): pass durations from circular-orbit geometry, 400-1200 km, 5-20 deg masks: about 4-17 minutes maximum, 3-14 minutes mean. K in {2,3,4,6} is the count of message slots usable for this exchange and is far below geometric capacity; it represents command-window scarcity, which is an assumption.
- Gilbert-Elliott: NOT fitted. Pre-specified matched-stationary rule: good state loses nothing, bad state loses everything, mean bad sojourn m in {2,4} slots, stationary loss equal to the i.i.d. grid value (invalid if a > 1). Chosen before looking at any model output.
- Disclosure: the ping summary statistics were inspected before this rule was written, and the author saw the SatNOGS trace in Study 8E; neither anchor is blind. They bound plausible ranges and are not tuned to any endpoint.
Claims allowed: "parametric study anchored to downlink and broadband proxies and published ranges". Claims not allowed: measured TT&C uplink loss, representative contact statistics, CCSDS conformance, verified cryptography.

## Limitations to state in the paper
Abstract model, not flight software; parameters not fitted to a measured TT&C link (anchors are proxies); i.i.d./two-state loss; same-author TLA+ check (support only); TLA+ jar not compared with a publisher digest; resumable verification and R0/R2 parameters are assumptions; SDLS-DR read from the accepted version.

## Open before freeze
- Author's separate explicit freeze approval (items 1-3 decided in chat 2026-11-19: grid, policy set, GE rule and stress wording, R2 limitation).
- ESA OPS-SAT reply pending; it would add an anchor only if link logs are provided, and would then be a documented amendment, not a silent change.
- AI-use inventory: v2 recorded with the author's stated review (code line by line; text in full); two bracketed confirmations remain. Author declarations: blank checklist supplied; needed at submission, not at freeze.
- Data-deposit decision: DECIDED in chat 2026-11-19 - summaries only (see DATA_DEPOSIT_PLAN_DRAFT_for_author.md): code MIT, documents and result tables CC BY 4.0, SatNOGS-derived summary file as a separate CC BY-SA 4.0 file with attribution; raw SatNOGS and Starlink data not redeposited (hashes and DOI cited). Nothing is published by this decision.

## Freeze-approval checklist (all author-only)
1. Grid design: APPROVED in chat (full-factorial exchange grid + full composite grid); composite on the full exchange grid and the three-policy set (expired-only, restart-indeterminate, resume; resume labelled sensitivity, never the headline) both APPROVED in chat. Items 2-6 open.
2. Gilbert-Elliott rule (matched-stationary, m in {2,4}, labelled a sensitivity probe, not a calibrated channel model) and the wording 'stress points, not observed conditions' for p = 0.3 and 0.5: BOTH APPROVED in chat 2026-11-19.
3. R2 coupling: DECIDED in chat 2026-11-19 - R2 stays an independent mechanism with its own P(desync) endpoint, stated as a limitation; coupling named as future work (possible later pre-registered study). No code change.
4. Mac and Docker reruns on v0.6.0-dev passed (above); Docker digest now pinned: re-run `docker compose build --no-cache` and `make docker-test` once more on the pinned image.
5. Record commit hash and tag; only then may the pre-registered analysis run.
6. Data-deposit decision: DECIDED (above). AI-use statement v2 recorded; author declarations are a submission item.
