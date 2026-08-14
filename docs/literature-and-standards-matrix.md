# Literature and Standards Matrix

**Metadata review date:** 2026-08-14

This matrix records the source families currently used to ground the paper. Publication metadata
must be checked again immediately before submission because standards and bibliographic records
can change.

| Source | Verified contribution used by this paper | Boundary / remaining question |
|---|---|---|
| CCSDS 355.0-B-2, *Space Data Link Security Protocol*, Issue 2, Aug. 2022 | Standardized data-link security framing for CCSDS telemetry/telecommand/AOS links | Does not by itself establish this paper's post-compromise resynchronization behavior |
| CCSDS 355.1-B-1, *Space Data Link Security Protocol—Extended Procedures*, Issue 1, Feb. 2020 | Auxiliary key-management, SA-management, and monitoring/control procedures | Does not supply the final experimental T1 behavior studied here |
| CCSDS 350.5-G-2, *Space Data Link Security Protocol—Summary of Concept and Rationale*, Jan. 2024 | Current SDLS concept/rationale context | Informational, not a proof or experiment result |
| CCSDS 350.11-G-1, *Space Data Link Security Protocol—Extended Procedures—Summary of Concept and Rationale*, Jul. 2024 | Current Extended Procedures concept/rationale context | Informational, not a recovery-security claim |
| Hülsing, Lange, and Weber, *A Key-Update Mechanism for the Space Data Link Security Protocol*, CANS 2025 proceedings, published 2026, DOI 10.1007/978-981-95-4434-9_29 | KEM-based SDLS key-update construction and confirmation semantics used to motivate B1 | Operational activation/status behavior added by this project is not attributed to the source |
| Poettering and Rösler, *Towards Bidirectional Ratcheted Key Exchange*, CRYPTO 2018, DOI 10.1007/978-3-319-96884-1_1; extended asynchronous RKE material, ePrint 2018/296 | Stateful sender/receiver evolution and exposure semantics used to motivate B2 | TT&C role mapping, activation, telemetry, and lockout classification are project abstractions |
| NIST FIPS 203, final Aug. 13, 2024 | Standardizes ML-KEM | Does not define TT&C recovery policy or state restoration |
| NIST SP 800-227, final Sep. 18, 2025 | Current NIST recommendations for KEM implementation/use | General KEM guidance, not a TT&C resynchronization procedure |
| Singh doctoral dissertation (2025; ProQuest publication 2026) | Practitioner/research motivation for hands-on follow-on work | The present article uses new synthetic experimental evidence rather than reusing interview outcomes |

## Working novelty hypothesis

The manuscript's novelty claim remains **provisional until a submission-stage systematic search
is completed**. The current defensible contribution is narrower than a universal “first” claim:

> The study implements a bounded TT&C recovery/resynchronization treatment and evaluates its
> operational behavior under predeclared matched scenarios, deterministic communication/state
> faults, a fixed mixed schedule population, sensitivity settings, and bounded formal/Python
> assurance checks.

Do not use “to our knowledge, no prior work...” language in the final manuscript until the
submission-stage literature search supports it.
