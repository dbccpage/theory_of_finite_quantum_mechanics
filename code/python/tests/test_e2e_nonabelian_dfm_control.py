"""End-to-end tests for QM-213 substantial-vs-artificial & hierarchical non-Abelian DFM control.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/nonabelian_dfm.py
Claim: DIAMOND_EDGES certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.nonabelian_dfm_control import (
    DIAMOND_EDGES,
    borel2,
    borel2_torus_part,
    borel2_unipotent_part,
    classify_punctured_diamond_connection,
    dga_covariant_differential_deg2,
    dga_curvature,
    dga_gauge,
    flat_cover_extension_p5,
    gauge_transform_edges,
    id2,
    is_diagonal_2x2,
    is_unit_upper_triangular,
    mat2,
    mat2_det,
    mat2_inv,
    mat2_mul,
    mat2_trace,
    poset_p5_chains,
    run_qm213_nonabelian_dfm_control,
    tree_transport_and_dressing,
    walk_holonomy,
    zero2,
)


def test_unit_substantial_vs_artificial_local_green_global_red_classification() -> None:
    """Verify artificial (GaugeTrivial) vs substantial (FlatNontrivial) vs curved classification."""
    potentials = [
        borel2(1, 0, 1),
        borel2(2, 3, Fraction(1, 2)),
        borel2(Fraction(1, 3), -2, 3),
        borel2(Fraction(3, 2), 5, Fraction(2, 3)),
    ]
    u_art = gauge_transform_edges(DIAMOND_EDGES, [id2() for _ in range(5)], potentials)
    assert classify_punctured_diamond_connection(u_art) == "GaugeTrivial"
    _, _, res_art = tree_transport_and_dressing(4, DIAMOND_EDGES, u_art, (0, 2, 3))
    assert all(m == id2() for m in res_art)

    chord = borel2(2, 3, Fraction(1, 2))
    u_sub = gauge_transform_edges(DIAMOND_EDGES, [id2(), id2(), id2(), id2(), chord], potentials)
    assert classify_punctured_diamond_connection(u_sub) == "FlatNontrivial"
    assert walk_holonomy(u_sub, ((0, 1), (1, 1), (2, -1))) == id2()
    _, _, res_sub = tree_transport_and_dressing(4, DIAMOND_EDGES, u_sub, (0, 2, 3))
    assert all(res_sub[e] == id2() for e in (0, 2, 3))
    assert res_sub[4] != id2()


def test_second_kind_residual_ambiguity_under_spanning_tree_change() -> None:
    """Verify exact vertex intertwiner C(v) = u_{T_2}(v) u_{T_1}(v)^{-1} and cycle invariants."""
    potentials = [
        borel2(1, 0, 1),
        borel2(2, 3, Fraction(1, 2)),
        borel2(Fraction(1, 3), -2, 3),
        borel2(Fraction(3, 2), 5, Fraction(2, 3)),
    ]
    u_sub = gauge_transform_edges(
        DIAMOND_EDGES,
        [id2(), id2(), id2(), id2(), borel2(2, 3, Fraction(1, 2))],
        potentials,
    )
    _, u_t1, res_t1 = tree_transport_and_dressing(4, DIAMOND_EDGES, u_sub, (0, 2, 3))
    _, u_t2, res_t2 = tree_transport_and_dressing(4, DIAMOND_EDGES, u_sub, (0, 1, 4))
    transition_c = [mat2_mul(g2, mat2_inv(g1)) for g1, g2 in zip(u_t1, u_t2)]
    assert gauge_transform_edges(DIAMOND_EDGES, res_t1, transition_c) == res_t2

    right_loop = ((1, 1), (3, 1), (4, -1))
    hol_t1 = walk_holonomy(res_t1, right_loop)
    hol_t2 = walk_holonomy(res_t2, right_loop)
    assert mat2_trace(hol_t1) == mat2_trace(hol_t2) == Fraction(5, 2)
    assert mat2_det(hol_t1) == mat2_det(hol_t2) == Fraction(1, 1)


def test_two_stage_hierarchical_nonabelian_dressing_n_in_b() -> None:
    """Verify Stage 1 unipotent dressing u_N in N and Stage 2 torus dressing u_T in B/N."""
    borel_conn = [
        borel2(2, 3, Fraction(1, 2)),
        borel2(3, -1, 2),
        borel2(Fraction(1, 2), 4, 3),
        borel2(4, 2, Fraction(1, 3)),
        borel2(Fraction(5, 2), -3, Fraction(2, 5)),
    ]
    tree_edges = (0, 2, 3)
    t_borel, full_dressing, full_residual = tree_transport_and_dressing(
        4, DIAMOND_EDGES, borel_conn, tree_edges
    )
    u_n_vec = []
    u_t_vec = []
    for v in range(4):
        d_v = borel2_torus_part(t_borel[v])
        d_v_inv = mat2_inv(d_v)
        n_v = borel2_unipotent_part(t_borel[v])
        n_v_inv = mat2_inv(n_v)
        u_n_vec.append(mat2_mul(mat2_mul(d_v, n_v_inv), d_v_inv))
        u_t_vec.append(d_v_inv)

    assert all(is_unit_upper_triangular(m) for m in u_n_vec)
    assert all(is_diagonal_2x2(m) for m in u_t_vec)

    conn_stage1 = gauge_transform_edges(DIAMOND_EDGES, borel_conn, u_n_vec)
    assert all(is_diagonal_2x2(conn_stage1[e]) for e in tree_edges)
    assert all(
        borel2_torus_part(conn_stage1[e]) == borel2_torus_part(borel_conn[e]) for e in range(5)
    )

    conn_stage2 = gauge_transform_edges(DIAMOND_EDGES, conn_stage1, u_t_vec)
    assert conn_stage2 == full_residual
    assert all(mat2_mul(u_t_vec[v], u_n_vec[v]) == full_dressing[v] for v in range(4))


def test_poset_p5_flat_cover_extension_and_global_red_obstruction() -> None:
    """Verify flat_cover_extension succeeds on path-independent covers and refuses GlobalRed."""
    m01 = mat2(2, 1, 0, 1)
    m13 = mat2(1, 3, 0, 2)
    m02_flat = mat2(1, 2, 0, 2)
    m23_flat = mat2(2, 6, 0, 1)
    m34 = mat2(1, -1, 0, 1)
    ok_flat, ext_flat = flat_cover_extension_p5(
        {(0, 1): m01, (1, 3): m13, (0, 2): m02_flat, (2, 3): m23_flat, (3, 4): m34}
    )
    assert ok_flat
    assert isinstance(ext_flat, dict)
    assert all(m == zero2() for m in dga_curvature(ext_flat).values())

    ok_sub, err_sub = flat_cover_extension_p5(
        {
            (0, 1): m01,
            (1, 3): m13,
            (0, 2): mat2(1, 1, 0, 1),
            (2, 3): mat2(2, 1, 0, 2),
            (3, 4): m34,
        }
    )
    assert not ok_sub
    assert err_sub == (0, 3, (0, 1, 3), (0, 2, 3))


def test_dga_dressed_curvature_covariance_and_bianchi_identity() -> None:
    """Verify K(A^u) = u K(A) u^{-1} and D_{A^u} K(A^u) = 0 under N and B/N."""
    a_cochain = {
        ch: mat2(1 + ((idx + 1) % 2), idx + 1, 0, 1 + ((idx + 2) % 2))
        for idx, ch in enumerate(poset_p5_chains(1))
    }
    k_cochain = dga_curvature(a_cochain)
    assert any(m != zero2() for m in k_cochain.values())
    assert all(m == zero2() for m in dga_covariant_differential_deg2(k_cochain, a_cochain).values())

    u_n = [
        borel2(1, 2, 1),
        borel2(1, Fraction(-3, 2), 1),
        borel2(1, Fraction(5, 3), 1),
        borel2(1, Fraction(-7, 4), 1),
        borel2(1, Fraction(11, 5), 1),
    ]
    a_u_n = dga_gauge(1, a_cochain, u_n)
    k_u_n = dga_curvature(a_u_n)
    assert k_u_n == dga_gauge(2, k_cochain, u_n)
    assert all(
        k_cochain[ch][0][0] == k_u_n[ch][0][0] and k_cochain[ch][1][1] == k_u_n[ch][1][1]
        for ch in poset_p5_chains(2)
    )
    assert all(m == zero2() for m in dga_covariant_differential_deg2(k_u_n, a_u_n).values())

    t_quot = [
        borel2(2, 0, 3),
        borel2(Fraction(1, 2), 0, Fraction(5, 3)),
        borel2(Fraction(3, 4), 0, Fraction(2, 5)),
        borel2(Fraction(5, 2), 0, Fraction(1, 3)),
        borel2(Fraction(4, 3), 0, Fraction(3, 2)),
    ]
    a_stage2 = dga_gauge(1, a_u_n, t_quot)
    k_stage2 = dga_curvature(a_stage2)
    assert k_stage2 == dga_gauge(2, k_u_n, t_quot)
    assert all(m == zero2() for m in dga_covariant_differential_deg2(k_stage2, a_stage2).values())


def test_negative_full_qm213_receipt_invariants_and_refusals() -> None:
    """Verify full QM-213 receipt fields and input validation refusals."""
    receipt = run_qm213_nonabelian_dfm_control()
    assert receipt.artificial_verdict == "GaugeTrivial"
    assert receipt.artificial_local_dressing_neutralizes_all_edges
    assert receipt.artificial_poset_flat_cover_extension_is_ok
    assert receipt.artificial_poset_extended_curvature_is_zero
    assert receipt.substantial_verdict == "FlatNontrivial"
    assert receipt.substantial_face_f0_is_local_green
    assert receipt.substantial_tree_dressing_neutralizes_tree_only
    assert receipt.substantial_poset_returns_path_dependent_global_red
    assert receipt.second_kind_tree_change_intertwiner_exact
    assert receipt.second_kind_cycle_traces_and_dets_invariant
    assert receipt.curved_verdict == "Curved"
    assert receipt.stage1_u_n_all_in_normal_unipotent_subgroup
    assert receipt.stage1_tree_edges_reduced_to_diagonal_quotient
    assert receipt.stage1_preserves_b_mod_n_projection_on_all_edges
    assert receipt.stage1_residual_first_kind_torus_preserves_diagonal_tree
    assert receipt.stage2_u_t_all_in_diagonal_torus
    assert receipt.two_stage_factorization_matches_full_tree_gauge
    assert receipt.stage2_matches_tree_gauge_residual_exactly
    assert receipt.dga_poset_vertex_count == 5
    assert receipt.dga_poset_two_chain_count == 7
    assert receipt.dga_poset_three_chain_count == 2
    assert receipt.dga_b_squared_zero_on_a
    assert receipt.dga_undressed_curvature_nonzero
    assert receipt.dga_undressed_bianchi_identity_zero
    assert receipt.dga_stage1_curvature_equals_gauged_curvature
    assert receipt.dga_stage1_preserves_diagonal_b_mod_n_curvature
    assert receipt.dga_stage1_bianchi_identity_zero
    assert receipt.dga_quotient_b_mod_n_covariance_exact
    assert receipt.dga_composite_two_stage_curvature_matches
    assert receipt.dga_stage2_bianchi_identity_zero

    with pytest.raises(ValueError, match="non-zero"):
        borel2(0, 1, 1)
    with pytest.raises(ValueError, match="Singular"):
        mat2_inv(mat2(1, 2, 2, 4))


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'nonabelian_dfm.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'DIAMOND_EDGES' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.nonabelian_dfm', 'finite_qm.use_cases.nonabelian_dfm', 'src.qm.campaigns.nonabelian_dfm_control', 'finite_qm.use_cases.nonabelian_dfm_control')
_USE_SHIM = True
_MUTANTS = (('id2:48', '    return mat2(1, 0, 0, 1)', '    return mat2(2, 0, 0, 1)'),)
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
