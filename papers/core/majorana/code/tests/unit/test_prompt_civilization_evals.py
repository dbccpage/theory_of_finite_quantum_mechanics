from __future__ import annotations

import json
from pathlib import Path
import tempfile

from omega_engine.crates.prompt_civilization import (
    AntiSkillEvaluationReceiptV1,
    Err,
    compile_registry_syntax_only,
    evaluate_fixtures,
)


ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / ".agents" / "anti_skills" / "fixtures" / "eval_cases.json"
PROPOSAL = (
    ROOT / ".agents" / "anti_skills" / "fixtures" / "valid_prompt_proposal.json"
)


def _evaluate(cases: Path = CASES):
    return evaluate_fixtures(
        cases, PROPOSAL, compile_registry_syntax_only([]).unwrap()
    )


def test_named_evaluation_is_deterministic_and_computed_only() -> None:
    first = _evaluate().unwrap()
    second = _evaluate().unwrap()
    assert first.to_dict() == second.to_dict()
    assert first.outcome == "COMPUTED_PASS"
    assert first.authority_effect == "None"
    assert len(first.case_results) == 6
    assert sum(item.negative_control for item in first.case_results) == 4
    assert all(item.passed for item in first.case_results)
    assert AntiSkillEvaluationReceiptV1.from_dict(first.to_dict()) == first
    committed = AntiSkillEvaluationReceiptV1.from_dict(
        json.loads(
            (
                ROOT
                / ".agents"
                / "anti_skills"
                / "fixtures"
                / "eval_receipt.json"
            ).read_text(encoding="utf-8")
        )
    )
    assert committed == first


def test_fixture_mutation_changes_receipt_even_when_case_still_passes() -> None:
    original = json.loads(CASES.read_text(encoding="utf-8"))
    original["cases"][0]["original_prompt"] += " Additional legitimate context."
    with tempfile.TemporaryDirectory() as folder:
        mutated = Path(folder) / "cases.json"
        mutated.write_text(
            json.dumps(original, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        changed = _evaluate(mutated).unwrap()
    assert changed.outcome == "COMPUTED_PASS"
    assert changed.receipt_id != _evaluate().unwrap().receipt_id
    assert changed.fixture_digest != _evaluate().unwrap().fixture_digest


def test_extra_or_missing_finding_fails_the_exact_case() -> None:
    wire = json.loads(CASES.read_text(encoding="utf-8"))
    wire["cases"][-1]["expected_codes"] = []
    with tempfile.TemporaryDirectory() as folder:
        changed_path = Path(folder) / "cases.json"
        changed_path.write_text(json.dumps(wire), encoding="utf-8")
        changed = _evaluate(changed_path).unwrap()
    assert changed.outcome == "COMPUTED_FAIL"
    assert not changed.case_results[-1].passed


def test_caller_cannot_relabel_computed_failure_as_pass() -> None:
    wire = json.loads(CASES.read_text(encoding="utf-8"))
    wire["cases"][-1]["expected_codes"] = []
    with tempfile.TemporaryDirectory() as folder:
        changed_path = Path(folder) / "cases.json"
        changed_path.write_text(json.dumps(wire), encoding="utf-8")
        receipt = _evaluate(changed_path).unwrap().to_dict()
    receipt["outcome"] = "COMPUTED_PASS"
    try:
        AntiSkillEvaluationReceiptV1.from_dict(receipt)
    except ValueError as exc:
        assert "outcome" in str(exc) or "receipt_id" in str(exc)
    else:
        raise AssertionError("caller-minted pass outcome was accepted")


def test_unknown_fixture_fields_refuse() -> None:
    wire = json.loads(CASES.read_text(encoding="utf-8"))
    wire["cases"][0]["dynamic_executor"] = "evil.module:function"
    with tempfile.TemporaryDirectory() as folder:
        changed_path = Path(folder) / "cases.json"
        changed_path.write_text(json.dumps(wire), encoding="utf-8")
        result = _evaluate(changed_path)
    assert isinstance(result, Err)
    assert result.error.code == "EVALUATION_REFUSED"
