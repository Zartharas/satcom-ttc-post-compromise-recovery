# Phase 15 Data-Capture Controls

## Status

`PROVISIONAL_CONTROLS_ACTIVE_FOR_PILOT`

These controls govern Phase 15 pilot execution and preservation. They are designed to prevent silent parameter drift, outcome-based exclusions, manual alteration of raw data, and unsupported publication claims.

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

1. the exact protocol and configuration paths are recorded;
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

Example:

```text
phase15-pilot-20260804T021530Z-g10148d0
```

Run IDs are immutable and must not be reused.

## Required directory structure

Each retained run should use a dedicated directory outside the Git repository or in an ignored evidence location:

```text
<run_id>/
  config/
    phase-15-pilot.json
    phase-15-experiment-protocol-candidate.json
  raw/
    phase15-pilot-results.json
    phase15-pilot-metrics.csv
  analysis/
    phase08-analysis.json
    phase08-*.csv
  logs/
    command.txt
    stdout.log
    stderr.log
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
- exact configuration and protocol copies;
- SHA-256 of those copies;
- Python version;
- operating system and architecture;
- exact command line;
- dependency information required to reproduce the run; and
- destination directory.

The configuration copies inside the run directory are authoritative for that run.

## Execution logging

Capture stdout and stderr separately. Record the process exit code.

A successful process exit does not prove scientific validity. A failed process exit does not permit deletion of the run record when any output was produced; preserve it as a failed attempt and document the disposition.

## Raw-data immutability

After the raw manifest is created:

- do not edit raw JSON, CSV, logs, configuration copies, or metadata;
- do not overwrite files in place;
- do not reuse the directory for a corrected run;
- do not manually fix malformed rows;
- do not remove unexpected outcomes; and
- do not regenerate a manifest to conceal an unauthorized edit.

Corrections require a new run ID and, when applicable, a corrective commit.

Read-only filesystem permissions may be used after validation. Permission changes do not replace checksum verification.

## Configuration control

Every parameter must come from the retained configuration. Command-line overrides are prohibited unless the exact override is predeclared, recorded, and represented in the metadata.

The Phase 15 pilot parameters are candidates only. Running them does not freeze them for the publication study.

## Schedule identity

The integer seed is not sufficient to identify a schedule. Preserve:

- the seed;
- the complete canonical serialized schedule; and
- its SHA-256 digest.

Any schedule-generation code change can alter the schedule even when the seed is unchanged. A later run must therefore compare schedule digests, not seeds alone.

## Inclusion control

Include all valid generated runs, including:

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
- run ID and seed, when applicable;
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
- `PROTOCOL_CORRECTION`

An unexpected or unfavorable outcome is not an exclusion reason.

## Rerun control

A rerun must:

1. use a new run ID;
2. preserve the earlier attempt;
3. cite the authorized reason;
4. identify any corrective commit or configuration change;
5. state whether the schedules remained byte-identical; and
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

## Checksum control

Create separate manifests for raw, analysis, and complete run bundles. Manifest paths must be relative and deterministic.

Verify manifests:

- immediately after generation;
- after transfer or archival;
- before analysis;
- before manuscript value extraction; and
- before public release.

A checksum pass proves byte identity only. It does not prove correctness, completeness, or scientific validity.

## Data-quality gates

Before accepting a pilot run as a valid pipeline test, confirm:

- JSON parses successfully;
- CSV headers and row counts match expectations;
- every result has a seed and schedule digest;
- schedule digests are unique where schedules differ;
- JSON and CSV metrics agree;
- event ordering passes the existing trace audit;
- no undeclared output file is treated as authoritative;
- checksum manifests verify; and
- all exclusions and reruns are documented.

## Treatment-parity gate

The pilot may validate T1 capture. It may not support comparative publication conclusions until B0, B1, and B2 provide equivalent or explicitly justified:

- scenario inputs;
- contact-window accounting;
- retry accounting;
- event logs;
- security and availability fields;
- exclusion handling;
- provenance; and
- checksum preservation.

This gap must remain visible in the Phase 15 tracker and issue register.

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
