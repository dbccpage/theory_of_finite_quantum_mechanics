"""kitaev_chain_exact.py — 1D Discrete Kitaev Chain Hamiltonian & Majorana Zero Modes.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C6, gemini_000.md.

Mechanizes:
1. Exact Rational 1D Kitaev Model:
   - Discrete chain of N sites with parameters t (hopping), mu (chemical potential),
     and Delta (p-wave pairing) in Q (fractions.Fraction).
   - Zero-Float Law: strictly forbids float or bool in Hamiltonian weights and parameters.
2. Majorana Operator Decomposition:
   - Decomposes Dirac fermions c_j, c_j^dagger into 2N Majorana operators gamma_1, ..., gamma_2N
     satisfying the Clifford algebra {gamma_a, gamma_b} = 2 delta_{ab}.
   - Expresses H as an exact sum of Majorana bilinears i * gamma_a * gamma_b.
3. Sweet-Spot Majorana Zero Modes (MZMs):
   - At the sweet spot mu = 0 and t = Delta, bulk pairs (gamma_2j, gamma_2j+1) form
     with energy gap 2t.
   - Boundary modes gamma_1 and gamma_2N decouple completely, having exact zero commutator
     [H, gamma_1] = 0 and [H, gamma_2N] = 0.
4. Non-Sweet-Spot & Boundary Coupling Witness:
   - Evaluates commutator norms and identifies boundary leakage when mu != 0 or t != Delta.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    call_native,
    decode_rational,
)


@dataclass(frozen=True)
class MajoranaBilinear:
    """Hermitian basis term i gamma_a gamma_b, with positive ordered indices."""

    mode_a: int
    mode_b: int

    def __post_init__(self) -> None:
        if not isinstance(self.mode_a, int) or not isinstance(self.mode_b, int):
            raise TypeError("Majorana mode indices must be integers")
        if isinstance(self.mode_a, bool) or isinstance(self.mode_b, bool):
            raise TypeError("Majorana mode indices cannot be boolean")
        if self.mode_a <= 0 or self.mode_b <= 0:
            raise ValueError("Majorana mode indices must be positive (1-indexed)")
        if self.mode_a >= self.mode_b:
            raise ValueError(
                f"Majorana modes must be ordered a < b, got a={self.mode_a}, b={self.mode_b}"
            )

    def commutator_with_mode(self, k: int) -> tuple[Fraction, int] | None:
        """Return the real generator i[i gamma_a gamma_b, gamma_k].

        This preserves the historical API's coefficients; the commutator itself
        has an extra factor of -i relative to this real generator.
        """
        if not isinstance(k, int) or isinstance(k, bool) or k < 1:
            raise ValueError("Majorana mode index must be a positive integer")
        result = call_native(
            "majorana_kitaev_wire",
            {"operation": "bilinear", "a": self.mode_a, "b": self.mode_b, "mode": k},
        )["commutator"]
        return None if result is None else (decode_rational(result[0]), result[1])


class KitaevChainExact:
    """Open wire whose exact coefficients and diagnostics are owned by Rust.

    The sparse native owner preserves this paper's t/delta sign convention and
    scalar energy offset. It reports isolated coordinate Majoranas, rather than
    the full quadratic nullspace or a physical device's topological protection.
    """

    def __init__(
        self,
        num_sites: int,
        t: Fraction | int = Fraction(1),
        mu: Fraction | int = Fraction(0),
        delta: Fraction | int = Fraction(1),
    ) -> None:
        if not isinstance(num_sites, int) or isinstance(num_sites, bool) or num_sites < 2:
            raise ValueError(f"num_sites must be an integer >= 2, got {num_sites}")
        for name, value in (("t", t), ("mu", mu), ("delta", delta)):
            if not isinstance(value, (Fraction, int)) or isinstance(value, bool):
                raise TypeError(
                    f"Parameter {name} must be exact Fraction or int, not {type(value).__name__}"
                )
        self.num_sites = num_sites
        self.num_modes = 2 * num_sites
        self.t = Fraction(t)
        self.mu = Fraction(mu)
        self.delta = Fraction(delta)
        self._terms: dict[MajoranaBilinear, Fraction] = {}
        self._constant_energy = Fraction(0)
        self._build_hamiltonian()

    def _native_result(self, mode: int | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "num_sites": self.num_sites,
            "t": str(self.t),
            "mu": str(self.mu),
            "delta": str(self.delta),
        }
        if mode is not None:
            payload["mode"] = mode
        return call_native("majorana_kitaev_wire", payload)

    def _build_hamiltonian(self) -> None:
        result = self._native_result()
        self._terms = {
            MajoranaBilinear(a, b): decode_rational(coefficient)
            for a, b, coefficient in result["terms"]
        }
        self._constant_energy = decode_rational(result["constant_energy"])

    @property
    def is_sweet_spot(self) -> bool:
        return self._native_result()["is_sweet_spot"]

    def terms(self) -> dict[MajoranaBilinear, Fraction]:
        return dict(self._terms)

    def bulk_paired_modes(self) -> set[int]:
        return {mode for term in self.terms() for mode in (term.mode_a, term.mode_b)}

    def boundary_modes(self) -> tuple[int, int]:
        return tuple(self._native_result()["boundary_modes"])

    def unpaired_zero_modes(self) -> set[int]:
        return set(self._native_result()["unpaired_modes"])

    def commutator_with_mode(self, k: int) -> dict[int, Fraction]:
        """Return i[H, gamma_k] in the real Majorana basis (legacy naming)."""
        if not isinstance(k, int) or isinstance(k, bool) or not 1 <= k <= self.num_modes:
            raise ValueError(f"Mode {k} out of range [1, {self.num_modes}]")
        return {
            mode: decode_rational(coefficient)
            for mode, coefficient in self._native_result(k)["mode_commutator"]
        }

    def verify_mzm_isolation(self) -> dict[str, object]:
        """Return native finite-wire isolation diagnostics in the legacy schema.

        The retained `mzm_topologically_protected` key denotes boundary isolation
        only; no physical or bulk topological certification follows from it.
        """
        return self._native_result()["diagnostics"]
