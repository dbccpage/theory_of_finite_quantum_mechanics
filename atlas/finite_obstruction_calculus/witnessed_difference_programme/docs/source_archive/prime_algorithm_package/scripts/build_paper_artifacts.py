"""Build oe_prime_algorithms.tex and .pdf from Markdown sources.

pandoc writes the LaTeX; pdflatex runs twice with a fixed SOURCE_DATE_EPOCH
so the dates and the trailer ID are stable.

``python scripts/build_paper_artifacts.py`` writes both files;
``--out DIR`` writes them elsewhere (used by the reproducibility check).
AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
STEM = "oe_prime_algorithms"
SOURCE_DATE_EPOCH = "1790424000"  # 2026-09-26T12:00:00Z
FAIL_MARKERS = ("Missing character:", "Undefined control sequence", "LaTeX Error")


def tool_versions() -> dict[str, str]:
    versions = {}
    for tool in ("pandoc", "pdflatex"):
        out = subprocess.run([tool, "--version"], capture_output=True, text=True, check=True).stdout
        versions[tool] = out.splitlines()[0].strip()
    return versions


def spine_body() -> str:
    text = (PACKAGE / f"{STEM}.md").read_text(encoding="utf-8")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    text = re.sub(r"^# .*\n", "", text, count=1, flags=re.M)
    return text


def assemble() -> str:
    parts = [
        "---",
        'title: "Algorithm Prime Triad: Candidate Intake, Adapter Descent, and Continuation Control"',
        'author: "Jeremy H. Carroll"',
        'date: "Version 1.0.0 — 2026-09-26"',
        "---",
        "",
        spine_body(),
    ]
    return "\n".join(parts)


def build(out_dir: Path) -> list[str]:
    env = dict(os.environ, SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH, FORCE_SOURCE_DATE="1")
    with tempfile.TemporaryDirectory(prefix="prime-pdf-") as tmp:
        work = Path(tmp)
        (work / "combined.md").write_text(assemble(), encoding="utf-8")
        subprocess.run(
            [
                "pandoc",
                "combined.md",
                "--from",
                "markdown",
                "--to",
                "latex",
                "--standalone",
                "--toc",
                "--include-in-header",
                str(PACKAGE / "scripts" / "preamble.tex"),
                "--variable",
                "geometry:margin=1in",
                "--variable",
                "fontsize=11pt",
                "--variable",
                "colorlinks=true",
                "--output",
                f"{STEM}.tex",
            ],
            cwd=work,
            env=env,
            check=True,
        )
        tex_path = work / f"{STEM}.tex"
        tex_content = tex_path.read_text(encoding="utf-8")
        title_block = r"""\makeatletter
\begin{center}
{\LARGE \@title\par}
\vspace{0.8em}
{\normalsize \@author\par}
\vspace{0.5em}
{\small \@date\par}
\end{center}
\makeatother"""
        tex_content = tex_content.replace(r"\maketitle", title_block)
        tex_path.write_text(tex_content, encoding="utf-8")
        for _ in range(3):
            run = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{STEM}.tex"],
                cwd=work,
                env=env,
                capture_output=True,
                text=True,
            )
            if run.returncode:
                sys.stderr.write(run.stdout[-3000:])
                return ["pdflatex failed"]
        log = (work / f"{STEM}.log").read_text(encoding="utf-8", errors="replace")
        problems = [marker for marker in FAIL_MARKERS if marker in log]
        overfull = log.count("Overfull \\hbox")
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(work / f"{STEM}.tex", out_dir / f"{STEM}.tex")
        shutil.copyfile(work / f"{STEM}.pdf", out_dir / f"{STEM}.pdf")
    print(f"built {STEM}.tex and {STEM}.pdf ({overfull} overfull hbox warnings)")
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=PACKAGE)
    args = parser.parse_args(argv)
    problems = build(args.out)
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
