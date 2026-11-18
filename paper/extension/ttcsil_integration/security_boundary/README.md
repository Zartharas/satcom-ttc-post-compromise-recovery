# TTCSIL pre-dispatch safety guard — standalone C11 component

**Scope:** F1 defensive policy feasibility, **NOT** cFS/NOS3 integration, Recovery SA implementation, formal proof, verified cryptography, flight code, or a canonical TTCSIL study. No NASA code is copied or modified. This subdirectory contains only original policy functions, strict C11 tests, and a disposable local runner.

## Exact checks implemented

- `ttcsil_guard_length` refuses a declared total shorter than the trusted header, longer than the actual allocated input capacity or configured maximum, an impossible minimum, or zero header; it zeroes the output on failure. It subtracts lengths **only after** the lower bound has been proved. This tests a guard pattern related to CVE-2026-82480, **not** a patch to `CFE_SB_GetUserDataLength` or a demonstration that all cFE Software Bus consumers are safe.
- `ttcsil_guard_tc` refuses absent cryptographic verification, non-operational or non-authenticating SA, SPI zero, mismatched frame/selected/authorized SPI, mismatched complete (TFVN, SCID, VCID, MAP ID) tuples, and an unknown or unequal trusted epoch. This tests an explicit SA/channel policy pattern relevant to CVE-2026-79954, **not** proof that either upstream CryptoLib pin enforces it or is patched.
- **Fail closed:** every denial leaves returned payload length zero. Positive controls require matching evidence. No data plane dispatch or post-recovery resume signal is produced here.
- The MAP ID must be independently available in the installed frame format; the integration must fail closed when it cannot be verified. No wildcarding of a field was introduced for convenience.

## Mandatory trust sourcing for a future adapter

`ttcsil_policy` must originate from protected, independently configured authorization and active-epoch state. `ttcsil_evidence` must be assembled from separately verified CryptoLib / inbound frame / trusted coordinator provenance, **not** arbitrary flags from the TC message, mission-wide success enum, an IDS anomaly label, or an untrusted application. The `cryptographic_verification_succeeded` flag in these tests is a synthetic **unit-test input**; no implemented CryptoLib adapter currently supplies it. A caller able to forge these inputs bypasses this stand-alone policy; end-to-end trust requires independent validation.

A correct cFS adapter must, in order: (1) validate a physical input buffer's bound and minimum frame size, (2) parse the channel/SPI safely, (3) enforce an independently configured channel-authorized SA and avoid clear/downgrade acceptance, (4) require CryptoLib's real authenticated processing success and the actual selected SA state, (5) recheck the accepted frame and active epoch using this policy **before** dispatch, (6) separately bind outgoing authenticated TM to the same command and epoch before ever claiming safe resumption. These steps are an **unimplemented integration contract**, not an observed execution path.

## Run without upstream downloads

```bash
bash paper/extension/ttcsil_integration/security_boundary/run_guard_tests.sh
```

Requires C11 compiler and AddressSanitizer + UndefinedBehaviorSanitizer. Performs 32 assertions in two builds. Does **not** run NOS3, NASA CryptoLib, cFE, spacecraft apps, actual packet processing, COMMIT/CONFIRM restart scenarios, a scientific comparison, or a publisher-format claim.

## Remaining hard gates

**F1:** Full upstream source/license/patch review; independent SA-to-GVCID authorization and actual cFE ingress bounds. **F2:** Actual cFS/NOS3 process restarts with durable-write evidence. **F3:** Both endpoint SA/epoch and candidate/receipt instrumentation. **F4:** Authenticated TC and independently authenticated TM return with a separate trace oracle. **F5–F8:** Equal-information comparators, negative controls, frozen protocol, cross-publication non-overlap. All remain on HOLD/NOT EXECUTED as specified in `../INTEGRATED_RECOVERY_GATE_AND_EVIDENCE_CONTRACT_2026-11-17.md`.

No data from SatNOGS, ESA, CuCD-ID, AegisSat, UNSW-IoTSAT or the mission-aware/lifecycle author repositories are used. Scientific Studies A–D and the main TAES manuscript are unaffected.
