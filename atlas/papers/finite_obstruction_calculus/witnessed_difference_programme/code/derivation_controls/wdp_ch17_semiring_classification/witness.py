"""Finite (Z, +, ·) endpoint-block census on carriers {0, 1} and {0, 1, 2}.

P1 means MH = HB for a nonempty vertex-block partition. The 81-matrix count
is the {-1, 0, 1} box on two vertices only. Powers are checked through a
finite bound. This is not a general-semiring classification.
"""

from __future__ import annotations

Matrix = tuple[tuple[int, ...], ...]
Partition = tuple[tuple[int, ...], ...]
_ENTRIES = (-1, 0, 1)
_CENSUS_LAST = 8
_EX1_LAST = 12
_EX2_LAST = 6
_EX4_LAST = 8
_MAX_LENGTH = 12

EX1: Matrix = (
    (2, -1, 3),
    (0, 1, 3),
    (4, -2, 1),
)
EX2: Matrix = (
    (2, 0, 0),
    (0, 0, 2),
    (0, 0, 2),
)
EX3: Matrix = (
    (1, -1),
    (0, 0),
)
EX4: Matrix = (
    (1, -1, 0),
    (0, 1, -1),
    (0, 0, 0),
)
_BLOCKS_01_2: Partition = ((0, 1), (2,))


def _as_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} is not an exact integer")
    return value


def _matrix(matrix: object) -> Matrix:
    if type(matrix) is not tuple or len(matrix) == 0:
        raise ValueError("matrix is not a nonempty tuple of rows")
    parsed: list[tuple[int, ...]] = []
    width: int | None = None
    for row in matrix:
        if type(row) is not tuple or len(row) == 0:
            raise ValueError("row is not a nonempty tuple")
        parsed_row = tuple(_as_int(entry, "entry") for entry in row)
        if width is None:
            width = len(parsed_row)
        elif len(parsed_row) != width:
            raise ValueError("ragged matrix")
        parsed.append(parsed_row)
    if width != len(parsed):
        raise ValueError("refused: row-source matrix must be square")
    return tuple(parsed)


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    shared = len(right)
    if len(left[0]) != shared:
        raise ValueError("matrix product shapes do not match")
    width = len(right[0])
    product: list[tuple[int, ...]] = []
    for row in left:
        if len(row) != shared:
            raise ValueError("ragged left factor")
        out: list[int] = []
        for column in range(width):
            total = 0
            for index in range(shared):
                if len(right[index]) != width:
                    raise ValueError("ragged right factor")
                total += row[index] * right[index][column]
            out.append(total)
        product.append(tuple(out))
    return tuple(product)


def _transpose(matrix: Matrix) -> Matrix:
    width = len(matrix[0])
    return tuple(
        tuple(matrix[row][column] for row in range(len(matrix)))
        for column in range(width)
    )


def _identity(size: int) -> Matrix:
    if type(size) is not int or size < 1:
        raise ValueError("identity size is outside the selected carriers")
    return tuple(
        tuple(1 if column == row else 0 for column in range(size))
        for row in range(size)
    )


def _matpow(matrix: Matrix, length: int) -> Matrix:
    if type(length) is not int or length < 0 or length > _MAX_LENGTH:
        raise ValueError("refused: length is outside the checked finite range")
    power = _identity(len(matrix))
    for _ in range(length):
        power = _matmul(power, matrix)
    return power

def _partition(size: int, partition: object) -> Partition:
    if type(partition) is not tuple:
        raise ValueError("partition is not a tuple")
    if len(partition) == 0:
        raise ValueError("refused: nonempty block partition required")
    seen: list[int] = []
    blocks: list[tuple[int, ...]] = []
    for block in partition:
        if type(block) is not tuple or len(block) == 0:
            raise ValueError("refused: empty block or block is not a tuple")
        vertices: list[int] = []
        for vertex in block:
            if type(vertex) is not int or vertex < 0 or vertex >= size:
                raise ValueError("vertex outside the carrier")
            vertices.append(vertex)
        blocks.append(tuple(vertices))
        seen.extend(vertices)
    if len(seen) != size or sorted(seen) != list(range(size)):
        raise ValueError("refused: blocks are not a partition of the carrier")
    return tuple(blocks)


def _partitions(size: int) -> tuple[Partition, ...]:
    if type(size) is not int or size not in (2, 3):
        raise ValueError("refused: carrier is outside {0,1} and {0,1,2}")
    found: list[Partition] = []

    def rec(vertex: int, blocks: list[list[int]]) -> None:
        if vertex == size:
            found.append(tuple(tuple(block) for block in blocks))
            return
        for index in range(len(blocks)):
            blocks[index].append(vertex)
            rec(vertex + 1, blocks)
            blocks[index].pop()
        blocks.append([vertex])
        rec(vertex + 1, blocks)
        blocks.pop()

    rec(0, [])
    ordered = tuple(sorted(found))
    if len(ordered) != len(set(ordered)):
        raise RuntimeError("partition generator repeated a partition")
    if any(len(part) == 0 or any(len(block) == 0 for block in part) for part in ordered):
        raise RuntimeError("empty partition was enumerated")
    return ordered


def _membership(size: int, blocks: Partition) -> Matrix:
    rows: list[tuple[int, ...]] = []
    for vertex in range(size):
        row = [0] * len(blocks)
        placed = 0
        for index, block in enumerate(blocks):
            if vertex in block:
                row[index] = 1
                placed += 1
        if placed != 1:
            raise RuntimeError("vertex is not in exactly one block")
        rows.append(tuple(row))
    return tuple(rows)


def _block_sums(matrix: Matrix, blocks: Partition) -> tuple[tuple[int, ...], ...]:
    sums: list[tuple[int, ...]] = []
    for row in matrix:
        totals: list[int] = []
        for block in blocks:
            total = 0
            for vertex in block:
                total += row[vertex]
            totals.append(total)
        sums.append(tuple(totals))
    return tuple(sums)


def quotient(matrix: object, partition: object) -> Matrix | None:
    """Block-sum quotient, or None when a source block disagrees.

    An empty partition is refused. B is the row of block sums of the first
    vertex in each block. MH = HB is checked before that matrix is returned.
    """

    parsed = _matrix(matrix)
    blocks = _partition(len(parsed), partition)
    sums = _block_sums(parsed, blocks)
    rows: list[tuple[int, ...]] = []
    for block in blocks:
        head = sums[block[0]]
        for vertex in block[1:]:
            if sums[vertex] != head:
                return None
        rows.append(head)
    found = tuple(rows)
    height = _membership(len(parsed), blocks)
    if _matmul(parsed, height) != _matmul(height, found):
        raise RuntimeError("quotient adapter disagreed with MH=HB")
    return found


def _rows_agree(matrix: Matrix, blocks: Partition) -> int:
    for block in blocks:
        head = matrix[block[0]]
        for vertex in block[1:]:
            if matrix[vertex] != head:
                return 0
    return 1

def dual_quotient(matrix: object, partition: object) -> Matrix | None:
    """Solve PM = BP, or return None when a target block is not constant.

    Columns of any BP repeat inside a target block, so unequal columns of PM
    inside one block are an exact obstruction over Z.
    """

    parsed = _matrix(matrix)
    blocks = _partition(len(parsed), partition)
    summed_rows: list[list[int]] = []
    for block in blocks:
        summed = [0] * len(parsed)
        for source in block:
            for target, weight in enumerate(parsed[source]):
                summed[target] += weight
        summed_rows.append(summed)
    rows: list[tuple[int, ...]] = []
    for summed in summed_rows:
        row: list[int] = []
        for target_block in blocks:
            value = summed[target_block[0]]
            for target in target_block[1:]:
                if summed[target] != value:
                    return None
            row.append(value)
        rows.append(tuple(row))
    found = tuple(rows)
    push = _transpose(_membership(len(parsed), blocks))
    if _matmul(push, parsed) != _matmul(found, push):
        raise RuntimeError("dual adapter disagreed with PM=BP")
    return found


def _unique_readout(matrix: Matrix, blocks: Partition, found: Matrix) -> int:
    image = _matmul(matrix, _membership(len(matrix), blocks))
    if len(found) != len(blocks):
        raise RuntimeError("quotient shape mismatch")
    for index, block in enumerate(blocks):
        if len(block) == 0:
            raise RuntimeError("empty block in readout")
        for vertex in block:
            if image[vertex] != found[index]:
                return 0
    return 1


def _entry_sum(matrix: Matrix) -> int:
    total = 0
    for row in matrix:
        for entry in row:
            total += entry
    return total


def _row_sums(matrix: Matrix) -> tuple[int, ...]:
    return tuple(sum(row) for row in matrix)


def _intertwines(matrix: Matrix, blocks: Partition, found: Matrix, last: int) -> int:
    if type(last) is not int or last < 0 or last > _MAX_LENGTH:
        raise ValueError("refused: length is outside the checked finite range")
    height = _membership(len(matrix), blocks)
    if _matmul(matrix, height) != _matmul(height, found):
        return 0
    power_m = _identity(len(matrix))
    power_b = _identity(len(blocks))
    for length in range(last + 1):
        left = _matmul(power_m, height)
        right = _matmul(height, power_b)
        if left != right:
            return 0
        for block in blocks:
            head = left[block[0]]
            for vertex in block[1:]:
                if left[vertex] != head:
                    return 0
        if length == last:
            break
        step_left = _matmul(matrix, left)
        step_mid = _matmul(matrix, right)
        mh = _matmul(matrix, height)
        step_blocks = _matmul(mh, power_b)
        step_copy = _matmul(_matmul(height, found), power_b)
        step_right = _matmul(height, _matmul(found, power_b))
        if not (
            step_left == step_mid
            and step_mid == step_blocks
            and step_blocks == step_copy
            and step_copy == step_right
        ):
            raise RuntimeError("induction step failed on the checked length")
        power_m = _matmul(power_m, matrix)
        power_b = _matmul(power_b, found)
        if power_m != _matpow(matrix, length + 1) or power_b != _matpow(found, length + 1):
            raise RuntimeError("successive power disagreed with the product")
    return 1


def classify(matrix: object) -> tuple[tuple[Partition, Matrix | None], ...]:
    """One result for every nonempty partition of a carrier of size 2 or 3."""

    parsed = _matrix(matrix)
    return tuple((part, quotient(parsed, part)) for part in _partitions(len(parsed)))


def _require_quotient(matrix: Matrix, blocks: Partition, last: int) -> Matrix:
    found = quotient(matrix, blocks)
    if found is None:
        raise RuntimeError("expected quotient was refused")
    if _unique_readout(matrix, blocks, found) != 1:
        raise RuntimeError("quotient is not the common block-sum row")
    if _intertwines(matrix, blocks, found, last) != 1:
        raise RuntimeError("quotient failed the checked finite lengths")
    return found

def _census() -> dict[str, object]:
    parts = _partitions(2)
    if parts != (((0,), (1,)), ((0, 1),)):
        raise RuntimeError("two-vertex partitions are not the two nonempty ones")
    matrices: list[Matrix] = []
    multiplicity = {total: 0 for total in (-2, -1, 0, 1, 2)}
    for left in _ENTRIES:
        for right in _ENTRIES:
            multiplicity[left + right] += 1
    counts = tuple(multiplicity[total] for total in (-2, -1, 0, 1, 2))
    if counts != (1, 2, 3, 2, 1):
        raise RuntimeError("row-sum multiplicities are not 1, 2, 3, 2, 1")
    closed = 0
    for count in counts:
        closed += count * count
    if closed != 19:
        raise RuntimeError("multiplicity square sum is not 19")
    for a in _ENTRIES:
        for b in _ENTRIES:
            for c in _ENTRIES:
                for d in _ENTRIES:
                    matrices.append(((a, b), (c, d)))
    if len(matrices) != 81:
        raise RuntimeError("entry box is not 81 matrices")
    one_p1 = 0
    one_p0 = 0
    one_p1_not_p0 = 0
    p0_pairs = 0
    p0_not_p1 = 0
    p1_pairs = 0
    for matrix in matrices:
        results = classify(matrix)
        if len(results) != 2:
            raise RuntimeError("two-vertex matrix did not return two partitions")
        by_part = dict(results)
        if set(by_part) != {((0,), (1,)), ((0, 1),)}:
            raise RuntimeError("unexpected two-vertex partitions")
        discrete = by_part[((0,), (1,))]
        one = by_part[((0, 1),)]
        if discrete != matrix:
            raise RuntimeError("discrete quotient is not M")
        if _rows_agree(matrix, ((0,), (1,))) != 1:
            raise RuntimeError("singleton blocks failed P0")
        p0_pairs += 1
        p1_pairs += 1
        if _intertwines(matrix, ((0,), (1,)), matrix, _CENSUS_LAST) != 1:
            raise RuntimeError("discrete intertwining failed")
        agrees = _rows_agree(matrix, ((0, 1),))
        if agrees == 1:
            one_p0 += 1
            p0_pairs += 1
            if one is None:
                p0_not_p1 += 1
        if one is not None:
            one_p1 += 1
            p1_pairs += 1
            if agrees == 0:
                one_p1_not_p0 += 1
            if one != ((_row_sums(matrix)[0],),):
                raise RuntimeError("one-block B is not the common row sum")
            if _intertwines(matrix, ((0, 1),), one, _CENSUS_LAST) != 1:
                raise RuntimeError("one-block intertwining failed")
        elif _row_sums(matrix)[0] == _row_sums(matrix)[1]:
            raise RuntimeError("equal row sums did not produce a quotient")
    if one_p1 != closed or one_p1 != 19:
        raise RuntimeError("enumerated one-block count disagreed with 19")
    if one_p0 != 9 or one_p1_not_p0 != 10 or one_p0 + one_p1_not_p0 != one_p1:
        raise RuntimeError("P0/P1 split on the one-block partition is not 9 and 10")
    if p0_not_p1 != 0:
        raise RuntimeError("P0 failed to imply P1 on the two-vertex box")
    if p1_pairs != 100 or p0_pairs != 90:
        raise RuntimeError("pair count mismatch")
    pairs = 81 * 2
    if pairs != 162 or pairs - p1_pairs != 62:
        raise RuntimeError("failure count is not 62")
    return {
        "matrices": 81,
        "partitions_two": 2,
        "pairs": pairs,
        "multiplicity": counts,
        "one_block_p1": one_p1,
        "one_block_p0": one_p0,
        "one_block_p1_not_p0": one_p1_not_p0,
        "discrete_p1": 81,
        "p1_pairs": p1_pairs,
        "p1_fail_pairs": pairs - p1_pairs,
        "p0_pairs": p0_pairs,
        "p0_not_p1": p0_not_p1,
        "census_through": _CENSUS_LAST,
        "census_powers_match": 1,
    }

def _example_powers(
    matrix: Matrix, last: int, scale: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    sources: list[int] = []
    entries: list[int] = []
    for length in range(last + 1):
        power = _matpow(matrix, length)
        rows = _row_sums(power)
        if any(value != rows[0] for value in rows):
            raise RuntimeError("per-source aggregates disagreed")
        total = _entry_sum(power)
        grouped = 0
        for value in rows:
            grouped += value
        if total != grouped:
            raise RuntimeError("entry sum disagreed with the sum of row sums")
        if rows[0] != scale**length or total != len(matrix) * rows[0]:
            raise RuntimeError("closed form disagreed with the summed entries")
        if total == rows[0]:
            raise RuntimeError("1D per-source aggregate was copied into the entry sum")
        sources.append(rows[0])
        entries.append(total)
    return tuple(sources), tuple(entries)


def _examples() -> dict[str, object]:
    if 1 + (-1) != 0 or 1 == 0 or -1 == 0:
        raise RuntimeError("(Z, +, ·) cancellation record failed")
    three = _partitions(3)
    if len(three) != 5 or set(three) != {
        ((0, 1, 2),),
        ((0, 1), (2,)),
        ((0, 2), (1,)),
        ((0,), (1, 2)),
        ((0,), (1,), (2,)),
    }:
        raise RuntimeError("three-vertex carrier does not have five partitions")
    for matrix, expected in ((EX1, 5), (EX2, 5), (EX4, 5), (EX3, 2)):
        results = classify(matrix)
        if len(results) != expected:
            raise RuntimeError("classify did not return every nonempty partition")
        for part, found in results:
            if _rows_agree(matrix, part) == 1 and found is None:
                raise RuntimeError("P0 failed to imply P1")
            if found is not None and _intertwines(matrix, part, found, 4) != 1:
                raise RuntimeError("classified quotient missed lengths 0 through 4")

    ex1_b = _require_quotient(EX1, _BLOCKS_01_2, _EX1_LAST)
    if ex1_b != ((1, 3), (2, 1)):
        raise RuntimeError("example 1 quotient is not ((1, 3), (2, 1))")
    if _rows_agree(EX1, _BLOCKS_01_2) != 0 or EX1[0] == EX1[1]:
        raise RuntimeError("example 1 rows unexpectedly agreed")
    ex1_sums = _row_sums(EX1)
    if ex1_sums != (4, 4, 3):
        raise RuntimeError("example 1 row sums are not 4, 4, 3")
    if quotient(EX1, ((0, 1, 2),)) is not None:
        raise RuntimeError("example 1 unexpectedly satisfied P2")
    ex1_pm = _matmul(_transpose(_membership(3, _BLOCKS_01_2)), EX1)
    if ex1_pm != ((2, 0, 6), (4, -2, 1)):
        raise RuntimeError("example 1 pushforward is not the recorded PM")
    if (ex1_pm[0][0], ex1_pm[1][0]) == (ex1_pm[0][1], ex1_pm[1][1]):
        raise RuntimeError("dual obstruction columns unexpectedly agreed")
    if dual_quotient(EX1, _BLOCKS_01_2) is not None:
        raise RuntimeError("example 1 dual equation was solved")

    if quotient(EX2, _BLOCKS_01_2) is not None:
        raise RuntimeError("example 2 two-block quotient should fail")
    if _rows_agree(EX2, _BLOCKS_01_2) != 0 or _rows_agree(EX2, ((0, 1, 2),)) != 0:
        raise RuntimeError("example 2 rows unexpectedly agreed")
    ex2_b = _require_quotient(EX2, ((0, 1, 2),), _EX2_LAST)
    if ex2_b != ((2,),):
        raise RuntimeError("example 2 one-block quotient is not ((2,),)")
    ex2_sources, ex2_entries = _example_powers(EX2, _EX2_LAST, 2)
    if ex2_sources != tuple(2**length for length in range(_EX2_LAST + 1)):
        raise RuntimeError("example 2 per-source column is not 2^n")
    if ex2_entries != tuple(3 * (2**length) for length in range(_EX2_LAST + 1)):
        raise RuntimeError("example 2 entry sums are not 3 times 2^n")

    ex3_blocks: Partition = ((0, 1),)
    ex3_b = _require_quotient(EX3, ex3_blocks, 4)
    if ex3_b != ((0,),) or EX3 != ((1, -1), (0, 0)):
        raise RuntimeError("example 3 quotient or rows changed")
    if _rows_agree(EX3, ex3_blocks) != 0:
        raise RuntimeError("example 3 rows unexpectedly agreed")
    if EX3[0][0] + EX3[0][1] != 0 or EX3[0][0] == 0 or EX3[0][1] == 0:
        raise RuntimeError("example 3 cancellation is not 1+(-1)=0 with nonzero summands")
    if dual_quotient(EX3, ex3_blocks) is not None:
        raise RuntimeError("example 3 one-block dual was solved")
    height = _membership(2, ex3_blocks)
    wrong: Matrix = ((1,),)
    # B^0 is I for every B, so length 0 does not determine the quotient.
    if _matpow(wrong, 0) != ((1,),) or _matmul(height, _matpow(wrong, 0)) != height:
        raise RuntimeError("length 0 rejected a wrong quotient")
    image = _matmul(EX3, height)
    if image != ((0,), (0,)) or image == _matmul(height, wrong):
        raise RuntimeError("length 1 accepted a wrong quotient")

    if _rows_agree(EX4, _BLOCKS_01_2) != 0 or _rows_agree(EX4, ((0, 1, 2),)) != 0:
        raise RuntimeError("example 4 rows unexpectedly agreed")
    if quotient(EX4, _BLOCKS_01_2) is not None:
        raise RuntimeError("example 4 two-block quotient should fail")
    ex4_b = _require_quotient(EX4, ((0, 1, 2),), _EX4_LAST)
    if ex4_b != ((0,),):
        raise RuntimeError("example 4 one-block quotient is not ((0,),)")
    ex4_height = _membership(3, ((0, 1, 2),))
    length0 = _matmul(_identity(3), ex4_height)
    length1 = _matmul(EX4, ex4_height)
    if length0 != ((1,), (1,), (1,)) or length1 != ((0,), (0,), (0,)):
        raise RuntimeError("example 4 aggregates are not 1 at length 0 and 0 at length 1")
    if EX4[0][0] != 1 or EX4[1][0] != 0:
        raise RuntimeError("example 4 edge weights are not the recorded pair")
    for length in range(1, _EX4_LAST + 1):
        if _row_sums(_matpow(EX4, length)) != (0, 0, 0):
            raise RuntimeError("example 4 positive length did not send ones to 0")

    refused = 0
    try:
        quotient(EX3, ())
    except ValueError as exc:
        if "nonempty" not in str(exc):
            raise
        refused = 1
    if refused != 1:
        raise RuntimeError("empty partition was classified")

    return {
        "zerosumfree": 0,
        "ex1_p0": 0,
        "ex1_p1": 1,
        "ex1_p2": 0,
        "ex1_b": ex1_b,
        "ex1_row_sums": ex1_sums,
        "ex1_pm": ex1_pm,
        "ex1_dual": 0,
        "ex1_b_unique": 1,
        "ex1_through": _EX1_LAST,
        "ex1_intertwines": 1,
        "ex2_two_block_p0": 0,
        "ex2_one_block_p0": 0,
        "ex2_block_p1": 0,
        "ex2_p2": 1,
        "ex2_b": ex2_b,
        "ex2_b_unique": 1,
        "ex2_through": _EX2_LAST,
        "ex2_sources": ex2_sources,
        "ex2_entry_sums": ex2_entries,
        "ex2_source_equals_entries": 0,
        "ex3_p0": 0,
        "ex3_p1": 1,
        "ex3_b": ex3_b,
        "ex3_b_unique": 1,
        "ex3_rows": EX3,
        "ex3_one_block_dual": 0,
        "ex3_length0_accepts_wrong_b": 1,
        "ex3_length1_rejects_wrong_b": 1,
        "ex4_two_block_p0": 0,
        "ex4_block_p1": 0,
        "ex4_one_block_p0": 0,
        "ex4_p2": 1,
        "ex4_b": ex4_b,
        "ex4_b_unique": 1,
        "ex4_length0": 1,
        "ex4_length1": 0,
        "ex4_edge_00": EX4[0][0],
        "ex4_edge_10": EX4[1][0],
        "ex4_through": _EX4_LAST,
        "ex4_intertwines": 1,
        "partitions_three": len(three),
        "empty_partition_refused": refused,
    }

def _exact(value: object) -> None:
    if type(value) is int:
        return
    if type(value) is tuple:
        for item in value:
            _exact(item)
        return
    if type(value) is dict:
        for item in value.values():
            _exact(item)
        return
    raise RuntimeError("result left the exact integers")


def witness() -> dict[str, object]:
    """Exact integer census and the five separating matrices. No float tolerance."""

    result: dict[str, object] = {}
    result.update(_census())
    result.update(_examples())
    result["general_semiring_classified"] = 0
    result["continuum_limit"] = 0
    result["infinite_sum"] = 0
    if result["general_semiring_classified"] != 0 or result["continuum_limit"] != 0:
        raise RuntimeError("a finite integer box was reported as a general classification")
    if result["infinite_sum"] != 0:
        raise RuntimeError("a finite length was reported as an infinite path sum")
    _exact(result)
    return result


def refuse_general_semiring(p1_pairs: object) -> None:
    """The two-vertex count does not classify a general semiring."""

    if type(p1_pairs) is not int:
        raise ValueError("p1 pair count is not an exact integer")
    if p1_pairs == 100:
        raise ValueError(
            "refused: 100 of 162 is the {-1,0,1} two-vertex census, "
            "not a classification of coarse-grainings over a general semiring"
        )
    raise ValueError("refused: count is outside the selected census")


def refuse_source_as_entry_sum(per_source: object, total: object, width: object) -> None:
    """The per-source column is not the sum of every matrix entry."""

    if type(per_source) is not int or type(total) is not int or type(width) is not int:
        raise ValueError("aggregates are not exact integers")
    if width != 3:
        raise ValueError("refused: width is outside example 2")
    if per_source == total:
        raise ValueError("refused: the recorded aggregates are not equal")
    if total == width * per_source:
        raise ValueError(
            "refused: do not copy a 1D per-source aggregate into the sum of all matrix entries"
        )
    raise ValueError("refused: pair is outside example 2")


def refuse_continuum() -> None:
    raise ValueError("refused: a finite model does not establish a continuum limit")


def refuse_infinite_sum() -> None:
    raise ValueError("refused: a finite-length aggregate is not an infinite path sum")
