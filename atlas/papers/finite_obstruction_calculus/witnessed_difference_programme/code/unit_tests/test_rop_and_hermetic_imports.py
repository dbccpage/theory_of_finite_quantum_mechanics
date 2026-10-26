# Executable finite evidence; AuthorityEffect: None.
"""The package's own railway values, and the deposit's import boundary."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from witnessed_difference.rop import Err, Ok, Refusal

CODE = Path(__file__).resolve().parents[1]
ENGINE_PREFIXES = ("omega_engine",)


def test_ok_and_err_map_and_bind() -> None:
    assert Ok(2).map(lambda value: value + 1) == Ok(3)
    assert Ok(2).bind(lambda value: Ok(value * 5)) == Ok(10)
    refusal = Refusal(code="NOT_EXACT", message="residual is nonzero")
    err = Err(refusal)
    assert err.map(lambda value: value + 1) is err
    assert err.bind(lambda value: Ok(value)) is err
    with pytest.raises(ValueError, match="cannot unwrap Err"):
        err.unwrap()
    with pytest.raises(ValueError, match="cannot unwrap_err"):
        Ok(1).unwrap_err()


def test_refusal_normalizes_and_refuses_bad_fields() -> None:
    refusal = Refusal(
        code=" NO_RULE ", message=" none ", locus=" here ", details=(("b", "2"), ("a", "1"))
    )
    assert refusal.to_dict() == {
        "code": "NO_RULE",
        "message": "none",
        "locus": "here",
        "details": {"a": "1", "b": "2"},
    }
    with pytest.raises(ValueError, match="canonical identifier"):
        Refusal(code="not an id", message="x")
    with pytest.raises(ValueError, match="non-empty"):
        Refusal(code="X", message="  ")
    with pytest.raises(ValueError, match="unique"):
        Refusal(code="X", message="x", details=(("k", "1"), ("k", "2")))


def _module_level_engine_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[str] = []
    # Only statements outside function bodies run at import time. The two live
    # provider runners import engine packages inside run(), by design.
    stack: list[ast.AST] = list(tree.body)
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        if isinstance(node, ast.Import):
            found.extend(a.name for a in node.names if a.name.startswith(ENGINE_PREFIXES))
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith(ENGINE_PREFIXES):
                found.append(node.module)
        stack.extend(ast.iter_child_nodes(node))
    return found


def test_deposit_code_imports_no_engine_package_at_module_level() -> None:
    offenders = {
        path.relative_to(CODE).as_posix(): names
        for path in sorted(CODE.rglob("*.py"))
        if "rust" not in path.relative_to(CODE).parts[:1]
        and (names := _module_level_engine_imports(path))
    }
    assert offenders == {}


def test_import_scanner_sees_a_module_level_engine_import(tmp_path: Path) -> None:
    sample = tmp_path / "sample.py"
    sample.write_text(
        "import omega_engine_x\n"
        "if True:\n    from omega_engine_y.z import q\n"
        "def run():\n    from omega_engine_w import v\n",
        encoding="utf-8",
    )
    assert sorted(_module_level_engine_imports(sample)) == ["omega_engine_x", "omega_engine_y.z"]
