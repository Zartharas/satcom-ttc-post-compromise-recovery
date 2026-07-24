# Source Note: Poettering-Rösler URKE

## Source

Bertram Poettering and Paul Rösler, *Asynchronous Ratcheted Key Exchange*,
full version associated with CRYPTO 2018 work on bidirectional ratcheted key exchange.

## Points used by this project

- URKE combines a hash-chain state with fresh KEM encapsulations.
- The sender state includes an epoch, chaining state, and the receiver's current public key.
- On sending, the sender encapsulates to that public key, derives the session and next state,
  and updates the receiver public key used for the next send.
- The receiver correspondingly updates its secret state for each accepted ciphertext.
- The paper provides unidirectional, sesquidirectional, and bidirectional constructions.
- The more asynchronous bidirectional variants require more complex multi-epoch machinery and
  stronger primitives.

## Selection rationale

The unidirectional pattern is the smallest construction that matches this study's primary
ground-to-space fresh-entropy path. It also permits a generic KEM abstraction and makes
one-sided evolution observable without importing the full bidirectional design.

## Modeling boundary

This repository does not implement the paper's cryptographic algorithms or claim its proof.
The TT&C role mapping, operational-key activation, state deletion, status telemetry, and
lockout classification are experimental model decisions.

## Phase 04 strict baseline

Ground evolves on send; spacecraft evolves on accepted receipt. Prior state is deleted at the
respective evolution point. No skipped-state cache, rollback state, or recovery checkpoint is
available.
