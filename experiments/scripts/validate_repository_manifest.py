#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "artifacts" / "manifests" / "repository-v0.1.1.sha256"


def tracked_paths() -> list[Path]:
    raw = subprocess.check_output(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
    ).decode("utf-8")
    paths = []
    for name in sorted(filter(None, raw.split("\0"))):
        path = ROOT / name
        if path == MANIFEST:
            continue
        if not path.is_file():
            raise SystemExit(f"Tracked path is missing or not a file: {name}")
        paths.append(path)
    return paths


def expected_text() -> str:
    lines = []
    for path in tracked_paths():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{digest}  {relative}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or refresh the tracked-file manifest.")
    parser.add_argument("--write", action="store_true", help="Replace the manifest with expected content.")
    parser.add_argument("--print", dest="print_only", action="store_true", help="Print expected content.")
    args = parser.parse_args()

    expected = expected_text()
    if args.print_only:
        print(expected, end="")
        return
    if args.write:
        MANIFEST.write_text(expected, encoding="utf-8")
        print(f"Updated {MANIFEST.relative_to(ROOT)} with {len(expected.splitlines())} entries.")
        return

    actual = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else ""
    if actual != expected:
        print("Tracked-file manifest mismatch.")
        print("--- expected manifest ---")
        print(expected, end="")
        print("--- end expected manifest ---")
        raise SystemExit(1)

    print(f"Tracked-file manifest valid: {len(expected.splitlines())} entries.")


if __name__ == "__main__":
    main()
