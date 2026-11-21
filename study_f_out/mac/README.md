# Study F results (macOS run, tag study-f-plan-v1)

Files: study_f_results.csv (116 cells), study_f_not_defined.csv (44 records), run_manifest.json (as written by study_f/run_grid.py).

Line endings: the runner wrote these CSV files with CRLF line endings. The repository stores them with LF (.gitattributes: text=auto eol=lf), and the stored LF form is what is committed. Content is identical; only line endings differ.

- study_f_results.csv: sha256 as written (CRLF) 1cc09e16e260e4c66cc279eae51aa78d411796f9edd67ed157b45c9bad9cb95b, as stored (LF) bce544600f9f714b5ecf906aaa35c73608833a28037463929d2b127321e731ab
- study_f_not_defined.csv: sha256 as written (CRLF) 25d96fb75a5c3bf0166e05d07388f908e93860d9a158afc296ac94eec1adf94f, as stored (LF) b0e6e32d93c92eecb6ca14e235f1ccb5257a17d729f22b8ac93763b27c4ef829

The CRLF hashes in run_manifest.json were identical on macOS (Python 3.11.7), Docker python:3.11-slim (3.11.18) and Linux (3.10.12).
