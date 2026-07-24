# Deterministic Simulator Architecture

## Components

1. Scenario Loader
2. Deterministic Event Queue ordered by logical time and insertion sequence
3. Ground Endpoint
4. Spacecraft Endpoint
5. Protocol Adapter for B0, B1, or B2
6. Contact and Link Scheduler
7. Adversary Model
8. Invariant Monitor
9. Outcome Evaluator
10. Append-only Evidence Writer

## Determinism

The first implementation uses explicit fault schedules. Later seeded scenario generation
must serialize the generated schedule before execution.

## Cryptographic abstraction

A key is an opaque identifier with epoch, lifecycle state, attacker-knowledge status,
and endpoint acceptance status. Algorithm names do not create security claims.

## Baseline sequences

B0: OTAR_UPLOAD -> KEY_ACTIVATE -> TEST_COMMAND -> STATUS_TELEMETRY

B1: KEM_INIT -> KEM_RESPONSE -> KEM_CONFIRM -> TEST_COMMAND -> STATUS_TELEMETRY

B2: RATCHET_ADVANCE -> RATCHET_ACK -> TEST_COMMAND -> STATUS_TELEMETRY

## T1 interface

- prepare_recovery()
- accept_prepare()
- commit_candidate()
- confirm_activation()
- expire_candidate()
- retry_within_bounds()
- verify_recovery()

The interface does not specify cryptographic internals.

## Development order

1. Validate schemas
2. Implement endpoint state and event queue
3. Implement B0
4. Implement B1
5. Implement B2
6. Implement invariant monitor
7. Run baseline catalog
8. Freeze baseline behavior
9. Review T1 candidates
10. Add T1
11. Integrate selected scenarios with NOS3/cFS

## Formal-methods path

After baseline semantics stabilize, encode the abstract state machine in TLA+ or an
equivalent model checker, focusing on epoch monotonicity, unique authority, replay
rejection, bounded pending states, no fallback to compromised state, bounded-delivery
termination, and reachable lockout states.
