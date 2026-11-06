# -*- coding: utf-8 -*-
r"""
coda_gtla_core.py: CODA-GTLA: Layered Authority and the Master Normal Form.

Implemented finite contracts:
1. Sequential evaluation of exact data with complete profile/gluing checks.
   Historical function names ending in sharp do not supply categories or a
   categorical factorization theorem.
2. Three disjoint local outcome labels. Authorization uses a declared model
   licence; it does not authenticate an external grant or inhabit FDA Standing.
3. Exact repair or positive-residual report. Extended carriers and enumeration
   of tied minimizers are not implemented.
4. Full-record hashes bind supplied data and results. They are integrity
   summaries and do not establish external provenance or policy legitimacy.
5. Regular action of a validated finite groupoid on incoming arrows. Identity,
   composition and hom-set injection are checked for the supplied finite table.
6. Exact rational quotient distances and primal/dual certificates, plus the
   explicitly bounded two-row E2 target ker(dv20)/dh10(ker(dv10)). No general
   spectral-sequence or Lean categorical theorem is asserted.
7. Exact rational arithmetic rejects floats and Boolean scalar inputs.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from cochain_presentation import (
    LinearRepairProblem,
    QuotientDistanceCertificate,
    exact_matrix_from_matrix,
)
from sympy import Abs, Basic, Float, ImmutableMatrix, Integer, Matrix, Rational, simplify
from sympy.matrices.matrixbase import MatrixBase

# ---------------------------------------------------------------------------
# Strict Exact Rational & Type Validation Helpers
# ---------------------------------------------------------------------------


def _validate_exact_rational(val: Any, name: str) -> Rational:
    """Ensure value is an exact rational or integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if isinstance(val, (float, Float)) or (
        val_dtype is not None and "float" in str(val_dtype).lower()
    ):
        raise TypeError(
            f"{name} must be an exact rational or integer, got float (floats strictly forbidden)"
        )
    if isinstance(val, (int, Integer, Fraction, Rational)):
        return Rational(val)
    if isinstance(val, str):
        try:
            return Rational(val)
        except Exception as exc:
            raise TypeError(
                f"{name} string could not be converted to exact Rational: {exc}"
            ) from exc
    if isinstance(val, Basic) and val.is_rational:
        return Rational(val)
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Ensure value is an exact non-negative integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if not isinstance(val, (int, Integer)) or (
        val_dtype is not None and "float" in str(val_dtype).lower()
    ):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    int_val = int(val)
    if int_val < 0:
        raise ValueError(f"{name} must be non-negative, got {int_val}")
    return int_val


def _validate_matrix_exactness(mat: MatrixBase, name: str) -> Matrix:
    """Validate that every entry of a matrix passes the exact rational gate."""
    if not isinstance(mat, MatrixBase):
        raise TypeError(f"{name} must be a SymPy MatrixBase instance, got {type(mat).__name__}")
    for r in range(mat.rows):
        for c in range(mat.cols):
            _validate_exact_rational(mat[r, c], f"{name}[{r},{c}]")
    return exact_matrix_from_matrix(mat)


def _canonical_record(value: Any) -> Any:
    """Canonical, typed serialization of the complete finite evidence record."""
    if isinstance(value, Enum):
        return {"enum": type(value).__name__, "value": value.value}
    if is_dataclass(value) and not isinstance(value, type):
        return {
            "record": type(value).__name__,
            "fields": {
                field.name: _canonical_record(getattr(value, field.name)) for field in fields(value)
            },
        }
    if isinstance(value, MatrixBase):
        return {"matrix_shape": list(value.shape), "entries": [str(x) for x in value]}
    if isinstance(value, Mapping):
        pairs = [(_canonical_record(k), _canonical_record(v)) for k, v in value.items()]
        return {"mapping": sorted(pairs, key=lambda item: json.dumps(item[0], sort_keys=True))}
    if isinstance(value, (tuple, list)):
        return [_canonical_record(x) for x in value]
    if isinstance(value, (Rational, Fraction)):
        return {"rational": str(value)}
    if value is None or isinstance(value, (str, bool, int)):
        return value
    raise TypeError(f"Unsupported evidence value: {type(value).__name__}")


def _record_digest(value: Any) -> str:
    payload = json.dumps(_canonical_record(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Categorical Foundations: CODA_pres and CODA_trace
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FinitePresentation:
    """
    Definition 1.1: Finite Carrier Presentation P = (V, delta).
    - V is an inhabited finite set with carrier_size n >= 1.
    - delta: V x V -> Q>=0 is a symmetric, irreflexive primitive difference matrix.
    """

    name: str
    carrier_size: int
    diff_matrix: Tuple[Tuple[Rational, ...], ...]

    def __post_init__(self) -> None:
        size = _validate_exact_int(self.carrier_size, "carrier_size")
        if size <= 0:
            raise ValueError("Carrier size must be at least 1")
        if len(self.diff_matrix) != size:
            raise ValueError(
                f"Diff matrix rows {len(self.diff_matrix)} mismatch with carrier size {size}"
            )
        if any(len(row) != size for row in self.diff_matrix):
            raise ValueError("Diff matrix row length must match carrier size")
        for r_idx, row in enumerate(self.diff_matrix):
            if len(row) != size:
                raise ValueError(
                    f"Diff matrix row {r_idx} length {len(row)} mismatch with carrier size {size}"
                )
            for c_idx, val in enumerate(row):
                r_val = _validate_exact_rational(val, f"diff[{r_idx},{c_idx}]")
                if r_val < Rational(0, 1):
                    raise ValueError(f"Primitive differences must be non-negative, got {r_val}")
                if r_idx == c_idx and r_val != Rational(0, 1):
                    raise ValueError(f"Self-difference on diagonal must be zero, got {r_val}")
                # Symmetry check
                other_val = _validate_exact_rational(
                    self.diff_matrix[c_idx][r_idx], f"diff[{c_idx},{r_idx}]"
                )
                if r_val != other_val:
                    raise ValueError(
                        f"Primitive difference matrix must be symmetric: diff[{r_idx},{c_idx}]={r_val} != diff[{c_idx},{r_idx}]={other_val}"
                    )
        object.__setattr__(self, "carrier_size", size)
        object.__setattr__(
            self, "diff_matrix", tuple(tuple(Rational(x) for x in row) for row in self.diff_matrix)
        )


@dataclass(frozen=True)
class ComparisonSpan:
    """
    Definition 1.2: Comparison Span P1 <- M -> P2 with extensional morphism cost.
    p1: left presentation
    p2: right presentation
    mid_size: size of intermediate carrier M (must be >= 1)
    left_map: surjective map p1: M -> V1
    right_map: surjective map p2: M -> V2
    ext_cost: extensional morphism cost c_mor(S) in Q>=0
    """

    p1: FinitePresentation
    p2: FinitePresentation
    mid_size: int
    left_map: Tuple[int, ...]
    right_map: Tuple[int, ...]
    ext_cost: Rational = Rational(0, 1)

    def __post_init__(self) -> None:
        size = _validate_exact_int(self.mid_size, "mid_size")
        if size < 1:
            raise ValueError(f"ComparisonSpan intermediate carrier size must be >= 1, got {size}")
        if len(self.left_map) != size or len(self.right_map) != size:
            raise ValueError(f"Projection maps length must match mid_size {size}")

        # Validate range of left and right projection indices
        v1_size = self.p1.carrier_size
        v2_size = self.p2.carrier_size
        for idx, val in enumerate(self.left_map):
            val_int = _validate_exact_int(val, f"left_map[{idx}]")
            if val_int >= v1_size:
                raise ValueError(
                    f"left_map[{idx}]={val_int} out of range for carrier size {v1_size}"
                )
        for idx, val in enumerate(self.right_map):
            val_int = _validate_exact_int(val, f"right_map[{idx}]")
            if val_int >= v2_size:
                raise ValueError(
                    f"right_map[{idx}]={val_int} out of range for carrier size {v2_size}"
                )

        # Enforce surjectivity onto V1 and V2
        if set(self.left_map) != set(range(v1_size)):
            raise ValueError(
                f"left_map must be surjective onto {v1_size} elements, covered {set(self.left_map)}"
            )
        if set(self.right_map) != set(range(v2_size)):
            raise ValueError(
                f"right_map must be surjective onto {v2_size} elements, covered {set(self.right_map)}"
            )

        cost = _validate_exact_rational(self.ext_cost, "ext_cost")
        if cost < Rational(0, 1):
            raise ValueError(f"Extensional cost must be non-negative, got {cost}")
        object.__setattr__(self, "mid_size", size)
        object.__setattr__(self, "left_map", tuple(int(x) for x in self.left_map))
        object.__setattr__(self, "right_map", tuple(int(x) for x in self.right_map))
        object.__setattr__(self, "ext_cost", cost)

    def relation(self) -> Set[Tuple[int, int]]:
        """Extensional relation R subseteq V1 x V2 induced by the span."""
        return set(zip(self.left_map, self.right_map))


def extensional_equal(s1: ComparisonSpan, s2: ComparisonSpan) -> bool:
    """
    Check extensional equality of two comparison spans in CODA_pres:
    Same domain, same codomain, identical induced relation, and identical extensional cost.
    """
    return (
        s1.p1 == s2.p1
        and s1.p2 == s2.p2
        and s1.relation() == s2.relation()
        and s1.ext_cost == s2.ext_cost
    )


def make_diag_span(p: FinitePresentation) -> ComparisonSpan:
    """Identity morphism in CODA_pres: diagonal span [Delta_P] with cost 0."""
    indices = tuple(range(p.carrier_size))
    return ComparisonSpan(
        p1=p,
        p2=p,
        mid_size=p.carrier_size,
        left_map=indices,
        right_map=indices,
        ext_cost=Rational(0, 1),
    )


def compose_spans(s1: ComparisonSpan, s2: ComparisonSpan) -> ComparisonSpan:
    """
    Definition 1.3: Relational pullback composition of comparison spans [S2] * [S1].
    M_12 = {(m1, m2) in M1 x M2 | s1.right_map[m1] == s2.left_map[m2]}
    c_mor([S2] * [S1]) <= c_mor([S2]) + c_mor([S1]) (subadditive cost).
    """
    if s1.p2 != s2.p1:
        raise ValueError(f"Span composition target/source mismatch: {s1.p2.name} != {s2.p1.name}")

    pb_pairs: List[Tuple[int, int]] = []
    for m1 in range(s1.mid_size):
        for m2 in range(s2.mid_size):
            if s1.right_map[m1] == s2.left_map[m2]:
                pb_pairs.append((m1, m2))

    if len(pb_pairs) == 0:
        raise ValueError("Empty relational pullback apex in span composition")

    left_map = tuple(s1.left_map[p[0]] for p in pb_pairs)
    right_map = tuple(s2.right_map[p[1]] for p in pb_pairs)
    cost = _validate_exact_rational(s1.ext_cost + s2.ext_cost, "composite_ext_cost")

    return ComparisonSpan(
        p1=s1.p1,
        p2=s2.p2,
        mid_size=len(pb_pairs),
        left_map=left_map,
        right_map=right_map,
        ext_cost=cost,
    )


@dataclass(frozen=True)
class Trace:
    """
    Intensional execution trace in CODA_trace.
    Carries execution step count and physical work cost in Q>=0.
    """

    steps: int
    work_cost: Rational
    span: ComparisonSpan

    def __post_init__(self) -> None:
        _validate_exact_int(self.steps, "steps")
        cost = _validate_exact_rational(self.work_cost, "work_cost")
        if cost < Rational(0, 1):
            raise ValueError(f"Work cost must be non-negative, got {cost}")
        object.__setattr__(self, "steps", int(self.steps))
        object.__setattr__(self, "work_cost", cost)


def make_id_trace(p: FinitePresentation) -> Trace:
    """Identity trace with zero steps and zero work."""
    return Trace(steps=0, work_cost=Rational(0, 1), span=make_diag_span(p))


def compose_traces(t1: Trace, t2: Trace) -> Trace:
    """Intensional composition of execution traces."""
    comp_span = compose_spans(t1.span, t2.span)
    steps = t1.steps + t2.steps
    work = _validate_exact_rational(t1.work_cost + t2.work_cost, "composite_work_cost")
    return Trace(steps=steps, work_cost=work, span=comp_span)


def erase_trace(t: Trace) -> ComparisonSpan:
    """Erasure quotient functor q: CODA_trace -> CODA_pres."""
    return t.span


# ---------------------------------------------------------------------------
# Transport Certificates (\tau^\sharp) and Monodromy Evaluation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TransportCertificate:
    r"""
    Certified transport outcome \tau^\sharp for a comparison span or span chain.
    Records:
    - span: Underlying ComparisonSpan in CODA_pres
    - trace: Optional underlying intensional execution Trace in CODA_trace
    - is_closed_loop: Whether span domain equals codomain (p1 == p2)
    - is_trivial_monodromy: True iff closed loop and induced relation is the diagonal Delta_{V0}
    - monodromy_permutation: Optional tuple representing permutation sigma: V0 -> V0
    - monodromy_defect: Exact rational distance from identity
    - ext_cost: Extensional morphism cost c_mor(span) in Q>=0
    - work_cost: Declared intensional work cost c_trace(trace) in Q>=0
    - certificate_id: Canonical identifier
    - extensional_hash: Deterministic digest of extensional properties in CODA_pres
    - sha256_hash: Cryptographic digest of full execution trace
    """

    span: ComparisonSpan
    trace: Optional[Trace]
    is_closed_loop: bool
    is_trivial_monodromy: bool
    monodromy_permutation: Optional[Tuple[int, ...]]
    monodromy_defect: Rational
    ext_cost: Rational
    work_cost: Rational
    certificate_id: str
    extensional_hash: str
    sha256_hash: str

    def __post_init__(self) -> None:
        _validate_exact_rational(self.monodromy_defect, "monodromy_defect")
        _validate_exact_rational(self.ext_cost, "ext_cost")
        _validate_exact_rational(self.work_cost, "work_cost")
        if not isinstance(self.is_closed_loop, bool):
            raise TypeError("is_closed_loop must be bool")
        if not isinstance(self.is_trivial_monodromy, bool):
            raise TypeError("is_trivial_monodromy must be bool")
        if self.is_trivial_monodromy and not self.is_closed_loop:
            raise ValueError("Non-closed loop cannot have trivial monodromy")
        if self.is_trivial_monodromy and self.monodromy_defect != Rational(0, 1):
            raise ValueError("Trivial monodromy must have defect 0")


def compute_transport_certificate(
    span: ComparisonSpan,
    trace: Optional[Trace] = None,
    certificate_id: Optional[str] = None,
) -> TransportCertificate:
    r"""
    Compute and certify transport outcome \tau^\sharp for a comparison span.
    Evaluates closed-loop status, fiber relation, permutation monodromy, and exact rational defect.
    """
    if trace is not None:
        if not extensional_equal(trace.span, span):
            raise ValueError("Supplied trace span does not match comparison span extensionally")
        work_cost = trace.work_cost
    else:
        work_cost = Rational(0, 1)

    cid = certificate_id or f"tau_{span.p1.name}_{span.p2.name}_{span.mid_size}"
    is_closed = span.p1 == span.p2

    if not is_closed:
        summary = {
            "certificate_id": cid,
            "is_closed_loop": False,
            "is_trivial_monodromy": False,
            "monodromy_permutation": None,
            "monodromy_defect": "0",
            "ext_cost": str(span.ext_cost),
            "work_cost": str(work_cost),
            "p1": span.p1.name,
            "p2": span.p2.name,
        }
        digest = _record_digest(
            {"schema": "gtla-transport-v2", "span": span, "trace": trace, "outcome": summary}
        )
        ext_summary = {
            "is_closed_loop": False,
            "p1_size": span.p1.carrier_size,
            "p2_size": span.p2.carrier_size,
            "relation": sorted(list(span.relation())),
            "ext_cost": str(span.ext_cost),
            "is_trivial_monodromy": False,
            "monodromy_permutation": None,
            "monodromy_defect": "0",
        }
        ext_digest = _record_digest(
            {"schema": "gtla-extensional-v2", "p1": span.p1, "p2": span.p2, "outcome": ext_summary}
        )
        return TransportCertificate(
            span=span,
            trace=trace,
            is_closed_loop=False,
            is_trivial_monodromy=False,
            monodromy_permutation=None,
            monodromy_defect=Rational(0, 1),
            ext_cost=span.ext_cost,
            work_cost=work_cost,
            certificate_id=cid,
            extensional_hash=ext_digest,
            sha256_hash=digest,
        )

    # Closed loop: evaluate fiber relation on V0
    n = span.p1.carrier_size
    rel = span.relation()

    left_to_right: Dict[int, Set[int]] = {}
    for left_pt, right_pt in rel:
        left_to_right.setdefault(left_pt, set()).add(right_pt)

    is_bijective = (
        len(left_to_right) == n
        and all(len(tgts) == 1 for tgts in left_to_right.values())
        and {next(iter(tgts)) for tgts in left_to_right.values()} == set(range(n))
    )

    if is_bijective:
        perm = tuple(next(iter(left_to_right[i])) for i in range(n))
        is_trivial = perm == tuple(range(n))
        if is_trivial:
            defect = Rational(0, 1)
        else:
            diff_sum = sum(span.p1.diff_matrix[i][perm[i]] for i in range(n))
            if diff_sum > Rational(0, 1):
                defect = Rational(diff_sum)
            else:
                hamming = sum(1 for i in range(n) if perm[i] != i)
                defect = Rational(hamming, 1)
        perm_val = perm
    else:
        is_trivial = False
        perm_val = None
        diag = {(i, i) for i in range(n)}
        sym_diff_count = len(rel.symmetric_difference(diag))
        defect = Rational(sym_diff_count, 1)

    summary = {
        "certificate_id": cid,
        "is_closed_loop": True,
        "is_trivial_monodromy": is_trivial,
        "monodromy_permutation": list(perm_val) if perm_val is not None else None,
        "monodromy_defect": str(defect),
        "ext_cost": str(span.ext_cost),
        "work_cost": str(work_cost),
        "p1": span.p1.name,
        "p2": span.p2.name,
    }
    digest = _record_digest(
        {"schema": "gtla-transport-v2", "span": span, "trace": trace, "outcome": summary}
    )

    ext_summary = {
        "is_closed_loop": True,
        "p1_size": span.p1.carrier_size,
        "p2_size": span.p2.carrier_size,
        "relation": sorted(list(span.relation())),
        "ext_cost": str(span.ext_cost),
        "is_trivial_monodromy": is_trivial,
        "monodromy_permutation": list(perm_val) if perm_val is not None else None,
        "monodromy_defect": str(defect),
    }
    ext_digest = _record_digest(
        {"schema": "gtla-extensional-v2", "p1": span.p1, "p2": span.p2, "outcome": ext_summary}
    )

    return TransportCertificate(
        span=span,
        trace=trace,
        is_closed_loop=True,
        is_trivial_monodromy=is_trivial,
        monodromy_permutation=perm_val,
        monodromy_defect=defect,
        ext_cost=span.ext_cost,
        work_cost=work_cost,
        certificate_id=cid,
        extensional_hash=ext_digest,
        sha256_hash=digest,
    )


def perturb_presentation_carrier_size(
    pres: FinitePresentation,
    delta_size: int,
    fill_diff: Rational = Rational(1, 1),
    name_suffix: str = "_perturbed",
) -> FinitePresentation:
    r"""
    Adversarial carrier size mutation: n \to n + delta_size.
    Preserves existing difference submatrix and fills added elements symmetrically.
    """
    n = pres.carrier_size
    new_size = n + delta_size
    if new_size < 1:
        raise ValueError(f"Perturbed carrier size must be >= 1, got {new_size}")
    fill_rat = _validate_exact_rational(fill_diff, "fill_diff")

    if delta_size == 0:
        return pres

    new_diff: List[List[Rational]] = [
        [Rational(0, 1) for _ in range(new_size)] for _ in range(new_size)
    ]

    for r in range(new_size):
        for c in range(new_size):
            if r == c:
                new_diff[r][c] = Rational(0, 1)
            elif r < n and c < n:
                new_diff[r][c] = pres.diff_matrix[r][c]
            else:
                new_diff[r][c] = fill_rat

    matrix_tuple = tuple(tuple(row) for row in new_diff)
    return FinitePresentation(
        name=f"{pres.name}{name_suffix}_{new_size}",
        carrier_size=new_size,
        diff_matrix=matrix_tuple,
    )


def build_monodromy_transport_loop(
    base_pres: FinitePresentation,
    mode: str = "unperturbed",
) -> Tuple[ComparisonSpan, Optional[Trace]]:
    r"""
    Constructs a closed transport loop S_loop = S_k * ... * S_1: base_pres -> base_pres
    under declared perturbation modes:
    - 'unperturbed': Identity round-trip (e.g. g * g^-1 in Z2), trivial monodromy.
    - 'spectator_mutation': Extends carrier size by +1 as an unentangled spectator state.
      Core base points remain flat (trivial monodromy).
    - 'entangled_mutation': Extends carrier size by +1 (ancilla point n) and weaves
      base points through the ancilla: (0 n) o (1 n) o (0 n) = (0 1)(n).
      Produces non-trivial monodromy permutation (1, 0, 2, ..., n).
    - 'branching_mutation': Enlarges intermediate apex M to produce a multi-valued
      fiber branching relation with non-trivial defect.
    """
    n = base_pres.carrier_size
    if n < 2 and mode in ("unperturbed", "entangled_mutation"):
        raise ValueError(f"Base presentation size must be >= 2 for non-trivial test, got {n}")

    if mode == "unperturbed":
        perm_g = (1, 0) + tuple(range(2, n))
        s1 = ComparisonSpan(
            p1=base_pres,
            p2=base_pres,
            mid_size=n,
            left_map=tuple(range(n)),
            right_map=perm_g,
            ext_cost=Rational(0, 1),
        )
        s2 = ComparisonSpan(
            p1=base_pres,
            p2=base_pres,
            mid_size=n,
            left_map=tuple(range(n)),
            right_map=perm_g,
            ext_cost=Rational(0, 1),
        )
        t1 = Trace(steps=1, work_cost=Rational(3, 2), span=s1)
        t2 = Trace(steps=1, work_cost=Rational(3, 2), span=s2)
        s_comp = compose_spans(s1, s2)
        t_comp = compose_traces(t1, t2)
        return s_comp, t_comp

    elif mode == "spectator_mutation":
        pert_pres = perturb_presentation_carrier_size(base_pres, delta_size=1)
        s1 = make_diag_span(pert_pres)
        s2 = make_diag_span(pert_pres)
        t1 = Trace(steps=1, work_cost=Rational(2, 1), span=s1)
        t2 = Trace(steps=1, work_cost=Rational(2, 1), span=s2)
        s_comp = compose_spans(s1, s2)
        t_comp = compose_traces(t1, t2)
        return s_comp, t_comp

    elif mode == "entangled_mutation":
        pert_pres = perturb_presentation_carrier_size(base_pres, delta_size=1)
        n_pert = pert_pres.carrier_size
        ancilla = n_pert - 1

        perm_0_anc = list(range(n_pert))
        perm_0_anc[0], perm_0_anc[ancilla] = perm_0_anc[ancilla], perm_0_anc[0]
        t_0_anc = tuple(perm_0_anc)

        perm_1_anc = list(range(n_pert))
        perm_1_anc[1], perm_1_anc[ancilla] = perm_1_anc[ancilla], perm_1_anc[1]
        t_1_anc = tuple(perm_1_anc)

        s1 = ComparisonSpan(
            p1=pert_pres,
            p2=pert_pres,
            mid_size=n_pert,
            left_map=tuple(range(n_pert)),
            right_map=t_0_anc,
            ext_cost=Rational(0, 1),
        )
        s2 = ComparisonSpan(
            p1=pert_pres,
            p2=pert_pres,
            mid_size=n_pert,
            left_map=tuple(range(n_pert)),
            right_map=t_1_anc,
            ext_cost=Rational(0, 1),
        )
        s3 = ComparisonSpan(
            p1=pert_pres,
            p2=pert_pres,
            mid_size=n_pert,
            left_map=tuple(range(n_pert)),
            right_map=t_0_anc,
            ext_cost=Rational(0, 1),
        )

        tr1 = Trace(steps=1, work_cost=Rational(1, 1), span=s1)
        tr2 = Trace(steps=1, work_cost=Rational(1, 1), span=s2)
        tr3 = Trace(steps=1, work_cost=Rational(1, 1), span=s3)

        s_12 = compose_spans(s1, s2)
        s_123 = compose_spans(s_12, s3)
        tr_12 = compose_traces(tr1, tr2)
        tr_123 = compose_traces(tr_12, tr3)
        return s_123, tr_123

    elif mode == "branching_mutation":
        pert_pres = perturb_presentation_carrier_size(base_pres, delta_size=0)
        m_size = n + 1
        left_map = tuple(range(n)) + (0,)
        right_map = tuple(range(n)) + (1,)
        s_branch = ComparisonSpan(
            p1=pert_pres,
            p2=pert_pres,
            mid_size=m_size,
            left_map=left_map,
            right_map=right_map,
            ext_cost=Rational(1, 2),
        )
        tr_branch = Trace(steps=2, work_cost=Rational(5, 2), span=s_branch)
        return s_branch, tr_branch

    else:
        raise ValueError(f"Unknown monodromy loop mode: {mode}")


# ---------------------------------------------------------------------------
# Carrier Gauge Transformations & Exact Cochain Homotopy
# ---------------------------------------------------------------------------


def apply_carrier_gauge_transformation(
    s1: ComparisonSpan,
    s2: ComparisonSpan,
    gauge_perm: Tuple[int, ...],
) -> Tuple[ComparisonSpan, ComparisonSpan]:
    r"""
    Applies an isometric gauge automorphism g \in S_{V_mid} to the intermediate carrier P_mid = s1.p2 = s2.p1.
    Transforms:
      S_1: P_0 <- M_1 -> P_mid  ===>  S_1^g: P_0 <- M_1 -> P_mid^g (right map composed with g)
      S_2: P_mid <- M_2 -> P_2  ===>  S_2^g: P_mid^g <- M_2 -> P_2 (left map composed with g)
    Preserves exact span composition: S_2^g * S_1^g == S_2 * S_1 in CODA_pres.
    """
    if s1.p2 != s2.p1:
        raise ValueError(
            f"Spans must be composable at intermediate presentation: {s1.p2.name} != {s2.p1.name}"
        )

    p_mid = s1.p2
    n_mid = p_mid.carrier_size
    if len(gauge_perm) != n_mid:
        raise ValueError(
            f"gauge_perm length {len(gauge_perm)} does not match intermediate carrier size {n_mid}"
        )
    if set(gauge_perm) != set(range(n_mid)):
        raise ValueError("gauge_perm must be a bijective permutation on intermediate carrier")

    # Inverse permutation to pull back metric differences
    inv_g = [0] * n_mid
    for i, gi in enumerate(gauge_perm):
        inv_g[gi] = i

    # Gauge-transformed difference matrix: delta^g(gi, gj) = delta(i, j) => delta^g(r, c) = delta(inv_g[r], inv_g[c])
    new_diff = [[p_mid.diff_matrix[inv_g[r]][inv_g[c]] for c in range(n_mid)] for r in range(n_mid)]
    p_mid_g = FinitePresentation(
        name=f"{p_mid.name}_gauge",
        carrier_size=n_mid,
        diff_matrix=tuple(tuple(row) for row in new_diff),
    )

    new_s1_right = tuple(gauge_perm[val] for val in s1.right_map)
    s1_g = ComparisonSpan(
        p1=s1.p1,
        p2=p_mid_g,
        mid_size=s1.mid_size,
        left_map=s1.left_map,
        right_map=new_s1_right,
        ext_cost=s1.ext_cost,
    )

    new_s2_left = tuple(gauge_perm[val] for val in s2.left_map)
    s2_g = ComparisonSpan(
        p1=p_mid_g,
        p2=s2.p2,
        mid_size=s2.mid_size,
        left_map=new_s2_left,
        right_map=s2.right_map,
        ext_cost=s2.ext_cost,
    )

    return s1_g, s2_g


def apply_cochain_homotopy(defect: Matrix, d0: Matrix, h: Matrix) -> Matrix:
    r"""
    Applies exact cochain coboundary shift \delta' = \delta + d_0 h.
    Preserves cohomology / quotient class [\delta'] = [\delta] in Q^1.
    """
    _validate_matrix_exactness(defect, "defect")
    _validate_matrix_exactness(d0, "d0")
    _validate_matrix_exactness(h, "h")

    if defect.cols != 1:
        raise ValueError(f"Defect must be a single column vector, got cols={defect.cols}")
    if h.cols != 1:
        raise ValueError(f"Homotopy h must be a single column vector, got cols={h.cols}")
    if d0.rows != defect.rows:
        raise ValueError(f"d0 rows {d0.rows} must match defect rows {defect.rows}")
    if d0.cols != h.rows:
        raise ValueError(f"d0 cols {d0.cols} must match h rows {h.rows}")

    shifted = defect + d0 * h
    return exact_matrix_from_matrix(shifted)


def verify_cochain_homotopy_invariance(
    d0: Matrix,
    defect_1: Matrix,
    defect_2: Matrix,
    h: Optional[Matrix] = None,
) -> Dict[str, Any]:
    r"""
    Verifies that two defect cochains differing by coboundary d_0 h
    induce identical exact rational quotient distances \Phi_1 and that
    dual witness certificates pair identically.
    """
    _validate_matrix_exactness(d0, "d0")
    _validate_matrix_exactness(defect_1, "defect_1")
    _validate_matrix_exactness(defect_2, "defect_2")

    is_exact_homotopy = True
    if h is not None:
        _validate_matrix_exactness(h, "h")
        diff = defect_2 - (defect_1 + d0 * h)
        if not diff.is_zero_matrix:
            is_exact_homotopy = False
    else:
        diff = defect_2 - defect_1
        solver_diff = LinearRepairProblem(repair_map_d0=d0)
        cert_diff = solver_diff.quotient_l1_distance(cochain=diff)
        is_exact_homotopy = cert_diff.distance == Rational(0, 1)

    solver = LinearRepairProblem(repair_map_d0=d0)
    cert1 = solver.quotient_l1_distance(cochain=defect_1)
    cert2 = solver.quotient_l1_distance(cochain=defect_2)

    phi1_1 = Rational(cert1.distance)
    phi1_2 = Rational(cert2.distance)
    distances_equal = phi1_1 == phi1_2

    witness1_valid_on_defect2 = False
    witness2_valid_on_defect1 = False

    if phi1_1 > Rational(0, 1):
        witness1 = tuple(Rational(cert1.dual_witness[r, 0]) for r in range(cert1.dual_witness.rows))
        witness1_valid_on_defect2 = validate_dual_witness(d0, defect_2, witness1, phi1_2)
    else:
        witness1_valid_on_defect2 = phi1_2 == Rational(0, 1)

    if phi1_2 > Rational(0, 1):
        witness2 = tuple(Rational(cert2.dual_witness[r, 0]) for r in range(cert2.dual_witness.rows))
        witness2_valid_on_defect1 = validate_dual_witness(d0, defect_1, witness2, phi1_1)
    else:
        witness2_valid_on_defect1 = phi1_1 == Rational(0, 1)

    return {
        "is_exact_homotopy": is_exact_homotopy,
        "phi1_defect1": str(phi1_1),
        "phi1_defect2": str(phi1_2),
        "distances_equal": distances_equal,
        "witness1_certifies_defect2": witness1_valid_on_defect2,
        "witness2_certifies_defect1": witness2_valid_on_defect1,
        "invariance_holds": is_exact_homotopy
        and distances_equal
        and witness1_valid_on_defect2
        and witness2_valid_on_defect1,
    }


def evaluate_span_homotopy_transport(
    seq1: Sequence[ComparisonSpan],
    seq2: Sequence[ComparisonSpan],
    traces1: Optional[Sequence[Trace]] = None,
    traces2: Optional[Sequence[Trace]] = None,
) -> Dict[str, Any]:
    r"""
    Evaluates whether two composable sequences of comparison spans induce identical
    transport certificates \tau_1^\sharp \equiv \tau_2^\sharp despite intermediate carrier
    gauge transformations or differing internal path topologies.
    """
    if len(seq1) == 0 or len(seq2) == 0:
        raise ValueError("Span sequences must be non-empty")

    s1_comp = seq1[0]
    for s in seq1[1:]:
        s1_comp = compose_spans(s1_comp, s)

    s2_comp = seq2[0]
    for s in seq2[1:]:
        s2_comp = compose_spans(s2_comp, s)

    tr1_comp = None
    if traces1 is not None and len(traces1) == len(seq1):
        tr1_comp = traces1[0]
        for t in traces1[1:]:
            tr1_comp = compose_traces(tr1_comp, t)

    tr2_comp = None
    if traces2 is not None and len(traces2) == len(seq2):
        tr2_comp = traces2[0]
        for t in traces2[1:]:
            tr2_comp = compose_traces(tr2_comp, t)

    cert1 = compute_transport_certificate(s1_comp, trace=tr1_comp)
    cert2 = compute_transport_certificate(s2_comp, trace=tr2_comp)

    spans_extensionally_equal = extensional_equal(s1_comp, s2_comp)
    ext_hashes_equal = cert1.extensional_hash == cert2.extensional_hash
    trace_hashes_equal = cert1.sha256_hash == cert2.sha256_hash
    monodromy_equal = (
        cert1.is_closed_loop == cert2.is_closed_loop
        and cert1.is_trivial_monodromy == cert2.is_trivial_monodromy
        and cert1.monodromy_permutation == cert2.monodromy_permutation
        and cert1.monodromy_defect == cert2.monodromy_defect
    )

    two_level_divergence = False
    if tr1_comp is not None and tr2_comp is not None:
        two_level_divergence = (
            tr1_comp.work_cost != tr2_comp.work_cost or tr1_comp.steps != tr2_comp.steps
        )

    return {
        "spans_extensionally_equal": spans_extensionally_equal,
        "hashes_equal": ext_hashes_equal,
        "extensional_hashes_equal": ext_hashes_equal,
        "trace_hashes_equal": trace_hashes_equal,
        "monodromy_equal": monodromy_equal,
        "certificates_identical": spans_extensionally_equal
        and ext_hashes_equal
        and monodromy_equal,
        "ext_cost_1": str(cert1.ext_cost),
        "ext_cost_2": str(cert2.ext_cost),
        "work_cost_1": str(cert1.work_cost),
        "work_cost_2": str(cert2.work_cost),
        "two_level_cost_divergence": two_level_divergence,
        "tau1": cert1,
        "tau2": cert2,
    }


# ---------------------------------------------------------------------------
# CD-12 Faithful Groupoid Embedding & Two-Level Cost Accounting
# ---------------------------------------------------------------------------


@dataclass
class FiniteGroupoid:
    """Finite groupoid with objects, morphisms, identities, compositions, and inverses."""

    objects: List[str]
    morphisms: Dict[str, Dict[str, List[str]]]  # obj_src -> obj_tgt -> list of mor_names
    id_map: Dict[str, str]  # obj -> id_mor_name
    comp_table: Dict[Tuple[str, str], str]  # (g, f) -> g o f (where f: A->B, g: B->C)
    inv_map: Dict[str, str]  # f -> f^-1

    def validate(self) -> bool:
        """Thoroughly validate all groupoid laws: identities, inverses, associativity, totality."""
        if not self.objects or len(set(self.objects)) != len(self.objects):
            return False
        objects = set(self.objects)
        if set(self.id_map) != objects or not set(self.morphisms).issubset(objects):
            return False
        if any(not set(targets).issubset(objects) for targets in self.morphisms.values()):
            return False
        # 1. Identity map presence and hom-set placement
        for obj in self.objects:
            if obj not in self.id_map:
                return False
            id_mor = self.id_map[obj]
            if id_mor not in self.morphisms.get(obj, {}).get(obj, []):
                return False

        # Build morphism lookup: mor_name -> (src, tgt)
        mor_lookup: Dict[str, Tuple[str, str]] = {}
        for src, tgts in self.morphisms.items():
            for tgt, mors in tgts.items():
                for m in mors:
                    if m in mor_lookup:
                        return False  # Duplicate morphism name
                    mor_lookup[m] = (src, tgt)

        # 2. Inverses and units
        for f, (a, b) in mor_lookup.items():
            if f not in self.inv_map:
                return False
            f_inv = self.inv_map[f]
            if f_inv not in mor_lookup:
                return False
            if mor_lookup[f_inv] != (b, a):
                return False
            # Inverse laws: f_inv o f == id_a and f o f_inv == id_b
            if self.comp_table.get((f_inv, f)) != self.id_map[a]:
                return False
            if self.comp_table.get((f, f_inv)) != self.id_map[b]:
                return False
            # Unit laws: id_b o f == f and f o id_a == f
            if self.comp_table.get((self.id_map[b], f)) != f:
                return False
            if self.comp_table.get((f, self.id_map[a])) != f:
                return False

        if set(self.inv_map) != set(mor_lookup):
            return False
        required_pairs = {
            (g, f)
            for g, (sg, _) in mor_lookup.items()
            for f, (_, tf) in mor_lookup.items()
            if tf == sg
        }
        if set(self.comp_table) != required_pairs:
            return False
        # 3. Composition totality and codomain matching
        for (g, f), gf in self.comp_table.items():
            if g not in mor_lookup or f not in mor_lookup:
                return False
            src_f, tgt_f = mor_lookup[f]
            src_g, tgt_g = mor_lookup[g]
            if tgt_f != src_g:
                return False  # Non-composable pair in table
            if gf not in mor_lookup:
                return False
            if mor_lookup[gf] != (src_f, tgt_g):
                return False

        # 4. Associativity for all composable triples (h, g, f)
        for (g, f), gf in self.comp_table.items():
            src_f, tgt_f = mor_lookup[f]
            src_g, tgt_g = mor_lookup[g]
            for h, (src_h, tgt_h) in mor_lookup.items():
                if src_h == tgt_g:
                    # h o (g o f)
                    h_gf = self.comp_table.get((h, gf))
                    # (h o g) o f
                    hg = self.comp_table.get((h, g))
                    if hg is None:
                        return False
                    hg_f = self.comp_table.get((hg, f))
                    if h_gf != hg_f:
                        return False

        return True


def make_z2_groupoid() -> FiniteGroupoid:
    """Finite groupoid for Z_2 (single object point groupoid)."""
    return FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e", "g"]}},
        id_map={"*": "e"},
        comp_table={
            ("e", "e"): "e",
            ("e", "g"): "g",
            ("g", "e"): "g",
            ("g", "g"): "e",
        },
        inv_map={"e": "e", "g": "g"},
    )


def make_z3_groupoid() -> FiniteGroupoid:
    """Finite groupoid for Z_3."""
    return FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e", "g", "g2"]}},
        id_map={"*": "e"},
        comp_table={
            ("e", "e"): "e",
            ("e", "g"): "g",
            ("e", "g2"): "g2",
            ("g", "e"): "g",
            ("g", "g"): "g2",
            ("g", "g2"): "e",
            ("g2", "e"): "g2",
            ("g2", "g"): "e",
            ("g2", "g2"): "g",
        },
        inv_map={"e": "e", "g": "g2", "g2": "g"},
    )


class FaithfulGroupoidEmbedding:
    """
    CD-12 finite model: checked regular action with span and trace records.

    To be genuinely faithful on hom-sets (E(f) = E(g) implies f = g), the target
    presentations must have sufficient carrier size to distinguish non-trivial automorphisms.
    For Z_2 = {e, g}, we embed into a presentation with carrier size 2:
      E(e) = identity span: (0, 1) -> (0, 1)
      E(g) = transposition span: (0, 1) -> (1, 0)
    Then E(e) != E(g) extensionally, E(g) * E(g) = E(e), and faithfulness is verified.
    """

    def __init__(self, groupoid: FiniteGroupoid):
        self.groupoid = deepcopy(groupoid)
        if not self.groupoid.validate():
            raise ValueError("Groupoid fails structural laws validation")
        groupoid = self.groupoid
        # V_a is the finite set of all arrows ending at a. Postcomposition
        # by g:a->b is a bijection V_a->V_b, with inverse postcomposition by g^-1.
        incoming = {
            obj: [
                m for src in groupoid.objects for m in groupoid.morphisms.get(src, {}).get(obj, [])
            ]
            for obj in groupoid.objects
        }
        self.presentations: Dict[str, FinitePresentation] = {
            obj: FinitePresentation(
                name=f"Pres_{obj}",
                carrier_size=len(arrows),
                diff_matrix=tuple(tuple(Rational(0) for _ in arrows) for _ in arrows),
            )
            for obj, arrows in incoming.items()
        }
        self.spans: Dict[str, ComparisonSpan] = {}
        for src, targets in groupoid.morphisms.items():
            for tgt, arrows in targets.items():
                positions = {m: i for i, m in enumerate(incoming[tgt])}
                for arrow in arrows:
                    image = tuple(positions[groupoid.comp_table[(arrow, h)]] for h in incoming[src])
                    self.spans[arrow] = ComparisonSpan(
                        p1=self.presentations[src],
                        p2=self.presentations[tgt],
                        mid_size=len(incoming[src]),
                        left_map=tuple(range(len(incoming[src]))),
                        right_map=image,
                    )
        if not self.check_faithfulness():
            raise ArithmeticError("Regular action failed functor or injectivity check")

    def embed_object(self, obj: str) -> FinitePresentation:
        return self.presentations[obj]

    def embed_morphism(self, mor: str) -> ComparisonSpan:
        return self.spans[mor]

    def lift_trace(self, mor: str, work_cost: Rational = Rational(1, 1)) -> Trace:
        _validate_exact_rational(work_cost, "work_cost")
        return Trace(steps=1, work_cost=work_cost, span=self.spans[mor])

    def check_faithfulness(self) -> bool:
        """
        Verify genuine categorical faithfulness:
        For every hom-set Hom(A, B), the map E: Hom(A, B) -> Mor_CODA_pres(E(A), E(B))
        is injective up to extensional equivalence.
        Also verify that E preserves identities and composition.
        """
        for src, tgts in self.groupoid.morphisms.items():
            for tgt, mors in tgts.items():
                # Hom-set injectivity
                for i in range(len(mors)):
                    for j in range(i + 1, len(mors)):
                        m1, m2 = mors[i], mors[j]
                        s1, s2 = self.spans[m1], self.spans[m2]
                        if extensional_equal(s1, s2):
                            return False  # Non-injective on hom-set!

        # Preservation of identities: E(id_A) == Delta_{E(A)}
        for obj in self.groupoid.objects:
            id_mor = self.groupoid.id_map[obj]
            e_id = self.spans[id_mor]
            diag = make_diag_span(self.presentations[obj])
            if not extensional_equal(e_id, diag):
                return False

        # Preservation of composition: E(g o f) == E(g) * E(f)
        for (g, f), gf in self.groupoid.comp_table.items():
            s_f = self.spans[f]
            s_g = self.spans[g]
            s_comp = compose_spans(s_f, s_g)
            s_gf = self.spans[gf]
            if not extensional_equal(s_comp, s_gf):
                return False

        return True

    def check_two_level_cost_accounting(
        self, mor: str, work: Rational = Rational(5, 2)
    ) -> Dict[str, Any]:
        """
        Verify that extensional cost is 0 on inverse round-trip while
        intensional trace cost is strictly positive.
        """
        _validate_exact_rational(work, "work")
        inv_mor = self.groupoid.inv_map[mor]
        s = self.embed_morphism(mor)
        s_inv = self.embed_morphism(inv_mor)
        s_comp = compose_spans(s, s_inv)

        t = self.lift_trace(mor, work_cost=work)
        t_inv = self.lift_trace(inv_mor, work_cost=work)
        t_comp = compose_traces(t, t_inv)

        return {
            "extensional_cost": s_comp.ext_cost,
            "intensional_work_cost": t_comp.work_cost,
            "trace_steps": t_comp.steps,
            "extensional_is_zero": bool(s_comp.ext_cost == Rational(0, 1)),
            "intensional_is_positive": bool(t_comp.work_cost > Rational(0, 1)),
        }


# ---------------------------------------------------------------------------
# Authority Provenance & Token Model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AuthorityToken:
    """
    Declared licence record for the finite evaluator, not an authenticated grant.
    is_valid is supplied model data. signature_hash is an opaque provenance label;
    this package verifies neither signatures nor institutional entitlement.
    """

    token_id: str
    issuer: str
    subject: str
    scope: str
    is_valid: bool
    signature_hash: str

    def __post_init__(self) -> None:
        if not isinstance(self.token_id, str) or not self.token_id:
            raise ValueError("AuthorityToken token_id must be a non-empty string")
        if not isinstance(self.issuer, str) or not self.issuer:
            raise ValueError("AuthorityToken issuer must be a non-empty string")
        if not isinstance(self.subject, str) or not self.subject:
            raise ValueError("AuthorityToken subject must be a non-empty string")
        if not isinstance(self.scope, str) or not self.scope:
            raise ValueError("AuthorityToken scope must be a non-empty string")
        if not isinstance(self.is_valid, bool):
            raise TypeError("AuthorityToken is_valid must be a bool")
        if not isinstance(self.signature_hash, str) or not self.signature_hash:
            raise ValueError("AuthorityToken signature_hash must be a non-empty string")


# ---------------------------------------------------------------------------
# Master Normal Form: Terminal Partition & Outcome Types
# ---------------------------------------------------------------------------


class TerminalKind(str, Enum):
    AUTHORIZED = "T_auth"
    CLOSED_RESIDUAL = "T_res"
    REFUSED = "F_term"


@dataclass(frozen=True)
class TerminalOutcome:
    r"""
    Disjoint terminal outcome in T_auth \sqcup T_res \sqcup F_term.
    Booleans are derived directly from the single source of truth: `kind`.
    Uncomputed distances are None rather than fabricated sentinel values.
    """

    kind: TerminalKind
    payload_id: str
    phi1_distance: Optional[Rational] = None
    gamma2_distance: Optional[Rational] = None
    refusal_reason: Optional[str] = None
    dual_witness: Optional[Tuple[Rational, ...]] = None
    authority_token: Optional[AuthorityToken] = None

    @property
    def is_authorized(self) -> bool:
        return self.kind == TerminalKind.AUTHORIZED

    @property
    def is_anomalon(self) -> bool:
        return self.kind == TerminalKind.CLOSED_RESIDUAL

    @property
    def is_refused(self) -> bool:
        return self.kind == TerminalKind.REFUSED

    def __post_init__(self) -> None:
        # Exactness checks on distances if present
        if self.phi1_distance is not None:
            phi1 = _validate_exact_rational(self.phi1_distance, "phi1_distance")
            if phi1 < Rational(0, 1):
                raise ValueError("phi1_distance must be non-negative")
        if self.gamma2_distance is not None:
            gamma2 = _validate_exact_rational(self.gamma2_distance, "gamma2_distance")
            if gamma2 < Rational(0, 1):
                raise ValueError("gamma2_distance must be non-negative")

        # Semantic conditions per branch
        if self.kind == TerminalKind.AUTHORIZED:
            if self.phi1_distance != Rational(0, 1) or self.gamma2_distance != Rational(0, 1):
                raise ValueError("TerminalKind.AUTHORIZED strictly requires phi1=0 and gamma2=0")
            if self.authority_token is None or not self.authority_token.is_valid:
                raise ValueError("TerminalKind.AUTHORIZED strictly requires a valid AuthorityToken")
            if self.refusal_reason is not None:
                raise ValueError("TerminalKind.AUTHORIZED cannot carry a refusal reason")
        elif self.kind == TerminalKind.CLOSED_RESIDUAL:
            if self.phi1_distance is None or self.phi1_distance <= Rational(0, 1):
                raise ValueError("TerminalKind.CLOSED_RESIDUAL strictly requires phi1 > 0")
            if self.gamma2_distance != Rational(0, 1):
                raise ValueError("TerminalKind.CLOSED_RESIDUAL strictly requires gamma2 = 0")
            if not self.dual_witness or len(self.dual_witness) == 0:
                raise ValueError(
                    "TerminalKind.CLOSED_RESIDUAL strictly requires a verified dual witness"
                )
        elif self.kind == TerminalKind.REFUSED:
            if self.refusal_reason is None:
                raise ValueError("TerminalKind.REFUSED strictly requires a refusal reason")


@dataclass(frozen=True)
class ProblemInstance:
    """
    Input problem instance to the Master Normal Form pipeline.
    Validates shapes, cochain complex condition (d1 * d0 = 0), and strict exactness.
    """

    problem_id: str
    raw_data: str
    candidate_sieve: Tuple[str, ...]
    coarse_profile: Tuple[int, ...]
    fine_profile: Tuple[int, ...]
    projection_map: Mapping[int, int]
    local_sections: Mapping[str, Tuple[Rational, ...]]
    overlaps: Mapping[Tuple[str, str], bool]
    d0: Matrix
    d1: Optional[Matrix]
    defect_cochain: Matrix
    fda_license_granted: bool = False
    authority_token: Optional[AuthorityToken] = None
    cover: Optional[Mapping[str, Tuple[int, ...]]] = None

    def __post_init__(self) -> None:
        if not isinstance(self.problem_id, str) or not self.problem_id:
            raise ValueError("problem_id must be a non-empty string")

        # 1. Defect cochain validation: strictly 1 column
        if not isinstance(self.defect_cochain, MatrixBase):
            raise TypeError("defect_cochain must be a SymPy Matrix")
        if self.defect_cochain.cols != 1:
            raise ValueError(
                f"defect_cochain must have exactly 1 column, got {self.defect_cochain.cols}"
            )
        defect = _validate_matrix_exactness(self.defect_cochain, "defect_cochain")
        object.__setattr__(self, "defect_cochain", ImmutableMatrix(defect))

        # 2. d0 validation: rows must match defect rows
        if not isinstance(self.d0, MatrixBase):
            raise TypeError("d0 must be a SymPy Matrix")
        d0_mat = _validate_matrix_exactness(self.d0, "d0")
        if d0_mat.rows != defect.rows:
            raise ValueError(f"d0 rows ({d0_mat.rows}) must match defect rows ({defect.rows})")
        object.__setattr__(self, "d0", ImmutableMatrix(d0_mat))

        # 3. d1 validation: cols must match defect rows, and d1 * d0 == 0
        if self.d1 is not None:
            if not isinstance(self.d1, MatrixBase):
                raise TypeError("d1 must be a SymPy Matrix")
            d1_mat = _validate_matrix_exactness(self.d1, "d1")
            if d1_mat.cols != defect.rows:
                raise ValueError(f"d1 cols ({d1_mat.cols}) must match defect rows ({defect.rows})")
            # Cochain complex condition: d1 * d0 == 0
            d1_d0 = d1_mat * d0_mat
            if not all(
                simplify(d1_d0[r, c]) == 0 for r in range(d1_d0.rows) for c in range(d1_d0.cols)
            ):
                raise ValueError("Cochain complex condition failed: d1 * d0 != 0")
            object.__setattr__(self, "d1", ImmutableMatrix(d1_mat))

        if not isinstance(self.raw_data, str):
            raise TypeError("raw_data must be a string")
        if not isinstance(self.fda_license_granted, bool):
            raise TypeError("fda_license_granted must be a bool")
        if len(self.coarse_profile) != len(self.fine_profile):
            raise ValueError("coarse_profile and fine_profile must have equal lengths")
        object.__setattr__(
            self,
            "coarse_profile",
            tuple(_validate_exact_int(v, "coarse_profile") for v in self.coarse_profile),
        )
        object.__setattr__(
            self,
            "fine_profile",
            tuple(_validate_exact_int(v, "fine_profile") for v in self.fine_profile),
        )
        object.__setattr__(
            self,
            "projection_map",
            MappingProxyType(
                {
                    _validate_exact_int(k, "projection key"): _validate_exact_int(
                        v, "projection value"
                    )
                    for k, v in self.projection_map.items()
                }
            ),
        )
        object.__setattr__(
            self,
            "local_sections",
            MappingProxyType(
                {
                    name: tuple(_validate_exact_rational(v, f"local_sections[{name}]") for v in sec)
                    for name, sec in self.local_sections.items()
                }
            ),
        )
        if any(not isinstance(flag, bool) for flag in self.overlaps.values()):
            raise TypeError("overlap flags must be bool")
        if any(not isinstance(pair, tuple) or len(pair) != 2 for pair in self.overlaps):
            raise ValueError("overlap keys must be pairs of chart names")
        object.__setattr__(self, "overlaps", MappingProxyType(dict(self.overlaps)))
        object.__setattr__(self, "candidate_sieve", tuple(self.candidate_sieve))
        if self.cover is not None:
            cover = {
                name: tuple(_validate_exact_int(x, "cover coordinate") for x in domain)
                for name, domain in self.cover.items()
            }
            if any(len(set(domain)) != len(domain) for domain in cover.values()):
                raise ValueError("cover chart coordinates must be distinct")
            object.__setattr__(self, "cover", MappingProxyType(cover))
        if self.authority_token is not None and not isinstance(
            self.authority_token, AuthorityToken
        ):
            raise TypeError("authority_token must be an AuthorityToken")
        if self.authority_token is None and self.fda_license_granted:
            # Backward-compatible model flag; this creates no verified signature.
            object.__setattr__(
                self,
                "authority_token",
                AuthorityToken(
                    token_id=f"model_flag_{self.problem_id}",
                    issuer="DECLARED_MODEL_FLAG",
                    subject=self.problem_id,
                    scope="STANDARD_EVALUATION",
                    is_valid=True,
                    signature_hash="UNAUTHENTICATED_MODEL_RECORD",
                ),
            )


# ---------------------------------------------------------------------------
# Dual Witness Mechanical Certification Helper
# ---------------------------------------------------------------------------


def validate_dual_witness(
    d0: Matrix,
    defect: Matrix,
    dual_witness: Sequence[Any],
    phi1: Rational,
) -> bool:
    """
    Mechanically validate that a dual witness vector y satisfies all 3 required conditions:
    1. Annihilator condition: d0^T * y = 0
    2. Dual norm bound: ||y||_infty <= 1
    3. Objective equality: <y, defect> = y^T * defect = Phi_1
    """
    if len(dual_witness) != d0.rows:
        return False

    y = Matrix(
        d0.rows,
        1,
        [_validate_exact_rational(w, f"witness[{idx}]") for idx, w in enumerate(dual_witness)],
    )

    # 1. Annihilator condition: d0^T * y == 0
    d0_t_y = d0.T * y
    if not all(simplify(d0_t_y[r, 0]) == 0 for r in range(d0_t_y.rows)):
        return False

    # 2. Dual norm bound: ||y||_infty <= 1
    if any(bool(Abs(y[r, 0]) > 1) for r in range(y.rows)):
        return False

    # 3. Objective equality: y^T * defect == phi1
    pairing = (y.T * defect)[0, 0]
    if simplify(pairing - phi1) != 0:
        return False

    return True


# ---------------------------------------------------------------------------
# The Five Constituent Functors of the Master Normal Form
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RSharpOutput:
    """Output of Reduction & Refusal Functor (R^sharp, Layer 3: OR)."""

    is_refused: bool
    active_complex: Optional[str] = None
    refusal_reason: Optional[str] = None


def functor_r_sharp(problem: ProblemInstance) -> RSharpOutput:
    """
    2.1 The Reduction and Refusal Functor (R^sharp).
    Filters input request; evaluates candidate repair sieve. Emits refusal if empty.
    """
    if len(problem.candidate_sieve) == 0:
        return RSharpOutput(
            is_refused=True, refusal_reason="Candidate repair sieve empty (R_empty)"
        )
    return RSharpOutput(is_refused=False, active_complex=f"ActiveComplex_{problem.problem_id}")


@dataclass(frozen=True)
class RhoSharpOutput:
    """Output of Representation Functor (rho^sharp, Layer 4: CS / 4Q: CS-Q)."""

    cochain_delta_b: Matrix
    refinement_consistent: bool


def functor_rho_sharp(problem: ProblemInstance, r_out: RSharpOutput) -> RhoSharpOutput:
    """
    2.2 The Representation Functor (rho^sharp).
    Projects active configurations through observation fibers.
    Checks p_coarse = pi o p_fine consistency and extracts cochain delta_b.
    """
    if r_out.is_refused:
        raise ValueError("Cannot apply rho^sharp to a refused state")

    consistent = True
    for c_val, f_val in zip(problem.coarse_profile, problem.fine_profile):
        if problem.projection_map.get(f_val) != c_val:
            consistent = False
            break

    return RhoSharpOutput(
        cochain_delta_b=problem.defect_cochain,
        refinement_consistent=consistent,
    )


@dataclass(frozen=True)
class DSharpOutput:
    """Output of Descent Functor (D^sharp, Layer 1: FDA)."""

    gluing_succeeded: bool
    descent_cocycle_zero: bool
    global_section: Optional[Tuple[Rational, ...]] = None
    global_domain: Optional[Tuple[int, ...]] = None


def functor_d_sharp(problem: ProblemInstance, rho_out: RhoSharpOutput) -> DSharpOutput:
    """Glue finite coordinate sections by checking every shared coordinate.

    An omitted overlap flag never suppresses an actual intersection. Without
    cover data, tuple indices are the declared common coordinate domain.
    Explicit false flags veto gluing, but true flags cannot prove agreement.
    """
    failure = DSharpOutput(gluing_succeeded=False, descent_cocycle_zero=False)
    if not rho_out.refinement_consistent or not problem.local_sections:
        return failure
    if any(not sec for sec in problem.local_sections.values()):
        return failure
    cover = (
        problem.cover
        if problem.cover is not None
        else {name: tuple(range(len(sec))) for name, sec in problem.local_sections.items()}
    )
    if set(cover) != set(problem.local_sections):
        return failure
    for (left, right), flag in problem.overlaps.items():
        if not flag or left not in cover or right not in cover:
            return failure
    assembled: Dict[int, Rational] = {}
    for name, section in problem.local_sections.items():
        domain = cover[name]
        if len(domain) != len(section):
            return failure
        for point, value in zip(domain, section):
            if point in assembled and assembled[point] != value:
                return failure
            assembled[point] = value
    domain = tuple(sorted(assembled))
    return DSharpOutput(
        gluing_succeeded=True,
        descent_cocycle_zero=True,
        global_section=tuple(assembled[point] for point in domain),
        global_domain=domain,
    )


@dataclass(frozen=True)
class FocSharpOutput:
    """Output of Finite Obstruction Calculus Functor (FOC^sharp, Layer 0: FOC)."""

    phi1_distance: Rational
    gamma2_distance: Rational
    is_exact_repair: bool
    is_coherent_residual: bool
    is_nonclosed_defect: bool
    dual_witness: Optional[Tuple[Rational, ...]] = None


def functor_foc_sharp(problem: ProblemInstance, d_out: DSharpOutput) -> FocSharpOutput:
    """
    2.4 The Finite Obstruction Calculus Functor (FOC^sharp).
    Uses canonical LinearRepairProblem to compute exact rational quotient distances:
    Phi_1([delta_b]) = min_{f} ||delta_b + d0 f||_1,
    Gamma_2([d1 delta_b]) = ||d1 delta_b||_1.
    Dual witnesses are mechanically validated against annihilator, norm, and pairing conditions.
    """
    if not d_out.gluing_succeeded:
        raise ValueError("FOC stage requires successful gluing; distances are uncomputed")

    # 1. Stage-2 check Gamma_2 across the entire column vector
    gamma2 = Rational(0, 1)
    if problem.d1 is not None and problem.d1.rows > 0:
        d1_defect = problem.d1 * problem.defect_cochain
        if not d1_defect.is_zero_matrix:
            gamma2 = sum(
                Abs(_validate_exact_rational(d1_defect[i, 0], f"d1_defect[{i}]"))
                for i in range(d1_defect.rows)
            )

    # 2. Stage-1 quotient LP via canonical LinearRepairProblem
    solver = LinearRepairProblem(repair_map_d0=problem.d0)
    cert: QuotientDistanceCertificate = solver.quotient_l1_distance(cochain=problem.defect_cochain)
    phi1 = Rational(cert.distance)

    if gamma2 > 0:
        return FocSharpOutput(
            phi1_distance=phi1,
            gamma2_distance=gamma2,
            is_exact_repair=False,
            is_coherent_residual=False,
            is_nonclosed_defect=True,
            dual_witness=tuple(cert.dual_witness),
        )

    if phi1 == Rational(0, 1):
        return FocSharpOutput(
            phi1_distance=Rational(0, 1),
            gamma2_distance=Rational(0, 1),
            is_exact_repair=True,
            is_coherent_residual=False,
            is_nonclosed_defect=False,
            dual_witness=None,
        )

    # Distance > 0: Extract and mechanically validate the dual witness
    witness_list: List[Rational] = [
        _validate_exact_rational(cert.dual_witness[i, 0], f"witness[{i}]")
        for i in range(cert.dual_witness.rows)
    ]

    is_valid = validate_dual_witness(
        d0=problem.d0,
        defect=problem.defect_cochain,
        dual_witness=witness_list,
        phi1=phi1,
    )
    if not is_valid:
        raise ArithmeticError("Solver returned dual witness that failed mechanical validation")

    return FocSharpOutput(
        phi1_distance=phi1,
        gamma2_distance=Rational(0, 1),
        is_exact_repair=False,
        is_coherent_residual=True,
        is_nonclosed_defect=False,
        dual_witness=tuple(witness_list),
    )


def functor_tau_sharp(
    problem: ProblemInstance,
    r_out: RSharpOutput,
    d_out: DSharpOutput,
    foc_out: Optional[FocSharpOutput],
) -> TerminalOutcome:
    r"""
    2.5 The Terminalization and Transport Functor (tau^sharp).
    Evaluates FDA standing soundness and Layer 5 residual closure.
    Strictly preserves the disjoint terminal partition:
    T_auth \sqcup T_res \sqcup F_term.
    """
    expected_r = functor_r_sharp(problem)
    expected_d = None
    if not expected_r.is_refused:
        expected_d = functor_d_sharp(problem, functor_rho_sharp(problem, expected_r))
    if r_out != expected_r or (expected_d is not None and d_out != expected_d):
        return TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id=f"invalid_stage_{problem.problem_id}",
            refusal_reason="Stage evidence does not match the supplied problem",
        )
    # 1. Check early refusal from R^sharp (M3: do not invent evidence values)
    if r_out.is_refused:
        return TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id=f"term_{problem.problem_id}",
            phi1_distance=None,
            gamma2_distance=None,
            refusal_reason=r_out.refusal_reason or "Refused at R^sharp",
        )

    # 2. Check descent gluing failure (M3: do not invent evidence values)
    if not d_out.gluing_succeeded:
        return TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id=f"term_{problem.problem_id}",
            phi1_distance=None,
            gamma2_distance=None,
            refusal_reason="Descent gluing failure across covers",
        )

    if foc_out is None:
        return TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id=f"term_{problem.problem_id}",
            phi1_distance=None,
            gamma2_distance=None,
            refusal_reason="FOC stage not executed",
        )

    if foc_out != functor_foc_sharp(problem, d_out):
        return TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id=f"invalid_foc_{problem.problem_id}",
            refusal_reason="FOC evidence does not match the supplied problem",
        )

    # 3. Check nonclosed higher defect
    if foc_out.is_nonclosed_defect:
        return TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id=f"term_{problem.problem_id}",
            phi1_distance=foc_out.phi1_distance,
            gamma2_distance=foc_out.gamma2_distance,
            refusal_reason="Nonclosed higher coboundary defect (Gamma_2 > 0)",
        )

    # 4. Exact repair uses the declared, matching model licence.
    if foc_out.is_exact_repair:
        if (
            problem.authority_token is not None
            and problem.authority_token.is_valid
            and problem.authority_token.subject == problem.problem_id
            and problem.authority_token.scope == "STANDARD_EVALUATION"
        ):
            return TerminalOutcome(
                kind=TerminalKind.AUTHORIZED,
                payload_id=f"auth_{problem.problem_id}",
                phi1_distance=Rational(0, 1),
                gamma2_distance=Rational(0, 1),
                refusal_reason=None,
                authority_token=problem.authority_token,
            )
        else:
            # Strict non-promotion: zero residual WITHOUT authority license routes to refusal
            return TerminalOutcome(
                kind=TerminalKind.REFUSED,
                payload_id=f"refused_unauthorized_{problem.problem_id}",
                phi1_distance=Rational(0, 1),
                gamma2_distance=Rational(0, 1),
                refusal_reason="Non-promotion firewall: Phi_1=0 does not entail authority without valid authority grant",
            )

    # 5. Coherent residual -> T_res (Anomalon terminal)
    if foc_out.is_coherent_residual:
        return TerminalOutcome(
            kind=TerminalKind.CLOSED_RESIDUAL,
            payload_id=f"anomalon_{problem.problem_id}",
            phi1_distance=foc_out.phi1_distance,
            gamma2_distance=Rational(0, 1),
            refusal_reason=None,
            dual_witness=foc_out.dual_witness,
        )

    # Fallback refusal
    return TerminalOutcome(
        kind=TerminalKind.REFUSED,
        payload_id=f"term_fallback_{problem.problem_id}",
        phi1_distance=foc_out.phi1_distance,
        gamma2_distance=foc_out.gamma2_distance,
        refusal_reason="Unclassified terminal condition",
    )


# ---------------------------------------------------------------------------
# The Master Normal Form Pipeline (\Pi^\sharp) & Cryptographic Result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PipelineResult:
    """
    Execution result of the Master Normal Form pipeline.
    Carries deterministic SHA-256 cryptographic digest over all constituent stages.
    """

    problem: ProblemInstance
    pipeline_id: str
    r_stage: RSharpOutput
    rho_stage: Optional[RhoSharpOutput]
    d_stage: Optional[DSharpOutput]
    foc_stage: Optional[FocSharpOutput]
    terminal_outcome: TerminalOutcome

    def is_authorized(self) -> bool:
        return self.terminal_outcome.is_authorized

    def is_anomalon(self) -> bool:
        return self.terminal_outcome.is_anomalon

    def is_refused(self) -> bool:
        return self.terminal_outcome.is_refused

    def sha256_digest(self) -> str:
        """Bind all input and stage fields; this digest is not an authentication token."""
        return _record_digest({"schema": "gtla-pipeline-v2", "result": self})


# Backwards compatibility alias
MasterNormalFormReceipt = PipelineResult


def execute_master_normal_form(problem: ProblemInstance) -> PipelineResult:
    """
    Executes the Master Normal Form pipeline:
    Pi^sharp = tau^sharp circ_k FOC^sharp circ_k D^sharp circ_k rho^sharp circ_k R^sharp
    """
    # 1. R^sharp
    r_out = functor_r_sharp(problem)
    if r_out.is_refused:
        term = functor_tau_sharp(
            problem,
            r_out,
            DSharpOutput(gluing_succeeded=False, descent_cocycle_zero=False),
            None,
        )
        return PipelineResult(
            problem=problem,
            pipeline_id=f"mnf_{problem.problem_id}",
            r_stage=r_out,
            rho_stage=None,
            d_stage=None,
            foc_stage=None,
            terminal_outcome=term,
        )

    # 2. rho^sharp
    rho_out = functor_rho_sharp(problem, r_out)

    # 3. D^sharp
    d_out = functor_d_sharp(problem, rho_out)
    if not d_out.gluing_succeeded:
        term = functor_tau_sharp(problem, r_out, d_out, None)
        return PipelineResult(
            problem=problem,
            pipeline_id=f"mnf_{problem.problem_id}",
            r_stage=r_out,
            rho_stage=rho_out,
            d_stage=d_out,
            foc_stage=None,
            terminal_outcome=term,
        )

    # 4. FOC^sharp
    foc_out = functor_foc_sharp(problem, d_out)

    # 5. tau^sharp
    term_out = functor_tau_sharp(problem, r_out, d_out, foc_out)

    return PipelineResult(
        problem=problem,
        pipeline_id=f"mnf_{problem.problem_id}",
        r_stage=r_out,
        rho_stage=rho_out,
        d_stage=d_out,
        foc_stage=foc_out,
        terminal_outcome=term_out,
    )


# ---------------------------------------------------------------------------
# Strict Non-Promotion Authority Firewall & Countermodels (GTLA-02, FDA-04)
# ---------------------------------------------------------------------------


def evaluate_authority_firewall(receipt: PipelineResult) -> Dict[str, Any]:
    """
    Checks the declared finite evaluator and its non-promotion rule:
    [delta_b] in Q^1_b -/-> Auth_L(x; q).
    Obstruction evidence, dual witnesses, and zero-residual certificates
    do not entail authorization standing.

    Verifies semantic consistency: An outcome claiming authorization but
    carrying nonzero distances or mismatching declared model licence data
    violates the firewall!
    """
    term = receipt.terminal_outcome
    evidence_zero = receipt.foc_stage is not None and receipt.foc_stage.phi1_distance == Rational(
        0, 1
    )

    # Semantic branch validation
    semantic_valid = receipt == execute_master_normal_form(receipt.problem)
    if term.is_authorized:
        if (
            term.phi1_distance != Rational(0, 1)
            or term.gamma2_distance != Rational(0, 1)
            or term.authority_token is None
            or not term.authority_token.is_valid
        ):
            semantic_valid = False

    firewall_intact = (
        not (term.is_anomalon and term.is_authorized)
        and not (term.is_refused and term.is_authorized)
        and semantic_valid
    )

    disjoint_partition_holds = (
        (term.is_authorized and not term.is_anomalon and not term.is_refused)
        or (term.is_anomalon and not term.is_authorized and not term.is_refused)
        or (term.is_refused and not term.is_authorized and not term.is_anomalon)
    ) and semantic_valid

    return {
        "pipeline_id": receipt.pipeline_id,
        "evidence_zero_residual": evidence_zero,
        "is_authorized": term.is_authorized,
        "is_anomalon": term.is_anomalon,
        "is_refused": term.is_refused,
        "firewall_intact": firewall_intact,
        "disjoint_partition_holds": disjoint_partition_holds,
        "sha256_digest": receipt.sha256_digest(),
        "authority_effect": "None",
    }


def untrusted_verifier_countermodel() -> Dict[str, Any]:
    """
    Countermodel 1 to self-justifying records (FDA-04):
    An unsound verifier reports valid=True on an invalid state.
    Authority firewall prevents self-authorization.
    """
    d0 = Matrix([[1], [1]])
    defect = Matrix([[0], [0]])  # Phi_1 = 0
    problem = ProblemInstance(
        problem_id="countermodel_untrusted",
        raw_data="untrusted_payload",
        candidate_sieve=("repair_1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=None,
        defect_cochain=defect,
        fda_license_granted=False,
    )
    receipt = execute_master_normal_form(problem)
    return {
        "verifier_claimed_valid": True,
        "phi1": receipt.foc_stage.phi1_distance if receipt.foc_stage else None,
        "is_authorized": receipt.is_authorized(),
        "is_refused": receipt.is_refused(),
        "firewall_blocked_unauthorized": receipt.is_refused() and not receipt.is_authorized(),
    }


def observation_collision_countermodel() -> Dict[str, Any]:
    """
    Countermodel 2 to observation-as-authority (FDA-04, CSQ-03):
    Two distinct states s1, s2 produce identical observational profiles
    and identical cochain data, but carry different declared model licence flags.
    """
    d0 = Matrix([[1], [1]])
    defect = Matrix([[0], [0]])

    p1 = ProblemInstance(
        problem_id="state_s1_licensed",
        raw_data="sovereign_granted",
        candidate_sieve=("repair_1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=None,
        defect_cochain=defect,
        fda_license_granted=True,
    )

    p2 = ProblemInstance(
        problem_id="state_s2_unlicensed",
        raw_data="no_grant",
        candidate_sieve=("repair_1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=None,
        defect_cochain=defect,
        fda_license_granted=False,
    )

    r1 = execute_master_normal_form(p1)
    r2 = execute_master_normal_form(p2)

    return {
        "observation_identical": (
            r1.foc_stage is not None
            and r2.foc_stage is not None
            and r1.foc_stage.phi1_distance == r2.foc_stage.phi1_distance
        ),
        "s1_authorized": r1.is_authorized(),
        "s2_authorized": r2.is_authorized(),
        "authority_separated": r1.is_authorized() != r2.is_authorized(),
    }


# ---------------------------------------------------------------------------
# GTLA-03: Two-Rule Core Loop Implementation
# ---------------------------------------------------------------------------


def execute_two_rule_repair_loop(problem: ProblemInstance) -> Dict[str, Any]:
    """
    Report a finite repair witness or positive quotient residual.

    Historical function name retained for compatibility. No extension is
    constructed and no set of tied minimizers is enumerated. ties_retained=None
    explicitly records that the tie-retention obligation was not evaluated.
    """
    solver = LinearRepairProblem(repair_map_d0=problem.d0)
    cert = solver.quotient_l1_distance(cochain=problem.defect_cochain)
    phi1 = Rational(cert.distance)

    if phi1 == Rational(0, 1):
        return {
            "rule_applied": "Rule 1: Same-Grain Repair",
            "phi1": phi1,
            "repair_witness": [
                str(cert.repair_witness[r, 0]) for r in range(cert.repair_witness.rows)
            ],
            "ties_retained": None,
            "extension_constructed": False,
        }
    else:
        witness_list = [str(cert.dual_witness[r, 0]) for r in range(cert.dual_witness.rows)]
        return {
            "rule_applied": "Positive residual: extension remains open",
            "phi1": phi1,
            "dual_witness": witness_list,
            "ties_retained": None,
            "extension_constructed": False,
        }


# ---------------------------------------------------------------------------
# End-to-End Reproducible Example
# ---------------------------------------------------------------------------


def reproduce_master_normal_form_example() -> Dict[str, Any]:
    """
    Executes an end-to-end trace of the Master Normal Form across three
    distinct problem cases:
    1. Authorized Exact Repair (T_auth)
    2. Closed Residual Survivor / Anomalon (T_res)
    3. Empty Sieve Refusal (F_term)
    """
    d0 = Matrix([[1], [-1]])
    d1 = Matrix([[1, 1]])

    # Case 1: Exact repair with license
    p_auth = ProblemInstance(
        problem_id="demo_auth",
        raw_data="data_auth",
        candidate_sieve=("candidate_1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [-1]]),  # in im(d0)
        fda_license_granted=True,
    )
    rec_auth = execute_master_normal_form(p_auth)

    # Case 2: Anomalon closed residual (survivor)
    d0_res = Matrix([[0], [0]])
    d1_res = Matrix([[0, 0]])
    p_res = ProblemInstance(
        problem_id="demo_anomalon",
        raw_data="data_anomalon",
        candidate_sieve=("candidate_1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0_res,
        d1=d1_res,
        defect_cochain=Matrix([[1], [1]]),  # Phi_1 = 2, Gamma_2 = 0
        fda_license_granted=False,
    )
    rec_res = execute_master_normal_form(p_res)

    # Case 3: Refusal due to empty candidate sieve
    p_ref = ProblemInstance(
        problem_id="demo_refusal",
        raw_data="data_refusal",
        candidate_sieve=(),
        coarse_profile=(0,),
        fine_profile=(0,),
        projection_map={0: 0},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=False,
    )
    rec_ref = execute_master_normal_form(p_ref)

    return {
        "case_1_auth": {
            "kind": rec_auth.terminal_outcome.kind.value,
            "is_authorized": rec_auth.is_authorized(),
            "phi1": str(rec_auth.terminal_outcome.phi1_distance),
        },
        "case_2_anomalon": {
            "kind": rec_res.terminal_outcome.kind.value,
            "is_anomalon": rec_res.is_anomalon(),
            "phi1": str(rec_res.terminal_outcome.phi1_distance),
            "dual_witness": [str(w) for w in (rec_res.terminal_outcome.dual_witness or ())],
        },
        "case_3_refusal": {
            "kind": rec_ref.terminal_outcome.kind.value,
            "is_refused": rec_ref.is_refused(),
            "reason": rec_ref.terminal_outcome.refusal_reason,
        },
        "partition_disjoint": (
            rec_auth.is_authorized() and rec_res.is_anomalon() and rec_ref.is_refused()
        ),
        "authority_effect": "None",
    }


# ==============================================================================
# 11. 2-NERVE SPECTRAL SEQUENCE AND LP DUAL WITNESS CERTIFIER
# ==============================================================================


@dataclass(frozen=True)
class Bicomplex2Nerve:
    r"""
    Exact rational bicomplex (double complex) of a 2-truncated nerve C^{p,q}.

    Grading:
      p in {0, 1, 2}: simplicial nerve filtration degree (vertices, edges, triangles).
      q in {0, 1}: local fiber cochain degree (0-cochains, 1-cochains).

    Differentials:
      d_h^{p,q}: C^{p,q} -> C^{p+1,q} for p in {0, 1}, q in {0, 1}
      d_v^{p,0}: C^{p,0} -> C^{p,1}   for p in {0, 1, 2}

    Bicomplex Anticommutation Axioms:
      d_h^{1,q} * d_h^{0,q} = 0 for q in {0, 1}
      d_h^{p,1} * d_v^{p,0} + d_v^{p+1,0} * d_h^{p,0} = 0 for p in {0, 1}

    Higher Differential d_2: E_2^{0,1} -> E_2^{2,0}:
      Maps a local 1-cocycle omega in C^{0,1} across the zig-zag
      d_v^{1,0} eta = -d_h^{0,1} omega  =>  d_2 omega = d_h^{1,0} eta in C^{2,0}.

    AuthorityEffect: None.
    """

    dh_00: Matrix
    dh_01: Matrix
    dh_10: Matrix
    dh_11: Matrix
    dv_00: Matrix
    dv_10: Matrix
    dv_20: Matrix

    def __post_init__(self) -> None:
        object.__setattr__(self, "dh_00", ImmutableMatrix(exact_matrix_from_matrix(self.dh_00)))
        object.__setattr__(self, "dh_01", ImmutableMatrix(exact_matrix_from_matrix(self.dh_01)))
        object.__setattr__(self, "dh_10", ImmutableMatrix(exact_matrix_from_matrix(self.dh_10)))
        object.__setattr__(self, "dh_11", ImmutableMatrix(exact_matrix_from_matrix(self.dh_11)))
        object.__setattr__(self, "dv_00", ImmutableMatrix(exact_matrix_from_matrix(self.dv_00)))
        object.__setattr__(self, "dv_10", ImmutableMatrix(exact_matrix_from_matrix(self.dv_10)))
        object.__setattr__(self, "dv_20", ImmutableMatrix(exact_matrix_from_matrix(self.dv_20)))
        self.validate()

    def validate(self) -> bool:
        """Verify bicomplex horizontal composition and anticommutation identities."""
        # 1. Horizontal square zero
        if self.dh_10 * self.dh_00 != Matrix.zeros(self.dh_10.rows, self.dh_00.cols):
            raise ArithmeticError("dh_10 * dh_00 != 0")
        if self.dh_11 * self.dh_01 != Matrix.zeros(self.dh_11.rows, self.dh_01.cols):
            raise ArithmeticError("dh_11 * dh_01 != 0")

        # 2. Anticommutation identities: dh * dv + dv * dh == 0
        anticomm_0 = self.dh_01 * self.dv_00 + self.dv_10 * self.dh_00
        if anticomm_0 != Matrix.zeros(self.dh_01.rows, self.dh_00.cols):
            raise ArithmeticError(
                "Bicomplex anticommutation failed at p=0: dh_01 * dv_00 + dv_10 * dh_00 != 0"
            )

        anticomm_1 = self.dh_11 * self.dv_10 + self.dv_20 * self.dh_10
        if anticomm_1 != Matrix.zeros(self.dh_11.rows, self.dh_10.cols):
            raise ArithmeticError(
                "Bicomplex anticommutation failed at p=1: dh_11 * dv_10 + dv_20 * dh_10 != 0"
            )

        return True

    def total_complex_d0(self) -> Matrix:
        r"""Total differential D_0: Tot^0 -> Tot^1, Tot^0 = C^{0,0}, Tot^1 = C^{1,0} \oplus C^{0,1}."""
        return Matrix.vstack(self.dh_00, self.dv_00)

    def total_complex_d1(self) -> Matrix:
        r"""
        Total differential D_1: Tot^1 -> Tot^2.
        Tot^1 = C^{1,0} \oplus C^{0,1}
        Tot^2 = C^{2,0} \oplus C^{1,1}
        D_1 = [[dh_10, 0], [dv_10, dh_01]]
        """
        top_zero = Matrix.zeros(self.dh_10.rows, self.dh_01.cols)
        row0 = Matrix.hstack(self.dh_10, top_zero)
        row1 = Matrix.hstack(self.dv_10, self.dh_01)
        d1 = Matrix.vstack(row0, row1)

        # Re-verify D_1 * D_0 == 0
        d0 = self.total_complex_d0()
        if d1 * d0 != Matrix.zeros(d1.rows, d0.cols):
            raise ArithmeticError("Total complex differential failed D_1 * D_0 != 0")
        return d1

    def compute_d2_zigzag_obstruction(
        self,
        omega_01: Matrix,
        holonomy_flux: Optional[Matrix] = None,
    ) -> Tuple[Matrix, Matrix, Matrix]:
        r"""
        Computes the secondary differential d_2: E_2^{0,1} -> E_2^{2,0}.
        1. Solves dv_10 * eta = -dh_01 * omega_01 for eta in C^{1,0}.
        2. Optionally adds a checked holonomy_flux in ker(dv_10).
        3. Computes secondary obstruction d_2 omega = dh_10 * eta in C^{2,0}.
        4. Embeds into Tot^2 = C^{2,0} \oplus C^{1,1} as Omega_tot = [d_2 omega; 0].
        """
        omega = exact_matrix_from_matrix(omega_01)
        if omega.shape != (self.dh_01.cols, 1):
            raise ValueError(
                f"omega_01 shape {omega.shape} does not match C^{{0,1}} dimension {(self.dh_01.cols, 1)}"
            )

        rhs = -(self.dh_01 * omega)
        if self.dv_10.rank() != self.dv_10.row_join(rhs).rank():
            raise ArithmeticError("dh_01 * omega is not in im(dv_10); omega is not in ker(d_1)")

        solution, _ = self.dv_10.gauss_jordan_solve(rhs)
        subst = {symbol: Rational(0) for symbol in solution.free_symbols}
        eta = solution.subs(subst)

        if holonomy_flux is not None:
            flux = exact_matrix_from_matrix(holonomy_flux)
            if flux.shape != eta.shape:
                raise ValueError(
                    f"holonomy_flux shape {flux.shape} does not match C^{{1,0}} shape {eta.shape}"
                )
            if self.dv_10 * flux != Matrix.zeros(self.dv_10.rows, 1):
                raise ValueError("holonomy_flux must lie in ker(dv_10)")
            eta = eta + flux

        d2_omega = self.dh_10 * eta
        bot_zero = Matrix.zeros(self.dh_01.rows, 1)
        omega_tot = Matrix.vstack(d2_omega, bot_zero)

        return eta, d2_omega, omega_tot

    def certify_d2_quotient_bounds(
        self,
        omega_01: Matrix,
        holonomy_flux: Optional[Matrix] = None,
    ) -> QuotientDistanceCertificate:
        r"""Certify d2 in the finite target ker(dv_20) / dh_10(ker(dv_10)).

        The embedded total cochain is D1*[eta;omega], hence is always a total
        boundary. Its quotient by im(D1) cannot measure this E2 class.
        """
        _eta, d2_omega, _omega_tot = self.compute_d2_zigzag_obstruction(
            omega_01, holonomy_flux=holonomy_flux
        )
        return self.certify_e2_coboundary_bounds(d2_omega)

    def e2_page_boundary_d2(self) -> Matrix:
        r"""
        Returns the boundary matrix on the E_2^{2,0} page:
        B_2 = dh_10 * K, where K is a basis matrix for ker(dv_10).
        """
        nullspace = self.dv_10.nullspace()
        if not nullspace:
            return Matrix.zeros(self.dh_10.rows, 0)
        k_mat = Matrix.hstack(*nullspace)
        return self.dh_10 * k_mat

    def certify_e2_coboundary_bounds(self, cochain_20: Matrix) -> QuotientDistanceCertificate:
        r"""
        Solves and certifies the exact rational L1 quotient distance of a higher cochain
        in E_2^{2,0} with respect to the E_2 boundary matrix B_2 = dh_10 * K.
        """
        cochain = exact_matrix_from_matrix(cochain_20)
        if cochain.shape != (self.dv_20.cols, 1):
            raise ValueError("E2 representative must be a column in C^{2,0}")
        if self.dv_20 * cochain != Matrix.zeros(self.dv_20.rows, 1):
            raise ValueError("E2 representative must lie in ker(dv_20)")
        b2 = self.e2_page_boundary_d2()
        problem = LinearRepairProblem(b2)
        certificate = problem.quotient_l1_distance(cochain)
        if not certificate.verify():
            raise ArithmeticError("E2 page quotient certificate failed verification")
        return certificate

    @classmethod
    def build_canonical_2nerve(cls) -> Bicomplex2Nerve:
        r"""
        Constructs the canonical 3-cover nerve complex with local 2D fiber.
        Nerve: 3 vertices, 3 edges, 1 triangle.
        Fiber: V0 = Q^2, V1 = Q^1, with fiber differential [1, -1].
        """
        dh0 = Matrix([[-1, 1, 0], [0, -1, 1], [1, 0, -1]])
        dh1 = Matrix([[1, 1, 1]])
        v_fib = Matrix([[Rational(1), Rational(-1)]])

        i2 = Matrix.eye(2)

        # dh^{p,q} = dh^p (x) I_{fiber_q}
        dh_00 = Matrix.zeros(6, 6)
        for r in range(3):
            for c in range(3):
                dh_00[2 * r : 2 * r + 2, 2 * c : 2 * c + 2] = dh0[r, c] * i2

        dh_01 = dh0

        dh_10 = Matrix.zeros(2, 6)
        for c in range(3):
            dh_10[:, 2 * c : 2 * c + 2] = dh1[0, c] * i2

        dh_11 = dh1

        # dv^{p,0} = (-1)^p (I_{nerve_p} (x) v_fib)
        dv_00 = Matrix.zeros(3, 6)
        for r in range(3):
            dv_00[r, 2 * r : 2 * r + 2] = v_fib

        dv_10 = Matrix.zeros(3, 6)
        for r in range(3):
            dv_10[r, 2 * r : 2 * r + 2] = -v_fib

        dv_20 = v_fib

        return cls(
            dh_00=dh_00,
            dh_01=dh_01,
            dh_10=dh_10,
            dh_11=dh_11,
            dv_00=dv_00,
            dv_10=dv_10,
            dv_20=dv_20,
        )

    @staticmethod
    def compare_dimension_scaling(num_vertices: int, local_fiber_dim: int = 2) -> Dict[str, Any]:
        r"""
        Count faces through dimension two and in the full simplex.

        These counts do not prove that truncation preserves cohomology or
        that vertex-enumeration LP solving takes polynomial time.
        """
        num_vertices = _validate_exact_int(num_vertices, "num_vertices")
        local_fiber_dim = _validate_exact_int(local_fiber_dim, "local_fiber_dim")
        if local_fiber_dim < 1:
            raise ValueError("local_fiber_dim must be positive")
        if num_vertices < 3:
            raise ValueError("num_vertices must be at least 3")

        # Full combinatorial simplex faces: sum_{k=0}^{V-1} binom(V, k+1) = 2^V - 1
        full_simplex_faces = (1 << num_vertices) - 1

        # 2-nerve truncated to degree <= 2
        v_count = num_vertices
        e_count = num_vertices * (num_vertices - 1) // 2
        t_count = num_vertices * (num_vertices - 1) * (num_vertices - 2) // 6
        nerve_2_faces = v_count + e_count + t_count

        # Total complex D1 matrix rows and cols
        lp_matrix_rows = t_count * local_fiber_dim + e_count * 1
        lp_matrix_cols = e_count * local_fiber_dim + v_count * 1

        return {
            "num_vertices": num_vertices,
            "full_simplex_faces": full_simplex_faces,
            "2nerve_total_faces": nerve_2_faces,
            "compression_ratio": Rational(full_simplex_faces, nerve_2_faces),
            "lp_matrix_rows": lp_matrix_rows,
            "lp_matrix_cols": lp_matrix_cols,
            "truncated_face_count_smaller": bool(full_simplex_faces > nerve_2_faces),
            "authority_effect": "None",
        }
