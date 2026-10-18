"""Local-Green / Global-Red (LGGR) diagnostic witness on GF(2) schedules.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .gf2_terminalizer import (
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
    Gf2ScheduleReceipt,
)


@dataclass
class LggrWitness:
    local_green: bool
    global_red: bool
    is_lggr: bool
    d1_omega: list[int]
    certificate: Gf2ScheduleReceipt


def apply_d1(d1: GF2Matrix, omega: Sequence[int]) -> list[int]:
    return d1.multiply_vector(omega)


def detect_lggr(d0: GF2Matrix, d1: GF2Matrix, omega: Sequence[int]) -> LggrWitness:
    cert = Gf2CocycleClassifier.classify(d0, d1, omega)
    d1_omega = apply_d1(d1, omega)
    local_green = all(x == 0 for x in d1_omega)
    global_red = (cert.schedule_status == GF2ScheduleStatus.ClosedResidual)
    return LggrWitness(
        local_green=local_green,
        global_red=global_red,
        is_lggr=local_green and global_red,
        d1_omega=d1_omega,
        certificate=cert,
    )
