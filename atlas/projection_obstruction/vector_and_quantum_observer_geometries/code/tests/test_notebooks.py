"""Test execution integrity of companion notebooks."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

PAPER_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = sorted((PAPER_ROOT / "jupyter_notebooks").glob("*.ipynb"))


@pytest.mark.parametrize("notebook_path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_has_valid_executed_cells(notebook_path: Path) -> None:
    """Ensure companion notebook is valid and all code cells ran with zero errors."""
    data = json.loads(notebook_path.read_text(encoding="utf-8"))
    code_cells = [c for c in data.get("cells", []) if c.get("cell_type") == "code"]
    assert code_cells, f"Notebook {notebook_path.name} has no code cells"

    for i, cell in enumerate(code_cells):
        assert cell.get("execution_count") is not None, (
            f"Cell {i} in {notebook_path.name} is unexecuted"
        )
        for out in cell.get("outputs", []):
            assert out.get("output_type") != "error", (
                f"Cell {i} in {notebook_path.name} has error output: {out}"
            )
