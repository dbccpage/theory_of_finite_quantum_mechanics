#!/usr/bin/env python3
"""Rebuild the additivity manuscript with Pandoc 3 and XeLaTeX."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = "coordinate_wise_additivity"


def main() -> None:
    source = (ROOT / f"{STEM}.md").read_text(encoding="utf-8")
    body = source.split("\n", 1)[1]
    preamble = (ROOT / "scripts/paper_preamble.tex").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="cwa-pdf-") as temporary:
        build = Path(temporary)
        (build / "body.md").write_text(body, encoding="utf-8")
        subprocess.run([
            "pandoc", "--from", "markdown+tex_math_single_backslash", "--to", "latex",
            "--lua-filter", str(ROOT / "scripts/latex_inline_code.lua"),
            "body.md", "-o", "body.tex",
        ], cwd=build, check=True)
        heading = r"""
\title{Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection (GS-000)}
\author{Jeremy H. Carroll}
\date{Unpublished repository draft: 2026-10-02}
\begin{document}
\maketitle
"""
        tex = preamble + heading + (build / "body.tex").read_text() + "\n\\end{document}\n"
        (build / f"{STEM}.tex").write_text(tex, encoding="utf-8")
        environment = dict(os.environ, SOURCE_DATE_EPOCH="1790899200")
        for _ in range(2):
            completed = subprocess.run([
                "xelatex", "-interaction=nonstopmode", "-halt-on-error", f"{STEM}.tex",
            ], cwd=build, env=environment, text=True, capture_output=True, timeout=90)
            if completed.returncode:
                raise RuntimeError(completed.stdout[-8000:] + completed.stderr)
        log = (build / f"{STEM}.log").read_text(errors="replace")
        serious = [line for line in log.splitlines() if
                   "Overfull" in line or "Missing character" in line]
        if serious:
            raise RuntimeError("Layout diagnostics:\n" + "\n".join(serious))
        assert re.search(r"Output written on", log)
        (ROOT / f"{STEM}.tex").write_text(tex, encoding="utf-8")
        (ROOT / f"{STEM}.pdf").write_bytes((build / f"{STEM}.pdf").read_bytes())
        print("PASS: TeX/PDF rebuilt with no overfull or missing-character warnings")


if __name__ == "__main__":
    main()
