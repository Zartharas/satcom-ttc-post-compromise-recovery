# Phase 11 — Formal/Python Trace Cross-Validation and Bound Expansion

## Purpose

Phase 11 compares an actual bounded TLC success witness with the Python T1 controller under an explicitly
declared abstract projection. It also runs a small finite bound panel to confirm the Phase 10 baseline and
observe how the recorded state space changes when one model constant is adjusted at a time.

The phase does not claim refinement proof, implementation equivalence, cryptographic security, or parameter
selection.

## Success witness

`ReachabilityWitnessNoSuccess == outcome # "SUCCESS"` is intentionally false. TLC checks it only under
`formal/tla/SuccessWitness.cfg` so that the shortest behavior reaching `SUCCESS` is emitted as a trace.

The first successful CI run recorded eight witness states:

1. `Init`
2. `Prepare`
3. `SelectCandidate`
4. `Commit`
5. `Confirm`
6. `AcceptCommand`
7. `ReceiveStatus`
8. `Verify`

The witness run generated 28 states, found 21 distinct states, and reached search depth 8 before producing the
expected testing-only violation.

This expected violation is a reachability mechanism. It is not a discovered protocol defect or a failed
security property.

## Declared Python mapping

The comparison uses 16 abstract fields at every step:

- ground and spacecraft mode;
- current and previous epochs;
- candidate epoch;
- pending and activation-receipt flags;
- attempt and activation counts;
- command, status, and drop evidence;
- verification state; and
- outcome.

Three transitions require an explicit mapping rather than a one-method-to-one-action correspondence:

- `SelectCandidate` maps to spacecraft prepare acceptance followed by ground response acceptance;
- `AcceptCommand` is projected as the command-evidence substep before `verify_recovery`; and
- `ReceiveStatus` is projected as the telemetry-evidence substep before `verify_recovery`.

The first run compared 136 rows and recorded 136 matches with zero mismatches. The result is labeled only
`MATCH_WITHIN_DECLARED_ABSTRACTION`.

A future mismatch must be labeled `MISMATCH_REQUIRES_REVIEW`. The formal or Python trace must not be silently
changed to force agreement.

## Bound panel

The panel changes one finite constant at a time while retaining the same initial epochs and positive property
set.

| Case | Max attempts | Max epoch | Generated | Distinct | Depth | Status |
|---|---:|---:|---:|---:|---:|---|
| attempts-1 | 1 | 6 | 18 | 12 | 8 | `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` |
| base-3-6 | 3 | 6 | 50 | 28 | 10 | `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` |
| attempts-5 | 5 | 6 | 82 | 44 | 12 | `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` |
| epoch-4 | 3 | 4 | 50 | 28 | 10 | `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` |
| epoch-8 | 3 | 8 | 50 | 28 | 10 | `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` |

The base case exactly reproduces the Phase 10 counts.

The attempt-bound cases show a larger recorded state space and depth as additional retry states become
reachable. The epoch-ceiling cases do not change the recorded counts in this finite configuration because the
initial epochs lead to candidate epoch 3 and the model does not perform repeated recoveries. This is a local
observation, not a general parameter conclusion.

No bound in this panel is selected, recommended, or frozen.

## Outputs

A successful run writes:

- `phase11-cross-validation.json`;
- `phase11-success-witness.json`;
- `phase11-trace-comparison.csv`;
- `phase11-bound-expansion.csv`;
- Java and SANY logs;
- the success-witness TLC log;
- one TLC log for each of the five bound cases; and
- `phase11-derived-bundle.sha256`.

TLC metadata directories are scratch data and are not included in the derived manifest.

## Interpretation boundary

Phase 11 does not establish:

- equivalence between the TLA+ model and Python implementation;
- correctness or completeness of the macro-step mapping;
- correctness of a concrete cryptographic construction;
- post-compromise security;
- CCSDS or SDLS conformance;
- flight-software, network, RF, or spacecraft behavior;
- unbounded safety or liveness; or
- publication-ready formal evidence.

Independent review remains mandatory before the projection, property set, constants, treatment, or security
interpretation is frozen or used in a manuscript or external claim.
