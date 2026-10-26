"""Exact finite models of the consolidated paper's preservation contracts."""
from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence
from fractions import Fraction
from itertools import product
from typing import TypeVar

R = TypeVar("R", bound=Hashable)
S = TypeVar("S")


def report_factor(reports: Sequence[R], answers: Sequence[S]) -> dict[R, S] | None:
    """Return the unique answer table on the listed report image, or refuse."""
    if len(reports) != len(answers):
        raise ValueError("one report and answer are required per history")
    factor: dict[R, S] = {}
    for report, answer in zip(reports, answers, strict=True):
        if report in factor and factor[report] != answer:
            return None
        factor[report] = answer
    return factor


def demand_step(active: Iterable[int], discharged: Iterable[int], births: Iterable[int]) -> frozenset[int]:
    w, d, b = map(frozenset, (active, discharged, births))
    if not d <= w:
        raise ValueError("discharged demands must be active")
    residual = w - d
    if b & residual:
        raise ValueError("births must be disjoint from surviving demands")
    return residual | b


def refine(reports: Sequence[int], tags: Sequence[int]) -> tuple[tuple[int, int], ...]:
    if len(reports) != len(tags):
        raise ValueError("one tag is required per report")
    return tuple(zip(reports, tags, strict=True))


def boundary(vertices: int, edges: Sequence[tuple[int, int]], coefficients: Sequence[int]) -> tuple[int, ...]:
    """Integer graph boundary, with loops and repeated edges retained."""
    if vertices < 0 or len(edges) != len(coefficients):
        raise ValueError("invalid graph dimensions")
    result = [0] * vertices
    for (src, dst), weight in zip(edges, coefficients, strict=True):
        if not 0 <= src < vertices or not 0 <= dst < vertices:
            raise ValueError("edge endpoint outside vertex carrier")
        result[src] -= weight
        result[dst] += weight
    return tuple(result)


def component_labels(vertices: int, edges: Sequence[tuple[int, int]]) -> tuple[int, ...]:
    """Minimum vertex in each undirected component; loops and repeats retained."""
    boundary(vertices, edges, [0] * len(edges))  # Validate the same carrier.
    parent = list(range(vertices))

    def root(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = root(a), root(b)
        parent[max(ra, rb)] = min(ra, rb)
    return tuple(root(x) for x in range(vertices))


def components(vertices: int, edges: Sequence[tuple[int, int]]) -> int:
    return len(set(component_labels(vertices, edges)))


def component_totals(vertices: int, edges: Sequence[tuple[int, int]],
                     coefficients: Sequence[int]) -> tuple[tuple[int, int], ...]:
    """Component coordinates of an integral zero-chain, ordered by minimum vertex."""
    if len(coefficients) != vertices:
        raise ValueError("one coefficient required per vertex")
    labels = component_labels(vertices, edges)
    totals: dict[int, int] = {}
    for label, weight in zip(labels, coefficients, strict=True):
        totals[label] = totals.get(label, 0) + weight
    return tuple(sorted(totals.items()))


def rational_rank(matrix: Sequence[Sequence[int | Fraction]], columns: int) -> int:
    """Exact row reduction; columns is explicit even for an empty matrix."""
    if columns < 0 or any(len(row) != columns for row in matrix):
        raise ValueError("ragged matrix")
    rows = [list(map(Fraction, row)) for row in matrix]
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [x / scale for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank:
                multiplier = rows[i][column]
                rows[i] = [x - multiplier * y for x, y in zip(rows[i], rows[rank], strict=True)]
        rank += 1
    return rank


def graph_homology_ranks(vertices: int, edges: Sequence[tuple[int, int]]) -> tuple[int, int]:
    boundary(vertices, edges, [0] * len(edges))  # Validate even an empty edge list.
    columns = [boundary(vertices, edges, [int(i == j) for i in range(len(edges))])
               for j in range(len(edges))]
    matrix = [[column[i] for column in columns] for i in range(vertices)]
    rank = rational_rank(matrix, len(edges))
    return vertices - rank, len(edges) - rank


def encode(word: str) -> str:
    if any(letter not in "ab" for letter in word):
        raise ValueError("the declared source alphabet is {a,b}")
    return "".join("0" if letter == "a" else "00" for letter in word)


def chsh(values: Sequence[int]) -> tuple[int, int]:
    if len(values) != 4:
        raise ValueError("four correlations required")
    a, b, c, d = values
    return a + b + c - d, a + b - c + d


def cyclic_representative(modulus: int, value: int) -> int:
    """Canonical class in Z/(modulus Z); modulus zero retains the integer."""
    return value if modulus == 0 else value % abs(modulus)


def triangle_h1_class(filled: bool, coefficients: Sequence[int]) -> int:
    """Integral H1 coordinate; refuse a chain with nonzero graph boundary."""
    if len(coefficients) != 3:
        raise ValueError("one coefficient per oriented triangle edge required")
    if any(boundary(3, [(0, 1), (1, 2), (2, 0)], coefficients)):
        raise ValueError("homology class requires a cycle")
    return 0 if filled else coefficients[0]


def triangle_coboundary(coefficients: Sequence[int]) -> int:
    """Evaluate an edge cochain on the oriented boundary of one attached face."""
    if len(coefficients) != 3:
        raise ValueError("one cochain coefficient per oriented triangle edge required")
    return sum(coefficients)


def triangle_degree_class(modulus: int, coefficients: Sequence[int]) -> int:
    return cyclic_representative(modulus, triangle_h1_class(False, coefficients))


def bell_pair_distribution(negative: bool) -> tuple[Fraction, ...]:
    """Exact probabilities ordered (++,+-,-+,--), for correlation +1 or -1."""
    return tuple(Fraction(int((a != b) == negative), 2)
                 for a, b in ((False, False), (False, True), (True, False), (True, True)))


def decimal_encode(word: str) -> str:
    """Four binary bits per ASCII decimal digit; concatenation is preserved."""
    if any(letter not in "0123456789" for letter in word):
        raise ValueError("ASCII decimal digits required")
    return "".join(format(int(letter), "04b") for letter in word)


def decimal_decode(bits: str) -> str:
    if len(bits) % 4 or any(bit not in "01" for bit in bits):
        raise ValueError("complete four-bit blocks required")
    digits = [int(bits[i:i+4], 2) for i in range(0, len(bits), 4)]
    if any(digit >= 10 for digit in digits):
        raise ValueError("binary block outside decimal image")
    return "".join(map(str, digits))


def recover_word(word: str, old_alphabet: str = "ab") -> str | None:
    return word if all(letter in old_alphabet for letter in word) else None


def erase_word(word: str, old_alphabet: str = "ab") -> str:
    return "".join(letter for letter in word if letter in old_alphabet)


def rename_word(mapping: Sequence[int], word: Sequence[int]) -> tuple[int, ...]:
    if any(not 0 <= letter < len(mapping) for letter in word):
        raise ValueError("source letter outside mapping carrier")
    return tuple(mapping[letter] for letter in word)


def reverse_trace(trace: Sequence[tuple[int, bool, int]]) -> tuple[tuple[int, bool, int], ...]:
    return tuple((last, not direction, first) for first, direction, last in reversed(trace))


def free_reduce(word: str) -> str:
    """Canonical free-group word; capitals denote inverse generators."""
    if any(letter not in "abAB" for letter in word):
        raise ValueError("signed alphabet {a,b,A,B} required")
    stack: list[str] = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def bell_mixture(weights: Sequence[int]) -> tuple[Fraction, ...]:
    """Exact joint-model correlations in Boolean lexicographic assignment order."""
    if len(weights) != 16 or any(w < 0 for w in weights) or sum(weights) == 0:
        raise ValueError("sixteen nonnegative masses with positive total required")
    correlations = [Fraction(0) for _ in range(4)]
    for weight, assignment in zip(weights, product((1, -1), repeat=4), strict=True):
        a0, a1, b0, b1 = assignment
        for i, value in enumerate((a0*b0, a0*b1, a1*b0, a1*b1)):
            correlations[i] += Fraction(weight*value, sum(weights))
    c00, c01, c10, c11 = correlations
    return (*correlations, c00+c01-c10+c11)


def protocol(line: str) -> str:
    """Version 1 tab-separated finite replay. Malformed records are refused.

    Bounds: at most 8 vertices/histories, 16 edges, integer magnitude 1,000,000;
    demand masks range over a declared carrier of at most 8 elements.
    """
    fields = line.split("\t")

    def numbers(field: str) -> list[int]:
        pieces = [] if field == "" else field.split(",")
        values = [int(x) for x in pieces]
        if any(str(x) != piece for x, piece in zip(values, pieces, strict=True)):
            raise ValueError("noncanonical decimal spelling")
        if any(abs(x) > 1_000_000 for x in values):
            raise ValueError("integer outside replay bound")
        return values

    def natural(field: str) -> int:
        value = int(field)
        if value < 0 or str(value) != field:
            raise ValueError("noncanonical natural spelling")
        return value

    try:
        match fields:
            case ["v1", "factor", rs, ss]:
                reports, answers = numbers(rs), numbers(ss)
                if len(reports) > 8:
                    raise ValueError("history budget")
                return str(int(report_factor(reports, answers) is not None))
            case ["v1", "demand", ns, ws, ds, bs]:
                n, w, d, b = map(natural, (ns, ws, ds, bs))
                if not 0 <= n <= 8 or any(not 0 <= mask < 2**n for mask in (w, d, b)):
                    raise ValueError("mask outside carrier")
                sets = [{x for x in range(n) if mask & (1 << x)} for mask in (w, d, b)]
                return str(len(demand_step(*sets)))
            case ["v1", "boundary", ns, es, cs]:
                n, endpoints, coefficients = natural(ns), numbers(es), numbers(cs)
                if not 0 <= n <= 8 or len(endpoints) % 2 or len(coefficients) > 16:
                    raise ValueError("graph budget")
                edges = list(zip(endpoints[::2], endpoints[1::2], strict=True))
                return ",".join(map(str, boundary(n, edges, coefficients)))
            case ["v1", "components", ns, es, cs]:
                n, endpoints, coefficients = natural(ns), numbers(es), numbers(cs)
                if n > 8 or len(endpoints) % 2 or len(endpoints) > 32:
                    raise ValueError("graph budget")
                edges = list(zip(endpoints[::2], endpoints[1::2], strict=True))
                totals = component_totals(n, edges, coefficients)
                return ",".join(str(value) for pair in totals for value in pair)
            case ["v1", "cyclic", values]:
                parsed = numbers(values)
                if len(parsed) != 2:
                    raise ValueError("modulus and representative required")
                return str(cyclic_representative(*parsed))
            case ["v1", "triangle", fs, values]:
                filled = natural(fs)
                if filled > 1:
                    raise ValueError("filled flag is 0 or 1")
                return str(triangle_h1_class(bool(filled), numbers(values)))
            case ["v1", "cochain", values]:
                return str(triangle_coboundary(numbers(values)))
            case ["v1", "triangle_degree", values]:
                parsed = numbers(values)
                if len(parsed) != 4:
                    raise ValueError("degree and three triangle coefficients required")
                return str(triangle_degree_class(parsed[0], parsed[1:]))
            case ["v1", "bellpair", flag]:
                negative = natural(flag)
                if negative > 1:
                    raise ValueError("correlation flag is 0 or 1")
                probabilities = bell_pair_distribution(bool(negative))
                return ",".join(str(int(2*p)) for p in probabilities)
            case ["v1", "decimal", word]:
                if len(word) > 16:
                    raise ValueError("decimal word budget")
                return decimal_encode(word)
            case ["v1", "decimal_decode", bits]:
                if len(bits) > 64:
                    raise ValueError("binary word budget")
                return decimal_decode(bits)
            case ["v1", operation, word] if operation in ("recover", "erase"):
                if len(word) > 64 or any(letter not in "abc" for letter in word):
                    raise ValueError("declared alphabet or word budget")
                if operation == "erase":
                    return erase_word(word)
                recovered = recover_word(word)
                return "NON_DESCENT" if recovered is None else recovered
            case ["v1", "rename", ms, ws]:
                mapping, letters = numbers(ms), numbers(ws)
                if len(mapping) > 8 or len(letters) > 64:
                    raise ValueError("rename carrier or word budget")
                return ",".join(map(str, rename_word(mapping, letters)))
            case ["v1", "trace", values]:
                parsed = numbers(values)
                if len(parsed) % 3 or len(parsed) > 48:
                    raise ValueError("trace arity or edge budget")
                triples = list(zip(parsed[::3], parsed[1::3], parsed[2::3], strict=True))
                if any(direction not in (0, 1) for _, direction, _ in triples):
                    raise ValueError("arrow flag is 0 or 1")
                trace = [(a, bool(direction), b) for a, direction, b in triples]
                reversed_edges = reverse_trace(trace)
                return ",".join(str(value) for a, direction, b in reversed_edges
                                for value in (a, int(direction), b))
            case ["v1", "code", word]:
                if len(word) > 64:
                    raise ValueError("word budget")
                return encode(word)
            case ["v1", "freeword", word]:
                if len(word) > 64:
                    raise ValueError("free-word budget")
                return free_reduce(word)
            case ["v1", "bellmix", values]:
                return ",".join(map(str, bell_mixture(numbers(values))))
            case ["v1", "chsh", values]:
                return ",".join(map(str, chsh(numbers(values))))
            case _:
                raise ValueError("unknown version, operation or arity")
    except (ValueError, OverflowError):
        return "REFUSE"
