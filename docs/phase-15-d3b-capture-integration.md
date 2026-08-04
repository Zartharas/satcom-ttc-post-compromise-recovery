# Phase 15 WP15-D3B Immutable Capture Integration

## Status

`IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

WP15-D3B integrates the locally validated WP15-D3 executable qualified-family population into the immutable Phase 15 pilot bundle. It changes capture and provenance behavior only. It does not authorize family-level interpretation, percentages, pooled aggregation, inferential statistics, treatment-superiority claims, or publication evidence.

## Scope

The integration retains and executes the following contracts in one immutable run directory:

- the Phase 15 pilot configuration;
- the B0/B1/B2 metric-parity configuration;
- the WP15-D2 treatment-comparability matrix;
- the WP15-D3 matched-family population configuration;
- the Phase 15 protocol candidate;
- the Phase 08 descriptive-analysis configuration;
- the baseline scenario catalog; and
- the provisional T1 scenario catalog.

The retained copies, rather than repository-live copies, are passed to the D3 runner.

## Execution ordering

The capture wrapper performs these stages:

1. retain all configuration, matrix, protocol, and catalog inputs;
2. execute the seeded T1 pilot;
3. execute all 21 deterministic baseline scenarios;
4. execute WP15-D3 only when both the T1 and baseline processes exit successfully;
5. validate the D3 output structure, internal checksums, population counts, JSON/CSV identity, denominators, and claim boundaries;
6. execute the existing T1 descriptive-analysis stage when the T1 runner succeeds;
7. write governance metadata, exclusions, and rerun records; and
8. generate and verify run-level checksum manifests.

A T1 or baseline failure sets the D3 status to `SKIPPED_PREREQUISITE_FAILURE`. A D3 process failure sets `PROCESS_FAILED`. A zero-exit D3 process whose outputs fail capture-side validation sets `OUTPUT_VALIDATION_FAILED`. Only a structurally and semantically valid D3 output receives `COMPLETED_AND_VERIFIED`.

## Immutable run layout

```text
<run-id>/
  config/
    phase-08-provisional.json
    phase-15-baseline-parity.json
    phase-15-experiment-protocol-candidate.json
    phase-15-matched-family-population.json
    phase-15-pilot.json
    phase-15-treatment-comparability-matrix.json
    baseline-test-catalog.json
    t1-provisional-test-catalog.json
  raw/
    phase15-pilot-results.json
    phase15-pilot-metrics.csv
    phase15-baseline-parity-results.json
    phase15-baseline-parity-metrics.csv
  derived/
    phase-15-matched-family-population.json
    phase-15-matched-family-members.csv
    phase-15-matched-family-denominators.csv
    phase-15-matched-family-derived.sha256
  analysis/
    <Phase 08 descriptive outputs>
  governance/
    exclusions.json
    reruns.json
    run-metadata.json
  logs/
    command-runner.txt
    command-baseline.txt
    command-matched-family.txt
    command-analysis.txt
    <stdout, stderr, environment, and Git-state logs>
  manifests/
    raw.sha256
    derived.sha256
    analysis.sha256
    run-bundle.sha256
```

## Retained provenance

`governance/run-metadata.json` records:

- exact Git branch, commit, and clean or dirty status;
- UTC start and end times;
- Python and platform information;
- retained T1, baseline, D2, D3, protocol, analysis, and catalog paths;
- SHA-256 values for every retained contract and catalog;
- exact T1, baseline, D3, and analysis commands;
- process and capture-validation exit codes;
- D3 execution status;
- D3 output paths;
- D3 internal-manifest SHA-256;
- family, member-row, and analysis-unit counts when D3 completes;
- stdout and stderr paths; and
- the complete non-claim boundary.

The metadata schema version is `0.2.0` for D3B-integrated captures.

## Checksum hierarchy

Four run-level manifests protect separate layers:

1. `raw.sha256` protects retained inputs and raw T1/baseline outputs;
2. `derived.sha256` protects the complete D3 derived directory, including its internal manifest;
3. `analysis.sha256` protects the Phase 08 descriptive-analysis directory; and
4. `run-bundle.sha256` protects all retained files except itself, including the other three run-level manifests.

The D3 internal manifest independently protects its JSON, member CSV, and denominator CSV. This creates two checksum checks for each D3 data file before the complete-bundle check.

## Capture-side D3 validation

A zero-exit D3 process is not accepted automatically. The capture wrapper requires:

- all four D3 files to exist;
- the internal manifest to cover exactly the JSON and two CSV files;
- all internal SHA-256 values to verify;
- status `EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE`;
- run class `PILOT_INTERNAL_VALIDATION_ONLY`;
- eligible families exactly `CF-01`, `CF-02`, `CF-05`, and `CF-06`;
- four families, 13 member rows, and 12 analysis units;
- 13 unique row identifiers and 13 retained source executions;
- only `QUALIFIED_MATCH` member rows;
- complete family coverage;
- `success_rate_denominator=NOT_DEFINED`;
- `aggregate_authorized=false`;
- member and denominator JSON/CSV identity; and
- all comparison, statistical, superiority, and publication gates remaining closed.

The wrapper rejects both byte-level tampering and semantic relaxation that has been re-checksummed.

## Claim boundary

The integrated bundle preserves:

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

No D3B output may be cited as publication evidence. No family percentage or cross-treatment aggregate is generated.

## Validation gate

WP15-D3B may move to locally validated only after:

- focused capture tests pass;
- D2 and D3 validators pass;
- the complete Python regression suite passes;
- a disposable integrated capture completes with `COMPLETED_AND_VERIFIED`;
- the retained D2 and D3 SHA-256 values match their repository source files;
- the D3 internal, derived-layer, raw-layer, analysis-layer, and complete-bundle manifests verify;
- tamper and missing-output tests fail closed; and
- the tracked-file manifest verifies after all D3B files stabilize.

CI and independent review remain separate unresolved gates.
