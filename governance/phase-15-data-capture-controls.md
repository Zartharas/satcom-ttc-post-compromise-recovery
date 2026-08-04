# Phase 15 Data-Capture Controls

## Status

`PROVISIONAL_CONTROLS_ACTIVE_FOR_PILOT`

These controls govern Phase 15 T1, B0/B1/B2, D2, D3, and D3B pilot execution and preservation. They prevent silent parameter or catalog drift, outcome-based exclusions, manual alteration of retained data, incomplete provenance, unsupported aggregation, and unsupported publication claims.

## Scope

The pilot uses synthetic data and abstract models only. It does not authorize:

- live RF activity;
- testing operational spacecraft or ground systems;
- transmission of commands to third-party infrastructure;
- collection of production credentials or private telemetry;
- concrete cryptographic implementation claims;
- CCSDS/SDLS conformance claims; or
- treatment-effectiveness or superiority claims.

## Run authorization

A pilot run is authorized only when:

1. the exact protocol, T1 configuration, baseline configuration, D2 matrix, D3 configuration, analysis configuration, baseline catalog, and T1 catalog paths are recorded;
2. the repository commit is known;
3. Git status is recorded before execution;
4. the run class is `PILOT_INTERNAL_VALIDATION_ONLY`;
5. the output directory is new and empty; and
6. no command targets an operational or unauthorized system.

A dirty working tree does not automatically invalidate an internal pilot, but it must be captured verbatim and the run cannot be promoted to publication-candidate evidence.

## Run identifier

Use:

```text
phase15-pilot-YYYYMMDDTHHMMSSZ-g<short_commit>
```

Run IDs are immutable and must not be reused.

## Required directory structure

```text
<run_id>/
  config/
    phase-15-pilot.json
    phase-15-baseline-parity.json
    phase-15-matched-family-population.json
    phase-15-treatment-comparability-matrix.json
    phase-15-experiment-protocol-candidate.json
    phase-08-provisional.json
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
    phase08-analysis.json
    phase08-*.csv
  logs/
    command-runner.txt
    command-baseline.txt
    command-matched-family.txt
    command-analysis.txt
    runner-stdout.log
    runner-stderr.log
    baseline-stdout.log
    baseline-stderr.log
    matched-family-stdout.log
    matched-family-stderr.log
    analysis-stdout.log
    analysis-stderr.log
    environment.txt
    git-status.txt
  governance/
    run-metadata.json
    exclusions.json
    reruns.json
  manifests/
    raw.sha256
    derived.sha256
    analysis.sha256
    run-bundle.sha256
```

Empty exclusion or rerun files are acceptable when their schema and empty state are explicit.

## Pre-run capture

Before execution, record:

- UTC start timestamp;
- repository and branch;
- full commit SHA;
- `git status --porcelain` output;
- exact retained copies of all configurations, matrix, protocol, and catalogs;
- SHA-256 of every retained copy;
- Python version;
- operating system and architecture;
- exact T1, baseline, D3, and analysis commands;
- dependency information needed to reproduce the run; and
- destination directory.

The copies inside `config/` are authoritative for that run. The baseline and D3 runners must receive retained catalog and contract paths rather than silently re-reading repository-live files.

## Execution ordering

The required order is:

1. retain inputs;
2. execute the T1 pilot;
3. execute baseline parity;
4. execute D3 only when both T1 and baseline exit zero;
5. validate D3 outputs independently in the capture wrapper;
6. execute T1 descriptive analysis when the T1 runner succeeds;
7. write governance records; and
8. write and verify all manifest layers.

D3 statuses are:

- `SKIPPED_PREREQUISITE_FAILURE` when T1 or baseline fails;
- `PROCESS_FAILED` when the D3 process returns nonzero;
- `OUTPUT_VALIDATION_FAILED` when a zero-exit D3 process produces unacceptable output; and
- `COMPLETED_AND_VERIFIED` only after all D3 checks pass.

A D3 failure must contribute to `overall_exit_code`.

## Execution logging

Capture stdout and stderr separately for T1 execution, baseline execution, D3 execution, and T1 analysis. Record process exit codes and the capture-side D3 validation result.

A successful process exit does not prove scientific validity. A failed process exit does not permit deletion of the run record when any output was produced; preserve it as a failed attempt and document the disposition.

A catalog-oracle mismatch must terminate the affected execution. It may not be converted into a pass by changing a retained expected result after execution.

## Raw-data immutability

After manifests are created:

- do not edit raw JSON, CSV, derived files, logs, retained inputs, catalogs, metadata, or governance records;
- do not overwrite files in place;
- do not reuse the directory for a corrected run;
- do not manually fix malformed rows;
- do not remove unexpected outcomes; and
- do not regenerate a manifest to conceal an unauthorized edit.

Corrections require a new run ID and, when applicable, a corrective commit.

Read-only filesystem permissions may be used after validation. Permission changes do not replace checksum verification.

## Configuration, matrix, and catalog control

Every T1 parameter must come from the retained T1 configuration. Every baseline scenario must come from the retained baseline configuration and retained baseline catalog. Every D3 family and allowed field must come from the retained D2 matrix and retained D3 configuration. Every T1 D3 member must come from the retained T1 catalog.

Command-line overrides are prohibited unless predeclared, recorded, and represented in metadata.

The parameters, adapter contact convention, adapter transmission counts, family definitions, and D3 analysis units remain provisional. Execution does not freeze them for publication.

The catalogs contain internal design oracles pending independent review. Metric adaptation and D3 execution do not convert those values into empirical findings or approved ground truth.

## Schedule, scenario, and source identity

For T1 seeded runs, preserve:

- seed;
- canonical serialized schedule; and
- schedule SHA-256.

For B0/B1/B2, preserve:

- scenario ID;
- baseline variant;
- initial state;
- compromise scope;
- activation policy when present;
- normalized fault actions; and
- canonical scenario SHA-256.

For D3, preserve:

- family ID;
- treatment;
- source ID and source type;
- analysis-unit ID;
- allowed-field list;
- projected metrics;
- source-execution SHA-256;
- retained source execution evidence; and
- publication-evidence flag.

The integer seed alone is not sufficient T1 identity. A scenario ID alone is not sufficient baseline or D3 identity.

## Inclusion control

Include all valid generated T1 runs, all 21 baseline scenarios, and all 13 qualified D3 member rows, including:

- zero-fault schedules;
- success outcomes;
- adverse outcomes;
- incomplete or indeterminate outcomes;
- low-count groups; and
- results that contradict expectations.

Do not filter by outcome after results are known.

## Exclusion control

An exclusion requires:

- unique exclusion ID;
- run ID;
- seed, baseline scenario ID, or D3 row ID when applicable;
- UTC timestamp;
- allowed reason code;
- factual description;
- evidence paths;
- whether the outcome was known before the decision;
- disposition; and
- linked rerun, if any.

Allowed reason codes are limited to:

- `EXECUTION_FAILURE`
- `CORRUPT_OUTPUT`
- `SCHEMA_FAILURE`
- `CHECKSUM_FAILURE`
- `CONFIG_MISMATCH`
- `CATALOG_ORACLE_MISMATCH`
- `PROTOCOL_CORRECTION`

An unexpected or unfavorable outcome is not an exclusion reason.

## Rerun control

A rerun must:

1. use a new run ID;
2. preserve the earlier attempt;
3. cite the authorized reason;
4. identify any corrective commit or retained-input change;
5. state whether T1 schedules, baseline scenario digests, D2 matrix, D3 config, and source-execution digests remained identical; and
6. prevent accidental aggregation of pre-correction and post-correction data.

Repeated execution solely to obtain a preferred result is prohibited.

## Processing control

Processed and derived outputs must be generated from retained inputs by versioned scripts. Record source paths and SHA-256 values, script and commit, exact command, output paths, and output manifests.

Manual spreadsheet edits are not permitted as the authoritative analysis source. Manuscript tables must be reproducible from tracked scripts or documented transformations.

The Phase 08 analysis consumes T1 seeded rows only. D3 produces member-level family projections but does not perform family-level comparison.

## D3B capture-side acceptance

A zero-exit D3 process is accepted only when:

- all four D3 files exist;
- the internal D3 manifest covers exactly the JSON and two CSV files;
- internal checksums verify;
- status remains `EXECUTABLE_POPULATION_IMPLEMENTED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE`;
- run class remains `PILOT_INTERNAL_VALIDATION_ONLY`;
- eligible families are exactly CF-01, CF-02, CF-05, and CF-06;
- counts are 4 families, 13 member rows, 12 analysis units, and 13 source executions;
- row IDs are unique;
- every row is `QUALIFIED_MATCH`;
- family coverage is complete;
- `success_rate_denominator=NOT_DEFINED`;
- `aggregate_authorized=false`;
- JSON/CSV member and denominator identities agree;
- source-execution digests are present; and
- all comparison, inference, superiority, and publication gates remain closed.

The wrapper must reject both byte-level tampering and semantically relaxed output that has been re-checksummed.

## Checksum control

Create and verify:

1. the D3 internal derived manifest;
2. `manifests/raw.sha256` for retained inputs and raw T1/baseline outputs;
3. `manifests/derived.sha256` for the complete D3 directory, including its internal manifest;
4. `manifests/analysis.sha256` for Phase 08 outputs; and
5. `manifests/run-bundle.sha256` for all retained files except itself.

Verify manifests immediately after generation, after transfer or archive, before interpretation, before manuscript extraction, and before release.

A checksum pass proves byte identity only. It does not prove correctness, completeness, comparability, or scientific validity.

## Data-quality gates

Before accepting a pilot run as a valid pipeline test, confirm:

- all JSON files parse;
- T1 and baseline CSV headers and row counts match expectations;
- every T1 seeded result has a seed and schedule digest;
- every baseline result has a scenario ID, null seed, and scenario digest;
- baseline IDs exactly match the retained 21-entry order;
- baseline alignment, joint state when declared, and outcome match retained oracles;
- T1 and baseline JSON/CSV metrics agree within their own outputs;
- D3 member and denominator JSON/CSV identities agree;
- D3 counts and source digests match the contract;
- event ordering and completion evidence are retained;
- no undeclared file is treated as authoritative;
- all checksum layers verify; and
- exclusions and reruns are documented.

## Treatment-parity gate

WP15-D1 implements shared metric-field and capture parity for B0, B1, and B2. Metric-field parity is not semantic equivalence, timing equivalence, or treatment comparability.

WP15-D2 defines semantic families. WP15-D3 executes only the four qualified families. WP15-D3B preserves those contracts and outputs in one immutable bundle.

Even after D3B validation, comparative publication conclusions remain blocked until the project freezes or justifies:

- observation cutoffs;
- family-specific denominators;
- fault opportunities;
- contact and retry semantics;
- exclusion handling;
- thresholds;
- sensitivity plan; and
- statistical plan before aggregate review.

## Claim controls

The integrated pilot must preserve:

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

Issue #3 remains open. Pilot work must not change pending review, oracle-freeze restrictions, formal-completeness restrictions, implementation-equivalence restrictions, cryptographic-security restrictions, causal restrictions, or operational-spacecraft restrictions.

## AI-assisted development record

Where AI tools materially assist with code, documentation, analysis scaffolding, or manuscript text, retain enough information to support an accurate venue-specific disclosure. Human review, testing, source verification, and accountability remain mandatory.

Do not place confidential prompts, credentials, private correspondence, or sensitive third-party material in the public repository.

## Release control

No run is publication-grade merely because it passes these controls. Public release requires a separate decision confirming license compatibility, removal of private data, validated checksums, manuscript-to-data consistency, accurate AI disclosure, accurate external-review status, and no unresolved embargo or coordinated-disclosure restriction.
