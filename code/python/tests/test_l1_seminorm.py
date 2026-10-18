"""Unit, negative, integration, end-to-end, and mutation tests for Phi1."""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from src.homology.boundary import triangle_boundaries, triangle_boundary_defect
from src.functional.l1_seminorm import (
    ExactPhi1Certificate,
    L1Seminorm,
    L1SeminormError,
    evaluate_weighted_l1_quotient,
)

_MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "functional" / "l1_seminorm.py"
)


def test_zero_certificate() -> None:
    boundary = [[Fraction(1)], [Fraction(-1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)
    cert = ExactPhi1Certificate(
        omega=[Fraction(0), Fraction(0)],
        d0=boundary,
        weights=weights,
        alpha=[Fraction(0)],
        primal_residual=[Fraction(0), Fraction(0)],
        dual_witness=[Fraction(0), Fraction(0)],
        reported_value=Fraction(0),
    )
    verified = semi.verify_certificate(cert)
    assert verified.value == Fraction(0)


def test_quotient_projection_reduction() -> None:
    boundary = [[Fraction(1)], [Fraction(1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)
    cert = ExactPhi1Certificate(
        omega=[Fraction(2), Fraction(0)],
        d0=boundary,
        weights=weights,
        alpha=[Fraction(1)],
        primal_residual=[Fraction(1), Fraction(-1)],
        dual_witness=[Fraction(1), Fraction(-1)],
        reported_value=Fraction(2),
    )
    verified = semi.verify_certificate(cert)
    assert verified.value == Fraction(2)
    assert verified.d0 == boundary
    assert verified.weights == weights


def test_boundary_binding_mismatch() -> None:
    boundary = [[Fraction(1)], [Fraction(1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)
    other_boundary = [[Fraction(1)], [Fraction(-1)]]
    cert = ExactPhi1Certificate(
        omega=[Fraction(0), Fraction(0)],
        d0=other_boundary,
        weights=weights,
        alpha=[Fraction(0)],
        primal_residual=[Fraction(0), Fraction(0)],
        dual_witness=[Fraction(0), Fraction(0)],
        reported_value=Fraction(0),
    )
    with pytest.raises(L1SeminormError, match="Boundary binding mismatch") as caught:
        semi.verify_certificate(cert)
    assert caught.value.parameters["rows"] == 2


def test_dual_orthogonality_violation() -> None:
    boundary = [[Fraction(1)], [Fraction(1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)
    cert = ExactPhi1Certificate(
        omega=[Fraction(2), Fraction(0)],
        d0=boundary,
        weights=weights,
        alpha=[Fraction(1)],
        primal_residual=[Fraction(1), Fraction(-1)],
        dual_witness=[Fraction(1), Fraction(1)],
        reported_value=Fraction(2),
    )
    with pytest.raises(L1SeminormError, match="Dual witness not orthogonal") as caught:
        semi.verify_certificate(cert)
    assert caught.value.parameters["pairing"] == "2"


def test_negative_boundary_refusals() -> None:
    with pytest.raises(L1SeminormError, match="float refused") as caught:
        L1Seminorm([[1.5], [0.0]], [1, 1])
    assert caught.value.parameters["role"] == "boundary[0][0]"
    with pytest.raises(L1SeminormError, match="boolean refused"):
        L1Seminorm([[True], [False]], [1, 1])
    with pytest.raises(L1SeminormError, match="strictly positive") as caught:
        L1Seminorm([[1], [0]], [1, 0])
    assert caught.value.parameters["index"] == 1
    with pytest.raises(L1SeminormError, match="rectangular") as caught:
        L1Seminorm([[1, 0], [1]], [1, 1])
    assert caught.value.parameters["row"] == 1
    with pytest.raises(L1SeminormError, match="Boundary rows") as caught:
        L1Seminorm([[1]], [1, 1])
    assert caught.value.parameters["weights"] == 2
    with pytest.raises(L1SeminormError, match="denominator is zero"):
        L1Seminorm([[(1, 0)]], [(1, 1)])
    with pytest.raises(L1SeminormError, match="not an exact rational"):
        L1Seminorm([["1"]], [1])


def test_negative_certificate_refusals() -> None:
    boundary = [[Fraction(1)], [Fraction(0)]]
    weights = [Fraction(2), Fraction(3)]
    semi = L1Seminorm(boundary, weights)
    good = ExactPhi1Certificate(
        omega=[Fraction(1), Fraction(2)],
        d0=[[Fraction(1)], [Fraction(0)]],
        weights=[Fraction(2), Fraction(3)],
        alpha=[Fraction(1)],
        primal_residual=[Fraction(0), Fraction(2)],
        dual_witness=[Fraction(0), Fraction(3)],
        reported_value=Fraction(6),
    )
    assert semi.verify_certificate(good).value == Fraction(6)

    short = ExactPhi1Certificate(
        omega=[Fraction(1)],
        d0=good.d0,
        weights=good.weights,
        alpha=good.alpha,
        primal_residual=good.primal_residual,
        dual_witness=good.dual_witness,
        reported_value=good.reported_value,
    )
    with pytest.raises(L1SeminormError, match="vector length") as caught:
        semi.verify_certificate(short)
    assert caught.value.parameters["role"] == "omega"

    bad_alpha = ExactPhi1Certificate(
        omega=good.omega,
        d0=good.d0,
        weights=good.weights,
        alpha=[],
        primal_residual=good.primal_residual,
        dual_witness=good.dual_witness,
        reported_value=good.reported_value,
    )
    with pytest.raises(L1SeminormError, match="Alpha length") as caught:
        semi.verify_certificate(bad_alpha)
    assert caught.value.parameters["expected"] == 1

    bad_weight = ExactPhi1Certificate(
        omega=good.omega,
        d0=good.d0,
        weights=[Fraction(1), Fraction(1)],
        alpha=good.alpha,
        primal_residual=good.primal_residual,
        dual_witness=[Fraction(0), Fraction(1)],
        reported_value=Fraction(2),
    )
    with pytest.raises(L1SeminormError, match="Weight binding mismatch"):
        semi.verify_certificate(bad_weight)

    bad_residual = ExactPhi1Certificate(
        omega=good.omega,
        d0=good.d0,
        weights=good.weights,
        alpha=good.alpha,
        primal_residual=[Fraction(1), Fraction(2)],
        dual_witness=good.dual_witness,
        reported_value=good.reported_value,
    )
    with pytest.raises(L1SeminormError, match="Primal residual mismatch") as caught:
        semi.verify_certificate(bad_residual)
    assert caught.value.parameters["index"] == 0

    bad_box = ExactPhi1Certificate(
        omega=[Fraction(0), Fraction(1)],
        d0=good.d0,
        weights=good.weights,
        alpha=[Fraction(0)],
        primal_residual=[Fraction(0), Fraction(1)],
        dual_witness=[Fraction(0), Fraction(4)],
        reported_value=Fraction(4),
    )
    with pytest.raises(L1SeminormError, match="dual witness bound violated") as caught:
        semi.verify_certificate(bad_box)
    assert caught.value.parameters["weight"] == "3"

    bad_gap = ExactPhi1Certificate(
        omega=good.omega,
        d0=good.d0,
        weights=good.weights,
        alpha=good.alpha,
        primal_residual=good.primal_residual,
        dual_witness=good.dual_witness,
        reported_value=Fraction(7),
    )
    with pytest.raises(L1SeminormError, match="Duality gap not closed") as caught:
        semi.verify_certificate(bad_gap)
    assert caught.value.parameters["reported"] == "7"
    assert caught.value.invariant == "Duality gap not closed"


def test_integration_with_triangle_boundary() -> None:
    """Phi1 of the face column is zero, and the neighbor's matrix defect is zero."""
    assert triangle_boundary_defect() == Fraction(0)
    _edge, face = triangle_boundaries()
    boundary = [face.row(index) for index in range(face.rows)]
    weights = [Fraction(1), Fraction(1), Fraction(1)]
    column = [Fraction(entry) for entry in face.col(0)]
    certified = evaluate_weighted_l1_quotient(
        boundary=boundary,
        weights=weights,
        omega=column,
        alpha=[Fraction(1)],
        primal_residual=[Fraction(0), Fraction(0), Fraction(0)],
        dual_witness=[Fraction(0), Fraction(0), Fraction(0)],
        reported_value=Fraction(0),
    )
    assert certified == Fraction(0)
    off_face = evaluate_weighted_l1_quotient(
        boundary=boundary,
        weights=weights,
        omega=[Fraction(1), Fraction(0), Fraction(0)],
        alpha=[Fraction(0)],
        primal_residual=[Fraction(1), Fraction(0), Fraction(0)],
        dual_witness=[Fraction(1), Fraction(1), Fraction(0)],
        reported_value=Fraction(1),
    )
    assert off_face == Fraction(1)


def test_end_to_end_public_contract() -> None:
    value = evaluate_weighted_l1_quotient(
        boundary=[[(1, 1)], [(0, 1)]],
        weights=[(2, 1), (3, 1)],
        omega=[(1, 1), (2, 1)],
        alpha=[(1, 1)],
        primal_residual=[(0, 1), (2, 1)],
        dual_witness=[(0, 1), (3, 1)],
        reported_value=(6, 1),
    )
    assert value == Fraction(6)
    with pytest.raises(L1SeminormError, match="float refused") as caught:
        evaluate_weighted_l1_quotient(
            boundary=[[1], [0]],
            weights=[2, 3],
            omega=[1.0, 2],
            alpha=[1],
            primal_residual=[0, 2],
            dual_witness=[0, 3],
            reported_value=6,
        )
    assert caught.value.parameters["role"] == "omega[0]"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    dag = (root / "dag" / "derivation_dag.json").read_text(encoding="utf-8")
    lean = (root / "lean" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "L1-WDP-WINDOW-PHI1-GAMMA2" in dag
    assert "l1_gs001_replica_and_phi1_quotient_invariance" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:phi1:weighted-l1-quotient-certificate:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("zero weight admitted", "if weight <= 0:", "if weight < 0:"),
    ("residual check inverted", "if residual[index] != expected:", "if residual[index] == expected:"),
    ("orthogonality inverted", "if pairing != 0:", "if pairing == 0:"),
    ("dual ball opened at equality", "if abs(witness) > weights[index]:", "if abs(witness) >= weights[index]:"),
    ("repair sign flipped", "expected = omega[index] - repair", "expected = omega[index] + repair"),
    ("weights dropped from the cost", "total += weight * abs(value)", "total += abs(value)"),
    ("reported value unchecked", "if primal != dual or reported != primal:", "if primal != dual and reported == primal:"),
    (
        "float admitted as a binary fraction",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(value)\n    if False:",
    ),
    (
        "boolean admitted as an integer",
        "if isinstance(value, bool):",
        "if isinstance(value, bool):\n        return Fraction(int(value))\n    if False:",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module.__dict__


def _oracle(namespace: dict[str, object]) -> bool:
    evaluate = namespace["evaluate_weighted_l1_quotient"]
    error_type = namespace["L1SeminormError"]
    if not callable(evaluate) or not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    error = error_type
    try:
        value = evaluate(
            boundary=[[1], [0]],
            weights=[2, 3],
            omega=[1, 2],
            alpha=[1],
            primal_residual=[0, 2],
            dual_witness=[0, 3],
            reported_value=6,
        )
    except error:
        return False
    if value != Fraction(6):
        return False
    probes = (
        dict(boundary=[[1], [0]], weights=[2, 0], omega=[1, 2], alpha=[1], primal_residual=[0, 2], dual_witness=[0, 0], reported_value=0),
        dict(boundary=[[1.0], [0]], weights=[2, 3], omega=[1, 2], alpha=[1], primal_residual=[0, 2], dual_witness=[0, 3], reported_value=6),
        dict(boundary=[[True], [0]], weights=[2, 3], omega=[1, 2], alpha=[1], primal_residual=[0, 2], dual_witness=[0, 3], reported_value=6),
        dict(boundary=[[1], [0]], weights=[2, 3], omega=[1, 2], alpha=[1], primal_residual=[0, 2], dual_witness=[0, 3], reported_value=7),
        dict(boundary=[[1], [0]], weights=[2, 3], omega=[1, 2], alpha=[1], primal_residual=[0, 2], dual_witness=[2, 3], reported_value=8),
    )
    for probe in probes:
        try:
            evaluate(**probe)
        except error:
            continue
        return False
    return True


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_l1_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_l1_{index}"
            loaded.append(module_name)
            try:
                namespace = _load_source(source.replace(old, new, 1), module_name)
                survived = _oracle(namespace)
            except Exception:
                survived = False
            assert survived is False, name
            killed += 1
        assert killed == len(_MUTANTS)
        assert f"Mutation-Kills: {killed} non-equivalent" in source
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
