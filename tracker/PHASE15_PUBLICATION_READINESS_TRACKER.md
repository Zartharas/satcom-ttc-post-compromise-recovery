# Phase 15 Publication Readiness Tracker

**Branch:** `phase-15/publication-preparation`  
**Source baseline:** `04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4`  
**Last updated:** 2026-08-04  
**Overall status:** `IN_PROGRESS_PROVISIONAL_PUBLICATION_PREPARATION`

## Purpose

This tracker separates engineering completion, scientific comparability, immutable evidence capture, external review, and publication authorization. Percentages are project-management estimates, not confidence scores or security guarantees.

## Current position

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D2_LOCAL_VALIDATION=PASS
WP15-D3_LOCAL_VALIDATION=PASS
WP15-D3B=IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION
FAMILY_SPECIFIC_DESCRIPTIVE_COMPARISON=NOT_YET_AUTHORIZED
PUBLICATION_EVIDENCE=false
```

Issue #3 remains open. Review delay does not block provisional engineering, pilot capture, reproducibility testing, or manuscript methods work. It still blocks independent-approval, oracle-freeze, cryptographic-security, and publication-grade claims.

## Master phase tracker

| Phase | Workstream | Status | Estimated completion | Remaining work |
|---|---|---|---:|---|
| 1 | Related work and novelty framing | Complete | 100% | Refresh citations before submission |
| 2 | System and threat model | Complete | 100% | Final manuscript consistency review |
| 3 | Machine-readable abstract design | Complete | 100% | No major work expected |
| 4 | Baseline semantic mapping | Internally complete; externally pending | 85% | Independent review and corrections |
| 5 | Oracle-freeze candidate and handoff | Package complete; freeze pending | 80% | Decisions for 21 candidate oracles |
| 6 | Provisional T1 controller | Implemented and tested | 90% | Revalidate after baseline corrections |
| 7 | Seeded faults and metrics | Implemented and tested | 85% | Freeze schedules and metric population |
| 8 | Analysis and sensitivity framework | Implemented and tested | 85% | Freeze denominators and analysis grid |
| 9 | Adversarial coverage and formal scaffold | Implemented and tested | 90% | Review coverage assumptions |
| 10 | SANY/TLC execution | Complete internally | 95% | Preserve bounded interpretation |
| 11 | Formal/Python success comparison | Complete internally | 90% | Review projection assumptions |
| 12 | Adverse-outcome witnesses | Complete internally | 90% | Review evidence assumptions |
| 13 | Diagnostic outcome expansion | Complete internally | 85% | Accept, revise, or reject expansion |
| 14 | Independent-review package | Ready; review open | 90% | Reviewer acceptance and closure |
| 15 | Publication preparation and revalidation | In progress | 74% | Validate D3B, execute/audit pilot, freeze candidate protocol |
| 16 | Publication-candidate experiment | Not started | 0% | Execute frozen protocol |
| 17 | Results and final manuscript | Not started | 10% | Final analysis and prose |
| 18 | Pre-submission audit and submission | Not started | 0% | Audit, release, formatting, submission |

## Work packages

### WP15-A — Governance and tracking

**Status:** `IN_PROGRESS`

- [x] Create Phase 15 branch.
- [x] Keep Issue #3 open.
- [x] Create readiness and issue trackers.
- [x] Add protocol, data dictionary, capture controls, validators, and tests.
- [x] Commit validated D1 manifest at `fe93689`.
- [x] Commit validated D2 manifest at `0cd96a8`.
- [x] Commit validated D3 manifest at `8500cb5`.
- [x] Record D3B implementation and validation gates.
- [ ] Validate D3B locally.
- [ ] Refresh the manifest after D3B validation.
- [ ] Update `CHANGELOG.md`.
- [ ] Open a draft pull request only after explicit authorization.
- [ ] Complete CI validation.

### WP15-B — Protocol candidate

**Status:** `IN_PROGRESS`

- [x] Define research questions and treatment roles.
- [x] Define inclusion, exclusion, and rerun rules.
- [x] Define T1 and baseline pilot populations.
- [x] Define shared metric and capture parity.
- [x] Define eight comparison families and treatment-specific exclusions.
- [x] Implement four qualified executable families.
- [x] Define member-row and analysis-unit semantics.
- [x] Integrate D2/D3 contracts into immutable capture.
- [ ] Validate D3B execution ordering and metadata.
- [ ] Freeze observation cutoffs and final denominators.
- [ ] Freeze sensitivity and statistical plan.

### WP15-C — Data dictionary and capture controls

**Status:** `IN_PROGRESS`

- [x] Define T1, baseline, D2, and D3 fields.
- [x] Define null-seed and source-hash semantics.
- [x] Define `alignment_class` normalization.
- [x] Define immutable raw data and lineage.
- [x] Define exclusions, reruns, and layered manifests.
- [x] Define D3B metadata schema `0.2.0`.
- [x] Define the derived D3 capture layer.
- [ ] Validate retained-input SHA-256 parity.
- [ ] Define final archive and retention period.

### WP15-D1 — Baseline metric and capture parity

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Execute 21 baseline scenarios.
- [x] Preserve retained design oracles.
- [x] Emit shared metric fields and identifiers.
- [x] Generate JSON and CSV.
- [x] Capture retained configuration/catalog, logs, and manifests.
- [x] Pass 199 local tests and all validators.
- [x] Verify extended capture smoke.
- [ ] Run CI after draft-PR authorization.

### WP15-D2 — Semantic comparability matrix

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Define four qualified and four diagnostic-only families.
- [x] Classify all 36 catalog scenarios exactly once.
- [x] Prohibit `FULL_MATCH`.
- [x] Define family-specific allowed fields.
- [x] Prohibit pooled catalogs, raw timing, transmissions, retries, and epoch-bearing alignment.
- [x] Prevent B1 variants from becoming independent replications.
- [x] Pass 8 focused tests and 207 total tests.
- [x] Commit 169-entry manifest.
- [ ] Run CI after draft-PR authorization.

### WP15-D3 — Executable qualified-family population

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Execute CF-01, CF-02, CF-05, and CF-06.
- [x] Produce 13 member rows and 12 analysis units.
- [x] Preserve the shared B1 analysis unit for two CF-02 policy variants.
- [x] Execute exact T1 catalog behaviors.
- [x] Preserve baseline and T1 internal design oracles.
- [x] Emit strict allowed-field projections and `alignment_class`.
- [x] Emit source-execution SHA-256 values.
- [x] Generate JSON, member CSV, denominator CSV, and internal manifest.
- [x] Keep rates, aggregation, inference, and superiority disabled.
- [x] Pass 9 focused tests and 216 total tests.
- [x] Commit 175-entry manifest.
- [ ] Run CI after draft-PR authorization.

### WP15-D3B — Immutable pilot-bundle integration

**Status:** `IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION`

#### Retained inputs

- [x] Retain T1 pilot configuration.
- [x] Retain baseline-parity configuration.
- [x] Retain D3 matched-family configuration.
- [x] Retain D2 comparability matrix.
- [x] Retain Phase 15 protocol and Phase 08 analysis configuration.
- [x] Retain baseline and T1 catalogs.
- [x] Record every retained path and SHA-256 in metadata.

#### Execution and fail-closed behavior

- [x] Run D3 only after T1 and baseline exit zero.
- [x] Record `SKIPPED_PREREQUISITE_FAILURE` when prerequisites fail.
- [x] Record `PROCESS_FAILED` for a D3 process failure.
- [x] Record `OUTPUT_VALIDATION_FAILED` for rejected zero-exit output.
- [x] Record `COMPLETED_AND_VERIFIED` only after capture-side validation.
- [x] Propagate D3 failure into `overall_exit_code`.

#### Derived capture and validation

- [x] Capture D3 JSON, member CSV, denominator CSV, and internal manifest.
- [x] Require exact 4-family, 13-row, 12-unit population.
- [x] Require 13 source executions and unique row identifiers.
- [x] Require only `QUALIFIED_MATCH` rows.
- [x] Require complete family coverage.
- [x] Require `success_rate_denominator=NOT_DEFINED`.
- [x] Require `aggregate_authorized=false`.
- [x] Verify JSON/CSV member and denominator identity.
- [x] Reject byte tampering.
- [x] Reject re-checksummed semantic gate relaxation.

#### Manifest hierarchy

- [x] Preserve D3 internal manifest.
- [x] Add `manifests/derived.sha256`.
- [x] Preserve `raw.sha256` and `analysis.sha256`.
- [x] Include all layers in `run-bundle.sha256`.
- [x] Verify all manifests before returning success.

#### Validation pending

- [ ] Parse D3B contract locally.
- [ ] Run focused capture and protocol tests.
- [ ] Run D2, D3, D3B, and protocol validators.
- [ ] Run complete regression suite.
- [ ] Run disposable integrated capture from a clean Git state.
- [ ] Verify retained-source and captured SHA-256 equality.
- [ ] Verify D3 internal and all run-level manifests.
- [ ] Refresh and commit the tracked-file manifest.
- [ ] Run CI after draft-PR authorization.

### WP15-D — Pilot execution

**Status:** `NOT_STARTED_GATE_P1_PENDING`

- [ ] Complete D3B validation.
- [ ] Run retained 12-seed T1 pilot.
- [ ] Run all 21 baseline scenarios.
- [ ] Run the four qualified D3 families in the same bundle.
- [ ] Preserve raw, derived, analysis, logs, governance records, and manifests.
- [ ] Keep family-level comparison disabled.

### WP15-E — Pilot audit and protocol-freeze candidate

**Status:** `NOT_STARTED`

- [ ] Verify JSON/CSV consistency and all manifests.
- [ ] Audit source identity, outcomes, schedules, and events.
- [ ] Audit missing and weakly represented groups.
- [ ] Confirm no post-outcome tuning.
- [ ] Record failures, exclusions, and reruns.
- [ ] Resolve defects and rerun where required.

### WP15-F — Publication-candidate capture

**Status:** `BLOCKED_BY_D3B_VALIDATION_AND_PILOT_AUDIT`

- [ ] Freeze protocol, population, cutoffs, and analysis plan.
- [ ] Execute candidate and sensitivity panel.
- [ ] Preserve raw, derived, audit, and formal evidence.
- [ ] Reproduce every manuscript value from retained artifacts.

### WP15-G — Manuscript preparation

**Status:** `IN_PROGRESS`

- [ ] Draft core methods using D2/D3/D3B constraints.
- [ ] Prepare result placeholders without conclusions.
- [ ] Draft limitations, AI-use disclosure, reproducibility, and availability.

### WP15-H — External review

**Status:** `OPEN_NON_BLOCKING_FOR_PROVISIONAL_WORK`

- [x] Initial outreach sent.
- [x] Public prospective-reviewer list removed.
- [ ] Reviewer accepts scope and provides conflict statement.
- [ ] Review completed and corrections revalidated.
- [ ] Baseline oracle outcomes frozen.
- [ ] Publication-facing claims authorized.

## Claim gates

Still prohibited:

- independent approval of baseline mappings;
- cryptographic proof or PCS;
- model completeness or implementation equivalence;
- causal or treatment-superiority claims;
- family success rates or pooled percentages;
- operational timing or transmission equivalence;
- CCSDS/SDLS, flight, RF, or operational applicability; and
- publication-grade evidence before final audit.

## Readiness gates

### Gate P1 — Pilot ready

D1–D3 are locally validated; D3B integrated capture, tests, validators, smoke run, and manifest must also pass.

### Gate P2 — Pilot accepted

Pilot outputs reproduce, all manifests verify, failures remain retained, and corrections close.

### Gate P3 — Comparative publication-candidate execution authorized

D2/D3/D3B are validated, observation cutoffs and denominators are frozen, and the analysis plan is versioned before aggregate review.

### Gate P4 — Manuscript results ready

Every table and value reproduces from retained candidate artifacts.

### Gate P5 — Submission ready

Claims, references, disclosure, availability, formatting, and unresolved limitations pass final audit.

## Immediate next actions

1. Pull the D3B implementation checkpoint.
2. Run focused and complete validation.
3. Execute and audit one disposable integrated bundle.
4. Refresh the repository manifest only after D3B passes.
5. Keep the pull request unopened until explicit authorization.
6. Keep Issue #3 and all publication boundaries accurate.

## Update rule

Update this tracker after every material change to protocol state, capture behavior, validation evidence, review status, or manuscript readiness. Never mark a gate complete from intention or an unverified run.
