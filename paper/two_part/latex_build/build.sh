#!/bin/bash
# Local review-PDF build of the compact two-part manuscript in the IEEE TAES template.
# usage: build.sh <dir with IEEEtaes.cls and IEEEtaes.bst> <empty work dir outside the repo> [trim]
# The optional third argument "trim" builds from manuscript_two_part_compact_trim.md (made with --compact --trim-conclusion).
# Needs: pandoc, pdflatex, bibtex, python3, LaTeX packages fvextra and longtable.
# Inputs (read-only): paper/two_part/out/manuscript_two_part_compact.md, out/bibliography_two_part.bib, figures_ieee/fig{1,2,3}.pdf
# Run python3 -I paper/two_part/build_two_part_manuscript.py --compact first. The IEEE class files are not stored in the repo.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); TWO=$(dirname "$HERE"); T=$(cd "$1" && pwd); W=$2
mkdir -p "$W/figs"; cd "$W"
cp "$T/IEEEtaes.cls" "$T/IEEEtaes.bst" .
cp "$TWO/out/manuscript_two_part_compact${3:+_$3}.md" src.md
cp "$TWO/out/bibliography_two_part.bib" bibliography.bib
cp "$TWO"/figures_ieee/fig1.pdf "$TWO"/figures_ieee/fig2.pdf "$TWO"/figures_ieee/fig3.pdf figs/
python3 "$HERE/prep.py"
python3 "$HERE/tabs.py" body.md body2.md
pandoc body2.md -f markdown+pipe_tables+tex_math_dollars+raw_tex -t latex --natbib --top-level-division=section --shift-heading-level-by=-1 -o body.tex
python3 "$HERE/assemble.py"
python3 "$HERE/post.py"
sed -i 's/\\section\*{Acknowledgment}/\\section*{ACKNOWLEDGMENT}/' main.tex
pdflatex -interaction=nonstopmode main.tex >p1.log 2>&1 || true
bibtex main >bib.log 2>&1 || true
pdflatex -interaction=nonstopmode main.tex >p2.log 2>&1 || true
pdflatex -interaction=nonstopmode main.tex >p3.log 2>&1 || true
pdfinfo main.pdf | grep Pages
echo "overfull: $(grep -c 'Overfull .hbox' p3.log)"; grep -E '^! ' p3.log | head -5 || true
