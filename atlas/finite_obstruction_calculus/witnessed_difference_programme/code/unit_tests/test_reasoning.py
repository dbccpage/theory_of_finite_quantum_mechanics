"""Independent valuation and graph oracles, plus adversarial certificate mutations."""

from dataclasses import replace
from itertools import product

import pytest
from witnessed_difference.reasoning import (
    BudgetExhausted,
    Countermodel,
    Proof,
    ProofStep,
    Rule,
    Theory,
    check_countermodel,
    check_path,
    check_proof,
    decode_path,
    graph_theory,
    report_collision,
    solve,
)


def subsets(items):
    return [tuple(x for x, keep in zip(items, mask) if keep)
            for mask in product((False, True), repeat=len(items))]


def test_all_two_atom_theories_against_truth_tables():
    carrier = (0, 1)
    rules = tuple(Rule(p, q) for p in subsets(carrier) for q in carrier)
    count = 0
    for chosen in subsets(rules):
        for facts in subsets(carrier):
            theory = Theory(("a", "b"), frozenset(facts), chosen)
            models = [v for v in product((False, True), repeat=2)
                      if all(v[a] for a in facts) and
                      all(not all(v[a] for a in r.premises) or v[r.conclusion] for r in chosen)]
            for goal in carrier:
                result = solve(theory, goal)
                entails = all(v[goal] for v in models)
                assert isinstance(result, Proof) == entails
                if entails:
                    assert check_proof(theory, goal, result)
                else:
                    assert isinstance(result, Countermodel)
                    assert check_countermodel(theory, goal, result)
                count += 1
    assert count == 2048


def test_all_three_node_graphs_against_independent_paths():
    nodes = ("a", "b", "c")
    count = 0
    for edges in subsets(tuple(product(range(3), repeat=2))):
        for start, goal in product(range(3), repeat=2):
            paths = [(start,) + middle + (goal,)
                     for length in range(2) for middle in product(range(3), repeat=length)]
            if start == goal:
                paths.append((start,))
            reachable = any(check_path(nodes, edges, start, goal, p) for p in paths)
            theory = graph_theory(nodes, edges, start)
            result = solve(theory, goal)
            assert isinstance(result, Proof) == reachable
            if reachable:
                path = decode_path(nodes, edges, start, goal, result)
                assert check_path(nodes, edges, start, goal, path)
            else:
                assert check_countermodel(theory, goal, result)
            count += 1
    assert count == 4608


def test_certificate_mutations_and_task_binding():
    t = Theory(("a", "b", "c"), frozenset({0}), (Rule((0,), 1), Rule((1,), 2)))
    p = solve(t, 2)
    assert check_proof(t, 2, p)
    mutations = [
        replace(p, theory_digest="wrong"), replace(p, goal=1), replace(p, goal=True),
        replace(p, steps=()), replace(p, steps=p.steps[:-1]),
        replace(p, steps=(ProofStep(1, None),) + p.steps[1:]),
        replace(p, steps=(ProofStep(True, None),) + p.steps[1:]),
        replace(p, steps=p.steps[:1] + (ProofStep(1, 0, (1,)),) + p.steps[2:]),
        replace(p, steps=p.steps[:1] + (ProofStep(1, 0, (True,)),) + p.steps[2:]),
        replace(p, steps=p.steps[:1] + (ProofStep(1, 0, ()),) + p.steps[2:]),
        replace(p, steps=p.steps[:2] + (ProofStep(2, 0, (0,)),)),
        replace(p, steps=p.steps[:2] + (ProofStep(2, 2, (1,)),)),
        replace(p, steps=p.steps[:2] + (ProofStep(2, True, (1,)),)),
    ]
    assert all(not check_proof(t, 2, bad) for bad in mutations)
    for altered in [replace(t, atoms=("other", "b", "c")),
                    replace(t, facts=frozenset()), replace(t, rules=t.rules[:1])]:
        assert not check_proof(altered, 2, p)
    assert not check_proof(t, 1, p)
    nodes, edges = t.atoms, ((0, 1), (1, 2))
    assert decode_path(nodes, edges, 0, 2, p) == (0, 1, 2)
    assert decode_path(nodes, ((0, 1),), 0, 2, p) is None
    assert not check_path(nodes, ((0, 1),), 0, 2, (0, 1, 2))


def test_countermodel_mutations_and_budget():
    t = Theory(("a", "b", "c"), frozenset({0}), (Rule((0,), 1),))
    m = solve(t, 2)
    assert check_countermodel(t, 2, m)
    for bad in [replace(m, true_atoms=frozenset()),
                replace(m, true_atoms=frozenset({0})),
                replace(m, true_atoms=frozenset({0, 1, 2})),
                replace(m, true_atoms=frozenset({0, 1, 3})),
                replace(m, theory_digest="wrong"), replace(m, goal=1)]:
        assert not check_countermodel(t, 2, bad)
    assert isinstance(solve(t, 1, budget=1), BudgetExhausted)
    assert isinstance(solve(t, 1, budget=2), Proof)
    assert isinstance(solve(t, 2, budget=2), Countermodel)
    assert not check_countermodel(t, 2, BudgetExhausted(1))


def test_inert_seed_cycles_zero_premises_and_conservative_reuse():
    empty = Theory(("<> can reason",), frozenset(), ())
    assert isinstance(solve(empty, 0, 0), Countermodel)
    cycle = Theory(("a", "b"), frozenset(), (Rule((0,), 1), Rule((1,), 0)))
    assert isinstance(solve(cycle, 0), Countermodel)
    admitted = replace(cycle, rules=cycle.rules + (Rule((), 0),))
    p = solve(admitted, 1)
    assert check_proof(admitted, 1, p)
    learned = replace(admitted, facts=frozenset({1}))
    assert all(isinstance(solve(admitted, a), Proof) == isinstance(solve(learned, a), Proof)
               for a in (0, 1))
    assert not check_proof(cycle, 1, p)
    duplicate = Theory(("a", "b"), frozenset({0}), (Rule((0, 0), 1),))
    assert check_proof(duplicate, 1, solve(duplicate, 1))


def test_information_limits_need_target_separation_and_all_histories():
    assert report_collision((0, 0), (0, 1)) == (1, 0)
    assert report_collision((0, 0), (1, 1)) is None
    states = ((0, 0), (0, 1))
    def observe(s):
        return s[0]

    def swap(s):
        return (s[1], s[0])
    assert observe(states[0]) == observe(states[1])
    assert observe(swap(states[0])) != observe(swap(states[1]))
    with pytest.raises(ValueError):
        report_collision((0,), ())


@pytest.mark.parametrize("theory", [
    lambda: Theory(("a", "a"), frozenset(), ()),
    lambda: Theory(("",), frozenset(), ()),
    lambda: Theory(("a",), frozenset({True}), ()),
    lambda: Theory((), frozenset({0}), ()),
    lambda: Theory(("a",), frozenset(), (Rule((1,), 0),)),
    lambda: graph_theory(("a",), ((0, 1),), 0),
])
def test_invalid_source_is_refused(theory):
    with pytest.raises(ValueError):
        theory()


@pytest.mark.parametrize("goal,budget", [(True, 1), (1, 1), (0, -1), (0, True)])
def test_invalid_query_is_refused(goal, budget):
    with pytest.raises(ValueError):
        solve(Theory(("a",), frozenset(), ()), goal, budget)
