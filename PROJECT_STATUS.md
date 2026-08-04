# Project Status

## Completed

- Phases 1–3 related work, threat model, and machine-readable abstract design
- Phase 04 baseline semantics and corrected B1/B2 deterministic fault tests
- Phase 05 independent-review handoff and 21-oracle freeze candidate
- Phase 06 provisional T1 bounded-resynchronization controller
- Phase 07 seeded and explicit fault schedules with recovery metrics
- Phase 08 provisional analysis, trace audit, and sensitivity framework
- Phases 9–13 bounded formal execution, cross-validation, adverse witnesses, and diagnostic expansion
- Phase 14 independent-review and claims-traceability package
- Phase 15 publication-readiness and engineering-issue trackers
- Phase 15 protocol, data dictionary, capture controls, and immutable pilot wrapper
- WP15-D1 B0/B1/B2 metric and capture parity
- WP15-D1 local validation: 199 tests, 21 scenarios, layered capture manifests, 163-entry repository manifest
- WP15-D2 matched treatment-scenario and semantic-comparability matrix
- WP15-D2 local validation: 207 tests, 8 families, 36 unique dispositions, 169-entry repository manifest at `0cd96a8`
- WP15-D3 executable qualified-family population implementation

## Current phase

Phase 15 prepares the controlled experiment population, capture controls, pilot workflow, and manuscript method required before a defensible publication-candidate run.

Current status:

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

Phase 15 does not change the Phase 14 review result, baseline oracles, T1 transition semantics, or hard claim boundaries.

## Current checkpoints

```text
WP15-D1_LOCAL_VALIDATION=PASS
WP15-D1_CI_VALIDATION=PENDING
WP15-D2_LOCAL_VALIDATION=PASS
WP15-D2_CI_VALIDATION=PENDING
WP15-D3_IMPLEMENTATION=COMPLETE_PENDING_LOCAL_VALIDATION
WP15-D3_CAPTURE_INTEGRATION=DEFERRED_PENDING_STANDALONE_VALIDATION
FAMILY_SPECIFIC_DESCRIPTIVE_COMPARISON=NOT_YET_AUTHORIZED
POOLED_CROSS_TREATMENT_AGGREGATION=NOT_PERMITTED
PUBLICATION_EVIDENCE=false
```

## WP15-D1 — Metric and capture parity

B0, B1, and B2 execute through a deterministic adapter that:

- runs all 21 retained catalog scenarios;
- checks alignment, joint state when declared, and outcome design oracles;
- emits the shared metric field set;
- retains treatment, variant, and scenario identity;
- uses null seeds for deterministic baseline rows;
- creates canonical scenario SHA-256 identities;
- writes JSON and CSV;
- preserves event logs and provenance; and
- is included in the immutable Phase 15 pilot bundle.

Status:

`BASELINE_METRIC_CAPTURE_PARITY_LOCALLY_VALIDATED_CI_PENDING`

Metric-field and capture parity do not establish semantic or treatment comparability.

## WP15-D2 — Semantic comparability

WP15-D2 defines:

- four `QUALIFIED_MATCH` families;
- four `DIAGNOSTIC_FAMILY_ONLY` families;
- no `FULL_MATCH` classification;
- one disposition for every one of the 21 baseline and 15 T1 catalog scenarios;
- family-specific allowed fields;
- treatment-specific and non-outcome-guard exclusions; and
- a normalized `alignment_class` projection.

The matrix prohibits:

- raw epoch-bearing alignment comparison;
- contact-duration, divergent-window, transmission, and retry comparison;
- pooling the curated baseline catalog with the seeded T1 pilot;
- catalog success percentages;
- treating B1 policy variants as independent replications;
- quantitative aggregation of diagnostic-only families; and
- any field not explicitly authorized by a family.

Status:

`TREATMENT_COMPARABILITY_MATRIX_LOCALLY_VALIDATED_CI_PENDING`

## WP15-D3 — Executable qualified-family population

WP15-D3 executes only CF-01, CF-02, CF-05, and CF-06.

Population:

| Family | Member rows | Analysis units | Status |
|---|---:|---:|---|
| CF-01 | 4 | 4 | Implemented pending validation |
| CF-02 | 5 | 4 | Implemented pending validation |
| CF-05 | 2 | 2 | Implemented pending validation |
| CF-06 | 2 | 2 | Implemented pending validation |
| **Total** | **13** | **12** |  |

CF-02 retains both B1 policy variants as separate source rows, but both share the `CF-02:B1` analysis unit. They are not independent replicates.

### Execution

- Baseline members use the existing oracle-checking baseline adapter.
- T1-01 executes no-fault ground-ahead recovery.
- T1-09 executes post-convergence status loss.
- T1-13 executes successful recovery followed by replay of the retained last commit.
- T1-15 executes equal-epoch recovery with initially compromised operational keys.
- Every source execution is checked against the retained internal catalog oracle.
- Every source execution receives a deterministic SHA-256 digest.

### Derived dataset

Each member row contains only the metric fields allowed by its D2 family. Raw alignment, duration, transmissions, retries, and all unauthorized fields are omitted.

Outputs:

- `phase-15-matched-family-population.json`
- `phase-15-matched-family-members.csv`
- `phase-15-matched-family-denominators.csv`
- `phase-15-matched-family-derived.sha256`

The denominator file is a coverage record only:

- member-row count is recorded;
- unique treatment-family analysis units are recorded;
- policy-variant rows are recorded;
- success-rate denominator remains `NOT_DEFINED`; and
- aggregate authorization remains `false`.

Status:

`EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_LOCAL_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

The D3 artifacts are not yet integrated into the immutable pilot wrapper. That integration is intentionally deferred until the standalone runner, tests, validator, and derived manifest pass locally.

## Capture status

The existing Phase 15 wrapper has already been locally validated for:

- exact protocol and configurations;
- retained baseline catalog;
- Git and environment state;
- T1 seeded outputs;
- baseline-adapter outputs;
- T1 analysis outputs;
- commands, logs, exclusions, reruns, and metadata; and
- raw, analysis, and full-bundle manifests.

Status:

`PHASE15_CAPTURE_WRAPPER_LOCALLY_VALIDATED_CI_PENDING`

D3 capture integration remains:

`DEFERRED_PENDING_STANDALONE_LOCAL_VALIDATION`

## Review status

- Phase 14 package: `READY_FOR_OUTREACH_NOT_REVIEWED`
- Reviewer issue: `#3`, open
- Qualified reviewer accepted a defined scope: no
- Permission to identify a reviewer publicly: no
- Independent cryptography review: not performed
- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Oracle freeze: `NOT_PERMITTED`
- T1 status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Formal model: `NOT_INDEPENDENTLY_REVIEWED`

The following remain prohibited:

- independently accepted baseline mappings;
- cryptographic proof or post-compromise-security claims;
- formal completeness or implementation equivalence;
- causal or treatment-superiority conclusions;
- family-level success rates without a predeclared denominator;
- pooled cross-treatment aggregation;
- CCSDS/SDLS conformance;
- flight, RF, or operational-spacecraft applicability; and
- publication evidence from Phase 15 pilot outputs.

## Open governance findings

### GOV-01 — incomplete historical response template

Phase 05 omitted the endpoint-knowledge question later identified as `B1-R5`. Phase 14 restores it without rewriting historical evidence.

### GOV-02 — retrospective provisional T1 work

Phases 6–13 proceeded provisionally after an earlier gate stated that T1 work was blocked pending review. A future reviewer must determine the required retrospective revalidation scope.

### GOV-03 — implementation lock versus independent approval

“Corrected and locked” is an internal implementation decision, not independent approval or publication permission.

### GOV-04 — review-target commit drift

Any future review must identify the exact commit reviewed and repeat it in the completed response.

## Allowed Phase 15 work while review remains open

- protocol, matrix, population, and data-dictionary development;
- unit, regression, validator, and bounded formal testing;
- baseline, T1, and matched-family pipeline validation;
- immutable capture and checksum work;
- pilot execution after Gate P1;
- exploratory analysis labeled provisional;
- manuscript method, limitations, disclosure, and reproducibility drafting.

## Mandatory stop points

Independent review and correction closure remain mandatory before claiming external acceptance, oracle freeze, cryptographic security, formal completeness, implementation equivalence, conformance, or operational applicability.

Separate internal gates remain mandatory before:

- integrating unvalidated D3 outputs into the retained pilot bundle;
- authorizing family-specific descriptive comparison;
- defining or computing success percentages;
- viewing comparative publication aggregates;
- beginning publication-candidate execution; or
- extracting final manuscript result values.

## Phase 15 artifacts

- `spec/phase-15-experiment-protocol-candidate.json`
- `spec/phase-15-treatment-comparability-matrix.json`
- `experiments/configs/phase-15-pilot.json`
- `experiments/configs/phase-15-baseline-parity.json`
- `experiments/configs/phase-15-matched-family-population.json`
- `docs/phase-15-treatment-comparability.md`
- `docs/phase-15-matched-family-population.md`
- `src/ttc_recovery/baseline_metrics.py`
- `src/ttc_recovery/treatment_comparability.py`
- `src/ttc_recovery/matched_family_population.py`
- `experiments/scripts/run_phase15_matched_family_population.py`
- `experiments/scripts/validate_phase15_matched_family_population.py`
- `tests/test_phase15_matched_family_population.py`
- `tracker/PHASE15_PUBLICATION_READINESS_TRACKER.md`
- `tracker/RESEARCH_ISSUES_AND_DISCLOSURES.md`

## Next internal work

1. Validate the WP15-D3 JSON contract.
2. Run the focused D3 tests and standalone validator.
3. Execute the standalone D3 runner and audit all 13 rows and 12 analysis units.
4. Verify the derived checksum manifest and deterministic source digests.
5. Run the complete regression suite.
6. Refresh the tracked-file manifest only after D3 passes.
7. Integrate D3 into the immutable pilot bundle after standalone validation.
8. Keep the pull request unopened until explicit authorization.
