#!/usr/bin/env python3
"""Execute plain-Python notebook cells when kernel sockets are unavailable.

This explicit mode uses Python exec and an Agg figure capture. It verifies code
and assertions, but not a Jupyter kernel, notebook magics, or widget interaction.
Each notebook is executed in its own subprocess from outside the package root.
Without --record, checked-in notebook bytes are never rewritten.
"""

from __future__ import annotations

import base64
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "inline_code_companion.ipynb",
    "refutation_sandbox.ipynb",
    "reviewer_coordinate_additivity.ipynb",
)


def execute(source: Path, destination: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    notebook = json.loads(source.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__", "__file__": str(source)}
    outputs: list[dict[str, object]] = []

    def show(*args: object, **kwargs: object) -> None:
        for number in plt.get_fignums():
            stream = io.BytesIO()
            plt.figure(number).savefig(stream, format="png", dpi=110)
            outputs.append({"output_type": "display_data", "metadata": {}, "data": {
                "image/png": base64.b64encode(stream.getvalue()).decode("ascii"),
                "text/plain": ["<Figure rendered by explicit direct-Python replay>"]}})
        plt.close("all")

    plt.show = show
    os.chdir(ROOT / "jupyter_notebooks")
    count = 0
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        count += 1
        outputs = []
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(compile("".join(cell["source"]), f"{source.name}:cell{index}", "exec"), namespace)
        for name, stream in (("stdout", stdout), ("stderr", stderr)):
            if stream.getvalue():
                outputs.append({"output_type": "stream", "name": name,
                                "text": stream.getvalue().splitlines(keepends=True)})
        cell["execution_count"] = count
        cell["outputs"] = outputs
    notebook.setdefault("metadata", {})["review_execution"] = {
        "method": "direct-python-exec-with-agg", "date": "2026-10-02",
        "python": sys.version.split()[0], "kernel_replay": False,
        "scope": "Plain Python cells and assertions; no widget or kernel verification",
    }
    destination.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    print(f"PASS {source.name}: {count} code cells (direct Python; no Jupyter kernel)")


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "--worker":
        execute(Path(argv[1]), Path(argv[2]))
        return 0
    if argv not in ([], ["--record"]):
        print("usage: direct_notebook_replay.py [--record]", file=sys.stderr)
        return 2
    actual = {path.name for path in (ROOT / "jupyter_notebooks").glob("*.ipynb")}
    if actual != set(NAMES):
        raise ValueError("notebook inventory mismatch")
    with tempfile.TemporaryDirectory(prefix="cwa-direct-replay-") as temporary:
        for name in NAMES:
            source = ROOT / "jupyter_notebooks" / name
            destination = Path(temporary) / name
            subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker",
                            str(source), str(destination)], cwd=ROOT.parent, check=True)
            if argv == ["--record"]:
                source.write_bytes(destination.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
