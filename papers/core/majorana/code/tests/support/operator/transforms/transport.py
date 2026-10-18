"""CODA-MUR transport coherence (chi_F, ChiBoxSquare, TriangleWitness, PentagonWitness).

AuthorityEffect: None.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Sequence


@dataclass
class ChiBoxSquare:
    chi_h_top: Any = None
    chi_h_bottom: Any = None
    chi_v_left: Any = None
    chi_v_right: Any = None
    q_F: float = 0.0
    licensed: bool = True
    authority_effect: str = "None"

    def verify(self, test_input: Any) -> Any:
        top_right = self.chi_v_right(self.chi_h_top(test_input))
        left_bottom = self.chi_h_bottom(self.chi_v_left(test_input))
        if top_right == left_bottom:
            return True
        return DiagonalTransportRefusal(reason="Square does not commute")


@dataclass
class TriangleWitness:
    maps: Any = field(default_factory=list)
    witness_id: str = "triangle_witness_001"
    is_valid: bool = True
    authority_effect: str = "None"

    def __init__(
        self,
        maps: Any = None,
        witness_id: str = "triangle_witness_001",
        is_valid: bool = True,
        authority_effect: str = "None",
    ):
        self.maps = maps or []
        self.witness_id = witness_id
        self.is_valid = is_valid
        self.authority_effect = authority_effect

    def verify(self, test_input: Any) -> bool:
        if len(self.maps) < 3:
            return False
        map0, map1, map2 = self.maps[0], self.maps[1], self.maps[2]
        return map2(map0(test_input)) == map1(test_input)


@dataclass
class PentagonWitness:
    maps: Any = field(default_factory=list)
    witness_id: str = "pentagon_witness_001"
    is_valid: bool = True
    authority_effect: str = "None"

    def __init__(
        self,
        maps: Any = None,
        witness_id: str = "pentagon_witness_001",
        is_valid: bool = True,
        authority_effect: str = "None",
    ):
        self.maps = maps or []
        self.witness_id = witness_id
        self.is_valid = is_valid
        self.authority_effect = authority_effect

    def verify(self, test_input: Any) -> bool:
        if len(self.maps) < 5:
            return False
        m0, m1, m2, m3, m4 = self.maps
        left = m4(m3(m0(test_input)))
        right = m2(m1(test_input))
        return left == right


@dataclass
class RefusedTransport:
    reason: str
    authority_effect: str = "Refused"


@dataclass
class DiagonalTransportRefusal:
    reason: str
    authority_effect: str = "Refused"


def chi_F(q_F: float, context: Optional[Any] = None) -> Any:
    """CODA-MUR transport licensing functional chi_F."""
    if q_F == 0.0:
        return True
    return RefusedTransport(reason=f"q_F non-zero ({q_F})", authority_effect="Refused")
