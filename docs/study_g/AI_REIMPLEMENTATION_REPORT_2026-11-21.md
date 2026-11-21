# Independent re-implementation report (Part I T1 exchange, Study B 31 cells / 40 schedules, Part II sample)

## 0. What this is and is not
The implementer is an AI agent (Claude), not an independent human party. It worked alone from the written specification
(manuscript.txt, spec/*.json, docs/*.md, paper/manuscript/*.md, docs/study_e preregistration, S1 columns 1-4), then froze code, outputs and
IMPLEMENTATION_LOG.md (sha256 in /tmp/g2/FREEZE.sha256, verified unchanged after comparison) before opening any reference result.
It is NOT blind: the allowed manuscript prose already states the Study B aggregate and the restart/exhaustion outcomes, and one grep
accidentally printed 12 rows of the published table (log C-1, C-2). Agreement on the restart, exhaustion and verification-loss cells is therefore weak
evidence. The cells the prose did not state (DUPLICATE, REORDER, STALE_*, DELAY, rejection counters) are the more informative checks.
Reference data read only after freezing: paper/tables/table-2-deterministic-t1.csv, study-b-fault-response-summary.csv, the raw
paper-final run 20260814T022506Z-gc630fb4/raw/study-b-deterministic-t1.json (via device_bash, read-only), confirmatory_results.json,
and (post-freeze, for diagnosis only) study_e/study_e/{rules,model,multi}.py.
Files: reimpl/{t1_model,run_study_b,study_e_model,run_study_e}.py, out/reimpl_*.{json,csv}, compare_*.py, diag_variant.py (post-freeze diagnostic only).

## 1. Spec ambiguity (Part I)
IMPLEMENTATION_LOG.md lists 15 Part I assumptions A-01..A-15 (and 9 Part II ones). Material ones for Study B: Study B parameters (initial epochs 2/1,
floor 0, budget 3, lifetime 3) are not stated for Study B itself; delay length; contact-counter rules; who retries RESPONSE/CONFIRM; restart semantics;
rejection-counter attribution; STATUS after lost TEST. Ambiguity that changed an outcome: none found. Ambiguity that changed a secondary field: 5 items (below).
Some Part I rules were fully determinate from the spec (epoch negotiation, activation rules, single-opportunity verification, 3 retries, outcome enum).

## 2. Study B agreement (40 schedules; 31 canonical cells)
| field | all 40 | canonical 31 |
|---|---|---|
| outcome | 40/40 | 31/31 |
| alignment (SYNC(3)/G_AHEAD/S_AHEAD) | 40/40 | 31/31 |
| security_state | 40/40 | 31/31 |
| availability_state | 40/40 | 31/31 |
| verification_complete | 40/40 | 31/31 |
| all five together | 40/40 | 31/31 |
| rejection triple (rejection/replay/stale-state) | 32/40 | 23/31 |
| recovery_duration_contacts (raw JSON; mine = contacts+1) | 40/40 | |
| total_transmissions (raw JSON) | 37/40 | |
Schedule set (IDs, class, kind, phase) generated from the manuscript rule equals the 40 published IDs. The raw JSON matches table-2 on every
field I compared (outcome, alignment, security, availability, verification, rejection triple).
Aggregates reproduced: canonical 25 SUCCESS / 4 INDETERMINATE / 1 EXPIRED / 1 SECURE_DEGRADED; exhaustion 6 EXPIRED / 2 SECURE_DEGRADED (but see C-1).

### Disagreements (all secondary fields; none affects outcome, alignment, security, availability or verification)
1. DET-CELL-DUP-{PREP,RESP,COMM,CONF}: rejection triple mine 1/0/0, ref 1/1/0. Classification: spec ambiguity plus my reading error. The reference
   counts a duplicate-message-id rejection as replay-attributed; spec guard G-003 is literally named "replay_identifier_unused", so the reference reading is
   defensible, while the data dictionary only says "replay-attributed rejections". Event log: reason "duplicate message identifier".
2. DET-CELL-SRPL-{COMM,CONF}: mine 1/1/0, ref 1/0/1. Spec ambiguity. The manuscript's CF-06 (Study A) reports replay_rejection=1 for a stale replay, but in
   Study B the reference books the replayed message as stale-state ("commit conflicts with activation receipt"), not replay. Nothing in the spec says which counter.
   Also an ordering difference: the reference delivers the replay after the legitimate message is processed; I injected it before. No outcome effect.
3. DET-CELL-RST-COMM: mine 3/0/0 and 5 transmissions, ref 1/0/1 and 3 transmissions. Implementation difference (my A-08). In the reference the ground
   abandons the attempt after the first "no exact pending candidate" rejection (event t1_attempt_expired_without_activation); I retried COMMIT to budget.
   The spec says exhaustion before activation yields EXPIRED but does not say whether a rejection stops retries. Outcome unaffected; the reference behavior is
   arguably more consistent with "restart destroyed pending state" but is not derivable from the spec. Also the reference tags this rejection stale-state.
4. DET-CELL-RST-CONF: mine 1/0/0, ref 1/0/1. Same stale-state attribution (spec ambiguity).
5. DET-CELL-DROP-TEST and DET-CELL-CLOSE-TEST: transmissions mine 5, ref 6. Implementation difference (my A-05): I skip the STATUS opportunity after TEST is lost;
   the reference still counts it. Outcome unaffected (both INDETERMINATE).
No bug found on either side. Not checked: Study B fields beyond those listed (retry_overhead, divergent/degraded windows, event-log order).

## 3. Part II sample (Study E)
Spec adequacy: low. The preregistration gives hypotheses and the grid but not the restart/persistence rules, so those were my inventions (E-01..E-09).
Two spec hints (six-message chain; "P(S-ahead) = P(exactly 3 successes)") fixed the chain structure, activation steps (local after COMMIT, gated after TEST) and
classification; the reference rules.py confirms my chain, budget, lifetime, activation and classify rules. I did not implement R0/RECOVERED/UNRECOVERED, expected
attempts/contacts, R2 or Gilbert-Elliott (E-07/E-08): not derivable from the allowed text (R0 values n_msgs=4, B0=8, L0=3 appear only in the reference).
I computed exact rational outcome masses at 54 points (36 mixed-factor + 18 at p=0.3,K=3,B=8,L=3,r=0.1,H=20; covers all p, r, persistence, H, both activations, 3 policies).
confirmatory_results.json holds hypothesis summaries, not per-point masses, so my 54 points cannot be compared one by one. What can be checked against it:
| check | mine (frozen) | reference |
|---|---|---|
| exact rational witness entries quoted in the JSON (20 entries, both values must match) | 10/20 (E2b 5/5, E2c 5/5, K 0/5, p 0/5) | variant: 15/15 tested (K, p, E2b; E2c not rerun) |
| SUCCESS monotone in B (viol/pairs) | 0/5760 | 0/5760 |
| SUCCESS monotone in L | 0/5760 | 0/5760 |
| SUCCESS vs K violations | 32 | 31 |
| SUCCESS vs p violations (non-increasing) | 0 | 22 |
| journal distribution invariant to r | 0 violations/1920 | 0/1920 |
| volatile divergence non-decreasing in r, violations | 627 | 447 |
| H-E2b gated P(G-ahead) ordering, violations | 628 | 288 |
| divergence rises with B (pairs) | 587 | 568 |
| H-E3 points with INDETERMINATE mass (H=20) | 5520 | 5520 |
| H-E3 primary dS<IND holds | 5502/5520 | 5520/5520 |
| resume gain > dS, over IND points / all points | 5502 / 5502 | 5520 / 5520 |
| qualitative verdicts | same on B, L, journal-invariance, E2b (fails), E2c volatile (fails), K (fails); differs on p (mine holds, ref fails) and H-E3 (18 counterexamples vs none) | |
Note: the reference's H-E2a p row has 22 violations (a restart artifact), mine has 0.
Disagreement cause (diagnosed after reading rules.py; post-freeze, not independent): two restart rules. (i) For commit persistence I kept all progress from step 3 on, the
reference keeps only the spacecraft's activation (step>=3 local, >=5 gated). (ii) For a restart with ground already activated and spacecraft state lost, the reference
ends the attempt as DIVERGED_G_AHEAD; I reset to step 0. A diagnostic variant implementing exactly these two rules (diag_variant.py) reproduces 15/15 exact witness
values and the counts 31, 22, 288, 447, 568 exactly. Classification: spec ambiguity (preregistration silent on restart effect; it only hints "volatile fallback-required").
Anchor point p=0.3,K=3,B=8,L=3,r=0.1: preregistration dev values volatile/local expired-only 0.458 -> 0.485 and resume 0.77-0.95; mine (frozen) 0.516 expired-only and
0.82-0.95 resume. Consistent with the restart-rule difference; not verified against the variant at H=20.
The E2b and E2c witnesses lie in regions where both rule sets coincide, which is why they matched.

## 4. Honest summary
Part I: five key output fields 40/40 (31/31 canonical), subject to the contamination caveat; rejection-counter attribution 32/40 and transmissions 37/40 disagree for spec-ambiguity or
implementation-difference reasons, not bugs. Part II: structural model recovered from two hints; restart semantics not recoverable from the written spec, so aggregate counts
disagree until the two rules above are supplied. Caveat: one implementer, same model family as the code's likely authoring assistant, not blind; this supports "the prose
spec determines Study B outcomes" but is not independent replication by a human.
