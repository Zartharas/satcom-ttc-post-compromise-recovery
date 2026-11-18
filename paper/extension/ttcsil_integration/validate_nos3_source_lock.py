#!/usr/bin/env python3
"""Read-only, fail-closed upstream source inventory; no simulator or canonical study.

Verifies the exact NOS3 gitlink graph and screens two pinned CryptoLib TC
receive-path function bodies. A successful return means 'provenance checked,
security blocked until independent review', not 'secure/compatible'.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_COMPONENTS = {
    "components/cryptolib": "b46879c094f1ae279c2ff04dea3d8e5ecbd4ef92",
    "fsw/cfe": "87e273743f3d07ed9216462b461e9f398ff96c87",
    "fsw/osal": "08a79bb6ac02b9ced8aa555853ecdd96e5ebc1a7",
    "fsw/psp": "d0a5d6fa4093d473a929fde42a0983e489d89d4a",
    "gsw/cosmos": "bae4d7470ef05a75a8e006f35dd448927df6a1a5",
}
NOS3_SHA = "1dadc685effc26730603c36c7864afce3c546406"
STANDALONE_SHA = "c216ede78b2f51b42838b13955602c0b481b53c2"
EMBEDDED_SHA = REQUIRED_COMPONENTS["components/cryptolib"]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.stdout.rstrip("\n")


def validate_lock(data: dict) -> None:
    check(data.get("schema_version") == 1, "unexpected lock schema")
    check(data.get("study") == "TTCSIL-SA-RST-001", "unexpected study ID")
    check(data.get("phase") == "F1_PIN_AND_SECURITY_REVIEW_ONLY", "non-F1 lock")
    check(data.get("science_protocol_state") == "DRAFT_NOT_FROZEN_NO_CANONICAL_EXECUTION", "cannot execute canonical study")
    upstream = data["upstream"]
    nos3 = upstream["nos3"]
    check(nos3["sha"] == NOS3_SHA and nos3["tag"] == "v1_07_06", "NOS3 revision mismatch")
    links = nos3["gitlinks"]
    check(nos3["gitmodules_count"] == len(links) and len(links) >= 40, "incomplete gitlink graph")
    check(len({x["path"] for x in links}) == len(links), "duplicate gitlinks")
    check(all(re.fullmatch(r"[a-f0-9]{40}", x["sha"]) for x in links), "bad gitlink sha")
    link_map = {x["path"]: x["sha"] for x in links}
    for path, sha in REQUIRED_COMPONENTS.items():
        check(link_map.get(path) == sha, "changed pinned component: " + path)
    check(upstream["cryptolib_standalone"]["sha"] == STANDALONE_SHA, "standalone CryptoLib SHA mismatch")
    check(upstream["cryptolib_nos3"]["sha"] == EMBEDDED_SHA, "embedded CryptoLib SHA mismatch")
    check(upstream["cfs_standalone"]["integrated_with_nos3"] is False, "invalid cFS compatibility claim")
    check(upstream["cfe_nos3"]["sha"] == REQUIRED_COMPONENTS["fsw/cfe"], "incorrect embedded cFE")
    reviews = {x["id"]: x for x in data["security_review"]}
    check("CVE-2026-79954" in reviews and "CVE-2026-82480" in reviews, "missing advisory screen")
    for item in reviews.values():
        check(item["disposition"] == "HOLD_AND_REVIEW", "security hold missing: " + item["id"])
    check(data["readiness"]["F2_real_integrated_restart"] == "NOT_EXECUTED", "F2 incorrectly promoted")
    check(data["readiness"]["F3_dual_endpoint_state"] == "NOT_EXECUTED", "F3 incorrectly promoted")
    check(data["readiness"]["F4_end_to_end_tc_tm"] == "NOT_EXECUTED", "F4 incorrectly promoted")


def inspect_nos3(root: Path, expected: dict) -> None:
    head = git(root, "rev-parse", "HEAD")
    check(head == NOS3_SHA, f"NOS3 source mismatch: {head}")
    text = git(root, "ls-tree", "-r", "HEAD")
    actual = {}
    for line in text.splitlines():
        if not line.startswith("160000 commit "):
            continue
        m = re.fullmatch(r"160000 commit ([a-f0-9]{40})\t(.+)", line)
        check(m is not None, "unexpected gitlink entry")
        actual[m.group(2)] = m.group(1)
    planned = {x["path"]: x["sha"] for x in expected["upstream"]["nos3"]["gitlinks"]}
    check(actual == planned, "NOS3 complete gitlink graph does not match pinned source lock")
    print(f"TTCSIL_NOS3_HEAD_AND_GITLINKS=PASS head={head} count={len(actual)}")


def extract_function(source: str, name: str) -> str:
    sig = "static int32_t " + name + "("
    start = source.rfind(sig)
    check(start >= 0, name + " missing")
    opening = source.find("{", start)
    check(opening >= 0 and opening - start < 250, name + " definition not found")
    depth = 0
    for i in range(opening, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return source[start:i + 1]
    raise ValueError("unclosed source function: " + name)


def inspect_crypto(path: Path, label: str) -> None:
    source = path.read_text(encoding="utf-8")
    function = extract_function(source, "crypto_tc_validate_sa")
    check("sa->sa_state" in function, "unexpected crypto_tc_validate_sa layout")
    # This screen is deliberately limited: absence of a binding here does not
    # prove absence everywhere. The full TC receive path needs expert audit.
    direct_binding = ("gvcid_blk" in function or "Gvcid" in function)
    check(not direct_binding, "Source changed: manual security review required before CI approval")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    print(f"TTCSIL_{label}_CRYPTO_TC_VALIDATE_SA_SOURCE_SHA256={digest}")
    print(f"TTCSIL_{label}_DIRECT_SA_GVCID_BINDING_IN_CHECKED_FUNCTION=NOT_OBSERVED")
    print(f"TTCSIL_{label}_FULL_RECEIVE_PATH_AUTHORIZATION=UNVERIFIED")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lock", type=Path, default=Path(__file__).with_name("NOS3_SOURCE_LOCK_AND_SECURITY_HOLD_2026-11-17.json"))
    p.add_argument("--nos3", type=Path)
    p.add_argument("--standalone-crypto-tc", type=Path)
    p.add_argument("--embedded-crypto-tc", type=Path)
    args = p.parse_args()
    data = json.loads(args.lock.read_text(encoding="utf-8"))
    validate_lock(data)
    print("TTCSIL_PROSPECTIVE_SOURCE_LOCK_SCHEMA=PASS")
    if args.nos3:
        inspect_nos3(args.nos3, data)
    if args.standalone_crypto_tc:
        inspect_crypto(args.standalone_crypto_tc, "STANDALONE")
    if args.embedded_crypto_tc:
        inspect_crypto(args.embedded_crypto_tc, "NOS3_EMBEDDED")
    print("TTCSIL_F1_SECURITY_AND_COMPATIBILITY=HOLD")
    print("TTCSIL_F2_F3_F4_INTEGRATED_RUNTIME=NOT_EXECUTED")
    print("TTCSIL_CANONICAL_RESEARCH_EXECUTION=PROHIBITED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print("TTCSIL_INTEGRATION_PIN_CHECK=FAIL: " + str(exc), file=sys.stderr)
        sys.exit(2)
