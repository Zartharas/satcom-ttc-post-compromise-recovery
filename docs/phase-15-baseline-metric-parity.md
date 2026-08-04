# Phase 15 Baseline Metric and Capture Parity

## Status

`IMPLEMENTED_PENDING_VALIDATION`

This document describes the Phase 15 adapter that executes the existing B0, B1, and B2 deterministic scenario catalog and emits the shared T1 metric fields.

The adapter does not change baseline transitions, expected outcomes, or the pending independent-review status. Its outputs are labeled `PILOT_INTERNAL_VALIDATION_ONLY` and are not publication evidence.

## Objective

WP15-D1 closes a structural capture gap: the T1 seeded runner already emits event logs, per-run metrics, JSON, CSV, provenance, and checksum-protected run bundles, while B0, B1, and B2 previously existed only as deterministic unit-test scenarios.

The adapter provides:

- execution of all 21 baseline catalog scenarios;
- validation against each existing catalog alignment and outcome oracle;
- normalized scenario schedules and SHA-256 identities;
- the complete shared `RecoveryMetrics` field set;
- baseline-specific treatment and scenario identifiers;
- JSON and CSV output;
- event-log retention;
- integration into the immutable Phase 15 pilot run directory;
- command, environment, configuration, and catalog provenance;
- raw and complete-bundle checksum coverage.

## Source artifacts

- Catalog: `tests/scenarios/baseline-test-catalog.json`
- Adapter: `src/ttc_recovery/baseline_metrics.py`
- Configuration: `experiments/configs/phase-15-baseline-parity.json`
- Runner: `experiments/scripts/run_phase15_baseline_parity.py`
- Capture wrapper: `experiments/scripts/run_phase15_pilot_capture.py`
- Tests: `tests/test_baseline_metrics.py`

## Treatment normalization

| Catalog label | Normalized treatment | Retained variant |
|---|---|---|
| `B0` | `B0` | `B0` |
| `B1` | `B1` | `B1` |
| `B1-STATUS-ENHANCED` | `B1` | `B1-STATUS-ENHANCED` |
| `B2-URKE` | `B2` | `B2-URKE` |

The normalized treatment supports grouping. The retained variant prevents the status-enhanced B1 integration from being silently merged with the three-message B1 policy.

## Shared metric schema

The baseline CSV includes every field declared by `RecoveryMetrics`:

- `seed`
- `schedule_sha256`
- `outcome`
- `alignment`
- `security_state`
- `availability_state`
- `recovery_duration_contacts`
- `divergent_contact_windows`
- `degraded_contact_windows`
- `total_transmissions`
- `retry_overhead`
- `fault_count`
- `drop_count`
- `delay_count`
- `duplicate_count`
- `reorder_count`
- `contact_close_count`
- `restart_count`
- `replay_count`
- `rejection_count`
- `replay_rejection_count`
- `stale_state_rejection_count`
- `command_accepted`
- `telemetry_complete`
- `verification_complete`
- `active_key_compromised`

Baseline-specific fields are:

- `treatment`
- `baseline_variant`
- `scenario_id`
- `other_fault_count`

## Adapter semantics

### Seed

`seed` is null for B0, B1, and B2. These rows come from named deterministic catalog scenarios rather than seeded generation.

A null seed is meaningful data and must not be replaced with zero or an invented seed.

### Schedule identity

`schedule_sha256` is the SHA-256 digest of a canonical JSON object containing:

- scenario ID;
- baseline variant;
- initial-state description;
- compromise scope;
- activation policy when present; and
- normalized fault actions.

This digest identifies the complete deterministic scenario adapter input. It is not a seed-derived T1 schedule hash.

### Contact windows

Each catalog scenario is represented as one discrete adapter contact:

```text
recovery_duration_contacts = 1
```

A terminal non-synchronized state contributes one `divergent_contact_windows` value. A synchronized terminal state contributes zero.

This convention permits schema-complete capture but does not establish operational timing equivalence with T1 or a spacecraft contact plan.

### Transmission counts

`total_transmissions` uses declared attempted-message counts for each scenario. The values represent the abstract messages needed by the modeled path, including a dropped or replayed message when the scenario requires one.

`retry_overhead` is the nonnegative difference between the scenario count and the declared no-fault reference for its retained baseline variant.

These are adapter values. They are not measured network packets, frames, bytes, RF transmissions, CCSDS exchanges, or wall-clock observations.

### Fault normalization

The adapter converts catalog faults into structured actions when the catalog describes a concrete disruption:

- upload, confirmation, status, or ratchet-update loss → `DROP`;
- required-fragment reordering → `REORDER`;
- stale ratchet-update replay → `STALE_REPLAY`;
- stale ground-state restoration → `ENDPOINT_RESTART` with a `STALE_GROUND_RESTORE` detail;
- active sender impersonation → adapter-specific `ACTIVE_SENDER_IMPERSONATION`.

Catalog phrases that describe assumptions or conditions, such as a passive attacker interval or fresh entropy, are not counted as delivery faults.

`other_fault_count` retains normalized actions that do not have a direct T1 fault-kind field.

### Security and availability

Security and availability remain separate dimensions.

- An active endpoint key known to the abstract attacker produces `UNSAFE`.
- A verified synchronized state without a known active key produces `SECURE_PROVISIONAL`.
- An expired, divergent, locked, or incompletely verified state produces `NOT_ESTABLISHED` unless the active key is already known.

Availability follows the existing T1 grouping:

- `SUCCESS` → `AVAILABLE`;
- `AVAILABLE_UNSAFE`, `INDETERMINATE`, or `SECURE_DEGRADED` → `DEGRADED`;
- other outcomes → `UNAVAILABLE`.

These labels describe model state only. They are not cryptographic proofs or operational availability measurements.

### Command and telemetry evidence

The original baseline simulator does not implement a concrete command protocol. The adapter derives `command_accepted`, `telemetry_complete`, and `verification_complete` from final abstract state and records an explicit `phase15_baseline_metric_adapter_complete` event.

These fields support schema and capture testing. They must remain identified as adapter-derived until a matched experiment design defines equivalent evidence transitions for every treatment.

## Oracle preservation

Before a row is emitted, the runner checks:

1. final alignment against `expected_alignment`;
2. final joint state when `expected_joint_state` exists; and
3. final outcome against `expected_outcome`.

Any mismatch terminates the run. The adapter may not silently rewrite the catalog or replace an unexpected result.

The catalog values remain design oracles pending independent review.

## Capture integration

The Phase 15 wrapper retains:

```text
config/phase-15-baseline-parity.json
config/baseline-test-catalog.json
raw/phase15-baseline-parity-results.json
raw/phase15-baseline-parity-metrics.csv
logs/command-baseline.txt
logs/baseline-stdout.log
logs/baseline-stderr.log
```

Run metadata records the baseline configuration and catalog hashes, the exact command, and the baseline exit code. The files are covered by `raw.sha256` and `run-bundle.sha256`.

## What parity now means

After successful validation, the repository may state:

> B0, B1, B2, and T1 emit a common set of captured metric fields under the Phase 15 pilot infrastructure.

It may not infer from that statement that:

- scenarios are matched across treatments;
- contact durations have identical semantics;
- fault distributions are equivalent;
- transmission counts are operationally comparable;
- the baselines are independently approved;
- T1 is more secure or effective;
- results establish PCS or cryptographic security; or
- the pilot is publication-grade evidence.

## Remaining work after WP15-D1

Metric-field and capture parity are necessary but not sufficient for comparative execution. The next design task must define a matched treatment-scenario matrix or formally justify where matching is impossible.

That matrix must be versioned before comparative aggregate outcomes are viewed.
