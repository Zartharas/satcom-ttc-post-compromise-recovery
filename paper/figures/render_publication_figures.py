#!/usr/bin/env python3
# Render publication-facing SVG figures using only the Python standard library.

from __future__ import annotations

import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = ROOT / "paper" / "figures"
OUTPUT_DIR = FIGURE_DIR / "rendered"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def svg_text(x, y, text, size=18, anchor="middle", weight="normal"):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">'
        f'{escape(str(text))}</text>'
    )


def box(x, y, w, h, lines):
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10" '
        'fill="none" stroke="black" stroke-width="2"/>'
    ]
    start = y + h / 2 - (len(lines) - 1) * 12
    for index, line in enumerate(lines):
        parts.append(svg_text(x + w / 2, start + index * 24, line, size=17))
    return "\n".join(parts)


def arrow(x1, y1, x2, y2):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        'stroke="black" stroke-width="2" marker-end="url(#arrow)"/>'
    )


def svg_doc(width, height, content):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        '<defs>\n'
        '  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">\n'
        '    <path d="M0,0 L0,6 L9,3 z" fill="black"/>\n'
        '  </marker>\n'
        '</defs>\n'
        '<rect width="100%" height="100%" fill="white"/>\n'
        f'{content}\n'
        '</svg>\n'
    )


def render_figure1():
    width, height = 1400, 760
    p = []
    p.append(svg_text(
        700, 42,
        "Figure 1. Bounded post-compromise TT&C resynchronization architecture",
        size=24, weight="bold"
    ))
    p.append(box(90, 105, 310, 100, ["Recovery authority", "counter + epoch floor"]))
    p.append(box(545, 105, 310, 100, ["Adversary / fault model", "loss - delay - replay - restart"]))
    p.append(box(70, 300, 330, 135, ["Ground endpoint", "candidate / active state"]))
    p.append(box(510, 280, 380, 175, [
        "Intermittent TT&C link",
        "fault-controlled delivery",
        "G->S: PREPARE - COMMIT - TEST",
        "S->G: RESPONSE - CONFIRM - STATUS",
    ]))
    p.append(box(1000, 300, 330, 135, ["Spacecraft endpoint", "candidate / active state"]))
    p.append(box(535, 590, 330, 100, ["Append-only evidence", "+ outcome evaluator"]))

    p.append(arrow(245, 205, 245, 300))
    p.append(svg_text(270, 255, "authorize + monotonic state", size=15, anchor="start"))
    p.append(arrow(700, 205, 700, 280))
    p.append(svg_text(725, 248, "controls delivery", size=15, anchor="start"))
    p.append(arrow(400, 338, 510, 338))
    p.append(arrow(510, 397, 400, 397))
    p.append(arrow(890, 338, 1000, 338))
    p.append(arrow(1000, 397, 890, 397))
    p.append(arrow(255, 435, 600, 590))
    p.append(arrow(1145, 435, 800, 590))

    p.append(svg_text(
        700, 520,
        "Activation: spacecraft on exact COMMIT; ground on exact CONFIRM.",
        size=16, weight="bold"
    ))
    p.append(svg_text(
        700, 548,
        "SUCCESS additionally requires post-convergence command and telemetry verification.",
        size=16
    ))

    (OUTPUT_DIR / "figure-1-architecture.svg").write_text(
        svg_doc(width, height, "\n".join(p)),
        encoding="utf-8",
    )


def render_figure2():
    with (FIGURE_DIR / "figure-2-outcome-distribution-source.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))

    width, height = 1100, 700
    left, right, top, bottom = 110, 55, 95, 130
    plot_w = width - left - right
    plot_h = height - top - bottom
    ymax = 80
    bar_gap = 55
    bar_w = (plot_w - bar_gap * (len(rows) + 1)) / len(rows)

    p = [
        svg_text(
            550, 42,
            "Figure 2. Terminal outcomes in the fixed 100-schedule population",
            size=24, weight="bold"
        ),
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" '
        f'y2="{top + plot_h}" stroke="black" stroke-width="2"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" '
        f'y2="{top + plot_h}" stroke="black" stroke-width="2"/>',
    ]

    for tick in range(0, ymax + 1, 10):
        y = top + plot_h - tick / ymax * plot_h
        p.append(
            f'<line x1="{left - 7}" y1="{y}" x2="{left}" y2="{y}" stroke="black"/>'
        )
        p.append(svg_text(left - 15, y + 6, tick, size=14, anchor="end"))

    for index, row in enumerate(rows):
        count = int(row["count"])
        x = left + bar_gap + index * (bar_w + bar_gap)
        h = count / ymax * plot_h
        y = top + plot_h - h
        p.append(
            f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" '
            'fill="none" stroke="black" stroke-width="2"/>'
        )
        p.append(svg_text(x + bar_w / 2, y - 12, count, size=18, weight="bold"))
        label = row["outcome"].replace("_", " ")
        p.append(svg_text(x + bar_w / 2, top + plot_h + 36, label, size=15))

    p.append(svg_text(38, 350, "Schedules (n = 100)", size=17, anchor="middle"))
    p.append(svg_text(
        550, 655,
        "Descriptive fixed-population counts; not a real-world fault-prevalence or reliability estimate.",
        size=14
    ))

    (OUTPUT_DIR / "figure-2-outcome-distribution.svg").write_text(
        svg_doc(width, height, "\n".join(p)),
        encoding="utf-8",
    )


def render_figure3():
    with (FIGURE_DIR / "figure-3-sensitivity-source.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))

    values = {
        (int(r["max_transmissions"]), int(r["candidate_lifetime_contacts"])):
        int(r["verification_complete_count"])
        for r in rows
    }

    transmissions = [2, 3, 4]
    lifetimes = [2, 3, 4]
    width, height = 920, 690
    left, top = 180, 120
    cell_w, cell_h = 200, 135

    p = [
        svg_text(
            460, 42,
            "Figure 3. Verification-complete executions in the fixed 12-schedule challenge set",
            size=22, weight="bold"
        ),
        svg_text(480, 88, "Maximum transmissions", size=18, weight="bold"),
    ]

    for j, tx in enumerate(transmissions):
        p.append(svg_text(left + j * cell_w + cell_w / 2, top - 18, tx, size=18))

    for i, life in enumerate(lifetimes):
        p.append(svg_text(115, top + i * cell_h + cell_h / 2 + 6, life, size=18))
        for j, tx in enumerate(transmissions):
            x = left + j * cell_w
            y = top + i * cell_h
            p.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
                'fill="none" stroke="black" stroke-width="2"/>'
            )
            value = values[(tx, life)]
            p.append(svg_text(
                x + cell_w / 2, y + cell_h / 2 + 7,
                f"{value}/12", size=27, weight="bold"
            ))

    p.append(svg_text(35, 340, "Candidate lifetime (contacts)", size=17, anchor="start"))
    p.append(svg_text(
        480, 590,
        "No observed lifetime effect over 2-4 contacts; change occurs between transmission budgets 2 and 3.",
        size=14
    ))

    (OUTPUT_DIR / "figure-3-retry-retention-sensitivity.svg").write_text(
        svg_doc(width, height, "\n".join(p)),
        encoding="utf-8",
    )


def main():
    render_figure1()
    render_figure2()
    render_figure3()
    for path in sorted(OUTPUT_DIR.glob("figure-*.svg")):
        print(f"rendered={path.relative_to(ROOT)}")
    print("publication_figures_rendered=3")


if __name__ == "__main__":
    main()
