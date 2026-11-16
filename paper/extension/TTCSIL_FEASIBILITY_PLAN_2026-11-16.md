# TTCSIL-SA-RST-001 — Software-in-the-loop feasibility and stop/go plan

**Date:** 2026-11-16  
**Authority:** `TTCSIL_PROSPECTIVE_PROTOCOL_DRAFT.json`. Design only; it is **not** frozen or executed.

## Specific aerospace motivation

- CCSDS 350.5-G-2 §§3.5.1.2, 4.5.6 describes a last-resort Recovery SA with segregated persistent context. It does not establish crash-safe completion for this *new* transaction implementation. https://ccsds.org/Pubs/350x5g2.pdf
- ECSS-E-ST-70-11C Rev.1 (2025), §§4.2 observability and 4.3 commandability, motivates the need to distinguish verified resumption, safe-hold, and authenticated reinitiation; this study does not claim ECSS compliance. https://ecss.nl/standard/ecss-e-st-70-11c-rev-1-space-segment-operability-15-october-2025/
- Critical field outcome: after process restart, do **not** resume normal telecommands merely because fresh key material or a local success flag exists.

## Candidate environment, not an installed or compatible stack

Upstream release records inspected 2026-11-16: [CryptoLib](https://github.com/nasa/CryptoLib) `v1.5.2` (2026-11-04); [NOS3](https://github.com/nasa/nos3) `v1_07_06` (2026-10-30); [cFS](https://github.com/nasa/cFS) `v7.0.1` (2026-05-14). A release name is NOT a pinned commit or compatibility guarantee. CryptoLib/NOS3 use NASA Open Source Agreement 1.3; the cFS bundle uses Apache 2.0. Never mix incompatible standalone cFS/NOS3 dependency graphs, vendor upstream code, or claim NASA certification.

| Stop/go | Evidence needed **before** scientific execution | Stop condition |
|---|---|---|
| F1 Source/version/license | Pin exact tag->SHA, submodule graph, build environment, dependency rights, security advisory review | Any unresolved source or distribution restrictions |
| F2 Restart is real | Observe actual spacecraft/ground application termination/restart plus durable/volatile storage transition | Restart only resets an in-memory simulator variable |
| F3 SA state measurable | Instrument ground and spacecraft epoch/SA acceptance, pending/receipt state, persist/flush boundaries | State inferred from a final label or hidden simulator oracle |
| F4 Command verification genuine | Under supported SDLS API, observe accepted/rejected protected command and authenticated status return | Merely an artificial `command_verified=true` flag |
| F5 Comparators fair | Same initial state, recovery authority, fault schedule, input visibility, time/contact opportunities | Different input privileges or contrived strawman |
| F6 Adversarial/independent oracle | Independently reconstruct acceptance and resumption from event stream; confirm false-resume and replay negative controls | An attacked SUT success flag is used as ground truth |
| F7 Protocol frozen | Exact preregistered case registry, fault positions, analysis denominators, exclusions, artifact hashes, source locks | Post-hoc case selection or incomplete pre-execution freeze |
| F8 Originality refreshed | Check other repos' live `main` and pending publication claims; no reused observations, datasets or same endpoint | Collides with Study 8E/9 or lifecycle/multi-paper outcomes |

### Comparator and interpretation constraints

`H0_SAFE_HOLD` is a **safety** reference and intentionally makes no claim of progress. `H1_VOLATILE_RETRY` is the retry-only comparator; `H2_DURABLE_OR_REINIT` is an unimplemented candidate and not a proven mitigation. Each must receive equivalent initial state, restart schedule, and trust assumptions; report false resume, unsafe SA acceptance, convergence, and verified commandability **separately**. A single violation counts as negative evidence, even if aggregate recovery progresses. Missing field-level status = `UNVERIFIED` not `SUCCESS`.

### What would justify execution?

First demonstrate source reproducibility and **actual instrumented process/SA integration** on a bounded smoke test, validate the independent event oracle, adjudicate the planned case list without looking at comparative outcomes, and freeze the protocol under a separate decision. If upstream CryptoLib does not expose the required SA/persistence APIs, document that limitation and consider a clearly named extension or alternative integration rather than pretending the library implements T1.

**Prohibited:** new source-population claims based on SatNOGS/ESA/CuCD/AegisSat/UNSW; claiming actual operational compromise/recovery; running the frozen A–D campaigns to tune outputs; reporting cryptographic security/conformance without specialist validation; publishing the retained raw bundle. The present TAES manuscript may be strengthened editorially with existing A–D evidence while this extension remains on hold.

**Planned artifacts, not yet present:** `environment_lock.json`, `integration_contract.json`, `case_registry.json`, `oracle_spec.json`, `comparator_contract.json`, `execution_manifest.json`, `event_traces.jsonl`, `integrity_manifest.sha256`, and `deviation_log.md`.
