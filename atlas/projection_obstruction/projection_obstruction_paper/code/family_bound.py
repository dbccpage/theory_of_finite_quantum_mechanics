"""Exact finite premise certificates for the PO-000 uniform family bound.

This module checks the hypotheses and arithmetic of Corollary 5.1.A on a
*supplied finite family*.  It does not simulate quantum dynamics and it does
not promote the paper's quantified, conditional theorem to a Python proof.
Every scalar on this rail is rational and binary floating point is rejected.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from exactsym import Rational, simplify

from exact import ExactInput, as_rational


@dataclass(frozen=True, init=False)
class FiniteFamilyMember:
    """One finite system and the active-edge rates supplied by its caller."""

    system_id: str
    site_count: int
    edge_count: int
    local_interaction_norm: Rational
    active_edge_rates: tuple[Rational, ...]

    def __init__(
        self,
        system_id: str,
        site_count: int,
        edge_count: int,
        local_interaction_norm: ExactInput,
        active_edge_rates: Sequence[ExactInput],
    ) -> None:
        if not system_id.strip():
            raise ValueError("system_id must be nonempty")
        if isinstance(site_count, bool) or not isinstance(site_count, int) or site_count <= 0:
            raise ValueError("site_count must be a positive integer")
        if isinstance(edge_count, bool) or not isinstance(edge_count, int) or edge_count <= 0:
            raise ValueError("edge_count must be a positive integer")

        interaction_norm = as_rational(local_interaction_norm)
        rates = tuple(as_rational(rate) for rate in active_edge_rates)
        if interaction_norm < 0:
            raise ValueError("local_interaction_norm must be nonnegative")
        if len(rates) > edge_count:
            raise ValueError("active-edge count cannot exceed edge_count")
        if any(rate < 0 for rate in rates):
            raise ValueError("active-edge rates must be nonnegative")

        object.__setattr__(self, "system_id", system_id)
        object.__setattr__(self, "site_count", site_count)
        object.__setattr__(self, "edge_count", edge_count)
        object.__setattr__(self, "local_interaction_norm", interaction_norm)
        object.__setattr__(self, "active_edge_rates", rates)

    @property
    def active_edge_count(self) -> int:
        return len(self.active_edge_rates)

    @property
    def active_edge_density(self) -> Rational:
        return Rational(self.active_edge_count, self.edge_count)

    @property
    def edge_site_density(self) -> Rational:
        return Rational(self.edge_count, self.site_count)


@dataclass(frozen=True, init=False)
class UniformFamilyPremises:
    """Candidate constants from the displayed hypotheses of Corollary 5.1.A."""

    g_star: Rational
    eta_star: Rational
    nu_star: Rational
    a_star: Rational

    def __init__(
        self,
        g_star: ExactInput,
        eta_star: ExactInput,
        nu_star: ExactInput,
        a_star: ExactInput,
    ) -> None:
        object.__setattr__(self, "g_star", as_rational(g_star))
        object.__setattr__(self, "eta_star", as_rational(eta_star))
        object.__setattr__(self, "nu_star", as_rational(nu_star))
        object.__setattr__(self, "a_star", as_rational(a_star))


@dataclass(frozen=True)
class PremiseRefusal:
    """A checkable reason that the finite certificate was not issued."""

    code: str
    detail: str
    system_id: str | None = None


@dataclass(frozen=True)
class MemberDensityBound:
    """The exact conditional lower-bound arithmetic for one supplied member."""

    system_id: str
    active_edge_density: Rational
    edge_site_density: Rational
    edge_density_lower_bound: Rational
    site_density_lower_bound: Rational


@dataclass(frozen=True)
class UniformFamilyBoundCertificate:
    """Result of the finite premise audit and exact bound calculation."""

    accepted: bool
    time: Rational
    uniform_window_upper: Rational | None
    local_edge_polynomial: Rational | None
    edge_density_floor: Rational | None
    site_density_floor: Rational | None
    half_slope_site_floor: Rational | None
    member_bounds: tuple[MemberDensityBound, ...]
    refusals: tuple[PremiseRefusal, ...]
    evidence_scope: str = "exact finite supplied-family premise certificate"
    universal_theorem_status: str = "not claimed"
    authority_effect: str = "None"

    def verify(self) -> bool:
        """Recheck internal consistency without strengthening the scope."""

        if not self.accepted:
            return bool(self.refusals) and not self.member_bounds
        if self.refusals or not self.member_bounds:
            return False
        if (
            self.uniform_window_upper is None
            or self.local_edge_polynomial is None
            or self.edge_density_floor is None
            or self.site_density_floor is None
            or self.half_slope_site_floor is None
        ):
            return False
        if (
            self.local_edge_polynomial <= 0
            or self.edge_density_floor <= 0
            or self.site_density_floor <= 0
        ):
            return False
        if not (0 < self.time <= self.uniform_window_upper):
            return False
        if (
            self.half_slope_site_floor <= 0
            or self.site_density_floor < self.half_slope_site_floor
        ):
            return False
        for member in self.member_bounds:
            if (
                member.edge_density_lower_bound < self.edge_density_floor
                or member.site_density_lower_bound < self.site_density_floor
            ):
                return False
            expected_edge_bound = simplify(member.active_edge_density * self.local_edge_polynomial)
            if member.edge_density_lower_bound != expected_edge_bound:
                return False
        return True


def _constant_refusals(premises: UniformFamilyPremises) -> list[PremiseRefusal]:
    refusals: list[PremiseRefusal] = []
    if premises.g_star <= 0:
        refusals.append(
            PremiseRefusal(
                "g_star_not_positive",
                "the displayed finite time window requires g_star > 0",
            )
        )
    if premises.eta_star <= 0:
        refusals.append(
            PremiseRefusal("eta_star_not_positive", "eta_star must be strictly positive")
        )
    elif premises.eta_star > 1:
        refusals.append(
            PremiseRefusal("eta_star_exceeds_one", "an active-edge density cannot exceed one")
        )
    if premises.nu_star <= 0:
        refusals.append(PremiseRefusal("nu_star_not_positive", "nu_star must be strictly positive"))
    if premises.a_star <= 0:
        refusals.append(PremiseRefusal("a_star_not_positive", "a_star must be strictly positive"))
    return refusals


def certify_uniform_family(
    members: tuple[FiniteFamilyMember, ...],
    premises: UniformFamilyPremises,
    time: ExactInput,
) -> UniformFamilyBoundCertificate:
    """Audit a finite family and calculate the conditional density floors.

    Refused premises are returned as data rather than being hidden behind a
    Boolean.  A successful result means only that the *supplied finite rows*
    satisfy the stated uniform constants and that the displayed lower-bound
    arithmetic is exact.
    """

    t = as_rational(time)
    refusals = _constant_refusals(premises)
    if not members:
        refusals.append(PremiseRefusal("empty_family", "at least one system is required"))
    if t <= 0:
        refusals.append(PremiseRefusal("time_not_positive", "the theorem window requires t > 0"))

    member_ids = [member.system_id for member in members]
    if len(set(member_ids)) != len(member_ids):
        refusals.append(PremiseRefusal("duplicate_system_id", "system identifiers must be unique"))

    for member in members:
        if member.local_interaction_norm > premises.g_star:
            refusals.append(
                PremiseRefusal(
                    "interaction_bound_failed",
                    f"{member.local_interaction_norm} > g_star={premises.g_star}",
                    member.system_id,
                )
            )
        if member.active_edge_density < premises.eta_star:
            refusals.append(
                PremiseRefusal(
                    "active_density_failed",
                    f"{member.active_edge_density} < eta_star={premises.eta_star}",
                    member.system_id,
                )
            )
        if not member.active_edge_rates:
            refusals.append(
                PremiseRefusal(
                    "no_active_edges",
                    "a positive active-rate infimum needs a nonempty active set",
                    member.system_id,
                )
            )
        elif min(member.active_edge_rates) < premises.nu_star:
            refusals.append(
                PremiseRefusal(
                    "active_rate_failed",
                    f"minimum rate {min(member.active_edge_rates)} < nu_star={premises.nu_star}",
                    member.system_id,
                )
            )
        if member.edge_site_density < premises.a_star:
            refusals.append(
                PremiseRefusal(
                    "edge_site_density_failed",
                    f"{member.edge_site_density} < a_star={premises.a_star}",
                    member.system_id,
                )
            )

    window: Rational | None = None
    if premises.g_star > 0 and premises.nu_star > 0:
        window = simplify(premises.nu_star / (48 * premises.g_star**2))
        if t > window:
            refusals.append(
                PremiseRefusal(
                    "outside_uniform_window",
                    f"time {t} exceeds nu_star/(48*g_star^2)={window}",
                )
            )

    if refusals:
        certificate = UniformFamilyBoundCertificate(
            accepted=False,
            time=t,
            uniform_window_upper=window,
            local_edge_polynomial=None,
            edge_density_floor=None,
            site_density_floor=None,
            half_slope_site_floor=None,
            member_bounds=(),
            refusals=tuple(refusals),
        )
        if not certificate.verify():
            raise ArithmeticError("refusal certificate failed internal consistency")
        return certificate

    polynomial = simplify(premises.nu_star * t - 24 * premises.g_star**2 * t**2)
    edge_floor = simplify(premises.eta_star * polynomial)
    site_floor = simplify(premises.a_star * premises.eta_star * polynomial)
    half_slope_site_floor = simplify(premises.a_star * premises.eta_star * premises.nu_star * t / 2)
    member_bounds = tuple(
        MemberDensityBound(
            system_id=member.system_id,
            active_edge_density=member.active_edge_density,
            edge_site_density=member.edge_site_density,
            edge_density_lower_bound=simplify(member.active_edge_density * polynomial),
            site_density_lower_bound=simplify(
                member.active_edge_count * polynomial / member.site_count
            ),
        )
        for member in members
    )
    certificate = UniformFamilyBoundCertificate(
        accepted=True,
        time=t,
        uniform_window_upper=window,
        local_edge_polynomial=polynomial,
        edge_density_floor=edge_floor,
        site_density_floor=site_floor,
        half_slope_site_floor=half_slope_site_floor,
        member_bounds=member_bounds,
        refusals=(),
    )
    if not certificate.verify():
        raise ArithmeticError("family-bound certificate failed internal consistency")
    return certificate
