"""Primitive Difference Candidates, Pointed Structures, and Implication Matrix.

Selected educational models related to 19L57G1:
- code/derivation/primdiff.py
- code/derivation/primitive_core.py
- lean4/Derivation/PrimDiff.lean
- lean4/Derivation/PrimitiveCore.lean
- lean4/Derivation/PrimitiveCats.lean

Classification: Metatheory apparatus & formal mathematical spine.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

from .canonical import FrozenMap, validate_typed_fields

# ---------------------------------------------------------------------------
# Base Mathematical Carrier Types
# ---------------------------------------------------------------------------

Rel = frozenset[tuple[int, int]]
Func = tuple[int, ...]
Partition = tuple[tuple[int, ...], ...]


def _validate_relation(n: int, relation: Rel) -> None:
    if any(not 0 <= x < n or not 0 <= y < n for x, y in relation):
        raise ValueError("REFUSED_SHAPE: relation outside declared carrier")


def _validate_pointed(n: int, relation: Rel, a: int, b: int) -> None:
    if n < 1 or not 0 <= a < n or not 0 <= b < n:
        raise ValueError("REFUSED_SHAPE: pointed endpoints outside declared carrier")
    _validate_relation(n, relation)


MAX_N = 3

CANDIDATES: tuple[str, ...] = (
    "W",
    "A",
    "Bs",
    "Bc",
    "Bl",
    "C",
    "D",
    "E",
    "F",
)


# ---------------------------------------------------------------------------
# Composed Pointed Carrier Structure (PrimDiff)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Pointed:
    """A pointed structure (n, rel, a, b):
    carrier range(n), binary relation rel on range(n), and designated endpoints a, b.
    """

    n: int
    rel: Rel
    a: int
    b: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)
        _validate_pointed(self.n, self.rel, self.a, self.b)

    def json(self) -> dict[str, object]:
        return {
            "n": self.n,
            "rel": sorted(list(p) for p in self.rel),
            "a": self.a,
            "b": self.b,
        }


# ---------------------------------------------------------------------------
# Composed Setting Structure (PrimitiveCore 9-Candidate Matrix)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Setting:
    """The common signature carrying every datum mentioned by the 9 candidate readings:
    carrier range(n), relation r, designated endpoints a and b,
    retention store ret, protection-demand store prot,
    and admitted endofunction family ops.
    """

    n: int
    r: Rel
    a: int
    b: int
    ret: Rel
    prot: Rel
    ops: frozenset[Func]

    def __post_init__(self) -> None:
        validate_typed_fields(self)
        _validate_pointed(self.n, self.r, self.a, self.b)
        _validate_relation(self.n, self.ret)
        _validate_relation(self.n, self.prot)
        if any(len(f) != self.n or any(not 0 <= x < self.n for x in f) for f in self.ops):
            raise ValueError("REFUSED_SHAPE: endofunction outside declared carrier")

    def json(self) -> dict[str, object]:
        return {
            "n": self.n,
            "r": [list(p) for p in sorted(self.r)],
            "a": self.a,
            "b": self.b,
            "ret": [list(p) for p in sorted(self.ret)],
            "prot": [list(p) for p in sorted(self.prot)],
            "ops": [list(f) for f in sorted(self.ops)],
        }


# ---------------------------------------------------------------------------
# Algebraic Operators & Predicates on Relations
# ---------------------------------------------------------------------------


def irreflexive(rel: Rel) -> bool:
    """Irreflexivity: forall x, not (x, x) in rel.

    The foundational object-level fidelity commitment: the weakest
    axiom found that gives an asserted difference any consequence at all.
    """
    return all(x != y for (x, y) in rel)


def symmetric(rel: Rel) -> bool:
    """Symmetry: forall x y, (x, y) in rel ==> (y, x) in rel."""
    return all((y, x) in rel for (x, y) in rel)


def symmetrize(rel: Rel) -> Rel:
    """Symmetrization of a relation."""
    return rel | frozenset((y, x) for (x, y) in rel)


def transpose(rel: Rel) -> Rel:
    """Transpose of a relation."""
    return frozenset((y, x) for (x, y) in rel)


def cotransitive(rel: Rel, n: int) -> bool:
    """Cotransitivity: forall x y in rel, forall z in range(n), (x, z) in rel or (z, y) in rel."""
    for x, y in rel:
        for z in range(n):
            if (x, z) not in rel and (z, y) not in rel:
                return False
    return True


def compose(f: Func, g: Func) -> Func:
    """Function composition f o g."""
    return tuple(f[g[x]] for x in range(len(g)))


def closure(n: int, family: Sequence[Func]) -> frozenset[Func]:
    """Closure of an endofunction family under identity and composition (finite monoid)."""
    identity = tuple(range(n))
    out: set[Func] = {identity} | set(family)
    changed = True
    while changed:
        changed = False
        for f in list(out):
            for g in list(out):
                h = compose(f, g)
                if h not in out:
                    out.add(h)
                    changed = True
    return frozenset(out)


def irreducible(ops: frozenset[Func], a: int, b: int, n: int) -> bool:
    """Irreducibility: no endofunction in Clos(ops) merges a and b."""
    return all(f[a] != f[b] for f in closure(n, tuple(ops)))


# ---------------------------------------------------------------------------
# The Nine Candidate Readings of Primitive Difference
# ---------------------------------------------------------------------------


def W(s: Setting) -> bool:
    """W: Bare witnessed pair (r a b). No laws."""
    return (s.a, s.b) in s.r


def A(s: Setting) -> bool:
    """A: Pointed witnessed irreflexive relation (PD-A).

    Within the declared nine-candidate signature, PD-A is the weakest
    studied positive-witness candidate forcing distinct endpoints.
    """
    return W(s) and irreflexive(s.r)


def Bs(s: Setting) -> bool:
    """Bs: Symmetric PD-B axis: A plus symmetry."""
    return A(s) and symmetric(s.r)


def Bc(s: Setting) -> bool:
    """Bc: Cotransitive PD-B axis: A plus cotransitivity."""
    return A(s) and cotransitive(s.r, s.n)


def Bl(s: Setting) -> bool:
    """Bl: Located PD-B axis: A plus locatedness (decidable boolean function)."""
    # In finite decidable tables, Bl coincides extensionally with A
    return A(s)


def C(s: Setting) -> bool:
    """C: Witnessed non-identification (PD-C): asserted fact plus protection demand."""
    return W(s) and ((s.a, s.b) in s.prot)


def D(s: Setting) -> bool:
    """D: Non-factorization through the point (PD-D): metatheoretic endpoint inequality a != b."""
    return s.a != s.b


def E(s: Setting) -> bool:
    """E: Irreducibility under admitted operation family (PD-E)."""
    return irreducible(s.ops, s.a, s.b, s.n)


def F(s: Setting) -> bool:
    """F: Protected retained primitive difference (PD-F): A plus retention plus protection."""
    return A(s) and ((s.a, s.b) in s.ret) and ((s.a, s.b) in s.prot)


CANDIDATE_PREDICATES: Mapping[str, Callable[[Setting], bool]] = {
    "W": W,
    "A": A,
    "Bs": Bs,
    "Bc": Bc,
    "Bl": Bl,
    "C": C,
    "D": D,
    "E": E,
    "F": F,
}


# ---------------------------------------------------------------------------
# Concrete Minimal Carrier Primitives: D2, D2rev, S2
# ---------------------------------------------------------------------------

D2_REL: Rel = frozenset({(0, 1)})
D2_REV_REL: Rel = frozenset({(1, 0)})
S2_REL: Rel = frozenset({(0, 1), (1, 0)})

D2 = Pointed(2, D2_REL, 0, 1)
D2_REV = Pointed(2, D2_REV_REL, 0, 1)
S2 = Pointed(2, S2_REL, 0, 1)


# ---------------------------------------------------------------------------
# Category of Pointed Witnessed Relations (PrimitiveCats)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PtdRel:
    """Pointed witnessed relation object in category PtdRel."""

    n: int
    r: Rel
    a: int
    b: int

    def __post_init__(self) -> None:
        _validate_pointed(self.n, self.r, self.a, self.b)
        if (self.a, self.b) not in self.r:
            raise ValueError(f"Pointed relation requires (a, b) in r, got ({self.a}, {self.b})")
        validate_typed_fields(self)


@dataclass(frozen=True)
class Hom:
    """Morphism in category PtdRel preserving designated endpoints and arrows."""

    src: PtdRel
    tgt: PtdRel
    f: Func

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def is_valid(self) -> bool:
        if len(self.f) != self.src.n or any(not 0 <= x < self.tgt.n for x in self.f):
            return False
        if self.f[self.src.a] != self.tgt.a or self.f[self.src.b] != self.tgt.b:
            return False
        return all((self.f[x], self.f[y]) in self.tgt.r for (x, y) in self.src.r)


# ---------------------------------------------------------------------------
# Implication Matrix Scan Result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ScanResult:
    """Result of evaluating the 72-cell candidate implication matrix."""

    total: int
    counts: dict[str, int]
    witnesses: dict[str, Setting]
    cotrans_violation_le2: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "counts", FrozenMap(self.counts))
        object.__setattr__(self, "witnesses", FrozenMap(self.witnesses))
        validate_typed_fields(self)
