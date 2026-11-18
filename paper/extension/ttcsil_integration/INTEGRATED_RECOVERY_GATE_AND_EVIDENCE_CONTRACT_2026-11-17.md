# TTCSIL integrated NOS3/cFS readiness and safety decision

**Date:** 2026-11-17  
**Study:** `TTCSIL-SA-RST-001` (prospective, *unfrozen*)  
**Mode:** Design and upstream source review only. No integrated runtime, scenario execution, scientific data, new conclusions or publisher amendment.  
**Pinned evidence:** `NOS3_SOURCE_LOCK_AND_SECURITY_HOLD_2026-11-17.json`

## Decision: STOP before a nominal NOS3/cFS Recovery SA runtime

Do **not** treat the previously passing native standalone CryptoLib PR #17 as a validated NOS3 integration. NOS3 v1_07_06 embeds **another** CryptoLib revision and a separately versioned cFE. A nominal cFS/COSMOS NOOP already exists as an unmerged P2X workstream in the author's **mission-aware** repository (PR #214 and #215). Repeating that operation would not independently test this project's target, and no experiments from those PRs may be imported as evidence.

### Security sources requiring adjudication

- **CVE-2026-79954** (CNA description names CryptoLib 1.5.0): receiver SA selection uses a frame-supplied SPI and a missing SA-to-GVCID binding can allow an authentication downgrade. Public advisory https://nvd.nist.gov/vuln/detail/CVE-2026-79954 ; published research https://starsec.io/en/blog/cve-2026-79954-cryptolib-sdls-downgrade (September 25, 2026). The latter reports a real cFS satellite integration; it also means that *basic protected-command acceptance in CryptoLib/cFS is already reported elsewhere*, and cannot be claimed as a novel aerospace result here.
- I inspected **both** [standalone CryptoLib v1.5.2](https://github.com/nasa/CryptoLib/blob/c216ede78b2f51b42838b13955602c0b481b53c2/src/core/crypto_tc.c) and [NOS3-embedded CryptoLib](https://github.com/nasa/CryptoLib/blob/b46879c094f1ae279c2ff04dea3d8e5ecbd4ef92/src/core/crypto_tc.c). In each, the *checked* `crypto_tc_validate_sa` function validates SA structural state but contains no direct `gvcid_blk` check. The receive parser checks the frame GVCID for managed-parameter selection, which is **not equivalent on its own to SA authorization**. This is a **source-level concern**, not a demonstrated exploit or proof of the precise versions' affected state. Full end-to-end source review and/or maintainer confirmation are required.
- **CVE-2026-82480** (CNA lists cFS 7.0.0 and 7.0.1): cFE Software Bus message-length underflow. https://nvd.nist.gov/vuln/detail/CVE-2026-82480. **Direct source evidence at NOS3-embedded cFE SHA `87e273743f3d07ed9216462b461e9f398ff96c87`:** [`modules/sb/fsw/src/cfe_sb_util.c`](https://github.com/nasa-itc/cFE/blob/87e273743f3d07ed9216462b461e9f398ff96c87/modules/sb/fsw/src/cfe_sb_util.c) computes `TotalMsgSize - HdrSize` inside `CFE_SB_GetUserDataLength` **without a local lower-bound check**. This matches the described underflow pattern. Whether any actual NOS3 message path can present malformed sizes, or other layers prevent it, is **UNVERIFIED**. Do not claim confirmed exploitation or patched status.
- Keep every potential integration **offline and on isolated simulation networks** even after clearance. Never use public command ports, operational keys, real RF, live mission ground equipment, or spacecraft; no security certification.

### Required controls before any F2–F4 runtime

1. **F1 safety gate:** determine the exact receiving component and SDLS integration path. Require validated enforcement of *active authorized SA + expected GVCID* **before** any command reaches cFE Software Bus, or documented strictly isolated authenticated-only SA provisioning with an independent channel-binding check. Identify all clear-mode SAs and prevent unintended acceptance by policy. Do not merely assert this via protocol configuration.
2. **F1 software graph:** verify all 48 NOS3 gitlinks and any out-of-graph Docker images, apt packages, toolchains and external downloads; capture exact digests. NOS3 pins CryptoLib `b46879c...`, not standalone `c216ede...`. Do not silently replace either or claim interoperability.
3. **F1 vulnerable cFE exposure:** validate that the test's input framing bounds prevent malformed length delivery to the cFE Software Bus and that any remaining CVE exposure is explicitly accepted for isolated research only. Software bench tests do not imply operational software is safe.
4. **F2 actual restart:** process supervisor or cFE restart of a named *onboard recovery coordination component*, with OS-level PID/start-time evidence and known volatile/durable journals; do not count a simulator dictionary reset. Observe the exact last durable write and process event.
5. **F3 dual-endpoint instrumentation:** ground and spacecraft must independently record active SPI/epoch, pending transaction ID, expected GVCID, persisted candidate/receipt evidence, and monotonic event sequence. Attribute each event to a real component/process, not an outcome flag.
6. **F4 authenticated TC/TM:** prove TC accepted/rejected through the configured cryptographic library and telemetry status authentically returned and correlated to *that* TC and current epoch. A `SAMPLE NOOP` event, CRC-only confirmation, or SUT's own success enumeration is insufficient.
7. **F5/F6/F7:** equal-input comparators, independent trace checker and explicit negative controls, and frozen case/analysis criteria before viewing results. Do not run fault campaigns or report comparative performance before these pass.

## Concrete minimal architecture (planned, not built)

```text
ground controller ──[SDLS protected TC / independent wire capture]──> spacecraft ingress
  | ground SA/epoch log                                      | expected GVCID/SPI policy
  | candidate/receipt journal                                v
  |                                               CryptoLib TC validation
  |                                                          |
  |                                       onboard recovery coordinator (cFS app)
  |                                       journal / activation / restart barrier
  |                                                          |
  +<──[independently protected status TM + wire capture]── telemetry output
                |
       offline independent checker
       (reconstructs state, never trusts SUT "SUCCESS" alone)
```

The recovery coordinator is an **unimplemented new component**. Its intended function is *not* the already published Recovery SA concept; it is fault-tolerant activation/confirmation state management under real process/storage boundaries.

## Independent evidence contract (requires actual measured sources)

| Producer | Minimum raw record | Why it is needed |
|---|---|---|
| Ground control process | PID, process start, monotonic sequence, active SPI/epoch, pending transaction and receipt ID, outbound TC hash | Detect resumed ground state not corroborated by spacecraft |
| OS/process supervisor | Child PID/start and stop, exit signal, disk-flush step and restarted process identity | Prove an actual process interruption and timing |
| Spacecraft ingress/crypto integration | frame ID and observed channel, SPI, SA mode, validation return code, current anti-replay window, accepted/rejected | Verify *channel authorization* and cryptographic library path, not a fake outcome |
| cFS coordinator | transaction phase, pending/active state, journal write/flush/rename evidence, commit and confirmation transitions | Distinguish volatile recovery and persistence order |
| Telemetry protection and ground verify | return TM frame identity, auth verification status, correlated command and epoch, independent receiver result | Distinguish accepted command from verified post-recovery commandability |
| Independent checker | bounded classification `VERIFIED_RESUME` / `SAFE_HOLD` / `UNVERIFIED` / `UNSAFE` with exact observed event IDs | Prevent selective success attribution |

Records must have explicit clock domain and an ordering protocol; a monotonically increasing local sequence is **not** a synchronized cross-host clock. The independent checker must refuse `VERIFIED_RESUME` if either endpoint's SA/epoch, authenticated TM, or trusted receiver path is missing. Key material and sensitive plaintext must never appear in logs.

## Staged runtime implementation once safety gates pass

- **I1** build NOS3 exactly pinned graph with an isolated no-egress runtime and capture component process IDs (no commands). Independent verification of actual software launch.
- **I2** add *new TTCSIL-specific* onboard transaction coordinator and ground adapter with instrumentation; compile into NOS3/cFS without replacing upstream CryptoLib; start with no fault and no operational actions.
- **I3** validate actual protected TC reception and independent authenticated TM return with explicit channel-binding negative controls. No reader should infer security from FECF.
- **I4** enable actual process termination/restart at defined **COMMIT and CONFIRM boundaries** with exact predeclared cutpoints, durable/volatile state comparison, absent-TM safe-hold and stale transaction rejection.
- **I5** independent oracle and matched comparator design review. **Only then** consider authorizing a canonical study/freeze. Retain failures and do not change Study A–D evidence.

**Current status:** source inventory is available; security conditions **HOLD**; integrated NOS3 runtime **NOT EXECUTED**. This is a risk-aware decision, not an inability to launch a simulator. The known concerns must be controlled before any security-sensitive integration output is trusted.
