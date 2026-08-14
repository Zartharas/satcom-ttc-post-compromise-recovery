# 6. Results

This section reports the retained final experiment executed from commit
`c630fb4f65ad78211fd3ffb0391000d7ed3629b1` using the predeclared final plan committed at
`cfb730a8191d37863e9e419823686b3c3afe18a2`. The retained run identifier is
`20260814T022506Z-gc630fb4`. All results below are descriptive observations from the bounded
synthetic model. They are not estimates of real-world satellite fault prevalence, cryptographic
security guarantees, or causal treatment effects.

## 6.1 Matched-family comparison

Study A compared B0, B1, B2, and T1 only where the repository's treatment-comparability analysis
identified defensibly matched operational semantics. The retained population contained 13 member
rows representing 12 treatment-within-family analysis units across four qualified families.
The two B1 activation-policy variants in CF-02 were retained as separate traceability rows but
counted as one B1 analysis unit.

In CF-01, which represents passive operational-key compromise followed by fresh recovery
material, B0, B1, B2, and T1 all terminated with `SUCCESS`, synchronized endpoint state,
`AVAILABLE` availability, and `SECURE_PROVISIONAL` security classification. In all four rows,
the active key was not marked compromised at the observation cutoff.

CF-02 represents a no-fault transition/recovery-completion case. B0, B2, T1, and both B1
activation-policy traces all terminated with `SUCCESS`, synchronized endpoint state,
`AVAILABLE` availability, `SECURE_PROVISIONAL` security classification, and complete
verification evidence. Because the two B1 traces implement alternative activation policies
rather than independent replications, they are not double-counted.

CF-05 evaluates post-convergence loss of status telemetry. B2 and T1 produced the same
classification: `INDETERMINATE`, synchronized endpoint state, `DEGRADED` availability,
`NOT_ESTABLISHED` security state, incomplete telemetry, and incomplete verification. The
protocol state had converged, but the experiment intentionally withheld a success classification
because the required post-recovery evidence was incomplete.

CF-06 evaluates stale replay after successful state advancement. Both B2 and T1 terminated with
`SUCCESS`, synchronized state, and `AVAILABLE` availability while recording one replay and one
replay rejection. Thus, within this matched family, replay rejection did not prevent successful
completion.

Taken together, the four qualified families showed categorical parity on their pre-authorized
comparison fields. The retained matched-family evidence therefore does not support a claim that
T1 categorically outperforms B0, B1, or B2. Its value is instead to establish that, under the
subset of conditions that can be compared conservatively, T1 reproduces the same terminal
classifications while preserving the model's evidence and security boundaries.

## 6.2 Deterministic T1 fault behavior

Study B executed 40 predeclared deterministic schedules: one no-fault control, 31 canonical
fault-kind/phase cells, and eight retry-exhaustion boundary schedules. The no-fault control
completed successfully.

Across the 31 canonical fault cells, 25 terminated `SUCCESS`, four terminated
`INDETERMINATE`, one terminated `EXPIRED`, and one terminated `SECURE_DEGRADED`.

### 6.2.1 Loss and contact interruption

A single `DROP` during `RECOVERY_PREPARE`, `RECOVERY_RESPONSE`, `RECOVERY_COMMIT`, or
`RECOVERY_CONFIRM` recovered within the configured retry budget and terminated `SUCCESS`.
The same pattern occurred for a single `CONTACT_CLOSE` in those four recovery phases.

The behavior changed when the fault affected post-convergence verification evidence. A dropped
or closed `TEST_COMMAND` opportunity and a dropped or closed `STATUS_TELEMETRY` opportunity
left the endpoints synchronized but produced `INDETERMINATE`, `NOT_ESTABLISHED`,
`DEGRADED`, and `verification_complete=false`. These four cases account for all four canonical
`INDETERMINATE` outcomes.

This distinction is important: endpoint synchronization was not treated as sufficient evidence
of trusted operational recovery. The result classifier required the configured verification
evidence before assigning `SUCCESS`.

### 6.2.2 Delay, duplication, reordering, and stale input

All six canonical `DELAY` cells completed successfully, including delays during the four
recovery-message phases and both post-convergence verification opportunities.

All four message-bearing `DUPLICATE` cells also completed successfully. Each recorded a
rejection of the duplicate message identifier, demonstrating idempotent handling within the
bounded model without preventing recovery.

The four `REORDER` cells similarly completed successfully while recording rejection of the
injected out-of-order message. `STALE_COUNTER` at `RECOVERY_PREPARE` and stale replay at
`RECOVERY_COMMIT` or `RECOVERY_CONFIRM` were rejected and still terminated `SUCCESS`.

These results show that the bounded controller distinguishes invalid or stale protocol material
from the valid in-progress recovery transaction rather than allowing one malformed/replayed
message to overwrite the accepted state transition.

### 6.2.3 Endpoint restart

Endpoint restart exposed the clearest deterministic recovery boundary. A spacecraft restart at
`RECOVERY_COMMIT` terminated `EXPIRED` with the ground side ahead (`G_AHEAD`), `UNSAFE`
security state, `UNAVAILABLE` availability, and incomplete verification. The restart destroyed
pending protocol state needed to complete the transition.

A restart at `RECOVERY_CONFIRM` produced the raw outcome label `SECURE_DEGRADED`, with the
spacecraft side ahead (`S_AHEAD`), `UNSAFE` security state, `DEGRADED` availability, and
incomplete verification. The raw enum name is retained for reproducibility, but the independent
security-state field is authoritative for interpretation: this case is not evidence of a
cryptographically secure degraded state.

### 6.2.4 Retry exhaustion

The eight retry-exhaustion schedules repeatedly dropped or closed one recovery phase until the
configured transmission budget was exhausted. Six terminated `EXPIRED`; two terminated
`SECURE_DEGRADED`.

Exhaustion at `RECOVERY_PREPARE`, `RECOVERY_RESPONSE`, or `RECOVERY_COMMIT` produced
`EXPIRED`, `G_AHEAD`, `UNSAFE`, and `UNAVAILABLE`. Exhaustion at
`RECOVERY_CONFIRM` instead produced `SECURE_DEGRADED`, `S_AHEAD`, `UNSAFE`, and
`DEGRADED`. This split reflects the activation boundary: confirmation loss can occur after the
spacecraft has advanced, whereas earlier exhaustion prevents the same terminal state from being
established at both endpoints.

## 6.3 Fixed mixed-schedule characterization

Study C executed the 100 predeclared serialized schedules generated from seeds 10001 through
10100. The retained terminal distribution was:

- 74 `SUCCESS`;
- 15 `INDETERMINATE`;
- 6 `SECURE_DEGRADED`; and
- 5 `EXPIRED`.

Verification completed in 74 of 100 schedules. These values describe the fixed synthetic
schedule population and are shown in Figure 2. They must not be interpreted as estimates of
mission reliability or real-world fault prevalence.

A post-execution reachability audit revealed an important limitation of the random schedule
generator. The 100 serialized schedules contained 191 scheduled fault actions, but only 77 were
actually reached and applied by the runtime. Forty-three schedules reached no scheduled fault
action. Although the schedule definitions referenced all 31 valid fault-kind/phase cells, only
24 cells were exercised at runtime.

The difference arises because the generator may schedule an action for attempt two or three even
when the recovery transaction succeeds, terminates, or changes state before that opportunity is
reached. Consequently, the observation that 74 schedules terminated successfully is properly
reported as the outcome distribution of the fixed 100-schedule population, not as a 74% success
rate "under faults." Deterministic Study B, in which each canonical cell was explicitly reached,
provides the stronger fault-coverage evidence.

## 6.4 Retry and candidate-retention sensitivity

Study D applied a 3 x 3 parameter grid to a fixed 12-schedule challenge set. Maximum
transmissions took values 2, 3, and 4; candidate-retention lifetime took values 2, 3, and 4
contacts. Each grid cell therefore contained the same 12 challenges.

For every candidate-lifetime value, `max_transmissions=2` produced five verification-complete
executions out of 12. The corresponding terminal outcomes were five `SUCCESS`, five `EXPIRED`,
and two `SECURE_DEGRADED`.

Increasing the transmission budget to three changed the result to 11 verification-complete
executions out of 12, with 11 `SUCCESS` and one `EXPIRED`. Increasing the budget from three to
four did not change any terminal count: the same 11 schedules completed verification and the
same one schedule expired.

Candidate lifetime from two through four contacts produced no observed change in this fixed
challenge set. The persistent failure at transmission budgets three and four was the
COMMIT-stage spacecraft-restart case, where loss of pending endpoint state cannot be repaired by
additional retransmission alone.

The T1-only descriptive transmission metrics changed with the retry budget as expected. The
median total-transmission count was 6.0 for the two-transmission setting and 7.5 for the
three- and four-transmission settings; median retry overhead increased from 0.0 to 1.5. Median
modeled recovery duration remained one contact across the grid, with a range of one to three
contacts. These values describe only the fixed T1 challenge set and are not cross-treatment
performance measurements.

## 6.5 Supporting bounded formal/Python agreement

The earlier formal-methods work is treated as supporting assurance rather than as a proof of the
final implementation or of cryptographic security.

For the bounded success witness, the TLA+ trace and Python replay were compared over 16 declared
abstract fields. The first retained cross-validation compared 136 field rows and recorded
136 matches with zero mismatches. The result was explicitly labeled
`MATCH_WITHIN_DECLARED_ABSTRACTION`.

Three adverse-outcome witnesses were then examined with the same projection. The
`INDETERMINATE` witness produced 119 of 119 matching rows, the `SECURE_DEGRADED` witness
produced 119 of 119, and the `EXPIRED` witness produced 85 of 85. The original bounded model did
not assign `DIVERGED`, `AVAILABLE_UNSAFE`, or `LOCKED`; those outcomes were reported as absent
from the original transition assignments rather than impossible.

An opt-in diagnostic expansion subsequently added one explicit path for each of those three
previously absent outcomes while preserving the original TLA+ module. Across the three expanded
witnesses, 272 of 272 projected rows matched the corresponding Python traces, again with zero
mismatches.

These observations support internal consistency between selected bounded formal traces and the
Python projection. They do not establish refinement, implementation equivalence, unbounded
safety/liveness, cryptographic security, or completeness of the outcome space.

## 6.6 Answers to the research questions

**RQ1 — matched recovery behavior.** In the four qualified matched families, T1 produced the
same authorized categorical terminal classifications as the corresponding abstract baselines.
No categorical-superiority claim is supported.

**RQ2 — T1 fault robustness.** Within the deterministic model, isolated message loss/contact
closure during the recovery exchange, bounded delay, duplication, reordering, stale counters,
and stale replay were recoverable or rejectable without preventing successful completion.
Incomplete post-convergence verification evidence produced conservative `INDETERMINATE`
classification. Endpoint restart and retry exhaustion around activation exposed the principal
failure/degradation boundaries.

**RQ3 — T1 sensitivity.** In the fixed 12-schedule challenge set, increasing the transmission
budget from two to three materially changed terminal behavior, while increasing it from three to
four did not. Candidate lifetime from two to four contacts produced no observed difference in
that challenge set. These findings are bounded and do not establish a universal optimum.

**RQ4 — assurance.** Selected bounded TLA+ witnesses and Python executions agreed over the
declared 16-field projection with zero recorded mismatches in the retained comparisons. This is
supporting consistency evidence, not a formal refinement or cryptographic-security proof.
