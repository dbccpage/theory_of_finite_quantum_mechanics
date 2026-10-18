"""Native Majorana adapter boundaries; these mocked checks do not test Rust math."""

from fractions import Fraction

import kitaev_chain_exact as kitaev
import majorana_braid_exact as braid
import pytest

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathRefusal,
    decode_rational,
)


def test_matrix_owns_immutable_exact_values_after_input_alias_mutation():
    rows = [[1, 0], [0, 1]]
    matrix = braid.ExactSignedPermutationMatrix(2, rows)
    original_hash = hash(matrix)
    rows[0][0] = 1.0
    rows[1][1] = True
    rows[0].append(2)
    assert matrix.data == ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    assert all(isinstance(value, Fraction) for row in matrix.data for value in row)
    assert hash(matrix) == original_hash
    assert braid._matrix_wire(matrix) == {
        "rows": 2,
        "cols": 2,
        "data": [["1", "0"], ["0", "1"]],
    }


def test_circuit_relays_word_and_uses_native_matrix(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append((action, payload))
        return {"matrix": {"rows": 2, "cols": 2, "data": [["0", "-1"], ["1", "0"]]}}

    monkeypatch.setattr(braid, "call_native", native)
    circuit = braid.MajoranaBraidCircuit(2).append(1, inverse=True)
    assert circuit.evaluate_matrix().data == (
        (Fraction(0), Fraction(-1)),
        (Fraction(1), Fraction(0)),
    )
    assert calls == [("majorana_braid_action", {"num_modes": 2, "steps": [(1, True)]})]


def test_arbitrary_rational_matrix_uses_generic_native_owner(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append((action, payload))
        return {"value": "-3/14"}

    monkeypatch.setattr(braid, "call_native", native)
    matrix = braid.ExactSignedPermutationMatrix(
        2, ((Fraction(1, 2), Fraction(0)), (Fraction(0), Fraction(-3, 7)))
    )
    assert matrix.determinant() == Fraction(-3, 14)
    assert calls == [
        (
            "math_rational_matrix",
            {
                "operation": "determinant",
                "matrix": {"rows": 2, "cols": 2, "data": [["1/2", "0"], ["0", "-3/7"]]},
            },
        )
    ]


def test_kitaev_relays_exact_parameters_and_bilinear_generator(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append((action, payload))
        if payload.get("operation") == "bilinear":
            return {"commutator": ["-2", 2]}
        return {
            "terms": [
                [1, 2, "1/10"],
                [1, 4, "1/66"],
                [2, 3, "-43/66"],
                [3, 4, "1/10"],
                [3, 6, "1/66"],
                [4, 5, "-43/66"],
                [5, 6, "1/10"],
            ],
            "constant_energy": "3/10",
        }

    monkeypatch.setattr(kitaev, "call_native", native)
    wire = kitaev.KitaevChainExact(3, Fraction(2, 3), Fraction(-1, 5), Fraction(7, 11))
    assert wire.terms()[kitaev.MajoranaBilinear(1, 4)] == Fraction(1, 66)
    assert calls[0] == (
        "majorana_kitaev_wire",
        {"num_sites": 3, "t": "2/3", "mu": "-1/5", "delta": "7/11"},
    )
    assert kitaev.MajoranaBilinear(2, 5).commutator_with_mode(5) == (Fraction(-2), 2)
    assert calls[-1] == (
        "majorana_kitaev_wire",
        {"operation": "bilinear", "a": 2, "b": 5, "mode": 5},
    )


def test_native_failure_propagates_without_python_math_fallback(monkeypatch):
    class Unavailable(RuntimeError):
        pass

    def fail(*_args, **_kwargs):
        raise Unavailable("native unavailable")

    monkeypatch.setattr(braid, "call_native", fail)
    monkeypatch.setattr(kitaev, "call_native", fail)
    with pytest.raises(Unavailable, match="native unavailable"):
        braid.MajoranaBraidCircuit(3).append(1).evaluate_matrix()
    with pytest.raises(Unavailable, match="native unavailable"):
        braid.ExactSignedPermutationMatrix(2, ((0, 0), (0, 0))).determinant()
    with pytest.raises(Unavailable, match="native unavailable"):
        kitaev.KitaevChainExact(2)


def test_boolean_indices_and_inexact_parameters_rejected_before_native_call(monkeypatch):
    def unexpected(*_args, **_kwargs):
        raise RuntimeError("native must not receive invalid values")

    monkeypatch.setattr(braid, "call_native", unexpected)
    monkeypatch.setattr(kitaev, "call_native", unexpected)
    with pytest.raises(ValueError):
        braid.MajoranaBraidGenerator(True, 1)
    with pytest.raises(ValueError):
        braid.MajoranaBraidCircuit(4).append(True)
    with pytest.raises(TypeError):
        kitaev.KitaevChainExact(2, t=1.0)
    with pytest.raises(ValueError):
        kitaev.MajoranaBilinear(1, 2).commutator_with_mode(True)


@pytest.mark.parametrize("coefficient", [1.0, True, "1/1", " 1", "0.5", "-0"])
@pytest.mark.parametrize("operation", ["matrix", "determinant"])
def test_native_braid_coefficients_require_canonical_strings(monkeypatch, coefficient, operation):
    def native(_action, _payload):
        if operation == "matrix":
            return {"matrix": {"rows": 2, "cols": 2, "data": [[coefficient, "0"], ["0", "1"]]}}
        return {"value": coefficient}

    monkeypatch.setattr(braid, "call_native", native)
    with pytest.raises(ValueError, match="canonical rational string"):
        if operation == "matrix":
            braid.MajoranaBraidCircuit(2).evaluate_matrix()
        else:
            braid.ExactSignedPermutationMatrix(2, ((1, 0), (0, 1))).determinant()


@pytest.mark.parametrize("coefficient", [1.0, True, "1/1", " 1", "0.5", "-0"])
@pytest.mark.parametrize("field", ["term", "constant", "mode", "bilinear"])
def test_native_kitaev_coefficients_require_canonical_strings(monkeypatch, coefficient, field):
    def native(_action, payload):
        if payload.get("operation") == "bilinear":
            return {"commutator": [coefficient, 2]}
        if "mode" in payload:
            return {"mode_commutator": [[3, coefficient]]}
        return {
            "terms": [[2, 3, coefficient if field == "term" else "-1"]],
            "constant_energy": coefficient if field == "constant" else "0",
        }

    monkeypatch.setattr(kitaev, "call_native", native)
    with pytest.raises(ValueError, match="canonical rational string"):
        if field == "bilinear":
            kitaev.MajoranaBilinear(1, 2).commutator_with_mode(2)
        else:
            wire = kitaev.KitaevChainExact(2)
            if field == "mode":
                wire.commutator_with_mode(2)


@pytest.mark.parametrize("token", ["0", "-11", "7/13", "-3/14"])
def test_native_rational_decoder_accepts_canonical_integer_and_fraction_tokens(token):
    assert decode_rational(token) == Fraction(token)


@pytest.mark.parametrize("token", [1.0, True, 1, "1/1", " 1", "0.5", "-0", "1/0", "invalid"])
def test_native_rational_refusal_retains_original_coefficient(token):
    with pytest.raises(NativeMathRefusal, match="canonical rational string") as refused:
        decode_rational(token)
    assert refused.value.code == "NATIVE_MATH_RATIONAL"
    assert refused.value.outcome is token
