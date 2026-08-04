# Phase 15 Data Dictionary

## Status

`PROVISIONAL_CAPTURE_SCHEMA_NOT_FROZEN`

This dictionary defines the fields expected from the Phase 15 T1 pilot, deterministic B0/B1/B2 metric adapter, and later publication-candidate workflow. It is descriptive of the current abstract simulator and capture design. It does not authorize a security, causal, timing, or treatment-effectiveness claim.

## Dataset layers

| Layer | Purpose | Editing rule |
|---|---|---|
| Configuration | Declares exact T1 and baseline-adapter inputs | Versioned; never edited after a run begins |
| Catalog | Declares the 21 baseline design-oracle scenarios | Retained byte-for-byte in each capture bundle |
| Run metadata | Records environment, commands, commit, timing, and provenance | Immutable after capture |
| Raw result JSON | Preserves config, schedule, metrics, and event log per seed or scenario | Immutable |
| Metrics CSV | Provides flat analysis-ready values | Regenerated from raw data only |
| Processed analysis | Contains T1 summaries, audits, and sensitivity outputs | Must identify sources and script commit |
| Exclusion/rerun record | Explains technical exclusions or superseded attempts | Append-only |
| Checksum manifests | Verifies retained file bytes | Regenerated only for a new run directory |

## Run metadata fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `run_id` | string | yes | Unique identifier in the form `phase15-pilot-YYYYMMDDTHHMMSSZ-g<short_commit>` |
| `run_class` | enum | yes | `PILOT_INTERNAL_VALIDATION_ONLY` or a later explicitly authorized class |
| `start_time_utc` | RFC 3339 string | yes | UTC run start time |
| `end_time_utc` | RFC 3339 string | yes | UTC run completion time |
| `repository` | string | yes | Repository owner and name |
| `branch` | string | yes | Branch checked out at execution |
| `commit_sha` | 40-character hex string | yes | Exact source commit |
| `git_status` | string | yes | Exact recorded porcelain status or `CLEAN` |
| `config_path` | path string | yes | T1 pilot configuration used for the run |
| `config_sha256` | SHA-256 | yes | Digest of exact T1 configuration bytes |
| `baseline_config_path` | path string | yes | Retained baseline-parity configuration |
| `baseline_config_sha256` | SHA-256 | yes | Digest of exact baseline-parity configuration bytes |
| `baseline_catalog_path` | path string | yes | Retained baseline scenario catalog |
| `baseline_catalog_sha256` | SHA-256 | yes | Digest of exact retained catalog bytes |
| `protocol_path` | path string | yes | Machine-readable Phase 15 protocol candidate |
| `protocol_sha256` | SHA-256 | yes | Digest of protocol bytes |
| `analysis_config_path` | path string | yes | T1 descriptive-analysis configuration |
| `analysis_config_sha256` | SHA-256 | yes | Digest of analysis configuration bytes |
| `python_version` | string | yes | Interpreter version |
| `platform` | string | yes | Operating system and architecture |
| `runner_command` | string array | yes | Exact T1 executable and arguments |
| `runner_exit_code` | integer | yes | T1 runner exit code |
| `baseline_command` | string array | yes | Exact baseline-adapter executable and arguments |
| `baseline_exit_code` | integer | yes | Baseline runner exit code |
| `analysis_command` | string array/null | yes | Exact T1 analysis command when executed |
| `analysis_exit_code` | integer/null | yes | T1 analysis exit code when executed |
| `overall_exit_code` | integer | yes | First nonzero pipeline exit, otherwise zero |
| `stdout_paths` | path-string array | yes | Retained standard-output logs |
| `stderr_paths` | path-string array | yes | Retained standard-error logs |
| `claim_boundary` | object | yes | Prohibited interpretation flags |

## Raw experiment-result objects

A T1 seed produces one logical experiment result. A baseline catalog scenario produces one deterministic adapter result.

Shared result fields are:

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `schema_version` | string | yes | Result schema version |
| `status` | enum | yes | Provisional internal status recorded by the runner |
| `config` | object | yes | Per-result execution inputs or adapter context |
| `schedule` | array | yes | Canonically ordered fault actions |
| `metrics` | object | yes | Outcome and measurement fields |
| `event_log` | array | yes | Ordered abstract execution events |

Baseline results additionally retain:

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `metric_parity_status` | enum | yes | `IMPLEMENTED_PENDING_VALIDATION` during WP15-D1 |
| `treatment` | enum | yes | Normalized `B0`, `B1`, or `B2` treatment |
| `baseline_variant` | string | yes | Original catalog variant, including `B1-STATUS-ENHANCED` |
| `scenario_id` | string | yes | Catalog ID from `B0-01` through `B2-10` |

## T1 per-result configuration

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `seed` | integer | yes | Input to deterministic T1 schedule generation |
| `ground_epoch` | integer | yes | Initial abstract ground epoch |
| `spacecraft_epoch` | integer | yes | Initial abstract spacecraft epoch |
| `authority_epoch_floor` | integer | yes | Minimum authority epoch used by the controller |
| `max_transmissions` | integer | yes | Maximum bounded transmissions per recovery phase |
| `candidate_lifetime_contacts` | integer | yes | Candidate lifetime in discrete contact windows |
| `max_faults` | integer | yes | Upper bound supplied to schedule generation |
| `compromise_active_keys` | boolean | yes | Whether initial active keys are marked compromised |
| `allowed_faults` | string array | yes | Fault kinds available to the generator |

## Baseline adapter configuration context

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `initial_state` | string | yes | Catalog initial-state description |
| `compromise` | string | yes | Catalog compromise scope |
| `activation_policy` | string/null | yes | B1 policy when declared |
| `properties` | string array | yes | Catalog property labels |
| `adapter_semantics` | string | yes | Explicit reminder that timing and transmission counts are provisional adapter values |

## Schedule-action fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `phase` | enum/string | yes | Protocol or adapter phase receiving the fault action |
| `attempt` | integer | yes | One-based phase attempt index |
| `kind` | enum/string | yes | Fault kind |
| `target` | enum/string | yes | Abstract target such as `ground`, `spacecraft`, `link`, or `exchange` |
| `contacts` | integer | yes | Contact-window duration used by delay-like actions; baseline adapter actions currently use zero |
| `detail` | string | no | Additional normalized adapter detail, such as `STALE_GROUND_RESTORE` |

T1 phases are `RECOVERY_PREPARE`, `RECOVERY_RESPONSE`, `RECOVERY_COMMIT`, `RECOVERY_CONFIRM`, `TEST_COMMAND`, and `STATUS_TELEMETRY`.

Baseline adapter phases include `OTAR_UPLOAD`, `REQUIRED_FRAGMENT`, `KEM_CONFIRM`, `AUTHENTICATED_STATUS`, `RATCHET_UPDATE`, `RATCHET_STATE`, and `STATUS_TELEMETRY`.

Shared T1 fault kinds are `DROP`, `DELAY`, `DUPLICATE`, `REORDER`, `CONTACT_CLOSE`, `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY`. The adapter-specific `ACTIVE_SENDER_IMPERSONATION` action is retained through `other_fault_count` and must not be silently relabeled as a T1 fault kind.

## Shared metric fields

The following fields are emitted by both the T1 runner and baseline adapter:

| Field | Type | Unit/domain | Interpretation boundary |
|---|---|---|---|
| `seed` | integer/null | identifier | T1 reproduction input; null for deterministic baseline catalog scenarios |
| `schedule_sha256` | string | SHA-256 | T1 schedule identity or canonical deterministic baseline-scenario identity |
| `outcome` | enum | model classification | Abstract outcome, not proof of cryptographic security |
| `alignment` | string | abstract joint state | Ground/spacecraft state relation under the model |
| `security_state` | string | abstract category | Must remain separate from availability |
| `availability_state` | string | abstract category | Must remain separate from security |
| `recovery_duration_contacts` | integer | contact windows | T1 modeled contacts; baseline currently one adapter contact per catalog case |
| `divergent_contact_windows` | integer | contact windows | T1 observed windows or baseline terminal adapter indicator |
| `degraded_contact_windows` | integer | contact windows | Windows marked degraded by the current model/adapter rule |
| `total_transmissions` | integer | count | Abstract attempted messages; baseline values are declared adapter counts |
| `retry_overhead` | integer | count | Attempts beyond the treatment-specific no-retry reference |
| `fault_count` | integer | count | Number of normalized fault actions |
| `drop_count` | integer | count | Drop actions |
| `delay_count` | integer | count | Delay actions |
| `duplicate_count` | integer | count | Duplicate actions |
| `reorder_count` | integer | count | Reorder actions |
| `contact_close_count` | integer | count | Contact-close actions |
| `restart_count` | integer | count | Endpoint-restart or stale-restore adapter actions |
| `replay_count` | integer | count | Replay-related actions |
| `rejection_count` | integer | count | Total modeled message or state rejections |
| `replay_rejection_count` | integer | count | Rejections attributed to replay handling |
| `stale_state_rejection_count` | integer | count | Rejections attributed to stale state or counters |
| `command_accepted` | boolean | true/false | T1 observed command evidence or baseline adapter-derived final-state evidence |
| `telemetry_complete` | boolean | true/false | T1 observed telemetry evidence or baseline adapter-derived verification evidence |
| `verification_complete` | boolean | true/false | Whether the current model/adapter verification condition completed |
| `active_key_compromised` | boolean | true/false | Whether an active abstract endpoint key remains attacker-known |

## Baseline-specific metric fields

| Field | Type | Meaning |
|---|---|---|
| `treatment` | enum | Normalized `B0`, `B1`, or `B2` grouping |
| `baseline_variant` | string | Original catalog baseline label |
| `scenario_id` | string | Deterministic catalog scenario |
| `other_fault_count` | integer | Normalized adapter actions without a direct T1 fault-count field |

## Event-log fields

Event entries differ by event type. Every entry retains all fields emitted by the simulator or controller.

| Field | Type | Required when available | Meaning |
|---|---|---:|---|
| `event_seq` | integer | baseline events | Zero-based event order |
| `event` | string | yes | Event label |
| `contact` | integer | contact-specific | Current contact index or adapter contact |
| `logical_time` | integer | scheduled baseline events | Simulator logical dispatch time |
| `phase` | string | phase-specific | Recovery or adapter phase |
| `attempt` | integer | attempt-specific | Attempt number |
| `kind` | string | fault-specific | Applied fault kind |
| `target` | string | fault/restart-specific | Abstract target |
| `alignment` | string | state-specific | Joint state after or during event |
| `reason` | string | terminal/rejection-specific | Machine-readable reason |
| `publication_evidence` | boolean | adapter completion event | Must remain false for the pilot |

The event log is diagnostic evidence. Event labels are not causal findings and must not be converted into real-world operational claims.

## Exclusion record

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `exclusion_id` | string | yes | Unique exclusion record |
| `run_id` | string | yes | Affected run |
| `seed` | integer/null | yes | Affected T1 seed or null |
| `scenario_id` | string/null | yes | Affected baseline scenario or null |
| `recorded_at_utc` | RFC 3339 string | yes | Time exclusion was documented |
| `reason_code` | enum | yes | `EXECUTION_FAILURE`, `CORRUPT_OUTPUT`, `SCHEMA_FAILURE`, `CHECKSUM_FAILURE`, `CONFIG_MISMATCH`, `CATALOG_ORACLE_MISMATCH`, or `PROTOCOL_CORRECTION` |
| `description` | string | yes | Factual explanation |
| `evidence_paths` | string array | yes | Logs or validation records supporting the exclusion |
| `outcome_known_before_decision` | boolean | yes | Transparency field; does not authorize outcome-based exclusion |
| `disposition` | enum | yes | `EXCLUDED`, `RETAINED_WITH_WARNING`, or `SUPERSEDED_BY_RERUN` |
| `rerun_id` | string/null | yes | Linked rerun when applicable |

## Rerun record

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `rerun_id` | string | yes | New immutable run identifier |
| `supersedes_run_id` | string | yes | Earlier attempt |
| `authorized_reason` | string | yes | Reason allowed by the protocol |
| `correction_commit` | string/null | yes | Corrective commit when code or configuration changed |
| `comparison_rule` | string | yes | How old and new attempts are separated analytically |

## Outcome vocabulary

The repository may produce `SUCCESS`, `INDETERMINATE`, `SECURE_DEGRADED`, `EXPIRED`, `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`.

These terms are model classifications. They do not establish formal security, real-world recoverability, protocol conformance, or operational-spacecraft behavior.

## Current parity status

B0, B1, and B2 now emit the complete shared metric field set and are included in the Phase 15 immutable capture bundle. The status remains:

`IMPLEMENTED_PENDING_VALIDATION`

This closes metric-field and capture-structure gaps only. It does not establish matched treatment scenarios, equivalent contact semantics, equivalent fault distributions, operational transmission comparability, or publication-grade evidence.

A matched treatment-scenario matrix or a predeclared justification for unmatched cases remains mandatory before comparative aggregate analysis.

## Schema-change rule

Any field addition, removal, rename, unit change, or interpretation change requires:

1. a schema-version increment;
2. a documented migration or incompatibility note;
3. validator and test updates;
4. a new run directory for affected captures; and
5. an updated manuscript data-availability description.
