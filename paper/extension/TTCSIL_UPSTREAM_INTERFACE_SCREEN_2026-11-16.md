# TTCSIL-SA-RST-001 — source-level SA and command-path feasibility screen

**Date:** 2026-11-16  
**Status:** READ_ONLY_SOURCE_SCREEN; NO build, test, dependency download, activation, or result has occurred.  
**Scope:** prospective F1–F4 feasibility evidence only. Not a qualified, interoperable, or secure implementation.

## Upstream source identity (release tag reference, not an approved integrated lock)

| Repository | Release | Tag ref resolved to commit (checked 2026-11-16) | License/source condition |
|---|---|---|---|
| [nasa/CryptoLib](https://github.com/nasa/CryptoLib) | `v1.5.2` | `c216ede78b2f51b42838b13955602c0b481b53c2` | Repo LICENSE is NASA Open Source Agreement 1.3; individual source headers include JPL rights/export notices. Review actual obligations before copying/modifying/distributing. |
| [nasa/nos3](https://github.com/nasa/nos3) | `v1_07_06` | `1dadc685effc26730603c36c7864afce3c546406` | NASA Open Source Agreement 1.3, plus third-party dependencies; no approval to redistribute bundled sources. |
| [nasa/cFS](https://github.com/nasa/cFS) | `v7.0.1` | `088b2fa828db9ff7e00733f1908e0eeb59f66ce3` | Apache 2.0 for bundle, with separate submodule licenses to inspect. NASA describes the demo as **not a verified flight distribution**. |

These SHA values are upstream tag observations, **not** confirmation that the three versions are compatible or a valid frozen full-stack version graph. In particular, NOS3 pins its own gitlinks; standalone cFS `v7.0.1` must not be mixed with a NOS3 runtime without an explicit compatibility test.

## Concrete read-only interface evidence

- [CryptoLib v1.5.2 `include/sa_interface.h`](https://github.com/nasa/CryptoLib/blob/v1.5.2/include/sa_interface.h) defines SA lifecycle and interaction callbacks including `sa_init`, `sa_get_from_spi`, `sa_get_operational_sa_from_gvcid`, `sa_save_sa`, `sa_start`, `sa_stop`, `sa_rekey` and `sa_status`.
- [CryptoLib internal SA backend](https://github.com/nasa/CryptoLib/blob/v1.5.2/src/sa/internal/sa_interface_inmemory.template.c) includes `sa_load_file`, optional `SA_FILE` save behavior, `fread`/`fwrite`, and `fclose`. In this inspected source no explicit `fflush` or `fsync` call was found. This absence **does not prove** unsafe crash behavior throughout the complete stack; it means neither atomicity nor durable ordering may be assumed without controlled process/storage tests.
- [CryptoLib MariaDB backend](https://github.com/nasa/CryptoLib/blob/v1.5.2/src/sa/mariadb/sa_interface_mariadb.template.c) provides an alternative SA storage interface, but its transaction/crash behavior was not evaluated.
- [CryptoLib usage documentation](https://github.com/nasa/CryptoLib/blob/v1.5.2/docs/wiki/Usage.md) documents `Crypto_TC_ApplySecurity` and `Crypto_TC_ProcessSecurity` for TC frame protection/processing; it describes Extended Procedures as **work in progress and not mature enough for operational use**. It does not document a project-defined PREPARE/RESPONSE/COMMIT/CONFIRM transaction as a supported feature.
- [NOS3 command-encryption scenario](https://github.com/nasa/nos3/blob/v1_07_06/docs/wiki/Scenario_Encryption.md) walks through authenticated commands and telemetry using CryptoLib, but states it was last updated in 2025 against a specific earlier branch. This is an integration **lead**, not validated behavior of the candidate releases.

## Implications for the independent TT&C study

1. An instrumented, resettable *SA state and packet acceptance* test appears technically plausible, but **no F1–F4 gate is passed** until native build, pinning, storage durability and packet semantics are demonstrated.
2. The project-defined T1 control protocol would need a **separate, openly identified orchestration layer**. Do not attribute that layer or a crash-safe recovery algorithm to upstream CryptoLib, NASA, CCSDS or NOS3.
3. A file-backed SA update must be tested at exact before/after-write/activation/restart boundaries, including corrupted or missing state and behavior after reinitialization. A successful `sa_save_sa` return alone is not evidence of persistence across process crash or power failure.
4. Distinguish a controlled **process restart** from real loss of power, radiation or nonvolatile media failure. Persistence durability, trust-anchor independence and replay-counter continuity require an explicit storage and attack model.
5. A negative test must verify that stale/replayed or retired-SA frames are **rejected by the actual library integration**, not just by a test-controller classification. A separate verifier reconstructs ground/space state and observed TC/TM evidence.
6. The relevant standards are prior art, not certifications: [CCSDS 350.5-G-2](https://ccsds.org/Pubs/350x5g2.pdf) §§3.5.1.2/4.5.6 (Recovery SA); [ECSS-E-ST-70-11C Rev.1](https://ecss.nl/standard/ecss-e-st-70-11c-rev-1-space-segment-operability-15-october-2025/) §§4.2/4.3 (contingency observability/commandability). The test may characterize implementation behavior but cannot claim CCSDS/ECSS conformance without an independently defined conformity program.

## Current disposition

**F1 = NOT PASSED** (tag refs identified; compatibility, dependency graph, licenses and security issues not qualified).  
**F2/F3/F4 = NOT EXECUTED** (no process restart, instrumented SA state or authenticated command exchange tested).  
**H2 persistence/reinitiation = PROPOSAL ONLY** (not implemented, evaluated or proven).

Continue manuscript source/visual improvement against frozen Studies A–D independently from this prospective line. No experiment, test-case denominator, claim, or publisher submission changes follow from this source-screen.
