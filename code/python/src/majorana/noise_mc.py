"""IID bit-flip Monte Carlo on growing planar grids.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass

from .complexes import surface_grid
from .gf2_terminalizer import GF2ScheduleStatus, Gf2CocycleClassifier

NOISE_MC_RECEIPT_TAG = "omega.majorana-noise-mc-receipt.v1"


class Lcg:
    """Seedable LCG (Numerical Recipes)."""
    def __init__(self, seed: int) -> None:
        self.state = (seed | 1) & 0xFFFFFFFFFFFFFFFF

    def next_u64(self) -> int:
        self.state = (self.state * 1664525 + 1013904223) & 0xFFFFFFFFFFFFFFFF
        return self.state

    def bernoulli(self, p: float) -> bool:
        if p <= 0.0:
            return False
        if p >= 1.0:
            return True
        thr = int(p * 4294967295)
        return (self.next_u64() & 0xFFFFFFFF) < thr


@dataclass
class NoiseMcReceipt:
    certificate_tag: str
    grid_m: int
    num_edges: int
    num_faces: int
    p: float
    trials: int
    seed: int
    count_exact: int
    count_closed_residual: int
    count_open: int
    frac_exact: float
    frac_closed_residual: float
    frac_open: float
    authority_effect: str = "None"
    notes: str = ""


def run_noise_mc(grid_m: int, p: float, trials: int, seed: int = 42) -> NoiseMcReceipt:
    complex = surface_grid(grid_m, grid_m, False)
    lcg = Lcg(seed)
    c_exact = 0
    c_closed = 0
    c_open = 0

    for _ in range(trials):
        omega = [1 if lcg.bernoulli(p) else 0 for _ in range(complex.num_edges)]
        receipt = Gf2CocycleClassifier.classify(complex.d0, complex.d1, omega)
        if receipt.schedule_status == GF2ScheduleStatus.Exact:
            c_exact += 1
        elif receipt.schedule_status == GF2ScheduleStatus.ClosedResidual:
            c_closed += 1
        elif receipt.schedule_status == GF2ScheduleStatus.OpenObstruction:
            c_open += 1

    f_exact = c_exact / trials if trials > 0 else 0.0
    f_closed = c_closed / trials if trials > 0 else 0.0
    f_open = c_open / trials if trials > 0 else 0.0

    return NoiseMcReceipt(
        certificate_tag=NOISE_MC_RECEIPT_TAG,
        grid_m=grid_m,
        num_edges=complex.num_edges,
        num_faces=complex.num_faces,
        p=p,
        trials=trials,
        seed=seed,
        count_exact=c_exact,
        count_closed_residual=c_closed,
        count_open=c_open,
        frac_exact=f_exact,
        frac_closed_residual=f_closed,
        frac_open=f_open,
        notes="noise MC sweep completed",
    )
