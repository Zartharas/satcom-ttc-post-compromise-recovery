# Study E model assumptions and source status (v0.1, DEVELOPMENT; not frozen)

Source status key: CITED = read in a fetched primary/secondary source (section noted; re-verify against the full document before freeze); ASSUMPTION = modelling choice, not from a source; OPEN = not yet implemented/decided.

| # | Item | Status | Source / note |
|---|------|--------|---------------|
| A1 | Six-message exchange m1..m6 (PREPARE, RESPONSE, COMMIT, CONFIRM, TEST_COMMAND, STATUS_TELEMETRY) | ASSUMPTION | Project-defined T1/B1 abstraction from the frozen study; not an SDLS-EP message set. |
| A2 | Per-end activation is a single state transition (Pre-Active to Active); Initiator activates before signalling, Recipient on receipt, no acknowledgement in the procedure | CITED (read in full text) | CCSDS 355.1-B-1, 3.2.3.2 and CCSDS 354.0-M-1, 4.3.1 (spacecraft = Recipient). The earlier 350.11-G-1 atomicity citation is NOT verified and is withdrawn. |
| A3 | Spacecraft-ahead / ground-ahead divergence are the activation-window failures | ASSUMPTION | local: S active after m3, G after m4; gated: S after m5. Mirrors frozen Study B classes. |
| A4 | Verification as a separate challenge-response procedure after activation | CITED (read in full text) | 355.1-B-1, 3.2.3.5 (five steps). Message count and mapping to m5/m6 remain a project abstraction. |
| A5 | Existing resynchronisation aids: Set ARSN / Read ARSN commands and Key Inventory (and Key Verification) | CITED (table of contents and 3.2.3.5-3.2.3.6 of CCSDS 355.1-B-1 read; PDU names for ARSN in its list of PDUs) | They need a working SA; the paper must NOT claim no resynchronisation mechanism exists. The earlier 350.11-G-1 citation and the 'SA Status Request' item are unverified and withdrawn. |
| A6 | Recovery SA: last-resort SA, keys not erasable/reloadable/revocable | CITED (read in full text) | CCSDS 350.5-G-2, 3.5.1.2 and 4.5.6 (not 350.11-G-1). Implemented as R0 in recovery.py with MODEL-PARAMETER message count and detection delay. |
| A7 | A divergence terminal = "needs fallback (Recovery SA/operator)", not necessarily permanent lockout | ASSUMPTION | Terminology: use "divergence requiring fallback" unless the Recovery SA is absent or compromised. |
| A8 | Static-state recovery versus post-compromise security trade-off | CITED | eprint 2024/1886, Sec. 3.5 / 4.4: a resilient protocol cannot achieve conversation PCS against full compromise (static + dynamic state). Informs R0 framing; messaging model, so transfer to SDLS is an argument, not a theorem. |
| A9 | Ratchet recovery = re-bootstrap via a recovery association after sustained authentication failure; no injected-loss/restart evaluation | CITED (partly inferred) | SDLS-DR paper, Sec. V.I, VIII; "no experiments for injected loss/restart" is the reader's inference from the text. |
| A10 | Per-message loss i.i.d. with probability p (default), or Gilbert-Elliott 2-state channel (params.ge); one transmission per slot; K slots per contact | ASSUMPTION | GE state evolves per slot and is redrawn from the stationary law at each contact start (contacts are separated in time). Parameters are not fitted to any real link; real-link burst statistics are OPEN. Mutation tests for the GE transitions and state losses exist (tests/test_bursty.py). |
| A11 | Spacecraft restarts only at contact boundaries with probability r; ground never restarts | ASSUMPTION | |
| A12 | Persistence levels: volatile / commit / journal (see rules.py) | ASSUMPTION | Mapping to real flight software is OPEN (needs F1-F4 evidence). |
| A13 | Attempt = budget B transmissions, lifetime L contacts; multi-attempt run over horizon H with automatic retry of EXPIRED_OLD only (docs/MULTI_ATTEMPT_RULES.md) | ASSUMPTION | v0.3.0-dev. INDETERMINATE retry is a sensitivity setting, not a protocol claim. Horizon H=20 of prereg v1 is representable (H is a parameter). |
| A14 | R2 bounded skipped-key cache desynchronisation (ratchet.py) and R0 Recovery-SA re-bootstrap (recovery.py) | IMPLEMENTED v0.3.1-dev, parameters ASSUMED | Sources and what is/is not specified: docs/R0_R2_SOURCES.md. R2 models frame-level desynchronisation only (not the cryptography). R0 and R2 are not yet connected to the exchange model. |
| A15 | TLA+/TLC reachability (support) cross-check against the Python model | DONE for single- and multi-attempt, i.i.d. loss | tla/; 432 and 2,592 configurations, 0 mismatches; a seeded mutant is detected. Jar: TLA+ Tools v1.7.4 downloaded by the author from the official releases page; SHA-256 936a2620...0e88 NOT compared to a publisher digest. Same-author spec: limited independence. Bursty loss not covered (support equals the i.i.d. support when all loss probabilities are in (0,1)). |

## Corrections to earlier statements (recorded for honesty)
1. Hypothesis H-E2a said lockout probability falls with the retry budget. With loss only it does NOT fall monotonically: P(S-ahead divergence) = P(exactly 3 successes in B transmissions), which rises with B at small B (see tests/test_properties.py). The hypothesis must be reworded before freeze.
2. The planned property "lockout never rises with budget" was wrong for the same reason and is replaced by a documented non-monotonicity witness test.
3. "No in-band resync procedure exists" is too strong; EP offers ARSN read/set, status and inventory commands, which require a working SA.

4. A bursty channel does not necessarily lower success: with equal stationary loss 1/2, K=3, B=6, L=2, success is 0.164 for long bursts vs 0.0156 memoryless, because long good bursts help complete a 6-message run. Do not claim burstiness is harmful without the grid result.

5. Retry only helps when the failure is EXPIRED_OLD. In the development grid the dominant failure is INDETERMINATE and divergence, so the earlier intuition that more retries fix most failures is not supported by the model.
6. Option (b) resumable verification is a design assumption outside the cited standards; it is reported only as an upper-bound sensitivity.
7. Candidate grid size and runtime: tools/size_grid.py (about 2.1e5 points, float arithmetic cheap); the pre-registered grid itself is not fixed.
