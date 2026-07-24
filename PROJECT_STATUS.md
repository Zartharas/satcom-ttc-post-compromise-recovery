# Project Status

## Completed

- Phase One related-work and novelty framing
- Phase Two system and threat model
- Phase Three machine-readable abstract design
- repository foundation and automated Python test workflow
- B1 Triple-KEM source-semantic review
- B2 construction selection: Poettering-Roesler URKE-inspired strict baseline
- machine-readable Phase 04 baseline semantics
- adversarial review of B1 activation and B2 compromise scope
- corrected deterministic B1 and B2 fault tests

## Current gate

Validate the corrected Phase 04 branch locally and through pull-request CI, then obtain independent
cryptography review of the B1 activation boundary and B2 URKE exposure mapping.

T1 remains blocked until the corrected baseline semantic review is accepted and the test oracles
are frozen.

## Corrected Phase 04 decisions

- B1 cryptographic completion remains separate from operational SDLS activation.
- The primary B1 baseline activates each endpoint on local completion.
- B1 final-confirmation loss therefore produces `G_AHEAD` and `DIVERGED`.
- Authenticated-status gating is an enhanced four-message comparison and status loss produces
  `S_AHEAD` and `DIVERGED`.
- No B1 policy uses simulator-wide bilateral-delivery knowledge as an activation oracle.
- B2 maps ground to the strict URKE sender and spacecraft to the receiver.
- B2 distinguishes traffic-key reveal, sender-state exposure, receiver-state exposure, and both-state
  exposure.
- Passive sender-state exposure may recover while active sender impersonation can lock the strict
  model on an attacker-known receiver branch.
- Receiver-state exposure makes later aligned keys `AVAILABLE_UNSAFE` in the strict URKE model.
- Lost status telemetry after endpoint convergence produces an indeterminate evidence outcome,
  not cryptographic divergence.

## Deferred

- named independent cryptography review
- named space-systems review
- formal model checking
- T1 implementation
- real cryptography
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
