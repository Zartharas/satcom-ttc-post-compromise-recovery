# Phase 15 Publication Readiness Tracker

**Branch:** `phase-15/publication-preparation`  
**Source baseline:** `04c086bc8f75fe6a7bf8e3eede3e24a8ebdf19a4`  
**Last updated:** 2026-08-03  
**Overall status:** `IN_PROGRESS_PROVISIONAL_PUBLICATION_PREPARATION`

## Purpose

This tracker records the work required to move from internally validated research software to a defensible research-paper submission. It separates completed engineering work from publication-grade experiment execution and from activities that remain dependent on independent review.

Percentages are project-management estimates. They are not scientific confidence scores, security guarantees, or evidence of external validation.

## Current position

The repository has completed the major implementation, deterministic testing, and bounded formal-model preparation through Phase 14. The external-review gate remains open in Issue #3. Phase 15 may continue with manuscript preparation, experiment-protocol design, pilot execution, data-capture controls, and internal revalidation, but it must not convert pending baseline mappings into independently approved claims.

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
| 15 | Publication preparation and internal revalidation | In progress | 10% | Protocol, pilot, capture, analysis, and manuscript work |
| 16 | Publication-candidate experiment execution | Not started | 0% | Execute frozen candidate protocol and preserve evidence |
| 17 | Results, discussion, and final manuscript | Not started | 10% | Final tables, interpretation, limitations, and prose |
| 18 | Pre-submission audit and submission | Not started | 0% | Reproducibility audit, formatting, release, and submission |

## Phase 15 work packages

### WP15-A — Governance and tracking

**Status:** `IN_PROGRESS`

- [x] Create Phase 15 branch from the validated Phase 14 commit.
- [x] Keep Issue #3 open as the external-review tracker.
- [x] Create a detailed publication-readiness tracker.
- [x] Create an engineering issue and disclosure tracker.
- [ ] Update `PROJECT_STATUS.md` for the non-blocking provisional-work rule.
- [ ] Update `CHANGELOG.md`.
- [ ] Add Phase 15 machine-readable contract and validator.
- [ ] Add Phase 15 unit tests.
- [ ] Refresh the tracked-file manifest.
- [ ] Open a draft Phase 15 pull request.
- [ ] Complete local and CI validation.

### WP15-B — Experiment protocol candidate

**Status:** `NOT_STARTED`

- [ ] Define research questions and hypotheses mapped to measurable outputs.
- [ ] Define baseline and T1 treatment matrix.
- [ ] Define inclusion and exclusion rules.
- [ ] Define candidate retry budgets and lifetime parameters.
- [ ] Define fixed seed and serialized fault-schedule policy.
- [ ] Define sensitivity-analysis grid.
- [ ] Define adverse-outcome handling.
- [ ] Define rerun policy before viewing aggregate outcomes.
- [ ] Version the protocol candidate.
- [ ] Mark all protocol elements as provisional until internal freeze.

**Required outputs:**

- `spec/phase-15-experiment-protocol-candidate.json`
- `experiments/configs/phase-15-pilot.json`
- `docs/phase-15-experiment-protocol.md`

### WP15-C — Data dictionary and capture controls

**Status:** `NOT_STARTED`

- [ ] Define every raw event field.
- [ ] Define every per-run metric.
- [ ] Define aggregate denominators.
- [ ] Define missing-value and failed-run representation.
- [ ] Define provenance fields.
- [ ] Define run identifier and directory naming.
- [ ] Define immutable raw-data rules.
- [ ] Define derived-data lineage.
- [ ] Define checksum and manifest policy.
- [ ] Define archive and retention policy.

**Minimum provenance fields:**

- exact Git commit;
- branch and dirty-tree state;
- run identifier and UTC creation time;
- experiment configuration hash;
- schedule serialization and hash;
- seed;
- Python and dependency versions;
- Java and TLA+ versions when applicable;
- operating-system and platform details;
- commands executed;
- exit status;
- raw and derived manifests.

### WP15-D — Pilot execution

**Status:** `NOT_STARTED`

**Pilot label:** `PILOT_INTERNAL_VALIDATION_ONLY`

- [ ] Run no-fault controls.
- [ ] Run one representative case for every supported fault kind.
- [ ] Run retry-budget boundary cases.
- [ ] Run candidate-lifetime boundary cases.
- [ ] Run replay, stale-state, restart, and evidence-loss cases.
- [ ] Run baseline and T1 comparison cases.
- [ ] Capture raw event traces and metrics.
- [ ] Preserve failures rather than deleting or silently rerunning them.
- [ ] Generate checksums and provenance.
- [ ] Confirm deterministic replay from recorded schedules.

### WP15-E — Pilot audit and protocol freeze candidate

**Status:** `NOT_STARTED`

- [ ] Verify JSON/CSV field consistency.
- [ ] Verify all checksum manifests.
- [ ] Audit outcome-field consistency.
- [ ] Audit schedule hashes and event ordering.
- [ ] Audit missing and weakly represented groups.
- [ ] Confirm no post-outcome parameter tuning occurred.
- [ ] Record every excluded or failed run.
- [ ] Resolve pilot defects.
- [ ] Rerun the complete pilot after corrections.
- [ ] Decide whether the protocol is ready for publication-candidate execution.

### WP15-F — Publication-candidate data capture

**Status:** `BLOCKED_BY_WP15-E`

**Candidate label:** `PUBLICATION_CANDIDATE_NOT_EXTERNALLY_VALIDATED`

- [ ] Freeze candidate configuration before execution.
- [ ] Execute the complete comparison population.
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
- [ ] Prepare Results placeholders without inserting provisional conclusions.
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
- CCSDS/SDLS conformance;
- flight-software correctness;
- RF or operational-spacecraft applicability;
- security-vulnerability claims without validated impact;
- publication-grade evidence before the final capture audit.

## Readiness gates

### Gate P1 — Pilot ready

All WP15-B and WP15-C items complete, configuration parses, unit tests pass, validators pass, and no unresolved critical internal defect affects capture.

### Gate P2 — Pilot accepted

Pilot is reproducible, manifests verify, failures are retained, coverage gaps are understood, and all pilot corrections are closed.

### Gate P3 — Publication-candidate execution authorized

Protocol candidate is internally frozen, outcome labels remain appropriately qualified, no parameters are changed after viewing final aggregate outcomes, and the reviewer issue is accurately disclosed as open if still unresolved.

### Gate P4 — Manuscript results ready

Publication-candidate outputs verify, all tables reproduce from preserved data, exclusions match the protocol, and every reported value maps to a retained artifact.

### Gate P5 — Submission ready

Claims audit passes, AI-use disclosure matches venue policy, references are verified, data/code availability statements are accurate, and all unresolved limitations are stated.

## Immediate next actions

1. Complete WP15-A repository governance.
2. Build the experiment protocol candidate.
3. Build the data dictionary and capture schema.
4. Execute the pilot only after Gate P1 passes.
5. Keep Issue #3 open without blocking provisional manuscript and pilot preparation.

## Update rule

Update this tracker in the same pull request as any material change to phase status, experiment readiness, data capture, reviewer disposition, or manuscript readiness. Never mark a gate complete based only on intention, email outreach, or an unverified run.
