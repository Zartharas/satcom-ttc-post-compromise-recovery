#!/usr/bin/env python3
"""Read-only post hoc reanalysis of retained Part I raw records (Studies B and C).

Splits UNSAFE end states into (a) no endpoint ever activated a new key and
(b) exactly one endpoint activated, and counts the contacts that elapsed while
each endpoint still held the seeded compromised key. Descriptive only. Frozen
files are read, never written. The run length is a schedule parameter, so
contacts for endpoints that never activate are lower bounds.
"""
import argparse
import collections
import json
import pathlib
import sys

STUDIES = ("study-b-deterministic-t1", "study-c-mixed-fault-t1")


def contacts_before(log, wanted):
    n = 0
    for e in log:
        if e["event"] == "phase07_contact_advanced":
            n += 1
        if e["event"] == wanted:
            return n
    return None


def classify(rec):
    r = rec["result"]
    m = r["metrics"]
    log = r["event_log"]
    contacts_total = sum(1 for e in log if e["event"] == "phase07_contact_advanced")
    g = contacts_before(log, "t1_ground_activated")
    s = contacts_before(log, "t1_spacecraft_activated")
    if g is None and s is None:
        kind = "no_endpoint_activated"
    elif g is not None and s is not None:
        kind = "both_activated"
    elif s is not None:
        kind = "spacecraft_only_activated"
    else:
        kind = "ground_only_activated"
    return {
        "schedule_id": rec["schedule_id"],
        "outcome": m["outcome"],
        "alignment": m["alignment"],
        "security_state": m["security_state"],
        "kind": kind,
        "run_contacts_advanced": contacts_total,
        "contacts_spacecraft_held_old_key": s if s is not None else contacts_total,
        "spacecraft_never_activated": s is None,
        "contacts_ground_held_old_key": g if g is not None else contacts_total,
        "ground_never_activated": g is None,
        "divergent_contact_windows": m["divergent_contact_windows"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"note": "post hoc descriptive reanalysis of retained Part I records; frozen files read only", "studies": {}}
    for st in STUDIES:
        rows = [classify(x) for x in json.load(open(pathlib.Path(a.raw_dir) / f"{st}.json"))]
        unsafe = [x for x in rows if x["security_state"] == "UNSAFE"]
        out["studies"][st] = {
            "schedules": len(rows),
            "unsafe": len(unsafe),
            "unsafe_by_kind": dict(collections.Counter(x["kind"] for x in unsafe)),
            "unsafe_by_alignment": dict(collections.Counter(x["alignment"][:7] for x in unsafe)),
            "unsafe_by_outcome": dict(collections.Counter(x["outcome"] for x in unsafe)),
            "unsafe_rows": unsafe,
        }
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for st, v in out["studies"].items():
        print(st, v["schedules"], "unsafe", v["unsafe"], v["unsafe_by_kind"], v["unsafe_by_alignment"], v["unsafe_by_outcome"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
