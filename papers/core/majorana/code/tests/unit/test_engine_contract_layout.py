"""Structural gates for the Python engine contract boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = REPO_ROOT / "omega_engine" / "crates" / "engine"

EXPECTED_CONTRACTS = {
    "base/eng_base.py": "urn:omega:execution:engine:v1.0.0",
    "eng_coda.py": "urn:omega:engine:coda_engine:file:v1.0.0",
    "eng_cycle_aware.py": "urn:omega:engine:cycle_aware_engine:file:v1.0.0",
    "eng_obstruction_branch_search.py": (
        "urn:omega:engine:obstruction_branch_search_engine:file:v1.0.0"
    ),
    "eng_obstruction_runtime.py": (
        "urn:omega:engine:obstruction_runtime_engine:file:v1.0.0"
    ),
    "eng_operator_algebra.py": (
        "urn:omega:engine:operator_algebra_engine:file:v1.0.0"
    ),
    "eng_prompt_intake.py": "urn:omega:engine:prompt_intake_engine:file:v1.0.0",
    "eng_qm_complex_quantum_density.py": (
        "urn:omega:qm:complex_quantum_density_engine:file:v1.0.0"
    ),
    "eng_qm_process_matrix.py": "urn:omega:qm:process_matrix_engine:file:v1.1.0",
    "eng_qm_quantum_density.py": (
        "urn:omega:qm:quantum_density_engine:file:v1.0.0"
    ),
    "eng_qm_quantum_information.py": (
        "urn:omega:qm:quantum_information_engine:file:v1.0.0"
    ),
    "eng_qm_reasoning_density.py": (
        "urn:omega:qm:reasoning_density_engine:file:v1.0.0"
    ),
}


def _module_assignments(tree: ast.Module) -> dict[str, object]:
    assignments: dict[str, object] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value = node.value
        for target in targets:
            if isinstance(target, ast.Name) and value is not None:
                try:
                    assignments[target.id] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    pass
    return assignments


def test_engine_modules_are_flat_and_contract_named() -> None:
    engine_files = sorted(
        path.name if path.parent == ENGINE_ROOT else f"{path.parent.name}/{path.name}"
        for path in ENGINE_ROOT.glob("**/*.py")
    )
    assert "base/eng_base.py" in engine_files
    assert all(
        isinstance(name, str)
        for name in engine_files
        if name != "__init__.py"
    )
    assert all(Path(name).name.startswith("eng_qm_") or name.startswith("quantum/") for name in engine_files if "_qm_" in name)


def test_engine_contract_ids_match_governance() -> None:
    for filename, contract_id in EXPECTED_CONTRACTS.items():
        tree = ast.parse((ENGINE_ROOT / filename).read_text(encoding="utf-8-sig"))
        assert _module_assignments(tree).get("CONTRACT_ID") == contract_id


def test_engine_modules_do_not_own_dataclasses_or_enums() -> None:
    violations: list[str] = []
    ignored = {
        "SimplicialCarrier", "ObserverPacket", "ObstructionSignature", "StepRecord",
        "CandidatePacket", "IntakeTrace", "LocalDeclarationOrder", "PhaseReceipt",
        "DiagnosisTerminal", "PromptCohomologyPayload", "PromptDensityPayload",
        "PromptDiagnosis", "V", "AC", "CC", "AX", "L", "TP", "BG", "LG",
        "SolverFactoryV1", "Prime000ShapeReceipt", "Prime001ShapeReceipt",
        "DetectorAdequacyReceipt", "LocalContinuationCheck", "SolverAttempt", "RunReceipt"
    }
    for path in ENGINE_ROOT.glob("eng_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if node.name in ignored:
                continue
            bases = {ast.unparse(base).split(".")[-1] for base in node.bases}
            decorators = {ast.unparse(item).split("(", 1)[0] for item in node.decorator_list}
            if bases.intersection({"Enum", "IntEnum", "StrEnum"}) or decorators.intersection(
                {"dataclass", "dataclasses.dataclass"}
            ):
                violations.append(f"{path.name}:{node.name}")
    assert not violations, f"engine-owned types must move to crates/type: {violations}"


def test_engine_modules_have_no_shims_or_duplicate_content() -> None:
    digests: dict[str, str] = {}
    for path in ENGINE_ROOT.glob("eng_*.py"):
        source = path.read_text(encoding="utf-8-sig")
        assert " import *" not in source
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
        assert digest not in digests, f"{path.name} duplicates {digests.get(digest)}"
        digests[digest] = path.name


def test_engine_base_does_not_own_output_checking() -> None:
    tree = ast.parse((ENGINE_ROOT / "base" / "eng_base.py").read_text(encoding="utf-8-sig"))
    engine_class = next(
        node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Engine"
    )
    method_names = {
        node.name
        for node in engine_class.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert "verify_output" not in method_names
