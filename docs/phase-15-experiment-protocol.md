# Phase 15 Experiment Protocol Candidate

## Status

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

This document defines the first publication-preparation protocol candidate. It permits pilot execution and data-capture validation while preserving every unresolved Phase 14 review gate.

The machine-readable source is `spec/phase-15-experiment-protocol-candidate.json`. T1 pilot parameters are in `experiments/configs/phase-15-pilot.json`. The B0/B1/B2 adapter configuration is in `experiments/configs/phase-15-baseline-parity.json`.

## Purpose

Phase 15 moves the project from internally validated software toward a reproducible research-paper experiment. It separates three activities that must not be conflated:

1. **engineering validation** — unit tests, validators, formal gates, deterministic regression checks, and catalog-oracle preservation;
2. **pilot data capture** — testing T1 and baseline-adapter execution, provenance, schema, checksum, exclusion, and analysis pipelines; and
3. **publication-candidate execution** — a later, versioned run using matched-treatment controls and a protocol frozen before aggregate results are interpreted.

The Phase 15 pilot belongs only to the second category.

## Research questions

### RQ-1 — Outcome classification

Within the declared abstract model, how do B0, B1, B2, and provisional T1 classify recovery outcomes under matched fault scenarios?

This question cannot be answered comparatively until treatment scenarios are matched or unmatched cases are justified before aggregate results are viewed.

### RQ-2 — Contact-window recovery behavior

Within discrete contact windows, how do recovery duration, retry overhead, security state, and availability state vary across matched fault schedules?

The metric definitions, denominators, exclusions, treatment population, and analysis rules remain unfrozen. Baseline adapter contact and transmission values are not yet accepted as comparative measurement semantics.

### RQ-3 — Formal and Python diagnostics

Where do bounded formal witnesses and Python execution traces agree or differ under the declared projection?

Any result remains bounded and diagnostic. It is not a refinement proof, implementation-equivalence claim, or cryptographic-security result.

## Treatment readiness

| Treatment | Current support | Publication-metric parity |
|---|---|---|
| B0 | Deterministic catalog metric adapter | Implemented, pending validation |
| B1 | Deterministic catalog metric adapter | Implemented, pending validation |
| B2 | Deterministic catalog metric adapter | Implemented, pending validation |
| T1 | Seeded and explicit fault pipeline | Available provisionally |

Metric-field parity is not treatment comparability. The B0/B1/B2 adapter now emits the shared T1 metric fields and is included in the immutable capture bundle, but the 21 deterministic catalog cases are not a matched seeded fault population.

The pilot must not infer effectiveness or superiority from differences between baseline adapter rows and T1 seeded rows.

## WP15-D1 baseline adapter

WP15-D1 executes all 21 scenarios in `tests/scenarios/baseline-test-catalog.json` without changing baseline transition logic or expected design oracles.

Before emitting a row, the adapter validates:

- `expected_alignment`;
- `expected_joint_state` when declared; and
- `expected_outcome`.

The adapter emits:

- normalized treatment and retained baseline-variant identifiers;
- deterministic scenario ID;
- canonical scenario/schedule SHA-256;
- the complete shared `RecoveryMetrics` field set;
- baseline-specific `other_fault_count`;
- complete simulator event logs;
- JSON and CSV outputs; and
- an explicit adapter-completion event marked `publication_evidence=false`.

Detailed semantics and limitations are documented in `docs/phase-15-baseline-metric-parity.md`.

## Pilot scope

The pilot label is:

`PILOT_INTERNAL_VALIDATION_ONLY`

The pilot validates:

- deterministic T1 schedule generation from recorded seeds;
- canonical T1 schedule serialization and SHA-256 identity;
- execution of all 21 baseline catalog scenarios;
- preservation of existing baseline catalog design oracles;
- canonical baseline scenario/schedule identity;
- shared metric-field generation;
- raw T1 and baseline JSON and analysis-ready CSV generation;
- event-log completeness;
- T1 analysis handoff;
- run-directory and provenance capture;
- exclusion and rerun controls;
- checksum manifests; and
- reproducibility from retained configurations and the retained catalog.

The pilot does not establish treatment effectiveness, matched scenario coverage, statistical significance, security guarantees, baseline fairness, independent validation, operational timing, or publication-ready evidence.

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

These values reproduce the existing Phase 07 development population so that Phase 15 initially tests capture controls rather than silently changing the experiment at the same time.

## Baseline adapter rules

- All 21 catalog scenarios are mandatory.
- `seed` is null because the catalog is deterministic.
- Each scenario is represented as one adapter contact.
- Transmission counts are declared abstract attempted-message counts.
- Catalog assumptions and conditions are not counted as delivery faults.
- Concrete disruptions are normalized into structured actions.
- Active sender impersonation remains an adapter-specific fault and is retained through `other_fault_count`.
- Metric-field parity must not be described as timing, scenario, or causal equivalence.

## Inclusion rules

Include every successfully parsed T1 run generated from the exact recorded configuration and serialized schedule. Include all 21 baseline catalog scenarios in their declared order. This includes zero-fault schedules and every adverse or unfavorable outcome.

Retain low-count groups and mark them descriptive-only. Do not suppress a run because its outcome is unexpected, inconvenient, or inconsistent with a preferred narrative.

## Exclusion rules

A run or scenario may be excluded only for a documented technical reason:

- execution failure;
- corrupted or incomplete output;
- schema failure;
- checksum failure;
- configuration mismatch;
- baseline catalog-oracle mismatch; or
- a predeclared protocol correction.

Every exclusion must record the run ID, seed or scenario ID, reason, supporting evidence, date, and disposition before aggregate interpretation.

A catalog-oracle mismatch terminates the adapter run. It must not be resolved by silently changing the captured expected value.

## Rerun rules

A rerun is allowed only after a documented software, environment, schema, checksum, catalog, or protocol problem. The original attempt must be retained and linked to the rerun.

Do not rerun solely to obtain a preferred outcome. Do not combine pre-correction and post-correction runs unless the analysis protocol explicitly defines a stratified comparison.

## Analysis boundary

Pilot analysis is limited to descriptive summaries and pipeline validation.

The following are not authorized in the pilot:

- hypothesis testing;
- causal inference;
- confidence-interval claims;
- effect-size claims;
- treatment-superiority claims;
- direct aggregate comparison between the current baseline catalog and T1 seed population; or
- cryptographic-security or post-compromise-security claims.

## Required capture record

Each retained pilot run must identify:

- exact Git commit and branch;
- clean or dirty Git status;
- T1 configuration path and SHA-256;
- baseline configuration path and SHA-256;
- retained baseline catalog path and SHA-256;
- protocol and analysis configuration hashes;
- Python and platform versions;
- exact T1, baseline, and analysis command lines;
- UTC start and end timestamps;
- T1 serialized schedules and SHA-256 values;
- baseline canonical scenario/schedule SHA-256 values;
- raw T1 and baseline result JSON;
- analysis-ready T1 and baseline CSV;
- stdout and stderr logs;
- exclusion or rerun records, where applicable; and
- checksum manifests.

Raw outputs are immutable. Corrections produce a new run directory rather than editing the original capture.

## Publication-candidate entry gate

A publication-candidate run must not begin until:

1. the T1 and baseline pilot pipelines reproduce from retained configurations, retained catalog, and checksums;
2. B0, B1, and B2 metric-field and capture parity is validated;
3. treatment scenarios are matched or differences are justified explicitly;
4. adapter contact and transmission semantics are accepted, replaced, or excluded from comparative inference;
5. seeds, parameters, exclusions, denominators, thresholds, and the statistical plan are versioned before publication aggregates are viewed;
6. scientific-validity defects are closed or accepted transparently as limitations; and
7. the external-review status is represented accurately.

## External-review relationship

Issue #3 remains open. The review delay does not block protocol drafting, parity implementation, or pilot execution, but it does block claims that the baseline mappings or 21 oracle candidates are independently approved.

A later reviewer correction may require rerunning affected treatment groups. The retained schedule, catalog, configuration, and provenance design is intended to make that impact traceable.

## Hard boundaries

The pilot does not permit claims of:

- independent validation;
- frozen baseline oracles;
- cryptographic security or PCS;
- formal completeness;
- refinement or implementation equivalence;
- causal validity;
- operational timing equivalence;
- CCSDS/SDLS conformance;
- flight-software, RF, or operational-spacecraft applicability; or
- publication-grade comparative evidence.
