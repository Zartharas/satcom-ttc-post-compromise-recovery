# Research Charter

## Article type

Original hands-on experimental cybersecurity journal article using satellite TT&C as the
application environment. This is not another dissertation, a re-analysis of the prior
interviews, or a broad SATCOM review.

## Current manuscript title

**Post-Compromise Satellite TT&C Resynchronization Under Intermittent Links: A Controlled Fault-Injection Study**

The title may receive venue-specific editorial adjustment before submission. The repository does not claim
concrete SDLS conformance.

## Problem

Key update and state evolution can exclude previously compromised operational material, but
interrupted ground-space transitions can leave legitimate operators synchronized, asymmetric,
degraded, or unable to complete trusted recovery evidence.

## Primary objective

Experimentally characterize recovery behavior under bounded compromise, intermittent contact,
message faults, stale/replayed state, and endpoint disruption, while separating matched
cross-treatment evidence from T1-specific robustness evidence.

## Research questions

1. Under defensibly matched conditions, how do B0, B1, B2, and T1 compare in terminal security,
   availability, alignment, and verification classifications?
2. How does T1 behave under controlled loss, delay, duplication, reordering, contact closure,
   endpoint restart, stale counters, and replay?
3. How does T1 behavior change across bounded retry budgets and candidate-retention lifetimes?
4. Where do bounded TLA+ witnesses and Python executions agree or differ under the declared
   projection?

The design does not require a universal treatment ranking. Cross-treatment claims remain limited
to the four qualified matched families and their pre-authorized fields.

## Current empirical status

The final predeclared synthetic experiment was retained as
`20260814T022506Z-gc630fb4` at execution commit
`c630fb4f65ad78211fd3ffb0391000d7ed3629b1`. See `paper/RESULTS_SUMMARY.md`.

## Working venue candidate

IEEE Transactions on Aerospace and Electronic Systems remains a working venue candidate. Venue
scope, article type, formatting, and current author instructions must be rechecked immediately
before submission.

## Boundaries

No live RF, operational satellites, proprietary mission data, classified information, new
cryptographic primitive, flight-readiness claim, human-subject experiment, cryptographic proof,
or real-world fault-prevalence inference is included in the current study.
