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
- Phase 15 pilot capture wrapper with immutable run directories and layered manifests
- WP15-D1 B0/B1/B2 shared metric-field adapter and capture integration
- WP15-D1 local validation: 199 tests, 21 baseline scenarios, retained-catalog capture, and 163-entry manifest
- WP15-D2 matched treatment-scenario matrix and semantic comparability contract

## Current phase

Phase 15 prepares the experiment protocol, data-capture controls, pilot workflow, treatment comparability, and manuscript structure needed before a defensible publication-candidate run.

Current status:

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

Phase 15 does not change the Phase 14 review outcome, baseline oracles, T1 transition semantics, or hard claim boundaries.

## Phase 15 protocol position

The protocol candidate currently defines:

- three candidate research questions;
- B0, B1, B2, and provisional T1 treatment roles;
- a 12-seed T1 pipeline pilot using seeds 7001 through 7012;
- all 21 deterministic B0/B1/B2 catalog scenarios;
- eight treatment-comparison families;
- dispositions for all 21 baseline and 15 T1 catalog scenarios;
- two explicit T1 regression tests used only in diagnostic families;
- family-specific metric authorization and prohibited metrics;
- inclusion, exclusion, rerun, provenance, checksum, and immutability controls;
- a publication-candidate entry gate; and
- explicit non-claim boundaries.

The pilot label is:

`PILOT_INTERNAL_VALIDATION_ONLY`

The pilot may validate T1 schedule generation, baseline catalog adaptation, oracle preservation, treatment-family classification, output capture, analysis handoff, provenance, and checksums. It may not support comparative effectiveness, pooled treatment percentages, inferential statistics, cryptographic-security, causal, timing-equivalence, or publication-grade claims.

## WP15-D1 status

### Baseline metric and capture parity

B0, B1, and B2 execute through a deterministic adapter that:

- runs all 21 existing catalog scenarios;
- checks existing alignment, joint-state when declared, and outcome design oracles;
- emits every shared `RecoveryMetrics` field;
- retains treatment, baseline variant, and scenario ID;
- uses null seeds for deterministic catalog rows;
- creates canonical scenario/schedule SHA-256 identities;
- preserves event logs and adapter-completion evidence;
- writes JSON and CSV outputs; and
- is included in the immutable Phase 15 capture bundle.

Status:

`BASELINE_METRIC_CAPTURE_PARITY_LOCALLY_VALIDATED_CI_PENDING`

Local evidence:

- 199 tests passed;
- all Phase 4–15 validators passed;
- all 21 baseline scenarios matched their retained design oracles;
- 21 unique scenario hashes were retained;
- JSON/CSV consistency passed;
- T1, baseline, and analysis processes exited zero;
- raw, analysis, and complete-bundle manifests verified; and
- the repository manifest verified at 163 entries.

Metric-field and capture parity do not establish matched treatment semantics.

## WP15-D2 status

### Matched treatment-scenario matrix

WP15-D2 defines eight comparison families:

- four `QUALIFIED_MATCH` families;
- four `DIAGNOSTIC_FAMILY_ONLY` families;
- no full-equivalence family.

The matrix classifies every existing catalog scenario exactly once as:

- assigned to one comparison family;
- treatment-specific; or
- a non-outcome guard.

Status:

`TREATMENT_COMPARABILITY_MATRIX_DEFINED_PENDING_VALIDATION`

The matrix permits only family-specific categorical fields. It prohibits raw alignment, contact duration, divergent/degraded window counts, total transmissions, retry overhead, and other treatment-specific units from cross-treatment comparison.

It also prohibits:

- pooling 21 curated baseline rows with 12 seeded T1 rows;
- computing treatment success percentages from unequal curated catalogs;
- counting B1 policy variants as independent replications;
- quantitative aggregation of diagnostic-only families; and
- any field not explicitly authorized by the family.

### Remaining executable-population gap

The matrix is a semantic contract, not a completed comparative experiment.

Status:

`EXECUTABLE_MATCHED_FAMILY_POPULATION_NOT_IMPLEMENTED`

Comparative publication execution remains blocked until the project:

- instantiates the qualified families with equivalent treatment-specific inputs;
- validates equivalent fault opportunities and observation cutoffs;
- emits the normalized `alignment_class` in derived capture;
- defines family-specific denominators;
- freezes the descriptive and statistical plan before viewing comparative aggregates; and
- preserves treatment-specific exceptions without forcing false symmetry.

## Capture status

The Phase 15 wrapper currently captures:

- exact protocol, T1 configuration, baseline configuration, analysis configuration, and baseline catalog;
- Git and environment state;
- T1 seeded outputs;
- B0/B1/B2 baseline adapter outputs;
- T1 analysis outputs;
- commands, stdout, stderr, exclusions, reruns, and metadata; and
- raw, analysis, and complete-bundle SHA-256 manifests.

Status:

`PHASE15_CAPTURE_WRAPPER_LOCALLY_VALIDATED_CI_PENDING`

The WP15-D2 matrix remains a tracked repository contract. Retaining it in a future comparative run bundle is required before publication-candidate execution.

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
- Formal-model-completeness claim: `NOT_PERMITTED`
- Implementation-equivalence claim: `NOT_PERMITTED`
- Cryptographic-security or PCS claim: `NOT_PERMITTED`
- Treatment-superiority claim: `NOT_PERMITTED`
- Causal interpretation of `gapCause`: `NOT_PERMITTED`
- CCSDS/SDLS conformance claim: `NOT_PERMITTED`
- Flight-software, RF, or operational-spacecraft claim: `NOT_PERMITTED`
- Phase 15 pilot publication-evidence status: `NOT_PERMITTED`

## Open governance findings

### GOV-01 — incomplete historical response template

The Phase 04 gate contains 16 required questions. The Phase 05 response template contains only 15 and omits the endpoint-knowledge question now identified as `B1-R5`. The Phase 14 template restores the question without rewriting the historical file.

### GOV-02 — retrospective provisional T1 work

The Phase 04 gate states that T1 work is blocked pending independent review, while Phases 6–13 proceeded as provisional internal work. A future reviewer must decide whether retrospective review is acceptable and identify all later phases requiring revalidation after a baseline correction.

Phase 15 permits provisional preparation, adapter development, comparability design, and pilot-pipeline work, but it does not convert earlier work into independently approved or publication-grade evidence.

### GOV-03 — implementation lock versus independent approval

The phrase corrected and locked for abstract implementation is an internal implementation decision. It is not independent approval, oracle freeze, or publication permission.

### GOV-04 — review-target commit drift

Earlier handoff records point to older candidate commits. Any future review must identify the exact commit reviewed, and the completed response must repeat that SHA.

## Allowed Phase 15 work while review remains open

- protocol, matrix, and data-dictionary development;
- capture-wrapper and baseline-instrumentation implementation;
- unit, regression, validator, and formal testing;
- T1 and deterministic baseline pipeline pilot execution after Gate P1 passes;
- internal reproducibility and checksum validation;
- executable matched-family population design before comparative aggregate review;
- exploratory analysis labeled provisional;
- manuscript structure, methods, limitations, and disclosure drafting; and
- preparation of a concise mature manuscript for possible later review.

## Mandatory stop points

Independent review and correction closure remain mandatory before:

- claiming baseline mappings or oracle decisions are independently accepted;
- freezing baseline or T1 outcome oracles as externally approved;
- accepting a Phase 13 expansion transition or `gapCause` label as externally validated;
- claiming refinement, implementation equivalence, formal completeness, or cryptographic security;
- mapping the abstract model to a concrete protocol implementation;
- claiming CCSDS/SDLS conformance, flight-software correctness, RF behavior, or operational-spacecraft applicability; or
- representing the study as independently validated.

Separate internal protocol, parity, comparability, and population gates remain mandatory before:

- beginning the comparative publication-candidate experiment;
- freezing the final experiment population, fault distribution, exclusions, parameters, thresholds, or statistical plan;
- treating baseline adapter contact or transmission values as directly comparable with T1;
- computing treatment percentages from curated scenario catalogs;
- extracting final manuscript result values; or
- describing Phase 15 pilot outputs as publication evidence.

## Phase 15 artifacts

- `tracker/PHASE15_PUBLICATION_READINESS_TRACKER.md`
- `tracker/RESEARCH_ISSUES_AND_DISCLOSURES.md`
- `spec/phase-15-experiment-protocol-candidate.json`
- `spec/phase-15-treatment-comparability-matrix.json`
- `experiments/configs/phase-15-pilot.json`
- `experiments/configs/phase-15-baseline-parity.json`
- `docs/phase-15-experiment-protocol.md`
- `docs/phase-15-data-dictionary.md`
- `docs/phase-15-baseline-metric-parity.md`
- `docs/phase-15-treatment-comparability.md`
- `governance/phase-15-data-capture-controls.md`
- `src/ttc_recovery/baseline_metrics.py`
- `src/ttc_recovery/treatment_comparability.py`
- `experiments/scripts/validate_phase15_protocol.py`
- `experiments/scripts/validate_phase15_treatment_comparability.py`
- `experiments/scripts/run_phase15_baseline_parity.py`
- `experiments/scripts/run_phase15_pilot_capture.py`
- `tests/test_baseline_metrics.py`
- `tests/test_phase15_treatment_comparability.py`
- `.github/workflows/python-tests.yml`
- `.github/workflows/phase15-comparability.yml`

## Next internal work

1. Validate WP15-D2 JSON, unit tests, standalone validator, and complete regression suite.
2. Confirm all 36 catalog scenarios have one correct disposition and all eight family contracts pass.
3. Refresh and validate the tracked-file manifest after the D2 files stabilize.
4. Keep the Phase 15 pull request unopened until explicit authorization.
5. Begin WP15-D3 only after D2 validation: executable matched-family population and derived comparison dataset.
6. Keep Issue #3 open and report its status accurately without blocking provisional preparation.

## Deferred

- completed independent cryptography review
- completed formal-methods review where required
- frozen baseline and T1 oracles
- accepted or frozen Phase 13 expansion transitions or causes
- frozen formal/Python projection or implementation-equivalence argument
- executable matched-family population
- frozen family-specific denominators and analysis plan
- publication-grade comparative evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- publication-candidate experiment
- final journal manuscript results
