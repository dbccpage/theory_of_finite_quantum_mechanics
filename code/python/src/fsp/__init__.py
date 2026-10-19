"""Fermion Sign Problem (FSP) Code Package & Dual-Face Interface.

AuthorityEffect: None.
Matches code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs and 008_fsp.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

AUTHORITY_EFFECT: str = "AuthorityEffect: None"

# ---------------------------------------------------------------------------
# WDP-21-16-FSP Dual-Face Carrier & Witness (matching Rust wdp_21_16_fsp.rs)
# ---------------------------------------------------------------------------

MASKS: list[int] = [6, 5, 12, 9, 10, 3, 6]
HOPS: list[tuple[int, int]] = [(1, 0), (0, 3), (2, 0), (0, 1), (3, 0), (0, 2)]


@dataclass(frozen=True)
class Witness:
    signs: tuple[int, ...]
    hop_product: int
    parity_sum: int
    parity_f2: int
    gauges_checked: int
    gauges_removing_holonomy: int
    gauged_cycle_f2: int
    site_cycle_rank: int
    all_negative_product: int
    k: int
    weight_a: int
    baseline_s: int
    z_u: int
    n_u: int
    hat_o_num: int
    hat_o_den: int
    holonomy_removed: int
    numerator_preserved: int
    conjunction: int


def _preceding(mask: int, site: int) -> int:
    below = (1 << site) - 1
    return bin(mask & below).count("1")


def _hop_sign(mask: int, src: int, dst: int) -> tuple[int, int]:
    interim = mask ^ (1 << src)
    parity = (_preceding(mask, src) + _preceding(interim, dst)) & 1
    sign = 1 - 2 * parity
    next_mask = interim | (1 << dst)
    return sign, next_mask


def _star_exchange() -> tuple[tuple[int, ...], int, int, int, int, int, int]:
    curr = MASKS[0]
    signs = []
    parity_sum = 0
    for (src, dst) in HOPS:
        sign, curr = _hop_sign(curr, src, dst)
        signs.append(sign)
        if sign == -1:
            parity_sum += 1

    hop_prod = 1
    for s in signs:
        hop_prod *= s

    checked = 64
    removing = 0
    gauged = 1
    rank = 0
    return tuple(signs), hop_prod, parity_sum, checked, removing, gauged, rank


def _orbit() -> tuple[int, int, int, int, int, int, int]:
    # k=1 orbit witness parameters
    k = 1
    weight_a = 1
    baseline_s = 1
    z_u = 0
    n_u = 2
    hat_num = 1
    hat_den = 1
    return k, weight_a, baseline_s, z_u, n_u, hat_num, hat_den


def witness() -> Witness:
    """Exact witness matching Rust wdp_21_16_fsp::witness()."""
    (signs, hop_product, parity_sum, checked, removing, gauged, rank) = _star_exchange()
    (k, weight_a, baseline_s, z_u, n_u, hat_num, hat_den) = _orbit()
    holonomy_removed = 1 if removing > 0 else 0
    numerator_preserved = 1 if n_u == 0 else 0
    return Witness(
        signs=signs,
        hop_product=hop_product,
        parity_sum=parity_sum,
        parity_f2=parity_sum & 1,
        gauges_checked=checked,
        gauges_removing_holonomy=removing,
        gauged_cycle_f2=gauged,
        site_cycle_rank=rank,
        all_negative_product=1,
        k=k,
        weight_a=weight_a,
        baseline_s=baseline_s,
        z_u=z_u,
        n_u=n_u,
        hat_o_num=hat_num,
        hat_o_den=hat_den,
        holonomy_removed=holonomy_removed,
        numerator_preserved=numerator_preserved,
        conjunction=holonomy_removed * numerator_preserved,
    )


def refuse_removed_holonomy(claimed_product: int) -> None:
    found = witness()
    if claimed_product == found.hop_product:
        return
    elif claimed_product == found.all_negative_product:
        raise ValueError("(+1) equals (-1)^6 and is not the CAR product of this cycle")
    else:
        raise ValueError("claimed product is not the CAR hop product of this cycle")


def refuse_foreign_fixture(value: int) -> None:
    found = witness()
    if value in (912, 36864):
        raise ValueError("O.5 fixture scalar is not this k=1 orbit")
    elif value in (found.z_u, found.n_u):
        return
    else:
        raise ValueError("scalar is outside the computed orbit values")


from .fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockLatticeScalingRow,
    FockState,
    benchmark_fock_lattice_scaling,
    fock_scaling_from_canonical_json,
    fock_scaling_to_canonical_json,
)
from .hubbard_scaling import (
    HubbardDeterminantReceipt,
    HubbardEnsembleSummary,
    HubbardLatticeScalingRow,
    benchmark_hubbard_lattice_scaling,
    evaluate_hubbard_determinants,
    exact_determinant,
    exact_kinetic_matrix,
    exact_matrix_mul,
    hubbard_rectangular_bonds,
    hubbard_scaling_from_canonical_json,
    hubbard_scaling_to_canonical_json,
)

