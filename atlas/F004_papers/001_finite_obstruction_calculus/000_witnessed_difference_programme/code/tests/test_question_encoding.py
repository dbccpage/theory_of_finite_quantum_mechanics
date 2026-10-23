"""Native wire integration and receipt mutation controls (monorepo required)."""

import json

import pytest
import question_encoding.replay as replay_module
from question_encoding.ffi import NativeRefusal, NativeUnavailable, invoke
from question_encoding.replay import RECEIPT, replay

pytestmark = pytest.mark.monorepo


def request(anchor=0, edges=(0, 0, 0)):
    task = {"derivative": [0, 0], "value_at_zero": 0}
    report = {"schema_version": 1, "domain": "integer_quadratic_antiderivative_at_zero_v1",
              "task": task, "anchor": anchor, "edges": list(edges)}
    return {"action": "verify_cochain", "expected_task": task, "report": json.dumps(report)}


def test_same_unanchored_report_can_have_opposite_checked_answers():
    assert invoke(request())["accepted"] is True
    assert invoke(request(anchor=1))["accepted"] is False


def test_corrupted_edge_is_a_parser_refusal():
    with pytest.raises(NativeRefusal) as error:
        invoke(request(edges=(0, 0, 1)))
    assert error.value.payload["refused"] == "NON_CLOSED_REPORT"


def test_changed_expected_question_is_not_accepted_as_the_old_one():
    changed = request()
    changed["expected_task"]["value_at_zero"] = 1
    with pytest.raises(NativeRefusal) as error:
        invoke(changed)
    assert error.value.payload["refused"] == "TASK_MISMATCH"


def test_undeclared_action_and_claimed_authority_are_refused():
    changed = request(); changed["authority"] = "grant"
    with pytest.raises(NativeRefusal):
        invoke(changed)
    with pytest.raises(NativeRefusal):
        invoke({"action": "verify_anything"})


def test_missing_native_capability_has_no_mathematical_fallback(monkeypatch):
    monkeypatch.delenv("WDP_QUESTION_ENCODING_BINARY", raising=False)
    with pytest.raises(NativeUnavailable):
        invoke({"action": "experiment"})


def test_deposited_result_and_source_bindings_replay():
    expected = json.loads(RECEIPT.read_text(encoding="utf-8"))
    actual = replay()
    assert actual == expected
    expected["experiment"]["strategies"][2]["checker_calls"] -= 1
    assert actual != expected


def test_stale_native_source_snapshot_is_not_relabeled_as_a_fresh_build(monkeypatch):
    monkeypatch.setattr(replay_module, "invoke", lambda _request: {"compiled_source_sha256": {}})
    with pytest.raises(RuntimeError, match="different source bytes"):
        replay()
