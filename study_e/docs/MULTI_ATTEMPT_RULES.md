# Multi-attempt recovery rules (v0.3.0-dev, DRAFT for author review; not frozen)

Run = at most H contacts. An attempt = the single-attempt exchange of v0.1 (budget B transmissions, lifetime L contacts counted from the attempt's first contact).

1. An attempt ends at the first of: SUCCESS; budget exhausted; attempt lifetime L reached; horizon H reached. It is classified by the step reached (rules.classify).
2. SUCCESS ends the run.
3. DIVERGED_S_AHEAD and DIVERGED_G_AHEAD end the run: fallback (Recovery SA / operator) is required, retrying cannot be assumed safe.
4. EXPIRED_OLD (both sides still on the old keys) before the horizon is retried automatically from the NEXT contact with a fresh budget and lifetime. If the budget ran out mid-contact, the rest of that contact is not used.
5. INDETERMINATE (both sides on the new keys, exchange not completed) ends the run by default (needs a status check/operator). `retry_on=("EXPIRED_OLD","INDETERMINATE")` is a SENSITIVITY setting that presumes the verification messages are idempotent/resumable; it is an upper bound, not a protocol claim.
6. A spacecraft restart can only occur at contact boundaries inside an attempt; restarts between attempts are not modelled (an EXPIRED_OLD attempt holds no state worth losing).
7. Outcome key: (outcome, end_contact, attempts).

Deviation from the earlier draft: the draft retried INDETERMINATE too. The default is now the conservative choice because INDETERMINATE means the new keys are live on both sides and an automatic restart of the exchange is a protocol design decision the paper must not assume.

Finding to report (illustrative grid point p=0.3, K=3, B=8, L=3, r=0.1, H=12): automatic retry of EXPIRED_OLD alone adds only a few points of success (e.g. 0.458 -> 0.485 volatile/local) because the dominant failure is INDETERMINATE (about 0.39) and divergence (0.12-0.30), not expiry. Resumable verification raises success to 0.77-0.90 (sensitivity upper bound). The paper's contribution therefore concerns resumable/idempotent completion and persistence, not just more retries. These are development-run numbers, not pre-registered results.

## Resumable verification (sensitivity option b, added v0.5.0-dev; author approved modelling it next to option a)
- Default (option a, operator-handled): INDETERMINATE ends the run and is reported, not modelled further.
- `resume=True` (option b): an INDETERMINATE end before the horizon is followed, from the next contact, by an attempt that CONTINUES from the step reached with a fresh budget/lifetime. This presumes the remaining activation/verification messages are idempotent and that the state reached survives between contacts (it is still subject to the restart/persistence rules inside each attempt). It is an assumption about protocol design that neither EP (355.1-B-1) nor 354.0-M-1 specifies, so results are reported as an upper-bound sensitivity, never as a property of the standards.
- Distinct from `retry_on=("EXPIRED_OLD","INDETERMINATE")`, which restarts the exchange at step 0.
- Development result (p=0.3, K=3, B=8, L=3, r=0.1, H=20, 4-message recovery): success rises from 0.49-0.59 to 0.77-0.95 and INDETERMINATE falls to 0; divergence is then handled by R0. Not pre-registered.
