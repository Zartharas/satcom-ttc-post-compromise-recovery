"""Study G comparison tables and protocol-prediction checks (reads results; no new simulation of T1)."""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

from study_f import baseline_fault_grid as F
from study_g import run_grid as G

ABBR = {"B0": "B0", "B1_LOCAL": "B1L", "B1_DEFERRED": "B1D", "B2": "B2"}


def read(path):
    with open(path) as fh:
        return list(csv.DictReader(fh))


def baseline_exposure():
    """Re-execute Study F cells keeping the sim, to read end-of-run key exposure. Returns (map, reproduced_ok)."""
    out, ok = {}, True
    for c in F.enumerate_cells():
        ref = F.run_cell(c, "T1_BASE")
        sim = F.initial_sim(c.flow, "T1_BASE")
        {"B0": lambda: F._run_b0(sim, c), "B1_LOCAL": lambda: F._run_b1(sim, c, False),
         "B1_DEFERRED": lambda: F._run_b1(sim, c, True), "B2": lambda: F._run_b2(sim, c)}[c.flow]()
        if (sim.evaluate().value, sim.alignment_state()) != (ref["outcome"], ref["alignment"]):
            ok = False
        out[c.cell_id] = (sim.spacecraft.active_key in sim.spacecraft.attacker_known_keys,
                          sim.ground.active_key in sim.ground.attacker_known_keys)
    return out, ok


def main(g_csv, f_csv, out_md):
    g = read(g_csv)
    f = read(f_csv)
    gi = {(r["step"], r["kind"], int(r["lost_transmissions"]), int(r["verification_budget"])): r for r in g}
    fi = {(r["flow"], r["step"], r["kind"], int(r["lost_transmissions"]), int(r["budget"])): r for r in f}
    exp, exp_ok = baseline_exposure()
    checks = []

    def t1(step, kind, lost, vb):
        return gi[(step, kind, lost, vb)]

    def short(r):
        return f'{r["outcome"]} {r["alignment"]}'

    def base_text(step, kind, lost, vb):
        parts = []
        for flow, bstep in G.ROLE_MAP[step]:
            bkind = {"ENDPOINT_RESTART": "ENDPOINT_RESTART", "REORDER": "REORDER"}.get(kind, kind)
            key = (flow, bstep, bkind, lost, vb)
            if key in fi:
                parts.append(f'{ABBR[flow]}:{fi[key]["outcome"]}')
        return "; ".join(parts) if parts else "n/a"

    lines = []
    lines.append("| T1 step | fault | lost | T1 budget 1 (Part I) | T1 budget 3 (Study G) | baselines, budget 1 (Study F) | baselines, budget 3 (Study F) |")
    lines.append("|---|---|---|---|---|---|---|")
    ctrl1, ctrl3 = t1("-", "CONTROL", 0, 1), t1("-", "CONTROL", 0, 3)
    lines.append(f"| - | CONTROL | 0 | {short(ctrl1)} | {short(ctrl3)} | B0,B1L,B1D,B2: SUCCESS | B0,B1L,B1D,B2: SUCCESS |")
    kind_equal = True
    for step in [s.value for s in G.STEPS]:
        for lost in G.LOST_COUNTS:
            a1, a3 = t1(step, "DROP", lost, 1), t1(step, "DROP", lost, 3)
            b1, b3 = t1(step, "CONTACT_CLOSE", lost, 1), t1(step, "CONTACT_CLOSE", lost, 3)
            if short(a1) != short(b1) or short(a3) != short(b3):
                kind_equal = False
            lines.append(f"| {step} | DROP = CONTACT_CLOSE | {lost} | {short(a1)} | {short(a3)} | {base_text(step, 'DROP', lost, 1)} | {base_text(step, 'DROP', lost, 3)} |")
    for step in [s.value for s in G.REORDER_STEPS]:
        fk = base_text("RECOVERY_PREPARE", "REORDER", 0, 1) if step in ("RECOVERY_PREPARE", "RECOVERY_RESPONSE") else "n/a"
        f3 = base_text("RECOVERY_PREPARE", "REORDER", 0, 3) if step in ("RECOVERY_PREPARE", "RECOVERY_RESPONSE") else "n/a"
        lines.append(f"| {step} | REORDER | 0 | {short(t1(step,'REORDER',0,1))} | {short(t1(step,'REORDER',0,3))} | {fk} | {f3} |")
    for step in [s.value for s in G.RESTART_STEPS]:
        lines.append(f"| {step} | ENDPOINT_RESTART | 0 | {short(t1(step,'ENDPOINT_RESTART',0,1))} | {short(t1(step,'ENDPOINT_RESTART',0,3))} | {base_text(step,'ENDPOINT_RESTART',0,1)} | {base_text(step,'ENDPOINT_RESTART',0,3)} |")
    table = "\n".join(lines)

    # outcome counts
    cnt = {a: Counter(r["outcome"] for r in g if r["arm"] == a) for a in ("T1_V1", "T1_V3")}
    fcnt = {b: Counter(r["outcome"] for r in f if r["budget"] == str(b)) for b in (1, 3)}

    # checks P1..P8
    ver = ("TEST_COMMAND", "STATUS_TELEMETRY")
    kinds = ("DROP", "CONTACT_CLOSE")
    def okrow(r, o, al, sec=None, vc=None):
        return r["outcome"] == o and r["alignment"] == al and (sec is None or r["security_state"] == sec) and (vc is None or r["verification_complete"] == vc)
    P1 = all(okrow(t1(s, k, n, 3), "SUCCESS", "SYNC(3)", "SECURE_PROVISIONAL", "True") for s in ver for k in kinds for n in (1, 2))
    P2 = all(okrow(t1(s, k, 3, 3), "INDETERMINATE", "SYNC(3)", "NOT_ESTABLISHED", "False") for s in ver for k in kinds) and \
        okrow(fi[("B2", "STATUS_TELEMETRY", "DROP", 3, 3)], "INDETERMINATE", "SYNC(3)", "NOT_ESTABLISHED")
    P3 = all(t1(s, k, n, 1)["outcome"] == "INDETERMINATE" for s in ver for k in kinds for n in (1, 2, 3))
    fields = [c for c in g[0] if c not in ("cell_id", "arm", "verification_budget")]
    P4 = all(all(t1(s, k, n, 1)[x] == t1(s, k, n, 3)[x] for x in fields)
             for s in [x.value for x in G.STEPS] if s not in ver for k in kinds for n in G.LOST_COUNTS) and \
        all(all(t1(s, k, 0, 1)[x] == t1(s, k, 0, 3)[x] for x in fields) for s, k in
            [(x.value, "REORDER") for x in G.REORDER_STEPS] + [(x.value, "ENDPOINT_RESTART") for x in G.RESTART_STEPS])
    P5 = all((t1(s, k, n, 3)["outcome"] == "SUCCESS") for s in ("RECOVERY_PREPARE","RECOVERY_RESPONSE","RECOVERY_COMMIT","RECOVERY_CONFIRM") for k in kinds for n in (1, 2)) and \
        all(t1(s, k, 3, 3)["outcome"] == "EXPIRED" for s in ("RECOVERY_PREPARE","RECOVERY_RESPONSE","RECOVERY_COMMIT") for k in kinds) and \
        all(t1("RECOVERY_CONFIRM", k, 3, 3)["outcome"] == "SECURE_DEGRADED" for k in kinds) and \
        okrow(t1("RECOVERY_COMMIT", "ENDPOINT_RESTART", 0, 3), "EXPIRED", "G_AHEAD") and \
        okrow(t1("RECOVERY_CONFIRM", "ENDPOINT_RESTART", 0, 3), "SECURE_DEGRADED", "S_AHEAD")
    P6_miss, P7_label = [], []
    for step, pairs in G.ROLE_MAP.items():
        for flow, bstep in pairs:
            for k in kinds:
                for n in G.LOST_COUNTS:
                    tr, br = t1(step, k, n, 3), fi[(flow, bstep, k, n, 3)]
                    ts, bs = tr["outcome"] == "SUCCESS", br["outcome"] == "SUCCESS"
                    if ts != bs:
                        P6_miss.append((step, flow, bstep, k, n))
                    elif tr["outcome"] != br["outcome"] or tr["alignment"] != br["alignment"]:
                        P7_label.append((step, k, n, short(tr), flow, f'{br["outcome"]} {br["alignment"]}'))
    # P8 exposure
    t1_rows = [r for r in g if r["arm"] == "T1_V3"]
    ind_ok = all(r["spacecraft_on_compromised_key"] == "False" and r["ground_on_compromised_key"] == "False" for r in t1_rows if r["outcome"] == "INDETERMINATE")
    other_exposed = all(r["spacecraft_on_compromised_key"] == "True" or r["ground_on_compromised_key"] == "True"
                        for r in t1_rows if r["outcome"] not in ("SUCCESS", "INDETERMINATE"))
    base_nonsucc = [(r["cell_id"], r["outcome"]) for r in f if r["outcome"] != "SUCCESS"]
    base_other_exposed = all(any(exp[c]) for c, o in base_nonsucc if o != "INDETERMINATE") if exp_ok else None
    base_ind = [(c, exp[c]) for c, o in base_nonsucc if o == "INDETERMINATE"] if exp_ok else []
    P8 = ind_ok and other_exposed and bool(base_other_exposed)
    # reorder/restart observed differences
    reorder_diff = [(s, short(t1(s, "REORDER", 0, 3))) for s in ("RECOVERY_PREPARE", "RECOVERY_RESPONSE")]

    md = []
    md.append("## Outcome counts (cells; descriptive only)\n")
    md.append("| arm | " + " | ".join(sorted({o for c in cnt.values() for o in c} | {o for c in fcnt.values() for o in c})) + " | cells |")
    allo = sorted({o for c in cnt.values() for o in c} | {o for c in fcnt.values() for o in c})
    md[-1] = "| arm | " + " | ".join(allo) + " | cells |"
    md.append("|---|" + "---|" * (len(allo) + 1))
    for a, c in cnt.items():
        md.append(f"| {a} | " + " | ".join(str(c.get(o, 0)) for o in allo) + f" | {sum(c.values())} |")
    for b, c in fcnt.items():
        md.append(f"| Study F baselines, budget {b} | " + " | ".join(str(c.get(o, 0)) for o in allo) + f" | {sum(c.values())} |")
    md.append("")
    md.append("## Per-cell comparison\n")
    md.append(table)
    md.append("")
    md.append(f"DROP and CONTACT_CLOSE gave identical T1 outcome and alignment in every cell: {kind_equal}.\n")
    md.append("## Protocol predictions (computed by study_g/compare.py)\n")
    md.append("| prediction | holds |\n|---|---|")
    for name, val in [("P1 budget 3 absorbs 1 or 2 losses at verification steps (8 cells)", P1),
                      ("P2 3 losses at verification steps stay INDETERMINATE and match B2 c3 R3", P2),
                      ("P3 budget 1 reproduces Part I (12 INDETERMINATE)", P3),
                      ("P4 recovery-step, REORDER and RESTART rows identical across budgets", P4),
                      ("P5 recovery-step outcomes as predicted (SUCCESS at 1-2 lost; EXPIRED/SECURE_DEGRADED at 3; restart cells)", P5),
                      (f"P6 SUCCESS/not-SUCCESS partition agrees with every mapped budget-3 baseline row (mismatches: {len(P6_miss)})", not P6_miss),
                      ("P8 exposure pattern (INDETERMINATE not exposed; other non-SUCCESS exposed)", P8)]:
        md.append(f"| {name} | {val} |")
    md.append("")
    md.append(f"P6 mismatches: {P6_miss}\n")
    md.append(f"P7 label-only differences between T1 budget 3 and mapped budget-3 baseline rows (count {len(P7_label)}):\n")
    seen = Counter((a, d, e, g_) for _, _, _, a, d, g_ in [(x[0], x[1], x[2], x[3], x[4], x[5]) for x in P7_label] for e in [0])
    by = defaultdict(set)
    for step, k, n, t, flow, b in P7_label:
        by[(step, n, t)].add(f"{flow}={b}")
    for (step, n, t), v in sorted(by.items()):
        md.append(f"- {step}, lost {n}: T1 {t}; baselines {', '.join(sorted(v))}")
    md.append("")
    md.append(f"Baseline exposure re-execution reproduced Study F outcome and alignment on all rows: {exp_ok}.\n")
    md.append(f"Baseline INDETERMINATE cells and (spacecraft, ground) on compromised key: {sorted(set((v) for _, v in base_ind))}\n")
    md.append("\n".join(["", "## Exposure at end: endpoints still on the attacker-known key (non-SUCCESS cells)\n", "| arm | outcome | cells | spacecraft on compromised key | ground on compromised key |", "|---|---|---|---|---|"]))
    for a in ("T1_V1", "T1_V3"):
        grp = defaultdict(list)
        for r in g:
            if r["arm"] == a and r["outcome"] != "SUCCESS":
                grp[r["outcome"]].append(r)
        for o, rs in sorted(grp.items()):
            md.append(f"| {a} | {o} | {len(rs)} | {sum(r['spacecraft_on_compromised_key']=='True' for r in rs)} | {sum(r['ground_on_compromised_key']=='True' for r in rs)} |")
    for b in (1, 3):
        grp = defaultdict(list)
        for r in f:
            if r["budget"] == str(b) and r["outcome"] != "SUCCESS":
                grp[r["outcome"]].append(r)
        for o, rs in sorted(grp.items()):
            sc = sum(exp[r["cell_id"]][0] for r in rs)
            gr = sum(exp[r["cell_id"]][1] for r in rs)
            md.append(f"| Study F budget {b} | {o} | {len(rs)} | {sc} | {gr} |")
    Path(out_md).write_text("\n".join(md) + "\n")
    print("\n".join(md[:3]))
    return dict(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5, P6_miss=P6_miss, P8=P8, exp_ok=exp_ok, kind_equal=kind_equal)


if __name__ == "__main__":
    print(main(sys.argv[1], sys.argv[2], sys.argv[3]))
