# F1-F4 software-only follow-up: pinned CryptoLib, SA_FILE on/off, restart harness.
# Build needs network (clone, apt); run with --network none.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git ca-certificates libgcrypt20-dev \
    && rm -rf /var/lib/apt/lists/*
ARG CRYPTOLIB_SHA=329f895bd19a6ca1bce509f5f88ebfc9f98c3900
ARG OLD_API=
ENV OLD_API=${OLD_API}
WORKDIR /src
RUN git clone https://github.com/nasa/CryptoLib.git && cd CryptoLib && git checkout ${CRYPTOLIB_SHA}
COPY restart_harness.c /src/restart_harness.c
COPY run_variants.sh /usr/local/bin/run_variants.sh
RUN chmod +x /usr/local/bin/run_variants.sh
CMD ["/usr/local/bin/run_variants.sh"]
