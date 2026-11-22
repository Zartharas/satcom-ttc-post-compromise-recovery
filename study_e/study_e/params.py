from dataclasses import dataclass
from fractions import Fraction
from .rules import PERSIST_LEVELS, ACTIVATIONS


@dataclass(frozen=True)
class Params:
    p: object          # per-message loss probability (float or Fraction)
    K: int             # message opportunities (slots) per contact
    B: int             # maximum transmissions for the attempt (all messages, both directions)
    L: int             # candidate lifetime in contacts
    r: object = 0      # per-contact-boundary spacecraft restart probability
    persist: str = "journal"
    activation: str = "local"
    ge: object = None  # None = i.i.d. loss. Else (a, b, p_bad): Gilbert-Elliott channel, a=P(good->bad), b=P(bad->good)
                       # per transmission slot; p is the GOOD-state loss; p_bad the BAD-state loss. The channel state is
                       # redrawn from the stationary law at the start of every contact (contacts are separated in time).

    def __post_init__(self):
        if not (0 <= self.p <= 1 and 0 <= self.r <= 1):
            raise ValueError("p and r must be in [0,1]")
        if self.K < 1 or self.B < 1 or self.L < 1:
            raise ValueError("K, B, L must be >= 1")
        if self.ge is not None:
            a, b, pb = self.ge
            if not (0 <= a <= 1 and 0 <= b <= 1 and 0 <= pb <= 1 and a + b > 0):
                raise ValueError("bad ge parameters")
        if self.persist not in PERSIST_LEVELS or self.activation not in ACTIVATIONS:
            raise ValueError("bad persist/activation")
