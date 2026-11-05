from copy import deepcopy
from itertools import product
import json

import pytest

from faithful_representation.core import (AdmissionError, apply_change, assignments, backward, check,
                                         encode, evaluate_family, family_at, family_count, forward,
                                         digest, load, replay, search, solution)
from faithful_representation.examples import (boundaries, compare, cycle, exhaustive_boolean_cases,
                                              presentation_chain, problem, run_examples)


def test_exhaustive_all_4096_boolean_triangle_instances():
    result = exhaustive_boolean_cases()
    assert result["instances"] == 4096


@pytest.mark.parametrize("p,expected", [
    (problem(), "Proved"), (problem([("x", [])]), "Refuted"),
    (problem([], [("f", [], [])]), "Refuted"), (problem([], [("t", [], [[]])]), "Proved"),
    (problem([("x", ["a", "b"])]), "Proved"),
    (problem([("x", ["a"])], [("empty", ["x"], [])]), "Refuted"),
    (cycle(True), "Proved"), (cycle(False), "Refuted"),
])
def test_boundary_carriers(p, expected):
    compare(p)
    encoded = encode(p)
    certificate = search(encoded, family_count(encoded))
    assert certificate["status"] == expected
    assert check(p, certificate)["accepted"]


def test_each_presentation_change_has_actual_inverse_on_solutions():
    current, changes = presentation_chain()
    for spec in changes:
        target = apply_change(current, spec)
        for source_answer in assignments(current):
            if solution(current, source_answer):
                target_answer = forward(source_answer, spec)
                assert solution(target, target_answer)
                assert backward(target_answer, spec) == source_answer
        for target_answer in assignments(target):
            if solution(target, target_answer):
                source_answer = backward(target_answer, spec)
                assert solution(current, source_answer)
                assert forward(source_answer, spec) == target_answer
        current = target


def test_all_boolean_binary_tables_split_exactly_when_no_spurious_rows():
    rows = list(product(["0", "1"], repeat=2))
    spec = {"kind": "split", "relation": "ab", "components": [["a"], ["b"]], "names": ["a", "b"]}
    for mask in range(16):
        table = [r for i, r in enumerate(rows) if mask & (1 << i)]
        p = problem([("a", ["0", "1"]), ("b", ["0", "1"])], [("ab", ["a", "b"], table)])
        joined = set(product({r[0] for r in table}, {r[1] for r in table}))
        if joined != set(table):
            with pytest.raises(AdmissionError, match="spurious"):
                apply_change(p, spec)
        else:
            target = apply_change(p, spec)
            assert all(solution(p, x) == solution(target, x) for x in assignments(p))


def test_all_pairs_of_boolean_binary_tables_join_preserves_assignments():
    rows = list(product(["0", "1"], repeat=2))
    tables = [[r for i, r in enumerate(rows) if mask & (1 << i)] for mask in range(16)]
    for left, right in product(tables, repeat=2):
        p = problem([(v, ["0", "1"]) for v in "abc"], [("ab", "ab", left), ("bc", "bc", right)])
        target = apply_change(p, {"kind": "join", "left": "ab", "right": "bc", "name": "abc"})
        assert all(solution(p, x) == solution(target, x) for x in assignments(p))


def test_nonstarving_search_and_actual_cost_of_transports():
    p = cycle(False)
    e = encode(p)
    result = search(e, 2 * family_count(e), proposals=[[999]] * 10000)
    assert result["status"] == "Refuted"
    assert [x["kind"] for x in result["events"]] == ["proposal", "canonical"] * 8
    assert check(p, result)["accepted"]
    p, changes = presentation_chain()
    e = encode(p, changes)
    partial = search(e, 3)
    assert partial["status"] == "Undetermined" and partial["checkpoint"]["state"]["transport"] == 3
    complete = search(e, 20, partial)
    assert complete["status"] == "Proved"
    assert complete["events"][:3] == partial["events"]
    assert check(p, complete)["accepted"]


@pytest.mark.parametrize("fuel,max_steps", [(0, None), (2, None), (10, 3)])
def test_interruption_and_resume(fuel, max_steps):
    p = cycle(False)
    e = encode(p)
    first = search(e, fuel, max_steps=max_steps)
    assert first["status"] == "Undetermined" and check(p, first)["accepted"]
    result = search(e, 20, first)
    assert result["status"] == "Refuted" and check(p, result)["accepted"]
    assert result["events"][:len(first["events"])] == first["events"]
    with pytest.raises(AdmissionError):
        search(e, 0, search(e, 2))


@pytest.mark.parametrize("mutation", [
    lambda c: c.update(answer={"a": "bad"}),
    lambda c: c.update(authority_effect="Granted"),
    lambda c: c["encoding"]["problem"]["assumptions"].append("new assumption"),
    lambda c: c["encoding"]["problem"]["authorization"].append("new permission"),
    lambda c: c["encoding"]["changes"][0].update(parent="stale"),
    lambda c: c["checkpoint"].update(spent=0),
    lambda c: c["events"][-1].update(candidate=[999]),
    lambda c: c["events"][0].update(cost=0),
    lambda c: c["grants"][0].update(total=0),
    lambda c: c.update(status="Refuted"),
    lambda c: c["encoding"].update(hash="forged"),
])
def test_reject_mutated_claims_without_substituting_a_solution(mutation):
    p, changes = presentation_chain()
    c = search(encode(p, changes), 30)
    mutation(c)
    assert not check(p, c)["accepted"]


def test_wrong_task_and_incomplete_negative():
    c = search(encode(cycle(True)), 10)
    assert not check(cycle(False), c)["accepted"]


def test_rehashed_false_solution_is_still_refused():
    p = cycle(False)
    c = search(encode(p), 1)
    event = c["events"][0]
    false_answer = dict.fromkeys("xyz", "0")
    event["result"] = {"outcome": "SOLUTION", "defect": [0] * 6, "answer": false_answer}
    event["hash"] = digest({k: v for k, v in event.items() if k != "hash"})
    c["checkpoint"]["parent"] = event["hash"]
    c["checkpoint"]["state"]["answer"] = false_answer
    c.update(status="Proved", reason="CERTIFIED_SOLUTION", answer=false_answer)
    assert not check(p, c)["accepted"]
    c = search(encode(cycle(False)), 1)
    c.update(status="Refuted", reason="EXHAUSTIVE_FAILURE")
    assert not check(cycle(False), c)["accepted"]


def test_unsafe_presentation_changes_refused():
    p = problem([("a", ["0", "1"]), ("b", ["0", "1"])],
                [("ab", ["a", "b"], [["0", "0"], ["1", "1"]])])
    with pytest.raises(AdmissionError, match="spurious"):
        encode(p, [{"kind": "split", "relation": "ab", "components": [["a"], ["b"]],
                    "names": ["a", "b"]}])
    for rows in ([["0", "0"]], [["0", "0"], ["0", "1"], ["1", "0"]]):
        with pytest.raises(AdmissionError):
            encode(p, [{"kind": "auxiliary", "name": "c", "domain": ["0", "1"],
                        "scope": ["a"], "rows": rows, "relation": "ac"}])
    with pytest.raises(AdmissionError):
        encode(p, [{"kind": "rename", "variables": {"a": "c", "b": "c"},
                    "values": {v: {"0": "0", "1": "1"} for v in "ab"}}])


@pytest.mark.parametrize("malformed", [
    '{"x": 1, "x": 2}', '{"x": NaN}', '{"x": Infinity}',
])
def test_strict_json_admission(tmp_path, malformed):
    path = tmp_path / "bad.json"
    path.write_text(malformed)
    with pytest.raises(AdmissionError):
        load(path)


def test_boolean_row_index_is_not_integer_witness():
    result = search(encode(cycle(True)), 1, proposals=[[True, 0, 0]])
    assert result["events"][0]["result"]["outcome"] == "INVALID_CANDIDATE"
    assert result["status"] == "Undetermined"
    assert result["answer"] is None


def test_checker_failure_cannot_be_counted_as_exhaustive_rejection(monkeypatch):
    import faithful_representation.core as core
    p = cycle(True)
    valid = search(encode(p), 10)
    def broken(*args):
        raise AdmissionError("checker unavailable")
    monkeypatch.setattr(core, "evaluate_family", broken)
    with pytest.raises(AdmissionError, match="exhaustion is unproved"):
        search(encode(p), 10)
    assert not check(p, valid)["accepted"]


def test_changed_queue_and_checkpoint_binding():
    e = encode(cycle(False))
    c = search(e, 1, proposals=[[999]])
    with pytest.raises(AdmissionError):
        search(e, 20, c, proposals=[])
    c["checkpoint"]["parent"] = "old"
    with pytest.raises(AdmissionError):
        search(e, 20, c)


def test_no_information_or_completion_laundering():
    result = boundaries()
    assert result["blind_observer_false_greens"] == 8
    assert result["whole_defect_repair_space_false_greens"] == 8
    assert result["original_solutions"] == 0
    assert result["calculus"]["samples_only"]["primary_status"] == "Undetermined"
    assert result["calculus"]["affine_assumption"]["conditional_answer"] == "50"


def test_replay_is_offline_and_uses_retained_witness(tmp_path, monkeypatch):
    import socket
    def forbidden(*args, **kwargs):
        raise AssertionError("replay attempted network access")
    monkeypatch.setattr(socket, "socket", forbidden)
    run = run_examples()["four_transports"]
    for name in ("problem", "certificate"):
        (tmp_path / f"{name}.json").write_text(json.dumps(run[name]), encoding="utf-8")
    assert replay(tmp_path)["accepted"]
    run["certificate"]["answer"] = {}
    (tmp_path / "certificate.json").write_text(json.dumps(run["certificate"]), encoding="utf-8")
    assert not replay(tmp_path)["accepted"]
