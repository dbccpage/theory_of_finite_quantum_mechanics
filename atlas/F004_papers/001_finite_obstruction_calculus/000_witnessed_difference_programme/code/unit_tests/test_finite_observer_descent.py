"""Finite evidence for constrained descent, independent of production Rust."""

import pytest
from witnessed_difference.finite_observer_descent import (
    FiniteConstrainedSite,
    IncompatibleReports,
    equality_constraint_site,
)


def test_compatible_fixed_sections_can_be_globally_inadmissible():
    site = equality_constraint_site()
    cover = (frozenset({"x"}), frozenset({"y"}))
    families = site.classify_cover(site.carrier, cover)
    assert len(families) == 4
    assert sorted(len(globals_) for _, globals_ in families) == [0, 0, 1, 1]
    assert site.descent_fiber(site.carrier, cover, ((("x", "0"),), (("y", "1"),))) == ()
    assert site.descent_fiber(site.carrier, cover, ((("x", "1"),), (("y", "1"),))) == ((("x", "1"), ("y", "1")),)


def test_complete_assignment_family_restores_unique_gluing():
    site = equality_constraint_site(complete=True)
    cover = (frozenset({"x"}), frozenset({"y"}))
    assert all(len(globals_) == 1 for _, globals_ in site.classify_cover(site.carrier, cover))
    assert site.descent_fiber(frozenset(), (), ()) == ((),)


def test_overlap_disagreement_and_nonpresheaf_families_refuse():
    site = equality_constraint_site()
    with pytest.raises(IncompatibleReports):
        site.descent_fiber(site.carrier, (site.carrier, frozenset({"x"})),
                           ((("x", "0"), ("y", "0")), (("x", "1"),)))
    table = dict(site.families)
    table[frozenset({"x"})] = ((("x", "0"),),)
    with pytest.raises(ValueError, match="closed under restriction"):
        FiniteConstrainedSite(site.carrier, tuple(table.items()))
    with pytest.raises(ValueError, match="union cover"):
        site.descent_fiber(site.carrier, (frozenset({"x"}),), ((("x", "0"),),))


def test_mutable_input_families_are_frozen():
    base = equality_constraint_site()
    families = list(base.families)
    checked = FiniteConstrainedSite(base.carrier, families)
    families[0] = (frozenset(), ((("x", "0"),),))
    assert checked.families[0][1] == ((),)

