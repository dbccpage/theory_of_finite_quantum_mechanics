from __future__ import annotations

from dataclasses import replace

import pytest

from omega_engine.kernel.higher_operad import (
    Err,
    Ok,
    OperationSpec,
    PortSpec,
    Primitive,
    normalize,
)
from omega_engine.kernel.presentation_difference import (
    DemandV1,
    PresentationV1,
    QuestionV1,
)
from omega_engine.kernel.solver_of_solvers import (
    CandidatePlanV1,
    CostOrder,
    EvaluationStatus,
    FinitePlanGrammarV1,
    PlanEvaluationV1,
    PlanKind,
    SearchDeclarationV1,
    bind_declared_plan_evaluation,
)
from omega_engine.kernel.structure_extension import (
    CheckedQuestionExtensionV1,
    evaluate_extension_after_exhaustion,
    reconstruct_declared_extension,
)


def _digest(seed: str) -> str:
    encoded = seed.encode("utf-8").hex()
    return "sha256:" + (encoded + ("0" * 64))[:64]


def _term(name: str):
    operation = OperationSpec(
        operation_id=f"solver.{name}",
        version="v1",
        input_ports=(PortSpec("input", "colour.problem", "schema.problem.v1"),),
        output_port=PortSpec("output", "colour.answer", "schema.answer.v1"),
        executor_ref=f"executor.{name}",
        executor_digest=_digest(f"executor-{name}"),
    )
    result = normalize(Primitive(operation))
    assert isinstance(result, Ok)
    return result.value


def _candidate(kind: PlanKind = PlanKind.SAME_LEVEL_REPAIR) -> CandidatePlanV1:
    return CandidatePlanV1(
        candidate_ref="candidate.same-level",
        grammar_id="grammar.same-level",
        term=_term("same-level"),
        kind=kind,
        cost=(1, 0),
        provenance_digest=_digest("provenance"),
    )


def _grammar(candidate: CandidatePlanV1 | None = None) -> FinitePlanGrammarV1:
    return FinitePlanGrammarV1(
        "grammar.same-level",
        (candidate or _candidate(),),
    )


def _search(grammar: FinitePlanGrammarV1) -> SearchDeclarationV1:
    return SearchDeclarationV1(
        grammar_id=grammar.grammar_id,
        grammar_digest=grammar.canonical_id,
        policy_digest=_digest("policy"),
        cost_order=CostOrder.LEXICOGRAPHIC,
        cost_dimension=2,
        max_candidates=1,
    )


def _admit(
    candidate: CandidatePlanV1,
    status: EvaluationStatus,
):
    evaluation = PlanEvaluationV1(
        candidate_id=candidate.canonical_id,
        status=status,
        residual=(1,),
        evidence_digest=_digest("evidence"),
        policy_id=_digest("policy"),
        verifier_ref="verifier.test",
        verifier_digest=_digest("verifier"),
        replay_receipt_ref=_digest("replay"),
        environment_digest=_digest("environment"),
    )
    result = bind_declared_plan_evaluation(candidate, evaluation)
    assert isinstance(result, Ok)
    return result.value


def _parent() -> PresentationV1:
    return PresentationV1(
        ("a", "b"),
        (QuestionV1("q.constant", ("0", "0")),),
    )


def _child() -> PresentationV1:
    parent = _parent()
    return PresentationV1(
        parent.points,
        parent.questions + (QuestionV1("q.split", ("left", "right")),),
    )


def _demand() -> DemandV1:
    return DemandV1("a", "b", True, True)


def _run(
    *,
    status: EvaluationStatus = EvaluationStatus.REJECTED,
    child: PresentationV1 | None = None,
    demand: DemandV1 | None = None,
):
    candidate = _candidate()
    grammar = _grammar(candidate)
    return evaluate_extension_after_exhaustion(
        _search(grammar),
        grammar,
        (_admit(candidate, status),),
        _parent(),
        child or _child(),
        demand or _demand(),
    )


def test_resolving_extension_is_checked_after_same_level_exhaustion() -> None:
    result = _run()
    assert isinstance(result, Ok)
    assert result.value.receipt.new_question_ids == ("q.split",)
    assert result.value.receipt.class_count_before == 1
    assert result.value.receipt.class_count_after == 2
    assert result.value.authority_effect.value == "None"


def test_verified_same_level_repair_blocks_extension_branch() -> None:
    result = _run(status=EvaluationStatus.VERIFIED)
    assert isinstance(result, Err)
    assert result.error.code == "SAME_LEVEL_REPAIR_AVAILABLE"


def test_inconclusive_same_level_evaluation_blocks_extension_branch() -> None:
    result = _run(status=EvaluationStatus.INCONCLUSIVE)
    assert isinstance(result, Err)
    assert result.error.code == "SAME_LEVEL_EVALUATION_INCONCLUSIVE"


def test_incomplete_same_level_evaluation_is_refused() -> None:
    candidate = _candidate()
    grammar = _grammar(candidate)
    result = evaluate_extension_after_exhaustion(
        _search(grammar), grammar, (), _parent(), _child(), _demand()
    )
    assert isinstance(result, Err)
    assert result.error.code == "INCOMPLETE_GRAMMAR_EVALUATION"


def test_mixed_grammar_cannot_certify_same_level_exhaustion() -> None:
    grammar = _grammar(_candidate(PlanKind.STRUCTURE_EXTENSION))
    result = evaluate_extension_after_exhaustion(
        _search(grammar),
        grammar,
        (_admit(grammar.candidates[0], EvaluationStatus.REJECTED),),
        _parent(),
        _child(),
        _demand(),
    )
    assert isinstance(result, Err)
    assert result.error.code == "MIXED_SAME_LEVEL_GRAMMAR"


def test_extension_that_does_not_split_is_refused() -> None:
    parent = _parent()
    child = PresentationV1(
        parent.points,
        parent.questions + (QuestionV1("q.repeated", ("x", "x")),),
    )
    result = _run(child=child)
    assert isinstance(result, Err)
    assert result.error.code == "INEFFECTIVE_STRUCTURE_EXTENSION"


def test_changed_parent_question_prefix_is_refused() -> None:
    child = PresentationV1(
        ("a", "b"),
        (
            QuestionV1("q.changed", ("0", "0")),
            QuestionV1("q.split", ("left", "right")),
        ),
    )
    result = _run(child=child)
    assert isinstance(result, Err)
    assert result.error.code == "INEFFECTIVE_STRUCTURE_EXTENSION"


@pytest.mark.parametrize(
    "demand",
    [
        DemandV1("a", "b", False, True),
        DemandV1("a", "b", True, False),
    ],
)
def test_unretained_or_unprotected_pair_cannot_trigger_extension(
    demand: DemandV1,
) -> None:
    result = _run(demand=demand)
    assert isinstance(result, Err)
    assert result.error.code == "NO_ACTIVE_OBSTRUCTION"


def test_grammar_digest_mismatch_is_refused() -> None:
    candidate = _candidate()
    grammar = _grammar(candidate)
    search = replace(_search(grammar), grammar_digest=_digest("wrong"))
    result = evaluate_extension_after_exhaustion(
        search,
        grammar,
        (_admit(candidate, EvaluationStatus.REJECTED),),
        _parent(),
        _child(),
        _demand(),
    )
    assert isinstance(result, Err)
    assert result.error.code == "GRAMMAR_DIGEST_MISMATCH"


def test_checked_extension_is_an_explicitly_structural_record() -> None:
    admitted = _run()
    assert isinstance(admitted, Ok)
    rebuilt = CheckedQuestionExtensionV1(
        admitted.value.parent,
        admitted.value.child,
        admitted.value.demand,
        admitted.value.receipt,
    )
    assert rebuilt == admitted.value


def test_receipt_authority_cannot_be_minted() -> None:
    admitted = _run()
    assert isinstance(admitted, Ok)
    with pytest.raises(ValueError, match="AuthorityEffect None"):
        replace(admitted.value.receipt, authority_effect="Minted")


def test_mutated_child_is_refused_fail_closed() -> None:
    child = _child()
    object.__setattr__(child.questions[-1], "answers", ["left", "right"])
    result = _run(child=child)
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_PRESENTATION"


def test_extension_receipt_is_content_bound_to_frontier_and_child() -> None:
    first = _run()
    second = _run()
    assert isinstance(first, Ok) and isinstance(second, Ok)
    assert first.value.receipt.canonical_id == second.value.receipt.canonical_id
    assert first.value.receipt.frontier_id.startswith("sha256:")
    assert first.value.receipt.child_id == _child().presentation_id


def test_extension_receipt_binds_rejected_evaluation_content() -> None:
    candidate = _candidate()
    grammar = _grammar(candidate)
    first_declared = _admit(candidate, EvaluationStatus.REJECTED)
    changed_evaluation = replace(
        first_declared.evaluation,
        evidence_digest=_digest("different-evidence"),
    )
    changed_declared = bind_declared_plan_evaluation(candidate, changed_evaluation)
    assert isinstance(changed_declared, Ok)
    first = evaluate_extension_after_exhaustion(
        _search(grammar),
        grammar,
        (first_declared,),
        _parent(),
        _child(),
        _demand(),
    )
    changed = evaluate_extension_after_exhaustion(
        _search(grammar),
        grammar,
        (changed_declared.value,),
        _parent(),
        _child(),
        _demand(),
    )
    assert isinstance(first, Ok) and isinstance(changed, Ok)
    assert first.value.receipt.frontier_id != changed.value.receipt.frontier_id
    assert first.value.receipt.canonical_id != changed.value.receipt.canonical_id


def test_declared_extension_reconstructs_deterministically() -> None:
    candidate = _candidate()
    grammar = _grammar(candidate)
    evaluations = (_admit(candidate, EvaluationStatus.REJECTED),)
    admitted = evaluate_extension_after_exhaustion(
        _search(grammar),
        grammar,
        evaluations,
        _parent(),
        _child(),
        _demand(),
    )
    assert isinstance(admitted, Ok)
    assert reconstruct_declared_extension(
        admitted.value,
        _search(grammar),
        grammar,
        evaluations,
    )


def test_post_admission_nested_mutation_fails_reconstruction() -> None:
    candidate = _candidate()
    grammar = _grammar(candidate)
    evaluations = (_admit(candidate, EvaluationStatus.REJECTED),)
    admitted = evaluate_extension_after_exhaustion(
        _search(grammar),
        grammar,
        evaluations,
        _parent(),
        _child(),
        _demand(),
    )
    assert isinstance(admitted, Ok)
    object.__setattr__(admitted.value.child.questions[-1], "answers", ["left", "right"])
    assert not reconstruct_declared_extension(
        admitted.value,
        _search(grammar),
        grammar,
        evaluations,
    )
