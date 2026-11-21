"""Protocol rules used by the exact DP (model.py). The path simulator (sim.py) re-implements
these rules independently on purpose, so that disagreement exposes a modelling bug.

Protocol: six sequential messages m1..m6 on one link, one transmission per slot.
  m1 G->S PREPARE, m2 S->G RESPONSE, m3 G->S COMMIT, m4 S->G CONFIRM,
  m5 G->S TEST_COMMAND, m6 S->G STATUS_TELEMETRY.
A message is transmitted only after the previous one was delivered; a lost message is retried
in the next slot and consumes budget. 'step' = number of messages delivered so far.
Ground activates the new epoch on receipt of m4. The spacecraft activates on receipt of m3
('local' completion) or m5 ('gated' on authenticated status). SUCCESS = m6 delivered.
"""
N_STEPS = 6
G_ACT_STEP = 4
S_ACT_STEP = {"local": 3, "gated": 5}
OUTCOMES = ("SUCCESS", "INDETERMINATE", "EXPIRED_OLD", "DIVERGED_S_AHEAD", "DIVERGED_G_AHEAD")
PERSIST_LEVELS = ("volatile", "commit", "journal")
ACTIVATIONS = ("local", "gated")


def classify(step, activation):
    """Terminal class when the attempt ends (budget exhausted or lifetime over) at `step`."""
    if step >= N_STEPS:
        return "SUCCESS"
    s_active = step >= S_ACT_STEP[activation]
    g_active = step >= G_ACT_STEP
    if s_active and g_active:
        return "INDETERMINATE"
    if s_active:
        return "DIVERGED_S_AHEAD"
    if g_active:
        return "DIVERGED_G_AHEAD"
    return "EXPIRED_OLD"


def restart_effect(step, persist, activation):
    """Spacecraft restart at a contact boundary. Returns ('CONTINUE', new_step) or ('TERMINAL', outcome).

    journal : candidate and activation are durable; nothing is lost.
    commit  : activation is persisted when it happens; the pending candidate is volatile.
    volatile: candidate and activation are lost until the exchange completes (m6).
    If the spacecraft loses its candidate/activation while ground has already activated,
    ground is ahead and cannot reach the spacecraft: terminal DIVERGED_G_AHEAD.
    Otherwise the handshake restarts from m1 (budget and lifetime keep running).
    """
    s_active = step >= S_ACT_STEP[activation]
    g_active = step >= G_ACT_STEP
    if persist == "journal":
        return ("CONTINUE", step)
    if persist == "commit":
        if s_active:
            return ("CONTINUE", step)
    elif persist == "volatile":
        pass
    else:
        raise ValueError(persist)
    if g_active:
        return ("TERMINAL", "DIVERGED_G_AHEAD")
    return ("CONTINUE", 0)
