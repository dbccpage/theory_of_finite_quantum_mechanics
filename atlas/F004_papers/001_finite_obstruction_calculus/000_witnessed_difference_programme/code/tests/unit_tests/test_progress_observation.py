"""Congruence sufficiency, its finite construction, and reporting boundaries."""

from fractions import Fraction

import pytest
from certified_progress import compile_model, solve_progress
from certified_progress.fixtures import cheaper_route
from certified_progress.model import ModelError, graph_model
from certified_progress.observation import is_congruence, quotient_model, refine_observation
from certified_progress.reporting import report_termination


def test_structural_congruence_preserves_value_and_refinement_stabilizes():
    model = graph_model({"s": [("choose", "1", ["p", "q"])],
                         "p": [("finish", "1", ["t"])], "q": [("finish", "1", ["t"])]})
    model["authorization"] = {"effect": "None", "note": "kept"}
    blocks = [[["s"]], [["p"], ["q"]], [["t"]]]
    assert is_congruence(model, blocks)
    quotient = quotient_model(model, blocks)
    assert quotient["authorization"] == {"effect": "None", "note": "kept"}
    from certified_progress import check_certificate
    original_value = check_certificate(model, solve_progress(model)["certificate"])["initial_value"]
    quotient_value = check_certificate(quotient, solve_progress(quotient)["certificate"])["initial_value"]
    assert original_value == quotient_value == "2"
    refined = refine_observation(model, [[[b for b in belief] for belief in compile_model(model).reachable]])
    assert refined["strict_rounds"] <= refined["round_bound"]
    assert is_congruence(model, refined["blocks"])
    assert refine_observation(model, refined["blocks"])["strict_rounds"] == 0


def test_accidental_value_equality_does_not_require_congruence():
    graph = {"s": [("choose", "1", ["p", "q"])],
             "p": [("d", "1", ["t"]), ("a", "2", ["t"])],
             "q": [("d", "1", ["t"]), ("b", "2", ["t"])]}
    model = graph_model(graph)
    blocks = [[["s"]], [["p"], ["q"]], [["t"]]]
    assert not is_congruence(model, blocks)
    with pytest.raises(ModelError, match="congruence"):
        quotient_model(model, blocks)
    from certified_progress.fixtures import value_at
    assert value_at(solve_progress(graph_model(graph, initial="p"))["certificate"], "p") == 1
    assert value_at(solve_progress(graph_model(graph, initial="q"))["certificate"], "q") == 1
    retargeted = graph_model(graph, initial="q", targets=("p",))
    assert solve_progress(retargeted)["certificate"]["kind"] == "LOSS"


def test_targets_costs_enabled_actions_and_successor_classes_all_refine():
    graph = {"s": [("choose", "1", ["p", "q"])],
             "p": [("go", "1", ["t"])], "q": [("go", "2", ["t"])]}
    model = graph_model(graph)
    all_one = [[list(b) for b in compile_model(model).reachable]]
    result = refine_observation(model, all_one)
    assert len(result["blocks"]) == 4
    assert result["strict_rounds"] <= result["round_bound"] == 3


def test_partition_must_be_an_exact_cover():
    with pytest.raises(ModelError, match="cover"):
        refine_observation(cheaper_route(), [[["s"]]])


def test_exhaustion_requires_optimal_finite_cost():
    model = cheaper_route()
    cert = solve_progress(model)["certificate"]
    assert report_termination(model, cert, "3/2")["termination"] == "Exhausted"
    assert report_termination(model, cert, "2")["termination"] == "ResolvedWithinBudget"
    cert["strategy"][0]["action"] = "direct"
    cert["values"][0]["value"] = "5"
    cert.update(kind="WIN_FEASIBLE", optimality_requested=False)
    assert report_termination(model, cert, "3")["termination"] == "UndeterminedBudget"


def test_loss_stall_and_successful_zero_cost_terminal_have_distinct_reports():
    active = graph_model({"s": [("loop", "1", ["s"])]})
    cert = solve_progress(active)["certificate"]
    assert report_termination(active, cert, "4")["termination"] == "LosingInDeclaredArena"
    assert report_termination(active, cert, "4", task_admits_impossibility=True)["termination"] == "Impossible"
    stalled = graph_model({"s": []})
    assert report_termination(stalled, solve_progress(stalled)["certificate"], "4",
                              task_admits_impossibility=True)["termination"] == "Stalled"
    successful = graph_model({"s": []}, targets=("s",))
    assert report_termination(successful, solve_progress(successful)["certificate"], "0")["termination"] == "ResolvedWithinBudget"


def test_optional_actions_cannot_raise_value_and_setup_payback_is_separate():
    base = graph_model({"s": [("direct", "5", ["t"])]})
    improved = cheaper_route()
    from certified_progress.fixtures import value_at
    difference = value_at(solve_progress(base)["certificate"], "s") - value_at(solve_progress(improved)["certificate"], "s")
    assert difference == 3
    assert not difference > Fraction(4)  # Operating improvement does not pay setup 4.
    assert difference > Fraction(2)
