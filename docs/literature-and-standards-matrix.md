# Literature and Standards Matrix

**Submission-stage review date:** 2026-08-14

This matrix records the primary/authoritative source families used to position the paper.
Publication metadata must still be checked immediately before submission because standards and
bibliographic records can change.

| Source | Contribution relevant to this paper | Boundary relative to this study |
|---|---|---|
| CCSDS 355.0-B-2, *Space Data Link Security Protocol*, Issue 2, Aug. 2022 | Standardized data-link security framing for CCSDS telemetry/telecommand/AOS links | Does not by itself define this paper's post-compromise resynchronization treatment |
| CCSDS 355.1-B-1, *Space Data Link Security Protocol—Extended Procedures*, Issue 1, Feb. 2020 | Auxiliary key management, SA management, and monitoring/control procedures | Does not provide the experimental T1 recovery-control behavior |
| CCSDS 350.5-G-2, Jan. 2024; CCSDS 350.11-G-1, Jul. 2024 | Current SDLS/Extended Procedures concept and rationale | Informational standards context, not experimental recovery evidence |
| Bader, *On Requirements & Concepts for TT&C Link Key Management*, SpaceSec 2024, DOI 10.14722/spacesec.2024.23053 | Defines TT&C key-management requirements including post-compromise security and all-frame operational constraints; evaluates SDLS/SDLS EP and discusses stateful key evolution | Requirements/concept analysis; does not experimentally evaluate post-compromise ground-space resynchronization |
| Hülsing, Lange, and Weber, *A Key-Update Mechanism for the Space Data Link Security Protocol*, CANS 2025 proceedings, published 2026, DOI 10.1007/978-981-95-4434-9_29 | KEM/PQNoise-based fresh SDLS key-update construction with cryptographic analysis and confirmation | Does not specify the project-added operational activation/status/resynchronization state machine |
| Dowling, Hale, Tian, and Wimalasiri, *Key Establishment in the Space Environment*, 2025, arXiv:2503.06785 | Analyzes space key-establishment tradeoffs and continuous/stateful key agreement for intermittent/high-latency architectures | Architecture/key-establishment focus; not a fault-injected TT&C recovery-control experiment |
| Poettering and Rösler, *Towards Bidirectional Ratcheted Key Exchange*, CRYPTO 2018, DOI 10.1007/978-3-319-96884-1_1; related asynchronous RKE material, ePrint 2018/296 | Stateful sender/receiver evolution and exposure semantics used to motivate B2 | TT&C role mapping, strict deletion, telemetry evidence, activation, and lockout classifications are project abstractions |
| NIST FIPS 203, final Aug. 13, 2024 | Standardizes ML-KEM | Does not define TT&C recovery policy or operational resynchronization |
| NIST SP 800-227, final Sep. 18, 2025 | Current NIST recommendations for KEM implementation/use | General KEM guidance, not a TT&C recovery procedure |
| Idan et al., *AegisSat: A Satellite Cybersecurity Testbed*, SpaceSec 2025, DOI 10.14722/spacesec.2025.23069 | Earth-based CubeSat cybersecurity testbed, environment emulation, attack experiments, telemetry/dataset | Higher physical/environmental fidelity; not focused on post-compromise key-state resynchronization |
| Castanon Remy et al., *Space Cybersecurity Testbed: Fidelity Framework, Example Implementation, and Characterization*, SpaceSec 2025, DOI 10.14722/spacesec.2025.23042 | Seven-attribute fidelity framework and concrete multi-segment cybersecurity testbed | Testbed/fidelity contribution rather than TT&C recovery-control mechanism |
| Singh doctoral dissertation (2025; ProQuest publication 2026) | Earlier empirical/practitioner motivation for hands-on follow-on research | Present article uses new synthetic experimental evidence rather than reusing interview outcomes |

## Submission-stage positioning

The literature reviewed for the current manuscript demonstrates active work in four adjacent
areas: TT&C security standards and key-management requirements; post-compromise/fresh
key-establishment mechanisms for space communication; stateful/continuous key agreement suited
to disrupted or long-lived communication; and experimental satellite cybersecurity testbeds.

The current manuscript should therefore **not** claim to be the first work on satellite
post-compromise key management, space key establishment, ratcheted/stateful key agreement, or
satellite cybersecurity testbeds.

The narrower defensible positioning is:

> This study experimentally isolates the operational resynchronization layer between fresh
> key-establishment/key-evolution concepts and trusted TT&C recovery. It evaluates activation
> asymmetry, verification evidence, bounded retries, stale/replayed state, endpoint restart, and
> matched terminal-state behavior under a predeclared deterministic synthetic experiment.

This is a contribution statement, not a universal priority claim. Avoid “first” or “to our
knowledge, no prior work” language unless an even broader venue-specific search immediately
before submission supports it.

## Remaining pre-submission verification

Immediately before submission:

- recheck all standard editions and publication metadata;
- confirm whether `Key Establishment in the Space Environment` has acquired final proceedings
  metadata superseding the arXiv record;
- run one venue-specific database search using the final title/keywords;
- recheck any claim that uses “novel,” “first,” “only,” or “state of the art”; and
- ensure citations distinguish cryptographic construction claims from project operational
  abstractions.
