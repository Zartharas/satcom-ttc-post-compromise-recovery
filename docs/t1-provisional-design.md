# Provisional T1 Bounded-Resynchronization Design

## Status

**Provisional and internally reviewed only.** This phase implements an abstract recovery-control
state machine so the research can continue without presenting T1 as an independently validated
cryptographic protocol.

T1 does not replace the selected cryptographic core. It adds bounded recovery state, explicit
activation control, retransmission behavior, and verification evidence around an opaque candidate
key reference.

## Research objective

The treatment tests whether bounded, replay-resistant recovery control can reduce the permanent
lockout observed in the strict B2 baseline after ground-space state divergence.

It must not:

- reactivate a prior compromised epoch;
- maintain multiple authoritative operational epochs;
- depend on simulator-only knowledge of the peer's active state;
- retain candidates, receipts, or retries without a configured bound;
- treat candidate generation or endpoint convergence alone as successful recovery.

## Provisional message flow

```text
Ground                         Spacecraft
  |                                |
  |---- RECOVERY_PREPARE --------->|
  |<--- RECOVERY_RESPONSE ---------|
  |---- RECOVERY_COMMIT ---------->|
  |<--- RECOVERY_CONFIRM ----------|
  |---- TEST_COMMAND ------------->|
  |<--- STATUS_TELEMETRY ---------|
```

Every recovery-control message binds the spacecraft identity, recovery ID, epoch information,
recovery-authority counter, transcript reference, authorized authority, and—after response—the
candidate key reference.

## Epoch selection without a hidden oracle

The ground proposes:

```text
max(ground active epoch, recovery-authority epoch floor) + 1
```

The spacecraft selects:

```text
max(proposed epoch, spacecraft active epoch + 1)
```

The exact selected epoch is returned in `RECOVERY_RESPONSE`. This lets the same flow address either
`G_AHEAD` or `S_AHEAD` without allowing ground logic to read the spacecraft's simulator state
directly.

## Activation boundary

`RECOVERY_PREPARE` and `RECOVERY_RESPONSE` create only a bounded candidate. The candidate cannot
authorize normal commands.

On an exact, fresh `RECOVERY_COMMIT`, the spacecraft activates the candidate and retains one bounded
activation receipt. The ground activates only after validating `RECOVERY_CONFIRM`.

An exact commit retransmission may use the receipt to re-emit confirmation without a second
spacecraft activation. A conflicting commit, replayed message identifier, unauthorized authority,
or mismatched binding is rejected without changing operational state.

## Bounded failure behavior

- Prepare, response, commit, and confirmation may be retransmitted within a configured transmission
  budget.
- Only one pending candidate is permitted at each endpoint.
- Candidate and activation-receipt lifetimes are bounded by contact count.
- If delivery is exhausted before either endpoint activates, the attempt is `EXPIRED`.
- If the spacecraft activated but all confirmations were lost, the attempt is
  `SECURE_DEGRADED`: operational synchronization is incomplete, but permanent `LOCKED` is not
  asserted while the abstract recovery-control path remains available.
- If both endpoints converge but test-command or status evidence is missing, the outcome is
  `INDETERMINATE`.

No liveness claim is made against indefinite suppression.

## Success condition

`SUCCESS` requires all of the following:

1. ground and spacecraft use the same forward epoch and candidate key reference;
2. a fresh command under that state is accepted;
3. authenticated status telemetry is received;
4. the active candidate is not marked compromised;
5. append-only records show the prepare, response, commit, confirmation, command, and status path.

## Threat and claim boundary

The controller treats cryptographic values as opaque references. It does not establish that an
attacker cannot derive, forge, or distinguish those values. The model can test recovery-control
logic and fault handling, but it cannot prove post-compromise security.

The recovery authority is modeled as independent of the compromised operational traffic key. A
future cryptographic design must justify that assumption and define how its counter and credentials
survive endpoint rollback.

## External-review stop points

Work may continue on abstract code, deterministic tests, scenarios, metrics, and seeded simulation
scaffolding.

Independent cryptography review becomes mandatory before any of the following:

- changing the Phase 05 oracle candidate to `ACCEPTED` or `FROZEN`;
- naming this provisional controller as the final T1 treatment;
- freezing final experiment parameters or the complete experiment protocol;
- interpreting simulation output as evidence of post-compromise security;
- implementing real cryptographic primitives or claiming protocol/CCSDS conformance;
- using NOS3/cFS integration as publication evidence;
- submitting the manuscript or making external security claims.

## Phase 06 evaluation target

Phase 06 evaluates internal consistency only:

- both `G_AHEAD` and `S_AHEAD` recovery;
- bounded loss of each recovery-control message;
- idempotent retransmission;
- candidate isolation;
- unauthorized and conflicting message rejection;
- replay rejection;
- operational-key replacement after a finite passive interval;
- explicit `SUCCESS`, `INDETERMINATE`, `EXPIRED`, and `SECURE_DEGRADED` outcomes.

The expected outcomes remain provisional and may change after independent review.
