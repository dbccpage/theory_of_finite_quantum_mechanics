"""Replay the exact example cells; only --write updates the notebook."""
from pathlib import Path
import argparse
import json
import os
import sys
import tempfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "jupyter_notebooks/000_pre_genesis_to_mssn_walkthrough.ipynb"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    stored = nbformat.read(PATH, as_version=4)
    notebook = nbformat.read(PATH, as_version=4)
    with tempfile.TemporaryDirectory(prefix="pre-mssn-kernel-") as kernel:
        directory = Path(kernel) / "kernels/pre-mssn-python"
        directory.mkdir(parents=True)
        (directory / "kernel.json").write_text(json.dumps(dict(
            argv=[sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            display_name="Pre-MSSN Python", language="python")), encoding="utf-8")
        previous = os.environ.get("JUPYTER_PATH")
        os.environ["JUPYTER_PATH"] = kernel + (os.pathsep + previous if previous else "")
        try:
            NotebookClient(notebook, timeout=300, kernel_name="pre-mssn-python",
                           resources={"metadata": {"path": str(ROOT)}}).execute()
        finally:
            if previous is None:
                os.environ.pop("JUPYTER_PATH", None)
            else:
                os.environ["JUPYTER_PATH"] = previous
    if args.write:
        nbformat.write(notebook, PATH)
        count = sum(c.cell_type == "code" for c in notebook.cells)
        print(f"Executed and stored {count} code cells without errors")
    else:
        before = [(c.execution_count, c.outputs) for c in stored.cells if c.cell_type == "code"]
        after = [(c.execution_count, c.outputs) for c in notebook.cells if c.cell_type == "code"]
        if before != after:
            raise ValueError("Fresh notebook execution differs from stored outputs")
        print(f"Fresh execution matches all {len(after)} stored code cells; payload unchanged")
