# Phase 15 Experiment Protocol Candidate

## Status

`PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE`

This protocol permits synthetic pilot execution, engineering validation, and immutable data-capture testing while preserving every unresolved Phase 14 review and publication gate.

Machine-readable contracts:

- `spec/phase-15-experiment-protocol-candidate.json`
- `spec/phase-15-treatment-comparability-matrix.json`
- `spec/phase-15-d3b-capture-integration.json`
- `experiments/configs/phase-15-pilot.json`
- `experiments/configs/phase-15-baseline-parity.json`
- `experiments/configs/phase-15-matched-family-population.json`

## Purpose

Phase 15 separates four activities that must not be conflated:

1. **engineering validation** — tests, validators, formal gates, internal design-oracle preservation, and checksums;
2. **pilot data capture** — T1, baseline, D2, D3, provenance, schema, and immutable-bundle validation;
3. **qualified-family population validation** — execution of only the four D2-qualified families with member-level projection and coverage denominators; and
4. **publication-candidate execution** — a later versioned run using frozen observation controls and an analysis plan fixed before comparative aggregates are viewed.

The current work belongs only to the first three categories. It is not publication evidence.

## Research questions

### RQ-1 — Outcome classification

Within the declared abstract model, how do B0, B1, B2, and provisional T1 classify recovery outcomes under matched fault scenarios?

This cannot support comparative conclusions until the population, observation boundaries, denominators, and analysis plan are validated and frozen.

### RQ-2 — Contact-window behavior

Within discrete contact windows, how do recovery duration, retry overhead, security state, and availability state vary across matched fault schedules?

Current baseline adapter contact and transmission values are not accepted as cross-treatment timing or cost units. Raw duration, transmission, retry, and epoch-bearing alignment fields remain excluded from D3 projections.

### RQ-3 — Formal/Python diagnostics

Where do bounded formal witnesses and Python execution traces agree or differ under the declared projection?

Results remain bounded and diagnostic. They are not refinement proofs, implementation-equivalence claims, or cryptographic-security results.

## Treatment readiness

| Treatment | Current support | metric parity status |
|---|---|---|
| B0 | Deterministic catalog metric adapter | Locally validated; CI pending |
| B1 | Deterministic catalog metric adapter | Locally validated; CI pending |
| B2 | Deterministic catalog metric adapter | Locally validated; CI pending |
| T1 | Seeded, explicit-fault, and catalog-behavior execution | Available provisionally |

Shared metric parity is not treatment comparability.

## WP15-D1 — Baseline metric and capture parity

D1 executes all 21 retained baseline catalog scenarios without changing transition semantics or internal design oracles. Before emitting a row, the adapter verifies expected alignment, joint state when declared, and outcome.

The adapter emits the complete shared metric field set, baseline identifiers, canonical scenario SHA-256, event logs, JSON, CSV, retained configuration/catalog provenance, and checksums.

D1 passed local validation. CI remains pending.

## WP15-D2 — Semantic comparability

D2 defines eight conservative families:

- CF-01, CF-02, CF-05, and CF-06 are `QUALIFIED_MATCH`;
- CF-03, CF-04, CF-07, and CF-08 are `DIAGNOSTIC_FAMILY_ONLY`;
- no family is `FULL_MATCH`.

All 21 baseline and 15 T1 catalog scenarios have exactly one disposition. The matrix prohibits pooled curated catalogs, treatment success percentages, independent-replication treatment of B1 policy variants, diagnostic-family aggregation, raw alignment comparison, contact timing, transmissions, retries, and any field not explicitly authorized by a family.

D2 passed local validation. CI remains pending.

## WP15-D3 — Executable qualified-family population

D3 executes only CF-01, CF-02, CF-05, and CF-06.

| Family | Member rows | Analysis units |
|---|---:|---:|
| CF-01 | 4 | 4 |
| CF-02 | 5 | 4 |
| CF-05 | 2 | 2 |
| CF-06 | 2 | 2 |
| **Total** | **13** | **12** |

The two CF-02 B1 policy variants remain separate member rows but share one B1 analysis unit. They are not independent replications.

Baseline members execute through the D1 oracle-checking adapter. T1 members execute exact retained catalog behaviors, including post-success replay for T1-13. Every source must match its retained internal design oracle before projection.

Each member row contains only the fields authorized by its family. `alignment_class` is derived from raw alignment. Raw timing, transmissions, retries, seeds, schedule identity, and all unauthorized fields are omitted.

The denominator table records coverage only. `success_rate_denominator` remains `NOT_DEFINED`, and `aggregate_authorized` remains false.

D3 passed local validation. CI remains pending.

## WP15-D3B — Immutable pilot-bundle integration

D3B integrates D2 and D3 into `experiments/scripts/run_phase15_pilot_capture.py`.

Status:

`IMPLEMENTED_PENDING_LOCAL_AND_CI_VALIDATION_NOT_COMPARATIVE_EVIDENCE`

### Retained inputs

The wrapper copies these inputs into `config/` before execution:

- T1 pilot configuration;
- baseline-parity configuration;
- D3 matched-family configuration;
- D2 comparability matrix;
- Phase 15 protocol candidate;
- Phase 08 analysis configuration;
- baseline catalog; and
- T1 catalog.

The retained copies are passed to the D3 runner. Repository-live D2/D3/catalog files are not silently substituted during capture.

### Execution order

1. retain all inputs;
2. run the seeded T1 pilot;
3. run all 21 baseline scenarios;
4. run D3 only when both T1 and baseline exit zero;
5. validate D3 files, internal checksums, population, JSON/CSV identity, denominators, and claim boundaries;
6. run T1 descriptive analysis when T1 succeeds;
7. write metadata, exclusions, and reruns; and
8. write and verify all run-level manifests.

D3 statuses:

- `SKIPPED_PREREQUISITE_FAILURE`
- `PROCESS_FAILED`
- `OUTPUT_VALIDATION_FAILED`
- `COMPLETED_AND_VERIFIED`

Only the final status is a successful D3B capture. A D3 failure contributes to `overall_exit_code`.

### Capture-side validation

A zero-exit D3 process is accepted only when:

- all D3 JSON/CSV/manifest files exist;
- the D3 internal manifest covers exactly the expected three data files;
- internal checksums verify;
- status and pilot run class remain correct;
- eligible families remain exactly CF-01, CF-02, CF-05, and CF-06;
- counts remain 4 families, 13 member rows, 12 analysis units, and 13 source executions;
- row IDs are unique and all rows are `QUALIFIED_MATCH`;
- family coverage is complete;
- success-rate denominators remain undefined;
- aggregation remains unauthorized;
- JSON/CSV identities agree; and
- comparison, inference, superiority, and publication gates remain closed.

The wrapper rejects byte-level tampering and semantic relaxation even when modified files have been re-checksummed.

### Metadata

D3B run metadata schema `0.2.0` records:

- exact Git commit, branch, and status;
- retained paths and SHA-256 values for T1, baseline, D2, D3, protocol, analysis, and both catalogs;
- exact commands and exit codes;
- D3 process and capture-validation statuses;
- D3 output paths and internal-manifest digest;
- D3 population counts;
- stdout/stderr paths; and
- complete closed claim boundaries.

### Manifest hierarchy

- D3 internal manifest protects D3 JSON and CSV files.
- `manifests/raw.sha256` protects retained inputs and raw T1/baseline outputs.
- `manifests/derived.sha256` protects the complete D3 directory, including its internal manifest.
- `manifests/analysis.sha256` protects Phase 08 outputs.
- `manifests/run-bundle.sha256` protects every retained file except itself.

All manifests must verify before the wrapper returns success.

## Pilot scope

The pilot label is:

`PILOT_INTERNAL_VALIDATION_ONLY`

The pilot may validate deterministic execution, internal design-oracle preservation, shared metric generation, D2 family classification, D3 member projection, D3B provenance, JSON/CSV integrity, metadata, logs, exclusions, reruns, and checksums.

The pilot does not establish treatment effectiveness, statistical significance, cryptographic security, baseline fairness, independent validation, operational timing, or publication-ready evidence.

## Candidate T1 pilot parameters

| Parameter | Candidate value | Status |
|---|---:|---|
| Seeds | 7001–7012 | Unfrozen pilot candidate |
| Ground epoch | 2 | Unfrozen pilot candidate |
| Spacecraft epoch | 1 | Unfrozen pilot candidate |
| Authority epoch floor | 0 | Unfrozen pilot candidate |
| Maximum transmissions | 3 | Unfrozen pilot candidate |
| Candidate lifetime | 3 contacts | Unfrozen pilot candidate |
| Maximum scheduled faults | 4 | Unfrozen pilot candidate |
| Active keys initially compromised | true | Unfrozen pilot candidate |

Allowed seeded faults are `DROP`, `DELAY`, `DUPLICATE`, `REORDER`, `CONTACT_CLOSE`, `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY`.

These values test the pipeline. They do not define a final publication population.

## Inclusion rules

Include:

- every successfully parsed T1 run from the exact retained configuration and schedule;
- all 21 baseline scenarios in retained order;
- all 13 D3 qualified-family member rows;
- success, adverse, degraded, indeterminate, unsafe, locked, divergent, and expired outcomes;
- zero-fault schedules; and
- low-count groups labeled descriptive-only.

Do not suppress a run because its outcome is unexpected, inconvenient, or unfavorable.

## Exclusion rules

Exclude only for documented technical execution failure, corrupt/incomplete output, schema failure, checksum failure, configuration mismatch, catalog-oracle mismatch, or a predeclared protocol correction.

Every exclusion must identify the run or row, reason, evidence, time, disposition, and linked rerun before interpretation.

## Rerun rules

A rerun requires a new run ID, preserved earlier attempt, authorized reason, identified corrective commit/input change, and a rule separating pre-correction and post-correction data.

Do not rerun to obtain a preferred outcome.

## Analysis boundary

Authorized now:

- engineering validation;
- member-level family projection for internal validation;
- family coverage and analysis-unit counting;
- immutable-capture and checksum auditing; and
- methods, limitations, reproducibility, and disclosure drafting.

Not authorized:

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

## Publication-candidate entry gate

A publication-candidate run must not begin until:

1. D1, D2, D3, and D3B validations pass at exact retained commits;
2. the integrated pilot reproduces from retained inputs and all manifests;
3. baseline metric/capture parity and family exceptions remain explicit;
4. observation cutoffs, family denominators, fault opportunities, thresholds, exclusions, and sensitivity/statistical plans are versioned before comparative aggregate review;
5. scientific-validity defects are closed or transparently accepted as limitations;
6. external-review status is represented accurately; and
7. the publication-candidate protocol is separately authorized.

## External-review relationship

Issue #3 remains open. Review delay does not block provisional protocol, parity, comparability, population, capture, or manuscript-method work. It does block claims that baseline mappings or the 21 oracle candidates are independently approved.

A later correction may require affected reruns. Retained contracts, source executions, hashes, and manifests are intended to make that impact auditable.

## Hard boundaries

The pilot does not permit claims of independent validation, frozen baseline oracles, cryptographic security or PCS, formal completeness, refinement or implementation equivalence, causal validity, treatment superiority, operational timing equivalence, CCSDS/SDLS conformance, flight/RF/operational applicability, or publication-grade comparative evidence.
