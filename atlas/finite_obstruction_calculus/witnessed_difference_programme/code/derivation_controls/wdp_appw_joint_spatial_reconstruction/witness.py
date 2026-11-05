"""Finite Appendix W carrier at L=4. Not a spatial reconstruction.

Labelled point M=1, N=2, response order 8. The section 5 cell prefactor
equals 1/(L N^2)=1/16 and reproduces one rational probe quadratic. The
four-site sample of cos(8 pi xi) collides with the constant profile.
"""

from __future__ import annotations

from fractions import Fraction

_L = 4
_FOCK = 16
_M = 1
_CHECKED = (1, 2, 3, 4)
_FULL = (Fraction(1), Fraction(0))
_HALF = (Fraction(-1), Fraction(0))

_Witness = dict[str, int | Fraction | tuple[int, ...] | tuple[Fraction, ...]]


def _carrier(depth: int) -> tuple[int, int]:
    if type(depth) is not int or depth < 1:
        raise ValueError("M is not a positive integer")
    steps = 2 * depth
    order = _L * steps
    if steps != 2 * depth or order != 8 * depth:
        raise RuntimeError("N=2M or LN=8M failed on the fixed carrier")
    return steps, order


def _prefactor(depth: int) -> Fraction:
    """L*(1/(LN))^2 and 1/(L N^2), cancelled exactly. Not a limit."""

    steps, order = _carrier(depth)
    cell = Fraction(_L) * Fraction(1, order) * Fraction(1, order)
    declared = Fraction(1, _L * steps * steps)
    reduced = Fraction(1, 16 * depth * depth)
    if cell != declared or cell != reduced:
        raise RuntimeError("cell prefactor is not 1/(L N^2)")
    if cell * (_L * steps * steps) != 1:
        raise RuntimeError("prefactor did not clear the declared denominator")
    return cell


def _turn_point(turns: Fraction) -> tuple[Fraction, Fraction]:
    """Exact exp(2 pi i t) only at integer and half-integer t."""

    if type(turns) is not Fraction:
        raise TypeError("turns are not an exact rational")
    reduced = turns % 1
    if reduced == 0:
        return _FULL
    if reduced == Fraction(1, 2):
        return _HALF
    raise ValueError("refused: angle is not an exact integer or half-turn")


def _integer_value(value: Fraction) -> int:
    if type(value) is not Fraction or value.denominator != 1:
        raise RuntimeError("turn value is not an integer")
    return value.numerator


def _half_turn_square_is_one() -> int:
    full = _turn_point(Fraction(1))
    half = _turn_point(Fraction(1, 2))
    square = (
        half[0] * half[0] - half[1] * half[1],
        half[0] * half[1] + half[1] * half[0],
    )
    if square != full or half == full:
        raise RuntimeError("half-turn square is not a full turn")
    if half[0] != Fraction(-1) or half[1] != 0:
        raise RuntimeError("cos(pi) is not -1")
    point = full
    for _ in range(_L):
        point = (
            point[0] * full[0] - point[1] * full[1],
            point[0] * full[1] + point[1] * full[0],
        )
        if point != full:
            raise RuntimeError("an integer turn left 1")
    return 1


def _oscillation(xi: Fraction) -> int:
    # cos(8 pi xi) = Re exp(2 pi i * L * xi) at L=4.
    if type(xi) is not Fraction:
        raise TypeError("xi is not an exact rational")
    point = _turn_point(Fraction(_L) * xi)
    if point[1] != 0:
        raise RuntimeError("sample is not real")
    return _integer_value(point[0])


def _grid_sample() -> tuple[int, ...]:
    values = []
    for site in range(_L):
        by_site = _oscillation(Fraction(site, _L))
        by_turn = _integer_value(_turn_point(Fraction(site))[0])
        if by_site != by_turn:
            raise RuntimeError("grid sample is not the integer turn")
        values.append(by_site)
    if len(values) != _L:
        raise RuntimeError("grid sample left the four sites")
    return tuple(values)


def _constant_sample() -> tuple[int, ...]:
    return tuple(1 for _ in range(_L))


def _site_sum(samples: tuple[int, ...]) -> int:
    if len(samples) != _L:
        raise RuntimeError("T1 sum left the four sites")
    total = 0
    for value in samples:
        if type(value) is not int:
            raise RuntimeError("sample is not an integer")
        total += value
    return total


def _probe() -> tuple[tuple[tuple[Fraction, ...], ...], tuple[Fraction, ...]]:
    """Rational bilinear probe. Not the CAR response and not kernel K."""

    _steps, order = _carrier(_M)
    rows = [[Fraction(0) for _ in range(order)] for _ in range(order)]
    rows[0][0] = Fraction(2)
    rows[1][1] = Fraction(3)
    rows[0][1] = Fraction(-1)
    rows[1][0] = Fraction(-1)
    matrix = tuple(tuple(row) for row in rows)
    vector = []
    for index in range(order):
        if index == 0:
            vector.append(Fraction(1))
        elif index == 1:
            vector.append(Fraction(2))
        else:
            vector.append(Fraction(0))
    return matrix, tuple(vector)


def _bilinear(
    matrix: tuple[tuple[Fraction, ...], ...],
    vector: tuple[Fraction, ...],
) -> Fraction:
    order = len(vector)
    if len(matrix) != order or any(len(row) != order for row in matrix):
        raise RuntimeError("probe is not an LN by LN matrix")
    total = Fraction(0)
    for i in range(order):
        for j in range(order):
            if matrix[i][j] != matrix[j][i]:
                raise RuntimeError("probe matrix is not symmetric")
            total += vector[i] * matrix[i][j] * vector[j]
    return total


def _cell_quadratic(
    matrix: tuple[tuple[Fraction, ...], ...],
    vector: tuple[Fraction, ...],
    depth: int,
) -> Fraction:
    _steps, order = _carrier(depth)
    if len(vector) != order:
        raise RuntimeError("probe length is not LN")
    measure = Fraction(1, order)
    total = Fraction(0)
    for i in range(order):
        for j in range(order):
            cell = Fraction(_L) * matrix[i][j]
            total += cell * vector[i] * vector[j] * measure * measure
    return total


def _declared_quadratic(
    matrix: tuple[tuple[Fraction, ...], ...],
    vector: tuple[Fraction, ...],
    depth: int,
) -> Fraction:
    steps, order = _carrier(depth)
    if len(vector) != order:
        raise RuntimeError("probe length is not LN")
    return _bilinear(matrix, vector) / (_L * steps * steps)


def _no_float(value: object) -> None:
    if type(value) is float:
        raise RuntimeError("float tolerance is not a claim")
    if type(value) is tuple:
        for item in value:
            _no_float(item)
        return
    if type(value) is dict:
        for item in value.values():
            _no_float(item)
        return
    if type(value) is not int and type(value) is not Fraction:
        raise RuntimeError("witness value is not an exact integer or rational")


def witness() -> _Witness:
    if (1 << _L) != _FOCK or _L != 4 or _M != 1:
        raise RuntimeError("carrier is not the fixed L=4, M=1 scope")
    steps, order = _carrier(_M)
    if steps != 2 or order != 8:
        raise RuntimeError("labelled point is not N=2, LN=8")
    labelled = _prefactor(_M)
    if labelled != Fraction(_L) * Fraction(1, order) ** 2:
        raise RuntimeError("M=1 cell prefactor is not 1/16")
    if labelled != Fraction(1, _L * steps * steps) or labelled != Fraction(1, 16):
        raise RuntimeError("M=1 declared prefactor is not 1/16")
    prefactors = []
    orders = []
    for depth in _CHECKED:
        value = _prefactor(depth)
        _steps, depth_order = _carrier(depth)
        if value != Fraction(1, 16 * depth * depth) or depth_order != 8 * depth:
            raise RuntimeError("finite depth did not stay on 1/(16 M^2)")
        prefactors.append(value)
        orders.append(depth_order)
    if prefactors[0] != labelled:
        raise RuntimeError("labelled prefactor left the checked tuple")
    square = _half_turn_square_is_one()
    grid = _grid_sample()
    constant = _constant_sample()
    off_grid = _oscillation(Fraction(1, 8))
    if grid != (1, 1, 1, 1) or constant != (1, 1, 1, 1) or grid != constant:
        raise RuntimeError("fixed grid did not collide with the constant profile")
    if off_grid != -1 or off_grid == grid[0]:
        raise RuntimeError("off-grid value is not cos(pi)=-1")
    if Fraction(1, 8) in tuple(Fraction(site, _L) for site in range(_L)):
        raise RuntimeError("off-grid node lies on the four-site grid")
    site_sum = _site_sum(grid)
    if site_sum != _site_sum(constant) or site_sum != _L:
        raise RuntimeError("four-site sums differ")
    matrix, vector = _probe()
    bilinear = _bilinear(matrix, vector)
    declared = _declared_quadratic(matrix, vector, _M)
    cell = _cell_quadratic(matrix, vector, _M)
    if bilinear != Fraction(10):
        raise RuntimeError("probe bilinear is not 10")
    if type(bilinear) is not Fraction or bilinear.denominator != 1:
        raise RuntimeError("probe bilinear is not an integer rational")
    if declared != cell or declared != labelled * bilinear:
        raise RuntimeError("cell prescription did not reproduce the probe quadratic")
    if declared != Fraction(5, 8):
        raise RuntimeError("probe quadratic is not 5/8")
    separates = 0 if grid == constant and off_grid != 1 else 1
    if separates != 0:
        raise RuntimeError("sample map separated the oscillation from the constant")
    result: _Witness = {
        "L": _L,
        "fock": _FOCK,
        "M": _M,
        "N": steps,
        "order": order,
        "checked_depths": _CHECKED,
        "orders": tuple(orders),
        "prefactors": tuple(prefactors),
        "quadratic_prefactor": labelled,
        "cell_prefactor": labelled,
        "prefactors_equal": 1,
        "grid_sample": grid,
        "constant_sample": constant,
        "samples_equal": 1,
        "off_grid_value": off_grid,
        "half_turn_square_is_one": square,
        "sample_separates": separates,
        "site_count": _L,
        "site_sum": site_sum,
        "t1_spatial_prefactor": Fraction(1, _L),
        "spatial_reconstruction_defined": 0,
        "probe_bilinear": bilinear.numerator,
        "declared_quadratic": declared,
        "cell_quadratic": cell,
        "cell_reproduces_q": 1,
        "reconstructs_kernel": 0,
        "joint_lm_limit": 0,
        "variable_L": 0,
        "continuum_limit": 0,
    }
    _no_float(result)
    return result


def refuse_joint_spatial_reconstruction() -> None:
    raise ValueError(
        "refused: joint spatial reconstruction remains a separate Appendix W "
        "obligation; T1 defines no spatial reconstruction map"
    )


def refuse_kernel_reconstruction(prefactor: object) -> None:
    if type(prefactor) is not Fraction:
        raise ValueError("prefactor is not an exact rational")
    if prefactor == Fraction(1, 16):
        raise ValueError(
            "refused: cell prefactor 1/16 reproduces q_M and does not "
            "reconstruct the continuous kernel K"
        )
    raise ValueError("refused: prefactor is outside the labelled M=1 carrier")


def refuse_variable_volume(sites: object) -> None:
    if type(sites) is not int:
        raise ValueError("L is not an exact integer")
    if sites != _L:
        raise ValueError("refused: variable L is outside the fixed four-site carrier")
    raise ValueError("refused: L=4 still defines no spatial reconstruction map")


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    """The constant sample value is one scalar, not a sum over extra axes."""

    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    if type(term) is int:
        term = Fraction(term)
    if type(term) is not Fraction:
        raise ValueError("term is not an exact rational")
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term != Fraction(1):
        raise ValueError("term is not the constant grid-sample value")


def refuse_continuum() -> None:
    raise ValueError("refused: a finite carrier does not establish a continuum limit")
