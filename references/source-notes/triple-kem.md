# Source Note: Triple-KEM SDLS Key Update

## Source

Andreas Hülsing, Tanja Lange, and Fiona Johanna Weber, *A Key-Update Mechanism for the Space
Data Link Security Protocol*, in *Cryptology and Network Security: 24th International
Conference, CANS 2025, Osaka, Japan, November 17–20, 2025, Proceedings*, Lecture Notes in
Computer Science 16351, Springer, 2026, pp. 602–611.
DOI: `10.1007/978-981-95-4434-9_29`.

## Points used by this project

- The proposal is a standalone key exchange that outputs a key for SDLS rather than a complete
  secure-channel protocol.
- Final keys are derived only after the handshake is complete for the party in question.
- Key confirmation is mandatory.
- Triple-KEM uses three exchanged messages and can optionally update long-term KEM keys.
- Missing or out-of-order fragments cause the presented protocol to drop the connection unless
  another layer provides ordering and re-requesting.
- The source presents security claims in its stated cryptographic model.

## What the source does not specify for this experiment

The source does not define:

- when an SDLS security association becomes operational in this simulator;
- how the initiator learns that the responder received final confirmation;
- rollback after unilateral operational activation; or
- this project's post-handshake operational-key installation/status semantics.

## B1 project mapping

`ACTIVATE_ON_LOCAL_COMPLETION` is the primary minimal-assumption operational mapping. Ground
activates after its local completion; spacecraft activates after receiving/validating final
confirmation. Loss of that confirmation therefore produces one-sided activation.

`DEFER_UNTIL_AUTHENTICATED_STATUS` is an enhanced four-message integration variant supplied by
this project. It adds spacecraft status after Triple-KEM completion and separately tests status
loss. It is not attributed to the source paper.

## Modeling boundary

The simulator does not implement the source cryptographic construction and does not inherit its
proof. No independent cryptography review of this source-to-model mapping was completed for the
current paper. The manuscript reports that limitation explicitly; any future independent review
should evaluate the mapping against the primary source.
