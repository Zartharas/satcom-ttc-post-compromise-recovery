# TTCSIL native CryptoLib F1–F4 feasibility scaffold

**State:** `PROSPECTIVE_NATIVE_SMOKE_NOT_CANONICAL`  
**Date:** 2026-11-17  
**Authoritative science:** Studies A–D and their retained artifacts are immutable.  
**Upstream checked:** NASA CryptoLib `v1.5.2` -> `c216ede78b2f51b42838b13955602c0b481b53c2`.

## Purpose and proper interpretation

This isolated native harness is intended to determine whether a public, pinned CryptoLib library (i) builds on a fresh runner, (ii) can save/reload **selected SA metadata** across distinct OS processes without a graceful library shutdown, and (iii) can produce, accept and reject a modified **synthetic protected TC frame**. No new research-population outcomes may be drawn from its feasibility logs.

A native-library probe is not the same as a spacecraft cFS restart, a CCSDS Recovery SA transaction, a protected pending/receipt journal, a post-reset command/status recovery trace, a crash-atomic storage test, or external cryptographic validation. In particular, `_exit(0)` simulates process termination after an acknowledged save; it does **not** simulate power loss or a crash during `fwrite`/`fclose`. The `akid` sentinel tests persistence of a metadata field, **not** possession or authentication of key material. TC tamper rejection may be due to FECF and should not be described as cryptographic forgery resistance without further evidence.

## Inputs and upstream behavior

- Source is downloaded from public `https://github.com/nasa/CryptoLib.git` **inside an ephemeral directory**. The tag is checked out at a shallow exact SHA and the HEAD is compared against the expected literal hash. No git submodule or vendor source is stored here.
- CryptoLib is configured `CRYPTO_LIBGCRYPT=ON`, `KEY_INTERNAL=ON`, `MC_INTERNAL=ON`, `SA_INTERNAL=ON`, `SA_FILE=ON`, `DEBUG=ON`, `TEST=ON`, and `CRYPTO_EPROC=OFF`.
- `DEBUG=ON` permits the upstream SA backend's missing-file fallback to initial in-memory test state. This **must not** be interpreted as recovery of a missing or corrupt SA store.
- Selected **upstream** test names `UT_TC_APPLY`, `UT_TC_PROCESS`, `UT_SA_SAVE` are run serially. Their coverage is library-specific and does not establish the project's recovery transaction correctness.
- For the process test, `sa-seed` saves an SA4 metadata marker and exits without `Crypto_Shutdown`; `sa-verify` is a *new OS process*, reinitializes CryptoLib and checks that marker. File-backed behavior here has not established atomicity or durability on power failure.
- A separate synthetic packet probe uses the upstream TC apply-test fixture with a test key index. Sender and receiver are separate processes/working directories. The receiver's strict IV window rejects the first sender frame (IV=0), so the sender performs one local warm-up apply and transmits the next protected frame (advanced IV) without weakening anti-replay. A MAC-byte mutation is made with the FECF recalculated to a valid checksum; the probe now requires the library to return an authentication/MAC-validation error rather than merely an FECF error. This is an *API feasibility check*, not fully independent cryptographic validation.
- The transient packet bytes, saved SA state, and all build outputs are deleted with the script's temp directory. CI logs report only statuses and metadata counts, not keys or raw data.

## Preflight trace and correction (not scientific results)

The first PR #17 native run with `SA_FILE=ON` initially failed to compile because Ubuntu did not have `mysql/mysql.h`; adding `libmariadb-dev-compat` resolved that environment dependency. The next run established exact upstream SHA, native compilation, three upstream unit suites, custom native process-to-process SA metadata reload, and protected TC generation; a fresh receiver then rejected the **first sender IV=0 frame** with CryptoLib status `-23` (IV window). The new fixture uses the subsequent sender IV while keeping anti-replay checks enabled. The initial rejection is retained in GitHub Actions logs and is not a cryptographic attack finding. In the next successful native run, a simple modified-frame probe failed with `CRYPTO_LIB_ERR_INVALID_FECF (-12)`, which is checksum rejection only. The amended negative control now recomputes FECF after modifying the MAC and accepts **only** `CRYPTO_LIB_ERR_MAC_VALIDATION_ERROR` or `CRYPTO_LIB_ERR_AUTHENTICATION_ERROR`; any other rejection remains a failed authentication-isolation gate. **These fixture corrections are not evidence of increased experiment success; the canonical population has not run.**

## Tested/untested boundaries

| Gate | What native CI might establish | Still unproven |
|---|---|---|
| F1 | Exact CryptoLib tag SHA, native build, selected upstream tests | NASA NOS3/cFS dependency graph compatibility, full license/security/advisory audit, version governance |
| F2 | Distinct host processes, reload after acknowledged save | Real spacecraft component reset, crash-mid-write durability, power loss |
| F3 | Readable `spi`, `sa_state`, and metadata marker from library SA API | Pending/receipt states and true ground–space epoch alignment |
| F4 | Protected synthetic TC API acceptance and rejection path | Authenticated TM return, complete post-compromise recovery, independent packet/security oracle |

## Running

CI: workflow `.github/workflows/ttcsil-cryptolib-native-feasibility.yml` with least-privilege `contents: read`, no secrets and no uploaded artifacts.

On a disposable Linux machine with Bash, Git, CMake, compiler and libgcrypt development headers:

```bash
bash paper/extension/ttcsil_preflight/run_native_feasibility.sh --verify-only
bash paper/extension/ttcsil_preflight/run_native_feasibility.sh
```

Not intended to run against an actual spacecraft, live RF, production credentials, flight hardware, or operational ground station.

## Security and provenance concerns

- CryptoLib v1.5.2's file-based SA backend is a feature flag. Its source writes an SA array with `fwrite` and `fclose` and does not show a transactional journal or an explicit `fsync` in that function. No crash-atomicity is established.
- An upstream MariaDB conversion issue [GHSA-3m35-m689-h29x](https://github.com/nasa/CryptoLib/security/advisories/GHSA-3m35-m689-h29x) affects releases <= 1.4.2 and lists v1.4.3 as patched. It is **not** evidence that 1.5.2 is affected; a complete current security review is still pending.
- Current NOS3 `v1_07_06` is tag `1dadc685effc26730603c36c7864afce3c546406`, whose embedded `components/cryptolib` gitlink is `b46879c094f1ae279c2ff04dea3d8e5ecbd4ef92`, **not** standalone `v1.5.2`. cFS `v7.0.1` is `088b2fa828db9ff7e00733f1908e0eeb59f66ce3`. Do **not** substitute or combine these into an alleged validated stack.
- The mission-aware repository's on-hold P2X PRs #214/#215 already assess NOS3/cFS recovery-gate and nominal command evidence. Our prospective novelty must be the independently designed **SA transaction activation/persistence/restart boundary**, not another nominal NOS3 command demo.
- No third-party source code is vendored. CryptoLib and NOS3 are under NASA Open Source Agreement 1.3, with per-file JPL/export notices; cFS bundle under Apache 2.0. A separate redistribution/legal check remains required.

**Do not merge this into an IEEE manuscript as results.** Any subsequent full implementation requires F1–F8 review, protocol freeze and independent exact-event validation before a canonical study.
