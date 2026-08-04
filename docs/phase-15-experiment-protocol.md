# Phase 15 Experiment Protocol Candidate

## Status

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

This protocol permits pilot execution and data-capture validation while preserving every unresolved Phase 14 review gate.

Machine-readable sources:

- `spec/phase-15-experiment-protocol-candidate.json`
- `spec/phase-15-treatment-comparability-matrix.json`
- `experiments/configs/phase-15-pilot.json`
- `experiments/configs/phase-15-baseline-parity.json`
- `experiments/configs/phase-15-matched-family-population.json`

## Purpose

Phase 15 separates four activities that must not be conflated:

1. **engineering validation** — tests, validators, formal gates, catalog-oracle preservation, and checksums;
2. **pilot data capture** — validating T1, baseline-adapter, provenance, schema, and immutable-bundle behavior;
3. **qualified-family population validation** — executing only the four D2 qualified families and enforcing member-level projection and denominator discipline; and
4. **publication-candidate execution** — a later versioned run using frozen controls and an analysis plan fixed before comparative aggregates are viewed.

The current work belongs only to the first three categories. It is not publication evidence.

## Research questions

### RQ-1 — Outcome classification

Within the declared abstract model, how do B0, B1, B2, and provisional T1 classify recovery outcomes under matched fault scenarios?

This question cannot support comparative conclusions until the matched-family population, observation boundaries, and analysis plan are validated and frozen.

### RQ-2 — Contact-window recovery behavior

Within discrete contact windows, how do recovery duration, retry overhead, security state, and availability state vary across matched fault schedules?

Current baseline adapter contact and transmission values are not accepted as cross-treatment timing or cost units. Duration, transmission, retry, and raw epoch-bearing alignment fields remain excluded from D3 projections.

### RQ-3 — Formal and Python diagnostics

Where do bounded formal witnesses and Python execution traces agree or differ under the declared projection?

Any result remains bounded and diagnostic. It is not a refinement proof, implementation-equivalence claim, or cryptographic-security result.

## Treatment readiness

| Treatment | Current support | Publication-metric parity |
|---|---|---|
| B0 | Deterministic catalog metric adapter | Implemented, locally validated, CI pending |
| B1 | Deterministic catalog metric adapter | Implemented, locally validated, CI pending |
| B2 | Deterministic catalog metric adapter | Implemented, locally validated, CI pending |
| T1 | Seeded, explicit-fault, and catalog-behavior execution | Available provisionally |

Metric parity is not treatment comparability.

## WP15-D1 — Baseline metric and capture parity

WP15-D1 executes all 21 retained baseline catalog scenarios without changing baseline transition logic or expected design oracles.

Before emitting a row, it validates:

- `expected_alignment`;
- `expected_joint_state` when declared; and
- `expected_outcome`.

The adapter emits shared metric fields, baseline-specific identifiers, canonical scenario SHA-256 values, complete event logs, JSON, CSV, and immutable capture evidence.

Detailed semantics are documented in `docs/phase-15-baseline-metric-parity.md`.

## WP15-D2 — Semantic comparability

WP15-D2 defines eight conservative families:

- CF-01, CF-02, CF-05, and CF-06 are `QUALIFIED_MATCH`;
- CF-03, CF-04, CF-07, and CF-08 are `DIAGNOSTIC_FAMILY_ONLY`;
- no family is a `FULL_MATCH`.

All 21 baseline and 15 T1 catalog scenarios have exactly one disposition. The matrix defines family-specific allowed fields, treatment-specific exceptions, and non-outcome guards.

The matrix prohibits:

- pooling the curated baseline catalog with the seeded T1 pilot;
- treatment success percentages from unequal scenario catalogs;
- counting B1 policy variants as independent replications;
- quantitative aggregation of diagnostic families;
- raw epoch-bearing alignment comparison;
- contact duration, divergent/degraded windows, transmissions, or retries as cross-treatment units; and
- any field not explicitly authorized by a family.

The D2 matrix passed local validation. CI remains pending.

## WP15-D3 — Executable qualified-family population

WP15-D3 executes only CF-01, CF-02, CF-05, and CF-06.

Population:

| Family | Member rows | Analysis units |
|---|---:|---:|
| CF-01 | 4 | 4 |
| CF-02 | 5 | 4 |
| CF-05 | 2 | 2 |
| CF-06 | 2 | 2 |
| **Total** | **13** | **12** |

The two CF-02 B1 policy variants remain separate member rows but share the same B1 family analysis unit. They are not independent replicates.

### Source execution

- B0/B1/B2 members execute through the D1 oracle-checking adapter.
- T1-01 executes no-fault ground-ahead recovery.
- T1-09 executes post-convergence status loss.
- T1-13 executes successful recovery followed by replay of the retained commit.
- T1-15 executes equal-epoch recovery with compromised active operational keys.

Every source member must match its retained internal design oracle before projection.

### Projection

Each row contains only the fields authorized by its D2 family. `alignment_class` is derived from raw alignment. Raw `alignment`, contact-duration fields, transmissions, retries, seed identity, schedule identity, and every other unauthorized field are omitted from the member projection.

### Denominators

The D3 denominator table records coverage only:

- member rows;
- unique treatment-family analysis units;
- policy-variant rows; and
- family coverage status.

`success_rate_denominator` remains `NOT_DEFINED`, and `aggregate_authorized` remains `false`.

Family-specific descriptive comparison remains `NOT_YET_AUTHORIZED`.

Detailed D3 semantics are documented in `docs/phase-15-matched-family-population.md`.

## Pilot scope

The pilot label is:

`PILOT_INTERNAL_VALIDATION_ONLY`

The pilot may validate:

- deterministic T1 schedule generation;
- all 21 baseline catalog scenarios and retained design oracles;
- the eight-family D2 semantic matrix;
- the four-family D3 executable population;
- member-level field projection;
- family coverage denominators;
- source-execution SHA-256 values;
- JSON and CSV generation;
- provenance and event retention;
- exclusion and rerun controls; and
- checksum manifests.

The pilot does not establish treatment effectiveness, statistical significance, cryptographic security, baseline fairness, independent validation, operational timing, or publication-ready evidence.

## Candidate T1 pilot parameters

| Parameter | Candidate value | Status |
|---|---:|---|
| Seeds | 7001–7012 | Pilot candidate, unfrozen |
| Ground epoch | 2 | Pilot candidate, unfrozen |
| Spacecraft epoch | 1 | Pilot candidate, unfrozen |
| Authority epoch floor | 0 | Pilot candidate, unfrozen |
| Maximum transmissions | 3 | Pilot candidate, unfrozen |
| Candidate lifetime | 3 contacts | Pilot candidate, unfrozen |
| Maximum scheduled faults | 4 | Pilot candidate, unfrozen |
| Active keys initially marked compromised | true | Pilot candidate, unfrozen |

Allowed T1 fault kinds are `DROP`, `DELAY`, `DUPLICATE`, `REORDER`, `CONTACT_CLOSE`, `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY`.

These values reproduce the existing Phase 07 development population. They do not define the D3 family population or a final publication population.

## Inclusion rules

Include:

- every successfully parsed T1 run from the exact recorded configuration and schedule;
- all 21 baseline catalog scenarios in declared order;
- every member of the four D3 qualified families;
- zero-fault and adverse outcomes; and
- low-count groups labeled descriptive-only.

Do not suppress a run because its outcome is unexpected, inconvenient, or unfavorable.

## Exclusion rules

A run or member may be excluded only for a documented technical reason:

- execution failure;
- corrupted or incomplete output;
- schema failure;
- checksum failure;
- configuration mismatch;
- catalog-oracle mismatch; or
- a predeclared protocol correction.

Every exclusion must record the run or row identifier, reason, evidence, date, and disposition before interpretation.

## Rerun rules

A rerun is allowed only after a documented software, environment, schema, checksum, catalog, or protocol problem. Preserve and link the original attempt.

Do not rerun solely to obtain a preferred outcome. Do not combine pre-correction and post-correction outputs unless the protocol explicitly defines a stratified analysis.

## Analysis boundary

Authorized now:

- engineering validation;
- member-level family projection for internal validation;
- family coverage and analysis-unit counting; and
- checksum and reproducibility auditing.

Not authorized:

- family-specific descriptive conclusions;
- success rates or percentages;
- pooled cross-treatment aggregation;
- hypothesis testing;
- confidence intervals;
- effect-size claims;
- causal inference;
- treatment superiority; or
- cryptographic-security or PCS claims.

## Required capture record

Each retained pilot bundle must ultimately identify:

- exact Git commit and branch;
- clean or dirty Git status;
- T1, baseline, D2, and D3 configuration paths and SHA-256 values;
- retained baseline and T1 catalogs;
- Python and platform versions;
- exact command lines and UTC timestamps;
- raw T1 and baseline outputs;
- D3 member and denominator outputs;
- source-execution SHA-256 values;
- stdout and stderr logs;
- exclusion and rerun records; and
- raw, derived, analysis, and complete-bundle manifests.

Raw outputs are immutable. Corrections produce a new run directory.

D3 immutable-bundle integration is deferred until the standalone D3 runner, tests, validator, and derived manifest pass locally.

## Publication-candidate entry gate

A publication-candidate run must not begin until:

1. the T1 and baseline pilot pipelines reproduce from retained configurations and checksums;
2. D1 metric and capture parity is validated;
3. D2 semantic comparability is validated;
4. D3 execution, projection, denominators, and immutable capture are validated;
5. observation cutoffs and treatment-specific exceptions are versioned;
6. the descriptive and statistical plan is fixed before comparative aggregates are viewed;
7. scientific-validity defects are closed or accepted transparently as limitations; and
8. the external-review status is represented accurately.

## External-review relationship

Issue #3 remains open. The delay does not block provisional protocol, parity, matrix, population, pilot, or manuscript work. It does block claims that baseline mappings or candidate oracles are independently approved.

A later reviewer correction may require rerunning affected family members. Retained source executions, digests, configurations, and manifests are intended to make that impact traceable.

## Hard boundaries

The pilot does not permit claims of:

- independent validation;
- frozen baseline oracles;
- cryptographic security or PCS;
- formal completeness;
- refinement or implementation equivalence;
- causal validity;
- treatment superiority;
- operational timing equivalence;
- CCSDS/SDLS conformance;
- flight-software, RF, or operational-spacecraft applicability; or
- publication-grade comparative evidence.
