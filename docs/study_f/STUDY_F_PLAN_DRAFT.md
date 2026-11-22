# Study F plan (DRAFT, not frozen, not executed)

Status: DRAFT for the author. Nothing here is a frozen record. Part I (Studies A-D) and Study E are unchanged. No Study F result has been produced or read; only the reduction tests below were run.

## Question
Part I injects faults into T1 only. Study F asks, descriptively: when the frozen baseline abstractions (B0 OTAR, B1 triple-KEM in two activation policies, B2 strict URKE) face message-step faults at the steps their abstractions define, which terminal outcomes follow, and how do they differ from T1's results in Table 2? No superiority claim, no pooling with Part I, no inferential statistics.

## Design (implemented in study_f/baseline_fault_grid.py)
1. **Defined cells only.** A cell exists where the frozen baseline code defines the fault: loss of a step's message (DROP and CONTACT_CLOSE, equivalent in a sequential one-message-per-step flow, assumption A-seq), B1 reordering of required fragments, a spacecraft restart that loses B1 pending state (assumption A-vol), and the two native B2 faults (stale ground restore, replayed update). Every other (baseline, step, T1 fault kind) is written to the output as NOT_DEFINED_BY_BASELINE (44 records); DELAY, DUPLICATE, STALE_COUNTER and STALE_REPLAY have no frozen baseline semantics and are not invented.
2. **Bracketing budgets.** Budget 1 = as specified (the baselines define no retransmission). Budget 3 = a named assumption favourable to baselines: a lost message is retransmitted up to three transmissions, matching T1's default. Loss counts 1, 2, 3 consecutive losses per step, so a budget-3 run with 3 losses is exhaustion. This separates "baselines lack retries" from "T1 differs in recovery logic".
3. **Initial states.** T1_BASE (ground epoch 2, spacecraft epoch 1, current keys attacker-known) for the comparison with Part I; CATALOG and CATALOG_COMPROMISED reproduce the frozen catalog's setups for validation only.
4. **Size.** 116 cells (58 per budget) from T1_BASE. Plan-table hash (cell ids plus not-defined records): d0e0199056f7394ea471905f71c69e46ab384333dd108b2c7cdaef14819781c1.
5. **Outputs.** Outcome, alignment, security state, verification-complete per cell. No timing or retry-count comparison across treatments.

## Validation already done
Study F's engine reproduces outcome, alignment and security state of 13 frozen catalog scenarios (B0-01, B0-04, B1-01, B1-03 to B1-07, B2-01, B2-07 to B2-10) exactly (tests in study_f/tests). The frozen code is imported read-only.

## Assumptions that favour or limit the result (stated before running)
- A-seq: contact closure equals a drop for these flows.
- A-vol: a B1 responder restart destroys pending state.
- A-retx (budget 3): the sender can retransmit or re-request a lost message, and the receiver keeps its pending state across retransmissions. For B2 this also means a lost update does not lock out if a later copy arrives; the frozen B2 code locks out on the first loss.
- Baselines were not designed for these faults; their behaviour is the frozen abstraction's, not a claim about the published protocols.

## Not covered
Active attackers beyond the frozen scopes, baseline-specific cryptographic properties, timing, and any pooled score.

## Governance before running
1. Author reviews the cell table and the assumptions above.
2. Author commits this plan and the engine (plan commit), then tags it, mirroring study-e-prereg-v1.
3. Only then run the grid once, retaining all outcomes including unfavourable ones.
4. Part I bundle, manifest and tags stay untouched.

## Reporting route (author decision)
Add a short "Study F" section and one table to the two-part paper (about one page; the paper is at 20 pages), or hold it as a follow-up paper. The abstract and contributions change only if the run is reported.
