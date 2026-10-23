"""Replay each notebook in an independent host process and pinned Python kernel.

Run from the detached package: python verification/replay_notebooks.py
Add --write to refresh stored outputs only after successful execution.
The parent prints a JSON receipt; failures propagate as nonzero exit status.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def worker(path: Path, write: bool) -> dict:
    # nbclient is imported only by an independent worker, never by pytest.
    import nbformat
    from jupyter_client.kernelspec import KernelSpecManager
    from nbclient import NotebookClient

    package = path.parent.parent
    notebook = nbformat.read(path, as_version=4)
    with tempfile.TemporaryDirectory(prefix="mur-notebook-kernel-") as temp:
        kernel = Path(temp) / "kernels" / "mur-verification"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "MUR verification", "language": "python",
        }), encoding="utf-8")
        manager = KernelSpecManager(kernel_dirs=[str(kernel.parent)])
        client = NotebookClient(
            notebook, timeout=60, kernel_name="mur-verification",
            resources={"metadata": {"path": str(package)}},
        )
        client.create_kernel_manager()
        client.km.kernel_spec_manager = manager
        client.execute()
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    if any(output.output_type == "error" for cell in code_cells for output in cell.outputs):
        raise RuntimeError(f"Error output in {path.name}")
    if write:
        nbformat.write(notebook, path)
    return {"notebook": path.name, "status": "passed", "code_cells": len(code_cells),
            "python": sys.executable, "cwd": str(package)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker.resolve(), args.write)))
        return
    package = Path(__file__).resolve().parent.parent
    receipts = []
    for notebook in sorted((package / "jupyter_notebooks").glob("*.ipynb")):
        command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(notebook)]
        if args.write:
            command.append("--write")
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        result = subprocess.run(command, cwd=package, env=env, text=True,
                                capture_output=True, check=True, timeout=300)
        receipts.append(json.loads(result.stdout))
    print(json.dumps({"notebooks": receipts}, indent=2))


if __name__ == "__main__":
    main()

