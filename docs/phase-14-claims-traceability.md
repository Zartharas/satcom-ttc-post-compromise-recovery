# Phase 14 Claims Traceability

## Status

`READY_FOR_OUTREACH_NOT_REVIEWED`

This document is a human-readable companion to `spec/phase-14-independent-review-package.json` and
`governance/phase-14-claims-traceability.csv`. The JSON contract is authoritative when wording differs.

## Status vocabulary

| Status | Meaning |
|---|---|
| `PENDING_INDEPENDENT_REVIEW` | The wording is a review candidate and must not be presented as accepted. |
| `PERMITTED_WITH_QUALIFIER` | The wording may be used only with the listed qualifier and supporting evidence. |
| `DIAGNOSTIC_ONLY` | The wording describes internal diagnostic output and cannot support equivalence, security, or completeness claims. |
| `NOT_PERMITTED` | The claim is prohibited under the current evidence and review status. |
| `GOVERNANCE_EXCEPTION_REQUIRES_REVIEW` | The statement records a process inconsistency that must be resolved explicitly. |

## Claims matrix

| ID | Category | Status | Candidate or permitted wording |
|---|---|---|---|
| `CLM-01` | baseline_semantics | `PENDING_INDEPENDENT_REVIEW` | The repository deterministically implements the documented B0, B1, and B2 abstract outcome rules. |
| `CLM-02` | b1_mapping | `PENDING_INDEPENDENT_REVIEW` | ACTIVATE_ON_LOCAL_COMPLETION is a project-supplied minimum-assumption operational integration for the three-message B1 exchange. |
| `CLM-03` | b1_mapping | `PENDING_INDEPENDENT_REVIEW` | Under ACTIVATE_ON_LOCAL_COMPLETION, loss of KEM_CONFIRM produces ground-ahead divergence in the abstract simulator. |
| `CLM-04` | b1_mapping | `PENDING_INDEPENDENT_REVIEW` | DEFER_UNTIL_AUTHENTICATED_STATUS is an explicit project-added four-message comparison variant. |
| `CLM-05` | b2_mapping | `PENDING_INDEPENDENT_REVIEW` | The B2 baseline adapts a unidirectional ratcheted-key-exchange pattern with ground as sender and spacecraft as receiver. |
| `CLM-06` | b2_compromise_scope | `PENDING_INDEPENDENT_REVIEW` | The B2 abstraction separates traffic-key disclosure from sender-state, receiver-state, and both-endpoint-state exposure. |
| `CLM-07` | b2_outcome | `PENDING_INDEPENDENT_REVIEW` | Receiver-state exposure is classified as AVAILABLE_UNSAFE after aligned update in the current B2 abstraction. |
| `CLM-08` | b2_outcome | `PENDING_INDEPENDENT_REVIEW` | Active sender-state impersonation, dropped update after sender evolution, and stale restore are classified as LOCKED in the strict B2 model. |
| `CLM-09` | formal_execution | `PERMITTED_WITH_QUALIFIER` | The Phase 10 TLA+ model parsed successfully and TLC found no counterexample within the recorded finite configuration. |
| `CLM-10` | trace_cross_validation | `DIAGNOSTIC_ONLY` | Recorded formal and Python traces matched within the declared 16-field abstraction for the tested witness paths. |
| `CLM-11` | outcome_expansion | `DIAGNOSTIC_ONLY` | The opt-in Phase 13 module contains one explicit bounded witness path each for DIVERGED, AVAILABLE_UNSAFE, and LOCKED while preserving the Phase 10–12 baseline module. |
| `CLM-12` | causal_interpretation | `NOT_PERMITTED` | No causal claim is permitted for the Phase 13 gapCause labels. |
| `CLM-13` | model_completeness | `NOT_PERMITTED` | No claim of formal-model or outcome-population completeness is permitted. |
| `CLM-14` | implementation_equivalence | `NOT_PERMITTED` | No refinement or implementation-equivalence claim is permitted. |
| `CLM-15` | cryptographic_security | `NOT_PERMITTED` | No cryptographic security, PCS, confidentiality, authenticity, or key-indistinguishability claim is permitted from the simulator or formal traces. |
| `CLM-16` | operational_applicability | `NOT_PERMITTED` | No CCSDS/SDLS conformance, flight-software correctness, RF behavior, or operational-spacecraft claim is permitted. |
| `CLM-17` | publication_evidence | `NOT_PERMITTED` | Current simulation and formal outputs are internal diagnostic evidence only. |
| `CLM-18` | oracle_freeze | `NOT_PERMITTED` | The 21 baseline scenario oracles remain a freeze candidate pending independent review. |
| `CLM-19` | governance | `GOVERNANCE_EXCEPTION_REQUIRES_REVIEW` | Phases 6–13 proceeded as provisional internal work even though the Phase 04 gate states that T1 work is blocked pending review. |
| `CLM-20` | governance | `PENDING_INDEPENDENT_REVIEW` | The phrase corrected and locked for abstract implementation refers to an internal implementation decision, not independent approval or oracle freeze. |

## Cross-cutting restrictions

The following remain `NOT_PERMITTED` regardless of a clean test or model-check run:

- claiming that the baseline or T1 has been cryptographically proved secure;
- inheriting PCS or other source-paper guarantees;
- calling finite TLC output a proof or formal verification of a concrete protocol;
- claiming refinement or implementation equivalence from selected trace matches;
- treating `gapCause` as a validated causal explanation;
- treating the modeled outcome population as complete, realistic, necessary, sufficient, or exhaustive;
- claiming CCSDS/SDLS conformance, flight-software correctness, RF behavior, or operational-spacecraft applicability; and
- using the current outputs as publication-ready security evidence.

## Review effect

Independent review may accept, narrow, correct, or reject candidate wording. It cannot by itself convert an
abstract simulator or finite state model into cryptographic, conformance, flight-software, RF, or operational
evidence. Any accepted correction must be implemented and revalidated before the claims matrix changes.

Baseline oracle freeze is separate from semantic review. Formal-diagnostic acceptance is separate from both.
Any scope not covered by the primary reviewer requires a second qualified reviewer.

## Governance exceptions

Phase 14 explicitly preserves four open governance findings:

1. the missing B1-R5 question in the Phase 05 response template;
2. provisional T1 work performed after the Phase 04 gate stated that T1 work was blocked;
3. ambiguity between internal implementation lock and independent approval; and
4. differing review-target commits in earlier handoff records.

None of these findings is resolved merely by creating this package.
