#!/usr/bin/env python3
"""Compare an implementer's Study B CSV with paper/tables/table-2-deterministic-t1.csv (author-side only)."""
import csv, json, sys, os
REF = os.path.join(os.path.dirname(__file__), "..", "..", "paper", "tables", "table-2-deterministic-t1.csv")
PRIMARY = ["outcome", "alignment", "security_state", "availability_state", "verification_complete"]
def load(p):
    with open(p, newline="") as f:
        return {r["schedule_id"]: r for r in csv.DictReader(f)}
def norm(v): return str(v).strip().lower() if v is not None else ""
def rej(r):
    try: return json.loads(r["rejection_evidence"])
    except Exception: return None
def main():
    if len(sys.argv) != 2: sys.exit("usage: compare_study_b.py implementer.csv")
    ref, imp = load(REF), load(sys.argv[1])
    ids = sorted(ref)
    missing = [i for i in ids if i not in imp]; extra = [i for i in imp if i not in ref]
    print(f"reference schedules {len(ref)}, implementer {len(imp)}, missing {len(missing)}, extra {len(extra)}")
    for i in missing: print("  missing:", i)
    for i in extra: print("  extra:", i)
    common = [i for i in ids if i in imp]
    canon = [i for i in common if ref[i]["schedule_class"] == "CANONICAL_CELL"]
    def agree(field, group):
        return sum(norm(ref[i][field]) == norm(imp[i].get(field)) for i in group)
    print(f"\n{'field':26} {'all ('+str(len(common))+')':>10} {'canonical ('+str(len(canon))+')':>16}")
    for f in PRIMARY:
        print(f"{f:26} {agree(f, common):>10} {agree(f, canon):>16}")
    both = lambda g: sum(all(norm(ref[i][f]) == norm(imp[i].get(f)) for f in PRIMARY) for i in g)
    print(f"{'all five primary':26} {both(common):>10} {both(canon):>16}")
    rj = lambda g: sum(rej(ref[i]) == rej(imp[i]) for i in g)
    print(f"{'rejection triple':26} {rj(common):>10} {rj(canon):>16}")
    print("\nDisagreements:")
    for i in common:
        bad = [f for f in PRIMARY if norm(ref[i][f]) != norm(imp[i].get(f))]
        rb = rej(ref[i]) != rej(imp[i])
        if bad or rb:
            print(f"  {i}: " + ", ".join(f"{f} ref={ref[i][f]} impl={imp[i].get(f)}" for f in bad) + (f"; rejection ref={rej(ref[i])} impl={rej(imp[i])}" if rb else ""))
if __name__ == "__main__":
    main()
