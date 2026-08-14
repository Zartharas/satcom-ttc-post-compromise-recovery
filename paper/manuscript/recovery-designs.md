# 4. Recovery Designs

The study uses three abstract baselines and one recovery-control treatment. The baselines are not
claimed to be complete implementations of the cited standards or cryptographic constructions.
They preserve only the state transitions needed for the controlled comparison.

## 4.1 B0 — SDLS Extended Procedures-style symmetric rekeying

B0 represents a conventional symmetric over-the-air rekeying path motivated by SDLS Extended
Procedures [@ccsds_sdls_ep_355_1_b_1]. Its abstract sequence is:

```text
OTAR_UPLOAD -> KEY_ACTIVATE -> TEST_COMMAND -> STATUS_TELEMETRY
```

The baseline assumes that an uncompromised higher-level symmetric recovery/master capability
survives the operational-key compromise represented by the scenario. A fresh operational key is
uploaded, activated, and then tested through modeled command and telemetry evidence.

B0 is intentionally an **SDLS EP-style abstraction**, not a CCSDS conformance implementation.
The simulator does not encode every SDLS security-association procedure, key-management data unit,
or cryptographic mechanism.

## 4.2 B1 — Triple-KEM/PQNoise-inspired key update

B1 is motivated by the three-message SDLS key-update mechanism of Hülsing, Lange, and Weber
[@hulsing_lange_weber_sdls_key_update]:

```text
KEM_INIT -> KEM_RESPONSE -> KEM_CONFIRM -> TEST_COMMAND -> STATUS_TELEMETRY
```

The ground is mapped to the initiator and the spacecraft to the responder. Source-supported
cryptographic completion is tracked separately at each endpoint.

The source construction requires confirmation but does not define the simulator's operational
SDLS activation rule. We therefore model two explicit policies.

### 4.2.1 Local-completion activation

`ACTIVATE_ON_LOCAL_COMPLETION` is the minimum-assumption mapping. Ground activates after its
local cryptographic completion when it constructs/sends the final confirmation. Spacecraft
activates only after receiving and validating that confirmation. Loss of the final confirmation
can therefore leave ground ahead.

### 4.2.2 Authenticated-status gating

`DEFER_UNTIL_AUTHENTICATED_STATUS` is an enhanced project-defined integration. Spacecraft
activates after completing the three-message exchange and sends authenticated status under the
candidate state; ground activates only after receiving that status.

This fourth-message variant reduces one activation ambiguity but introduces another final-message
boundary if the authenticated status itself is lost. It is retained as a separate policy trace,
not attributed to the Triple-KEM authors and not counted as an independent B1 replication in the
matched analysis.

## 4.3 B2 — strict ratcheted state evolution

B2 is motivated by the unidirectional state-evolution pattern in ratcheted key exchange
[@poettering_roesler_bidirectional_rke; @poettering_roesler_async_rke]. Ground is the sender and
spacecraft is the receiver.

The strict operational abstraction deliberately uses sender-state advancement when the update is
sent; receiver-state advancement only when the update is accepted; no skipped-state cache; no
rollback state; no recovery checkpoint; and telemetry as evidence rather than as a ratchet
transition.

This creates observable failure boundaries. If the sender deletes prior state and the update is
lost, the ground can become ahead with no modeled strict-ratchet transition back. A stale ground
snapshot can similarly leave the spacecraft ahead. Replayed or non-forward updates are rejected
without state change.

B2 also distinguishes traffic-key exposure from sender-state, receiver-state, and both-endpoint
state exposure. This distinction is essential because state exposure has different implications
from disclosure of one output traffic key. The simulator does not inherit the source paper's
cryptographic proof.

## 4.4 T1 — bounded resynchronization treatment

T1 surrounds an opaque authenticated recovery-control core with an explicit operational state
machine:

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

Every recovery-control message is bound to the spacecraft identity, recovery identifier, epoch
information, authority/counter, transcript reference, and—after response—the candidate key
reference.

### 4.4.1 Candidate isolation

PREPARE and RESPONSE create only a bounded candidate. Candidate state cannot authorize ordinary
command traffic. This separates possession of proposed recovery material from operational
activation.

### 4.4.2 Forward epoch negotiation

Ground proposes an epoch above both its current state and the recovery-authority floor.
Spacecraft selects an epoch at least one greater than its own active epoch and at least as great as
the proposal. The selected value returns in RESPONSE.

This allows the same recovery flow to address either ground-ahead or spacecraft-ahead state
without permitting ground code to inspect hidden spacecraft state.

### 4.4.3 Asymmetric activation and receipt

Spacecraft activates only on an exact, fresh COMMIT and retains one bounded activation receipt.
Ground activates only after validating CONFIRM.

If COMMIT is retransmitted exactly after spacecraft activation, the receipt permits the
spacecraft to re-emit CONFIRM without activating the candidate twice. A conflicting binding,
repeated message identifier, unauthorized authority, stale counter, or incompatible transcript is
rejected without replacing accepted operational state.

### 4.4.4 Bounded retries and expiry

PREPARE, RESPONSE, COMMIT, and CONFIRM each have bounded transmission opportunities. Exact retries
preserve the transaction binding while using fresh message identifiers. Candidate and receipt
lifetimes are bounded in modeled contact windows.

Exhaustion before activation produces `EXPIRED`. Confirmation exhaustion after spacecraft
activation may leave the spacecraft ahead and produce the historical `SECURE_DEGRADED` raw
outcome; the independent security-state dimension determines whether that state is safe.

### 4.4.5 Verification

Endpoint convergence is not sufficient for `SUCCESS`. The treatment requires a fresh test
command under the new state followed by authenticated status telemetry. Loss of either evidence
opportunity after convergence yields `INDETERMINATE`.

This verification step is the operational bridge between “the endpoints appear to share new
state” and “the modeled TT&C path has demonstrated post-transition command/telemetry function.”

## 4.5 Treatment boundaries

T1 is not a new cryptographic primitive and does not replace the cryptographic construction that
would authenticate recovery-control messages or derive candidate keys. It tests control-state
behavior under assumed cryptographic authenticity and fresh candidate material.

Likewise, B0–B2 are comparison abstractions, not claims of SDLS, Triple-KEM, or ratcheted-key-
exchange conformance. The experiment therefore compares terminal operational behavior only where
the semantics are sufficiently aligned and avoids importing cryptographic proofs into the
simulator.
