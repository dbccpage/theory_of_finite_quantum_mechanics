"""Exact checks for the corrected relational point-coincidence statements.

Source rows are copied from the source paper's ``code/tests/test_relational_spacetime.py``
(lines 18-29 and 62-69). AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

import pytest

from relational_coincidence.relational_coincidence import (
    CONFIGURATIONS,
    IDENTITY,
    S3,
    Z3,
    Relation,
    act,
    all_maps,
    candidate_keys,
    compose,
    dress,
    field_values,
    heath_split,
    instance_satisfies_fd,
    inverse,
    is_equivariant,
    is_free,
    is_right_equivariant,
    is_superkey,
    join_of_projections,
    make_relation,
    maps_satisfying,
    natural_join,
    orbits,
    point_coincidence_holds,
    prop_4_1_consistency_failures,
    prop_4_1_dress,
    prop_4_1_is_equivariant,
    prop_4_1_step_failures,
    reference_dressing_field,
    source_1_2_dress,
    source_1_2_invariance_failures,
    source_1_2_is_equivariant,
    source_1_2_transform,
    spurious_rows,
)

K = frozenset({"phi0", "phi1", "phi2", "phi3"})
SOURCE_HEADING = ("phi0", "phi1", "phi2", "phi3", "matter_density", "kretschmann")


def source_event_rows() -> Relation:
    """test_relational_spacetime.py lines 18-29, value for value."""
    t1 = {
        "phi0": Fraction(1, 1), "phi1": Fraction(0, 1), "phi2": Fraction(0, 1),
        "phi3": Fraction(0, 1), "matter_density": Fraction(10, 1), "kretschmann": Fraction(48, 1),
    }
    t2 = {
        "phi0": Fraction(2, 1), "phi1": Fraction(1, 1), "phi2": Fraction(0, 1),
        "phi3": Fraction(0, 1), "matter_density": Fraction(5, 1), "kretschmann": Fraction(12, 1),
    }
    t3 = {
        "phi0": Fraction(3, 1), "phi1": Fraction(1, 1), "phi2": Fraction(1, 1),
        "phi3": Fraction(1, 1), "matter_density": Fraction(1, 1), "kretschmann": Fraction(3, 1),
    }
    return make_relation(SOURCE_HEADING, [t1, t2, t3])


def source_observer_rows() -> Relation:
    """test_relational_spacetime.py lines 62-69, value for value."""
    t1 = {
        "phi0": Fraction(1), "phi1": Fraction(0), "phi2": Fraction(0), "phi3": Fraction(0),
        "obs_alpha_curr": Fraction(100), "obs_beta_temp": Fraction(300),
    }
    t2 = {
        "phi0": Fraction(2), "phi1": Fraction(1), "phi2": Fraction(0), "phi3": Fraction(0),
        "obs_alpha_curr": Fraction(200), "obs_beta_temp": Fraction(273),
    }
    heading = ("phi0", "phi1", "phi2", "phi3", "obs_alpha_curr", "obs_beta_temp")
    return make_relation(heading, [t1, t2])


def boolean_relations(heading: tuple[str, ...]):
    """Every relation over the heading with values 0 and 1 (2^(2^n) instances)."""
    tuples = list(product((0, 1), repeat=len(heading)))
    for mask in range(2 ** len(tuples)):
        chosen = [t for i, t in enumerate(tuples) if mask >> i & 1]
        yield make_relation(heading, [dict(zip(heading, t)) for t in chosen])


def subsets(names):
    for size in range(len(names) + 1):
        yield from (frozenset(c) for c in combinations(names, size))


# ---------------------------------------------------------------- point coincidence ----


def test_source_rows_are_reproduced_exactly():
    rel = source_event_rows()
    assert rel.heading == ("kretschmann", "matter_density", "phi0", "phi1", "phi2", "phi3")
    expected = {(48, 10, 1, 0, 0, 0), (12, 5, 2, 1, 0, 0), (3, 1, 3, 1, 1, 1)}
    assert rel.rows == frozenset(tuple(Fraction(v) for v in row) for row in expected)
    assert all(isinstance(v, Fraction) for row in rel.rows for v in row)


def test_four_invariants_are_a_superkey_of_the_source_rows():
    rel = source_event_rows()
    assert point_coincidence_holds(rel, K)
    assert is_superkey(rel, K)


def test_phi0_alone_is_a_superkey_of_the_source_rows():
    assert is_superkey(source_event_rows(), {"phi0"})


def test_four_invariants_are_not_a_candidate_key_of_the_source_rows():
    keys = candidate_keys(source_event_rows())
    assert K not in keys
    assert keys == (
        frozenset({"kretschmann"}),
        frozenset({"matter_density"}),
        frozenset({"phi0"}),
        frozenset({"phi1", "phi2"}),
        frozenset({"phi1", "phi3"}),
    )
    within_k = candidate_keys(source_event_rows(), K)
    assert within_k == (
        frozenset({"phi0"}),
        frozenset({"phi1", "phi2"}),
        frozenset({"phi1", "phi3"}),
    )


def test_source_line_38_assertion_already_contradicts_minimality():
    rel = source_event_rows()
    assert instance_satisfies_fd(rel, {"phi1", "phi2", "phi3"}, {"matter_density"})
    assert is_superkey(rel, {"phi1", "phi2", "phi3"})


def test_constructed_instance_has_the_four_invariants_as_its_only_candidate_key():
    base = {"matter_density": Fraction(7, 2), "kretschmann": Fraction(48)}
    rows = []
    for unit in [None, "phi0", "phi1", "phi2", "phi3"]:
        row = {name: Fraction(1 if name == unit else 0) for name in K}
        row.update(base)
        rows.append(row)
    rel = make_relation(SOURCE_HEADING, rows)
    assert candidate_keys(rel) == (K,)
    for dropped in sorted(K):
        assert not is_superkey(rel, K - {dropped})


def test_point_coincidence_is_the_superkey_property_on_every_boolean_instance():
    heading = ("A", "B", "C")
    checked = superkey_not_minimal = 0
    for rel in boolean_relations(heading):
        keys = candidate_keys(rel)
        for attrs in subsets(heading):
            assert point_coincidence_holds(rel, attrs) == is_superkey(rel, attrs)
            if is_superkey(rel, attrs) and attrs not in keys:
                superkey_not_minimal += 1
            checked += 1
    assert checked == 256 * 8
    assert superkey_not_minimal > 0


def test_relation_inputs_are_exact_and_typed():
    with pytest.raises(TypeError):
        make_relation(("A",), [{"A": 0.5}])
    with pytest.raises(TypeError):
        make_relation(("A",), [{"A": True}])
    with pytest.raises(ValueError):
        make_relation(("A",), [{"A": 1}, {"A": Fraction(1)}])
    with pytest.raises(ValueError):
        make_relation(("A", "B"), [{"A": 1}])
    with pytest.raises(ValueError):
        make_relation(("A", "A"), [])
    with pytest.raises(TypeError):
        Relation(("A",), frozenset({(0.5,)}))
    with pytest.raises(TypeError):
        is_superkey(source_event_rows(), "phi0")
    assert make_relation(("A",), [{"A": 3}]).rows == frozenset({(Fraction(3),)})
    wide = tuple(f"x{i:02d}" for i in range(11))
    with pytest.raises(ValueError):
        candidate_keys(make_relation(wide, [dict.fromkeys(wide, 0)]))


# ----------------------------------------------------------------------------- Heath ----


def test_source_observer_sheets_rejoin_losslessly():
    rel = source_observer_rows()
    assert instance_satisfies_fd(rel, K, {"obs_alpha_curr"})
    first, second = heath_split(rel, K, {"obs_alpha_curr"})
    assert set(second) == K | {"obs_beta_temp"}
    assert join_of_projections(rel, first, second) == rel


def test_heath_on_every_boolean_instance_over_three_attributes():
    heading = ("A", "B", "C")
    splits = [(x, y) for x in subsets(heading) if x for y in subsets(set(heading) - x) if y]
    assert len(splits) == 12
    fd_cases = lossless_without_fd = 0
    for rel in boolean_relations(heading):
        for x, y in splits:
            first, second = heath_split(rel, x, y)
            joined = join_of_projections(rel, first, second)
            assert rel.rows <= joined.rows
            if instance_satisfies_fd(rel, x, y):
                assert joined == rel
                fd_cases += 1
            elif joined == rel:
                lossless_without_fd += 1
    assert fd_cases > 0
    assert lossless_without_fd > 0  # the instance FD is sufficient, not necessary


def test_negative_control_coincident_events_give_spurious_rows():
    shared = {"phi0": 1, "phi1": 0, "phi2": 0, "phi3": 0}
    rows = [
        {**shared, "obs_alpha_curr": 100, "obs_beta_temp": 300},
        {**shared, "obs_alpha_curr": 200, "obs_beta_temp": 273},
    ]
    rel = make_relation(rows[0].keys(), rows)
    assert not instance_satisfies_fd(rel, K, {"obs_alpha_curr"})
    first, second = heath_split(rel, K, {"obs_alpha_curr"})
    extra = {tuple(zip(rel.heading, row)) for row in spurious_rows(rel, first, second)}
    assert extra == {
        tuple(sorted({**shared, "obs_alpha_curr": 100, "obs_beta_temp": 273}.items())),
        tuple(sorted({**shared, "obs_alpha_curr": 200, "obs_beta_temp": 300}.items())),
    }


def test_negative_control_plain_three_attribute_instance():
    rel = make_relation(("A", "B", "C"), [{"A": 0, "B": 0, "C": 0}, {"A": 0, "B": 1, "C": 1}])
    assert not instance_satisfies_fd(rel, {"A"}, {"B"})
    first, second = heath_split(rel, {"A"}, {"B"})
    assert (first, second) == (("A", "B"), ("A", "C"))
    assert spurious_rows(rel, first, second) == frozenset(
        {(Fraction(0), Fraction(0), Fraction(1)), (Fraction(0), Fraction(1), Fraction(0))}
    )


def test_lossless_snapshot_does_not_license_component_edits():
    """WDP SQL note, S,J,T countermodel: F = {SJ -> T, T -> J}, split (J,T), (S,T)."""
    snapshot = make_relation(
        ("S", "J", "T"), [{"S": "s0", "J": "j", "T": "t0"}, {"S": "s1", "J": "j", "T": "t1"}]
    )
    assert instance_satisfies_fd(snapshot, {"S", "J"}, {"T"})
    assert instance_satisfies_fd(snapshot, {"T"}, {"J"})
    assert join_of_projections(snapshot, {"J", "T"}, {"S", "T"}) == snapshot
    jt = make_relation(("J", "T"), [{"J": "j", "T": "t0"}, {"J": "j", "T": "t1"}])
    st = make_relation(("S", "T"), [{"S": "s", "T": "t0"}, {"S": "s", "T": "t1"}])
    assert instance_satisfies_fd(jt, {"T"}, {"J"})
    rejoined = natural_join(jt, st)
    assert not instance_satisfies_fd(rejoined, {"S", "J"}, {"T"})


# -------------------------------------------------------------------------- dressing ----


@pytest.fixture(scope="module")
def s3_fields():
    found = {"left": [], "right": [], "source_1_2": [], "prop_4_1": []}
    for u in all_maps(S3):
        if is_equivariant(S3, u):
            found["left"].append(u)
        if is_right_equivariant(S3, u):
            found["right"].append(u)
        if source_1_2_is_equivariant(S3, u):
            found["source_1_2"].append(u)
        if prop_4_1_is_equivariant(S3, u):
            found["prop_4_1"].append(u)
    return found


def test_s3_acts_freely_transitively_on_the_left():
    assert len(S3.elements) == 6 and not S3.is_abelian()
    assert len(CONFIGURATIONS) == 6 and is_free(S3)
    assert orbits(S3) == (tuple(sorted(CONFIGURATIONS)),)
    for g, h, phi in product(S3.elements, S3.elements, CONFIGURATIONS):
        assert act(g, act(h, phi)) == act(compose(g, h), phi)
    assert all(act(IDENTITY, phi) == phi for phi in CONFIGURATIONS)


def test_exactly_six_equivariant_dressing_fields_out_of_all_maps(s3_fields):
    assert len(s3_fields["left"]) == 6
    assert {u[("a", "b", "c")] for u in s3_fields["left"]} == set(S3.elements)


def test_corrected_dressing_is_invariant_idempotent_and_one_representative(s3_fields):
    for u in s3_fields["left"]:
        for phi, g in product(CONFIGURATIONS, S3.elements):
            assert dress(u, act(g, phi)) == dress(u, phi)
        for phi in CONFIGURATIONS:
            assert dress(u, dress(u, phi)) == dress(u, phi)
        assert len({dress(u, phi) for phi in CONFIGURATIONS}) == 1


def test_idempotence_follows_from_equivariance(s3_fields):
    for u in s3_fields["left"]:
        for phi in CONFIGURATIONS:
            assert u[dress(u, phi)] == IDENTITY


def test_dressed_configuration_is_not_a_fixed_point():
    u = reference_dressing_field(S3)
    for phi in CONFIGURATIONS:
        dressed = dress(u, phi)
        assert all(act(g, dressed) != dressed for g in S3.elements if g != IDENTITY)


def test_source_1_2_equivariance_is_the_corrected_one(s3_fields):
    left = {field_values(u) for u in s3_fields["left"]}
    assert {field_values(u) for u in s3_fields["source_1_2"]} == left


def test_source_1_2_dressing_is_not_invariant_in_s3():
    u = reference_dressing_field(S3)
    phi, h = ("a", "b", "c"), (1, 2, 0)
    assert source_1_2_transform(h, phi) == ("b", "c", "a")
    assert u[("b", "c", "a")] == (2, 0, 1) == compose(inverse(h), u[phi])
    assert source_1_2_dress(u, source_1_2_transform(h, phi)) == ("c", "a", "b")
    assert source_1_2_dress(u, phi) == ("a", "b", "c")
    assert dress(u, source_1_2_transform(h, phi)) == dress(u, phi) == ("a", "b", "c")
    failures = source_1_2_invariance_failures(S3, u)
    assert failures[0] == (phi, h, ("c", "a", "b"), ("a", "b", "c"))
    assert len(failures) == 18


@pytest.mark.parametrize("group", [S3, Z3], ids=["S3", "Z3"])
def test_source_1_2_dressing_fails_for_every_equivariant_field(group):
    for u in maps_satisfying(group, is_equivariant):
        assert source_1_2_invariance_failures(group, u)


def test_source_1_2_dressing_fails_on_z3_too():
    u = reference_dressing_field(Z3)
    failures = source_1_2_invariance_failures(Z3, u)
    assert {h for _, h, _, _ in failures} == {(1, 2, 0), (2, 0, 1)}
    assert len(failures) == 12


def test_prop_4_1_equivariance_has_no_solution_in_s3(s3_fields):
    assert s3_fields["prop_4_1"] == []
    failures = prop_4_1_consistency_failures(S3)
    assert failures[0] == ((0, 2, 1), (1, 0, 2))
    g1, g2 = failures[0]
    assert compose(g1, g2) != compose(g2, g1)
    assert len(failures) == 18


def test_prop_4_1_step_fails_in_s3():
    failures = prop_4_1_step_failures(S3)
    assert failures[0] == ((0, 2, 1), (1, 0, 2), ("a", "b", "c"), ("c", "b", "a"), ("b", "a", "c"))
    assert len(failures) == 18 * 6
    for g, a, _, _, _ in failures:
        assert compose(g, a) != compose(a, g)


def test_right_multiplication_repairs_prop_4_1_in_s3(s3_fields):
    left = s3_fields["left"]
    right = s3_fields["right"]
    assert {field_values(u) for u in right} == {
        tuple(inverse(g) for g in field_values(v)) for v in left
    }
    for u in right:
        v = {phi: inverse(g) for phi, g in u.items()}
        for phi, g in product(CONFIGURATIONS, S3.elements):
            assert prop_4_1_dress(u, act(g, phi)) == prop_4_1_dress(u, phi) == dress(v, phi)


def test_z3_conventions_agree():
    assert Z3.is_abelian() and is_free(Z3) and len(orbits(Z3)) == 2
    assert prop_4_1_step_failures(Z3) == ()
    assert prop_4_1_consistency_failures(Z3) == ()
    prop = maps_satisfying(Z3, prop_4_1_is_equivariant)
    left = maps_satisfying(Z3, is_equivariant)
    assert len(prop) == len(left) == 9
    right = maps_satisfying(Z3, is_right_equivariant)
    assert {field_values(u) for u in prop} == {field_values(u) for u in right}
    assert {field_values(u) for u in prop} == {
        tuple(inverse(g) for g in field_values(v)) for v in left
    }
    for u in prop:
        v = {phi: inverse(g) for phi, g in u.items()}
        for phi, g in product(CONFIGURATIONS, Z3.elements):
            assert prop_4_1_dress(u, act(g, phi)) == prop_4_1_dress(u, phi) == dress(v, phi)
        image = {prop_4_1_dress(u, phi) for phi in CONFIGURATIONS}
        assert all(len(image & set(orbit)) == 1 for orbit in orbits(Z3))


def test_permutation_and_configuration_inputs_are_typed():
    with pytest.raises(TypeError):
        act((True, 0, 2), ("a", "b", "c"))
    with pytest.raises(TypeError):
        compose((0.0, 1, 2), IDENTITY)
    with pytest.raises(ValueError):
        act(IDENTITY, ("a", "a", "c"))
    u = dict(reference_dressing_field(S3))
    u[("a", "b", "c")] = (True, False, 2)
    with pytest.raises(TypeError):
        is_equivariant(S3, u)
    with pytest.raises(ValueError):
        is_equivariant(Z3, reference_dressing_field(S3))
