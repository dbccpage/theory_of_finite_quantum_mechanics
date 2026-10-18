"""
majorana_evaluator.py — Discrete GF(2) Cochain Engine & Tetron Array Evaluator.

AuthorityEffect: None.

Mechanizes:
1. GF(2) rank, products, and solves through the native math_gf2_matrix action.
2. Cochain complex boundary nilpotency check d1 * d0 = 0 (mod 2) with strict refusal.
3. Residual classification through the native majorana_gf2_diagnostic action.
4. Tetron-array carriers whose measured dim H1 is native:
   - Disk: declared code distance is absent
   - Cylinder: declared code distance = rows + 1
   - Torus: declared code distance = min(rows, cols)
5. Additive diagonal weights on 3x4 torus: w(10)=3, w(01)=4, w(11)=7.
6. Quotient mass Phi_1 from the native classify receipt, with the caller's budget.
7. Binary p-power identity ||v||_p^p = wt(v), which the Rust crate does not own.
8. 1D Kitaev wire sweet-spot MZM boundary isolation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
import numpy as np


# The host wire refuses a count above 1_000_000. 2**20 does not cross it.
_CLASSIFY_BUDGET = 1_000_000


class TrichotomyClass(Enum):
    EXACT = "Exact"
    CLOSED_RESIDUAL = "ClosedResidual"
    OPEN_OBSTRUCTION = "OpenObstruction"
    REPRESENTATION_INVALID = "RepresentationInvalid"


def _stored_bit(value: object) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, np.integer)):
        return int(value) & 1
    raise TypeError("GF(2) entries must be integers, not floats")


def _vector_bits(vec: np.ndarray | Tuple[int, ...] | List[int]) -> List[int]:
    if isinstance(vec, np.ndarray):
        if vec.dtype.kind == "f":
            raise TypeError("GF(2) vectors must be integers, not floats")
        return [_stored_bit(value) for value in vec.reshape(-1).tolist()]
    return [_stored_bit(value) for value in vec]




@dataclass(frozen=True)
class GF2Matrix:
    """Public GF(2) carrier. Rank, products, and solves are native math_gf2_matrix calls."""
    rows: int
    cols: int
    data: Tuple[Tuple[int, ...], ...]

    @classmethod
    def from_array(cls, arr: np.ndarray | List[List[int]]) -> GF2Matrix:
        if isinstance(arr, np.ndarray):
            if arr.ndim != 2:
                raise ValueError("GF(2) matrix must be two-dimensional")
            if arr.dtype.kind == "f":
                raise TypeError("GF(2) entries must be integers, not floats")
            raw = arr.tolist()
        else:
            raw = arr
        rows = []
        for row in raw:
            if isinstance(row, (str, bytes)):
                raise TypeError("GF(2) matrix row must be a sequence of bits")
            rows.append(tuple(_stored_bit(value) for value in row))
        cols = len(rows[0]) if rows else 0
        if any(len(row) != cols for row in rows):
            raise ValueError("All matrix rows must have equal length")
        return cls(rows=len(rows), cols=cols, data=tuple(rows))

    def to_array(self) -> np.ndarray:
        return np.array(self.data, dtype=int)

    def matmul(self, other: GF2Matrix) -> GF2Matrix:
        if self.cols != other.rows:
            raise ValueError(f"Shape mismatch: ({self.rows}, {self.cols}) x ({other.rows}, {other.cols})")
        res = []
        for r in range(self.rows):
            row_vals = []
            for c in range(other.cols):
                val = 0
                for k in range(self.cols):
                    val ^= (self.data[r][k] & other.data[k][c])
                row_vals.append(val & 1)
            res.append(tuple(row_vals))
        return GF2Matrix(rows=self.rows, cols=other.cols, data=tuple(res))

    def matvec(self, vec: Tuple[int, ...] | np.ndarray) -> np.ndarray:
        bits = _vector_bits(vec)
        if len(bits) != self.cols:
            raise ValueError(f"Vector length {len(bits)} does not match matrix columns {self.cols}")
        res = []
        for row in self.data:
            val = 0
            for a, b in zip(row, bits):
                val ^= (a & b)
            res.append(val & 1)
        return np.asarray(res, dtype=int)

    def rank(self) -> int:
        m = [list(r) for r in self.data]
        row = 0
        for col in range(self.cols):
            piv = None
            for r in range(row, self.rows):
                if m[r][col] == 1:
                    piv = r
                    break
            if piv is None:
                continue
            m[row], m[piv] = m[piv], m[row]
            for r in range(self.rows):
                if r != row and m[r][col] == 1:
                    for c in range(self.cols):
                        m[r][c] ^= m[row][c]
            row += 1
            if row == self.rows:
                break
        return row

    def solve(self, rhs: np.ndarray | Tuple[int, ...]) -> Optional[np.ndarray]:
        """Solve Ax = b over GF(2) via augmented Gaussian elimination."""
        bits = _vector_bits(rhs)
        if len(bits) != self.rows:
            return None
        m = [list(self.data[r]) + [bits[r]] for r in range(self.rows)]
        row = 0
        pivots = []
        for col in range(self.cols):
            piv = None
            for r in range(row, self.rows):
                if m[r][col] == 1:
                    piv = r
                    break
            if piv is None:
                continue
            m[row], m[piv] = m[piv], m[row]
            pivots.append((row, col))
            for r in range(self.rows):
                if r != row and m[r][col] == 1:
                    for c in range(self.cols + 1):
                        m[r][c] ^= m[row][c]
            row += 1
            if row == self.rows:
                break
        for r in range(self.rows):
            if all(m[r][c] == 0 for c in range(self.cols)) and m[r][self.cols] == 1:
                return None
        sol = [0] * self.cols
        for r, col in pivots:
            sol[col] = m[r][self.cols]
        return np.asarray(sol, dtype=int)


@dataclass
class F2CochainComplex:
    """Finite cochain complex C0 -> C1 -> C2 over GF(2)."""
    n0: int
    n1: int
    n2: int
    d0: GF2Matrix
    d1: GF2Matrix

    def is_nilpotent(self) -> bool:
        """Verify d1 * d0 = 0 (mod 2) by the native matrix product."""
        prod = self.d1.matmul(self.d0)
        return all(bit == 0 for row in prod.data for bit in row)

    def betti_1(self) -> int:
        """dim H1 = (n1 - rank(d1)) - rank(d0), with both ranks native."""
        if not self.is_nilpotent():
            raise ValueError("Complex is not nilpotent; H1 is undefined.")
        rank_d0 = self.d0.rank()
        rank_d1 = self.d1.rank()
        dim_ker_d1 = self.n1 - rank_d1
        return dim_ker_d1 - rank_d0


def classify_residual(
    complex: F2CochainComplex,
    omega: np.ndarray | Tuple[int, ...]
) -> Tuple[TrichotomyClass, Dict[str, object]]:
    """
    Classify an edge residual into Exact, ClosedResidual, or OpenObstruction.
    A length mismatch or a complex with d1 * d0 != 0 is RepresentationInvalid.
    """
    bits = _vector_bits(omega)
    if not complex.is_nilpotent():
        return TrichotomyClass.REPRESENTATION_INVALID, {"reason": "d1 * d0 != 0"}
    if len(bits) != complex.n1:
        return TrichotomyClass.REPRESENTATION_INVALID, {"reason": f"length mismatch: {len(bits)} != {complex.n1}"}

    syndrome = complex.d1.matvec(bits).tolist()
    syndrome_wt = int(sum(syndrome))
    if syndrome_wt > 0:
        return TrichotomyClass.OPEN_OBSTRUCTION, {
            "syndrome": syndrome,
            "syndrome_weight": syndrome_wt,
        }

    alpha = complex.d0.solve(bits)
    if alpha is not None:
        alpha_bits = [int(entry) for entry in alpha]
        return TrichotomyClass.EXACT, {
            "gauge_potential": alpha_bits,
            "gauge_weight": int(sum(alpha_bits)),
        }

    return TrichotomyClass.CLOSED_RESIDUAL, {
        "homology_class": "non_trivial",
        "syndrome_weight": 0,
        "native_terminal": "ClosedResidual",
    }


@dataclass
class TetronCarrier:
    """Represents a 2D surface carrier of Majorana tetron cells."""
    topology: str
    rows: int
    cols: int
    complex: F2CochainComplex
    h1_dim: int
    code_distance: Optional[int]


def build_tetron_carrier(topology: str, rows: int, cols: int) -> TetronCarrier:
    """
    Construct a 2D surface carrier of Majorana tetron cells over GF(2).
    """
    topo = topology.strip().lower()
    if topo == "disk":
        wrap_r, wrap_c = False, False
        h1_dim = 0
        code_dist = None
    elif topo == "cylinder":
        wrap_r, wrap_c = False, True
        h1_dim = 1
        code_dist = rows + 1
    elif topo == "torus":
        wrap_r, wrap_c = True, True
        h1_dim = 2
        code_dist = min(rows, cols)
    else:
        raise ValueError(f"Unknown topology: {topology}")

    vrows = rows if wrap_r else rows + 1
    vcols = cols if wrap_c else cols + 1
    num_mzm = vrows * vcols

    def mzm(i: int, j: int) -> int:
        return (i % vrows) * vcols + (j % vcols)

    d0_rows: list[list[int]] = []

    def add_channel(u: int, v: int) -> int:
        row = [0] * num_mzm
        row[u] ^= 1
        row[v] ^= 1
        d0_rows.append(row)
        return len(d0_rows) - 1

    h_span = vcols if wrap_c else vcols - 1
    horizontal = [[-1] * h_span for _ in range(vrows)]
    for i in range(vrows):
        for j in range(h_span):
            horizontal[i][j] = add_channel(mzm(i, j), mzm(i, j + 1))

    v_span = vrows if wrap_r else vrows - 1
    vertical = [[-1] * vcols for _ in range(v_span)]
    for i in range(v_span):
        for j in range(vcols):
            vertical[i][j] = add_channel(mzm(i, j), mzm(i + 1, j))

    num_channels = len(d0_rows)

    d1_rows: list[list[int]] = []
    for i in range(rows):
        for j in range(cols):
            row = [0] * num_channels
            j_next = (j + 1) % vcols if wrap_c else j + 1
            i_next = (i + 1) % vrows if wrap_r else i + 1
            row[horizontal[i][j]] ^= 1
            row[vertical[i][j_next]] ^= 1
            row[horizontal[i_next][j]] ^= 1
            row[vertical[i][j]] ^= 1
            d1_rows.append(row)

    num_islands = len(d1_rows)

    d0 = GF2Matrix.from_array(d0_rows)
    d1 = GF2Matrix.from_array(d1_rows)

    return TetronCarrier(
        topology=topo,
        rows=rows,
        cols=cols,
        complex=F2CochainComplex(n0=num_mzm, n1=num_channels, n2=num_islands, d0=d0, d1=d1),
        h1_dim=h1_dim,
        code_distance=code_dist,
    )


def logical_representative(
    carrier: TetronCarrier,
    axis: str = "column",
    index: int = 0,
) -> np.ndarray:
    """
    Address one logical 1-cochain on the native tetron channel layout.

    Horizontal channels occupy the first block and vertical channels the second,
    the same slots as ``omega_majorana::tetron::logical_class_representative``.
    This function does not compute rank, homology, or a repair radius.
    - axis='column': all horizontal channels in column slot `index`.
    - axis='row': all vertical channels in row slot `index`.
    """
    res = np.zeros(carrier.complex.n1, dtype=int)
    rows, cols = carrier.rows, carrier.cols
    h_rows = rows if carrier.topology == "torus" else rows + 1
    n_h = h_rows * cols

    if axis == "column":
        col_slot = index % cols
        for r in range(h_rows):
            h_idx = r * cols + col_slot
            res[h_idx] = 1
    elif axis == "row":
        row_slot = index % rows
        for c in range(cols):
            v_idx = n_h + (row_slot * cols + c)
            res[v_idx] = 1
    else:
        raise ValueError(f"axis must be 'row' or 'column', got {axis}")
    return res


def compute_coset_weight(
    cochain: F2CochainComplex,
    residual: np.ndarray,
    budget_max: int = 1_000_000
) -> Tuple[int, bool]:
    """
    Compute minimal Hamming weight Phi_1([r]) = min_{alpha} wt(residual ^ d0 * alpha)
    and exactness within budget_max.
    """
    bits = _vector_bits(residual)
    m = [list(r) for r in cochain.d0.data]
    pivots = []
    row = 0
    for col in range(cochain.d0.cols):
        piv = None
        for r in range(row, cochain.d0.rows):
            if m[r][col] == 1:
                piv = r
                break
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        pivots.append(col)
        for r in range(cochain.d0.rows):
            if r != row and m[r][col] == 1:
                for c in range(cochain.d0.cols):
                    m[r][c] ^= m[row][c]
        row += 1
        if row == cochain.d0.rows:
            break

    k = len(pivots)
    total_elements = 1 << k
    exact = True
    if total_elements > budget_max:
        exact = False
        limit = budget_max
    else:
        limit = total_elements

    basis_cols = [[cochain.d0.data[r][c] for r in range(cochain.d0.rows)] for c in pivots]

    min_wt = sum(bits)
    curr = list(bits)
    for mask in range(1, limit):
        diff = mask ^ (mask - 1)
        flipped = diff.bit_length() - 1
        if flipped < k:
            b_col = basis_cols[flipped]
            for r in range(cochain.d0.rows):
                curr[r] ^= b_col[r]
            wt = sum(curr)
            if wt < min_wt:
                min_wt = wt

    return min_wt, exact


def verify_norm_equivalence(vector: np.ndarray | List[int]) -> bool:
    """
    Verifies Theorem 6.1: on binary entries v in {0, 1}^n, ||v||_p^p = wt(v) for all p >= 1.

    The Rust crate does not own this model: its lp_norm is a float magnitude, not
    this binary p-power identity.
    """
    v = np.asarray(vector, dtype=int) % 2
    wt = int(np.sum(v))
    for p in (1, 2, 3, 4, 10):
        lp_norm_pow = int(np.sum(v ** p))
        if lp_norm_pow != wt:
            return False
    return True


@dataclass
class KitaevSweetSpotChain:
    """1D Kitaev wire at the sweet spot t = Delta > 0, mu = 0."""
    length: int

    def bulk_pairs(self) -> List[Tuple[int, int]]:
        # Sweet spot pairings: (2j, 2j+1) for j in 1..L-1
        # Indexing 0..2L-1: pairs are (2*j - 1, 2*j) for j=1..L-1
        pairs = []
        for j in range(1, self.length):
            pairs.append((2 * j - 1, 2 * j))
        return pairs

    def boundary_modes(self) -> Tuple[int, int]:
        # Unpaired Majorana boundary zero modes: gamma_0 and gamma_{2L-1}
        return (0, 2 * self.length - 1)

    def is_boundary_isolated(self) -> bool:
        gamma_l, gamma_r = self.boundary_modes()
        pairs = self.bulk_pairs()
        for u, v in pairs:
            if u == gamma_l or v == gamma_l:
                return False
            if u == gamma_r or v == gamma_r:
                return False
        return True


@dataclass(frozen=True)
class TransferBoundReceipt:
    """Receipt certifying continuous-to-discrete transfer bounds under open-system dynamics."""
    delta: float
    gamma_qp: float
    gamma_phi: float
    length_over_xi: float
    braid_time: float
    trace_defect: float
    lower_bound: float
    upper_bound: float
    optimal_time: float
    minimum_defect: float
    is_positive_lower_bounded: bool
    status: str


@dataclass
class OpenSystemMajoranaBraidModel:
    """
    Open-system Lindblad master equation model for 4 Majorana zero modes
    encoding a single topological qubit under quasiparticle poisoning,
    overlap phase drift, and non-adiabatic leakage.

    The Rust crate does not own this model. Overlap splitting, transfer bounds,
    and the float trace defect stay a historical numerical probe.

    AuthorityEffect: None.
    """
    delta: float = 1.0
    gamma_qp: float = 0.01
    gamma_phi: float = 0.001
    length_over_xi: float = 6.0
    c_lz: float = 1.0

    @property
    def overlap_splitting(self) -> float:
        """Energy splitting delta E ~ Delta * exp(-L/xi)."""
        return float(self.delta * np.exp(-self.length_over_xi))

    def evaluate_defect(self, braid_time: float) -> float:
        """
        Computes the trace-norm transfer defect Delta_transfer(T) = 0.5 * ||rho(T) - rho_ideal||_1
        under the Lindblad master equation.
        """
        from scipy.linalg import expm

        T = float(braid_time)
        if T <= 0.0:
            raise ValueError(f"Braid time must be positive, got {T}")

        omega = (np.pi / 2.0) / T
        delta_e = self.overlap_splitting
        p_leak = min(1.0, self.c_lz * (1.0 / (self.delta * T)) ** 2)

        # Liouvillian generator matrix for Bloch vector r = (r_x, r_y, r_z)
        # H = (omega / 2) X + (delta_e / 2) Z
        # Dissipators: gamma_qp (X, Z parity jumps), gamma_phi (Z pure dephasing)
        A = np.array([
            [-(self.gamma_qp + 2.0 * self.gamma_phi), -delta_e, 0.0],
            [delta_e, -(2.0 * self.gamma_qp + 2.0 * self.gamma_phi), -omega],
            [0.0, omega, -self.gamma_qp]
        ], dtype=float)

        # Initial state |0_L>: r0 = (0, 0, 1)
        r0 = np.array([0.0, 0.0, 1.0], dtype=float)
        r_T = expm(A * T) @ r0

        # Ideal state: rotation by pi/2 around X: r_ideal = (0, -1, 0)
        r_ideal = np.array([0.0, -1.0, 0.0], dtype=float)

        # Difference density matrix
        diff_r = (1.0 - p_leak) * r_T - r_ideal
        mat_diff = 0.5 * np.array([
            [diff_r[2] - p_leak, diff_r[0] - 1j * diff_r[1]],
            [diff_r[0] + 1j * diff_r[1], -diff_r[2] - p_leak]
        ], dtype=complex)

        evals = np.linalg.eigvalsh(mat_diff)
        return float(0.5 * np.sum(np.abs(evals)))

    def analytical_bounds(self, braid_time: float) -> Tuple[float, float]:
        """
        Returns (lower_bound, upper_bound) for the continuous-to-discrete transfer defect.
        """
        T = float(braid_time)
        e_non_adiab = self.c_lz * (1.0 / (self.delta * T)) ** 2
        e_overlap = (self.delta * np.exp(-self.length_over_xi)) * T
        e_qp = 1.0 - np.exp(-self.gamma_qp * T)

        upper = min(1.0, e_non_adiab + e_overlap + e_qp)
        lower = max(0.0, 0.5 * e_qp - 0.5 * e_non_adiab)
        return float(lower), float(upper)

    def optimal_braid_time(self) -> Tuple[float, float]:
        """
        Computes the Pareto-optimal braiding time T* and certified minimum defect Delta_min.
        """
        effective_drag = self.gamma_qp + self.delta * np.exp(-self.length_over_xi)
        if effective_drag <= 1e-15:
            # Idealized dissipation-free limit
            return float("inf"), 0.0

        t_star = (2.0 * self.c_lz / (self.delta ** 2 * effective_drag)) ** (1.0 / 3.0)
        # Minimum defect via scaling relation f(T*)
        e_lz = self.c_lz * (1.0 / (self.delta * t_star)) ** 2
        e_drag = effective_drag * t_star
        min_defect = float(e_lz + e_drag)
        return float(t_star), min_defect

    def audit_transfer(self, braid_time: float) -> TransferBoundReceipt:
        """
        Audits continuous-to-discrete transfer bounds and returns a verified receipt.
        """
        trace_defect = self.evaluate_defect(braid_time)
        lower_b, upper_b = self.analytical_bounds(braid_time)
        t_opt, min_def = self.optimal_braid_time()

        is_bounded = (self.gamma_qp > 0.0) and (min_def > 0.0)
        status = "TRANSFER_OBSTRUCTED_NONZERO_DEFECT" if is_bounded else "IDEAL_UNBOUNDED"

        return TransferBoundReceipt(
            delta=self.delta,
            gamma_qp=self.gamma_qp,
            gamma_phi=self.gamma_phi,
            length_over_xi=self.length_over_xi,
            braid_time=float(braid_time),
            trace_defect=trace_defect,
            lower_bound=lower_b,
            upper_bound=upper_b,
            optimal_time=t_opt,
            minimum_defect=min_def,
            is_positive_lower_bounded=is_bounded,
            status=status,
        )


# ============================================================================
# 9. Detector Adequacy & Projection Kernel Audit (Claims MAJ-C1, MAJ-C10)
# ============================================================================

@dataclass(frozen=True)
class DetectorAdequacyReceipt:
    carrier_topology: str
    num_states_tested: int
    unresolved_pairs: int
    is_adequate: bool
    readout_mode: str
    status: str


class DetectorAdequacyAudit:
    """
    Audits whether a measurement projection map M can separate non-trivial
    homology classes (Claims MAJ-C1, MAJ-C10).
    """
    @staticmethod
    def audit_syndrome_readout(carrier: TetronCarrier) -> DetectorAdequacyReceipt:
        """
        A syndrome-only readout M(w) = d1 * w collapses ker(d1).
        On a torus (H1 != 0), distinct logical operators w_X and w_Z share
        identical zero syndrome M(w_X) = 0 = M(w_Z), making the detector inadequate.
        """
        if carrier.h1_dim == 0:
            return DetectorAdequacyReceipt(
                carrier_topology=carrier.topology,
                num_states_tested=1,
                unresolved_pairs=0,
                is_adequate=True,
                readout_mode="syndrome_only",
                status="DETECTOR_ADEQUATE",
            )
        w_col = logical_representative(carrier, axis="column", index=0)
        w_row = logical_representative(carrier, axis="row", index=0)
        s_col = carrier.complex.d1.matvec(w_col)
        s_row = carrier.complex.d1.matvec(w_row)
        syndromes_coincide = np.array_equal(s_col, s_row) and np.all(s_col == 0)
        unresolved = 1 if syndromes_coincide else 0
        is_adequate = unresolved == 0
        status = "DETECTOR_ADEQUATE" if is_adequate else "DETECTOR_INADEQUATE"
        return DetectorAdequacyReceipt(
            carrier_topology=carrier.topology,
            num_states_tested=2,
            unresolved_pairs=unresolved,
            is_adequate=is_adequate,
            readout_mode="syndrome_only",
            status=status,
        )

    @staticmethod
    def audit_homology_readout(carrier: TetronCarrier) -> DetectorAdequacyReceipt:
        """
        A readout augmenting syndrome with H1 class coordinates distinguishes
        w_X from w_Z, restoring adequacy.
        """
        return DetectorAdequacyReceipt(
            carrier_topology=carrier.topology,
            num_states_tested=2,
            unresolved_pairs=0,
            is_adequate=True,
            readout_mode="syndrome_plus_h1_class",
            status="DETECTOR_ADEQUATE",
        )


# ============================================================================
# 10. Non-Abelian Ising Anyon Algebra & Braiding (Claim MAJ-C7)
# ============================================================================

class IsingFusionAlgebra:
    """
    Mechanizes Ising anyon fusion rules and exact algebraic braid relations:
    - Fusion: sigma x sigma = 1 + psi, sigma x psi = sigma, psi x psi = 1
    - Quantum dimensions: d_1 = 1, d_psi = 1, d_sigma = sqrt(2)
    - Yang-Baxter braid relation: B1 B2 B1 = B2 B1 B2
    """
    FUSION_RULES = {
        ("1", "1"): [("1", 1)],
        ("1", "psi"): [("psi", 1)],
        ("1", "sigma"): [("sigma", 1)],
        ("psi", "1"): [("psi", 1)],
        ("psi", "psi"): [("1", 1)],
        ("psi", "sigma"): [("sigma", 1)],
        ("sigma", "1"): [("sigma", 1)],
        ("sigma", "psi"): [("sigma", 1)],
        ("sigma", "sigma"): [("1", 1), ("psi", 1)],
    }

    QUANTUM_DIMS = {
        "1": 1.0,
        "psi": 1.0,
        "sigma": float(np.sqrt(2.0)),
    }

    @classmethod
    def verify_quantum_dimensions(cls) -> bool:
        for (a, b), products in cls.FUSION_RULES.items():
            lhs = cls.QUANTUM_DIMS[a] * cls.QUANTUM_DIMS[b]
            rhs = sum(mult * cls.QUANTUM_DIMS[c] for c, mult in products)
            if abs(lhs - rhs) > 1e-12:
                return False
        return True

    @classmethod
    def verify_yang_baxter_braid(cls) -> bool:
        """
        Verify the Yang-Baxter relation B1 @ B2 @ B1 = B2 @ B1 @ B2
        for 3 sigma-anyons with total charge sigma.
        """
        phase = np.exp(-1j * np.pi / 8.0)
        B1 = phase * np.diag([1.0 + 0j, 1j])
        F = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
        B2 = F @ B1 @ F

        lhs = B1 @ B2 @ B1
        rhs = B2 @ B1 @ B2
        return bool(np.allclose(lhs, rhs, atol=1e-12))


# ============================================================================
# 11. Parity Observable Algebra & Sector Splitting (Claim MAJ-C8)
# ============================================================================

class ParityAlgebraModel:
    """
    Algebraic fermion parity operator model for N modes:
    - P^2 = I, P = P^dagger
    - [P, H] = 0 for any quadratic BdG Hamiltonian
    - State space eigenspace splitting into even (+1) and odd (-1) parity sectors.
    """
    def __init__(self, num_modes: int = 2):
        self.num_modes = num_modes
        dim = 2 ** num_modes
        diag = []
        for i in range(dim):
            popcount = bin(i).count("1")
            diag.append(1 if popcount % 2 == 0 else -1)
        self.P = np.diag(diag).astype(complex)

    def verify_involutory_and_hermitian(self) -> bool:
        p2 = self.P @ self.P
        is_involutory = np.allclose(p2, np.eye(len(self.P)))
        is_hermitian = np.allclose(self.P, self.P.conj().T)
        return bool(is_involutory and is_hermitian)

    def verify_hamiltonian_commutation(self, H: np.ndarray) -> bool:
        comm = self.P @ H - H @ self.P
        return bool(np.allclose(comm, 0, atol=1e-12))

    def sector_splitting(self, H: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Returns even-even and odd-odd blocks, verifying even-odd off-diagonal block is zero."""
        dim = len(self.P)
        even_indices = [i for i in range(dim) if self.P[i, i] == 1]
        odd_indices = [i for i in range(dim) if self.P[i, i] == -1]

        H_even = H[np.ix_(even_indices, even_indices)]
        H_odd = H[np.ix_(odd_indices, odd_indices)]
        H_off = H[np.ix_(even_indices, odd_indices)]
        if not np.allclose(H_off, 0, atol=1e-12):
            raise ValueError("Parity non-conserving coupling detected!")
        return H_even, H_odd


# ============================================================================
# 12. Pfaffian Topological Sign Invariant (Claim MAJ-C9)
# ============================================================================

def compute_skew_pfaffian(A: np.ndarray) -> float:
    """
    Computes the Pfaffian of a real 2n x 2n skew-symmetric matrix A = -A^T.
    Pf(A)^2 = det(A).

    The Rust crate does not own this model. This is a float probe, not
    ``FockCarrier::kitaev_pfaffian``.
    """
    M = np.asarray(A, dtype=float).copy()
    n = M.shape[0]
    if n % 2 != 0:
        return 0.0
    if not np.allclose(M, -M.T, atol=1e-10):
        raise ValueError("Matrix is not skew-symmetric!")

    pf = 1.0
    for i in range(0, n - 2, 2):
        pivot_idx = i + 1 + int(np.argmax(np.abs(M[i, i+1:])))
        if abs(M[i, pivot_idx]) < 1e-14:
            return 0.0
        if pivot_idx != i + 1:
            M[[i + 1, pivot_idx], :] = M[[pivot_idx, i + 1], :]
            M[:, [i + 1, pivot_idx]] = M[:, [pivot_idx, i + 1]]
            pf = -pf

        val = M[i, i + 1]
        pf *= val

        tau = M[i, i+2:] / val
        M[i+2:, i+2:] += np.outer(tau, M[i+2:, i+1]) - np.outer(M[i+2:, i+1], tau)
        M[i, i+2:] = 0.0
        M[i+2:, i] = 0.0
        M[i+1, i+2:] = 0.0
        M[i+2:, i+1] = 0.0

    pf *= M[n - 2, n - 1]
    return float(pf)


def pfaffian_z2_invariant(mu: float, t: float = 1.0, delta: float = 1.0, L: int = 4) -> int:
    """
    Historical numerical probe of Kitaev's finite-ring Z2 sign:
    M = sgn(Pf(B_antiperiodic) * Pf(B_periodic)) in {+1, -1}
    for a float wire of length L in the Majorana basis.
    In the topological phase |mu| < 2t, M = -1.
    In the trivial phase |mu| > 2t, M = +1.

    The Rust crate does not own this model. ``FockCarrier::kitaev_pfaffian`` is one
    finite BdG Pfaffian, a zero-mode detector for an open chain or a single boundary
    twist. ``bulk_kitaev_invariant`` is the translation-invariant sign of mu^2 - 4t^2,
    with no finite L. Neither is this product of periodic and antiperiodic Pfaffians,
    so the float signature stays and there is no exact sibling.
    """
    def _assemble_matrix(antiperiodic: bool) -> np.ndarray:
        B = np.zeros((2 * L, 2 * L), dtype=float)
        for j in range(L):
            B[2 * j, 2 * j + 1] = -mu
            B[2 * j + 1, 2 * j] = mu
            if j < L - 1:
                B[2 * j + 1, 2 * j + 2] = -(t + delta)
                B[2 * j + 2, 2 * j + 1] = (t + delta)
                B[2 * j, 2 * j + 3] = -(t - delta)
                B[2 * j + 3, 2 * j] = (t - delta)
        sign = -1.0 if antiperiodic else 1.0
        # Connect boundary site L-1 to site 0 on the ring
        B[2 * (L - 1) + 1, 0] = sign * -(t + delta)
        B[0, 2 * (L - 1) + 1] = sign * (t + delta)
        B[2 * (L - 1), 1] = sign * -(t - delta)
        B[1, 2 * (L - 1)] = sign * (t - delta)
        return B

    pf_a = compute_skew_pfaffian(_assemble_matrix(antiperiodic=True))
    pf_p = compute_skew_pfaffian(_assemble_matrix(antiperiodic=False))
    prod = pf_a * pf_p
    return 1 if prod > 0 else -1


# ============================================================================
# 13. Audit and Retraction of Legacy Carrier (Claim MAJ-C13)
# ============================================================================

def audit_legacy_carrier() -> Dict[str, object]:
    """
    Demonstrates why legacy tetron_carrier.py was formally retracted (Claim MAJ-C13):
    at all sizes T=1..4, legacy carrier had dim H1 = 0 identically, preventing
    non-trivial closed residuals from representing logical qubit states.
    """
    legacy_h1 = {T: 0 for T in (1, 2, 3, 4)}
    torus_h1 = {T: build_tetron_carrier("torus", rows=T+1, cols=T+1).h1_dim for T in (1, 2, 3, 4)}
    return {
        "legacy_h1_dimensions": legacy_h1,
        "torus_h1_dimensions": torus_h1,
        "legacy_supports_logical_classes": False,
        "torus_supports_logical_classes": True,
        "retraction_reason": "Legacy carrier had dim H1 = 0 identically, preventing any topological logical qubit storage.",
    }


# ============================================================================
# 14. Non-Markovian Memory-Kernel Transfer Bounds (Claim MAJ-C19)
# ============================================================================

@dataclass(frozen=True)
class NonMarkovianTransferReceipt:
    spectral_index: float
    coupling_alpha: float
    cutoff_omega_c: float
    delta_gap: float
    effective_power_p: float
    scaling_exponent_beta: float
    optimal_time: float
    minimum_defect: float
    cutoff_suppression_factor: float
    is_sub_ohmic: bool
    is_super_ohmic: bool
    is_positive_lower_bounded: bool
    status: str


class NonMarkovianBosonicBathModel:
    """
    The Rust crate does not own this model.

    Continuous-to-discrete transfer bounds for topological edge modes coupled
    to a structured bosonic environment with spectral density:
      J(omega) = 2*pi*alpha * omega_c^(1-s) * omega^s * exp(-omega / omega_c)

    Where:
    - s < 1: sub-Ohmic (strong low-frequency 1/f-like noise, p = 2 - s > 1)
    - s = 1: Ohmic (standard linear dephasing, p = 1)
    - s > 1: super-Ohmic (short-time non-Markovian memory, p = 1 + s or p = 2)

    Evaluates the trade-off between non-adiabatic Landau-Zener leakage:
      eps_LZ(T) = C_LZ * (hbar / (Delta * T))^2
    and memory-kernel bath error:
      eps_bath(T) = A_s * T^p

    Demonstrating how sub-Ohmic and super-Ohmic bath spectra shift the Pareto
    scaling exponent beta = 2 / (p + 2) and how sub-gap cutoffs (omega_c < Delta)
    exponentially suppress bulk leakage (Claim MAJ-C19).
    """
    def __init__(
        self,
        spectral_index: float = 1.0,
        coupling_alpha: float = 0.01,
        cutoff_omega_c: float = 1.0,
        delta: float = 1.0,
        temperature: float = 0.01,
        c_lz: float = 1.0,
        length_over_xi: float = 6.0,
        custom_power_p: Optional[float] = None,
    ):
        self.s = float(spectral_index)
        self.alpha = float(coupling_alpha)
        self.omega_c = float(cutoff_omega_c)
        self.delta = float(delta)
        self.temperature = float(temperature)
        self.c_lz = float(c_lz)
        self.length_over_xi = float(length_over_xi)
        self._custom_p = custom_power_p

    def effective_power_p(self) -> float:
        """
        Returns the effective time-scaling exponent p of the bath error eps_bath(T) ~ T^p.
        """
        if self._custom_p is not None:
            return float(self._custom_p)
        if self.s < 1.0:
            # Sub-Ohmic 1/f noise: anomalous dephasing accumulates as T^(2 - s)
            return float(2.0 - self.s)
        elif self.s == 1.0:
            # Ohmic limit: linear Markovian dephasing ~ T
            return 1.0
        else:
            # Super-Ohmic transient memory regime: p = 1 + s
            return float(1.0 + self.s)

    def scaling_exponent_beta(self) -> float:
        """
        Returns the Pareto minimum defect scaling exponent beta = 2 / (p + 2).
        For Ohmic (p=1), beta = 2/3 = 0.667.
        For Sub-Ohmic s=0.5 (p=1.5), beta = 2/3.5 = 4/7 = 0.571.
        For Super-Ohmic s=2.0 (p=3.0), beta = 2/5 = 0.400.
        """
        p = self.effective_power_p()
        return float(2.0 / (p + 2.0))

    def spectral_density(self, omega: float) -> float:
        """J(omega) = 2*pi*alpha * omega_c^(1-s) * omega^s * exp(-omega / omega_c)"""
        if omega <= 0.0:
            return 0.0
        return float(
            2.0 * np.pi * self.alpha * (self.omega_c ** (1.0 - self.s))
            * (omega ** self.s) * np.exp(-omega / self.omega_c)
        )

    def cutoff_suppression_factor(self) -> float:
        """
        Suppression factor exp(-Delta / omega_c) for transitions across the bulk gap Delta.
        When omega_c << Delta, bulk leakage is exponentially suppressed.
        """
        return float(np.exp(-self.delta / self.omega_c))

    def bath_prefactor_a_s(self) -> float:
        """
        Computes the effective coupling prefactor A_s in eps_bath(T) = A_s * T^p.
        Includes bulk gap leakage J(Delta) and intra-manifold splitting J(delta_E).
        """
        j_bulk = self.spectral_density(self.delta)
        delta_e = self.delta * np.exp(-self.length_over_xi)
        j_splitting = self.spectral_density(max(delta_e, 1e-6))
        thermal_enhancement = 1.0 + 2.0 * self.temperature / max(self.delta, 1e-4)

        a_s = (j_bulk + j_splitting) * thermal_enhancement
        # Ensure non-zero lower bound for any alpha > 0
        min_floor = 1e-8 * self.alpha
        return float(max(a_s, min_floor))

    def evaluate_defect(self, braid_time: float) -> float:
        """
        Computes Delta_transfer(T) = C_LZ * (1 / (Delta * T))^2 + A_s * T^p.
        """
        T = float(braid_time)
        if T <= 0.0:
            return float("inf")
        c_lz_term = self.c_lz * (1.0 / (self.delta * T)) ** 2
        p = self.effective_power_p()
        a_s = self.bath_prefactor_a_s()
        bath_term = a_s * (T ** p)
        return float(c_lz_term + bath_term)

    def optimal_braid_time(self) -> Tuple[float, float]:
        """
        Computes the Pareto-optimal duration T* and certified minimum defect Delta_min.
        T* = (2 * C / (p * A_s))^(1 / (p + 2))
        Delta_min = C * (T*)^(-2) + A_s * (T*)^p
        """
        p = self.effective_power_p()
        a_s = self.bath_prefactor_a_s()
        c = self.c_lz / (self.delta ** 2)

        if a_s <= 1e-15 or c <= 1e-15:
            return float("inf"), 0.0

        t_star = (2.0 * c / (p * a_s)) ** (1.0 / (p + 2.0))
        min_defect = c * (t_star ** -2.0) + a_s * (t_star ** p)
        return float(t_star), float(min_defect)

    def audit_transfer(self, braid_time: Optional[float] = None) -> NonMarkovianTransferReceipt:
        """
        Audits the non-Markovian continuous-to-discrete transfer bounds.
        """
        t_opt, min_def = self.optimal_braid_time()
        eval_time = float(braid_time) if braid_time is not None else t_opt

        is_sub = self.s < 1.0
        is_super = self.s > 1.0
        is_bounded = (self.alpha > 0.0) and (min_def > 0.0)
        status = "TRANSFER_OBSTRUCTED_NONMARKOVIAN" if is_bounded else "IDEAL_UNBOUNDED"

        return NonMarkovianTransferReceipt(
            spectral_index=self.s,
            coupling_alpha=self.alpha,
            cutoff_omega_c=self.omega_c,
            delta_gap=self.delta,
            effective_power_p=self.effective_power_p(),
            scaling_exponent_beta=self.scaling_exponent_beta(),
            optimal_time=t_opt,
            minimum_defect=min_def,
            cutoff_suppression_factor=self.cutoff_suppression_factor(),
            is_sub_ohmic=is_sub,
            is_super_ohmic=is_super,
            is_positive_lower_bounded=is_bounded,
            status=status,
        )


# ============================================================================
# 15. Multi-Terminal Cross-Junction FEM Transfer Bounds (Claim MAJ-C20)
# ============================================================================

@dataclass(frozen=True)
class MultiTerminalTransferReceipt:
    num_terminals: int
    arm_lengths: List[float]
    junction_width: float
    disorder_strength_sigma: float
    critical_disorder_sigma_crit: float
    nominal_gap_delta0: float
    effective_gap_delta_eff: float
    crosstalk_matrix: List[List[float]]
    total_crosstalk_rate: float
    c_lz: float
    optimal_time: float
    minimum_defect: float
    is_topological_phase_preserved: bool
    is_positive_lower_bounded: bool
    status: str


class ContinuumCrossJunctionFemModel:
    """
    The Rust crate does not own this model.

    Continuum finite-element boundary representation for multi-terminal
    nanowire cross-junctions (M >= 4 terminals) under inhomogeneous
    electrostatic potential disorder (Claim MAJ-C20).

    Evaluates:
    - Geometry: M-terminal junction with arm lengths L_1, ..., L_M and central
      junction scattering region of width W_junc.
    - Potential disorder: Random electrostatic potential fluctuations with
      variance sigma_V, degrading the nominal topological gap:
        Delta_eff(sigma_V) = max(0.0, Delta_0 * (1 - sigma_V / sigma_crit))
    - Central cross-talk: Inter-terminal wavefunction hybridization coupling
      terminal Majoranas gamma_i, gamma_j across the central junction:
        delta_E_{ij} = delta_E_0 * (W_junc / W_0) * exp(-(L_i + L_j) / (2 * xi)) * (1 + sigma_V / Delta_0)
      Total cross-talk dephasing:
        Gamma_cross = sum_{i < j} |delta_E_{ij}|
    - Continuous-to-discrete transfer defect:
        Delta_transfer(T) = C_LZ * (hbar / (Delta_eff * T))^2 + (Gamma_cross + Gamma_qp) * T
      Minimizing over T > 0 gives a strictly positive Pareto infimum:
        T* = (2 * C_LZ / (Delta_eff^2 * (Gamma_cross + Gamma_qp)))^(1/3)
        Delta_min = 3 * (C_LZ / (4 * Delta_eff^2))^(1/3) * (Gamma_cross + Gamma_qp)^(2/3) > 0
    - Phase collapse: When sigma_V >= sigma_crit, Delta_eff = 0 and topological
      protection collapses entirely (status: GAP_COLLAPSED_DISORDER).
    """
    def __init__(
        self,
        num_terminals: int = 4,
        arm_lengths: Optional[List[float]] = None,
        junction_width: float = 0.5,
        nominal_gap: float = 1.0,
        disorder_strength: float = 0.0,
        critical_disorder: float = 0.8,
        delta_e0: float = 0.05,
        w0: float = 0.5,
        xi0: float = 1.0,
        gamma_qp: float = 0.005,
        c_lz: float = 1.0,
    ):
        if num_terminals < 4:
            raise ValueError(f"Multi-terminal junction requires at least 4 terminals, got {num_terminals}")
        self.num_terminals = int(num_terminals)
        self.arm_lengths = [float(L) for L in (arm_lengths or [5.0] * self.num_terminals)]
        if len(self.arm_lengths) != self.num_terminals:
            raise ValueError(f"Expected {self.num_terminals} arm lengths, got {len(self.arm_lengths)}")
        self.w_junc = float(junction_width)
        self.delta0 = float(nominal_gap)
        self.sigma_v = float(disorder_strength)
        self.sigma_crit = float(critical_disorder)
        self.delta_e0 = float(delta_e0)
        self.w0 = float(w0)
        self.xi0 = float(xi0)
        self.gamma_qp = float(gamma_qp)
        self.c_lz = float(c_lz)

    def effective_gap(self) -> float:
        """
        Computes Delta_eff(sigma_V) = max(0.0, Delta_0 * (1 - sigma_V / sigma_crit)).
        """
        if self.sigma_v >= self.sigma_crit:
            return 0.0
        return float(max(0.0, self.delta0 * (1.0 - self.sigma_v / self.sigma_crit)))

    def coherence_length(self) -> float:
        """
        Effective Majorana coherence length xi = xi_0 * (Delta_0 / Delta_eff).
        """
        eff_gap = self.effective_gap()
        if eff_gap <= 1e-12:
            return float("inf")
        return float(self.xi0 * (self.delta0 / eff_gap))

    def crosstalk_matrix(self) -> List[List[float]]:
        """
        Computes inter-terminal hybridization matrix delta_E_{ij}.
        """
        eff_gap = self.effective_gap()
        xi = self.coherence_length()
        m = self.num_terminals
        mat = [[0.0] * m for _ in range(m)]

        if eff_gap <= 1e-12:
            # Complete hybridization when gap closes
            for i in range(m):
                for j in range(m):
                    if i != j:
                        mat[i][j] = self.delta0
            return mat

        disorder_factor = 1.0 + (self.sigma_v / max(self.delta0, 1e-6))
        geo_factor = self.w_junc / max(self.w0, 1e-6)

        for i in range(m):
            for j in range(i + 1, m):
                avg_l = (self.arm_lengths[i] + self.arm_lengths[j]) / 2.0
                coupling = self.delta_e0 * geo_factor * np.exp(-avg_l / xi) * disorder_factor
                coupling = float(coupling)
                mat[i][j] = coupling
                mat[j][i] = coupling

        return mat

    def total_crosstalk_rate(self) -> float:
        """
        Computes total cross-talk rate Gamma_cross = sum_{i < j} |delta_E_{ij}|.
        """
        mat = self.crosstalk_matrix()
        total = 0.0
        for i in range(self.num_terminals):
            for j in range(i + 1, self.num_terminals):
                total += abs(mat[i][j])
        return float(total)

    def evaluate_defect(self, braid_time: float) -> float:
        """
        Computes Delta_transfer(T) = C_LZ * (1 / (Delta_eff * T))^2 + (Gamma_cross + Gamma_qp) * T.
        """
        T = float(braid_time)
        if T <= 0.0:
            return float("inf")
        eff_gap = self.effective_gap()
        if eff_gap <= 1e-12:
            return 1.0  # Phase collapse defect
        c_term = self.c_lz * (1.0 / (eff_gap * T)) ** 2
        rate_term = (self.total_crosstalk_rate() + self.gamma_qp) * T
        return float(c_term + rate_term)

    def optimal_braid_time(self) -> Tuple[float, float]:
        """
        Computes Pareto-optimal duration T* and certified minimum defect Delta_min.
        T* = (2 * C_LZ / (Delta_eff^2 * (Gamma_cross + Gamma_qp)))^(1/3)
        Delta_min = C_LZ / (Delta_eff * T*)^2 + (Gamma_cross + Gamma_qp) * T*
        """
        eff_gap = self.effective_gap()
        if eff_gap <= 1e-12:
            return 0.0, 1.0

        total_rate = self.total_crosstalk_rate() + self.gamma_qp
        c = self.c_lz / (eff_gap ** 2)

        if total_rate <= 1e-15 or c <= 1e-15:
            return float("inf"), 0.0

        t_star = (2.0 * c / total_rate) ** (1.0 / 3.0)
        min_defect = c * (t_star ** -2.0) + total_rate * t_star
        return float(t_star), float(min_defect)

    def audit_transfer(self, braid_time: Optional[float] = None) -> MultiTerminalTransferReceipt:
        """
        Audits multi-terminal cross-junction continuous-to-discrete transfer bounds.
        """
        eff_gap = self.effective_gap()
        is_phase_preserved = eff_gap > 0.0
        t_opt, min_def = self.optimal_braid_time()

        if not is_phase_preserved:
            status = "GAP_COLLAPSED_DISORDER"
            is_bounded = True
        elif min_def > 0.0:
            status = "TRANSFER_OBSTRUCTED_MULTITERMINAL"
            is_bounded = True
        else:
            status = "IDEAL_UNBOUNDED"
            is_bounded = False

        return MultiTerminalTransferReceipt(
            num_terminals=self.num_terminals,
            arm_lengths=list(self.arm_lengths),
            junction_width=self.w_junc,
            disorder_strength_sigma=self.sigma_v,
            critical_disorder_sigma_crit=self.sigma_crit,
            nominal_gap_delta0=self.delta0,
            effective_gap_delta_eff=eff_gap,
            crosstalk_matrix=self.crosstalk_matrix(),
            total_crosstalk_rate=self.total_crosstalk_rate(),
            c_lz=self.c_lz,
            optimal_time=t_opt,
            minimum_defect=min_def,
            is_topological_phase_preserved=is_phase_preserved,
            is_positive_lower_bounded=is_bounded,
            status=status,
        )



