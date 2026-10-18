"""Exact / Survivor / Open trichotomy (A2). Diagnostic, firewall-clean."""

from omega_engine.crates.functional.trichotomy import classify, Trichotomy


def _triangle_d0():
    # (E=3, V=3) incidence for cycle 0->1->2->0.
    return [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]


def _no_face_d1():
    return []  # 0 faces -> everything closed


def _bad_face_complex():
    # A square graph 0->1->2->3->0 (4 edges) PLUS a single triangle-ish face that
    # only covers some edges so that some cochains are NOT closed.
    d0 = [
        [-1, 1, 0, 0],  # e0: 0->1
        [0, -1, 1, 0],  # e1: 1->2
        [0, 0, -1, 1],  # e2: 2->3
        [1, 0, 0, -1],  # e3: 3->0
    ]
    # One face = the full 4-cycle e0+e1+e2+e3 (d1 d0 = 0 holds).
    d1 = [[1, 1, 1, 1]]
    return d0, d1


def test_exact_branch():
    d0 = _triangle_d0()
    # x = d0 alpha, alpha=[0,3,5]: edges [3,2,-5] -> Phi1 = 0 -> EXACT.
    x = [3, 2, -5]
    r = classify(d0, _no_face_d1(), x)
    assert r.label == Trichotomy.EXACT
    assert r.closed is True
    assert r.exact_membership is True
    assert r.phi1_is_zero is True
    assert r.exact_test_agrees is True
    assert r.is_auth is False


def test_survivor_branch():
    d0 = _triangle_d0()
    # x = [1,1,1] cycle cochain: closed (no faces) but not a coboundary; Phi1 = 3.
    x = [1, 1, 1]
    r = classify(d0, _no_face_d1(), x)
    assert r.label == Trichotomy.SURVIVOR
    assert r.closed is True
    assert r.exact_membership is False
    assert r.phi1_estimate > 0
    assert abs(r.phi1_estimate - 3.0) < 1e-6
    assert r.is_auth is False


def test_open_branch():
    d0, d1 = _bad_face_complex()
    # x = e0 only = [1,0,0,0]: d1 x = sum over face = 1 != 0 -> NOT closed -> OPEN.
    x = [1, 0, 0, 0]
    r = classify(d0, d1, x)
    assert r.label == Trichotomy.OPEN
    assert r.closed is False
    assert r.gamma2_zero is False
    assert r.gamma2_value > 0  # ||d1 x||_1 = 1 (x hits the face once)
    assert abs(r.gamma2_value - 1.0) < 1e-12
    assert r.exact_membership is None
    assert r.is_auth is False


def test_result_carries_no_authority():
    d0 = _triangle_d0()
    r = classify(d0, _no_face_d1(), [1, 1, 1])
    d = r.as_dict()
    assert d["is_auth"] is False
    assert d["diagnostic_only"] is True
    assert "proved" not in d
    assert "terminal" not in d


def test_float_exact_decision_agrees_with_exact_membership():
    # On a clean integer example the float LP and exact membership must agree.
    d0 = _triangle_d0()
    for x in ([3, 2, -5], [1, 1, 1], [0, 0, 0]):
        r = classify(d0, _no_face_d1(), x)
        assert r.exact_test_agrees is True


