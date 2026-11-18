#!/usr/bin/env bash
set -euo pipefail
base="$(cd -- "$(dirname -- "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf -- "$tmp"' EXIT
command -v cc >/dev/null

cc -std=c11 -O2 -Wall -Wextra -Wpedantic -Wconversion -Werror \
  -I"$base" "$base/ttcsil_ingress_guard.c" "$base/test_ttcsil_ingress_guard.c" \
  -o "$tmp/ttcsil_guard_unit"
"$tmp/ttcsil_guard_unit"

cc -std=c11 -g -O1 -Wall -Wextra -Wpedantic -Wconversion -Werror \
  -fsanitize=address,undefined -fno-omit-frame-pointer -I"$base" \
  "$base/ttcsil_ingress_guard.c" "$base/test_ttcsil_ingress_guard.c" \
  -o "$tmp/ttcsil_guard_sanitized"
ASAN_OPTIONS=detect_leaks=1 "$tmp/ttcsil_guard_sanitized"
echo "TTCSIL_C11_SANITIZERS=PASS"
echo "TTCSIL_UPSTREAM_CRYPTO_VALIDATION=NOT_EXECUTED"
echo "TTCSIL_NOS3_CFE_DISPATCH_INTEGRATION=NOT_EXECUTED"
echo "TTCSIL_RESEARCH_PROTOCOL=DRAFT_NOT_FROZEN"
