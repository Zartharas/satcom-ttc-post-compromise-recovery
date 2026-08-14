# 7. Discussion

The retained experiment shifts the paper's central contribution away from a treatment-ranking
claim and toward a more operational question: what prevents a key-recovery mechanism from
becoming a trusted TT&C recovery mechanism when communication is intermittent and endpoint
state can diverge? The data show that several common communication faults are recoverable with a
bounded transaction, but successful state convergence is not identical to verified operational
recovery, and retransmission cannot compensate for lost endpoint protocol state.

## 7.1 Convergence is not the same as verified recovery

The clearest recurring pattern is the separation between synchronization and evidence of
recovery completion. In deterministic Study B, loss of the test-command or status-telemetry
opportunity left both endpoints synchronized, yet the terminal result was `INDETERMINATE` rather
than `SUCCESS`. The same principle appears in matched family CF-05, where B2 and T1 both
converged but lacked the required telemetry/verification evidence.

This behavior is intentionally conservative. A recovery procedure that changes key state but
cannot demonstrate that trusted command and telemetry operations function after the transition
should not automatically be treated as operationally recovered. For TT&C, this distinction is
especially relevant because legitimate state advancement can still produce an unusable control
path if the ground cannot confirm what the spacecraft accepted or if the final operational
evidence is lost.

The result therefore supports an architectural separation between at least three properties:
cryptographic/key-state transition, endpoint synchronization, and mission-facing verification.
The simulator does not establish cryptographic security, but it demonstrates why an operational
recovery design benefits from making these properties explicit rather than collapsing them into
one success flag.

## 7.2 Bounded retransmission handles omission but not state destruction

Single `DROP` and `CONTACT_CLOSE` faults during the four recovery-message phases were recovered
within the configured retry budget. The sensitivity experiment further showed that a third
transmission opportunity changed six challenge cases from non-success to verified success,
whereas a fourth opportunity produced no additional observed benefit.

This does not imply that three transmissions is globally optimal. It shows something narrower
and more useful: bounded retransmission can absorb a class of omission/contact failures, and its
marginal benefit depends on the challenge set. The unchanged result between budgets three and
four suggests that once the repeated omission cases are covered, additional retries do not solve
qualitatively different failures.

The persistent spacecraft-restart failure demonstrates that distinction. A restart at COMMIT
destroyed pending protocol state needed to complete the transaction. Additional retries cannot
reconstruct state that the endpoint no longer retains. This is a different failure class from
message loss.

A practical follow-on implementation should therefore treat recoverable transport interruption
and recoverability of protocol state as separate design problems. Candidate/pending recovery
state may need protected persistence across restart, or the protocol may need a clean,
authenticated re-initiation path that can abandon the interrupted transaction without leaving
the endpoints in an unsafe asymmetric state.

## 7.3 Activation boundaries create asymmetric failure modes

The deterministic exhaustion cases expose a useful distinction around activation. Exhaustion
before or at COMMIT left the ground side ahead and produced `EXPIRED`, `UNSAFE`, and
`UNAVAILABLE`. Exhaustion at CONFIRM left the spacecraft side ahead and produced a degraded,
unsafe asymmetric state.

The difference is not merely a naming artifact. It reflects where each endpoint commits the
candidate state. Once one endpoint has advanced, losing the evidence or final message required
by the other endpoint can create an asymmetric terminal condition even though every prior
message was legitimate.

This observation is relevant to the B1 mapping as well. The source construction motivates
key-update and confirmation semantics, but the simulator-added question of *when a recovered key
becomes operational* is an integration decision rather than a theorem inherited from the
cryptographic source [@hulsing_lange_weber_sdls_key_update]. The experiment reinforces the need
to document activation policy explicitly in any operational mapping to SDLS-style systems
[@ccsds_sdls_355_0_b_2; @ccsds_sdls_ep_355_1_b_1].

## 7.4 Security and availability must remain separate

The raw enum `SECURE_DEGRADED` predates the final experiment and should be interpreted cautiously.
In the retained restart and confirmation-exhaustion cases, the independent `security_state`
field is `UNSAFE`. The paper therefore should not use the enum label as evidence that the
terminal state is cryptographically secure.

The broader design lesson is valuable: availability, alignment, and security classification are
different dimensions. A synchronized system can lack verification evidence; an available system
can be unsafe; and an asymmetric system can remain partially operational while failing the
recovery security objective.

The Phase 13 diagnostic expansion made the same separation explicit by constructing an
`AVAILABLE_UNSAFE` path in which availability and convergence coexist with candidate exposure.
That diagnostic model does not prove such a path's real-world likelihood, but it illustrates why
a single composite "success" metric would hide important state distinctions.

## 7.5 Replay and stale-state rejection are necessary but not sufficient

The deterministic replay, stale-counter, duplicate, and reordering cases were all rejected
without blocking completion. This is a positive property of the bounded controller: malformed,
stale, or duplicate material does not silently replace the currently accepted transaction.

However, the results also show why replay resistance alone is not a complete recovery story.
The dominant adverse cases were not successful replays. They were missing evidence, exhausted
delivery opportunities, and destroyed endpoint state. A post-compromise recovery design for
intermittent TT&C therefore needs both message-validity protections and explicit recovery-state
management.

The B2 abstraction similarly separates traffic-key exposure from sender/receiver state exposure,
following the state-evolution distinction motivated by ratcheted key-exchange work
[@poettering_roesler_bidirectional_rke; @poettering_roesler_async_rke]. The simulator does not
inherit those constructions' proofs, but the distinction is operationally useful because
different state-loss/exposure conditions produce different recovery possibilities.

## 7.6 Matched-family parity is a boundary, not a negative result

Study A found categorical parity rather than treatment superiority. This is not a failed
comparison. The comparability work intentionally excluded families in which fields or semantics
were not equivalent enough to support a defensible cross-treatment claim.

Within the four retained families, T1 reached the same authorized terminal classifications as
the corresponding abstract baselines. This provides a sanity boundary for the treatment: the
new controller does not obtain its practical fault-handling story by producing obviously
different classifications under the simplest matched cases.

The distinctive T1 contribution appears instead in Study B and Study D, where the experiment can
control faults and parameters inside one implementation without pretending that baseline contact
counts, retry semantics, or transmission metrics are directly equivalent. This separation is
methodologically preferable to constructing a pooled score from non-equivalent mechanisms.

## 7.7 The mixed-schedule panel is descriptive, not a reliability estimate

Study C originally appeared capable of yielding a simple synthetic success proportion. The
post-execution reachability audit demonstrated why that interpretation would be misleading.
Only 77 of 191 scheduled actions were actually reached, 43 schedules applied no fault action,
and seven of the 31 referenced fault-kind/phase cells were not exercised at runtime.

This is not a reason to discard or replace the retained run. The schedule population was
predeclared and executed correctly. Rather, the audit reveals a property of the generator:
scheduling a later-attempt fault is not equivalent to forcing that fault to occur.

The paper should therefore use Study C as secondary evidence about the outcome distribution of a
fixed synthetic schedule population. Deterministic Study B provides the controlled cell-level
fault evidence. A future study designed specifically to estimate outcomes conditional on an
applied fault could use a generator that guarantees runtime reachability or samples from
execution opportunities instead of only precomputing schedule positions.

## 7.8 Implications for mission-aware TT&C recovery

Several concrete design implications follow from the bounded evidence.

First, a recovery transaction should preserve a distinction between **candidate state** and
**operational state**. Candidates should not authorize ordinary command traffic before the
defined activation condition is satisfied.

Second, activation should be paired with explicit, authenticated evidence that can survive
intermittent contact. The experiment shows that losing this evidence can leave the implementation
synchronized but unable to justify a success classification.

Third, message identifiers, epoch/counter checks, and exact transaction binding are useful for
idempotent recovery. The duplicate, stale, and reordered cases completed because invalid material
was rejected without forcing valid progress to be discarded.

Fourth, restart behavior must be part of the protocol design rather than left to the transport
layer. If pending state is volatile, a reset near activation can create an unsafe asymmetric
state. Durable protected state or authenticated transaction restart is therefore a more relevant
mitigation than simply increasing retry count.

Finally, recovery policy should expose security and availability separately to mission decision
logic. A controller deciding whether to resume normal TT&C operations needs to know not only
whether keys/epochs match, but whether the state is trusted, whether command/telemetry verification
succeeded, and whether the system has retained enough evidence to explain the transition.

## 7.9 Role of the formal evidence

The bounded TLA+ work strengthens the study by providing an independently encoded control-state
view and by making adverse outcome paths explicit. The zero-mismatch projection results for the
selected success/adverse witnesses show consistency between those bounded traces and the Python
model over the declared fields.

That evidence should remain supporting rather than headline evidence. The macro-step mapping is
project-defined, the state spaces are finite, and no refinement relation is proven. Phase 13 also
shows that outcome reachability depends on what transitions the abstraction contains: three
outcomes absent from the original model became reachable only when explicit diagnostic
transitions were added.

Accordingly, the formal results are best used to demonstrate transparency and internal
consistency of the modeled control logic, not to elevate the simulator into a proof of
cryptographic or flight-system correctness.

## 7.10 What the paper can and cannot conclude

The retained evidence supports the conclusion that the bounded T1 controller tolerates several
classes of isolated communication fault, rejects stale/replayed protocol material, and
conservatively distinguishes state convergence from verified recovery. It also identifies
endpoint-state loss near activation and confirmation as a principal failure boundary and shows
that additional retransmissions do not repair that class of failure.

The evidence does not support a universal superiority ranking over B0/B1/B2, a real-world
reliability estimate, an optimal retry budget for satellite missions, or a cryptographic
post-compromise-security proof. Those narrower boundaries make the operational findings more,
not less, defensible.
