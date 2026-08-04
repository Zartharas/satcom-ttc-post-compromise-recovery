# Separate WP15-D4 Freeze Review

## Status

`REVIEW_PACKAGE_DEFINED_DECISION_PENDING_NOT_FROZEN`

This review evaluates the locally validated WP15-D4 freeze candidate at checkpoint `34d63a5`. It does not itself accept, freeze, or authorize the candidate.

Machine-readable review contract:

`spec/phase-15-d4-freeze-review.json`

Validator:

`experiments/scripts/validate_phase15_d4_freeze_review.py`

## Purpose

WP15-D4 predeclared four family-specific observation cutoffs, 13 member identities, 12 treatment-within-family analysis units, denominator behavior, allowed planning displays, and post-observation revision controls. Local engineering validation established that the candidate is internally consistent and outcome-blind.

The separate freeze review asks a different question: should the exact validated candidate be accepted, revised, rejected, or deferred before any family member values are viewed side by side?

## Review target

The review target is fixed as:

```text
branch=phase-15/publication-preparation
validated_checkpoint=34d63a5
candidate=experiments/configs/phase-15-family-descriptive-plan.json
matrix=spec/phase-15-treatment-comparability-matrix.json
```

A later change is not covered by this review unless the review target is updated and the complete validation and review process is repeated.

## Outcome-blind review boundary

The reviewer may inspect:

- the D2 and D4 machine-readable contracts;
- family, member-row, and analysis-unit identifiers;
- cutoff identifiers and cutoff wording;
- allowed field names without values;
- validation and checksum results;
- issue and governance records; and
- source commits and file hashes.

The reviewer must not inspect:

- projected metric values;
- raw execution values;
- family outcome distributions;
- success counts or percentages;
- treatment rankings;
- effect estimates;
- confidence intervals; or
- hypothesis-test results.

This boundary prevents observed results from influencing cutoff, denominator, or display decisions.

## Objects under review

The review covers only:

1. the family order CF-01, CF-02, CF-05, and CF-06;
2. the 13 member-row identities;
3. the 12 treatment-within-family analysis units;
4. the four observation cutoffs;
5. exact D2-authorized field-name lists;
6. missing-unit and extra-unit behavior;
7. the planning-display registry; and
8. post-observation revision controls.

It does not review treatment effectiveness, security strength, operational suitability, cryptographic PCS, or publication conclusions.

## Decision options

### ACCEPT

Accept freezes only the exact reviewed:

- observation cutoffs;
- member registry;
- treatment-within-family analysis-unit denominators; and
- planning-display registry.

Acceptance does not authorize family member values, success rates, pooled aggregation, inference, superiority, or publication evidence.

### REVISE

Revision preserves the current candidate, creates a new versioned pre-observation candidate, records the rationale, and repeats local validation and freeze review before any family-value display.

### REJECT

Rejection preserves the candidate and rationale but keeps family comparison closed.

### DEFER

Deferral preserves the current candidate and keeps all freeze and display gates closed pending additional non-outcome evidence.

## Review questions

The machine contract contains 16 questions covering:

- exact review-target identity;
- outcome blindness;
- family and member completeness;
- analysis-unit semantics;
- CF-02 policy-variant handling;
- each of the four cutoffs;
- exact D2 field parity;
- missing and extra analysis-unit behavior;
- planning-display limits;
- revision control; and
- claim boundaries.

Each question must be answered with one of:

```text
PASS
FAIL
NEEDS_REVISION
DEFER
```

Every answer requires a rationale.

## Acceptance prerequisites

An `ACCEPT` decision requires all of the following:

- all 16 questions answered `PASS`;
- exact reviewed commit recorded;
- local validation passed;
- CI validation passed;
- reviewer and UTC decision date recorded;
- explicit rationale recorded; and
- a separately committed decision record.

Implicit acceptance is prohibited.

## Current state

```text
current_decision=PENDING
decision_authorized=false
observation_cutoffs=CANDIDATE_NOT_FROZEN
analysis_unit_denominators=CANDIDATE_NOT_FROZEN
member_registry=CANDIDATE_NOT_FROZEN
allowed_displays=CANDIDATE_NOT_FROZEN
family_member_value_display=NOT_YET_AUTHORIZED
family_specific_descriptive_comparison=NOT_YET_AUTHORIZED
success_rate_denominator=NOT_DEFINED
publication_evidence=false
```

## Claim boundary

This review cannot authorize:

- member-value display;
- success counts or percentages;
- pooled or cross-family aggregation;
- inferential statistics;
- treatment ranking or superiority;
- causal interpretation;
- cryptographic-security or PCS claims;
- independent validation; or
- publication evidence.

Those remain separate future gates even if the freeze candidate is later accepted.
