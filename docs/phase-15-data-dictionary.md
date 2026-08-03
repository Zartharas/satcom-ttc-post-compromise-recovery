# Phase 15 Data Dictionary

## Status

`PROVISIONAL_CAPTURE_SCHEMA_NOT_FROZEN`

This dictionary defines the fields expected from the Phase 15 pilot and later publication-candidate workflow. It is descriptive of the current abstract simulator and capture design. It does not authorize a security, causal, or treatment-effectiveness claim.

## Dataset layers

| Layer | Purpose | Editing rule |
|---|---|---|
| Configuration | Declares the exact experiment inputs | Versioned; never edited after a run begins |
| Run metadata | Records environment, command, commit, timing, and provenance | Immutable after capture |
| Raw result JSON | Preserves complete config, schedule, metrics, and event log per seed | Immutable |
| Metrics CSV | Provides flat analysis-ready values | Regenerated from raw data only |
| Processed analysis | Contains summaries, audits, and sensitivity outputs | Must identify sources and script commit |
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
| `config_path` | path string | yes | Configuration used for the run |
| `config_sha256` | 64-character hex string | yes | SHA-256 of exact configuration bytes |
| `protocol_path` | path string | yes | Machine-readable protocol candidate |
| `protocol_sha256` | 64-character hex string | yes | SHA-256 of protocol bytes |
| `python_version` | string | yes | Interpreter version |
| `platform` | string | yes | Operating system and architecture |
| `command` | string array | yes | Exact executable and arguments |
| `exit_code` | integer | yes | Process exit code |
| `stdout_path` | path string | yes | Retained standard-output log |
| `stderr_path` | path string | yes | Retained standard-error log |
| `manifest_path` | path string | yes | Run-level SHA-256 manifest |
| `notes` | string | no | Non-interpretive operational notes |

## Raw experiment-result object

Each seed produces one logical experiment result.

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `schema_version` | string | yes | Result schema version |
| `status` | enum | yes | Provisional internal status recorded by the runner |
| `config` | object | yes | Per-result execution inputs |
| `schedule` | array | yes | Canonically ordered fault actions |
| `metrics` | object | yes | Outcome and measurement fields |
| `event_log` | array | yes | Ordered abstract execution events |

## Per-result configuration

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `seed` | integer | yes | Input to deterministic schedule generation |
| `ground_epoch` | integer | yes | Initial abstract ground epoch |
| `spacecraft_epoch` | integer | yes | Initial abstract spacecraft epoch |
| `authority_epoch_floor` | integer | yes | Minimum authority epoch used by the controller |
| `max_transmissions` | integer | yes | Maximum bounded transmissions per recovery phase |
| `candidate_lifetime_contacts` | integer | yes | Candidate lifetime in discrete contact windows |
| `max_faults` | integer | yes | Upper bound supplied to schedule generation |
| `compromise_active_keys` | boolean | yes | Whether initial active keys are marked compromised in the abstract model |
| `allowed_faults` | string array | yes | Fault kinds available to the deterministic generator |

## Schedule-action fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `phase` | enum | yes | Protocol phase receiving the fault action |
| `attempt` | integer | yes | One-based phase attempt index |
| `kind` | enum | yes | Fault kind |
| `target` | enum/string | yes | Abstract target such as `ground`, `spacecraft`, or `link` |
| `contacts` | integer | yes | Contact-window duration used by delay-like actions |

Supported phases are:

- `RECOVERY_PREPARE`
- `RECOVERY_RESPONSE`
- `RECOVERY_COMMIT`
- `RECOVERY_CONFIRM`
- `TEST_COMMAND`
- `STATUS_TELEMETRY`

Supported fault kinds are:

- `DROP`
- `DELAY`
- `DUPLICATE`
- `REORDER`
- `CONTACT_CLOSE`
- `ENDPOINT_RESTART`
- `STALE_COUNTER`
- `STALE_REPLAY`

## Metric fields

| Field | Type | Unit/domain | Interpretation boundary |
|---|---|---|---|
| `seed` | integer | identifier | Reproduction input, not the complete schedule identity |
| `schedule_sha256` | string | SHA-256 | Authoritative identity of the canonical serialized schedule |
| `outcome` | enum | model classification | Abstract outcome, not proof of cryptographic security |
| `alignment` | string | abstract joint state | Ground/spacecraft state relation under the model |
| `security_state` | string | abstract category | Must remain separate from availability |
| `availability_state` | string | abstract category | Must remain separate from security |
| `recovery_duration_contacts` | integer | contact windows | Discrete modeled contacts, not wall-clock seconds |
| `divergent_contact_windows` | integer | contact windows | Windows where abstract endpoints are not synchronized |
| `degraded_contact_windows` | integer | contact windows | Windows marked degraded by the model |
| `total_transmissions` | integer | count | Abstract transmitted message attempts |
| `retry_overhead` | integer | count | Attempts beyond the no-retry path under current instrumentation |
| `fault_count` | integer | count | Number of serialized scheduled fault actions |
| `drop_count` | integer | count | Scheduled/applied drop actions counted by the runner |
| `delay_count` | integer | count | Delay actions |
| `duplicate_count` | integer | count | Duplicate actions |
| `reorder_count` | integer | count | Reorder actions |
| `contact_close_count` | integer | count | Contact-close actions |
| `restart_count` | integer | count | Endpoint-restart actions |
| `replay_count` | integer | count | Replay-related actions counted by the runner |
| `rejection_count` | integer | count | Total modeled message or state rejections |
| `replay_rejection_count` | integer | count | Rejections attributed to replay handling |
| `stale_state_rejection_count` | integer | count | Rejections attributed to stale state or counters |
| `command_accepted` | boolean | true/false | Whether the abstract post-recovery command was accepted |
| `telemetry_complete` | boolean | true/false | Whether expected abstract telemetry evidence completed |
| `verification_complete` | boolean | true/false | Whether the modeled verification condition completed |
| `active_key_compromised` | boolean | true/false | Whether the active abstract key remains marked compromised |

## Event-log fields

Event entries may differ by event type. Every entry should preserve all fields emitted by the controller. At minimum, each entry should provide enough information to reconstruct event order and the relevant phase or state transition.

| Field | Type | Required when available | Meaning |
|---|---|---:|---|
| `event` | string | yes | Event label |
| `contact` | integer | yes | Current contact-window index |
| `phase` | string | phase-specific | Recovery or observation phase |
| `attempt` | integer | attempt-specific | Attempt number |
| `kind` | string | fault-specific | Applied fault kind |
| `target` | string | fault/restart-specific | Abstract target |
| `alignment` | string | state-specific | Joint state after or during event |
| `reason` | string | terminal/rejection-specific | Machine-readable reason |

The event log is diagnostic evidence. Event labels are not causal findings and must not be converted into real-world operational claims.

## Exclusion record

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `exclusion_id` | string | yes | Unique exclusion record |
| `run_id` | string | yes | Affected run |
| `seed` | integer/null | yes | Affected seed, or null when the whole run failed |
| `recorded_at_utc` | RFC 3339 string | yes | Time exclusion was documented |
| `reason_code` | enum | yes | `EXECUTION_FAILURE`, `CORRUPT_OUTPUT`, `SCHEMA_FAILURE`, `CHECKSUM_FAILURE`, `CONFIG_MISMATCH`, or `PROTOCOL_CORRECTION` |
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

The current repository may produce classifications including `SUCCESS`, `INDETERMINATE`, `SECURE_DEGRADED`, `EXPIRED`, `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`.

These terms are model classifications. They do not establish formal security, real-world recoverability, protocol conformance, or operational-spacecraft behavior.

## Missing publication-parity data

B0, B1, and B2 do not yet emit the same contact-window, retry, event-log, and capture fields as T1. Therefore:

- no publication comparison may treat their deterministic unit-test counts as equivalent to T1 experiment rows;
- baseline metric schemas must be implemented or justified before the publication-candidate run; and
- any treatment-specific field that cannot be made comparable must be declared and excluded from cross-treatment inference before results are viewed.

## Schema-change rule

Any field addition, removal, rename, unit change, or interpretation change requires:

1. a schema-version increment;
2. a documented migration or incompatibility note;
3. validator and test updates;
4. a new run directory for affected captures; and
5. an updated manuscript data-availability description.
