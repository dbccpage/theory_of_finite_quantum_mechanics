from __future__ import annotations
r"""
Lefschetz Thimble data structures and abstract action interface.

AuthorityEffect: None.

Provides:
1. AnalyticAction — abstract base for complex actions S(z) with eval/gradient/hessian.
2. ThimbleFlowResult — trajectory + conserved phase + terminal saddle label.
3. IntegrationCycle — formal Z-linear combination of thimbles Gamma = sum n_sigma J_sigma.
4. StokesData — critical values and Stokes matrix m_{sigma,tau}.
"""


import abc
from dataclasses import field
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


class AnalyticAction(abc.ABC):
    """Abstract base for a complex holomorphic action S(z_0, ..., z_{n-1}).

    Subclasses must implement eval, gradient, hessian for their specific functional form.
    This decouples the Newton/flow engine from the polynomial representation.
    """

    @property
    @abc.abstractmethod
    def n_vars(self) -> int: ...

    @abc.abstractmethod
    def eval(self, z: List[complex]) -> complex: ...

    @abc.abstractmethod
    def gradient(self, z: List[complex]) -> List[complex]: ...

    @abc.abstractmethod
    def hessian(self, z: List[complex]) -> List[List[complex]]: ...


@dataclass
class ThimbleFlowResult:
    """Result of a steepest-descent flow from a starting point.

    Attributes:
        trajectory: list of z-vectors along the flow.
        conserved_im_s: Im(S) at the starting point (conserved along exact flow).
        max_im_deviation: maximum observed |Im(S(z(t))) - conserved_im_s|.
        source_label: index of the critical point nearest to the start (may be None).
        target_label: index of the critical point the flow converges to (None if no convergence).
        orientation_sign: +1 or -1, the sign of det(linearised flow) at the target.
        jacobian_history: list of n x n complex matrices J(t) representing parallel transport.
        residual_phase: continuous residual phase phi_res = arg(det J(t)) along flow.
        jacobian_determinant: magnitude |det J(t)| of tangent frame embedding.
    """

    trajectory: List[List[complex]]
    conserved_im_s: float
    max_im_deviation: float
    source_label: Optional[int] = None
    target_label: Optional[int] = None
    orientation_sign: Optional[int] = None
    jacobian_history: List[List[List[complex]]] = field(default_factory=list)
    residual_phase: float = 0.0
    jacobian_determinant: Optional[float] = None



@dataclass
class IntegrationCycle:
    r"""Formal Z-linear combination of Lefschetz thimbles: Gamma = sum_sigma n_sigma J_sigma.

    The coefficients update under Stokes wall-crossing according to
    n_sigma -> n_sigma + m_{sigma,tau} * n_tau
    when crossing the Stokes ray where Re(S(z_sigma)) = Re(S(z_tau)).
    """

    coefficients: Dict[int, int] = field(default_factory=dict)

    def stokes_jump(self, sigma: int, tau: int, m_st: int) -> "IntegrationCycle":
        """Apply Stokes wall-crossing: n_sigma -> n_sigma + m_{sigma,tau} * n_tau.

        Returns a new IntegrationCycle.
        """
        new_coeffs = dict(self.coefficients)
        n_tau = new_coeffs.get(tau, 0)
        n_sigma = new_coeffs.get(sigma, 0)
        new_coeffs[sigma] = n_sigma + m_st * n_tau
        return IntegrationCycle(coefficients=new_coeffs)

    def __repr__(self) -> str:
        terms = []
        for label in sorted(self.coefficients):
            c = self.coefficients[label]
            if c != 0:
                terms.append(f"{c}·J_{label}")
        return " + ".join(terms) if terms else "0"


@dataclass
class StokesData:
    """Critical values and Stokes matrix for an action.

    Attributes:
        critical_values: sigma -> S(z_sigma).
        stokes_matrix: (sigma, tau) -> m_{sigma,tau} (the integer jumping coefficient).
        stokes_rays: list of (sigma, tau, angle) where the Stokes ray occurs.
    """

    critical_values: Dict[int, complex] = field(default_factory=dict)
    stokes_matrix: Dict[Tuple[int, int], int] = field(default_factory=dict)
    stokes_rays: List[Tuple[int, int, float]] = field(default_factory=list)



