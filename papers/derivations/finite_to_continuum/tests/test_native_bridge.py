"""Real native receipts, exact arithmetic, and separating invalid presentations."""

from copy import deepcopy
from types import MappingProxyType

import pytest

from omega_engine_operations.domain.rop.result import Err, Ok
from omega_engine_operating_system.adapters.rust_host.ffi import _verify_input_binding
from omega_engine_projects.finite_to_continuum.code.native_bridge import evaluate_finite_bridge


def outcome(request):
    result = evaluate_finite_bridge(request)
    assert isinstance(result, Ok), result
    return result.value


def evidence(request):
    receipt = outcome(request)
    assert receipt["success"] is True, receipt
    assert receipt["authority_effect"] == "None"
    assert receipt["result"]["provenance"] == {
        "realizes": None,
        "genesis_effect": "None",
        "genesis_register_access": "not_performed",
        "model_evidence_only": True,
    }
    return receipt["result"]["evidence"]


def test_cyclic_embedding_and_input_binding():
    request = {"kind": "cyclic_embedding", "order": 3, "residue": 2, "refinement_order": 12}
    assert evidence(request) == {
        "turn": "2/3",
        "refined_residue": 8,
        "refined_turn": "2/3",
        "commutes": True,
    }
    receipt = outcome(request)
    changed = dict(request, residue=1)
    assert isinstance(_verify_input_binding("continuum_evaluate", changed, receipt), Err)
    assert outcome(dict(request, refinement_order=8))["success"] is False
    assert isinstance(evaluate_finite_bridge(MappingProxyType(request)), Err)


@pytest.mark.parametrize("payload", [None, 1, True, [], "untyped"])
def test_malformed_outer_request_returns_a_native_refusal(payload):
    assert outcome(payload)["success"] is False


def test_executed_haar_sum_separates_aliasing_from_recovery():
    request = {
        "kind": "haar_polynomial",
        "order": 4,
        "terms": [{"frequency": 4, "coefficient": "1"}],
    }
    early = evidence(request)
    assert early["finite_average"] == "1" and early["haar_integral"] == "0"
    assert early["observed_recovery"] is False and early["alias_free"] is False
    late = evidence(dict(request, order=8))
    assert late["finite_average"] == "0" and late["observed_recovery"] is True


@pytest.mark.parametrize("mutant", [True, False, 1.0, "1"])
def test_frequency_rejects_noninteger_wire_types(mutant):
    receipt = outcome(
        {
            "kind": "haar_polynomial",
            "order": 8,
            "terms": [{"frequency": mutant, "coefficient": "1"}],
        }
    )
    assert receipt["success"] is False


@pytest.mark.parametrize("coefficient", [1, True, 0.5, "0.5", "2/4", "1/0"])
def test_coefficients_require_canonical_exact_rationals(coefficient):
    assert (
        outcome(
            {
                "kind": "haar_polynomial",
                "order": 8,
                "terms": [{"frequency": 1, "coefficient": coefficient}],
            }
        )["success"]
        is False
    )


def test_duplicate_frequency_is_not_silently_overwritten():
    term = {"frequency": 1, "coefficient": "1"}
    assert (
        outcome({"kind": "haar_polynomial", "order": 8, "terms": [term, term]})["success"] is False
    )


def test_lipschitz_prefix_is_bound_to_samples_and_seams():
    request = {
        "kind": "lipschitz_samples",
        "lipschitz_constant": "1",
        "samples": [["0"], ["0", "1/2"], ["0", "1/4", "1/2", "1/4"]],
    }
    proof = evidence(request)
    assert proof["enclosures"][-1] == {
        "order": 4,
        "average": "1/4",
        "radius": "1/8",
        "lower": "1/8",
        "upper": "3/8",
    }
    assert proof["infinite_family_verified"] is False
    changed = deepcopy(request)
    changed["samples"][2][2] = "0"
    assert outcome(changed)["success"] is False
    assert outcome(dict(request, samples=[]))["success"] is False
    assert outcome(dict(request, lipschitz_constant="1/2"))["success"] is False


def test_graph_symmetry_checks_actual_adjacency():
    request = {
        "kind": "graph_symmetry",
        "nodes": ["a", "b", "c"],
        "edges": [[0, 1], [1, 2], [2, 0]],
        "image": [1, 2, 0],
    }
    assert evidence(request)["edge_image"] == [1, 2, 0]
    for image in ([0, 0, 2], [1, 0, 2], [0, 1, 3], []):
        assert outcome(dict(request, image=image))["success"] is False


def test_cochain_and_difference_operator_symmetry():
    request = {
        "kind": "cochain_symmetry",
        "dimensions": [2, 1, 0],
        "d0": ["-1", "1"],
        "d1": [],
        "maps": [
            {"image": [1, 0], "signs": [1, 1]},
            {"image": [0], "signs": [-1]},
            {"image": [], "signs": []},
        ],
        "difference_operator": ["1", "-1", "-1", "1"],
    }
    assert evidence(request)["difference_operator_verified"] is True
    bad = deepcopy(request)
    bad["maps"][1]["signs"] = [1]
    assert outcome(bad)["success"] is False
    assert outcome(dict(request, difference_operator=["1", "0", "0", "2"]))["success"] is False
    bad = dict(request, dimensions=[2, 1, 1], d1=["1"])
    assert outcome(bad)["success"] is False  # d1*d0 != 0, before any symmetry claim.


def test_no_caller_supplied_authority_or_unknown_attestation():
    request = {"kind": "graph_symmetry", "nodes": ["a"], "edges": [], "image": [0]}
    assert outcome(dict(request, verified=True))["success"] is False
    assert outcome(dict(request, authority_effect="Admit"))["success"] is False
