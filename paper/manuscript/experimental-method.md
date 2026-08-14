# 5. Experimental Method

## 5.1 Research questions

The final study addresses four research questions.

**RQ1 — Matched recovery behavior.** Under defensibly matched conditions, how do B0, B1, B2,
and T1 compare in terminal security, availability, alignment, and verification classifications?

**RQ2 — T1 fault robustness.** How does T1 behave under controlled loss, delay, duplication,
reordering, contact interruption, endpoint restart, stale counter, and replay faults?

**RQ3 — T1 sensitivity.** How does T1 behavior change across bounded retry budgets and
candidate-retention lifetimes?

**RQ4 — Assurance.** Where do bounded TLA+ witnesses and Python executions agree or differ
under the declared abstraction/projection?

## 5.2 Experimental platform

The experiment uses a deterministic Python simulator with a scenario loader, logical-time event
queue, ground and spacecraft endpoints, baseline adapters, T1 controller, recovery authority,
contact/link scheduler, adversary/fault model, invariant monitor, outcome evaluator, and
append-only evidence writer.

Deterministic studies use explicit serialized schedules. Seeded studies serialize the generated
schedule before execution so that the replay artifact is the schedule plus its SHA-256 rather
than the integer seed alone.

The final experiment was executed from commit
`c630fb4f65ad78211fd3ffb0391000d7ed3629b1`. The outcome-blind plan was committed earlier at
`cfb730a8191d37863e9e419823686b3c3afe18a2`, with plan SHA-256
`3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`.

## 5.3 Outcome dimensions

Each execution records terminal outcome, alignment, security state, availability state,
verification completeness, fault/rejection evidence, and T1-specific duration/transmission/retry
metrics where applicable.

The experiment treats these dimensions separately. In particular, synchronization does not imply
verification; availability does not imply security; an adverse raw outcome enum does not override
the separate security-state field; and T1-specific contact/retry metrics are not assumed
equivalent to baseline adapter metrics.

## 5.4 Conservative cross-treatment comparability

Structural output parity does not make baseline and T1 measurements scientifically equivalent.
Baseline scenarios and T1 runs differ in contact accounting, retry opportunities, transmission
semantics, and activation behavior.

The comparability matrix therefore classifies scenario families as `QUALIFIED_MATCH`,
`DIAGNOSTIC_FAMILY_ONLY`, `TREATMENT_SPECIFIC`, or `NON_OUTCOME_GUARD`. Only four families
qualified for final matched comparison: CF-01 passive operational-key compromise followed by
fresh recovery material; CF-02 no-fault transition/recovery completion; CF-05 post-convergence
status-telemetry loss; and CF-06 replay after successful state advancement.

The final matched population contains 13 member rows and 12 treatment-within-family analysis
units. The two CF-02 B1 activation-policy traces remain separate rows for traceability but
represent one B1 analysis unit.

Study A uses only family-authorized categorical/evidence fields. It does not pool treatments
across families and does not compare recovery duration, total transmissions, or retry overhead
across B0/B1/B2/T1.

## 5.5 Study A — matched treatment families

Study A executes the four qualified families unchanged from the frozen comparison plan. Member
outcomes are displayed side by side within each family.

The analysis is descriptive case comparison, not an inferential treatment trial. No pooled
treatment score, ranking, confidence interval, or superiority test is computed.

## 5.6 Study B — deterministic T1 fault coverage

Study B contains 40 schedules: one no-fault control, 31 canonical schedules covering every
semantically implemented fault-kind/phase cell, and eight retry-exhaustion boundary schedules.

The 31 canonical cells comprise `DROP` across six phases; `DELAY` across six phases; `DUPLICATE`
across the four message-bearing recovery phases; `REORDER` across those four phases;
`CONTACT_CLOSE` across six phases; `ENDPOINT_RESTART` at COMMIT and CONFIRM; `STALE_COUNTER`
at PREPARE; and `STALE_REPLAY` at COMMIT and CONFIRM.

Duplicate faults are not counted at TEST_COMMAND or STATUS_TELEMETRY because those verification
opportunities are modeled as Boolean evidence rather than `RecoveryMessage` objects. Counting
duplicates there would overstate simulator behavior.

The retry-exhaustion schedules apply `DROP` or `CONTACT_CLOSE` at every permitted attempt of
PREPARE, RESPONSE, COMMIT, or CONFIRM. All adverse outcomes are retained.

## 5.7 Study C — fixed mixed-schedule population

Study C uses exactly 100 predeclared seeds, 10001 through 10100 inclusive. The deterministic
schedule generator selects a fault count from zero through four, fault kinds from the eight
supported kinds, valid phase, applicable attempt, and delay duration. Duplicate
`(phase, attempt, kind)` schedule cells are suppressed.

The schedule-only preflight contained 191 planned actions and referenced all 31 valid
fault-kind/phase cells. No seed was selected or discarded based on final outcomes.

Authorized summaries are descriptive: outcome counts/percentages with denominator 100,
security/availability counts, verification-complete count, T1-only median/range for modeled
duration/transmissions/retry overhead, and schedule fault distributions. No confidence intervals,
hypothesis tests, causal inference, or real-world prevalence inference are used.

After execution, a separate diagnostic reachability audit compared scheduled actions with actual
runtime `fault_applied` events. That audit was not used to alter the retained population.

## 5.8 Study D — retry/retention sensitivity

Study D uses a fixed 12-schedule challenge set across a 3 x 3 grid:

```text
max_transmissions = [2, 3, 4]
candidate_lifetime_contacts = [2, 3, 4]
```

The challenge set contains no-fault recovery; single and repeated drops; repeated contact
closures; two-contact delays; COMMIT-stage spacecraft restart; and stale COMMIT replay.

The grid produces 108 executions. Each parameter cell has the same fixed denominator of 12.
Reported summaries are terminal outcome/verification counts and T1-only descriptive
duration/retry/transmission statistics. The challenge set is designed to expose parameter
sensitivity, not to estimate the probability of mission faults.

## 5.9 Bounded formal assurance

RQ4 reuses the existing bounded TLA+ and Python evidence rather than introducing a new formal
phase after result observation. The formal work includes positive safety/property execution, an
explicit success witness, success-trace comparison against the Python controller, adverse
witnesses for `INDETERMINATE`, `SECURE_DEGRADED`, and `EXPIRED`, diagnostic checks for outcomes
absent from the original transition relation, and an opt-in expanded diagnostic model.

Trace comparison uses a declared 16-field projection. A mismatch would be retained for review
rather than reconciled silently. The formal work is supporting consistency evidence, not
refinement proof or cryptographic validation.

## 5.10 Predeclaration, retention, and rerun policy

The committed final plan fixed the matched families, analysis units, deterministic cell matrix,
Study C seed population and serialized schedules, Study D challenge set/grid, permitted summary
statistics, and target table/figure schemas before final outcome execution.

The retained run was executed once from a clean exact commit. Unfavorable outcomes remain in the
dataset. A material implementation or execution defect discovered later would require a new,
separately identified correction run while preserving the original bundle; a rerun is not
performed merely to obtain preferred results.
