"""Value types for the wired operator composition."""

import hashlib
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class V(Enum):
    """Anti-cheat violation types (OE003-02)."""

    DEG = auto()
    LIFT = auto()
    ANOM = auto()
    SKEL = auto()
    DET = auto()
    FUDH = auto()


@dataclass
class AC:
    """Adapter contract with its loss ledger (OE002-02)."""

    s: str
    t: str
    ll: List[str] = field(default_factory=list)
    ok: bool = True

    @property
    def d(self) -> bool:
        return bool(self.ll)


@dataclass
class CC:
    """Nine-conjunct continuation predicate (OE003-01)."""

    o: bool = False
    w: bool = False
    c: bool = True
    a: bool = True
    d: bool = True
    m: bool = True
    k: bool = True
    b: bool = True
    g: bool = False

    def v(self) -> bool:
        return (
            self.o
            and self.w
            and self.c
            and self.a
            and self.d
            and self.m
            and self.k
            and self.b
            and not self.g
        )


@dataclass
class AX:
    """Anti-cheat state tracker."""

    fp: set = field(default_factory=set)
    dw: int = 1
    sk: str = ""
    n0: int = 1

    def chk(
        self,
        new_deg: int,
        has_ndim_obl: bool,
        has_same_carrier_repair: bool,
        r_hash: str,
        sk_hash: str,
        det_revalidated: bool,
        claims_above_n0: bool,
        n0_resolved: bool,
    ) -> List[V]:
        violations: List[V] = []
        if new_deg > self.dw and not has_ndim_obl:
            violations.append(V.DEG)
        if new_deg > self.dw and has_same_carrier_repair:
            violations.append(V.LIFT)
        if r_hash in self.fp:
            violations.append(V.ANOM)
        if self.sk and sk_hash != self.sk:
            violations.append(V.SKEL)
        if new_deg > self.dw and not det_revalidated:
            violations.append(V.DET)
        if claims_above_n0 and not n0_resolved:
            violations.append(V.FUDH)
        self.fp.add(r_hash)
        if new_deg > self.dw:
            self.dw = new_deg
        self.sk = sk_hash
        return violations


class L(Enum):
    """Eight-letter DDA alphabet (OE010-09)."""

    E = "E"
    R = "R"
    C = "C"
    I = "I"
    Lm = "L"
    D = "D"
    M = "M"
    T = "T"


@dataclass
class TP:
    """DDA tape state (OE010-10)."""

    t: List[str] = field(default_factory=list)
    h: str = "G0"

    def w(self, letter: str, receipt: str) -> str:
        self.t.append(letter)
        payload = f"{len(self.t)}:{letter}:{receipt}:{self.h}"
        self.h = hashlib.sha256(payload.encode()).hexdigest()
        return self.h

    @property
    def done(self) -> bool:
        return bool(self.t) and self.t[-1] == "T"


@dataclass
class BG:
    """Operation budget tracker (OE003-03)."""

    bt: float = 100.0
    dc: float = 1.0
    n: int = 0

    @property
    def mx(self) -> int:
        return int(self.bt / self.dc) if self.dc > 0 else 0

    @property
    def ok(self) -> bool:
        return self.n < self.mx

    def spend(self) -> bool:
        if not self.ok:
            return False
        self.n += 1
        return True


@dataclass
class LG:
    """LGGR trilogy closure gate."""

    gr: bool = False
    ga: bool = False
    gt: bool = False
    ge: bool = False

    @property
    def el(self) -> bool:
        return self.gr and self.ga and self.gt and self.ge


__all__ = ["AC", "AX", "BG", "CC", "L", "LG", "TP", "V"]
