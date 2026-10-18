"""Wave C: coda_engine carve-out to DomainWorker + functional (path-scoped)."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from omega_engine.crates.runtime.rt_coda_domain_worker import CodaDomainWorker
from omega_engine.crates.engine.eng_coda import (
    CODA_ENGINE_FILE_CONTRACT,
    CODA_ENGINE_ROLE,
    CohomologicalEngine,
    ObstructionCalculus,
    SimplicialCarrier,
)
from omega_engine.crates.runtime.rt_domain_worker import CONTRACT_ID as DW_ID
from omega_engine.crates.engine.base.eng_base import Engine
from omega_engine.crates.type.engine_io import DomainWorkerInput


def _assert_receipt_identity(out) -> None:
    assert out.residual_l1 == pytest.approx(
        sum(abs(x) for x in out.residual_vector), abs=1e-9
    )


def test_coda_engine_role_is_math_suite_not_domain_worker_implementor() -> None:
    assert CODA_ENGINE_ROLE == "math_suite_callable_by_domain_worker"
    assert CODA_ENGINE_FILE_CONTRACT == "urn:omega:engine:coda_engine:file:v1.0.0"
    coda_src = Path(inspect.getfile(ObstructionCalculus)).read_text(encoding="utf-8")
    assert "urn:omega:execution:domain_worker:v1.0.0" not in coda_src
    assert "StateTransition" not in coda_src
    assert "residual_l1" in coda_src
    worker = CodaDomainWorker()
    assert DW_ID in worker.implements
    assert CODA_ENGINE_FILE_CONTRACT not in worker.implements


def test_analyze_1cochain_source_uses_functional_and_orientation() -> None:
    src = Path(inspect.getfile(ObstructionCalculus)).read_text(encoding="utf-8")
    tree = ast.parse(src)
    analyze = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "ObstructionCalculus":
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "analyze_1cochain":
                    analyze = item
                    break
    assert analyze is not None
    body_src = ast.get_source_segment(src, analyze) or ""
    assert "residual_l1" in body_src
    assert "gamma2" in body_src
    assert "h_on_edge" in body_src or "project_h1_to_edge_basis" in body_src
    assert "math.sqrt(sum" not in body_src


def test_reverse_edge_cochain_orientation_gamma2() -> None:
    carrier = SimplicialCarrier(
        vertices=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"), ("a", "c")],
        faces=[("a", "b", "c")],
    )
    h1 = {("b", "a"): 1.0}
    assert CohomologicalEngine.h_on_edge(h1, "a", "b") == pytest.approx(-1.0)
    proj = CohomologicalEngine.project_h1_to_edge_basis(carrier, h1)
    assert proj == pytest.approx([-1.0, 0.0, 0.0])
    sig = ObstructionCalculus.analyze_1cochain(carrier, h1)
    assert sig.gamma_2 == pytest.approx(1.0)
    assert sig.input_cochain == pytest.approx([-1.0, 0.0, 0.0])
    assert sig.phi_1 == pytest.approx(sum(abs(x) for x in sig.residual_vector))


def test_coda_domain_worker_contract() -> None:
    w = CodaDomainWorker()
    assert DW_ID in w.implements
    assert set(w.supported_task_kinds()) == {
        "obstruction_analyze",
        "mur_l1_gauge",
        "foc_curvature",
    }


def test_obstruction_analyze_removable_gauge() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="obs1",
            task_kind="obstruction_analyze",
            payload={
                "vertices": ["a", "b", "c"],
                "edges": [["a", "b"], ["b", "c"], ["a", "c"]],
                "faces": [["a", "b", "c"]],
                "h1": {("a", "b"): 5.0, ("b", "c"): 7.0, ("a", "c"): 12.0},
            },
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.status == "SOLVED"
    assert out.result["status_label"] == "REMOVABLE_GAUGE"
    assert out.residual_l1 < 1e-4
    _assert_receipt_identity(out)
    assert out.result["input_cochain"] == pytest.approx([5.0, 7.0, 12.0])
    assert any("analyze_1cochain" in p for p in out.math_path)


def test_obstruction_analyze_reverse_keys_receipt_identity() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="obs_rev",
            task_kind="obstruction_analyze",
            payload={
                "vertices": ["a", "b", "c"],
                "edges": [["a", "b"], ["b", "c"], ["a", "c"]],
                "faces": [["a", "b", "c"]],
                "h1": {("b", "a"): 1.0},
            },
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.result["gamma_2"] == pytest.approx(1.0)
    assert out.result["input_cochain"] == pytest.approx([-1.0, 0.0, 0.0])
    _assert_receipt_identity(out)


def test_mur_l1_gauge_via_domain_worker() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="mur1",
            task_kind="mur_l1_gauge",
            payload={
                "vertices": [0, 1, 2],
                "edges": [[0, 1], [1, 2], [2, 0]],
                "faces": [[0, 1, 2]],
                "cochain": [1.0, 0.5, -0.8],
            },
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.result["phi1_lp"] > 0.0
    _assert_receipt_identity(out)


def test_foc_curvature_via_domain_worker() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="foc1",
            task_kind="foc_curvature",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2], [2, 0]],
                "faces": [[0, 1, 2]],
                "cochain": [1.0, 1.0, 1.0],
            },
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.status == "OBSTRUCTED"
    assert abs(out.result["curvature"][0] - 3.0) < 1e-6
    _assert_receipt_identity(out)


def test_coda_domain_worker_refuses_bad_carrier() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="bad",
            task_kind="mur_l1_gauge",
            payload={
                "vertices": [0, 1],
                "edges": [[0, 1], [1, 2]],
                "cochain": [1.0, 0.0],
            },
        )
    )
    assert out.status == "REFUSED"


def test_fail_closed_fractional_n_nodes() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="frac",
            task_kind="foc_curvature",
            payload={
                "n_nodes": 3.9,
                "edges": [[0, 1], [1, 2]],
                "cochain": [1.0, 0.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "fractional" in out.result["reason"] or "integer" in out.result["reason"]


def test_fail_closed_n_nodes_inf() -> None:
    w = CodaDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inf",
            task_kind="foc_curvature",
            payload={
                "n_nodes": float("inf"),
                "edges": [[0, 1]],
                "cochain": [1.0],
            },
        )
    )
    assert out.status == "REFUSED"


def test_fail_closed_cochain_nan_inf() -> None:
    w = CodaDomainWorker()
    out_nan = w.run(
        DomainWorkerInput(
            task_id="nan",
            task_kind="mur_l1_gauge",
            payload={
                "vertices": [0, 1],
                "edges": [[0, 1]],
                "cochain": [float("nan")],
            },
        )
    )
    assert out_nan.status == "REFUSED"
    out_inf = w.run(
        DomainWorkerInput(
            task_id="pinf",
            task_kind="mur_l1_gauge",
            payload={
                "vertices": [0, 1],
                "edges": [[0, 1]],
                "cochain": [float("inf")],
            },
        )
    )
    assert out_inf.status == "REFUSED"


def test_fail_closed_tol_eps() -> None:
    w = CodaDomainWorker()
    base = {
        "vertices": [0, 1],
        "edges": [[0, 1]],
        "cochain": [0.0],
    }
    out_tol_nan = w.run(
        DomainWorkerInput(
            task_id="tn",
            task_kind="mur_l1_gauge",
            payload=base,
            parameters={"tol": float("nan")},
        )
    )
    assert out_tol_nan.status == "REFUSED"
    out_tol_neg = w.run(
        DomainWorkerInput(
            task_id="tneg",
            task_kind="mur_l1_gauge",
            payload=base,
            parameters={"tol": -1.0},
        )
    )
    assert out_tol_neg.status == "REFUSED"
    out_eps = w.run(
        DomainWorkerInput(
            task_id="eps",
            task_kind="obstruction_analyze",
            payload={
                "vertices": ["a", "b"],
                "edges": [["a", "b"]],
                "h1": {("a", "b"): 0.0},
            },
            parameters={"eps": float("nan")},
        )
    )
    assert out_eps.status == "REFUSED"
    out_eps_neg = w.run(
        DomainWorkerInput(
            task_id="epsneg",
            task_kind="obstruction_analyze",
            payload={
                "vertices": ["a", "b"],
                "edges": [["a", "b"]],
                "h1": {("a", "b"): 0.0},
            },
            parameters={"eps": -1.0},
        )
    )
    assert out_eps_neg.status == "REFUSED"


def test_carrier_rejects_self_loop_and_duplicate_edge() -> None:
    assert not SimplicialCarrier(vertices=[0, 1], edges=[(0, 0)]).validate()
    assert not SimplicialCarrier(
        vertices=[0, 1], edges=[(0, 1), (0, 1)]
    ).validate()
    assert not SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1)],
        faces=[(0, 1, 2)],
    ).validate()


def test_legacy_coda_suite_still_works() -> None:
    from omega_engine.crates.engine.eng_coda import (
        CODAMasterSuite,
        run_coda_master_suite,
    )

    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [(0, 1, 2)]
    coda = CODAMasterSuite(3, edges, faces)
    cochain = __import__("numpy").array([1.0, 1.0, 1.0])
    curv = coda.coda_000_foc_curvature(cochain)
    assert abs(curv[0] - 3.0) < 1e-6
    ledger = run_coda_master_suite()
    assert ledger["coda_002_l1_gauge_norm_phi1"] > 0.0


def test_oe_000_obstruction_signature_still_removable() -> None:
    carrier = SimplicialCarrier(
        vertices=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"), ("a", "c")],
        faces=[("a", "b", "c")],
    )
    f0 = {"a": 0.0, "b": 5.0, "c": 12.0}
    d0_f = CohomologicalEngine.d0(carrier, f0)
    sig = ObstructionCalculus.analyze_1cochain(carrier, d0_f)
    assert sig.status_label == "REMOVABLE_GAUGE"
    assert sig.phi_1 < 1e-5
    assert sig.phi_1 == pytest.approx(sum(abs(x) for x in sig.residual_vector))


