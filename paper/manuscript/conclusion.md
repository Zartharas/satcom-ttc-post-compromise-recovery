# 10. Conclusion

Post-compromise TT&C recovery requires more than establishing fresh key material. Legitimate
ground and spacecraft endpoints must also agree on which state is operational, survive disrupted
delivery without accepting stale or replayed control material, and produce enough evidence to
justify resuming trusted command operations.

This paper evaluated that operational problem in a bounded, reproducible software model. The
matched-family analysis showed categorical parity between T1 and the corresponding abstract
baselines in the four families where comparison semantics could be defended. That result does not
support a universal treatment-superiority claim; instead, it provides a conservative baseline
for interpreting T1's treatment-specific experiments.

The deterministic T1 study provided the clearest mechanism-level evidence. Isolated loss and
contact closure during recovery-message phases were absorbed within the configured retry budget.
Delay, duplicate, reordered, stale-counter, and stale-replay cases completed while invalid
material was rejected. When post-convergence command or telemetry evidence was lost, the
controller remained synchronized but classified recovery as `INDETERMINATE` rather than
declaring success.

Endpoint restart exposed a different failure class. Restart around COMMIT or CONFIRM can destroy
or separate pending/activated state, producing unsafe asymmetric outcomes. The sensitivity study
reinforced that distinction: increasing the transmission budget from two to three repaired the
repeated omission/contact challenges in the fixed panel, while a fourth opportunity added no
observed benefit and did not repair the COMMIT-stage restart failure. Retransmission can recover
missing messages; it cannot reconstruct protocol state that no longer exists.

The fixed 100-schedule mixed population adds descriptive robustness evidence but also illustrates
the importance of execution-aware coverage. Because many later-attempt scheduled faults were
never reached at runtime, its 74 successful schedules are not interpreted as a fault-conditioned
success rate. The deterministic cell study remains the stronger evidence for explicit fault
coverage.

Bounded TLA+/Python comparisons provide supporting assurance that selected success and adverse
traces agree over the declared abstraction. They do not establish refinement, cryptographic
security, or completeness of the model.

The principal design implication is architectural: post-compromise recovery should separate
candidate state from operational state, bind recovery to monotonic authority/evidence, make
activation and confirmation rules explicit, retain enough protected state to survive restart or
support authenticated re-initiation, and distinguish security, availability, alignment, and
verification when deciding whether normal TT&C control may resume.

Future work should instantiate the recovery-control layer with concrete reviewed cryptographic
mechanisms, evaluate protected persistent-state strategies across endpoint restart, integrate the
logic with representative flight/ground software such as cFS/NOS3, and test it under realistic
link/RF behavior. Those steps would address external and cryptographic validity beyond the
current study. The present contribution is a reproducible experimental foundation for reasoning
about a narrower but operationally consequential question: how trusted TT&C state is restored
without converting key update into lockout or false confidence after compromise.
