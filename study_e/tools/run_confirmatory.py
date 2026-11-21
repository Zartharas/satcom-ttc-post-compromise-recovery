"""Runs the Study E confirmatory analysis. Usage (from the study_e folder):
   python3 -I tools/run_confirmatory.py --grid frozen --out OUTDIR      (full run; requires the git guard below)
   python3 -I tools/run_confirmatory.py --grid tiny --out OUTDIR        (smoke test only; writes NOTHING that may be called a result)
Full-run guard: HEAD must contain tag study-e-prereg-v1 as an ancestor, tag study-e-analysis-script-v1 must point at HEAD, and
study_e/ and docs/study_e/ must have no uncommitted changes. Refuses otherwise."""
import argparse, json, os, platform, subprocess, sys, time
sys.path.insert(0, ".")
from study_e import confirm as C

PREREG_TAG, SCRIPT_TAG = "study-e-prereg-v1", "study-e-analysis-script-v1"


def git(*a):
    return subprocess.run(("git",) + a, capture_output=True, text=True, check=True).stdout.strip()


def guard():
    try:
        head = git("rev-parse", "HEAD")
        if git("rev-list", "-n1", SCRIPT_TAG) != head:
            raise SystemExit("refused: tag %s does not point at HEAD" % SCRIPT_TAG)
        subprocess.run(["git", "merge-base", "--is-ancestor", PREREG_TAG, "HEAD"], check=True)
        if git("status", "--porcelain", "--", "study_e", "docs/study_e"):
            raise SystemExit("refused: uncommitted changes under study_e/ or docs/study_e/")
        return {"head": head, "prereg_commit": git("rev-list", "-n1", PREREG_TAG), "script_tag_commit": head}
    except (subprocess.CalledProcessError, FileNotFoundError) as ex:
        raise SystemExit("refused: git guard failed (%s)" % ex)


def md(res, meta):
    L = ["# Study E confirmatory results" + (" (SMOKE TEST: NOT A RESULT)" if meta["grid"] != "frozen" else ""), "",
         "Run meta: %s" % json.dumps(meta, sort_keys=True), "", "Table SHA-256 (exchange + composite, exact): %s" % res["table_sha256"], ""]
    for k in ("H-E2a", "H-E2b", "H-E2c", "H-E3", "H-E4", "H-E5", "exploratory_post_hoc"):
        L += ["## " + k, "```json", json.dumps(res[k], indent=1, default=str), "```", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", choices=("frozen", "tiny"), required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    meta = {"grid": a.grid, "python": platform.python_version(), "platform": platform.platform()}
    if a.grid == "frozen":
        meta.update(guard())
        grid = C.FROZEN_GRID
    else:
        grid = dict(p=[C.F(1, 5), C.F(1, 2)], K=[2, 3], B=[4, 6], L=[1, 2], r=[C.F(0), C.F(1, 10)], persist=list(C.PERSIST_ORDER),
                    activation=["local", "gated"], H=[4, 8], policy=list(C.POLICIES), detect=[1, 3])
    t0 = time.time()
    res = C.run_all(grid)
    meta["seconds"] = round(time.time() - t0, 1)
    os.makedirs(a.out, exist_ok=True)
    tag = "" if a.grid == "frozen" else "_SMOKE"
    with open(os.path.join(a.out, "confirmatory_results%s.json" % tag), "w") as fh:
        json.dump({"meta": meta, "results": res}, fh, indent=1, sort_keys=True, default=str)
    with open(os.path.join(a.out, "CONFIRMATORY_RESULTS%s.md" % tag), "w") as fh:
        fh.write(md(res, meta))
    print("wrote", a.out, "seconds", meta["seconds"])


if __name__ == "__main__":
    main()
