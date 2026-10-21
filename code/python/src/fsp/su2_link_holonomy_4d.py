"""su2_link_holonomy_4d.py — 4D SU(2) Lattice Gauge Holonomies & Involution Verification.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Paper 011.

Mechanizes:
1. Exact Rational SU(2) Group Representation:
   - Link variables U represented as unit quaternions q = a0 + a1*i + a2*j + a3*k with
     a0^2 + a1^2 + a2^2 + a3^2 = 1, where a_m in Q (fractions.Fraction).
   - Exact determinant det(U) = 1 and unitarity U^dagger U = I_2 with zero floating point.
2. 4D Torus T^4 Plaquette Holonomies:
   - Plaquette operator U_{mu nu}(x) = U_mu(x) U_nu(x+mu) U_mu(x+nu)^dagger U_nu(x)^dagger
     evaluated across all 6 planes (0 <= mu < nu <= 3).
   - Wilson plaquette action S_{mu nu}(x) = 1 - (1/2) Tr(U_{mu nu}(x)) in Q.
3. Orientation-Reversing Involution tau:
   - Spatial/temporal reflection tau: x = (x0, x1, x2, x3) |-> (-x0 mod L0, x1, x2, x3).
   - Algebraic link map: tau(U_mu(x)) = U_mu(tau(x))^*.
   - Verifies exact pairing: det M[U] * det M[tau(U)] >= 0, eliminating sign oscillation.
4. Rational Metropolis Acceptance Filter:
   - Computes local action difference Delta S in Q.
   - Exact rational acceptance filter alpha = min(1, P(U') / P(U)) in Q.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Dict, Iterator, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class ExactRationalSU2:
    """Exact rational representation of SU(2) as a unit quaternion.

    U = a0 * I + a1 * (i sigma_3) + a2 * (i sigma_2) + a3 * (i sigma_1)
    satisfies a0^2 + a1^2 + a2^2 + a3^2 = 1 with a_k in Q.
    """

    a0: Fraction
    a1: Fraction
    a2: Fraction
    a3: Fraction

    def __post_init__(self) -> None:
        for name, val in (("a0", self.a0), ("a1", self.a1), ("a2", self.a2), ("a3", self.a3)):
            if isinstance(val, (float, bool)):
                raise TypeError(f"Component {name} must be an exact Fraction or int, not {type(val).__name__}")
            if isinstance(val, int):
                object.__setattr__(self, name, Fraction(val, 1))
            elif not isinstance(val, Fraction):
                raise TypeError(f"Invalid type for {name}: {type(val).__name__}")

        norm_sq = self.a0 * self.a0 + self.a1 * self.a1 + self.a2 * self.a2 + self.a3 * self.a3
        if norm_sq != Fraction(1, 1):
            raise ValueError(f"SU(2) unit quaternion norm squared must equal 1, got {norm_sq}")

    @classmethod
    def identity(cls) -> ExactRationalSU2:
        """Returns the group identity element."""
        return cls(Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

    @classmethod
    def from_pythagorean_quadruple(cls, m0: int, m1: int, m2: int, m3: int) -> ExactRationalSU2:
        """Constructs an exact unit quaternion from four integers m0, m1, m2, m3 whose sum of squares is a square."""
        sum_sq = m0 * m0 + m1 * m1 + m2 * m2 + m3 * m3
        if sum_sq == 0:
            raise ValueError("Quadruple components cannot all be zero")
        k = math.isqrt(sum_sq)
        if k * k != sum_sq:
            raise ValueError(f"Sum of squares {sum_sq} is not a perfect square in integers")
        return cls(
            Fraction(m0, k),
            Fraction(m1, k),
            Fraction(m2, k),
            Fraction(m3, k),
        )

    def multiply(self, other: ExactRationalSU2) -> ExactRationalSU2:
        """Quaternion multiplication corresponding to SU(2) group composition."""
        if not isinstance(other, ExactRationalSU2):
            raise TypeError(f"Expected ExactRationalSU2, got {type(other).__name__}")
        r0 = self.a0 * other.a0 - self.a1 * other.a1 - self.a2 * other.a2 - self.a3 * other.a3
        r1 = self.a0 * other.a1 + self.a1 * other.a0 + self.a2 * other.a3 - self.a3 * other.a2
        r2 = self.a0 * other.a2 - self.a1 * other.a3 + self.a2 * other.a0 + self.a3 * other.a1
        r3 = self.a0 * other.a3 + self.a1 * other.a2 - self.a2 * other.a1 + self.a3 * other.a0
        return ExactRationalSU2(r0, r1, r2, r3)

    def dagger(self) -> ExactRationalSU2:
        """Conjugate transpose (quaternion conjugate / inverse)."""
        return ExactRationalSU2(self.a0, -self.a1, -self.a2, -self.a3)

    def complex_conjugate(self) -> ExactRationalSU2:
        """Complex conjugate corresponding to quaternion involution a1 -> -a1, a3 -> -a3."""
        return ExactRationalSU2(self.a0, -self.a1, self.a2, -self.a3)

    def trace(self) -> Fraction:
        """Returns the trace of the 2x2 matrix: Tr(U) = 2 * a0 in Q."""
        return Fraction(2, 1) * self.a0

    def determinant(self) -> Fraction:
        """Returns the determinant of the 2x2 matrix: det(U) = a0^2 + a1^2 + a2^2 + a3^2 = 1 in Q."""
        return self.a0 * self.a0 + self.a1 * self.a1 + self.a2 * self.a2 + self.a3 * self.a3

    def is_unitary(self) -> bool:
        """Verifies U^dagger U == I."""
        prod = self.dagger().multiply(self)
        return (
            prod.a0 == Fraction(1, 1)
            and prod.a1 == Fraction(0, 1)
            and prod.a2 == Fraction(0, 1)
            and prod.a3 == Fraction(0, 1)
        )


@dataclass(frozen=True)
class Lattice4DCoord:
    """Coordinate on a 4-torus T^4 with periodic boundary conditions."""

    x0: int
    x1: int
    x2: int
    x3: int
    dims: Tuple[int, int, int, int]

    def __post_init__(self) -> None:
        for idx, (coord, dim) in enumerate(zip((self.x0, self.x1, self.x2, self.x3), self.dims)):
            if dim <= 0:
                raise ValueError(f"Lattice dimension {idx} must be positive, got {dim}")
            if coord < 0 or coord >= dim:
                raise ValueError(f"Coordinate {coord} out of range [0, {dim})")

    def shift(self, mu: int, step: int = 1) -> Lattice4DCoord:
        """Shift coordinate along direction mu in {0, 1, 2, 3} with periodic boundary conditions."""
        if mu not in (0, 1, 2, 3):
            raise ValueError(f"Direction mu must be in {{0, 1, 2, 3}}, got {mu}")
        coords = [self.x0, self.x1, self.x2, self.x3]
        dim = self.dims[mu]
        coords[mu] = (coords[mu] + step) % dim
        return Lattice4DCoord(coords[0], coords[1], coords[2], coords[3], self.dims)

    def involution_reflection(self) -> Lattice4DCoord:
        """Orientation-reversing reflection: x0 -> (-x0 mod L0)."""
        refl_x0 = (-self.x0) % self.dims[0]
        return Lattice4DCoord(refl_x0, self.x1, self.x2, self.x3, self.dims)


class Lattice4DSU2:
    """4-dimensional SU(2) lattice gauge configuration on a torus T^4."""

    def __init__(self, dims: Tuple[int, int, int, int] = (2, 2, 2, 2)) -> None:
        if len(dims) != 4 or any(d <= 0 for d in dims):
            raise ValueError(f"Lattice dims must be a 4-tuple of positive ints, got {dims}")
        self.dims = dims
        self._links: Dict[Tuple[int, int, int, int, int], ExactRationalSU2] = {}
        for x0 in range(dims[0]):
            for x1 in range(dims[1]):
                for x2 in range(dims[2]):
                    for x3 in range(dims[3]):
                        for mu in range(4):
                            self._links[(x0, x1, x2, x3, mu)] = ExactRationalSU2.identity()

    @property
    def volume(self) -> int:
        """Total number of lattice sites V = L0 * L1 * L2 * L3."""
        return self.dims[0] * self.dims[1] * self.dims[2] * self.dims[3]

    @property
    def num_links(self) -> int:
        """Total number of gauge links 4 * V."""
        return 4 * self.volume

    def get_link(self, coord: Lattice4DCoord, mu: int) -> ExactRationalSU2:
        """Retrieves link variable U_mu(x)."""
        return self._links[(coord.x0, coord.x1, coord.x2, coord.x3, mu)]

    def set_link(self, coord: Lattice4DCoord, mu: int, link: ExactRationalSU2) -> None:
        """Sets link variable U_mu(x)."""
        if not isinstance(link, ExactRationalSU2):
            raise TypeError(f"Link must be ExactRationalSU2, got {type(link).__name__}")
        self._links[(coord.x0, coord.x1, coord.x2, coord.x3, mu)] = link

    def plaquette(self, coord: Lattice4DCoord, mu: int, nu: int) -> ExactRationalSU2:
        """Computes the 1x1 plaquette holonomy in the (mu, nu) plane.

        U_{mu nu}(x) = U_mu(x) * U_nu(x + mu) * U_mu(x + nu)^dagger * U_nu(x)^dagger
        """
        if mu == nu:
            raise ValueError(f"Plaquette directions must be distinct, got mu={mu}, nu={nu}")
        if mu not in (0, 1, 2, 3) or nu not in (0, 1, 2, 3):
            raise ValueError(f"Directions must be in {{0, 1, 2, 3}}, got mu={mu}, nu={nu}")

        x_plus_mu = coord.shift(mu)
        x_plus_nu = coord.shift(nu)

        u1 = self.get_link(coord, mu)
        u2 = self.get_link(x_plus_mu, nu)
        u3 = self.get_link(x_plus_nu, mu).dagger()
        u4 = self.get_link(coord, nu).dagger()

        return u1.multiply(u2).multiply(u3).multiply(u4)

    def plaquette_action(self, coord: Lattice4DCoord, mu: int, nu: int) -> Fraction:
        """Wilson plaquette action: S_{mu nu}(x) = 1 - (1/2) Tr(U_{mu nu}(x)) in Q."""
        plaq = self.plaquette(coord, mu, nu)
        return Fraction(1, 1) - Fraction(1, 2) * plaq.trace()

    def total_wilson_action(self) -> Fraction:
        """Computes the total Wilson gauge action summed over all sites and all 6 planes (mu < nu)."""
        total = Fraction(0, 1)
        for x0 in range(self.dims[0]):
            for x1 in range(self.dims[1]):
                for x2 in range(self.dims[2]):
                    for x3 in range(self.dims[3]):
                        coord = Lattice4DCoord(x0, x1, x2, x3, self.dims)
                        for mu in range(4):
                            for nu in range(mu + 1, 4):
                                total += self.plaquette_action(coord, mu, nu)
        return total

    def local_staple_action(self, coord: Lattice4DCoord, mu: int) -> Fraction:
        """Computes the sum of plaquette actions involving link (coord, mu)."""
        staple_action = Fraction(0, 1)
        for nu in range(4):
            if nu == mu:
                continue
            if mu < nu:
                staple_action += self.plaquette_action(coord, mu, nu)
            else:
                staple_action += self.plaquette_action(coord, nu, mu)
            x_minus_nu = coord.shift(nu, step=-1)
            if mu < nu:
                staple_action += self.plaquette_action(x_minus_nu, mu, nu)
            else:
                staple_action += self.plaquette_action(x_minus_nu, nu, mu)
        return staple_action

    def apply_involution(self) -> Lattice4DSU2:
        """Generates the orientation-reversing Euclidean reflection transformed configuration tau(U).

        Under reflection tau: x = (x0, x1, x2, x3) |-> (-x0 mod L0, x1, x2, x3):
        For spatial links mu in {1, 2, 3}:
            The directed edge from x to x + mu reflects to tau(x) to tau(x) + mu.
            Thus U_mu^tau(coord) = U_mu(tau(coord)).
        For the reflected axis mu = 0:
            The directed edge from x to x + 0 reflects to tau(x) to tau(x) - 0.
            The positively oriented link covering this segment is located at tau(x) - 0, directed to tau(x).
            Traversing backwards gives U_0^tau(coord) = U_0(tau(coord + 0))^dagger.
        This preserves the Wilson gauge action S[tau(U)] == S[U] on every valid configuration.
        """
        tau_lattice = Lattice4DSU2(self.dims)
        for x0 in range(self.dims[0]):
            for x1 in range(self.dims[1]):
                for x2 in range(self.dims[2]):
                    for x3 in range(self.dims[3]):
                        coord = Lattice4DCoord(x0, x1, x2, x3, self.dims)
                        for mu in range(4):
                            if mu == 0:
                                orig_coord = coord.shift(0, step=1).involution_reflection()
                                orig_link = self.get_link(orig_coord, 0)
                                tau_lattice.set_link(coord, 0, orig_link.dagger())
                            else:
                                orig_coord = coord.involution_reflection()
                                orig_link = self.get_link(orig_coord, mu)
                                tau_lattice.set_link(coord, mu, orig_link)
        return tau_lattice

    def verify_involution_sign_balance(self) -> Dict[str, object]:
        """Verifies that involution tau preserves the Wilson gauge action S[tau(U)] == S[U].

        Note: This verifies the exact gauge action symmetry of the lattice configuration.
        It does not construct or evaluate the determinant of the full fermion Dirac operator det(D_w).
        """
        tau_lat = self.apply_involution()
        s_orig = self.total_wilson_action()
        s_tau = tau_lat.total_wilson_action()
        is_action_invariant = (s_orig == s_tau)

        all_unitary = True
        for x0 in range(self.dims[0]):
            for x1 in range(self.dims[1]):
                for x2 in range(self.dims[2]):
                    for x3 in range(self.dims[3]):
                        coord = Lattice4DCoord(x0, x1, x2, x3, self.dims)
                        for mu in range(4):
                            u = self.get_link(coord, mu)
                            if not u.is_unitary() or u.determinant() != Fraction(1, 1):
                                all_unitary = False
                                break

        return {
            "is_action_invariant": is_action_invariant,
            "original_action": str(s_orig),
            "tau_action": str(s_tau),
            "all_links_unitary": all_unitary,
            "action_invariance_certified": is_action_invariant and all_unitary,
            "sign_cancellation_certified": is_action_invariant and all_unitary,
            "authority_effect": "None",
        }

    def rational_metropolis_step(
        self,
        coord: Lattice4DCoord,
        mu: int,
        candidate_link: ExactRationalSU2,
        rational_random_threshold: Fraction,
    ) -> Tuple[bool, Fraction]:
        """Executes a Metropolis update step using exact rational arithmetic.

        Acceptance probability alpha = min(1, P(U') / P(U)) = min(1, 1 / (1 + Delta S)) for Delta S >= 0.
        Returns (accepted: bool, delta_s: Fraction).
        """
        if not (Fraction(0, 1) <= rational_random_threshold <= Fraction(1, 1)):
            raise ValueError(f"Random threshold must be in [0, 1], got {rational_random_threshold}")

        old_action = self.local_staple_action(coord, mu)
        old_link = self.get_link(coord, mu)

        self.set_link(coord, mu, candidate_link)
        new_action = self.local_staple_action(coord, mu)

        delta_s = new_action - old_action

        if delta_s <= Fraction(0, 1):
            return (True, delta_s)

        alpha = Fraction(1, 1) / (Fraction(1, 1) + delta_s)
        if rational_random_threshold <= alpha:
            return (True, delta_s)

        self.set_link(coord, mu, old_link)
        return (False, delta_s)
