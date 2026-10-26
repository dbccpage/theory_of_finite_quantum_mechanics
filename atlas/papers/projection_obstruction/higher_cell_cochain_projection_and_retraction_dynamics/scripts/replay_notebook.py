"""Replay PO-034's notebook, explicitly separating kernel and direct modes."""

from __future__ import annotations

import argparse
import atexit
import contextlib
import hashlib
import io
import json
import os
import platform
import sys
import tempfile
from datetime import date
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "jupyter_notebooks/034_higher_cell_projection_demo.ipynb"


def source_digest(nb) -> str:
    source = [{"type": c.cell_type, "source": c.source} for c in nb.cells]
    return hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()


def replay(direct: bool, record: bool) -> None:
    nb = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(nb)
    digest = source_digest(nb)
    code = str(ROOT / "code")
    with tempfile.TemporaryDirectory(prefix="po034-notebook-") as raw:
        work = Path(raw)
        if direct:
            namespace = {"__name__": "__main__"}
            sys.path.insert(0, code)
            old_cwd = Path.cwd()
            count = 0
            try:
                os.chdir(work)
                for i, cell in enumerate(nb.cells):
                    if cell.cell_type != "code":
                        continue
                    if any(
                        line.lstrip().startswith(("%", "!")) for line in cell.source.splitlines()
                    ):
                        raise ValueError("direct mode does not support IPython magics")
                    count += 1
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                        exec(compile(cell.source, f"{NOTEBOOK.name}:cell-{i}", "exec"), namespace)
                    cell.execution_count = count
                    cell.outputs = (
                        [nbformat.v4.new_output("stream", name="stdout", text=output.getvalue())]
                        if output.getvalue()
                        else []
                    )
            finally:
                os.chdir(old_cwd)
                sys.path.remove(code)
            method = "direct-python-exec"
        else:
            from jupyter_client import AsyncKernelManager
            from jupyter_client.kernelspec import KernelSpecManager
            from nbclient import NotebookClient

            kernel = work / "kernels/po034"
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
                        "display_name": "PO-034 pinned Python",
                        "language": "python",
                    }
                )
            )

            class PinnedKernelManager(AsyncKernelManager):
                def __init__(self, **kwargs):
                    kwargs["kernel_spec_manager"] = KernelSpecManager(
                        kernel_dirs=[str(kernel.parent)]
                    )
                    super().__init__(**kwargs)

            client = NotebookClient(
                nb,
                kernel_name="po034",
                kernel_manager_class=PinnedKernelManager,
                timeout=45,
                resources={"metadata": {"path": str(work)}},
            )
            try:
                environment = dict(os.environ)
                environment["PYTHONPATH"] = code
                client.execute(env=environment)
            finally:
                # Avoid a duplicate atexit cleanup after the manager is closed.
                if client.km is None:
                    atexit.unregister(client._cleanup_kernel)
            count = sum(c.cell_type == "code" for c in nb.cells)
            method = "native-jupyter-kernel"
    nb.metadata["po034_execution"] = {
        "method": method,
        "kernel_replay": not direct,
        "date": date.today().isoformat(),
        "python": platform.python_version(),
        "cell_source_sha256": digest,
        "code_cells": count,
    }
    nbformat.validate(nb)
    if record:
        nbformat.write(nb, NOTEBOOK)
    print(f"PASS {method}: {count} code cells; source {digest}; recorded={record}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--direct", action="store_true", help="explicit direct Python mode, not a kernel fallback"
    )
    parser.add_argument(
        "--record", action="store_true", help="write outputs only after successful execution"
    )
    args = parser.parse_args()
    try:
        replay(args.direct, args.record)
    except Exception as error:
        print(
            f"FAIL {'direct Python' if args.direct else 'native Jupyter'}: {type(error).__name__}: {error}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
