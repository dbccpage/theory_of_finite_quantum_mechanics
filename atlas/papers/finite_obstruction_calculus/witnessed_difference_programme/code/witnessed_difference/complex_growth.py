"""Restriction, face attachment, and edge subdivision of weighted degree-1 windows.

Restricting an edge field and its weights to a subcomplex never raises Phi_1;
attaching 2-simplices leaves Phi_1 unchanged and can raise Gamma_2; replacing
an edge u -> v by u -> m -> v through a new degree-two vertex m, with the value
split into two summands and both halves carrying the old weight, leaves Phi_1
unchanged.  ``growth_receipt`` reports both certified signatures and refuses
nothing about their order: a change of carrier is reported, never read as a
repair.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Mapping, Sequence

from .cochains import Edge, Face, FiniteComplex, Vertex
from .exact import as_fraction
from .obstruction import (
    DiagnosticClass,
    ObstructionSignature,
    QuotientCertificate,
    _cochain_vector,
    edge_weights,
    obstruction_signature,
)
from .outcomes import Accepted, Outcome, RefusalCode, Refused

ExactScalar = int | str | Fraction


@dataclass(frozen=True)
class WeightedWindow:
    """A finite complex with an edge field and positive weights aligned with its edges."""

    complex_: FiniteComplex
    cochain: tuple[Fraction, ...]
    weights: tuple[Fraction, ...]

    def cochain_map(self) -> dict[Edge, Fraction]:
        return dict(zip(self.complex_.edges, self.cochain))

    def weight_map(self) -> dict[Edge, Fraction]:
        return dict(zip(self.complex_.edges, self.weights))


def make_window(
    complex_: FiniteComplex,
    cochain: Mapping[Edge, ExactScalar],
    weights: Mapping[Edge, ExactScalar] | None = None,
) -> Outcome[WeightedWindow]:
    """Admit an exact edge field and positive exact weights (default 1) on a finite complex."""

    if not isinstance(complex_, FiniteComplex):
        return Refused(RefusalCode.INVALID_INPUT, "a weighted window needs a finite complex")
    vector = _cochain_vector(complex_, cochain)
    if isinstance(vector, Refused):
        return vector
    admitted = edge_weights(complex_, weights)
    if isinstance(admitted, Refused):
        return admitted
    return Accepted(WeightedWindow(complex_, vector.value, admitted.value))


def _readmit(window: object) -> Outcome[WeightedWindow]:
    if not isinstance(window, WeightedWindow) or not isinstance(window.complex_, FiniteComplex):
        return Refused(RefusalCode.INVALID_INPUT, "a weighted window is required")
    edges = window.complex_.edges
    if len(window.cochain) != len(edges) or len(window.weights) != len(edges):
        return Refused(RefusalCode.INVALID_INPUT, "the window's field and weights are not aligned with its edges")
    return make_window(window.complex_, window.cochain_map(), window.weight_map())


def _subcomplex(vertices: object, edges: object, faces: object) -> Outcome[FiniteComplex]:
    try:
        return Accepted(FiniteComplex(vertices, edges, faces))  # type: ignore[arg-type]
    except (TypeError, ValueError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"not a finite complex: {error}")


def _within(items: tuple[object, ...], declared: tuple[object, ...]) -> bool:
    try:
        return set(items) <= set(declared)
    except TypeError:
        return False


def _new_face(face: object, faces: tuple[Face, ...]) -> bool:
    try:
        return type(face) is tuple and all(set(face) != set(existing) for existing in faces)
    except TypeError:
        return False


def restrict_complex(
    window: WeightedWindow,
    vertices: Sequence[Vertex],
    edges: Sequence[Edge],
    faces: Sequence[Face] = (),
) -> Outcome[WeightedWindow]:
    """Keep declared vertices, edges (same orientation), and faces with the restricted field and weights."""

    admitted = _readmit(window)
    if isinstance(admitted, Refused):
        return admitted
    big = admitted.value.complex_
    kept = (tuple(vertices), tuple(edges), tuple(faces))
    declared = (big.vertices, big.edges, big.faces)
    if not all(_within(items, pool) for items, pool in zip(kept, declared)):
        return Refused(RefusalCode.OUTSIDE_CARRIER, "a restriction keeps only declared vertices, edges, and faces")
    small = _subcomplex(*kept)
    if isinstance(small, Refused):
        return small
    field, weights = admitted.value.cochain_map(), admitted.value.weight_map()
    return Accepted(
        WeightedWindow(
            small.value,
            tuple(field[edge] for edge in small.value.edges),
            tuple(weights[edge] for edge in small.value.edges),
        )
    )


def attach_face(window: WeightedWindow, face: Face) -> Outcome[WeightedWindow]:
    """Attach one 2-simplex whose three boundary edges are already present."""

    admitted = _readmit(window)
    if isinstance(admitted, Refused):
        return admitted
    old = admitted.value
    if not _new_face(face, old.complex_.faces):
        return Refused(RefusalCode.INVALID_INPUT, f"{face!r} is not a new face tuple")
    grown = _subcomplex(old.complex_.vertices, old.complex_.edges, old.complex_.faces + (face,))
    if isinstance(grown, Refused):
        return grown
    return Accepted(WeightedWindow(grown.value, old.cochain, old.weights))


def subdivide_edge(
    window: WeightedWindow,
    edge: Edge,
    new_vertex: Hashable,
    first_value: ExactScalar,
) -> Outcome[WeightedWindow]:
    """Replace u -> v by u -> m -> v with values (x1, x - x1), each weighted w(u, v)."""

    admitted = _readmit(window)
    if isinstance(admitted, Refused):
        return admitted
    old = admitted.value
    edges = old.complex_.edges
    if edge not in edges:
        return Refused(RefusalCode.OUTSIDE_CARRIER, f"{edge!r} is not a declared edge in its declared orientation")
    if any(set(edge) <= set(face) for face in old.complex_.faces):
        return Refused(RefusalCode.INVALID_INPUT, f"{edge!r} bounds a declared face; subdivision would break it")
    if new_vertex in old.complex_.vertices:
        return Refused(RefusalCode.INVALID_INPUT, "the subdivision vertex must be new")
    try:
        first = as_fraction(first_value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"the split value must be exact: {error}")
    index = edges.index(edge)
    tail, head = edge
    new_edges = edges[:index] + ((tail, new_vertex), (new_vertex, head)) + edges[index + 1 :]
    grown = _subcomplex(old.complex_.vertices + (new_vertex,), new_edges, old.complex_.faces)
    if isinstance(grown, Refused):
        return grown
    value, weight = old.cochain[index], old.weights[index]
    return Accepted(
        WeightedWindow(
            grown.value,
            old.cochain[:index] + (first, value - first) + old.cochain[index + 1 :],
            old.weights[:index] + (weight, weight) + old.weights[index + 1 :],
        )
    )


@dataclass(frozen=True)
class GrowthReceipt:
    """Both certified signatures of a change of carrier; a report, not a repair."""

    before_phi1: Fraction
    after_phi1: Fraction
    before_gamma2: Fraction
    after_gamma2: Fraction
    before_class: DiagnosticClass
    after_class: DiagnosticClass
    before_certificate: QuotientCertificate
    after_certificate: QuotientCertificate

    @property
    def phi1_change(self) -> Fraction:
        return self.after_phi1 - self.before_phi1

    @property
    def gamma2_change(self) -> Fraction:
        return self.after_gamma2 - self.before_gamma2


def _signature(window: object) -> Outcome[ObstructionSignature]:
    admitted = _readmit(window)
    if isinstance(admitted, Refused):
        return admitted
    checked = admitted.value
    return obstruction_signature(
        checked.complex_, checked.cochain_map(), closure_declared=True, weights=checked.weight_map()
    )


def growth_receipt(before: WeightedWindow, after: WeightedWindow) -> Outcome[GrowthReceipt]:
    """Compute (Phi_1, Gamma_2) on both windows with independently verified certificates."""

    first, second = _signature(before), _signature(after)
    for outcome in (first, second):
        if isinstance(outcome, Refused):
            return outcome
    old, new = first.value, second.value  # type: ignore[union-attr]
    return Accepted(
        GrowthReceipt(
            old.phi1,
            new.phi1,
            old.gamma2,
            new.gamma2,
            old.diagnostic_class,
            new.diagnostic_class,
            old.certificate,
            new.certificate,
        )
    )


def claim_growth_repair(receipt: GrowthReceipt) -> Refused:
    """A change of carrier is never a repair of a quotient residual, whatever Phi_1 did."""

    if not isinstance(receipt, GrowthReceipt):
        return Refused(RefusalCode.INVALID_INPUT, "only a growth receipt can be examined for a repair claim")
    return Refused(
        RefusalCode.SCOPE_VIOLATION,
        f"Phi_1 moved {receipt.before_phi1} -> {receipt.after_phi1} under a change of carrier; a repair is a "
        "potential on one fixed window, not an arbitrary change of carrier",
    )


# Executable finite evidence; AuthorityEffect: None.
