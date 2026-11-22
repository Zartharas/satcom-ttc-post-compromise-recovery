#!/bin/bash
# Builds CryptoLib (SA_FILE on and off), runs its own tests (MySQL/TLS targets excluded: they need a database
# server and certificates), then runs the restart harness: each invocation is a new process (abrupt restart).
set -u
mkdir -p /out; : > /out/summary.txt
cd /src/CryptoLib; git rev-parse HEAD > /out/cryptolib_sha.txt
{ gcc --version | head -1; cmake --version | head -1; dpkg -s libgcrypt20-dev | grep '^Version'; uname -m; } > /out/toolchain.txt
for cfg in on off; do
  b=/build/sa_file_$cfg; rm -rf $b; mkdir -p $b; cd $b
  flag=$([ $cfg = on ] && echo ON || echo OFF)
  cmake /src/CryptoLib -DTEST=ON -DKEY_INTERNAL=ON -DSA_INTERNAL=ON -DSA_FILE=$flag -DCRYPTO_EPROC=ON -DMC_INTERNAL=ON -DDEBUG=ON -DCRYPTO_LIBGCRYPT=ON -DKEY_VALIDATION=OFF > /out/sa_file_${cfg}_cmake.txt 2>&1
  make -k -j2 > /out/sa_file_${cfg}_make.txt 2>&1
  echo "sa_file_$cfg make exit: $? (mysql/TLS targets may fail to compile)" >> /out/summary.txt
  ctest -E mysql --output-on-failure > /out/sa_file_${cfg}_ctest.txt 2>&1
  echo "sa_file_$cfg ctest exit: $?" >> /out/summary.txt
  grep -E "tests passed|tests failed" /out/sa_file_${cfg}_ctest.txt >> /out/summary.txt
  # harness
  gcc ${OLD_API:+-DCRYPTOLIB_OLD_API} -o /build/h_$cfg /src/restart_harness.c -I/src/CryptoLib/include -L$b -lcryptolib -Wl,-rpath,$b -lgcrypt > /out/harness_${cfg}_compile.txt 2>&1
  w=/work/$cfg; rm -rf $w; mkdir -p $w; cd $w
  for sc in sa_stop6 set_arsn7 key_direct otar_only otar_activate activate_only; do
    /build/h_$cfg $sc > /out/harness_${cfg}_${sc}_p1.txt 2>&1
    /build/h_$cfg dump > /out/harness_${cfg}_${sc}_p2.txt 2>&1
    echo "harness $cfg $sc done" >> /out/summary.txt
  done
done
cat /out/summary.txt
