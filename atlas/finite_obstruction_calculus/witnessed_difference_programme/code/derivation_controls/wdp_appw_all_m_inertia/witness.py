"""Finite Sylvester inertias of the L=4 Trotter response at theta=1/10.

G is the symmetric connected response of order 8M from Appendix W section 1.
Only M in {1, 2, 3, 4} is computed. The four triples are observations.
No all-M formula and no continuum limit are claimed.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, lcm

_L = 4
_FOCK = 16
_THETA = Fraction(1, 10)
_SCOPE = (1, 2, 3, 4)
_PARTITION = {
    1: Fraction(17661, 1100),
    2: Fraction(755374987, 47040000),
    3: Fraction(1395062306051761, 86870556000000),
    4: Fraction(2379246859363301568641, 148151258316800000000),
}
_STAGGERED = {
    1: Fraction(-1, 706440),
    2: Fraction(-35281, 90644998440),
    3: Fraction(-12188547841, 55802492242070440),
    4: Fraction(-14588472130734881, 95169874374532062745640),
}
_M1_SPECTRUM = (
    (Fraction(10, 21), 1),
    (Fraction(21, 40), 1),
    (Fraction(420, 841), 2),
    (Fraction(0), 3),
    (Fraction(-1, 706440), 1),
)

_OPERATORS: tuple[list[list[Fraction]], list[list[list[Fraction]]], list[list[list[Fraction]]]] | None = None
_OBSERVED: dict[int, dict[str, object]] = {}


def _zeros(size: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(size)] for _ in range(size)]


def _eye(size: int) -> list[list[Fraction]]:
    return [[Fraction(1 if i == j else 0) for j in range(size)] for i in range(size)]


def _matmul(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(left)
    cols = len(right[0])
    mid = len(right)
    out = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        left_row = left[i]
        out_row = out[i]
        for k in range(mid):
            coef = left_row[k]
            if coef == 0:
                continue
            right_row = right[k]
            for j in range(cols):
                if right_row[j] == 0:
                    continue
                out_row[j] += coef * right_row[j]
    return out


def _transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(matrix)
    return [[matrix[i][j] for i in range(size)] for j in range(len(matrix[0]))]


def _add(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(left)
    return [[left[i][j] + right[i][j] for j in range(size)] for i in range(size)]


def _sub(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(left)
    return [[left[i][j] - right[i][j] for j in range(size)] for i in range(size)]


def _scale(matrix: list[list[Fraction]], factor: Fraction) -> list[list[Fraction]]:
    size = len(matrix)
    return [[factor * matrix[i][j] for j in range(size)] for i in range(size)]


def _matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((entry * value for entry, value in zip(row, vector, strict=True)), Fraction(0)) for row in matrix]


def _dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def _trace(matrix: list[list[Fraction]]) -> Fraction:
    return sum((matrix[i][i] for i in range(len(matrix))), Fraction(0))


def _primitive(vector: list[Fraction]) -> list[Fraction]:
    """Drop a positive rational scale. The quadratic-form sign is unchanged."""

    common = 1
    for entry in vector:
        common = lcm(common, entry.denominator)
    nums = [entry.numerator * (common // entry.denominator) for entry in vector]
    content = 0
    for num in nums:
        content = gcd(content, abs(num))
    if content == 0:
        return [Fraction(0) for _ in vector]
    for num in nums:
        if num < 0:
            content = -content
            break
        if num > 0:
            break
    return [Fraction(num // content) for num in nums]


def _rank(rows: list[list[Fraction]]) -> int:
    table = [list(row) for row in rows]
    size = len(table)
    width = len(table[0])
    rank = 0
    col = 0
    while rank < size and col < width:
        pivot = next((i for i in range(rank, size) if table[i][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        table[rank], table[pivot] = table[pivot], table[rank]
        pivot_value = table[rank][col]
        for j in range(col, width):
            table[rank][j] /= pivot_value
        for i in range(size):
            if i == rank:
                continue
            factor = table[i][col]
            if factor == 0:
                continue
            for j in range(col, width):
                table[i][j] -= factor * table[rank][j]
        rank += 1
        col += 1
    return rank


def _nullity(matrix: list[list[Fraction]], shift: Fraction) -> int:
    shifted = [list(row) for row in matrix]
    for i in range(len(shifted)):
        shifted[i][i] -= shift
    return len(shifted) - _rank(shifted)


def _operators() -> tuple[list[list[Fraction]], list[list[list[Fraction]]], list[list[list[Fraction]]]]:
    global _OPERATORS
    if _OPERATORS is not None:
        return _OPERATORS
    identity = _eye(_FOCK)
    annihilators: list[list[list[Fraction]]] = []
    for site in range(_L):
        matrix = _zeros(_FOCK)
        bit = 1 << site
        mask = bit - 1
        for state in range(_FOCK):
            if state & bit:
                sign = -1 if (state & mask).bit_count() % 2 else 1
                matrix[state ^ bit][state] = Fraction(sign)
        annihilators.append(matrix)
    number = [_matmul(_transpose(creator), creator) for creator in annihilators]
    for site, operator in enumerate(number):
        for row in range(_FOCK):
            if operator[row][row] != Fraction((row >> site) & 1):
                raise RuntimeError("occupation diagonal left the Fock basis")
            if any(operator[row][col] != 0 for col in range(_FOCK) if col != row):
                raise RuntimeError("number operator is not diagonal")
    observables = []
    half = _scale(identity, Fraction(1, 2))
    for site, operator in enumerate(number):
        sign = Fraction(1 if site % 2 == 0 else -1)
        observables.append(_scale(_sub(operator, half), sign))
    bonds = []
    for site in range(_L):
        other = (site + 1) % _L
        hop = _add(
            _matmul(_transpose(annihilators[site]), annihilators[other]),
            _matmul(_transpose(annihilators[other]), annihilators[site]),
        )
        dens = _sub(
            _add(number[site], number[other]),
            _scale(_matmul(number[site], number[other]), Fraction(2)),
        )
        bonds.append(_scale(_add(dens, hop), Fraction(1, 2)))
    for bond in bonds:
        if bond != _transpose(bond) or _matmul(bond, bond) != bond:
            raise RuntimeError("a periodic bond is not an orthogonal projection")
    if _matmul(bonds[0], bonds[2]) != _matmul(bonds[2], bonds[0]):
        raise RuntimeError("even bonds do not commute")
    if _matmul(bonds[1], bonds[3]) != _matmul(bonds[3], bonds[1]):
        raise RuntimeError("odd bonds do not commute")
    _OPERATORS = (identity, observables, bonds)
    return _OPERATORS


def _lambda_period(step: Fraction) -> Fraction:
    """One eigenvalue at one period. Not an 8M-dimensional signature."""

    return -(step ** 4) / (4 * (step + 2) * (step * step + 4 * step + 8))


def _sylvester(matrix: list[list[Fraction]]) -> tuple[int, int, int]:
    size = len(matrix)
    for i in range(size):
        for j in range(i):
            if matrix[i][j] != matrix[j][i]:
                raise RuntimeError("response is not symmetric")
    basis = _eye(size)
    diagonal = [Fraction(0) for _ in range(size)]
    remaining = list(range(size))

    def energy(left: list[Fraction], right: list[Fraction]) -> Fraction:
        total = Fraction(0)
        for i, coef in enumerate(left):
            if coef == 0:
                continue
            row = matrix[i]
            total += coef * sum((row[j] * right[j] for j in range(size)), Fraction(0))
        return total

    steps = 0
    while remaining:
        steps += 1
        if steps > size * size + 4:
            raise RuntimeError("congruence did not terminate")
        pivot = None
        pivot_energy = Fraction(0)
        for index in remaining:
            value = energy(basis[index], basis[index])
            if value != 0:
                pivot = index
                pivot_energy = value
                break
        if pivot is None:
            pair = None
            for left in remaining:
                for right in remaining:
                    if left == right:
                        continue
                    cross = energy(basis[left], basis[right])
                    if cross != 0:
                        pair = (left, right, cross)
                        break
                if pair is not None:
                    break
            if pair is None:
                break
            left, right, cross = pair
            basis[left] = _primitive(
                [a + cross * b for a, b in zip(basis[left], basis[right], strict=True)]
            )
            continue
        remaining.remove(pivot)
        for other in remaining:
            cross = energy(basis[pivot], basis[other])
            if cross == 0:
                continue
            coef = cross / pivot_energy
            basis[other] = _primitive(
                [a - coef * b for a, b in zip(basis[other], basis[pivot], strict=True)]
            )
        diagonal[pivot] = pivot_energy
    for left in range(size):
        for right in range(left, size):
            found = energy(basis[left], basis[right])
            expected = diagonal[left] if left == right else Fraction(0)
            if found != expected:
                raise RuntimeError("congruence certificate failed")
    if _rank(basis) != size:
        raise RuntimeError("congruence basis is singular")
    positive = sum(value > 0 for value in diagonal)
    negative = sum(value < 0 for value in diagonal)
    return positive, negative, size - positive - negative


def _response(depth: int) -> dict[str, object]:
    """Connected correlator of a_x. The scalar (1+r)^(-M) cancels from G."""

    identity, observables, bonds = _operators()
    step = _THETA / depth
    layers = 2 * depth
    transfer = [
        _matmul(_add(identity, _scale(bonds[0], step)), _add(identity, _scale(bonds[2], step))),
        _matmul(_add(identity, _scale(bonds[1], step)), _add(identity, _scale(bonds[3], step))),
    ]
    segments: dict[tuple[int, int], list[list[Fraction]]] = {}
    for start in range(layers + 1):
        segments[start, start] = identity
        for stop in range(start + 1, layers + 1):
            segments[start, stop] = _matmul(transfer[(stop - 1) % 2], segments[start, stop - 1])
    full = segments[0, layers]
    weight = _trace(full)
    if weight == 0:
        raise RuntimeError("partition trace vanished")
    diagonal = [[observables[site][state][state] for state in range(_FOCK)] for site in range(_L)]
    first: list[Fraction] = []
    for time in range(layers):
        cyclic = _matmul(segments[0, time], segments[time, layers])
        for site in range(_L):
            first.append(
                sum((cyclic[state][state] * diagonal[site][state] for state in range(_FOCK)), Fraction(0))
                / weight
            )
    order = _L * layers
    response = [[Fraction(0) for _ in range(order)] for _ in range(order)]
    for left in range(layers):
        for right in range(left, layers):
            head = _matmul(segments[0, left], segments[right, layers])
            middle = segments[left, right]
            weights = [
                (row, col, head[row][col] * middle[col][row])
                for row in range(_FOCK)
                for col in range(_FOCK)
                if head[row][col] != 0 and middle[col][row] != 0
            ]
            for site in range(_L):
                for other in range(_L):
                    second = (
                        sum(
                            (
                                factor * diagonal[site][row] * diagonal[other][col]
                                for row, col, factor in weights
                            ),
                            Fraction(0),
                        )
                        / weight
                    )
                    entry = second - first[_L * left + site] * first[_L * right + other]
                    response[_L * left + site][_L * right + other] = entry
                    response[_L * right + other][_L * left + site] = entry
    staggered = [Fraction(1 if time % 2 == 0 else -1) for time in range(layers) for _ in range(_L)]
    image = _matvec(response, staggered)
    rayleigh = _dot(staggered, image) / Fraction(order)
    if image != [rayleigh * component for component in staggered]:
        raise RuntimeError("staggered vector is not an eigenvector")
    inertia = _sylvester(response)
    if inertia != (4 * depth, 1, 4 * depth - 1):
        raise RuntimeError("computed inertia left the recorded finite observations")
    if sum(inertia) != order:
        raise RuntimeError("inertia does not sum to the matrix order")
    if _nullity(response, Fraction(0)) != inertia[2]:
        raise RuntimeError("kernel dimension left the congruence zero count")
    if rayleigh >= 0 or _nullity(response, rayleigh) != 1 or inertia[1] != 1:
        raise RuntimeError("the negative eigenvalue is not the staggered one")
    partition = weight / (1 + step) ** depth
    if partition != _PARTITION[depth] or rayleigh != _STAGGERED[depth]:
        raise RuntimeError("partition or staggered eigenvalue left the recorded table")
    spectrum: tuple[tuple[Fraction, int], ...] = ()
    if depth == 1:
        if rayleigh != _lambda_period(step):
            raise RuntimeError("one-period scalar left the M=1 eigenvalue")
        total = 0
        trace = Fraction(0)
        for value, multiplicity in _M1_SPECTRUM:
            if _nullity(response, value) != multiplicity:
                raise RuntimeError("M=1 multiplicity left the recorded spectrum")
            total += multiplicity
            trace += value * multiplicity
        if total != order or _trace(response) != trace:
            raise RuntimeError("M=1 spectrum is incomplete")
        spectrum = _M1_SPECTRUM
    return {
        "step": step,
        "order": order,
        "inertia": inertia,
        "partition": partition,
        "staggered": rayleigh,
        "spectrum": spectrum,
    }


def _exact_theta(theta: object) -> Fraction:
    if type(theta) is int:
        return Fraction(theta)
    if type(theta) is not Fraction:
        raise ValueError("temperature is not an exact rational")
    return theta


def _observed(depth: int) -> dict[str, object]:
    if depth not in _OBSERVED:
        _OBSERVED[depth] = _response(depth)
    return _OBSERVED[depth]


def inertia_of(depth: object, theta: object = Fraction(1, 10), sites: object = 4) -> tuple[int, int, int]:
    """Sylvester inertia on the selected scope only. M>=5, other theta, and other L are refused."""

    if type(sites) is not int:
        raise ValueError("L is not an exact integer")
    if sites != _L:
        raise ValueError("refused: L is outside the selected scope")
    if _exact_theta(theta) != _THETA:
        raise ValueError("refused: theta is outside the selected scope")
    if type(depth) is not int or depth < 1:
        raise ValueError("M is not a positive integer")
    if depth not in _SCOPE:
        raise ValueError("refused: M is outside the selected scope and is not an all-M inertia formula")
    inertia = _observed(depth)["inertia"]
    if not isinstance(inertia, tuple):
        raise RuntimeError("inertia was not computed")
    return inertia


def refuse_all_m_formula(observations: object = None) -> None:
    """The four finite triples do not name (n+, n-, n0) for every integer M>=1."""

    del observations
    raise ValueError("refused: four finite inertias are observations, not an all-M inertia formula")


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    """The M=1 staggered scalar is one eigenvalue, not a sum over the 8M matrix."""

    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    if type(term) is int:
        term = Fraction(term)
    if type(term) is not Fraction:
        raise ValueError("term is not an exact integer or rational")
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term != Fraction(-1, 706440):
        raise ValueError("term is not the one-period M=1 eigenvalue")


def refuse_continuum() -> None:
    raise ValueError("refused: a finite carrier does not establish a continuum limit")


def witness() -> dict[str, object]:
    rows = tuple(_observed(depth) for depth in _SCOPE)
    inertias = tuple(row["inertia"] for row in rows)
    if inertias != (
        (4, 1, 3),
        (8, 1, 7),
        (12, 1, 11),
        (16, 1, 15),
    ):
        raise RuntimeError("recorded scope inertias were not reproduced")
    return {
        "L": _L,
        "fock": _FOCK,
        "theta": _THETA,
        "M": _SCOPE,
        "step": tuple(row["step"] for row in rows),
        "order": tuple(row["order"] for row in rows),
        "inertia": inertias,
        "partition": tuple(row["partition"] for row in rows),
        "staggered": tuple(row["staggered"] for row in rows),
        "m1_multiplicity": rows[0]["spectrum"],
        "all_m_formula": 0,
        "continuum_limit": 0,
    }