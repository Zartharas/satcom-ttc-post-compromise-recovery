# Supplementary Tables S2-S7 (S2-S6 derived read-only from frozen Part I inputs; S7 from the Study F run)

**Supplementary Table S2. Study D challenge set: fault structure of the 12 designed schedules.**

| Schedule | Faults | Same-phase consecutive faults | Transmissions needed for that phase |
|---|---|---|---|
| SENS-00-NO-FAULT | none | 0 | 1 |
| SENS-01-PREP-DROP-1 | DROP PREPARE (attempt 1, 1 contact(s)) | 1 | 2 |
| SENS-02-PREP-DROP-1-2 | DROP PREPARE (attempt 1, 1 contact(s)); DROP PREPARE (attempt 2, 1 contact(s)) | 2 | 3 |
| SENS-03-RESP-DROP-1-2 | DROP RESPONSE (attempt 1, 1 contact(s)); DROP RESPONSE (attempt 2, 1 contact(s)) | 2 | 3 |
| SENS-04-COMMIT-DROP-1-2 | DROP COMMIT (attempt 1, 1 contact(s)); DROP COMMIT (attempt 2, 1 contact(s)) | 2 | 3 |
| SENS-05-CONFIRM-DROP-1-2 | DROP CONFIRM (attempt 1, 1 contact(s)); DROP CONFIRM (attempt 2, 1 contact(s)) | 2 | 3 |
| SENS-06-PREP-CLOSE-1-2 | CONTACT_CLOSE PREPARE (attempt 1, 1 contact(s)); CONTACT_CLOSE PREPARE (attempt 2, 1 contact(s)) | 2 | 3 |
| SENS-07-CONFIRM-CLOSE-1-2 | CONTACT_CLOSE CONFIRM (attempt 1, 1 contact(s)); CONTACT_CLOSE CONFIRM (attempt 2, 1 contact(s)) | 2 | 3 |
| SENS-08-RESP-DELAY-2 | DELAY RESPONSE (attempt 1, 2 contact(s)) | - | not set by the budget (delay or replay) |
| SENS-09-COMMIT-DELAY-2 | DELAY COMMIT (attempt 1, 2 contact(s)) | - | not set by the budget (delay or replay) |
| SENS-10-COMMIT-RESTART | ENDPOINT_RESTART COMMIT (attempt 1, 1 contact(s)) | - | no budget in the grid repairs it |
| SENS-11-COMMIT-STALE-REPLAY | STALE_REPLAY COMMIT (attempt 1, 1 contact(s)) | - | not set by the budget (delay or replay) |

6 of 12 schedules carry two consecutive drops or contact closures in one phase and therefore need three transmissions; one is an endpoint restart that no budget in the grid repaired; the other 5 carry at most one drop, a delay or a stale replay, or no fault. The counts in the sensitivity summary (5 verification-complete at a budget of two; 11 at three and four) match the five schedules with no repeated drop or closure and no restart, and those five plus the six repeated-fault schedules, and the three candidate lifetimes gave identical counts. Per-schedule outcomes are not tabulated here because they are not in the tracked tables.

**Supplementary Table S3. Study C: the 7 of 31 fault cells never exercised at runtime.**

| Fault | Phase | Scheduled | Applied |
|---|---|---|---|
| CONTACT_CLOSE | CONFIRM | 2 | 0 |
| CONTACT_CLOSE | PREPARE | 2 | 0 |
| CONTACT_CLOSE | RESPONSE | 2 | 0 |
| DELAY | PREPARE | 5 | 0 |
| DELAY | RESPONSE | 1 | 0 |
| DROP | COMMIT | 1 | 0 |
| DUPLICATE | COMMIT | 2 | 0 |

Across all 31 cells, 191 fault actions were scheduled and 77 were applied.

**Supplementary Table S4. Outcome by security state in the 40 deterministic schedules.**

| Schedule class | Raw outcome | Security state | Schedules |
|---|---|---|---|
| CANONICAL_CELL | EXPIRED | UNSAFE | 1 |
| CANONICAL_CELL | INDETERMINATE | NOT_ESTABLISHED | 4 |
| CANONICAL_CELL | SECURE_DEGRADED | UNSAFE | 1 |
| CANONICAL_CELL | SUCCESS | SECURE_PROVISIONAL | 25 |
| CONTROL | SUCCESS | SECURE_PROVISIONAL | 1 |
| RETRY_EXHAUSTION | EXPIRED | UNSAFE | 6 |
| RETRY_EXHAUSTION | SECURE_DEGRADED | UNSAFE | 2 |

10 of 40 schedules end `UNSAFE`.

**Supplementary Table S5. Terms.**

| Term | Meaning in this paper |
|---|---|
| `G_AHEAD`, `S_AHEAD` (Part I) | Ground (spacecraft) epoch counter exceeds the other endpoint's at the end of the run. The base scenario starts with the ground at epoch 2 and the spacecraft at epoch 1, with active keys marked compromised, so `G_AHEAD` after expiry is the starting divergence left unresolved; `S_AHEAD` arises when the spacecraft activates the new epoch and ground never confirms. |
| `UNSAFE` (security state) | At the end, a compromised key is still marked active at the ground or the spacecraft, or the recovery authority is marked compromised. It means recovery did not complete, not that an attack occurred during the run. |
| `SECURE_DEGRADED` (raw outcome) | Historical enum name kept for reproducibility; its security state is `UNSAFE` in all three deterministic schedules in which it occurs, so it is not a secure state. |
| `SUCCESS` | Endpoints converged and verification evidence (test command and authenticated status) completed. |
| `INDETERMINATE` | Endpoints converged but verification evidence is missing. |
| `DIVERGED_G_AHEAD`, `DIVERGED_S_AHEAD` (Part II) | Ground has activated the new epoch and the spacecraft has not, or the reverse. |
| gated activation (Part II) | The spacecraft activates only on authenticated status; local activation activates on COMMIT. |
| $B$ | Transmission budget per phase. Part I uses 2-4; Part II grid uses 4-12; it is unrelated to baseline B0-B2. |

**Supplementary Table S6. Fault kinds exercised and not exercised.**

Fault kinds the plan allows: DROP, DELAY, DUPLICATE, REORDER, CONTACT_CLOSE, ENDPOINT_RESTART, STALE_COUNTER, STALE_REPLAY. Faults are single, scheduled and non-adaptive. Not exercised: adaptive fault timing; injected messages other than stale-counter and stale-replay cases; wall-clock timing, clock drift or link budgets (contacts are abstract slots); and any baseline under Studies B-D (baselines are covered only by Study F, Table S7).

**Supplementary Table S7. Study F: baselines under step-level faults (descriptive; a later run, plan tag `study-f-plan-v1`, not part of the frozen Part I).**

Cells exist only where the frozen baseline abstraction defines the fault; other fault kinds and steps are recorded as not defined. Budget 1 transmits each message once, as specified; budget 3 allows up to three transmissions of a lost message, an assumption favorable to the baselines (COP-1 retransmits telecommand frames). Start state: ground epoch 2, spacecraft epoch 1, current keys attacker-known. Unsafe means a compromised key is still active.

| Baseline | Budget | Cells | Success | Expired | Diverged | Locked | Indeterminate | Unsafe |
|---|---|---|---|---|---|---|---|---|
| B0 OTAR | 1 | 7 | 1 | 0 | 6 | 0 | 0 | 6 |
| B0 OTAR | 3 | 7 | 5 | 0 | 2 | 0 | 0 | 2 |
| B1 local activation | 1 | 15 | 1 | 7 | 7 | 0 | 0 | 14 |
| B1 local activation | 3 | 15 | 9 | 3 | 3 | 0 | 0 | 6 |
| B1 deferred activation | 1 | 21 | 1 | 14 | 6 | 0 | 0 | 20 |
| B1 deferred activation | 3 | 21 | 13 | 6 | 2 | 0 | 0 | 8 |
| B2 strict URKE | 1 | 15 | 2 | 0 | 0 | 7 | 6 | 6 |
| B2 strict URKE | 3 | 15 | 10 | 0 | 0 | 3 | 2 | 2 |

At budget 1, all 16 single-loss cells ended without success. At budget 3, all 32 cells with one or two consecutive losses succeeded; the 21 non-successes were 16 cells with three consecutive losses, 2 endpoint restart, 2 reorder, 1 stale ground restore. Cells per budget: B0 OTAR 7, B1 local activation 15, B1 deferred activation 21, B2 strict URKE 15; the controller has 31 canonical cells. 44 flow-step-kind combinations are not defined for the baseline abstractions and are not run (study_f_not_defined.csv). Budget 3 also lets B2 re-request a lost status, whereas the controller treats lost verification evidence as indeterminate by rule, so those cells are not like for like. Baseline cells map to the controller's fault kinds by family, not one to one, and the same author wrote the engine and the model.

