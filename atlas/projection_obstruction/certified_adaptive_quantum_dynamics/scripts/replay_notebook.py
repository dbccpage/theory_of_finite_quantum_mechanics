#!/usr/bin/env python3
"""Replay committed notebook code cells in a fresh headless Python process."""

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-notebook-dir", action="store_true")
    args = parser.parse_args()
    os.environ["MPLBACKEND"] = "Agg"
    os.chdir(ROOT / "jupyter_notebooks" if args.from_notebook_dir else ROOT)
    notebook = json.loads((ROOT / "jupyter_notebooks/001_reviewer_adaptive_quantum.ipynb").read_text(encoding="utf-8"))
    scope = {"__name__": "__notebook_replay__"}
    count = 0
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] == "code":
            if cell["outputs"] or cell["execution_count"] is not None:
                raise ValueError("committed notebook must have cleared outputs and execution counts")
            exec(compile("".join(cell["source"]), f"notebook-cell-{index}", "exec"), scope)
            count += 1
    import matplotlib.pyplot as plt
    plt.close("all")
    print(f"OK: {count} notebook code cells replayed from {Path.cwd().name}; no live widgets tested")


if __name__ == "__main__":
    main()
