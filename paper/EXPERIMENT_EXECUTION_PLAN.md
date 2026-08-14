# Lean Final Experiment Execution Plan

**Status:** `DRAFT_PRE_RUN_NOT_FROZEN`
**Source:** `ff10a51ffbd986ef875fe462472d134fdf59695d`

This plan defines the minimum final hands-on experiment. It does not modify the frozen WP15-D4
objects and does not itself authorize a publication claim.

## RQ1 — matched recovery behavior

Use the four already-qualified D4 families unchanged:

- `CF-01` passive operational-key compromise + fresh recovery material;
- `CF-02` no-fault transition/recovery completion;
- `CF-05` post-convergence status-telemetry loss;
- `CF-06` replay after successful state advancement.

Retain 13 member rows and 12 treatment-within-family analysis units. The two CF-02 B1 variants
remain two traceability rows under one B1 analysis unit.

### Analysis rule

- Compare only D2/D4-allowed fields.
- Show family-specific categorical outcomes side by side.
- No pooled cross-family treatment score.
- No double-counting of B1 policy variants.
- No cross-treatment comparison of contact duration, retries, or transmissions.

This is a matched scenario/case comparison, not an inferential treatment trial.

## RQ2 — deterministic T1 fault coverage

Create a predeclared matrix from all valid fault-kind/phase combinations implemented by
`src/ttc_recovery/fault_metrics.py`.

Use at least one canonical schedule per valid cell. Where retry-attempt position changes the
meaning of the fault, add early/final-attempt boundary cases before freezing the matrix.

Record terminal outcome, security state, availability state, alignment, verification, and
rejection/fault evidence. Retain adverse and unexpected valid outcomes.

## RQ2 robustness panel — fixed mixed faults

Run **100 predeclared seeds** through the existing seeded generator.

Before execution:

- enumerate all 100 seeds explicitly;
- state the generator sampling rules;
- serialize/checksum every generated schedule; and
- prohibit replacing a seed because of its outcome.

Interpret the panel descriptively as a synthetic T1 population. It does not estimate real-world
satellite fault prevalence and is not a B0/B1/B2/T1 rate comparison.

## RQ3 — retry/retention sensitivity

Use the already-declared grid:

- `max_transmissions = [2, 3, 4]`
- `candidate_lifetime_contacts = [2, 3, 4]`

Candidate design: 12 fixed schedules x 9 settings = 108 T1 sensitivity executions. Prefer the
existing serialized pilot schedules if their lineage is complete; otherwise generate/freeze a
new 12-schedule set before viewing final sensitivity outputs.

## RQ4 — assurance

Use existing Phase 10-13 bounded TLA+/Python evidence. No new formal expansion is planned unless
the final experiment reveals a specific inconsistency.

## Target paper artifacts

1. **Table 1:** matched families and observed categorical outcomes.
2. **Table 2:** deterministic T1 fault-coverage matrix.
3. **Figure 1:** experiment/recovery architecture.
4. **Figure 2:** fixed 100-seed T1 mixed-fault outcome distribution.
5. **Figure 3:** 3 x 3 retry/retention sensitivity.
6. **Supplement:** formal/Python agreement, adverse witnesses, representative traces.

## Reproducibility requirements

Every retained final run records exact commit/branch, clean/dirty status, Python/platform,
configs and SHA-256 values, serialized schedules and hashes, raw/analysis-ready outputs,
stdout/stderr, commands, exclusions/reruns, derived table/figure source data, and bundle
checksums.

Valid unfavorable results remain in the dataset. Technical corrections create a new run.

## Pre-run decisions still required

Resolve once, before final execution:

1. exact deterministic Study B schedules, including boundary attempts;
2. exact 100 Study C seeds;
3. exact 12 Study D schedules;
4. final T1 descriptive summary fields;
5. final table/figure schemas; and
6. confirmation that frozen D4 objects are referenced unchanged.

Then execute rather than create another governance phase.
