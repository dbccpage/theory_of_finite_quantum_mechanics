"""Replay each notebook in a fresh kernel using this interpreter.

--write retains outputs; --check compares deterministic outputs with the deposit.
Run this script as a subprocess, never inside pytest's interpreter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def outputs(notebook: dict) -> list:
    return [(cell.get("execution_count"), cell.get("outputs", []))
            for cell in notebook["cells"] if cell["cell_type"] == "code"]


def replay(*, write: bool = False, cwd: Path = PACKAGE) -> list[str]:
    import nbformat
    from nbclient import NotebookClient

    problems = []
    with tempfile.TemporaryDirectory(prefix="ddc-kernel-") as tmp:
        kernel = Path(tmp) / "kernels" / "ddc-review"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-X", "utf8", "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "DDC isolated replay",
            "language": "python",
            "env": {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        }), encoding="utf-8")
        previous = os.environ.get("JUPYTER_PATH")
        os.environ["JUPYTER_PATH"] = tmp + (os.pathsep + previous if previous else "")
        try:
            for path in sorted((PACKAGE / "jupyter_notebooks").glob("*.ipynb")):
                notebook = nbformat.read(path, as_version=4)
                nbformat.validator.normalize(notebook)
                old_outputs = outputs(notebook)
                source = json.dumps([(c.cell_type, c.source) for c in notebook.cells], ensure_ascii=False)
                NotebookClient(notebook, timeout=120, kernel_name="ddc-review", record_timing=False,
                               resources={"metadata": {"path": str(cwd)}}).execute()
                if any(count is None or any(o.get("output_type") == "error" for o in result)
                       for count, result in outputs(notebook)):
                    problems.append(f"invalid execution evidence: {path.name}")
                if write:
                    nbformat.validator.normalize(notebook)
                    notebook.metadata["ddc_replay"] = {
                        "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                        "method": "nbclient-fresh-kernel",
                    }
                    path.write_text(nbformat.writes(notebook), encoding="utf-8", newline="\n")
                elif old_outputs != outputs(notebook):
                    problems.append(f"stale notebook outputs: {path.name}")
                print(f"notebook: {path.name} replayed with {sys.executable}")
        finally:
            if previous is None:
                os.environ.pop("JUPYTER_PATH", None)
            else:
                os.environ["JUPYTER_PATH"] = previous
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    parser.add_argument("--cwd", type=Path, default=PACKAGE)
    args = parser.parse_args()
    problems = replay(write=args.write, cwd=args.cwd.resolve())
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
