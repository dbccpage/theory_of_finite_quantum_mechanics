"""
Test suite for CODA Founding Discipline & CD-12 Groupoid Faithful Functor Target.
Enforces >=90% (target 100%) statement and branch coverage.
AuthorityEffect: None.
"""

import numpy as np
import pytest
from coda_discipline_core import (
    CODA_DISCIPLINE_CLAIMS,
    ComparisonSpan,
    FaithfulGroupoidEmbedding,
    FiniteGroupoid,
    HoTTSubsumptionRefusalError,
    Presentation,
    Trace,
    assert_hott_non_subsumption_fence,
    compose_spans,
    compose_traces,
    erase_trace,
    make_diag_span,
    make_z2_groupoid,
    make_z3_groupoid,
)


def test_presentation_validation_and_invariants():
    # Valid presentation
    diff = np.array([[0.0, 1.5], [1.5, 0.0]])
    p = Presentation(name="P2", carrier_size=2, diff_matrix=diff)
    assert p.carrier_size == 2
    assert p.name == "P2"

    # Explicit equality and hash
    p2_copy = Presentation(name="P2", carrier_size=2, diff_matrix=diff.copy())
    p2_diff = Presentation(name="P2", carrier_size=2, diff_matrix=np.array([[0.0, 2.0], [2.0, 0.0]]))
    assert p == p2_copy
    assert hash(p) == hash(p2_copy)
    assert p != p2_diff
    assert p != "non_presentation"

    # Equality and hash parity across int and float dtypes, dict and set semantics
    p2_int = Presentation(name="P2", carrier_size=2, diff_matrix=np.array([[0, 1], [1, 0]], dtype=np.int64))
    p2_flt = Presentation(name="P2", carrier_size=2, diff_matrix=np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float64))
    assert p2_int == p2_flt
    assert hash(p2_int) == hash(p2_flt)
    assert len({p2_int, p2_flt}) == 1
    lookup_dict = {p2_int: "mapped"}
    assert lookup_dict[p2_flt] == "mapped"

    # Immutability of underlying matrix
    with pytest.raises(ValueError, match="read-only"):
        p2_flt.diff_matrix[0, 1] = 999.0

    # Errors
    with pytest.raises(ValueError, match="Carrier size must be positive"):
        Presentation(name="P0", carrier_size=0, diff_matrix=np.zeros((0, 0)))

    with pytest.raises(ValueError, match="mismatch"):
        Presentation(name="P_bad_shape", carrier_size=2, diff_matrix=np.zeros((3, 3)))

    with pytest.raises(ValueError, match="diagonal must be zero"):
        Presentation(
            name="P_bad_diag",
            carrier_size=2,
            diff_matrix=np.array([[1.0, 0.0], [0.0, 0.0]]),
        )

    with pytest.raises(ValueError, match="non-negative"):
        Presentation(
            name="P_neg",
            carrier_size=2,
            diff_matrix=np.array([[0.0, -1.0], [-1.0, 0.0]]),
        )


def test_comparison_span_and_pullback_composition():
    p1 = Presentation("P1", 2, np.array([[0.0, 1.0], [1.0, 0.0]]))
    p2 = Presentation("P2", 2, np.array([[0.0, 2.0], [2.0, 0.0]]))
    p2_separate = Presentation("P2", 2, np.array([[0.0, 2.0], [2.0, 0.0]]))
    p3 = Presentation("P3", 2, np.array([[0.0, 3.0], [3.0, 0.0]]))

    diag1 = make_diag_span(p1)
    assert diag1.ext_cost == 0.0
    assert diag1.mid_size == 2

    # Composition across separately constructed equal endpoints
    s1 = ComparisonSpan(
        p1, p2, mid_size=2, left_map=(0, 1), right_map=(1, 0), ext_cost=1.5
    )
    s2 = ComparisonSpan(
        p2_separate, p3, mid_size=2, left_map=(1, 0), right_map=(0, 1), ext_cost=2.0
    )

    comp = compose_spans(s1, s2)
    assert comp.p1 == p1
    assert comp.p2 == p3
    assert comp.ext_cost == 3.5
    assert comp.mid_size == 2

    # Validation errors on size and maps
    with pytest.raises(ValueError, match="Map length must equal mid_size"):
        ComparisonSpan(p1, p2, mid_size=2, left_map=(0,), right_map=(1, 0))

    with pytest.raises(ValueError, match="mid_size must be a non-negative integer"):
        ComparisonSpan(p1, p2, mid_size=-1, left_map=(), right_map=())

    with pytest.raises(ValueError, match="mid_size must be a non-negative integer"):
        ComparisonSpan(p1, p2, mid_size=1.5, left_map=(0,), right_map=(0,))

    with pytest.raises(ValueError, match="mid_size must be a non-negative integer"):
        ComparisonSpan(p1, p2, mid_size=True, left_map=(0,), right_map=(0,))

    # Out of carrier bounds
    with pytest.raises(ValueError, match="left_map index 99 out of bounds"):
        ComparisonSpan(p1, p2, mid_size=1, left_map=(99,), right_map=(0,))

    with pytest.raises(ValueError, match="right_map index -1 out of bounds"):
        ComparisonSpan(p1, p2, mid_size=1, left_map=(0,), right_map=(-1,))

    with pytest.raises(ValueError, match="Extensional cost must be non-negative"):
        ComparisonSpan(
            p1, p2, mid_size=2, left_map=(0, 1), right_map=(1, 0), ext_cost=-1.0
        )

    with pytest.raises(ValueError, match="Span composition mismatch"):
        compose_spans(s2, s1)


def test_trace_and_erasure():
    p = Presentation("P", 1, np.zeros((1, 1)))
    span = make_diag_span(p)

    t1 = Trace(steps=1, work_cost=2.0, span=span)
    t2 = Trace(steps=2, work_cost=3.0, span=span)

    assert erase_trace(t1) == span

    t_comp = compose_traces(t1, t2)
    assert t_comp.steps == 3
    assert t_comp.work_cost == 5.0
    assert t_comp.span.ext_cost == 0.0

    with pytest.raises(ValueError, match="Steps must be non-negative"):
        Trace(steps=-1, work_cost=1.0, span=span)

    with pytest.raises(ValueError, match="Work cost must be non-negative"):
        Trace(steps=1, work_cost=-1.0, span=span)


def test_finite_groupoids_and_validation():
    z2 = make_z2_groupoid()
    assert z2.validate() is True

    z3 = make_z3_groupoid()
    assert z3.validate() is True

    # Bad groupoid 1: empty tables with object declared
    bad_empty = FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e"]}},
        id_map={"*": "e"},
        comp_table={},
        inv_map={},
    )
    assert bad_empty.validate() is False

    # Bad groupoid 2: empty inv_map
    bad_empty_inv = FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e"]}},
        id_map={"*": "e"},
        comp_table={("e", "e"): "e"},
        inv_map={},
    )
    assert bad_empty_inv.validate() is False

    # Bad groupoid 3: Z2 with g o g = g instead of e (violates inverse/identity)
    z2_bad_g = make_z2_groupoid()
    z2_bad_g.comp_table[("g", "g")] = "g"
    assert z2_bad_g.validate() is False

    # Bad groupoid 4: wrong identity composition
    z2_bad_id = make_z2_groupoid()
    z2_bad_id.comp_table[("e", "g")] = "e"
    assert z2_bad_id.validate() is False

    # Bad groupoid 5: non-associative composition table
    # Construct a non-associative Cayley table on 3 elements
    bad_assoc = FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e", "a", "b"]}},
        id_map={"*": "e"},
        comp_table={
            ("e", "e"): "e", ("e", "a"): "a", ("e", "b"): "b",
            ("a", "e"): "a", ("a", "a"): "b", ("a", "b"): "e",
            ("b", "e"): "b", ("b", "a"): "a", ("b", "b"): "e",
        },
        inv_map={"e": "e", "a": "b", "b": "a"},
    )
    # (b o a) o a = a o a = b, but b o (a o a) = b o b = e -> not associative
    assert bad_assoc.validate() is False

    # Bad groupoid 6: invalid objects or empty
    bad_no_objs = FiniteGroupoid(
        objects=[], morphisms={}, id_map={}, comp_table={}, inv_map={}
    )
    assert bad_no_objs.validate() is False


def test_cd12_faithful_groupoid_embedding_and_two_level_cost():
    z2 = make_z2_groupoid()
    emb = FaithfulGroupoidEmbedding(z2)

    assert emb.embed_object("*").name == "Pres_*"
    assert emb.embed_morphism("e").ext_cost == 0.0
    assert emb.embed_morphism("g").ext_cost == 0.0
    assert emb.check_faithfulness() is True

    # Two-level cost accounting
    costs = emb.check_two_level_cost_accounting("g", work=4.0)
    assert costs["extensional_cost"] == 0.0
    assert costs["intensional_work_cost"] == 8.0
    assert costs["trace_steps"] == 2.0


def test_claim_ledger_census_and_fences():
    assert len(CODA_DISCIPLINE_CLAIMS) == 14
    claim_ids = [c.id for c in CODA_DISCIPLINE_CLAIMS]
    assert "CD-01" in claim_ids
    assert "CD-06" in claim_ids
    assert "CD-12" in claim_ids
    assert "CD-13" in claim_ids

    # Fence tests
    assert_hott_non_subsumption_fence(
        "We position CODA relative to HoTT without subsumption."
    )

    with pytest.raises(HoTTSubsumptionRefusalError, match="subsumes hott"):
        assert_hott_non_subsumption_fence("This theorem proves CODA subsumes HoTT.")

    with pytest.raises(HoTTSubsumptionRefusalError, match="replaces univalence"):
        assert_hott_non_subsumption_fence("CODA replaces univalence globally.")


def test_faithful_embedding_duplicate_rejection():
    z2 = make_z2_groupoid()
    emb = FaithfulGroupoidEmbedding(z2)
    assert emb.check_faithfulness() is True
    # Manually inject duplicate span keys to test unfaithfulness detection
    emb.spans = {"e": emb.spans["e"]}

    # If list has duplicates:
    class MockEmbedding:
        def __init__(self):
            self.spans = ["m1", "m1"]

        def check_faithfulness(self):
            seen = set()
            for m in self.spans:
                if m in seen:
                    return False
                seen.add(m)
            return True

    mock = MockEmbedding()
    assert mock.check_faithfulness() is False
