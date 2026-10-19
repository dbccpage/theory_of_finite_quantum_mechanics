"""
fermionic_hamiltonian.py — Discrete Fermionic Hamiltonian, Path Parities, and Sign Decay

Status: Discrete Mathematical & Computational Model
AuthorityEffect: None
Primary Reference: sealed-derivation-v1 (commit 3100c4e)
Companion: Troyer-Wiese (2005) PRL 94, 170201; paper 023 (PO-023 to PO-028)

Claim Hygiene:
1. What this supports:
   - Discrete Fock space construction for finite lattice fermion models (hopping + Hubbard U).
   - Exact rational many-body Hamiltonian matrices and finite Euler path sums.
   - Numerical spectral estimates of the thermal partition function Tr(e^(-beta H)).
   - Decomposition into configuration paths with explicit permutation parities (-1)^pi(gamma).
   - Signed contributions in explicitly enumerated finite path ensembles.
   - Comparison with discrete Wheeler-DeWitt Hamiltonian scalar constraint H_perp on simplicial complexes.
2. What this does not support:
   - Continuous field theory path integrals, continuous thermodynamic limits (N -> inf), or solving generic NP-hard problems.
3. Narrowest defensible claim:
   - Nonzero signed Euler paths are retained exactly; graph topology alone does not certify sign severity or asymptotic scaling.
4. Next test needed:
   - Feed generated configuration paths into the BQNF cochain quotient evaluator.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Set, Optional, Any
from fractions import Fraction
import json
import math
import itertools
import numpy as np


def exact_fraction(value: int | float | Fraction, name: str) -> Fraction:
    """Keep rationals exact; a finite float means its exact binary value."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        raise TypeError(f"{name} must be an integer, Fraction, or finite float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return Fraction(value)

@dataclass
class FermionicLattice:
    """Finite graph defining lattice sites and hopping edges."""
    num_sites: int
    edges: List[Tuple[int, int]]

    def __post_init__(self) -> None:
        if not isinstance(self.num_sites, int) or self.num_sites <= 0:
            raise ValueError(f"num_sites must be a positive integer, got {self.num_sites}")
        valid_edges = []
        for e in self.edges:
            if len(e) != 2:
                raise ValueError(f"Edge must be a 2-tuple, got {e}")
            u, v = int(e[0]), int(e[1])
            if u < 0 or u >= self.num_sites or v < 0 or v >= self.num_sites:
                raise ValueError(f"Edge ({u}, {v}) outside site range [0, {self.num_sites - 1}]")
            if u == v:
                raise ValueError(f"Self-loops are not permitted in hopping graph: ({u}, {v})")
            low, high = min(u, v), max(u, v)
            if (low, high) not in valid_edges:
                valid_edges.append((low, high))
        self.edges = sorted(valid_edges)

    @classmethod
    def linear_chain(cls, n: int, periodic: bool = False) -> "FermionicLattice":
        if n <= 0:
            raise ValueError(f"Chain length must be positive, got {n}")
        edges = [(i, i + 1) for i in range(n - 1)]
        if periodic and n > 2:
            edges.append((n - 1, 0))
        return cls(num_sites=n, edges=edges)

    @classmethod
    def triangle_cluster(cls) -> "FermionicLattice":
        """Three-site geometry used for a finite signed-path example."""
        return cls(num_sites=3, edges=[(0, 1), (1, 2), (0, 2)])

    @classmethod
    def triangle(cls) -> "FermionicLattice":
        """Alias matching Rust FermionicLattice::triangle()."""
        return cls.triangle_cluster()

    @classmethod
    def square_plaquette(cls) -> "FermionicLattice":
        """Four-site square plaquette matching Rust FermionicLattice::square_plaquette()."""
        return cls(num_sites=4, edges=[(0, 1), (1, 2), (2, 3), (3, 0)])

    @classmethod
    def rectangular_grid(cls, rows: int, cols: int, periodic: bool = False) -> "FermionicLattice":
        """2D rectangular grid of rows x cols sites, matching Rust FermionicLattice::rectangular_grid."""
        if rows <= 0 or cols <= 0:
            raise ValueError("grid dimensions must be positive")
        num_sites = rows * cols
        edges: List[Tuple[int, int]] = []
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if c + 1 < cols:
                    edges.append((idx, r * cols + (c + 1)))
                elif periodic and cols > 2:
                    edges.append((idx, r * cols))
                if r + 1 < rows:
                    edges.append((idx, (r + 1) * cols + c))
                elif periodic and rows > 2:
                    edges.append((idx, c))
        return cls(num_sites=num_sites, edges=edges)

    @classmethod
    def triangular_ladder(cls, rungs: int) -> "FermionicLattice":
        """2-leg frustrated triangular ladder with `rungs` rungs (2 * rungs sites)."""
        if rungs < 2:
            raise ValueError("triangular ladder requires at least 2 rungs")
        num_sites = 2 * rungs
        edges: List[Tuple[int, int]] = []
        for i in range(rungs):
            top = 2 * i
            bot = 2 * i + 1
            edges.append((top, bot))
            if i + 1 < rungs:
                next_top = 2 * (i + 1)
                next_bot = 2 * (i + 1) + 1
                edges.append((top, next_top))
                edges.append((bot, next_bot))
                edges.append((top, next_bot))
        return cls(num_sites=num_sites, edges=edges)


@dataclass(frozen=True)
class FockState:
    """
    Many-body state represented by occupied sites for spin-up and spin-down.
    Each is a bitmask of length num_sites.
    """
    up_mask: int
    down_mask: int

    def __post_init__(self) -> None:
        if self.up_mask < 0 or self.down_mask < 0:
            raise ValueError(f"Occupation masks must be non-negative: up={self.up_mask}, down={self.down_mask}")

    def count_up(self) -> int:
        return bin(self.up_mask).count("1")

    def count_down(self) -> int:
        return bin(self.down_mask).count("1")

    def total_particles(self) -> int:
        return self.count_up() + self.count_down()

    def is_occupied(self, site: int, spin: str) -> bool:
        mask = self.up_mask if spin == "up" else self.down_mask
        return bool(mask & (1 << site))


class DiscreteFermionicHamiltonian:
    """
    Exact matrix and path representation of Fermi-Hubbard Hamiltonian:
    H = -t sum_{<i,j>, sigma} (c_{i sigma}^dagger c_{j sigma} + h.c.) + U sum_i n_{i up} n_{i down}
    """
    def __init__(self, lattice: FermionicLattice, t: int | float | Fraction = 1.0, u: int | float | Fraction = 2.0, num_up: int = 1, num_down: int = 1):
        try:
            exact_t = exact_fraction(t, "t")
            exact_u = exact_fraction(u, "u")
        except ValueError as exc:
            raise ValueError("Couplings t and u must be finite real numbers") from exc
        if not isinstance(num_up, int) or not isinstance(num_down, int):
            raise TypeError("Fermion particle counts must be integers")
        if num_up < 0 or num_down < 0:
            raise ValueError(f"Fermion counts must be non-negative, got num_up={num_up}, num_down={num_down}")
        if num_up + num_down == 0:
            raise ValueError("Must specify at least one fermion in physical sector")
        if num_up > lattice.num_sites or num_down > lattice.num_sites:
            raise ValueError(
                f"Fermion counts (up={num_up}, down={num_down}) cannot exceed lattice sites ({lattice.num_sites})"
            )

        self.lattice = lattice
        self.t = exact_t
        self.u = exact_u
        self.num_up = int(num_up)
        self.num_down = int(num_down)
        self.basis: List[FockState] = self._build_basis()
        if not self.basis:
            raise ValueError("Empty physical Fock basis")
        self.basis_index: Dict[FockState, int] = {st: idx for idx, st in enumerate(self.basis)}
        self.dim = len(self.basis)
        self.matrix: List[List[Fraction]] = self._build_hamiltonian_matrix()

    @classmethod
    def create_free_triangle(cls, t: float = 1.0, num_up: int = 2, num_down: int = 0) -> "DiscreteFermionicHamiltonian":
        """Convenience constructor for the 3-site spinless free fermion triangle benchmark."""
        lattice = FermionicLattice.triangle_cluster()
        return cls(lattice=lattice, t=t, u=0.0, num_up=num_up, num_down=num_down)

    def _build_basis(self) -> List[FockState]:
        """Construct all Fock states with declared particle counts."""
        n = self.lattice.num_sites
        all_sites = range(n)
        up_combos = [sum(1 << s for s in combo) for combo in itertools.combinations(all_sites, self.num_up)]
        down_combos = [sum(1 << s for s in combo) for combo in itertools.combinations(all_sites, self.num_down)]

        basis = []
        for u_m in up_combos:
            for d_m in down_combos:
                basis.append(FockState(up_mask=u_m, down_mask=d_m))
        return basis

    def _fermionic_sign(self, mask: int, site1: int, site2: int) -> int:
        """
        Computes the Jordan-Wigner / anticommutation phase (-1)^p
        when hopping between site1 and site2.
        p is the number of occupied sites strictly between min(site1, site2) and max(site1, site2).
        """
        low, high = min(site1, site2), max(site1, site2)
        count = 0
        for s in range(low + 1, high):
            if mask & (1 << s):
                count += 1
        return -1 if (count % 2 == 1) else 1

    def _build_hamiltonian_matrix(self) -> List[List[Fraction]]:
        dim = self.dim
        mat = [[Fraction(0) for _ in range(dim)] for _ in range(dim)]

        for i, state in enumerate(self.basis):
            diag_e = Fraction(0)
            for s in range(self.lattice.num_sites):
                if state.is_occupied(s, "up") and state.is_occupied(s, "down"):
                    diag_e += self.u
            mat[i][i] += diag_e

            for (u_site, v_site) in self.lattice.edges:
                for (src, dst) in [(u_site, v_site), (v_site, u_site)]:
                    if state.is_occupied(src, "up") and not state.is_occupied(dst, "up"):
                        sign = self._fermionic_sign(state.up_mask, src, dst)
                        new_up = (state.up_mask ^ (1 << src)) | (1 << dst)
                        new_state = FockState(up_mask=new_up, down_mask=state.down_mask)
                        j = self.basis_index[new_state]
                        mat[j][i] += -self.t * sign

                    if state.is_occupied(src, "down") and not state.is_occupied(dst, "down"):
                        sign = self._fermionic_sign(state.down_mask, src, dst)
                        new_down = (state.down_mask ^ (1 << src)) | (1 << dst)
                        new_state = FockState(up_mask=state.up_mask, down_mask=new_down)
                        j = self.basis_index[new_state]
                        mat[j][i] += -self.t * sign

        return mat

    def compute_exact_thermal_trace(self, beta: float) -> float:
        """
        Numerically estimates Tr(e^(-beta * H)) by spectral decomposition.
        The legacy method name distinguishes the exponential from Euler steps;
        floating-point eigenvalues and exponentials are not exact certificates.
        For any finite-dimensional Hermitian matrix H and finite real beta, Z_exact > 0 strictly.
        """
        if not math.isfinite(beta) or beta <= 0:
            raise ValueError(f"beta must be a positive finite real number, got {beta}")
        h_arr = np.array(self.matrix, dtype=float)
        h_herm = (h_arr + h_arr.T) / 2.0
        eigvals = np.linalg.eigvalsh(h_herm)
        z_exact = float(np.sum(np.exp(-float(beta) * eigvals)))
        return z_exact

    def compute_partition_functions(self, beta: int | float | Fraction, trotter_steps: int = 4) -> Dict[str, Any]:
        """
        Evaluates discrete imaginary-time path partition functions:
        Z_ferm = Tr( (I - dtau * H)^M ) with exact signs
        Z_bos  = Tr( |I - dtau * H|^M ) (absolute / sign-quenched ensemble)
        Average Sign <Sign> = Z_ferm / Z_bos
        Rational fields retain exact Euler sums. Legacy numeric fields and the
        spectral exponential/error comparison are floating-point displays.
        """
        if not math.isfinite(beta) or beta <= 0:
            raise ValueError(f"beta must be a positive finite real number, got {beta}")
        if not isinstance(trotter_steps, int) or trotter_steps < 1:
            raise ValueError(f"trotter_steps must be a positive integer >= 1, got {trotter_steps}")

        dtau = exact_fraction(beta, "beta") / trotter_steps
        dim = self.dim

        T_ferm = self.exact_transfer_matrix(beta, trotter_steps)
        T_bos = [[abs(T_ferm[i][j]) for j in range(dim)] for i in range(dim)]

        def mat_mult(A: List[List[Fraction]], B: List[List[Fraction]]) -> List[List[Fraction]]:
            n = len(A)
            C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                row_a = A[i]
                row_c = C[i]
                for k in range(n):
                    aik = row_a[k]
                    if aik == 0:
                        continue
                    row_b = B[k]
                    for j in range(n):
                        bkj = row_b[j]
                        if bkj != 0:
                            row_c[j] += aik * bkj
            return C

        P_ferm = T_ferm
        P_bos = T_bos
        for _ in range(trotter_steps - 1):
            P_ferm = mat_mult(P_ferm, T_ferm)
            P_bos = mat_mult(P_bos, T_bos)

        z_ferm = sum((P_ferm[i][i] for i in range(dim)), Fraction(0))
        z_bos = sum((P_bos[i][i] for i in range(dim)), Fraction(0))
        avg_sign = z_ferm / z_bos if z_bos > 0 else Fraction(0)

        z_exact = self.compute_exact_thermal_trace(beta)
        discretization_error = abs(z_ferm - z_exact) / z_exact if z_exact > 0 else 0.0

        h_arr = np.array(self.matrix, dtype=float)
        eigvals = np.linalg.eigvalsh((h_arr + h_arr.T) / 2.0)
        max_abs_eig = float(np.max(np.abs(eigvals))) if len(eigvals) > 0 else 0.0
        euler_radius_safe = bool(dtau * max_abs_eig < 1.0)

        return {
            "beta": beta,
            "trotter_steps": trotter_steps,
            "dtau": float(dtau),
            "z_fermionic": float(z_ferm),
            "z_bosonic": float(z_bos),
            "z_fermionic_exact": z_ferm,
            "z_bosonic_exact": z_bos,
            "average_sign_exact": avg_sign,
            "z_fermionic_rational": str(z_ferm),
            "z_bosonic_rational": str(z_bos),
            "average_sign_rational": str(avg_sign),
            "z_exact": z_exact,
            "trotter_discretization_error": discretization_error,
            "euler_contraction_safe": euler_radius_safe,
            "max_abs_eigenvalue": max_abs_eig,
            "average_sign": float(avg_sign),
            "sign_problem_severity": float(1 - avg_sign)
        }

    def exact_transfer_matrix(self, beta: int | float | Fraction, trotter_steps: int) -> List[List[Fraction]]:
        """Exact finite Euler transfer I - (beta/M) H; no exponential claim."""
        exact_beta = exact_fraction(beta, "beta")
        if exact_beta <= 0:
            raise ValueError("beta must be positive")
        if isinstance(trotter_steps, bool) or not isinstance(trotter_steps, int) or trotter_steps < 1:
            raise ValueError("trotter_steps must be a positive integer")
        dtau = exact_beta / trotter_steps
        return [[Fraction(i == j) - dtau * self.matrix[i][j]
                 for j in range(self.dim)] for i in range(self.dim)]

    def generate_sample_paths(self, beta: int | float | Fraction, trotter_steps: int = 3) -> List[Dict[str, Any]]:
        """
        Enumerates every nonzero cyclic Euler path with rational amplitudes.
        This costs dim**M candidate paths. "parity" is the full weight sign;
        negative diagonal Euler factors can also contribute, beyond exchange.
        """
        T = self.exact_transfer_matrix(beta, trotter_steps)
        dim = self.dim

        paths = []
        indices = range(dim)
        for seq in itertools.product(indices, repeat=trotter_steps):
            closed_seq = seq + (seq[0],)
            w_signed = Fraction(1)
            for k in range(trotter_steps):
                u, v = closed_seq[k], closed_seq[k+1]
                w_signed *= T[v][u]

            if w_signed != 0:
                sign = 1 if w_signed > 0 else (-1 if w_signed < 0 else 0)
                paths.append({
                    "path_indices": closed_seq,
                    "signed_amplitude": w_signed,
                    "abs_weight": abs(w_signed),
                    "parity": sign,
                    "is_cancelling": sign < 0
                })
        return paths


def free_triangle_analytics(beta: float = 2.0, t: float = 1.0) -> Dict[str, Any]:
    """
    Analytical solution for the 3-site spinless free fermion triangle (U=0, 2 identical fermions).
    Single-particle Hamiltonian on the triangle with hopping t has eigenvalues:
      lambda_sp in {-2t, t, t}.
    Two-particle sector has eigenvalues:
      E_1 = -2t + t = -t
      E_2 = -2t + t = -t
      E_3 = t + t = 2t.
    For t = 1.0: E in {-1, -1, 2}.
    Exact partition function:
      Z(beta) = 2 * exp(beta) + exp(-2*beta).
    At beta = 2.0:
      Z(2) = 2 * exp(2) + exp(-4) = 14.796427836750041.
    Demonstrates that the sign problem is representation-dependent:
    the occupation-basis Trotter sum has alternating signs on the frustrated odd cycle,
    whereas diagonalizing in single-particle eigenmodes solves the problem in O(N^3) time.
    """
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError(f"beta must be a positive finite real number, got {beta}")
    if not math.isfinite(t):
        raise ValueError(f"t must be finite, got {t}")

    sp_energies = [-2.0 * t, 1.0 * t, 1.0 * t]
    mb_energies = [-1.0 * t, -1.0 * t, 2.0 * t]
    z_exact = float(sum(math.exp(-beta * e) for e in mb_energies))

    return {
        "beta": beta,
        "t": t,
        "single_particle_energies": sp_energies,
        "two_particle_energies": mb_energies,
        "exact_partition_function": z_exact,
        "is_representation_dependent": True,
        "single_particle_solvable": True,
    }


@dataclass
class WheelerDeWittToyConstraint:
    r"""
    Discrete Wheeler-DeWitt Hamiltonian scalar constraint diagnostic:
    H_perp(v) = (1 / sqrt(q_v)) * sum_{e, e' \supset v} G_ee' pi_e pi_e' - sqrt(q_v) R(v)
    """
    vertices: List[int]
    momenta: Dict[int, float]
    curvatures: Dict[int, float]
    dual_volumes: Dict[int, float]

    def evaluate_scalar_violations(self) -> Dict[int, float]:
        """Calculates scalar constraint violation at each vertex."""
        violations = {}
        for v in self.vertices:
            vol = self.dual_volumes.get(v, 1.0)
            curv = self.curvatures.get(v, 0.0)
            p_energy = sum(p**2 for p in self.momenta.values()) / max(len(self.momenta), 1)
            violations[v] = (p_energy / math.sqrt(vol)) - math.sqrt(vol) * curv
        return violations

    def evaluate_l1_hamiltonian_defect(self) -> float:
        """Total ||H_perp||_1 violation."""
        violations = self.evaluate_scalar_violations()
        return sum(abs(val) for val in violations.values())


@dataclass(frozen=True)
class FockLatticeScalingRow:
    """Exact rational Fock-space partition function row matching Rust FockLatticeScalingRow."""
    label: str
    num_sites: int
    num_edges: int
    num_up: int
    num_down: int
    fock_dim: int
    trotter_steps: int
    z_fermionic: Fraction
    z_bosonic: Fraction
    average_sign: Fraction
    has_sign_cancellation: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "num_sites": self.num_sites,
            "num_edges": self.num_edges,
            "num_up": self.num_up,
            "num_down": self.num_down,
            "fock_dim": self.fock_dim,
            "trotter_steps": self.trotter_steps,
            "z_fermionic": str(self.z_fermionic),
            "z_bosonic": str(self.z_bosonic),
            "average_sign": str(self.average_sign),
            "has_sign_cancellation": self.has_sign_cancellation,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FockLatticeScalingRow":
        return cls(
            label=str(data["label"]),
            num_sites=int(data["num_sites"]),
            num_edges=int(data["num_edges"]),
            num_up=int(data["num_up"]),
            num_down=int(data["num_down"]),
            fock_dim=int(data["fock_dim"]),
            trotter_steps=int(data["trotter_steps"]),
            z_fermionic=Fraction(str(data["z_fermionic"])),
            z_bosonic=Fraction(str(data["z_bosonic"])),
            average_sign=Fraction(str(data["average_sign"])),
            has_sign_cancellation=bool(data["has_sign_cancellation"]),
        )


def benchmark_fock_lattice_scaling(
    beta: int | float | Fraction = Fraction(2),
    trotter_steps: int = 3,
) -> List[FockLatticeScalingRow]:
    """Finite lattice scaling benchmark for exact Fock-space partition functions across
    1D chains/rings, 2D rectangular grids, and frustrated triangular ladders up to N = 8 sites.
    Matches Rust tfqm_fsp::benchmark_fock_lattice_scaling bit-for-bit.
    """
    exact_beta = exact_fraction(beta, "beta")
    if exact_beta <= 0:
        raise ValueError("beta must be positive")
    if isinstance(trotter_steps, bool) or not isinstance(trotter_steps, int) or trotter_steps < 1:
        raise ValueError("trotter_steps must be a positive integer")

    specs: List[Tuple[str, FermionicLattice, int, int, Fraction]] = [
        ("triangle_3", FermionicLattice.triangle(), 2, 0, Fraction(0)),
        ("square_4", FermionicLattice.square_plaquette(), 2, 0, Fraction(0)),
        ("ring_5_frustrated", FermionicLattice.linear_chain(5, True), 2, 0, Fraction(0)),
        ("chain_6_open", FermionicLattice.linear_chain(6, False), 3, 0, Fraction(0)),
        ("ladder_2x3_rect", FermionicLattice.rectangular_grid(2, 3, False), 2, 1, Fraction(2)),
        ("triangular_ladder_6", FermionicLattice.triangular_ladder(3), 2, 0, Fraction(0)),
        ("ring_7_frustrated", FermionicLattice.linear_chain(7, True), 2, 0, Fraction(0)),
        ("grid_2x4_rect", FermionicLattice.rectangular_grid(2, 4, False), 2, 0, Fraction(0)),
        ("triangular_ladder_8", FermionicLattice.triangular_ladder(4), 2, 0, Fraction(0)),
    ]

    rows: List[FockLatticeScalingRow] = []
    for label, lattice, num_up, num_down, u_val in specs:
        ham = DiscreteFermionicHamiltonian(
            lattice=lattice,
            t=Fraction(1),
            u=u_val,
            num_up=num_up,
            num_down=num_down,
        )
        res = ham.compute_partition_functions(beta=exact_beta, trotter_steps=trotter_steps)
        z_ferm: Fraction = res["z_fermionic_exact"]
        z_bos: Fraction = res["z_bosonic_exact"]
        avg_sign: Fraction = res["average_sign_exact"]
        rows.append(
            FockLatticeScalingRow(
                label=label,
                num_sites=lattice.num_sites,
                num_edges=len(lattice.edges),
                num_up=num_up,
                num_down=num_down,
                fock_dim=ham.dim,
                trotter_steps=trotter_steps,
                z_fermionic=z_ferm,
                z_bosonic=z_bos,
                average_sign=avg_sign,
                has_sign_cancellation=avg_sign < Fraction(1),
            )
        )
    return rows


def fock_scaling_to_canonical_json(rows: List[FockLatticeScalingRow]) -> str:
    """Serialize FockLatticeScalingRow list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def fock_scaling_from_canonical_json(json_str: str) -> List[FockLatticeScalingRow]:
    """Deserialize FockLatticeScalingRow list from canonical JSON string."""
    raw = json.loads(json_str)
    return [FockLatticeScalingRow.from_dict(item) for item in raw]

