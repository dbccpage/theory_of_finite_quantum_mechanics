"""Independent source arithmetic and adversarial observer-certificate checks."""

from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations, product
from math import prod
from pathlib import Path

import pytest
from observer_completion import observer_completion as oc
from observer_completion import replay_examples as replay

PACKAGE = Path(__file__).resolve().parents[1] / "observer_completion"


def rank_by_minors(matrix):
    """Independent tiny-case oracle: nonzero determinant minors, no elimination."""
    for size in range(min(matrix.r, matrix.c), 0, -1):
        for rows in combinations(range(matrix.r), size):
            for columns in combinations(range(matrix.c), size):
                determinant = sum(
                    (-1)**sum(p[i] > p[j] for i in range(size) for j in range(i+1, size))
                    * prod(matrix.a[rows[i]][columns[p[i]]] for i in range(size))
                    for p in permutations(range(size))
                )
                if determinant:
                    return size
    return 0


def test_delivered_certificates_and_regeneration_agree():
    receipt = oc.read_json(PACKAGE / "observer_completion_certificates.json")
    assert replay.check(receipt)
    assert oc.same_json(replay.generate(), receipt)
    expected = oc.read_json(PACKAGE / "generic_input.json")
    generic = oc.read_json(PACKAGE / "generic_receipt.json")
    assert oc.check_receipt(generic, expected)
    assert oc.same_json(oc.run_input(expected), generic)


def test_all_retained_adversarial_certificates_refuse():
    receipt = oc.read_json(PACKAGE / "observer_completion_certificates.json")
    assert len(replay.adversarial(receipt)) == 15
    for location in ("initial", "completion"):
        altered = deepcopy(receipt)
        item = altered["cases"][0]
        container = item["initial"]["raw"] if location == "initial" else item["completions"][0]
        container["authority_effect"] = "Grant"
        with pytest.raises(ValueError, match="evidence fields"):
            replay.check(altered)


def test_handwritten_source_incidence_and_sharpness():
    three, lggr, projection, scalar = replay.source_instances()
    incidence = (
        (1, 0, 0, -1, 0, 0), (0, 1, 0, -1, 0, 0),
        (0, 1, 0, 0, -1, 0), (0, 0, 1, 0, -1, 0),
        (0, 0, 1, 0, 0, -1), (1, 0, 0, 0, 0, -1),
    )
    expected = tuple(
        tuple(Fraction(incidence[e][site] if coordinate == j else 0)
              for site in range(6) for coordinate in range(3))
        for e in range(6) for j in range(3)
    )
    assert three["d0"].a == expected
    assert rank_by_minors(oc.M(incidence)) == 5
    assert oc.rank(three["d0"]) == 5 * 3
    assert [oc.construct(three["d0"], three["Q"], target)["minimum"]
            for target in ("raw", "quotient", "both")] == [3, 3, 6]
    sites = oc.M([[1 if i == 0 else 0] for i in range(18)])
    defect = three["d0"] @ sites
    observer = oc.vc(three["Q"], three["completions"]["raw"])
    assert oc.l1(defect) == 2 and oc.l1(observer @ defect) == 1
    assert oc.l1(three["L"] @ defect) == 0
    invisible = oc.eye(18).cols([0])
    assert oc.l1(three["Q"] @ invisible) == 0
    assert oc.l1(three["L"] @ invisible) == 1

    expected_coupled = oc.M([
        [-1, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0],
    ])
    for source in (lggr, projection):
        assert source["d0"] == expected_coupled
        assert [oc.construct(source["d0"], source["Q"], target)["minimum"]
                for target in ("raw", "quotient", "both")] == [0, 2, 2]
        defect = oc.M([[1], [1], [1], [1]])
        assert oc.l1(defect) == 4
        assert oc.l1(source["Q"] @ defect) == 2
        assert max(abs(row[0]) for row in (source["Q"] @ defect).a) == 1
    assert lggr["Q"] != projection["Q"]
    assert oc.l1(scalar["L"] @ oc.M([[1], [-1]])) == 2


def test_small_completions_against_independent_rank_calculation():
    def rank(matrix):
        return rank_by_minors(matrix)

    for d_values in product((-1, 0, 1), repeat=2):
        d = oc.M([[x] for x in d_values])
        for q_values in product((-1, 0, 1), repeat=2):
            q = oc.M([q_values])
            k = 2 - rank(q)
            r = rank(d) - rank(q @ d)
            for target, minimum in (("raw", r), ("quotient", k-r), ("both", k)):
                cert = oc.construct(d, q, target)
                assert cert["minimum"] == minimum
                assert oc.check_completion(d, q, cert)
                a = oc.vc(q, oc.M.decode(cert["R"]))
                if target in ("raw", "both"):
                    assert rank(a @ d) == rank(d)
                if target in ("quotient", "both"):
                    assert rank(a) - rank(a @ d) == 2 - rank(d)


@pytest.mark.parametrize("value", [True, False, 0.5, 1, "1/1", "2/4", "0.5"])
def test_wire_scalars_require_canonical_rational_strings(value):
    with pytest.raises(ValueError):
        oc.M.decode({"rows": 1, "cols": 1, "data": [[value]]})


@pytest.mark.parametrize("dimension", [True, -1, 1.0, "1"])
def test_wire_shapes_require_nonnegative_exact_integers(dimension):
    with pytest.raises(ValueError):
        oc.M.decode({"rows": dimension, "cols": 1, "data": [["1"]]})


@pytest.mark.parametrize("text", ['{"x":0,"x":1}', '{"x":NaN}', '{"x":1.5}'])
def test_strict_json_refuses_ambiguous_or_nonexact_input(text):
    with pytest.raises(ValueError):
        oc.decode_json(text)


@pytest.mark.parametrize("target", ["raw", "quotient", "both"])
def test_zero_dimensional_recovery_and_distance(target):
    problem = {"d0": oc.zero(0, 3).encode(), "Q": oc.zero(0, 0).encode(),
               "target": target, "V_facets": oc.facets_linf(0).encode(),
               "augmented_facets": oc.facets_linf(0).encode()}
    receipt = oc.run_input(problem)
    assert oc.check_receipt(receipt, problem)
    assert all(c["constant"] == "0" for c in receipt["recovery"])
    receipt["recovery"][0]["vacuous"] = 1
    with pytest.raises(ValueError, match="vacuous constant"):
        oc.check_receipt(receipt, problem)
    distance = oc.distance_certificate(oc.zero(0, 0), oc.zero(0, 0), oc.zero(0, 1))
    assert oc.check_distance(oc.zero(0, 0), oc.zero(0, 0), distance) == 0
    distance["zero_dimensional"] = 1
    with pytest.raises(ValueError, match="zero distance convention"):
        oc.check_distance(oc.zero(0, 0), oc.zero(0, 0), distance)


@pytest.mark.parametrize("d,target", [(oc.zero(2, 0), "raw"), (oc.eye(2), "quotient")])
def test_vacuous_recovery_domains_have_zero_constant(d, target):
    problem = {"d0": d.encode(), "Q": oc.zero(0, 2).encode(), "target": target,
               "V_facets": oc.facets_l1(2).encode(),
               "augmented_facets": oc.facets_linf(0).encode()}
    assert oc.run_input(problem)["recovery"][0]["constant"] == "0"


@pytest.mark.parametrize("d,target", [(oc.eye(1), "raw"), (oc.zero(1, 0), "quotient")])
def test_zero_report_space_does_not_supply_zero_recovery_constant(d, target):
    q = oc.zero(0, 1)
    assert not oc.guarantees(d, q)[target]
    assert oc.check_failure(d, q, oc.failure(d, q, target))
    with pytest.raises(ValueError):
        oc.recovery_certificate(d, q, oc.facets_l1(1), oc.facets_linf(0), target)


def test_receipt_requires_separate_input_and_complete_initial_diagnosis():
    expected = oc.read_json(PACKAGE / "generic_input.json")
    receipt = oc.read_json(PACKAGE / "generic_receipt.json")
    altered_input = deepcopy(expected)
    altered_input["Q"]["data"][0][0] = "2"
    with pytest.raises(ValueError, match="expected input"):
        oc.check_receipt(receipt, altered_input)
    receipt["initial_failure"] = None
    with pytest.raises(ValueError, match="failure"):
        oc.check_receipt(receipt, expected)


def test_recovery_cannot_change_its_vacuity_claim():
    expected = oc.read_json(PACKAGE / "generic_input.json")
    receipt = oc.read_json(PACKAGE / "generic_receipt.json")
    receipt["recovery"][0]["vacuous"] = True
    with pytest.raises(ValueError, match="nonvacuous"):
        oc.check_receipt(receipt, expected)
