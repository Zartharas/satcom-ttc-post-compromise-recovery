---------------------------- MODULE T1Recovery ----------------------------
EXTENDS Integers, Sequences, TLC

CONSTANTS MaxAttempts, InitialGroundEpoch, InitialSpaceEpoch, MaxEpoch

Modes == {"NORMAL", "RECOVERING", "CANDIDATE", "ACTIVATED", "VERIFIED", "EXPIRED"}
Outcomes == {"NONE", "SUCCESS", "INDETERMINATE", "SECURE_DEGRADED", "EXPIRED", "DIVERGED", "AVAILABLE_UNSAFE", "LOCKED"}

VARIABLES
    gMode,
    sMode,
    gEpoch,
    sEpoch,
    gPrevEpoch,
    sPrevEpoch,
    candidateEpoch,
    pending,
    receipt,
    attempts,
    activationCount,
    commandAccepted,
    statusSeen,
    statusDropped,
    verified,
    outcome

vars == <<
    gMode,
    sMode,
    gEpoch,
    sEpoch,
    gPrevEpoch,
    sPrevEpoch,
    candidateEpoch,
    pending,
    receipt,
    attempts,
    activationCount,
    commandAccepted,
    statusSeen,
    statusDropped,
    verified,
    outcome
>>

Null == -1

Init ==
    /\ gMode = "NORMAL"
    /\ sMode = "NORMAL"
    /\ gEpoch = InitialGroundEpoch
    /\ sEpoch = InitialSpaceEpoch
    /\ gPrevEpoch = InitialGroundEpoch
    /\ sPrevEpoch = InitialSpaceEpoch
    /\ candidateEpoch = Null
    /\ pending = FALSE
    /\ receipt = FALSE
    /\ attempts = 0
    /\ activationCount = 0
    /\ commandAccepted = FALSE
    /\ statusSeen = FALSE
    /\ statusDropped = FALSE
    /\ verified = FALSE
    /\ outcome = "NONE"

Prepare ==
    /\ gMode = "NORMAL"
    /\ attempts < MaxAttempts
    /\ gMode' = "RECOVERING"
    /\ pending' = TRUE
    /\ attempts' = attempts + 1
    /\ UNCHANGED <<
        sMode, gEpoch, sEpoch, gPrevEpoch, sPrevEpoch, candidateEpoch,
        receipt, activationCount, commandAccepted, statusSeen,
        statusDropped, verified, outcome
    >>

SelectCandidate ==
    /\ pending
    /\ gMode = "RECOVERING"
    /\ candidateEpoch = Null
    /\ candidateEpoch' = IF gEpoch >= sEpoch THEN gEpoch + 1 ELSE sEpoch + 1
    /\ candidateEpoch' <= MaxEpoch
    /\ gMode' = "CANDIDATE"
    /\ sMode' = "CANDIDATE"
    /\ UNCHANGED <<
        gEpoch, sEpoch, gPrevEpoch, sPrevEpoch, pending, receipt,
        attempts, activationCount, commandAccepted, statusSeen,
        statusDropped, verified, outcome
    >>

Commit ==
    /\ pending
    /\ candidateEpoch # Null
    /\ sMode = "CANDIDATE"
    /\ candidateEpoch > sEpoch
    /\ sPrevEpoch' = sEpoch
    /\ sEpoch' = candidateEpoch
    /\ sMode' = "ACTIVATED"
    /\ receipt' = TRUE
    /\ activationCount' = activationCount + 1
    /\ UNCHANGED <<
        gMode, gEpoch, gPrevEpoch, candidateEpoch, pending, attempts,
        commandAccepted, statusSeen, statusDropped, verified, outcome
    >>

Confirm ==
    /\ receipt
    /\ pending
    /\ gMode = "CANDIDATE"
    /\ candidateEpoch > gEpoch
    /\ gPrevEpoch' = gEpoch
    /\ gEpoch' = candidateEpoch
    /\ gMode' = "ACTIVATED"
    /\ pending' = FALSE
    /\ UNCHANGED <<
        sMode, sEpoch, sPrevEpoch, candidateEpoch, receipt, attempts,
        activationCount, commandAccepted, statusSeen, statusDropped,
        verified, outcome
    >>

AcceptCommand ==
    /\ gMode = "ACTIVATED"
    /\ sMode = "ACTIVATED"
    /\ gEpoch = sEpoch
    /\ commandAccepted' = TRUE
    /\ UNCHANGED <<
        gMode, sMode, gEpoch, sEpoch, gPrevEpoch, sPrevEpoch,
        candidateEpoch, pending, receipt, attempts, activationCount,
        statusSeen, statusDropped, verified, outcome
    >>

ReceiveStatus ==
    /\ commandAccepted
    /\ ~statusDropped
    /\ statusSeen' = TRUE
    /\ UNCHANGED <<
        gMode, sMode, gEpoch, sEpoch, gPrevEpoch, sPrevEpoch,
        candidateEpoch, pending, receipt, attempts, activationCount,
        commandAccepted, statusDropped, verified, outcome
    >>

Verify ==
    /\ commandAccepted
    /\ statusSeen
    /\ gEpoch = sEpoch
    /\ gMode = "ACTIVATED"
    /\ sMode = "ACTIVATED"
    /\ gMode' = "VERIFIED"
    /\ sMode' = "VERIFIED"
    /\ verified' = TRUE
    /\ receipt' = FALSE
    /\ outcome' = "SUCCESS"
    /\ UNCHANGED <<
        gEpoch, sEpoch, gPrevEpoch, sPrevEpoch, candidateEpoch,
        pending, attempts, activationCount, commandAccepted,
        statusSeen, statusDropped
    >>

DropStatus ==
    /\ commandAccepted
    /\ ~statusSeen
    /\ statusDropped' = TRUE
    /\ outcome' = "INDETERMINATE"
    /\ UNCHANGED <<
        gMode, sMode, gEpoch, sEpoch, gPrevEpoch, sPrevEpoch,
        candidateEpoch, pending, receipt, attempts, activationCount,
        commandAccepted, statusSeen, verified
    >>

Retry ==
    /\ pending
    /\ attempts < MaxAttempts
    /\ attempts' = attempts + 1
    /\ UNCHANGED <<
        gMode, sMode, gEpoch, sEpoch, gPrevEpoch, sPrevEpoch,
        candidateEpoch, pending, receipt, activationCount,
        commandAccepted, statusSeen, statusDropped, verified, outcome
    >>

ExpireBeforeActivation ==
    /\ attempts = MaxAttempts
    /\ pending
    /\ ~receipt
    /\ gMode' = "EXPIRED"
    /\ sMode' = "EXPIRED"
    /\ pending' = FALSE
    /\ outcome' = "EXPIRED"
    /\ UNCHANGED <<
        gEpoch, sEpoch, gPrevEpoch, sPrevEpoch, candidateEpoch,
        receipt, attempts, activationCount, commandAccepted,
        statusSeen, statusDropped, verified
    >>

ExpireAfterSpacecraftActivation ==
    /\ attempts = MaxAttempts
    /\ pending
    /\ receipt
    /\ sMode = "ACTIVATED"
    /\ gMode' = "EXPIRED"
    /\ pending' = FALSE
    /\ outcome' = "SECURE_DEGRADED"
    /\ UNCHANGED <<
        sMode, gEpoch, sEpoch, gPrevEpoch, sPrevEpoch, candidateEpoch,
        receipt, attempts, activationCount, commandAccepted,
        statusSeen, statusDropped, verified
    >>

Next ==
    \/ Prepare
    \/ SelectCandidate
    \/ Commit
    \/ Confirm
    \/ AcceptCommand
    \/ ReceiveStatus
    \/ Verify
    \/ DropStatus
    \/ Retry
    \/ ExpireBeforeActivation
    \/ ExpireAfterSpacecraftActivation

Spec == Init /\ [][Next]_vars

TypeOK ==
    /\ gMode \in Modes
    /\ sMode \in Modes
    /\ gEpoch \in 0..MaxEpoch
    /\ sEpoch \in 0..MaxEpoch
    /\ gPrevEpoch \in 0..MaxEpoch
    /\ sPrevEpoch \in 0..MaxEpoch
    /\ candidateEpoch \in {Null} \cup 0..MaxEpoch
    /\ pending \in BOOLEAN
    /\ receipt \in BOOLEAN
    /\ attempts \in 0..MaxAttempts
    /\ activationCount \in 0..1
    /\ commandAccepted \in BOOLEAN
    /\ statusSeen \in BOOLEAN
    /\ statusDropped \in BOOLEAN
    /\ verified \in BOOLEAN
    /\ outcome \in Outcomes

EpochMonotonicity == gEpoch >= gPrevEpoch /\ sEpoch >= sPrevEpoch
CandidateNotAuthority == pending => ~verified
BoundedControlState == attempts <= MaxAttempts /\ activationCount <= 1
NoRollback == gEpoch >= InitialGroundEpoch /\ sEpoch >= InitialSpaceEpoch
AtMostOneSpacecraftActivation == activationCount <= 1
SuccessRequiresEvidence ==
    outcome = "SUCCESS" =>
        verified /\ commandAccepted /\ statusSeen /\ gEpoch = sEpoch
DegradedNotSuccess == outcome = "SECURE_DEGRADED" => ~verified
StatusLossNotDivergence ==
    statusDropped /\ gEpoch = sEpoch => outcome # "DIVERGED"

\* Testing-only false invariant used to demonstrate that the execution pipeline captures
\* an expected TLC counterexample. It is not a claimed protocol property.
NegativeControlNoActivation == activationCount = 0

=============================================================================
