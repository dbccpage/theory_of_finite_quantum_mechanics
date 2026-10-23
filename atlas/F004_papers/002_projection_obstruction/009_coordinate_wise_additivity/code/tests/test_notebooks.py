"""Test execution integrity of companion notebooks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

PAPER_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = PAPER_ROOT / "jupyter_notebooks"
EXPECTED_NOTEBOOK_NAMES = (
    "inline_code_companion.ipynb",
    "refutation_sandbox.ipynb",
    "reviewer_coordinate_additivity.ipynb",
)
NOTEBOOKS = [NOTEBOOK_DIR / name for name in EXPECTED_NOTEBOOK_NAMES]
REPLAYED_SOURCE_SHA256 = {
    "inline_code_companion.ipynb": "29970e4cfe6384b78ebfe01df940cfece21ba1253bbe7f06270f1c24d6263e30",
    "refutation_sandbox.ipynb": "9f057eca51368b19e7cb80ec7a8157ab3bda9b19296b187c5e167268124317a5",
    "reviewer_coordinate_additivity.ipynb": "446e072514f9dd02c0079a43b505dc9eefec7c5c4df38a041d2cc75d06c5d6e7",
}


def test_notebook_inventory_is_exact() -> None:
    """Fail closed if a required notebook is missing or an unreviewed one appears."""
    actual = {path.name for path in NOTEBOOK_DIR.glob("*.ipynb")}
    assert actual == set(EXPECTED_NOTEBOOK_NAMES)


def test_notebook_sources_match_direct_python_receipt() -> None:
    """Bind the reviewed source bytes to the 2026-10-02 direct-Python computational receipt."""
    actual = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in NOTEBOOKS
    }
    assert actual == REPLAYED_SOURCE_SHA256


@pytest.mark.parametrize("notebook_path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_has_valid_executed_cells(notebook_path: Path) -> None:
    """Check stored direct-Python output structure; this does not attest kernel replay."""
    data = json.loads(notebook_path.read_text(encoding="utf-8"))
    assert data["metadata"]["review_execution"]["method"] == "direct-python-exec-with-agg"
    assert data["metadata"]["review_execution"]["kernel_replay"] is False
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
