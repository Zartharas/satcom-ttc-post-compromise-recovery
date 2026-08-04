# Phase 15 Executable Matched-Family Population

## Status

Machine-output status:

`EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

Engineering checkpoint:

`LOCALLY_VALIDATED_CI_PENDING`

WP15-D3 converts the four `QUALIFIED_MATCH` families from the WP15-D2 semantic matrix into a reproducible member-level execution population. It does not authorize comparative conclusions, pooled aggregation, success-rate calculations, inferential statistics, treatment-superiority claims, cryptographic-security claims, or publication evidence.

Machine-readable execution contract:

`experiments/configs/phase-15-matched-family-population.json`

Source semantic matrix:

`spec/phase-15-treatment-comparability-matrix.json`

Immutable-capture integration contract:

`spec/phase-15-d3b-capture-integration.json`

## Scope

Only these qualified families execute:

| Family | Topic | Member rows | Analysis units |
|---|---|---:|---:|
| CF-01 | Passive operational-key compromise followed by fresh recovery material | 4 | 4 |
| CF-02 | No-fault state transition or recovery completion | 5 | 4 |
| CF-05 | Post-convergence status telemetry loss | 2 | 2 |
| CF-06 | Replay after successful state advancement | 2 | 2 |
| **Total** |  | **13** | **12** |

CF-02 contains two B1 policy variants. They remain separate source rows for transparency but share `CF-02:B1`. They are not independent replicates.

Diagnostic-only families CF-03, CF-04, CF-07, and CF-08 are not emitted into the derived dataset.

## Execution sources

### Baseline members

B0, B1, and B2 execute through:

`src/ttc_recovery/baseline_metrics.py:run_baseline_scenario`

Before projection, the adapter verifies retained catalog alignment, joint state when declared, and outcome. D3 does not alter baseline transition semantics or outcome labels.

### T1 members

| Source | Exact behavior |
|---|---|
| T1-15 | Equal-epoch recovery with both active operational keys initially compromised |
| T1-01 | No-fault ground-ahead bounded recovery |
| T1-09 | Ground-ahead recovery with status telemetry dropped after convergence |
| T1-13 | Successful ground-ahead recovery followed by replay of the retained last commit |

Provenance seeds support deterministic identity only; `seed_is_comparable=false`.

T1-13 replays only after the original recovery reaches `SUCCESS`. The runner verifies rejection and no spacecraft state change.

## Member rows

Each row retains:

- unique `row_id`;
- family ID/name and `QUALIFIED_MATCH` classification;
- `analysis_unit_id`;
- treatment and source identity;
- source role;
- exact family `allowed_fields`;
- `projected_metrics` containing only allowed fields;
- source-execution SHA-256; and
- `publication_evidence=false`.

The JSON separately retains complete source execution records, raw metrics, event logs, execution parameters, internal design-oracle checks, and source digests.

## Projection rules

The runner:

1. executes the source;
2. verifies the retained internal design oracle;
3. derives `alignment_class` when authorized;
4. projects only family-allowed fields;
5. omits raw epoch-bearing alignment and unauthorized fields;
6. assigns the family-treatment analysis unit; and
7. retains complete source evidence separately.

Excluded from cross-treatment projection:

- raw `alignment`;
- `recovery_duration_contacts`;
- `divergent_contact_windows`;
- `degraded_contact_windows`;
- `total_transmissions`;
- `retry_overhead`;
- seed identity;
- schedule identity; and
- every field not explicitly permitted by the family.

## Denominator policy

The denominator table records coverage, not statistical analysis.

- Member row: one executed matrix member.
- Analysis unit: one treatment within one family.
- Policy variant: a retained row sharing a treatment-family analysis unit.
- Family coverage denominator: expected unique treatment analysis units.
- Success-rate denominator: `NOT_DEFINED`.
- Cross-family denominator: `NOT_PERMITTED`.
- Aggregate authorization: `false`.

No success percentage, pooled score, confidence interval, hypothesis test, effect estimate, or superiority ranking is produced.

## Outputs

The runner writes:

- `phase-15-matched-family-population.json`;
- `phase-15-matched-family-members.csv`;
- `phase-15-matched-family-denominators.csv`; and
- `phase-15-matched-family-derived.sha256`.

The member CSV serializes family-specific metrics in `projected_metrics_json`, preventing global comparison columns from implying universal field authorization.

## Standalone validation evidence

At the D3 checkpoint:

- 9 focused D3 tests passed;
- 216 total tests passed;
- the D3 validator passed;
- 4 families, 13 rows, and 12 analysis units were reproduced;
- member and denominator JSON/CSV identities matched;
- source-execution digests were deterministic;
- the internal derived manifest verified; and
- the repository manifest verified at 175 entries.

This evidence is internal engineering validation, not comparative or publication evidence.

## WP15-D3B integration

D3B now copies the exact D2 matrix, D3 configuration, baseline catalog, and T1 catalog into the immutable pilot bundle and passes those retained copies to the D3 runner.

D3 executes only after T1 and baseline processes succeed. Capture-side validation independently checks D3 files, internal checksums, counts, row identity, family coverage, denominator gates, JSON/CSV identity, source digests, and claim boundaries.

The D3 directory is protected by:

1. its internal manifest;
2. the run-level `manifests/derived.sha256`; and
3. the complete `manifests/run-bundle.sha256`.

D3B implementation status:

`IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

## Interpretation boundary

D3 establishes population plumbing and projection discipline. D3B establishes immutable provenance and fail-closed capture. Neither establishes equivalent cryptographic assumptions, initial states, message semantics, timing, cost, fault opportunities, causal effects, or operational applicability.

Family-specific descriptive comparison remains:

`NOT_YET_AUTHORIZED`

## Remaining blocker

RIT-014 is fixed pending D3B integrated validation and CI. RIT-016 tracks immutable D3 capture specifically. Publication-candidate execution remains blocked until D3B passes, the pilot is audited, observation cutoffs and denominators are frozen, and the analysis plan is versioned before aggregate review.
