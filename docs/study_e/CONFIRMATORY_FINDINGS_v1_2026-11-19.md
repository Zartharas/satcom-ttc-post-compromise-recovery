# Study E confirmatory findings v1 (as run; no hypothesis rewritten)
Run: tag study-e-analysis-script-v1 = commit 6eb87f272444c6965e2fd9b36bbe2c4aec53212d on top of frozen study-e-prereg-v1 = 93636b1777e7865f5f3c0480e0ce1d3e6be6c3cf. Author's Mac, Python 3.11.7, 613 s, exact rational arithmetic, full factorial exchange grid (7,680) and full composite grid (207,360). Table SHA-256 dfed99fac58eecd39eb67dd51ae40f662153212d5abefa3eadb55a4f20ada47d. Independent reproduction: the same table digest was recomputed in the Claude container (Python 3.13, Linux) and matches exactly. Operationalisations are those declared in ANALYSIS_SCRIPT_AMENDMENT.md before the run.

| Hypothesis | Result as run | Verdict |
|---|---|---|
| H-E1 exact DP = enumeration | 99-test suite passes natively (1 skipped) and in the container; Docker verified 88 tests before the amendment, not yet rerun on 99 | supported (validation grid) |
| H-E2a SUCCESS monotone | B: 0/5,760 violations; L: 0/5,760; H (per policy): 0/46,080. K: 31/5,760 violations; p: 22/6,144 violations | PARTLY FALSIFIED (K and p) |
| H-E2b gated: durability never raises G-ahead | 288/2,560 violations, all commit to journal, max rise 0.0815 | FALSIFIED |
| H-E2c journal invariant to r | 0/1,920 violations | supported |
| H-E2c volatile divergence non-decreasing in r | 447/1,920 violations (local 171, gated 276), max drop 0.0407 | FALSIFIED as operationalised |
| H-E3 retry vs INDETERMINATE mass; resume is the lever | dS < INDETERMINATE mass at H=20 and at H=4: 5,520/5,520 each; resume gain > dS: 5,520/5,520 over points with INDETERMINATE mass (5,520/7,680 over all points, the rest have none) | supported |
| H-E4 divergence almost always recoverable (declared: recovery fraction >= 0.95) | median about 1.0, but share >= 0.95 is 89.8% (expired_only, resume) and 83.2% (restart_indeterminate); minimum 0.583 | NOT SUPPORTED at the declared threshold |
| H-E4 delay matters only at short horizons / heavy loss | range over detect > 0.01 at H=20 in 5% (p=0.05), 2% (0.1), 13% (0.2), 25% (0.3), 61% (0.5) of points; at H=4 up to 0.97 | consistent; at H=20 delay matters mostly at p >= 0.3, but not only there |
| H-E5 bursty vs i.i.d. at equal stationary loss | higher 4,664, lower 3,112, equal 7,584 of 15,360; max difference 0.317; no invalid cases | supported (witness in both directions) |

## Where the falsified hypotheses fail (post hoc descriptive characterisation, not new hypotheses)
- H-E2a K: all 31 violations have r > 0 and persistence volatile (18) or commit (13); none under journal; none at r = 0; max drop 0.077.
- H-E2a p: all 22 violations have r > 0 and non-journal persistence; max rise in SUCCESS with more loss 0.0127.
- H-E2b: only commit to journal; independent enumerator confirmed the first witness (p=1/5, K=2, B=4, L=2, r=1/10, gated).
- Mechanism (model rules): restarts reset or terminate non-durable progress; extra slots or fewer losses carry an attempt into the activation-asymmetry zone (steps 3-4) before a restart or budget end, and journal keeps that progress, so more attempts end there. These are properties of the 6-message abstraction, not measured behaviour.
- Exploratory (post hoc): total divergence also fails to decrease monotonically with persistence durability: 609/5,120 violations.
- H-E2c reading: "fallback required" was operationalised as total divergence (the same quantity as the earlier development test). A different reading would need a deviation note.

## Caveats
Parametric study: loss values are stress parameters, not measured TT&C uplink loss; Gilbert-Elliott cases are a sensitivity probe; R0/R2 parameters are assumptions; 6-message abstraction not independently reviewed. Do not describe the K and p non-monotonicities as real-link behaviour.
