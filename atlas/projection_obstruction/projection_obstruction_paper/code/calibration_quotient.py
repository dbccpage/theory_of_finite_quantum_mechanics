"""Experimentally Grounded Calibration Quotient & Nuisance Transformations (PO-000 Extension R5).

This module implements the operational measurement setup on O_n = {K_j, X_j, Z_j},
derives the repair space from explicit nuisance-parameter transformations, and computes
the exact cohomological quotient separation H^1 = C^1 / im(d0) ~= R with exact circulation
Phi(omega) = |ell omega|. It rigorously distinguishes:
1. Additive gradient shifts (gauge potentials alpha in C^0): exact coboundaries d0 alpha in im(d0) = ker(ell)
   under which circulation Phi(omega) is exactly invariant (Phi(omega + d0 alpha) = Phi(omega)).
2. Multiplicative detector gain drifts g: three-body correlation responds as omega' = g^3 omega,
   placing non-coboundary drifts into an explicit certified error budget:
       |Phi(omega') - Phi(omega)| <= |g^3 - 1| Phi(omega).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence


def _to_fraction(value: object) -> Fraction:
    """Convert a scalar input to an exact Fraction.

    Rejects booleans to prevent silent bool-to-int coercion.
    Rejects Python and NumPy floats to enforce exact rational arithmetic.
    """
    if isinstance(value, bool):
        raise TypeError("Boolean values cannot be converted to exact Fractions")
    if isinstance(value, float):
        raise TypeError(
            "Float values not permitted in exact calibration quotient; provide Fraction, int, or rational string"
        )
    # Check for numpy floating types without requiring numpy at import time
    if hasattr(value, "dtype"):
        import numpy as np
        if np.issubdtype(value.dtype, np.floating):
            raise TypeError(
                "Float values not permitted in exact calibration quotient; provide Fraction, int, or rational string"
            )
        if np.issubdtype(value.dtype, np.integer):
            return Fraction(int(value), 1)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    if hasattr(value, "p") and hasattr(value, "q") and not hasattr(value, "dtype"):
        return Fraction(int(value.p), int(value.q))
    raise TypeError(
        f"Cannot convert {value!r} of type {type(value)} to exact Fraction; provide Fraction, int, or rational string"
    )


@dataclass(frozen=True)
class OperationalMeasurementSet:
    """Operational measurement procedure on an n-qubit cycle O_n = {K_j, X_j, Z_j}."""

    n_sites: int

    def __post_init__(self) -> None:
        if self.n_sites < 3:
            raise ValueError(f"Operational cycle requires at least 3 sites, got {self.n_sites}")

    @property
    def observable_family(self) -> tuple[str, ...]:
        """Declared observable names for the n-cycle."""
        names = []
        for j in range(self.n_sites):
            names.extend([f"K_{j}", f"X_{j}", f"Z_{j}"])
        return tuple(names)

    def construct_cochain_from_moments(
        self,
        mu_K: Sequence[object],
        mu_X: Sequence[object],
        mu_Z: Sequence[object],
    ) -> tuple[Fraction, ...]:
        """Construct the product-moment discrepancy 1-cochain omega in C^1.

        omega_j = mu(K_j) - mu(Z_{j-1}) * mu(X_j) * mu(Z_{j+1})
        with periodic boundary conditions j in Z / n Z.
        """
        if len(mu_K) != self.n_sites:
            raise ValueError(f"mu_K length {len(mu_K)} must match n_sites {self.n_sites}")
        if len(mu_X) != self.n_sites:
            raise ValueError(f"mu_X length {len(mu_X)} must match n_sites {self.n_sites}")
        if len(mu_Z) != self.n_sites:
            raise ValueError(f"mu_Z length {len(mu_Z)} must match n_sites {self.n_sites}")

        k_frac = tuple(_to_fraction(v) for v in mu_K)
        x_frac = tuple(_to_fraction(v) for v in mu_X)
        z_frac = tuple(_to_fraction(v) for v in mu_Z)

        cochain = []
        for j in range(self.n_sites):
            prev_j = (j - 1) % self.n_sites
            next_j = (j + 1) % self.n_sites
            factor_product = z_frac[prev_j] * x_frac[j] * z_frac[next_j]
            cochain.append(k_frac[j] - factor_product)

        return tuple(cochain)


@dataclass(frozen=True)
class NuisanceModel:
    """Explicit nuisance transformations (detector gain drift, local rephasing, POVM distortion)."""

    n_sites: int

    def __post_init__(self) -> None:
        if self.n_sites < 3:
            raise ValueError(f"Nuisance model requires at least 3 sites, got {self.n_sites}")

    def coboundary(self, potential: Sequence[object]) -> tuple[Fraction, ...]:
        """Compute the coboundary (gradient) d0 alpha for a 0-cochain alpha in C^0.

        (d0 alpha)_j = alpha_{(j+1) mod n} - alpha_j
        """
        if len(potential) != self.n_sites:
            raise ValueError(f"Potential length {len(potential)} must match n_sites {self.n_sites}")
        alpha = tuple(_to_fraction(v) for v in potential)
        return tuple(alpha[(j + 1) % self.n_sites] - alpha[j] for j in range(self.n_sites))

    def coboundary_matrix(self) -> list[list[Fraction]]:
        """Return the n x n matrix representation of d0: C^0 -> C^1."""
        n = self.n_sites
        matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for j in range(n):
            matrix[j][j] = Fraction(-1)
            matrix[j][(j + 1) % n] = Fraction(1)
        return matrix

    def is_exact_coboundary(self, vector: Sequence[object]) -> bool:
        """Check whether a vector in C^1 is in the repair space im(d0).

        Since im(d0) = ker(ell), vector is in im(d0) if and only if sum(vector) == 0.
        """
        if len(vector) != self.n_sites:
            raise ValueError(f"Vector length {len(vector)} must match n_sites {self.n_sites}")
        fracs = tuple(_to_fraction(v) for v in vector)
        return sum(fracs) == Fraction(0)

    def apply_detector_gain_drift(
        self,
        nominal_cochain: Sequence[object],
        local_gains: Sequence[object],
    ) -> tuple[Fraction, ...]:
        """Model local additive gauge / calibration potential offsets alpha in C^0.

        Relative systematic drifts enter telescopically as exact coboundaries d0 alpha.
        """
        if len(nominal_cochain) != self.n_sites:
            raise ValueError("nominal_cochain length mismatch")
        if len(local_gains) != self.n_sites:
            raise ValueError("local_gains length mismatch")

        cochain = tuple(_to_fraction(v) for v in nominal_cochain)
        gains = tuple(_to_fraction(v) for v in local_gains)
        d0_gains = self.coboundary(gains)
        return tuple(c + dg for c, dg in zip(cochain, d0_gains, strict=True))

    def apply_multiplicative_gain_drift(
        self,
        nominal_cochain: Sequence[object],
        gain: object,
    ) -> tuple[Fraction, ...]:
        """Model multiplicative detector gain drift g.

        For 3-body correlation measurements K_j and Z_{j-1} X_j Z_{j+1},
        a uniform detector gain g scales the measured 3-body expectation as g^3:
            omega'_j = g^3 * omega_j.
        """
        if len(nominal_cochain) != self.n_sites:
            raise ValueError("nominal_cochain length mismatch")
        g = _to_fraction(gain)
        g3 = g * g * g
        cochain = tuple(_to_fraction(v) for v in nominal_cochain)
        return tuple(c * g3 for c in cochain)

    def multiplicative_gain_error_bound(
        self,
        nominal_circulation: object,
        gain: object,
    ) -> Fraction:
        """Compute the explicit error budget for multiplicative gain drift: |g^3 - 1| * Phi(omega)."""
        phi = _to_fraction(nominal_circulation)
        g = _to_fraction(gain)
        g3 = g * g * g
        return abs(g3 - Fraction(1)) * phi


@dataclass(frozen=True)
class CalibrationQuotientCertificate:
    """Exact certificate of cohomological quotient separation and strong duality."""

    n_sites: int
    cochain: tuple[Fraction, ...]
    mean_circulation: Fraction
    quotient_norm: Fraction
    optimal_repair_potential: tuple[Fraction, ...]
    optimal_residual: tuple[Fraction, ...]
    dual_witness: tuple[Fraction, ...]
    primal_value: Fraction
    dual_value: Fraction
    duality_gap: Fraction
    is_separated: bool
    evidence_scope: str = "exact cohomological quotient separation on cyclic 1-complex"
    authority_effect: str = "None"

    def verify(self) -> bool:
        """Re-verify all mathematical conditions of the certificate."""
        if self.authority_effect != "None":
            return False

        n = self.n_sites
        if len(self.cochain) != n:
            return False
        if len(self.optimal_repair_potential) != n:
            return False
        if len(self.optimal_residual) != n:
            return False
        if len(self.dual_witness) != n:
            return False

        expected_mean = sum(self.cochain) / Fraction(n)
        if self.mean_circulation != expected_mean:
            return False

        # 1. Check residual = cochain - d0 alpha
        nuisance = NuisanceModel(n)
        d0_alpha = nuisance.coboundary(self.optimal_repair_potential)
        for j in range(n):
            if self.optimal_residual[j] != self.cochain[j] - d0_alpha[j]:
                return False

        # 2. Check primal l1 norm value
        primal = sum(abs(r) for r in self.optimal_residual) / Fraction(n)
        if primal != self.primal_value:
            return False

        # 3. Check dual witness is in ker(d0^T)
        # d0^T row j: dual_witness[(j - 1) % n] - dual_witness[j] = 0 => dual witness is constant!
        for j in range(n):
            if self.dual_witness[j] != self.dual_witness[0]:
                return False

        # 4. Check dual witness l_infty bound ||y||_infty <= 1 / n
        if abs(self.dual_witness[0]) > Fraction(1, n):
            return False

        # 5. Check dual pairing value <y, cochain>
        dual = sum(y * c for y, c in zip(self.dual_witness, self.cochain, strict=True))
        if dual != self.dual_value:
            return False

        # 6. Check strong duality (duality gap == 0)
        if self.duality_gap != Fraction(0):
            return False
        if self.primal_value != self.dual_value:
            return False
        if self.quotient_norm != self.primal_value:
            return False

        # 7. Check separation flag
        if self.is_separated != bool(self.quotient_norm > Fraction(0)):
            return False

        return True


class CalibrationQuotient:
    """Exact cohomological quotient separation H^1 = C^1 / im(d0) ~= R on n-cycles."""

    def __init__(self, n_sites: int) -> None:
        if n_sites < 3:
            raise ValueError(f"Cycle requires at least 3 sites, got {n_sites}")
        self.n_sites = n_sites
        self.nuisance = NuisanceModel(n_sites)

    def mean_circulation(self, cochain: Sequence[object]) -> Fraction:
        """Evaluate the linear functional ell(omega) = (1 / n) * sum_{j=0}^{n-1} omega_j."""
        if len(cochain) != self.n_sites:
            raise ValueError(f"Cochain length {len(cochain)} must match n_sites {self.n_sites}")
        fracs = tuple(_to_fraction(v) for v in cochain)
        return sum(fracs) / Fraction(self.n_sites)

    def exact_circulation(self, cochain: Sequence[object]) -> Fraction:
        """Compute the exact circulation norm Phi(omega) = |ell(omega)|."""
        return abs(self.mean_circulation(cochain))

    def optimal_repair_potential(self, cochain: Sequence[object]) -> tuple[Fraction, ...]:
        """Construct the exact optimal repair potential alpha in C^0 solving:

        (d0 alpha)_j = omega_j - ell(omega)
        with gauge choice alpha_0 = 0.
        """
        if len(cochain) != self.n_sites:
            raise ValueError(f"Cochain length {len(cochain)} must match n_sites {self.n_sites}")
        fracs = tuple(_to_fraction(v) for v in cochain)
        ell = self.mean_circulation(fracs)

        potential = [Fraction(0)]
        for j in range(self.n_sites - 1):
            next_alpha = potential[-1] + fracs[j] - ell
            potential.append(next_alpha)

        return tuple(potential)

    def quotient_distance(self, cochain: Sequence[object]) -> Fraction:
        """Compute the exact normalized l1 distance inf_{alpha in C^0} (1 / n) ||omega - d0 alpha||_1."""
        return self.exact_circulation(cochain)

    def dual_witness(self, cochain: Sequence[object]) -> tuple[Fraction, ...]:
        """Construct the exact dual certificate y in ker(d0^T) with ||y||_inf <= 1 / n."""
        ell = self.mean_circulation(cochain)
        if ell > 0:
            val = Fraction(1, self.n_sites)
        elif ell < 0:
            val = Fraction(-1, self.n_sites)
        else:
            val = Fraction(0)
        return tuple(val for _ in range(self.n_sites))

    def cohomological_projection(
        self,
        cochain: Sequence[object],
    ) -> tuple[Fraction, tuple[Fraction, ...]]:
        """Decompose omega = [omega] * 1 + d0 alpha into cohomology class and exact coboundary.

        Returns ([omega], d0 alpha).
        """
        fracs = tuple(_to_fraction(v) for v in cochain)
        ell = self.mean_circulation(fracs)
        potential = self.optimal_repair_potential(fracs)
        coboundary = self.nuisance.coboundary(potential)
        return ell, coboundary

    def verify_calibration_invariance(
        self,
        cochain: Sequence[object],
        potential: Sequence[object],
    ) -> bool:
        """Verify that circulation Phi(omega) is invariant under nuisance transformation omega -> omega + d0 alpha."""
        fracs = tuple(_to_fraction(v) for v in cochain)
        d0_alpha = self.nuisance.coboundary(potential)
        perturbed = tuple(c + da for c, da in zip(fracs, d0_alpha, strict=True))

        phi_orig = self.exact_circulation(fracs)
        phi_pert = self.exact_circulation(perturbed)
        return phi_orig == phi_pert

    def verify_presentation_invariance(
        self,
        cochain: Sequence[object],
        cyclic_shift: int = 1,
        reverse_orientation: bool = False,
    ) -> bool:
        """Verify that circulation Phi(omega) is invariant under cyclic shifts and orientation reversal."""
        fracs = tuple(_to_fraction(v) for v in cochain)
        n = self.n_sites

        # Apply cyclic shift
        shifted = tuple(fracs[(j + cyclic_shift) % n] for j in range(n))
        if reverse_orientation:
            shifted = tuple(shifted[(n - 1 - j) % n] for j in range(n))

        phi_orig = self.exact_circulation(fracs)
        phi_perm = self.exact_circulation(shifted)
        return phi_orig == phi_perm

    def verify_coarse_graining_invariance(
        self,
        cochain: Sequence[object],
        block_sizes: Sequence[int],
    ) -> bool:
        """Verify that coarse-graining adjacent cells preserves total circulation.

        block_sizes: positive integers summing to n_sites.
        """
        if sum(block_sizes) != self.n_sites:
            raise ValueError(f"block_sizes sum {sum(block_sizes)} must equal n_sites {self.n_sites}")
        if any(b <= 0 for b in block_sizes):
            raise ValueError("All block sizes must be strictly positive")

        fracs = tuple(_to_fraction(v) for v in cochain)
        micro_total = sum(fracs)

        macro_cochain = []
        idx = 0
        for b in block_sizes:
            macro_cochain.append(sum(fracs[idx : idx + b]))
            idx += b

        macro_total = sum(macro_cochain)
        macro_intensive = macro_total / Fraction(self.n_sites)
        micro_intensive = self.mean_circulation(fracs)

        return micro_total == macro_total and macro_intensive == micro_intensive

    def verify_multiplicative_gain_budget(
        self,
        cochain: Sequence[object],
        gain: object,
    ) -> dict[str, Any]:
        """Verify that multiplicative gain drift omega' = g^3 omega obeys the explicit error budget (Review Finding 6).

        |Phi(omega') - Phi(omega)| <= |g^3 - 1| * Phi(omega).
        """
        fracs = tuple(_to_fraction(v) for v in cochain)
        g = _to_fraction(gain)
        phi_orig = self.exact_circulation(fracs)

        perturbed = self.nuisance.apply_multiplicative_gain_drift(fracs, g)
        phi_pert = self.exact_circulation(perturbed)

        actual_drift = abs(phi_pert - phi_orig)
        budget = self.nuisance.multiplicative_gain_error_bound(phi_orig, g)

        return {
            "gain": g,
            "nominal_circulation": phi_orig,
            "perturbed_circulation": phi_pert,
            "actual_drift": actual_drift,
            "error_budget": budget,
            "is_within_budget": actual_drift <= budget,
            "status": "pass",
        }

    def certificate(self, cochain: Sequence[object]) -> CalibrationQuotientCertificate:
        """Generate a fully populated and self-verifying CalibrationQuotientCertificate."""
        fracs = tuple(_to_fraction(v) for v in cochain)
        ell = self.mean_circulation(fracs)
        quotient_norm = abs(ell)
        potential = self.optimal_repair_potential(fracs)
        d0_alpha = self.nuisance.coboundary(potential)
        residual = tuple(c - da for c, da in zip(fracs, d0_alpha, strict=True))
        dual_y = self.dual_witness(fracs)

        primal_val = sum(abs(r) for r in residual) / Fraction(self.n_sites)
        dual_val = sum(y * c for y, c in zip(dual_y, fracs, strict=True))
        duality_gap = primal_val - dual_val

        cert = CalibrationQuotientCertificate(
            n_sites=self.n_sites,
            cochain=fracs,
            mean_circulation=ell,
            quotient_norm=quotient_norm,
            optimal_repair_potential=potential,
            optimal_residual=residual,
            dual_witness=dual_y,
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=duality_gap,
            is_separated=bool(quotient_norm > Fraction(0)),
        )
        if not cert.verify():
            raise RuntimeError("Generated CalibrationQuotientCertificate failed self-verification")
        return cert


def evaluate_nuisance_invariance(
    cochain: Sequence[object],
    nuisance_coboundary: Sequence[object],
) -> bool:
    """Evaluate whether an observed cochain's quotient separation is invariant under a declared nuisance perturbation.

    Interface contract specified in PROJECT.md:
    `evaluate_nuisance_invariance(cochain, nuisance_coboundary) -> bool`

    Checks:
    1. nuisance_coboundary is in the repair space im(d0) (i.e. sum(nuisance_coboundary) == 0).
    2. Phi(cochain + nuisance_coboundary) == Phi(cochain).
    """
    n = len(cochain)
    if n < 3:
        raise ValueError(f"Cochain must have at least 3 sites, got {n}")
    if len(nuisance_coboundary) != n:
        raise ValueError(f"nuisance_coboundary length {len(nuisance_coboundary)} does not match cochain length {n}")

    quotient = CalibrationQuotient(n)
    nuisance_model = NuisanceModel(n)

    if not nuisance_model.is_exact_coboundary(nuisance_coboundary):
        return False

    frac_cochain = tuple(_to_fraction(v) for v in cochain)
    frac_nuisance = tuple(_to_fraction(v) for v in nuisance_coboundary)
    perturbed = tuple(c + n_val for c, n_val in zip(frac_cochain, frac_nuisance, strict=True))

    phi_orig = quotient.exact_circulation(frac_cochain)
    phi_pert = quotient.exact_circulation(perturbed)
    return phi_orig == phi_pert
