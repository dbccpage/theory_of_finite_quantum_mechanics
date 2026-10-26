"""Exact finite observer-carrier certificates for PO-000 §7.4.

The three quantities are intentionally kept distinct:

``I``
    The raw represented edge-defect tally.
``J[alpha]``
    One observer's projected local tally.
``Lambda``
    The best-single-observer visibility gap ``I - max_alpha J[alpha]``.
    It can include edgewise projection loss and portfolio fragmentation.

All results are certificates for explicitly supplied finite matrices and
defects.  They do not claim the paper's universally quantified statements are
proved by Python.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import TypeVar

from exactsym import Basic, Matrix, MatrixBase, Rational, simplify

from covering_edge import CoveringEdge, CoveringEdgeDiagram, l1_operator_norm
from exact import ExactInput, as_rational, exact_column, exact_equal, l1_norm


def _exact_matrix(value: MatrixBase) -> Matrix:
    return Matrix(
        value.rows,
        value.cols,
        [as_rational(value[row, col]) for row in range(value.rows) for col in range(value.cols)],
    )


_ValueT = TypeVar("_ValueT")


def _frozen_mapping(values: Mapping[str, _ValueT]) -> Mapping[str, _ValueT]:
    return MappingProxyType(dict(values))


@dataclass(frozen=True)
class LocalObserverCarrier:
    """A nonempty finite edge domain with one contractive map per edge."""

    observer_id: str
    maps: Mapping[str, MatrixBase]

    def __post_init__(self) -> None:
        if not self.observer_id.strip():
            raise ValueError("observer_id must be nonempty")
        if not self.maps:
            raise ValueError("an observer must watch at least one edge")
        object.__setattr__(self, "maps", MappingProxyType(dict(self.maps)))


@dataclass(frozen=True)
class ObserverTallies:
    """Exact values of the raw, observed, and lost defect tallies."""

    I: Basic
    J: Mapping[str, Basic]
    Lambda: Basic
    evidence_scope: str = "exact finite observer tally"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        if not self.J:
            return False
        if bool(self.I < 0) or bool(self.Lambda < 0) or any(bool(v < 0) for v in self.J.values()):
            return False
        expected_loss = simplify(self.I - max(self.J.values()))
        return simplify(self.Lambda - expected_loss) == 0 and bool(self.Lambda >= 0)


@dataclass(frozen=True)
class PassivityRow:
    observer_id: str
    observed_J: Basic
    watched_raw_tally: Basic
    raw_I: Basic
    observed_le_watched: bool
    watched_le_raw: bool


@dataclass(frozen=True)
class VisibilityGapDecomposition:
    """Exact split of ``Lambda`` into edgewise loss and observer fragmentation."""

    p_by_edge: Mapping[str, Basic]
    edgewise_observation_loss: Basic
    single_observer_fragmentation: Basic
    Lambda: Basic
    evidence_scope: str = "exact finite visibility-gap decomposition"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        return (
            bool(self.p_by_edge)
            and bool(self.edgewise_observation_loss >= 0)
            and bool(self.single_observer_fragmentation >= 0)
            and simplify(
                self.edgewise_observation_loss + self.single_observer_fragmentation - self.Lambda
            )
            == 0
        )


@dataclass(frozen=True)
class PassivityCertificate:
    """Finite exact check of ``J^alpha <= I_watched <= I``."""

    rows: tuple[PassivityRow, ...]
    holds: bool
    evidence_scope: str = "exact finite passivity instance"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        if not self.rows:
            return False
        for row in self.rows:
            if not (
                bool(row.observed_J >= 0)
                and bool(row.watched_raw_tally >= 0)
                and bool(row.raw_I >= 0)
                and bool(row.observed_J <= row.watched_raw_tally)
                and bool(row.watched_raw_tally <= row.raw_I)
                and row.observed_le_watched
                and row.watched_le_raw
            ):
                return False
        return self.holds is True


@dataclass(frozen=True)
class AllGreenKernelCertificate:
    """Instance check of the All-Green/joint-kernel equivalence."""

    all_green: bool
    edgewise_joint_kernel_membership: Mapping[str, bool]
    joint_kernel_condition: bool
    equivalent: bool
    evidence_scope: str = "exact finite All-Green joint-kernel instance"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        condition = all(self.edgewise_joint_kernel_membership.values())
        return (
            condition == self.joint_kernel_condition
            and self.equivalent == (self.all_green == condition)
            and self.equivalent
        )


@dataclass(frozen=True)
class JointInjectivityCertificate:
    """Rank certificate for the combined watcher map on every edge."""

    full_edge_coverage: bool
    edgewise_injective: Mapping[str, bool]
    edgewise_combined_rank: Mapping[str, int]
    premises_hold: bool
    evidence_scope: str = "exact finite joint-injectivity certificate"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        ranks_valid = all(r >= 0 for r in self.edgewise_combined_rank.values())
        expected = self.full_edge_coverage and all(self.edgewise_injective.values())
        return bool(self.edgewise_injective) and ranks_valid and self.premises_hold == expected


@dataclass(frozen=True)
class LocalToGlobalCertificate:
    """Premise-gated finite implication check; refusal is explicit."""

    accepted: bool
    all_green: bool
    global_green: bool
    implication_holds: bool | None
    refusals: tuple[str, ...]
    evidence_scope: str = "exact finite local-to-global instance"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        if not self.accepted:
            return bool(self.refusals) and self.implication_holds is None
        expected = (not self.all_green) or self.global_green
        return not self.refusals and self.implication_holds == expected and expected


class ObserverFamily:
    """A nonempty family of exact finite observer carriers."""

    def __init__(
        self,
        edge_dimensions: Mapping[str, int],
        observers: Sequence[LocalObserverCarrier],
    ):
        if not edge_dimensions:
            raise ValueError("an observer family needs at least one edge")
        if any(
            isinstance(dimension, bool) or dimension <= 0 for dimension in edge_dimensions.values()
        ):
            raise ValueError("edge dimensions must be positive integers")
        if not observers:
            raise ValueError("an observer family must be nonempty")
        if len({observer.observer_id for observer in observers}) != len(observers):
            raise ValueError("observer identifiers must be unique")

        self.edge_dimensions = dict(edge_dimensions)
        normalized_observers: list[LocalObserverCarrier] = []
        for observer in observers:
            unknown = set(observer.maps) - set(self.edge_dimensions)
            if unknown:
                raise ValueError(
                    f"observer {observer.observer_id!r} references unknown edges {sorted(unknown)}"
                )
            normalized: dict[str, Matrix] = {}
            for edge_id, raw_map in observer.maps.items():
                matrix = _exact_matrix(Matrix(raw_map))
                expected_columns = self.edge_dimensions[edge_id]
                if matrix.rows <= 0 or matrix.cols != expected_columns:
                    raise ValueError(
                        f"observer {observer.observer_id!r} map on {edge_id!r} "
                        f"has shape {matrix.shape}, expected positive rows and "
                        f"{expected_columns} columns"
                    )
                if l1_operator_norm(matrix) > 1:
                    raise ValueError(
                        f"observer {observer.observer_id!r} map on {edge_id!r} "
                        "is not l1-contractive"
                    )
                normalized[edge_id] = matrix
            normalized_observers.append(LocalObserverCarrier(observer.observer_id, normalized))
        self.observers = tuple(normalized_observers)
        self._by_id = {observer.observer_id: observer for observer in self.observers}

    def normalize_defects(
        self,
        defects: Mapping[str, Sequence[ExactInput] | MatrixBase],
    ) -> dict[str, Matrix]:
        missing = set(self.edge_dimensions) - set(defects)
        extra = set(defects) - set(self.edge_dimensions)
        if missing or extra:
            raise ValueError(
                f"defect domain mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
            )
        normalized: dict[str, Matrix] = {}
        for edge_id, dimension in self.edge_dimensions.items():
            raw = defects[edge_id]
            vector = (
                _exact_matrix(Matrix(raw)) if isinstance(raw, MatrixBase) else exact_column(raw)
            )
            if vector.shape != (dimension, 1):
                raise ValueError(
                    f"defect on {edge_id!r} has shape {vector.shape}, expected {(dimension, 1)}"
                )
            normalized[edge_id] = vector
        return normalized

    def watchers(self, edge_id: str) -> tuple[LocalObserverCarrier, ...]:
        if edge_id not in self.edge_dimensions:
            raise KeyError(edge_id)
        return tuple(observer for observer in self.observers if edge_id in observer.maps)

    @property
    def full_edge_coverage(self) -> bool:
        return all(self.watchers(edge_id) for edge_id in self.edge_dimensions)

    def combined_watcher_map(self, edge_id: str) -> Matrix:
        watchers = self.watchers(edge_id)
        if not watchers:
            return Matrix.zeros(0, self.edge_dimensions[edge_id])
        return Matrix.vstack(*(watcher.maps[edge_id] for watcher in watchers))

    def joint_kernel_basis(self, edge_id: str) -> tuple[Matrix, ...]:
        return tuple(self.combined_watcher_map(edge_id).nullspace())

    def jointly_injective(self, edge_id: str) -> bool:
        combined = self.combined_watcher_map(edge_id)
        return bool(self.watchers(edge_id)) and combined.rank() == self.edge_dimensions[edge_id]

    def tallies(
        self,
        defects: Mapping[str, Sequence[ExactInput] | MatrixBase],
    ) -> ObserverTallies:
        values = self.normalize_defects(defects)
        raw_tally = simplify(sum(l1_norm(value) for value in values.values()))
        observed = {
            observer.observer_id: simplify(
                sum(l1_norm(observer.maps[edge_id] * values[edge_id]) for edge_id in observer.maps)
            )
            for observer in self.observers
        }
        loss = simplify(raw_tally - max(observed.values()))
        certificate = ObserverTallies(
            I=raw_tally,
            J=_frozen_mapping(observed),
            Lambda=loss,
        )
        if not certificate.verify():
            raise ArithmeticError("observer tally failed internal exact recheck")
        return certificate

    def visibility_gap_decomposition(
        self,
        defects: Mapping[str, Sequence[ExactInput] | MatrixBase],
    ) -> VisibilityGapDecomposition:
        values = self.normalize_defects(defects)
        tallies = self.tallies(values)
        p_by_edge = {}
        for edge_id, value in values.items():
            watched_values = [
                l1_norm(observer.maps[edge_id] * value) for observer in self.watchers(edge_id)
            ]
            p_by_edge[edge_id] = simplify(max(watched_values) if watched_values else Rational(0))
        edgewise_loss = simplify(
            sum(l1_norm(values[edge_id]) - p_by_edge[edge_id] for edge_id in values)
        )
        fragmentation = simplify(sum(p_by_edge.values()) - max(tallies.J.values()))
        certificate = VisibilityGapDecomposition(
            p_by_edge=_frozen_mapping(p_by_edge),
            edgewise_observation_loss=edgewise_loss,
            single_observer_fragmentation=fragmentation,
            Lambda=tallies.Lambda,
        )
        if not certificate.verify():
            raise ArithmeticError("visibility-gap decomposition failed internal exact recheck")
        return certificate

    def passivity_certificate(
        self,
        defects: Mapping[str, Sequence[ExactInput] | MatrixBase],
    ) -> PassivityCertificate:
        values = self.normalize_defects(defects)
        tallies = self.tallies(values)
        rows: list[PassivityRow] = []
        for observer in self.observers:
            watched = simplify(sum(l1_norm(values[edge_id]) for edge_id in observer.maps))
            observed = tallies.J[observer.observer_id]
            rows.append(
                PassivityRow(
                    observer_id=observer.observer_id,
                    observed_J=observed,
                    watched_raw_tally=watched,
                    raw_I=tallies.I,
                    observed_le_watched=bool(observed <= watched),
                    watched_le_raw=bool(watched <= tallies.I),
                )
            )
        certificate = PassivityCertificate(
            rows=tuple(rows),
            holds=all(row.observed_le_watched and row.watched_le_raw for row in rows),
        )
        if not certificate.verify():
            raise ArithmeticError("passivity certificate failed internal exact recheck")
        return certificate

    def all_green_kernel_certificate(
        self,
        defects: Mapping[str, Sequence[ExactInput] | MatrixBase],
    ) -> AllGreenKernelCertificate:
        values = self.normalize_defects(defects)
        tallies = self.tallies(values)
        all_green = all(value == 0 for value in tallies.J.values())
        memberships = {
            edge_id: exact_equal(
                self.combined_watcher_map(edge_id) * values[edge_id],
                Matrix.zeros(self.combined_watcher_map(edge_id).rows, 1),
            )
            for edge_id in self.edge_dimensions
        }
        condition = all(memberships.values())
        certificate = AllGreenKernelCertificate(
            all_green=all_green,
            edgewise_joint_kernel_membership=_frozen_mapping(memberships),
            joint_kernel_condition=condition,
            equivalent=all_green == condition,
        )
        if not certificate.verify():
            raise ArithmeticError("All-Green certificate failed internal exact recheck")
        return certificate

    def joint_injectivity_certificate(self) -> JointInjectivityCertificate:
        injective = {edge_id: self.jointly_injective(edge_id) for edge_id in self.edge_dimensions}
        ranks = {
            edge_id: self.combined_watcher_map(edge_id).rank() for edge_id in self.edge_dimensions
        }
        certificate = JointInjectivityCertificate(
            full_edge_coverage=self.full_edge_coverage,
            edgewise_injective=_frozen_mapping(injective),
            edgewise_combined_rank=_frozen_mapping(ranks),
            premises_hold=self.full_edge_coverage and all(injective.values()),
        )
        if not certificate.verify():
            raise ArithmeticError("joint-injectivity certificate failed internal recheck")
        return certificate

    def local_to_global_certificate(
        self,
        defects: Mapping[str, Sequence[ExactInput] | MatrixBase],
    ) -> LocalToGlobalCertificate:
        values = self.normalize_defects(defects)
        injectivity = self.joint_injectivity_certificate()
        all_green = self.all_green_kernel_certificate(values).all_green
        global_green = self.tallies(values).I == 0
        refusals: list[str] = []
        if not injectivity.full_edge_coverage:
            refusals.append("full_edge_coverage_not_supplied")
        noninjective = [
            edge_id
            for edge_id, is_injective in injectivity.edgewise_injective.items()
            if not is_injective
        ]
        if noninjective:
            refusals.append(f"nontrivial_joint_kernels={sorted(noninjective)}")
        accepted = not refusals
        certificate = LocalToGlobalCertificate(
            accepted=accepted,
            all_green=all_green,
            global_green=global_green,
            implication_holds=((not all_green) or global_green) if accepted else None,
            refusals=tuple(refusals),
        )
        if not certificate.verify():
            raise ArithmeticError("local-to-global certificate failed internal recheck")
        return certificate


@dataclass(frozen=True)
class ThreePatchCertificate:
    """Exact replay of Proposition 7.4.5 at one positive rational scale."""

    scale: Rational
    family: ObserverFamily
    diagram: CoveringEdgeDiagram
    section: Mapping[str, Matrix]
    defects: Mapping[str, Matrix]
    tallies: ObserverTallies
    passivity: PassivityCertificate
    all_green_kernel: AllGreenKernelCertificate
    full_edge_coverage: bool
    raw_formula_holds: bool
    evidence_scope: str = "exact finite three-patch witness"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        derived_defects = self.diagram.coboundary(self.section)
        defects_are_derived = set(derived_defects) == set(self.defects) and all(
            exact_equal(derived_defects[edge_id], self.defects[edge_id])
            for edge_id in derived_defects
        )
        if not defects_are_derived:
            return False
        try:
            recomputed = self.family.tallies(self.defects)
        except Exception:
            return False
        tallies_match = (
            exact_equal(recomputed.I, self.tallies.I)
            and set(recomputed.J) == set(self.tallies.J)
            and all(exact_equal(recomputed.J[k], self.tallies.J[k]) for k in recomputed.J)
            and exact_equal(recomputed.Lambda, self.tallies.Lambda)
        )
        return (
            self.scale > 0
            and tallies_match
            and exact_equal(self.diagram.inconsistency(self.section), self.tallies.I)
            and self.full_edge_coverage == self.family.full_edge_coverage
            and self.full_edge_coverage
            and self.raw_formula_holds
            and simplify(self.tallies.I - 6 * self.scale) == 0
            and all(value == 0 for value in self.tallies.J.values())
            and simplify(self.tallies.Lambda - self.tallies.I) == 0
            and self.passivity.verify()
            and self.all_green_kernel.verify()
            and self.all_green_kernel.all_green
        )


@dataclass(frozen=True)
class ScalingFamilyCertificate:
    """A finite list of exact scaled three-patch instances."""

    instances: tuple[ThreePatchCertificate, ...]
    exact_linear_scaling: bool
    evidence_scope: str = "exact finite scaling instances"
    universal_recovery_modulus_status: str = "not claimed by finite replay"
    authority_effect: str = "None"

    def verify(self) -> bool:
        return (
            bool(self.instances)
            and all(instance.verify() for instance in self.instances)
            and self.exact_linear_scaling
            == all(
                simplify(instance.tallies.I - 6 * instance.scale) == 0
                and all(value == 0 for value in instance.tallies.J.values())
                for instance in self.instances
            )
        )


def _coordinate_deletion(coordinate: int) -> Matrix:
    if coordinate == 0:
        return Matrix([[0, 1, 0], [0, 0, 1]])
    if coordinate == 1:
        return Matrix([[1, 0, 0], [0, 0, 1]])
    if coordinate == 2:
        return Matrix([[1, 0, 0], [0, 1, 0]])
    raise ValueError("coordinate must be 0, 1, or 2")


def three_patch_certificate(scale: ExactInput = 1) -> ThreePatchCertificate:
    """Construct and recheck the exact six-edge Local-Green/Global-Red witness."""

    scalar = as_rational(scale)
    if scalar <= 0:
        raise ValueError("the three-patch scaling parameter must be positive")

    edge_specs = (
        ("x12->u1", "x12", "u1", "C1"),
        ("x12->u2", "x12", "u2", "C2"),
        ("x23->u2", "x23", "u2", "C2"),
        ("x23->u3", "x23", "u3", "C3"),
        ("x31->u3", "x31", "u3", "C3"),
        ("x31->u1", "x31", "u1", "C1"),
    )
    edges_by_observer = {
        observer_id: tuple(
            edge_id for edge_id, _lower, _upper, watcher in edge_specs if watcher == observer_id
        )
        for observer_id in ("C1", "C2", "C3")
    }
    fiber_dimensions = {
        "x12": 3,
        "x23": 3,
        "x31": 3,
        "u1": 3,
        "u2": 3,
        "u3": 3,
    }
    diagram = CoveringEdgeDiagram(
        fiber_dimensions,
        tuple(
            CoveringEdge(edge_id, lower, upper, Matrix.eye(3))
            for edge_id, lower, upper, _watcher in edge_specs
        ),
    )
    section = {
        "x12": Matrix.zeros(3, 1),
        "x23": Matrix.zeros(3, 1),
        "x31": Matrix.zeros(3, 1),
        "u1": Matrix([scalar, 0, 0]),
        "u2": Matrix([0, scalar, 0]),
        "u3": Matrix([0, 0, scalar]),
    }
    edge_dimensions = {edge_id: 3 for edge_id, *_rest in edge_specs}
    observers = tuple(
        LocalObserverCarrier(
            observer_id,
            {edge_id: _coordinate_deletion(index) for edge_id in edges},
        )
        for index, (observer_id, edges) in enumerate(edges_by_observer.items())
    )
    family = ObserverFamily(edge_dimensions, observers)
    defects = diagram.coboundary(section)
    tallies = family.tallies(defects)
    certificate = ThreePatchCertificate(
        scale=scalar,
        family=family,
        diagram=diagram,
        section=_frozen_mapping(section),
        defects=_frozen_mapping(defects),
        tallies=tallies,
        passivity=family.passivity_certificate(defects),
        all_green_kernel=family.all_green_kernel_certificate(defects),
        full_edge_coverage=family.full_edge_coverage,
        raw_formula_holds=simplify(tallies.I - 6 * scalar) == 0,
    )
    if not certificate.verify():
        raise ArithmeticError("three-patch witness failed internal exact recheck")
    return certificate


def scaling_family_certificate(
    scales: Sequence[ExactInput],
) -> ScalingFamilyCertificate:
    """Replay a nonempty finite list of positive rational scaling instances."""

    if not scales:
        raise ValueError("at least one scaling instance is required")
    instances = tuple(three_patch_certificate(scale) for scale in scales)
    certificate = ScalingFamilyCertificate(
        instances=instances,
        exact_linear_scaling=all(
            simplify(instance.tallies.I - 6 * instance.scale) == 0
            and all(value == 0 for value in instance.tallies.J.values())
            for instance in instances
        ),
    )
    if not certificate.verify():
        raise ArithmeticError("scaling-family certificate failed internal exact recheck")
    return certificate
