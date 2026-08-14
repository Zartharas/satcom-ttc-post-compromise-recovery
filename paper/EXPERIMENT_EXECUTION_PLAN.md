# Lean Final Experiment Execution Plan

**Status:** `PREDECLARED_PRE_RUN_NOT_EXECUTED`
**Plan parent:** `18b09cb60c8a11e309874ffc8a2cb3322610d37f`
**Authoritative machine-readable plan:** `experiments/configs/paper-final-experiment.json`

This plan defines the minimum final hands-on experiment. It does not modify the frozen WP15-D4
objects. The commit containing this pre-run plan is the analysis/execution-plan boundary: after
final-study outcomes are viewed, any material change to schedules, denominators, allowed
cross-treatment fields, or summary definitions must be versioned and disclosed rather than
silently replacing this plan.

## RQ1 — matched recovery behavior

Use the four already-qualified D4 families unchanged:

- `CF-01` passive operational-key compromise + fresh recovery material;
- `CF-02` no-fault transition/recovery completion;
- `CF-05` post-convergence status-telemetry loss;
- `CF-06` replay after successful state advancement.

Retain 13 member rows and 12 treatment-within-family analysis units. The two CF-02 B1 variants
remain two traceability rows under one B1 analysis unit.

### Study A analysis rule

- Compare only fields permitted by the existing D2 matrix and frozen D4 plan.
- Show family-specific categorical member outcomes side by side.
- Do not calculate a pooled cross-family treatment score.
- Do not double-count B1 policy variants.
- Do not compare contact duration, retry overhead, or transmission counts across B0/B1/B2/T1.

Study A is a matched scenario/case comparison, not an inferential treatment trial.

## RQ2 — deterministic T1 fault coverage

The final deterministic matrix contains:

- one no-fault control;
- one canonical schedule for every semantically implemented fault-kind/phase cell; and
- eight retry-exhaustion boundary schedules for `DROP` and `CONTACT_CLOSE` across PREPARE,
  RESPONSE, COMMIT, and CONFIRM.

After the pre-run modeling correction, the implementation has **31** valid fault-kind/phase
cells:

- `DROP`: 6 phases;
- `DELAY`: 6 phases;
- `DUPLICATE`: 4 message-bearing recovery phases;
- `REORDER`: 4 message-bearing recovery phases;
- `CONTACT_CLOSE`: 6 phases;
- `ENDPOINT_RESTART`: COMMIT and CONFIRM;
- `STALE_COUNTER`: PREPARE;
- `STALE_REPLAY`: COMMIT and CONFIRM.

`DUPLICATE` is intentionally excluded from TEST_COMMAND and STATUS_TELEMETRY because those
verification opportunities are represented as boolean delivery evidence in the current model,
not as `RecoveryMessage` objects. Counting a duplicate there as an injected behavioral fault
would overstate what the simulator actually executes.

Total Study B schedules: **40**.

Record terminal outcome, security state, availability state, alignment, verification state, and
rejection/fault evidence. Retain all valid adverse and unexpected outcomes.

## RQ2 robustness panel — fixed mixed faults

Study C uses exactly **100 predeclared integer seeds: `10001` through `10100` inclusive**.

The seed range was selected before final-study outcome execution and does not overlap the earlier
12-seed development pilot. The authoritative artifact is the serialized schedule plus SHA-256,
not the seed alone.

The fixed schedule generator uses:

- fault count: uniform integer selection from 0 through 4;
- fault kind: uniform selection from the eight supported kinds;
- phase: uniform selection from the valid phases for the selected kind;
- handshake attempt: uniform integer selection from 1 through 3;
- DELAY duration: uniform selection of 1 or 2 contact windows;
- duplicate schedule cells suppressed by `(phase, attempt, kind)` identity.

Schedule-only preflight for this fixed seed range contains **191 total injected actions** and
covers all **31** semantically valid fault-kind/phase cells at least once. No seed was selected
or discarded based on an experimental outcome.

Interpret Study C descriptively as a fixed synthetic T1 population. It does not estimate
real-world satellite fault prevalence and is not a B0/B1/B2/T1 rate comparison.

Authorized post-execution Study C summaries:

- count and percentage by `outcome` with denominator 100;
- count by `security_state` and `availability_state`;
- verification-complete count;
- descriptive median/range for T1-only recovery duration, transmissions, and retry overhead;
- descriptive fault-kind and fault-count distributions.

No confidence intervals, hypothesis tests, causal inference, or real-world prevalence inference
are planned.

## RQ3 — retry/retention sensitivity

Use the fixed 3 x 3 grid:

- `max_transmissions = [2, 3, 4]`
- `candidate_lifetime_contacts = [2, 3, 4]`

Study D uses **12 predeclared challenge schedules** chosen to isolate retry/lifetime behavior,
not to represent fault prevalence:

1. no fault;
2. single PREPARE drop;
3. PREPARE drops at attempts 1 and 2;
4. RESPONSE drops at attempts 1 and 2;
5. COMMIT drops at attempts 1 and 2;
6. CONFIRM drops at attempts 1 and 2;
7. PREPARE contact closures at attempts 1 and 2;
8. CONFIRM contact closures at attempts 1 and 2;
9. two-contact RESPONSE delay;
10. two-contact COMMIT delay;
11. spacecraft restart before COMMIT delivery; and
12. stale COMMIT replay.

Total Study D executions: **108**.

Authorized post-execution Study D summaries are outcome/verification counts per grid cell and
T1-only descriptive duration/retry/transmission summaries. The challenge-set denominator is 12
fixed schedules per grid cell; it is not a probabilistic sample.

## RQ4 — assurance

Use existing Phase 10-13 bounded TLA+/Python evidence. No new formal expansion is planned unless
the final experiment reveals a specific inconsistency.

## Target paper artifacts

1. **Table 1:** matched-family member outcomes using only family-authorized fields.
2. **Table 2:** 40-row deterministic T1 fault-coverage matrix.
3. **Figure 1:** experiment/recovery architecture.
4. **Figure 2:** Study C outcome distribution for the fixed 100-schedule population.
5. **Figure 3:** Study D verification-complete count across the 3 x 3 grid.
6. **Supplement:** formal/Python agreement, adverse witnesses, representative traces, and
   supporting Study C/D descriptive tables.

### Table 1 schema

- family;
- treatment / policy variant;
- source scenario;
- outcome;
- alignment class;
- availability state; and
- family-specific evidence limited to fields authorized by D2/D4.

### Table 2 schema

- schedule ID;
- schedule class (`CONTROL`, `CANONICAL_CELL`, or `RETRY_EXHAUSTION`);
- fault kind / phase;
- terminal outcome;
- alignment;
- security state;
- availability state;
- verification complete; and
- rejection evidence.

## Protected scientific inputs

The machine-readable final plan records SHA-256 values for the frozen D4 plan/decision/review,
D2 matrix, D3 population config, baseline/T1 catalogs, and execution modules that define the
matched comparison and T1 behavior. Final execution must use byte-identical protected inputs or
create a new pre-run plan version before viewing replacement results.

## Reproducibility requirements

Every retained final run records exact commit/branch, clean/dirty status, Python/platform,
configs and SHA-256 values, serialized schedules and hashes, raw/analysis-ready outputs,
stdout/stderr, commands, exclusions/reruns, derived table/figure source data, and bundle
checksums.

Valid unfavorable results remain in the dataset. Technical corrections produce a new retained
run rather than silently replacing the original.

## Pre-run decisions resolved

The following are now fixed before final-study outcome execution:

- deterministic Study B coverage and boundary design;
- Study C seeds `10001–10100` and serialized schedules;
- Study D 12 challenge schedules;
- 3 x 3 sensitivity grid;
- permitted descriptive summaries;
- Table 1 / Table 2 / Figure 2 / Figure 3 schemas; and
- byte-level references to the existing D2/D3/D4 objects.

The next task is implementation of the lean final runner against this plan, followed by one
retained execution. No additional governance phase or separate decision commit is required.
