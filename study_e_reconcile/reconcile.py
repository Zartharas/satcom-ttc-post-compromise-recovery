"""Reconcile Part I deterministic T1 cells with Part II (study_e) at shared points.
Frozen Part II code is only imported, never modified. Deterministic loss is expressed by driving the frozen
independent path simulator (study_e.sim.run_path) with a forced Bernoulli outcome per transmission; p=0/p=1 and
r=1 points are also computed directly with the frozen exact DP (study_e.model.exact_distribution).
Usage: python3 reconcile.py <out_csv>"""
import csv, json, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "study_e"))
from study_e.params import Params
from study_e.model import exact_distribution, outcome_probs
from study_e import sim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
P1 = json.load(open(os.path.join(HERE, "part1_raw_compact.json")))
VOCAB = {"SUCCESS": "SUCCESS", "INDETERMINATE": "INDETERMINATE", "EXPIRED": "EXPIRED_OLD",
         "SECURE_DEGRADED": "DIVERGED_S_AHEAD"}

# ---- Part I table-2 vs raw JSON consistency ----
t2 = {r["schedule_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "paper/tables/table-2-deterministic-t1.csv")))}
assert set(t2) == set(P1), "schedule id sets differ"
for k, r in t2.items():
    assert (r["outcome"], r["alignment"]) == (P1[k][0], P1[k][1]), k
assert sum(1 for r in t2.values() if r["schedule_class"] == "CANONICAL_CELL") == 31


def forced(params, lost):
    """Deterministic replay: transmission i (1-based) is lost iff i in lost. Returns (outcome, contact, tx_used)."""
    gen = sim.run_path(params)
    tx = 0
    try:
        next(gen)
    except StopIteration as e:
        return e.value[0], e.value[1], 0
    while True:
        tx += 1
        try:
            gen.send(tx not in lost)
        except StopIteration as e:
            return e.value[0], e.value[1], tx


def direct(K, B, L, p, r, persist, act):
    d = exact_distribution(Params(p=F(p), K=K, B=B, L=L, r=F(r), persist=persist, activation=act), exact=True)
    o = outcome_probs(d)
    o = {k: v for k, v in o.items() if v != 0}
    return o, d


# ---- internal validity of the replay approach: frozen DP == frozen enumerator at p=1/3 on every config used ----
def dp_equals_enum(K, B, L, r, persist, act):
    pr = Params(p=F(1, 3), K=K, B=B, L=L, r=F(r), persist=persist, activation=act)
    a = exact_distribution(pr, exact=True)
    b = sim.enumerate_distribution(pr)
    a = {k: v for k, v in a.items() if v != 0}
    b = {k: v for k, v in b.items() if v != 0}
    return a == b


rows = []
checked_cfgs = set()


def add(rid, sched, cfg, how, outcome, contacts, txu, note, cls):
    K, B, L, r, persist, act = cfg
    if cfg not in checked_cfgs:
        assert dp_equals_enum(*cfg), cfg
        checked_cfgs.add(cfg)
    p1 = P1[sched] if sched in P1 else None
    p1o = VOCAB.get(p1[0], p1[0]) if p1 else ""
    # Part I raw is keyed by schedule id
    ag = "YES" if outcome == p1o else "NO"
    if cls == "NO_COUNTERPART":
        ag = ("VACUOUS_YES" if outcome == p1o and sched.split("-")[2] in ("DLY", "DUP", "REO", "SCTR", "SRPL") else "NA_DIFFERENT_MECHANISM")
    if cls == "VACUOUS_AGREEMENT":
        ag = "VACUOUS_YES"
    t = t2[sched]
    rows.append(dict(row_id=rid, part1_schedule=sched, part1_fault=t["fault_kind_or_control"], part1_phase=t["phase_or_control"],
                     part1_outcome=p1[0], part1_alignment=p1[1], part1_tx=p1[2], part1_contacts=p1[3],
                     part1_as_part2_vocab=p1o, comparability=cls, K=K, B=B, L=L, r=str(r), persist=persist, activation=act,
                     part2_input=how, part2_outcome=outcome, part2_end_contact=contacts, part2_tx_used=txu,
                     agree=ag, note=note))


def forced_row(rid, sched, cfg, lost, note, cls, label=None):
    K, B, L, r, persist, act = cfg
    pr = Params(p=F(1, 2), K=K, B=B, L=L, r=F(r), persist=persist, activation=act)
    o, c, tx = forced(pr, set(lost))
    # necessary-condition check against the frozen exact DP: the forced path is one of the DP's paths, so its
    # probability (at p=1/3) cannot exceed the DP mass of the same (outcome, end contact).
    p3 = F(1, 3)
    w = p3 ** len(set(lost)) * (1 - p3) ** (tx - len(set(lost)))
    dp = exact_distribution(Params(p=p3, K=K, B=B, L=L, r=F(r), persist=persist, activation=act), exact=True)
    assert dp.get((o, c), 0) >= w, (rid, o, c)
    add(rid, sched, cfg, label or ("forced loss of tx " + ",".join(map(str, sorted(lost))) if lost else "no loss"), o, c, tx, note, cls)


def direct_row(rid, sched, cfg, p, note, cls):
    K, B, L, r, persist, act = cfg
    o, d = direct(K, B, L, p, r, persist, act)
    assert len(o) == 1 and sum(o.values()) == 1, o  # deterministic point: single outcome with mass 1
    out = next(iter(o))
    c = {t for (oo, t) in d if oo == out and d[(oo, t)] != 0}
    add(rid, sched, cfg, "frozen DP p=%s r=%s mass=1" % (p, r), out, "/".join(map(str, sorted(c))), "", note, cls)


G = (3, 8, 3, 0, "commit", "local")      # shared grid point K=3,B=8,L=3 (the headline point of the pre-registration); Part I = local activation
MSG = ["PREP", "RESP", "COMM", "CONF", "TEST", "STAT"]

# control
direct_row("C0", "DET-000-NO-FAULT", G, 0, "p=0: SUCCESS with mass 1 (also holds for every persistence/activation level).", "AGREE")
direct_row("C0b", "DET-000-NO-FAULT", (6, 6, 1, 0, "commit", "local"), 0, "same, single-contact K=6,B=6,L=1.", "AGREE")

# single DROP, one transmission lost, retry available
for i, m in enumerate(MSG[:4], start=1):
    s = "DET-CELL-DROP-" + m
    forced_row("D%d" % i, s, G, [i], "Part II retransmits the lost message itself (7 tx); Part I re-sends the initiating request (%d tx). Outcome agrees, transmission count does not necessarily." % P1[s][2], "AGREE")
    forced_row("D%db" % i, s, (3, 6, 3, 0, "commit", "local"), [i], "Sensitivity B=6: Part II needs 7 tx, a global cap of 6 ends the attempt at step 5; Part I has no global cap (per-phase cap 3).", "SENSITIVITY")
for i, m in ((5, "TEST"), (6, "STAT")):
    s = "DET-CELL-DROP-" + m
    forced_row("D%d" % i, s, G, [i], "Part II retries the lost verification message while budget remains; Part I never retries verification, so Part I stays INDETERMINATE.", "AGREE_ONLY_AT_TUNED_PARAMS")
    forced_row("D%dt" % i, s, (3, i, 3, 0, "commit", "local"), [i], "Tuned B=%d (no spare transmission after the loss) reproduces Part I; agreement encodes 'verification is not retried'." % i, "AGREE_ONLY_AT_TUNED_PARAMS")

# CONTACT_CLOSE: boundary after the lost transmission needs K = position of the lost message
for i, m in enumerate(MSG, start=1):
    s = "DET-CELL-CLOSE-" + m
    for L in (3, 8):
        forced_row("X%d_L%d" % (i, L), s, (i, 8, L, 0, "commit", "local"), [i],
                   "K=%d puts the contact boundary right after the lost tx; Part II slots/contact are finite, Part I contacts hold unlimited messages%s." % (
                       i, "; lifetime L=3 equals Part I candidate lifetime" if L == 3 else "; L=8 removes the lifetime limit"),
                   "AGREE_ONLY_AT_TUNED_PARAMS")
forced_row("X5_L1", "DET-CELL-CLOSE-TEST", (5, 8, 1, 0, "commit", "local"), [5], "L=1 makes the close end the lifetime (not Part I's lifetime of 3): reproduces INDETERMINATE only by shrinking L.", "AGREE_ONLY_AT_TUNED_PARAMS")
forced_row("X6_L1", "DET-CELL-CLOSE-STAT", (6, 8, 1, 0, "commit", "local"), [6], "same with K=6, L=1.", "AGREE_ONLY_AT_TUNED_PARAMS")

# retry exhaustion: DROP; B tuned so that 3 consecutive losses of message m exhaust the budget
base = {"PREP": 0, "RESP": 1, "COMM": 2, "CONF": 3}
for m, nb in base.items():
    s = "DET-EXHAUST-DROP-" + m
    lost = [nb + 1, nb + 2, nb + 3]
    forced_row("E_%s_tight" % m, s, (3, nb + 3, 3, 0, "commit", "local"), lost,
               "B=%d (= %d delivered + 3 lost) exhausts exactly at the third loss; Part I cap is per phase loop, Part II cap is global." % (nb + 3, nb), "AGREE_ONLY_AT_TUNED_PARAMS")
    forced_row("E_%s_B12" % m, s, (3, 12, 3, 0, "commit", "local"), lost, "Same three losses with grid budget B=12, L=3: global budget not exhausted (9 tx needed, 9 slots available), Part II completes. Part I's per-phase cap of 3 is exhausted regardless.", "SENSITIVITY")
direct_row("E_PREP_p1", "DET-EXHAUST-DROP-PREP", (3, 3, 3, 0, "commit", "local"), 1, "p=1, B=3 (frozen DP, mass 1): total loss, EXPIRED_OLD.", "AGREE_ONLY_AT_TUNED_PARAMS")
forced_row("E_CONF_gated", "DET-EXHAUST-DROP-CONF", (3, 6, 3, 0, "commit", "gated"), [4, 5, 6],
           "Gated activation: spacecraft not yet active at step 3, so Part II reports EXPIRED_OLD; Part I activates on COMMIT (local).", "AGREE_ONLY_AT_TUNED_PARAMS")

# EXHAUST-CLOSE: boundary after every lost tx -> only K=1 expresses it; outcome then independent of the losses
for m, nb in base.items():
    s = "DET-EXHAUST-CLOSE-" + m
    forced_row("EC_%s" % m, s, (1, 12, 3, 0, "commit", "local"), [nb + 1, nb + 2, nb + 3],
               "K=1,L=3: agreement is VACUOUS, the outcome is the same with no loss at all (see row EC0).", "VACUOUS_AGREEMENT")
forced_row("EC0", "DET-EXHAUST-CLOSE-CONF", (1, 12, 3, 0, "commit", "local"), [],
           "Control for the vacuity: p=0, K=1, L=3 already yields the same outcome as the exhaustion cell.", "VACUOUS_AGREEMENT")

# ENDPOINT_RESTART (spacecraft, volatile pending, counters/epoch retained)
for pers in ("commit", "volatile", "journal"):
    direct_row("R_COMM_%s" % pers, "DET-CELL-RST-COMM", (2, 8, 2, 1, pers, "local"), 0,
               {"commit": "p=0, r=1, one boundary after m2 (K=2,L=2): candidate lost, handshake restarts, lifetime ends at step 2. Matches Part I 'pending lost, epoch/counters retained'.",
                "volatile": "volatile also loses nothing more at step 2 (no activation yet): same outcome.",
                "journal": "journal keeps the candidate (no Part I analogue: Part I has no durable pending state): different outcome by design."}[pers],
               "AGREE" if pers != "journal" else "NO_COUNTERPART")
for pers in ("commit", "volatile", "journal"):
    direct_row("R_CONF_%s" % pers, "DET-CELL-RST-CONF", (3, 8, 2, 1, pers, "local"), 0,
               {"commit": "Part II restarts the SPACECRAFT at the step-3 boundary; activation is persisted so it continues to SUCCESS. Part I restarts the GROUND (no counterpart).",
                "volatile": "Outcome class equals Part I (S_AHEAD) but by a different mechanism (spacecraft restart, lifetime end), not a reconciliation.",
                "journal": "journal continues to SUCCESS."}[pers], "NO_COUNTERPART")

# no-counterpart families: only p=0 consistency
nocp = {"DLY": "Part II has no delay event; p=0 SUCCESS is consistent but vacuous.",
        "DUP": "Part II has no duplicate delivery or message-ID rejection; p=0 SUCCESS is consistent but vacuous.",
        "REO": "Part II has no reordering (messages are strictly sequential); p=0 SUCCESS is consistent but vacuous.",
        "SCTR": "Part II has no counters/authentication state; p=0 SUCCESS is consistent but vacuous.",
        "SRPL": "Part II has no replay/stale-state rejection; p=0 SUCCESS is consistent but vacuous."}
for s in sorted(P1):
    for k, n in nocp.items():
        if s.startswith("DET-CELL-" + k + "-"):
            direct_row("N_" + s[9:], s, G, 0, n, "NO_COUNTERPART")

with open(sys.argv[1], "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", len(checked_cfgs), "configs with DP==enumerator at p=1/3")
