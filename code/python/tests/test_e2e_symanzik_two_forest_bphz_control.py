"""End-to-end tests for QM-214: Second Symanzik 2-forest polynomial F_G(alpha; q, m^2),
DFM spanning-tree momentum routing, and Zimmermann BPHZ forest renormalization.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/symanzik_two_forest.py
Claim: DivergentSubgraph certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.symanzik_two_forest_bphz_control import (
    DivergentSubgraph,
    bphz_two_loop_nested_sector_integrand,
    bubble_graph,
    dfm_loop_eliminated_f0,
    diamond_graph,
    enumerate_spanning_trees,
    enumerate_spanning_two_forests,
    enumerate_zimmermann_forests,
    evaluate_symanzik_two_forest_bphz_control,
    kirchhoff_schur_symanzik_f0,
    symanzik_f0_polynomial,
    symanzik_f_polynomial,
    symanzik_u_polynomial,
    tree_routed_edge_momenta,
    triangle_graph,
    vertex_divergence_of_edge_flow,
)

Q = Fraction


def test_unit_part_a_bubble_and_triangle_symanzik_f_and_kirchhoff_duality() -> None:
    bub = bubble_graph()
    alpha_bub = [Q(2), Q(3)]
    q_bub = [(Q(5), Q(-2)), (Q(-5), Q(2))]
    m2_bub = [Q(7), Q(11)]
    assert symanzik_u_polynomial(bub, alpha_bub) == Q(5)
    assert symanzik_f0_polynomial(bub, alpha_bub, q_bub) == Q(2 * 3 * 29)
    assert kirchhoff_schur_symanzik_f0(bub, alpha_bub, q_bub) == Q(174)
    assert symanzik_f_polynomial(bub, alpha_bub, q_bub, m2_bub) == Q(409)

    tri = triangle_graph()
    alpha_tri = [Q(2), Q(3), Q(5)]
    q_tri = [(Q(1), Q(2)), (Q(3), Q(-1)), (Q(-4), Q(-1))]
    assert symanzik_u_polynomial(tri, alpha_tri) == Q(10)
    assert symanzik_f0_polynomial(tri, alpha_tri, q_tri) == Q(365)
    assert kirchhoff_schur_symanzik_f0(tri, alpha_tri, q_tri) == Q(365)


def test_part_a_diamond_two_loop_two_forests_match_kirchhoff_schur() -> None:
    dia = diamond_graph()
    assert len(enumerate_spanning_trees(dia)) == 8
    assert len(enumerate_spanning_two_forests(dia)) == 10

    alpha_dia = [Q(2), Q(3), Q(5), Q(7), Q(11)]
    q_dia = [(Q(2), Q(1)), (Q(-1), Q(3)), (Q(4), Q(-2)), (Q(-5), Q(-2))]
    f0_comb = symanzik_f0_polynomial(dia, alpha_dia, q_dia)
    f0_kirch = kirchhoff_schur_symanzik_f0(dia, alpha_dia, q_dia)
    assert f0_comb == f0_kirch
    assert f0_comb > Q(0)


def test_negative_part_a_rejects_nonconserved_external_momenta() -> None:
    bub = bubble_graph()
    with pytest.raises(ValueError, match="External momenta must satisfy conservation"):
        symanzik_f0_polynomial(bub, [Q(1), Q(1)], [(Q(1), Q(0)), (Q(1), Q(0))])


def test_part_b_dfm_spanning_tree_momentum_routing_and_tree_invariance() -> None:
    dia = diamond_graph()
    alpha_dia = [Q(2), Q(3), Q(5), Q(7), Q(11)]
    q_dia = [(Q(2), Q(1)), (Q(-1), Q(3)), (Q(4), Q(-2)), (Q(-5), Q(-2))]
    u_expected = symanzik_u_polynomial(dia, alpha_dia)
    f0_expected = symanzik_f0_polynomial(dia, alpha_dia, q_dia)

    trees = enumerate_spanning_trees(dia)
    for tree in trees:
        p_t = tree_routed_edge_momenta(dia, tree, q_dia)
        assert vertex_divergence_of_edge_flow(dia, p_t) == q_dia
        for e_idx in range(dia.edge_count):
            if e_idx not in tree:
                assert p_t[e_idx] == (Q(0), Q(0))
        u_dfm, f0_dfm = dfm_loop_eliminated_f0(dia, tree, alpha_dia, q_dia)
        assert u_dfm == u_expected
        assert f0_dfm == f0_expected


def test_part_c_zimmermann_forests_and_uv_pole_cancellation() -> None:
    overlapping_subs = [
        DivergentSubgraph("gamma_L", frozenset({0, 1, 2}), 0),
        DivergentSubgraph("gamma_R", frozenset({2, 3, 4}), 0),
        DivergentSubgraph("G_all", frozenset({0, 1, 2, 3, 4}), 0),
    ]
    forests = enumerate_zimmermann_forests(overlapping_subs)
    assert len(forests) == 6
    for f in forests:
        names = {g.name for g in f}
        assert not ("gamma_L" in names and "gamma_R" in names)

    for lam1 in [Q(1, 5), Q(1, 100), Q(1, 1000000)]:
        for lam2 in [Q(1, 7), Q(1, 200), Q(1, 1000000)]:
            res = bphz_two_loop_nested_sector_integrand(lam1, lam2, Q(3, 5))
            assert res["r_sum"] == res["r_analytic_regular"]


def test_full_qm214_receipt() -> None:
    receipt = evaluate_symanzik_two_forest_bphz_control()
    assert receipt["all_graphs_f0_match_kirchhoff_schur"] is True
    assert receipt["dfm_all_eight_trees_conserve_momentum"] is True
    assert receipt["dfm_all_eight_trees_match_f0_and_u"] is True
    assert receipt["dfm_tree_change_is_cycle_cocycle"] is True
    assert receipt["bphz_nested_2loop_forest_count"] == 4
    assert receipt["bphz_overlapping_subgraph_forest_count"] == 6
    assert receipt["bphz_uv_boundary_poles_cancel_identically"] is True
    assert receipt["bphz_uv_boundary_regular_value_at_zero"] == Q(9, 25)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'symanzik_two_forest.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'DivergentSubgraph' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.symanzik_two_forest', 'finite_qm.use_cases.symanzik_two_forest', 'src.qm.campaigns.symanzik_two_forest_bphz_control', 'finite_qm.use_cases.symanzik_two_forest_bphz_control')
_USE_SHIM = True
_MUTANTS = (('bubble_graph:58', '        vertex_count=2,', '        vertex_count=3,'),)
_CHILD = '\nimport importlib\nimport importlib.util\nimport json\nimport sys\nimport tempfile\nfrom pathlib import Path\n\npayload = json.loads(sys.stdin.read())\nfor root in payload["roots"]:\n    if root not in sys.path:\n        sys.path.insert(0, root)\nif payload["shim"]:\n    import tests.conftest\nprimary = payload["modules"][0]\nreal = importlib.import_module(primary)\nspec = importlib.util.spec_from_loader(primary, loader=None)\nmodule = importlib.util.module_from_spec(spec)\nmodule.__package__ = real.__package__\nmodule.__file__ = payload["origin"]\nif hasattr(real, "__path__"):\n    module.__path__ = list(real.__path__)\nfor name in payload["modules"]:\n    sys.modules[name] = module\n    parent, _, child = name.rpartition(".")\n    if parent in sys.modules:\n        setattr(sys.modules[parent], child, module)\nexec(compile(payload["source"], payload["origin"], "exec"), module.__dict__)\ntest_spec = importlib.util.spec_from_file_location("certificate_probe", payload["test"])\ntest_mod = importlib.util.module_from_spec(test_spec)\ntest_spec.loader.exec_module(test_mod)\n\n\ndef _unwrap(fn):\n    wrapped = getattr(fn, "__wrapped__", None)\n    if callable(wrapped):\n        return wrapped\n    holder = getattr(fn, "__pytest_wrapped__", None)\n    obj = getattr(holder, "obj", None)\n    if callable(obj):\n        return obj\n    return fn\n\n\ndef _fixture(name):\n    if name == "tmp_path":\n        return Path(tempfile.mkdtemp())\n    fix = getattr(test_mod, name, None)\n    if not callable(fix):\n        return None\n    target = _unwrap(fix)\n    code = getattr(target, "__code__", None)\n    if code is None or code.co_argcount != 0:\n        return None\n    return target()\n\n\nran = 0\ntry:\n    for name in dir(test_mod):\n        if not name.startswith("test_"):\n            continue\n        if "mutation" in name:\n            continue\n        if name == "test_integration_origin_locks_the_source_module":\n            continue\n        fn = getattr(test_mod, name)\n        code = getattr(fn, "__code__", None)\n        if code is None:\n            continue\n        values = []\n        ready = True\n        for arg in code.co_varnames[: code.co_argcount]:\n            value = _fixture(arg)\n            if value is None:\n                ready = False\n                break\n            values.append(value)\n        if ready is False:\n            continue\n        fn(*values)\n        ran += 1\n    if ran == 0:\n        print("FAIL none")\n    else:\n        print("PASS " + str(ran))\nexcept Exception as exc:\n    print("FAIL " + type(exc).__name__)\n'

def _suite_passes(source: str) -> bool:
    payload = json.dumps({
        "modules": list(_ALIAS_NAMES),
        "source": source,
        "origin": str(_MODULE_PATH),
        "test": str(__import__("pathlib").Path(__file__).resolve()),
        "shim": _USE_SHIM,
        "roots": [str(__import__("pathlib").Path(__file__).resolve().parents[1]), str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src")],
    })
    completed = subprocess.run(
        [sys.executable, "-c", _CHILD],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = completed.stdout.strip().splitlines()
    status = lines[-1] if lines else ""
    return status.startswith("PASS")

def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    if _suite_passes(source) is False:
        raise AssertionError("baseline suite failed")
    killed = 0
    for name, old, new in _MUTANTS:
        if source.count(old) != 1:
            raise AssertionError(name)
        if _suite_passes(source.replace(old, new, 1)) is not False:
            raise AssertionError(name)
        killed += 1
    if killed != len(_MUTANTS):
        raise AssertionError(str(killed))
    record = f"Mutation-Kills: {killed} non-equivalent"
    if record not in __import__('pathlib').Path(__file__).read_text(encoding="utf-8"):
        raise AssertionError(record)
