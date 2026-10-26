"""Execute the walkthrough with this Python interpreter and a temporary kernel."""

import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient


def replay() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "jupyter_notebooks/01_coda_walkthrough.ipynb"
    with TemporaryDirectory(prefix="coda-notebook-") as scratch:
        directory = Path(scratch)
        kernel = directory / "kernels" / "coda-local"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(
            json.dumps(
                {
                    "argv": [
                        sys.executable,
                        "-m",
                        "ipykernel_launcher",
                        "-f",
                        "{connection_file}",
                    ],
                    "display_name": "CODA local replay",
                    "language": "python",
                }
            ),
            encoding="utf-8",
        )
        os.environ["IPYTHONDIR"] = str(directory / "ipython")
        os.environ["JUPYTER_RUNTIME_DIR"] = str(directory / "runtime")
        os.environ["JUPYTER_CONFIG_DIR"] = str(directory / "config")
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        manager = KernelManager(
            kernel_name="coda-local",
            kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel.parent)]),
        )
        notebook = nbformat.read(path, as_version=4)
        client = NotebookClient(
            notebook,
            km=manager,
            timeout=90,
            record_timing=False,
            resources={"metadata": {"path": str(root)}},
        )
        client.execute(cleanup_kc=True)
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
        count = sum(cell.cell_type == "code" for cell in notebook.cells)
        print(f"Executed {count} code cells; all assertions passed.")


if __name__ == "__main__":
    replay()
