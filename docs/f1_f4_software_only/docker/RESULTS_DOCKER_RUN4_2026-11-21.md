# F1-F4 software-only Docker run (run 4, passing) - 2026-11-21

Scope: software only. CryptoLib at pinned commit 329f895bd19a6ca1bce509f5f88ebfc9f98c3900, built in a container on the author's Mac (x86_64 Linux image, `--network none` at run time). No hardware, RF, vendor image, live network or spacecraft. cFE/PSP/NOS3 not run.

Image: `cryptolib-f1f4`, `docker inspect` id sha256:7858b3cc1aa9f808f509e66bd854eb2699ea9b31d10e33a95592af2e588e11cc (manifest-list digest). Base: ubuntu:24.04@sha256:9c7f200c07e3d4a03e7249d2c16bf66a51120fb876aa2242cf31451412543289. gcc 13.3.0, cmake 3.28.3, libgcrypt 1.10.3-2ubuntu0.2 (apt, not hash-pinned).
Flags: -DTEST=ON -DKEY_INTERNAL=ON -DSA_INTERNAL=ON -DSA_FILE=ON|OFF -DCRYPTO_EPROC=ON -DMC_INTERNAL=ON -DDEBUG=ON -DCRYPTO_LIBGCRYPT=ON -DKEY_VALIDATION=OFF.

History: runs 1-3 failed for kit configuration errors (MySQL header abort; missing MC_INTERNAL; missing CRYPTO_LIBGCRYPT) and are kept as out_run1..3_*. They support no conclusions. Run 4 output: `out_run4_pass/`.

Unit tests (CryptoLib's own, MySQL/TLS targets excluded; make -k exit 2 from those targets only): SA_FILE=ON 13/13 pass; SA_FILE=OFF 12/12 pass.

Restart harness (abrupt exit without Crypto_Shutdown, second process re-inits). Setup states are forced by the harness, so results show persistence, not protocol compliance.
| scenario | SA_FILE=ON after restart | SA_FILE=OFF after restart |
|---|---|---|
| sa_stop6 (SA6 forced OPERATIONAL, then SA_STOP) | SA6 state 3 (OPERATIONAL): stop not persisted (snapshot saved before command executes) | SA6 state 2: back to init baseline; stop not persisted |
| set_arsn7 (SA7 ARSN set by command) | SA7 state 3, arsn_len 11: persisted | SA7 state 2, arsn_len 2: reverted to baseline |
| key_direct (key 132 set ACTIVE in RAM directly) | key 132 state 0: reverted | key 132 state 0: reverted |
Also: with SA_FILE=ON, SA0 reads state 3 after restart (frame-driven snapshot); with OFF it returns to 1.

Reading: matches the earlier sandbox result. SA persistence depends on the build option and is a snapshot at the next accepted frame; the in-memory key ring does not persist in either build. Not tested: EP key commands (OTAR/ACTIVATE) via valid frames, cFS processor vs power-on reset, CCSDS behaviour. The key_direct row mutates RAM directly and says nothing about command-driven activation.
Caveats: single run per configuration, one architecture; image not rebuilt bit-for-bit reproducibly (apt unpinned).

## Run 5 addendum: command-driven key load and activation (2026-11-21)

Image id sha256:abaf63dc248f370c36ff7de6bc51dbc5fb8c101e2e0e50ff6012f89faa1b9057 (same base image and CryptoLib commit; kit commit 73c876a). Output: `out_run5_pass/`. Unit tests again 13/13 (SA_FILE on) and 12/12 (off).

Why run 4's key row said nothing about commands: the unit-test OTAR/ACTIVATE frames carry two extra 0x0000 bytes before the 0x1980 packet header (SA0 shivf_len = 0), so the extended-procedure dispatcher never ran; the test frame's ACTIVATE TLV length is also not in bits. Run 5 builds valid frames in `restart_harness.c` (`build_ep_frame`, no FECF; OTAR payload AES-256-GCM encrypted under the library's default master key 0, a published test key). All frames returned status 0 and changed the key ring.

| scenario | in process 1 | after restart, SA_FILE on | after restart, SA_FILE off |
|---|---|---|---|
| otar_only (load keys 140-142) | values loaded (a0.., a1.., a2..), state 0 | empty, state 0 | empty, state 0 |
| otar_activate (load, then ACTIVATE) | loaded, state 1 | empty, state 0 | empty, state 0 |
| activate_only | state 1 | state 0 | state 0 |

Reading: command-driven key load and activation do not survive a process restart in either build; the key ring is volatile. This removes run 4's caveat that the key row was a direct RAM change. Not tested: cFS processor reset vs power-on reset (cFE CDS), CCSDS-level behaviour, FECF-enabled or encrypted-SA command paths, other key IDs. Library quirk seen, not investigated: key_len stays 0 after OTAR although the bytes are stored.
