"""Selected native-framed P.17 certificates, with adversarial boundaries."""
from __future__ import annotations

import copy
import os
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.monorepo

PAPER = next(p for p in Path(__file__).resolve().parents if (p / "witnessed_difference_programme.md").exists())
sys.path.insert(0, str(PAPER))
from scripts import check_causal_execution as causal  # noqa: E402
from scripts import check_causal_three_cells as cells  # noqa: E402


@pytest.fixture(scope="module")
def native():
    names = ("WDP_CAUSAL_NATIVE_BIN", "WDP_CAUSAL_BUILD_RECEIPT", "WDP_CAUSAL_SOURCE_ROOT")
    if not all(os.environ.get(n) for n in names):
        pytest.skip("fresh native integration requires explicit binary, build receipt and source root")
    return causal.NativeOwner(*(Path(os.environ[n]) for n in names))


@pytest.fixture(scope="module")
def problem():
    return causal.read_json(PAPER / "code/causal_certificates/antichain_problem.json")


@pytest.fixture(scope="module")
def execution(problem, native):
    return causal.produce_certificate(problem, native)


def request(source, target, target_order):
    return {"schema": "wdp-causal-three-request-v1", "source_order": [0, 1, 2, 3],
            "target_order": target_order, "source_word": source, "target_word": target}


@pytest.mark.parametrize("kind,before,after,target", [
    ("backtrack", [0, 0], [], [0, 1, 2, 3]),
    ("backtrack", [], [1, 1], [0, 1, 2, 3]),
    ("square", [0, 2], [2, 0], [1, 0, 3, 2]),
    ("braid", [0, 1, 0], [1, 0, 1], [2, 1, 0, 3]),
])
def test_local_three_witnesses(kind, before, after, target, problem, execution, native):
    boundary = request(before, after, target)
    moves = [{"kind": kind, "offset": 0, "before": before, "after": after}]
    cert = cells.assemble_three(problem, boundary, moves, execution)
    assert cells.verify_three(problem, boundary, cert, native)["fresh_native_replay"] is True
    assert cert["proofs"][0]["source_history_sha256"] == cert["proofs"][1]["source_history_sha256"]
    assert cert["proofs"][0]["target_history_sha256"] == cert["proofs"][1]["target_history_sha256"]


def test_whiskered_braid_retains_prefix_and_suffix(problem, execution, native):
    source_word = [2, 2, 0, 1, 0, 2, 2]
    target_word = [2, 2, 1, 0, 1, 2, 2]
    boundary = request(source_word, target_word, [2, 1, 0, 3])
    cert = cells.assemble_three(problem, boundary,
        [{"kind": "braid", "offset": 2, "before": [0, 1, 0], "after": [1, 0, 1]}], execution)
    assert cells.verify_three(problem, boundary, cert, native)["replacements"] == 1


def test_braid_comparable_events_refuses(problem, native):
    problem = copy.deepcopy(problem)
    problem["events"][1]["predecessors"] = ["birth-b"]
    execution = causal.produce_certificate(problem, native)
    with pytest.raises(causal.CertificateRefusal, match="comparable"):
        cells.assemble_three(problem, request([0, 1, 0], [1, 0, 1], [2, 1, 0, 3]),
            [{"kind": "braid", "offset": 0, "before": [0, 1, 0], "after": [1, 0, 1]}], execution)


@pytest.mark.parametrize("offset", [1, 99, True, -1])
def test_incorrect_offset_refuses(offset, problem, execution):
    with pytest.raises(causal.CertificateRefusal):
        cells.assemble_three(problem, request([0, 1, 0], [1, 0, 1], [2, 1, 0, 3]),
            [{"kind": "braid", "offset": offset, "before": [0, 1, 0], "after": [1, 0, 1]}], execution)


def test_changed_boundary_with_same_endpoint_packet_refuses(problem, execution, native):
    boundary = request([0, 1, 0], [1, 0, 1], [2, 1, 0, 3])
    cert = cells.assemble_three(problem, boundary,
        [{"kind": "braid", "offset": 0, "before": [0, 1, 0], "after": [1, 0, 1]}], execution)
    cert["target_history_sha256"] = cert["source_history_sha256"]
    with pytest.raises(causal.CertificateRefusal, match="differs"):
        cells.verify_three(problem, boundary, cert, native)
    changed = copy.deepcopy(boundary)
    changed["target_order"] = [0, 1, 2, 3]
    with pytest.raises(causal.CertificateRefusal, match="boundary history"):
        cells.assemble_three(problem, changed, cert["replacements"], execution)


def test_corrupted_intermediate_native_state_refuses(problem, execution, native):
    boundary = request([0, 0], [], [0, 1, 2, 3])
    cert = cells.assemble_three(problem, boundary,
        [{"kind": "backtrack", "offset": 0, "before": [0, 0], "after": []}], copy.deepcopy(execution))
    cert["execution"]["histories"][1]["native"]["states"][2]["r"][0] = "500"
    with pytest.raises(causal.CertificateRefusal, match="fresh native replay"):
        cells.verify_three(problem, boundary, cert, native)


def test_distinct_three_certificates_remain_distinct(problem, execution, native):
    boundary = request([], [], [0, 1, 2, 3])
    empty = cells.assemble_three(problem, boundary, [], execution)
    loop = cells.assemble_three(problem, boundary, [
        {"kind": "backtrack", "offset": 0, "before": [], "after": [0, 0]},
        {"kind": "backtrack", "offset": 0, "before": [0, 0], "after": []}], execution)
    assert cells.verify_three(problem, boundary, empty, native)["status"] == "PASS"
    assert cells.verify_three(problem, boundary, loop, native)["status"] == "PASS"
    assert causal.digest(empty) != causal.digest(loop)


@pytest.mark.parametrize("size", [0, 1])
def test_empty_and_single_event_intervals(size, problem, native):
    p = copy.deepcopy(problem)
    p["events"] = p["events"][:size]
    execution = causal.produce_certificate(p, native)
    order = list(range(size))
    boundary = {"schema": "wdp-causal-three-request-v1", "source_order": order,
                "target_order": order, "source_word": [], "target_word": []}
    cert = cells.assemble_three(p, boundary, [], execution)
    assert cells.verify_three(p, boundary, cert, native)["status"] == "PASS"
    assert execution["price_potential"]["0"] == [0, 0, 0, 0]
