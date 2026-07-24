# Phase 04 Baseline Semantics Decision

## Decision status

**Corrected and locked for abstract implementation.** This revision resolves the adversarial
review findings that blocked PR #1 from merge.

## Why the correction was required

The first Phase 04 implementation still contained two unfair abstractions:

1. B1 used simulator-wide knowledge to activate both endpoints only after the simulator knew
   that the final Triple-KEM confirmation had arrived.
2. B2 represented all compromise as disclosure of the current traffic key even though the URKE
   source distinguishes traffic-key reveal, sender-state exposure, and receiver-state exposure.

The corrected model removes the hidden B1 oracle and makes B2 compromise scope explicit.

## B1: Triple-KEM key update

### Source-supported behavior

Triple-KEM is a standalone three-message key exchange that provides a fresh key for SDLS.
Final keys are derived only after the handshake has completed for the party in question, and key
confirmation is mandatory. The source does not define SDLS operational-key activation, rollback,
or a post-handshake installation acknowledgment.

### Primary baseline: local-completion activation

The minimum-assumption integration policy is `ACTIVATE_ON_LOCAL_COMPLETION`:

- Ground is the initiator.
- Spacecraft is the responder.
- Ground cryptographically completes after constructing and sending `KEM_CONFIRM`.
- Ground activates its candidate SDLS epoch after that local completion.
- Spacecraft cryptographically completes and activates only after receiving and validating
  `KEM_CONFIRM`.

Consequently, loss of `KEM_CONFIRM` produces `G_AHEAD` and `DIVERGED`. This is the primary
B1 baseline because it adds no hidden bilateral-delivery oracle and no extra protocol message.

### Enhanced comparison: authenticated-status gating

`DEFER_UNTIL_AUTHENTICATED_STATUS` is retained as an explicitly enhanced four-message
integration policy:

1. Triple-KEM completes through `KEM_CONFIRM`.
2. Spacecraft activates and sends authenticated status under the candidate state.
3. Ground activates after receiving that status.

This extension avoids ground activation when `KEM_CONFIRM` is lost, but it does not eliminate
the last-message problem. If authenticated status is lost, spacecraft is ahead and the outcome is
`DIVERGED`. Solving that uncertainty would require another acknowledgment, bounded rollback, or
a recovery mechanism and therefore belongs outside the B1 source protocol.

### Attribution boundary

Neither activation policy is attributed to the Triple-KEM authors. The source supports
party-specific cryptographic completion and mandatory confirmation; this repository supplies and
labels the operational SDLS integration rules.

## B2: strict URKE state evolution

### Selected construction family

B2 uses the Poettering-Rösler unidirectional ratcheted key-exchange pattern with ground as sender
and spacecraft as receiver. The sender evolves in `snd`; the receiver evolves in `rcv` after
accepting the ciphertext. The strict TT&C baseline retains no skipped-state cache, rollback state,
or recovery checkpoint.

### Explicit compromise scopes

The simulator distinguishes:

- `NONE`
- `TRAFFIC_KEY`
- `SENDER_STATE`
- `RECEIVER_STATE`
- `BOTH_ENDPOINT_STATES`

These scopes are not interchangeable.

#### Traffic-key exposure

Disclosure of the current output traffic key does not itself expose the evolving URKE state. A
fresh legitimate update can replace that exposed key in the abstract model.

#### Sender-state exposure

The URKE analysis states that sender-state exposure does not harm later keys if the adversary does
not use the copied sender state to bring the receiver out of sync. Under a passive recovery
interval, the next legitimate update is therefore modeled as restoring a secret active key.

If an active adversary uses copied sender state first, it can impersonate the sender, advance the
spacecraft onto an attacker-known branch, and leave the legitimate ground state behind. The
strict TT&C adaptation classifies that path as `S_AHEAD` and `LOCKED`.

#### Receiver-state exposure

An exposed in-sync receiver state allows the adversary to trace later receiver keys and, by
correctness, corresponding sender keys. A normal future update may remain operationally aligned,
but the resulting key is attacker-known, so the outcome is `AVAILABLE_UNSAFE`.

#### Both endpoint states

Receiver-state traceability dominates. With both states exposed, a normal aligned update remains
`AVAILABLE_UNSAFE` in the strict URKE model.

### Other locked B2 faults

- Update lost after sender evolution: `G_AHEAD`, `LOCKED`.
- Status telemetry lost after both endpoints evolve: `SYNC`, `INDETERMINATE`.
- Stale ground snapshot restored: `S_AHEAD`, `LOCKED`.
- Replayed or non-forward update: reject without state change.

## Red-team conclusions

### Baseline fairness

B1 no longer receives a hidden fourth-message oracle. The enhanced status-gated variant is
measured separately and exposes its own final-message failure.

### Compromise precision

B2 no longer turns traffic-key disclosure into a claim about state-exposure recovery. Sender and
receiver exposure are encoded separately according to the source model.

### Claim boundary

The simulator demonstrates state and attacker-knowledge consequences under an abstract model. It
does not inherit the source papers' proofs, establish formal PCS, or claim CCSDS conformance.

## Phase gate

T1 remains blocked until:

1. the corrected 19-test suite passes locally and in CI;
2. B1 and B2 semantic mappings receive independent cryptography review; and
3. baseline outcomes are frozen in the experiment protocol.
