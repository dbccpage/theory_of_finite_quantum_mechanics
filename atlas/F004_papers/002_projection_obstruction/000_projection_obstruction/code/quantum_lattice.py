"""Finite quantum-lattice numerical replays for PO-000 §5.

This module evaluates explicitly supplied finite matrices.  It does not prove
the quantified lattice theorem.  In particular, every evolution and norm is a
deterministic floating-point replay, and bound results retain their signed,
unclipped right-hand side.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from math import fsum, isfinite, prod
from types import MappingProxyType
from typing import Any, Literal, TypeAlias, cast

import numpy as np
import numpy.typing as npt

SiteId: TypeAlias = str
ComplexMatrix: TypeAlias = npt.NDArray[np.complex128]

DEFAULT_VALIDATION_ATOL = 1.0e-10
DEFAULT_COMPARISON_ATOL = 1.0e-9


class QuantumInputError(ValueError):
    """An input does not satisfy the declared finite quantum-host premises."""


def _finite_nonnegative_float(value: object, *, name: str) -> float:
    if isinstance(value, bool):
        raise QuantumInputError(f"{name} must be a finite real number")
    try:
        result = float(cast(Any, value))
    except (TypeError, ValueError) as error:
        raise QuantumInputError(f"{name} must be a finite real number") from error
    if not isfinite(result) or result < 0.0:
        raise QuantumInputError(f"{name} must be finite and nonnegative")
    return result


def _finite_float(value: object, *, name: str) -> float:
    if isinstance(value, bool):
        raise QuantumInputError(f"{name} must be a finite real number")
    try:
        result = float(cast(Any, value))
    except (TypeError, ValueError) as error:
        raise QuantumInputError(f"{name} must be a finite real number") from error
    if not isfinite(result):
        raise QuantumInputError(f"{name} must be finite")
    return result


def _readonly_matrix(value: object, *, name: str) -> ComplexMatrix:
    try:
        matrix = np.array(value, dtype=np.complex128, copy=True)
    except (TypeError, ValueError) as error:
        raise QuantumInputError(f"{name} must be a finite complex matrix") from error
    if matrix.ndim != 2:
        raise QuantumInputError(f"{name} must be rank two, got shape {matrix.shape}")
    if not np.isfinite(matrix.real).all() or not np.isfinite(matrix.imag).all():
        raise QuantumInputError(f"{name} contains NaN or infinity")
    matrix.flags.writeable = False
    return matrix


def _readonly_square_matrix(value: object, *, name: str) -> ComplexMatrix:
    matrix = _readonly_matrix(value, name=name)
    if matrix.shape[0] != matrix.shape[1]:
        raise QuantumInputError(f"{name} must be square, got shape {matrix.shape}")
    return matrix


def _readonly_copy(matrix: ComplexMatrix) -> ComplexMatrix:
    result = np.array(matrix, dtype=np.complex128, copy=True)
    result.flags.writeable = False
    return result


def _require_hermitian(
    matrix: ComplexMatrix, *, name: str, atol: float = DEFAULT_VALIDATION_ATOL
) -> None:
    if not np.allclose(matrix, matrix.conj().T, atol=atol, rtol=0.0):
        defect = float(np.linalg.norm(matrix - matrix.conj().T, ord="fro"))
        raise QuantumInputError(f"{name} is not Hermitian; Frobenius defect={defect}")


def trace_norm(matrix: object) -> float:
    """Return the numerical Schatten-1 norm of a finite matrix."""

    value = _readonly_matrix(matrix, name="trace-norm input")
    return float(np.linalg.svd(value, compute_uv=False).sum())


def operator_norm(matrix: object) -> float:
    """Return the numerical operator norm of a finite matrix."""

    value = _readonly_matrix(matrix, name="operator-norm input")
    return float(np.linalg.norm(value, ord=2))


def partial_trace_bipartite(
    matrix: object, dim_a: int, dim_b: int, *, keep: Literal["a", "b"]
) -> ComplexMatrix:
    """Trace one factor from an operator on ``A tensor B``."""

    if (
        isinstance(dim_a, bool)
        or isinstance(dim_b, bool)
        or not isinstance(dim_a, int)
        or not isinstance(dim_b, int)
        or dim_a <= 0
        or dim_b <= 0
    ):
        raise QuantumInputError("bipartite dimensions must be positive integers")
    value = _readonly_square_matrix(matrix, name="bipartite operator")
    expected = dim_a * dim_b
    if value.shape != (expected, expected):
        raise QuantumInputError(
            f"bipartite operator has shape {value.shape}, expected {(expected, expected)}"
        )
    tensor = value.reshape(dim_a, dim_b, dim_a, dim_b)
    if keep == "a":
        result = np.trace(tensor, axis1=1, axis2=3)
    elif keep == "b":
        result = np.trace(tensor, axis1=0, axis2=2)
    else:
        raise QuantumInputError("keep must be 'a' or 'b'")
    return _readonly_copy(result)


@dataclass(frozen=True)
class LocalHamiltonianTerm:
    """One validated Hermitian one- or two-site Hamiltonian term.

    The matrix tensor-factor order is exactly ``support``.
    """

    label: str
    support: tuple[SiteId, ...]
    operator: ComplexMatrix

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or not self.label.strip():
            raise QuantumInputError("Hamiltonian term labels must be nonempty strings")
        support = tuple(self.support)
        if len(support) not in (1, 2):
            raise QuantumInputError("Hamiltonian terms must have support size one or two")
        if any(not isinstance(site, str) or not site for site in support):
            raise QuantumInputError("Hamiltonian supports must contain nonempty site identifiers")
        if len(set(support)) != len(support):
            raise QuantumInputError("a Hamiltonian support may not repeat a site")
        matrix = _readonly_square_matrix(self.operator, name=f"term {self.label!r}")
        _require_hermitian(matrix, name=f"term {self.label!r}")
        object.__setattr__(self, "support", support)
        object.__setattr__(self, "operator", matrix)


@dataclass(frozen=True)
class IncidentNormReplay:
    """Numerical inventory for the paper's full incident norm ``g``."""

    term_operator_norms: tuple[tuple[str, float], ...]
    per_site_loads: tuple[tuple[SiteId, float], ...]
    g: float
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "Finite supplied matrices only; operator norms are floating-point SVD replays.",
    )


@dataclass(frozen=True)
class EdgeNormalRateReplay:
    """Numerical replay of ``L_e``, ``P_e L_e``, ``n_e=Q_e L_e``, and ``nu_e``."""

    edge: tuple[SiteId, SiteId]
    term_labels: tuple[str, ...]
    l_e: ComplexMatrix
    p_e_l_e: ComplexMatrix
    n_e: ComplexMatrix
    nu_e: float
    l_e_trace_error: float
    normal_marginal_a_norm: float
    normal_marginal_b_norm: float
    decomposition_error: float
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "One finite product state and finite Hamiltonian instance; not a proof of Lemma 5.3.",
    )


@dataclass(frozen=True)
class EdgeEvolutionReplay:
    """Deterministic eigendecomposition replay for one reduced edge defect."""

    edge: tuple[SiteId, SiteId]
    t: float
    rho_edge_t: ComplexMatrix
    rho_a_t: ComplexMatrix
    rho_b_t: ComplexMatrix
    product_of_marginals_t: ComplexMatrix
    defect_operator: ComplexMatrix
    defect: float
    eigendecomposition_residual: float
    unitarity_error: float
    state_trace_error: float
    state_hermiticity_error: float
    state_minimum_eigenvalue: float
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "Finite floating-point eigendecomposition; no all-time or all-system theorem claim.",
    )


@dataclass(frozen=True)
class ShortTimeBoundReplay:
    """One finite numerical comparison with an unclipped signed theorem RHS."""

    edge: tuple[SiteId, SiteId]
    t: float
    nu_e: float
    full_incident_g: float
    observed_defect: float
    signed_lower_bound_rhs: float
    numerical_margin: float
    comparison_tolerance: float
    bound_satisfied_with_tolerance: bool
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "Passing is evidence for this finite replay only, not verification of Theorem 5.1.",
    )


@dataclass(frozen=True)
class FiniteQuantumLattice:
    """Validated finite one-/two-local Hamiltonian with a product initial state."""

    site_order: tuple[SiteId, ...]
    dimensions: Mapping[SiteId, int]
    terms: tuple[LocalHamiltonianTerm, ...]
    product_state: Mapping[SiteId, ComplexMatrix]
    validation_atol: float = field(default=DEFAULT_VALIDATION_ATOL, repr=False)

    def __post_init__(self) -> None:
        atol = _finite_nonnegative_float(self.validation_atol, name="validation_atol")
        if atol == 0.0:
            raise QuantumInputError("validation_atol must be strictly positive")
        if atol > 1.0e-4:
            raise QuantumInputError(
                f"validation_atol ({atol}) exceeds maximum host-enforced cap of 1.0e-4"
            )

        sites = tuple(self.site_order)
        if not sites or any(not isinstance(site, str) or not site for site in sites):
            raise QuantumInputError("site_order must contain nonempty site identifiers")
        if len(set(sites)) != len(sites):
            raise QuantumInputError("site_order contains duplicates")

        dimensions = dict(self.dimensions)
        if set(dimensions) != set(sites):
            raise QuantumInputError("dimensions must cover exactly site_order")
        for site, dimension in dimensions.items():
            if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension <= 0:
                raise QuantumInputError(f"dimension for {site!r} must be a positive integer")

        terms = tuple(self.terms)
        if len({term.label for term in terms}) != len(terms):
            raise QuantumInputError("Hamiltonian term labels must be unique")
        for term in terms:
            if not isinstance(term, LocalHamiltonianTerm):
                raise QuantumInputError("terms must be LocalHamiltonianTerm instances")
            unknown = set(term.support) - set(sites)
            if unknown:
                raise QuantumInputError(
                    f"term {term.label!r} references unknown sites {sorted(unknown)}"
                )
            expected_dimension = prod(dimensions[site] for site in term.support)
            if term.operator.shape != (expected_dimension, expected_dimension):
                raise QuantumInputError(
                    f"term {term.label!r} has shape {term.operator.shape}, "
                    f"expected {(expected_dimension, expected_dimension)}"
                )

        supplied_states = dict(self.product_state)
        if set(supplied_states) != set(sites):
            raise QuantumInputError("product_state must cover exactly site_order")
        states: dict[SiteId, ComplexMatrix] = {}
        for site in sites:
            state = _readonly_square_matrix(supplied_states[site], name=f"local state at {site!r}")
            expected_shape = (dimensions[site], dimensions[site])
            if state.shape != expected_shape:
                raise QuantumInputError(
                    f"local state at {site!r} has shape {state.shape}, expected {expected_shape}"
                )
            _require_hermitian(state, name=f"local state at {site!r}", atol=atol)
            trace_error = abs(complex(np.trace(state)) - 1.0)
            if trace_error > atol:
                raise QuantumInputError(
                    f"local state at {site!r} is not trace one; error={trace_error}"
                )
            minimum_eigenvalue = float(np.linalg.eigvalsh(state).min())
            if minimum_eigenvalue < -atol:
                raise QuantumInputError(
                    f"local state at {site!r} is not positive semidefinite; "
                    f"minimum eigenvalue={minimum_eigenvalue}"
                )
            states[site] = state

        object.__setattr__(self, "site_order", sites)
        object.__setattr__(self, "dimensions", MappingProxyType(dimensions))
        object.__setattr__(self, "terms", terms)
        object.__setattr__(self, "product_state", MappingProxyType(states))
        object.__setattr__(self, "validation_atol", atol)

    @property
    def total_dimension(self) -> int:
        return prod(self.dimensions[site] for site in self.site_order)

    @property
    def initial_state(self) -> ComplexMatrix:
        result = np.array([[1.0 + 0.0j]], dtype=np.complex128)
        for site in self.site_order:
            result = np.asarray(np.kron(result, self.product_state[site]), dtype=np.complex128)
        return _readonly_copy(result)

    def _canonical_edge(self, edge: Sequence[SiteId]) -> tuple[SiteId, SiteId]:
        requested = tuple(edge)
        if len(requested) != 2 or requested[0] == requested[1]:
            raise QuantumInputError("an edge must contain two distinct sites")
        unknown = set(requested) - set(self.site_order)
        if unknown:
            raise QuantumInputError(f"edge references unknown sites {sorted(unknown)}")
        positions = {site: index for index, site in enumerate(self.site_order)}
        ordered = tuple(sorted(requested, key=positions.__getitem__))
        return ordered[0], ordered[1]

    def embed_operator(self, operator: object, support: Sequence[SiteId]) -> ComplexMatrix:
        """Embed an operator on arbitrary, possibly nonadjacent, sites."""

        local_support = tuple(support)
        if not local_support or len(set(local_support)) != len(local_support):
            raise QuantumInputError("operator support must be nonempty and contain unique sites")
        unknown = set(local_support) - set(self.site_order)
        if unknown:
            raise QuantumInputError(f"operator support has unknown sites {sorted(unknown)}")
        local = _readonly_square_matrix(operator, name="local operator")
        local_dimension = prod(self.dimensions[site] for site in local_support)
        if local.shape != (local_dimension, local_dimension):
            raise QuantumInputError(
                f"local operator has shape {local.shape}, "
                f"expected {(local_dimension, local_dimension)}"
            )

        complement = tuple(site for site in self.site_order if site not in local_support)
        complement_dimension = prod(self.dimensions[site] for site in complement)
        combined_order = local_support + complement
        combined_dimensions = tuple(self.dimensions[site] for site in combined_order)
        base = np.kron(local, np.eye(complement_dimension, dtype=np.complex128))
        tensor = base.reshape(combined_dimensions + combined_dimensions)
        factor_count = len(combined_order)
        permutation = tuple(combined_order.index(site) for site in self.site_order)
        transpose_axes = permutation + tuple(factor_count + index for index in permutation)
        embedded = tensor.transpose(transpose_axes).reshape(
            self.total_dimension, self.total_dimension
        )
        return _readonly_copy(np.asarray(embedded, dtype=np.complex128))

    def _selected_terms(
        self, term_labels: Iterable[str] | None
    ) -> tuple[LocalHamiltonianTerm, ...]:
        if term_labels is None:
            return self.terms
        labels = tuple(term_labels)
        if len(set(labels)) != len(labels):
            raise QuantumInputError("term_labels contains duplicates")
        known = {term.label for term in self.terms}
        unknown = set(labels) - known
        if unknown:
            raise QuantumInputError(f"unknown Hamiltonian term labels {sorted(unknown)}")
        selected = set(labels)
        return tuple(term for term in self.terms if term.label in selected)

    def hamiltonian(self, term_labels: Iterable[str] | None = None) -> ComplexMatrix:
        """Assemble the global Hamiltonian for all or selected local terms."""

        result = np.zeros((self.total_dimension, self.total_dimension), dtype=np.complex128)
        for term in self._selected_terms(term_labels):
            result += self.embed_operator(term.operator, term.support)
        return _readonly_copy(result)

    @property
    def total_hamiltonian(self) -> ComplexMatrix:
        return self.hamiltonian()

    def partial_trace(self, matrix: object, keep_sites: Sequence[SiteId]) -> ComplexMatrix:
        """Trace to ``keep_sites`` and return tensor factors in the requested order."""

        keep = tuple(keep_sites)
        if len(set(keep)) != len(keep):
            raise QuantumInputError("keep_sites contains duplicates")
        unknown = set(keep) - set(self.site_order)
        if unknown:
            raise QuantumInputError(f"keep_sites has unknown sites {sorted(unknown)}")
        value = _readonly_square_matrix(matrix, name="global operator")
        expected_shape = (self.total_dimension, self.total_dimension)
        if value.shape != expected_shape:
            raise QuantumInputError(
                f"global operator has shape {value.shape}, expected {expected_shape}"
            )

        current_sites = list(self.site_order)
        current_dimensions = [self.dimensions[site] for site in current_sites]
        tensor: npt.NDArray[np.complex128] = value.reshape(
            tuple(current_dimensions + current_dimensions)
        )
        keep_set = set(keep)
        for index in range(len(current_sites) - 1, -1, -1):
            if current_sites[index] in keep_set:
                continue
            factor_count = len(current_sites)
            tensor = np.trace(tensor, axis1=index, axis2=index + factor_count)
            current_sites.pop(index)
            current_dimensions.pop(index)

        if not current_sites:
            return _readonly_copy(np.asarray(tensor).reshape(1, 1))

        if tuple(current_sites) != keep:
            factor_count = len(current_sites)
            permutation = tuple(current_sites.index(site) for site in keep)
            tensor = tensor.reshape(tuple(current_dimensions + current_dimensions))
            tensor = tensor.transpose(
                permutation + tuple(factor_count + index for index in permutation)
            )
            current_dimensions = [self.dimensions[site] for site in keep]

        kept_dimension = prod(current_dimensions)
        return _readonly_copy(tensor.reshape(kept_dimension, kept_dimension))

    def incident_norm_replay(self) -> IncidentNormReplay:
        """Compute ``g=max_v sum_(X contains v) ||h_X||_op`` over all terms."""

        term_norms = tuple((term.label, operator_norm(term.operator)) for term in self.terms)
        norm_by_label = dict(term_norms)
        loads = tuple(
            (
                site,
                fsum(norm_by_label[term.label] for term in self.terms if site in term.support),
            )
            for site in self.site_order
        )
        g = max((load for _site, load in loads), default=0.0)
        return IncidentNormReplay(
            term_operator_norms=term_norms,
            per_site_loads=loads,
            g=float(g),
        )

    @property
    def full_incident_norm_g(self) -> float:
        return self.incident_norm_replay().g

    def global_derivative(self, term_labels: Iterable[str] | None = None) -> ComplexMatrix:
        """Compute ``-i[H, rho(0)]`` for selected finite terms."""

        hamiltonian = self.hamiltonian(term_labels)
        rho0 = self.initial_state
        return _readonly_copy(-1.0j * (hamiltonian @ rho0 - rho0 @ hamiltonian))

    def reduced_derivative(
        self, edge: Sequence[SiteId], term_labels: Iterable[str] | None = None
    ) -> ComplexMatrix:
        canonical = self._canonical_edge(edge)
        return self.partial_trace(self.global_derivative(term_labels), canonical)

    def apply_p_e(self, edge: Sequence[SiteId], tangent: object) -> ComplexMatrix:
        """Apply the product-retraction tangent map ``P_e`` to a trace-zero tangent."""

        canonical = self._canonical_edge(edge)
        site_a, site_b = canonical
        dim_a = self.dimensions[site_a]
        dim_b = self.dimensions[site_b]
        value = _readonly_square_matrix(tangent, name="edge tangent")
        expected = dim_a * dim_b
        if value.shape != (expected, expected):
            raise QuantumInputError(
                f"edge tangent has shape {value.shape}, expected {(expected, expected)}"
            )
        trace_error = abs(complex(np.trace(value)))
        if trace_error > 100.0 * self.validation_atol:
            raise QuantumInputError(
                f"P_e is declared here on trace-zero tangents; trace error={trace_error}"
            )
        marginal_a = partial_trace_bipartite(value, dim_a, dim_b, keep="a")
        marginal_b = partial_trace_bipartite(value, dim_a, dim_b, keep="b")
        projected = np.kron(marginal_a, self.product_state[site_b]) + np.kron(
            self.product_state[site_a], marginal_b
        )
        return _readonly_copy(projected)

    def apply_q_e(self, edge: Sequence[SiteId], tangent: object) -> ComplexMatrix:
        """Apply ``Q_e := I-P_e`` without conflating it with the residual vector."""

        value = _readonly_square_matrix(tangent, name="edge tangent")
        return _readonly_copy(value - self.apply_p_e(edge, value))

    def normal_rate_replay(
        self, edge: Sequence[SiteId], term_labels: Iterable[str] | None = None
    ) -> EdgeNormalRateReplay:
        """Replay ``n_e=Q_e L_e`` and ``nu_e=||n_e||_1``."""

        canonical = self._canonical_edge(edge)
        selected = self._selected_terms(term_labels)
        labels = tuple(term.label for term in selected)
        l_e = self.reduced_derivative(canonical, labels)
        p_e_l_e = self.apply_p_e(canonical, l_e)
        n_e = _readonly_copy(l_e - p_e_l_e)
        dim_a = self.dimensions[canonical[0]]
        dim_b = self.dimensions[canonical[1]]
        marginal_a = partial_trace_bipartite(n_e, dim_a, dim_b, keep="a")
        marginal_b = partial_trace_bipartite(n_e, dim_a, dim_b, keep="b")
        return EdgeNormalRateReplay(
            edge=canonical,
            term_labels=labels,
            l_e=l_e,
            p_e_l_e=p_e_l_e,
            n_e=n_e,
            nu_e=trace_norm(n_e),
            l_e_trace_error=float(abs(complex(np.trace(l_e)))),
            normal_marginal_a_norm=trace_norm(marginal_a),
            normal_marginal_b_norm=trace_norm(marginal_b),
            decomposition_error=float(np.linalg.norm(l_e - p_e_l_e - n_e, ord="fro")),
        )

    def edge_evolution_replay(self, edge: Sequence[SiteId], t: object) -> EdgeEvolutionReplay:
        """Replay the exact finite matrix evolution using Hermitian eigendecomposition."""

        canonical = self._canonical_edge(edge)
        time = _finite_nonnegative_float(t, name="t")
        hamiltonian = self.total_hamiltonian
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
        phases = np.exp(-1.0j * eigenvalues * time)
        unitary = (eigenvectors * phases) @ eigenvectors.conj().T
        rho0 = self.initial_state
        rho_t = unitary @ rho0 @ unitary.conj().T
        rho_edge = self.partial_trace(rho_t, canonical)
        dim_a = self.dimensions[canonical[0]]
        dim_b = self.dimensions[canonical[1]]
        rho_a = partial_trace_bipartite(rho_edge, dim_a, dim_b, keep="a")
        rho_b = partial_trace_bipartite(rho_edge, dim_a, dim_b, keep="b")
        product_state = _readonly_copy(np.asarray(np.kron(rho_a, rho_b), dtype=np.complex128))
        defect_operator = _readonly_copy(np.asarray(rho_edge - product_state, dtype=np.complex128))

        identity = np.eye(self.total_dimension, dtype=np.complex128)
        eigen_residual = np.linalg.norm(
            hamiltonian @ eigenvectors - eigenvectors * eigenvalues, ord="fro"
        )
        unitarity_error = np.linalg.norm(unitary.conj().T @ unitary - identity, ord="fro")
        state_hermiticity_error = np.linalg.norm(rho_t - rho_t.conj().T, ord="fro")
        return EdgeEvolutionReplay(
            edge=canonical,
            t=time,
            rho_edge_t=_readonly_copy(rho_edge),
            rho_a_t=_readonly_copy(rho_a),
            rho_b_t=_readonly_copy(rho_b),
            product_of_marginals_t=product_state,
            defect_operator=defect_operator,
            defect=trace_norm(defect_operator),
            eigendecomposition_residual=float(eigen_residual),
            unitarity_error=float(unitarity_error),
            state_trace_error=float(abs(complex(np.trace(rho_t)) - 1.0)),
            state_hermiticity_error=float(state_hermiticity_error),
            state_minimum_eigenvalue=float(np.linalg.eigvalsh(rho_t).min()),
        )

    def short_time_bound_replay(
        self,
        edge: Sequence[SiteId],
        t: object,
        *,
        comparison_tolerance: object = DEFAULT_COMPARISON_ATOL,
    ) -> ShortTimeBoundReplay:
        """Compare one observed defect with ``nu_e*t - 24*g**2*t**2``.

        The returned right-hand side is deliberately not clipped at zero.
        """

        tolerance = _finite_nonnegative_float(comparison_tolerance, name="comparison_tolerance")
        if tolerance == 0.0:
            raise QuantumInputError("comparison_tolerance must be strictly positive")
        evolution = self.edge_evolution_replay(edge, t)
        normal = self.normal_rate_replay(edge)
        g = self.full_incident_norm_g
        signed_rhs = normal.nu_e * evolution.t - 24.0 * g**2 * evolution.t**2
        margin = evolution.defect - signed_rhs
        return ShortTimeBoundReplay(
            edge=evolution.edge,
            t=evolution.t,
            nu_e=normal.nu_e,
            full_incident_g=g,
            observed_defect=evolution.defect,
            signed_lower_bound_rhs=float(signed_rhs),
            numerical_margin=float(margin),
            comparison_tolerance=tolerance,
            bound_satisfied_with_tolerance=margin >= -tolerance,
        )

    def half_slope_window(self, edge: Sequence[SiteId]) -> float:
        """Return ``nu_e/(48*g**2)`` for this finite replay, or zero."""

        nu_e = self.normal_rate_replay(edge).nu_e
        g = self.full_incident_norm_g
        if nu_e <= self.validation_atol or g <= self.validation_atol:
            return 0.0
        return float(nu_e / (48.0 * g**2))
