# -*- coding: utf-8 -*-
"""Static notebook checks only; replay runs in verification/replay_notebooks.py."""
import ast
import json
from pathlib import Path

import nbformat
import pytest

NOTEBOOK_DIR = Path(__file__).resolve().parents[2] / "jupyter_notebooks"
NOTEBOOKS = [
    "000_moving_a_picture_to_a_coarser_one.ipynb",
    "001_when_two_moves_compose.ipynb",
    "002_what_you_cannot_get_back.ipynb",
]


@pytest.mark.parametrize("nb_name", NOTEBOOKS)
def test_notebook_stored_output_format(nb_name: str) -> None:
    """Validate schema and available outputs without launching a kernel."""
    nb_path = NOTEBOOK_DIR / nb_name
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    nbformat.validate(nbformat.from_dict(data))
    code_cells = [cell for cell in data["cells"] if cell["cell_type"] == "code"]
    assert code_cells
    for cell in code_cells:
        source = "".join(cell["source"])
        ast.parse(source)
        assert cell["execution_count"] is None or isinstance(cell["execution_count"], int)
        assert all(out["output_type"] != "error" for out in cell["outputs"])

