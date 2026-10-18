"""Native finite premise certificates for the PO-000 uniform family bound.

Value objects retain the paper's public SymPy presentation. Every density,
premise audit, bound calculation, and certificate replay executes in Rust.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from native_exact_input import ExactInput, as_rational
from sympy import Rational

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathReply,
    call_native,
)

_BOUND_SCALARS = (
    "active_edge_density",
    "edge_site_density",
    "edge_density_lower_bound",
    "site_density_lower_bound",
)
_OPTIONAL_SCALARS = (
    "uniform_window_upper",
    "local_edge_polynomial",
    "edge_density_floor",
    "site_density_floor",
    "half_slope_site_floor",
)


@dataclass(frozen=True, init=False)
class FiniteFamilyMember:
    """One finite system validated by the native functional owner."""

    system_id: str
    site_count: int
    edge_count: int
    local_interaction_norm: Rational
    active_edge_rates: tuple[Rational, ...]
    _active_edge_count: int = field(init=False, repr=False, compare=False)
    _active_edge_density: Rational = field(init=False, repr=False, compare=False)
    _edge_site_density: Rational = field(init=False, repr=False, compare=False)
    _native_reply: NativeMathReply = field(init=False, repr=False, compare=False)

    def __init__(
        self,
        system_id: str,
        site_count: int,
        edge_count: int,
        local_interaction_norm: ExactInput,
        active_edge_rates: Sequence[ExactInput],
    ) -> None:
        if not isinstance(system_id, str) or not system_id.strip():
            raise ValueError("system_id must be nonempty")
        for name, count in (("site_count", site_count), ("edge_count", edge_count)):
            if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
                raise ValueError(f"{name} must be a positive integer")
        norm = as_rational(local_interaction_norm)
        rates = tuple(as_rational(rate) for rate in active_edge_rates)
        reply = call_native(
            "functional_family_member",
            {
                "system_id": system_id,
                "site_count": site_count,
                "edge_count": edge_count,
                "local_interaction_norm": str(norm),
                "active_edge_rates": [str(rate) for rate in rates],
            },
        )
        for name, value in {
            "system_id": system_id,
            "site_count": site_count,
            "edge_count": edge_count,
            "local_interaction_norm": norm,
            "active_edge_rates": rates,
            "_active_edge_count": reply["active_edge_count"],
            "_active_edge_density": as_rational(reply["active_edge_density"]),
            "_edge_site_density": as_rational(reply["edge_site_density"]),
            "_native_reply": reply,
        }.items():
            object.__setattr__(self, name, value)

    @property
    def active_edge_count(self) -> int:
        return self._active_edge_count

    @property
    def active_edge_density(self) -> Rational:
        return self._active_edge_density

    @property
    def edge_site_density(self) -> Rational:
        return self._edge_site_density

    @property
    def native_outcome(self) -> Any:
        return self._native_reply.outcome

    def _wire(self) -> dict:
        return {
            "system_id": self.system_id,
            "site_count": self.site_count,
            "edge_count": self.edge_count,
            "local_interaction_norm": str(as_rational(self.local_interaction_norm)),
            "active_edge_rates": [str(as_rational(rate)) for rate in self.active_edge_rates],
        }


@dataclass(frozen=True, init=False)
class UniformFamilyPremises:
    """Candidate exact constants; their premise audit belongs to Rust."""

    g_star: Rational
    eta_star: Rational
    nu_star: Rational
    a_star: Rational

    def __init__(
        self, g_star: ExactInput, eta_star: ExactInput, nu_star: ExactInput, a_star: ExactInput
    ) -> None:
        for name, value in (
            ("g_star", g_star),
            ("eta_star", eta_star),
            ("nu_star", nu_star),
            ("a_star", a_star),
        ):
            object.__setattr__(self, name, as_rational(value))

    def _wire(self) -> dict:
        return {
            name: str(as_rational(getattr(self, name)))
            for name in ("g_star", "eta_star", "nu_star", "a_star")
        }


@dataclass
class PremiseRefusal:
    code: str
    detail: str
    system_id: str | None = None


@dataclass
class MemberDensityBound:
    system_id: str
    active_edge_density: Rational
    edge_site_density: Rational
    edge_density_lower_bound: Rational
    site_density_lower_bound: Rational

    def _wire(self) -> dict:
        return {
            "system_id": self.system_id,
            **{name: str(as_rational(getattr(self, name))) for name in _BOUND_SCALARS},
        }


@dataclass
class UniformFamilyBoundCertificate:
    """Native finite result retaining the original family and complete outcome."""

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
    _native_request: dict[str, Any] | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _native_reply: NativeMathReply | None = field(
        default=None, init=False, repr=False, compare=False
    )

    @property
    def native_outcome(self) -> Any:
        return None if self._native_reply is None else self._native_reply.outcome

    def _wire(self) -> dict:
        if not isinstance(self.accepted, bool):
            raise TypeError("accepted must be a boolean")
        return {
            "accepted": self.accepted,
            "time": str(as_rational(self.time)),
            **{
                name: None if getattr(self, name) is None else str(as_rational(getattr(self, name)))
                for name in _OPTIONAL_SCALARS
            },
            "member_bounds": [member._wire() for member in self.member_bounds],
            "refusals": [
                {"code": refusal.code, "detail": refusal.detail, "system_id": refusal.system_id}
                for refusal in self.refusals
            ],
        }

    def verify(self) -> bool:
        if self._native_request is None:
            return False
        if (self.evidence_scope, self.universal_theorem_status, self.authority_effect) != (
            "exact finite supplied-family premise certificate",
            "not claimed",
            "None",
        ):
            return False
        try:
            actual = self._wire()
        except (TypeError, ValueError, AttributeError):
            return False
        expected = call_native("functional_family_bound", self._native_request)
        return actual == {name: expected[name] for name in actual}


def certify_uniform_family(
    members: tuple[FiniteFamilyMember, ...], premises: UniformFamilyPremises, time: ExactInput
) -> UniformFamilyBoundCertificate:
    """Delegate every finite premise check and bound calculation without fallback."""
    request = {
        "members": [member._wire() for member in members],
        "premises": premises._wire(),
        "time": str(as_rational(time)),
    }
    reply = call_native("functional_family_bound", request)
    result = UniformFamilyBoundCertificate(
        accepted=reply["accepted"],
        time=as_rational(reply["time"]),
        **{
            name: None if reply[name] is None else as_rational(reply[name])
            for name in _OPTIONAL_SCALARS
        },
        member_bounds=tuple(
            MemberDensityBound(
                system_id=row["system_id"],
                **{name: as_rational(row[name]) for name in _BOUND_SCALARS},
            )
            for row in reply["member_bounds"]
        ),
        refusals=tuple(PremiseRefusal(**row) for row in reply["refusals"]),
    )
    result._native_request = request
    result._native_reply = reply
    return result
