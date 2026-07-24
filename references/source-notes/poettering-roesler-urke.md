# Source Note: Poettering-Rösler URKE

## Source

Bertram Poettering and Paul Rösler, *Asynchronous Ratcheted Key Exchange*, full version
associated with the CRYPTO 2018 work on bidirectional ratcheted key exchange.

## Construction points used by this project

- URKE defines separate sender and receiver states.
- `snd` returns an updated sender state, a session key, and a ciphertext.
- `rcv` returns an updated receiver state and matching session key or rejects.
- The construction combines evolving chaining state, authentication state, transcripts, and a
  fresh KEM encapsulation.
- The sender evolves when sending; the receiver evolves when accepting the ciphertext.

## Exposure semantics used by this project

The source distinguishes key reveal from state exposure.

- Revealing a traffic key does not by itself expose future ratchet state.
- Exposing an in-sync receiver lets an adversary trace later receiver keys and corresponding
  sender keys.
- Exposing the sender permits impersonation with copied state; if the adversary advances the
  receiver first, the receiver becomes out of sync on an attacker-known branch.
- Exposing the sender without bringing the receiver out of sync does not harm later keys in the
  source model.
- URKE does not generally recover once receiver-state tracing or sender-state impersonation has
  made future keys weak; the paper introduces stronger directional constructions for recovery
  from broader state-exposure attacks.

## Selection rationale

The unidirectional pattern is the smallest construction matching the study's primary
ground-to-space fresh-entropy path. It uses a generic KEM abstraction and makes one-sided
evolution observable without importing full bidirectional concurrent-epoch machinery.

## Modeling boundary

This repository does not implement the source algorithms or inherit their proof. TT&C role
mapping, operational activation, strict deletion, status telemetry, and lockout classification are
experimental model decisions.
