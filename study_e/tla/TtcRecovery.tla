---- MODULE TtcRecovery ----
\* Reachability model of the Study E single-attempt exchange (support check only; TLC computes no probabilities).
\* Written separately from rules.py/model.py/sim.py but by the same author: independence is limited.
EXTENDS Naturals
VARIABLES K, B, L, Pers, Act, step, tx, c, slot, ph, out, T
vars == <<K, B, L, Pers, Act, step, tx, c, slot, ph, out, T>>

SThr(a) == IF a = "local" THEN 3 ELSE 5
SAct(s, a) == s >= SThr(a)
GAct(s) == s >= 4
Cls(s, a) ==
  IF s >= 6 THEN "SUCCESS"
  ELSE IF SAct(s, a) /\ GAct(s) THEN "INDETERMINATE"
  ELSE IF SAct(s, a) THEN "DIVERGED_S_AHEAD"
  ELSE IF GAct(s) THEN "DIVERGED_G_AHEAD"
  ELSE "EXPIRED_OLD"
Survives == Pers = "journal" \/ (Pers = "commit" /\ SAct(step, Act))

Init == /\ K \in 1..3 /\ B \in 1..8 /\ L \in 1..3
        /\ Pers \in {"volatile", "commit", "journal"} /\ Act \in {"local", "gated"}
        /\ step = 0 /\ tx = 0 /\ c = 1 /\ slot = 0 /\ ph = "slot" /\ out = "none" /\ T = 0

Send(ok) ==
  /\ ph = "slot"
  /\ LET s2 == IF ok THEN step + 1 ELSE step IN
     /\ tx' = tx + 1 /\ step' = s2 /\ slot' = slot + 1
     /\ \/ /\ s2 >= 6 /\ out' = "SUCCESS" /\ T' = c /\ ph' = "done"
        \/ /\ s2 < 6 /\ tx + 1 >= B /\ out' = Cls(s2, Act) /\ T' = c /\ ph' = "done"
        \/ /\ s2 < 6 /\ tx + 1 < B /\ slot + 1 >= K /\ ph' = "boundary" /\ UNCHANGED <<out, T>>
        \/ /\ s2 < 6 /\ tx + 1 < B /\ slot + 1 < K /\ ph' = "slot" /\ UNCHANGED <<out, T>>
  /\ UNCHANGED <<K, B, L, Pers, Act, c>>

Boundary ==
  /\ ph = "boundary"
  /\ \/ /\ c = L /\ out' = Cls(step, Act) /\ T' = c /\ ph' = "done" /\ UNCHANGED <<step, tx, c, slot>>
     \/ /\ c < L /\ c' = c + 1 /\ slot' = 0 /\ ph' = "slot" /\ UNCHANGED <<step, tx, out, T>>
     \/ /\ c < L /\ Survives /\ c' = c + 1 /\ slot' = 0 /\ ph' = "slot" /\ UNCHANGED <<step, tx, out, T>>
     \/ /\ c < L /\ ~Survives /\ GAct(step) /\ out' = "DIVERGED_G_AHEAD" /\ T' = c /\ ph' = "done" /\ UNCHANGED <<step, tx, c, slot>>
     \/ /\ c < L /\ ~Survives /\ ~GAct(step) /\ step' = 0 /\ c' = c + 1 /\ slot' = 0 /\ ph' = "slot" /\ UNCHANGED <<tx, out, T>>
  /\ UNCHANGED <<K, B, L, Pers, Act>>

Done == ph = "done" /\ UNCHANGED vars
Next == Send(TRUE) \/ Send(FALSE) \/ Boundary \/ Done
Spec == Init /\ [][Next]_vars
====
