# Project Status

## Current phase

Phase 15 prepares a reproducible synthetic experiment protocol, immutable capture workflow, qualified-family execution layer, and manuscript foundation while preserving every unresolved independent-review and publication-claim gate.

Current overall status:

```text
PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE
```

The work does not change Phase 14 review status, freeze baseline oracles, establish cryptographic security, or authorize publication conclusions.

## Completed internal engineering

- Phases 1–3 research framing, system/threat model, and machine-readable abstract design
- Phase 4 baseline semantics and deterministic adversarial regression tests
- Phase 5 independent-review handoff and 21-oracle freeze candidate
- Phase 6 provisional T1 bounded-resynchronization controller
- Phase 7 seeded and explicit fault schedules with contact-window metrics
- Phase 8 descriptive analysis, trace audit, and sensitivity tooling
- Phases 9–13 bounded formal execution, cross-validation, adverse witnesses, and diagnostic outcome expansion
- Phase 14 independent-review package and claims traceability
- Phase 15 protocol, data dictionary, capture controls, readiness tracker, and issue register
- WP15-D1 B0/B1/B2 metric and capture parity
- WP15-D2 treatment-comparability matrix and semantic projection
- WP15-D3 executable qualified-family population and derived dataset
- WP15-D3B immutable pilot-bundle integration implementation

## Phase 15 checkpoint summary

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D2_LOCAL_VALIDATION=PASS
WP15-D3_LOCAL_VALIDATION=PASS
WP15-D3B_IMPLEMENTATION=COMPLETE_PENDING_LOCAL_AND_CI_VALIDATION
FAMILY_SPECIFIC_DESCRIPTIVE_COMPARISON=NOT_YET_AUTHORIZED
POOLED_CROSS_TREATMENT_AGGREGATION=NOT_PERMITTED
PUBLICATION_EVIDENCE=false
```

### WP15-D1

B0, B1, and B2 execute through a deterministic adapter that preserves all 21 retained design oracles and emits the shared T1 metric fields, JSON, CSV, event evidence, configuration/catalog provenance, and checksums.

Local evidence retained before D3B:

- 199 tests passed;
- 21 baseline scenarios matched retained design oracles;
- 21 unique scenario hashes;
- JSON/CSV consistency;
- integrated T1, baseline, and analysis processes exited zero; and
- the repository manifest verified at 163 entries.

Status:

`BASELINE_METRIC_CAPTURE_PARITY_LOCALLY_VALIDATED_CI_PENDING`

### WP15-D2

The semantic matrix defines eight families:

- four `QUALIFIED_MATCH` families;
- four `DIAGNOSTIC_FAMILY_ONLY` families;
- no `FULL_MATCH` family.

All 21 baseline and 15 T1 catalog scenarios have exactly one disposition. Raw epoch-bearing alignment, contact duration, divergent/degraded window counts, transmissions, retries, and all other unauthorized fields are excluded from cross-treatment projection.

Local evidence:

- 8 focused tests passed;
- 207 total tests passed at the D2 checkpoint;
- all 36 catalog dispositions were unique and complete; and
- the repository manifest verified at 169 entries.

Status:

`TREATMENT_COMPARABILITY_MATRIX_LOCALLY_VALIDATED_CI_PENDING`

### WP15-D3

Only CF-01, CF-02, CF-05, and CF-06 execute in the derived population.

Population:

| Family | Member rows | Analysis units |
|---|---:|---:|
| CF-01 | 4 | 4 |
| CF-02 | 5 | 4 |
| CF-05 | 2 | 2 |
| CF-06 | 2 | 2 |
| **Total** | **13** | **12** |

The two CF-02 B1 policy variants remain separate member rows but share one B1 analysis unit. They are not independent replications.

Local evidence:

- 9 focused D3 tests passed;
- 216 total tests passed at the D3 checkpoint;
- the standalone D3 validator passed;
- the 13-row JSON and CSV outputs matched;
- the derived checksum manifest verified; and
- the repository manifest verified at 175 entries.

Status:

`EXECUTABLE_MATCHED_FAMILY_POPULATION_LOCALLY_VALIDATED_CI_PENDING`

D3 member-level projection is internal validation evidence only. Family-specific descriptive comparison remains unauthorized.

## WP15-D3B status

### Immutable pilot-bundle integration

D3B integrates the validated D3 population into `experiments/scripts/run_phase15_pilot_capture.py`.

The wrapper now retains byte-for-byte copies of:

- Phase 15 T1 pilot configuration;
- baseline-parity configuration;
- D3 matched-family configuration;
- D2 comparability matrix;
- Phase 15 protocol candidate;
- Phase 08 analysis configuration;
- baseline catalog; and
- T1 catalog.

D3 executes only when both T1 and baseline processes exit zero. The wrapper then performs an independent capture-side validation of D3 files, internal checksums, population counts, JSON/CSV identity, denominators, source digests, and claim boundaries.

D3B metadata schema `0.2.0` records retained D2/D3/T1-catalog paths and SHA-256 values, exact command, process and capture-validation exit codes, D3 status, output paths, internal-manifest digest, and population counts.

D3B status:

`IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

Success requires:

`COMPLETED_AND_VERIFIED`

Fail-closed statuses are:

- `SKIPPED_PREREQUISITE_FAILURE`;
- `PROCESS_FAILED`; and
- `OUTPUT_VALIDATION_FAILED`.

## Immutable capture layers

The integrated run directory contains:

- `config/` retained inputs;
- `raw/` T1 and baseline outputs;
- `derived/` D3 JSON, member CSV, denominator CSV, and internal manifest;
- `analysis/` Phase 08 descriptive outputs;
- `governance/` metadata, exclusions, and reruns;
- `logs/` commands, stdout, stderr, environment, and Git state; and
- `manifests/` raw, derived, analysis, and complete-bundle manifests.

Checksum hierarchy:

1. D3 internal manifest protects its JSON and two CSV files.
2. `manifests/derived.sha256` protects the complete D3 directory, including the internal manifest.
3. `manifests/run-bundle.sha256` protects all retained files except itself.

The wrapper also verifies `raw.sha256` and `analysis.sha256`.

## Analysis and claim boundary

Authorized now:

- engineering validation;
- member-level family projection for internal validation;
- family coverage and analysis-unit counting;
- reproducibility and checksum auditing; and
- manuscript method/limitation drafting without result conclusions.

Not authorized:

```text
family_specific_descriptive_comparison=NOT_YET_AUTHORIZED
pooled_cross_treatment_aggregation=NOT_PERMITTED
success_rate_or_percentage=NOT_PERMITTED
inferential_statistics=NOT_PERMITTED
treatment_superiority=NOT_PERMITTED
cryptographic_security_or_pcs=NOT_PERMITTED
independent_validation=NOT_PERMITTED
publication_evidence=NOT_PERMITTED
```

## Review status

- Phase 14 package: `READY_FOR_OUTREACH_NOT_REVIEWED`
- Reviewer issue: `#3`, open
- Reviewer accepted a defined scope: no
- Independent cryptography review completed: no
- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Oracle freeze: `NOT_PERMITTED`
- Formal model: not independently reviewed
- T1 treatment: `PROVISIONAL_INTERNAL_REVIEW_ONLY`

No external review, approval, endorsement, or publication permission is implied.

## Open governance findings

### GOV-01 — Historical response-template omission

The Phase 04 gate contains 16 questions, while the historical Phase 05 template contains 15 and omitted the endpoint-knowledge question now identified as `B1-R5`. Phase 14 restores it without rewriting historical evidence.

### GOV-02 — Retrospective provisional T1 work

Phases 6–13 proceeded as provisional internal work after an earlier gate stated that T1 work was blocked pending independent review. A future reviewer must determine retrospective revalidation scope.

### GOV-03 — Implementation lock versus approval

“Corrected and locked” describes an internal implementation decision only. It is not independent approval, oracle freeze, or publication permission.

### GOV-04 — Review-target commit drift

Any future completed review must identify the exact commit reviewed and repeat that SHA in the response record.

## Allowed Phase 15 work while review remains open

- protocol, matrix, data-dictionary, and capture-control development;
- baseline instrumentation and matched-family execution;
- immutable capture integration;
- unit, regression, validator, formal, and checksum testing;
- disposable pilot and reproducibility runs;
- exploratory member-level inspection labeled non-comparative;
- manuscript methods, limitations, disclosure, and reproducibility drafting; and
- reviewer-outreach administration without implying participation.

## Mandatory stop points

Independent review and correction closure remain mandatory before claiming:

- approved baseline mappings or frozen oracles;
- external validation;
- formal completeness, refinement, or implementation equivalence;
- cryptographic security or PCS;
- CCSDS/SDLS conformance;
- flight, RF, or operational-spacecraft applicability; or
- treatment effectiveness or superiority.

Separate internal gates remain mandatory before:

- viewing or reporting family-level comparative aggregates;
- defining success percentages;
- running inferential statistics;
- beginning the publication-candidate experiment;
- extracting final manuscript result values; or
- describing pilot outputs as publication evidence.

## Phase 15 primary artifacts

- `spec/phase-15-experiment-protocol-candidate.json`
- `spec/phase-15-treatment-comparability-matrix.json`
- `spec/phase-15-d3b-capture-integration.json`
- `experiments/configs/phase-15-pilot.json`
- `experiments/configs/phase-15-baseline-parity.json`
- `experiments/configs/phase-15-matched-family-population.json`
- `experiments/scripts/run_phase15_pilot_capture.py`
- `experiments/scripts/run_phase15_matched_family_population.py`
- `experiments/scripts/validate_phase15_d3b_capture_integration.py`
- `docs/phase-15-d3b-capture-integration.md`
- `src/ttc_recovery/baseline_metrics.py`
- `src/ttc_recovery/treatment_comparability.py`
- `src/ttc_recovery/matched_family_population.py`
- `tests/test_phase15_capture.py`
- `.github/workflows/phase15-comparability.yml`
- `tracker/PHASE15_PUBLICATION_READINESS_TRACKER.md`
- `tracker/RESEARCH_ISSUES_AND_DISCLOSURES.md`

## Immediate next work

1. Pull the D3B implementation checkpoint.
2. Parse the protocol, D2, D3, and D3B JSON contracts.
3. Run focused capture and protocol tests.
4. Run D2, D3, D3B, and Phase 15 validators.
5. Run the complete Python regression suite.
6. Execute a disposable integrated capture from a clean Git state.
7. Verify retained D2/D3/T1-catalog hashes, D3 counts, closed gates, and all five checksum checks.
8. Refresh the tracked-file manifest only after every D3B check passes.
9. Keep the Phase 15 pull request unopened until explicit authorization.

## Deferred

- D3B local and CI validation
- completed independent cryptography review
- completed formal-methods review where required
- frozen baseline and T1 oracles
- family-level descriptive comparison authorization
- frozen denominators, observation cutoffs, and analysis plan
- publication-candidate experiment
- publication-grade comparative evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- final manuscript results and submission
