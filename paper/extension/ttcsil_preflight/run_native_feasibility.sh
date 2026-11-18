#!/usr/bin/env bash
# Isolated feasibility smoke test, NOT canonical TTCSIL outcome execution.
# Uses a public upstream CryptoLib revision, synthetic packets and ephemeral workdirs.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CRYPTO_SHA="c216ede78b2f51b42838b13955602c0b481b53c2"
CRYPTO_TAG="v1.5.2"
ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ttcsil-cryptolib-native.XXXXXXXX")"
trap 'rm -rf -- "$ROOT"' EXIT
export GIT_TERMINAL_PROMPT=0

if [[ "${1:-}" == "--verify-only" ]]; then
  test -r "$SCRIPT_DIR/native_sa_smoke.c"
  test "$CRYPTO_SHA" = "c216ede78b2f51b42838b13955602c0b481b53c2"
  echo "TTCSIL_PREFLIGHT_SOURCE_LAYOUT=PASS"
  exit 0
fi
if [[ $# -ne 0 ]]; then
  echo "Usage: $0 [--verify-only]" >&2
  exit 64
fi

for command in git cmake ctest cc sha256sum; do
  command -v "$command" >/dev/null || { echo "MISSING_TOOL=$command" >&2; exit 2; }
done
echo "TTCSIL_PREFLIGHT_MODE=UPSTREAM_NATIVE_FEASIBILITY_ONLY"
echo "TTCSIL_PREFLIGHT_PUBLIC_UPSTREAM=nasa/CryptoLib"
echo "TTCSIL_PREFLIGHT_EXPECTED_UPSTREAM=$CRYPTO_SHA"
echo "TTCSIL_PREFLIGHT_PROTECTED_RESEARCH_MODIFIED=false"
echo "TTCSIL_PREFLIGHT_CANONICAL_RESULTS_GENERATED=false"

git clone --quiet --depth 1 --branch "$CRYPTO_TAG" \
  https://github.com/nasa/CryptoLib.git "$ROOT/cryptolib"
HEAD="$(git -C "$ROOT/cryptolib" rev-parse HEAD)"
[[ "$HEAD" == "$CRYPTO_SHA" ]] || {
  echo "UPSTREAM_SOURCE_PIN_MISMATCH expected=$CRYPTO_SHA actual=$HEAD" >&2
  exit 3
}
[[ -f "$ROOT/cryptolib/LICENSE" ]] || { echo "UPSTREAM_LICENSE_MISSING" >&2; exit 3; }
echo "TTCSIL_CRYPTO_SOURCE_PIN=PASS sha=$HEAD"
echo "TTCSIL_UPSTREAM_LICENSE_REVIEW=MANUAL_GATE_REQUIRED"

cmake -S "$ROOT/cryptolib" -B "$ROOT/build" \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCRYPTO_LIBGCRYPT=ON \
  -DKEY_INTERNAL=ON \
  -DMC_INTERNAL=ON \
  -DSA_INTERNAL=ON \
  -DSA_FILE=ON \
  -DDEBUG=ON \
  -DCRYPTO_EPROC=OFF \
  -DSUPPORT=OFF \
  -DTEST=ON
cmake --build "$ROOT/build" --parallel 2
echo "TTCSIL_NATIVE_CRYPTO_LIBRARY_BUILD=PASS"

# Vendor test coverage is informative, not evidence of our custom recovery protocol.
ctest --test-dir "$ROOT/build" --output-on-failure -j 1 \
  -R '^(UT_TC_APPLY|UT_TC_PROCESS|UT_SA_SAVE)$'
echo "TTCSIL_UPSTREAM_SELECTED_TESTS=PASS"

cc -std=c11 -Wall -Wextra -Werror -O0 -g \
  -I"$ROOT/cryptolib/include" \
  "$SCRIPT_DIR/native_sa_smoke.c" \
  -L"$ROOT/build/src" -lcryptolib \
  -Wl,-rpath,"$ROOT/build/src" \
  -o "$ROOT/ttcsil_native_probe"
test -x "$ROOT/ttcsil_native_probe"
echo "TTCSIL_CUSTOM_NATIVE_PROBE_COMPILE=PASS"

# Distinct OS process invocations, same isolated SA file.
mkdir -p "$ROOT/restart"
(
  cd "$ROOT/restart"
  "$ROOT/ttcsil_native_probe" sa-seed
  test -s sa_save_file.bin
  "$ROOT/ttcsil_native_probe" sa-verify
)
echo "TTCSIL_NATIVE_SA_SEPARATE_PROCESS_RELOAD=PASS"

# Separate TX and RX working directories ensure no shared SA snapshot or test runtime state.
mkdir -p "$ROOT/tc-sender" "$ROOT/tc-receiver" "$ROOT/tc-negative"
(
  cd "$ROOT/tc-sender"
  "$ROOT/ttcsil_native_probe" tc-send "$ROOT/protected_tc.bin"
)
(
  cd "$ROOT/tc-receiver"
  "$ROOT/ttcsil_native_probe" tc-receive "$ROOT/protected_tc.bin"
)
(
  cd "$ROOT/tc-negative"
  "$ROOT/ttcsil_native_probe" tc-tamper "$ROOT/protected_tc.bin"
)
echo "TTCSIL_NATIVE_PROTECTED_TC_FRESH_ACCEPT_AND_TAMPER_REJECT=PASS"

# Separate F1-only bridge: actual CryptoLib decode/SA lookup -> independent
# local authorization policy, never cFS dispatch or a recovery transaction.
GUARD_DIR="$(dirname -- "$SCRIPT_DIR")/ttcsil_integration/security_boundary"
cc -std=c11 -Wall -Wextra -Werror -O0 -g \
  -I"$ROOT/cryptolib/include" -I"$GUARD_DIR" \
  "$GUARD_DIR/native_cryptolib_guard_bridge.c" \
  "$GUARD_DIR/ttcsil_ingress_guard.c" \
  -L"$ROOT/build/src" -lcryptolib \
  -Wl,-rpath,"$ROOT/build/src" \
  -o "$ROOT/ttcsil_native_guard_bridge"
mkdir -p "$ROOT/native-guard-adapter"
(
  cd "$ROOT/native-guard-adapter"
  "$ROOT/ttcsil_native_guard_bridge" "$ROOT/protected_tc.bin"
)
echo "TTCSIL_NATIVE_CRYPTO_TO_GUARD_BRIDGE=PASS"
echo "TTCSIL_NATIVE_LIMITATIONS=No_crash_atomicity;No_T1_or_Recovery_SA_transaction;No_measured_epoch;No_TM_status;No_NOS3_or_cFS_integration"
echo "TTCSIL_F1_TO_F4_CANONICAL_GATE=NOT_PASSED"
