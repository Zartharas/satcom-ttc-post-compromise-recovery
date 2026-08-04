# WP15-D4 Freeze Candidate Tracker

**Branch:** `phase-15/publication-preparation`  
**Status:** `LOCALLY_VALIDATED_CI_AND_FREEZE_REVIEW_PENDING_NOT_ANALYSIS_EVIDENCE`  
**Publication evidence:** `false`

## Objective

Predeclare the family-level observation cutoffs, member registry, treatment-within-family analysis units, denominator membership, allowed display candidates, and revision rules before any family member values or comparative aggregates are viewed.

## Implemented artifacts

- `experiments/configs/phase-15-family-descriptive-plan.json`
- `docs/phase-15-d4-family-descriptive-analysis-plan.md`
- `src/ttc_recovery/family_descriptive_plan.py`
- `experiments/scripts/run_phase15_family_descriptive_plan.py`
- `experiments/scripts/validate_phase15_family_descriptive_plan.py`
- `tests/test_phase15_family_descriptive_plan.py`
- `.github/workflows/phase15-comparability.yml`

## Candidate population

| Family | Member rows | Analysis units | Cutoff |
|---|---:|---:|---|
| CF-01 | 4 | 4 | `OC-CF01-TERMINAL-ORACLE` |
| CF-02 | 5 | 4 | `OC-CF02-NO-FAULT-COMPLETION` |
| CF-05 | 2 | 2 | `OC-CF05-STATUS-OPPORTUNITY` |
| CF-06 | 2 | 2 | `OC-CF06-SINGLE-REPLAY` |
| **Total** | **13** | **12** | **4 unique cutoffs** |

CF-02 B1-01 and B1-05 remain separate traceability rows under one `CF-02:B1` candidate denominator unit.

## Outcome-blind controls

- `projected_metric_values_read=false`
- `raw_execution_values_read=false`
- `outcome_dependent_branching=false`
- member values are not emitted;
- raw execution values are not emitted;
- no outcome-frequency table is generated;
- no denominator is changed based on a result; and
- mutation of projected values must not change the D4 identity contract.

## Freeze state

```text
observation_cutoffs=CANDIDATE_NOT_FROZEN
analysis_unit_denominators=CANDIDATE_NOT_FROZEN
member_registry=CANDIDATE_NOT_FROZEN
allowed_displays=CANDIDATE_NOT_FROZEN
publication_analysis_plan=NOT_FROZEN
```

## Closed gates

```text
family_specific_descriptive_comparison=NOT_YET_AUTHORIZED
success_rate_denominator=NOT_DEFINED
pooled_cross_treatment_aggregation=NOT_PERMITTED
success_rate_or_percentage=NOT_PERMITTED
inferential_statistics=NOT_PERMITTED
treatment_superiority=NOT_PERMITTED
causal_interpretation=NOT_PERMITTED
cryptographic_security_or_pcs=NOT_PERMITTED
publication_evidence=false
```

## Generated candidate outputs

- `phase-15-family-descriptive-plan-candidate.json`
- `phase-15-family-member-registry.csv`
- `phase-15-family-analysis-units.csv`
- `phase-15-family-observation-plans.csv`
- `phase-15-family-descriptive-plan.sha256`

The member registry contains no outcome column and no projected-metric value field.

## Local validation evidence

- [x] D4 JSON contract parsed.
- [x] Exact D2/D4 allowed-field membership and order verified.
- [x] Ten focused D4 tests passed.
- [x] D4 validator passed.
- [x] Standalone D4 candidate bundle generated.
- [x] Four families, 13 member rows, 12 analysis units, and 4 cutoffs verified.
- [x] Outcome-blind mutation test passed.
- [x] Four-file D4 manifest verified.
- [x] Phase 15 protocol tests and validator passed.
- [x] Complete 236-test regression suite passed.
- [x] Tracked-file manifest validated at 185 entries.
- [ ] CI validation remains pending.
- [ ] Explicit freeze review remains pending.

## Current validated state

```text
WP15-D4_LOCAL_VALIDATION=PASS
FAMILY_ANALYSIS_FREEZE_CANDIDATE=LOCALLY_VALIDATED
OBSERVATION_CUTOFF_FREEZE=CANDIDATE_NOT_FROZEN
DENOMINATOR_FREEZE=CANDIDATE_NOT_FROZEN
FAMILY_VALUE_DISPLAY=NOT_YET_AUTHORIZED
RIT-017=FIXED_PENDING_CI_AND_FREEZE_REVIEW
RIT-018=FIXED_PENDING_CI
PUBLICATION_EVIDENCE=false
```

## Future decision gate

D4 local and CI validation does not freeze the candidate. A separate, explicit review must decide whether to:

1. accept the exact cutoffs and denominator units;
2. revise them before any comparative display is viewed; or
3. keep family comparison closed.

No implicit freeze is permitted.
