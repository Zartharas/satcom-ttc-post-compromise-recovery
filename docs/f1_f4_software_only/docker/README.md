# Docker follow-up for F1-F4 (software only)

Purpose: exercise what the cloud sandbox could not (MariaDB-backed SA tests, SA_FILE off) in a pinned container on your Mac. Nothing here touches hardware or the network at run time.

Not run yet. It is written from the sandbox build notes and may need small flag fixes (CryptoLib option names, test targets, MariaDB init). The key-command path (OTAR/ACTIVATE, which returned status 0 without changing the key ring) and the restart harness are not part of this kit.

Build (needs network once):
    docker build -t cryptolib-f1f4 .
Run (no network, results to ./out):
    mkdir -p out && docker run --rm --network none -v "$PWD/out:/out" cryptolib-f1f4
Record the image digest: docker inspect --format '{{.Id}}' cryptolib-f1f4
Then tell Claude the output folder; do not edit frozen records.
