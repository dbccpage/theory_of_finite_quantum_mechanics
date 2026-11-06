"""Finite validation boundaries and injected solver-certificate failures."""

from dataclasses import replace

import cochain_presentation as cochain
import coda_gtla_core as core
import pytest
from sympy import Matrix, Mul, Rational


def presentation(size=2):
    return core.FinitePresentation(
        "boundary", size, tuple(tuple(0 for _ in range(size)) for _ in range(size))
    )


def residual_packet():
    return core.ProblemInstance(
        problem_id="boundary",
        raw_data="exact input",
        candidate_sieve=("c",),
        coarse_profile=(0,),
        fine_profile=(0,),
        projection_map={0: 0},
        local_sections={"U": (0,)},
        overlaps={},
        d0=Matrix([[0]]),
        d1=None,
        defect_cochain=Matrix([2]),
        fda_license_granted=False,
    )


@pytest.mark.parametrize("right, message", [((0, 2), "out of range"), ((0, 0), "surjective")])
def test_right_projection_must_cover_exact_target(right, message):
    p = presentation()
    with pytest.raises(ValueError, match=message):
        core.ComparisonSpan(p, p, 2, (0, 1), right)


@pytest.mark.parametrize(
    "changes, error",
    [
        ({"is_closed_loop": 1}, TypeError),
        ({"is_trivial_monodromy": "false"}, TypeError),
        ({"is_closed_loop": False}, ValueError),
        ({"monodromy_defect": Rational(1)}, ValueError),
    ],
)
def test_transport_records_reject_contradictory_flags(changes, error):
    cert = core.compute_transport_certificate(core.make_diag_span(presentation()))
    with pytest.raises(error):
        replace(cert, **changes)


def test_transport_mode_and_homotopy_domain_boundaries():
    with pytest.raises(ValueError, match="size must be >= 2"):
        core.build_monodromy_transport_loop(presentation(1))
    with pytest.raises(ValueError, match="Unknown"):
        core.build_monodromy_transport_loop(presentation(), "unregistered-mode")
    for defect, d0, h in (
        (Matrix([[1, 2]]), Matrix([[1]]), Matrix([0])),
        (Matrix([1]), Matrix([[1]]), Matrix([[0, 0]])),
        (Matrix([1, 2]), Matrix([[1]]), Matrix([0])),
    ):
        with pytest.raises(ValueError):
            core.apply_cochain_homotopy(defect, d0, h)
    wrong_h = core.verify_cochain_homotopy_invariance(
        Matrix([[1]]), Matrix([1]), Matrix([2]), Matrix([0])
    )
    assert not wrong_h["is_exact_homotopy"] and not wrong_h["invariance_holds"]
    assert wrong_h["phi1_defect1"] == wrong_h["phi1_defect2"] == "0"
    assert wrong_h["witness1_certifies_defect2"] and wrong_h["witness2_certifies_defect1"]
    span = core.make_diag_span(presentation())
    no_traces = core.evaluate_span_homotopy_transport([span], [span])
    assert no_traces["certificates_identical"]
    assert not no_traces["two_level_cost_divergence"]


def test_terminal_constructors_and_dual_validation_reject_inconsistent_data():
    token = core.AuthorityToken("t", "model", "boundary", "STANDARD_EVALUATION", True, "opaque")
    with pytest.raises(ValueError, match="phi1_distance must be non-negative"):
        core.TerminalOutcome(core.TerminalKind.REFUSED, "negative", Rational(-1), None, "refuse")
    with pytest.raises(ValueError, match="cannot carry a refusal"):
        core.TerminalOutcome(
            core.TerminalKind.AUTHORIZED,
            "contradictory",
            Rational(0),
            Rational(0),
            "refuse",
            authority_token=token,
        )
    with pytest.raises(ValueError, match="gamma2 = 0"):
        core.TerminalOutcome(
            core.TerminalKind.CLOSED_RESIDUAL,
            "nonclosed",
            Rational(1),
            Rational(1),
            dual_witness=(Rational(1),),
        )
    assert not core.validate_dual_witness(Matrix([[0]]), Matrix([1]), (), Rational(1))
    assert not core.validate_dual_witness(Matrix([[1]]), Matrix([1]), (Rational(1),), Rational(1))
    receipt = core.execute_master_normal_form(
        replace(residual_packet(), d0=Matrix([[1]]), fda_license_granted=True)
    )
    assert core.evaluate_authority_firewall(receipt)["firewall_intact"]
    # Simulate corrupted storage bypassing construction; replay must detect it.
    object.__setattr__(receipt.terminal_outcome, "phi1_distance", Rational(9))
    assert not core.evaluate_authority_firewall(receipt)["firewall_intact"]


def pair_groupoid():
    arrows = ["aa", "ab", "ba", "bb"]
    return core.FiniteGroupoid(
        objects=["a", "b"],
        morphisms={"a": {"a": ["aa"], "b": ["ab"]}, "b": {"a": ["ba"], "b": ["bb"]}},
        id_map={"a": "aa", "b": "bb"},
        comp_table={(g, f): f[0] + g[1] for g in arrows for f in arrows if f[1] == g[0]},
        inv_map={f: f[::-1] for f in arrows},
    )


@pytest.mark.parametrize(
    "change",
    [
        {"inv_map": {"aa": "aa", "ab": "aa", "ba": "ab", "bb": "bb"}},
        {"comp_table_entry": (("ab", "ba"), "aa")},
        {"comp_table_entry": (("bb", "ab"), "bb")},
        {"comp_table_entry": (("ab", "aa"), "aa")},
    ],
)
def test_groupoid_rejects_wrong_inverse_endpoints_and_unit_laws(change):
    g = pair_groupoid()
    assert g.validate()
    if "comp_table_entry" in change:
        pair, value = change["comp_table_entry"]
        g.comp_table[pair] = value
    else:
        g.inv_map = change["inv_map"]
    assert not g.validate()
    with pytest.raises(ValueError):
        core.FaithfulGroupoidEmbedding(g)


def test_groupoid_rejects_extra_entries_unknown_products_and_nonassociativity():
    g = core.make_z2_groupoid()
    g.inv_map["undeclared"] = "e"
    assert not g.validate()
    g = core.make_z2_groupoid()
    g.comp_table[("undeclared", "e")] = "e"
    assert not g.validate()
    # Unit/inverse checks alone do not imply valid composition or associativity.
    for product in ("undeclared", "e"):
        g = core.make_z3_groupoid()
        g.comp_table[("g", "g")] = product
        assert not g.validate()


def test_exact_scalar_gate_does_not_numerically_approximate_expressions():
    assert cochain._as_exact_rational(7) == Rational(7)
    expression = Mul(2, Rational(1, 2), evaluate=False)
    with pytest.raises(TypeError):
        cochain._as_exact_rational(expression)
    with pytest.raises(TypeError):
        core._validate_exact_rational(expression, "expression")


def test_solver_rejects_faulty_exactness_and_quotient_certificates(monkeypatch):
    solver = cochain.LinearRepairProblem(Matrix([[1]]))
    with monkeypatch.context() as patch:
        patch.setattr(cochain.ExactnessCertificate, "verify", lambda self: False)
        with pytest.raises(ArithmeticError, match="exactness certificate"):
            solver.exactness_certificate(Matrix([2]))
    with monkeypatch.context() as patch:
        patch.setattr(cochain.QuotientDistanceCertificate, "verify", lambda self: False)
        with pytest.raises(ArithmeticError, match="quotient certificate"):
            solver.quotient_l1_distance(Matrix([2]))
    with monkeypatch.context() as patch:
        patch.setattr(
            cochain, "_exact_l1_dual_vertex", lambda d0, omega: (Matrix([0]), Rational(1))
        )
        with pytest.raises(ArithmeticError, match="optima disagree"):
            solver.quotient_l1_distance(Matrix([2]))


def test_foc_and_cycle_quotient_reject_a_corrupted_solver_witness(monkeypatch):
    p = residual_packet()
    good = cochain.LinearRepairProblem(p.d0).quotient_l1_distance(p.defect_cochain)
    bad = replace(good, dual_witness=Matrix([0]))
    assert not bad.verify()
    monkeypatch.setattr(
        cochain.LinearRepairProblem, "quotient_l1_distance", lambda self, cochain: bad
    )
    with pytest.raises(ArithmeticError, match="dual witness"):
        core.functor_foc_sharp(p, core.DSharpOutput(True, True, (Rational(0),), (0,)))
    z = Matrix([[0]])
    b = core.Bicomplex2Nerve(z, z, z, z, z, z, z)
    with pytest.raises(ArithmeticError, match="E2 page quotient certificate"):
        b.certify_e2_coboundary_bounds(Matrix([2]))


def test_solver_backend_failure_never_returns_a_zero_certificate(monkeypatch):
    with monkeypatch.context() as patch:
        patch.setattr(cochain, "_independent_column_indices", lambda d0, rank: (0,))
        patch.setattr(cochain, "combinations", lambda values, count: iter(()))
        with pytest.raises(ArithmeticError, match="no candidates"):
            cochain._exact_l1_primal_vertex(Matrix([[1]]), Matrix([2]))
    with monkeypatch.context() as patch:

        def failed_linear_solve(self, rhs, *args, **kwargs):
            raise ValueError("injected linear-algebra backend failure")

        patch.setattr(type(Matrix([[1]])), "gauss_jordan_solve", failed_linear_solve)
        with pytest.raises(ArithmeticError, match="no dual l1 vertex"):
            cochain._exact_l1_dual_vertex(Matrix([[1], [1]]), Matrix([1, 0]))


def test_generated_action_is_checked_before_exposure(monkeypatch):
    monkeypatch.setattr(core.FaithfulGroupoidEmbedding, "check_faithfulness", lambda self: False)
    with pytest.raises(ArithmeticError, match="Regular action"):
        core.FaithfulGroupoidEmbedding(core.make_z2_groupoid())
