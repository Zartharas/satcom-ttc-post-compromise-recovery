# Deterministic Simulator Architecture

## Components

1. Scenario Loader
2. Deterministic Event Queue ordered by logical time and insertion sequence
3. Ground Endpoint
4. Spacecraft Endpoint
5. Baseline Protocol Adapter for B0, B1, or B2
6. Provisional T1 Recovery Controller
7. Recovery Authority and Epoch-Floor Record
8. Contact and Link Scheduler
9. Adversary Model
10. Invariant Monitor
11. Outcome Evaluator
12. Append-only Evidence Writer

## Determinism

The first implementation uses explicit fault schedules. Later seeded scenario generation must
serialize the generated schedule before execution.

## Cryptographic abstraction

A key is an opaque identifier with epoch, lifecycle state, attacker-knowledge status, and endpoint
acceptance status. Algorithm names do not create security claims.

The T1 controller assumes that recovery-control messages are authenticated by an established
cryptographic core. It does not implement that core or inherit its proof.

## Baseline sequences

B0:

```text
OTAR_UPLOAD -> KEY_ACTIVATE -> TEST_COMMAND -> STATUS_TELEMETRY
```

B1:

```text
KEM_INIT -> KEM_RESPONSE -> KEM_CONFIRM -> TEST_COMMAND -> STATUS_TELEMETRY
```

B2:

```text
RATCHET_ADVANCE -> TEST_COMMAND -> STATUS_TELEMETRY
```

Status telemetry is evidence of completion, not a cryptographic ratchet acknowledgment.

## Provisional T1 sequence

```text
RECOVERY_PREPARE
  -> RECOVERY_RESPONSE
  -> RECOVERY_COMMIT
  -> RECOVERY_CONFIRM
  -> TEST_COMMAND
  -> STATUS_TELEMETRY
```

### Epoch negotiation

Ground proposes:

```text
max(ground epoch, recovery-authority epoch floor) + 1
```

Spacecraft selects:

```text
max(proposed epoch, spacecraft epoch + 1)
```

The selected target is returned in `RECOVERY_RESPONSE`. This prevents ground logic from reading
simulator-only peer state.

### Activation

- Prepare and response create only a bounded candidate.
- Spacecraft activates on an exact commit and stores one bounded activation receipt.
- An exact commit retry may re-emit confirmation from the receipt.
- Ground activates on an exact confirmation.
- Success requires a fresh test command and status telemetry after convergence.

### Retry and expiry

- Prepare, response, commit, and confirmation retransmissions are independently bounded.
- Exact retries reuse the same recovery binding while using a fresh message identifier.
- Conflicting bindings, repeated message identifiers, and unauthorized authorities are rejected.
- Expiry before activation yields `EXPIRED`.
- Confirmation-budget exhaustion after spacecraft activation yields provisional
  `SECURE_DEGRADED`, not automatic `LOCKED`.
- Missing command or status evidence after convergence yields `INDETERMINATE`.

## T1 interface

- `start_recovery()`
- `retry_prepare()`
- `spacecraft_accept_prepare()`
- `ground_accept_response()`
- `retry_commit()`
- `spacecraft_accept_commit()`
- `ground_accept_confirm()`
- `verify_recovery()`
- `expire_attempt()`
- `run_bounded_recovery()`

The interface specifies control-state behavior only.

## Development order

1. Validate schemas
2. Implement endpoint state and event queue
3. Implement and test B0
4. Implement and test B1
5. Implement and test B2
6. Freeze a provisional baseline-oracle candidate
7. Add the provisional T1 controller
8. Red-team T1 state transitions and outcome classes
9. Add seeded scenario generation and metrics
10. Stop for independent cryptography review before final oracle freeze or security claims
11. Select the final T1 treatment and experiment parameters
12. Integrate approved scenarios with NOS3/cFS

## Formal-methods path

After provisional T1 behavior stabilizes, encode the abstract state machine in TLA+ or an equivalent
model checker, focusing on epoch monotonicity, unique authority, replay rejection, exact-binding
retransmission, bounded pending states and receipts, no fallback to compromised state,
bounded-delivery termination, and reachable degraded or lockout states.

Formal modeling may be prepared before external review, but any claim that it establishes security
for a concrete protocol remains review-gated.
