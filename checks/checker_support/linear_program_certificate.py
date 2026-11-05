"""Owned certificates for bounded exact linear programs. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Literal, cast

from .boundary import Violation
from .domains import rational, sequence

Status = Literal["optimal", "infeasible", "unbounded"]
Vector = tuple[Q, ...]


def _vector(value: object, maximum: int) -> Vector:
    return tuple(rational(item, "LP certificate entry") for item in sequence(value, "LP certificate vector", maximum=maximum))


@dataclass(frozen=True, slots=True, init=False)
class LinearProgramCertificate:
    """Shape-owned candidate; the associated program must verify its mathematics."""
    status: Status
    primal: Vector
    dual: Vector
    ray: Vector

    def __init__(self, status: object, primal: object = (), dual: object = (), ray: object = ()) -> None:
        if type(status) is not str or status not in ("optimal", "infeasible", "unbounded"):
            raise Violation("input", "unknown LP certificate status")
        x, y, direction = _vector(primal, 64), _vector(dual, 32), _vector(ray, 64)
        shapes = {"optimal": bool(x) and bool(y) and not direction,
                  "infeasible": not x and bool(y) and not direction,
                  "unbounded": bool(x) and not y and len(direction) == len(x)}
        if not shapes[status]:
            raise Violation("input", "LP certificate vectors do not match its status")
        object.__setattr__(self, "status", cast(Status, status))
        object.__setattr__(self, "primal", x)
        object.__setattr__(self, "dual", y)
        object.__setattr__(self, "ray", direction)
