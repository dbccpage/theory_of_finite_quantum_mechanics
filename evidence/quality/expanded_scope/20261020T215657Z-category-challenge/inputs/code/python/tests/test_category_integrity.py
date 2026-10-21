"""Independent finite law, factorization, ownership and checker controls."""
from dataclasses import FrozenInstanceError
from itertools import product
from pathlib import Path
import sys
import types

import pytest

from src import category_theory as facade
from src.category_theory import finite_category as api


class ClassCallback:
    @property
    def __class__(self):
        raise RuntimeError("admission must not inspect user __class__")


class HostileDict(dict):
    def __len__(self):
        raise RuntimeError("must refuse before user length")

    def items(self):
        raise RuntimeError("must refuse before user iteration")


class HostileTuple(tuple):
    def __len__(self):
        raise RuntimeError("must refuse before user length")

    def __iter__(self):
        raise RuntimeError("must refuse before user iteration")


def arrow_fields():
    return (frozenset({"A", "B"}), {"i": ("A", "A"), "j": ("B", "B"), "f": ("A", "B")},
            {"A": "i", "B": "j"}, {("i", "i"): "i", ("j", "j"): "j", ("f", "i"): "f", ("j", "f"): "f"})


def test_policy_constants_are_explicit_engineering_limits():
    assert (api.MAX_OBJECTS, api.MAX_MORPHISMS, api.MAX_COMPOSITION_ENTRIES) == (64, 64, 4096)
    assert (api.MAX_FACTOR_SOURCES, api.MAX_LABEL_CHARACTERS, api.MAX_INTEGER_BITS) == (4096, 256, 1024)


def test_ghost_composites_and_noncomposable_pairs_are_rejected():
    table = {("i", "i"): "i", ("i", "f"): "f", ("f", "i"): "f", ("f", "f"): "ghost",
             ("ghost", "i"): "ghost", ("i", "ghost"): "ghost"}
    assert not api.FiniteCategory(frozenset({"A"}), {"i": ("A", "A"), "f": ("A", "A")}, {"A": "i"}, table).verify_axioms()
    objects, arrows, identities, composition = arrow_fields()
    composition[("f", "f")] = "f"  # A->B cannot compose with A->B.
    assert not api.FiniteCategory(objects, arrows, identities, composition).verify_axioms()


def test_endpoint_identity_and_composite_typing_guards():
    objects, arrows, identities, composition = arrow_fields()
    unknown = dict(arrows, h=("outside", "A"))
    assert not api.FiniteCategory(objects, unknown, identities, composition).verify_axioms()
    extra_identity = dict(identities, ghost="i")
    assert not api.FiniteCategory(objects, arrows, extra_identity, composition).verify_axioms()
    wrong_codomain = dict(composition)
    wrong_codomain[("f", "i")] = "i"
    assert not api.FiniteCategory(objects, arrows, identities, wrong_codomain).verify_axioms()
    missing = dict(composition)
    del missing[("f", "i")]
    assert not api.FiniteCategory(objects, arrows, identities, missing).verify_axioms()
    assert api.FiniteCategory(frozenset(), {}, {}, {}).verify_axioms() is True


def test_category_owns_immutable_detached_state():
    objects, arrows, identities, composition = arrow_fields()
    category = api.FiniteCategory(objects, arrows, identities, composition)
    equal = api.FiniteCategory(*arrow_fields())
    arrows.clear(); identities.clear(); composition.clear()
    assert category.verify_axioms() and category == equal
    assert category != ClassCallback()
    with pytest.raises(FrozenInstanceError):
        category.objects = frozenset()
    with pytest.raises(TypeError):
        category.composition[("f", "i")] = "i"
    with pytest.raises(api.CategoryLawError, match="already initialized"):
        category.__init__(frozenset(), {}, {}, {})
    assert category.verify_axioms()
    with pytest.raises(TypeError, match="does not admit subclasses"):
        type("UnsafeCategory", (api.FiniteCategory,), {})
    with pytest.raises(TypeError):
        hash(category)  # Explicitly unhashable because its API contains maps.


def test_category_admission_shape_and_resource_refusals():
    objects, arrows, identities, composition = arrow_fields()
    for fields in [
        ({"A"}, arrows, identities, composition),
        (frozenset({1}), {}, {}, {}),
        (objects, HostileDict(arrows), identities, composition),
        (objects, {"f": HostileTuple(("A", "B"))}, identities, composition),
        (objects, {"f": ("A",)}, identities, composition),
        (objects, {ClassCallback(): ("A", "B")}, identities, composition),
    ]:
        with pytest.raises(api.CategoryLawError):
            api.FiniteCategory(*fields)


def test_positive_object_arrow_composition_and_label_policy_edges():
    # The one-object cyclic group C64 reaches both the morphism and complete
    # composition limits. Addition modulo 64 supplies an independent model.
    names = [str(i) for i in range(64)]
    arrows = {name: ("X", "X") for name in names}
    table = {(names[a], names[b]): names[(a + b) % 64] for a, b in product(range(64), repeat=2)}
    assert api.FiniteCategory(frozenset({"X"}), arrows, {"X": "0"}, table).verify_axioms()
    # A discrete category reaches the object limit with only identity arrows.
    objects = frozenset(names)
    assert api.FiniteCategory(objects, {name: (name, name) for name in names},
                              {name: name for name in names}, {(name, name): name for name in names}).verify_axioms()
    label = "x" * 256
    assert api.FiniteCategory(frozenset({label}), {label: (label, label)},
                              {label: label}, {(label, label): label}).verify_axioms()


def test_category_budget_refusals():
    objects, arrows, identities, composition = arrow_fields()
    for fields in [
        (frozenset(str(n) for n in range(65)), {}, {}, {}),
        (frozenset({"A"}), {str(n): ("A", "A") for n in range(65)}, {}, {}),
        (objects, arrows, identities, {(str(n), "i"): "i" for n in range(4097)}),
        (frozenset({"x" * 257}), {}, {}, {}),
    ]:
        with pytest.raises(api.CategoryLawError, match="budget exceeded"):
            api.FiniteCategory(*fields)


def test_all_three_element_unital_operation_tables():
    # Identity 0 fixes five of nine entries. Enumerate the other 3^4=81
    # tables; compare the typed string presentation with independent integer
    # left-translation composition, including non-associative operations.
    labels = ["e", "a", "b"]
    arrows = {label: ("X", "X") for label in labels}
    successes = failures = 0
    for choices in product(range(3), repeat=4):
        operation = {(0, x): x for x in range(3)} | {(x, 0): x for x in range(3)}
        operation.update(dict(zip([(1, 1), (1, 2), (2, 1), (2, 2)], choices, strict=True)))
        translations = {a: [operation[a, x] for x in range(3)] for a in range(3)}
        expected = all([translations[c][translations[b][x]] for x in range(3)] == translations[operation[c, b]]
                       for b, c in product(range(3), repeat=2))
        table = {(labels[a], labels[b]): labels[value] for (a, b), value in operation.items()}
        observed = api.FiniteCategory(frozenset({"X"}), arrows, {"X": "e"}, table).verify_axioms()
        assert observed is expected
        successes += int(expected); failures += int(not expected)
    assert successes > 0 and failures > 0 and successes + failures == 81


def test_factorization_uses_the_exact_common_carrier_and_all_values():
    for report, query in [({0: 10}, {0: 1, 9: 2}), ({0: 10, 9: 20}, {0: 1}),
                          ({0: 10}, {0: 1, 9: 0.5}), ({0: 10}, {0: True}),
                          ({1.0: 10}, {1: 1}), ({0: 10}, {0: 1.0}),
                          (HostileDict({0: 10}), {0: 1}), ({0: 10}, HostileDict({0: 1}))]:
        with pytest.raises(api.CategoryLawError):
            api.factor_report_query(report, query)
        assert api.verify_report_query_factorization(report, query) == (False, {})


def test_exhaustive_three_source_factorizations():
    # A decoder exists exactly when each report fibre has one query value.
    # This oracle uses fibre sets, independently of the implementation's
    # incremental decoder assignment and conflict branch.
    accepted = rejected = 0
    for report_values, query_values in product(product(range(2), repeat=3), repeat=2):
        report = dict(enumerate(report_values)); query = dict(enumerate(query_values))
        fibres = [{query[i] for i in range(3) if report[i] == value} for value in set(report_values)]
        compatible = all(len(fibre) == 1 for fibre in fibres)
        observed, decoder = api.verify_report_query_factorization(report, query)
        assert observed is compatible
        if compatible:
            accepted += 1
            assert set(decoder) == set(report_values)
            assert all(decoder[report[i]] == query[i] for i in range(3))
        else:
            rejected += 1
            assert decoder == {}
    assert accepted + rejected == 64 and accepted > 0 and rejected > 0


def test_factorization_resource_and_ownership_boundaries():
    report = {i: 10 for i in range(4096)}; query = {i: 1 for i in range(4096)}
    decoder = api.factor_report_query(report, query)
    assert decoder == {10: 1}
    decoder[10] = 99
    assert query[0] == 1
    largest_label = (1 << 1024) - 1
    assert api.factor_report_query({largest_label: largest_label}, {largest_label: -largest_label}) == {largest_label: -largest_label}
    with pytest.raises(api.CategoryLawError, match="source budget exceeded"):
        api.factor_report_query({**report, 4096: 10}, {**query, 4096: 1})
    for value in [1 << 1024, -(1 << 20000)]:
        with pytest.raises(api.CategoryLawError, match="bit budget exceeded"):
            api.factor_report_query({0: 10}, {0: value})
        with pytest.raises(api.CategoryLawError, match="bit budget exceeded"):
            facade.arrow_decoder_size(report=((value, 10),), query=((value, 1),))


def test_witness_tables_never_drop_duplicate_keys():
    for rows in [((0, 999), (0, 10), (1, 10), (2, 20)), ((0, 10), (0, 10), (1, 10), (2, 20))]:
        with pytest.raises(api.CategoryLawError, match="duplicate witness source"):
            facade.arrow_decoder_size(report=rows)
    with pytest.raises(api.CategoryLawError, match="duplicate witness source"):
        facade.arrow_decoder_size(query=((0, 99), (0, 1), (1, 1), (2, 0)))
    assert facade.arrow_decoder_size() == 2


def test_facade_quota_refusal_precedes_factor_provider(monkeypatch):
    def must_not_delegate(*args):
        raise AssertionError("oversized witness reached factor provider")
    monkeypatch.setattr(facade, "factor_report_query", must_not_delegate)
    with pytest.raises(api.CategoryLawError, match="witness table source budget exceeded"):
        facade.arrow_decoder_size(report=((0, 10),) * 4097)
    with pytest.raises(api.CategoryLawError, match="integer label bit budget exceeded") as caught:
        facade.arrow_decoder_size(report=(((1 << 1024), 10),))
    assert caught.value.parameters["role"] == "report_0"


def test_witness_container_and_scalar_guards():
    for argument in [HostileTuple(((0, 10),)), ClassCallback(), ((ClassCallback(), 10),),
                     (HostileTuple((0, 10)),), ((0, 10),) * 4097]:
        with pytest.raises(api.CategoryLawError):
            facade.arrow_decoder_size(report=argument)
    with pytest.raises(api.CategoryLawError):
        api.factor_report_query({0: ClassCallback()}, {0: 1})


def test_checker_witnesses_are_computed_and_class_guards_are_safe():
    from src.category_theory import test_finite_category as category_checks
    from src.category_theory import test_arrow_decoder as decoder_checks
    assert (category_checks.witness_decoder(), category_checks.witness_sources(), category_checks.witness_axiom()) == (2, 3, 1)
    assert (decoder_checks.witness_width(), decoder_checks.witness_sources(), decoder_checks.witness_points()) == (2, 3, 2)
    for checks in [category_checks, decoder_checks]:
        assert checks.witness_guard() == "float refused at the public boundary"
        with pytest.raises(checks.ClaimCheckError):
            checks.parse_exact_label(ClassCallback())
        with pytest.raises(KeyError):
            checks._safe_holds({})
        with pytest.raises(KeyError):
            checks._safe_self({})


def test_invalid_checker_candidates_refuse_and_restore_modules(monkeypatch):
    from src.category_theory import test_finite_category as category_checks
    from src.category_theory import test_arrow_decoder as decoder_checks
    name = "category_invalid_lifecycle_guard"
    marker = types.ModuleType(name)
    monkeypatch.setitem(sys.modules, name, marker)
    for checks, anchor in [(category_checks, "return decoder"), (decoder_checks, "return len(decoder)")]:
        source = Path(checks._LIBRARY).read_text()
        for old, new in [(anchor, "return ("), ("from typing import", "from __category_missing_dependency__ import")]:
            assert source.count(old) == 1
            with pytest.raises(checks.ClaimCheckError, match="not counted as a kill"):
                checks._one_mutant(source, ("invalid control", old, new), name, str(checks._LIBRARY), checks._safe_holds)
            assert sys.modules[name] is marker
        own = Path(checks.__file__).read_text()
        with pytest.raises(checks.ClaimCheckError, match="not counted as a kill"):
            checks._one_mutant(own, ("invalid self control", "def witness_guard() -> str:", "def witness_guard("), name, checks.__file__, checks._safe_self)
        assert sys.modules[name] is marker
