"""Native integration tests; require explicitly configured binary/build/source."""
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
from scripts.check_ideal_swaps import minimum_swap_receipt  # noqa: E402


@pytest.fixture(scope="module")
def native():
    names = ("WDP_CAUSAL_NATIVE_BIN", "WDP_CAUSAL_BUILD_RECEIPT", "WDP_CAUSAL_SOURCE_ROOT")
    if not all(os.environ.get(n) for n in names):
        pytest.skip("fresh native integration requires explicit binary, build receipt and source root")
    return causal.NativeOwner(*(Path(os.environ[n]) for n in names))


@pytest.fixture(scope="module")
def problem():
    return causal.read_json(PAPER / "code/causal_certificates/five_edit_problem.json")


@pytest.fixture(scope="module")
def certificate(problem, native):
    return causal.produce_certificate(problem, native)


def test_five_native_edits_and_all_order_token_alignment(problem, certificate, native):
    result = causal.verify_certificate(problem, certificate, native)
    assert result["fresh_native_replay"] is True
    assert result["histories"] == 24
    histories = certificate["histories"]
    assert {step["kind"] for h in histories for step in h["native"]["changes"]} == {
        "add_term", "add_assertion", "fill", "remove", "identify"}
    assert {tuple(h["protected_total"]) for h in histories} == {(3, 1, 2, 2)}
    boundaries = [h["frames"][-1]["boundary"] for h in histories]
    assert all(causal.same(boundaries[0], boundary) for boundary in boundaries)
    assert len({tuple(h["frames"][3]["native_to_frame"]) for h in histories}) > 1


def test_valid_poset_with_impossible_remove_refuses(native):
    problem = {"schema": "wdp-causal-problem-v1", "initial": {"terms": ["t0"], "r": ["0"], "s": ["0"], "filled": []},
               "initial_tokens": ["origin"], "events": [{"tag": "impossible", "kind": "remove", "relation": "r",
                   "tokens": ["origin", "origin"], "predecessors": []}], "protected_prices": ["assertion_additions"]}
    assert minimum_swap_receipt([0], 0, 1, [0], [0]).inversion_count == 0
    with pytest.raises(causal.CertificateRefusal, match="native refusal"):
        causal.produce_certificate(problem, native)


@pytest.mark.parametrize("part", ["initial", "occurrence", "transition", "alignment", "boundary", "price", "omission", "authority"])
def test_changed_certificate_is_refused(problem, certificate, native, part):
    submitted = copy.deepcopy(certificate)
    history = submitted["histories"][0]
    if part == "initial":
        history["native"]["states"][0]["r"][0] = "3"
    elif part == "occurrence":
        history["occurrences"][0] = "different-birth"
    elif part == "transition":
        history["native"]["states"][-1]["s"][0] = "99"
    elif part == "alignment":
        history["frames"][1]["native_to_frame"] = [0, 1]
    elif part == "boundary":
        history["frames"][-1]["boundary"]["token_classes"][0] = ["forged"]
    elif part == "price":
        history["protected_total"][0] = 99
    elif part == "omission":
        submitted["histories"].pop()
    else:
        submitted["authority_effect"] = "Grant"
    before = causal.encoded(submitted)
    with pytest.raises(causal.CertificateRefusal, match="differs"):
        causal.verify_certificate(problem, submitted, native)
    assert causal.encoded(submitted) == before


def test_changed_problem_and_birth_precedence_refuse(problem, certificate, native):
    changed = copy.deepcopy(problem)
    changed["initial"]["r"] = ["3"]
    with pytest.raises(causal.CertificateRefusal, match="differs"):
        causal.verify_certificate(changed, certificate, native)
    changed = copy.deepcopy(problem)
    changed["events"][3]["predecessors"] = []
    with pytest.raises(causal.CertificateRefusal, match="birth-before-use"):
        causal.produce_certificate(changed, native)


def test_native_refusal_is_not_suppressed_by_another_legal_order(native):
    p = causal.read_json(PAPER / "code/causal_certificates/antichain_problem.json")
    p["events"] = [p["events"][3], {"tag": "remove", "kind": "remove", "relation": "r", "tokens": ["origin", "origin"], "predecessors": []}]
    with pytest.raises(causal.CertificateRefusal, match="native refusal"):
        causal.produce_certificate(p, native)


def test_nonzero_protected_fee_curl_refuses(native):
    p = causal.read_json(PAPER / "code/causal_certificates/antichain_problem.json")
    p["events"] = [p["events"][0], p["events"][3]]
    p["protected_prices"] = ["assertion_source_size_fee"]
    with pytest.raises(causal.CertificateRefusal, match="nonzero diamond curl"):
        causal.produce_certificate(p, native)


@pytest.mark.parametrize("value", [True, 1.0, "00", "1.0", "-0"])
def test_exact_boundary_refuses_noncanonical_counts(problem, value):
    p = copy.deepcopy(problem)
    p["initial"]["r"][0] = value
    with pytest.raises(causal.CertificateRefusal):
        causal.admit_problem(p)


def test_duplicate_birth_refuses(problem):
    p = copy.deepcopy(problem)
    p["events"][1]["birth"] = "b"
    with pytest.raises(causal.CertificateRefusal, match="birth name"):
        causal.admit_problem(p)


def test_native_executable_custody_refuses(native, tmp_path):
    receipt = copy.deepcopy(native.build)
    receipt["binary_sha256"] = "0" * 64
    path = tmp_path / "bad_build.json"
    path.write_text(causal.encoded(receipt), encoding="utf-8")
    with pytest.raises(causal.CertificateRefusal, match="executable changed"):
        causal.NativeOwner(native.binary, path, native.source_root)
