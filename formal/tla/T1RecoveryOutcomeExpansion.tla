-------------------- MODULE T1RecoveryOutcomeExpansion --------------------
EXTENDS T1Recovery

VARIABLE gapCause

GapCauses == {"NONE", "CANDIDATE_KNOWN", "CONFIRM_LOSS", "SENDER_STATE_DELETED"}

expandedVars == <<
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
    outcome,
    gapCause
>>

InitExpanded ==
    /\ Init
    /\ gapCause = "NONE"

PrepareExpanded ==
    /\ Prepare
    /\ UNCHANGED gapCause

SelectCandidateExpanded ==
    /\ SelectCandidate
    /\ UNCHANGED gapCause

CommitExpanded ==
    /\ Commit
    /\ UNCHANGED gapCause

ConfirmExpanded ==
    /\ Confirm
    /\ UNCHANGED gapCause

MarkCandidateKnown ==
    /\ gMode = "CANDIDATE"
    /\ sMode = "CANDIDATE"
    /\ candidateEpoch # Null
    /\ gapCause = "NONE"
    /\ gapCause' = "CANDIDATE_KNOWN"
    /\ UNCHANGED vars

MarkSenderStateDeleted ==
    /\ gMode = "CANDIDATE"
    /\ sMode = "CANDIDATE"
    /\ candidateEpoch # Null
    /\ gapCause = "NONE"
    /\ gapCause' = "SENDER_STATE_DELETED"
    /\ UNCHANGED vars

DivergeOnConfirmLoss ==
    /\ gMode = "CANDIDATE"
    /\ sMode = "CANDIDATE"
    /\ candidateEpoch # Null
    /\ gapCause = "NONE"
    /\ gPrevEpoch' = gEpoch
    /\ gEpoch' = candidateEpoch
    /\ gMode' = "NORMAL"
    /\ sMode' = "EXPIRED"
    /\ pending' = FALSE
    /\ outcome' = "DIVERGED"
    /\ gapCause' = "CONFIRM_LOSS"
    /\ UNCHANGED <<
        sEpoch, sPrevEpoch, candidateEpoch, receipt, attempts,
        activationCount, commandAccepted, statusSeen, statusDropped, verified
        >>

VerifyAvailableUnsafe ==
    /\ gMode = "ACTIVATED"
    /\ sMode = "ACTIVATED"
    /\ gEpoch = sEpoch
    /\ gapCause = "CANDIDATE_KNOWN"
    /\ gMode' = "VERIFIED"
    /\ sMode' = "VERIFIED"
    /\ receipt' = FALSE
    /\ commandAccepted' = TRUE
    /\ statusSeen' = TRUE
    /\ verified' = TRUE
    /\ outcome' = "AVAILABLE_UNSAFE"
    /\ UNCHANGED <<
        gEpoch, sEpoch, gPrevEpoch, sPrevEpoch, candidateEpoch, pending,
        attempts, activationCount, statusDropped, gapCause
        >>

LockAfterSenderAdvance ==
    /\ gMode = "CANDIDATE"
    /\ sMode = "CANDIDATE"
    /\ candidateEpoch # Null
    /\ gapCause = "SENDER_STATE_DELETED"
    /\ gPrevEpoch' = gEpoch
    /\ gEpoch' = candidateEpoch
    /\ gMode' = "NORMAL"
    /\ pending' = FALSE
    /\ outcome' = "LOCKED"
    /\ UNCHANGED <<
        sMode, sEpoch, sPrevEpoch, candidateEpoch, receipt, attempts,
        activationCount, commandAccepted, statusSeen, statusDropped, verified,
        gapCause
        >>

NextExpanded ==
    \/ PrepareExpanded
    \/ SelectCandidateExpanded
    \/ MarkCandidateKnown
    \/ MarkSenderStateDeleted
    \/ CommitExpanded
    \/ ConfirmExpanded
    \/ DivergeOnConfirmLoss
    \/ VerifyAvailableUnsafe
    \/ LockAfterSenderAdvance

SpecExpanded == InitExpanded /\ [][NextExpanded]_expandedVars

TypeOKExpanded == TypeOK /\ gapCause \in GapCauses

\* Testing-only false properties used to obtain bounded diagnostic witnesses.
\* They do not assert model completeness, protocol security, or implementation equivalence.
ReachabilityWitnessNoExpandedDiverged == outcome # "DIVERGED"
ReachabilityWitnessNoExpandedAvailableUnsafe == outcome # "AVAILABLE_UNSAFE"
ReachabilityWitnessNoExpandedLocked == outcome # "LOCKED"

=============================================================================
