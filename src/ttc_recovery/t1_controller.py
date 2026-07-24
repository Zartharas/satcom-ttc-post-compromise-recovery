from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

from .simulator import Outcome


class T1Mode(str, Enum):
    NORMAL = "NORMAL"
    RECOVERING = "RECOVERING"
    CANDIDATE = "CANDIDATE"
    ACTIVATED = "ACTIVATED"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"


class RecoveryMessageKind(str, Enum):
    PREPARE = "RECOVERY_PREPARE"
    RESPONSE = "RECOVERY_RESPONSE"
    COMMIT = "RECOVERY_COMMIT"
    CONFIRM = "RECOVERY_CONFIRM"


@dataclass(frozen=True)
class RecoveryMessage:
    message_id: str
    kind: RecoveryMessageKind
    spacecraft_id: str
    recovery_id: str
    target_epoch: int
    counter: int
    transcript_ref: str
    authorized_by: str
    candidate_key_ref: Optional[str] = None


@dataclass
class PendingRecovery:
    recovery_id: str
    proposal_epoch: int
    target_epoch: Optional[int]
    counter: int
    transcript_ref: str
    authorized_by: str
    candidate_key_ref: Optional[str]
    created_contact: int
    expires_after_contact: int

    def matches_prepare(self, message: RecoveryMessage) -> bool:
        return (
            message.recovery_id == self.recovery_id
            and message.target_epoch == self.proposal_epoch
            and message.counter == self.counter
            and message.transcript_ref == self.transcript_ref
            and message.authorized_by == self.authorized_by
        )

    def matches_selected(self, message: RecoveryMessage) -> bool:
        return (
            self.target_epoch is not None
            and self.candidate_key_ref is not None
            and message.recovery_id == self.recovery_id
            and message.target_epoch == self.target_epoch
            and message.counter == self.counter
            and message.transcript_ref == self.transcript_ref
            and message.authorized_by == self.authorized_by
            and message.candidate_key_ref == self.candidate_key_ref
        )


@dataclass
class T1Endpoint:
    endpoint_id: str
    epoch: int = 0
    active_key: str = "K0"
    mode: T1Mode = T1Mode.NORMAL
    pending: Optional[PendingRecovery] = None
    activation_receipt: Optional[PendingRecovery] = None
    monotonic_counter: int = 0
    allowed_authorities: Set[str] = field(default_factory=lambda: {"recovery-authority"})
    seen_message_ids: Set[str] = field(default_factory=set)
    retired_keys: Set[str] = field(default_factory=set)
    compromised_keys: Set[str] = field(default_factory=set)

    def activate(self, target_epoch: int, candidate_key_ref: str) -> None:
        if target_epoch <= self.epoch:
            raise ValueError("Recovery activation must advance the active epoch.")
        self.retired_keys.add(self.active_key)
        self.epoch = target_epoch
        self.active_key = candidate_key_ref
        self.mode = T1Mode.ACTIVATED


@dataclass
class RecoveryAuthority:
    authority_id: str = "recovery-authority"
    counter: int = 0
    epoch_floor: int = 0
    compromised: bool = False


@dataclass
class T1Session:
    ground: T1Endpoint
    spacecraft: T1Endpoint
    authority: RecoveryAuthority = field(default_factory=RecoveryAuthority)
    spacecraft_id: str = "spacecraft"
    max_transmissions: int = 3
    candidate_lifetime_contacts: int = 3
    current_contact: int = 0
    event_log: List[Dict[str, object]] = field(default_factory=list)
    verification_complete: bool = False
    attempt_expired: bool = False
    secure_degraded: bool = False
    rejection_reason: Optional[str] = None
    lockout_reason: Optional[str] = None
    last_commit: Optional[RecoveryMessage] = None
    _message_sequence: int = 0

    def log(self, event: str, **details: object) -> None:
        self.event_log.append(
            {
                "event_seq": len(self.event_log),
                "event": event,
                "ground_epoch": self.ground.epoch,
                "spacecraft_epoch": self.spacecraft.epoch,
                **details,
            }
        )

    def _next_message_id(self, label: str) -> str:
        self._message_sequence += 1
        return f"{label}-{self._message_sequence}"

    def _message(
        self,
        kind: RecoveryMessageKind,
        pending: PendingRecovery,
        *,
        target_epoch: int,
        candidate_key_ref: Optional[str],
    ) -> RecoveryMessage:
        return RecoveryMessage(
            message_id=self._next_message_id(kind.value.lower()),
            kind=kind,
            spacecraft_id=self.spacecraft_id,
            recovery_id=pending.recovery_id,
            target_epoch=target_epoch,
            counter=pending.counter,
            transcript_ref=pending.transcript_ref,
            authorized_by=pending.authorized_by,
            candidate_key_ref=candidate_key_ref,
        )

    def _reject(self, endpoint: T1Endpoint, message: RecoveryMessage, reason: str) -> None:
        self.rejection_reason = reason
        endpoint.seen_message_ids.add(message.message_id)
        self.log(
            "t1_message_rejected",
            endpoint=endpoint.endpoint_id,
            message_kind=message.kind.value,
            message_id=message.message_id,
            reason=reason,
        )

    def check_invariants(self) -> None:
        for endpoint in (self.ground, self.spacecraft):
            if endpoint.epoch < 0:
                raise AssertionError("Negative epoch.")
            if endpoint.active_key in endpoint.retired_keys:
                raise AssertionError("Active key cannot be retired.")
            if endpoint.pending is not None:
                if endpoint.pending.proposal_epoch <= 0:
                    raise AssertionError("Proposal epoch must be positive.")
                if (
                    endpoint.pending.target_epoch is not None
                    and endpoint.pending.target_epoch <= endpoint.epoch
                ):
                    raise AssertionError("Selected recovery epoch must advance endpoint state.")
            receipt = endpoint.activation_receipt
            if receipt is not None:
                if receipt.target_epoch != endpoint.epoch:
                    raise AssertionError("Activation receipt epoch must match active epoch.")
                if receipt.candidate_key_ref != endpoint.active_key:
                    raise AssertionError("Activation receipt key must match active key.")
        if self.verification_complete:
            if not self.alignment_state().startswith("SYNC"):
                raise AssertionError("Verified recovery requires endpoint convergence.")
            if self.ground.mode != T1Mode.VERIFIED or self.spacecraft.mode != T1Mode.VERIFIED:
                raise AssertionError("Verified recovery requires VERIFIED endpoint modes.")

    def alignment_state(self) -> str:
        if (
            self.ground.epoch == self.spacecraft.epoch
            and self.ground.active_key == self.spacecraft.active_key
        ):
            return f"SYNC({self.ground.epoch})"
        if self.ground.epoch > self.spacecraft.epoch:
            return "G_AHEAD"
        if self.spacecraft.epoch > self.ground.epoch:
            return "S_AHEAD"
        return "DIVERGED"

    def outcome(self) -> Outcome:
        if self.lockout_reason:
            return Outcome.LOCKED
        if self.secure_degraded:
            return Outcome.SECURE_DEGRADED
        if self.attempt_expired:
            return Outcome.EXPIRED
        alignment = self.alignment_state()
        if alignment.startswith("SYNC"):
            if not self.verification_complete:
                return Outcome.INDETERMINATE
            active = self.ground.active_key
            known = (
                active in self.ground.compromised_keys
                or active in self.spacecraft.compromised_keys
                or self.authority.compromised
            )
            return Outcome.AVAILABLE_UNSAFE if known else Outcome.SUCCESS
        return Outcome.DIVERGED

    def candidate_can_authorize(self, endpoint: T1Endpoint, key_ref: str) -> bool:
        return key_ref == endpoint.active_key and key_ref not in endpoint.compromised_keys

    def start_recovery(
        self,
        recovery_id: str,
        *,
        transcript_ref: Optional[str] = None,
    ) -> RecoveryMessage:
        if self.ground.pending is not None:
            raise RuntimeError("Ground already has a pending recovery.")
        self.authority.counter += 1
        proposal_epoch = max(self.ground.epoch, self.authority.epoch_floor) + 1
        pending = PendingRecovery(
            recovery_id=recovery_id,
            proposal_epoch=proposal_epoch,
            target_epoch=None,
            counter=self.authority.counter,
            transcript_ref=transcript_ref or f"transcript:{recovery_id}",
            authorized_by=self.authority.authority_id,
            candidate_key_ref=None,
            created_contact=self.current_contact,
            expires_after_contact=self.current_contact + self.candidate_lifetime_contacts,
        )
        self.ground.pending = pending
        self.ground.mode = T1Mode.RECOVERING
        message = self._message(
            RecoveryMessageKind.PREPARE,
            pending,
            target_epoch=proposal_epoch,
            candidate_key_ref=None,
        )
        self.log(
            "t1_prepare_sent",
            recovery_id=recovery_id,
            proposed_epoch=proposal_epoch,
            counter=pending.counter,
        )
        self.check_invariants()
        return message

    def retry_prepare(self) -> RecoveryMessage:
        pending = self.ground.pending
        if pending is None:
            raise RuntimeError("No ground recovery is available for prepare retry.")
        message = self._message(
            RecoveryMessageKind.PREPARE,
            pending,
            target_epoch=pending.proposal_epoch,
            candidate_key_ref=None,
        )
        self.log("t1_prepare_retried", recovery_id=pending.recovery_id)
        return message

    def spacecraft_accept_prepare(
        self, message: RecoveryMessage
    ) -> Optional[RecoveryMessage]:
        endpoint = self.spacecraft
        if message.message_id in endpoint.seen_message_ids:
            self._reject(endpoint, message, "duplicate message identifier")
            return None
        if message.kind != RecoveryMessageKind.PREPARE:
            self._reject(endpoint, message, "unexpected message kind")
            return None
        if message.spacecraft_id != self.spacecraft_id:
            self._reject(endpoint, message, "spacecraft identity mismatch")
            return None
        if message.authorized_by not in endpoint.allowed_authorities:
            self._reject(endpoint, message, "recovery authority not allowed")
            return None
        if message.candidate_key_ref is not None:
            self._reject(endpoint, message, "prepare must not carry an installed candidate")
            return None

        existing = endpoint.pending
        if existing is not None:
            if not existing.matches_prepare(message):
                self._reject(endpoint, message, "bounded pending capacity or binding conflict")
                return None
            endpoint.seen_message_ids.add(message.message_id)
            response = self._message(
                RecoveryMessageKind.RESPONSE,
                existing,
                target_epoch=existing.target_epoch or existing.proposal_epoch,
                candidate_key_ref=existing.candidate_key_ref,
            )
            self.log(
                "t1_prepare_retry_accepted",
                recovery_id=existing.recovery_id,
                target_epoch=existing.target_epoch,
            )
            return response

        if message.counter <= endpoint.monotonic_counter:
            self._reject(endpoint, message, "non-monotonic recovery counter")
            return None

        target_epoch = max(message.target_epoch, endpoint.epoch + 1)
        candidate_key_ref = f"T1:{message.recovery_id}:{target_epoch}"
        pending = PendingRecovery(
            recovery_id=message.recovery_id,
            proposal_epoch=message.target_epoch,
            target_epoch=target_epoch,
            counter=message.counter,
            transcript_ref=message.transcript_ref,
            authorized_by=message.authorized_by,
            candidate_key_ref=candidate_key_ref,
            created_contact=self.current_contact,
            expires_after_contact=self.current_contact + self.candidate_lifetime_contacts,
        )
        endpoint.pending = pending
        endpoint.monotonic_counter = message.counter
        endpoint.mode = T1Mode.CANDIDATE
        endpoint.seen_message_ids.add(message.message_id)
        response = self._message(
            RecoveryMessageKind.RESPONSE,
            pending,
            target_epoch=target_epoch,
            candidate_key_ref=candidate_key_ref,
        )
        self.log(
            "t1_prepare_accepted",
            recovery_id=pending.recovery_id,
            proposed_epoch=pending.proposal_epoch,
            target_epoch=target_epoch,
        )
        self.check_invariants()
        return response

    def ground_accept_response(
        self, message: RecoveryMessage
    ) -> Optional[RecoveryMessage]:
        endpoint = self.ground
        pending = endpoint.pending
        if message.message_id in endpoint.seen_message_ids:
            self._reject(endpoint, message, "duplicate message identifier")
            return None
        if message.kind != RecoveryMessageKind.RESPONSE:
            self._reject(endpoint, message, "unexpected message kind")
            return None
        if pending is None:
            self._reject(endpoint, message, "no matching ground recovery")
            return None
        if (
            message.spacecraft_id != self.spacecraft_id
            or message.recovery_id != pending.recovery_id
            or message.counter != pending.counter
            or message.transcript_ref != pending.transcript_ref
            or message.authorized_by != pending.authorized_by
        ):
            self._reject(endpoint, message, "response binding mismatch")
            return None
        if message.target_epoch <= endpoint.epoch or message.candidate_key_ref is None:
            self._reject(endpoint, message, "response did not select a forward candidate")
            return None

        pending.target_epoch = message.target_epoch
        pending.candidate_key_ref = message.candidate_key_ref
        endpoint.mode = T1Mode.CANDIDATE
        endpoint.seen_message_ids.add(message.message_id)
        commit = self._message(
            RecoveryMessageKind.COMMIT,
            pending,
            target_epoch=message.target_epoch,
            candidate_key_ref=message.candidate_key_ref,
        )
        self.last_commit = commit
        self.log(
            "t1_response_accepted",
            recovery_id=pending.recovery_id,
            target_epoch=pending.target_epoch,
        )
        self.check_invariants()
        return commit

    def retry_commit(self) -> RecoveryMessage:
        pending = self.ground.pending
        if pending is None or pending.target_epoch is None or pending.candidate_key_ref is None:
            raise RuntimeError("No selected ground candidate is available for commit retry.")
        commit = self._message(
            RecoveryMessageKind.COMMIT,
            pending,
            target_epoch=pending.target_epoch,
            candidate_key_ref=pending.candidate_key_ref,
        )
        self.last_commit = commit
        self.log("t1_commit_retried", recovery_id=pending.recovery_id)
        return commit

    def spacecraft_accept_commit(
        self, message: RecoveryMessage
    ) -> Optional[RecoveryMessage]:
        endpoint = self.spacecraft
        if message.message_id in endpoint.seen_message_ids:
            self._reject(endpoint, message, "duplicate message identifier")
            return None
        if message.kind != RecoveryMessageKind.COMMIT:
            self._reject(endpoint, message, "unexpected message kind")
            return None

        receipt = endpoint.activation_receipt
        if receipt is not None:
            if not receipt.matches_selected(message):
                self._reject(endpoint, message, "commit conflicts with activation receipt")
                return None
            endpoint.seen_message_ids.add(message.message_id)
            confirm = self._message(
                RecoveryMessageKind.CONFIRM,
                receipt,
                target_epoch=receipt.target_epoch or endpoint.epoch,
                candidate_key_ref=receipt.candidate_key_ref,
            )
            self.log(
                "t1_commit_retry_confirmed",
                recovery_id=receipt.recovery_id,
                target_epoch=receipt.target_epoch,
            )
            return confirm

        pending = endpoint.pending
        if pending is None or not pending.matches_selected(message):
            self._reject(endpoint, message, "commit has no exact pending candidate")
            return None
        if self.current_contact > pending.expires_after_contact:
            self._reject(endpoint, message, "candidate expired before commit")
            return None

        endpoint.seen_message_ids.add(message.message_id)
        endpoint.activate(message.target_epoch, message.candidate_key_ref or "")
        endpoint.activation_receipt = pending
        endpoint.pending = None
        confirm = self._message(
            RecoveryMessageKind.CONFIRM,
            pending,
            target_epoch=message.target_epoch,
            candidate_key_ref=message.candidate_key_ref,
        )
        self.log(
            "t1_spacecraft_activated",
            recovery_id=pending.recovery_id,
            target_epoch=message.target_epoch,
        )
        self.check_invariants()
        return confirm

    def ground_accept_confirm(self, message: RecoveryMessage) -> bool:
        endpoint = self.ground
        pending = endpoint.pending
        if message.message_id in endpoint.seen_message_ids:
            self._reject(endpoint, message, "duplicate message identifier")
            return False
        if message.kind != RecoveryMessageKind.CONFIRM:
            self._reject(endpoint, message, "unexpected message kind")
            return False
        if pending is None or not pending.matches_selected(message):
            self._reject(endpoint, message, "confirmation has no exact pending candidate")
            return False
        if message.target_epoch <= endpoint.epoch:
            self._reject(endpoint, message, "confirmation is not forward")
            return False

        endpoint.seen_message_ids.add(message.message_id)
        endpoint.activate(message.target_epoch, message.candidate_key_ref or "")
        endpoint.pending = None
        self.authority.epoch_floor = max(self.authority.epoch_floor, message.target_epoch)
        self.log(
            "t1_ground_activated",
            recovery_id=message.recovery_id,
            target_epoch=message.target_epoch,
        )
        self.check_invariants()
        return True

    def verify_recovery(
        self,
        *,
        drop_test_command: bool = False,
        drop_status: bool = False,
    ) -> bool:
        if not self.alignment_state().startswith("SYNC"):
            self.log("t1_verification_blocked", reason="endpoints are not synchronized")
            return False
        if self.ground.mode != T1Mode.ACTIVATED or self.spacecraft.mode != T1Mode.ACTIVATED:
            self.log("t1_verification_blocked", reason="activation is incomplete")
            return False
        if drop_test_command:
            self.log("t1_test_command_dropped")
            return False

        active = self.ground.active_key
        if not self.candidate_can_authorize(self.spacecraft, active):
            self.log("t1_test_command_rejected", key_ref=active)
            return False
        self.log("t1_test_command_accepted", key_ref=active)

        if drop_status:
            self.log("t1_status_telemetry_dropped", key_ref=active)
            return False

        self.ground.mode = T1Mode.VERIFIED
        self.spacecraft.mode = T1Mode.VERIFIED
        self.spacecraft.activation_receipt = None
        self.verification_complete = True
        self.authority.epoch_floor = max(self.authority.epoch_floor, self.ground.epoch)
        self.log("t1_recovery_verified", target_epoch=self.ground.epoch)
        self.check_invariants()
        return True

    def expire_attempt(self) -> None:
        activated_only_on_spacecraft = (
            self.spacecraft.activation_receipt is not None
            and self.ground.pending is not None
        )
        if activated_only_on_spacecraft:
            self.ground.pending = None
            self.ground.mode = T1Mode.EXPIRED
            self.spacecraft.activation_receipt = None
            self.secure_degraded = True
            self.log(
                "t1_confirmation_budget_exhausted",
                alignment=self.alignment_state(),
            )
        else:
            self.ground.pending = None
            self.spacecraft.pending = None
            self.ground.mode = T1Mode.EXPIRED
            self.spacecraft.mode = T1Mode.EXPIRED
            self.attempt_expired = True
            self.log("t1_attempt_expired_without_activation")
        self.check_invariants()


def run_bounded_recovery(
    *,
    ground_epoch: int,
    spacecraft_epoch: int,
    authority_epoch_floor: int = 0,
    max_transmissions: int = 3,
    drop_prepare_attempts: int = 0,
    drop_response_attempts: int = 0,
    drop_commit_attempts: int = 0,
    drop_confirm_attempts: int = 0,
    drop_test_command: bool = False,
    drop_status: bool = False,
    compromise_active_keys: bool = False,
    recovery_id: str = "recovery-1",
) -> T1Session:
    same_state = ground_epoch == spacecraft_epoch
    ground_key = f"K{ground_epoch}" if same_state else f"G{ground_epoch}"
    spacecraft_key = f"K{spacecraft_epoch}" if same_state else f"S{spacecraft_epoch}"
    ground = T1Endpoint("ground", epoch=ground_epoch, active_key=ground_key)
    spacecraft = T1Endpoint("spacecraft", epoch=spacecraft_epoch, active_key=spacecraft_key)
    authority = RecoveryAuthority(epoch_floor=authority_epoch_floor)
    session = T1Session(
        ground=ground,
        spacecraft=spacecraft,
        authority=authority,
        max_transmissions=max_transmissions,
    )

    if compromise_active_keys:
        ground.compromised_keys.add(ground.active_key)
        spacecraft.compromised_keys.add(spacecraft.active_key)

    prepare = session.start_recovery(recovery_id)
    response: Optional[RecoveryMessage] = None
    prepare_drops = drop_prepare_attempts
    response_drops = drop_response_attempts

    for attempt in range(max_transmissions):
        if attempt > 0:
            prepare = session.retry_prepare()
        if prepare_drops > 0:
            prepare_drops -= 1
            session.log("t1_prepare_dropped", attempt=attempt + 1)
            continue
        response = session.spacecraft_accept_prepare(prepare)
        if response is None:
            break
        if response_drops > 0:
            response_drops -= 1
            session.log("t1_response_dropped", attempt=attempt + 1)
            response = None
            continue
        break

    if response is None:
        session.expire_attempt()
        return session

    commit = session.ground_accept_response(response)
    if commit is None:
        session.expire_attempt()
        return session

    confirmed = False
    commit_drops = drop_commit_attempts
    confirm_drops = drop_confirm_attempts

    for attempt in range(max_transmissions):
        if attempt > 0:
            commit = session.retry_commit()
        if commit_drops > 0:
            commit_drops -= 1
            session.log("t1_commit_dropped", attempt=attempt + 1)
            continue
        confirm = session.spacecraft_accept_commit(commit)
        if confirm is None:
            break
        if confirm_drops > 0:
            confirm_drops -= 1
            session.log("t1_confirm_dropped", attempt=attempt + 1)
            continue
        confirmed = session.ground_accept_confirm(confirm)
        if confirmed:
            break

    if not confirmed:
        session.expire_attempt()
        return session

    session.verify_recovery(
        drop_test_command=drop_test_command,
        drop_status=drop_status,
    )
    return session


__all__ = [
    "PendingRecovery",
    "RecoveryAuthority",
    "RecoveryMessage",
    "RecoveryMessageKind",
    "T1Endpoint",
    "T1Mode",
    "T1Session",
    "run_bounded_recovery",
]
