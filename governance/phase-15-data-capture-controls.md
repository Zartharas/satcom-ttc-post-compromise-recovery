# Phase 15 Data-Capture Controls

## Status

`PROVISIONAL_CONTROLS_ACTIVE_FOR_PILOT`

These controls govern Phase 15 T1 and B0/B1/B2 pilot execution and preservation. They prevent silent parameter drift, catalog drift, outcome-based exclusions, manual alteration of raw data, and unsupported publication claims.

## Scope

The pilot uses synthetic data and abstract models only. It does not authorize:

- live RF activity;
- testing operational spacecraft or ground systems;
- transmission of commands to third-party infrastructure;
- collection of production credentials or private telemetry;
- concrete cryptographic implementation claims; or
- CCSDS/SDLS conformance claims.

## Run authorization

A pilot run is authorized only when:

1. the exact protocol, T1 configuration, baseline configuration, and baseline catalog paths are recorded;
2. the repository commit is known;
3. Git status is recorded before execution;
4. the intended run class is `PILOT_INTERNAL_VALIDATION_ONLY`;
5. the output directory is new and empty; and
6. the command does not target an operational or unauthorized system.

A dirty working tree does not automatically invalidate an internal pilot, but it must be captured verbatim and the run cannot be promoted to publication-candidate evidence.

## Run identifier

Use:

```text
phase15-pilot-YYYYMMDDTHHMMSSZ-g<short_commit>
```

Run IDs are immutable and must not be reused.

## Required directory structure

Each retained run should use a dedicated directory outside the Git repository or in an ignored evidence location:

```text
<run_id>/
  config/
    phase-15-pilot.json
    phase-15-baseline-parity.json
    phase-15-experiment-protocol-candidate.json
    phase-08-provisional.json
    baseline-test-catalog.json
  raw/
    phase15-pilot-results.json
    phase15-pilot-metrics.csv
    phase15-baseline-parity-results.json
    phase15-baseline-parity-metrics.csv
  analysis/
    phase08-analysis.json
    phase08-*.csv
  logs/
    command-runner.txt
    command-baseline.txt
    command-analysis.txt
    runner-stdout.log
    runner-stderr.log
    baseline-stdout.log
    baseline-stderr.log
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
- exact T1, baseline, protocol, analysis, and catalog copies;
- SHA-256 of those copies;
- Python version;
- operating system and architecture;
- exact T1, baseline, and analysis commands;
- dependency information required to reproduce the run; and
- destination directory.

The configuration and catalog copies inside the run directory are authoritative for that run. The baseline runner must prefer the retained catalog copy over the live repository path.

## Execution logging

Capture stdout and stderr separately for T1 execution, baseline execution, and T1 analysis. Record every process exit code.

A successful process exit does not prove scientific validity. A failed process exit does not permit deletion of the run record when any output was produced; preserve it as a failed attempt and document the disposition.

A baseline catalog-oracle mismatch must terminate the baseline runner. It may not be converted into a pass by changing the captured expected result after execution.

## Raw-data immutability

After the raw manifest is created:

- do not edit raw JSON, CSV, logs, configuration copies, catalog copies, or metadata;
- do not overwrite files in place;
- do not reuse the directory for a corrected run;
- do not manually fix malformed rows;
- do not remove unexpected outcomes; and
- do not regenerate a manifest to conceal an unauthorized edit.

Corrections require a new run ID and, when applicable, a corrective commit.

Read-only filesystem permissions may be used after validation. Permission changes do not replace checksum verification.

## Configuration and catalog control

Every T1 parameter must come from the retained T1 configuration. Every baseline scenario must come from the retained baseline configuration and retained catalog. Command-line overrides are prohibited unless the exact override is predeclared, recorded, and represented in metadata.

The Phase 15 parameters, adapter contact convention, and adapter transmission counts are candidates only. Running them does not freeze them for the publication study.

The catalog contains design oracles pending independent review. Metric adaptation does not convert those values into empirical findings or approved ground truth.

## Schedule and scenario identity

For T1, preserve:

- the seed;
- the complete canonical serialized schedule; and
- its SHA-256 digest.

For B0/B1/B2, preserve:

- the scenario ID;
- baseline variant;
- initial state;
- compromise scope;
- activation policy when present;
- normalized fault actions; and
- the canonical scenario/schedule SHA-256 digest.

The integer seed alone is not sufficient for T1 identity. The baseline scenario ID alone is not sufficient for adapter identity.

## Inclusion control

Include all valid generated T1 runs and all 21 baseline catalog scenarios, including:

- zero-fault schedules;
- success outcomes;
- adverse outcomes;
- incomplete or indeterminate outcomes;
- low-count groups; and
- results that contradict expectations.

Do not filter by outcome after results are known.

## Exclusion control

An exclusion requires a record containing:

- unique exclusion ID;
- run ID;
- seed or baseline scenario ID, when applicable;
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
4. identify any corrective commit, configuration, or catalog change;
5. state whether T1 schedules and baseline scenario digests remained byte-identical; and
6. prevent accidental aggregation of pre-correction and post-correction data.

Repeated execution solely to obtain a preferred result is prohibited.

## Processing control

Processed outputs must be generated from retained raw files by versioned scripts. Record:

- source paths and SHA-256 values;
- analysis script path and commit;
- configuration path and SHA-256;
- exact command;
- output paths; and
- processed-output manifest.

Manual spreadsheet edits are not permitted as the authoritative analysis source. Human-readable tables for the manuscript must be reproducible from tracked scripts or documented transformations.

The current Phase 08 analysis consumes T1 rows only. Baseline metric rows must not be silently inserted into that analysis because the scenario populations and contact semantics are not yet matched.

## Checksum control

Create separate manifests for raw, analysis, and complete run bundles. Manifest paths must be relative and deterministic.

Verify manifests:

- immediately after generation;
- after transfer or archival;
- before analysis;
- before manuscript value extraction; and
- before public release.

A checksum pass proves byte identity only. It does not prove correctness, completeness, comparability, or scientific validity.

## Data-quality gates

Before accepting a pilot run as a valid pipeline test, confirm:

- all JSON files parse successfully;
- T1 and baseline CSV headers and row counts match expectations;
- every T1 result has a seed and schedule digest;
- every baseline result has a scenario ID, null seed, and scenario/schedule digest;
- baseline scenario IDs exactly match the 21-entry retained catalog order;
- every baseline alignment, declared joint state, and outcome matches the existing catalog oracle;
- T1 and baseline JSON/CSV metrics agree within their respective outputs;
- T1 event ordering passes the existing trace audit;
- baseline event order and adapter-completion records are retained;
- no undeclared output file is treated as authoritative;
- checksum manifests verify; and
- all exclusions and reruns are documented.

## Treatment-parity gate

WP15-D1 implements shared metric-field and capture parity for B0, B1, and B2. Its status remains:

`IMPLEMENTED_PENDING_VALIDATION`

The pilot may state only that all four treatments emit a common captured metric field set after successful validation.

Comparative publication conclusions remain blocked until the project provides equivalent or explicitly justified:

- matched scenario inputs;
- contact-window semantics;
- retry semantics;
- fault distributions;
- command and telemetry evidence transitions;
- event interpretation;
- exclusion handling;
- provenance; and
- checksum preservation.

Metric-field parity is not semantic equivalence, timing equivalence, or treatment comparability. The remaining matched-scenario gap must remain visible in the Phase 15 tracker and issue register.

## Reviewer and claim controls

Issue #3 remains open. Pilot work must not change:

- `PENDING_INDEPENDENT_REVIEW` baseline status;
- `NOT_PERMITTED` oracle freeze status;
- formal completeness restrictions;
- implementation-equivalence restrictions;
- cryptographic-security or PCS restrictions;
- causal restrictions; or
- operational-spacecraft restrictions.

A reviewer may later require corrections and reruns. The capture design must make those changes auditable rather than obscuring them.

## AI-assisted development record

Where AI tools materially assist with code, documentation, analysis scaffolding, or manuscript text, retain enough information to support an accurate venue-specific disclosure. Human review, testing, source verification, and accountability remain mandatory.

Do not place confidential prompts, credentials, private correspondence, or sensitive third-party material in the public repository.

## Release control

No run is publication-grade merely because it passes these controls. Public release requires a separate decision confirming:

- license compatibility;
- removal of credentials and private data;
- validated checksums;
- manuscript-to-data consistency;
- accurate AI-use disclosure;
- accurate external-review status; and
- no unresolved embargo or coordinated-disclosure restriction.
