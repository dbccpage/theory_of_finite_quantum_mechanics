"""toric_code_observer_completion.py — Discrete F_2 Toric-Code Observer Completion & Certificate Engine.

AuthorityEffect: None.
Reference: WDP Chapter 23 (WDP-CH23-D01 through WDP-CH23-P20).

Instantiates the operational question:
  "Given what the observer already sees, which further observations are necessary
   and sufficient, and what is the cheapest way to obtain them?"
on the declared finite carrier Lambda = Z_L x Z_L.
"""

import itertools
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass(frozen=True)
class ToricCodeGeometry:
    """Toric code geometry on Lambda = Z_L x Z_L."""
    L: int
    n_qubits: int  # 2 * L^2
    n_faces: int   # L^2
    n_sites: int   # L^2


def build_toric_code_geometry(L: int) -> ToricCodeGeometry:
    if type(L) is not int or L < 3:
        raise ValueError("lattice linear dimension must be an integer >= 3")
    return ToricCodeGeometry(L=L, n_qubits=2 * L * L, n_faces=L * L, n_sites=L * L)


def build_toric_incidence_matrices(L: int) -> Tuple[np.ndarray, np.ndarray]:
    """Construct face-qubit incidence matrix A and site-qubit incidence matrix A_v over F_2.
    
    Qubit indexing:
      - Horizontal edge h_{i,j} from (i,j) to (i, (j+1)%L): index 2*(i*L + j)
      - Vertical edge v_{i,j} from (i,j) to ((i+1)%L, j): index 2*(i*L + j) + 1
      
    Face f_{i,j} boundaries:
      - h_{i,j} (bottom), h_{(i+1)%L, j} (top), v_{i,j} (left), v_{i, (j+1)%L} (right)
      
    Site s_{i,j} star coboundary:
      - h_{i,j} (right), h_{i, (j-1)%L} (left), v_{i,j} (up), v_{(i-1)%L, j} (down)
    """
    build_toric_code_geometry(L)
    n_qubits = 2 * L * L
    n_cells = L * L
    
    A = np.zeros((n_cells, n_qubits), dtype=int)
    A_v = np.zeros((n_cells, n_qubits), dtype=int)
    
    for i in range(L):
        for j in range(L):
            f_idx = i * L + j
            s_idx = i * L + j
            
            # Face f_{i,j}
            h_bot = 2 * (i * L + j)
            h_top = 2 * (((i + 1) % L) * L + j)
            v_left = 2 * (i * L + j) + 1
            v_right = 2 * (i * L + ((j + 1) % L)) + 1
            
            A[f_idx, h_bot] ^= 1
            A[f_idx, h_top] ^= 1
            A[f_idx, v_left] ^= 1
            A[f_idx, v_right] ^= 1
            
            # Site s_{i,j}
            h_r = 2 * (i * L + j)
            h_l = 2 * (i * L + ((j - 1) % L))
            v_u = 2 * (i * L + j) + 1
            v_d = 2 * (((i - 1) % L) * L + j) + 1
            
            A_v[s_idx, h_r] ^= 1
            A_v[s_idx, h_l] ^= 1
            A_v[s_idx, v_u] ^= 1
            A_v[s_idx, v_d] ^= 1
            
    return A, A_v


def gf2_rank(M: np.ndarray) -> int:
    """Compute exact matrix rank over F_2."""
    M = _gf2_matrix(M)
    return M.shape[1] - len(gf2_nullspace(M))


def _gf2_matrix(matrix: np.ndarray) -> np.ndarray:
    if not isinstance(matrix, np.ndarray) or matrix.ndim != 2 or matrix.dtype.kind not in "biu":
        raise ValueError("a two-dimensional integer or binary matrix is required")
    return (matrix % 2).astype(np.uint8)

def gf2_nullspace(M: np.ndarray) -> List[np.ndarray]:
    """Compute exact right nullspace basis over F_2: vectors x such that M x = 0 mod 2."""
    M = _gf2_matrix(M)
    if M.size == 0 or M.shape[0] == 0:
        ncols = M.shape[1]
        return [np.eye(ncols, dtype=int)[i] for i in range(ncols)]
    
    nrows, ncols = M.shape
    A = (M % 2).copy()
    r = 0
    pivots: List[Tuple[int, int]] = []
    
    for col in range(ncols):
        if r >= nrows:
            break
        pivot = None
        for i in range(r, nrows):
            if A[i, col] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        for i in range(nrows):
            if i != r and A[i, col] == 1:
                A[i] ^= A[r]
        pivots.append((r, col))
        r += 1
        
    pivot_cols = {c for (_, c) in pivots}
    free_cols = [c for c in range(ncols) if c not in pivot_cols]
    
    basis = []
    for f in free_cols:
        v = np.zeros(ncols, dtype=int)
        v[f] = 1
        for row, col in pivots:
            if A[row, f] == 1:
                v[col] = 1
        basis.append(v)
    return basis


def is_in_span(basis_matrix: np.ndarray, vec: np.ndarray) -> bool:
    """Check if vec is in row span of basis_matrix over F_2."""
    if len(basis_matrix) == 0:
        return np.all(vec % 2 == 0)
    r1 = gf2_rank(basis_matrix)
    augmented = np.vstack([basis_matrix, vec.reshape(1, -1)])
    r2 = gf2_rank(augmented)
    return r1 == r2


def get_canonical_logicals(L: int) -> Dict[str, np.ndarray]:
    """X supports are dual cycles in ker(A); Z supports are primal cycles in ker(A_v).

    X_i and Z_i intersect once; differently indexed pairs have zero intersection.
    These conventions agree with Q(x|z)=(A x, A_v z).
    """
    n = build_toric_code_geometry(L).n_qubits
    x1, x2, z1, z2 = (np.zeros(n, dtype=int) for _ in range(4))
    for j in range(L):
        z1[2 * j] = 1                 # horizontal primal loop on row 0
        x2[2 * j + 1] = 1             # dual cut across vertical edges on row 0
    for i in range(L):
        z2[2 * (i * L) + 1] = 1       # vertical primal loop on column 0
        x1[2 * (i * L)] = 1           # dual cut across horizontal edges on column 0
    return {"X1": x1, "X2": x2, "Z1": z1, "Z2": z2}


@dataclass
class CompletionDichotomyResult:
    is_sufficient: bool
    primal_recovery_table: Optional[Dict[str, str]]
    dual_failure_witness: Optional[Tuple[str, str]]
    unresolved_kernel_dimension: int
    authority_effect: str = "None"


def evaluate_observer_completion(
    H_D: np.ndarray,
    admissible_errors: List[np.ndarray],
    stabilizer_basis: np.ndarray,
) -> CompletionDichotomyResult:
    """Evaluate the exact report-question factorization criterion:
    
      (E - E) cap ker H_D subseteq B
      
    Returns either a primal recovery table or a dual failure witness pair (e1, e2).
    """
    # 1. Compute kernel of H_D over F_2
    ker_basis = gf2_nullspace(H_D)
    ker_dim = len(ker_basis)
    
    # 2. Check all pairs (e1, e2) in admissible_errors
    # Map syndrome -> candidate representative
    syndrome_table: Dict[Tuple[int, ...], np.ndarray] = {}
    
    for e in admissible_errors:
        syn = tuple(int(x) for x in (H_D @ e % 2))
        if syn not in syndrome_table:
            syndrome_table[syn] = e
        else:
            rep = syndrome_table[syn]
            diff = (e + rep) % 2
            # Check if diff is in stabilizer_basis (B)
            if not is_in_span(stabilizer_basis, diff):
                # Found dual failure witness!
                e1_str = "".join(map(str, e))
                e2_str = "".join(map(str, rep))
                return CompletionDichotomyResult(
                    is_sufficient=False,
                    primal_recovery_table=None,
                    dual_failure_witness=(e1_str, e2_str),
                    unresolved_kernel_dimension=ker_dim,
                )
                
    # If no violation found, construct primal recovery table
    recovery_dict = {}
    for syn, rep in syndrome_table.items():
        syn_str = "".join(map(str, syn))
        rep_str = "".join(map(str, rep))
        recovery_dict[syn_str] = rep_str
        
    return CompletionDichotomyResult(
        is_sufficient=True,
        primal_recovery_table=recovery_dict,
        dual_failure_witness=None,
        unresolved_kernel_dimension=ker_dim,
    )


# Finite instruments for the declared report-fiber and cost criteria.
# The full syndrome kernel is S-perpendicular, not the stabilizer space S.

WEIGHT_CONVENTION = "wt(e)=|supp e_X|+|supp e_Z|"
LATTICE_ASSUMPTION = (
    "periodic Z_L x Z_L, L>=3, one qubit on each edge of the grid; "
    "Pauli space F_2^n ⊕ F_2^n with n=2 L^2"
)


def pauli_commutation_syndrome(L: int) -> np.ndarray:
    """Full CSS commutation syndrome Q(x|z) = (A x, A_v z).

    Its kernel is the symplectic orthogonal S⊥ of the declared stabilizer
    space, not S itself.
    """
    face, star = build_toric_incidence_matrices(L)
    zeros = np.zeros_like(face)
    return np.vstack([
        np.hstack([face, zeros]),
        np.hstack([zeros, star]),
    ]) % 2


def stabilizer_generator_rows(L: int) -> np.ndarray:
    """Rows are X-stars in the X block and Z-plaquettes in the Z block."""
    face, star = build_toric_incidence_matrices(L)
    qubits = face.shape[1]
    rows = []
    for support in star:
        vector = np.zeros(2 * qubits, dtype=int)
        vector[:qubits] = support
        rows.append(vector)
    for support in face:
        vector = np.zeros(2 * qubits, dtype=int)
        vector[qubits:] = support
        rows.append(vector)
    return np.vstack(rows)


def logical_x_representative(L: int) -> np.ndarray:
    """Weight-L vector in S⊥ \\ S: the code's Z1 support placed in the X block.

    That support lies in ker(A) and not in the star span, so it commutes with
    every declared stabilizer and is not a stabilizer.
    """
    face, _star = build_toric_incidence_matrices(L)
    vector = np.zeros(2 * face.shape[1], dtype=int)
    vector[: face.shape[1]] = get_canonical_logicals(L)["X1"]
    return vector


def commutation_kernel_report(L: int) -> dict:
    syndrome = pauli_commutation_syndrome(L)
    generators = stabilizer_generator_rows(L)
    kernel = gf2_nullspace(syndrome)
    rank_syndrome = gf2_rank(syndrome)
    rank_s = gf2_rank(generators)
    witness = logical_x_representative(L)
    in_kernel = bool(np.all(syndrome @ witness % 2 == 0))
    in_s = is_in_span(generators, witness)
    quotient = len(kernel) - rank_s
    return {
        "L": L,
        "lattice": LATTICE_ASSUMPTION,
        "weight_convention": WEIGHT_CONVENTION,
        "ambient_dimension": int(syndrome.shape[1]),
        "rank_syndrome": rank_syndrome,
        "kernel_dimension": len(kernel),
        "stabilizer_dimension": rank_s,
        "quotient_dimension": quotient,
        "kernel_equals_stabilizer": quotient == 0 and in_kernel and in_s,
        "logical_in_kernel": in_kernel,
        "logical_in_stabilizer": in_s,
        "logical_weight": int(np.sum(witness)),
    }


def admitted_collision(syndrome: np.ndarray, errors: List[np.ndarray],
                       repair_rows: np.ndarray):
    """Return an admitted pair with equal syndrome and difference outside B.

    A global rank defect is not consulted. The empty difference set, including
    the t=0 family {0}, yields no collision.
    """
    for left_index, left in enumerate(errors):
        for right in errors[left_index + 1:]:
            difference = (left + right) % 2
            if np.all(syndrome @ difference % 2 == 0) and not is_in_span(repair_rows, difference):
                return left.copy(), right.copy()
    return None


def recovery_witness(syndrome: np.ndarray, errors: List[np.ndarray],
                     repair_rows: np.ndarray) -> dict:
    collision = admitted_collision(syndrome, errors, repair_rows)
    if collision is not None:
        left, right = collision
        return {
            "sufficient": False,
            "kind": "admitted-pair",
            "left": left.tolist(),
            "right": right.tolist(),
        }
    table = {}
    for error in errors:
        if syndrome.size == 0:
            key = tuple()
        else:
            key = tuple(int(bit) for bit in (syndrome @ error % 2))
        table.setdefault(key, error.copy())
    dictionary = {
        "".join(map(str, key)): representative.tolist()
        for key, representative in table.items()
    }
    return {"sufficient": True, "kind": "recovery-table", "table": dictionary}


def _stack_rows(rows: List[np.ndarray], width: int) -> np.ndarray:
    if not rows:
        return np.zeros((0, width), dtype=int)
    return np.vstack(rows) % 2


def suite_separates(rows: List[np.ndarray], errors: List[np.ndarray],
                    repair_rows: np.ndarray) -> bool:
    if not errors:
        return True
    width = errors[0].shape[0]
    return admitted_collision(_stack_rows(rows, width), errors, repair_rows) is None


def _positive_rational(value: object) -> bool:
    if isinstance(value, bool) or isinstance(value, float):
        return False
    if type(value) is int or type(value) is Fraction:
        return value > 0
    return False


def minimum_cost_suite(shelf: List[np.ndarray], costs: List, errors: List[np.ndarray],
                       repair_rows: np.ndarray) -> dict:
    """Terminating exact minimum over a finite shelf with positive rational costs."""
    if len(shelf) != len(costs) or any(not _positive_rational(cost) for cost in costs):
        raise ValueError("positive rational costs required")
    best = None
    best_cost = None
    for size in range(len(shelf) + 1):
        for chosen in itertools.combinations(range(len(shelf)), size):
            rows = [shelf[index] for index in chosen]
            if not suite_separates(rows, errors, repair_rows):
                continue
            cost = sum(costs[index] for index in chosen)
            if best_cost is None or cost < best_cost:
                best = chosen
                best_cost = cost
    if best is None:
        return {"feasible": False, "reason": "shelf_impossible"}
    return {"feasible": True, "indices": best, "cost": best_cost}


def check_minimum_cost_suite(shelf: List[np.ndarray], costs: List, errors: List[np.ndarray],
                             repair_rows: np.ndarray, witness: dict) -> dict:
    """Separate optimality checker. It re-enumerates; it does not call the producer."""
    if len(shelf) != len(costs) or any(not _positive_rational(cost) for cost in costs):
        raise ValueError("positive rational costs required")
    feasible = witness.get("feasible")
    if type(feasible) is not bool:
        raise ValueError("feasible flag required")
    if not feasible:
        whole = suite_separates(list(shelf), errors, repair_rows)
        if whole:
            raise ValueError("false impossibility")
        return {"accepted": True, "feasible": False}
    chosen = tuple(witness["indices"])
    if (any(type(i) is not int or not 0 <= i < len(shelf) for i in chosen)
            or len(set(chosen)) != len(chosen)):
        raise ValueError("suite indices must be distinct declared integers")
    if type(witness.get("cost")) not in (int, Fraction) or witness["cost"] < 0:
        raise ValueError("claimed cost must be an exact nonnegative rational")
    if not suite_separates([shelf[index] for index in chosen], errors, repair_rows):
        raise ValueError("insufficient suite")
    cost = sum(costs[index] for index in chosen)
    if cost != witness["cost"]:
        raise ValueError("cost mismatch")
    if cost > 0 and suite_separates([], errors, repair_rows):
        raise ValueError("t0_requires_full_detector_basis")
    for size in range(len(shelf) + 1):
        for other in itertools.combinations(range(len(shelf)), size):
            other_cost = sum(costs[index] for index in other)
            if other_cost < cost and suite_separates(
                [shelf[index] for index in other], errors, repair_rows
            ):
                raise ValueError("suite is not minimum cost")
    return {"accepted": True, "feasible": True, "cost": cost}


def t0_family(width: int) -> List[np.ndarray]:
    return [np.zeros(width, dtype=int)]


def passive_adaptive_gap() -> dict:
    """Three passive instruments on a four-point admitted family.

    Nonadaptive separation costs 6. The adaptive policy that reads the balanced
    test first and then one branch test has worst-case cost 4. Histories are
    the answer sequences actually produced. Instruments are passive queries:
    they do not change the admitted error.
    """
    hypotheses = ("w", "x", "y", "z")
    tests = {
        "split": {"cost": 2, "answer": {"w": 0, "x": 0, "y": 1, "z": 1}},
        "wx": {"cost": 2, "answer": {"w": 0, "x": 1, "y": 0, "z": 0}},
        "yz": {"cost": 2, "answer": {"w": 0, "x": 0, "y": 0, "z": 1}},
    }

    def separated(selected: tuple) -> bool:
        signatures = []
        for name in hypotheses:
            signatures.append(tuple(tests[key]["answer"][name] for key in selected))
        return len(set(signatures)) == len(hypotheses)

    nonadaptive = min(
        sum(tests[key]["cost"] for key in chosen)
        for size in range(len(tests) + 1)
        for chosen in itertools.combinations(tests, size)
        if separated(chosen)
    )

    def worst_case(remaining: tuple, cache: dict) -> int:
        if remaining in cache:
            return cache[remaining]
        if len(remaining) <= 1:
            cache[remaining] = 0
            return 0
        best = None
        for key, test in tests.items():
            branches: dict = {}
            for name in remaining:
                branches.setdefault(test["answer"][name], []).append(name)
            if len(branches) == 1:
                continue
            cost = test["cost"] + max(
                worst_case(tuple(group), cache) for group in branches.values()
            )
            if best is None or cost < best:
                best = cost
        cache[remaining] = best
        return best

    adaptive = worst_case(hypotheses, {})
    return {
        "hypotheses": hypotheses,
        "nonadaptive_cost": nonadaptive,
        "adaptive_worst_case_cost": adaptive,
        "histories": "answer sequences of passive queries; the error is fixed",
        "instruments": "passive",
        "false_lower_bound": nonadaptive,
    }


def check_kernel_claim(claim: dict, report: dict) -> None:
    """Reject a witness that names the commutation kernel as S."""
    if claim.get("kernel") == "S":
        if (
            report["quotient_dimension"] == 4
            and report["logical_in_kernel"]
            and not report["logical_in_stabilizer"]
            and not report["kernel_equals_stabilizer"]
        ):
            raise ValueError("toric_kernel_identified_with_s")
        raise ValueError("kernel claim does not match the computed carrier")


def check_rank_defect_claim(claim: dict, collision, quotient_dimension: int) -> None:
    """A nonzero quotient is not, by itself, an admitted low-weight pair."""
    if claim.get("collision_from_global_quotient") and collision is None and quotient_dimension > 0:
        raise ValueError("rank_defect_as_low_weight_collision")


def check_adaptive_lower_bound(claimed_lower_bound: int) -> None:
    gap = passive_adaptive_gap()
    if claimed_lower_bound > gap["adaptive_worst_case_cost"]:
        raise ValueError("false_adaptive_lower_bound")


def current_answer_preserves_future(report_matches: bool, future_enabled: bool,
                                    claims_future: bool) -> None:
    """A current-answer instrument that disables a declared future operation
    does not solve the future-operation task.
    """
    if claims_future and report_matches and not future_enabled:
        raise ValueError("current_answer_loses_future_operation")
    if claims_future and not future_enabled:
        raise ValueError("current_answer_loses_future_operation")
