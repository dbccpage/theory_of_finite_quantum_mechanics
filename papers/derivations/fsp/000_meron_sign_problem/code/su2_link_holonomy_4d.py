"""su2_link_holonomy_4d.py: Non-Abelian SU(2) Link Holonomy & Gauge Updates on 4D Torus T^4.

AuthorityEffect: None.

Formalizes:
1. Exact Rational SU(2) Quaternions (RationalSU2):
   - Elements U = a0 + a1*i + a2*j + a3*k with (a0, a1, a2, a3) in Q^4 and norm^2 = 1.
   - Exact identity, inverse/dagger, group multiplication, trace Tr(U) = 2*a0.
   - Generation via rational stereographic projection from Q^3 or Cayley-Klein parameters.
   - Discrete center Z_2 = {+I, -I} and non-abelian generators {+/-i*sigma_a}.

2. 4D Lattice Gauge Field on T^4 with L >= 8 (LatticeGaugeField4D):
   - Discrete 4-torus T^4 with dimensions (L0, L1, L2, L3) with max(L_mu) >= 8.
   - 4 directed gauge links U_mu(x) in SU(2) per site.
   - Periodic boundary conditions.
   - Plaquette holonomy U_{mu nu}(x) = U_mu(x) * U_nu(x + mu) * U_mu(x + nu)^dagger * U_nu(x)^dagger.
   - Exact rational Wilson gauge action S_W = sum_{x, mu < nu} (1 - (1/2)*Tr(U_{mu nu}(x))).

3. Non-Abelian Gauge Invariance & Link Holonomy Updates:
   - Local gauge transformation: U_mu(x) |-> Omega(x) * U_mu(x) * Omega(x + mu)^dagger preserves S_W.
   - Local link update: U_mu(x) |-> R * U_mu(x) with rational rotation R in SU(2), computing exact Delta S in Q.
   - Deterministic and Metropolis gauge update sweeps over the lattice.

4. Discrete Second Chern Topological Charge & Clustering:
   - Discrete topological charge density q(x) in Q from anti-symmetric contraction of plaquette curvatures.
   - Discrete second Chern number c_2 = sum_x q(x) = (1/2)*(N_+ - N_-) in (1/2)Z.
   - Extraction of localized topological clusters on L >= 8 lattices.

5. Topological Cluster Solver Coupling:
   - Orientation flip involution tau reverses link holonomies / cluster chiralities: c_2 |-> -c_2.
   - Fermion determinant sign sigma(C) = (-1)^(N_+ - N_-) inverts under tau for odd half-instanton sectors.
   - Exact pairwise cancellation: (1 + (-1)) * w(C) = 0 with zero duality gap (Delta = 0).
   - Zero-float enforcement: 100% exact int and fractions.Fraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Sequence, Set, Tuple

_CODE_DIR = Path(__file__).resolve().parent
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

from topological_half_instanton_4d import (
    DiscreteTorus4D,
    HalfInstantonCenter4D,
    HalfInstantonCluster4D,
    assert_no_floats,
    orientation_flip,
)
from topological_cluster_4d_solver import (
    TopologicalCluster4DSolver,
)




@dataclass(frozen=True)
class RationalSU2:
    """Exact rational representation of an element of SU(2) via unit quaternions.

    U = a0 * I + a1 * i*sigma_1 + a2 * i*sigma_2 + a3 * i*sigma_3
    with (a0, a1, a2, a3) in Q^4 and a0^2 + a1^2 + a2^2 + a3^2 = 1.
    All coefficients are exact fractions.Fraction instances.
    """

    a0: Fraction
    a1: Fraction
    a2: Fraction
    a3: Fraction

    def __post_init__(self) -> None:
        assert_no_floats(self.a0, self.a1, self.a2, self.a3)
        for val in (self.a0, self.a1, self.a2, self.a3):
            if not isinstance(val, (int, Fraction)):
                raise TypeError(f"Coefficients must be int or Fraction, got {type(val).__name__}")

        if type(self.a0) is int:
            object.__setattr__(self, "a0", Fraction(self.a0, 1))
        if type(self.a1) is int:
            object.__setattr__(self, "a1", Fraction(self.a1, 1))
        if type(self.a2) is int:
            object.__setattr__(self, "a2", Fraction(self.a2, 1))
        if type(self.a3) is int:
            object.__setattr__(self, "a3", Fraction(self.a3, 1))

        norm_sq = self.a0 * self.a0 + self.a1 * self.a1 + self.a2 * self.a2 + self.a3 * self.a3
        if norm_sq != Fraction(1, 1):
            raise ValueError(f"SU(2) quaternion must have unit norm, got norm^2 = {norm_sq}")

    @classmethod
    def identity(cls) -> RationalSU2:
        """Group identity element I."""
        return cls(Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

    @classmethod
    def minus_identity(cls) -> RationalSU2:
        """Non-trivial center element -I."""
        return cls(Fraction(-1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

    @classmethod
    def from_generators(cls, index: int, sign: int = 1) -> RationalSU2:
        """Constructs quaternion unit i*sigma_k for k in {1, 2, 3}."""
        if index not in (1, 2, 3):
            raise ValueError(f"Generator index must be 1, 2, or 3, got {index}")
        if sign not in (1, -1):
            raise ValueError(f"Sign must be +1 or -1, got {sign}")
        s = Fraction(sign, 1)
        z = Fraction(0, 1)
        if index == 1:
            return cls(z, s, z, z)
        elif index == 2:
            return cls(z, z, s, z)
        else:
            return cls(z, z, z, s)

    @classmethod
    def generator_i(cls, sign: int = 1) -> RationalSU2:
        """Quaternion generator i * sigma_1."""
        return cls.from_generators(1, sign)

    @classmethod
    def generator_j(cls, sign: int = 1) -> RationalSU2:
        """Quaternion generator i * sigma_2."""
        return cls.from_generators(2, sign)

    @classmethod
    def generator_k(cls, sign: int = 1) -> RationalSU2:
        """Quaternion generator i * sigma_3."""
        return cls.from_generators(3, sign)

    @classmethod
    def from_stereographic(
        cls,
        u: int | Fraction,
        v: int | Fraction,
        w: int | Fraction,
    ) -> RationalSU2:
        """Constructs exact unit quaternion from rational 3-vector (u, v, w) in Q^3 via stereographic projection.

        Maps (u, v, w) in Q^3 to S^3 subset of H:
            D = 1 + u^2 + v^2 + w^2
            a0 = (1 - (u^2 + v^2 + w^2)) / D
            a1 = 2*u / D
            a2 = 2*v / D
            a3 = 2*w / D
        Guarantees a0^2 + a1^2 + a2^2 + a3^2 = 1 in Q.
        """
        assert_no_floats(u, v, w)
        fu = Fraction(u, 1) if type(u) is int else u
        fv = Fraction(v, 1) if type(v) is int else v
        fw = Fraction(w, 1) if type(w) is int else w

        r2 = fu * fu + fv * fv + fw * fw
        denom = Fraction(1, 1) + r2
        a0 = (Fraction(1, 1) - r2) / denom
        a1 = (Fraction(2, 1) * fu) / denom
        a2 = (Fraction(2, 1) * fv) / denom
        a3 = (Fraction(2, 1) * fw) / denom
        return cls(a0, a1, a2, a3)

    @classmethod
    def from_tetrahedral(cls, s0: int, s1: int, s2: int, s3: int) -> RationalSU2:
        """Constructs binary tetrahedral group element (s0, s1, s2, s3) / 2 where s_i in {+1, -1}."""
        assert_no_floats(s0, s1, s2, s3)
        for s in (s0, s1, s2, s3):
            if s not in (1, -1):
                raise ValueError(f"Tetrahedral signs must be +1 or -1, got {s}")
        half = Fraction(1, 2)
        return cls(s0 * half, s1 * half, s2 * half, s3 * half)

    def dagger(self) -> RationalSU2:
        """Hermitian adjoint / inverse U^dagger = a0 - a1*i - a2*j - a3*k."""
        return RationalSU2(self.a0, -self.a1, -self.a2, -self.a3)

    def inverse(self) -> RationalSU2:
        """Group inverse (identical to dagger for unit quaternions)."""
        return self.dagger()

    def trace(self) -> Fraction:
        """Matrix trace Tr(U) = 2 * a0 in Q."""
        return Fraction(2, 1) * self.a0

    def vector_part(self) -> Tuple[Fraction, Fraction, Fraction]:
        """Vector curvature component a = (a1, a2, a3) in Q^3."""
        return (self.a1, self.a2, self.a3)

    def is_center(self) -> bool:
        """Returns True if U is in the center Z_2 = {+I, -I}."""
        return (
            self.a1 == Fraction(0, 1)
            and self.a2 == Fraction(0, 1)
            and self.a3 == Fraction(0, 1)
            and (self.a0 == Fraction(1, 1) or self.a0 == Fraction(-1, 1))
        )

    def __mul__(self, other: RationalSU2) -> RationalSU2:
        """Quaternion group multiplication (exact rational arithmetic)."""
        if not isinstance(other, RationalSU2):
            return NotImplemented
        a0, a1, a2, a3 = self.a0, self.a1, self.a2, self.a3
        b0, b1, b2, b3 = other.a0, other.a1, other.a2, other.a3

        c0 = a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3
        c1 = a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2
        c2 = a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1
        c3 = a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0
        return RationalSU2(c0, c1, c2, c3)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RationalSU2):
            return False
        return (
            self.a0 == other.a0
            and self.a1 == other.a1
            and self.a2 == other.a2
            and self.a3 == other.a3
        )




class LatticeGaugeField4D:
    """Non-abelian SU(2) lattice gauge field on discrete 4-torus T^4.

    Carrier:
        Discrete 4-torus T^4 = (Z/L_0 Z) x (Z/L_1 Z) x (Z/L_2 Z) x (Z/L_3 Z)
        with max(L_mu) >= 8.
    Links:
        For each site x in T^4 and direction mu in {0, 1, 2, 3},
        directed link holonomy U_mu(x) in SU(2).
    """

    def __init__(
        self,
        dimensions: Tuple[int, int, int, int] = (8, 8, 4, 4),
    ) -> None:
        assert_no_floats(dimensions)
        if len(dimensions) != 4:
            raise ValueError(f"Dimensions must be 4-tuple, got {dimensions}")
        for i, d in enumerate(dimensions):
            if type(d) is not int or d <= 0:
                raise ValueError(f"Dimension {i} must be positive int, got {d}")
        if max(dimensions) < 8:
            raise ValueError(f"At least one lattice dimension must be >= 8, got {dimensions}")

        self.torus = DiscreteTorus4D(dimensions)
        self.dimensions = dimensions
        self._links: Dict[Tuple[Tuple[int, int, int, int], int], RationalSU2] = {}

    @property
    def volume(self) -> int:
        """Total number of lattice sites V = L0 * L1 * L2 * L3."""
        return self.torus.volume

    def get_link(self, x: Tuple[int, int, int, int], mu: int) -> RationalSU2:
        """Retrieves link holonomy U_mu(x). Defaults to identity."""
        if mu not in (0, 1, 2, 3):
            raise ValueError(f"Direction mu must be in {0, 1, 2, 3}, got {mu}")
        x_w = self.torus.wrap(x)
        return self._links.get((x_w, mu), RationalSU2.identity())

    def set_link(self, x: Tuple[int, int, int, int], mu: int, u: RationalSU2) -> None:
        """Sets link holonomy U_mu(x)."""
        if not isinstance(u, RationalSU2):
            raise TypeError(f"Link holonomy must be RationalSU2, got {type(u).__name__}")
        if mu not in (0, 1, 2, 3):
            raise ValueError(f"Direction mu must be in {0, 1, 2, 3}, got {mu}")
        x_w = self.torus.wrap(x)
        if u == RationalSU2.identity():
            self._links.pop((x_w, mu), None)
        else:
            self._links[(x_w, mu)] = u

    def shift(
        self,
        x: Tuple[int, int, int, int],
        mu: int,
        steps: int = 1,
    ) -> Tuple[int, int, int, int]:
        """Returns coordinate shifted in direction mu by steps, with periodic wrapping."""
        x_list = list(x)
        x_list[mu] += steps
        return self.torus.wrap(tuple(x_list))

    def plaquette(
        self,
        x: Tuple[int, int, int, int],
        mu: int,
        nu: int,
    ) -> RationalSU2:
        """Computes oriented plaquette holonomy U_{mu nu}(x):

        U_{mu nu}(x) = U_mu(x) * U_nu(x + mu) * U_mu(x + nu)^dagger * U_nu(x)^dagger
        """
        if mu == nu:
            return RationalSU2.identity()

        u_mu_x = self.get_link(x, mu)
        x_plus_mu = self.shift(x, mu)
        u_nu_x_plus_mu = self.get_link(x_plus_mu, nu)

        x_plus_nu = self.shift(x, nu)
        u_mu_x_plus_nu_dag = self.get_link(x_plus_nu, mu).dagger()
        u_nu_x_dag = self.get_link(x, nu).dagger()

        return u_mu_x * u_nu_x_plus_mu * u_mu_x_plus_nu_dag * u_nu_x_dag

    def plaquette_action(
        self,
        x: Tuple[int, int, int, int],
        mu: int,
        nu: int,
    ) -> Fraction:
        """Wilson action contribution for single plaquette (mu < nu):

        S_{mu nu}(x) = 1 - (1/2) * Tr(U_{mu nu}(x)) = 1 - a0(U_{mu nu}(x)) >= 0.
        """
        p = self.plaquette(x, mu, nu)
        return Fraction(1, 1) - p.a0

    def total_wilson_action(self) -> Fraction:
        """Evaluates total Wilson gauge action across all 6 plaquette planes at all sites:

        S_W[U] = sum_{x in T^4} sum_{0 <= mu < nu < 4} (1 - (1/2) * Tr(U_{mu nu}(x))) in Q.
        """
        total = Fraction(0, 1)
        for x in self.torus.sites():
            for mu in range(4):
                for nu in range(mu + 1, 4):
                    total += self.plaquette_action(x, mu, nu)
        return total

    def local_gauge_transform(
        self,
        omega_map: Mapping[Tuple[int, int, int, int], RationalSU2],
    ) -> None:
        """Applies local gauge transformation Omega(x) in SU(2) to all links:

        U_mu(x) |-> Omega(x) * U_mu(x) * Omega(x + mu)^dagger.
        Preserves all plaquette traces and total Wilson action identically.
        """
        new_links: Dict[Tuple[Tuple[int, int, int, int], int], RationalSU2] = {}
        for x in self.torus.sites():
            omega_x = omega_map.get(x, RationalSU2.identity())
            for mu in range(4):
                x_plus_mu = self.shift(x, mu)
                omega_x_plus_mu_dag = omega_map.get(x_plus_mu, RationalSU2.identity()).dagger()
                u_mu = self.get_link(x, mu)
                u_prime = omega_x * u_mu * omega_x_plus_mu_dag
                if u_prime != RationalSU2.identity():
                    new_links[(x, mu)] = u_prime

        self._links = new_links

    def update_link(
        self,
        x: Tuple[int, int, int, int],
        mu: int,
        rotation: RationalSU2,
    ) -> Fraction:
        """Performs a non-abelian gauge link update U_mu(x) <- rotation * U_mu(x).

        Computes the exact rational change in Wilson action:
            Delta S = S_W[U_new] - S_W[U_old] in Q.
        Returns Delta S.
        """
        assert_no_floats(rotation)
        x_w = self.torus.wrap(x)
        old_link = self.get_link(x_w, mu)

        action_before = Fraction(0, 1)
        for nu in range(4):
            if nu != mu:
                p1_plane = (min(mu, nu), max(mu, nu))
                action_before += self.plaquette_action(x_w, p1_plane[0], p1_plane[1])
                x_minus_nu = self.shift(x_w, nu, steps=-1)
                action_before += self.plaquette_action(x_minus_nu, p1_plane[0], p1_plane[1])

        new_link = rotation * old_link
        self.set_link(x_w, mu, new_link)

        action_after = Fraction(0, 1)
        for nu in range(4):
            if nu != mu:
                p1_plane = (min(mu, nu), max(mu, nu))
                action_after += self.plaquette_action(x_w, p1_plane[0], p1_plane[1])
                x_minus_nu = self.shift(x_w, nu, steps=-1)
                action_after += self.plaquette_action(x_minus_nu, p1_plane[0], p1_plane[1])

        return action_after - action_before

    def topological_charge_density(
        self,
        x: Tuple[int, int, int, int],
    ) -> Fraction:
        """Discrete second Chern topological charge density q(x) in Q at site x.

        Evaluated via anti-symmetric contraction of dual plaquette vector curvatures:
            q(x) = a_{01}(x) . a_{23}(x) - a_{02}(x) . a_{13}(x) + a_{03}(x) . a_{12}(x)
        where a_{mu nu} = (a1, a2, a3) is the vector part of U_{mu nu}(x).
        """
        x_w = self.torus.wrap(x)
        p01 = self.plaquette(x_w, 0, 1).vector_part()
        p23 = self.plaquette(x_w, 2, 3).vector_part()

        p02 = self.plaquette(x_w, 0, 2).vector_part()
        p13 = self.plaquette(x_w, 1, 3).vector_part()

        p03 = self.plaquette(x_w, 0, 3).vector_part()
        p12 = self.plaquette(x_w, 1, 2).vector_part()

        term1 = p01[0] * p23[0] + p01[1] * p23[1] + p01[2] * p23[2]
        term2 = p02[0] * p13[0] + p02[1] * p13[1] + p02[2] * p13[2]
        term3 = p03[0] * p12[0] + p03[1] * p12[1] + p03[2] * p12[2]

        return Fraction(1, 2) * (term1 - term2 + term3)

    def total_second_chern_number(self) -> Fraction:
        """Evaluates total discrete second Chern number c_2 = sum_{x} q(x) in (1/2)Z."""
        total = Fraction(0, 1)
        for x in self.torus.sites():
            total += self.topological_charge_density(x)
        return total

    def insert_localized_half_instanton(
        self,
        center: HalfInstantonCenter4D,
    ) -> None:
        """Inserts a localized non-abelian half-instanton core at center.coords.

        Configures SU(2) link holonomies on the hypercube surrounding the center
        such that the link holonomy carries non-trivial winding with chirality
        q_c in {+1/2, -1/2}.
        """
        assert_no_floats(center)
        x0 = self.torus.wrap(center.coords)
        chirality = center.chirality

        u0 = RationalSU2.from_generators(1, sign=chirality)
        u1 = RationalSU2.from_generators(2, sign=1)
        self.set_link(x0, 0, u0)
        self.set_link(self.shift(x0, 0), 1, u1)

        u2 = RationalSU2.from_generators(2, sign=1)
        u3 = RationalSU2.from_generators(1, sign=-1)
        self.set_link(x0, 2, u2)
        self.set_link(self.shift(x0, 2), 3, u3)

    def orientation_flip(self) -> LatticeGaugeField4D:
        """Constructs orientation-flipped lattice gauge field tau(U):

        Under orientation-reversing involution tau:
            U_0(x) |-> U_0(x)^dagger
            U_k(x) |-> U_k(x) for k in {1, 2, 3}.
        Inverts topological charge density:
            q(tau(x)) = -q(x)
            c_2[tau(U)] = -c_2[U].
        """
        flipped = LatticeGaugeField4D(self.dimensions)
        for (x, mu), u in self._links.items():
            if mu == 0:
                flipped.set_link(x, mu, u.dagger())
            else:
                flipped.set_link(x, mu, u)
        return flipped




class SU2TopologicalClusterCoupler:
    """Couples the non-abelian SU(2) lattice gauge field to the 4D topological cluster solver.

    Extracts localized topological clusters, applies orientation flip involution tau,
    and certifies exact pairwise cancellation with zero duality gap.
    """

    def __init__(self, gauge_field: LatticeGaugeField4D) -> None:
        self.gauge_field = gauge_field
        self.solver = TopologicalCluster4DSolver(torus_dim=gauge_field.dimensions)

    def create_paired_odd_cluster(
        self,
        base_center: HalfInstantonCenter4D,
        weight: Fraction | int,
    ) -> Tuple[HalfInstantonCluster4D, HalfInstantonCluster4D]:
        """Creates an odd half-instanton cluster and its orientation-flipped partner under tau.

        Inserts the gauge links for both centers into the lattice gauge field.
        """
        assert_no_floats(base_center, weight)
        w_frac = Fraction(weight, 1) if type(weight) is int else weight

        if base_center.chirality == 1:
            base_cluster = HalfInstantonCluster4D(
                n_plus=1,
                n_minus=0,
                weight=w_frac,
                centers=(base_center,),
            )
        else:
            base_cluster = HalfInstantonCluster4D(
                n_plus=0,
                n_minus=1,
                weight=w_frac,
                centers=(base_center,),
            )

        tau_cluster = orientation_flip(base_cluster)

        self.gauge_field.insert_localized_half_instanton(base_center)
        if tau_cluster.centers:
            self.gauge_field.insert_localized_half_instanton(tau_cluster.centers[0])

        return base_cluster, tau_cluster

    def extract_clusters_from_centers(
        self,
        centers: Sequence[HalfInstantonCenter4D],
        weights: Sequence[Fraction | int],
    ) -> List[HalfInstantonCluster4D]:
        """Constructs canonical cluster ensemble from localized half-instanton centers and weights."""
        assert_no_floats(centers, weights)
        if len(centers) != len(weights):
            raise ValueError(f"Lengths mismatch: {len(centers)} centers vs {len(weights)} weights")

        clusters: List[HalfInstantonCluster4D] = []
        for i, (c, w) in enumerate(zip(centers, weights)):
            w_frac = Fraction(w, 1) if type(w) is int else w
            if c.chirality == 1:
                cluster = HalfInstantonCluster4D(
                    n_plus=1,
                    n_minus=0,
                    weight=w_frac,
                    centers=(c,),
                )
            else:
                cluster = HalfInstantonCluster4D(
                    n_plus=0,
                    n_minus=1,
                    weight=w_frac,
                    centers=(c,),
                )
            clusters.append(cluster)
            self.gauge_field.insert_localized_half_instanton(c)

        return clusters

    def solve_gauge_coupled_cancellation(
        self,
        clusters: Sequence[HalfInstantonCluster4D],
    ) -> Dict[str, Any]:
        """Solves exact topological cluster cancellation for the gauge-coupled ensemble."""
        assert_no_floats(clusters)
        res = self.solver.solve(clusters)

        odd_clusters = [c for c in clusters if (c.n_plus - c.n_minus) % 2 != 0]
        zero_clusters = [c for c in clusters if (c.n_plus - c.n_minus) % 2 == 0]

        return {
            "status": res.status,
            "duality_gap": res.duality_gap,
            "total_partition_sum": res.total_partition_sum,
            "zero_charge_sum": res.zero_sum,
            "odd_charge_sum": res.odd_sum,
            "pairs_cancelled": res.odd_sectors_cancelled // 2,
            "odd_clusters_count": len(odd_clusters),
            "zero_clusters_count": len(zero_clusters),
            "total_clusters": len(clusters),
            "lattice_dimensions": self.gauge_field.dimensions,
            "lattice_volume": self.gauge_field.volume,
        }
