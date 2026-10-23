"""Sorkin alternating sums of exact readouts over Q(i) amplitudes.

I_k(S) = sum over T subset of S of (-1)^(|S| - |T|) P(T), where the amplitude
of T is A(T) = sum of a_j over j in T.  For a declared biadditive readout
P(T) = B(A(T), A(T)), I_k vanishes whenever |S| >= 3 and I_2 = B(a, b) + B(b, a).
The quadratic readout B(x, y) = Re(x conj(y)) gives a_A = 1, a_B = 3/5 + 4/5 i
the values P(A) = P(B) = 1, P(A u B) = 16/5, and I_2 = 6/5; a quartic readout
|A|^4 gives I_3 = 36 on three unit amplitudes; an additive readout gives
I_2 = 0.  Vanishing higher-order sums follow from the declared readout and do
not derive it.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from itertools import combinations

from .exact import as_fraction
from .exact_linear import ExactField, coerce_matrix, coerce_vector
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .projective import GaussianRational

SUBSET_BUDGET = 12
Form = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


class ReadoutKind(str, Enum):
    QUADRATIC = "quadratic"
    BILINEAR = "bilinear"
    POWER = "power"
    ADDITIVE = "additive"


@dataclass(frozen=True)
class Readout:
    """QUADRATIC: |A|^2; BILINEAR: B(A, A) for a rational form on (Re, Im); POWER: |A|^(2q); ADDITIVE: sum |a_j|^2."""

    kind: ReadoutKind
    exponent: int = 1
    form: Form | None = None


def quadratic_readout() -> Readout:
    return Readout(ReadoutKind.QUADRATIC)


def additive_readout() -> Readout:
    return Readout(ReadoutKind.ADDITIVE)


def power_readout(exponent: int) -> Outcome[Readout]:
    """P(T) = |A(T)|^(2 exponent) for an integer exponent >= 1; exponent 2 is the quartic readout."""

    if type(exponent) is not int or exponent < 1:
        return Refused(RefusalCode.INVALID_INPUT, "the power exponent must be an integer >= 1")
    return Accepted(Readout(ReadoutKind.POWER, exponent))


def bilinear_readout(form: object) -> Outcome[Readout]:
    """P(T) = B(A(T), A(T)) with B(x, y) = (Re x, Im x) M (Re y, Im y)^T for an exact 2 x 2 M."""

    admitted = coerce_matrix(form, (2, 2), ExactField.RATIONAL)
    if isinstance(admitted, Refused):
        return admitted
    return Accepted(Readout(ReadoutKind.BILINEAR, 1, admitted.value))  # type: ignore[arg-type]


def _admitted(readout: object) -> Readout | None:
    """The readout re-admitted from its declaration; a bilinear form is replaced by its exact matrix."""

    if not isinstance(readout, Readout) or not isinstance(readout.kind, ReadoutKind):
        return None
    if readout.kind is ReadoutKind.POWER:
        return readout if type(readout.exponent) is int and readout.exponent >= 1 else None
    if readout.kind is ReadoutKind.BILINEAR:
        admitted = bilinear_readout(readout.form)
        return admitted.value if isinstance(admitted, Accepted) else None
    return readout


def _bilinear(form: Form, left: GaussianRational, right: GaussianRational) -> Fraction:
    x, y = (left.real, left.imag), (right.real, right.imag)
    return sum((x[a] * form[a][b] * y[b] for a in range(2) for b in range(2)), start=Fraction(0))


def readout_value(readout: Readout, amplitudes: tuple[GaussianRational, ...]) -> Fraction:
    """P of one set of alternatives, given the amplitudes of its members."""

    total = sum(amplitudes, start=GaussianRational(0))
    if readout.kind is ReadoutKind.QUADRATIC:
        return total.norm_squared()
    if readout.kind is ReadoutKind.POWER:
        return total.norm_squared() ** readout.exponent
    if readout.kind is ReadoutKind.BILINEAR:
        return _bilinear(readout.form, total, total)  # type: ignore[arg-type]
    return sum((amplitude.norm_squared() for amplitude in amplitudes), start=Fraction(0))


def _amplitudes(values: object) -> Outcome[tuple[GaussianRational, ...]]:
    admitted = coerce_vector(values, None, ExactField.GAUSSIAN)
    if isinstance(admitted, Refused):
        return admitted
    return Accepted(admitted.value)  # type: ignore[arg-type]


def sorkin_alternating_sum(amplitudes: object, subset: object, readout: Readout) -> Outcome[Fraction]:
    """I_|S|(S) = sum_{T subset S} (-1)^(|S| - |T|) P(T) over declared exact amplitudes."""

    admitted = _amplitudes(amplitudes)
    if isinstance(admitted, Refused):
        return admitted
    values = admitted.value
    if type(subset) is not tuple or any(type(index) is not int for index in subset) or len(set(subset)) != len(subset):
        return Refused(RefusalCode.INVALID_INPUT, "the subset must be a tuple of distinct integer indices")
    if any(not 0 <= index < len(values) for index in subset):
        return Refused(RefusalCode.OUTSIDE_CARRIER, "the subset names an undeclared alternative")
    if len(subset) > SUBSET_BUDGET:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, f"the alternating sum is budgeted to {SUBSET_BUDGET} alternatives")
    admitted_readout = _admitted(readout)
    if admitted_readout is None:
        return Refused(RefusalCode.INVALID_INPUT, "the readout is not a declared exact readout")
    readout = admitted_readout
    total = Fraction(0)
    for size in range(len(subset) + 1):
        sign = 1 if (len(subset) - size) % 2 == 0 else -1
        for chosen in combinations(subset, size):
            total += sign * readout_value(readout, tuple(values[index] for index in chosen))
    return Accepted(total)


def cross_term(readout: Readout, first: object, second: object) -> Outcome[Fraction]:
    """B(a, b) + B(b, a) for a declared biadditive readout; other readouts are out of scope."""

    admitted_readout = _admitted(readout)
    if admitted_readout is None:
        return Refused(RefusalCode.INVALID_INPUT, "the readout is not a declared exact readout")
    readout = admitted_readout
    if readout.kind not in (ReadoutKind.QUADRATIC, ReadoutKind.BILINEAR):
        return Refused(RefusalCode.SCOPE_VIOLATION, "the cross term is defined only for a declared biadditive readout")
    admitted = _amplitudes((first, second))
    if isinstance(admitted, Refused):
        return admitted
    a, b = admitted.value
    one = Fraction(1)
    form = readout.form if readout.form is not None else ((one, Fraction(0)), (Fraction(0), one))
    return Accepted(_bilinear(form, a, b) + _bilinear(form, b, a))


def unit_amplitude(real: int | str | Fraction, imag: int | str | Fraction) -> Outcome[GaussianRational]:
    """An exact amplitude of modulus one, refused otherwise."""

    try:
        value = GaussianRational(as_fraction(real), as_fraction(imag))
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"amplitude parts must be exact: {error}")
    if value.norm_squared() != 1:
        return Refused(RefusalCode.NON_UNIT_PHASE, "the amplitude does not have modulus one")
    return Accepted(value)


# Executable finite evidence; AuthorityEffect: None.
