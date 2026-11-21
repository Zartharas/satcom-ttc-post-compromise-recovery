from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

from study_f.baseline_fault_grid import not_defined_records, plan_sha256, run_grid, write_csv


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return ""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = run_grid("T1_BASE")
    results = out / "study_f_results.csv"
    write_csv(rows, str(results))
    nd = not_defined_records()
    nd_path = out / "study_f_not_defined.csv"
    write_csv(nd, str(nd_path))
    manifest = {
        "plan_sha256": plan_sha256(),
        "cell_rows": len(rows),
        "not_defined_rows": len(nd),
        "results_csv_sha256": _sha256(results),
        "not_defined_csv_sha256": _sha256(nd_path),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_tag_study_f_plan_v1": _git("rev-list", "-n", "1", "study-f-plan-v1"),
    }
    (out / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
