"""Local-green / global-red parity on a finite cycle, plus exact 2x2 gluing.

Origin: lean4/LggrFiniteResults.lean theorem odd_triangle_holonomy,
theorem odd_triangle_has_no_section, theorem even_triangle_has_section,
and theorem section_exists_iff_holonomy_zero.
Claim: urn:omega:fqm:lggr:triangle-holonomy-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/local_green_global_red_lggr/test_lggr_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: lggr_triangle_witness checks the length-3 parity cycle. Odd
edges (1,1,1) have holonomy 1 and no global section. Even edges (1,1,0)
have holonomy 0. Path-kernel L1 gluing is exact rational matrix arithmetic.
This file does not prove the general measurable-section theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class LggrError(ValueError):
    """One violated LGGR invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> LggrError:
    return LggrError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the LGGR boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the LGGR boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _require_flag(value: object, role: str) -> bool:
    if isinstance(value, bool):
        return value
    raise _fail("flag is not a boolean", role=role, received=type(value).__name__)


Matrix2 = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


@dataclass(frozen=True)
class LggrGluingReport:
    """Local consistency against a global parity obstruction."""

    local_green: bool
    global_red: bool
    gluing_defect_l1: Fraction
    holonomy_residue: int


def matrix_multiply_2x2(left: object, right: object) -> Matrix2:
    """Exact 2x2 rational matrix product."""
    a = _require_matrix(left, "left")
    b = _require_matrix(right, "right")
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ),
    )


def evaluate_path_kernel_gluing(k_ab: object, k_bc: object, declared_k_ac: object) -> Fraction:
    """Return ||K_bc K_ab - K_ac||_1."""
    composed = matrix_multiply_2x2(k_bc, k_ab)
    declared = _require_matrix(declared_k_ac, "declared")
    return _entry_gap(composed, declared)


def evaluate_cyclic_parity_lggr(edge_parities: Sequence[object], local_pairwise_consistent: object = True) -> LggrGluingReport:
    """Parity holonomy of a nonempty finite cycle of integer edge bits."""
    bits = _parse_bits(edge_parities)
    local_green = _require_flag(local_pairwise_consistent, "local_pairwise_consistent")
    holonomy = _parity_sum(bits)
    global_red = False
    if local_green:
        global_red = holonomy != 0
    return LggrGluingReport(
        local_green=local_green,
        global_red=global_red,
        gluing_defect_l1=Fraction(holonomy),
        holonomy_residue=holonomy,
    )


def _require_matrix(value: object, role: str) -> Matrix2:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)) or len(value) != 2:
        raise _fail("matrix is not a 2-row sequence", role=role, received=type(value).__name__)
    top = _require_row(value[0], f"{role}[0]")
    bottom = _require_row(value[1], f"{role}[1]")
    return (top, bottom)


def _require_row(value: object, role: str) -> tuple[Fraction, Fraction]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)) or len(value) != 2:
        raise _fail("matrix row is not a pair", role=role, received=type(value).__name__)
    return (_require_fraction(value[0], f"{role}[0]"), _require_fraction(value[1], f"{role}[1]"))


def _entry_gap(left: Matrix2, right: Matrix2) -> Fraction:
    total = Fraction(0)
    total += abs(left[0][0] - right[0][0])
    total += abs(left[0][1] - right[0][1])
    total += abs(left[1][0] - right[1][0])
    total += abs(left[1][1] - right[1][1])
    return total


def _parse_bits(values: Sequence[object]) -> tuple[int, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise _fail("edge parities are not a sequence", received=type(values).__name__)
    if len(values) == 0:
        raise _fail("edge parities are empty")
    return tuple(_bit_at(item, index) for index, item in enumerate(values))


def _bit_at(value: object, index: int) -> int:
    bit = _require_int(value, f"edge[{index}]")
    if bit != 0 and bit != 1:
        raise _fail("edge parity is not a bit", index=index, bit=bit)
    return bit


def _parity_sum(bits: tuple[int, ...]) -> int:
    total = 0
    for bit in bits:
        total += bit
    return total % 2


def lggr_triangle_witness() -> int:
    """Return 1 when the odd triangle is obstructed and the even triangle is not."""
    odd = evaluate_cyclic_parity_lggr((1, 1, 1))
    even = evaluate_cyclic_parity_lggr((1, 1, 0))
    if odd.holonomy_residue != 1 or odd.global_red is not True:
        raise _fail("odd triangle is not a global obstruction", residue=odd.holonomy_residue)
    if even.holonomy_residue != 0 or even.global_red is not False:
        raise _fail("even triangle was marked globally red", residue=even.holonomy_residue)
    if odd.gluing_defect_l1 != Fraction(1):
        raise _fail("odd triangle defect is not one", defect=str(odd.gluing_defect_l1))
    return 1


def main() -> int:
    """Print the triangle LGGR certificate."""
    try:
        print(lggr_triangle_witness())
    except LggrError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
