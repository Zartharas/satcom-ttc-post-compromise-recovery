# Phase 15 Data Dictionary

## Status

`PROVISIONAL_CAPTURE_SCHEMA_NOT_FROZEN`

This dictionary covers the Phase 15 T1 pilot, deterministic B0/B1/B2 adapter, WP15-D2 matrix, WP15-D3 qualified-family dataset, and WP15-D3B immutable capture bundle. It describes the current abstract simulator and capture design. It does not authorize security, causal, timing-equivalence, treatment-effectiveness, or publication claims.

## Dataset layers

| Layer | Purpose | Editing rule |
|---|---|---|
| Configuration | Declares exact T1, baseline, D2, D3, and analysis inputs | Versioned; never edited after run start |
| Catalog | Declares retained baseline and T1 internal design-oracle scenarios | Retained byte-for-byte |
| Run metadata | Records environment, commands, commits, statuses, and provenance | Immutable after capture |
| Raw T1/baseline JSON | Preserves per-seed or per-scenario execution evidence | Immutable |
| Raw T1/baseline CSV | Flat analysis-ready values for each source pipeline | Regenerated from raw JSON only |
| D3 derived JSON | Preserves 13 member rows, denominators, and source executions | Immutable |
| D3 member CSV | Flat member-level projections | Regenerated from D3 JSON only |
| D3 denominator CSV | Family coverage and analysis-unit counts | Regenerated from D3 JSON only |
| Phase 08 analysis | T1 descriptive outputs and audits | Must identify source and script |
| Exclusion/rerun records | Documents technical exclusions and superseded attempts | Append-only through new run records |
| Checksum manifests | Verify retained bytes at multiple layers | Regenerated only for a new run directory |

## Run metadata schema

D3B-integrated captures use metadata schema `0.2.0`.

### Core fields

| Field | Type | Meaning |
|---|---|---|
| `run_id` | string | Unique immutable run identifier |
| `run_class` | enum | `PILOT_INTERNAL_VALIDATION_ONLY` |
| `publication_evidence` | boolean | Must be false |
| `repository` | string | Repository owner/name |
| `branch` | string | Checked-out branch |
| `commit_sha` | 40-character hex/string | Exact source commit |
| `git_status` | string | `CLEAN` or exact porcelain output |
| `start_time_utc` | RFC 3339 string | UTC start |
| `end_time_utc` | RFC 3339 string | UTC completion |
| `python_version` | string | Interpreter version |
| `platform` | string | Operating system and architecture |
| `overall_exit_code` | integer | First nonzero stage result, otherwise zero |
| `claim_boundary` | object | Closed interpretation and publication gates |

### Retained input paths and hashes

| Field | Meaning |
|---|---|
| `config_path` / `config_sha256` | T1 pilot configuration |
| `baseline_config_path` / `baseline_config_sha256` | Baseline-parity configuration |
| `baseline_catalog_path` / `baseline_catalog_sha256` | Retained baseline catalog |
| `t1_catalog_path` / `t1_catalog_sha256` | Retained T1 catalog |
| `comparability_matrix_path` / `comparability_matrix_sha256` | Retained WP15-D2 matrix |
| `matched_family_config_path` / `matched_family_config_sha256` | Retained WP15-D3 configuration |
| `protocol_path` / `protocol_sha256` | Retained Phase 15 protocol candidate |
| `analysis_config_path` / `analysis_config_sha256` | Retained Phase 08 analysis configuration |

All SHA-256 fields are lowercase 64-character hexadecimal digests of exact retained bytes.

### Process and log fields

| Field | Type | Meaning |
|---|---|---|
| `runner_command` | string array | Exact T1 command |
| `runner_exit_code` | integer | T1 process result |
| `baseline_command` | string array | Exact baseline command |
| `baseline_exit_code` | integer | Baseline process result |
| `matched_family_command` | string array/null | Exact D3 command or null when skipped |
| `matched_family_process_exit_code` | integer/null | D3 subprocess result |
| `matched_family_exit_code` | integer/null | D3 process plus capture-validation result |
| `matched_family_status` | enum | D3B execution/capture status |
| `analysis_command` | string array/null | Exact Phase 08 command |
| `analysis_exit_code` | integer/null | Phase 08 process result |
| `stdout_paths` | path array | Retained stdout logs |
| `stderr_paths` | path array | Retained stderr logs |

`matched_family_status` values:

- `SKIPPED_PREREQUISITE_FAILURE`
- `PROCESS_FAILED`
- `OUTPUT_VALIDATION_FAILED`
- `COMPLETED_AND_VERIFIED`

### D3B provenance fields

| Field | Type | Meaning |
|---|---|---|
| `matched_family_output_paths` | path array | Existing D3 files retained in `derived/` |
| `matched_family_internal_manifest_sha256` | SHA-256/null | Digest of D3 internal manifest when present |
| `matched_family_population_counts` | object/null | Family/member/analysis-unit counts after verified D3 completion |

Verified counts are:

```text
family_count=4
member_row_count=13
analysis_unit_count=12
```

## Raw source result objects

A T1 seed produces one logical T1 result. A baseline catalog scenario produces one deterministic adapter result.

Shared top-level fields:

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | string | Result schema version |
| `status` | enum | Provisional internal status |
| `config` | object | Per-result execution input/context |
| `schedule` | array | Canonically ordered fault actions |
| `metrics` | object | Outcome and measurement fields |
| `event_log` | array | Ordered abstract execution events |

Baseline results also retain `metric_parity_status`, `treatment`, `baseline_variant`, and `scenario_id`.

## T1 per-result configuration

| Field | Type | Meaning |
|---|---|---|
| `seed` | integer | Deterministic schedule-generation input |
| `ground_epoch` | integer | Initial ground epoch |
| `spacecraft_epoch` | integer | Initial spacecraft epoch |
| `authority_epoch_floor` | integer | Minimum authority epoch |
| `max_transmissions` | integer | Bounded attempts per recovery phase |
| `candidate_lifetime_contacts` | integer | Candidate lifetime in contacts |
| `max_faults` | integer | Schedule-generation fault bound |
| `compromise_active_keys` | boolean | Initial active-key compromise marker |
| `allowed_faults` | string array | Generator fault vocabulary |

## Baseline adapter context

| Field | Type | Meaning |
|---|---|---|
| `initial_state` | string | Catalog initial-state description |
| `compromise` | string | Catalog compromise scope |
| `activation_policy` | string/null | B1 policy when declared |
| `properties` | string array | Catalog property labels |
| `adapter_semantics` | string | Explicit timing/transmission limitation |

## Schedule-action fields

| Field | Type | Meaning |
|---|---|---|
| `phase` | string | Protocol or adapter phase |
| `attempt` | integer | One-based attempt index |
| `kind` | string | Fault kind |
| `target` | string | Abstract target |
| `contacts` | integer | Delay/contact duration when applicable |
| `detail` | string/null | Additional normalized adapter detail |

T1 fault kinds are `DROP`, `DELAY`, `DUPLICATE`, `REORDER`, `CONTACT_CLOSE`, `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY`.

The baseline-only `ACTIVE_SENDER_IMPERSONATION` action remains treatment-specific and is not silently relabeled as a T1 fault.

## Shared metric fields

| Field | Type | Interpretation boundary |
|---|---|---|
| `seed` | integer/null | T1 reproduction input; null for deterministic baselines |
| `schedule_sha256` | SHA-256 | Schedule or canonical scenario identity, not a comparison value |
| `outcome` | enum | Abstract classification, not security proof |
| `alignment` | string | Raw epoch-bearing state; not cross-treatment comparable |
| `security_state` | string | Abstract category separate from availability |
| `availability_state` | string | Abstract category separate from security |
| `recovery_duration_contacts` | integer | Treatment-specific contact meaning; not cross-treatment comparable |
| `divergent_contact_windows` | integer | Treatment-specific modeled windows |
| `degraded_contact_windows` | integer | Treatment-specific modeled windows |
| `total_transmissions` | integer | Treatment-specific attempted-message count |
| `retry_overhead` | integer | Attempts beyond treatment-specific reference |
| `fault_count` | integer | Normalized fault-action count |
| `drop_count` | integer | Drop actions |
| `delay_count` | integer | Delay actions |
| `duplicate_count` | integer | Duplicate actions |
| `reorder_count` | integer | Reorder actions |
| `contact_close_count` | integer | Contact-close actions |
| `restart_count` | integer | Restart/stale-restore actions |
| `replay_count` | integer | Replay-related actions |
| `rejection_count` | integer | Total modeled rejections |
| `replay_rejection_count` | integer | Replay-attributed rejections |
| `stale_state_rejection_count` | integer | Stale-state/counter rejections |
| `command_accepted` | boolean | Abstract command evidence |
| `telemetry_complete` | boolean | Abstract telemetry evidence |
| `verification_complete` | boolean | Current model verification condition |
| `active_key_compromised` | boolean | Whether active abstract endpoint key remains attacker-known |

Baseline-specific fields include `treatment`, `baseline_variant`, `scenario_id`, and `other_fault_count`.

## D3 member rows

Each D3 row contains:

| Field | Type | Meaning |
|---|---|---|
| `row_id` | string | Unique `<family>:<treatment>:<source>` identity |
| `family_id` | enum | CF-01, CF-02, CF-05, or CF-06 |
| `family_name` | string | D2 family name |
| `family_classification` | enum | Must be `QUALIFIED_MATCH` |
| `analysis_unit_id` | string | `<family>:<treatment>`; B1 variants share one CF-02 unit |
| `treatment` | enum | B0, B1, B2, or T1 |
| `source_type` | enum | Current qualified members are catalog-backed |
| `source_id` | string | Baseline or T1 scenario ID |
| `role` | string | D2 member role |
| `allowed_fields` | string array | Exact D2-authorized projection fields |
| `projected_metrics` | object | Only allowed fields; includes derived `alignment_class` where permitted |
| `source_execution_sha256` | SHA-256 | Canonical source-execution evidence digest |
| `publication_evidence` | boolean | Must be false |

Raw `alignment`, timing, transmissions, retries, seed, schedule identity, and all other unauthorized fields are omitted from D3 member projections.

## D3 denominator rows

| Field | Type | Meaning |
|---|---|---|
| `family_id` | enum | Qualified family |
| `member_row_count` | integer | Retained source-member rows |
| `analysis_unit_count` | integer | Unique treatment-family units |
| `treatment_count` | integer | Treatments represented |
| `policy_variant_row_count` | integer | Additional policy rows sharing an analysis unit |
| `family_coverage_status` | enum | Must be `COMPLETE` |
| `success_rate_denominator` | enum | Must be `NOT_DEFINED` |
| `aggregate_authorized` | boolean | Must be false |
| `publication_evidence` | boolean | Must be false |

Denominator rows record coverage only. They do not authorize percentages.

## D3 comparison authorization

The D3 JSON must retain:

```text
member_level_projection=AUTHORIZED_FOR_INTERNAL_VALIDATION
family_specific_descriptive_comparison=NOT_YET_AUTHORIZED
pooled_cross_treatment_aggregation=NOT_PERMITTED
success_rate_or_percentage=NOT_PERMITTED
inferential_statistics=NOT_PERMITTED
treatment_superiority=NOT_PERMITTED
publication_evidence=false
```

## Event-log fields

Event entries retain all fields emitted by the simulator/controller. Common fields include `event_seq`, `event`, `contact`, `logical_time`, `phase`, `attempt`, `kind`, `target`, `alignment`, `reason`, and `publication_evidence`.

Event logs are diagnostic evidence, not causal findings.

## Exclusion and rerun records

Exclusion records identify run/row, reason code, description, evidence, whether outcome was known, disposition, and linked rerun. Allowed reasons are execution failure, corrupt output, schema failure, checksum failure, configuration mismatch, catalog-oracle mismatch, or predeclared protocol correction.

Rerun records identify the superseded run, authorized reason, corrective commit/input changes, and rule separating old/new data.

Outcome-seeking exclusion or rerun is prohibited.

## Manifest layers

| Manifest | Scope |
|---|---|
| `derived/phase-15-matched-family-derived.sha256` | D3 JSON and two CSV files |
| `manifests/raw.sha256` | Retained inputs and raw T1/baseline outputs |
| `manifests/derived.sha256` | Complete D3 derived directory, including internal manifest |
| `manifests/analysis.sha256` | Phase 08 analysis outputs |
| `manifests/run-bundle.sha256` | Every retained run file except itself |

Checksum verification establishes byte identity only.

## Outcome vocabulary

The repository may produce `SUCCESS`, `INDETERMINATE`, `SECURE_DEGRADED`, `EXPIRED`, `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`.

These are model classifications. They do not establish formal security, real-world recoverability, conformance, or operational-spacecraft behavior.

## Current status boundaries

D1–D3 are locally validated, CI pending. D3B is implemented pending local and CI validation.

Metric parity does not establish semantic parity. Semantic family membership does not establish causal equivalence. Executable D3 rows do not authorize family-level interpretation. Immutable D3B capture does not create publication evidence.

## Schema-change rule

Any field addition, removal, rename, unit change, interpretation change, or manifest-scope change requires:

1. schema-version review;
2. migration or incompatibility note;
3. validator and test updates;
4. a new immutable run directory; and
5. updated manuscript data-availability language.
