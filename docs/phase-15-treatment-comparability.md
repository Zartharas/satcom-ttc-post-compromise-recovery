# Phase 15 Treatment Comparability

## Status

`DEFINED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

This document explains WP15-D2, the matched treatment-scenario matrix and semantic comparability layer for B0, B1, B2, and provisional T1.

The authoritative machine-readable contract is:

`spec/phase-15-treatment-comparability-matrix.json`

The matrix organizes existing scenarios. It does not change baseline semantics, T1 behavior, external-review status, or publication claim boundaries.

## Why metric-field parity was not enough

WP15-D1 made the baseline and T1 outputs structurally compatible. B0, B1, and B2 now emit the same shared metric field names as T1 and are retained under the same provenance and checksum controls.

That achievement does not make the values scientifically interchangeable.

The baseline adapter currently treats one deterministic catalog scenario as one adapter contact and uses declared scenario-level transmission counts. T1 records contact advancement, retries, and explicit or seeded fault schedules. Therefore, identical columns such as `recovery_duration_contacts`, `total_transmissions`, and `retry_overhead` do not yet have identical units or observation opportunities.

WP15-D2 prevents structural parity from being mistaken for semantic equivalence.

## Comparison classifications

### `QUALIFIED_MATCH`

At least two treatments share a high-level initial condition, fault or observation boundary, and outcome dimension. Protocol assumptions or execution semantics still differ. Only the fields explicitly authorized for that family may later be compared.

A qualified match is not a claim of protocol equivalence.

### `DIAGNOSTIC_FAMILY_ONLY`

The scenarios illuminate a related failure boundary but differ materially in attacker capability, activation timing, retry policy, initial alignment, or state deletion. They may be discussed side by side, but they cannot be pooled or treated as matched observations.

### `TREATMENT_SPECIFIC`

No defensible cross-treatment counterpart is currently defined.

### `NON_OUTCOME_GUARD`

The scenario tests a guard or rejection path and does not enter the common terminal outcome population.

No family is classified as a full match.

## Comparison-family matrix

| Family | Theme | Classification | Treatments represented | Quantitative status |
|---|---|---|---|---|
| CF-01 | Passive operational-key compromise followed by fresh recovery material | `QUALIFIED_MATCH` | B0, B1, B2, T1 | Categorical fields only after validation |
| CF-02 | No-fault state transition or recovery completion | `QUALIFIED_MATCH` | B0, B1, B2, T1 | Categorical fields only after validation |
| CF-03 | Delivery loss before safe shared activation or completion | `DIAGNOSTIC_FAMILY_ONLY` | B0, B1, B2, T1 | No cross-treatment aggregation |
| CF-04 | Post-activation confirmation evidence loss | `DIAGNOSTIC_FAMILY_ONLY` | B1, T1 | No cross-treatment aggregation |
| CF-05 | Post-convergence status telemetry loss | `QUALIFIED_MATCH` | B2, T1 | Restricted categorical and evidence fields |
| CF-06 | Replay after successful state advancement | `QUALIFIED_MATCH` | B2, T1 | Restricted categorical and replay-rejection fields |
| CF-07 | Ordering fault at a required exchange boundary | `DIAGNOSTIC_FAMILY_ONLY` | B1, T1 | No cross-treatment aggregation |
| CF-08 | Persisted-state rollback or endpoint restart | `DIAGNOSTIC_FAMILY_ONLY` | B2, T1 | No cross-treatment aggregation |

## Family details

### CF-01 — Passive operational-key compromise

The four treatments each begin with an attacker-known operational or traffic key while retaining a treatment-specific uncompromised recovery root or authority.

Members:

- B0-02
- B1-02
- B2-02
- T1-15

Potentially comparable categories are terminal outcome, normalized alignment class, security state, availability state, and whether the active key remains attacker-known.

The mechanisms are not equivalent: B0 depends on a surviving master, B1 on its long-term update assumptions, B2 on a fresh update under its construction, and T1 on its recovery authority and bounded controller.

### CF-02 — No-fault completion

Members:

- B0-01
- B1-01
- B1-05
- B2-01
- T1-01

This family is qualified because the baseline cases begin synchronized, while T1-01 begins `G_AHEAD`. The two B1 members are alternative activation policies and cannot be counted as independent replicates.

### CF-03 — Pre-completion delivery loss

Members:

- B0-04
- B1-06
- B2-07
- T1-08

This is a diagnostic family only. B2 has already advanced and deleted prior sender state, B0 retains an attacker-known active key, B1 uses status-gated activation, and T1 starts from a pre-existing alignment gap with a retry budget. Their terminal labels cannot be pooled as equivalent responses to one common experiment.

### CF-04 — Confirmation evidence loss

Members:

- B1-04
- B1-07
- T1-07

The cases share final-message uncertainty after one endpoint may have progressed, but activation boundaries and retained evidence differ. The family supports a structured narrative comparison only.

### CF-05 — Post-convergence status loss

Members:

- B2-08
- T1-09

Both abstractions reach synchronized key state while losing expected status telemetry. This family may later compare normalized alignment, outcome, security, availability, verification completion, telemetry completion, and the declared drop count.

### CF-06 — Replay after success

Members:

- B2-10
- T1-13

Both cases present a stale state-advancing message after successful advancement. The replayed message types and cache semantics differ, so comparison is restricted to categorical terminal state and explicitly validated replay or rejection counts.

### CF-07 — Ordering fault

Members:

- B1-03
- `tests/test_fault_metrics.py::test_reordered_response_is_rejected_then_normal_response_succeeds`

B1 aborts on reordered required fragments. The T1 regression injects an out-of-order response, rejects it, and then continues with the normal response. The opportunity model and retry behavior are not equivalent.

### CF-08 — Rollback or restart

Members:

- B2-09
- `tests/test_fault_metrics.py::test_spacecraft_restart_before_commit_prevents_activation`

A stale persistent ground snapshot and loss of volatile spacecraft pending state are different faults. They share only a broad state-loss theme and are therefore diagnostic rather than quantitatively matched.

## Metric comparability

### Candidate categorical fields

The matrix permits family-specific use of:

- `outcome`
- derived `alignment_class`
- `security_state`
- `availability_state`
- `verification_complete`
- `active_key_compromised`

The derived `alignment_class` maps `SYNC(<epoch>)` to `SYNC` and preserves `G_AHEAD`, `S_AHEAD`, `DIVERGED`, and `LOCKED`. Raw epoch-bearing `alignment` values are not compared across treatments.

### Family-conditional fields

A family may explicitly authorize selected evidence or fault fields, such as:

- `command_accepted`
- `telemetry_complete`
- `drop_count`
- `reorder_count`
- `replay_count`
- `rejection_count`
- `replay_rejection_count`

These fields are not globally comparable. They are usable only where the family contract identifies a sufficiently similar event and observation boundary.

### Fields currently prohibited for cross-treatment comparison

- `seed`
- `schedule_sha256`
- raw `alignment`
- `recovery_duration_contacts`
- `divergent_contact_windows`
- `degraded_contact_windows`
- `total_transmissions`
- `retry_overhead`
- `delay_count`
- `duplicate_count`
- `contact_close_count`
- `restart_count`

Seeds and hashes are provenance identifiers, not treatment metrics. Timing and transmission fields remain treatment-specific until an executable matched-family population provides equivalent units and fault opportunities.

## Population rules

The following are prohibited:

1. Pooling the 21 curated baseline catalog cases with the 12 seeded T1 pilot runs.
2. Computing treatment success percentages from unequal curated catalogs.
3. Treating B1 policy variants as independent replications.
4. Including diagnostic-only families in quantitative aggregates.
5. Using a metric that is not explicitly allowed by that family.
6. Interpreting the matrix as independent validation, cryptographic security, or treatment superiority.

## Scenario coverage

Every existing catalog scenario has one explicit disposition:

- assigned to one comparison family;
- marked treatment-specific; or
- marked as a non-outcome guard.

The current matrix covers:

- 21 baseline catalog scenarios;
- 15 T1 catalog scenarios; and
- two additional explicit T1 regression tests used only in diagnostic families.

Coverage means the scenario has been classified. It does not mean every classified scenario is eligible for comparison.

## Remaining implementation gate

WP15-D2 defines the comparison contract, but it does not yet create a publication-candidate matched execution population.

Before quantitative comparison, the project must still:

- instantiate each quantitative family under equivalent treatment-specific inputs;
- implement and validate `alignment_class` in captured derived outputs;
- establish equivalent fault opportunities and observation cutoffs;
- define family-specific denominators;
- freeze the descriptive and statistical analysis plan before viewing comparative aggregates;
- retain treatment-specific exceptions without forcing false symmetry; and
- preserve the external-review limitation if it remains unresolved.

## Claim boundaries

This work does not authorize claims of:

- independent validation;
- frozen baseline oracles;
- cryptographic security or PCS;
- treatment superiority;
- causal inference;
- operational timing;
- CCSDS/SDLS conformance;
- flight, RF, or operational-spacecraft applicability; or
- publication-grade evidence.
