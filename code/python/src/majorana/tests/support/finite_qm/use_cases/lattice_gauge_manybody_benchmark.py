"""Campaign C500 Block 09: Finite Many-Body and Lattice-Gauge Bridge.

Mechanizes:
1. Benchmark 1: Finite 1D Transverse-Field Ising Model (TFIM) L=2:
   - H = -J Z_1 Z_2 - h (X_1 + X_2).
   - Exact algebraic spectrum at J=1, h=1: E in {-sqrt(5), -1, 1, sqrt(5)}.
   - Ground state E_0 = -sqrt(5); gap above the ground state is sqrt(5)-1.
2. Benchmark 2: Finite Z_2 Lattice Gauge Plaquette:
   - 4 boundary links l in {1, 2, 3, 4} with Pauli operators.
   - Gauss-law generators at 4 vertices: G_v = prod_{l in star(v)} sigma^x_l = +1.
   - Plaquette Hamiltonian H = -K (sigma^z_1 sigma^z_2 sigma^z_3 sigma^z_4) - g sum_l sigma^x_l.
   - Proof of gauge invariance: [H, G_v] = 0 for all v.
   - Strict preservation of physical subspace H_phys.
3. Separation of 3 continuum scaling obligations:
   - Large-volume error Delta_vol(L) as L -> infty (Thermodynamic limit).
   - Gauge Hilbert space truncation error Delta_trunc(Lambda) as Lambda -> infty.
   - Lattice spacing error Delta_lat(a) as a -> 0 (Continuum field limit).
4. Refusal of premature Standard Model or empirical claims.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
from math import isqrt
from typing import Any, Dict


def tfim_l2_hamiltonian(j: int, h: int) -> list[list[int]]:
    """Construct -j Z1 Z2 - h (X1 + X2) in computational-basis order."""
    if type(j) is not int or type(h) is not int:
        raise TypeError("j and h must be exact integers")
    return [[-j, -h, -h, 0], [-h, j, 0, -h],
            [-h, 0, j, -h], [0, -h, -h, -j]]


def _matrix_product(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def tfim_l2_exact_spectrum(j: int = 1, h: int = 1) -> Dict[str, Any]:
    """Exact spectrum of 2-site TFIM with open boundary conditions:

    Basis: {|00>, |01>, |10>, |11>}.
    Z_1 Z_2 = diag(1, -1, -1, 1).
    X_1 + X_2 connects states differing by 1 bit flip.
    Matrix:
    [ -J,   -h,   -h,    0 ]
    [ -h,    J,    0,   -h ]
    [ -h,    0,    J,   -h ]
    [  0,   -h,   -h,   -J ]

    The invertible basis with columns (00+11, 01+10, 00-11, 01-10)
    gives a 2x2 block [[-j, -2h], [-2h, j]] and singleton blocks -j, j.
    The 2x2 block squares to (j*j + 4*h*h) I. Values are encoded as exact
    integer/radical expressions, without converting irrational roots to floats.
    The gap counts distinct energy levels; the zero Hamiltonian has gap zero.
    """
    matrix = tfim_l2_hamiltonian(j, h)
    magnitude = abs(j)
    radicand = j * j + 4 * h * h
    square_root = isqrt(radicand)
    is_square = square_root * square_root == radicand
    root = str(square_root) if is_square else f"sqrt({radicand})"
    negative_root = f"-{root}" if radicand else "0"
    evals = [negative_root, str(-magnitude), str(magnitude), root]
    if h == 0:
        gap = str(2 * magnitude)
    elif is_square:
        gap = str(square_root - magnitude)
    else:
        gap = f"{root} - {magnitude}" if magnitude else root

    basis = [[1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, -1], [1, 0, -1, 0]]
    blocks = [[-j, -2*h, 0, 0], [-2*h, j, 0, 0],
              [0, 0, -j, 0], [0, 0, 0, j]]
    decomposition_verified = _matrix_product(matrix, basis) == _matrix_product(basis, blocks)
    basis_gram_verified = _matrix_product(list(map(list, zip(*basis))), basis) == [
        [2 * (i == k) for k in range(4)] for i in range(4)
    ]

    return {
        "model": "1D Transverse-Field Ising Model (L=2)",
        "coupling_j": j,
        "transverse_field_h": h,
        "exact_eigenvalues": evals,
        "ground_state_energy": negative_root,
        "gap": gap,
        "gap_convention": "next distinct energy above the ground eigenspace; zero if no next level",
        "dimension": 4,
        "hamiltonian": matrix,
        "eigenvalue_encoding": "exact integer or signed principal square root",
        "radicand": str(radicand),
        "characteristic_polynomial_descending": [
            "1", "0", str(-(2*j*j + 4*h*h)), "0", str(j*j*radicand)
        ],
        "block_decomposition_verified": decomposition_verified,
        "basis_gram_verified": basis_gram_verified,
    }


def z2_gauge_plaquette_invariance() -> Dict[str, Any]:
    """Verify gauge invariance of the Z_2 plaquette Hamiltonian:

    Plaquette with 4 links l in {1, 2, 3, 4}, vertices v in {1, 2, 3, 4}.
    Each vertex is incident to 2 links:
      v_1: links 1, 4
      v_2: links 1, 2
      v_3: links 2, 3
      v_4: links 3, 4
    Gauss generators:
      G_1 = X_1 X_4
      G_2 = X_1 X_2
      G_3 = X_2 X_3
      G_4 = X_3 X_4
    Plaquette flux operator: U_box = Z_1 Z_2 Z_3 Z_4.
    Electric energy: H_E = -g (X_1 + X_2 + X_3 + X_4).
    Magnetic energy: H_B = -K U_box.

    Commutation checks:
    1. [X_l, G_v] = 0 because all X operators commute with each other.
    2. [U_box, G_v] = 0 because each vertex v is incident to EXACTLY TWO links,
       and each link anti-commutes once: (-1)^2 = +1.
    Therefore, [H, G_v] = 0 for all vertices v!
    Physical subspace H_phys = { |psi> : G_v |psi> = +1 for all v } is strictly preserved.
    """
    # X strings are masks in the four-link Pauli basis. Commutation with
    # the ZZZZ flux is determined by the parity of their common support.
    generator_masks = [0b1001, 0b0011, 0b0110, 0b1100]
    flux_mask = 0b1111
    links_per_vertex = [(mask & flux_mask).bit_count() for mask in generator_masks]
    anti_commutation_signs = [(-1) ** k for k in links_per_vertex]
    commutes_with_flux = all(sign == 1 for sign in anti_commutation_signs)
    # In the X eigenbasis, each Gauss constraint has eigenvalue (-1)^parity.
    physical_labels = [label for label in range(16)
                       if all((label & mask).bit_count() % 2 == 0 for mask in generator_masks)]
    # Electric terms are diagonal there. The flux flips all four X eigenbits.
    commutes_with_electric = all(
        (label ^ (1 << link)) ^ mask == (label ^ mask) ^ (1 << link)
        for label in range(16) for link in range(4) for mask in generator_masks
    )
    flux_preserves_constraints = all(label ^ flux_mask in physical_labels for label in physical_labels)

    return {
        "gauge_group": "Z_2",
        "geometry": "Single 2D square plaquette (4 links, 4 vertices)",
        "gauss_generators": ["X_1 X_4", "X_1 X_2", "X_2 X_3", "X_3 X_4"],
        "links_per_vertex": links_per_vertex,
        "gauss_generator_masks": generator_masks,
        "physical_x_basis_labels": physical_labels,
        "flux_commutation_sign": anti_commutation_signs,
        "flux_term_commutes": commutes_with_flux,
        "electric_term_commutes": commutes_with_electric,
        "hamiltonian_preserves_gauge_subspace": commutes_with_flux and commutes_with_electric and flux_preserves_constraints,
        "physical_subspace_dimension": len(physical_labels),
    }


def separate_continuum_scaling_obligations() -> Dict[str, Any]:
    """Catalog the 3 distinct scaling obligations required for continuum limits:

    1. Large-volume limit (L -> infty): Thermodynamic limit, infrared control.
    2. Gauge truncation limit (Lambda -> infty): Infinite-dimensional local link spaces.
    3. Vanishing lattice spacing (a -> 0): Ultraviolet continuum field theory limit.
    """
    obligations = [
        {
            "obligation_id": "CONT-OBLIG-1",
            "limit_name": "Large-Volume Limit (L -> infty)",
            "control": "Lieb-Robinson decay, boundary conditions",
            "status": "OPEN_THERMODYNAMIC_PROOF",
        },
        {
            "obligation_id": "CONT-OBLIG-2",
            "limit_name": "Gauge Truncation Limit (Lambda -> infty)",
            "control": "Quantum link / truncation error convergence",
            "status": "OPEN_TRUNCATION_PROOF",
        },
        {
            "obligation_id": "CONT-OBLIG-3",
            "limit_name": "Vanishing Lattice Spacing (a -> 0)",
            "control": "Coupling constant renormalization flow g(a) -> g*",
            "status": "OPEN_RENORMALIZATION_PROOF",
        },
    ]
    return {
        "obligations": obligations,
        "all_required_continuum_limits_proved": False,
        "standard_model_or_empirical_recovery_claimed": False,
    }


def generate_canonical_block09_receipt() -> Dict[str, Any]:
    """Generate the complete canonical receipt for Block 09."""
    tfim = tfim_l2_exact_spectrum(1, 1)
    gauge = z2_gauge_plaquette_invariance()
    limits = separate_continuum_scaling_obligations()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_09",
        "global_targets": "C500-T501..C500-T525",
        "terminal_outcome": "FINITE_LATTICE_BENCHMARKS_WITH_SCALING_OBLIGATIONS",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "tfim_benchmark": tfim,
        "z2_gauge_benchmark": gauge,
        "continuum_obligations": limits,
        "machine_bet_clauses": {
            "finite_gauge_subspace_preserved": gauge["hamiltonian_preserves_gauge_subspace"],
            "exact_small_system_observable_count": 2,
            "volume_truncation_and_spacing_errors_are_separate": True,
            "all_required_continuum_limits_proved": False,
            "standard_model_or_empirical_recovery_claimed": False,
            "extrapolation_grid_frozen_before_results": False,
        },
    }


if __name__ == "__main__":
    receipt = generate_canonical_block09_receipt()
    print(json.dumps(receipt, indent=2))

__all__ = ['generate_canonical_block09_receipt', 'separate_continuum_scaling_obligations', 'tfim_l2_exact_spectrum', 'tfim_l2_hamiltonian', 'z2_gauge_plaquette_invariance']
