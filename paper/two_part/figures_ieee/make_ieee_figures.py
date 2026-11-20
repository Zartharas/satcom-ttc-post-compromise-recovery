#!/usr/bin/env python3
"""Build IEEE TAES-ready copies of Figures 1-3 for the two-part paper.

Reads the Part I source CSVs READ-ONLY (paper/figures/*.csv). Does not touch, import, or
regenerate any Part I file. Writes only into this folder (paper/two_part/figures_ieee/).

What differs from the Part I figures (paper/figures/rendered/*.svg, checksum-locked):
  * physical size is fixed to the IEEE template widths (7.16 in page-wide, 3.5 in column);
    every length below is in points, so font sizes are the final printed sizes (>= 8 pt);
  * no "Figure N." title inside the image (IEEE: captions are not part of the figure);
    the two in-figure descriptive notes move into the caption (see build_two_part_manuscript.py);
  * output is vector PDF (an IEEE-accepted format) plus 600 dpi PNG line art and the SVG source.
The plotted values are exactly the CSV values; the layout is redrawn, not edited.

Optional dependency: cairosvg (for PDF/PNG). Without it only the SVG files are written.
"""
from __future__ import annotations

import csv
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / "paper" / "figures"

FONT = "Arial, Liberation Sans, Helvetica, sans-serif"
PAGE_W = 7.16 * 72  # 515.52 pt
COL_W = 3.5 * 72    # 252 pt
MIN_FONT = 8.0

# ---- optional text measurement (overflow guard); skipped when Pillow/Liberation are absent
try:
    from PIL import ImageFont
    _REG = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
    _BLD = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 100)
except Exception:  # pragma: no cover
    _REG = _BLD = None

_checks = []
_min_font_seen = [99.0]


def text_width(s: str, size: float, bold: bool) -> float | None:
    f = _BLD if bold else _REG
    return None if f is None else f.getlength(s) * size / 100.0


def txt(x, y, s, size=8.0, anchor="middle", bold=False, max_w=None):
    assert size >= MIN_FONT, f"font {size} < {MIN_FONT}"
    _min_font_seen[0] = min(_min_font_seen[0], size)
    w = text_width(str(s), size, bold)
    if max_w is not None and w is not None:
        _checks.append((str(s), w, max_w))
        assert w <= max_w, f"text overflows ({w:.1f} > {max_w:.1f}): {s}"
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
            f'text-anchor="{anchor}" font-weight="{"bold" if bold else "normal"}">{escape(str(s))}</text>')


def box(x, y, w, h, lines, size=8.0, lead=10.5):
    out = [f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="4" ry="4" '
           'fill="none" stroke="black" stroke-width="0.9"/>']
    top = y + h / 2 - (len(lines) - 1) * lead / 2 + size * 0.35
    for i, line in enumerate(lines):
        out.append(txt(x + w / 2, top + i * lead, line, size=size, max_w=w - 8))
    return "\n".join(out)


def arrow(x1, y1, x2, y2):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            'stroke="black" stroke-width="0.9" marker-end="url(#arrow)"/>')


def doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.2f}pt" height="{h:.2f}pt" '
            f'viewBox="0 0 {w:.2f} {h:.2f}">\n<defs>\n'
            '  <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="2" orient="auto" markerUnits="userSpaceOnUse">\n'
            '    <path d="M0,0 L0,4 L5.5,2 z" fill="black"/>\n  </marker>\n</defs>\n'
            '<rect width="100%" height="100%" fill="white"/>\n' + body + "\n</svg>\n")


def fig1():
    W, H = PAGE_W, 268
    gx, gw = 10, 122          # ground box
    lx, lw = 158, 199.52      # link box
    sx, sw = 383.52, 122      # spacecraft box
    p = []
    # top row
    p.append(box(gx, 8, gw, 38, ["Recovery authority", "counter + epoch floor"]))
    p.append(box(173, 8, 170, 38, ["Adversary / fault model", "loss - delay - replay - restart"]))
    # middle row
    p.append(box(gx, 100, gw, 46, ["Ground endpoint", "candidate / active state"]))
    p.append(box(lx, 86, lw, 74, ["Intermittent TT&C link", "fault-controlled delivery",
                                  "G->S: PREPARE - COMMIT - TEST", "S->G: RESPONSE - CONFIRM - STATUS"]))
    p.append(box(sx, 100, sw, 46, ["Spacecraft endpoint", "candidate / active state"]))
    # bottom
    p.append(box(183, 184, 150, 38, ["Append-only evidence", "+ outcome evaluator"]))
    # arrows
    p.append(arrow(71, 46, 71, 100))
    p.append(txt(77, 76, "authorize + monotonic state", anchor="start", max_w=80 + 100))
    p.append(arrow(258, 46, 258, 86))
    p.append(txt(264, 70, "controls delivery", anchor="start", max_w=100))
    p.append(arrow(gx + gw, 113, lx, 113))
    p.append(arrow(lx, 133, gx + gw, 133))
    p.append(arrow(lx + lw, 113, sx, 113))
    p.append(arrow(sx, 133, lx + lw, 133))
    p.append(arrow(85, 146, 205, 184))
    p.append(arrow(437, 146, 311, 184))
    # annotations (part of the diagram's meaning, not a caption)
    p.append(txt(W / 2, 244, "Activation: spacecraft on exact COMMIT; ground on exact CONFIRM.", bold=True, max_w=W - 20))
    p.append(txt(W / 2, 258, "SUCCESS additionally requires post-convergence command and telemetry verification.", max_w=W - 20))
    return W, H, "\n".join(p)


def fig2():
    with (SRC / "figure-2-outcome-distribution-source.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    W, H = PAGE_W, 196
    left, right, top, bottom = 54, 14, 16, 30
    pw, ph = W - left - right, H - top - bottom
    ymax, gap = 80, 34
    bw = (pw - gap * (len(rows) + 1)) / len(rows)
    p = [f'<line x1="{left}" y1="{top + ph}" x2="{left + pw}" y2="{top + ph}" stroke="black" stroke-width="0.9"/>',
         f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + ph}" stroke="black" stroke-width="0.9"/>']
    for t in range(0, ymax + 1, 20):
        y = top + ph - t / ymax * ph
        p.append(f'<line x1="{left - 4}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="black" stroke-width="0.7"/>')
        p.append(txt(left - 7, y + 2.8, t, anchor="end"))
    for i, r in enumerate(rows):
        c = int(r["count"])
        x = left + gap + i * (bw + gap)
        h = c / ymax * ph
        y = top + ph - h
        p.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bw:.2f}" height="{h:.2f}" fill="none" stroke="black" stroke-width="0.9"/>')
        p.append(txt(x + bw / 2, y - 4, c, size=9, bold=True))
        p.append(txt(x + bw / 2, top + ph + 14, r["outcome"].replace("_", " "), max_w=bw + gap - 4))
    p.append(f'<text transform="translate(13 {top + ph / 2:.1f}) rotate(-90)" font-family="{FONT}" font-size="8" '
             'text-anchor="middle">Schedules (n = 100)</text>')
    return W, H, "\n".join(p)


def fig3():
    with (SRC / "figure-3-sensitivity-source.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    vals = {(int(r["max_transmissions"]), int(r["candidate_lifetime_contacts"])): int(r["verification_complete_count"])
            for r in rows}
    tx, lf = [2, 3, 4], [2, 3, 4]
    W = COL_W
    left, top, cw, ch = 56, 34, 58, 36
    H = top + 3 * ch + 10
    p = [txt(left + 3 * cw / 2, 12, "Maximum transmissions", bold=True, max_w=3 * cw)]
    for j, t in enumerate(tx):
        p.append(txt(left + j * cw + cw / 2, top - 6, t))
    for i, l in enumerate(lf):
        p.append(txt(left - 8, top + i * ch + ch / 2 + 3, l, anchor="end"))
        for j, t in enumerate(tx):
            x, y = left + j * cw, top + i * ch
            p.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="none" stroke="black" stroke-width="0.9"/>')
            p.append(txt(x + cw / 2, y + ch / 2 + 4, f"{vals[(t, l)]}/12", size=11, bold=True, max_w=cw - 6))
    p.append(f'<text transform="translate(12 {top + 3 * ch / 2:.1f}) rotate(-90)" font-family="{FONT}" font-size="8" '
             'text-anchor="middle">Candidate lifetime (contacts)</text>')
    return W, H, "\n".join(p)


def main() -> int:
    try:
        import cairosvg  # type: ignore
    except Exception:
        cairosvg = None
    made = []
    for name, fn in (("fig1", fig1), ("fig2", fig2), ("fig3", fig3)):
        w, h, body = fn()
        svg = HERE / f"{name}.svg"
        svg.write_text(doc(w, h, body), encoding="utf-8")
        made.append(svg.name)
        if cairosvg:
            cairosvg.svg2pdf(url=str(svg), write_to=str(HERE / f"{name}.pdf"))
            cairosvg.svg2png(url=str(svg), write_to=str(HERE / f"{name}.png"), dpi=600)
            made += [f"{name}.pdf", f"{name}.png"]
        print(f"{name}: {w / 72:.2f} x {h / 72:.2f} in")
    print("written=" + ", ".join(made))
    print(f"min_font_pt={_min_font_seen[0]}  overflow_checks={'skipped (no Pillow/Liberation)' if _REG is None else len(_checks) and f'{len(_checks)} passed'}")
    if cairosvg is None:
        print("NOTE: cairosvg not installed; PDF/PNG not produced (pip install cairosvg)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
