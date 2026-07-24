# Source Note: Triple-KEM SDLS Key Update

## Source

Andreas Hülsing, Tanja Lange, and Fiona Johanna Weber, *A Key-Update Mechanism
for the Space Data Link Security Protocol*, CANS 2025 proceedings.

## Points used by this project

- The proposal is a pure key exchange that outputs keys at the end rather than a messaging
  protocol.
- Final keys are derived only after the handshake is complete for the party in question.
- Key confirmation is always required.
- Triple-KEM uses three exchanged messages and can optionally update long-term KEM keys.
- By completion, the entire transcript is authenticated.
- The paper claims forward secrecy and post-compromise security in its model.
- Missing or out-of-order fragments cause the presented protocol to drop the connection unless
  a fragmentation layer provides ordering and re-requesting.

## Modeling boundary

The source does not define when an SDLS implementation should activate the newly output key,
how an endpoint should roll back after unilateral completion, or how mission control should
verify that the peer installed the key. Those are treated as explicit integration policies in
this repository.

## Phase 04 decision

The simulator records cryptographic completion separately from active SDLS epoch. Final
confirmation loss expires the default conservative attempt without operational divergence.
A unilateral local-activation policy is retained only as a negative control.
