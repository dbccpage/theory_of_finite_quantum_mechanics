"""Dual observation maps on one declared complex (Rovelli kill-criterion).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .complexes import ChainComplexGf2
from .gf2_terminalizer import GF2Matrix

DUAL_OBS_RECEIPT_TAG = "omega.majorana-dual-observer-receipt.v1"


@dataclass
class ObservationMap:
    name: str
    matrix: GF2Matrix

    def apply(self, omega: Sequence[int]) -> list[int]:
        if len(omega) != self.matrix.cols:
            raise ValueError(f"omega length {len(omega)} != obs matrix cols {self.matrix.cols}")
        return self.matrix.multiply_vector(omega)

    def residual_weight(self, omega: Sequence[int]) -> int:
        return sum(self.apply(omega))

    def residual_zero(self, omega: Sequence[int]) -> bool:
        return all(b == 0 for b in self.apply(omega))


def observer_face_syndrome(complex: ChainComplexGf2) -> ObservationMap:
    return ObservationMap("O_face_d1", complex.d1)


def observer_first_face_only(complex: ChainComplexGf2) -> ObservationMap:
    if complex.d1.rows == 0:
        raise ValueError("no faces in complex")
    return ObservationMap("O_first_face", GF2Matrix.from_data([complex.d1.data[0]]))


def observer_even_edge_parity(num_edges: int) -> ObservationMap:
    row = [1 if j % 2 == 0 else 0 for j in range(num_edges)]
    return ObservationMap("O_even_edge_parity", GF2Matrix.from_data([row]))


@dataclass
class DualObserverReceipt:
    certificate_tag: str
    complex_name: str
    edge_vector: list[int]
    observer1_name: str
    residual_weight_1: int
    residual_zero_1: bool
    observer2_name: str
    residual_weight_2: int
    residual_zero_2: bool
    agree_on_weight: bool
    agree_on_zero: bool
    authority_effect: str = "None"
    notes: str = ""


def dual_observe(
    complex: ChainComplexGf2,
    omega: Sequence[int],
    obs1: ObservationMap,
    obs2: ObservationMap,
) -> DualObserverReceipt:
    w1 = obs1.residual_weight(omega)
    z1 = obs1.residual_zero(omega)
    w2 = obs2.residual_weight(omega)
    z2 = obs2.residual_zero(omega)
    agree_wt = (w1 == w2)
    agree_z = (z1 == z2)
    return DualObserverReceipt(
        certificate_tag=DUAL_OBS_RECEIPT_TAG,
        complex_name=complex.name,
        edge_vector=list(omega),
        observer1_name=obs1.name,
        residual_weight_1=w1,
        residual_zero_1=z1,
        observer2_name=obs2.name,
        residual_weight_2=w2,
        residual_zero_2=z2,
        agree_on_weight=agree_wt,
        agree_on_zero=agree_z,
        notes="dual observation completed",
    )
