# Source Note: Poettering-Rösler Ratcheted Key Exchange

## Sources

Bertram Poettering and Paul Rösler, *Towards Bidirectional Ratcheted Key Exchange*, in
*Advances in Cryptology — CRYPTO 2018*, LNCS 10991, Springer, 2018, pp. 3–32.
DOI: `10.1007/978-3-319-96884-1_1`.

The project also uses the authors' extended asynchronous/unidirectional ratcheted-key-exchange
material, Cryptology ePrint Archive Report 2018/296.

## Construction points used by this project

- The unidirectional construction separates sender and receiver state.
- Sending returns updated sender state, a session key, and ciphertext.
- Receiving returns updated receiver state and the matching session key or rejects.
- The construction combines evolving chaining/authentication state, transcript state, and fresh
  KEM encapsulation.
- Sender state evolves on send; receiver state evolves on accepted receipt.

## Exposure semantics used by this project

The source material distinguishes traffic-key reveal from protocol-state exposure.

- Revealing a traffic key does not by itself expose all future ratchet state.
- Exposure of receiver/sender state has stronger tracing or impersonation consequences than
  traffic-key reveal alone.
- Broader recovery properties depend on the construction and exposure direction; this project
  does not collapse them into one generic “compromise” condition.

## Selection rationale

The unidirectional pattern is the smallest source construction matching the study's primary
ground-to-space fresh-entropy path. It makes one-sided state evolution observable without
importing the full bidirectional concurrent-epoch machinery.

## Modeling boundary

This repository does not implement the source algorithms or inherit their proofs. TT&C role
mapping, operational activation, strict deletion, telemetry evidence, and lockout/outcome
classification are experimental model decisions. Independent review of the source-to-model
mapping remains open.
