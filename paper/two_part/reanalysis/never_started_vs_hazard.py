import csv, glob, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = sorted(glob.glob(str(ROOT / "results/raw/paper-final/*/raw")))[-1]
OUT = Path(__file__).resolve().parent


def classify(row):
    r = row["result"]
    m = r["metrics"]
    ev = [e["event"] for e in r["event_log"]]
    sc_rot = "t1_spacecraft_activated" in ev
    gr_rot = "t1_ground_activated" in ev
    prep_acc = "t1_prepare_accepted" in ev
    out, sec, align = m["outcome"], m["security_state"], m["alignment"]
    if out == "SUCCESS":
        cls = "recovered"
    elif out == "INDETERMINATE":
        cls = "rotated_unverified"
    elif sec == "UNSAFE" and not sc_rot and not gr_rot:
        cls = "no_rotation_at_either_endpoint_never_activated" if prep_acc else "no_rotation_recovery_never_reached_spacecraft"
    elif sec == "UNSAFE" and sc_rot and not gr_rot:
        cls = "spacecraft_rotated_ground_locked_out"
    else:
        cls = "other"
    exposed = 0 if sc_rot else m["divergent_contact_windows"]
    return {
        "schedule_id": row["schedule_id"],
        "outcome": out,
        "alignment": align,
        "security_state": sec,
        "prepare_accepted": prep_acc,
        "spacecraft_rotated": sc_rot,
        "ground_rotated": gr_rot,
        "class": cls,
        "divergent_contact_windows": m["divergent_contact_windows"],
        "spacecraft_rotated_flag_zero_exposure": sc_rot,
        "contacts_spacecraft_still_on_start_key": exposed,
    }


def run(name, fname):
    rows = json.load(open(Path(RAW) / fname))
    out = [classify(r) for r in rows]
    with open(OUT / f"{name}_classes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    return out


if __name__ == "__main__":
    lines = ["# Never-started versus new-hazard split (read-only reanalysis of retained raw JSON)", ""]
    for name, fname in (("study_b", "study-b-deterministic-t1.json"), ("study_c", "study-c-mixed-fault-t1.json")):
        res = run(name, fname)
        unsafe = [x for x in res if x["security_state"] == "UNSAFE"]
        c = Counter(x["class"] for x in unsafe)
        lines += [f"## {name}: {len(res)} schedules, {len(unsafe)} UNSAFE", ""]
        for k, v in sorted(c.items()):
            lines.append(f"- {k}: {v}")
        lines.append("")
        by = Counter((x["class"], x["outcome"], x["alignment"]) for x in unsafe)
        for k, v in sorted(by.items()):
            lines.append(f"  - {k}: {v}")
        lines.append("")
    (OUT / "never_started_vs_hazard.md").write_text("\n".join(lines))
    print("\n".join(lines))
