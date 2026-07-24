# Project Status

## Completed

- Phase One related-work and novelty framing
- Phase Two system and threat model
- Phase Three machine-readable abstract design
- repository foundation and automated Python test workflow
- B1 Triple-KEM source-semantic review
- B2 construction selection: Poettering-Roesler URKE-inspired strict baseline
- machine-readable Phase 04 baseline semantics
- deterministic B1 and B2 fault tests

## Current gate

Validate the Phase 04 branch locally and through pull-request CI, then obtain independent
cryptography review of the B1 activation boundary and B2 URKE adaptation.

T1 remains blocked until the baseline semantic review is accepted and the test oracles are
frozen.

## Phase 04 decisions

- B1 cryptographic completion is tracked separately from operational SDLS activation.
- B1 final-confirmation loss expires the conservative attempt without automatic epoch divergence.
- Unilateral B1 activation is retained only as a negative control.
- B2 maps ground to the strict URKE sender and spacecraft to the receiver.
- A dropped B2 update after sender evolution produces modeled lockout.
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
