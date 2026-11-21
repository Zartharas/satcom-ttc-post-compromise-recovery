# Docker follow-up for F1-F4 (software only)

Pinned CryptoLib build in a container, SA_FILE on/off, unit tests plus a restart harness. No hardware or network at run time. See RESULTS_DOCKER_RUN4_2026-11-21.md.

Build (needs network once):
    docker build -t cryptolib-f1f4 .
Run (no network, results to ./out):
    mkdir -p out && docker run --rm --network none -v "$PWD/out:/out" cryptolib-f1f4
Record the image id: docker inspect --format '{{.Id}}' cryptolib-f1f4

MySQL/TLS test targets are not built (make -k) or run. Key-command (OTAR/ACTIVATE) frames are not part of this kit.
Runs 1-3 failed for kit errors and are kept as out_run1..3_*; run 4 is out_run4_pass/. Do not edit frozen records.
