# Study G results (EXPLORATORY, post hoc, same-author, AI-implemented, not pre-registered with a third party)

Protocol: docs/study_g/STUDY_G_PROTOCOL.md (body SHA-256 74d6d7683fded82bf794ead5fdb08d5216141aba135801f280bd74c9a1303606; grid SHA-256 757b768a97864e0edc0f453c64cb9bb54aaedf7361b402048998def61c2cb26e). Run once, 86 cells, all reported; results CSV SHA-256 fe7e36e8388e9b1b5fc8169b3601545b9dabdb3192337793fc475f2f51833b00 (identical on a second run). Descriptive counts of cells in a designed grid; no statistics, no pooling with Part I or Study F, no superiority claim. Study F rows are read from study_f_out/mac/study_f_results.csv. T1-to-baseline step pairing is an analogy by role (protocol role map), not an equivalence.

## Headline
- Giving T1's TEST_COMMAND and STATUS_TELEMETRY steps a budget of 3 turns the four Part I canonical INDETERMINATE cells (one lost transmission per step and kind) into SUCCESS, and also the four cells with two losses. With three losses all four cells stay INDETERMINATE. T1 INDETERMINATE count over the 43-cell grid: 12 (budget 1) to 4 (budget 3); SUCCESS 21 to 29. The "converged is not verified" outcome for a single or double lost verification step is therefore a consequence of the one-attempt design, as the reviewer suggested. What survives is that exhaustion of the verification budget still yields a converged-but-unverified state, which T1 labels INDETERMINATE and which B2 at budget 3 (3 lost telemetry) also labels INDETERMINATE.
- Recovery-step, REORDER and ENDPOINT_RESTART rows are identical between budgets (P4), so the wrapper changed only the verification cells.
- At equal retransmission budget (3), the SUCCESS versus not-SUCCESS split for 1, 2 and 3 lost transmissions agrees between T1 and every role-mapped Study F baseline row (P6, zero mismatches).

## Outcome counts (cells; descriptive only)

| arm | DIVERGED | EXPIRED | INDETERMINATE | LOCKED | SECURE_DEGRADED | SUCCESS | cells |
|---|---|---|---|---|---|---|---|
| T1_V1 | 0 | 7 | 12 | 0 | 3 | 21 | 43 |
| T1_V3 | 0 | 7 | 4 | 0 | 3 | 29 | 43 |
| Study F baselines, budget 1 | 19 | 21 | 6 | 7 | 0 | 5 | 58 |
| Study F baselines, budget 3 | 7 | 9 | 2 | 3 | 0 | 37 | 58 |

## Per-cell comparison

| T1 step | fault | lost | T1 budget 1 (Part I) | T1 budget 3 (Study G) | baselines, budget 1 (Study F) | baselines, budget 3 (Study F) |
|---|---|---|---|---|---|---|
| - | CONTROL | 0 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B0,B1L,B1D,B2: SUCCESS | B0,B1L,B1D,B2: SUCCESS |
| RECOVERY_PREPARE | DROP = CONTACT_CLOSE | 1 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED | B0:SUCCESS; B1L:SUCCESS; B1D:SUCCESS; B2:SUCCESS |
| RECOVERY_PREPARE | DROP = CONTACT_CLOSE | 2 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED | B0:SUCCESS; B1L:SUCCESS; B1D:SUCCESS; B2:SUCCESS |
| RECOVERY_PREPARE | DROP = CONTACT_CLOSE | 3 | EXPIRED G_AHEAD | EXPIRED G_AHEAD | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED |
| RECOVERY_RESPONSE | DROP = CONTACT_CLOSE | 1 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED | B0:SUCCESS; B1L:SUCCESS; B1D:SUCCESS; B2:SUCCESS |
| RECOVERY_RESPONSE | DROP = CONTACT_CLOSE | 2 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED | B0:SUCCESS; B1L:SUCCESS; B1D:SUCCESS; B2:SUCCESS |
| RECOVERY_RESPONSE | DROP = CONTACT_CLOSE | 3 | EXPIRED G_AHEAD | EXPIRED G_AHEAD | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED | B0:DIVERGED; B1L:EXPIRED; B1D:EXPIRED; B2:LOCKED |
| RECOVERY_COMMIT | DROP = CONTACT_CLOSE | 1 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B1L:DIVERGED; B1D:EXPIRED | B1L:SUCCESS; B1D:SUCCESS |
| RECOVERY_COMMIT | DROP = CONTACT_CLOSE | 2 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B1L:DIVERGED; B1D:EXPIRED | B1L:SUCCESS; B1D:SUCCESS |
| RECOVERY_COMMIT | DROP = CONTACT_CLOSE | 3 | EXPIRED G_AHEAD | EXPIRED G_AHEAD | B1L:DIVERGED; B1D:EXPIRED | B1L:DIVERGED; B1D:EXPIRED |
| RECOVERY_CONFIRM | DROP = CONTACT_CLOSE | 1 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B1L:DIVERGED; B1D:EXPIRED | B1L:SUCCESS; B1D:SUCCESS |
| RECOVERY_CONFIRM | DROP = CONTACT_CLOSE | 2 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B1L:DIVERGED; B1D:EXPIRED | B1L:SUCCESS; B1D:SUCCESS |
| RECOVERY_CONFIRM | DROP = CONTACT_CLOSE | 3 | SECURE_DEGRADED S_AHEAD | SECURE_DEGRADED S_AHEAD | B1L:DIVERGED; B1D:EXPIRED | B1L:DIVERGED; B1D:EXPIRED |
| TEST_COMMAND | DROP = CONTACT_CLOSE | 1 | INDETERMINATE SYNC(3) | SUCCESS SYNC(3) | B1D:DIVERGED; B2:INDETERMINATE | B1D:SUCCESS; B2:SUCCESS |
| TEST_COMMAND | DROP = CONTACT_CLOSE | 2 | INDETERMINATE SYNC(3) | SUCCESS SYNC(3) | B1D:DIVERGED; B2:INDETERMINATE | B1D:SUCCESS; B2:SUCCESS |
| TEST_COMMAND | DROP = CONTACT_CLOSE | 3 | INDETERMINATE SYNC(3) | INDETERMINATE SYNC(3) | B1D:DIVERGED; B2:INDETERMINATE | B1D:DIVERGED; B2:INDETERMINATE |
| STATUS_TELEMETRY | DROP = CONTACT_CLOSE | 1 | INDETERMINATE SYNC(3) | SUCCESS SYNC(3) | B1D:DIVERGED; B2:INDETERMINATE | B1D:SUCCESS; B2:SUCCESS |
| STATUS_TELEMETRY | DROP = CONTACT_CLOSE | 2 | INDETERMINATE SYNC(3) | SUCCESS SYNC(3) | B1D:DIVERGED; B2:INDETERMINATE | B1D:SUCCESS; B2:SUCCESS |
| STATUS_TELEMETRY | DROP = CONTACT_CLOSE | 3 | INDETERMINATE SYNC(3) | INDETERMINATE SYNC(3) | B1D:DIVERGED; B2:INDETERMINATE | B1D:DIVERGED; B2:INDETERMINATE |
| RECOVERY_PREPARE | REORDER | 0 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B1L:EXPIRED; B1D:EXPIRED | B1L:EXPIRED; B1D:EXPIRED |
| RECOVERY_RESPONSE | REORDER | 0 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | B1L:EXPIRED; B1D:EXPIRED | B1L:EXPIRED; B1D:EXPIRED |
| RECOVERY_COMMIT | REORDER | 0 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | n/a | n/a |
| RECOVERY_CONFIRM | REORDER | 0 | SUCCESS SYNC(3) | SUCCESS SYNC(3) | n/a | n/a |
| RECOVERY_COMMIT | ENDPOINT_RESTART | 0 | EXPIRED G_AHEAD | EXPIRED G_AHEAD | B1L:DIVERGED; B1D:EXPIRED | B1L:DIVERGED; B1D:EXPIRED |
| RECOVERY_CONFIRM | ENDPOINT_RESTART | 0 | SECURE_DEGRADED S_AHEAD | SECURE_DEGRADED S_AHEAD | B1L:DIVERGED; B1D:EXPIRED | B1L:DIVERGED; B1D:EXPIRED |

DROP and CONTACT_CLOSE gave identical T1 outcome and alignment in every cell: True.

## Protocol predictions (computed by study_g/compare.py)

| prediction | holds |
|---|---|
| P1 budget 3 absorbs 1 or 2 losses at verification steps (8 cells) | True |
| P2 3 losses at verification steps stay INDETERMINATE and match B2 c3 R3 | True |
| P3 budget 1 reproduces Part I (12 INDETERMINATE) | True |
| P4 recovery-step, REORDER and RESTART rows identical across budgets | True |
| P5 recovery-step outcomes as predicted (SUCCESS at 1-2 lost; EXPIRED/SECURE_DEGRADED at 3; restart cells) | True |
| P6 SUCCESS/not-SUCCESS partition agrees with every mapped budget-3 baseline row (mismatches: 0) | True |
| P8 exposure pattern (INDETERMINATE not exposed; other non-SUCCESS exposed) | False |

P6 mismatches: []

P7 label-only differences between T1 budget 3 and mapped budget-3 baseline rows (count 18):

- RECOVERY_COMMIT, lost 3: T1 EXPIRED G_AHEAD; baselines B1_LOCAL=DIVERGED G_AHEAD
- RECOVERY_CONFIRM, lost 3: T1 SECURE_DEGRADED S_AHEAD; baselines B1_DEFERRED=EXPIRED G_AHEAD, B1_LOCAL=DIVERGED G_AHEAD
- RECOVERY_PREPARE, lost 3: T1 EXPIRED G_AHEAD; baselines B0=DIVERGED G_AHEAD, B2=LOCKED G_AHEAD
- RECOVERY_RESPONSE, lost 3: T1 EXPIRED G_AHEAD; baselines B0=DIVERGED G_AHEAD, B2=LOCKED G_AHEAD
- STATUS_TELEMETRY, lost 3: T1 INDETERMINATE SYNC(3); baselines B1_DEFERRED=DIVERGED S_AHEAD
- TEST_COMMAND, lost 3: T1 INDETERMINATE SYNC(3); baselines B1_DEFERRED=DIVERGED S_AHEAD

Baseline exposure re-execution reproduced Study F outcome and alignment on all rows: True.

Baseline INDETERMINATE cells and (spacecraft, ground) on compromised key: [(False, False)]


## Exposure at end: endpoints still on the attacker-known key (non-SUCCESS cells)

| arm | outcome | cells | spacecraft on compromised key | ground on compromised key |
|---|---|---|---|---|
| T1_V1 | EXPIRED | 7 | 7 | 7 |
| T1_V1 | INDETERMINATE | 12 | 0 | 0 |
| T1_V1 | SECURE_DEGRADED | 3 | 0 | 3 |
| T1_V3 | EXPIRED | 7 | 7 | 7 |
| T1_V3 | INDETERMINATE | 4 | 0 | 0 |
| T1_V3 | SECURE_DEGRADED | 3 | 0 | 3 |
| Study F budget 1 | DIVERGED | 19 | 13 | 12 |
| Study F budget 1 | EXPIRED | 21 | 21 | 21 |
| Study F budget 1 | INDETERMINATE | 6 | 0 | 0 |
| Study F budget 1 | LOCKED | 7 | 6 | 0 |
| Study F budget 3 | DIVERGED | 7 | 5 | 4 |
| Study F budget 3 | EXPIRED | 9 | 9 | 9 |
| Study F budget 3 | INDETERMINATE | 2 | 0 | 0 |
| Study F budget 3 | LOCKED | 3 | 2 | 0 |

## What remains distinguishing (and what does not)
Does not distinguish, in this grid: the success/not-success partition under loss at equal budget (P6: zero mismatches over all mapped pairs, 1 to 3 lost, both loss kinds). Loss-recovery by retransmission is shared; T1 is not shown to be better at absorbing loss. The Part I statement that T1 leaves a lost status "indeterminate by rule" is, with a budget of 3, true only after three consecutive losses, and B2 at budget 3 behaves the same (INDETERMINATE, synchronized).

Still different, stated as observed and with the caveats that apply:
1. Outcome vocabulary. After budget exhaustion T1 reports labels the baselines do not have for the same situation: SECURE_DEGRADED, S_AHEAD (spacecraft activated, ground unconfirmed; three lost CONFIRM and restart at CONFIRM) versus DIVERGED or EXPIRED in B1; EXPIRED with prior state preserved versus LOCKED in B2 at three lost RATCHET_UPDATE; INDETERMINATE (converged, unverified) versus DIVERGED S_AHEAD in B1_DEFERRED at three lost status. These are 18 label-only differences across the mapped pairs (P7, listed above). B2 already has INDETERMINATE. Because the vocabulary is the contribution, this is "B0/B2 plus retransmission plus the outcome vocabulary" and nothing more in the loss grid.
2. REORDER (not covered by P6, and contrary to the protocol's overall expectation that nothing differs in the success partition). T1 ends SUCCESS in all four REORDER cells, while the mapped B1 rows (KEM_INIT_RESPONSE REORDER, both policies) end EXPIRED at budgets 1 and 3. Caveat that limits this: in Part I a REORDER fault injects a forged wrong-kind message in addition to the real one, and T1 rejects it; Study F's B1 REORDER is a frozen-abstraction event that expires the attempt. The two are not the same fault, so this is a difference between how the fault is defined in each model, not shown to be a property of the protocols. B0 and B2 have no REORDER semantics in Study F.
3. Restart (equal partition, different label): T1 ENDPOINT_RESTART at COMMIT ends EXPIRED G_AHEAD and at CONFIRM ends SECURE_DEGRADED S_AHEAD; B1_LOCAL ends DIVERGED G_AHEAD in both budgets and B1_DEFERRED ends EXPIRED. All not-SUCCESS everywhere; retransmission does not help in any arm (as in Part I Section 7.2).
4. Verification as a separate required step. In the frozen B0 and B1_LOCAL abstractions delivery of the update scores as verification complete (no separate post-update step exists to lose), so no loss cell can ever make B0 or B1_LOCAL INDETERMINATE. T1 and B2 (and B1_DEFERRED via authenticated status) have such a step. This is a design property of what each abstraction scores, not an outcome from a fault.
5. Exposure at end (cheap metric; protocol P8). T1 INDETERMINATE cells have both endpoints rotated off the attacker-known key (0 of 12 and 0 of 4 exposed), as do baseline INDETERMINATE cells (B2, 0 of 6 and 0 of 2). T1 EXPIRED cells leave both endpoints on the compromised key (7 of 7); T1 SECURE_DEGRADED leaves the ground on it (3 of 3) and the spacecraft rotated. Baseline non-success cells are also mostly exposed (see exposure table). Exposure therefore tracks the terminal state, not the retransmission design. P8 as written did not hold for baselines: the two B2 STALE_GROUND_RESTORE LOCKED S_AHEAD cells (native fault, outside the mapped grid) have no endpoint on a compromised key. The T1 half of P8 held.

Net, honestly stated: at budget 3 the grid shows no T1 advantage in whether recovery succeeds under loss. The residual differences are labels (items 1 and 3), a fault-definition difference on REORDER (item 2), and the presence of an explicit verification step (item 4). If the manuscript keeps "converged is not verified recovery", the supportable form is that a recovery protocol that requires post-convergence evidence can end converged-but-unverified (INDETERMINATE) when that evidence cannot be obtained within the budget, not that single or double losses cause it.

## Limits
Single initial state (T1_BASE). One simulator; loss is deterministic and consecutive; contact-closure treated as equal to drop (A-seq) except that T1's CONTACT_CLOSE also advances the contact clock (outcomes were identical to DROP in all cells). Verification retransmission is assumed idempotent and safe (A-retx-T1). The two arms keep recovery-message budget 3 in both, while Study F budget 1 baselines have no retransmission anywhere, so T1 budget 1 versus baseline budget 1 is not a matched comparison; only budget 3 versus budget 3 is. Not tested: DELAY, DUPLICATE, STALE_COUNTER, STALE_REPLAY, B2 native faults, timing, retry cost.
