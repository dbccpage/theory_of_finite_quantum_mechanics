#!/usr/bin/env python3
"""Replay the exact companion-notebook inventory in isolated subprocesses.

Run with ``uv run --frozen --extra notebooks python scripts/replay_notebooks.py``.
Source notebooks are never overwritten; the command prints a JSON receipt that
binds each source digest to its temporary executed-output digest.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = (
    "jupyter_notebooks/so_k_invariant_gauge_classification.ipynb",
    "jupyter_notebooks/visual_gauge_rigidity_and_separation.ipynb",
)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_executed_notebook(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    code_cells = [cell for cell in data.get("cells", []) if cell.get("cell_type") == "code"]
    if not code_cells:
        raise RuntimeError(f"{path.name} contains no code cells")
    for index, cell in enumerate(code_cells):
        if cell.get("execution_count") is None:
            raise RuntimeError(f"{path.name} cell {index} was not executed")
        errors = [
            output
            for output in cell.get("outputs", [])
            if output.get("output_type") == "error"
        ]
        if errors:
            raise RuntimeError(f"{path.name} cell {index} produced an error output")


def main() -> int:
    actual = tuple(
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "jupyter_notebooks").glob("*.ipynb"))
    )
    if actual != tuple(sorted(NOTEBOOKS)):
        print(
            f"FAIL: notebook inventory mismatch: expected {sorted(NOTEBOOKS)!r}, got {actual!r}",
            file=sys.stderr,
        )
        return 1

    notebook_receipts: list[dict[str, object]] = []
    try:
        nbconvert_version = importlib.metadata.version("nbconvert")
    except importlib.metadata.PackageNotFoundError:
        print(
            "FAIL: nbconvert is not installed in the active environment.\n"
            "Invoke with: uv run --frozen --extra notebooks python scripts/replay_notebooks.py",
            file=sys.stderr,
        )
        return 1

    receipt: dict[str, object] = {
        "schema": "paper.notebook_replay.v1",
        "python": sys.version,
        "nbconvert": nbconvert_version,
        "notebooks": notebook_receipts,
        "claim_scope": "executed examples only; no theorem or publication authority",
    }
    try:
        with tempfile.TemporaryDirectory(prefix="paper008-notebooks-") as temp_name:
            temp_dir = Path(temp_name)
            for relative in NOTEBOOKS:
                source = ROOT / relative
                before = sha256_of(source)
                output_name = source.stem + ".executed.ipynb"
                command = [
                    sys.executable,
                    "-m",
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "notebook",
                    "--execute",
                    str(source),
                    "--output",
                    output_name,
                    "--output-dir",
                    str(temp_dir),
                    "--ExecutePreprocessor.timeout=300",
                    "--ExecutePreprocessor.kernel_name=python3",
                ]
                process = subprocess.run(
                    command,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=360,
                )
                if process.returncode != 0:
                    raise RuntimeError(
                        f"replay failed for {relative}:\n{process.stdout}\n{process.stderr}"
                    )
                executed = temp_dir / output_name
                validate_executed_notebook(executed)
                if sha256_of(source) != before:
                    raise RuntimeError(f"source notebook changed during replay: {relative}")
                notebook_receipts.append(
                    {
                        "path": relative,
                        "source_sha256": before,
                        "executed_sha256": sha256_of(executed),
                        "command": command,
                    }
                )
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
