"""Actual forged witnesses and independent finite policy enumeration."""

from __future__ import annotations

import copy
from fractions import Fraction
from itertools import product

import pytest
from certified_progress import check_certificate, compile_model, solve_progress
from certified_progress.fixtures import cheaper_route, value_at
from certified_progress.model import ModelError, graph_model


def accepted(model):
    result = solve_progress(model)
    receipt = check_certificate(model, result["certificate"])
    assert receipt["accepted"], receipt
    return result["certificate"]


def test_cheap_two_step_policy_uses_its_own_rank():
    model = cheaper_route()
    result = solve_progress(model)
    cert = result["certificate"]
    assert check_certificate(model, cert)["accepted"]
    assert value_at(cert, "s") == 2
    assert next(r["rank"] for r in result["producer"]["attractor_rank"] if r["belief"] == ["s"]) == 1
    assert next(r["rank"] for r in cert["ranks"] if r["belief"] == ["s"]) == 2


def test_fabricated_stall_cannot_hide_the_cheaper_route():
    model = cheaper_route()
    cert = accepted(model)
    cert["winning"] = [["s"], ["t"]]
    cert["losing"] = cert["stalled"] = [["u"]]
    cert["strategy"] = [{"belief": ["s"], "action": "direct"}]
    cert["ranks"] = [{"belief": ["s"], "rank": 1}, {"belief": ["t"], "rank": 0}]
    cert["values"] = [{"belief": ["s"], "value": "5"}, {"belief": ["t"], "value": "0"}]
    receipt = check_certificate(model, cert)
    assert not receipt["accepted"] and "stalled" in receipt["reason"]


def test_shifted_terminal_value_does_not_preserve_the_boundary_condition():
    model = graph_model({"s": [("finish", "1", ["t"])]})
    cert = accepted(model)
    for row in cert["values"]:
        row["value"] = "101" if row["belief"] == ["s"] else "100"
    assert "terminal value" in check_certificate(model, cert)["reason"]


def test_empty_win_omitting_losing_initial_state_refuses():
    model = graph_model({"s": [("loop", "1", ["s"])]})
    cert = accepted(model)
    cert.update(kind="WIN_OPTIMAL", optimality_requested=True, losing=[], stalled=[], closure=[])
    assert "initial belief" in check_certificate(model, cert)["reason"]


@pytest.mark.parametrize("with_actions", [False, True])
def test_successful_terminal_cannot_be_a_stall_or_trap(with_actions):
    graph = {"s": [("loop", "1", ["s"])]} if with_actions else {"s": []}
    source = graph_model(graph)
    cert = accepted(source)
    terminal_model = graph_model(graph, targets=("s", "t"))
    from certified_progress.model import digest
    cert["model_digest"] = digest(terminal_model)
    assert "successful terminal" in check_certificate(terminal_model, cert)["reason"]


def test_loss_win_fields_must_be_empty_lists():
    model = graph_model({"s": [("step", "1", ["d"])]})
    cert = accepted(model)
    for bad in (None, 0, "", False, {}):
        forged = copy.deepcopy(cert)
        forged["strategy"] = bad
        assert "win fields" in check_certificate(model, forged)["reason"]


def test_loss_producer_keeps_dead_ends_inside_the_trap():
    model = graph_model({"s": [("step", "1", ["d"])]})
    cert = accepted(model)
    assert cert["kind"] == "LOSS"
    assert cert["losing"] == [["d"], ["s"]] and cert["stalled"] == [["d"]]
    assert cert["closure"][0]["successor"] == ["d"]


def test_win_with_losing_branch_through_a_dead_end_produces_valid_partition():
    model = graph_model({"s": [("finish", "1", ["t"]), ("detour", "1", ["u"])],
                         "u": [("step", "1", ["d"])]})
    cert = accepted(model)
    assert cert["kind"] == "WIN_OPTIMAL" and value_at(cert, "s") == 1
    assert cert["losing"] == [["d"], ["u"]]


def test_avoidable_trap_does_not_certify_loss_of_initial_state():
    model = graph_model({"s": [("finish", "5", ["t"]), ("detour", "1", ["l"])],
                         "l": [("loop", "1", ["l"])]})
    cert = accepted(model)
    cert.update(kind="LOSS", optimality_requested=False, winning=[], values=[], ranks=[], strategy=[])
    assert "initial belief outside" in check_certificate(model, cert)["reason"]


def test_every_stalled_claim_is_checked_not_only_the_initial_state():
    model = graph_model({"s": [("next", "1", ["u"])], "u": [("loop", "1", ["u"])]})
    cert = accepted(model)
    cert["stalled"] = [["u"]]
    assert "stalled" in check_certificate(model, cert)["reason"]


def test_complete_partition_and_exact_map_domains():
    model = cheaper_route()
    cert = accepted(model)
    cert["winning"].remove(["u"])
    assert "partition" in check_certificate(model, cert)["reason"]


@pytest.mark.parametrize("field", ["values", "ranks", "strategy", "resolutions"])
def test_extraneous_or_missing_certificate_maps_refuse(field):
    model = cheaper_route()
    cert = accepted(model)
    if field == "resolutions":
        cert[field] = [{"belief": ["s"], "resolution": "invented"}]
    else:
        cert[field].pop()
    assert not check_certificate(model, cert)["accepted"]


@pytest.mark.parametrize("value", ["-1", "NaN", "Infinity", 0, False, 1.5])
def test_values_are_finite_nonnegative_rational_strings(value):
    model = cheaper_route()
    cert = accepted(model)
    cert["values"][0]["value"] = value
    assert not check_certificate(model, cert)["accepted"]


@pytest.mark.parametrize("rank", [-1, True, 1.5, "1"])
def test_ranks_are_naturals_with_exact_types(rank):
    model = cheaper_route()
    cert = accepted(model)
    cert["ranks"][0]["rank"] = rank
    assert not check_certificate(model, cert)["accepted"]


@pytest.mark.parametrize("field", ["model_digest", "task_id", "assumptions", "authorization", "initial"])
def test_wrong_model_assumptions_authorization_and_initial_bindings_refuse(field):
    model = cheaper_route()
    cert = accepted(model)
    cert[field] = {"effect": "grant"} if field == "authorization" else (["t"] if field == "initial" else "changed")
    assert not check_certificate(model, cert)["accepted"]


def test_feasibility_is_distinct_from_optimality():
    model = cheaper_route()
    cert = accepted(model)
    cert["strategy"][0]["action"] = "direct"
    cert["values"][0]["value"] = "5"
    assert "cheaper action" in check_certificate(model, cert)["reason"]
    cert.update(kind="WIN_FEASIBLE", optimality_requested=False)
    assert check_certificate(model, cert)["claim"] == "WIN_FEASIBLE"
    cert["kind"] = "WIN_OPTIMAL"
    assert "optimality obligation" in check_certificate(model, cert)["reason"]


def test_resolution_witnesses_replay_supplied_checks_and_bind_model():
    model = graph_model({"s": [("emit", "1/2", ["t"])]}, emissions={"emit": "answer"},
                        valid_resolutions={"s": ["answer"]})
    cert = accepted(model)
    assert cert["resolutions"] == [{"belief": ["s"], "resolution": "answer"}]
    cert["resolutions"][0]["resolution"] = "unproved"
    assert not check_certificate(model, cert)["accepted"]


def test_immediate_valid_emission_only_gives_an_upper_bound():
    model = graph_model({"s": [("emit_direct", "5", ["t"]), ("inspect", "1", ["u"])],
                         "u": [("emit_cheap", "1", ["t"])]},
                        emissions={"emit_direct": "answer", "emit_cheap": "answer"},
                        valid_resolutions={"s": ["answer"], "u": ["answer"]})
    assert value_at(accepted(model), "s") == 2


def test_unsound_restrictive_guard_can_leave_a_more_expensive_win():
    base = graph_model({"s": [("emit_direct", "1", ["t"]), ("repair", "1", ["u"])],
                        "u": [("emit_later", "1", ["t"])]})
    guarded = graph_model({"s": [("repair", "1", ["u"])], "u": [("emit_later", "1", ["t"])]})
    assert value_at(accepted(base), "s") == 1
    assert value_at(accepted(guarded), "s") == 2


def test_optional_self_loop_preserves_triangle_classification_win():
    valid = {s: ["non-exact"] for s in ("d1", "d2", "d3")}
    graph = {s: [("emit", "1/2", ["t"]), ("ab", "1", [s])] for s in valid}
    model = graph_model(graph, initial=list(valid), emissions={"emit": "non-exact"},
                        valid_resolutions=valid,
                        observations={(s, "ab"): "same" for s in valid})
    cert = accepted(model)
    assert Fraction(check_certificate(model, cert)["initial_value"]) == Fraction(1, 2)
    identification = graph_model({s: [("ab", "1", [s])] for s in valid}, initial=list(valid),
                                 observations={(s, "ab"): "same" for s in valid})
    assert accepted(identification)["kind"] == "LOSS"


def test_exact_triangle_obstruction_has_independent_primal_and_dual_values(monkeypatch):
    from fractions import Fraction as Q
    from witnessed_difference.obstruction import MatrixQuotientCertificate, verify_matrix_certificate
    from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
    import native_wdp
    import witnessed_difference.native_functionals as nf
    import witnessed_difference.obstruction

    d0_columns = [(-1, 0, -1), (1, -1, 0), (0, 1, 1)]
    dual = (1, 1, -1)
    assert all(sum(x*y for x, y in zip(column, dual)) == 0 for column in d0_columns)
    assert max(abs(x) for x in dual) == 1
    for defect, expected in [((0, 1, 0), 1), ((1, 1, 0), 2), ((0, 2, 0), 2)]:
        certificate = MatrixQuotientCertificate(
            tuple(tuple(map(Q, row)) for row in zip(*d0_columns)), 3, tuple(map(Q, defect)),
            (Q(1),)*3, (Q(0),)*3, tuple(map(Q, defect)), Q(expected), tuple(map(Q, dual)))
        assert isinstance(verify_matrix_certificate(certificate), Accepted)

    # Missing executable path must yield RefusalCode.NO_RULE, never CERTIFICATE_MISMATCH
    sample_cert = MatrixQuotientCertificate(
        tuple(tuple(map(Q, row)) for row in zip(*d0_columns)), 3, (Q(0), Q(1), Q(0)),
        (Q(1),)*3, (Q(0),)*3, (Q(0), Q(1), Q(0)), Q(1), tuple(map(Q, dual)))
    monkeypatch.setattr(native_wdp, "find_binary", lambda *_, **__: None)
    outcome_missing = verify_matrix_certificate(sample_cert)
    assert isinstance(outcome_missing, Refused)
    assert outcome_missing.code == RefusalCode.NO_RULE
    assert outcome_missing.code != RefusalCode.CERTIFICATE_MISMATCH

    # Simulated timeout path must yield RefusalCode.BUDGET_EXHAUSTED, never CERTIFICATE_MISMATCH
    def mock_timeout(*_, **__):
        raise nf.NativeTimeoutError("simulated timeout")
    monkeypatch.setattr(witnessed_difference.obstruction, "evaluate", mock_timeout)
    outcome_timeout = verify_matrix_certificate(sample_cert)
    assert isinstance(outcome_timeout, Refused)
    assert outcome_timeout.code == RefusalCode.BUDGET_EXHAUSTED
    assert outcome_timeout.code != RefusalCode.CERTIFICATE_MISMATCH


def test_dynamic_posterior_uses_post_state_not_prior_or_whole_fibre():
    model = graph_model({"0": [("a", "1", ["1"])], "2": [("a", "1", ["2"])]},
                        initial="0", targets=("1",), observations={("1", "a"): "o", ("2", "a"): "o"})
    arena = compile_model(model)
    assert arena.moves(("0",))[0][2] == (("1",),)


def test_indistinguishable_states_can_each_win_while_the_belief_stalls():
    graph = {"p": [("a", "1", ["t"])], "q": [("b", "1", ["t"])]}
    assert accepted(graph_model(graph, initial="p"))["kind"] == "WIN_OPTIMAL"
    assert accepted(graph_model(graph, initial="q"))["kind"] == "WIN_OPTIMAL"
    assert accepted(graph_model(graph, initial=["p", "q"]))["kind"] == "LOSS"


def test_horizon_budget_exhaustion_is_undetermined_not_loss():
    result = solve_progress(cheaper_route(), max_horizon=0)
    assert result["status"] == "Undetermined" and result["certificate"] is None


def test_checker_never_calls_producer_and_never_mutates_inputs(monkeypatch):
    model = cheaper_route()
    cert = accepted(model)
    original = copy.deepcopy((model, cert))
    import certified_progress.producer as producer
    monkeypatch.setattr(producer, "solve_progress", lambda *_: pytest.fail("checker called solver"))
    assert check_certificate(model, cert)["accepted"]
    assert (model, cert) == original


def test_model_rejects_empty_transitions_and_nonpositive_costs():
    model = cheaper_route()
    model["transitions"][0]["successors"] = []
    with pytest.raises(ModelError):
        compile_model(model)
    model = cheaper_route()
    model["costs"][0]["cost"] = "0"
    with pytest.raises(ModelError):
        compile_model(model)


def independent_policy_value(graph, start="s", target="t"):
    states = sorted(graph)
    alternatives = [graph[s] or [None] for s in states]
    best = None
    for chosen in product(*alternatives):
        policy = dict(zip(states, chosen))

        def evaluate(s, history):
            if s == target:
                return Fraction(0)
            if s in history or policy.get(s) is None:
                return None
            _, cost, successors = policy[s]
            values = [evaluate(y, history | {s}) for y in successors]
            return None if any(v is None for v in values) else Fraction(cost) + max(values)

        value = evaluate(start, set())
        if value is not None and (best is None or value < best):
            best = value
    return best


def test_exhaustive_three_state_games_against_independent_policy_enumeration():
    # Each of four possible state/action rows is absent or has one of seven
    # nonempty successor sets. This is all 8^4 = 4096 such finite games.
    states = ("s", "u", "t")
    subsets = [None] + [tuple(states[i] for i in range(3) if mask & (1 << i)) for mask in range(1, 8)]
    checked = 0
    for rows in product(subsets, repeat=4):
        graph = {"s": [], "u": []}
        for (s, a, cost), successors in zip(
                [("s", "a", "1"), ("s", "b", "2"), ("u", "a", "1"), ("u", "b", "2")], rows):
            if successors is not None:
                graph[s].append((a, cost, successors))
        model = graph_model(graph)
        cert = accepted(model)
        expected = independent_policy_value(graph)
        if expected is None:
            assert cert["kind"] == "LOSS"
        else:
            assert cert["kind"] == "WIN_OPTIMAL" and value_at(cert, "s") == expected
        checked += 1
    assert checked == 4096
