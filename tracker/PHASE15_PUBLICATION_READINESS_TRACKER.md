# Phase 15 Publication Readiness Tracker

**Branch:** `phase-15/publication-preparation`  
**Source baseline:** `04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4`  
**Last updated:** 2026-08-03  
**Overall status:** `IN_PROGRESS_PROVISIONAL_PUBLICATION_PREPARATION`

## Purpose

This tracker records progress from internally validated research software toward a defensible research-paper submission. It separates engineering completion, scientific comparability, publication evidence, and external review.

Percentages are project-management estimates, not confidence scores or security guarantees.

## Current position

Issue #3 remains open. The review delay does not block provisional engineering and manuscript work, but it still blocks claims of independent approval, frozen baseline oracles, or external validation.

Current engineering position:

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D1_CI_VALIDATION=PENDING
WP15-D2_MATRIX=DEFINED_PENDING_VALIDATION
EXECUTABLE_MATCHED_FAMILY_POPULATION=NOT_IMPLEMENTED
PUBLICATION_EVIDENCE=false
```

WP15-D1 passed 199 local tests, all Phase 4–15 validators, a 21-scenario standalone baseline run, an extended immutable capture smoke, and 163-entry repository-manifest validation.

WP15-D2 now defines eight conservative comparison families, classifies all 21 baseline and 15 T1 catalog scenarios, references two explicit T1 diagnostic tests, and prohibits pooled catalog percentages and treatment-specific timing comparisons.

## Master phase tracker

| Phase | Workstream | Status | Estimated completion | Remaining work |
|---|---|---|---:|---|
| 1 | Related work and novelty framing | Complete | 100% | Refresh citations before submission |
| 2 | System and threat model | Complete | 100% | Final manuscript consistency review |
| 3 | Machine-readable abstract design | Complete | 100% | No major work expected |
| 4 | Baseline semantic mapping | Internally complete; externally pending | 85% | Independent review and corrections |
| 5 | Oracle-freeze candidate and review handoff | Package complete; freeze pending | 80% | Decisions for 21 candidate oracles |
| 6 | Provisional T1 recovery controller | Implemented and tested | 90% | Revalidate after baseline corrections |
| 7 | Seeded faults and recovery metrics | Implemented and tested | 85% | Freeze schedules and metric population |
| 8 | Analysis and sensitivity framework | Implemented and tested | 85% | Freeze denominators and analysis grid |
| 9 | Adversarial coverage and formal scaffold | Implemented and tested | 90% | Review coverage |
| 10 | SANY/TLC execution pipeline | Complete internally | 95% | Preserve bounded interpretation |
| 11 | Formal/Python success-trace comparison | Complete internally | 90% | Review projection assumptions |
| 12 | Adverse-outcome witnesses | Complete internally | 90% | Review evidence assumptions |
| 13 | Diagnostic outcome expansion | Complete internally | 85% | Accept, revise, or reject expansion |
| 14 | Independent-review package | Ready; review open | 90% | Reviewer acceptance and closure |
| 15 | Publication preparation and internal revalidation | In progress | 62% | Validate D2, build matched population, run pilot, audit, draft manuscript |
| 16 | Publication-candidate experiment execution | Not started | 0% | Execute frozen protocol |
| 17 | Results, discussion, and final manuscript | Not started | 10% | Final analysis and prose |
| 18 | Pre-submission audit and submission | Not started | 0% | Audit, release, formatting, submission |

## Phase 15 work packages

### WP15-A — Governance and tracking

**Status:** `IN_PROGRESS`

- [x] Create Phase 15 branch.
- [x] Keep Issue #3 open.
- [x] Create publication-readiness and issue trackers.
- [x] Update project status for non-blocking provisional work.
- [x] Add Phase 15 protocol and validators.
- [x] Add unit tests and capture smoke integration.
- [x] Refresh the manifest after WP15-D1 local validation.
- [ ] Refresh the manifest after WP15-D2 validation.
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
- [x] Define matched treatment-scenario families.
- [x] Define treatment-specific and guard exclusions.
- [x] Define prohibited pooled comparisons.
- [ ] Implement executable matched-family cases.
- [ ] Define and freeze family-specific denominators.
- [ ] Freeze sensitivity and statistical plan.

### WP15-C — Data dictionary and capture controls

**Status:** `IN_PROGRESS`

- [x] Define T1 and baseline fields.
- [x] Define null-seed and scenario-hash semantics.
- [x] Define immutable raw-data and lineage controls.
- [x] Define provenance, checksum, exclusion, and rerun records.
- [x] Define semantic comparison categories.
- [x] Define derived `alignment_class` rule.
- [ ] Emit `alignment_class` into future derived comparison output.
- [ ] Define final archive and retention period.

### WP15-D1 — B0/B1/B2 metric and capture parity

**Status:** `LOCALLY_VALIDATED_CI_PENDING`

- [x] Execute all 21 baseline scenarios.
- [x] Preserve existing design oracles.
- [x] Emit shared metric fields and baseline identifiers.
- [x] Generate JSON and CSV.
- [x] Capture retained configuration and catalog.
- [x] Preserve logs, provenance, exclusions, reruns, and manifests.
- [x] Pass 199 local tests.
- [x] Pass all Phase 4–15 validators.
- [x] Verify 21 unique scenario hashes and JSON/CSV consistency.
- [x] Pass extended capture smoke and layered manifests.
- [x] Commit the 163-entry manifest at `fe93689`.
- [ ] Run CI after draft-PR authorization.

### WP15-D2 — Matched treatment-scenario matrix and semantic comparability

**Status:** `IMPLEMENTED_PENDING_VALIDATION`

#### Matrix construction

- [x] Add `spec/phase-15-treatment-comparability-matrix.json`.
- [x] Define four `QUALIFIED_MATCH` families.
- [x] Define four `DIAGNOSTIC_FAMILY_ONLY` families.
- [x] Prohibit a `FULL_MATCH` classification.
- [x] Classify all 21 baseline scenarios.
- [x] Classify all 15 T1 catalog scenarios.
- [x] Reference two explicit T1 diagnostic tests.
- [x] Record treatment-specific cases and non-outcome guards.

#### Semantic controls

- [x] Define candidate categorical fields.
- [x] Define family-conditional fields.
- [x] Prohibit raw timing, transmission, retry, and epoch-bearing alignment comparisons.
- [x] Define `alignment_class` normalization.
- [x] Prohibit pooling 21 curated baseline rows with 12 seeded T1 rows.
- [x] Prohibit catalog success percentages.
- [x] Prevent B1 policy variants from being counted as independent replications.
- [x] Prevent diagnostic families from quantitative aggregation.

#### Validation implementation

- [x] Add `src/ttc_recovery/treatment_comparability.py`.
- [x] Add `experiments/scripts/validate_phase15_treatment_comparability.py`.
- [x] Add `tests/test_phase15_treatment_comparability.py`.
- [x] Add focused CI workflow `.github/workflows/phase15-comparability.yml`.
- [x] Add `docs/phase-15-treatment-comparability.md`.
- [ ] Parse and validate the D2 JSON locally.
- [ ] Run the D2 unit tests.
- [ ] Run the standalone D2 validator.
- [ ] Run the complete regression suite.
- [ ] Refresh and validate the tracked-file manifest.
- [ ] Run CI after draft-PR authorization.

#### D2 family register

| Family | Theme | Class | Treatments | Quantitative use now |
|---|---|---|---|---|
| CF-01 | Passive operational-key compromise and fresh recovery | Qualified | B0/B1/B2/T1 | Not yet authorized |
| CF-02 | No-fault completion | Qualified | B0/B1/B2/T1 | Not yet authorized |
| CF-03 | Pre-completion delivery loss | Diagnostic | B0/B1/B2/T1 | Prohibited |
| CF-04 | Confirmation evidence loss | Diagnostic | B1/T1 | Prohibited |
| CF-05 | Post-convergence status loss | Qualified | B2/T1 | Not yet authorized |
| CF-06 | Replay after successful advancement | Qualified | B2/T1 | Not yet authorized |
| CF-07 | Ordering fault | Diagnostic | B1/T1 | Prohibited |
| CF-08 | Rollback or restart | Diagnostic | B2/T1 | Prohibited |

### WP15-D3 — Executable matched-family population

**Status:** `NOT_STARTED_BLOCKS_COMPARATIVE_EXECUTION`

- [ ] Convert each quantitative family into treatment-specific executable inputs.
- [ ] Define equivalent observation cutoffs.
- [ ] Define equivalent fault opportunities.
- [ ] Implement derived comparison rows with `alignment_class`.
- [ ] Define family-specific denominators.
- [ ] Preserve treatment-specific nonapplicability.
- [ ] Add cross-treatment projection tests without performing inferential statistics.
- [ ] Retain the exact D2 matrix in the run bundle.

### WP15-D — Pilot execution

**Status:** `NOT_STARTED_GATE_P1_PENDING`

- [ ] Run the retained 12-seed T1 pilot.
- [ ] Run all 21 baseline scenarios in the same immutable bundle.
- [ ] Capture raw traces, metrics, logs, and manifests.
- [ ] Confirm deterministic replay and catalog identity.
- [ ] Keep cross-treatment analysis disabled.

### WP15-E — Pilot audit and protocol freeze candidate

**Status:** `NOT_STARTED`

- [ ] Verify JSON/CSV consistency and all manifests.
- [ ] Audit outcome, schedule, scenario, and event consistency.
- [ ] Audit missing and weakly represented groups.
- [ ] Confirm no post-outcome tuning.
- [ ] Record all failures, exclusions, and reruns.
- [ ] Resolve pilot defects and rerun where required.

### WP15-F — Publication-candidate data capture

**Status:** `BLOCKED_BY_WP15-D3_AND_WP15-E`

- [ ] Freeze candidate configuration and analysis plan.
- [ ] Execute the matched population and sensitivity panel.
- [ ] Preserve raw, processed, audit, and formal evidence.
- [ ] Reproduce every manuscript value from retained artifacts.

### WP15-G — Manuscript preparation

**Status:** `IN_PROGRESS`

- [ ] Expand outline and draft core sections.
- [ ] Draft experimental method using the D2 comparability constraints.
- [ ] Prepare result placeholders without provisional conclusions.
- [ ] Draft limitations, AI-use disclosure, reproducibility, and data availability.

### WP15-H — External review

**Status:** `OPEN_NON_BLOCKING_FOR_PROVISIONAL_WORK`

- [x] Initial outreach sent.
- [x] Public prospective-reviewer list removed.
- [ ] Reviewer accepts scope and provides conflict statement.
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
- CCSDS/SDLS, flight, RF, or operational-spacecraft applicability;
- publication-grade evidence before the final audit.

## Readiness gates

### Gate P1 — Pilot ready

All Phase 15 files exist, tests and validators pass, manifests verify, baseline oracles are preserved, and no critical capture defect remains.

### Gate P2 — Pilot accepted

Pilot outputs reproduce, manifests verify, failures remain retained, and corrections are closed.

### Gate P3 — Comparative publication-candidate execution authorized

D2 is validated, D3 provides executable matched families, denominators and observation cutoffs are frozen, and the analysis plan is versioned before aggregate review.

### Gate P4 — Manuscript results ready

Every table and value reproduces from retained candidate artifacts.

### Gate P5 — Submission ready

Claims, references, disclosure, availability, formatting, and unresolved limitations pass final audit.

## Immediate next actions

1. Validate WP15-D2 locally.
2. Fix any matrix, validator, or test defects.
3. Refresh the repository manifest only after D2 passes.
4. Keep the pull request unopened until explicit authorization.
5. Begin WP15-D3 after D2 reaches a clean checkpoint.

## Update rule

Update this tracker with every material change to phase status, experiment readiness, capture behavior, review status, or manuscript readiness. Never mark a gate complete based only on intention or an unverified run.
