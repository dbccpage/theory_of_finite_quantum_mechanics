"""Shared hand-encoded 20-qubit stabilizer fixture, not a derived tensor network.

Bounded context: independent finite-model checking. Rank and mincut are independently
cross-checked by span enumeration and all 64 graph assignments in regression tests.
"""
from functools import lru_cache
from .domains import integer, sequence
from .boundary import Violation

def set_xz(q: int, x: int, z: int) -> int:
    integer(q, "qubit", 0, 19)
    integer(x, "Pauli X bit", 0, 1)
    integer(z, "Pauli Z bit", 0, 1)
    val = 0
    if x == 1:
        val |= 1 << (2 * q)
    if z == 1:
        val |= 1 << (2 * q + 1)
    return val


LOCAL_BLOCK_3 = (
    ((1, 0), (0, 1), (0, 1), (1, 0)),
    ((0, 1), (1, 1), (1, 1), (0, 1)),
    ((1, 1), (0, 1), (1, 1), (0, 0)),
)

PUSH_X_BLOCK = ((0, 1), (0, 1), (1, 0), (0, 0))
PUSH_Z_BLOCK = ((1, 0), (0, 0), (1, 0), (0, 1))

CENTRAL_GENS_5 = (
    ((1, 0), (0, 1), (0, 1), (1, 0), (0, 0)),
    ((0, 0), (1, 0), (0, 1), (0, 1), (1, 0)),
    ((1, 0), (0, 0), (1, 0), (0, 1), (0, 1)),
    ((0, 1), (1, 0), (0, 0), (1, 0), (0, 1)),
    ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1)),
)


def _pattern(value: object, size: int) -> tuple[tuple[int, int], ...]:
    pairs = [sequence(pair, "Pauli pair", 2) for pair in sequence(value, "Pauli pattern", size)]
    return tuple((integer(x, "X bit", 0, 1), integer(z, "Z bit", 0, 1)) for x, z in pairs)


def encode_local_gen(k: int, pat: object) -> int:
    integer(k, "block", 0, 4)
    pattern = _pattern(pat, 4)
    acc = 0
    for j in range(4):
        x, z = pattern[j]
        acc ^= set_xz(4 * k + j, x, z)
    return acc


def encode_central_gen(cpat: object) -> int:
    pattern = _pattern(cpat, 5)
    acc = 0
    for k in range(5):
        cx, cz = pattern[k]
        if cx == 1:
            acc ^= encode_local_gen(k, PUSH_X_BLOCK)
        if cz == 1:
            acc ^= encode_local_gen(k, PUSH_Z_BLOCK)
    return acc


def build_boundary_gens_20() -> list[int]:
    gens: list[int] = []
    for k in range(5):
        for pat in LOCAL_BLOCK_3:
            gens.append(encode_local_gen(k, pat))
    for cpat in CENTRAL_GENS_5:
        gens.append(encode_central_gen(cpat))
    return gens


def commutes_20(u: int, v: int) -> bool:
    integer(u, "40-bit Pauli row", 0, (1 << 40)-1)
    integer(v, "40-bit Pauli row", 0, (1 << 40)-1)
    s = 0
    for q in range(20):
        ux = (u >> (2 * q)) & 1
        uz = (u >> (2 * q + 1)) & 1
        vx = (v >> (2 * q)) & 1
        vz = (v >> (2 * q + 1)) & 1
        s += (ux * vz) ^ (uz * vx)
    return (s % 2) == 0


def gf2_rank(rows: object) -> int:
    admitted = tuple(integer(row, "40-bit row", 0, (1 << 40)-1)
                     for row in sequence(rows, "GF(2) rows"))
    basis: list[tuple[int, int]] = []
    for r in admitted:
        cur = r
        for p, b in basis:
            if (cur >> p) & 1:
                cur ^= b
        if cur != 0:
            first_bit = 0
            for b in range(40):
                if (cur >> b) & 1:
                    first_bit = b
                    break
            basis.append((first_bit, cur))
    return len(basis)


def in_contiguous_interval(start: int, length: int, q: int) -> bool:
    integer(start, "interval start", 0, 19)
    integer(length, "interval length", 0, 20)
    integer(q, "qubit", 0, 19)
    return ((q + 20 - start) % 20) < length


def interval_bitmask_40(start: int, length: int) -> int:
    mask = 0
    for q in range(20):
        if in_contiguous_interval(start, length, q):
            mask |= 3 << (2 * q)
    return mask


def interval_entropy(gens: object, start: int, length: int) -> int:
    generators = validate_generators(gens)
    mask = interval_bitmask_40(start, length)
    return gf2_rank([g & mask for g in generators]) - length


def interval_mincut(start: int, length: int) -> int:
    a = [
        sum(1 for j in range(4) if in_contiguous_interval(start, length, 4 * k + j))
        for k in range(5)
    ]

    def cost_for_central(s_c: int) -> int:
        total = 0
        for k in range(5):
            ak = a[k]
            c0 = ak + (1 if 0 != s_c else 0)
            c1 = (4 - ak) + (1 if 1 != s_c else 0)
            total += min(c0, c1)
        return total

    return min(cost_for_central(0), cost_for_central(1))


def region_entropy(gens: object, qs: list[int]) -> int:
    qs = validated_region(qs)
    generators = validate_generators(gens)
    mask = 0
    for q in qs:
        mask |= 3 << (2 * q)
    return gf2_rank([g & mask for g in generators]) - len(qs)


def region_mutual_information(gens: object, a: list[int], b: list[int]) -> int:
    a, b = validated_region(a), validated_region(b)
    if set(a) & set(b):
        raise Violation("input", "mutual-information regions must be disjoint")
    return region_entropy(gens, a) + region_entropy(gens, b) - region_entropy(gens, a + b)


def validated_region(qubits: object) -> list[int]:
    admitted = [integer(qubit, "qubit", 0, 19)
                for qubit in sequence(qubits, "qubit region", maximum=20)]
    if len(set(admitted)) != len(admitted):
        raise Violation("input", "qubit region contains duplicates")
    return admitted


def validate_generators(generators: object) -> tuple[int, ...]:
    admitted = tuple(integer(row, "40-bit Pauli row", 0, (1 << 40)-1)
                     for row in sequence(generators, "stabilizer generators", 20))
    _validate_pure_generators(admitted)
    return admitted


@lru_cache(maxsize=16)
def _validate_pure_generators(generators: tuple[int, ...]) -> None:
    if gf2_rank(list(generators)) != 20:
        raise Violation("input", "pure stabilizer fixture requires 20 independent generators")
    if any(not commutes_20(u,v) for u in generators for v in generators):
        raise Violation("input", "stabilizer generators must commute")


BOUNDARY_GENS_20 = tuple(build_boundary_gens_20())
