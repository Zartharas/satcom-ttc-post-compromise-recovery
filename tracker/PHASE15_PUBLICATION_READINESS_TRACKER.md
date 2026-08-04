# Phase 15 Publication Readiness Tracker

**Branch:** `phase-15/publication-preparation`  
**Source baseline:** `04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4`  
**Last updated:** 2026-08-04  
**Overall status:** `IN_PROGRESS_PROVISIONAL_PUBLICATION_PREPARATION`

## Purpose

This tracker separates engineering completion, scientific comparability, publication evidence, and external review. Percentages are project-management estimates, not confidence scores, proof, or security guarantees.

## Current position

Issue #3 remains open. The review delay does not block provisional implementation, validation, or manuscript preparation, but it still blocks claims of independent approval, frozen baseline oracles, cryptographic security, or externally validated publication conclusions.

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D1_CI_VALIDATION=PENDING
WP15-D2_LOCAL_VALIDATION=PASS
WP15-D2_CI_VALIDATION=PENDING
WP15-D3_IMPLEMENTATION=COMPLETE_PENDING_LOCAL_VALIDATION
WP15-D3_CAPTURE_INTEGRATION=DEFERRED_PENDING_STANDALONE_VALIDATION
FAMILY_SPECIFIC_DESCRIPTIVE_COMPARISON=NOT_YET_AUTHORIZED
PUBLICATION_EVIDENCE=false
```

Validated checkpoints:

- WP15-D1: 199 tests, 21 baseline scenarios, retained-catalog capture, layered manifests, 163-entry repository manifest.
- WP15-D2: 207 tests, 8 comparison families, 36 unique catalog dispositions, no `FULL_MATCH`, 169-entry repository manifest at commit `0cd96a8`.
- RIT-015 assertion defect: corrected and locally validated without changing the comparability matrix.

WP15-D3 now implements an executable member-level population for the four qualified families. It emits 13 member rows and 12 analysis units. The two CF-02 B1 policy variants remain separate rows but share one B1 analysis unit.

## Master phase tracker

| Phase | Workstream | Status | Estimated completion | Remaining work |
|---|---|---|---:|---|
| 1 | Related work and novelty framing | Complete | 100% | Refresh citations before submission |
| 2 | System and threat model | Complete | 100% | Final consistency review |
| 3 | Machine-readable abstract design | Complete | 100% | No major work expected |
| 4 | Baseline semantic mapping | Internally complete; externally pending | 85% | Independent review and corrections |
| 5 | Oracle-freeze candidate and handoff | Package complete; freeze pending | 80% | Decisions for 21 candidate oracles |
| 6 | Provisional T1 controller | Implemented and tested | 90% | Revalidate after any baseline correction |
| 7 | Seeded faults and metrics | Implemented and tested | 85% | Freeze final schedules and population |
| 8 | Analysis and sensitivity framework | Implemented and tested | 85% | Freeze denominators and analysis grid |
| 9 | Adversarial coverage and formal scaffold | Implemented and tested | 90% | Review coverage |
| 10 | SANY/TLC execution | Complete internally | 95% | Preserve bounded interpretation |
| 11 | Formal/Python success comparison | Complete internally | 90% | Review projection assumptions |
| 12 | Adverse-outcome witnesses | Complete internally | 90% | Review evidence assumptions |
| 13 | Diagnostic outcome expansion | Complete internally | 85% | Accept, revise, or reject expansion |
| 14 | Independent-review package | Ready; review open | 90% | Reviewer acceptance and closure |
| 15 | Publication preparation | In progress | 70% | Validate D3, integrate capture, run pilot, audit, draft manuscript |
| 16 | Publication-candidate execution | Not started | 0% | Execute frozen protocol |
| 17 | Results and final manuscript | Not started | 10% | Final analysis and prose |
| 18 | Pre-submission audit | Not started | 0% | Audit, release, formatting, submission |

## Phase 15 work packages

### WP15-A — Governance and tracking

**Status:** `IN_PROGRESS`

- [x] Create Phase 15 branch.
- [x] Keep Issue #3 open.
- [x] Create publication-readiness and issue trackers.
- [x] Add Phase 15 protocol, validators, tests, and CI workflows.
- [x] Refresh the manifest after WP15-D1 validation.
- [x] Refresh the manifest after WP15-D2 validation.
- [ ] Refresh the manifest after WP15-D3 validation.
- [ ] Update `CHANGELOG.md`.
- [ ] Open a draft pull request only after explicit authorization.
- [ ] Complete CI validation.

### WP15-B — Experiment protocol candidate

**Status:** `IN_PROGRESS`

- [x] Define research questions and treatment roles.
- [x] Define inclusion, exclusion, and rerun rules.
- [x] Define T1 pilot parameters and schedule identity.
- [x] Define baseline scenario identity.
- [x] Implement metric and capture parity.
- [x] Define matched scenario families and treatment-specific exclusions.
- [x] Define prohibited pooled comparisons.
- [x] Implement the executable qualified-family population.
- [x] Define family coverage denominators and B1 variant handling.
- [ ] Validate the D3 population locally and in CI.
- [ ] Freeze final observation cutoffs and descriptive-analysis plan.
- [ ] Freeze sensitivity and statistical plan.

### WP15-C — Data dictionary and capture controls

**Status:** `IN_PROGRESS`

- [x] Define T1 and baseline fields.
- [x] Define null-seed and scenario-hash semantics.
- [x] Define immutable raw-data and lineage controls.
- [x] Define provenance, checksum, exclusion, and rerun records.
- [x] Define semantic comparison categories.
- [x] Define and implement derived `alignment_class` projection.
- [x] Define member rows, analysis units, policy variants, and family coverage denominators.
- [ ] Integrate D3 artifacts into the immutable pilot bundle.
- [ ] Define final archive and retention period.

### WP15-D1 — B0/B1/B2 metric and capture parity

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Execute all 21 baseline scenarios and preserve design oracles.
- [x] Emit shared metric fields, JSON, CSV, events, provenance, and checksums.
- [x] Pass 199 tests and complete local capture validation.
- [x] Commit the 163-entry manifest at `fe93689`.
- [ ] Run CI after draft-PR authorization.

### WP15-D2 — Treatment-scenario matrix and semantic comparability

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Define four `QUALIFIED_MATCH` families.
- [x] Define four `DIAGNOSTIC_FAMILY_ONLY` families.
- [x] Prohibit a `FULL_MATCH` classification.
- [x] Classify all 21 baseline and 15 T1 catalog scenarios.
- [x] Define family-specific allowed fields.
- [x] Prohibit timing, transmission, retry, and raw epoch-bearing alignment comparisons.
- [x] Prohibit pooled catalog percentages and diagnostic-family aggregation.
- [x] Prevent B1 policy variants from being counted as independent replications.
- [x] Pass 8 focused tests and 207 total tests.
- [x] Pass standalone D2 validation and independent matrix audit.
- [x] Commit the 169-entry manifest at `0cd96a8`.
- [ ] Run CI after draft-PR authorization.

#### Family register

| Family | Theme | Class | Executed by D3 |
|---|---|---|---|
| CF-01 | Passive operational-key compromise and fresh recovery | Qualified | Yes |
| CF-02 | No-fault completion | Qualified | Yes |
| CF-03 | Pre-completion delivery loss | Diagnostic | No |
| CF-04 | Confirmation evidence loss | Diagnostic | No |
| CF-05 | Post-convergence status loss | Qualified | Yes |
| CF-06 | Replay after successful advancement | Qualified | Yes |
| CF-07 | Ordering fault | Diagnostic | No |
| CF-08 | Rollback or restart | Diagnostic | No |

### WP15-D3 — Executable matched-family population

**Status:** `IMPLEMENTED_PENDING_LOCAL_VALIDATION`

#### Contract and execution

- [x] Add `experiments/configs/phase-15-matched-family-population.json`.
- [x] Restrict execution to CF-01, CF-02, CF-05, and CF-06.
- [x] Pin the expected population to 4 families, 13 member rows, and 12 analysis units.
- [x] Execute B0/B1/B2 members through the oracle-checking baseline adapter.
- [x] Execute T1-01, T1-09, T1-13, and T1-15 through exact catalog behavior recipes.
- [x] Perform T1-13 replay only after successful recovery and verify no state change.
- [x] Retain provenance seeds while marking them noncomparable.

#### Projection and denominator controls

- [x] Project only each family’s explicit `allowed_fields`.
- [x] Derive `alignment_class` and omit raw alignment.
- [x] Omit timing, transmission, retry, and other unauthorized fields.
- [x] Keep the two CF-02 B1 variants as separate rows sharing one analysis unit.
- [x] Define family coverage denominators only.
- [x] Keep success-rate denominators `NOT_DEFINED`.
- [x] Keep every aggregate authorization `false`.
- [x] Keep family-specific descriptive comparison `NOT_YET_AUTHORIZED`.

#### Outputs and validation

- [x] Add `src/ttc_recovery/matched_family_population.py`.
- [x] Add `experiments/scripts/run_phase15_matched_family_population.py`.
- [x] Add `experiments/scripts/validate_phase15_matched_family_population.py`.
- [x] Add `tests/test_phase15_matched_family_population.py`.
- [x] Add `docs/phase-15-matched-family-population.md`.
- [x] Extend `.github/workflows/phase15-comparability.yml` for D3.
- [x] Generate JSON, member CSV, denominator CSV, and a derived SHA-256 manifest.
- [x] Add deterministic source-digest and manifest-tamper tests.
- [ ] Parse D3 JSON locally.
- [ ] Run focused D3 tests.
- [ ] Run the D3 validator.
- [ ] Run a standalone D3 output smoke.
- [ ] Verify 13 rows, 12 units, and all derived checksums.
- [ ] Run the complete regression suite.
- [ ] Refresh and validate the repository manifest.
- [ ] Integrate D3 into the immutable pilot bundle after standalone validation.
- [ ] Run CI after draft-PR authorization.

### WP15-D — Pilot execution

**Status:** `NOT_STARTED_GATE_P1_PENDING`

- [ ] Run the retained 12-seed T1 pilot.
- [ ] Run all 21 baseline scenarios in the same immutable bundle.
- [ ] Retain the D2 matrix and D3 configuration.
- [ ] Execute and retain the D3 member-level derived dataset.
- [ ] Preserve raw traces, metrics, logs, governance records, and manifests.
- [ ] Keep family comparison and all cross-treatment aggregation disabled.

### WP15-E — Pilot audit and protocol freeze candidate

**Status:** `NOT_STARTED`

- [ ] Verify all JSON/CSV files and manifests.
- [ ] Audit outcome, schedule, scenario, projection, denominator, and event consistency.
- [ ] Confirm no post-outcome tuning.
- [ ] Record every failure, exclusion, and rerun.
- [ ] Resolve defects and rerun when required.
- [ ] Decide whether family-specific descriptive comparison can be authorized.

### WP15-F — Publication-candidate data capture

**Status:** `BLOCKED_BY_WP15-D3_CAPTURE_AND_WP15-E`

- [ ] Freeze candidate configuration, observation cutoffs, and analysis plan.
- [ ] Execute the matched population and sensitivity panel.
- [ ] Preserve raw, processed, audit, and formal evidence.
- [ ] Reproduce every manuscript value from retained artifacts.

### WP15-G — Manuscript preparation

**Status:** `IN_PROGRESS`

- [ ] Expand the outline and draft core sections.
- [ ] Draft the experimental method using D2 and D3 constraints.
- [ ] Prepare result placeholders without provisional conclusions.
- [ ] Draft limitations, AI-use disclosure, reproducibility, and availability statements.

### WP15-H — External review

**Status:** `OPEN_NON_BLOCKING_FOR_PROVISIONAL_WORK`

- [x] Initial outreach sent.
- [x] Public prospective-reviewer list removed.
- [ ] Reviewer accepts scope and provides a conflict statement.
- [ ] Review completed and corrections revalidated.
- [ ] Baseline oracle outcomes frozen.
- [ ] Publication-facing claims authorized.

## Publication claim gates

Still prohibited:

- independent approval of baseline mappings;
- cryptographic proof or PCS;
- model completeness or implementation equivalence;
- causal or treatment-superiority claims;
- operational timing or transmission equivalence;
- pooled catalog success percentages;
- family-level success rates before a predeclared denominator exists;
- CCSDS/SDLS, flight, RF, or operational-spacecraft applicability;
- publication evidence before the final capture audit.

## Readiness gates

### Gate P1 — Pilot ready

All Phase 15 files exist, tests and validators pass, manifests verify, baseline oracles are preserved, the D3 standalone dataset verifies, and no critical capture defect remains.

### Gate P2 — Pilot accepted

Pilot outputs reproduce, the D3 artifacts are retained in the immutable bundle, manifests verify, failures remain preserved, and corrections are closed.

### Gate P3 — Comparative publication-candidate execution authorized

D2 and D3 are validated, observation cutoffs and denominators are frozen, and the analysis plan is versioned before comparative aggregates are viewed.

### Gate P4 — Manuscript results ready

Every table and value reproduces from retained candidate artifacts.

### Gate P5 — Submission ready

Claims, references, disclosure, availability, formatting, and unresolved limitations pass final audit.

## Immediate next actions

1. Validate WP15-D3 locally.
2. Correct any execution, projection, denominator, or checksum defect.
3. Refresh the repository manifest only after D3 passes.
4. Integrate the validated D3 outputs into the immutable pilot wrapper.
5. Keep the pull request unopened until explicit authorization.

## Update rule

Update this tracker with every material change to readiness, capture behavior, review status, or manuscript progress. Never mark a gate complete based only on intention or an unverified run.
