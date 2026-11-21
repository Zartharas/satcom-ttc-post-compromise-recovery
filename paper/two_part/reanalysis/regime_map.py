"""Regime map of the frozen Part II single-attempt model (exact outcome masses).
Illustrative slice, not a measurement and not part of the pre-registered confirmatory tests.
Uses study_e (read-only). Run: PYTHONPATH=../../../study_e python3 regime_map.py <out_prefix>"""
import sys
from study_e.params import Params
from study_e.model import exact_distribution, outcome_probs

B, L = 8, 3
PS = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
KS = [1, 2, 3, 4, 5, 6]
PANELS = [
    ("(a) P(SUCCESS), local activation, journaled, r = 0", dict(persist="journal", activation="local", r=0.0), ("SUCCESS",)),
    ("(b) P(INDETERMINATE), same settings", dict(persist="journal", activation="local", r=0.0), ("INDETERMINATE",)),
    ("(c) P(endpoints divergent), local, volatile, r = 0.1", dict(persist="volatile", activation="local", r=0.1), ("DIVERGED_S_AHEAD", "DIVERGED_G_AHEAD")),
    ("(d) P(endpoints divergent), gated, volatile, r = 0.1", dict(persist="volatile", activation="gated", r=0.1), ("DIVERGED_S_AHEAD", "DIVERGED_G_AHEAD")),
]

def grid(kw, outs):
    rows = []
    for K in KS:
        row = []
        for p in PS:
            d = outcome_probs(exact_distribution(Params(p=p, K=K, B=B, L=L, **kw)))
            row.append(sum(d.get(o, 0.0) for o in outs))
        rows.append(row)
    return rows

if __name__ == "__main__":
    import csv, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    prefix = sys.argv[1]
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 5.6), constrained_layout=True)
    with open(prefix + ".csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["panel", "K", "p", "probability"])
        for ax, (title, kw, outs) in zip(axes.flat, PANELS):
            g = grid(kw, outs)
            for i, K in enumerate(KS):
                for j, p in enumerate(PS):
                    w.writerow([title[:3], K, p, f"{g[i][j]:.6f}"])
            im = ax.imshow(g, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="viridis")
            ax.set_xticks(range(len(PS))); ax.set_xticklabels([f"{p:g}" for p in PS], fontsize=7)
            ax.set_yticks(range(len(KS))); ax.set_yticklabels(KS, fontsize=7)
            ax.set_xlabel("per-message loss p", fontsize=8); ax.set_ylabel("slots per contact K", fontsize=8)
            ax.set_title(title, fontsize=8)
            for i in range(len(KS)):
                for j in range(len(PS)):
                    ax.text(j, i, f"{g[i][j]:.2f}"[1:] if 0 < g[i][j] < 1 else f"{g[i][j]:.0f}", ha="center", va="center", fontsize=5.5, color="white" if g[i][j] < 0.6 else "black")
    fig.colorbar(im, ax=axes, shrink=0.8, label="probability")
    fig.suptitle(f"Part II model regime map (B = {B} transmissions, lifetime L = {L} contacts): exact masses, illustrative slice", fontsize=8.5)
    fig.savefig(prefix + ".pdf"); fig.savefig(prefix + ".png", dpi=200)
