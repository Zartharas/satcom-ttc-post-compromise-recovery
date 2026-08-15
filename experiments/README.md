# Experiments

The retained final-paper experiment was predeclared and executed once. Its reproducibility path is:

- `configs/paper-final-experiment.json` — committed outcome-blind final plan;
- `scripts/run_paper_final_experiment.py` — plan-bound final runner; and
- `scripts/summarize_paper_final_results.py` — post-run derivation of tracked paper result
  summaries from the immutable retained bundle.

Phase-numbered configs/scripts are preserved development and validation artifacts. Their
`PROVISIONAL` or phase-specific status strings are historical and are not current project status.

Final raw run bundles live under Git-ignored `results/` paths or an external archive. The
retained paper run is identified in `paper/RESULTS_SUMMARY.md`.
