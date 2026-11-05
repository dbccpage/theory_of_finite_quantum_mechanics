#!/usr/bin/env python3
"""Build the centered manuscript from Markdown with Pandoc and XeLaTeX."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEM = "so_k_invariant_gauge_classification"


def latex_fragment(source: str) -> str:
    return subprocess.run(
        ["pandoc", "--from=markdown+tex_math_dollars+raw_tex", "--to=latex"],
        input=source, text=True, capture_output=True, check=True,
    ).stdout.strip()


def main() -> None:
    source = (ROOT / f"{STEM}.md").read_text(encoding="utf-8")
    front, body = source.split("</div>", 1)
    title = re.search(r"^# (.+)$", front, re.M)
    subtitle = re.search(r"^## (.+)$", front, re.M)
    fields = re.findall(r"\*\*(Author|Date|Version|License):\*\*\s*(.*?)(?=\s*&nbsp;|\n|$)", front)
    if title is None or subtitle is None or [name for name, _ in fields] != [
        "Author", "Date", "Version", "License",
    ]:
        raise ValueError("Manuscript requires the centered title and four-field header")
    values = dict(fields)
    epoch = int(datetime.strptime(values["Date"], "%Y-%m-%d").replace(
        hour=12, tzinfo=timezone.utc,
    ).timestamp())
    rendered = [latex_fragment(f"**{name}:** {value}") for name, value in fields]
    header = (
        "\\begin{center}\n"
        "{\\LARGE \\textbf{" + latex_fragment(title.group(1)) + "}}\\\\[0.4em]\n"
        "{\\large \\textbf{" + latex_fragment(subtitle.group(1)) + "}}\\\\[1em]\n"
        + rendered[0] + " \\quad " + rendered[1] + "\\\\[0.4em]\n"
        + rendered[2] + " \\quad " + rendered[3] + "\n"
        "\\end{center}\n\\vspace{1em}\n\n"
    )
    with tempfile.TemporaryDirectory(prefix="gs002-paper-") as directory:
        build = Path(directory)
        tex = build / f"{STEM}.tex"
        subprocess.run(
            ["pandoc", "--from=markdown+tex_math_dollars+raw_tex", "--to=latex",
             "--standalone", "--template", str(ROOT / "scripts/paper_template.tex"),
             "--output", str(tex)],
            input=header + body, text=True, encoding="utf-8", check=True,
        )
        env = {**os.environ, "SOURCE_DATE_EPOCH": str(epoch), "FORCE_SOURCE_DATE": "1"}
        for _ in range(2):
            process = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                cwd=build, env=env, capture_output=True, text=True, encoding="utf-8",
            )
            if process.returncode != 0:
                raise RuntimeError(process.stdout + process.stderr)
        log = (build / f"{STEM}.log").read_text(encoding="utf-8", errors="replace")
        if "Missing character:" in log or "Overfull \\hbox" in log or "Overfull \\vbox" in log:
            raise RuntimeError("Inspect and repair missing glyphs or overfull boxes:\n" + log)
        for suffix in ["tex", "pdf"]:
            shutil.copyfile(build / f"{STEM}.{suffix}", ROOT / f"{STEM}.{suffix}")
        print(f"Built {STEM}.tex and {STEM}.pdf; no missing glyphs or overfull boxes.")


if __name__ == "__main__":
    main()
