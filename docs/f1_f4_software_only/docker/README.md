# Docker follow-up for F1-F4 (software only)

Pinned CryptoLib build in a container, SA_FILE on/off, unit tests plus a restart harness. No hardware or network at run time. See RESULTS_DOCKER_RUN4_2026-11-21.md.

Build (needs network once):
    docker build -t cryptolib-f1f4 .
Run (no network, results to ./out):
    mkdir -p out && docker run --rm --network none -v "$PWD/out:/out" cryptolib-f1f4
Record the image id: docker inspect --format '{{.Id}}' cryptolib-f1f4

MySQL/TLS test targets are not built (make -k) or run. Key-command (OTAR/ACTIVATE) frames are not part of this kit.
Runs 1-3 failed for kit errors and are kept as out_run1..3_*; runs 4 and 5 are out_run4_pass/ and out_run5_pass/. Do not edit frozen records.

NOS3-pinned CryptoLib (b46879c, older API; run 6): build the same kit at that commit with a separate image name and output folder:
    docker build -t cryptolib-f1f4-nos3pin --build-arg CRYPTOLIB_SHA=b46879c094f1ae279c2ff04dea3d8e5ecbd4ef92 --build-arg OLD_API=1 .
    mkdir -p out_nos3pin && docker run --rm --network none -v "$PWD/out_nos3pin:/out" cryptolib-f1f4-nos3pin
