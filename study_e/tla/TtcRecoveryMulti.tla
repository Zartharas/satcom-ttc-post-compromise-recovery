---- MODULE TtcRecoveryMulti ----
\* Multi-attempt reachability model (support only). An attempt ending EXPIRED_OLD before horizon H is retried from the
\* next contact with fresh budget/lifetime; every other end is terminal. Same-author caveat as TtcRecovery.tla.
EXTENDS Naturals
VARIABLES K, B, L, H, Pers, Act, step, tx, c, slot, a0, A, ph, out, T
vars == <<K, B, L, H, Pers, Act, step, tx, c, slot, a0, A, ph, out, T>>

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

Init == /\ K \in 1..3 /\ B \in 1..8 /\ L \in 1..3 /\ H \in 1..6
        /\ Pers \in {"volatile", "commit", "journal"} /\ Act \in {"local", "gated"}
        /\ step = 0 /\ tx = 0 /\ c = 1 /\ slot = 0 /\ a0 = 1 /\ A = 1 /\ ph = "slot" /\ out = "none" /\ T = 0

Finish(o, s2, t2) == /\ out' = o /\ T' = c /\ ph' = "done" /\ step' = s2 /\ tx' = t2 /\ UNCHANGED <<c, slot, a0, A>>
Retry == /\ step' = 0 /\ tx' = 0 /\ c' = c + 1 /\ slot' = 0 /\ a0' = c + 1 /\ A' = A + 1 /\ ph' = "slot" /\ UNCHANGED <<out, T>>
FinishOrRetry(o, s2, t2) == IF o = "EXPIRED_OLD" /\ c < H THEN Retry ELSE Finish(o, s2, t2)

Send(ok) ==
  /\ ph = "slot"
  /\ LET s2 == IF ok THEN step + 1 ELSE step IN
     \/ /\ s2 >= 6 /\ Finish("SUCCESS", s2, tx + 1)
     \/ /\ s2 < 6 /\ tx + 1 >= B /\ FinishOrRetry(Cls(s2, Act), s2, tx + 1)
     \/ /\ s2 < 6 /\ tx + 1 < B /\ step' = s2 /\ tx' = tx + 1 /\ slot' = slot + 1 /\ UNCHANGED <<c, a0, A, out, T>>
        /\ IF slot + 1 >= K THEN ph' = "boundary" ELSE ph' = "slot"
  /\ UNCHANGED <<K, B, L, H, Pers, Act>>

AttemptOver == (c - a0 + 1 >= L) \/ (c >= H)

Boundary ==
  /\ ph = "boundary"
  /\ \/ /\ AttemptOver /\ FinishOrRetry(Cls(step, Act), step, tx)
     \/ /\ ~AttemptOver /\ c' = c + 1 /\ slot' = 0 /\ ph' = "slot" /\ UNCHANGED <<step, tx, a0, A, out, T>>
     \/ /\ ~AttemptOver /\ Survives /\ c' = c + 1 /\ slot' = 0 /\ ph' = "slot" /\ UNCHANGED <<step, tx, a0, A, out, T>>
     \/ /\ ~AttemptOver /\ ~Survives /\ GAct(step) /\ Finish("DIVERGED_G_AHEAD", step, tx)
     \/ /\ ~AttemptOver /\ ~Survives /\ ~GAct(step) /\ step' = 0 /\ c' = c + 1 /\ slot' = 0 /\ ph' = "slot" /\ UNCHANGED <<tx, a0, A, out, T>>
  /\ UNCHANGED <<K, B, L, H, Pers, Act>>

Done == ph = "done" /\ UNCHANGED vars
Next == Send(TRUE) \/ Send(FALSE) \/ Boundary \/ Done
Spec == Init /\ [][Next]_vars
====
