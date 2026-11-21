# F1-F4 software-only evidence: restart persistence of SDLS SA / key / ARSN state

Run date (UTC): 2026-11-21. Author-authorised SOFTWARE-ONLY run. Skills applied (as instructed): multi-expert-analysis, cryptography-pki-zero-trust-suite (read-only; test keys from the library's own tests only), assessing-ot-ics-security (passive, source-based framing), secure-software-delivery-supply-chain (provenance), academic-research-suite and academic-manuscript-copyedit (wording).

## 1. Scope and safety conditions as followed
- Worked only under /tmp/f1f4 (src/, build/, work/, out/). No file in the user's repo or Mac was touched or read. Nothing published, posted or pushed.
- Network: only `git clone --depth 1` of nasa/CryptoLib, nasa/nos3, nasa/cFE, nasa/osal, nasa/PSP, plus `apt-get update` and `apt-get install libgcrypt20-dev` (pulls libgpg-error-dev) as a build dependency. The CCSDS standards were NOT downloaded (that would be network use outside the allowed list).
- No hardware, RF, vendor/proprietary images, live network or spacecraft. No Docker/VM started (Docker CLI present, daemon not running; not used). No privileged operation beyond root apt install in the sandbox.
- Keys used: only the hard-coded test keys in CryptoLib's own key_interface_internal and unit-test frames. No real key material.
- "Restart" = a new OS process of a user-space library with abrupt exit (no Crypto_Shutdown). It is not a processor reset.

## 2. Pinned commits and provenance
| Repo | Branch | SHA | Commit date |
|---|---|---|---|
| nasa/CryptoLib | dev (default) | 329f895bd19a6ca1bce509f5f88ebfc9f98c3900 | 2026-11-18 |
| nasa/cFE | dev | 3673163b7fd34d7bb69546f1cd13ddb39ac7cde6 | 2026-10-29 |
| nasa/PSP | dev | 5c8a96967e7fc8c6cab1c657fed114abe2336f76 | 2026-10-26 |
| nasa/osal | dev | ffc9d265abd5e21e257c3304fad54fe32c41407c | 2026-11-19 |
| nasa/nos3 | main | 1dadc685effc26730603c36c7864afce3c546406 | 2026-10-30 |
(out/pinned_shas.txt; shallow clones, submodules NOT fetched.)

Toolchain: gcc 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1), cmake 3.28.3, Python 3.13.18 (not used for the harness). Runtime/build deps: libgcrypt20(-dev) 1.10.3-2ubuntu0.2, libgpg-error-dev 1.47-3build2.1 (Ubuntu apt, version-recorded but not hash-pinned; the apt index was fetched live = unpinned dependency). The library links only libgcrypt, libgpg-error, libc (ldd, out/provenance.txt). The unit tests vendor utest.h (sheredom/utest.h; vendored copy, version unrecorded, license not verified here). Licenses (LICENSE heads read): CryptoLib and nos3 = NASA Open Source Agreement 1.3; cFE, PSP, osal = Apache-2.0. libgcrypt's license was not checked in this sandbox. Build flags: -DDEBUG -DMC_INTERNAL -DTEST -DSA_FILE -DCRYPTO_LIBGCRYPT -DKEY_INTERNAL -DSA_INTERNAL -DCRYPTO_EPROC -DKEY_VALIDATION=0 (note: KEY_VALIDATION=0 as an ON/OFF option; not toggled further). No SBOM tool, signature or checksum verification of the clones was done (GitHub TLS only).

## 3. EXERCISED vs READ-ONLY vs NOT EXERCISED
| Item | Status | Reason / evidence |
|---|---|---|
| CryptoLib in-memory SA + internal key ring + libgcrypt build | EXERCISED | out/build_log_k.txt |
| CryptoLib unit tests (13 of 13 buildable) | EXERCISED, 13/13 passed | out/ctest_output.txt. Three test targets (ut_mysql_tls_connection, ut_mysql_m_tls_connection, ut_sadb_err_cases_kmc_crypto) failed to compile: mysql/mysql.h absent (MariaDB dev package not installed). Built with `make -k`. |
| Process-restart harness: SA state loss (SA_STOP on SPI 6) | EXERCISED | out/harness/restart_harness.c, raw_sa_stop6_p*.txt |
| Process-restart harness: ARSN set on SPI 7 | EXERCISED but UNINFORMATIVE | command sets ARSN to all-zero, same as baseline; persistence of a non-zero advancing ARSN not demonstrated |
| Process-restart harness: key ring state after restart | EXERCISED (direct RAM mutation only) | scenario key_direct. |
| Key OTAR / ACTIVATE via real EP command frames | NOT EXERCISED (effect) | Unit-test frames returned status 0 but no "Received SDLS command" dispatch occurred and key ring stayed unchanged (raw_otar_*_p1.txt, MC log -17 NULL_ABM). Not diagnosed beyond one retry (stop rule). So half-finished OTAR+activate across restart was not shown by command; only code-read (Sec. 4). The repo's own key tests assert only status, not key state (test/unit/ut_ep_key_mgmt.c). |
| SA_FILE=OFF behaviour | READ-ONLY | not built |
| MariaDB SA backend | READ-ONLY / NOT EXERCISED | no DB server, no client headers; would need extra package + server |
| KMC key backend, SQLite | NOT EXERCISED / not present | SQLite backend does not exist in this commit (only inmemory, mariadb, custom) |
| cFE / PSP / OSAL | READ-ONLY | not built or run |
| NOS3 full simulator | NOT EXERCISED | docs/wiki/NOS3_Install_Build_Run_QuickStart.md:9-10,27: VirtualBox + Vagrant VM; NOS3 Makefile uses Docker; Docker daemon not running; forbidden/privileged. |
| CCSDS 355.0-B-2 / 355.1-B-1 | NOT OPENED | no document obtained; no claim made |

## 4. Persistence mapping with file:line evidence (paths relative to the pinned clones)
Observed (O) = seen in harness output; Code (C) = read only.

F1 SA state (UNKEYED/KEYED/OPERATIONAL; this library has SA_NONE=0, UNKEYED=1, KEYED=2, OPERATIONAL=3, include/crypto_config.h:71-74; PREACTIVE/ACTIVE exist only as KEY states, :88-92):
- C: SA table is a static array `sa[NUM_SA]` (src/sa/internal/sa_interface_inmemory.template.c:46).
- C: Persistence exists only when built with -DSA_FILE (CMakeLists.txt:62, :142; template.c:237, :663, :691), which writes the whole table to `sa_save_file.bin` (include/crypto_config.h:265; fwrite template.c:195-204) and reloads it at init (sa_load_file :77-120, sa_init :685-700). Default is OFF.
- C: With SA_FILE off, init rebuilds the table from hard-coded values (sa_init :703-750, sa_populate :251-600). With SA_FILE on and no file, the fallback-to-defaults is inside `#ifdef DEBUG` (:663-675), i.e. a non-DEBUG build returns an error instead.
- C: Management commands start/stop/rekey/expire/create/delete/setARSN mutate RAM only and do not call the save function (template.c:1204, :1287, :1385, :1450, :1590, :1648, :1683; save call sites are only in crypto_tc.c:1330, :1828, crypto_tm.c:128, :844, crypto_aos.c:923, :997).
- C: The save in the TC path is in Crypto_TC_Check_IV_ARSN (crypto_tc.c:1811, save :1828), invoked at :2214, BEFORE the extended-procedure command executes (:2224). No save follows the command.
- O (SA_STOP SPI 6): RAM after command = KEYED (2); after new process = OPERATIONAL (3). The ground-commanded stop is lost on restart, and a stale pre-command snapshot is restored. out/harness_summary_final.txt, raw_sa_stop6_p1/p2.txt.
- O: SA table mutations made by the test setup before the frame (SA0 -> OPERATIONAL etc.) were written out at the frame's save and survived restart; i.e. the snapshot is whole-table, taken at frame-processing time, not per-command.
- C: MariaDB backend: `sa_save_sa` issues only `UPDATE ... SET iv, arsn` (sa_interface_mariadb.template.c:58-61, :248-290); start/stop/rekey/expire/create/setARSN/delete are empty stubs returning success (:298-341). State is then whatever the database holds (externally managed). Not run.
- C: NOS3 builds CryptoLib with `-DSA_FILE=OFF` (nos3/Makefile:66) and the line setting SA_FILE in global_build_options.cmake is commented out (:36), so the NOS3 default is volatile SA state.
- C: sa_populate calls sa_perform_save unconditionally (template.c:602), so a default build still writes sa_save_file.bin to the working directory but never reads it (read gated by SA_FILE at :691). Observed file in work/ only for SA_FILE builds; the SA_FILE=OFF case is code-read.

F2 ARSN / IV:
- C: IV and ARSN live in the SA struct (crypto_structs.h SecurityAssociation_t) and share the F1 persistence path above; in the TC path they are saved only after the anti-replay check passes (crypto_tc.c:1820-1830).
- C: MariaDB persists IV and ARSN on each save (template.c:58-61), even though SA state transitions are not implemented there.
- O (limited): values in RAM at a frame's save survive restart (SA0 IV b6ac8e4963f49207ffd6374b was restored in otar_activate). A non-zero advancing ARSN counter across restart was not demonstrated; the harness ARSN scenario sets zeros.

F3 half-finished key activation / rotation:
- C: Key ring is a static array initialised from literals on every init: `key_ring[NUM_KEYS]` (src/key/internal/key_interface_internal.template.c:21), zeroed and re-seeded in key_init (:54-70, :103-599), called from Crypto_Init (src/core/crypto_config.c:352). No file or DB persistence of keys or key_state exists in the internal key interface. key_shutdown is empty (:607).
- C: OTAR writes key bytes into RAM and sets PREACTIVE (src/core/crypto_key_mgmt.c:195-210); activate/deactivate/destroy advance state only if current state == requested-1 (:347-349; dispatch crypto.c:653-677). Both RAM-only.
- O (direct mutation, not command-driven): key 141 set ACTIVE with new byte, key 132 PREACTIVE->ACTIVE; after new process key 141 back to PREACTIVE/zero and key 132 back to PREACTIVE (raw_key_direct_p1/p2.txt). The SA file was written at the same time and survived. So SA table and key ring have DIFFERENT persistence classes in the same library build.
- C: KMC key backend (key_interface_kmc) keeps keys externally; semantics not read in depth and not run.

F4 flight-software platform (cFE/PSP, read-only):
- cFE has two reset types, POWERON and PROCESSOR (cFE/modules/es/fsw/src/cfe_es_start.c:325-340 for power-on handling; processor-reset path :405-470; excessive processor resets escalate to power-on, :405-415).
- CDS "can survive an Application restart as well as a Processor Reset" (cFE/modules/core_api/fsw/inc/cfe_es.h:1034). CFE_ES_RegisterCDS does not initialise data; a new block must be filled by the app via CFE_ES_CopyToCDS (cfe_es.h:1040-1046; copy impl cfe_es_cds.c:1732); CFE_ES_RestoreFromCDS reports a CRC error but still copies data (cfe_es.h:1150-1180). At init cFE validates the CDS and wipes/rebuilds it if invalid (cfe_es_cds.c:69-150).
- On POWERON the PSP clears CDS memory (PSP/fsw/pc-linux/src/cfe_psp_memory.c:646-649). Reset area and user-reserved memory are cleared too (:650-655). Only the pc-linux and mcp750-vxworks PSP reset code was looked at; flight PSPs may differ.
- No use of CFE_ES_RegisterCDS/CopyToCDS was found in nasa/CryptoLib or the nasa/nos3 top-level tree (grep; nos3 submodules not fetched), so CryptoLib is not shown to use CDS.

### Mapping to the Part II levels (INTERPRETATION unless marked O)
| Component, configuration | Part II level | Basis |
|---|---|---|
| Key ring + key_state (internal key IF) | volatile (O for direct mutation; C for OTAR path) | re-seeded on init |
| SA state, SA_FILE off (CryptoLib/NOS3 default) | volatile | C |
| SA state + IV/ARSN, SA_FILE on | none of the three exactly: snapshot taken at the next accepted frame, before the command applies. Closest to "commit" but the commit point is an unrelated later event, and anti-replay progress is committed before the command effect | O for SA6 stop, C for ordering |
| SA IV/ARSN, MariaDB | journal-like for IV/ARSN only (per-frame update), volatile-or-external for SA state | C |
| cFS CDS app data (if an app chose to use it) | commit (explicit CopyToCDS), survives processor reset, lost on power-on | C |
Nothing in the sources read resembles an atomic "journal" of a pending-key-activation candidate.

## 5. Spec gaps found (for the author to decide on manuscript changes)
1. Three levels are not the right axis for CryptoLib: persistence differs per state class (SA table vs key ring vs IV/ARSN) and per build option; a single scalar "restart persistence level" for the pending candidate hides this. Consider a per-state-class tuple.
2. "Commit" in Part II means candidate survives only after commit. In CryptoLib SA_FILE the persist point is the next accepted frame's anti-replay check, which is not tied to command completion. Observed consequence: the last command's effect can be lost while earlier setup is kept (SA6 stop reverted to OPERATIONAL). This is a "stale-snapshot rollback" outcome the three-level model does not name.
3. Order inversion: anti-replay state (IV/ARSN) is persisted at crypto_tc.c:1828 before the command takes effect (:2224). A crash between them leaves ARSN advanced and effect not applied, so a ground retransmission of the same frame would fail replay checks while the commanded change is absent. This is code-read only; no crash-injection was run. Relevant to resynchronisation liveness.
4. Key state is volatile while SA state may be persistent (O). After restart an SA could reload as KEYED/OPERATIONAL while its key reverted to its boot-time state (the library reloads literal key values; real keys would need re-load). Divergence of SA and key state is plausible but I did not demonstrate an SA referencing a lost key.
5. Library vs platform: persistence in CryptoLib is app-level file/DB, not cFE CDS. cFE offers the commit-type primitive (CDS) with defined reset-type semantics (survives processor reset, wiped at power-on) but CryptoLib/NOS3 as read do not use it. The "assumption" framing in the manuscript is therefore justified; the mapping is configuration-dependent.
6. Reset-type distinction (processor vs power-on) exists in cFE but not in CryptoLib: a file or DB-based store survives both. The paper's levels may need a second dimension (survives processor reset only vs survives power cycle).
7. Spec ambiguity left open: CCSDS documents 355.0-B-2 / 355.1-B-1 were not opened; no claim about what they require for persistence.
8. Default-config quirk: SA_FILE-on, file-missing, non-DEBUG build fails init rather than defaulting (template.c:663-675). SA_FILE-off builds still write the file (:602).

## 6. Safety framing (OT/ICS lens, passive)
A processor restart on a satellite is a safety/availability event: persisted-stale security state (e.g. an old OPERATIONAL SA or reverted key state) may block or admit commands incorrectly while ground cannot physically intervene. This report is source-based and a user-space process-restart simulation; it makes no statement about any real spacecraft and recommends no operational test. Any hardware-in-loop or flatsat reset test would need separate authorisation.

## 7. Limitations
Software-only; one library version at a single commit; same-author interpretation of the mapping; process restart is not a processor/power reset (no timing, no brown-out, no partial-write, no torn-file behaviour tested; sa_perform_save truncates with fopen "wb" then fwrite, :195-204, so a crash mid-write was not tested); key-command path not shown to take effect in the harness; ARSN scenario did not exercise a non-zero advancing counter; MariaDB/KMC/SA_FILE=OFF not run; cFE/PSP read only, only two PSPs sampled; NOS3 not run; apt dependencies unpinned; shallow clones not signature-verified; CCSDS texts unopened.

## 8. Devil's advocate: what this does NOT show
A critic would say: CryptoLib is a ground/onboard reference library, not flight code that runs on a flight computer; its SA_FILE option is a test convenience (the repo's own tests use it), so its behaviour says little about how a real flight integrator would persist SA state, and NOS3 explicitly disables it. The one clean observation (a stale SA snapshot after a stop command) was produced by my harness's own setup (test setup mutated SA6 before the frame, which is why the saved copy was OPERATIONAL), and the key-activation half of the question, the most relevant to the paper, was not shown by commands at all. A process exit is not a spacecraft reset, so nothing here supports a claim about real flight persistence, only that this open-source implementation has heterogeneous, option-dependent persistence that does not cleanly fit three levels. Three data points chosen by the same author who proposed the mapping cannot validate it.

## 9. Ready-to-paste paragraph (<=120 words; no citations to preserve, add repo citation keys as needed)
"To check whether the persistence assumption has concrete counterparts, we read and partly ran the open-source NASA CryptoLib (commit 329f895) and read cFE/PSP. In a software-only process-restart test, the in-memory key ring reverted to its initial state, while the Security Association table survived only when built with the optional file-save option, as a snapshot taken at the next accepted frame, and a stop command issued before restart was lost. We did not exercise key activation by command, hardware, power or processor resets, or any CCSDS-specified behaviour. These observations are version- and configuration-specific, interpretive, and do not validate the volatile, commit and journal levels."
