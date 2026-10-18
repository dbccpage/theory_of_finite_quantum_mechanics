"""Freeze tests for 8 math contract implementations.

Covers: Fiber, FiberBundle, Fibration, FiberSequence, PostnikovTower,
        AHSS, AlgebraicField, AlgebraicKTheory.
"""

from __future__ import annotations

import sys

import pytest

sys.path.insert(0, "omega_engine/research/ooutwire_docs")

from omega_engine.crates.type.topology.fiber import (
    CONTRACT_ID as FIBER_CONTRACT_ID,
    Fiber,
    compute_basis_hash,
    make_fiber,
    make_standard_fiber,
)
from omega_engine.crates.type.topology.fiber_bundle import (
    CONTRACT_ID as BUNDLE_CONTRACT_ID,
    FiberBundle,
    make_trivial_bundle,
)
from omega_engine.crates.type.topology.fibration import (
    CONTRACT_ID as FIBRATION_CONTRACT_ID,
    Fibration,
    FibrationMap,
    HLPSample,
    make_fibration,
)
from omega_engine.crates.type.topology.fiber_sequence import (
    CONTRACT_ID as FSEQ_CONTRACT_ID,
    FiberSequence,
    make_fiber_sequence,
)
from omega_engine.crates.type.topology.postnikov_tower import (
    CONTRACT_ID as POSTNIKOV_CONTRACT_ID,
    PostnikovSection,
    PostnikovTower,
    make_postnikov_tower,
)
from omega_engine.crates.type.topology.atiyah_hirzebruch_spectral_sequence import (
    CONTRACT_ID as AHSS_CONTRACT_ID,
    AHSS,
    Differential,
    SpectralSequencePage,
    make_ahss_e2,
)
from omega_engine.crates.type.algebra.algebraic_field import (
    CONTRACT_ID as FIELD_CONTRACT_ID,
    AlgebraicField,
    make_rational_field,
    make_quadratic_field,
)
from omega_engine.crates.type.algebra.algebraic_k_theory import (
    CONTRACT_ID as KTHEORY_CONTRACT_ID,
    AlgebraicKTheory,
    KGroup,
    make_k_theory_integers,
    make_k_theory_field,
)


class TestContractIDs:

    def test_fiber_contract_id(self) -> None:
        assert FIBER_CONTRACT_ID == "urn:omega:math:fiber:v0.1.0"

    def test_bundle_contract_id(self) -> None:
        assert BUNDLE_CONTRACT_ID == "urn:omega:math:fiber_bundle:v0.1.0"

    def test_fibration_contract_id(self) -> None:
        assert FIBRATION_CONTRACT_ID == "urn:omega:math:fibration:v0.1.0"

    def test_fiber_sequence_contract_id(self) -> None:
        assert FSEQ_CONTRACT_ID == "urn:omega:math:fiber_sequence:v0.1.0"

    def test_postnikov_contract_id(self) -> None:
        assert POSTNIKOV_CONTRACT_ID == "urn:omega:math:postnikov_tower:v0.1.0"

    def test_ahss_contract_id(self) -> None:
        assert AHSS_CONTRACT_ID == "urn:omega:math:atiyah_hirzebruch_spectral_sequence:v0.1.0"

    def test_field_contract_id(self) -> None:
        assert FIELD_CONTRACT_ID == "urn:omega:math:algebraic_field:v1.0.0"

    def test_ktheory_contract_id(self) -> None:
        assert KTHEORY_CONTRACT_ID == "urn:omega:math:algebraic_k_theory:v0.1.0"


class TestFiber:

    def test_standard_fiber_valid(self) -> None:
        f = make_standard_fiber("R", 3, "origin")
        assert f.validate() == []
        assert f.dimension == 3
        assert f.field == "R"

    def test_fiber_hash_consistency(self) -> None:
        f = make_standard_fiber("C", 2, "p0")
        assert f.basis_hash == compute_basis_hash(f.basis)

    def test_fiber_rejects_zero_dimension(self) -> None:
        f = Fiber("R", 0, "x", (), "abc")
        errors = f.validate()
        assert any("dimension must be positive" in e for e in errors)

    def test_fiber_rejects_empty_base_point(self) -> None:
        f = make_fiber("R", 1, "", ((1.0 + 0j,),))
        errors = f.validate()
        assert any("base_point_id must be non-empty" in e for e in errors)

    def test_fiber_rejects_wrong_hash(self) -> None:
        f = Fiber("R", 1, "x", ((1.0 + 0j,),), "wrong_hash")
        errors = f.validate()
        assert any("basis_hash mismatch" in e for e in errors)


class TestFiberBundle:

    def test_trivial_bundle_valid(self) -> None:
        b = make_trivial_bundle("R", 2, ("a", "b", "c"))
        assert b.validate() == []
        assert len(b.fibers) == 3
        assert b.base_points == ("a", "b", "c")

    def test_bundle_rejects_dimension_mismatch(self) -> None:
        f1 = make_standard_fiber("R", 2, "a")
        f2 = make_standard_fiber("R", 3, "b")
        b = FiberBundle("R", 2, (f1, f2), ("a", "b"))
        errors = b.validate()
        assert any("dimension" in e for e in errors)

    def test_bundle_rejects_field_mismatch(self) -> None:
        f1 = make_standard_fiber("R", 2, "a")
        f2 = make_standard_fiber("C", 2, "b")
        b = FiberBundle("R", 2, (f1, f2), ("a", "b"))
        errors = b.validate()
        assert any("field" in e for e in errors)

    def test_bundle_rejects_unsorted_base_points(self) -> None:
        f1 = make_standard_fiber("R", 1, "b")
        f2 = make_standard_fiber("R", 1, "a")
        b = FiberBundle("R", 1, (f1, f2), ("b", "a"))
        errors = b.validate()
        assert any("sorted" in e for e in errors)


class TestFibration:

    def test_fibration_valid(self) -> None:
        fib = make_fibration("E", "B")
        assert fib.validate() == []

    def test_fibration_rejects_same_spaces(self) -> None:
        fib = make_fibration("X", "X")
        errors = fib.validate()
        assert any("distinct" in e for e in errors)

    def test_fibration_with_fiber_data(self) -> None:
        fiber = make_standard_fiber("R", 2, "b0")
        fib = make_fibration("E", "B", fiber=fiber)
        assert fib.validate() == []

    def test_fibration_failed_hlp(self) -> None:
        sample = HLPSample("h", "lift_h", verified=False)
        fib = Fibration(
            map=FibrationMap("E", "B", "p"),
            hlp_samples=(sample,),
        )
        errors = fib.validate()
        assert any("failed verification" in e for e in errors)


class TestFiberSequence:

    def test_fiber_sequence_valid(self) -> None:
        fs = make_fiber_sequence("F", "E", "B")
        assert fs.validate() == []

    def test_fiber_sequence_rejects_duplicate_ids(self) -> None:
        fs = make_fiber_sequence("F", "F", "B")
        errors = fs.validate()
        assert any("distinct" in e for e in errors)

    def test_fiber_sequence_checks_fibration_consistency(self) -> None:
        fib = make_fibration("E_wrong", "B")
        fs = FiberSequence(
            fiber_id="F",
            total_space_id="E",
            base_space_id="B",
            fibration=fib,
            inclusion_name="i",
        )
        errors = fs.validate()
        assert any("total_space" in e for e in errors)


class TestPostnikovTower:

    def test_postnikov_tower_valid(self) -> None:
        tower = make_postnikov_tower("S2", {1: "0", 2: "Z"})
        assert tower.validate() == []
        assert len(tower.sections) == 3
        assert len(tower.fibration_maps) == 2

    def test_postnikov_tower_base_is_level_zero(self) -> None:
        tower = make_postnikov_tower("X", {1: "Z"})
        assert tower.sections[0].level == 0

    def test_postnikov_rejects_bad_homotopy_group(self) -> None:
        sec = PostnikovSection(
            level=1,
            space_id="X_1",
            homotopy_groups={1: "Z", 2: "Z"},
        )
        errors = sec.validate()
        assert any("must be 0" in e for e in errors)

    def test_postnikov_rejects_wrong_map_count(self) -> None:
        sec0 = PostnikovSection(level=0, space_id="X_0", homotopy_groups={})
        sec1 = PostnikovSection(level=1, space_id="X_1", homotopy_groups={1: "Z"}, k_invariant="k_1")
        tower = PostnikovTower("X", (sec0, sec1), ())
        errors = tower.validate()
        assert any("expected 1 fibration maps" in e for e in errors)


class TestAHSS:

    def test_ahss_valid(self) -> None:
        ahss = make_ahss_e2(
            "S2", "KU",
            {(0, 0): "Z", (2, 0): "Z"},
            "KU^*(S^2)",
        )
        assert ahss.validate() == []

    def test_ahss_rejects_wrong_first_page(self) -> None:
        page = SpectralSequencePage(r=3, entries={}, differentials=())
        ahss = AHSS("X", "E", (page,), "E^*(X)")
        errors = ahss.validate()
        assert any("E_2" in e for e in errors)

    def test_ahss_differential_target_check(self) -> None:
        diff = Differential(source=(0, 0), target=(3, -1))
        page = SpectralSequencePage(
            r=2, entries={(0, 0): "Z"}, differentials=(diff,)
        )
        ahss = AHSS("X", "E", (page,), "E^*(X)")
        errors = ahss.validate()
        assert any("should target" in e for e in errors)

    def test_ahss_valid_differential(self) -> None:
        diff = Differential(source=(0, 0), target=(2, -1))
        page = SpectralSequencePage(
            r=2, entries={(0, 0): "Z"}, differentials=(diff,)
        )
        assert page.validate() == []


class TestAlgebraicField:

    def test_rational_field_valid(self) -> None:
        q = make_rational_field()
        assert q.validate() == []
        assert q.degree == 1

    def test_quadratic_field_valid(self) -> None:
        k = make_quadratic_field(2)
        assert k.validate() == []
        assert k.degree == 2

    def test_field_multiplication(self) -> None:
        k = make_quadratic_field(2)
        e0 = (1.0 + 0j, 0.0 + 0j)
        e1 = (0.0 + 0j, 1.0 + 0j)
        result = k.multiply(e1, e1)
        assert abs(result[0] - 2.0) < 1e-10
        assert abs(result[1]) < 1e-10

    def test_field_rejects_zero_degree(self) -> None:
        f = AlgebraicField((1.0 + 0j,), 0, (), ())
        errors = f.validate()
        assert any("degree must be positive" in e for e in errors)

    def test_field_sign_determination(self) -> None:
        q = make_rational_field()
        assert q.sign((3.0 + 0j,)) == 1
        assert q.sign((-1.0 + 0j,)) == -1
        assert q.sign((0.0 + 0j,)) == 0


class TestAlgebraicKTheory:

    def test_k_theory_integers_valid(self) -> None:
        kt = make_k_theory_integers()
        assert kt.validate() == []
        assert kt.k(0) is not None
        assert kt.k(0).group_description == "Z"

    def test_k_theory_field_valid(self) -> None:
        kt = make_k_theory_field("Q")
        assert kt.validate() == []
        assert kt.k(1).group_description == "Q*"

    def test_k_theory_rejects_bad_construction(self) -> None:
        kt = AlgebraicKTheory("Z", "bogus", ())
        errors = kt.validate()
        assert any("construction" in e for e in errors)

    def test_k_theory_rejects_negative_degree(self) -> None:
        kg = KGroup(degree=-1, group_description="Z")
        errors = kg.validate()
        assert any("non-negative" in e for e in errors)

    def test_k_theory_rejects_duplicate_degree(self) -> None:
        kt = AlgebraicKTheory(
            "Z", "plus",
            (KGroup(0, "Z"), KGroup(0, "Z/2")),
        )
        errors = kt.validate()
        assert any("duplicate" in e for e in errors)


