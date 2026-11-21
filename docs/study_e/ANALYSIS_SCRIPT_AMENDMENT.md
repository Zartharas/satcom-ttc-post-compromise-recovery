# Analysis-script amendment (written AFTER the freeze; discloses everything added)
Frozen record: tag study-e-prereg-v1 = commit 93636b1777e7865f5f3c0480e0ce1d3e6be6c3cf (author approval 2026-11-19). That commit contains the model, validation tests, anchors and the pre-registration, but NOT the confirmatory runner. This amendment adds the runner. It changes no frozen file.

## Added files
study_e/confirm.py, tests/test_confirm.py (11 tests), tools/run_confirmatory.py, this document. Tag study-e-analysis-script-v1 must be created on the commit that contains them BEFORE the full run; the runner refuses to run otherwise.

## What it does
Implements H-E2a, H-E2b, H-E2c, H-E3, H-E4, H-E5 as stated in the frozen text, in exact rational arithmetic, over the full factorial exchange grid (7,680) and the full composite grid (207,360 = 7,680 x H{4,8,20} x policy x3 x detect{1,3,5}). H-E1 is established by the validation suite, not the runner.

## Operationalisations declared before any confirmatory run
See OPERATIONALISATION in study_e/confirm.py (printed in the results file). Where the frozen text was ambiguous: R0 values (n_msgs=4, B0=8, L0=3) come from the frozen tools/size_grid.py because the pre-registration text gives none; H-E3 "INDETERMINATE mass" is tested at H=20 (primary) and at H=4 (secondary); "almost always" in H-E4 = recovery fraction >= 0.95; "detection delay matters" = range over detect > 0.01 absolute; H-E5 is exchange-level only because the composite scenario does not support Gilbert-Elliott loss.

## Disclosures
1. Before the full run, a 192-configuration test grid was executed (11 unit tests plus a smoke run). On it, H-E2b (gated: more durable persistence never increases ground-ahead divergence) showed witnesses between commit and journal. One witness (p=1/5, K=2, B=4, L=2, r=1/10, gated: volatile = commit = 1152/3125, journal = 256/625) was confirmed with the independent enumerator, so it is a real model result, not a runner bug. Reason: journal removes restart-terminal G-ahead losses and lets more attempts continue, some of which end at step 4. This was seen before the confirmatory run; the frozen hypothesis is unchanged and will be reported as run.
2. After that observation an EXPLORATORY check was added (total divergence vs persistence). It is labelled exploratory, post hoc, and is not a pre-registered hypothesis.
3. The full-grid results are unseen at the time of writing.
4. Frozen-record guard: Studies A-D untouched.
