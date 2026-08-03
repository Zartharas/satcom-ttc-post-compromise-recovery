# Project Status

## Completed

- Phase One related-work and novelty framing
- Phase Two system and threat model
- Phase Three machine-readable abstract design
- repository foundation and automated Python test workflow
- B1 Triple-KEM source-semantic review
- B2 construction selection: Poettering-Roesler URKE-inspired strict baseline
- machine-readable Phase 04 baseline semantics
- adversarial review of B1 activation and B2 compromise scope
- corrected deterministic B1 and B2 fault tests
- Phase 05 independent-review handoff and 21-oracle freeze candidate
- automated handoff validation and stacked-pull-request CI
- provisional Phase 06 T1 bounded-resynchronization controller
- deterministic provisional T1 fault and guard tests
- Phase 07 seeded and explicit fault-schedule framework
- provisional contact-window recovery metrics and JSON/CSV export
- preserved-run checksum and provenance workflow outside the Git repository
- provisional Phase 08 aggregation, trace-audit, and sensitivity analysis layer
- Phase 09 explicit adversarial coverage, bounded reachability, and formal-model scaffold
- Phase 10 command-line SANY/TLC execution and counterexample-capture workflow
- Phase 11 formal/Python success-trace cross-validation and finite bound panel
- Phase 12 adverse-outcome witnesses and abstraction-gap diagnostics
- Phase 13 opt-in abstraction-gap outcome expansion and baseline-preservation diagnostics
- Phase 14 independent-review package and claims-traceability preparation
- Phase 15 publication-readiness and engineering-issue trackers
- Phase 15 protocol candidate, pilot configuration, data dictionary, and capture controls
- Phase 15 validator, unit tests, and CI smoke-test integration

## Current phase

Phase 15 prepares the experiment protocol, data-capture controls, pilot workflow, treatment-parity work, and manuscript structure needed before a defensible publication-candidate run.

Current status:

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

Phase 15 does not change the Phase 14 review outcome, baseline oracles, T1 transition semantics, or hard claim boundaries.

## Phase 15 protocol position

The protocol candidate currently defines:

- three candidate research questions;
- B0, B1, B2, and provisional T1 treatment roles;
- a 12-seed T1 pipeline pilot using seeds 7001 through 7012;
- eight supported fault kinds;
- inclusion, exclusion, and rerun rules;
- immutable raw-data and derived-lineage controls;
- provenance, run-ID, checksum, and directory requirements;
- a field-level data dictionary for current T1 outputs;
- a publication-candidate entry gate; and
- explicit non-claim boundaries.

The pilot label is:

`PILOT_INTERNAL_VALIDATION_ONLY`

The pilot may validate schedule generation, T1 execution, output capture, analysis handoff, provenance, and checksums. It may not support comparative treatment, effectiveness, cryptographic-security, causal, or publication-grade claims.

## Experiment-readiness gaps

### Baseline metric parity

B0, B1, and B2 currently have deterministic scenario tests but do not emit the same contact-window, retry, event-log, provenance, exclusion, and checksum fields as the T1 seeded pipeline.

Status:

`BASELINE_METRIC_PARITY_MISSING`

Comparative publication execution is blocked until equivalent baseline instrumentation is implemented or a narrower comparison is justified and versioned before aggregate outcomes are viewed.

### Pilot capture wrapper

The existing seeded runner writes result JSON and metrics CSV. It does not yet create the complete Phase 15 run directory, metadata record, stdout/stderr logs, exclusion and rerun records, or layered checksum manifests.

Status:

`PHASE15_CAPTURE_WRAPPER_NOT_IMPLEMENTED`

A pilot must not be accepted as valid pipeline evidence until this wrapper and its tests are complete.

## Review status

- Phase 14 package status: `READY_FOR_OUTREACH_NOT_REVIEWED`
- Reviewer issue: `#3`, open
- Initial reviewer outreach: sent
- Reviewer accepted a defined scope: no
- Permission to identify a reviewer publicly: no
- Conflict statement received: no
- Independent cryptography review: not yet performed
- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Oracle freeze: `NOT_PERMITTED`
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Formal model review status: `NOT_INDEPENDENTLY_REVIEWED`
- Phase 09/10/11/12/13 formal property set: `PROVISIONAL_ONLY`
- Phase 10 execution status: `FORMAL_EXECUTION_GATES_PASSED`
- Phase 11 success-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 12 adverse-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 13 baseline status: `BASELINE_PRESERVED`
- Phase 13 expansion status: `EXPANDED_OUTCOME_POPULATION_DIAGNOSTIC_ONLY`
- Phase 13 expansion-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Formal-model-completeness claim: `NOT_PERMITTED`
- Implementation-equivalence claim: `NOT_PERMITTED`
- Cryptographic-security or PCS claim: `NOT_PERMITTED`
- Causal interpretation of `gapCause`: `NOT_PERMITTED`
- CCSDS/SDLS conformance claim: `NOT_PERMITTED`
- Flight-software, RF, or operational-spacecraft claim: `NOT_PERMITTED`
- Phase 15 pilot publication-evidence status: `NOT_PERMITTED`

## Open governance findings

### GOV-01 — incomplete historical response template

The Phase 04 gate contains 16 required questions. The Phase 05 response template contains only 15 and omits the endpoint-knowledge question now identified as `B1-R5`. The Phase 14 template restores the question without rewriting the historical file.

### GOV-02 — retrospective provisional T1 work

The Phase 04 gate states that T1 work is blocked pending independent review, while Phases 6-13 proceeded as provisional internal work. A future reviewer must decide whether retrospective review is acceptable and identify all later phases requiring revalidation after a baseline correction.

Phase 15 permits additional provisional preparation and pilot-pipeline work, but it does not convert the earlier work into independently approved or publication-grade evidence.

### GOV-03 — implementation lock versus independent approval

The phrase corrected and locked for abstract implementation is treated as an internal implementation decision. It is not independent approval, oracle freeze, or publication permission.

### GOV-04 — review-target commit drift

Earlier handoff records point to older candidate commits. Any future review must identify the exact commit reviewed, and the completed response must repeat that SHA.

## Allowed Phase 15 work while review remains open

- protocol and data-dictionary development;
- capture-wrapper and baseline-instrumentation implementation;
- unit, regression, validator, and formal testing;
- T1 pipeline pilot execution after Gate P1 passes;
- internal reproducibility and checksum validation;
- exploratory analysis labeled provisional;
- manuscript structure, methods, limitations, and disclosure drafting; and
- preparation of a concise mature manuscript for possible later review.

## Mandatory stop points

Independent review and correction closure remain mandatory before:

- claiming that baseline mappings or oracle decisions are independently accepted;
- freezing baseline or T1 outcome oracles as externally approved;
- accepting or freezing a Phase 13 expansion transition or `gapCause` label as externally validated;
- claiming refinement, implementation equivalence, formal completeness, or cryptographic security;
- mapping the abstract model to a concrete protocol implementation;
- claiming CCSDS/SDLS conformance, flight-software correctness, RF behavior, or operational-spacecraft applicability; or
- representing the study as independently validated.

Separate internal protocol and parity gates are mandatory before:

- beginning the comparative publication-candidate experiment;
- freezing the final experiment population, fault distribution, exclusions, parameters, thresholds, or statistical plan;
- treating T1 seeded metrics as directly comparable with baseline deterministic-test counts;
- extracting final manuscript result values; or
- describing Phase 15 pilot outputs as publication evidence.

Any `ACCEPT WITH CORRECTION` from a future reviewer requires linked corrective commits and complete affected revalidation. No unresolved `REJECT` may remain in a scope described as reviewed.

## Phase 15 artifacts

- `tracker/PHASE15_PUBLICATION_READINESS_TRACKER.md`
- `tracker/RESEARCH_ISSUES_AND_DISCLOSURES.md`
- `spec/phase-15-experiment-protocol-candidate.json`
- `experiments/configs/phase-15-pilot.json`
- `docs/phase-15-experiment-protocol.md`
- `docs/phase-15-data-dictionary.md`
- `governance/phase-15-data-capture-controls.md`
- `experiments/scripts/validate_phase15_protocol.py`
- `tests/test_phase15_protocol.py`
- `.github/workflows/python-tests.yml`

## Next internal work

1. Implement the Phase 15 pilot capture wrapper with immutable run directories and layered manifests.
2. Implement B0/B1/B2 metric and capture parity with T1.
3. Complete local unit, validator, smoke, and manifest checks.
4. Refresh the tracked-file manifest after the Phase 15 files stabilize.
5. Open a draft Phase 15 pull request only after explicit authorization.
6. Execute the T1 pipeline pilot only after Gate P1 passes.
7. Keep Issue #3 open and report its status accurately without blocking provisional preparation.

## Deferred

- completed independent cryptography review
- completed formal-methods review where required
- frozen baseline and T1 oracles
- accepted or frozen Phase 13 expansion transitions or causes
- frozen formal/Python projection or implementation-equivalence argument
- frozen formal outcome population or completeness argument
- frozen final experiment population, parameters, thresholds, and statistical analysis plan
- publication-grade comparative evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- publication-candidate experiment
- final journal manuscript results
