# Locked Research Decisions

## Article identity

This is an original experimental cybersecurity journal article using satellite TT&C as
the application environment. It is not another dissertation, a re-analysis of the 15
interviews, or a broad SATCOM review.

## Primary novelty target

A bounded, replay-resistant resynchronization controller for SDLS-protected TT&C
recovery after compromise-induced key-state divergence, evaluated jointly for attacker
exclusion, permanent-lockout risk, command restoration, missed contacts, message faults,
stale-state restoration, and evidence completeness.

## Baseline correction

B1 must not be called a purely stateless AKE baseline. Triple-KEM is a standalone
three-message key exchange that can optionally update long-term KEM keys. It requires
transcript completion and key confirmation; missing or reordered required material causes
abort/drop behavior in the published design.

## Minimalism rule

The first simulator is deterministic and standard-library-only. It models state,
attacker knowledge, contact windows, and faults. It does not implement ML-KEM,
signatures, AEAD, SDLS frames, NOS3, or cFS.

## Separation from other research tracks

No earlier one-message stateless recovery design is imported into T1. This paper remains
a separate stateful resynchronization track.

## Review boundary

This is a source-grounded technical desk review, not a substitute for named independent
cryptography and space-systems reviewers.
