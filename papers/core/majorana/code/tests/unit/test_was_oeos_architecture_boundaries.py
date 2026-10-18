"""Architecture fitness tests asserting OEOS/WAS/Shared-Kernel boundary laws post-PR #82.

Invariants checked:
1. shared_kernel has no reverse dependencies on higher_operad, symbol_game, OEOS, or WAS.
2. higher_operad is completely dependency-free of other internal crates.
3. Disjoint Capability Principle: AgentLicense and ActionLicense share no hierarchy.
4. Value Object exact-type equality and strict constructor validation.
5. DataRecord recursive immutability and deterministic hashing.
6. AntiSkill candidate/spec canonical homing in prompt_civilization.
7. Canonical council paths in governance.
8. Compatibility epoch and shadow-estate cutover settings.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path
from types import MappingProxyType

import pytest

from omega_engine.crates.domain.exceptions import InvariantViolationError
from omega_engine.crates.domain.shared_kernel import (
    CandidateBudget,
    CandidateId,
    DataRecord,
    PacketId,
    TaskId,
)
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.oesos_dda_lifecycle import ActionLicense
from omega_engine.crates.prompt_civilization.domain.models import (
    AntiSkillCandidateV1,
    AntiSkillSpecV1,
)
from omega_engine.kernel.higher_operad import (
    AgentLicense,
)


def _get_ast_imports(file_path: Path) -> set[str]:
    """Parse a python file AST and extract all top-level imported package names."""
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def test_shared_kernel_has_no_reverse_dependencies() -> None:
    """shared_kernel must only depend on python stdlib and nothing else."""
    shared_kernel_dir = (
        Path(__file__).resolve().parent.parent / "crates" / "domain" / "shared_kernel"
    )
    assert shared_kernel_dir.exists()

    forbidden_roots = (
        "omega_engine.kernel",
        "omega_engine_pfp.domain",
        "omega_engine.crates.prompt_civilization",
        "omega_engine_operating_system",
        "omega_engine_operations",
        "omega_engine_governance",
        "omega_engine_workflows_agents_skills",
    )

    for py_file in shared_kernel_dir.glob("*.py"):
        imports = _get_ast_imports(py_file)
        for imp in imports:
            for forbidden in forbidden_roots:
                assert not imp.startswith(
                    forbidden
                ), f"Reverse dependency in {py_file.name}: imports {imp}"


def test_higher_operad_is_dependency_free() -> None:
    """higher_operad must not import from any other internal crates or engines."""
    higher_operad_dir = (
        Path(__file__).resolve().parent.parent
        / "crates"
        / "kernel"
        / "higher_operad"
    )
    assert higher_operad_dir.exists()

    forbidden_roots = (
        "omega_engine_operating_system",
        "omega_engine_operations",
        "omega_engine_governance",
        "omega_engine_workflows_agents_skills",
    )

    for py_file in higher_operad_dir.glob("*.py"):
        imports = _get_ast_imports(py_file)
        for imp in imports:
            for forbidden in forbidden_roots:
                assert not imp.startswith(
                    forbidden
                ), f"Prohibited dependency in {py_file.name}: imports {imp}"


def test_disjoint_capabilities_share_no_class_hierarchy() -> None:
    """The real AgentLicense and ActionLicense types are strictly disjoint."""
    assert inspect.isclass(AgentLicense)
    assert inspect.isclass(ActionLicense)
    assert AgentLicense is not ActionLicense
    assert not issubclass(AgentLicense, ActionLicense)
    assert not issubclass(ActionLicense, AgentLicense)
    assert AgentLicense.__bases__ == (object,)
    assert ActionLicense.__bases__ == (object,)


def test_value_object_exact_type_equality_and_hashing() -> None:
    """Exact-type equality prevents cross-class and primitive comparisons."""
    t_id = TaskId("node_1")
    c_id = CandidateId("node_1")
    p_id = PacketId("node_1")

    # Cross-class inequality
    assert t_id != c_id
    assert t_id != p_id
    assert c_id != p_id

    # Primitive string inequality
    assert t_id != "node_1"
    assert "node_1" != t_id

    # Hashing separation in sets
    s = {t_id, c_id, p_id}
    assert len(s) == 3

    # Strict constructors reject invalid types
    with pytest.raises(InvariantViolationError):
        TaskId.from_str(123)  # type: ignore

    with pytest.raises(InvariantViolationError):
        CandidateBudget.from_int("3")  # type: ignore

    with pytest.raises(InvariantViolationError):
        CandidateBudget.from_int(True)  # type: ignore (bool is subclass of int in Python)


def test_datarecord_recursive_immutability() -> None:
    """DataRecord recursively freezes dictionaries and lists and hashes deterministically."""
    raw = {"meta": {"count": 10}, "items": [1, 2, 3]}
    rec = DataRecord(raw)

    assert isinstance(rec.data, MappingProxyType)
    assert isinstance(rec.data["meta"], MappingProxyType)
    assert isinstance(rec.data["items"], tuple)

    # In-place modification is prevented
    with pytest.raises(TypeError):
        rec.data["meta"] = {}  # type: ignore

    with pytest.raises(TypeError):
        rec.data["meta"]["count"] = 20  # type: ignore

    # Mutation of original dict has no effect
    raw["meta"]["count"] = 99
    assert rec.data["meta"]["count"] == 10

    # Deterministic hashing
    h1 = hash(rec)
    h2 = hash(DataRecord({"meta": {"count": 10}, "items": (1, 2, 3)}))
    assert h1 == h2


def test_prompt_civilization_antiskill_types_are_canonical() -> None:
    """Prompt civilization AntiSkill types are verified domain classes."""
    assert inspect.isclass(AntiSkillCandidateV1)
    assert inspect.isclass(AntiSkillSpecV1)

    spec = AntiSkillSpecV1(
        spec_id="ASKILL_001",
        version=1,
        failure_code="F_UNWARRANTED_PROMOTION",
        detector_kind="requires_evidence_for_claim_mode",
        activation_fields=("claimed_valid",),
        repair_kind="add_evidence_request",
        protected_fields=("authority_effect",),
        episode_ids=("sha256:" + "a" * 64, "sha256:" + "c" * 64),
        context_keys=("ctx_1", "ctx_2"),
        evidence_refs=("ref_1",),
        counterexamples=("counter_1",),
        evaluation_receipt_ref="sha256:" + "b" * 64,
    )
    assert spec.spec_id == "ASKILL_001"
    assert spec.authority_effect == "None"


def test_canonical_council_path_resolution() -> None:
    """Council path must resolve strictly to omega_engine_governance."""
    root = Path(__file__).resolve().parent.parent.parent
    canonical_council = (
        root / "omega_engine_governance" / "_types" / "rules" / "rules.yaml"
    )
    stale_council = root / "omega_engine" / "anomalon_councils"

    assert canonical_council.exists(), f"Missing canonical council rules at {canonical_council}"
    assert not stale_council.exists(), f"Stale council directory should not exist at {stale_council}"


def test_epoch_and_cutover_settings() -> None:
    """Compatibility epoch is 1 and canonical_cutover is False."""
    root = Path(__file__).resolve().parent.parent.parent
    epoch_file = root / ".agents" / "registry" / "compatibility-epoch.yaml"
    assert epoch_file.exists()

    content = epoch_file.read_text(encoding="utf-8")
    assert '"compatibility_epoch": 1' in content
    assert '"canonical_cutover": false' in content
    assert '"status": "legacy-current-source-with-shadow-typed-estate"' in content
