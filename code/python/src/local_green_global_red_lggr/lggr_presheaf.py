"""Local-Green / Global-Red (LGGR) path-kernel composition defects and detector adequacy diagnostics.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class LggrGluingReport:
    """Summary of local context consistency vs. global section or path-composition gluing defect."""

    local_green: bool
    global_red: bool
    gluing_defect_l1: Fraction
    holonomy_residue: int


def matrix_multiply_2x2(
    a: Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]],
    b: Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]],
) -> Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]]:
    """Exact 2x2 rational matrix multiplication."""
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ),
    )


def evaluate_path_kernel_gluing(
    k_ab: Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]],
    k_bc: Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]],
    declared_k_ac: Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]],
) -> Fraction:
    """Compute exact L1 gluing defect ||K_bc K_ab - K_ac||_1 across a 2-step boundary slice."""
    composed = matrix_multiply_2x2(k_bc, k_ab)
    defect = Fraction(0)
    for r in range(2):
        for c in range(2):
            defect += abs(composed[r][c] - declared_k_ac[r][c])
    return defect


def evaluate_cyclic_parity_lggr(
    edge_parities: Sequence[int],
    local_Pairwise_consistent: bool = True,
) -> LggrGluingReport:
    """Evaluate Local-Green / Global-Red status on a finite cycle of Z/2Z parity or holonomy constraints."""
    if not edge_parities:
        raise ValueError("edge_parities must be non-empty")
    holonomy = sum(edge_parities) % 2
    local_green = bool(local_Pairwise_consistent)
    global_red = local_green and (holonomy != 0)
    return LggrGluingReport(
        local_green=local_green,
        global_red=global_red,
        gluing_defect_l1=Fraction(holonomy),
        holonomy_residue=holonomy,
    )
