"""
test_coda_cs_q.py: Unit and mutation test suite for CODA-CS-Q Bridge.

Verifies:
1. BRIDGE-001: Profile factorization <=> fiber constancy (forward + constructive image reverse).
2. BRIDGE-002: Higher degree-bounded query family Q_{<= n}.
3. BRIDGE-003: 14-Tuple schema B_q and 8-Step BridgeAdmissible audit pipeline.
4. BRIDGE-006: Named terminalizer agreement (tau_Q vs tau_CODA-CS), step 8 independence.
5. BRIDGE-007: 6-Class typed bridge residual taxonomy.
6. Exact cochain quotient solving (LinearRepairProblem) over exact rationals.
7. Section 0 Worked Example replay (energy = 7/8, zero quotient distance).
8. Strict Zero Floats Invariant (floats and booleans rejected with TypeError).
AuthorityEffect: None.

Run: python -m pytest -n 8 coda_atlas/F005_coda/cs_q/code/tests -v
"""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

import pytest
from coda_cs_q_bridge_core import (
    BRIDGE_ADMISSIBLE_8_STEPS,
    BRIDGE_PACKET_14_SCHEMA_FIELDS,
    BridgePacketCore,
    BridgeResidualTaxonomy,
    CofinalShadowTower,
    GeneratorSemigroupAdapter,
    HigherQueryFamily,
    ImagePoint,
    NamedTerminalizers,
    ProfileFactorizationSolver,
    ProfileFiberQuotient,
    QueryProbe,
    ShadowNode,
    _validate_exact_int,
    _validate_exact_rational,
    compute_transition_quotient_obstruction,
    reproduce_section_0_worked_example,
    terminals_agree,
)
from sympy import Matrix, Rational


def test_bridge_001_forward_and_image_reverse() -> None:
    """BRIDGE-001: Profile Factorization <=> Fiber Constancy on Image."""
    nodes: list[ShadowNode[int]] = [ShadowNode("N1", 1)]
    # Projector extracts parity
    projectors = {"N1": lambda x: x % 2}
    transitions: dict[tuple[str, str], Callable[[int], int]] = {}
    tower = CofinalShadowTower(nodes, projectors, transitions)

    # Domain with even and odd numbers
    domain = [2, 4, 6, 1, 3, 5]

    # Query 1: Depends only on parity (fiber constant)
    q_const: QueryProbe[int, Rational] = QueryProbe("Q_Parity", degree=1, eval_fn=lambda x: Rational(10) if x % 2 == 0 else Rational(20))
    solver_const = ProfileFactorizationSolver(tower, q_const, domain)
    success, q_bar, err = solver_const.solve_factorization()

    assert success is True
    assert q_bar is not None
    assert err is None
    # Check constructive image reverse
    assert q_bar((0,)) == Rational(10)
    assert q_bar((1,)) == Rational(20)

    # Image points witness check
    img_pts = solver_const.construct_image_points()
    assert len(img_pts) == 6
    for pt in img_pts:
        assert pt.evaluate_factored(q_const, q_bar) == q_const.evaluate(pt.witness)

    # Query 2: Varies within same fiber (not fiber constant)
    q_var: QueryProbe[int, Rational] = QueryProbe("Q_Identity", degree=1, eval_fn=lambda x: Rational(x))
    solver_var = ProfileFactorizationSolver(tower, q_var, domain)
    success_var, q_bar_var, err_var = solver_var.solve_factorization()

    assert success_var is False
    assert q_bar_var is None
    assert "Fiber constancy violation" in str(err_var)


def test_bridge_002_higher_query_family() -> None:
    """BRIDGE-002: Degree-bounded query family Q_{<= n}."""
    nodes: list[ShadowNode[int]] = [ShadowNode("N1", 1)]
    projectors = {"N1": lambda x: x % 2}
    tower = CofinalShadowTower(nodes, projectors, {})
    quotient = ProfileFiberQuotient(tower, [0, 2, 4, 1, 3])

    q1: QueryProbe[int, Rational] = QueryProbe("Q1", degree=1, eval_fn=lambda x: Rational(1))
    q2: QueryProbe[int, Rational] = QueryProbe("Q2", degree=2, eval_fn=lambda x: Rational(x % 2))
    family = HigherQueryFamily(max_degree=2, queries=[q1, q2])

    is_ok, failures = family.verify_family_fiber_constancy(quotient)
    assert is_ok is True
    assert len(failures) == 0

    # Query exceeding degree bound
    with pytest.raises(ValueError, match="exceeds family bound"):
        HigherQueryFamily(max_degree=1, queries=[q2])


def test_bridge_003_14_schema_and_8_step_admission() -> None:
    """BRIDGE-003: 14-tuple schema field count and 8-step admission audit."""
    assert len(BRIDGE_PACKET_14_SCHEMA_FIELDS) == 14
    assert len(BRIDGE_ADMISSIBLE_8_STEPS) == 8

    nodes: list[ShadowNode[int]] = [ShadowNode("N0", 1), ShadowNode("N1", 2)]
    projectors = {"N0": lambda x: x % 3, "N1": lambda x: x % 6}
    transitions = {("N1", "N0"): lambda a: a % 3}
    tower = CofinalShadowTower(nodes, projectors, transitions)

    domain = [0, 1, 2, 3, 4, 5]
    q_valid: QueryProbe[int, Rational] = QueryProbe("Q_Valid", degree=1, eval_fn=lambda x: Rational(x % 3))

    packet = BridgePacketCore(
        packet_id="B_Q_Test",
        tower=tower,
        domain=domain,
        query=q_valid,
    )
    audit = packet.audit_8_step_admission()
    assert audit["is_admissible"] is True
    assert audit["status"] == "BOUNDED_EVALUATION_SCOPE"
    assert audit["declared_schema_slot_count"] == 14
    assert audit["admission_8_step_count"] == 8

    # Failure of step 4 (QHeld debt unpaid)
    packet_debt = BridgePacketCore(
        packet_id="B_Debt",
        tower=tower,
        domain=domain,
        query=q_valid,
        q_held_paid=False,
    )
    audit_debt = packet_debt.audit_8_step_admission()
    assert audit_debt["is_admissible"] is False
    assert audit_debt["steps"]["4_q_admission"] is False


def test_bridge_006_named_terminalizer_agreement() -> None:
    """BRIDGE-006: Named terminalizer agreement and independence from flags."""
    domain = [Rational(0, 1), Rational(1, 1)]

    # Agreeing terminals
    def tau_q(x: Rational) -> Rational:
        return x * Rational(2)

    def tau_coda(x: Rational) -> Rational:
        return x * Rational(2)

    agree, mismatch = terminals_agree(domain, tau_q, tau_coda)
    assert agree is True
    assert mismatch is None

    # Disagreeing terminals
    def tau_bad(x: Rational) -> Rational:
        return x * Rational(3)

    agree_bad, mismatch_bad = terminals_agree(domain, tau_q, tau_bad)
    assert agree_bad is False
    assert "Terminal mismatch" in str(mismatch_bad)

    # NamedTerminalizers object
    named = NamedTerminalizers(tau_q=tau_q, tau_coda_cs=tau_coda)
    nodes: list[ShadowNode[Rational]] = [ShadowNode("N0", 1)]
    tower = CofinalShadowTower(nodes, {"N0": lambda x: x}, {})
    q: QueryProbe[Rational, Rational] = QueryProbe("Q", 1, tau_q)

    packet_named = BridgePacketCore(
        packet_id="B_Named",
        tower=tower,
        domain=domain,
        query=q,
        named_terminals=named,
    )
    audit_named = packet_named.audit_8_step_admission()
    assert audit_named["step8_status"] == "NAMED_TERMINALIZERS_AGREE"
    assert audit_named["is_admissible"] is True


def test_bridge_007_residual_taxonomy() -> None:
    """BRIDGE-007: 6-Class typed bridge residual taxonomy."""
    # When everything holds
    res_clean = BridgeResidualTaxonomy.classify_residual(
        profile_factored=True,
        tower_coherent=True,
        terminal_conserved=True,
        authority_effect="None",
    )
    assert len(res_clean) == 0

    # When factor defect and overclaim occur
    res_defects = BridgeResidualTaxonomy.classify_residual(
        profile_factored=False,
        tower_coherent=True,
        terminal_conserved=True,
        authority_effect="GlobalGreen",
    )
    assert any("R_factor" in r for r in res_defects)
    assert any("R_overclaim" in r for r in res_defects)


def test_transition_cochain_quotient_solver() -> None:
    """Exact cochain quotient solving (LinearRepairProblem) over exact rationals."""
    d0 = Matrix([[1], [2]])
    defect_exact = Matrix([[3], [6]])
    dist_ex, wit_ex, is_ex = compute_transition_quotient_obstruction(d0, defect_exact)
    assert dist_ex == Rational(0, 1)
    assert wit_ex == Matrix([[3]])
    assert is_ex is True

    defect_bad = Matrix([[1], [0]])
    dist_bad, _wit_bad, is_bad = compute_transition_quotient_obstruction(d0, defect_bad)
    assert dist_bad > Rational(0, 1)
    assert is_bad is False


def test_section_0_worked_example_reproduction() -> None:
    """Section 0 Worked Example replay: energy = 7/8 and exact quotient distance."""
    res = reproduce_section_0_worked_example()
    assert res["energy_exact"] == Rational(7, 8)
    assert res["is_admissible"] is True
    assert res["quotient_distance"] == Rational(0, 1)
    assert res["is_cochain_exact"] is True


def test_zero_floats_invariant() -> None:
    """Zero Floats Invariant: floats and booleans strictly raise TypeError."""
    assert _validate_exact_rational(Rational(3, 5), "val") == Rational(3, 5)
    assert _validate_exact_rational(7, "val") == Rational(7, 1)

    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(0.5, "val")

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(True, "val")

    assert _validate_exact_int(3, "dim") == 3
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(False, "dim")

    with pytest.raises(TypeError):
        _validate_exact_int(2.0, "dim")

    # Float in node dimension
    with pytest.raises(TypeError):
        ShadowNode("N_Bad", cast(int, 2.5))

    # Float in query degree
    with pytest.raises(TypeError):
        QueryProbe("Q_Bad", cast(int, 1.5), lambda x: 1)

    # Float in cochain quotient defect
    d0 = Matrix([[1], [1]])
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        compute_transition_quotient_obstruction(d0, Matrix([[1.2], [2.4]]))

    # String conversion and invalid types
    assert _validate_exact_rational("1/3", "val") == Rational(1, 3)
    with pytest.raises(TypeError, match="could not be converted"):
        _validate_exact_rational("invalid_rational", "val")
    with pytest.raises(TypeError, match="must be an exact rational"):
        _validate_exact_rational(object(), "val")

    # Negative integer validation
    with pytest.raises(ValueError, match="must be non-negative"):
        _validate_exact_int(-5, "dim")


def test_coverage_auxiliary_paths() -> None:
    """Exercise remaining paths in core for >=95% coverage."""
    # Tower coherence failure
    nodes: list[ShadowNode[int]] = [ShadowNode("N0", 1), ShadowNode("N1", 1)]
    projectors = {"N0": lambda x: x, "N1": lambda x: x + 1}
    transitions = {("N0", "N1"): lambda a: a + 5}  # Mismatch: x+1 != (x)+5
    tower = CofinalShadowTower(nodes, projectors, transitions)
    assert tower.verify_tower_coherence(10) is False

    # Fiber quotient helpers
    quotient = ProfileFiberQuotient(tower, [1, 2, 3])
    assert quotient.num_fibers() == 3
    assert len(quotient.get_fiber_of(1)) == 1

    # Out of image profile KeyError
    q: QueryProbe[int, Rational] = QueryProbe("Q", 1, lambda x: Rational(x))
    solver = ProfileFactorizationSolver(tower, q, [1, 2])
    ok, q_bar, _ = solver.solve_factorization()
    assert ok is True
    assert q_bar is not None
    with pytest.raises(KeyError, match="outside the realized domain"):
        q_bar((999, 999))

    # HigherQueryFamily failure branch
    q_bad: QueryProbe[int, Rational] = QueryProbe("Q_Bad", 1, lambda x: Rational(x))
    fam = HigherQueryFamily(max_degree=1, queries=[q_bad])
    tower_const = CofinalShadowTower([ShadowNode("N", 1)], {"N": lambda x: 0}, {})
    q_const_quotient = ProfileFiberQuotient(tower_const, [1, 2])
    ok_fam, fails = fam.verify_family_fiber_constancy(q_const_quotient)
    assert ok_fam is False
    assert len(fails) > 0

    # Explicit tau_q and tau_coda_cs on BridgePacketCore
    packet_explicit = BridgePacketCore(
        packet_id="B_Expl",
        tower=tower_const,
        domain=[1, 2],
        query=QueryProbe("Q", 1, lambda x: Rational(1)),
        tau_q=lambda x: Rational(1),
        tau_coda_cs=lambda x: Rational(1),
    )
    audit_expl = packet_explicit.audit_8_step_admission()
    assert audit_expl["step8_status"] == "EXPLICIT_TERMINALIZERS_AGREE"

    # Generator semigroup adapter methods
    assert GeneratorSemigroupAdapter.translation_step(lambda x: x + 2, 3, 4) == 9
    assert GeneratorSemigroupAdapter.action_composition(Rational(1, 2), Rational(1, 3)) == Rational(5, 6)

    # Step8 un-implemented branch (lines 390-392)
    packet_no_fact = BridgePacketCore(
        packet_id="B_NoFact",
        tower=tower_const,
        domain=[1, 2],
        query=QueryProbe("Q_nonfact", 1, lambda x: Rational(x)),
        tau_q=None,
        tau_coda_cs=None,
    )
    audit_no_fact = packet_no_fact.audit_8_step_admission()
    assert audit_no_fact["step8_status"] == "OPEN_NOT_IMPLEMENTED"

    # Residual taxonomy flags (lines 468, 470)
    res_list = BridgeResidualTaxonomy.classify_residual(
        profile_factored=True,
        tower_coherent=False,
        terminal_conserved=False,
        authority_effect="None",
    )
    assert any("R_trans" in r for r in res_list)
    assert any("R_cons" in r for r in res_list)


def test_pseudometric_zero_error_countermodel_b1() -> None:
    """
    Review finding B1:
    In a pseudometric space, epsilon = 0 does NOT imply q(x) = q(y).
    Explicit countermodel: 2-point target Y = {'a', 'b'} with indiscrete pseudometric dist(y1, y2) = 0.
    Profile is constant, query separates states, decoder achieves epsilon = 0 distance,
    collision distance is 0 <= 2*0 = 0, but query is NOT fiber-constant as equality of elements.
    """
    states = ["x1", "x2"]

    def prof_map(x: str) -> int:
        return 0  # constant profile

    query_map = {"x1": "answer_a", "x2": "answer_b"}  # q(x1) != q(x2)
    decoder_val = "answer_a"  # g(0) = answer_a

    # Indiscrete pseudometric: dist(a, b) = 0 for all answers
    def pseudo_dist(y1: str, y2: str) -> Rational:
        return Rational(0)

    # 1. Decoder is zero-error in pseudometric distance:
    for s in states:
        assert pseudo_dist(query_map[s], decoder_val) <= 0

    # 2. Collision distance on fiber is zero:
    assert pseudo_dist(query_map["x1"], query_map["x2"]) <= 2 * 0
    assert pseudo_dist(query_map["x1"], query_map["x2"]) == 0

    # 3. But query values are distinct as values:
    assert query_map["x1"] != query_map["x2"]

    # 4. Therefore, exact value factorization on image fails:
    node: ShadowNode[str] = ShadowNode("N", 1)
    tower = CofinalShadowTower([node], {"N": prof_map}, {})
    query: QueryProbe[str, str] = QueryProbe("q", 1, lambda x: query_map[x])
    solver = ProfileFactorizationSolver(tower, query, states)
    ok, factor, err = solver.solve_factorization()
    assert ok is False
    assert factor is None
    assert "Fiber constancy violation" in str(err)


def test_prevent_vacuous_admission_b7() -> None:
    """Review finding B7: Empty evaluation domain must NOT pass admission."""
    node: ShadowNode[int] = ShadowNode("N", 1)
    tower = CofinalShadowTower([node], {"N": lambda x: 0}, {})
    query: QueryProbe[int, int] = QueryProbe("q", 1, lambda x: 42)

    # Empty domain packet
    packet = BridgePacketCore(
        packet_id="empty_domain_packet",
        tower=tower,
        domain=[],
        query=query,
    )
    audit = packet.audit_8_step_admission()
    assert audit["is_admissible"] is False
    assert audit["steps"]["1_finite_packet_validity"] is False
    assert audit["steps"]["2_tower_coherence"] is False
    assert audit["steps"]["5_profile_factorization"] is False
    assert audit["steps"]["8_terminal_conservativity"] is False
    assert audit["status"] == "ADMISSION_FAILED"


def test_honest_image_point_p2() -> None:
    """Review finding P2: ImagePoint must validate that p(witness) == val."""
    node: ShadowNode[int] = ShadowNode("N", 1)
    tower = CofinalShadowTower([node], {"N": lambda x: x * 2}, {})

    # Honest construction via tower factory
    pt = ImagePoint.from_tower(tower, witness=5)
    assert pt.val == (10,)
    assert pt.witness == 5

    # Fabricated point rejected by validator
    with pytest.raises(ValueError, match="ImagePoint witness mismatch"):
        ImagePoint(val=(999,), witness=5, profile_fn=tower.evaluate_profile)


def test_tower_validation_p1() -> None:
    """Review finding P1: Tower constructor must reject duplicate IDs and broken endpoints."""
    # Duplicate node ID
    with pytest.raises(ValueError, match="Duplicate node_id"):
        CofinalShadowTower(
            nodes=[ShadowNode("N1", 1), ShadowNode("N1", 2)],
            projectors={"N1": lambda x: x},
            transitions={},
        )

    # Missing projector
    with pytest.raises(ValueError, match="Missing projector"):
        CofinalShadowTower(
            nodes=[ShadowNode("N1", 1)],
            projectors={},
            transitions={},
        )

    # Transition with undeclared endpoint
    with pytest.raises(ValueError, match="not in tower nodes"):
        CofinalShadowTower(
            nodes=[ShadowNode("N1", 1)],
            projectors={"N1": lambda x: x},
            transitions={("N1", "N_UNDECLARED"): lambda a: a},
        )

