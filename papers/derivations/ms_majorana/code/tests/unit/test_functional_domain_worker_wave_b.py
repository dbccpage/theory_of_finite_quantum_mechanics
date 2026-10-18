"""Wave B: FunctionalDomainWorker PROTO_LIVE demos (path-scoped)."""

from __future__ import annotations

import ast
import inspect
import math
from pathlib import Path

import pytest

from omega_engine.crates.runtime.rt_domain_worker import (
    CONTRACT_ID as DW_ID,
    DomainWorker,
)
from omega_engine.crates.runtime.rt_functional_domain_worker import (
    FunctionalDomainWorker,
)
from omega_engine.crates.type.engine_io import DomainWorkerInput


# STUB_MIRROR import paths that Wave B workers must not use.
_FORBIDDEN_IMPORT_SUBSTRINGS = (
    "linear_algebra.gram_schmidt",  # use gram_schmidt_proto only
    "functional._rust_lib_surface",
    "search.search_mcts",
)


def test_functional_worker_contract() -> None:
    w = FunctionalDomainWorker()
    assert DW_ID in w.implements
    kinds = set(w.supported_task_kinds())
    assert kinds == {"residual_l1", "gamma2", "incidence_residual"}


def test_residual_l1_task() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="r1",
            task_kind="residual_l1",
            payload={"residual": [1.0, -2.0, 0.5]},
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.status == "OBSTRUCTED"
    assert out.residual_l1 == pytest.approx(3.5)
    assert any("residual_l1" in p for p in out.math_path)
    assert any("PROD_TODO:omega_functional" in p or "omega_functional" in p for p in out.math_path)


def test_residual_l1_zero_solved() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="r0",
            task_kind="residual_l1",
            payload={"residual": [0.0, 0.0]},
        )
    )
    assert out.status == "SOLVED"
    assert out.residual_l1 == 0.0


def test_residual_l1_refuses_nan() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="rnan",
            task_kind="residual_l1",
            payload={"residual": [float("nan")]},
        )
    )
    assert out.status == "REFUSED"
    assert "finite" in out.result["reason"].lower() or "not a finite" in out.result["reason"]


def test_residual_l1_refuses_inf_and_bad_tol() -> None:
    w = FunctionalDomainWorker()
    out_inf = w.run(
        DomainWorkerInput(
            task_id="rinf",
            task_kind="residual_l1",
            payload={"residual": [float("inf")]},
        )
    )
    assert out_inf.status == "REFUSED"
    out_tol = w.run(
        DomainWorkerInput(
            task_id="rtol",
            task_kind="residual_l1",
            payload={"residual": [0.0]},
            parameters={"tol": float("nan")},
        )
    )
    assert out_tol.status == "REFUSED"
    out_neg = w.run(
        DomainWorkerInput(
            task_id="rneg",
            task_kind="residual_l1",
            payload={"residual": [0.0]},
            parameters={"tol": -1.0},
        )
    )
    assert out_neg.status == "REFUSED"


def test_gamma2_closed() -> None:
    w = FunctionalDomainWorker()
    # d1 = [[1, -1]] maps h=[1,1] -> [0]
    out = w.run(
        DomainWorkerInput(
            task_id="g0",
            task_kind="gamma2",
            payload={
                "d1": {"rows": 1, "cols": 2, "data": [1.0, -1.0]},
                "h": [1.0, 1.0],
            },
        )
    )
    assert out.status == "SOLVED"
    assert out.result["gamma2"] == pytest.approx(0.0)
    assert out.result["is_closed"] is True
    assert out.result["closure_status"] == "Closed"
    assert out.residual_l1 == pytest.approx(0.0)
    assert any("gamma2" in p for p in out.math_path)
    assert any("residual_l1" in p for p in out.math_path)


def test_gamma2_open() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="g1",
            task_kind="gamma2",
            payload={
                "d1": {"rows": 2, "cols": 2, "data": [1.0, -1.0, 0.0, 1.0]},
                "h": [1.0, 1.0],
            },
        )
    )
    assert out.status == "OBSTRUCTED"
    assert out.result["gamma2"] == pytest.approx(1.0)
    assert out.result["is_closed"] is False
    assert out.result["closure_status"] == "Open"
    assert out.residual_l1 == pytest.approx(1.0)


def test_gamma2_indeterminate_not_solved() -> None:
    """0 < Gamma2 <= tol must be INDETERMINATE, never SOLVED."""
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="gind",
            task_kind="gamma2",
            payload={
                "d1": {"rows": 1, "cols": 1, "data": [1.0]},
                "h": [5e-10],
            },
            parameters={"tol": 1e-9},
        )
    )
    assert out.status == "INDETERMINATE"
    assert out.result["closure_status"] == "IndeterminateWithinTolerance"
    assert out.result["is_closed"] is True  # tol-admitted, not algebraic closed
    assert 0.0 < out.result["gamma2"] <= 1e-9
    assert out.status != "SOLVED"


def test_gamma2_negative_dims_refused() -> None:
    """rows*cols can match data length with negatives; must REFUSE before reshape."""
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="gneg",
            task_kind="gamma2",
            payload={
                "d1": {"rows": -1, "cols": -1, "data": [1.0]},
                "h": [1.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "d1.rows" in out.result["reason"] or ">=" in out.result["reason"]


def test_gamma2_rows_inf_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="ginf",
            task_kind="gamma2",
            payload={
                "d1": {"rows": float("inf"), "cols": 1, "data": [1.0]},
                "h": [1.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "finite" in out.result["reason"] or "integer" in out.result["reason"]


def test_gamma2_fractional_dims_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="gfrac",
            task_kind="gamma2",
            payload={
                "d1": {"rows": 1.5, "cols": 2, "data": [1.0, 0.0, 0.0]},
                "h": [1.0, 0.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "fractional" in out.result["reason"] or "integer" in out.result["reason"]


def test_incidence_residual_exact_repair() -> None:
    """omega1 - d0 alpha = 0 when omega1 is exact coboundary."""
    w = FunctionalDomainWorker()
    # path graph 0-1-2: edges (0,1),(1,2); alpha=[0,1,3] => d0 a = [1,2]
    out = w.run(
        DomainWorkerInput(
            task_id="inc1",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "alpha": [0.0, 1.0, 3.0],
                "omega1": [1.0, 2.0],
            },
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.status == "SOLVED"
    assert out.residual_l1 == pytest.approx(0.0)
    assert any("incidence_matrix" in p for p in out.math_path)
    assert any("residual_l1" in p for p in out.math_path)


def test_incidence_residual_obstructed() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc2",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "alpha": [0.0, 0.0, 0.0],
                "omega1": [1.0, -1.0],
            },
        )
    )
    assert out.status == "OBSTRUCTED"
    assert out.residual_l1 == pytest.approx(2.0)


def test_incidence_omega1_empty_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_empty",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "omega1": [],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "edge count" in out.result["reason"]


def test_incidence_omega1_length_mismatch_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_o3",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "omega1": [1.0, 2.0, 3.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "edge count" in out.result["reason"]


def test_incidence_alpha_length_mismatch_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_a2",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "alpha": [0.0, 1.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "n_nodes" in out.result["reason"]


def test_incidence_alpha_omega1_either_side_mismatch_refused() -> None:
    w = FunctionalDomainWorker()
    out_a = w.run(
        DomainWorkerInput(
            task_id="inc_m1",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "alpha": [0.0, 1.0],
                "omega1": [1.0, 2.0],
            },
        )
    )
    assert out_a.status == "REFUSED"
    out_o = w.run(
        DomainWorkerInput(
            task_id="inc_m2",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "alpha": [0.0, 1.0, 3.0],
                "omega1": [1.0],
            },
        )
    )
    assert out_o.status == "REFUSED"


def test_incidence_omega1_only_valid_computes() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_o1",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, 1], [1, 2]],
                "omega1": [0.5, -0.25],
            },
        )
    )
    assert out.status == "OBSTRUCTED"
    assert out.residual_l1 == pytest.approx(0.75)
    assert len(out.residual_vector) == 2
    assert out.result["n_edges"] == 2


def test_incidence_n_nodes_inf_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_inf",
            task_kind="incidence_residual",
            payload={
                "n_nodes": float("inf"),
                "edges": [[0, 1]],
                "omega1": [1.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "n_nodes" in out.result["reason"]


def test_incidence_edge_endpoint_inf_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_einf",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3,
                "edges": [[0, float("inf")]],
                "omega1": [1.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "edges[0]" in out.result["reason"] or "finite" in out.result["reason"]


def test_incidence_fractional_n_nodes_refused() -> None:
    """Must not truncate 3.9 -> 3 and invent a different carrier."""
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(
            task_id="inc_frac",
            task_kind="incidence_residual",
            payload={
                "n_nodes": 3.9,
                "edges": [[0, 1], [1, 2]],
                "omega1": [1.0, 0.0],
            },
        )
    )
    assert out.status == "REFUSED"
    assert "fractional" in out.result["reason"] or "integer" in out.result["reason"]


def test_domain_worker_hash_rejects_nan() -> None:
    class _Tiny(DomainWorker):
        def supported_task_kinds(self):
            return ()

        def run(self, inp):
            raise NotImplementedError

    tiny = _Tiny()
    with pytest.raises(ValueError):
        tiny._hash_payload({"x": float("nan")})
    with pytest.raises(ValueError):
        tiny._hash_payload({"x": float("inf")})
    h = tiny._hash_payload({"x": 1.0, "y": [0.0, 2.0]})
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


def test_unsupported_task_refused() -> None:
    w = FunctionalDomainWorker()
    out = w.run(
        DomainWorkerInput(task_id="x", task_kind="stub_mirror_demo", payload={})
    )
    assert out.status == "REFUSED"


def test_worker_source_forbids_stub_mirror_imports() -> None:
    src_path = Path(inspect.getfile(FunctionalDomainWorker))
    text = src_path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    assert isinstance(tree, ast.Module)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    for bad in _FORBIDDEN_IMPORT_SUBSTRINGS:
        assert not any(bad in m for m in imported), (
            f"Wave B must not import STUB_MIRROR path: {bad}; got {imported}"
        )
    # No DIY residual mass
    assert "sum(abs" not in text
    assert "from omega_engine.crates.functional.phi1 import residual_l1" in text
    assert "from omega_engine.crates.functional.gamma2 import gamma2" in text or (
        "ClosureStatus" in text and "gamma2" in text
    )


def test_linear_algebra_worker_still_avoids_stub_gram_schmidt() -> None:
    from omega_engine.crates.runtime import rt_linear_algebra_domain_worker as la

    text = Path(inspect.getfile(la)).read_text(encoding="utf-8")
    assert "gram_schmidt_proto" in text
    assert "linear_algebra.gram_schmidt import" not in text
    assert "from omega_engine.crates.linear_algebra_theory.gram_schmidt import" not in text


def test_epic_002_tombstone_exists() -> None:
    root = Path(__file__).resolve().parents[4]  # repo root via .../ooutwire_docs/../../..
    # worktree-safe: walk up from this test file to find master_plans
    here = Path(__file__).resolve()
    candidates = []
    for p in here.parents:
        cand = (
            p
            / "omega_engine"
            / "omega_engine_product_planning_office"
            / "_anomalon_architecture"
            / "_0_master_planning_documents"
            / "_master_plans"
            / "epic_002_main_planning_document_v001.md"
        )
        if cand.is_file():
            candidates.append(cand)
            break
    assert candidates, "epic_002 tombstone missing"
    text = candidates[0].read_text(encoding="utf-8")
    assert "TOMBSTONE" in text
    assert "WITHDRAWN" in text
    assert "epic_008_one_deterministic_rail_v001.md" in text



