"""Exact finite checks for a corrected reading of the relational point-coincidence paper.

The source is paper 003 of ``papers/general_relativity`` (relational point
coincidence, manuscript dated 2026-10-01); line numbers refer to its manuscript. Two parts
are checked here.

Relations. Rows over named attributes with exact atoms (``Fraction`` or ``str``). Every
dependency check below is a statement about one supplied instance. Declared schema
dependencies (the source's set F, Definition 2.1) are not represented, and nothing here
decides implication under F; that decision belongs to the native owner named in the WDP
SQL note (``docs/sql_normal_form_presentation.md``).

Dressing. The symmetric group S3 acts on the six ordered triples of the labels a, b, c by
moving the label at position j to position g(j). The action is a free, transitive left
action. The corrected convention is: u is equivariant when u(g.phi) = g u(phi), and the
dressed configuration is u(phi)^-1 . phi. The source's two printed conventions are encoded
as written, under the names ``source_1_2_*`` and ``prop_4_1_*``.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product

Atom = Fraction | str
Row = tuple[Atom, ...]
Perm = tuple[int, ...]
Config = tuple[str, ...]

MAX_KEY_SEARCH_ATTRIBUTES = 10


# --------------------------------------------------------------------------------------
# Relations over named attributes
# --------------------------------------------------------------------------------------


def _atom(value: object) -> Atom:
    """Admit an exact atom; integers become Fractions, floats and bools are refused."""
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"inexact or boolean atom refused: {value!r}")
    if isinstance(value, Fraction) or isinstance(value, str):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(f"atom must be a Fraction, an int or a str: {value!r}")


@dataclass(frozen=True)
class Relation:
    """A finite set of rows over a sorted, duplicate-free heading of attribute names."""

    heading: tuple[str, ...]
    rows: frozenset[Row]

    def __post_init__(self) -> None:
        if not isinstance(self.heading, tuple):
            raise TypeError("heading must be a tuple of attribute names")
        for name in self.heading:
            if not isinstance(name, str) or not name:
                raise TypeError(f"attribute name must be a nonempty str: {name!r}")
        if tuple(sorted(set(self.heading))) != self.heading:
            raise ValueError("heading must be sorted and free of duplicates")
        if not isinstance(self.rows, frozenset):
            raise TypeError("rows must be a frozenset")
        for row in self.rows:
            if not isinstance(row, tuple) or len(row) != len(self.heading):
                raise ValueError(f"row does not match the heading: {row!r}")
            for value in row:
                if not (isinstance(value, Fraction) or isinstance(value, str)):
                    raise TypeError(f"row value must be a Fraction or a str: {value!r}")


def make_relation(heading: Iterable[str], rows: Iterable[Mapping[str, object]]) -> Relation:
    """Build a relation from rows given as attribute -> value mappings.

    A duplicate attribute name, a row with missing or extra attributes, and a duplicate
    row are refused.
    """
    names = tuple(heading)
    if len(set(names)) != len(names):
        raise ValueError(f"duplicate attribute name in heading: {names!r}")
    ordered = tuple(sorted(names))
    seen: set[Row] = set()
    for row in rows:
        if set(row) != set(ordered):
            raise ValueError(f"row attributes {sorted(row)} differ from heading {list(ordered)}")
        values = tuple(_atom(row[name]) for name in ordered)
        if values in seen:
            raise ValueError(f"duplicate row refused: {values!r}")
        seen.add(values)
    return Relation(ordered, frozenset(seen))


def _attrs(rel: Relation, attrs: Iterable[str]) -> tuple[str, ...]:
    if isinstance(attrs, str):
        raise TypeError("pass a collection of attribute names, not a single str")
    names = tuple(sorted(set(attrs)))
    unknown = [name for name in names if name not in rel.heading]
    if unknown:
        raise ValueError(f"attributes not in heading: {unknown}")
    return names


def _positions(rel: Relation, names: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(rel.heading.index(name) for name in names)


def row_dict(rel: Relation, row: Row) -> dict[str, Atom]:
    return dict(zip(rel.heading, row))


def project(rel: Relation, attrs: Iterable[str]) -> Relation:
    """Projection with set semantics."""
    names = _attrs(rel, attrs)
    pos = _positions(rel, names)
    return Relation(names, frozenset(tuple(row[i] for i in pos) for row in rel.rows))


def natural_join(left: Relation, right: Relation) -> Relation:
    """Natural join on the shared attribute names."""
    heading = tuple(sorted(set(left.heading) | set(right.heading)))
    common = tuple(sorted(set(left.heading) & set(right.heading)))
    left_pos = _positions(left, common)
    right_pos = _positions(right, common)
    joined: set[Row] = set()
    for a in left.rows:
        for b in right.rows:
            if all(a[i] == b[j] for i, j in zip(left_pos, right_pos)):
                merged = dict(zip(left.heading, a))
                merged.update(zip(right.heading, b))
                joined.add(tuple(merged[name] for name in heading))
    return Relation(heading, frozenset(joined))


def instance_satisfies_fd(rel: Relation, lhs: Iterable[str], rhs: Iterable[str]) -> bool:
    """Whether this one instance satisfies lhs -> rhs. Not a schema declaration."""
    lhs_pos = _positions(rel, _attrs(rel, lhs))
    rhs_pos = _positions(rel, _attrs(rel, rhs))
    seen: dict[Row, Row] = {}
    for row in rel.rows:
        key = tuple(row[i] for i in lhs_pos)
        value = tuple(row[i] for i in rhs_pos)
        if seen.setdefault(key, value) != value:
            return False
    return True


def point_coincidence_holds(rel: Relation, attrs: Iterable[str]) -> bool:
    """Source Postulate 2.1 (line 105) read literally: t1[K] = t2[K] implies t1 = t2."""
    pos = _positions(rel, _attrs(rel, attrs))
    return all(
        t1 == t2
        for t1 in rel.rows
        for t2 in rel.rows
        if tuple(t1[i] for i in pos) == tuple(t2[i] for i in pos)
    )


def is_superkey(rel: Relation, attrs: Iterable[str]) -> bool:
    """Instance-level superkey: no two distinct rows agree on attrs."""
    return instance_satisfies_fd(rel, attrs, rel.heading)


def candidate_keys(
    rel: Relation, attributes: Iterable[str] | None = None
) -> tuple[frozenset[str], ...]:
    """Instance-level minimal superkeys among subsets of attributes (default: heading).

    Brute force over subsets in order of size, so at most ten attributes are admitted.
    """
    names = rel.heading if attributes is None else _attrs(rel, attributes)
    if len(names) > MAX_KEY_SEARCH_ATTRIBUTES:
        raise ValueError(
            f"key search admits at most {MAX_KEY_SEARCH_ATTRIBUTES} attributes, got {len(names)}"
        )
    keys: list[frozenset[str]] = []
    for size in range(len(names) + 1):
        for combo in combinations(names, size):
            subset = frozenset(combo)
            if any(key <= subset for key in keys):
                continue
            if is_superkey(rel, subset):
                keys.append(subset)
    return tuple(keys)


def heath_split(
    rel: Relation, x: Iterable[str], y: Iterable[str]
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Component headings (X u Y, X u Z) for disjoint X, Y, with Z the rest of the heading."""
    xs = _attrs(rel, x)
    ys = _attrs(rel, y)
    if set(xs) & set(ys):
        raise ValueError("X and Y must be disjoint")
    zs = tuple(name for name in rel.heading if name not in xs and name not in ys)
    return tuple(sorted(xs + ys)), tuple(sorted(xs + zs))


def join_of_projections(rel: Relation, first: Iterable[str], second: Iterable[str]) -> Relation:
    a = _attrs(rel, first)
    b = _attrs(rel, second)
    if set(a) | set(b) != set(rel.heading):
        raise ValueError("the two components must cover the heading")
    return natural_join(project(rel, a), project(rel, b))


def spurious_rows(rel: Relation, first: Iterable[str], second: Iterable[str]) -> frozenset[Row]:
    """Rows of the rejoined decomposition that are not rows of the original instance."""
    return join_of_projections(rel, first, second).rows - rel.rows


# --------------------------------------------------------------------------------------
# Permutations, the S3 action and its cyclic subgroup
# --------------------------------------------------------------------------------------

LABELS: tuple[str, ...] = ("a", "b", "c")
CONFIGURATIONS: tuple[Config, ...] = tuple(permutations(LABELS))
_CONFIGURATION_SET = frozenset(CONFIGURATIONS)
IDENTITY: Perm = (0, 1, 2)


def _perm(p: object) -> Perm:
    if not isinstance(p, tuple) or len(p) != 3:
        raise TypeError(f"permutation must be a 3-tuple: {p!r}")
    for entry in p:
        if not (isinstance(entry, int) and not isinstance(entry, bool)):
            raise TypeError(f"permutation entry must be an int, not {entry!r}")
    if sorted(p) != [0, 1, 2]:
        raise ValueError(f"not a permutation of 0, 1, 2: {p!r}")
    return p


def _config(phi: object) -> Config:
    if not isinstance(phi, tuple) or len(phi) != 3:
        raise TypeError(f"configuration must be a 3-tuple: {phi!r}")
    for label in phi:
        if not isinstance(label, str):
            raise TypeError(f"label must be a str: {label!r}")
    if sorted(phi) != list(LABELS):
        raise ValueError(f"configuration must order the labels a, b, c: {phi!r}")
    return phi


def _compose(p: Perm, q: Perm) -> Perm:
    return (p[q[0]], p[q[1]], p[q[2]])


def _inverse(p: Perm) -> Perm:
    out = [0, 0, 0]
    for i, image in enumerate(p):
        out[image] = i
    return (out[0], out[1], out[2])


def _act(g: Perm, phi: Config) -> Config:
    out = ["", "", ""]
    for j, label in enumerate(phi):
        out[g[j]] = label
    return (out[0], out[1], out[2])


def compose(p: Perm, q: Perm) -> Perm:
    """Group product p q: apply q first, then p."""
    return _compose(_perm(p), _perm(q))


def inverse(p: Perm) -> Perm:
    return _inverse(_perm(p))


def act(g: Perm, phi: Config) -> Config:
    """Left action g.phi: the label at position j moves to position g(j)."""
    return _act(_perm(g), _config(phi))


@dataclass(frozen=True)
class FiniteGroup:
    """A group of permutations of 0, 1, 2, closed under product and inverse."""

    name: str
    elements: tuple[Perm, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.elements, tuple):
            raise TypeError("group elements must be a tuple")
        for g in self.elements:
            _perm(g)
        if len(set(self.elements)) != len(self.elements):
            raise ValueError("repeated group element")
        members = set(self.elements)
        if IDENTITY not in members:
            raise ValueError("identity missing")
        for g in self.elements:
            if inverse(g) not in members:
                raise ValueError(f"not closed under inverse at {g!r}")
            for h in self.elements:
                if compose(g, h) not in members:
                    raise ValueError(f"not closed under product at {g!r}, {h!r}")

    def contains(self, g: object) -> bool:
        return _perm(g) in self.elements

    def is_abelian(self) -> bool:
        return all(compose(g, h) == compose(h, g) for g in self.elements for h in self.elements)


S3 = FiniteGroup("S3", tuple(permutations(range(3))))
Z3 = FiniteGroup("Z3", ((0, 1, 2), (1, 2, 0), (2, 0, 1)))  # rotations; Z3 as A3 in S3

DressingField = Mapping[Config, Perm]


def _field(group: FiniteGroup, u: DressingField) -> DressingField:
    if not isinstance(u, Mapping):
        raise TypeError("dressing field must be a mapping from configurations to elements")
    if set(u) != _CONFIGURATION_SET:
        raise ValueError("dressing field must be defined on every configuration")
    for g in u.values():
        if not group.contains(g):
            raise ValueError(f"value {g!r} is not an element of {group.name}")
    return u


def orbits(group: FiniteGroup) -> tuple[tuple[Config, ...], ...]:
    found: list[tuple[Config, ...]] = []
    for phi in CONFIGURATIONS:
        if any(phi in orbit for orbit in found):
            continue
        found.append(tuple(sorted({act(g, phi) for g in group.elements})))
    return tuple(found)


def is_free(group: FiniteGroup) -> bool:
    return all(
        act(g, phi) != phi for g in group.elements if g != IDENTITY for phi in CONFIGURATIONS
    )


def all_maps(group: FiniteGroup) -> Iterator[dict[Config, Perm]]:
    """Every map from the six configurations to the group (|G|^6 maps)."""
    for values in product(group.elements, repeat=len(CONFIGURATIONS)):
        yield dict(zip(CONFIGURATIONS, values))


def maps_satisfying(
    group: FiniteGroup, condition: Callable[[FiniteGroup, DressingField], bool]
) -> tuple[dict[Config, Perm], ...]:
    return tuple(u for u in all_maps(group) if condition(group, u))


def field_values(u: DressingField) -> tuple[Perm, ...]:
    return tuple(u[phi] for phi in CONFIGURATIONS)


def is_equivariant(group: FiniteGroup, u: DressingField) -> bool:
    """Corrected convention: u(g.phi) = g u(phi) for all g and phi."""
    u = _field(group, u)
    return all(
        u[_act(g, phi)] == _compose(g, u[phi]) for g in group.elements for phi in CONFIGURATIONS
    )


def is_right_equivariant(group: FiniteGroup, u: DressingField) -> bool:
    """u(g.phi) = u(phi) g^-1: consistent, and the inverse of an equivariant field."""
    u = _field(group, u)
    return all(
        u[_act(g, phi)] == _compose(u[phi], _inverse(g))
        for g in group.elements
        for phi in CONFIGURATIONS
    )


def dress(u: DressingField, phi: Config) -> Config:
    """Corrected dressing: phi^u := u(phi)^-1 . phi."""
    return _act(_inverse(_perm(u[_config(phi)])), phi)


def reference_dressing_field(group: FiniteGroup) -> dict[Config, Perm]:
    """For a free action: u(g.rep) = g, with rep the first configuration of each orbit."""
    if not is_free(group):
        raise ValueError(f"{group.name} does not act freely")
    u: dict[Config, Perm] = {}
    for orbit in orbits(group):
        representative = orbit[0]
        for g in group.elements:
            u[_act(g, representative)] = g
    return u


# Source section 1.2, lines 62-66. The field transforms as phi^h = rho(h^-1) phi (line 63),
# the dressing field as u^h = h^-1 u (lines 62 and 66), and phi^u = rho(u) phi (line 64).


def source_1_2_transform(h: Perm, phi: Config) -> Config:
    return _act(_inverse(_perm(h)), _config(phi))


def source_1_2_is_equivariant(group: FiniteGroup, u: DressingField) -> bool:
    u = _field(group, u)
    return all(
        u[source_1_2_transform(h, phi)] == _compose(_inverse(h), u[phi])
        for h in group.elements
        for phi in CONFIGURATIONS
    )


def source_1_2_dress(u: DressingField, phi: Config) -> Config:
    return _act(_perm(u[_config(phi)]), phi)


def source_1_2_invariance_failures(
    group: FiniteGroup, u: DressingField
) -> tuple[tuple[Config, Perm, Config, Config], ...]:
    """Every (phi, h, (phi^h)^u, phi^u) where the claimed invariance of line 66 fails."""
    u = _field(group, u)
    failures = []
    for phi in CONFIGURATIONS:
        for h in group.elements:
            transformed = source_1_2_dress(u, source_1_2_transform(h, phi))
            original = source_1_2_dress(u, phi)
            if transformed != original:
                failures.append((phi, h, transformed, original))
    return tuple(failures)


# Source Proposition 4.1, lines 162 and 172-173. The field transforms as phi^g = rho(g) phi,
# the dressing field as u(phi^g) = g^-1 u(phi), and Pi(phi) = rho(u(phi)) phi.


def prop_4_1_is_equivariant(group: FiniteGroup, u: DressingField) -> bool:
    u = _field(group, u)
    return all(
        u[_act(g, phi)] == _compose(_inverse(g), u[phi])
        for g in group.elements
        for phi in CONFIGURATIONS
    )


def prop_4_1_dress(u: DressingField, phi: Config) -> Config:
    return _act(_perm(u[_config(phi)]), phi)


def prop_4_1_consistency_failures(group: FiniteGroup) -> tuple[tuple[Perm, Perm], ...]:
    """Pairs for which u(g1 g2 . phi) computed in one step and in two steps disagree.

    One step gives (g1 g2)^-1 u(phi); two steps give g1^-1 g2^-1 u(phi). Cancelling u(phi),
    the line-172 condition is satisfiable only if every listed pair is absent.
    """
    return tuple(
        (g1, g2)
        for g1 in group.elements
        for g2 in group.elements
        if _inverse(_compose(g1, g2)) != _compose(_inverse(g1), _inverse(g2))
    )


def prop_4_1_step_failures(
    group: FiniteGroup,
) -> tuple[tuple[Perm, Perm, Config, Config, Config], ...]:
    """Every (g, a, phi, lhs, rhs) where line 173's rewrite fails, with a in place of u(phi).

    lhs = rho(g^-1 a) rho(g) phi, the expression before the rewrite;
    rhs = rho(a) phi, the value the rewrite reaches by moving rho(g^-1) past rho(a).
    """
    failures = []
    for g in group.elements:
        for a in group.elements:
            for phi in CONFIGURATIONS:
                lhs = _act(_compose(_inverse(g), a), _act(g, phi))
                rhs = _act(a, phi)
                if lhs != rhs:
                    failures.append((g, a, phi, lhs, rhs))
    return tuple(failures)
