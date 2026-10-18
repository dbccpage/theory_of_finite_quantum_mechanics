"""Integration checks for paper carriers using the canonical native math host."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from importlib import import_module
from unittest.mock import patch

import pytest

MODULE_ROOT = "omega_engine_atlas.coda_atlas.F004_papers.009_ms_majorana.code"
qmatrix = import_module(f"{MODULE_ROOT}.qmatrix")
exact_solve = import_module(f"{MODULE_ROOT}.exact_solve")
hpt = import_module(f"{MODULE_ROOT}.homological_perturbation")
gf2 = import_module(f"{MODULE_ROOT}.majorana.core.gf2_matrix")
gf2_schema = import_module(f"{MODULE_ROOT}.majorana.core.gf2_schema")


def test_rational_matrix_exact_native_arithmetic_and_image_witness():
    matrix = qmatrix.QMatrix.from_row_major(2, 3, ["1/3", 2, -1, 0, 0, 0])
    assert matrix.rank() == 1
    assert matrix.transpose().shape == (3, 2)
    witness = exact_solve.solve(matrix, ["2/3", 0])
    assert witness == [Fraction(2), 0, 0]
    assert matrix.matmul(qmatrix.QMatrix.from_row_major(3, 1, witness)).data == [
        [Fraction(2, 3)],
        [0],
    ]
    assert exact_solve.solve(matrix, [0, 1]) is None
    assert not exact_solve.in_image(matrix, [0, 1])


def test_native_rational_operations_preserve_empty_dimensions():
    matrix = qmatrix.QMatrix.zero(0, 3)
    assert matrix.transpose().shape == (3, 0)
    assert exact_solve.solve(matrix, []) == [0, 0, 0]
    assert qmatrix.QMatrix.zero(2, 0).matmul(matrix).data == [[0, 0, 0], [0, 0, 0]]
    assert hpt.ExactMatrix.zero(0, 0).try_invert() == hpt.ExactMatrix.identity(0)


def test_exact_matrix_inverse_and_singular_result():
    matrix = hpt.ExactMatrix.from_rows([["1/2", 1], [1, 0]])
    inverse = matrix.try_invert()
    assert inverse is not None
    assert matrix.matmul(inverse) == hpt.ExactMatrix.identity(2)
    assert (matrix + -matrix).is_zero()
    assert hpt.ExactMatrix.from_rows([[1, 1], [1, 1]]).try_invert() is None


def test_gf2_native_solver_and_empty_kernel():
    matrix = gf2.GF2Matrix([[1, 0], [1, 1], [0, 1]])
    reduced, pivots = matrix.rref()
    assert pivots == [0, 1]
    assert reduced.data == [[1, 0], [0, 1], [0, 0]]
    assert matrix.mat_vec_mul([1, 1]) == [1, 0, 1]
    assert matrix.solve([1, 0, 1]) == [1, 1]
    assert matrix.solve([1, 1, 1]) is None
    assert gf2.GF2Matrix([], cols=2).kernel_basis() == [[1, 0], [0, 1]]
    assert gf2.GF2Matrix([], cols=2).transpose().shape() == (2, 0)
    assert gf2.GF2Matrix([], cols=2).to_basic_matrix().shape() == (0, 2)


def test_hpl_native_identity_transfer_and_state_digest():
    contraction = hpt.identity_contraction((2, 1, 0), [[1, -1]], [])
    assert hpt.verify_normalized(contraction).is_normalized
    perturbation = hpt.DifferentialPerturbation.from_matrices((2, 1, 0), [[3, -1]], [])
    receipt = hpt.transfer_perturbation(contraction, perturbation)
    assert receipt.success
    assert receipt.delta_D0.data == ((3, -1),)
    assert receipt.reduced_square_zero is True
    assert receipt.evidence_sha256 == receipt.digest()
    assert receipt.extra["native_outcome"]["success"] is True
    assert receipt.extra["native_outcome"]["result"]["success"] is True
    assert replace(receipt, extra={}).digest() != receipt.evidence_sha256
    changed_target = replace(contraction, dD0=hpt.ExactMatrix.zero(1, 2))
    assert hpt._stable_digest_of_contraction(changed_target) != receipt.contraction_digest


def test_hpl_native_transfer_sign_for_nontrivial_retract():
    contraction = hpt.NormalizedContraction.from_matrices(
        C_dims=(2, 2, 0),
        D_dims=(1, 1, 0),
        dC0=[[0, 0], [0, 1]],
        dC1=[],
        dD0=[[0]],
        dD1=[],
        i0=[[1], [0]],
        i1=[[1], [0]],
        i2=[],
        r0=[[1, 0]],
        r1=[[1, 0]],
        r2=[],
        h1=[[0, 0], [0, 1]],
        h2=[[], []],
    )
    perturbation = hpt.DifferentialPerturbation.from_matrices((2, 2, 0), [[0, 1], [1, 0]], [])
    receipt = hpt.transfer_perturbation(contraction, perturbation)
    assert receipt.success
    assert receipt.delta_D0.data == ((-1,),)


def test_hpl_native_singular_resolvent_is_an_unsuccessful_receipt():
    contraction = hpt.NormalizedContraction.from_matrices(
        C_dims=(1, 1, 0),
        D_dims=(0, 0, 0),
        dC0=[[1]],
        dC1=[],
        dD0=[],
        dD1=[],
        i0=[[]],
        i1=[[]],
        i2=[],
        r0=[],
        r1=[],
        r2=[],
        h1=[[1]],
        h2=[[]],
    )
    assert hpt.verify_normalized(contraction).is_normalized
    perturbation = hpt.DifferentialPerturbation.from_matrices((1, 1, 0), [[-1]], [])
    receipt = hpt.transfer_perturbation(contraction, perturbation)
    assert not receipt.success
    assert not receipt.invertibility
    assert "singular" in receipt.obstruction_reason
    assert receipt.evidence_sha256 == receipt.digest()


def test_transport_refusal_does_not_fall_back_to_python_math():
    refusal = RuntimeError("native transport sentinel")
    matrix = qmatrix.QMatrix.identity(1)
    with patch.object(qmatrix, "call_native", side_effect=refusal):
        with pytest.raises(RuntimeError, match="native transport sentinel"):
            matrix.rank()
    with patch.object(gf2, "call_native", side_effect=refusal):
        with pytest.raises(RuntimeError, match="native transport sentinel"):
            gf2.GF2Matrix([[1]]).kernel_basis()
    with patch.object(hpt, "call_native", side_effect=refusal):
        with pytest.raises(RuntimeError, match="native transport sentinel"):
            hpt.verify_normalized(hpt.identity_contraction((1, 0, 0), [], []))


def test_absent_native_contraction_report_is_a_typed_refusal():
    outcome = {"report": None, "obstruction_reason": "source_differential_not_square_zero"}
    with patch.object(hpt, "call_native", return_value=outcome):
        with pytest.raises(hpt.NativeMathRefusal) as caught:
            hpt.verify_normalized(hpt.identity_contraction((1, 0, 0), [], []))
    assert caught.value.code == "NATIVE_CONTRACTION_REFUSED"
    assert caught.value.outcome == outcome


@pytest.mark.parametrize("value", [True, 0.25])
def test_approximate_and_boolean_rationals_are_refused(value):
    with pytest.raises(TypeError):
        qmatrix.QMatrix.from_row_major(1, 1, [value])
    with pytest.raises(TypeError):
        hpt.ExactMatrix(1, 1, ((value,),))
    with pytest.raises(TypeError):
        gf2.GF2Matrix([[value]])


@pytest.mark.parametrize("cols", [True, 1.0, -1])
def test_gf2_explicit_invalid_dimension_is_refused(cols):
    with pytest.raises(ValueError):
        gf2.GF2Matrix([[1]], cols=cols)


def test_hpl_perturbation_boolean_dimension_is_refused():
    with pytest.raises(ValueError):
        hpt.DifferentialPerturbation.from_matrices((True, 1, 0), [[1]], [])
    with pytest.raises(ValueError):
        hpt.ExactMatrix.from_rows([[1]], expected_cols=True)


@pytest.mark.parametrize("matrix_type", [qmatrix.QMatrix, hpt.ExactMatrix])
def test_native_matrix_output_requires_canonical_rational_tokens(matrix_type):
    with pytest.raises(hpt.NativeMathRefusal):
        matrix_type._from_wire({"rows": 1, "cols": 1, "data": [["1/1"]]})


def test_native_solve_output_requires_canonical_rational_tokens():
    with patch.object(exact_solve, "call_native", return_value={"solution": ["1/1"]}):
        with pytest.raises(hpt.NativeMathRefusal):
            exact_solve.solve(qmatrix.QMatrix.identity(1), [1])


@pytest.mark.parametrize("value", [True, False, 0.75, 1.0, Fraction(1, 2), "1"])
def test_gf2_schema_cannot_hide_invalid_numeric_inputs_before_native_matrix(value):
    with pytest.raises(TypeError):
        gf2_schema.normalize_vector([value])
    with pytest.raises(TypeError):
        gf2_schema.normalize_matrix([[value]])


def test_gf2_signed_integer_normalization_preserves_exact_native_solving():
    assert gf2_schema.normalize_vector([-3, -2, -1, 0, 1, 2, 3]) == [1, 0, 1, 0, 1, 0, 1]
    normalized = gf2_schema.normalize_matrix([[-1, 2], [3, -1]])
    assert normalized == [[1, 0], [1, 1]]
    assert gf2.GF2Matrix(normalized).solve(gf2_schema.normalize_vector([-1, 2])) == [1, 1]
