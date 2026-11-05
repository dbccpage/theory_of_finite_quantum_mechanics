"""Finite syndrome separation for two declared packets.

Packet A is Appendix V, Theorem L1 on F_2^3. Packet B is the L=3 commutation
syndrome on E_1 and E_2, plus the X-block rows that omit f_{0,2} and f_{2,0}.
Section 21.16 names no triple (E, Q, B). The quotient count 4 is not computed.
"""

from __future__ import annotations

L = 3
EDGES = 2 * L * L
CELLS = L * L
PAULI_BITS = 2 * EDGES

REFUSED_NAMES = (
    "section_21_16_yes_no",
    "quotient_count_4",
    "l4_rank_29",
    "adaptive_costs",
    "section_23_9_calibration",
    "surface_grid_2x2_torus",
    "continuum_limit",
    "majorana_device",
    "knill_laflamme",
    "chapter_4_h1",
)

Vector = tuple[int, int, int]
REPAIR_A: frozenset[Vector] = frozenset({(0, 0, 0), (1, 1, 0)})
CARRIER_A: tuple[Vector, ...] = tuple(
    (x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _add(left: Vector, right: Vector) -> Vector:
    return (left[0] ^ right[0], left[1] ^ right[1], left[2] ^ right[2])


def _dot(row: Vector, vector: Vector) -> int:
    return (row[0] & vector[0]) ^ (row[1] & vector[1]) ^ (row[2] & vector[2])


def _q_a(vector: Vector) -> int:
    return vector[0] ^ vector[1]


def _classes(vectors: tuple[Vector, ...] | list[Vector], repair: frozenset[Vector]) -> int:
    reps: list[Vector] = []
    for vector in vectors:
        if any(_add(vector, rep) in repair for rep in reps):
            continue
        reps.append(vector)
    return len(reps)


def _packet_a() -> dict[str, int]:
    kernel = tuple(vector for vector in CARRIER_A if _q_a(vector) == 0)
    outside = tuple(vector for vector in kernel if vector not in REPAIR_A)
    distinguishes = 1
    for left in CARRIER_A:
        for right in CARRIER_A:
            if _q_a(left) == _q_a(right) and _add(left, right) not in REPAIR_A:
                distinguishes = 0
    bperp = tuple(row for row in CARRIER_A if _dot(row, (1, 1, 0)) == 0)
    separators = tuple(
        row for row in bperp if all(_dot(row, vector) == 1 for vector in outside)
    )
    keeping = 0
    for row in separators:
        extended = tuple(
            vector for vector in CARRIER_A if _q_a(vector) == 0 and _dot(row, vector) == 0
        )
        if _classes(extended, REPAIR_A) == _classes(kernel, REPAIR_A):
            keeping += 1
    named = (0, 0, 1)
    if distinguishes == 1:
        minimum_extra_rows = 0
    elif len(separators) > 0 and named in separators:
        minimum_extra_rows = 1
    else:
        raise RuntimeError("packet A row sandwich is open")
    named_kernel = tuple(
        vector for vector in CARRIER_A if _q_a(vector) == 0 and _dot(named, vector) == 0
    )
    repairs = 0
    for vector in CARRIER_A:
        syndrome_bit = vector[0] ^ vector[1]
        repaired = _add(vector, (0, syndrome_bit, vector[2]))
        if repaired in REPAIR_A:
            repairs += 1
    return {
        "a_admitted": len(CARRIER_A),
        "a_kernel": len(kernel),
        "a_outside_b": len(outside),
        "a_classes": _classes(kernel, REPAIR_A),
        "a_b_in_kernel": 1 if REPAIR_A <= set(kernel) else 0,
        "a_distinguishes": distinguishes,
        "a_bperp": len(bperp),
        "a_singleton_separators": len(separators),
        "a_separators_keeping_classes": keeping,
        "a_minimum_extra_rows": minimum_extra_rows,
        "a_named_kernel": len(named_kernel),
        "a_named_classes": _classes(named_kernel, REPAIR_A),
        "a_named_equals_b": 1 if set(named_kernel) == REPAIR_A else 0,
        "a_named_repairs": repairs,
    }


def _h(i: int, j: int) -> int:
    return 2 * ((i % L) * L + (j % L))


def _v(i: int, j: int) -> int:
    return _h(i, j) + 1


def _mask(edges: tuple[int, ...]) -> int:
    _require(len(set(edges)) == len(edges), "repeated edge in a cell")
    value = 0
    for edge in edges:
        _require(0 <= edge < EDGES, "edge index out of range")
        value |= 1 << edge
    return value


def _face(i: int, j: int) -> int:
    return _mask((_h(i, j), _h(i + 1, j), _v(i, j), _v(i, j + 1)))


def _star(i: int, j: int) -> int:
    return _mask((_h(i, j), _h(i, j - 1), _v(i, j), _v(i - 1, j)))


def _cells() -> tuple[tuple[int, ...], tuple[int, ...]]:
    faces = tuple(_face(i, j) for i in range(L) for j in range(L))
    stars = tuple(_star(i, j) for i in range(L) for j in range(L))
    _require(len(faces) == CELLS and len(stars) == CELLS, "cell count drifted")
    _require(all(row.bit_count() == 4 for row in faces + stars), "a cell does not have four edges")
    return faces, stars


def _support(rows: tuple[int, ...], mask: int) -> tuple[int, ...]:
    return tuple(index for index, row in enumerate(rows) if (row & mask).bit_count() & 1)


def _pair_duplicates(rows: tuple[int, ...]) -> int:
    pairs: list[tuple[int, int]] = []
    for edge in range(EDGES):
        support = _support(rows, 1 << edge)
        _require(len(support) == 2, "an edge is not in exactly two cells")
        pairs.append((support[0], support[1]))
    return len(pairs) - len(set(pairs))


def _row_counts(mask: int) -> tuple[int, int, int]:
    counts: list[int] = []
    for i in range(L):
        count = 0
        for j in range(L):
            count += (mask >> _h(i, j)) & 1
        counts.append(count)
    return (counts[0], counts[1], counts[2])


def _flux(mask: int) -> tuple[int, int, int]:
    counts = _row_counts(mask)
    return (counts[0] & 1, counts[1] & 1, counts[2] & 1)


def _rref(rows: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    basis: list[int] = []
    for row in rows:
        value = row
        for basis_row in basis:
            pivot = (basis_row & -basis_row).bit_length() - 1
            if (value >> pivot) & 1:
                value ^= basis_row
        if value == 0:
            continue
        pivot = (value & -value).bit_length() - 1
        for index, basis_row in enumerate(basis):
            if (basis_row >> pivot) & 1:
                basis[index] = basis_row ^ value
        basis.append(value)
    return tuple(basis)


def _in_span(basis: tuple[int, ...], vector: int) -> bool:
    value = vector
    for basis_row in basis:
        pivot = (basis_row & -basis_row).bit_length() - 1
        if (value >> pivot) & 1:
            value ^= basis_row
    return value == 0


def _syndrome(faces: tuple[int, ...], stars: tuple[int, ...], pauli: int) -> int:
    x_mask = pauli & ((1 << EDGES) - 1)
    z_mask = pauli >> EDGES
    _require(z_mask < (1 << EDGES), "pauli wider than two blocks")
    value = 0
    for index, row in enumerate(faces):
        if (row & x_mask).bit_count() & 1:
            value |= 1 << index
    for index, row in enumerate(stars):
        if (row & z_mask).bit_count() & 1:
            value |= 1 << (CELLS + index)
    return value


def _in_stabilizer(
    basis: tuple[int, ...],
    pauli: int,
) -> bool:
    x_mask = pauli & ((1 << EDGES) - 1)
    z_mask = pauli >> EDGES
    if (x_mask.bit_count() & 1) or (z_mask.bit_count() & 1):
        return False
    if _flux(x_mask) != (0, 0, 0):
        return False
    return _in_span(basis, pauli)


def _ball(radius: int, bits: int):
    yield 0
    if radius >= 1:
        for i in range(bits):
            yield 1 << i
    if radius >= 2:
        for i in range(bits):
            for j in range(i + 1, bits):
                yield (1 << i) | (1 << j)


def _distinguishes(errors: list[int], syndrome, in_repair) -> int:
    first: dict[int, int] = {}
    for error in errors:
        image = syndrome(error)
        previous = first.get(image)
        if previous is None:
            first[image] = error
            continue
        if not in_repair(error ^ previous):
            return 0
    return 1


def _packet_b() -> dict[str, int]:
    faces, stars = _cells()
    for star in stars:
        _require(tuple(sorted(_row_counts(star))) == (0, 0, 2), "star horizontals are not one row pair")
    commutation_odd = sum(
        1 for face in faces for star in stars if (face & star).bit_count() & 1
    )
    generators = tuple(stars) + tuple(row << EDGES for row in faces)
    _require(all(generator.bit_count() == 4 for generator in generators), "generator weight drifted")
    basis = _rref(generators)
    _require(all(_in_span(basis, generator) for generator in generators), "generator left its span")
    _require(_in_span(basis, stars[0] ^ stars[1]), "sum of two stars left the span")
    _require(not _in_span(basis, 1), "weight-one edge is in the stabilizer span")
    bad_generators = 0
    for generator in generators:
        if _syndrome(faces, stars, generator) != 0:
            bad_generators += 1
    _require(bad_generators == 0, "a stabilizer generator is outside ker Q")

    def in_s(pauli: int) -> bool:
        return _in_stabilizer(basis, pauli)

    def full_syndrome(pauli: int) -> int:
        return _syndrome(faces, stars, pauli)

    e1 = list(_ball(1, PAULI_BITS))
    kernel_hits = [mask for mask in _ball(2, PAULI_BITS) if full_syndrome(mask) == 0]
    e1_distinguishes = _distinguishes(e1, full_syndrome, in_s)
    hit_set = set(kernel_hits)
    if hit_set == {0} and e1_distinguishes != 1:
        raise RuntimeError("zero kernel difference was called a collision")
    if any(hit != 0 and not in_s(hit) for hit in hit_set) and e1_distinguishes != 0:
        raise RuntimeError("kernel difference outside S was called separated")

    y_mask = 1 | (1 << EDGES)
    lx = _mask((_h(0, 0), _h(1, 0), _h(2, 0)))
    e2_one = 1 << _h(0, 0)
    e2_two = _mask((_h(1, 0), _h(2, 0)))
    omitted = frozenset({0 * L + 2, 2 * L + 0})
    h_edge = 1 << _h(0, 0)
    v_edge = 1 << _v(0, 0)
    h_support = _support(faces, h_edge)
    v_support = _support(faces, v_edge)
    h_retained = tuple(index for index in h_support if index not in omitted)
    v_retained = tuple(index for index in v_support if index not in omitted)
    diff_support = _support(faces, h_edge ^ v_edge)
    retained_rows = tuple(row for index, row in enumerate(faces) if index not in omitted)

    def partial_syndrome(pauli: int) -> int:
        x_mask = pauli & ((1 << EDGES) - 1)
        value = 0
        bit = 0
        for row in retained_rows:
            if (row & x_mask).bit_count() & 1:
                value |= 1 << bit
            bit += 1
        return value

    partial_errors = list(_ball(1, PAULI_BITS))
    partial_distinguishes = _distinguishes(partial_errors, partial_syndrome, in_s)
    pair_equal = 1 if h_retained == v_retained else 0
    pair_outside = 1 if not in_s(h_edge ^ v_edge) else 0
    if pair_equal and pair_outside and h_edge.bit_count() == 1 and partial_distinguishes != 0:
        raise RuntimeError("exhibited X-block collision was missed")
    lx_flux = _flux(lx)
    diff_blocked = _flux(h_edge ^ v_edge) != (0, 0, 0)
    if diff_blocked and in_s(h_edge ^ v_edge):
        raise RuntimeError("flux and stabilizer span disagree on the omitted-face pair")
    if lx_flux != (0, 0, 0) and in_s(lx):
        raise RuntimeError("flux and stabilizer span disagree on Lx")
    e2_collision = int(
        e2_one.bit_count() <= 2
        and e2_two.bit_count() <= 2
        and full_syndrome(e2_one) == full_syndrome(e2_two)
        and (e2_one ^ e2_two) == lx
        and not in_s(lx)
    )
    _require(e2_collision == 1, "declared E_2 pair did not decide the fiber")
    star_flux_failures = sum(1 for star in stars if _flux(star) != (0, 0, 0))
    return {
        "b_edges": EDGES,
        "b_pauli_bits": PAULI_BITS,
        "b_e1": len(e1),
        "b_e2": sum(1 for _ in _ball(2, PAULI_BITS)),
        "b_duplicate_face_pairs": _pair_duplicates(faces),
        "b_duplicate_star_pairs": _pair_duplicates(stars),
        "b_ball2_kernel": len(kernel_hits),
        "b_e1_distinguishes": e1_distinguishes,
        "b_y_weight": y_mask.bit_count(),
        "b_y_in_kernel": 1 if full_syndrome(y_mask) == 0 else 0,
        "b_lx_weight": lx.bit_count(),
        "b_lx_index_sum": _h(0, 0) + _h(1, 0) + _h(2, 0),
        "b_lx_face_support": len(_support(faces, lx)),
        "b_lx_in_kernel": 1 if full_syndrome(lx) == 0 else 0,
        "b_lx_flux": sum(lx_flux),
        "b_lx_in_s": 1 if in_s(lx) else 0,
        "b_e2_weight_one": e2_one.bit_count(),
        "b_e2_weight_two": e2_two.bit_count(),
        "b_e2_syndromes_equal": 1 if full_syndrome(e2_one) == full_syndrome(e2_two) else 0,
        "b_e2_diff_is_lx": 1 if (e2_one ^ e2_two) == lx else 0,
        "b_e2_diff_in_s": 1 if in_s(e2_one ^ e2_two) else 0,
        "b_e2_distinguishes": 1 - e2_collision,
        "b_partial_bits": len(retained_rows),
        "b_partial_edge_sum": _h(0, 0) + _v(0, 0),
        "b_partial_equal": pair_equal,
        "b_partial_common_face": h_retained[0] if pair_equal and len(h_retained) == 1 else -1,
        "b_partial_retained_weight": len(h_retained) if pair_equal else -1,
        "b_partial_omitted_support": len(diff_support),
        "b_partial_support_is_omitted": 1 if set(diff_support) == set(omitted) else 0,
        "b_partial_diff_in_kernel": 1 if full_syndrome(h_edge ^ v_edge) == 0 else 0,
        "b_partial_diff_in_s": 0 if pair_outside else 1,
        "b_partial_distinguishes": partial_distinguishes,
        "b_star_flux_failures": star_flux_failures,
        "b_commutation_odd": commutation_odd,
    }


def witness() -> dict[str, int]:
    result: dict[str, int] = {}
    result.update(_packet_a())
    result.update(_packet_b())
    flags = (
        result["a_distinguishes"],
        result["b_e1_distinguishes"],
        result["b_e2_distinguishes"],
        result["b_partial_distinguishes"],
    )
    result["packet_answers_agree"] = 1 if len(set(flags)) == 1 else 0
    # Section 21.16 names no triple, so the four packet booleans do not close it.
    result["bullet_closed"] = 0
    result["refused_names"] = len(REFUSED_NAMES)
    _require(all(type(value) is int for value in result.values()), "non-integer witness value")
    return result


def refuse(name: object) -> int:
    if isinstance(name, float):
        raise TypeError("float tolerance is not a claim")
    if type(name) is not str or name in REFUSED_NAMES:
        raise ValueError(f"refused: {name}")
    value = witness().get(name)
    if type(value) is not int:
        raise ValueError(f"refused: {name}")
    return value
