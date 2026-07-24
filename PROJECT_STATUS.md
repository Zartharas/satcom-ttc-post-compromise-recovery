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
- Phase 04 local, CI, JSON, and tracked-file manifest validation
- Phase 05 independent-review handoff package and oracle-freeze candidate

## Current gate

Obtain an independent cryptography review using the Phase 05 response template, resolve every
`REJECT` or `ACCEPT WITH CORRECTION` item, and then freeze the approved scenario oracles.

T1 remains blocked until the reviewer approves the B1 and B2 source-to-model mappings and the
oracle candidate status changes from `PENDING_INDEPENDENT_REVIEW` to an accepted state with
complete evidence metadata.

## Corrected Phase 04 decisions

- B1 cryptographic completion remains separate from operational SDLS activation.
- The primary B1 baseline activates each endpoint on local completion.
- B1 final-confirmation loss therefore produces `G_AHEAD` and `DIVERGED`.
- Authenticated-status gating is an enhanced four-message comparison and status loss produces
  `S_AHEAD` and `DIVERGED`.
- No B1 policy uses simulator-wide bilateral-delivery knowledge as an activation oracle.
- B2 maps ground to the strict URKE sender and spacecraft to the receiver.
- B2 distinguishes traffic-key reveal, sender-state exposure, receiver-state exposure, and
  both-state exposure.
- Passive sender-state exposure may recover while active sender impersonation can lock the strict
  model on an attacker-known receiver branch.
- Receiver-state exposure makes later aligned keys `AVAILABLE_UNSAFE` in the strict URKE model.
- Lost status telemetry after endpoint convergence produces an indeterminate evidence outcome,
  not cryptographic divergence.

## Phase 05 artifacts

- `governance/phase-05-reviewer-response-template.md`
- `spec/baseline-oracle-freeze-candidate.json`
- `experiments/scripts/validate_review_handoff.py`
- `tests/test_review_handoff.py`

The freeze candidate contains 21 scenario oracles and remains explicitly pending. It cannot become
accepted without reviewer identity, source-located decisions, an approved commit SHA, a CI run ID,
and manifest-verification evidence.

## Deferred

- completed independent cryptography review
- named space-systems review
- formal model checking
- T1 implementation
- real cryptography
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
