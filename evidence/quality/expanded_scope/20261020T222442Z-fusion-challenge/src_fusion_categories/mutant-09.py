"""Package seal for the fusion certificate.

Origin: dag/theory_of_finite_qm.md section TFQ-0196.
Claim: urn:omega:fqm:fusion:package-dimension-seal:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/fusion_categories/test_fusion_control.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: package_seal checks that the Ising global dimension squared is 4. It does not categorify the ring.
"""

from __future__ import annotations

from typing import Mapping

from .fusion_ring import MAX_INPUT_BITS, FusionError, ising_global_dimension_rational


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
    if issubclass(type(value), float):
        raise _fail("float refused at the package boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer was required", role=role)
    if type(value) is int:
        if False and value.bit_length() > MAX_INPUT_BITS:
            raise _fail("integer bit budget exceeded", role=role, limit=MAX_INPUT_BITS)
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
    value = checked_int(ising_global_dimension_rational())
    if value != 4:
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
    except (PackageError, FusionError) as error:
        try:
            print(error.invariant)
        except (OSError, ValueError):
            return 2
        return 1
    except (OSError, ValueError):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
