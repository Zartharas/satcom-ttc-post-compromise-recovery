# Source Note: Triple-KEM SDLS Key Update

## Source

Andreas Hülsing, Tanja Lange, and Fiona Johanna Weber, *A Key-Update Mechanism
for the Space Data Link Security Protocol*, CANS 2025 proceedings.

## Points used by this project

- The proposal is a standalone key exchange that outputs a key for SDLS rather than a complete
  secure-channel protocol.
- Final keys are derived only after the handshake is complete for the party in question.
- Key confirmation is mandatory.
- Triple-KEM uses three exchanged messages and can optionally update long-term KEM keys.
- Missing or out-of-order fragments cause the presented protocol to drop the connection unless
  another layer provides ordering and re-requesting.
- The proposal claims forward secrecy and post-compromise security in its stated model.

## What the source does not specify

The source does not define:

- when an SDLS security association becomes operational;
- how the initiator learns that the responder received the final confirmation;
- rollback after unilateral completion; or
- a post-handshake operational-key installation acknowledgment.

## Corrected Phase 04 mapping

`ACTIVATE_ON_LOCAL_COMPLETION` is the primary minimal-assumption baseline. Ground activates
after its local completion; spacecraft activates after receiving and validating the final
confirmation. Loss of that confirmation therefore produces one-sided activation.

`DEFER_UNTIL_AUTHENTICATED_STATUS` is an enhanced four-message integration variant supplied
by this project. It adds spacecraft status after Triple-KEM completion and must separately test
status loss. It is not attributed to the paper.
