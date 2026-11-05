from copy import deepcopy
from fractions import Fraction

from certified_progress.calculus import (
    bindings,
    bound_model,
    check_bound_progress,
    check_progress_with_resolutions,
    inputs,
    local_episode,
    task_checker,
)
from certified_progress.checker import check_certificate
from certified_progress.fixtures import cheaper_route, value_at
from certified_progress.model import compile_model, digest, graph_model
from certified_progress.observation import is_congruence, refine_observation
from certified_progress.producer import solve_progress
from certified_progress.structural import check_quotient, check_refinement


def test_actual_bound_calculus_resolution_and_rejection_controls():
    model = bound_model()
    c = solve_progress(model)["certificate"]
    episode = local_episode()
    assert check_bound_progress(model, c, episode)
    assert value_at(c, "ready") == 3
    feasible = deepcopy(c)
    feasible.update(kind="WIN_FEASIBLE", optimality_requested=False)
    assert check_certificate(model, feasible)["accepted"]
    assert not check_bound_progress(model, feasible, episode)
    for key in ("task", "candidate", "checker_sha256", "proposal_sha256"):
        bad = deepcopy(episode)
        bad["bindings"][key] = "0" * 64
        assert not check_bound_progress(model, c, bad)
    bad = deepcopy(episode)
    bad["submitted"]["antiderivative_coefficients"] = ["0", "5"]
    assert not check_bound_progress(model, c, bad)
    bad_model = deepcopy(model)
    bad_model["authorization"]["effect"] = "publish"
    assert not check_bound_progress(bad_model, c, episode)


def test_unhelpful_forever_is_loss_and_optional_shortcut_costs():
    loss_model = bound_model(allow_archive=False)
    loss = solve_progress(loss_model)["certificate"]
    assert loss["kind"] == "LOSS"
    assert check_certificate(loss_model, loss)["accepted"]
    old = solve_progress(bound_model())["certificate"]
    new = solve_progress(bound_model(shortcut=True))["certificate"]
    assert value_at(new, "ready") == Fraction(1, 2) < value_at(old, "ready")
    # Setup 8 costs more for one episode; after four uses, total cost falls.
    assert 8 + Fraction(1, 2) > 3
    assert 8 + 4 * Fraction(1, 2) < 4 * 3


def test_indistinguishable_actions_and_cheap_two_step():
    model = graph_model(
        {"a": [("left", "1", ["t"])], "b": [("right", "1", ["t"])]}, initial=["a", "b"]
    )
    loss = solve_progress(model)["certificate"]
    assert loss["kind"] == "LOSS" and check_certificate(model, loss)["accepted"]
    cheap = solve_progress(cheaper_route())["certificate"]
    assert value_at(cheap, "s") == 2
    assert next(r["action"] for r in cheap["strategy"] if r["belief"] == ["s"]) == "step"


def test_exact_quotient_iff_structural_tables_and_coarsest_refinement():
    model = graph_model(
        {
            "s": [("fork", "1", ["u", "v"])],
            "u": [("finish", "2", ["t"])],
            "v": [("finish", "2", ["t"])],
        }
    )
    arena = compile_model(model)
    blocks = [[["s"]], [["t"]], [["u"], ["v"]]]
    table = [
        {
            "target": False,
            "resolutions": [],
            "moves": [{"action": "fork", "cost": "1", "successors": [2]}],
        },
        {"target": True, "resolutions": [], "moves": []},
        {
            "target": False,
            "resolutions": [],
            "moves": [{"action": "finish", "cost": "2", "successors": [1]}],
        },
    ]
    assert check_quotient(model, blocks, table)
    assert is_congruence(model, blocks)
    changed = deepcopy(table)
    changed[2]["moves"][0]["cost"] = "1"
    assert not check_quotient(model, blocks, changed)
    seed = [[list(b) for b in arena.reachable]]
    final = refine_observation(model, seed)["blocks"]
    # Here one signature split is already stable. A repeated final step proves fixedness.
    cert = {"model_digest": digest(model), "rounds": [final, final]}
    assert check_refinement(model, seed, cert)
    cert["rounds"][0] = seed
    assert not check_refinement(model, seed, cert)


def test_accidental_value_equality_is_not_exactness():
    model = graph_model(
        {
            "i": [("fork", "1", ["s", "u"])],
            "s": [("direct", "2", ["t"]), ("extra", "7", ["t"])],
            "u": [("direct", "2", ["t"])],
        },
        initial="i",
    )
    # Equal current output "pending" and same optimal direct cost, but enabled sets differ.
    blocks = [[["i"]], [["s"], ["u"]], [["t"]]]
    assert not is_congruence(model, blocks)


def test_source_sound_antibody_is_not_valid_after_task_change():
    original, _, bad = inputs()
    checker = task_checker()
    assert checker.check(original, bad)["status"] == "invalid_witness"
    target = dict(original, integrand_coefficients=["5"])
    valid_target = dict(bad, input_sha256=checker.canonical_sha(target))
    assert checker.check(target, valid_target)["status"] == "checked_accept"
    assert bindings()["task"] != digest(target)


def test_budget_cutoff_is_not_impossibility():
    model = bound_model()
    outcome = solve_progress(model, max_horizon=0)
    assert outcome["status"] == "Undetermined" and outcome["certificate"] is None
    assert solve_progress(model)["certificate"]["kind"] == "WIN_OPTIMAL"


def test_generic_binding_requires_actual_checker_and_common_resolution():
    model = bound_model()
    c = solve_progress(model)["certificate"]
    p, good, bad = inputs()
    assert not check_progress_with_resolutions(model, c, p, {"answer-50": good}, lambda *_: False)
    assert not check_progress_with_resolutions(model, c, p, {"answer-50": good}, lambda *_: 1)
    assert not check_progress_with_resolutions(
        model,
        c,
        p,
        {"answer-50": bad},
        lambda p, _s, r: task_checker().check(p, r)["status"] == "checked_accept",
    )
    assert not check_progress_with_resolutions(
        model, c, dict(p, upper="11"), {"answer-50": good}, lambda *_: True
    )


def test_same_current_report_and_actions_can_lose_cost_information():
    model = graph_model(
        {
            "i": [("fork", "1", ["s", "u"])],
            "s": [("finish", "2", ["t"])],
            "u": [("finish", "9", ["t"])],
        },
        initial="i",
    )
    c = solve_progress(model)["certificate"]
    assert value_at(c, "s") == 2 and value_at(c, "u") == 9
    assert not is_congruence(model, [[["i"]], [["s"], ["u"]], [["t"]]])
