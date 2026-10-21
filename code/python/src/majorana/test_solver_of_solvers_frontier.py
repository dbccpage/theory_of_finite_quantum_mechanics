from __future__ import annotations

from dataclasses import replace
from typing import Optional

import omega_engine.kernel as public_kernel
from omega_engine.kernel.higher_operad import (
    Err,
    Ok,
    OperationSpec,
    PortSpec,
    Primitive,
    identity_path2,
    normalize,
)
from omega_engine.kernel.solver_of_solvers import (
    CandidatePlanV1,
    CostOrder,
    EvaluationStatus,
    FinitePlanGrammarV1,
    FrontierTerminal,
    PlanEvaluationV1,
    PlanKind,
    SearchDeclarationV1,
    bind_declared_plan_evaluation,
    route_declared_batch,
    route_declared_finite_grammar,
)


def _digest(seed: str) -> str:
    encoded = seed.encode("utf-8").hex()
    return "sha256:" + (encoded + ("0" * 64))[:64]


def _term(name: str):
    source = PortSpec("input", "colour.problem", "schema.problem.v1")
    target = PortSpec("output", "colour.answer", "schema.answer.v1")
    operation = OperationSpec(
        operation_id=f"solver.{name}",
        version="v1",
        input_ports=(source,),
        output_port=target,
        executor_ref=f"executor.{name}",
        executor_digest=_digest(f"executor-{name}"),
    )
    normalized = normalize(Primitive(operation))
    assert isinstance(normalized, Ok)
    return normalized.value


def _search(
    order: CostOrder = CostOrder.LEXICOGRAPHIC,
    *,
    dimension: int = 2,
    cap: int = 16,
) -> SearchDeclarationV1:
    return SearchDeclarationV1(
        grammar_id="grammar.test",
        grammar_digest=_digest("grammar"),
        policy_digest=_digest("policy"),
        cost_order=order,
        cost_dimension=dimension,
        max_candidates=cap,
    )


def _candidate(
    name: str,
    cost: tuple[int, ...],
    *,
    term=None,
    kind: PlanKind = PlanKind.SAME_LEVEL_REPAIR,
    provenance: Optional[str] = None,
) -> CandidatePlanV1:
    return CandidatePlanV1(
        candidate_ref=f"candidate.{name}",
        grammar_id="grammar.test",
        term=term or _term(name),
        kind=kind,
        cost=cost,
        provenance_digest=_digest(provenance or f"provenance-{name}"),
    )


def _evaluation(
    candidate: CandidatePlanV1,
    status: EvaluationStatus = EvaluationStatus.VERIFIED,
    *,
    residual: tuple[int, ...] = (0,),
) -> PlanEvaluationV1:
    return PlanEvaluationV1(
        candidate_id=candidate.canonical_id,
        status=status,
        residual=residual,
        evidence_digest=_digest(f"evidence-{candidate.candidate_ref}"),
        policy_id=_digest("policy"),
        verifier_ref="verifier.test",
        verifier_digest=_digest("verifier"),
        replay_receipt_ref=_digest(f"replay-{candidate.candidate_ref}"),
        environment_digest=_digest("environment"),
    )


def _admit(
    candidate: CandidatePlanV1,
    status: EvaluationStatus = EvaluationStatus.VERIFIED,
    *,
    residual: tuple[int, ...] = (0,),
):
    evaluation = _evaluation(candidate, status, residual=residual)
    assert evaluation.candidate_id == candidate.canonical_id
    assert evaluation.verifier_ref == "verifier.test"
    result = bind_declared_plan_evaluation(candidate, evaluation)
    assert isinstance(result, Ok)
    return result.value


def test_lexicographic_router_preserves_equal_cost_nonunique_plans() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    result = route_declared_batch(_search(), (_admit(left), _admit(right)))
    assert isinstance(result, Ok)
    assert result.value.terminal is FrontierTerminal.VERIFIED_FRONTIER
    assert len(result.value.classes) == 2
    assert result.value.dominated_candidate_ids == ()


def test_router_is_order_invariant_and_never_selects_first() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    forward = route_declared_batch(_search(), (_admit(left), _admit(right)))
    reverse = route_declared_batch(_search(), (_admit(right), _admit(left)))
    assert isinstance(forward, Ok) and isinstance(reverse, Ok)
    assert forward.value.canonical_id == reverse.value.canonical_id


def test_definitionally_equal_terms_form_one_class_without_losing_provenance() -> None:
    term = _term("shared")
    left = _candidate("left", (1, 0), term=term, provenance="left")
    right = _candidate("right", (1, 0), term=term, provenance="right")
    result = route_declared_batch(_search(), (_admit(left), _admit(right)))
    assert isinstance(result, Ok)
    assert len(result.value.classes) == 1
    assert set(result.value.classes[0].candidate_ids) == {
        left.canonical_id,
        right.canonical_id,
    }
    assert len(result.value.classes[0].term_ids) == 1


def test_equal_scalar_residual_is_not_equivalence() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    result = route_declared_batch(
        _search(),
        (_admit(left, residual=(7,)), _admit(right, residual=(7,))),
    )
    assert isinstance(result, Ok)
    assert len(result.value.classes) == 2


def test_lexicographic_dominance_is_recorded_without_deleting_receipt() -> None:
    best = _candidate("best", (1, 2))
    slower = _candidate("slower", (2, 0))
    result = route_declared_batch(_search(), (_admit(slower), _admit(best)))
    assert isinstance(result, Ok)
    assert result.value.dominated_candidate_ids == (slower.canonical_id,)
    assert set(result.value.accepted_candidate_ids) == {
        best.canonical_id,
        slower.canonical_id,
    }


def test_pareto_router_preserves_incomparable_minima() -> None:
    left = _candidate("left", (0, 2))
    right = _candidate("right", (2, 0))
    result = route_declared_batch(
        _search(CostOrder.PARETO),
        (_admit(left), _admit(right)),
    )
    assert isinstance(result, Ok)
    assert len(result.value.classes) == 2
    assert result.value.dominated_candidate_ids == ()


def test_pareto_router_removes_strictly_dominated_plan() -> None:
    best = _candidate("best", (1, 1))
    worse = _candidate("worse", (1, 2))
    result = route_declared_batch(
        _search(CostOrder.PARETO),
        (_admit(worse), _admit(best)),
    )
    assert isinstance(result, Ok)
    assert result.value.dominated_candidate_ids == (worse.canonical_id,)


def test_rejected_and_inconclusive_receipts_do_not_enter_frontier() -> None:
    rejected = _candidate("rejected", (0, 0))
    unknown = _candidate("unknown", (0, 0))
    result = route_declared_batch(
        _search(),
        (
            _admit(rejected, EvaluationStatus.REJECTED),
            _admit(unknown, EvaluationStatus.INCONCLUSIVE),
        ),
    )
    assert isinstance(result, Ok)
    assert result.value.terminal is FrontierTerminal.NO_VERIFIED_PLAN
    assert result.value.rejected_candidate_ids == (rejected.canonical_id,)
    assert result.value.inconclusive_candidate_ids == (unknown.canonical_id,)
    assert set(result.value.evaluation_ids) == {
        _evaluation(rejected, EvaluationStatus.REJECTED).canonical_id,
        _evaluation(unknown, EvaluationStatus.INCONCLUSIVE).canonical_id,
    }


def test_batch_cap_is_host_owned_and_checked_before_selection() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    result = route_declared_batch(
        _search(cap=1),
        (_admit(left), _admit(right)),
    )
    assert isinstance(result, Err)
    assert result.error.code == "BATCH_BUDGET_EXHAUSTED"


def test_evaluation_must_bind_candidate_before_replay() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    stale = replace(_evaluation(left), candidate_id=right.canonical_id)
    result = bind_declared_plan_evaluation(left, stale)
    assert isinstance(result, Err)
    assert result.error.code == "CANDIDATE_BINDING_MISMATCH"


def test_unbound_plan_evaluation_cannot_enter_router() -> None:
    candidate = _candidate("candidate", (1, 0))
    result = route_declared_batch(_search(), (_evaluation(candidate),))
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_DECLARED_EVALUATION"


def test_public_kernel_names_the_pure_handoff_as_declared_not_replayed() -> None:
    assert hasattr(public_kernel, "bind_declared_plan_evaluation")
    assert not hasattr(public_kernel, "ReplayedPlanEvaluationV1")
    assert not hasattr(public_kernel, "_seal_replayed_plan_evaluation")


def test_nested_mutation_after_admission_is_rejected() -> None:
    candidate = _candidate("candidate", (1, 0))
    admitted = _admit(candidate)
    object.__setattr__(admitted.evaluation, "residual", [0])
    result = route_declared_batch(_search(), (admitted,))
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_DECLARED_EVALUATION"


def test_candidate_cost_container_mutation_after_admission_is_rejected() -> None:
    candidate = _candidate("candidate", (1, 0))
    admitted = _admit(candidate)
    object.__setattr__(admitted.candidate, "cost", [1, 0])
    result = route_declared_batch(_search(), (admitted,))
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_DECLARED_EVALUATION"


def test_search_declaration_mutation_is_rejected() -> None:
    candidate = _candidate("candidate", (1, 0))
    search = _search()
    object.__setattr__(search, "max_candidates", True)
    result = route_declared_batch(search, (_admit(candidate),))
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_SEARCH"


def test_declared_evaluation_must_bind_exact_search_policy() -> None:
    candidate = _candidate("candidate", (1, 0))
    mismatched = replace(_evaluation(candidate), policy_id=_digest("other-policy"))
    bound = bind_declared_plan_evaluation(candidate, mismatched)
    assert isinstance(bound, Ok)
    result = route_declared_batch(_search(), (bound.value,))
    assert isinstance(result, Err)
    assert result.error.code == "EVALUATION_POLICY_MISMATCH"


def test_duplicate_candidate_declarations_are_rejected() -> None:
    candidate = _candidate("candidate", (1, 0))
    admitted = _admit(candidate)
    result = route_declared_batch(_search(), (admitted, admitted))
    assert isinstance(result, Err)
    assert result.error.code == "DUPLICATE_CANDIDATE"


def test_repair_and_extension_governance_classes_never_merge_definitionally() -> None:
    term = _term("shared")
    repair = _candidate("repair", (1, 0), term=term)
    extension = _candidate(
        "extension",
        (1, 0),
        term=term,
        kind=PlanKind.STRUCTURE_EXTENSION,
    )
    same_term_path = identity_path2(term)
    assert isinstance(same_term_path, Ok)
    result = route_declared_batch(
        _search(),
        (_admit(repair), _admit(extension)),
        (same_term_path.value,),
    )
    assert isinstance(result, Ok)
    assert len(result.value.classes) == 2
    assert {item.kind for item in result.value.classes} == {
        PlanKind.SAME_LEVEL_REPAIR,
        PlanKind.STRUCTURE_EXTENSION,
    }


def test_equivalence_endpoint_outside_batch_is_rejected() -> None:
    candidate = _candidate("candidate", (1, 0))
    outsider = _term("outsider")
    path = identity_path2(outsider)
    assert isinstance(path, Ok)
    result = route_declared_batch(
        _search(),
        (_admit(candidate),),
        (path.value,),
    )
    assert isinstance(result, Err)
    assert result.error.code == "EQUIVALENCE_ENDPOINT_OUTSIDE_BATCH"


def test_frontier_never_mints_authority() -> None:
    candidate = _candidate("candidate", (1, 0))
    result = route_declared_batch(_search(), (_admit(candidate),))
    assert isinstance(result, Ok)
    assert result.value.authority_effect.value == "None"
    assert result.value.classes[0].authority_effect.value == "None"


def test_declared_finite_grammar_requires_every_candidate_evaluation() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    grammar = FinitePlanGrammarV1("grammar.test", (left, right))
    search = SearchDeclarationV1(
        "grammar.test",
        grammar.canonical_id,
        _digest("policy"),
        CostOrder.LEXICOGRAPHIC,
        2,
        2,
    )
    result = route_declared_finite_grammar(
        search,
        grammar,
        (_admit(left),),
    )
    assert isinstance(result, Err)
    assert result.error.code == "INCOMPLETE_GRAMMAR_EVALUATION"


def test_declared_finite_grammar_rejects_extra_candidate() -> None:
    member = _candidate("member", (1, 0))
    outsider = _candidate("outsider", (1, 0))
    grammar = FinitePlanGrammarV1("grammar.test", (member,))
    search = SearchDeclarationV1(
        "grammar.test",
        grammar.canonical_id,
        _digest("policy"),
        CostOrder.LEXICOGRAPHIC,
        2,
        2,
    )
    result = route_declared_finite_grammar(
        search,
        grammar,
        (_admit(member), _admit(outsider)),
    )
    assert isinstance(result, Err)
    assert result.error.code == "INCOMPLETE_GRAMMAR_EVALUATION"


def test_declared_finite_grammar_binds_content_digest() -> None:
    candidate = _candidate("candidate", (1, 0))
    grammar = FinitePlanGrammarV1("grammar.test", (candidate,))
    search = SearchDeclarationV1(
        "grammar.test",
        _digest("wrong-grammar"),
        _digest("policy"),
        CostOrder.LEXICOGRAPHIC,
        2,
        1,
    )
    result = route_declared_finite_grammar(
        search,
        grammar,
        (_admit(candidate),),
    )
    assert isinstance(result, Err)
    assert result.error.code == "GRAMMAR_DIGEST_MISMATCH"


def test_complete_declared_finite_grammar_routes_all_co_minima() -> None:
    left = _candidate("left", (1, 0))
    right = _candidate("right", (1, 0))
    grammar = FinitePlanGrammarV1("grammar.test", (right, left))
    search = SearchDeclarationV1(
        "grammar.test",
        grammar.canonical_id,
        _digest("policy"),
        CostOrder.LEXICOGRAPHIC,
        2,
        2,
    )
    result = route_declared_finite_grammar(
        search,
        grammar,
        (_admit(right), _admit(left)),
    )
    assert isinstance(result, Ok)
    assert len(result.value.classes) == 2
    assert set(result.value.accepted_candidate_ids) == {
        left.canonical_id,
        right.canonical_id,
    }
