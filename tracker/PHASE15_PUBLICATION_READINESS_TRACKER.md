# Phase 15 Publication Readiness Tracker

**Branch:** `phase-15/publication-preparation`  
**Source baseline:** `04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4`  
**Last updated:** 2026-08-04  
**Overall status:** `IN_PROGRESS_PROVISIONAL_PUBLICATION_PREPARATION`

## Purpose

This tracker separates engineering completion, scientific comparability, immutable evidence capture, analysis-plan freezing, external review, and publication authorization. Percentages are project-management estimates, not confidence scores or security guarantees.

## Current position

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D2_LOCAL_VALIDATION=PASS
WP15-D3_LOCAL_VALIDATION=PASS
WP15-D3B_LOCAL_VALIDATION=PASS
WP15-D4_LOCAL_VALIDATION=PASS
WP15-D4R_REVIEW_QUESTIONS=FR01_THROUGH_FR16_PASS
WP15-D4R_REVIEW_PACKAGE_CI=PASS
WP15-D4F_FORMAL_DECISION=ACCEPT
WP15-D4F_DECISION_COMMIT_CI=PENDING
WP15-D4F_FREEZE_EFFECTIVE=false
OBSERVATION_CUTOFF_FREEZE=CANDIDATE_NOT_FROZEN
DENOMINATOR_FREEZE=CANDIDATE_NOT_FROZEN
FAMILY_SPECIFIC_DESCRIPTIVE_COMPARISON=NOT_YET_AUTHORIZED
PUBLICATION_EVIDENCE=false
```

Issue #3 remains open. Review delay does not block provisional engineering, reproducibility testing, immutable pilot capture, outcome-blind plan development, or manuscript methods work. It still blocks independent approval, oracle freeze, cryptographic-security claims, and publication-grade conclusions.

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
| 15 | Publication preparation and revalidation | In progress | 88% | Validate the explicit D4 decision commit in CI and record freeze effectiveness |
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
- [x] Commit validated D3B manifest at `05f114f`.
- [x] Create ignored local compliance archive and commit manifest at `7af4f02`.
- [x] Record D4 implementation and freeze gates.
- [x] Validate D4 locally.
- [ ] Commit the refreshed 185-entry manifest after D4 status reconciliation.
- [ ] Update `CHANGELOG.md` before pull-request preparation.
- [x] Open draft pull request #13 after explicit authorization.
- [x] Complete review-package CI validation.
- [ ] Complete decision-record commit CI validation.

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
- [x] Define outcome-blind D4 observation cutoffs and denominator candidates.
- [x] Define post-observation revision controls.
- [x] Validate D4 identities, cutoffs, denominator rules, and manifest.
- [x] Record the explicit `ACCEPT` decision for the D4 freeze candidate.
- [ ] Make the accepted freeze effective only after decision-record commit CI succeeds.
- [ ] Freeze sensitivity and statistical plan only under a later separate authorization.

### WP15-C — Data dictionary and capture controls

**Status:** `IN_PROGRESS`

- [x] Define T1, baseline, D2, and D3 fields.
- [x] Define null-seed and source-hash semantics.
- [x] Define `alignment_class` normalization.
- [x] Define immutable raw data and lineage.
- [x] Define exclusions, reruns, and layered manifests.
- [x] Define D3B metadata schema `0.2.0`.
- [x] Define the protected D3 derived layer.
- [x] Validate retained-input SHA-256 parity locally.
- [x] Preserve a local checksum-verified compliance archive under ignored `review_document/`.
- [ ] Define final external backup and retention period.

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

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Retain exact T1, baseline, D2, D3, protocol, analysis, and catalog inputs.
- [x] Record retained paths and SHA-256 values in metadata schema `0.2.0`.
- [x] Run D3 only after T1 and baseline exit zero.
- [x] Implement fail-closed prerequisite, process, and output-validation statuses.
- [x] Capture D3 JSON, member CSV, denominator CSV, and internal manifest.
- [x] Require exact 4-family, 13-row, 12-unit population.
- [x] Require 13 source executions and unique row identifiers.
- [x] Reject byte tampering and re-checksummed semantic gate relaxation.
- [x] Add and verify raw, derived, analysis, and complete-bundle manifests.
- [x] Pass 10 focused capture tests, 13 protocol tests, and 223 total tests.
- [x] Complete clean integrated local smoke with all process exit codes zero.
- [x] Commit 178-entry manifest.
- [ ] Run CI after draft-PR authorization.

### WP15-D4 — Outcome-blind family analysis freeze candidate

**Status:** `EXPLICIT_ACCEPT_DECISION_RECORDED_DECISION_COMMIT_CI_PENDING`

#### Population and cutoffs

- [x] Fix family order as CF-01, CF-02, CF-05, and CF-06.
- [x] Fix 13 member identities and 12 treatment-within-family analysis units.
- [x] Preserve two CF-02 B1 policy rows under one `CF-02:B1` unit.
- [x] Define 4 unique terminal observation cutoffs.
- [x] Match each family’s allowed-field names to the D2 matrix.

#### Outcome-blind construction

- [x] Set `projected_metric_values_read=false`.
- [x] Set `raw_execution_values_read=false`.
- [x] Prohibit outcome-dependent branching, filtering, or cutoff extension.
- [x] Add a mutation test requiring projected-value changes to leave the identity contract unchanged.
- [x] Omit outcome and projected-value columns from the member registry.

#### Denominator candidate

- [x] Use treatment-within-family as the candidate denominator unit.
- [x] Keep member rows as traceability records only.
- [x] Block family display when an expected unit is missing.
- [x] Reject undeclared units rather than expanding the denominator.
- [x] Keep `success_rate_denominator=NOT_DEFINED`.
- [x] Keep cross-family denominator and aggregation prohibited.

#### Outputs and controls

- [x] Generate plan JSON, member registry CSV, analysis-unit CSV, family-cutoff CSV, and manifest.
- [x] Require exact four-file manifest coverage.
- [x] Reject tampering and incomplete manifest coverage.
- [x] Add D4 validator, 10 focused tests, protocol checks, CI smoke, documentation, tracker, and RIT-017.

#### Local validation evidence

- [x] Parse D4 and Phase 15 contracts locally.
- [x] Verify exact D2/D4 allowed-field membership and order.
- [x] Run 10 focused D4 tests.
- [x] Run 16 Phase 15 protocol tests.
- [x] Run D2, D3, D3B, D4, and protocol validators.
- [x] Generate one disposable D4 candidate bundle.
- [x] Audit 4 families, 13 rows, 12 units, 4 cutoffs, and closed gates.
- [x] Verify the four-file D4 manifest.
- [x] Run 236 complete regression tests.
- [x] Refresh and validate the 185-entry tracked-file manifest.
- [x] Commit and validate the reconciled 191-entry review-package manifest.
- [x] Run review-package CI in draft PR #13.
- [x] Complete FR-01 through FR-16 with `PASS`.
- [x] Record the explicit formal decision as `ACCEPT`.
- [ ] Run CI for the containing decision-record commit.

#### Explicit decision recorded; effect pending CI

The formal decision is `ACCEPT`, based on 16 `PASS` responses and successful review-package CI. The freeze is not effective until both required workflows succeed for the exact Git commit containing the completed decision record. Family-member values remain closed.

### WP15-D — Pilot execution

**Status:** `NOT_STARTED_GATE_P1_PENDING`

- [x] Complete D3B local validation.
- [x] Complete D4 local validation.
- [ ] Run retained 12-seed T1 pilot under the selected protocol version.
- [ ] Run all 21 baseline scenarios.
- [ ] Run the four qualified D3 families in the same bundle.
- [ ] Preserve raw, derived, analysis, logs, governance records, and manifests.
- [ ] Keep family-level comparison disabled until separately authorized.

### WP15-E — Pilot audit and protocol-freeze candidate

**Status:** `NOT_STARTED`

- [ ] Verify JSON/CSV consistency and all manifests.
- [ ] Audit source identity, outcomes, schedules, and events.
- [ ] Audit missing and weakly represented groups.
- [ ] Confirm no post-outcome tuning.
- [ ] Record failures, exclusions, and reruns.
- [ ] Decide whether D4 can be frozen before comparative display.

### WP15-F — Publication-candidate capture

**Status:** `BLOCKED_BY_D4_VALIDATION_FREEZE_DECISION_AND_PILOT_AUDIT`

- [ ] Freeze protocol, population, cutoffs, denominators, and analysis plan.
- [ ] Execute candidate and sensitivity panel.
- [ ] Preserve raw, derived, audit, and formal evidence.
- [ ] Reproduce every manuscript value from retained artifacts.

### WP15-G — Manuscript preparation

**Status:** `IN_PROGRESS`

- [ ] Draft core methods using D2–D4 constraints.
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

Still candidate-only:

- D4 observation cutoffs;
- D4 treatment-within-family denominators;
- D4 member registry;
- D4 allowed display registry; and
- publication analysis plan.

## Readiness gates

### Gate P1 — Pilot ready

D1–D4 and the separate D4R package are validated. The explicit `ACCEPT` decision is recorded; decision-record commit CI remains pending and the freeze is not effective.

### Gate P2 — Pilot accepted

Pilot outputs reproduce, all manifests verify, failures remain retained, and corrections close.

### Gate P3 — Comparative publication-candidate execution authorized

D2–D4 are validated, D4 receives a separate explicit freeze decision, and the analysis plan is versioned before any comparative display or aggregate review.

### Gate P4 — Manuscript results ready

Every table and value reproduces from retained candidate artifacts.

### Gate P5 — Submission ready

Claims, references, disclosure, availability, formatting, and unresolved limitations pass final audit.

## Immediate next actions

1. Commit the explicit WP15-D4 `ACCEPT` decision record.
2. Push the exact decision-record commit to draft PR #13 only after explicit authorization.
3. Require both pull-request workflows to succeed for that exact commit.
4. Record freeze effectiveness in a separate audited post-CI action without viewing comparative values.
5. Keep member-value display, rates, aggregation, inference, ranking, causal, cryptographic, independent-validation, and publication gates closed.

## Update rule

Update this tracker after every material change to protocol state, capture behavior, validation evidence, freeze state, review status, or manuscript readiness. Never mark a gate complete from intention, an unverified run, or a candidate-only configuration.
