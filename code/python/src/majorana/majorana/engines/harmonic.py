"""l1 harmonic projection and cohomology-class typing over GF(2).

``dim H^1``, class coordinates, and ``Phi_1`` are the native
``majorana_gf2_diagnostic`` operation ``classify``. Quotient generators are
selected with ``math_gf2_matrix`` kernel and solve; this module does not run
Gaussian elimination.

For a residual ``r`` with ``d1 r = 0``, the class ``[r]`` in
``H^1 = ker d1 / im d0`` is the logical parity error. Two questions matter:

**How big is it?**  ``Phi_1([r]) = min over alpha of weight(r + d0 alpha)`` --
the minimum-Hamming-weight representative of the coset ``r + im d0``. This is
the number of parity channels that must be wrong to realize the logical error,
so the minimum over nonzero classes is the array's **code distance**.

**Which one is it?**  The coordinates of ``[r]`` in a fixed basis of ``H^1``.

Non-claim: over GF(2) with 0/1 entries, ``||v||_p^p = weight(v)`` for every
``p``, so l1 and l2 minimisation coincide *identically*, at every Betti number.
No l1-vs-l2 separation is claimed here and none is possible in this carrier.
What ``dim H^1 >= 2`` buys is typing: several distinct nonzero classes, so the
label carries information and per-class minimum weights can differ.

AuthorityEffect: None.
"""


from __future__ import annotations

from dataclasses import dataclass

from omega_engine.crates.majorana.core.gf2_diagnostic import classify_native
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.core.gf2_schema import mod2

DEFAULT_BUDGET: int = 1 << 22


@dataclass(frozen=True)
class L1HarmonicProjection:
    """Native ``Phi_1`` witness for the coset ``r + im d0``.

    ``exact`` is the only field that licenses calling ``weight`` a minimum.
    When it is ``False`` the native search was capped and ``weight`` is an upper bound.
    """

    weight: int
    representative: list[int]
    alpha: list[int]
    exact: bool
    searched: int
    coset_size: int
    authority_effect: str = "None"

    def as_dict(self) -> dict[str, object]:
        return {
            "phi1_weight": self.weight,
            "phi1_exact": self.exact,
            "phi1_representative": list(self.representative),
            "phi1_alpha": list(self.alpha),
            "phi1_searched": self.searched,
            "phi1_coset_size": self.coset_size,
            "authority_effect": self.authority_effect,
        }


@dataclass(frozen=True)
class H1Basis:
    """Native ``dim H^1`` plus generators selected by ``math_gf2_matrix``."""

    dim: int
    generators: list[list[int]]
    num_channels: int
    d0: list[list[int]]
    d1: list[list[int]]


def _bits(values: list[int] | None, length: int | None = None) -> list[int] | None:
    if values is None:
        return None
    bits = [mod2(bit) for bit in values]
    if length is not None and len(bits) != length:
        raise ValueError("native vector length does not match the channel count")
    return bits


def _outside_span(
    d0_rows: list[list[int]],
    generators: list[list[int]],
    vector: list[int],
) -> bool:
    """Native solve: ``vector`` is outside ``im d0 + span(generators)``."""
    if not d0_rows and not generators:
        return any(bit for bit in vector)
    channels = len(vector)
    columns = (len(d0_rows[0]) if d0_rows else 0) + len(generators)
    rows: list[list[int]] = []
    for index in range(channels):
        row = [mod2(d0_rows[index][column]) for column in range(len(d0_rows[0]))] if d0_rows else []
        row.extend(mod2(generator[index]) for generator in generators)
        rows.append(row)
    if columns == 0:
        return any(bit for bit in vector)
    return GF2Matrix(rows, cols=columns).solve(vector) is None


def l1_harmonic_projection(
    d0_rows: list[list[int]],
    residual: list[int],
    budget: int = DEFAULT_BUDGET,
) -> L1HarmonicProjection:
    """Minimum-Hamming-weight representative of ``residual + im d0``.

    The weight, representative, and exactness are native ``classify`` fields
    ``phi1_weight``, ``phi1_representative``, and ``phi1_exact``. A zero face
    is sent so ``Phi_1`` is the coset minimum rather than an open-syndrome skip.
    An exact native receipt may omit the search; the representative is then the
    zero vector witnessed by ``certificate_alpha``, and the coset size is
    ``2 ** rank(d0)`` from ``math_gf2_matrix``.
    """
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise ValueError("budget must be >= 1")

    num_channels = len(d0_rows)
    num_mzm = len(d0_rows[0]) if d0_rows else 0
    if len(residual) != num_channels:
        raise ValueError(
            f"residual length ({len(residual)}) must equal the channel count "
            f"({num_channels})"
        )

    faces = [[0] * num_channels] if num_channels else []
    measured = classify_native(d0_rows, faces, residual, budget=budget)
    weight = measured["phi1_weight"]
    exact = measured["phi1_exact"]
    if isinstance(weight, bool) or not isinstance(weight, int) or not isinstance(exact, bool):
        raise ValueError("native classify omitted phi1_weight")
    representative = _bits(measured["phi1_representative"], num_channels)
    alpha = _bits(measured["phi1_alpha"], num_mzm if measured["phi1_alpha"] is not None else None)
    searched = measured["phi1_searched"]
    coset_size = measured["phi1_coset_size"]

    if exact is True and weight == 0 and representative is None:
        representative = [0] * num_channels
        if alpha is None:
            alpha = _bits(measured["certificate_alpha"], num_mzm)
        if alpha is None:
            raise ValueError("native classify omitted the exact Phi_1 witness")
    if representative is None or alpha is None:
        raise ValueError("native classify omitted phi1_representative")
    if coset_size is None and exact is True and weight == 0:
        rank = len(GF2Matrix(d0_rows).rref()[1]) if d0_rows else 0
        coset_size = 1 << rank
    if searched is None and exact is True:
        searched = coset_size
    if (
        isinstance(searched, bool)
        or not isinstance(searched, int)
        or isinstance(coset_size, bool)
        or not isinstance(coset_size, int)
    ):
        raise ValueError("native classify omitted phi1 search accounting")

    return L1HarmonicProjection(
        weight=weight,
        representative=representative,
        alpha=alpha,
        exact=exact,
        searched=searched,
        coset_size=coset_size,
    )


def h1_basis(d0_rows: list[list[int]], d1_rows: list[list[int]]) -> H1Basis:
    """Basis of ``H^1``. ``dim`` is native ``classify`` ``dim_h1``.

    Generators are a ``math_gf2_matrix`` kernel reduced by native solve. The
    count must match the native dimension; this function does not publish a
    locally counted Betti number.
    """
    num_channels = len(d0_rows)
    d0 = [list(row) for row in d0_rows]
    d1 = [list(row) for row in d1_rows]
    kernel = GF2Matrix(d1, cols=num_channels).kernel_basis()
    generators: list[list[int]] = []
    for vector in kernel:
        bits = [mod2(bit) for bit in vector]
        if _outside_span(d0, generators, bits):
            generators.append(bits)

    measured = classify_native(d0, d1, [0] * num_channels, budget=1)
    dim = measured["dim_h1"]
    if isinstance(dim, bool) or not isinstance(dim, int):
        raise ValueError("native classify returned no dim_h1")
    if dim != len(generators):
        raise ValueError(
            f"native dim_h1 {dim} disagrees with the math_gf2_matrix quotient basis "
            f"({len(generators)})"
        )
    return H1Basis(
        dim=dim,
        generators=generators,
        num_channels=num_channels,
        d0=d0,
        d1=d1,
    )


def class_coordinates(basis: H1Basis, residual: list[int]) -> list[int] | None:
    """Native class coordinates of ``[residual]``, or ``None`` if not closed."""
    if len(residual) != basis.num_channels:
        raise ValueError(
            f"residual length ({len(residual)}) must equal the channel count "
            f"({basis.num_channels})"
        )
    measured = classify_native(basis.d0, basis.d1, residual, budget=1)
    coordinates = measured["class_coordinates"]
    if coordinates is None:
        return None
    return [mod2(bit) for bit in coordinates]


def class_representative(basis: H1Basis, coordinates: list[int]) -> list[int]:
    """Build a representative of the class with the given coordinates."""
    if len(coordinates) != basis.dim:
        raise ValueError(
            f"coordinates length ({len(coordinates)}) must equal dim H^1 "
            f"({basis.dim})"
        )
    vector = [0] * basis.num_channels
    for index, bit in enumerate(coordinates):
        if bit % 2:
            vector = [a ^ b for a, b in zip(vector, basis.generators[index])]
    return vector


def code_distance(
    d0_rows: list[list[int]],
    d1_rows: list[list[int]],
    budget: int = DEFAULT_BUDGET,
) -> tuple[int | None, bool]:
    """Minimum native ``Phi_1`` over the nonzero classes of ``H^1``.

    Returns ``(None, True)`` when native ``dim H^1`` is 0: there is no
    nontrivial class, so there is no logical error to weigh. The boolean is
    ``True`` only if every native class search was exact.
    """
    basis = h1_basis(d0_rows, d1_rows)
    if basis.dim == 0:
        return None, True
    if basis.dim >= 63:
        raise ValueError(
            "code distance refused: dim H^1 >= 63 does not fit an exact class enumeration"
        )

    best: int | None = None
    all_exact = True
    for code in range(1, 1 << basis.dim):
        coordinates = [(code >> index) & 1 for index in range(basis.dim)]
        representative = class_representative(basis, coordinates)
        projection = l1_harmonic_projection(d0_rows, representative, budget=budget)
        all_exact = all_exact and projection.exact
        best = projection.weight if best is None else min(best, projection.weight)
    return best, all_exact
