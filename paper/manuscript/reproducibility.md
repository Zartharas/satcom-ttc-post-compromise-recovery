# 9. Reproducibility and Artifact Availability

The final experiment was designed so that the manuscript's numerical results can be traced to an
exact code version, predeclared plan, serialized schedules, retained raw outputs, and derived
table/figure sources.

## 9.1 Versioned execution identity

The final retained study used:

- plan commit: `cfb730a8191d37863e9e419823686b3c3afe18a2`;
- plan SHA-256:
  `3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`;
- execution/runner commit:
  `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`; and
- retained run identifier: `20260814T022506Z-gc630fb4`.

The execution wrapper verified the exact local/remote branch head, clean tracked tree, protected
input hashes, repository manifest, plan contract, and full regression suite before crossing the
final result boundary.

## 9.2 Retained bundle

The retained final bundle has external SHA-256:

```text
b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1
```

Its internal 16-file checksum manifest verified completely. The bundle contains the exact final
plan input; raw Study A, B, C, and D outputs; processed matched/deterministic tables; Study C and
Study D summaries; figure-source CSVs; execution metadata; command/environment logs; and captured
runner stdout/stderr.

The raw retained bundle is intentionally not rewritten when manuscript summaries change.

## 9.3 Tracked manuscript-facing derivatives

The repository tracks derived source data under `paper/tables/` and `paper/figures/`, including
the matched-family table, deterministic T1 matrix, Study C outcome summary/reachability audit,
Study D sensitivity summary, and Figure 2/Figure 3 source values.

`experiments/scripts/summarize_paper_final_results.py` verifies the retained run identity and
checksum manifest before deriving manuscript-facing sources. This reduces reliance on manual
number transcription.

## 9.4 Regression and plan validation

At the final execution boundary, 256 repository tests passed. The plan-bound final runner also
supports `--validate-only`, which verifies the committed final plan, protected scientific inputs,
and Study B/C/D schedule contracts without executing outcome runs.

Subsequent manuscript-only commits continue to run the same regression and final-plan validation
in CI. Scientific inputs and retained outputs are not modified as part of manuscript editing.

## 9.5 Availability

The source repository contains the simulator, final experiment plan, validation/derivation tools,
tracked processed result sources, bounded formal models, and manuscript evidence mapping.

The large raw retained bundle is currently kept outside ordinary Git history and identified by
the run ID and SHA-256 above. The submission/release step should publish that immutable bundle
through a stable research archive or explicit software release and record the resulting
persistent identifier in the final manuscript.

Until that archive identifier exists, the manuscript should not claim that the raw artifact is
publicly archived. It can accurately state that the retained artifact exists, is checksum-pinned,
and is reproducible from the exact code/configuration identities above.

## 9.6 Reproduction boundary

Reproducing the synthetic results does not validate the cryptographic security of B0–B2 or T1,
nor does it demonstrate flight applicability. The reproducibility claim is limited to the
software model, serialized schedules, analysis pipeline, and bounded formal evidence described
in this paper.
