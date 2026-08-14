# Retained Experiment Results Summary

## Evidence identity

- Retained run: `20260814T022506Z-gc630fb4`
- Execution commit: `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`
- Plan commit: `cfb730a8191d37863e9e419823686b3c3afe18a2`
- Plan SHA-256: `3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`
- External retained-bundle SHA-256: `b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1`
- Internal retained-bundle manifest: `16/16` files verified
- Study counts: A=13, B=40, C=100, D=108

This file is a post-execution summary derived from the immutable retained run. It does not
modify the predeclared plan in `paper/EXPERIMENT_EXECUTION_PLAN.md` or
`experiments/configs/paper-final-experiment.json`.

## Study A — matched-family comparison

The four qualified matched families show categorical parity on the pre-authorized fields:

- `CF-01`: B0, B1, B2, and T1 are `SUCCESS`, `SYNC`, `AVAILABLE`, and
  `SECURE_PROVISIONAL`; the active key is not marked compromised.
- `CF-02`: all four treatment analysis units are `SUCCESS`, `SYNC`, `AVAILABLE`, and
  `SECURE_PROVISIONAL`, with verification complete. The two B1 policy variants remain two
  traceability rows under one B1 analysis unit.
- `CF-05`: B2 and T1 are both `INDETERMINATE`, `SYNC`, `DEGRADED`, and
  `NOT_ESTABLISHED` after status-telemetry loss.
- `CF-06`: B2 and T1 are both `SUCCESS`, `SYNC`, and `AVAILABLE`; the declared replay is
  rejected.

**Interpretation:** the retained matched-family study does not support a categorical-superiority
claim for T1 over B0/B1/B2. It supports parity on the fields for which treatment semantics could
be matched conservatively.

## Study B — deterministic T1 fault behavior

All 40 predeclared deterministic schedules were executed. Across the 31 canonical
fault-kind/phase cells:

- `25` `SUCCESS`
- `4` `INDETERMINATE`
- `1` `EXPIRED`
- `1` `SECURE_DEGRADED`

The eight retry-exhaustion schedules produced:

- `6` `EXPIRED`
- `2` `SECURE_DEGRADED`

Observed mechanisms:

- isolated recovery-phase `DROP` and `CONTACT_CLOSE` faults recovered within the configured
  retry budget;
- verification-stage command/status loss remained synchronized but was classified
  `INDETERMINATE`, avoiding a false-success classification when evidence was incomplete;
- canonical `DELAY`, message-bearing `DUPLICATE`, `REORDER`, `STALE_COUNTER`, and
  `STALE_REPLAY` cases completed successfully while invalid/stale material was rejected;
- endpoint restart was the principal hard boundary: COMMIT-stage spacecraft restart expired
  before convergence, while CONFIRM-stage restart left a spacecraft-ahead degraded state.

The historical outcome label `SECURE_DEGRADED` must not be read as a security proof. In the
critical retained restart/confirmation-exhaustion cases, the separate `security_state` is
`UNSAFE`.

## Study C — fixed 100-schedule synthetic population

The predeclared fixed population produced:

- `SUCCESS`: 74/100
- `INDETERMINATE`: 15/100
- `SECURE_DEGRADED`: 6/100
- `EXPIRED`: 5/100
- verification complete: 74/100

These are descriptive outcomes for the fixed synthetic schedule population, not estimates of
real satellite fault prevalence.

### Runtime-reachability audit

The predeclared schedules contain `191` scheduled
fault actions, of which `77` were actually
reached and applied. `43` of 100 schedules
had no runtime-applied fault action. Schedule definitions referenced
`31` valid fault-kind/phase cells, while runtime
execution exercised `24` of them.

Therefore the 74 successful schedules must **not** be reported as a “74% success rate under
faults.” Study C is secondary descriptive evidence. Deterministic Study B provides the
fault-cell coverage result.

## Study D — retry/retention sensitivity

Across each candidate-lifetime setting (2, 3, or 4 contacts):

- max transmissions 2: `5/12` verification complete; outcomes
  `{"EXPIRED":5,"SECURE_DEGRADED":2,"SUCCESS":5}`
- max transmissions 3: `11/12` verification complete; outcomes
  `{"EXPIRED":1,"SUCCESS":11}`
- max transmissions 4: `11/12` verification complete; outcomes
  `{"EXPIRED":1,"SUCCESS":11}`

Candidate lifetime produced no observed change within this fixed 12-schedule challenge set.
Increasing the transmission budget from two to three recovered the repeated loss/closure
challenge cases; increasing it from three to four produced no additional observed benefit. The
persistent failure was the COMMIT-stage spacecraft restart, which destroys pending protocol
state and is not repaired by additional message retries.

This is a bounded challenge-set result; it does not establish a universally optimal retry budget
or prove candidate lifetime irrelevant in other conditions.

## Paper claim boundary

The retained experiment supports controlled statements about behavior inside this synthetic
model. It does not establish:

- treatment superiority across incomparable scenarios;
- causal effectiveness outside the declared model;
- cryptographic or strong post-compromise security;
- CCSDS/SDLS conformance;
- real-world fault prevalence;
- flight/RF/operational-spacecraft applicability; or
- independent validation.

No independent baseline cryptography review was completed. The manuscript therefore retains
`independent_validation=false` and treats the baseline mappings as project-defined abstractions.
