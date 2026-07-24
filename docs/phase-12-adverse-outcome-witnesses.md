# Phase 12 — Adverse-outcome formal witnesses

## Purpose

Phase 12 extends the Phase 11 formal/Python comparison method to adverse outcomes. It captures bounded
TLC witnesses for `INDETERMINATE`, `SECURE_DEGRADED`, and `EXPIRED`, replays each action path through the
Python T1 controller, and compares the same 16-field abstract projection.

It also runs separate reachability checks for `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`. Those checks
are diagnostic only. No bounded absence is interpreted as impossibility.

## Captured adverse witnesses

The first successful CI execution recorded:

| Outcome | Formal actions | Trace states | Comparison rows | Mismatches |
|---|---|---:|---:|---:|
| `INDETERMINATE` | `Init → Prepare → SelectCandidate → Commit → Confirm → AcceptCommand → DropStatus` | 7 | 119 | 0 |
| `SECURE_DEGRADED` | `Init → Prepare → SelectCandidate → Commit → Retry → Retry → ExpireAfterSpacecraftActivation` | 7 | 119 | 0 |
| `EXPIRED` | `Init → Prepare → Retry → Retry → ExpireBeforeActivation` | 5 | 85 | 0 |

Each witness was produced by a testing-only false reachability invariant. The counterexamples are expected
witnesses, not discovered safety-property violations.

The comparison status is:

```text
MATCH_WITHIN_DECLARED_ABSTRACTION
```

That status means only that the recorded formal witness and the Python replay agree over the declared
projection. It is not a refinement proof, implementation-equivalence result, or cryptographic-security
claim.

## Receipt-evidence mapping

The formal `receipt` variable represents retained evidence that the spacecraft activated the candidate.
During terminal cleanup after confirmation-budget exhaustion, the Python controller clears its live
`activation_receipt` object. Phase 12 therefore projects the formal field to an explicitly tracked
receipt-evidence value.

This mapping is disclosed because the storage semantics are not identical. The comparison does not hide or
rewrite that difference.

## Currently unreached outcomes

The finite checks for `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED` each completed with:

```text
NOT_REACHED_WITHIN_RECORDED_BOUND
```

Each run explored 50 generated states, 28 distinct states, zero queued states, and depth 10 under the current
constants.

A source-level transition-assignment audit found zero assignments to each of those outcome values. Their
current diagnosis is therefore:

```text
ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS
```

This means the present TLA+ abstraction cannot generate those outcomes. It does not mean the outcomes are
impossible in the Python controller, a future model, a concrete protocol, flight software, or an operational
system.

## Evidence files

A Phase 12 run produces:

- one overall JSON report;
- three witness JSON files;
- three field-level comparison CSV files;
- one unreached-outcome diagnostic CSV;
- Java and SANY logs;
- six TLC logs; and
- one SHA-256 manifest for all derived files.

Generated run evidence remains outside Git or in short-lived CI artifacts.

## Review boundary

Independent review remains mandatory before:

- claiming refinement proof or implementation equivalence;
- claiming that the formal model is complete;
- treating bounded absence as impossibility;
- adding or freezing transition semantics for the currently absent outcomes;
- mapping the abstraction to concrete cryptographic mechanisms;
- using these results as post-compromise-security evidence;
- claiming CCSDS/SDLS, flight-software, RF, or operational-spacecraft applicability; or
- using Phase 12 output as publication evidence.

Phase 12 remains `PROVISIONAL_INTERNAL_REVIEW_ONLY`.
