# Phase 15 Executable Matched-Family Population

## Status

`EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

WP15-D3 converts the four `QUALIFIED_MATCH` families from the WP15-D2 semantic matrix into a reproducible member-level execution population. It does not authorize comparative conclusions, pooled aggregation, success-rate calculations, inferential statistics, treatment-superiority claims, cryptographic-security claims, or publication evidence.

The machine-readable execution contract is:

`experiments/configs/phase-15-matched-family-population.json`

The source semantic matrix remains:

`spec/phase-15-treatment-comparability-matrix.json`

## Scope

Only the following qualified families are executed:

| Family | Topic | Member rows | Analysis units |
|---|---|---:|---:|
| CF-01 | Passive operational-key compromise followed by fresh recovery material | 4 | 4 |
| CF-02 | No-fault state transition or recovery completion | 5 | 4 |
| CF-05 | Post-convergence status telemetry loss | 2 | 2 |
| CF-06 | Replay after successful state advancement | 2 | 2 |
| **Total** |  | **13** | **12** |

CF-02 contains two B1 policy variants. They are retained as separate source rows for transparency but share the same `CF-02:B1` analysis-unit identifier. They are not independent replicates.

The diagnostic-only families CF-03, CF-04, CF-07, and CF-08 are not emitted into the derived comparison dataset. They remain available for structured qualitative discussion only.

## Execution sources

### Baseline members

B0, B1, and B2 members execute through:

`src/ttc_recovery/baseline_metrics.py:run_baseline_scenario`

Before a baseline row is projected, the adapter verifies the retained catalog alignment, joint state when declared, and outcome oracle. WP15-D3 does not alter baseline transition semantics or outcome labels.

### T1 members

The selected T1 catalog members execute through explicit recipes recorded in the WP15-D3 configuration:

| Source | Exact behavior |
|---|---|
| T1-15 | Equal-epoch recovery with both active operational keys initially marked compromised |
| T1-01 | No-fault ground-ahead bounded recovery |
| T1-09 | Ground-ahead recovery with status telemetry dropped after convergence |
| T1-13 | Successful ground-ahead recovery followed by replay of the retained last commit |

Each recipe includes an integer provenance seed, but `seed_is_comparable=false`. These identifiers support deterministic traceability only and are excluded from cross-treatment interpretation.

T1-13 performs the replay only after the original recovery reaches `SUCCESS`. The runner verifies that the replay is rejected and does not change spacecraft epoch or active-key state.

## Derived row structure

Each member row contains:

- `row_id`;
- `family_id` and family name;
- `family_classification`;
- `analysis_unit_id`;
- treatment;
- source type and source identifier;
- source role;
- the exact family `allowed_fields` list;
- `projected_metrics` containing only those allowed fields;
- a SHA-256 digest of the complete source execution; and
- `publication_evidence=false`.

The complete JSON also retains source execution records, including baseline or T1 raw metrics, event logs, execution parameters, internal design-oracle checks, and source-execution digests.

## Projection rules

The projection source is each family’s `allowed_fields` array in the WP15-D2 matrix.

The runner:

1. executes the source member;
2. verifies the retained internal design oracle;
3. derives `alignment_class` from raw alignment when requested;
4. projects only the family-authorized fields;
5. omits raw epoch-bearing alignment and all other unauthorized fields;
6. assigns the family-treatment analysis unit; and
7. records the complete source execution separately from the member-level projection.

The following remain excluded from every cross-treatment projection:

- raw `alignment`;
- `recovery_duration_contacts`;
- `divergent_contact_windows`;
- `degraded_contact_windows`;
- `total_transmissions`;
- `retry_overhead`;
- seed identity;
- schedule identity; and
- any other field not explicitly permitted by that family.

## Denominator policy

The derived denominator table is a coverage table, not a statistical-analysis table.

- **Member row:** one executed matrix member.
- **Analysis unit:** one treatment within one family.
- **Policy variant:** a retained implementation-policy row sharing the treatment’s family analysis unit.
- **Family coverage denominator:** the number of unique treatment analysis units expected by the qualified family definition.
- **Success-rate denominator:** `NOT_DEFINED`.
- **Cross-family denominator:** `NOT_PERMITTED`.
- **Aggregate authorization:** `false`.

No treatment success percentage, pooled family score, confidence interval, hypothesis test, effect estimate, or superiority ranking is produced.

## Outputs

The standalone runner writes:

- `phase-15-matched-family-population.json`;
- `phase-15-matched-family-members.csv`;
- `phase-15-matched-family-denominators.csv`; and
- `phase-15-matched-family-derived.sha256`.

The member CSV uses a serialized `projected_metrics_json` field instead of global metric columns. This prevents fields authorized for one family from appearing as populated comparison columns for another family.

The denominator CSV records family coverage and analysis-unit counts while keeping `success_rate_denominator=NOT_DEFINED` and `aggregate_authorized=false`.

## Reproducibility controls

- The eligible family order is fixed as CF-01, CF-02, CF-05, and CF-06.
- The expected population is 13 member rows and 12 analysis units.
- Every source member must exist in the retained D2 matrix and its source catalog.
- Every source execution must match its retained internal design oracle.
- Every member row must have a unique identifier and source-execution digest.
- Repeated execution must produce identical source-execution SHA-256 values.
- The derived JSON and CSV files are protected by a dedicated SHA-256 manifest.
- Manifest tampering must be detected.

## Interpretation boundary

WP15-D3 establishes executable population plumbing and family-specific projection discipline. It does not establish that the treatments have equivalent cryptographic assumptions, initial states, message semantics, cost, timing, fault opportunities, or operational applicability.

A future internal gate must separately decide whether family-specific descriptive comparison may begin. Even then, any statement must remain bounded to the abstract models and the exact qualified-family conditions.

## Remaining blocker

RIT-014 remains open until WP15-D3 is locally and CI validated, retained in the immutable Phase 15 capture bundle, and followed by a predeclared family-level descriptive-analysis plan. Publication-candidate execution remains blocked.
