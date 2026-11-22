# NOS3 / cFS reset question: assessment (2026-11-22)

Status: software-only desk and local-build check. No full NOS3 simulator, cFS or hardware run was performed. Nothing here is a validation of the F1-F4 persistence levels.

Question: does a cFS processor reset versus power-on reset change what survives for the CryptoLib state classes (SA table, ARSN/IV, key ring)?

Evidence gathered (public NASA sources only; NOS3 at 1dadc685, CryptoLib at 329f895 for our runs):
1. CryptoLib source (329f895, src and include) contains no reference to cFE CDS, cFE ES or PSP reset APIs (case-insensitive grep). Its SA table and key ring live in ordinary process memory; the only optional persistence is the SA_FILE snapshot file (CMake option SA_FILE, default OFF in CMakeLists.txt line 62).
2. NOS3 (1dadc685) builds the flight CryptoLib as a cFE library (`CFE_LIB cryptolib` in cfg/nos3_defs/cpu1_cfe_es_startup.scr) and does not enable SA_FILE: the override in cfg/nos3_defs/global_build_options.cmake is commented out. The ground build in the Makefile sets -DSA_FILE=OFF explicitly. So a default NOS3 build corresponds to the SA_FILE=OFF runs here (SA table reverts to initial values on restart; key ring volatile), not to the SA_FILE=ON runs.
3. NOS3 pins CryptoLib b46879c (components/cryptolib), not our 329f895; b46879c has an older config API. Update: the harness was ported (-DCRYPTOLIB_OLD_API) and rerun in the same container kit at b46879c (docker/RESULTS_DOCKER_RUN4_2026-11-21.md, run 6, out_nos3pin/): restart behaviour is identical to 329f895 in all scenarios, with SA_FILE on and off.
Inference (not tested): because CryptoLib state is not placed in CDS, a cFS processor reset and a power-on reset should both lose it; whether the cFS wrapper or NOS3 adds persistence elsewhere (files, other apps) was not checked.

What a full NOS3 run would add: confirmation of that inference inside a real cFE reset path, and behaviour of the NOS3 wrapper/ground path. Cost: several GB of images, hours of build, x86 emulation on Apple Silicon, extra unpinned dependencies (OpenC3, NOS Engine packages). Not run.

Manuscript consequence: none needed. Section 8.10 already says processor or power resets were not exercised. Optional wording only if the author wants it: the default NOS3 build leaves SA_FILE off (this desk finding).
