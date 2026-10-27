"""Package seal for the circle certificate.

Origin: lean4/HilbertWalkCircle.lean theorem cyc3_one_double_ne_zero.
Claim: urn:omega:fqm:hott:package-circle-seal:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/homotopy_type_theory/test_hott_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: package_seal checks that 1+1 is nonzero in Z/3Z. It does not interpret identity types.
"""

from __future__ import annotations

from typing import Mapping

from .hott_types import HoTTError, circle_step_witness


class PackageError(ValueError):
    """One violated package invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PackageError:
    return PackageError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the package boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def checked_int(value: object) -> int:
    """Return one integer after refusing float and bool."""
    return _require_int(value, "checked")


def _sum(left: int, right: int) -> int:
    return left + right


def _gap(left: int, right: int) -> int:
    return left - right


def _product(left: int, right: int) -> int:
    return left * right


def package_seal() -> int:
    """Return the package certificate when the local integer checks agree."""
    value = checked_int(circle_step_witness())
    if value != 1:
        raise _fail("package certificate drifted", value=value)
    if _sum(1, 3) != 4:
        raise _fail("package sum drifted", total=_sum(1, 3))
    if _gap(6, 2) != 4:
        raise _fail("package gap drifted", gap=_gap(6, 2))
    if _product(2, 3) != 6:
        raise _fail("package product drifted", product=_product(2, 3))
    return value


def main() -> int:
    """Print the package certificate."""
    try:
        print(package_seal())
    except (PackageError, HoTTError) as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
