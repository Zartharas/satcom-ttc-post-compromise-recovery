# Phase 15 Experiment Protocol Candidate

## Status

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

This document defines the first publication-preparation protocol candidate. It permits pilot execution and data-capture validation while preserving every unresolved Phase 14 review gate.

The machine-readable source is `spec/phase-15-experiment-protocol-candidate.json`. The executable pilot parameters are in `experiments/configs/phase-15-pilot.json`.

## Purpose

Phase 15 moves the project from internally validated software toward a reproducible research-paper experiment. It separates three activities that must not be conflated:

1. **engineering validation** — unit tests, validators, formal gates, and deterministic regression checks;
2. **pilot data capture** — testing the run, provenance, schema, checksum, exclusion, and analysis pipeline; and
3. **publication-candidate execution** — a later, versioned run using treatment-parity controls and a protocol frozen before aggregate results are interpreted.

The Phase 15 pilot belongs only to the second category.

## Research questions

### RQ-1 — Outcome classification

Within the declared abstract model, how do B0, B1, B2, and provisional T1 classify recovery outcomes under matched fault scenarios?

This question cannot be answered comparatively until every treatment has equivalent scenario execution and metric capture.

### RQ-2 — Contact-window recovery behavior

Within discrete contact windows, how do recovery duration, retry overhead, security state, and availability state vary across matched fault schedules?

The metric definitions, denominators, exclusions, treatment population, and analysis rules remain unfrozen.

### RQ-3 — Formal and Python diagnostics

Where do bounded formal witnesses and Python execution traces agree or differ under the declared projection?

Any result remains bounded and diagnostic. It is not a refinement proof, implementation-equivalence claim, or cryptographic-security result.

## Treatment readiness

| Treatment | Current support | Publication-metric parity |
|---|---|---|
| B0 | Deterministic scenario tests | Missing |
| B1 | Deterministic scenario tests | Missing |
| B2 | Deterministic scenario tests | Missing |
| T1 | Seeded and explicit fault pipeline | Available provisionally |

This asymmetry is a hard publication-candidate blocker. The pilot may validate the T1 capture pipeline, but it must not compare T1 metric counts directly against baseline deterministic-test counts.

## Pilot scope

The pilot label is:

`PILOT_INTERNAL_VALIDATION_ONLY`

The pilot validates:

- deterministic schedule generation from recorded seeds;
- canonical schedule serialization and SHA-256 identity;
- raw JSON and analysis-ready CSV generation;
- event-log completeness;
- analysis handoff;
- run-directory and provenance capture;
- exclusion and rerun controls;
- checksum manifests; and
- reproducibility from the retained configuration.

The pilot does not establish treatment effectiveness, statistical significance, security guarantees, baseline fairness, independent validation, or publication-ready evidence.

## Candidate pilot parameters

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

Allowed fault kinds are `DROP`, `DELAY`, `DUPLICATE`, `REORDER`, `CONTACT_CLOSE`, `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY`.

These values reproduce the existing Phase 07 development population so that Phase 15 initially tests capture controls rather than silently changing the experiment at the same time.

## Inclusion rules

Include every successfully parsed run generated from the exact recorded configuration and serialized schedule. This includes zero-fault schedules and every adverse or unfavorable outcome.

Retain low-count groups and mark them descriptive-only. Do not suppress a run because its outcome is unexpected, inconvenient, or inconsistent with a preferred narrative.

## Exclusion rules

A run may be excluded only for a documented technical reason:

- execution failure;
- corrupted or incomplete output;
- schema failure;
- checksum failure;
- configuration mismatch; or
- a predeclared protocol correction.

Every exclusion must record the run ID, reason, supporting evidence, date, and disposition before aggregate interpretation.

## Rerun rules

A rerun is allowed only after a documented software, environment, schema, checksum, or protocol problem. The original attempt must be retained and linked to the rerun.

Do not rerun solely to obtain a preferred outcome. Do not combine pre-correction and post-correction runs unless the analysis protocol explicitly defines a stratified comparison.

## Analysis boundary

Pilot analysis is limited to descriptive summaries and pipeline validation.

The following are not authorized in the pilot:

- hypothesis testing;
- causal inference;
- confidence-interval claims;
- effect-size claims;
- treatment-superiority claims; or
- cryptographic-security or post-compromise-security claims.

## Required capture record

Each retained pilot run must identify:

- exact Git commit and branch;
- clean or dirty Git status;
- configuration path and SHA-256;
- Python and platform versions;
- exact command line;
- UTC start and end timestamps;
- serialized schedules and their SHA-256 values;
- raw result JSON;
- analysis-ready CSV;
- stdout and stderr logs;
- exclusion or rerun records, where applicable; and
- checksum manifests.

Raw outputs are immutable. Corrections produce a new run directory rather than editing the original capture.

## Publication-candidate entry gate

A publication-candidate run must not begin until:

1. the pilot reproduces from retained configuration and checksums;
2. B0, B1, and B2 have capture and metric parity with T1;
3. treatment scenarios are matched or differences are justified explicitly;
4. seeds, parameters, exclusions, denominators, thresholds, and the statistical plan are versioned before publication aggregates are viewed;
5. scientific-validity defects are closed or accepted transparently as limitations; and
6. the external-review status is represented accurately.

## External-review relationship

Issue #3 remains open. The review delay does not block protocol drafting or pilot execution, but it does block claims that the baseline mappings or 21 oracle candidates are independently approved.

A later reviewer correction may require rerunning affected treatment groups. The retained schedule, configuration, and provenance design is intended to make that impact traceable.

## Hard boundaries

The pilot does not permit claims of:

- independent validation;
- frozen baseline oracles;
- cryptographic security or PCS;
- formal completeness;
- refinement or implementation equivalence;
- causal validity;
- CCSDS/SDLS conformance;
- flight-software, RF, or operational-spacecraft applicability; or
- publication-grade comparative evidence.
