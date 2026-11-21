"""Study G wrapper: give T1's TEST_COMMAND and STATUS_TELEMETRY steps a retransmission budget.

Composition by subclassing the Part I experiment runner. Nothing under src/ is edited.
The Part I runner calls ``_pre_delivery(phase, 1, None)`` exactly once for each of the two
verification steps and then calls ``T1Session.verify_recovery`` with the resulting drop flags.
This subclass intercepts that single call and, when the verification budget is > 1, makes up
to ``verification_budget`` transmissions of the same step (attempts 1..budget), stopping at
the first delivered one. The result is returned to the unmodified runner as "delivered" or
"dropped". With verification_budget == 1 the override defers to the parent unchanged.
Recovery-message steps (PREPARE, RESPONSE, COMMIT, CONFIRM) are untouched: they already use
``max_transmissions`` (3) in Part I.
"""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from ttc_recovery.fault_metrics import (
    ExperimentPhase,
    FaultAction,
    FaultKind,
    SeededExperimentConfig,
    _ExperimentRunner,
    _active_key_compromised,
    _availability_state,
    _security_state,
)
from ttc_recovery.t1_controller import RecoveryMessage, T1Session

VERIFICATION_PHASES = (ExperimentPhase.TEST_COMMAND, ExperimentPhase.STATUS_TELEMETRY)


class T1VerificationRetryRunner(_ExperimentRunner):
    def __init__(self, config: SeededExperimentConfig, schedule: Sequence[FaultAction],
                 verification_budget: int = 1) -> None:
        if verification_budget < 1:
            raise ValueError("verification_budget must be >= 1")
        super().__init__(config, schedule)
        self.verification_budget = verification_budget

    def _pre_delivery(self, phase: ExperimentPhase, attempt: int,
                      message: Optional[RecoveryMessage]) -> bool:
        if phase in VERIFICATION_PHASES and attempt == 1 and self.verification_budget > 1:
            for a in range(1, self.verification_budget + 1):
                if a > 1:
                    # the parent already counted transmission 1
                    self.transmissions[phase] += 1
                    self.session.log("study_g_verification_retransmit", phase=phase.value, attempt=a)
                if super()._pre_delivery(phase, a, message):
                    return True
            return False
        return super()._pre_delivery(phase, attempt, message)


def run_with_verification_budget(config: SeededExperimentConfig, schedule: Sequence[FaultAction],
                                 verification_budget: int) -> Dict[str, object]:
    runner = T1VerificationRetryRunner(config, schedule, verification_budget)
    session: T1Session = runner.run()
    return {
        "outcome": session.outcome().value,
        "alignment": session.alignment_state(),
        "security_state": _security_state(session),
        "availability_state": _availability_state(session),
        "verification_complete": session.verification_complete,
        "command_accepted": any(e.get("event") == "t1_test_command_accepted" for e in session.event_log),
        "telemetry_complete": any(e.get("event") == "t1_recovery_verified" for e in session.event_log),
        "total_transmissions": sum(runner.transmissions.values()),
        "divergent_contact_windows": runner.divergent_contacts,
        "active_key_compromised": _active_key_compromised(session),
        # exposure at end: does the spacecraft / ground still run on the attacker-known key?
        "spacecraft_on_compromised_key": session.spacecraft.active_key in session.spacecraft.compromised_keys,
        "ground_on_compromised_key": session.ground.active_key in session.ground.compromised_keys,
        "_event_log": session.event_log,
    }
