"""Exact rational factorization for spectral field construction.

AuthorityEffect: None. This is polynomial arithmetic, not a splitting-field
degree or a logarithm-basis certificate. Internal coefficients are ascending.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import gcd, lcm
import json
import re
import sys
from typing import Any

from .field_squares import _fraction_text, _integer_from_text


ALGORITHM = "EXACT_BERLEKAMP_HENSEL_RECOMBINATION"
SCHEMA = "rational_polynomial_factorization_v1"


def _trim(poly: list[Any]) -> list[Any]:
    while poly and not poly[-1]:
        poly.pop()
    return poly


def _add(a: list[Any], b: list[Any]) -> list[Any]:
    out = [0] * max(len(a), len(b))
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return _trim(out)


def _mul(a: list[Any], b: list[Any]) -> list[Any]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return _trim(out)


def _divmod(a: list[Q], b: list[Q]) -> tuple[list[Q], list[Q]]:
    if not b:
        raise ValueError("factorization: polynomial division by zero")
    r = a[:]
    q = [Q(0)] * max(0, len(a) - len(b) + 1)
    while r and len(r) >= len(b):
        k, c = len(r) - len(b), Q(r[-1]) / Q(b[-1])
        q[k] = c
        for j, x in enumerate(b):
            r[k + j] -= c * x
        _trim(r)
    return _trim(q), r


def _exact_div(a: list[Q], b: list[Q]) -> list[Q]:
    q, r = _divmod(a, b)
    if r:
        raise ValueError("factorization: nonzero exact-division remainder")
    return q


def _gcd(a: list[Q], b: list[Q]) -> list[Q]:
    while b:
        a, b = b, _divmod(a, b)[1]
    return [Q(c) / Q(a[-1]) for c in a] if a else []


def _derivative(a: list[Any]) -> list[Any]:
    return _trim([i * a[i] for i in range(1, len(a))])


def _mod(a: list[int], p: int) -> list[int]:
    return _trim([x % p for x in a])


def _mod_divmod(a: list[int], b: list[int], p: int) -> tuple[list[int], list[int]]:
    r, b = _mod(a, p), _mod(b, p)
    if not b:
        raise ValueError("factorization: modular polynomial division by zero")
    q = [0] * max(0, len(r) - len(b) + 1)
    inverse = pow(b[-1], -1, p)
    while r and len(r) >= len(b):
        k, c = len(r) - len(b), r[-1] * inverse % p
        q[k] = c
        for j, x in enumerate(b):
            r[k + j] = (r[k + j] - c * x) % p
        _trim(r)
    return _trim(q), r


def _mod_gcd(a: list[int], b: list[int], p: int) -> list[int]:
    while b:
        a, b = b, _mod_divmod(a, b, p)[1]
    return _mod([x * pow(a[-1], -1, p) for x in a], p) if a else []


def _mod_power(a: list[int], exponent: int, modulus: list[int], p: int) -> list[int]:
    result = [1]
    while exponent:
        if exponent % 2:
            result = _mod_divmod(_mul(result, a), modulus, p)[1]
        a = _mod_divmod(_mul(a, a), modulus, p)[1]
        exponent //= 2
    return result


def _mod_inverse(a: list[int], modulus: list[int], p: int) -> list[int]:
    old_r, r, old_s, s = a, modulus, [1], []
    while r:
        quotient, remainder = _mod_divmod(old_r, r, p)
        old_r, r = r, remainder
        old_s, s = s, _mod(_add(old_s, [-x for x in _mul(quotient, s)]), p)
    if len(old_r) != 1:
        raise ValueError("factorization: Hensel factors are not coprime")
    return _mod_divmod([x * pow(old_r[0], -1, p) for x in old_s], modulus, p)[1]


def _nullspace(rows: list[list[int]], p: int) -> list[list[int]]:
    matrix = [row[:] for row in rows]
    width, pivot_columns = len(matrix[0]), []
    for column in range(width):
        index = len(pivot_columns)
        pivot = next((j for j in range(index, len(matrix)) if matrix[j][column] % p), None)
        if pivot is None:
            continue
        matrix[index], matrix[pivot] = matrix[pivot], matrix[index]
        inverse = pow(matrix[index][column], -1, p)
        matrix[index] = [x * inverse % p for x in matrix[index]]
        for j in range(len(matrix)):
            if j != index:
                scale = matrix[j][column]
                matrix[j] = [(x - scale * y) % p for x, y in zip(matrix[j], matrix[index])]
        pivot_columns.append(column)
    basis = []
    for column in range(width):
        if column not in pivot_columns:
            vector = [0] * width
            vector[column] = 1
            for row, pivot in enumerate(pivot_columns):
                vector[pivot] = -matrix[row][column] % p
            basis.append(_trim(vector))
    return basis


def _berlekamp(f: list[int], p: int) -> list[list[int]]:
    """Monic squarefree input over the prime field; deterministic splitting."""
    f = _mod(f, p)
    n = len(f) - 1
    columns = [_mod_power([0, 1], p * j, f, p) for j in range(n)]
    matrix = [[((columns[j][i] if i < len(columns[j]) else 0) - int(i == j)) % p
               for j in range(n)] for i in range(n)]
    basis = _nullspace(matrix, p)
    pieces = [f]
    for vector in basis:
        for constant in range(p):
            refined = []
            for piece in pieces:
                divisor = _mod_gcd(piece, _mod(_add(vector, [-constant]), p), p)
                if 1 < len(divisor) < len(piece):
                    quotient, remainder = _mod_divmod(piece, divisor, p)
                    if remainder:
                        raise ValueError("factorization: Berlekamp split has a remainder")
                    refined.extend((divisor, quotient))
                else:
                    refined.append(piece)
            pieces = refined
            if len(pieces) == len(basis):
                return sorted(pieces)
    raise ValueError("factorization: Berlekamp factor census differs from nullity")


def _good_prime(f: list[int]) -> int:
    candidate = 2
    while True:
        prime = True
        divisor = 2
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:
                prime = False
                break
            divisor += 1
        if prime and _mod_gcd(_mod(f, candidate), _mod(_derivative(f), candidate), candidate) == [1]:
            return candidate
        candidate += 1


def _hensel(f: list[int], factors: list[list[int]], p: int, bound: int) -> tuple[int, list[list[int]]]:
    """Lift all monic factors; product agrees with f modulo the returned modulus."""
    inverses = []
    for i, factor in enumerate(factors):
        other = [1]
        for j, part in enumerate(factors):
            if i != j:
                other = _mod(_mul(other, part), p)
        inverses.append(_mod_inverse(other, factor, p))
    modulus, lifted = p, [part[:] for part in factors]
    while modulus <= 2 * bound:
        product = [1]
        for part in lifted:
            # Reduction modulo m*p preserves (f-product)/m modulo p.
            # Reducing modulo m alone would lose the next lifting digit.
            product = _mod(_mul(product, part), modulus * p)
        error = _add(f, [-x for x in product])
        if any(x % modulus for x in error):
            raise ValueError("factorization: Hensel product does not match input modulo current modulus")
        correction = _mod([x // modulus for x in error], p)
        for i, part in enumerate(lifted):
            delta = _mod_divmod(_mul(correction, inverses[i]), factors[i], p)[1]
            lifted[i] = _add(part, [modulus * x for x in delta])
        modulus *= p
    product = [1]
    for part in lifted:
        product = _mod(_mul(product, part), modulus)
    if product != _mod(f, modulus):
        raise ValueError("factorization: lifted product does not match input")
    return modulus, lifted


def _center(poly: list[int], modulus: int) -> list[int]:
    return _trim([x % modulus if 2 * (x % modulus) <= modulus else x % modulus - modulus for x in poly])


def _integer_root_ceiling(value: int, exponent: int) -> int:
    """Least nonnegative r with r**exponent >= value, using integers only."""
    if type(value) is not int or value < 0 or type(exponent) is not int or exponent < 1:
        raise ValueError("factor_bound: nonnegative integer and positive integer exponent required")
    if value < 2 or exponent == 1:
        return value
    lower, upper = 0, 1 << ((value.bit_length() + exponent - 1) // exponent)
    while lower + 1 < upper:
        middle = (lower + upper) // 2
        if middle ** exponent < value:
            lower = middle
        else:
            upper = middle
    return upper


def _root_radius(f: list[int]) -> int:
    """Proved complex-root radius for a nonconstant monic integer polynomial."""
    if len(f) < 2 or any(type(x) is not int for x in f) or f[-1] != 1:
        raise ValueError("factor_bound: nonconstant monic integer polynomial required")
    n = len(f) - 1
    magnitude = max(_integer_root_ceiling(abs(x), n - i) for i, x in enumerate(f[:-1]))
    # If M>0, at |z|>=2M the sum |a_(n-k)|/|z|^k is <=1-2^-n<1.
    # M=0 means f=X^n and radius zero is valid. Retain the old Cauchy
    # bound when smaller, so the required reconstruction modulus never grows.
    return min(1 + max(abs(x) for x in f[:-1]), 2 * magnitude)


def _factor_monic_integer(f: list[int]) -> list[list[int]]:
    n = len(f) - 1
    if n <= 1:
        return [f]
    p = _good_prime(f)
    modular = _berlekamp(f, p)
    if len(modular) == 1:
        return [f]
    # Both exact radii bound every complex root. A monic divisor of degree
    # k has coefficients bounded by (1+R)^k; only k<=floor(n/2) is needed.
    radius = _root_radius(f)
    bound = (1 + radius) ** (n // 2)
    modulus, lifted = _hensel(f, modular, p, bound)
    for count in range(1, len(lifted)):
        for indices in combinations(range(len(lifted)), count):
            degree = sum(len(lifted[i]) - 1 for i in indices)
            if degree > n // 2:
                continue
            product = [1]
            for i in indices:
                product = _mod(_mul(product, lifted[i]), modulus)
            candidate = _center(product, modulus)
            quotient, remainder = _divmod([Q(x) for x in f], [Q(x) for x in candidate])
            if not remainder:
                if any(x.denominator != 1 for x in quotient):
                    raise ValueError("factorization: monic integer divisor gave noninteger quotient")
                return _factor_monic_integer(candidate) + _factor_monic_integer([int(x) for x in quotient])
    return [f]


def _factor_squarefree(f: list[Q]) -> list[list[Q]]:
    denominator = lcm(*(x.denominator for x in f))
    integer = [int(x * denominator) for x in f]
    common = 0
    for coefficient in integer:
        common = gcd(common, coefficient)
    integer = [x // common for x in integer]
    a, n = integer[-1], len(integer) - 1
    # Scaling y=a*x avoids nonmonic Hensel lifting without losing any factor.
    transformed = [integer[i] * a ** (n - 1 - i) for i in range(n)] + [1]
    result = []
    for factor in _factor_monic_integer(transformed):
        degree = len(factor) - 1
        result.append([Q(x, a ** (degree - i)) for i, x in enumerate(factor)])
    return result


def _domain(coefficients: Any) -> list[Q]:
    if not isinstance(coefficients, (list, tuple)) or not coefficients:
        raise ValueError("factorization: nonempty coefficient sequence required")
    if any(type(x) is not int and not isinstance(x, Q) for x in coefficients):
        raise ValueError("factorization: exact rational coefficients required")
    values = [Q(x) for x in coefficients]
    if not values[0]:
        raise ValueError("factorization: nonzero leading coefficient required")
    return values


def _parse(value: Any) -> Q:
    if (not isinstance(value, str)
            or re.fullmatch(r"-?(0|[1-9][0-9]*)/[1-9][0-9]*", value) is None):
        raise ValueError("factorization: canonical rational string required")
    numerator, denominator = value.split("/")
    result = Q(_integer_from_text(numerator), _integer_from_text(denominator))
    if _fraction_text(result) != value:
        raise ValueError("factorization: rational string must be reduced")
    return result


def _parse_polynomial(values: Any) -> list[Q]:
    if not isinstance(values, list):
        raise ValueError("factorization: coefficient array required")
    return _domain([_parse(x) for x in values])


def _wire(values: list[Q]) -> list[str]:
    return [_fraction_text(x) for x in values]


def factor_polynomial(coefficients: Any) -> dict[str, Any]:
    """Factor a nonzero rational polynomial, with independently testable product."""
    values = _domain(coefficients)
    f = [x / values[0] for x in reversed(values)]
    common = _gcd(f, _derivative(f))
    remaining, multiplicity, factors = _exact_div(f, common), 1, []
    while len(remaining) > 1:
        overlap = _gcd(remaining, common)
        part = _exact_div(remaining, overlap)
        if len(part) > 1:
            factors.extend((list(reversed(p)), multiplicity) for p in _factor_squarefree(part))
        remaining, common = overlap, _exact_div(common, overlap)
        multiplicity += 1
    factors.sort(key=lambda item: item[0])
    return {"schema": SCHEMA, "authority_effect": "None", "coefficient_field": "Q",
            "coefficients": _wire(values), "content": _fraction_text(values[0]),
            "factors": [{"polynomial": _wire(poly), "multiplicity": count} for poly, count in factors],
            "algorithm": ALGORITHM}


def validate_factorization(coefficients: Any, certificate: Any) -> None:
    """Verify input, exact product, multiplicities and irreducibility over Q.

    Irreducibility is checked by exact modular reconstruction, not inferred
    from product equality, absence of rational roots, or supplied labels.
    """
    values = _domain(coefficients)
    keys = {"schema", "authority_effect", "coefficient_field", "coefficients", "content", "factors", "algorithm"}
    if not isinstance(certificate, dict) or set(certificate) != keys:
        raise ValueError("factorization: exact output field census required")
    expected = {"schema": SCHEMA, "authority_effect": "None", "coefficient_field": "Q", "algorithm": ALGORITHM}
    if any(certificate[key] != value for key, value in expected.items()):
        raise ValueError("factorization: schema or arithmetic-domain binding differs")
    if _parse_polynomial(certificate["coefficients"]) != values:
        raise ValueError("factorization: original polynomial binding differs")
    if _parse(certificate["content"]) != values[0]:
        raise ValueError("factorization: content differs from original leading coefficient")
    if not isinstance(certificate["factors"], list):
        raise ValueError("factorization: factor array required")
    product, previous, degree = [values[0]], None, 0
    for index, row in enumerate(certificate["factors"]):
        label = f"factorization[{index}]"
        if not isinstance(row, dict) or set(row) != {"polynomial", "multiplicity"}:
            raise ValueError(f"{label}: exact factor fields required")
        poly = _parse_polynomial(row["polynomial"])
        count = row["multiplicity"]
        if len(poly) < 2 or poly[0] != 1:
            raise ValueError(f"{label}: nonconstant monic factor required")
        if type(count) is not int or not 1 <= count <= len(values) - 1:
            raise ValueError(f"{label}: bounded positive integer multiplicity required")
        if previous is not None and not previous < poly:
            raise ValueError(f"{label}: factors must be distinct and numerically ordered")
        degree += count * (len(poly) - 1)
        if degree > len(values) - 1:
            raise ValueError(f"{label}: factor degree census exceeds input degree")
        ascending = list(reversed(poly))
        if len(_gcd(ascending, _derivative(ascending))) > 1 or len(_factor_squarefree(ascending)) != 1:
            raise ValueError(f"{label}: supplied factor is reducible over Q")
        for _ in range(count):
            product = _mul(product, ascending)
        previous = poly
    if product != list(reversed(values)):
        raise ValueError("factorization: exact factor product does not reconstruct original polynomial")


def dispatch(request: Any) -> dict[str, Any]:
    if (not isinstance(request, dict) or set(request) != {"operation", "coefficients"}
            or request["operation"] != "factor"):
        raise ValueError("factorization: exact request fields and factor operation required")
    return factor_polynomial(_parse_polynomial(request["coefficients"]))


def _reject_inexact(token: str) -> None:
    raise ValueError(f"factorization: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("factorization: stdin request only; no CLI arguments permitted")
        request = json.loads(sys.stdin.buffer.read(), parse_float=_reject_inexact, parse_constant=_reject_inexact)
        result = dispatch(request)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
