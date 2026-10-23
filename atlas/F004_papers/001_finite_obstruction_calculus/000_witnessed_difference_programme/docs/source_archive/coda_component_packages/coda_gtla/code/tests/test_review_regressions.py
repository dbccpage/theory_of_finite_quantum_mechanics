"""Adversarial regressions for the 2026-09-27 statement and runtime review."""

from dataclasses import replace
from fractions import Fraction
from itertools import product

import pytest
from cochain_presentation import (
    LinearRepairProblem,
    _as_exact_rational,
    _independent_column_indices,
    exact_equal,
)
from coda_gtla_core import (
    Bicomplex2Nerve,
    ComparisonSpan,
    DSharpOutput,
    FaithfulGroupoidEmbedding,
    FiniteGroupoid,
    FinitePresentation,
    FocSharpOutput,
    ProblemInstance,
    Trace,
    _canonical_record,
    _validate_matrix_exactness,
    compute_transport_certificate,
    evaluate_authority_firewall,
    execute_master_normal_form,
    extensional_equal,
    functor_foc_sharp,
    functor_tau_sharp,
    make_z2_groupoid,
    make_z3_groupoid,
)
from sympy import Float, Matrix, Rational, sqrt


def packet(**changes):
    values = dict(
        problem_id="review",
        raw_data="datum",
        candidate_sieve=("c",),
        coarse_profile=(0,),
        fine_profile=(0,),
        projection_map={0: 0},
        local_sections={"U": (0,)},
        overlaps={},
        d0=Matrix([[1]]),
        d1=None,
        defect_cochain=Matrix([0]),
        fda_license_granted=True,
    )
    values.update(changes)
    return ProblemInstance(**values)


def test_all_intersections_are_checked_and_global_section_restricts():
    conflict = packet(cover={"U": (0,), "V": (0,)}, local_sections={"U": (0,), "V": (1,)})
    assert execute_master_normal_form(conflict).is_refused()
    for sections in ({"U": (2,), "V": (3,)}, {"V": (3,), "U": (2,)}):
        result = execute_master_normal_form(
            packet(cover={"U": (4,), "V": (9,)}, local_sections=sections)
        )
        assert result.is_authorized()
        assert dict(zip(result.d_stage.global_domain, result.d_stage.global_section)) == {
            4: 2,
            9: 3,
        }


@pytest.mark.parametrize(
    "changes",
    [
        {"cover": {"U": (0,), "V": (1,)}},
        {"cover": {"V": (0,)}},
        {"cover": {"U": (0, 1)}},
        {"local_sections": {"U": ()}},
        {"overlaps": {("U", "missing"): True}},
        {"overlaps": {("U", "U"): False}},
        {"local_sections": {"U": (0,), "V": (1,)}},
    ],
)
def test_incomplete_or_conflicting_cover_fails_closed(changes):
    result = execute_master_normal_form(packet(**changes))
    assert result.is_refused() and result.foc_stage is None
    assert result.terminal_outcome.phi1_distance is None


@pytest.mark.parametrize(
    "changes, error",
    [
        ({"coarse_profile": (0, 1)}, ValueError),
        ({"fine_profile": (0, 1)}, ValueError),
        ({"fda_license_granted": "false"}, TypeError),
        ({"fda_license_granted": 1}, TypeError),
        ({"raw_data": {}}, TypeError),
        ({"problem_id": ""}, ValueError),
        ({"defect_cochain": [0]}, TypeError),
        ({"d0": [[1]]}, TypeError),
        ({"d0": Matrix.zeros(2, 1)}, ValueError),
        ({"d1": [[0]]}, TypeError),
        ({"d1": Matrix.zeros(0, 2)}, ValueError),
        ({"overlaps": {("U", "U"): 1}}, TypeError),
        ({"overlaps": {"U": True}}, ValueError),
        ({"cover": {"U": (0, 0)}}, ValueError),
        ({"cover": {"U": (-1,)}}, ValueError),
        ({"authority_token": True}, TypeError),
    ],
)
def test_problem_domain_validation(changes, error):
    with pytest.raises(error):
        packet(**changes)


def test_exact_distance_and_forged_stage_rejection():
    problem = packet(d0=Matrix([[0]]), d1=Matrix([[1]]), defect_cochain=Matrix([7]))
    result = execute_master_normal_form(problem)
    assert result.foc_stage.phi1_distance == 7
    assert result.foc_stage.gamma2_distance == 7
    assert result.is_refused()
    fake = FocSharpOutput(Rational(0), Rational(0), True, False, False)
    refused = functor_tau_sharp(problem, result.r_stage, result.d_stage, fake)
    assert refused.is_refused and refused.phi1_distance is None
    no_foc = functor_tau_sharp(problem, result.r_stage, result.d_stage, None)
    assert no_foc.is_refused and no_foc.phi1_distance is None
    with pytest.raises(ValueError, match="uncomputed"):
        functor_foc_sharp(problem, DSharpOutput(False, False))
    forged_receipt = replace(result, foc_stage=fake)
    assert not evaluate_authority_firewall(forged_receipt)["firewall_intact"]


def test_input_snapshot_and_digest_bind_all_record_fields():
    matrix = Matrix([[1]])
    sections = {"U": [0]}
    p = packet(d0=matrix, local_sections=sections)
    matrix[0, 0] = 0
    sections["U"][0] = 99
    assert p.d0 == Matrix([[1]]) and p.local_sections["U"] == (0,)
    with pytest.raises(TypeError):
        p.d0[0, 0] = 0
    with pytest.raises(TypeError):
        p.local_sections["U"] = (9,)
    original = execute_master_normal_form(p)
    for changed in (
        replace(p, raw_data="other"),
        replace(p, d0=Matrix([[2]])),
        replace(p, authority_token=replace(p.authority_token, issuer="another")),
        replace(p, authority_token=replace(p.authority_token, signature_hash="other")),
    ):
        assert execute_master_normal_form(changed).sha256_digest() != original.sha256_digest()
    assert (
        replace(original, d_stage=replace(original.d_stage, global_section=(9,))).sha256_digest()
        != original.sha256_digest()
    )
    assert _canonical_record(Fraction(1, 3)) == {"rational": "1/3"}
    with pytest.raises(TypeError):
        _canonical_record(object())


@pytest.mark.parametrize(
    "field, value", [("subject", "another"), ("scope", "OTHER"), ("is_valid", False)]
)
def test_model_license_is_scoped(field, value):
    p = packet()
    assert p.authority_token.signature_hash == "UNAUTHENTICATED_MODEL_RECORD"
    assert execute_master_normal_form(
        replace(p, authority_token=replace(p.authority_token, **{field: value}))
    ).is_refused()


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("token_id", "", ValueError),
        ("issuer", "", ValueError),
        ("subject", "", ValueError),
        ("scope", "", ValueError),
        ("is_valid", "true", TypeError),
        ("signature_hash", "", ValueError),
    ],
)
def test_declared_token_schema(field, value, error):
    with pytest.raises(error):
        replace(packet().authority_token, **{field: value})


def test_transport_hash_covers_relation_presentation_and_trace_steps():
    p = FinitePresentation("P", 2, ((0, 0), (0, 0)))
    q = replace(p, name="Q")
    s = ComparisonSpan(p, q, 2, (0, 1), (0, 1))
    swap = replace(s, right_map=(1, 0))
    a, b = compute_transport_certificate(s), compute_transport_certificate(swap)
    assert a.sha256_hash != b.sha256_hash and a.extensional_hash != b.extensional_hash
    c = compute_transport_certificate(s, Trace(1, Rational(2), s))
    d = compute_transport_certificate(s, Trace(2, Rational(2), s))
    assert c.sha256_hash != d.sha256_hash and c.extensional_hash == d.extensional_hash
    changed = replace(s, p1=replace(p, diff_matrix=((0, 1), (1, 0))))
    assert not extensional_equal(s, changed)
    assert compute_transport_certificate(changed).extensional_hash != a.extensional_hash
    with pytest.raises(ValueError):
        compute_transport_certificate(s, Trace(1, Rational(0), swap))
    with pytest.raises(TypeError):
        _validate_matrix_exactness([[1]], "matrix")


def group(names, operation):
    return FiniteGroupoid(
        ["*"],
        {"*": {"*": names}},
        {"*": names[0]},
        {(g, f): names[operation(i, j)] for i, g in enumerate(names) for j, f in enumerate(names)},
        {
            g: next(f for j, f in enumerate(names) if operation(i, j) == 0)
            for i, g in enumerate(names)
        },
    )


def test_regular_action_handles_noncyclic_groups_and_arrow_renaming():
    klein = group(["id", "a", "b", "c"], lambda i, j: i ^ j)
    cyclic = group(["unit", "second", "third", "fourth"], lambda i, j: (i + j) % 4)
    for g in (klein, cyclic, make_z2_groupoid(), make_z3_groupoid()):
        assert FaithfulGroupoidEmbedding(g).check_faithfulness()
    two_objects = FiniteGroupoid(
        ["A", "B"],
        {"A": {"A": ["a"]}, "B": {"B": ["b"]}},
        {"A": "a", "B": "b"},
        {("a", "a"): "a", ("b", "b"): "b"},
        {"a": "a", "b": "b"},
    )
    assert FaithfulGroupoidEmbedding(two_objects).check_faithfulness()
    emb = FaithfulGroupoidEmbedding(cyclic)
    emb.spans["second"], emb.spans["third"] = emb.spans["third"], emb.spans["second"]
    assert not emb.check_faithfulness()
    emb = FaithfulGroupoidEmbedding(make_z2_groupoid())
    emb.spans["e"], emb.spans["g"] = emb.spans["g"], emb.spans["e"]
    assert not emb.check_faithfulness()
    emb.spans["g"] = emb.spans["e"]
    assert not emb.check_faithfulness()


@pytest.mark.parametrize(
    "change",
    [
        {"objects": []},
        {"objects": ["*", "*"]},
        {"id_map": {}},
        {"morphisms": {"alien": {"*": ["e", "g"]}}},
        {"morphisms": {"*": {"alien": ["e", "g"]}}},
        {"morphisms": {"*": {"*": ["g"]}}},
        {"morphisms": {"*": {"*": ["e", "g", "g"]}}},
        {"inv_map": {"e": "e"}},
        {"inv_map": {"e": "e", "g": "absent"}},
        {"comp_table": {("e", "e"): "e"}},
    ],
)
def test_invalid_groupoids_are_rejected(change):
    bad = replace(make_z2_groupoid(), **change)
    assert not bad.validate()
    with pytest.raises(ValueError):
        FaithfulGroupoidEmbedding(bad)


@pytest.mark.parametrize("value", [False, 0.5, Float("0.5"), sqrt(2), object()])
def test_cochain_scalar_rejections(value):
    with pytest.raises(TypeError):
        _as_exact_rational(value)


def test_exactness_and_lp_certificates_on_degenerate_and_rank_deficient_maps():
    assert _as_exact_rational(Fraction(2, 3)) == Rational(2, 3)
    assert _as_exact_rational("2/3") == Rational(2, 3)
    with pytest.raises((ValueError, TypeError)):
        _as_exact_rational("not-a-rational")
    assert not exact_equal(Matrix([[1]]), Matrix([[1, 1]]))
    with pytest.raises(ArithmeticError):
        _independent_column_indices(Matrix([[0]]), 1)
    maps = [
        Matrix.zeros(0, 0),
        Matrix.zeros(2, 0),
        Matrix.zeros(2, 1),
        Matrix([[1], [0]]),
        Matrix([[0, 1], [0, 2], [0, 0]]),
        Matrix.eye(2),
        Matrix([[2], [1], [0]]),
    ]
    for d0 in maps:
        solver = LinearRepairProblem(d0)
        for entries in product((-1, 0, 1), repeat=d0.rows):
            omega = Matrix(d0.rows, 1, entries)
            exact = solver.exactness_certificate(omega)
            assert exact.verify()
            cert = solver.quotient_l1_distance(omega)
            assert cert.verify() and cert.distance >= 0
            assert (cert.distance == 0) == exact.is_exact_coboundary
            assert cert.dual_pairing == sum(abs(x) for x in cert.residual)
        for method in (solver.exactness_certificate, solver.quotient_l1_distance):
            with pytest.raises(ValueError, match="shape"):
                method(Matrix.zeros(d0.rows, 2))
    exact = LinearRepairProblem(Matrix([[1]])).exactness_certificate(Matrix([2]))
    assert not replace(exact, witness=None).verify()
    nonexact = LinearRepairProblem(Matrix([[0]])).exactness_certificate(Matrix([2]))
    assert not replace(nonexact, separating_left_kernel_vector=None).verify()
    assert not replace(nonexact, separating_pairing=None).verify()
    assert not replace(nonexact, separating_pairing=Rational(0)).verify()
    cert = LinearRepairProblem(Matrix([[1], [0]])).quotient_l1_distance(Matrix([2, 3]))
    for changes in (
        {"residual": Matrix([0, 4])},
        {"distance": Rational(4)},
        {"dual_witness": Matrix([1, 1])},
        {"dual_witness": Matrix([0, 2])},
        {"dual_pairing": Rational(2)},
    ):
        assert not replace(cert, **changes).verify()


def test_bicomplex_input_and_representative_domains():
    b = Bicomplex2Nerve.build_canonical_2nerve()
    with pytest.raises(ValueError, match="shape"):
        b.compute_d2_zigzag_obstruction(Matrix([1]))
    with pytest.raises(ValueError, match="shape"):
        b.compute_d2_zigzag_obstruction(Matrix([1, 0, -1]), Matrix([1]))
    with pytest.raises(ValueError, match="column"):
        b.certify_e2_coboundary_bounds(Matrix([[1, 1]]))
    z, one = Matrix([[0]]), Matrix([[1]])
    unsolvable = Bicomplex2Nerve(z, one, z, z, z, z, z)
    with pytest.raises(ArithmeticError, match="not in im"):
        unsolvable.compute_d2_zigzag_obstruction(Matrix([1]))
    for maps in (
        (one, z, one, z, z, z, z),
        (z, one, z, one, z, z, z),
        (one, z, z, z, z, one, z),
        (z, z, one, z, z, z, one),
    ):
        with pytest.raises(ArithmeticError):
            Bicomplex2Nerve(*maps)
    for args in ((True, 2), (4, False), (4, 0), (2, 2)):
        with pytest.raises((TypeError, ValueError)):
            Bicomplex2Nerve.compare_dimension_scaling(*args)


def test_figure_cli_writes_requested_artifact(tmp_path, monkeypatch):
    import runpy
    import sys
    from pathlib import Path

    import generate_figures

    source = Path(generate_figures.__file__).resolve()
    output = tmp_path / "architecture.png"
    monkeypatch.setattr(sys, "argv", [str(source), "--output", str(output)])
    runpy.run_path(str(source), run_name="__main__")
    assert output.read_bytes().startswith(b"\x89PNG")
