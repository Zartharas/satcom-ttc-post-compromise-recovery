# Phase 04 Baseline Semantics Decision

## Decision status

**Locked for abstract implementation.** This decision fixes the B1 and B2 semantics that must
be stable before T1 is designed or coded.

## Why this phase exists

The Phase Three scaffold intentionally simplified both baselines. That simplification became
too strong in two places:

1. B1 treated loss of the final confirmation as automatic ground-space epoch divergence.
2. B2 advanced the spacecraft first and treated acknowledgment loss as the lockout event.

Neither behavior was sufficiently tied to the selected source construction. Phase 04 corrects
those assumptions.

## B1: Triple-KEM key update

### Source-supported behavior

Triple-KEM is modeled as a standalone three-message key exchange, not as a full secure
channel. Final keys are derived only once the handshake has completed for the party in
question, and key confirmation is mandatory. The proposal also states that missing or
out-of-order fragments cause the presented protocol to drop the connection unless another
layer supplies ordering and retransmission.

### Locked model

- Ground is the initiator.
- Spacecraft is the responder.
- Initiator cryptographic completion occurs after it constructs and sends the final
  confirmation.
- Responder cryptographic completion occurs only after it receives and validates that
  confirmation.
- Cryptographic completion does not itself define when an SDLS security association becomes
  operational.

The default experimental integration rule is
`DEFER_UNTIL_BILATERAL_COMPLETION`. Under this rule, loss of the final confirmation leaves
both endpoints on the previous operational SDLS epoch. The recovery attempt expires, and the
model records that the initiator completed cryptographically while the responder did not.

A second rule, `ACTIVATE_ON_LOCAL_COMPLETION`, is retained only as a negative control. It
allows the initiator to activate after local completion and demonstrates that final-confirmation
loss can then produce one-sided operational activation. This policy is not attributed to the
Triple-KEM authors.

### Consequence

B1 final-confirmation loss is no longer automatically classified as permanent lockout or
protocol-level divergence. The result depends on the explicit SDLS activation policy.

## B2: strict URKE state evolution

### Selected construction family

B2 uses the unidirectional ratcheted key-exchange pattern of Poettering and Rösler. Their URKE
construction combines KEM encapsulation with evolving sender and receiver state. The sender
updates after sending, and the receiver updates when it processes the ciphertext.

The unidirectional construction is selected instead of the full bidirectional construction
because this paper's primary compromise direction is ground-to-space recovery, and URKE uses
a generic KEM abstraction without importing the bidirectional construction's substantially
more complex concurrent-epoch machinery.

### TT&C role mapping

- Ground is the URKE sender.
- Spacecraft is the URKE receiver.
- A new ground-generated KEM encapsulation introduces fresh entropy.
- The strict sender deletes its prior state when sending the update.
- The spacecraft deletes its prior state after accepting the update.
- No skipped-state cache, rollback state, or recovery checkpoint exists.
- Status telemetry verifies completion but is not a ratchet transition.

### Locked fault behavior

- **Update dropped after sender evolution:** ground is ahead; strict baseline is locked.
- **Status telemetry lost after both endpoints evolve:** endpoints are synchronized, but the
  experiment outcome is indeterminate because completion evidence is missing.
- **Stale ground snapshot restored:** spacecraft is ahead; strict baseline is locked.
- **Replayed or non-forward update:** reject without state change.

### Attribution boundary

The simulator is URKE-inspired; it does not implement the original algorithms or inherit their
proof. The strict deletion and TT&C activation policy are experimental operational choices.

## Red-team review

### Risk: making B1 artificially strong

Deferring activation until bilateral completion adds an integration rule not supplied by the
key-exchange paper. The model therefore labels it explicitly and includes unilateral activation
as a negative control.

### Risk: making B2 artificially weak

The strict B2 intentionally has no skipped-state cache or rollback checkpoint. This is justified
only as a lower-bound recoverability baseline. T1 must later be compared against stronger
published recovery variants where suitable.

### Risk: conflating missing evidence with lost synchronization

Status-telemetry loss no longer changes cryptographic alignment. It changes the outcome from
success to indeterminate.

### Risk: overclaiming PCS

The simulator may demonstrate exclusion of modeled compromised key references after fresh
entropy. It cannot establish the cryptographic PCS proof of the source construction.

## Phase gate

T1 remains blocked until:

1. these semantics pass deterministic tests;
2. the B1 and B2 source mappings receive independent cryptography review; and
3. baseline fault outcomes are frozen for the experiment protocol.
