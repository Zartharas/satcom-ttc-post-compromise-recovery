# Phase 15 Publication Readiness Tracker

**Branch:** `phase-15/publication-preparation`  
**Source baseline:** `04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4`  
**Last updated:** 2026-08-03  
**Overall status:** `IN_PROGRESS_PROVISIONAL_PUBLICATION_PREPARATION`

## Purpose

This tracker records the work required to move from internally validated research software to a defensible research-paper submission. It separates completed engineering work from publication-grade experiment execution and from activities dependent on independent review.

Percentages are project-management estimates. They are not scientific confidence scores, security guarantees, or evidence of external validation.

## Current position

The external-review gate remains open in Issue #3. Phase 15 may continue with protocol, pilot, capture, parity, manuscript, and internal-revalidation work, but it must not convert pending baseline mappings into independently approved claims.

WP15-D1 now implements B0/B1/B2 metric-field and capture parity with T1. All 21 baseline catalog scenarios have an adapter, shared metric fields, JSON/CSV output, event retention, immutable-bundle capture, provenance, and checksum coverage.

Current parity status:

`IMPLEMENTED_PENDING_VALIDATION`

The remaining scientific blocker is not field availability; it is treatment-population comparability. The baseline population is a 21-case deterministic catalog, while T1 currently uses seeded and explicit fault populations.

Remaining comparison status:

`MATCHED_TREATMENT_SCENARIO_MATRIX_NOT_DEFINED`

## Master phase tracker

| Phase | Workstream | Status | Estimated completion | Remaining work |
|---|---|---|---:|---|
| 1 | Related work and novelty framing | Complete | 100% | Refresh citations before submission |
| 2 | System and threat model | Complete | 100% | Final manuscript consistency review |
| 3 | Machine-readable abstract design | Complete | 100% | No major work expected |
| 4 | Baseline semantic mapping | Internally complete; externally pending | 85% | Independent review and any corrections |
| 5 | Oracle-freeze candidate and review handoff | Package complete; freeze pending | 80% | Decisions for all 21 candidate oracles |
| 6 | Provisional T1 recovery controller | Implemented and tested | 90% | Revalidate after any baseline correction |
| 7 | Seeded faults and recovery metrics | Implemented and tested | 85% | Freeze seeds, schedules, and metric population |
| 8 | Analysis and sensitivity framework | Implemented and tested | 85% | Freeze denominators, grids, thresholds, and exclusions |
| 9 | Adversarial coverage and formal scaffold | Implemented and tested | 90% | Review scenario and property coverage |
| 10 | SANY/TLC execution pipeline | Complete internally | 95% | Retain bounded, non-proof interpretation |
| 11 | Formal/Python success-trace comparison | Complete internally | 90% | Review and freeze projection assumptions |
| 12 | Adverse-outcome witnesses | Complete internally | 90% | Review mapping and retained-evidence assumptions |
| 13 | Diagnostic outcome expansion | Complete internally | 85% | Accept, revise, or reject expansion paths |
| 14 | Independent-review package | Ready; review open | 90% | Reviewer acceptance, review, correction closure |
| 15 | Publication preparation and internal revalidation | In progress | 50% | Validate WP15-D1, run pilot, define matched matrix, audit, draft manuscript |
| 16 | Publication-candidate experiment execution | Not started | 0% | Execute frozen candidate protocol and preserve evidence |
| 17 | Results, discussion, and final manuscript | Not started | 10% | Final tables, interpretation, limitations, and prose |
| 18 | Pre-submission audit and submission | Not started | 0% | Reproducibility audit, formatting, release, and submission |

## Phase 15 work packages

### WP15-A — Governance and tracking

**Status:** `IN_PROGRESS`

- [x] Create Phase 15 branch from the validated Phase 14 commit.
- [x] Keep Issue #3 open as the external-review tracker.
- [x] Create publication-readiness and engineering-issue trackers.
- [x] Update `PROJECT_STATUS.md` for the non-blocking provisional-work rule.
- [ ] Update `CHANGELOG.md`.
- [x] Add Phase 15 machine-readable contract and validator.
- [x] Add Phase 15 unit tests.
- [x] Integrate Phase 15 validation and capture smoke execution into CI.
- [ ] Refresh the tracked-file manifest after WP15-D1 stabilizes.
- [ ] Open a draft Phase 15 pull request only after explicit authorization.
- [ ] Complete local and CI validation.

### WP15-B — Experiment protocol candidate

**Status:** `IN_PROGRESS`

- [x] Define candidate research questions mapped to measurable outputs.
- [x] Define baseline and T1 treatment roles.
- [x] Define inclusion and exclusion rules.
- [x] Define candidate retry budgets and lifetime parameters.
- [x] Define pilot seed and serialized T1 schedule policy.
- [x] Define deterministic baseline scenario identity policy.
- [ ] Define and freeze a publication sensitivity-analysis grid.
- [x] Define adverse-outcome handling.
- [x] Define rerun policy before viewing publication aggregates.
- [x] Version the protocol candidate.
- [x] Mark all protocol elements as provisional until internal freeze.
- [x] Implement B0/B1/B2 metric and capture parity with T1.
- [ ] Validate B0/B1/B2 parity locally and in CI.
- [ ] Define the matched treatment-scenario matrix.

**Required outputs:**

- [x] `spec/phase-15-experiment-protocol-candidate.json`
- [x] `experiments/configs/phase-15-pilot.json`
- [x] `experiments/configs/phase-15-baseline-parity.json`
- [x] `docs/phase-15-experiment-protocol.md`
- [x] `docs/phase-15-baseline-metric-parity.md`

### WP15-C — Data dictionary and capture controls

**Status:** `IN_PROGRESS`

- [x] Define raw event-field expectations.
- [x] Define current T1 per-run metrics.
- [x] Extend the dictionary for baseline metric-parity fields.
- [x] Define null-seed and canonical baseline scenario-digest semantics.
- [ ] Define final aggregate denominators for publication analysis.
- [x] Define technical exclusion and failed-run representation.
- [x] Add `CATALOG_ORACLE_MISMATCH` exclusion control.
- [x] Define provenance fields for T1 and baseline execution.
- [x] Define run identifier and directory naming.
- [x] Define immutable raw-data rules.
- [x] Define derived-data lineage.
- [x] Define checksum and manifest policy.
- [ ] Define final archive location and retention period.

**Current outputs:**

- [x] `docs/phase-15-data-dictionary.md`
- [x] `governance/phase-15-data-capture-controls.md`

### WP15-D1 — B0/B1/B2 metric and capture parity

**Status:** `IMPLEMENTED_PENDING_VALIDATION`

- [x] Add `src/ttc_recovery/baseline_metrics.py`.
- [x] Normalize B0/B1/B2 treatment and variant identifiers.
- [x] Execute all 21 catalog scenarios without changing baseline transition code.
- [x] Validate existing alignment, joint-state, and outcome design oracles before output.
- [x] Emit the complete shared `RecoveryMetrics` field set.
- [x] Add baseline-specific `scenario_id`, `baseline_variant`, and `other_fault_count`.
- [x] Use null seeds for deterministic catalog rows.
- [x] Generate canonical baseline scenario/schedule SHA-256 identities.
- [x] Preserve complete event logs and adapter-completion evidence.
- [x] Add JSON and CSV output.
- [x] Add `experiments/scripts/run_phase15_baseline_parity.py`.
- [x] Add retained-catalog preference for immutable capture.
- [x] Add baseline configuration and catalog to the Phase 15 run bundle.
- [x] Add separate baseline command, stdout, stderr, and exit-code records.
- [x] Add baseline outputs to raw and complete-bundle manifests.
- [x] Add focused parity and retained-catalog tests.
- [ ] Run all tests locally.
- [ ] Run the standalone baseline adapter and inspect 21 rows.
- [ ] Run the extended end-to-end capture smoke.
- [ ] Verify raw, analysis, and complete-bundle manifests.
- [ ] Run CI on Python 3.10, 3.13, and 3.14 after draft-PR authorization.
- [ ] Change status only after all validation evidence exists.

### WP15-D2 — Matched treatment-scenario design

**Status:** `NOT_STARTED_BLOCKS_COMPARATIVE_EXECUTION`

- [ ] Define scenario dimensions shared by B0, B1, B2, and T1.
- [ ] Separate protocol-inapplicable cases from missing instrumentation.
- [ ] Define matched initial compromise states.
- [ ] Define matched delivery-fault semantics.
- [ ] Define contact and transmission comparability rules.
- [ ] Define equivalent command and telemetry evidence rules.
- [ ] Define treatment-specific exceptions before viewing comparison aggregates.
- [ ] Version the complete matrix and exclusions.
- [ ] Add matrix validation and tests.

### WP15-D — Pilot execution

**Status:** `NOT_STARTED_GATE_P1_PENDING`

**Pilot label:** `PILOT_INTERNAL_VALIDATION_ONLY`

- [ ] Run the 12-seed T1 capture-pipeline pilot.
- [ ] Run all 21 baseline parity scenarios in the same immutable bundle.
- [ ] Confirm every supported T1 fault kind appears across pilot or explicit regression evidence.
- [ ] Confirm every baseline row matches its retained catalog oracle.
- [ ] Capture raw event traces and metrics.
- [ ] Preserve failures rather than deleting or silently rerunning them.
- [ ] Generate checksums and provenance.
- [ ] Confirm deterministic replay from recorded T1 schedules and baseline scenario digests.
- [ ] Keep cross-treatment aggregate comparison disabled until WP15-D2 is complete.

### WP15-E — Pilot audit and protocol freeze candidate

**Status:** `NOT_STARTED`

- [ ] Verify T1 and baseline JSON/CSV field consistency.
- [ ] Verify all checksum manifests.
- [ ] Audit outcome-field consistency.
- [ ] Audit T1 schedule hashes and baseline scenario hashes.
- [ ] Audit event ordering and adapter-completion records.
- [ ] Audit missing and weakly represented groups.
- [ ] Confirm no post-outcome parameter tuning occurred.
- [ ] Record every excluded or failed run.
- [ ] Resolve pilot defects.
- [ ] Rerun the complete pilot after corrections when required.
- [ ] Decide whether the protocol is ready for publication-candidate execution.

### WP15-F — Publication-candidate data capture

**Status:** `BLOCKED_BY_WP15-D2_AND_WP15-E`

**Candidate label:** `PUBLICATION_CANDIDATE_NOT_EXTERNALLY_VALIDATED`

- [ ] Freeze candidate configuration before execution.
- [ ] Execute the complete matched comparison population.
- [ ] Execute the sensitivity panel.
- [ ] Execute formal regression evidence.
- [ ] Generate raw, processed, and audit outputs.
- [ ] Verify independent rerun from the frozen configuration.
- [ ] Preserve signed checksum manifests.
- [ ] Record any deviation from the protocol.
- [ ] Separate exploratory runs from publication-candidate runs.

### WP15-G — Manuscript preparation

**Status:** `IN_PROGRESS`

- [ ] Expand the manuscript outline.
- [ ] Draft Introduction.
- [ ] Draft Standards and Related Work.
- [ ] Draft System and Threat Model.
- [ ] Draft Recovery Designs.
- [ ] Draft Experimental Method.
- [ ] Prepare Results placeholders without provisional conclusions.
- [ ] Draft Discussion framework.
- [ ] Draft Limitations and Threats to Validity.
- [ ] Add AI-assistance disclosure tailored to the target venue.
- [ ] Add reproducibility and data-availability statements.
- [ ] Add claim-to-evidence traceability.

### WP15-H — External review track

**Status:** `OPEN_NON_BLOCKING_FOR_PROVISIONAL_WORK`

- [x] Initial outreach sent.
- [x] Public reviewer list removed from Issue #3.
- [ ] Qualified reviewer accepts a defined scope.
- [ ] Permission received before publicly identifying a reviewer.
- [ ] Conflict statement received.
- [ ] Review completed.
- [ ] Corrections implemented and revalidated.
- [ ] Baseline oracle outcomes frozen.
- [ ] Publication-facing claims authorized.

## Publication claim gates

The following remain prohibited until supported by the required evidence:

- independent approval of baseline mappings;
- cryptographic proof or post-compromise security;
- model completeness;
- refinement or implementation equivalence;
- causal interpretation of diagnostic labels;
- operational timing or transmission equivalence;
- CCSDS/SDLS conformance;
- flight-software correctness;
- RF or operational-spacecraft applicability;
- security-vulnerability claims without validated impact;
- publication-grade evidence before the final capture audit.

## Readiness gates

### Gate P1 — Pilot ready

WP15-D1 tests, validator, standalone adapter run, and extended capture smoke pass; the tracked manifest verifies; every baseline catalog oracle is preserved; and no unresolved critical capture defect remains.

### Gate P2 — Pilot accepted

T1 and baseline pilot outputs are reproducible, manifests verify, failures are retained, coverage gaps are understood, and pilot corrections are closed.

### Gate P3 — Publication-candidate execution authorized

WP15-D2 is complete, the protocol candidate is internally frozen, outcome labels remain qualified, no parameters change after viewing final aggregate outcomes, and the reviewer issue is accurately disclosed as open if unresolved.

### Gate P4 — Manuscript results ready

Publication-candidate outputs verify, all tables reproduce from preserved data, exclusions match the protocol, and every reported value maps to a retained artifact.

### Gate P5 — Submission ready

Claims audit passes, AI-use disclosure matches venue policy, references are verified, data/code availability statements are accurate, and all unresolved limitations are stated.

## Immediate next actions

1. Fetch the WP15-D1 commits and discard or preserve the previously generated local manifest change before pulling.
2. Run the complete unit-test suite and Phase 15 validator.
3. Execute the standalone baseline parity runner and inspect its 21 rows.
4. Execute the extended Phase 15 capture smoke and verify all manifests.
5. Refresh the repository manifest only after validation passes.
6. Keep Issue #3 open without blocking provisional work.

## Update rule

Update this tracker with any material change to phase status, experiment readiness, capture behavior, reviewer disposition, or manuscript readiness. Never mark a gate complete based only on intention, email outreach, or an unverified run.
