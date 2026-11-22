# Study E confirmatory results

Run meta: {"grid": "frozen", "head": "6eb87f272444c6965e2fd9b36bbe2c4aec53212d", "platform": "macOS-26.7.3-x86_64-i386-64bit", "prereg_commit": "93636b1777e7865f5f3c0480e0ce1d3e6be6c3cf", "python": "3.11.7", "script_tag_commit": "6eb87f272444c6965e2fd9b36bbe2c4aec53212d", "seconds": 613.3}

Table SHA-256 (exchange + composite, exact): dfed99fac58eecd39eb67dd51ae40f662153212d5abefa3eadb55a4f20ada47d

## H-E2a
```json
{
 "single_attempt_SUCCESS_vs_B": {
  "label": "SUCCESS non-decreasing in B",
  "pairs_checked": 5760,
  "violations": 0,
  "holds_everywhere": true,
  "first_witnesses": []
 },
 "single_attempt_SUCCESS_vs_K": {
  "label": "SUCCESS non-decreasing in K",
  "pairs_checked": 5760,
  "violations": 31,
  "holds_everywhere": false,
  "first_witnesses": [
   "((Fraction(1, 20), 3, 12, 3, Fraction(1, 100), 'volatile', 'local'), (Fraction(1, 20), 4, 12, 3, Fraction(1, 100), 'volatile', 'local'), '1272352040928639/1280000000000000', '40622816063523691503/40960000000000000000')",
   "((Fraction(1, 20), 3, 12, 3, Fraction(1, 100), 'volatile', 'gated'), (Fraction(1, 20), 4, 12, 3, Fraction(1, 100), 'volatile', 'gated'), '1272352040928639/1280000000000000', '40622816063523691503/40960000000000000000')",
   "((Fraction(1, 20), 3, 12, 3, Fraction(1, 100), 'commit', 'gated'), (Fraction(1, 20), 4, 12, 3, Fraction(1, 100), 'commit', 'gated'), '20404692461439/20480000000000', '40625012448653158647/40960000000000000000')",
   "((Fraction(1, 20), 3, 12, 3, Fraction(1, 20), 'volatile', 'local'), (Fraction(1, 20), 4, 12, 3, Fraction(1, 20), 'volatile', 'local'), '49753794864479/51200000000000', '1570381113604189503/1638400000000000000')",
   "((Fraction(1, 20), 3, 12, 3, Fraction(1, 20), 'volatile', 'gated'), (Fraction(1, 20), 4, 12, 3, Fraction(1, 20), 'volatile', 'gated'), '49753794864479/51200000000000', '1570381113604189503/1638400000000000000')"
  ]
 },
 "single_attempt_SUCCESS_vs_L": {
  "label": "SUCCESS non-decreasing in L",
  "pairs_checked": 5760,
  "violations": 0,
  "holds_everywhere": true,
  "first_witnesses": []
 },
 "single_attempt_SUCCESS_vs_p": {
  "label": "SUCCESS non-increasing in p",
  "pairs_checked": 6144,
  "violations": 22,
  "holds_everywhere": false,
  "first_witnesses": [
   "((Fraction(1, 20), 4, 12, 3, Fraction(1, 100), 'volatile', 'local'), (Fraction(1, 10), 4, 12, 3, Fraction(1, 100), 'volatile', 'local'), '40622816063523691503/40960000000000000000', '9928486318405743/10000000000000000')",
   "((Fraction(1, 20), 4, 12, 3, Fraction(1, 100), 'volatile', 'gated'), (Fraction(1, 10), 4, 12, 3, Fraction(1, 100), 'volatile', 'gated'), '40622816063523691503/40960000000000000000', '9928486318405743/10000000000000000')",
   "((Fraction(1, 20), 4, 12, 3, Fraction(1, 100), 'commit', 'gated'), (Fraction(1, 10), 4, 12, 3, Fraction(1, 100), 'commit', 'gated'), '40625012448653158647/40960000000000000000', '9931759667598087/10000000000000000')",
   "((Fraction(1, 20), 4, 12, 3, Fraction(1, 20), 'volatile', 'local'), (Fraction(1, 10), 4, 12, 3, Fraction(1, 20), 'volatile', 'local'), '1570381113604189503/1638400000000000000', '385543345322943/400000000000000')",
   "((Fraction(1, 20), 4, 12, 3, Fraction(1, 20), 'volatile', 'gated'), (Fraction(1, 10), 4, 12, 3, Fraction(1, 20), 'volatile', 'gated'), '1570381113604189503/1638400000000000000', '385543345322943/400000000000000')"
  ]
 },
 "composite_SUCCESS_vs_H": {
  "label": "SUCCESS non-decreasing in H (per policy)",
  "pairs_checked": 46080,
  "violations": 0,
  "holds_everywhere": true,
  "first_witnesses": []
 },
 "divergence_vs_B_descriptive": {
  "pairs": 5760,
  "pairs_where_divergence_increases_with_B": 568,
  "note": "reported, not asserted"
 }
}
```

## H-E2b
```json
{
 "label": "gated: P(G-ahead) non-increasing with persistence durability",
 "pairs_checked": 2560,
 "violations": 288,
 "holds_everywhere": false,
 "first_witnesses": [
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 100)), 'commit', 'journal', '12901779/16000000', '130321/160000')",
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 20)), 'commit', 'journal', '2476099/3200000', '130321/160000')",
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 10)), 'commit', 'journal', '1172889/1600000', '130321/160000')",
  "((Fraction(1, 20), 2, 4, 3, Fraction(1, 100)), 'commit', 'journal', '12901779/16000000', '130321/160000')",
  "((Fraction(1, 20), 2, 4, 3, Fraction(1, 20)), 'commit', 'journal', '2476099/3200000', '130321/160000')"
 ]
}
```

## H-E2c
```json
{
 "journal_invariant_to_r": {
  "label": "journal distribution identical across r",
  "pairs_checked": 1920,
  "violations": 0,
  "holds_everywhere": true,
  "first_witnesses": []
 },
 "volatile_divergence_nondecreasing_in_r": {
  "label": "volatile divergence non-decreasing in r",
  "pairs_checked": 1920,
  "violations": 447,
  "holds_everywhere": false,
  "first_witnesses": [
   "((Fraction(1, 20), 2, 4, 2), 'local', '6859/40000', '679041/4000000')",
   "((Fraction(1, 20), 2, 4, 2), 'local', '679041/4000000', '130321/800000')",
   "((Fraction(1, 20), 2, 4, 2), 'local', '130321/800000', '61731/400000')",
   "((Fraction(1, 20), 2, 4, 3), 'local', '6859/40000', '679041/4000000')",
   "((Fraction(1, 20), 2, 4, 3), 'local', '679041/4000000', '130321/800000')"
  ]
 }
}
```

## H-E3
```json
{
 "points": 7680,
 "points_with_INDETERMINATE_mass_at_H_hi": 5520,
 "primary_dS_lt_IND_hi": {
  "holds": 5520,
  "of": 5520,
  "counterexamples": []
 },
 "secondary_dS_lt_IND_lo": {
  "holds": 5520,
  "of": 5520,
  "counterexamples": []
 },
 "resume_gain_gt_dS_over_points_with_IND_mass": {
  "holds": 5520,
  "of": 5520
 },
 "resume_gain_gt_dS_over_all_points": {
  "holds": 5520,
  "of": 7680
 }
}
```

## H-E4
```json
{
 "thresholds": {
  "almost_always": "19/20",
  "delay_matters": "1/100"
 },
 "recovery_fraction": {
  "expired_only": {
   "points_with_divergence": 6960,
   "share_ge_threshold": 0.8982758620689655,
   "min": 0.5829015143408901,
   "median": 0.9999999958604208
  },
  "restart_indeterminate": {
   "points_with_divergence": 6960,
   "share_ge_threshold": 0.832183908045977,
   "min": 0.5829015143408901,
   "median": 0.9991841417164636
  },
  "resume": {
   "points_with_divergence": 6960,
   "share_ge_threshold": 0.8982758620689655,
   "min": 0.5829015143408901,
   "median": 0.9999999958604208
  }
 },
 "detection_delay": {
  "H=4": {
   "1/10": {
    "points": 4608,
    "delay_matters": 1716,
    "max_range": 0.8778733047135
   },
   "1/2": {
    "points": 4608,
    "delay_matters": 2304,
    "max_range": 0.271148681640625
   },
   "1/20": {
    "points": 4608,
    "delay_matters": 1458,
    "max_range": 0.96524262356904
   },
   "1/5": {
    "points": 4608,
    "delay_matters": 1977,
    "max_range": 0.6232534417408
   },
   "3/10": {
    "points": 4608,
    "delay_matters": 2187,
    "max_range": 0.5680015601064
   }
  },
  "H=8": {
   "1/10": {
    "points": 4608,
    "delay_matters": 2337,
    "max_range": 0.8816309067979913
   },
   "1/2": {
    "points": 4608,
    "delay_matters": 4176,
    "max_range": 0.4771054834127426
   },
   "1/20": {
    "points": 4608,
    "delay_matters": 1925,
    "max_range": 0.9655897132729236
   },
   "1/5": {
    "points": 4608,
    "delay_matters": 3089,
    "max_range": 0.6484898105786367
   },
   "3/10": {
    "points": 4608,
    "delay_matters": 3818,
    "max_range": 0.6336458875258134
   }
  },
  "H=20": {
   "1/10": {
    "points": 4608,
    "delay_matters": 108,
    "max_range": 0.07402929515754035
   },
   "1/2": {
    "points": 4608,
    "delay_matters": 2796,
    "max_range": 0.1444578002184686
   },
   "1/20": {
    "points": 4608,
    "delay_matters": 240,
    "max_range": 0.10423827129777795
   },
   "1/5": {
    "points": 4608,
    "delay_matters": 594,
    "max_range": 0.043073660869885434
   },
   "3/10": {
    "points": 4608,
    "delay_matters": 1172,
    "max_range": 0.1061720355627039
   }
  }
 }
}
```

## H-E5
```json
{
 "bursty_higher": 4664,
 "bursty_lower": 3112,
 "equal": 7584,
 "invalid_combinations_skipped": 0,
 "max_abs_difference": 0.3172131472167969,
 "witness_in_both_directions": true,
 "examples_higher": [
  "(2, (Fraction(1, 20), 2, 6, 3, Fraction(0, 1), 'volatile', 'local'), '3607119/64000000')",
  "(2, (Fraction(1, 20), 2, 6, 3, Fraction(0, 1), 'volatile', 'gated'), '3607119/64000000')",
  "(2, (Fraction(1, 20), 2, 6, 3, Fraction(0, 1), 'commit', 'local'), '3607119/64000000')"
 ],
 "examples_lower": [
  "(2, (Fraction(1, 20), 2, 8, 4, Fraction(0, 1), 'volatile', 'local'), '-303291621/25600000000')",
  "(2, (Fraction(1, 20), 2, 8, 4, Fraction(0, 1), 'volatile', 'gated'), '-303291621/25600000000')",
  "(2, (Fraction(1, 20), 2, 8, 4, Fraction(0, 1), 'commit', 'local'), '-303291621/25600000000')"
 ]
}
```

## exploratory_post_hoc
```json
{
 "label": "EXPLORATORY: total divergence non-increasing with persistence durability",
 "pairs_checked": 5120,
 "violations": 609,
 "holds_everywhere": false,
 "first_witnesses": [
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 100), 'local'), 'commit', 'journal', '679041/4000000', '6859/40000')",
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 100), 'gated'), 'commit', 'journal', '12901779/16000000', '130321/160000')",
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 20), 'local'), 'commit', 'journal', '130321/800000', '6859/40000')",
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 20), 'gated'), 'commit', 'journal', '2476099/3200000', '130321/160000')",
  "((Fraction(1, 20), 2, 4, 2, Fraction(1, 10), 'local'), 'commit', 'journal', '61731/400000', '6859/40000')"
 ]
}
```
