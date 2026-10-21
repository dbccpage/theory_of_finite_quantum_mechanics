"""Architecture fitness tests for crates/domain and shared_kernel admission.

PR-1 freeze: no type moves. These tests fail the build when
(1) a kernel file is missing from admission.yaml,
(2) shared_kernel imports anything outside stdlib / domain.exceptions /
    sibling kernel modules,
(3) crates/domain imports runtime or a second type catalog,
(4) duplicate AuthorityEffect / Result / Refusal counts rise.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

import yaml

ENGINE_ROOT = Path(__file__).resolve().parent.parent
DOMAIN_ROOT = ENGINE_ROOT / "crates" / "domain"
KERNEL_ROOT = DOMAIN_ROOT / "shared_kernel"
ADMISSION_PATH = DOMAIN_ROOT / "admission.yaml"

ALLOWED_TAGS = frozenset({"keep", "evict:symbol_game", "review", "reexport"})
SNAPSHOT_NAMES = ("authority_effect", "result", "refusal")
COUNTED_DEF_NAMES = {
    "authority_effect": "AuthorityEffect",
    "result": "Result",
    "refusal": "Refusal",
}
DOMAIN_IMPORT_PREFIX = "omega_engine.crates.domain"
FORBIDDEN_HOST_PREFIXES = (
    "omega_engine_operations",
    "omega_engine_governance",
    "omega_engine_operating_system",
    "omega_engine_workflows_agents_skills",
)
ALLOWED_ABSOLUTE_PREFIXES = (
    "omega_engine.crates.domain.exceptions",
    "omega_engine.crates.domain.shared_kernel",
)
STDLIB_ROOTS = set(sys.stdlib_module_names) | {"__future__"}
EXCLUDE_DIR_DEFAULT = ("_experiments", "target", "__pycache__")


def _load_admission() -> dict:
    assert ADMISSION_PATH.is_file(), f"missing admission file: {ADMISSION_PATH}"
    payload = yaml.safe_load(ADMISSION_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), "admission.yaml must be a mapping"
    return payload


def _kernel_py_files() -> list[Path]:
    files = sorted(p for p in KERNEL_ROOT.rglob("*.py") if p.is_file())
    assert files, f"no kernel python files under {KERNEL_ROOT}"
    return files


def _domain_py_files() -> list[Path]:
    files = sorted(p for p in DOMAIN_ROOT.rglob("*.py") if p.is_file())
    assert files, f"no domain python files under {DOMAIN_ROOT}"
    return files


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))


def _resolved_imported_modules(tree: ast.Module, package: str) -> list[tuple[int, str]]:
    """Return absolute module names, resolving relative imports."""
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                if node.module:
                    found.append((node.lineno, node.module))
                continue

            relative_name = "." * node.level + (node.module or "")
            resolved = importlib.util.resolve_name(relative_name, package)
            if node.module:
                found.append((node.lineno, resolved))
            else:
                for alias in node.names:
                    if alias.name != "*":
                        found.append((node.lineno, f"{resolved}.{alias.name}"))
                if not node.names or any(alias.name == "*" for alias in node.names):
                    found.append((node.lineno, resolved))
    return found


def _imported_modules(path: Path) -> list[tuple[int, str]]:
    tree = _parse(path)
    package = ".".join(path.parent.relative_to(ENGINE_ROOT.parent).parts)
    return _resolved_imported_modules(tree, package)


def _is_allowed_kernel_absolute(module: str) -> bool:
    root = module.split(".", 1)[0]
    if root in STDLIB_ROOTS:
        return True
    return any(
        module == prefix or module.startswith(prefix + ".")
        for prefix in ALLOWED_ABSOLUTE_PREFIXES
    )


def _is_forbidden_domain_import(module: str) -> bool:
    if module == "omega_engine" or module.startswith("omega_engine."):
        return not (
            module == DOMAIN_IMPORT_PREFIX
            or module.startswith(DOMAIN_IMPORT_PREFIX + ".")
        )
    return any(
        module == prefix or module.startswith(prefix + ".")
        for prefix in FORBIDDEN_HOST_PREFIXES
    )


def _module_level_definitions(
    path: Path, names: frozenset[str]
) -> list[tuple[str, int]]:
    tree = _parse(path)
    hits: list[tuple[str, int]] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in names:
            hits.append((node.name, node.lineno))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    hits.append((target.id, node.lineno))
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id in names
        ):
            hits.append((node.target.id, node.lineno))
    return hits


def _iter_engine_py(exclude_dir_names: tuple[str, ...] | list[str]) -> list[Path]:
    excluded = set(exclude_dir_names)
    files: list[Path] = []
    for path in ENGINE_ROOT.rglob("*.py"):
        relative_parts = path.relative_to(ENGINE_ROOT).parts
        if any(part in excluded for part in relative_parts):
            continue
        files.append(path)
    return files


def test_admission_yaml_lists_every_shared_kernel_module() -> None:
    admission = _load_admission()
    modules = admission.get("modules")
    assert isinstance(modules, dict) and modules, (
        "admission.yaml modules must be a non-empty mapping"
    )

    disk = {path.relative_to(KERNEL_ROOT).as_posix() for path in _kernel_py_files()}
    listed = set(modules)
    missing_on_disk = listed - disk
    missing_in_yaml = disk - listed
    assert not missing_on_disk, (
        f"admission.yaml names files that are not on disk: {sorted(missing_on_disk)}"
    )
    assert not missing_in_yaml, (
        f"shared_kernel files missing from admission.yaml: {sorted(missing_in_yaml)}"
    )

    for name, row in modules.items():
        assert isinstance(row, dict), f"{name} admission row must be a mapping"
        tag = row.get("tag")
        assert tag in ALLOWED_TAGS, f"{name} has illegal tag {tag!r}"


def test_shared_kernel_imports_only_stdlib_exceptions_and_siblings() -> None:
    offenders: list[str] = []
    for path in _kernel_py_files():
        for lineno, module in _imported_modules(path):
            if not _is_allowed_kernel_absolute(module):
                offenders.append(f"{path.name}:{lineno} imports {module}")
    assert offenders == [], "shared_kernel absolute import violations:\n" + "\n".join(
        offenders
    )


def test_crates_domain_does_not_import_runtime_or_type_catalog() -> None:
    offenders: list[str] = []
    for path in _domain_py_files():
        rel = path.relative_to(ENGINE_ROOT).as_posix()
        for lineno, module in _imported_modules(path):
            if _is_forbidden_domain_import(module):
                offenders.append(f"{rel}:{lineno} imports {module}")
    assert offenders == [], "crates/domain import violations:\n" + "\n".join(offenders)


def test_duplicate_type_snapshots_have_not_increased() -> None:
    admission = _load_admission()
    snapshots = admission.get("snapshots")
    assert isinstance(snapshots, dict), "admission.yaml snapshots must be a mapping"
    exclude = snapshots.get("exclude_dir_names", list(EXCLUDE_DIR_DEFAULT))
    counted = {name: 0 for name in COUNTED_DEF_NAMES.values()}
    parse_failures: list[str] = []
    for path in _iter_engine_py(exclude):
        try:
            hits = _module_level_definitions(
                path, frozenset(COUNTED_DEF_NAMES.values())
            )
        except (SyntaxError, UnicodeDecodeError) as exc:
            parse_failures.append(f"{path.as_posix()}: {exc}")
            continue
        for name, _lineno in hits:
            counted[name] += 1
    assert parse_failures == [], "could not parse engine files:\n" + "\n".join(
        parse_failures
    )

    actual = {key: counted[class_name] for key, class_name in COUNTED_DEF_NAMES.items()}
    expected = {key: snapshots.get(key) for key in SNAPSHOT_NAMES}
    for key in SNAPSHOT_NAMES:
        assert type(expected[key]) is int and expected[key] >= 0, (
            f"snapshot {key} must be a non-negative int"
        )
    assert actual == expected, (
        "duplicate-type snapshot drift "
        f"(actual={actual} expected={expected}); "
        "counts may only decrease, and admission.yaml must be updated in the same PR"
    )


def test_relative_imports_are_resolved_before_dependency_checks() -> None:
    tree = ast.parse(
        "from ...epk import Registry\n"
        "from .id import Identifier\n"
        "from .. import exceptions\n"
    )
    resolved = _resolved_imported_modules(
        tree, "omega_engine.crates.domain.shared_kernel"
    )
    assert resolved == [
        (1, "omega_engine.crates.epk"),
        (2, "omega_engine.crates.domain.shared_kernel.id"),
        (3, "omega_engine.crates.domain.exceptions"),
    ]
    assert not _is_allowed_kernel_absolute(resolved[0][1])
    assert _is_forbidden_domain_import(resolved[0][1])
