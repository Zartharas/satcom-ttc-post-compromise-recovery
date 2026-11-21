# Part I (deterministic T1 cells) vs Part II (exact Study E model): reconciliation at shared points

Scratch copy: /tmp/g3/repo. No existing file was modified (`diff -rq` against /tmp/fresh/repo shows only the new directory `study_e_reconcile/`). Script: `/tmp/g3/repo/study_e_reconcile/reconcile.py`. Row-level results: `/tmp/g3/out/reconciliation.csv` (66 rows).
Part I source: `paper/tables/table-2-deterministic-t1.csv` (40 schedules = 1 control + 31 canonical cells + 8 exhaustion schedules), checked schedule by schedule against the raw Study B JSON (run 20260814T022506Z-gc630fb4, sha256 97e7a543...a87bf): outcome and alignment match for all 40; the 31/8/1 class counts match; max_transmissions = 3, candidate lifetime = 3.

## 1. Method and what the frozen model allows

- The frozen exact DP (`study_e.model.exact_distribution`) takes one i.i.d. loss probability p per transmission. It cannot lose "message m3 only". So deterministic cells are computed two ways, both from frozen code:
  1. Direct DP calls (exact Fractions) where the Part I cell is a p in {0,1}, r in {0,1} point (control, total loss, restart at a boundary): outcome mass is exactly 1.
  2. For "this transmission is lost, all others delivered": the frozen independent simulator `study_e.sim.run_path` driven with one forced Bernoulli outcome per transmission (the generator interface the frozen enumerator uses). The path is one path of the DP.
- Validity checks run in the script: for all 28 configurations used, frozen DP == frozen exhaustive enumerator in exact rationals at p = 1/3; for every forced path, its probability at p = 1/3 is <= the DP mass of the same (outcome, end contact).
- Part I corresponds to `activation = local` (spacecraft activates on COMMIT = m3, ground on CONFIRM = m4; manuscript Sec. 5 and the code agree) and, for restart, to `persist = commit` (Part I restart clears pending candidate and activation receipt; epoch, active key and counters survive).
- Vocabulary map: SUCCESS=SUCCESS; INDETERMINATE=INDETERMINATE; EXPIRED=EXPIRED_OLD; SECURE_DEGRADED (S_AHEAD)=DIVERGED_S_AHEAD. Hazard: Part I's EXPIRED rows carry alignment "G_AHEAD". That is the scenario's initial epoch gap (ground 2, spacecraft 1), NOT "ground activated, spacecraft not". It is not Part II's DIVERGED_G_AHEAD, which never occurs in any Part I cell.
- Shared grid point used as the primary configuration: K=3, B=8, L=3 (inside the Part II grid; L=3 equals Part I lifetime), r=0, commit, local. Off-grid values (B=3,4,5,6 tight, K=1,2,5,6 with L=8, L=1) are allowed by the model but are outside the frozen 7,680-point grid and are labelled "tuned".

## 2. Structural differences that decide the comparison

| Feature | Part I (T1 controller) | Part II (Study E) |
|---|---|---|
| Retry budget | 3 per phase loop (PREPARE/RESPONSE loop and COMMIT/CONFIRM loop separately); total tx not capped (up to 8 seen) | one global budget B over all six messages |
| What is retransmitted | the initiating request (lost RESPONSE -> PREPARE resent; lost CONFIRM -> COMMIT resent) | the lost message itself |
| Verification (TEST_COMMAND, STATUS_TELEMETRY) | single shot, never retried; a drop leaves INDETERMINATE | retried like any message while budget/lifetime remain |
| Contact | unlimited messages per contact; CONTACT_CLOSE costs one lost tx plus one contact | exactly K slots per contact; no close event, only boundaries |
| Restart | scripted fault at COMMIT (spacecraft) or CONFIRM (ground); expiry follows, no re-handshake | random spacecraft-only restart at boundaries (r); after loss of candidate the handshake restarts from m1 if lifetime allows |
| Authentication state | counters, message IDs, stale/replay rejection | none (messages are labels) |
| Delay, duplicate, reorder | explicit faults | do not exist |

## 3. Mapping table (one line per Part I family; 40 schedules)

Class: AGREE = outcomes agree at natural parameters; TUNED = agree only at a parameter chosen to reproduce Part I (and disagree at the grid point); VACUOUS = agreement independent of the fault; NONE = no Part II counterpart.

| Part I schedules (n) | Part II analogue | Part II outcome | Part I outcome | Class | Cause of any disagreement |
|---|---|---|---|---|---|
| DET-000-NO-FAULT (1) | p=0 (frozen DP, mass 1), K=3,B=8,L=3 and K=6,B=6,L=1 | SUCCESS | SUCCESS | AGREE | none |
| DROP PREP/RESP/COMM/CONF (4) | one lost tx of m1..m4, K=3,B=8,L=3 | SUCCESS (7 tx) | SUCCESS (7/8/7/8 tx) | AGREE | outcome agrees; tx counts differ for RESP and CONF (Part I 8, Part II 7). With B=6 Part II ends INDETERMINATE (needs 7 tx): budget artefact, Part I has no global cap |
| DROP TEST, STAT (2) | lost m5 / m6, B=8 | SUCCESS | INDETERMINATE | TUNED | Part II retries verification, Part I does not. Agrees only if B=5 (m5) or B=6 (m6), i.e. no spare transmission |
| CONTACT_CLOSE PREP/RESP (2) | lost m1/m2, contact boundary right after it (needs K=1 / K=2) | SUCCESS if L=8; EXPIRED_OLD (K=1) or INDETERMINATE (K=2) at L=3 | SUCCESS | TUNED | Part II has K slots per contact; Part I contacts are unbounded, so Part II needs many contacts |
| CONTACT_CLOSE COMM/CONF (2) | K=3 / K=4, lost m3/m4 | SUCCESS (L=3 and 8) | SUCCESS | AGREE (at the K that places the boundary; contact count differs: Part II 3 / 2, Part I 2) | boundary placement fixed by K |
| CONTACT_CLOSE TEST, STAT (2) | K=5 / K=6, lost m5/m6 | SUCCESS (L=3, 8); INDETERMINATE only at L=1 | INDETERMINATE | TUNED | verification retry (as DROP TEST/STAT); L=1 contradicts Part I lifetime 3 |
| ENDPOINT_RESTART at COMMIT, spacecraft (1) | p=0, r=1, K=2, L=2, commit or volatile (frozen DP, mass 1) | EXPIRED_OLD | EXPIRED | AGREE | journal persistence gives INDETERMINATE: a Part II design with no Part I analogue |
| ENDPOINT_RESTART at CONFIRM, ground (1) | none: Part II restarts only the spacecraft | (spacecraft volatile restart at step 3, L=2, gives DIVERGED_S_AHEAD; commit/journal give SUCCESS) | SECURE_DEGRADED (S_AHEAD) | NONE | S_AHEAD class is reached in Part II by a different mechanism; not a reconciliation |
| EXHAUST-DROP PREP/RESP/COMM (3) | m1 / m2 / m3 lost three times, B=3/4/5 (= delivered + 3) | EXPIRED_OLD | EXPIRED | TUNED | at B=12 Part II completes SUCCESS (global budget not exhausted); Part I's per-phase cap of 3 is exhausted regardless |
| EXHAUST-DROP CONF (1) | m4 lost three times, B=6, local | DIVERGED_S_AHEAD | SECURE_DEGRADED (S_AHEAD) | TUNED | B=12: SUCCESS; gated activation: EXPIRED_OLD (spacecraft not active at step 3) |
| EXHAUST-CLOSE PREP/RESP/COMM/CONF (4) | K=1, L=3 (only K that closes after every lost tx) | EXPIRED_OLD x3, DIVERGED_S_AHEAD | EXPIRED x3, SECURE_DEGRADED | VACUOUS | the same outcomes occur at p=0, K=1, L=3 (row EC0): lifetime, not loss, decides |
| DELAY (6), DUPLICATE (4), REORDER (4), STALE_COUNTER (1), STALE_REPLAY (2) = 17 | none; only p=0 SUCCESS consistency | SUCCESS | SUCCESS | NONE | Part II has no delay, duplicates, reordering, counters or replay rejection |

Totals over the 40 schedules: AGREE 6 (control, four DROP of m1..m4, RESTART at COMMIT) plus CLOSE COMM/CONF 2 at tuned boundary placement = 8; TUNED 10 (DROP TEST/STAT 2, CLOSE PREP/RESP 2, CLOSE TEST/STAT 2, EXHAUST-DROP 4); VACUOUS 4; NONE 18 (17 + ground restart). 8 + 10 + 4 + 18 = 40.

## 4. Agreements, disagreements, causes

Agree (natural parameters): p=0 SUCCESS; one lost message among m1..m4 with a spare retry -> SUCCESS; spacecraft loses its pending candidate before COMMIT -> EXPIRED/EXPIRED_OLD (p=0, r=1, one boundary, commit or volatile persistence). Outcome vocabulary maps one-to-one for these four classes.

Disagree or agree only when tuned:
1. Verification retry: Part II retries m5/m6; Part I does not. This is the largest real difference: Part I's INDETERMINATE after a single drop is a design choice (no retry), Part II's INDETERMINATE arises from budget or lifetime ending at step 4 or 5.
2. Budget semantics: per-phase cap 3 (Part I) versus global B (Part II), and retransmission of the request versus of the lost message (tx counts 8 vs 7). "Retry budget 3" has no direct Part II value.
3. Contact structure: unbounded versus K slots; close is a loss plus boundary in Part I, only a boundary at fixed K in Part II.
4. Activation: Part I is local; under gated activation the S_AHEAD cells become EXPIRED_OLD in Part II.
5. Restart: Part I restarts ground or spacecraft once by script; Part II restarts only the spacecraft at random boundaries, and re-handshakes after candidate loss. Ground-restart at CONFIRM (S_AHEAD) cannot be produced.
6. Not comparable at all: reorder, duplicate, delay, stale counter and replay.

## 5. Suggested manuscript paragraph (Part II, at most 150 words)

> Relation to Part I. At the points the two models share, Part II's exact outcomes agree with Part I only partly. With p = 0 both give SUCCESS. One lost message among the four recovery messages, with a spare retry, gives SUCCESS in both, and a spacecraft restart that discards the pending candidate before COMMIT (commit-level persistence, r = 1) gives EXPIRED in both. Other matches need parameters chosen to reproduce Part I: Part II retries lost verification messages and Part I does not, Part II caps transmissions globally and Part I per phase, and Part I contacts hold unlimited messages. Delay, duplicate, reorder, stale-counter, stale-replay and ground-restart cells have no Part II counterpart. The comparison checks shared definitions and outcome vocabulary, not equivalence, and no quantitative result is transferred between the parts.

(about 135 words)

## 6. Devil's advocate: is this reconciliation meaningful or circular?

Largely circular where it agrees, informative where it does not. Part II's six-message chain, its local activation at m3 and ground activation at m4, and its outcome classes were written as an abstraction of Part I, by the same author, so SUCCESS at p=0, SUCCESS after one retried loss and EXPIRED after exhaustion follow from any sequential retry protocol and test little. The informative-looking matches (INDETERMINATE after a lost verification message, EXPIRED and S_AHEAD after exhaustion) appear only after I set B or L to the value that reproduces Part I, and the outcome is then just the step reached, which my parameter choice fixed; at the grid point they disagree. The forced-loss runs use the frozen simulator, which re-implements the same rules as the DP (independent code, same author and same rule table), so they confirm internal consistency of Part II, not the match to Part I. Part I was not re-run with Part II-derived parameters, so nothing here shows Part I's code obeys Part II's rules in cells beyond its 40 scripted schedules. What the exercise does deliver is an honest boundary map: it exposes real semantic differences (verification retry, budget scope, ground restart, contact capacity) and the label hazard around G_AHEAD, which the reviewer's point about "a shared name" correctly anticipates. It is documentation of overlap, not validation. A genuine validation would need a Part I variant with a global budget and retried verification, run against Part II's exact distribution at deterministic points; that was out of scope and is not claimed.
