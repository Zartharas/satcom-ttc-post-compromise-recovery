# Project Status

## Current phase

Phase 15 prepares a reproducible synthetic experiment protocol, immutable capture workflow, qualified-family execution layer, outcome-blind analysis-freeze candidate, and manuscript foundation while preserving every unresolved independent-review and publication-claim gate.

Current overall status:

```text
PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE
```

The work does not change Phase 14 review status, freeze baseline oracles, establish cryptographic security, authorize family-value displays, or authorize publication conclusions.

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
- WP15-D3B immutable pilot-bundle integration
- WP15-D4 outcome-blind observation-cutoff and denominator freeze candidate implementation

## Phase 15 checkpoint summary

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D2_LOCAL_VALIDATION=PASS
WP15-D3_LOCAL_VALIDATION=PASS
WP15-D3B_LOCAL_VALIDATION=PASS
WP15-D4_LOCAL_VALIDATION=PASS
OBSERVATION_CUTOFF_FREEZE=CANDIDATE_NOT_FROZEN
DENOMINATOR_FREEZE=CANDIDATE_NOT_FROZEN
FAMILY_SPECIFIC_DESCRIPTIVE_COMPARISON=NOT_YET_AUTHORIZED
POOLED_CROSS_TREATMENT_AGGREGATION=NOT_PERMITTED
PUBLICATION_EVIDENCE=false
```

### WP15-D1

B0, B1, and B2 execute through a deterministic adapter that preserves all 21 retained design oracles and emits the shared T1 metric fields, JSON, CSV, event evidence, configuration/catalog provenance, and checksums.

Local checkpoint evidence:

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

Local checkpoint evidence:

- 8 focused tests passed;
- 207 total tests passed;
- all 36 catalog dispositions were unique and complete; and
- the repository manifest verified at 169 entries.

Status:

`TREATMENT_COMPARABILITY_MATRIX_LOCALLY_VALIDATED_CI_PENDING`

### WP15-D3

Only CF-01, CF-02, CF-05, and CF-06 execute in the derived population.

| Family | Member rows | Analysis units |
|---|---:|---:|
| CF-01 | 4 | 4 |
| CF-02 | 5 | 4 |
| CF-05 | 2 | 2 |
| CF-06 | 2 | 2 |
| **Total** | **13** | **12** |

The two CF-02 B1 policy variants remain separate member rows but share one B1 analysis unit. They are not independent replications.

Local checkpoint evidence:

- 9 focused D3 tests passed;
- 216 total tests passed;
- the standalone D3 validator passed;
- the 13-row JSON and CSV outputs matched;
- the derived checksum manifest verified; and
- the repository manifest verified at 175 entries.

Status:

`EXECUTABLE_MATCHED_FAMILY_POPULATION_LOCALLY_VALIDATED_CI_PENDING`

D3 member-level projection is internal validation evidence only. Family-specific descriptive comparison remains unauthorized.

## WP15-D3B status

D3B retains exact D2/D3 contracts and both catalogs in the immutable pilot bundle. D3 executes only after successful T1 and baseline stages. Capture-side validation independently checks D3 files, internal checksums, population counts, JSON/CSV identity, denominators, source digests, and claim boundaries.

D3B local validation evidence:

- 10 focused capture tests passed;
- 13 Phase 15 protocol tests passed;
- 223 total tests passed;
- T1, baseline, D3, and analysis stages exited zero;
- D3 status was `COMPLETED_AND_VERIFIED`;
- metadata schema `0.2.0` and retained-input hashes verified;
- 4 families, 13 member rows, 12 analysis units, and 13 source executions were retained;
- D3 internal, raw, derived, analysis, and complete-bundle manifests verified; and
- the repository manifest verified at 178 entries.

Status:

`IMMUTABLE_D2_D3_CAPTURE_LOCALLY_VALIDATED_CI_PENDING`

## WP15-D4 status

D4 predeclares candidate observation cutoffs, exact member identities, treatment-within-family analysis units, denominator membership, allowed display candidates, and post-observation revision controls.

Candidate population:

| Family | Member rows | Analysis units | Cutoff |
|---|---:|---:|---|
| CF-01 | 4 | 4 | `OC-CF01-TERMINAL-ORACLE` |
| CF-02 | 5 | 4 | `OC-CF02-NO-FAULT-COMPLETION` |
| CF-05 | 2 | 2 | `OC-CF05-STATUS-OPPORTUNITY` |
| CF-06 | 2 | 2 | `OC-CF06-SINGLE-REPLAY` |
| **Total** | **13** | **12** | **4 unique cutoffs** |

D4 is outcome-blind by construction:

```text
projected_metric_values_read=false
raw_execution_values_read=false
outcome_dependent_branching=false
```

The generator uses only identity, family membership, allowed-field names, analysis-unit membership, source-execution digests, coverage, and closed authorization flags. It does not emit member values or outcome aggregates.

D4 local validation evidence:

- authoritative D2/D4 allowed-field parity passed for all four qualified families;
- 10 focused D4 tests passed;
- standalone D4 candidate generation completed;
- the four-file D4 checksum manifest verified;
- D2, D3, D3B, D4, and Phase 15 validators passed;
- 236 total tests passed; and
- the repository manifest verified at 185 entries before closeout-status reconciliation.

Status:

`FAMILY_ANALYSIS_FREEZE_CANDIDATE_LOCALLY_VALIDATED_CI_PENDING`

Freeze state:

```text
observation_cutoffs=CANDIDATE_NOT_FROZEN
analysis_unit_denominators=CANDIDATE_NOT_FROZEN
member_registry=CANDIDATE_NOT_FROZEN
allowed_displays=CANDIDATE_NOT_FROZEN
publication_analysis_plan=NOT_FROZEN
```

Local and CI validation do not implicitly freeze D4. A separate explicit review decision is required before any family member value display is authorized.

## Immutable capture layers

The integrated D3B run directory contains:

- `config/` retained inputs;
- `raw/` T1 and baseline outputs;
- `derived/` D3 JSON, member CSV, denominator CSV, and internal manifest;
- `analysis/` Phase 08 descriptive outputs;
- `governance/` metadata, exclusions, and reruns;
- `logs/` commands, stdout, stderr, environment, and Git state; and
- `manifests/` raw, derived, analysis, and complete-bundle manifests.

D4 is currently a standalone outcome-blind plan-candidate generator. Immutable D4 capture integration is not implied by this work package.

## Analysis and claim boundary

Authorized now:

- engineering validation;
- member-level family projection for internal validation;
- outcome-blind plan generation;
- family/member/analysis-unit identity validation;
- candidate observation-cutoff and denominator registry generation;
- reproducibility and checksum auditing; and
- manuscript method/limitation drafting without result conclusions.

Not authorized:

```text
family_specific_descriptive_comparison=NOT_YET_AUTHORIZED
observation_cutoff_freeze=CANDIDATE_NOT_FROZEN
denominator_freeze=CANDIDATE_NOT_FROZEN
success_rate_denominator=NOT_DEFINED
pooled_cross_treatment_aggregation=NOT_PERMITTED
success_rate_or_percentage=NOT_PERMITTED
inferential_statistics=NOT_PERMITTED
treatment_superiority=NOT_PERMITTED
causal_interpretation=NOT_PERMITTED
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

No external review, approval, endorsement, freeze, or publication permission is implied.

## Open governance findings

### GOV-01 — Historical response-template omission

The Phase 04 gate contains 16 questions, while the historical Phase 05 template contains 15 and omitted the endpoint-knowledge question now identified as `B1-R5`. Phase 14 restores it without rewriting historical evidence.

### GOV-02 — Retrospective provisional T1 work

Phases 6–13 proceeded as provisional internal work after an earlier gate stated that T1 work was blocked pending independent review. A future reviewer must determine retrospective revalidation scope.

### GOV-03 — Implementation lock versus approval

“Corrected and locked” describes an internal implementation decision only. It is not independent approval, oracle freeze, analysis-plan freeze, or publication permission.

### GOV-04 — Review-target commit drift

Any future completed review must identify the exact commit reviewed and repeat that SHA in the response record.

## Allowed Phase 15 work while review remains open

- protocol, matrix, data-dictionary, and capture-control development;
- baseline instrumentation and matched-family execution;
- immutable capture integration;
- outcome-blind observation and denominator plan development;
- unit, regression, validator, formal, and checksum testing;
- disposable pilot and reproducibility runs;
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

Separate explicit internal gates remain mandatory before:

- freezing D4 observation cutoffs or denominators;
- displaying family member values side by side;
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
- `experiments/configs/phase-15-family-descriptive-plan.json`
- `experiments/scripts/run_phase15_pilot_capture.py`
- `experiments/scripts/run_phase15_matched_family_population.py`
- `experiments/scripts/run_phase15_family_descriptive_plan.py`
- `experiments/scripts/validate_phase15_d3b_capture_integration.py`
- `experiments/scripts/validate_phase15_family_descriptive_plan.py`
- `docs/phase-15-d3b-capture-integration.md`
- `docs/phase-15-d4-family-descriptive-analysis-plan.md`
- `src/ttc_recovery/baseline_metrics.py`
- `src/ttc_recovery/treatment_comparability.py`
- `src/ttc_recovery/matched_family_population.py`
- `src/ttc_recovery/family_descriptive_plan.py`
- `tests/test_phase15_capture.py`
- `tests/test_phase15_family_descriptive_plan.py`
- `.github/workflows/phase15-comparability.yml`
- `tracker/PHASE15_PUBLICATION_READINESS_TRACKER.md`
- `tracker/WP15_D4_FREEZE_CANDIDATE_TRACKER.md`
- `tracker/RESEARCH_ISSUES_AND_DISCLOSURES.md`

## Immediate next work

1. Record the validated D4 checkpoint and refreshed repository manifest.
2. Preserve the disposable D4 bundle in the ignored compliance archive.
3. Keep D4 cutoffs, denominators, and displays candidate-only.
4. Run CI only after explicit pull-request authorization.
5. Prepare the separate accept, revise, or reject decision for the D4 freeze candidate.
6. Keep the Phase 15 pull request unopened until explicit authorization.

## Deferred

- D4 CI validation
- explicit D4 cutoff/denominator freeze decision
- completed independent cryptography review
- completed formal-methods review where required
- frozen baseline and T1 oracles
- family-level descriptive comparison authorization
- publication-candidate experiment
- publication-grade comparative evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- final manuscript results and submission
