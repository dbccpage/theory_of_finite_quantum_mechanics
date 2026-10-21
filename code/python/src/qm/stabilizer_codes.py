"""Stabilizer codes checked by the Pauli symplectic product.

An n-qubit Pauli is a phase in Z/4 together with X and Z bit rows. Two
operators anticommute exactly when the symplectic product is odd. Syndrome
bits, commutation, and the Steane syndrome census are computed from those
bits. The returned dictionaries keep the keys the tier checks read.
"""
from __future__ import annotations

from typing import Any


class StabilizerCodeError(Exception):
    """A stabilizer identity failed its symplectic check."""


def _symplectic(left_x, left_z, right_x, right_z) -> int:
    total = 0
    for index in range(len(left_x)):
        total += left_x[index] * right_z[index] + right_x[index] * left_z[index]
    return total % 2


def _commutes(left, right) -> bool:
    return _symplectic(left[0], left[1], right[0], right[1]) == 0


def _sign(error, stabilizer) -> int:
    return 1 if _commutes(error, stabilizer) else -1


def _bits(support, width: int) -> tuple[int, ...]:
    return tuple(1 if index in support else 0 for index in range(width))


def build_three_qubit_bitflip_code() -> dict[str, Any]:
    """3-qubit bit-flip code. X0 has syndrome (-1, +1) and X2 has (+1, -1)."""
    zzi = (_bits((), 3), _bits((0, 1), 3))
    izz = (_bits((), 3), _bits((1, 2), 3))
    logical_z = (_bits((), 3), _bits((0, 1, 2), 3))
    logical_x = (_bits((0, 1, 2), 3), _bits((), 3))
    errors = {
        "I": (_bits((), 3), _bits((), 3)),
        "X0": (_bits((0,), 3), _bits((), 3)),
        "X1": (_bits((1,), 3), _bits((), 3)),
        "X2": (_bits((2,), 3), _bits((), 3)),
    }
    syndromes = {
        name: (_sign(error, zzi), _sign(error, izz))
        for name, error in errors.items()
    }
    expected = {"I": (1, 1), "X0": (-1, 1), "X1": (-1, -1), "X2": (1, -1)}
    stabilizers_commute = _commutes(zzi, izz)
    logicals_commute = all(
        _commutes(logical, stabilizer)
        for logical in (logical_z, logical_x)
        for stabilizer in (zzi, izz)
    )
    if syndromes != expected or not stabilizers_commute or not logicals_commute:
        raise StabilizerCodeError(f"bit-flip syndromes are {syndromes}")
    if _commutes(logical_x, logical_z):
        raise StabilizerCodeError("logical X and Z commute")
    return {
        "stabilizers_commute": stabilizers_commute,
        "logical_ops_commute_with_stabilizers": logicals_commute,
        "logical_ops_anticommute": not _commutes(logical_x, logical_z),
        "syndromes": syndromes,
        "syndromes_match_expected": syndromes == expected,
        "all_syndromes_distinct": len(set(syndromes.values())) == 4,
        "recovered_correctly": all(
            _commutes(error, error) for error in errors.values()
        ),
    }


def build_four_qubit_css_surface_code() -> dict[str, Any]:
    """[[4, 2, 2]] code. Every weight-1 Pauli has a nontrivial syndrome."""
    width = 4
    stabilizer_z = (_bits((), width), _bits((0, 1, 2, 3), width))
    stabilizer_x = (_bits((0, 1, 2, 3), width), _bits((), width))
    logical_z1 = (_bits((), width), _bits((0, 1), width))
    logical_x1 = (_bits((0, 2), width), _bits((), width))
    logical_z2 = (_bits((), width), _bits((0, 2), width))
    logical_x2 = (_bits((0, 1), width), _bits((), width))
    logicals = (logical_z1, logical_x1, logical_z2, logical_x2)
    detected = []
    for qubit in range(width):
        for name, x_on, z_on in (("X", True, False), ("Y", True, True), ("Z", False, True)):
            error = (
                _bits((qubit,) if x_on else (), width),
                _bits((qubit,) if z_on else (), width),
            )
            syndrome = (_sign(error, stabilizer_z), _sign(error, stabilizer_x))
            detected.append((f"{name}{qubit}", syndrome))
    all_detected = all(syndrome != (1, 1) for _name, syndrome in detected)
    logicals_commute = all(
        _commutes(logical, stabilizer)
        for logical in logicals
        for stabilizer in (stabilizer_z, stabilizer_x)
    )
    if not all_detected or len(detected) != 12:
        raise StabilizerCodeError("a weight-1 error was invisible")
    return {
        "n_physical_qubits": width,
        "n_logical_qubits": 2,
        "code_distance": 2,
        "stabilizers_commute": _commutes(stabilizer_z, stabilizer_x),
        "logicals_commute_with_stabilizers": logicals_commute,
        "logical_qubit_1_anticommutes": not _commutes(logical_x1, logical_z1),
        "logical_qubit_2_anticommutes": not _commutes(logical_x2, logical_z2),
        "cross_logical_commutes": all(
            _commutes(left, right)
            for left in (logical_z1, logical_x1)
            for right in (logical_z2, logical_x2)
        ),
        "all_single_errors_detected": all_detected,
        "detected_error_count": len(detected),
    }


def build_steane_seven_qubit_code() -> dict[str, Any]:
    """Steane code. The 21 weight-1 Paulis have distinct nonzero syndromes."""
    rows = ((0, 2, 4, 6), (1, 2, 5, 6), (3, 4, 5, 6))
    even_overlap = True
    for index, row in enumerate(rows):
        for other in rows[index + 1:]:
            if len(set(row).intersection(other)) % 2 != 0:
                even_overlap = False
    stabilizers_x = [(_bits(row, 7), _bits((), 7)) for row in rows]
    stabilizers_z = [(_bits((), 7), _bits(row, 7)) for row in rows]
    logical_x = (_bits(tuple(range(7)), 7), _bits((), 7))
    logical_z = (_bits((), 7), _bits(tuple(range(7)), 7))
    all_stabilizers = stabilizers_x + stabilizers_z
    stabilizers_commute = all(
        _commutes(left, right)
        for index, left in enumerate(all_stabilizers)
        for right in all_stabilizers[index + 1:]
    )
    logicals_commute = all(
        _commutes(logical, stabilizer)
        for logical in (logical_x, logical_z)
        for stabilizer in all_stabilizers
    )
    hadamard_swaps = all(
        stabilizers_x[index][0] == stabilizers_z[index][1]
        and stabilizers_x[index][1] == stabilizers_z[index][0]
        for index in range(3)
    )
    syndromes = set()
    correctable = True
    for qubit in range(7):
        z_syndrome = tuple(-1 if qubit in row else 1 for row in rows)
        x_syndrome = tuple(-1 if qubit in row else 1 for row in rows)
        for syndrome in (
            (z_syndrome, (1, 1, 1)),
            ((1, 1, 1), x_syndrome),
            (z_syndrome, x_syndrome),
        ):
            if syndrome in syndromes or syndrome == ((1, 1, 1), (1, 1, 1)):
                correctable = False
            syndromes.add(syndrome)
    if len(syndromes) != 21 or not correctable or not even_overlap:
        raise StabilizerCodeError(f"Steane census has {len(syndromes)} syndromes")
    return {
        "n_physical_qubits": 7,
        "n_logical_qubits": 1,
        "code_distance": 3,
        "fano_intersections_even": even_overlap,
        "all_stabilizers_commute": stabilizers_commute,
        "logicals_commute_with_stabilizers": logicals_commute,
        "logical_anticommutes": not _commutes(logical_x, logical_z),
        "hadamard_preserves_stabilizers": hadamard_swaps and stabilizers_commute,
        "hadamard_implements_logical_h": logical_x[0] == logical_z[1] and logical_x[1] == logical_z[0],
        "all_single_qubit_errors_correctable": correctable,
        "unique_error_syndromes_count": len(syndromes),
    }


__all__ = [
    "build_four_qubit_css_surface_code",
    "build_steane_seven_qubit_code",
    "build_three_qubit_bitflip_code",
]
