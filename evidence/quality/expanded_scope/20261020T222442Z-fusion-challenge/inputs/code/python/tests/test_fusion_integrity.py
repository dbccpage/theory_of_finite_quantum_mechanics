"""Canonical exact values, owned fusion presentations and honest checker controls."""
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys
import types

import pytest

from src import fusion_categories as facade
from src.fusion_categories import fusion_ring as api
from src.fusion_categories import test_fusion_control as checker


class ClassCallback:
    @property
    def __class__(self):
        raise RuntimeError("caller class callback executed")


class HostileTuple(tuple):
    def __len__(self):
        raise RuntimeError("caller sequence callback executed")


class LeakingInt(int):
    def __rmul__(self, other):
        return 0.5


class LeakingFraction(Q):
    def __mul__(self, other):
        return 0.5


def test_exact_scalar_admission_precedes_overrides():
    for invalid in [True, 0.5, LeakingInt(2), LeakingFraction(1), ClassCallback()]:
        with pytest.raises(api.FusionError):
            api.AbelianGroup([invalid])
        with pytest.raises(api.FusionError):
            api.QuadraticRational(invalid, 0, 2)
        with pytest.raises(facade.PackageError):
            facade.checked_int(invalid)
        with pytest.raises(checker.CheckError):
            checker.checked_int(invalid)


def test_specific_scalar_refusals_before_downstream_parsing():
    for invalid, kind in [(0.5, "float"), (True, "boolean")]:
        for function, error, boundary in [
            (lambda x: api.AbelianGroup([x]), api.FusionError, "fusion"),
            (facade.checked_int, facade.PackageError, "package"),
            (checker.checked_int, checker.CheckError, "harness"),
        ]:
            with pytest.raises(error) as caught:
                function(invalid)
            expected = f"float refused at the {boundary} boundary" if kind == "float" else "boolean refused where an integer was required"
            assert caught.value.invariant == expected


def test_oversized_group_refuses_before_scalar_provider(monkeypatch):
    def unreachable(*args):
        raise AssertionError("oversized sequence reached scalar parsing")
    monkeypatch.setattr(api, "_modulus_at", unreachable)
    with pytest.raises(api.FusionError, match="sequence entry budget") as caught:
        api.AbelianGroup([2] * 6)
    assert caught.value.parameters["role"] == "moduli"


def test_quadratic_canonical_equality_and_operations():
    x = api.QuadraticRational(1, 0, 2)
    y = api.QuadraticRational(1, 0, 3)
    assert x == y and hash(x) == hash(y) and x.disc == 1
    root = api.QuadraticRational(0, 1, 2)
    assert root * root == api.QuadraticRational(2, 0, 1)
    assert x * root == root and root * x == root
    assert x + root == root + x == api.QuadraticRational(1, 1, 2)
    assert api.QuadraticRational(0, 1, 8) == root.scale_int(2)
    assert api.QuadraticRational(1, 2, 9) == api.QuadraticRational(7, 0, 1)
    assert api.QuadraticRational(0, 0, 5) == api.QuadraticRational(0, 0, 1)
    assert not (x == ClassCallback())
    with pytest.raises(api.FusionError, match="discriminants differ"):
        root + api.QuadraticRational(0, 1, 3)
    with pytest.raises(api.FusionError, match="admitted values"):
        root * ClassCallback()
    with pytest.raises(api.FusionError):
        root.scale_int(LeakingInt(1))


def test_immutable_values_and_validated_tables():
    moduli = [2, 3]
    group = api.AbelianGroup(moduli)
    moduli[0] = 9
    assert group.moduli == [2, 3]
    group.moduli[0] = 9
    assert group.order == 6
    data = [1]
    names = ["one"]
    table = api.FusionTable(1, data, names)
    ring = api.FusionRing(table)
    data[0] = 0
    names[0] = "changed"
    table.names[0] = "changed"
    assert ring.n(0, 0, 0) == 1 and ring.names == ["one"]
    for value, field, replacement, args in [
        (group, "_order", 1, ([2],)),
        (table, "_n", (0,), (1, [1])),
        (ring, "_rank", 5, (table,)),
        (api.QuadraticRational(1, 0, 2), "a", Q(5), (5, 0, 2)),
    ]:
        with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
            setattr(value, field, replacement)
        with pytest.raises(api.FusionError, match="already initialized"):
            value.__init__(*args)
        with pytest.raises(TypeError):
            type("Child", (type(value),), {})
    with pytest.raises(api.FusionError, match="admitted table"):
        api.FusionRing(ClassCallback())


def test_group_mixed_radix_against_tuple_addition():
    for moduli in [(2,), (3, 2), (2, 2, 2), (2, 2, 2, 2, 2)]:
        group = api.AbelianGroup(moduli)
        for a, b in product(range(group.order), repeat=2):
            digits = [(x + y) % m for x, y, m in zip(group.digits(a), group.digits(b), moduli)]
            assert group.digits(group.add(a, b)) == digits
            assert group.label(group.digits(a)) == a
            assert group.add(a, group.negate(a)) == 0
        for bad in [-1, group.order]:
            with pytest.raises(api.FusionError):
                group.digits(bad)
        with pytest.raises(api.FusionError):
            group.label([0] * (len(moduli) + 1))
        with pytest.raises(api.FusionError):
            group.label([m for m in moduli])


def test_shape_and_representation_refusals():
    for bad in [HostileTuple([2]), "2", {2}, ClassCallback()]:
        with pytest.raises(api.FusionError):
            api.AbelianGroup(bad)
    for bad in [[], [1], [33], [2] * 6]:
        with pytest.raises(api.FusionError):
            api.AbelianGroup(bad)
    for bad in [0, 33, True, ClassCallback()]:
        with pytest.raises(api.FusionError):
            api.FusionTable(bad, [])
    for bad in [[], [[[1, 0]]], HostileTuple([[[1]]]), [[HostileTuple([1])]], [HostileTuple([[1]])]]:
        with pytest.raises(api.FusionError):
            api.FusionTable.from_3d(bad)
    for multiplicities, names in [([-1], None), ([1, 1], None), ([1], []), ([1], [ClassCallback()]), ([1], [""]), (HostileTuple([1]), None)]:
        with pytest.raises(api.FusionError):
            api.FusionTable(1, multiplicities, names)
    ring = api.FusionRing.fibonacci()
    for bad in [-1, 2, 0.5]:
        with pytest.raises(api.FusionError):
            ring.n(bad, 0, 0)
    with pytest.raises(api.FusionError):
        ring.fusion_path_count(0, HostileTuple([1]), 0)


def test_law_verification_against_explicit_finite_contractions():
    for k in range(7):
        tensor = (((1, 0), (0, 1)), ((0, 1), (1, k)))
        table = api.FusionTable.from_3d(tensor)
        assert table.first_defect() is None
        ring = api.FusionRing(table)
        for a, b, c, d in product(range(2), repeat=4):
            left = sum(tensor[a][b][x] * tensor[x][c][d] for x in range(2))
            right = sum(tensor[b][c][x] * tensor[a][x][d] for x in range(2))
            assert left == right
        dim = ring.frobenius_perron_dimension(1)
        assert dim * dim == api.QuadraticRational(1, 0, 1) + dim.scale_int(k)
    broken = api.FusionTable.from_3d((((0, 0), (0, 1)), ((0, 1), (1, 1))))
    assert broken.first_defect().defect_type == api.RingDefectType.UNIT
    with pytest.raises(api.FusionError, match="failed a ring law"):
        api.FusionRing(broken)


def test_dimensions_and_paths_against_independent_integer_enumeration():
    expected = [api.QuadraticRational(4, 0, 1), api.QuadraticRational(Q(5, 2), Q(1, 2), 5), api.QuadraticRational(4, 0, 1), api.QuadraticRational(6, 0, 1)]
    for ring, global_dimension in zip([api.FusionRing.ising(), api.FusionRing.fibonacci(), api.FusionRing.toric_code(), api.FusionRing.rep_s3()], expected):
        assert ring.global_dimension_squared() == global_dimension
        assert ring.global_dimension_squared() == global_dimension  # cached dimensions remain coherent
        for length in range(5):
            word = [1] * length
            counts = {0: 1}
            for factor in word:
                counts = {c: sum(counts.get(a, 0) * ring.n(factor, a, c) for a in range(ring.rank)) for c in range(ring.rank)}
            for target in range(ring.rank):
                assert ring.fusion_path_count(0, word, target) == counts.get(target, 0)
        matrix = ring.fusion_matrix(1)
        matrix[0][0] = -1
        assert ring.fusion_matrix(1)[0][0] >= 0


def test_distinct_ring_law_refusals():
    # This commutative unital table has orthonormal unit channels but fails
    # (x*x)*y = x*(x*y): left is y, right is zero.
    nonassoc = (((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                ((0, 1, 0), (1, 0, 0), (0, 0, 0)),
                ((0, 0, 1), (0, 0, 0), (1, 0, 0)))
    table = api.FusionTable.from_3d(nonassoc)
    assert table.n(1, 1, 0) * table.n(0, 2, 2) == 1
    assert sum(table.n(1, 2, x) * table.n(1, x, 2) for x in range(3)) == 0
    assert table.first_defect().defect_type == api.RingDefectType.ASSOCIATIVITY
    noncomm = [list(map(list, plane)) for plane in nonassoc]
    noncomm[1][2][0] = 1
    assert api.FusionTable.from_3d(noncomm).first_defect().defect_type == api.RingDefectType.COMMUTATIVITY
    no_dual = (((1, 0), (0, 1)), ((0, 1), (0, 1)))
    assert api.FusionTable.from_3d(no_dual).first_defect().defect_type == api.RingDefectType.DUALITY


def test_declared_budget_edges_and_preflight(monkeypatch):
    assert (api.MAX_INPUT_BITS, api.MAX_WORK_BITS, api.MAX_RANK, api.MAX_DISCRIMINANT, api.MAX_GROUP_FACTORS, api.MAX_LAW_PRODUCTS) == (1024, 8192, 32, 1_000_000, 5, 2_000_000)
    edge = (1 << 1024) - 1
    assert api.QuadraticRational(edge, 0, 1).a == edge
    assert facade.checked_int(edge) == checker.checked_int(edge) == edge
    for value in [1 << 1024, -(1 << 1024)]:
        for fn in [facade.checked_int, checker.checked_int, lambda x: api.QuadraticRational(x, 0, 1), lambda x: api.FusionTable(1, [x])]:
            with pytest.raises((api.FusionError, facade.PackageError, checker.CheckError), match="bit budget"):
                fn(value)
    assert api.QuadraticRational(0, 1, 1_000_000) == api.QuadraticRational(1000, 0, 1)
    for disc in [0, -1, 1_000_001]:
        with pytest.raises(api.FusionError):
            api.QuadraticRational(0, 1, disc)
    assert api.FusionTable(1, [1], ["x" * 256]).names == ["x" * 256]
    assert api.FusionTable(32, [0] * (32 ** 3)).rank == 32
    with pytest.raises(api.FusionError, match="product budget"):
        api.FusionTable(32, [0] * (32 ** 3)).first_defect()
    with pytest.raises(api.FusionError, match="name length"):
        api.FusionTable(1, [1], ["x" * 257])
    ring = api.FusionRing.fibonacci()
    assert ring.fusion_path_count(0, [0] * api.MAX_FUSION_WORD, 0) == 1
    with pytest.raises(api.FusionError):
        ring.fusion_path_count(0, [0] * (api.MAX_FUSION_WORD + 1), 0)
    monkeypatch.setattr(api, "MAX_WORK_BITS", 4)
    with pytest.raises(api.FusionError, match="bit budget") as work:
        ring.fusion_path_count(0, [1] * 9, 0)
    assert work.value.parameters["role"] == "fusion path count"
    monkeypatch.setattr(api, "MAX_LAW_PRODUCTS", 1)
    with pytest.raises(api.FusionError, match="product budget") as law:
        api.FusionTable(1, [1]).first_defect()
    assert law.value.parameters["role"] == "fusion laws"
    with pytest.raises(api.FusionError, match="product budget") as path:
        ring.fusion_path_count(0, [0], 0)
    assert path.value.parameters["role"] == "fusion paths"


def test_stdout_failures_have_status_two(monkeypatch):
    class Broken:
        def write(self, text):
            raise BrokenPipeError("unavailable")
        def flush(self):
            pass
    monkeypatch.setattr(sys, "stdout", Broken())
    assert api.main() == facade.main() == 2
    def refuse():
        raise api.FusionError("test refusal")
    monkeypatch.setattr(api, "ising_global_dimension_rational", refuse)
    monkeypatch.setattr(facade, "ising_global_dimension_rational", refuse)
    assert api.main() == facade.main() == 2


def test_candidate_protocol_and_module_ownership():
    source = Path(checker.__file__).read_text()
    prior = types.ModuleType("sentinel")
    name = "fusion_prior_binding"
    previous = sys.modules.get(name)
    sys.modules[name] = prior
    try:
        for invalid in ["x = (", 'raise RuntimeError("load")']:
            with pytest.raises(checker.CheckError, match="not counted as a kill"):
                checker._killed_one("x = 1", "invalid", "x = 1", invalid, name, "src.fusion_categories", lambda ns: True)
            assert sys.modules[name] is prior
        assert checker._killed_one("x = 1", "semantic", "x = 1", "x = 2", name, "src.fusion_categories", lambda ns: ns["x"] == 1)
        assert sys.modules[name] is prior
        def infrastructure(ns):
            raise RuntimeError("oracle unavailable")
        with pytest.raises(RuntimeError, match="oracle unavailable"):
            checker._killed_one("x = 1", "infra", "x = 1", "x = 2", name, "src.fusion_categories", infrastructure)
        assert sys.modules[name] is prior
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
    assert "Gate 5 measurement:" not in source
