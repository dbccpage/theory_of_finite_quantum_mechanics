"""Exact regression and adversarial controls for norm/dual CHSH witnesses."""

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import sys

import pytest


_path = Path(__file__).resolve().parents[1] / "src/qm/chsh_norm_admission.py"
_spec = importlib.util.spec_from_file_location("chsh_norm_admission_replay", _path)
bell = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = bell
_spec.loader.exec_module(bell)


def test_exact_quadratic_field_arithmetic_and_order():
    r = bell.ROOT_TWO
    assert r * r == 2
    assert 1 < r < Q(3, 2)
    assert Q(7, 5) < r < Q(10, 7)
    assert r / r == 1
    assert 1 / r == r / 2
    assert (1 + r) * (r - 1) == 1
    assert -Q(3, 2) < -r < -1
    assert abs(1 - r) == r - 1
    with pytest.raises(ZeroDivisionError):
        r / 0


@pytest.mark.parametrize("value", [True, 0.5, "1/2"])
def test_inexact_or_ambiguous_input_is_refused(value):
    with pytest.raises(TypeError):
        bell.Qsqrt2(value)
    with pytest.raises(TypeError):
        bell.behavior_from_correlations([value, 0, 0, 0])


@pytest.mark.parametrize("norm,states,effects,expected", [
    ("l1", ((1, 0), (0, 1)), ((1, 1), (1, -1)), 4),
    ("linfty", ((1, 1), (1, -1)), ((1, 0), (0, 1)), 4),
    ("l2", ((1, 0), (0, 1)),
     ((bell.ROOT_TWO / 2, bell.ROOT_TWO / 2),
      (bell.ROOT_TWO / 2, -bell.ROOT_TWO / 2)), 2 * bell.ROOT_TWO),
])
def test_norm_dual_witnesses_and_probability_tables(norm, states, effects, expected):
    correlations = bell.norm_dual_correlations(norm, states, effects)
    assert bell.chsh(correlations) == expected
    assert bell.chsh(correlations) * bell.chsh(correlations) == (8 if norm == "l2" else 16)
    behavior = bell.behavior_from_correlations(correlations)
    assert bell.behavior_correlations(behavior) == correlations
    for row in behavior:
        assert sum(row) == 1
        assert row[0] + row[1] == Q(1, 2)
        assert row[0] + row[2] == Q(1, 2)
    if norm != "l2":
        assert behavior[:3] == ((Q(1, 2), 0, 0, Q(1, 2)),) * 3
        assert behavior[3] == (0, Q(1, 2), Q(1, 2), 0)


def test_l2_does_not_admit_the_l1_dual_effects():
    with pytest.raises(ValueError, match="outside the l2"):
        bell.norm_dual_correlations("l2", ((1, 0), (0, 1)), ((1, 1), (1, -1)))
    # Testing effects against the primal infinity ball would incorrectly pass.
    with pytest.raises(ValueError, match="outside the l1"):
        bell.norm_dual_correlations("linfty", ((1, 0), (0, 1)), ((1, 1), (1, -1)))
    with pytest.raises(ValueError, match="outside the l1"):
        bell.norm_dual_correlations("l1", ((1, 1), (0, 1)), ((1, 0), (0, 1)))


def test_parallelogram_is_a_real_admission_not_a_norm_label():
    e1, e2 = (1, 0), (0, 1)
    assert bell.parallelogram_defect(e1, e2, "l1") == 4
    assert bell.parallelogram_defect(e1, e2, "linfty") == -2
    bell.require_parallelogram(e1, e2, "l2")
    for norm in ("l1", "linfty"):
        with pytest.raises(ValueError, match="parallelogram"):
            bell.require_parallelogram(e1, e2, norm)
    # A non-basis pair also checks actual squared norm arithmetic.
    bell.require_parallelogram((Q(3, 5), Q(4, 5)), (bell.ROOT_TWO, -1), "l2")


def test_all_local_vertices_and_positive_mixtures_obey_two():
    values = []
    for i, assignment in enumerate(bell.LOCAL_ASSIGNMENTS):
        correlations = bell.deterministic_correlations(assignment)
        value = bell.chsh(correlations)
        values.append(value)
        assert abs(value) == 2
        behavior = bell.local_mixture([int(i == j) for j in range(16)])
        assert bell.behavior_correlations(behavior) == correlations
    assert values.count(2) == values.count(-2) == 8
    for weights in ([Q(1, 16)] * 16, [Q(i, 136) for i in range(1, 17)]):
        actual = bell.chsh(bell.behavior_correlations(bell.local_mixture(weights)))
        assert actual == sum(w * v for w, v in zip(weights, values))
        assert abs(actual) <= 2


def test_signed_global_pr_witness_is_refused_by_positive_joint_interface():
    # Signed extension w=(1+CHSH(lambda))/16 reproduces PR correlations but
    # its eight negative entries violate exactly the admission under test.
    weights = [(1 + bell.chsh(bell.deterministic_correlations(a)).a) / 16
               for a in bell.LOCAL_ASSIGNMENTS]
    assert sum(weights) == 1
    assert weights.count(Q(-1, 16)) == 8
    assert sum(w * bell.chsh(bell.deterministic_correlations(a))
               for w, a in zip(weights, bell.LOCAL_ASSIGNMENTS)) == 4
    with pytest.raises(ValueError, match="nonnegative"):
        bell.local_mixture(weights)
    with pytest.raises(ValueError, match="normalized"):
        bell.local_mixture([Q(1, 8)] * 16)


def test_invalid_probabilities_normalization_and_signalling_are_refused():
    for correlation in (Q(3, 2), -bell.ROOT_TWO):
        with pytest.raises(ValueError, match="correlations"):
            bell.behavior_from_correlations([correlation, 0, 0, 0])
    uniform = [[Q(1, 4)] * 4 for _ in range(4)]
    negative = [row[:] for row in uniform]
    negative[0] = [Q(-1, 4), Q(3, 4), Q(1, 4), Q(1, 4)]
    with pytest.raises(ValueError, match="probabilities"):
        bell.validate_behavior(negative)
    unnormalized = [row[:] for row in uniform]
    unnormalized[0][0] = Q(1, 2)
    with pytest.raises(ValueError, match="normalized"):
        bell.validate_behavior(unnormalized)
    signalling = [row[:] for row in uniform]
    signalling[0] = [Q(1, 2), Q(1, 2), 0, 0]
    with pytest.raises(ValueError, match="Alice marginal"):
        bell.validate_behavior(signalling)
    signalling[0] = [Q(1, 2), 0, Q(1, 2), 0]
    with pytest.raises(ValueError, match="Bob marginal"):
        bell.validate_behavior(signalling)


def test_replay_is_json_ready_exact_and_scoped():
    receipt = bell.replay()
    assert json.loads(json.dumps(receipt)) == receipt
    assert receipt["schema"] == "chsh-norm-admission/1"
    assert receipt["witnesses"]["l2"]["chsh"] == {"rational": "0", "sqrt2_coefficient": "2"}
    assert receipt["witnesses"]["l1"]["chsh"] == {"rational": "4", "sqrt2_coefficient": "0"}
    assert "no physical reconstruction" in receipt["scope"]
