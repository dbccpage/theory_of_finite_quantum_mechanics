"""Wave E v4: path+symbol ratchet, inventory STUB bans, positive residual, receipt."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from omega_engine_governance.contracts.dual_home_evidence import (
    build_evidence_receipt,
    load_policy,
    sha256_json,
)
from omega_engine_governance.contracts.dual_home_gates import run_all_gates
from omega_engine_governance.contracts.dual_home_import_auditor import (
    audit_playpen,
    audit_source,
    discover_audit_targets,
    discover_domain_worker_files,
    discover_worker_spy_matrix,
    resolve_import_identities,
    stub_identities_from_inventory,
    transitive_local_deps,
)
from omega_engine_governance.contracts.dual_home_stub_inventory import (
    scan_packages,
)
from omega_engine_governance.contracts.dual_home_stub_ratchet import (
    baseline_digest,
    baseline_path,
    evaluate_ratchet,
    load_baseline,
)


def test_baseline_v4_paths_and_symbols_match_scan() -> None:
    data = load_baseline()
    assert data["version"] >= 4
    assert data.get("policy_version") in ("wave-e-v4", "wave-f-v1", "wave-g-v1")
    for pkg in ("functional", "linear_algebra", "homology", "solver", "search"):
        assert pkg in data["packages"]
        rep = scan_packages([pkg])[0]
        stubs = sorted(d.rel_path for d in rep.files_detail if d.kind == "STUB")
        assert data["packages"][pkg]["stub_paths"] == stubs
        assert data["packages"][pkg]["STUB"] == len(stubs)
        proto_sym: Dict[str, List[str]] = {}
        for d in rep.files_detail:
            if d.kind in ("PROTO", "MIXED") and d.top_level_real:
                proto_sym[d.rel_path] = list(d.top_level_real)
        assert data["packages"][pkg]["proto_symbols"] == proto_sym


def test_bootstrap_requires_flag_when_no_anchor() -> None:
    base = load_baseline()
    ok, violations, _ = evaluate_ratchet(base, anchor=None, allow_bootstrap=False)
    assert not ok
    assert any("bootstrap" in v.lower() or "anchor" in v.lower() for v in violations)


def test_bootstrap_passes_with_flag() -> None:
    base = load_baseline()
    ok, violations, measured = evaluate_ratchet(
        base, anchor=None, allow_bootstrap=True
    )
    assert ok, violations
    assert measured.get("packages")


def test_path_set_blocks_equal_count_substitution() -> None:
    base = load_baseline()
    anchor = json.loads(json.dumps(base))
    pkg = "search"
    paths = list(base["packages"][pkg]["stub_paths"])
    if len(paths) < 2:
        return
    # Equal count: drop one real stub path, add a fake path
    poisoned = json.loads(json.dumps(base))
    poisoned["packages"][pkg]["stub_paths"] = paths[1:] + [f"{pkg}/__fake_sub__.py"]
    poisoned["packages"][pkg]["STUB"] = len(paths)
    ok, violations, _ = evaluate_ratchet(poisoned, anchor=anchor)
    assert not ok
    assert any(
        "not in proposed" in v or "not measured" in v or "NEW STUB" in v
        for v in violations
    )


def test_anchor_blocks_baseline_inflation() -> None:
    base = load_baseline()
    anchor = json.loads(json.dumps(base))
    inflated = json.loads(json.dumps(base))
    pkg = "search"
    inflated["packages"][pkg]["stub_paths"] = list(
        inflated["packages"][pkg]["stub_paths"]
    ) + [f"{pkg}/__inflated__.py"]
    ok, violations, _ = evaluate_ratchet(inflated, anchor=anchor)
    assert not ok


def test_anchor_blocks_new_stub_vs_main() -> None:
    base = load_baseline()
    anchor = json.loads(json.dumps(base))
    pkg = "functional"
    apaths = list(anchor["packages"][pkg]["stub_paths"])
    if not apaths:
        return
    anchor["packages"][pkg]["stub_paths"] = apaths[1:]
    ok, violations, _ = evaluate_ratchet(base, anchor=anchor)
    assert not ok
    assert any("NEW STUB" in v for v in violations)


def test_symbol_inventory_mismatch_fails() -> None:
    base = load_baseline()
    poisoned = json.loads(json.dumps(base))
    # drop a proto symbol entry so measured != proposed
    ps = poisoned["packages"]["functional"]["proto_symbols"]
    if not ps:
        return
    first = next(iter(ps))
    if ps[first]:
        ps[first] = ps[first][1:]
    ok, violations, _ = evaluate_ratchet(poisoned, anchor=None, allow_bootstrap=True)
    assert not ok
    assert any("PROTO symbols" in v for v in violations)


def test_protected_proto_deletion_fails() -> None:
    base = load_baseline()
    anchor = json.loads(json.dumps(base))
    # Remove a PROTO path from measured by claiming empty package file_kinds in anchor
    # Use evaluate with anchor that has proto surface which we simulate missing by
    # shrinking measured via a fake package name not available — instead poison anchor
    # to claim a fake PROTO path that measured lacks.
    anchor["packages"]["functional"]["proto_symbols"]["functional/__missing_proto__.py"] = [
        "ghost_symbol"
    ]
    anchor["packages"]["functional"]["file_kinds"][
        "functional/__missing_proto__.py"
    ] = "PROTO"
    ok, violations, _ = evaluate_ratchet(base, anchor=anchor)
    assert not ok
    assert any("deleted" in v or "relocated" in v for v in violations)


def test_forbidden_identities_derived_from_inventory() -> None:
    forbidden = stub_identities_from_inventory()
    assert any("gram_schmidt" in f for f in forbidden)
    assert any("_rust_lib_surface" in f for f in forbidden)
    # PROTO residual surface must NOT be forbidden
    assert "omega_engine.crates.functional.phi1" not in forbidden
    assert "functional.phi1" not in forbidden or "phi1" in str(
        [x for x in forbidden if "phi1" in x]
    )
    # phi1 is PROTO — should not appear as STUB identity
    assert "omega_engine.crates.functional.phi1" not in forbidden


def test_exact_importfrom_symbol_identity() -> None:
    root = Path("dummy")
    # relative form
    src = "from ..linear_algebra import gram_schmidt\n"
    tree = __import__("ast").parse(src)
    # use real path under playpen for resolution
    from omega_engine_governance.contracts.dual_home_import_auditor import (
        playpen_omega_engine_root,
    )

    playpen = playpen_omega_engine_root()
    identities, binding = resolve_import_identities(
        tree,
        playpen / "engine" / "linear_algebra_domain_worker.py",
        playpen,
    )
    assert any(
        i.endswith("linear_algebra.gram_schmidt") or i == "gram_schmidt"
        for i in identities
    )
    assert "gram_schmidt" in binding
    assert binding["gram_schmidt"].endswith("linear_algebra.gram_schmidt")


def test_importfrom_parent_module_forbidden() -> None:
    forbidden = stub_identities_from_inventory()
    audit = audit_source(
        "engine/linear_algebra_domain_worker.py",
        "from omega_engine.crates.linear_algebra_theory import gram_schmidt\n"
        "from omega_engine.crates.functional.phi1 import residual_l1\n"
        "class W:\n"
        "    def run(self):\n"
        "        return residual_l1([1.0])\n",
        role="domain_worker",
        forbidden_modules=forbidden,
    )
    assert not audit.ok
    assert any("STUB_MIRROR" in i or "gram_schmidt" in i for i in audit.issues)


def test_importfrom_relative_forbidden() -> None:
    forbidden = stub_identities_from_inventory()
    audit = audit_source(
        "engine/linear_algebra_domain_worker.py",
        "from ..linear_algebra import gram_schmidt\n"
        "from omega_engine.crates.functional.phi1 import residual_l1\n"
        "class W:\n"
        "    def run(self):\n"
        "        return residual_l1([1.0])\n",
        role="domain_worker",
        forbidden_modules=forbidden,
    )
    assert not audit.ok


def test_discover_role_not_filename_only(tmp_path: Path) -> None:
    engine = tmp_path / "engine"
    engine.mkdir()
    (engine / "domain_worker.py").write_text(
        "class DomainWorker:\n    pass\n", encoding="utf-8"
    )
    (engine / "functional_domain_worker.py").write_text(
        "from .domain_worker import DomainWorker\n"
        "class FunctionalDomainWorker(DomainWorker):\n"
        "    pass\n",
        encoding="utf-8",
    )
    (engine / "weird_name.py").write_text(
        "from .functional_domain_worker import FunctionalDomainWorker\n"
        "class QuantumWorker(FunctionalDomainWorker):\n"
        "    pass\n",
        encoding="utf-8",
    )
    (engine / "helper_dep.py").write_text("X = 1\n", encoding="utf-8")
    (engine / "weird_name.py").write_text(
        "from .functional_domain_worker import FunctionalDomainWorker\n"
        "from .helper_dep import X\n"
        "class QuantumWorker(FunctionalDomainWorker):\n"
        "    pass\n",
        encoding="utf-8",
    )
    (engine / "engine.py").write_text("class Engine:\n    pass\n", encoding="utf-8")
    found = {rel: (via, role) for rel, via, role in discover_audit_targets(tmp_path)}
    assert "engine/weird_name.py" in found
    assert found["engine/weird_name.py"][0] == "ast_subclass_closure"
    assert "engine/helper_dep.py" in found
    assert found["engine/helper_dep.py"][1] == "worker_dependency"


def test_positive_delegation_required() -> None:
    # DomainWorker without residual import/call fails even without DIY
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        class W(DomainWorker):
            def run(self, xs):
                return 0.0
        """
    )
    audit = audit_source("engine/functional_domain_worker.py", src, role="domain_worker")
    assert not audit.ok
    assert any("positively import" in i or "positively call" in i for i in audit.issues)


def test_positive_delegation_with_approved_ok() -> None:
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1
        class W(DomainWorker):
            def run(self, xs):
                return residual_l1(xs)
        """
    )
    audit = audit_source("engine/functional_domain_worker.py", src, role="domain_worker")
    assert audit.ok, audit.issues
    assert audit.delegated_symbols


def test_diy_without_delegation_fails() -> None:
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        class W(DomainWorker):
            def run(self, xs):
                return sum(abs(x) for x in xs)
        """
    )
    audit = audit_source("engine/functional_domain_worker.py", src, role="domain_worker")
    assert not audit.ok


def test_dead_approved_call_live_diy_fails() -> None:
    """OMC P1 kill: file-scope delegation must not greenwash live DIY in run()."""
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1
        class W(DomainWorker):
            def _dead(self):
                return residual_l1([0.0])
            def run(self, xs):
                return sum(abs(x) for x in xs)
        """
    )
    audit = audit_source("engine/functional_domain_worker.py", src, role="domain_worker")
    assert not audit.ok, "dead residual_l1 + live DIY must FAIL path-sensitive gate"
    assert any("live run()" in i or "path-sensitive" in i for i in audit.issues)


def test_one_task_delegates_other_diy_fails() -> None:
    """OMC P1 kill: mixed task dispatch — DIY task hard-fails even if sibling delegates."""
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1
        class W(DomainWorker):
            def run(self, inp):
                if inp.task_kind == "good":
                    return self._good(inp)
                return self._bad(inp)
            def _good(self, inp):
                return residual_l1(inp.payload.get("xs", [1.0]))
            def _bad(self, inp):
                xs = inp.payload.get("xs", [1.0])
                return sum(abs(x) for x in xs)
        """
    )
    audit = audit_source("engine/mixed_worker.py", src, role="domain_worker")
    assert not audit.ok
    assert any("_bad" in i or "path-sensitive" in i or "live run()" in i for i in audit.issues)


# Unique base so natural L1 mass cannot accidentally equal the spy result.
_RESIDUAL_SPY_SENTINEL_BASE = 881337.0


def _patch_playpen_symbol(monkeypatch: pytest.MonkeyPatch, name: str, spy: Any) -> int:
    """Patch name on every loaded canonical omega-engine module that defines it."""
    import sys

    n = 0
    for mod_name, mod in list(sys.modules.items()):
        if not mod_name.startswith("omega_engine"):
            continue
        if hasattr(mod, name):
            monkeypatch.setattr(mod, name, spy, raising=False)
            n += 1
    return n


def _vecs_close(a: Any, b: Any, tol: float = 1e-9) -> bool:
    try:
        la = list(a)
        lb = list(b)
    except TypeError:
        return False
    if len(la) != len(lb):
        return False
    return all(abs(float(x) - float(y)) < tol for x, y in zip(la, lb))


def test_module_helper_diy_not_greenwashed_by_sibling_delegation() -> None:
    """OMC close-out kill: module-level helper DIY outside self.method graph."""
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1

        def helper(xs):
            return sum(abs(x) for x in xs)

        class W(DomainWorker):
            def run(self, inp):
                if inp.task_kind == "good":
                    return residual_l1(inp.payload["xs"])
                return helper(inp.payload["xs"])
        """
    )
    audit = audit_source("engine/helper_worker.py", src, role="domain_worker")
    assert not audit.ok, audit.issues
    assert any(
        "helper" in i or "same-module" in i or "path-sensitive" in i for i in audit.issues
    )


def test_imported_helper_diy_with_side_kernel_call_fails(tmp_path: Path) -> None:
    """OMC final kill: residual_l1([0]) side call + imported compute_metric DIY."""
    engine = tmp_path / "engine"
    engine.mkdir()
    (engine / "domain_worker.py").write_text(
        "class DomainWorker:\n    pass\n", encoding="utf-8"
    )
    (engine / "helper_dep.py").write_text(
        "def compute_metric(xs):\n    return sum(abs(x) for x in xs)\n",
        encoding="utf-8",
    )
    src = textwrap.dedent(
        """
        from .domain_worker import DomainWorker
        from .helper_dep import compute_metric
        from omega_engine.crates.functional.phi1 import residual_l1

        class W(DomainWorker):
            def run(self, inp):
                _ = residual_l1([0.0])
                return compute_metric(inp.payload.get("xs", [1.0, -2.0]))
        """
    )
    (engine / "bypass_worker.py").write_text(src, encoding="utf-8")
    audit = audit_source(
        "engine/bypass_worker.py",
        src,
        root=tmp_path,
        role="domain_worker",
    )
    assert not audit.ok, audit.issues
    assert any(
        "imported live helper" in i or "compute_metric" in i or "helper_dep" in i
        for i in audit.issues
    )


def test_side_kernel_call_does_not_bind_emitted_residual() -> None:
    """Runtime binding law: residual_l1([0]) side call must not greenwash DIY field."""
    from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
    from omega_engine.crates.type.engine_io import (
        DomainWorkerInput,
        DomainWorkerOutput,
    )

    r1_log: List[Dict[str, Any]] = []

    def r1_spy(xs, *args, **kwargs):  # type: ignore[no-untyped-def]
        xs_l = [float(x) for x in xs]
        result = _RESIDUAL_SPY_SENTINEL_BASE + sum(abs(x) for x in xs_l) * 1e-9
        r1_log.append({"xs": xs_l, "result": result})
        return result

    class BypassWorker(DomainWorker):
        def __init__(self) -> None:
            super().__init__(worker_id="bypass", worker_version="test")

        def supported_task_kinds(self):
            return ("bad",)

        def run(self, inp: DomainWorkerInput) -> DomainWorkerOutput:
            _ = r1_spy([0.0])  # side call — satisfies hit-only quantifier
            xs = list(inp.payload.get("xs", [1.0, -2.0, 3.0]))
            r = sum(abs(x) for x in xs)  # DIY residual for emitted field
            return self._output(
                task_id=inp.task_id,
                task_kind=inp.task_kind,
                status="SOLVED",
                result={"r": r},
                residual_vector=xs,
                residual_l1=float(r),
                math_path=["diy"],
            )

    out = BypassWorker().run(
        DomainWorkerInput(
            task_id="b",
            task_kind="bad",
            payload={"xs": [1.0, -2.0, 3.0]},
            parameters={},
        )
    )
    assert r1_log, "side call should hit spy"
    results = {e["result"] for e in r1_log}
    bound = any(abs(float(out.residual_l1) - r) < 1e-9 for r in results)
    assert not bound, "DIY residual_l1 field must not equal residual_l1 spy sentinel"
    # vector provenance also fails: spy saw [0.0], output vector is payload
    assert not any(_vecs_close(out.residual_vector, e["xs"]) for e in r1_log)
    # Binding predicate used by taskwise spy suite
    vector_bound = any(
        _vecs_close(out.residual_vector, e["xs"])
        and abs(float(out.residual_l1) - e["result"]) < 1e-9
        for e in r1_log
    )
    assert not vector_bound


def test_comment_sum_abs_ok() -> None:
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1
        class W(DomainWorker):
            def run(self, xs):
                # never use sum(abs — use residual_l1
                return residual_l1(xs)
        """
    )
    audit = audit_source("engine/functional_domain_worker.py", src, role="domain_worker")
    assert audit.ok, audit.issues


def test_local_def_residual_math_caught() -> None:
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1
        def phi1(x):
            return 0.0
        class W(DomainWorker):
            def run(self):
                return residual_l1([1.0])
        """
    )
    audit = audit_source("engine/functional_domain_worker.py", src, role="domain_worker")
    assert not audit.ok


def test_helper_import_bypass_caught() -> None:
    forbidden = stub_identities_from_inventory()
    # invent a residual-related helper path that is STUB if present
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.linear_algebra_theory.gram_schmidt import foo
        from omega_engine.crates.functional.phi1 import residual_l1
        class W(DomainWorker):
            def run(self, xs):
                return residual_l1(xs)
        """
    )
    audit = audit_source(
        "engine/functional_domain_worker.py",
        src,
        role="domain_worker",
        forbidden_modules=forbidden,
    )
    assert not audit.ok
    assert any("STUB_MIRROR" in i for i in audit.issues)


def test_live_auditor_and_gates_bootstrap() -> None:
    ok, audits, report = audit_playpen()
    assert ok, [(a.rel_path, a.issues) for a in audits if not a.ok]
    assert report["forbidden_stub_module_count"] > 3
    result = run_all_gates(allow_bootstrap=True)
    # Measurement may be green; ordinary PASS requires EVALUATOR_BOUND_TO_ANCHOR.
    assert result.get("measure_ok") is True, result.get("violations")
    assert result["authority_effect"] == "None"
    assert result["wave_e_status"] == "NOT_COMPLETE"
    assert result["prototype_status"] == "USEFUL_DIAGNOSTIC"
    receipt = result["evidence_receipt"]
    assert receipt is not None
    assert receipt["authority_effect"] == "None"
    assert receipt["policy_version"] in ("wave-e-v4", "wave-f-v1", "wave-g-v1")
    assert receipt["baseline_digest"]
    assert receipt["evaluator_hash"]
    assert receipt["receipt_digest"]
    assert receipt["discovered_dependency_set"]
    assert receipt["audited_target_hashes"]
    if result.get("gate_admission") == "EVALUATOR_BOUND_TO_ANCHOR":
        assert result["ok"] is True
    else:
        assert result["ok"] is False
    # Post Wave E land on main: anchor baseline exists — measure without bootstrap.
    result_main = run_all_gates(allow_bootstrap=False)
    assert result_main.get("measure_ok") is True, result_main.get("violations")
    assert result_main["stub_ratchet"]["measured"].get("has_anchor") is True
    if result_main.get("gate_admission") == "EVALUATOR_BOUND_TO_ANCHOR":
        assert result_main["ok"] is True
    else:
        assert result_main["ok"] is False
        assert any(
            "VERIFIER_RECEIPT_REQUIRED" in v
            for v in (result_main.get("violations") or [])
        )


def test_evidence_receipt_binds_fields(tmp_path: Path) -> None:
    policy = load_policy()
    receipt = build_evidence_receipt(
        repo_root=tmp_path,
        policy=policy,
        baseline_digest="abc",
        ok=True,
        violations=[],
        audited_target_hashes={"engine/x.py": "deadbeef"},
        dependency_set=["engine/x.py", "functional/phi1.py"],
        evaluator_head={"digest": "e1", "files": {}},
        evaluator_anchor={"digest": "e1", "files": {}},
        anchor_ref="origin/main",
        allow_bootstrap=False,
        ratchet_report={"ok": True},
        import_report={"ok": True},
    )
    assert receipt["evaluator_locus"] == "protected_anchor_hash_match"
    assert receipt["gate_admission"] == "EVALUATOR_BOUND_TO_ANCHOR"
    assert receipt["receipt_digest"]
    # digest is self-binding
    body = {k: v for k, v in receipt.items() if k != "receipt_digest"}
    assert receipt["receipt_digest"] == sha256_json(body)


def _spy_payload_for_task(task_kind: str) -> Optional[Dict[str, Any]]:
    """Minimal payloads for discovered task kinds (None => skip runtime spy)."""
    if task_kind == "residual_l1":
        return {"residual": [1.0, -2.0, 3.0]}
    if task_kind == "gamma2":
        return {
            "d1": {"rows": 2, "cols": 3, "data": [1.0, -1.0, 0.0, 0.0, 1.0, -1.0]},
            "h": [1.0, 0.0, 0.0],
        }
    if task_kind == "incidence_residual":
        return {
            "n_nodes": 2,
            "edges": [[0, 1]],
            "alpha": [1.0, 0.0],
            "omega1": [1.0],
        }
    if task_kind == "matmul":
        return {
            "a": {"rows": 2, "cols": 2, "data": [1.0, 0.0, 0.0, 1.0]},
            "b": {"rows": 2, "cols": 2, "data": [1.0, 0.0, 0.0, 1.0]},
            "expected": {"rows": 2, "cols": 2, "data": [1.0, 0.0, 0.0, 1.0]},
        }
    if task_kind == "gram_schmidt":
        return {"columns": [[1.0, 0.0], [1.0, 1.0]]}
    if task_kind == "obstruction_analyze":
        return {
            "vertices": [0, 1, 2],
            "edges": [[0, 1], [1, 2], [0, 2]],
            "faces": [[0, 1, 2]],
            "h_vector": [0.1, 0.2, 0.3],
        }
    if task_kind == "mur_l1_gauge":
        return {
            "vertices": [0, 1, 2],
            "edges": [[0, 1], [1, 2], [0, 2]],
            "cochain": [0.1, 0.2, 0.3],
        }
    if task_kind == "foc_curvature":
        return {
            "n_nodes": 3,
            "edges": [[0, 1], [1, 2], [0, 2]],
            "faces": [[0, 1, 2]],
            "cochain": [0.1, 0.2, 0.3],
        }
    return None


def test_discovered_worker_spy_matrix_not_hand_picked() -> None:
    matrix = discover_worker_spy_matrix()
    assert len(matrix) >= 3
    classes = {row["class_name"] for row in matrix}
    assert "FunctionalDomainWorker" in classes
    assert "LinearAlgebraDomainWorker" in classes
    assert "CodaDomainWorker" in classes
    for row in matrix:
        assert row["task_kinds"], row
        assert "run" in row["live_methods"]
        # expanded constants, not raw _TASK_* names alone
        assert not all(k.startswith("_TASK_") for k in row["task_kinds"])


# Explicit non-residual task exemptions (role/contract). Empty default: every
# discovered DomainWorker task is residual-producing EvidenceOnly and must hit
# an approved kernel under spy. Add a kind here only with a written justification.
NON_RESIDUAL_TASK_EXEMPTIONS: Dict[str, str] = {}


def test_discovered_workers_delegate_via_spy_taskwise(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Forall task_kind: hit approved kernel AND bind emitted residual to spy result.

    OMC final: existence of a residual_l1 call is not provenance of residual_l1 field.
    """
    import importlib

    from omega_engine.crates.type.engine_io import DomainWorkerInput

    matrix = discover_worker_spy_matrix()
    assert matrix, "discovery returned empty spy matrix"
    task_rows_exercised = 0
    for row in matrix:
        # Import worker (and deps) before patching so modules are loaded
        mod = importlib.import_module(row["module"])
        cls = getattr(mod, row["class_name"])

        r1_log: List[Dict[str, Any]] = []
        g2_log: List[Any] = []

        def r1_spy(xs, *args, _log=r1_log, **kwargs):  # type: ignore[no-untyped-def]
            try:
                xs_l = [float(x) for x in xs]
            except TypeError:
                xs_l = list(xs) if xs is not None else []
            result = _RESIDUAL_SPY_SENTINEL_BASE + sum(abs(x) for x in xs_l) * 1e-9
            _log.append({"xs": xs_l, "result": float(result)})
            return float(result)

        def g2_spy(*args, _log=g2_log, **kwargs):  # type: ignore[no-untyped-def]
            import numpy as np

            from omega_engine.crates.functional.gamma2 import (
                ClosureStatus,
            )

            _log.append(args)

            class _G:
                value = _RESIDUAL_SPY_SENTINEL_BASE * 0.1
                is_closed = True
                closure_status = ClosureStatus.CLOSED
                coboundary = np.asarray([0.0, 0.0], dtype=float)

            return _G()

        n_r1 = _patch_playpen_symbol(monkeypatch, "residual_l1", r1_spy)
        n_g2 = _patch_playpen_symbol(monkeypatch, "gamma2", g2_spy)
        assert n_r1 >= 1, "failed to patch residual_l1 anywhere in playpen modules"

        worker = cls()
        assert row["task_kinds"], f"{row['class_name']} has no discovered task kinds"
        for kind in row["task_kinds"]:
            if kind in NON_RESIDUAL_TASK_EXEMPTIONS:
                continue
            payload = _spy_payload_for_task(kind)
            assert payload is not None, (
                f"{row['class_name']} task {kind!r}: no spy payload and no "
                f"NON_RESIDUAL_TASK_EXEMPTIONS entry — cannot prove forall-task "
                f"delegation (OMC quantifier)"
            )
            r1_log.clear()
            g2_log.clear()
            out = worker.run(
                DomainWorkerInput(
                    task_id=f"spy-{row['class_name']}-{kind}",
                    task_kind=kind,
                    payload=payload,
                    parameters={},
                )
            )
            hit = bool(r1_log) or bool(g2_log)
            assert hit, (
                f"{row['class_name']} task {kind!r} did not call residual_l1/gamma2 "
                f"under spy (status={getattr(out, 'status', None)}; "
                f"live_methods={row['live_methods']}). "
                f"Exists-task satisfaction must not waive this task."
            )
            # Provenance: emitted residual_l1 must equal a residual_l1 spy return
            # (canonical kernel result flows to evidence field).
            if r1_log:
                results = {e["result"] for e in r1_log}
                bound = any(
                    abs(float(out.residual_l1) - r) < 1e-9 for r in results
                )
                if out.residual_vector:
                    bound = bound and any(
                        _vecs_close(out.residual_vector, e["xs"])
                        and abs(float(out.residual_l1) - e["result"]) < 1e-9
                        for e in r1_log
                    )
                assert bound, (
                    f"{row['class_name']} task {kind!r}: emitted residual_l1="
                    f"{out.residual_l1} residual_vector={getattr(out, 'residual_vector', None)} "
                    f"not bound to residual_l1 spy results {list(results)[:5]} "
                    f"(side-call greenwash refused; status={getattr(out, 'status', None)})"
                )
            task_rows_exercised += 1
    assert task_rows_exercised >= 6, (
        f"expected >=6 discovered (worker,task) spy rows, got {task_rows_exercised}"
    )


def test_taskwise_spy_a_does_not_satisfy_b(monkeypatch: pytest.MonkeyPatch) -> None:
    """Synthetic worker: task A delegates, task B DIYs — forall spy must fail B."""
    import types

    from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
    from omega_engine.crates.functional.phi1 import residual_l1 as real_r1
    from omega_engine.crates.type.engine_io import (
        DomainWorkerInput,
        DomainWorkerOutput,
    )

    calls: List[Any] = []

    def spy(xs, *args, **kwargs):  # type: ignore[no-untyped-def]
        calls.append(list(xs))
        return real_r1(xs)

    class MixedWorker(DomainWorker):
        def __init__(self) -> None:
            super().__init__(worker_id="mixed", worker_version="test")

        def supported_task_kinds(self):
            return ("good", "bad")

        def run(self, inp: DomainWorkerInput) -> DomainWorkerOutput:
            xs = list(inp.payload.get("xs", [1.0, -1.0]))
            if inp.task_kind == "good":
                r = spy(xs)
                return self._output(
                    task_id=inp.task_id,
                    task_kind=inp.task_kind,
                    status="SOLVED",
                    result={"r": r},
                    residual_vector=xs,
                    residual_l1=r,
                    math_path=["spy"],
                )
            # DIY residual path for bad task
            r = sum(abs(x) for x in xs)
            return self._output(
                task_id=inp.task_id,
                task_kind=inp.task_kind,
                status="SOLVED",
                result={"r": r},
                residual_vector=xs,
                residual_l1=float(r),
                math_path=["diy"],
            )

    # Static gate must already refuse this shape via helper/method DIY
    src = textwrap.dedent(
        """
        from omega_engine.crates.runtime.rt_domain_worker import DomainWorker
        from omega_engine.crates.functional.phi1 import residual_l1
        class MixedWorker(DomainWorker):
            def run(self, inp):
                xs = inp.payload.get("xs", [1.0])
                if inp.task_kind == "good":
                    return residual_l1(xs)
                return sum(abs(x) for x in xs)
        """
    )
    audit = audit_source("engine/mixed_ab.py", src, role="domain_worker")
    assert not audit.ok

    # Runtime quantifier: good hits spy, bad must not be waived by good
    worker = MixedWorker()
    calls.clear()
    worker.run(
        DomainWorkerInput(
            task_id="a", task_kind="good", payload={"xs": [1.0, -2.0]}, parameters={}
        )
    )
    assert calls, "task A must hit residual spy"
    calls.clear()
    worker.run(
        DomainWorkerInput(
            task_id="b", task_kind="bad", payload={"xs": [1.0, -2.0]}, parameters={}
        )
    )
    assert not calls, "task B DIY must not call residual spy — A must not satisfy B"


def test_policy_and_baseline_present() -> None:
    assert baseline_path().is_file()
    policy = load_policy()
    assert policy["policy_version"] in ("wave-e-v4", "wave-f-v1", "wave-g-v1")
    assert len(policy["approved_residual_symbols"]) >= 3
    assert baseline_digest(load_baseline())



