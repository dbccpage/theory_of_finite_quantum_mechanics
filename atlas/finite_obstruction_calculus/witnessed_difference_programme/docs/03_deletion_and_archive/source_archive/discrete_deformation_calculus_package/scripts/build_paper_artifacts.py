"""Build discrete_deformation_calculus.tex and .pdf from the Markdown sources.

The spine, the eight chapters and the appendices are assembled in that order.
The spine's own title heading is dropped (the assembler prints a centered title block) and
its headings are promoted one level so that spine sections, chapters and
appendices share one top level. pandoc writes the LaTeX; pdflatex runs twice
with a fixed SOURCE_DATE_EPOCH so the dates and the trailer ID are stable.

``python scripts/build_paper_artifacts.py`` writes both files;
``--out DIR`` writes them elsewhere (used by the reproducibility check).
AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
STEM = "discrete_deformation_calculus"
SOURCE_DATE_EPOCH = "1791028800"  # 2026-10-03T12:00:00Z
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
    text = re.sub(r'\A<div align="center">.*?</div>\s*', "", text, count=1, flags=re.S)
    return re.sub(r"^#(#+) ", r"\1 ", text, flags=re.M)


def assemble() -> str:
    metadata = json.loads((PACKAGE / "zenodo_metadata.json").read_text(encoding="utf-8"))
    parts = [
        r"\begin{center}",
        r"\phantomsection\label{discrete-deformation-calculus}",
        r"{\LARGE\bfseries Discrete Deformation Calculus}\par\medskip",
        r"{\large A Finite Trace Calculus for Obstruction Handling}\par\medskip",
        r"Jeremy H. Carroll\par",
        f"Version {metadata['version']} --- {metadata['publication_date']}" + r"\par",
        r"Text: CC BY 4.0 --- Code: PolyForm Noncommercial 1.0.0",
        r"\end{center}",
        "",
        spine_body(),
    ]
    for chapter in sorted((PACKAGE / "chapters").glob("*.md")):
        chapter_text = chapter.read_text(encoding="utf-8")
        chapter_text = re.sub(r"^\*\*Part of:\*\*[^\n]*\n+", "", chapter_text, flags=re.M)
        parts += ["", chapter_text]
    if (PACKAGE / "docs/appendices.md").is_file():
        parts += ["", "\\newpage", "", (PACKAGE / "docs/appendices.md").read_text(encoding="utf-8")]
    parts += ["", "\\newpage", "", (PACKAGE / "docs/references.md").read_text(encoding="utf-8")]
    assembled = "\n".join(parts)
    # Convert relative file links to internal PDF anchors so they work inside the unified PDF
    assembled = re.sub(r"\]\(chapters/01_e_exact_repair\.md\)", "](#chapter-1)", assembled)
    assembled = re.sub(r"\]\(chapters/02_r_residual_projection\.md\)", "](#chapter-2)", assembled)
    assembled = re.sub(r"\]\(chapters/03_c_context_exposure\.md\)", "](#chapter-3)", assembled)
    assembled = re.sub(r"\]\(chapters/04_i_integration\.md\)", "](#chapter-4)", assembled)
    assembled = re.sub(r"\]\(chapters/05_lambda_structural_lift\.md\)", "](#chapter-5)", assembled)
    assembled = re.sub(r"\]\(chapters/06_d_descent\.md\)", "](#chapter-6)", assembled)
    assembled = re.sub(r"\]\(chapters/07_m_typed_refusal\.md\)", "](#chapter-7)", assembled)
    assembled = re.sub(r"\]\(chapters/08_t_terminalization\.md\)", "](#chapter-8)", assembled)
    assembled = re.sub(r"\]\(docs/references\.md\)", "](#references-and-their-role)", assembled)
    assembled = re.sub(r"\]\(\.\./discrete_deformation_calculus\.md\)", "](#discrete-deformation-calculus)", assembled)
    return assembled


def break_identifiers(text: str) -> str:
    """Permit code identifiers to wrap at camel-case and punctuation boundaries."""
    def rewrite(match: re.Match[str]) -> str:
        body = re.sub(r"(?<=[a-z])(?=[A-Z])", r"\\allowbreak ", match.group(1))
        body = body.replace(".", r".\allowbreak ").replace("/", r"/\allowbreak ")
        return r"\texttt{" + body + "}"
    return re.sub(r"\\texttt\{([^{}]*)\}", rewrite, text)


def build(out_dir: Path) -> list[str]:
    env = dict(os.environ, SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH, FORCE_SOURCE_DATE="1")
    with tempfile.TemporaryDirectory(prefix="ddc-pdf-") as tmp:
        work = Path(tmp)
        (work / "combined.md").write_text(assemble(), encoding="utf-8")
        subprocess.run(
            [
                "pandoc", "combined.md", "--from", "markdown", "--to", "latex", "--standalone",
                "--include-in-header", str(PACKAGE / "scripts" / "preamble.tex"),
                "--variable", "geometry:margin=1in", "--variable", "fontsize=11pt",
                "--variable", "colorlinks=true", "--output", f"{STEM}.tex",
            ],
            cwd=work, env=env, check=True, timeout=60,
        )
        tex = work / f"{STEM}.tex"
        tex.write_text(break_identifiers(tex.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        for _ in range(2):
            run = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{STEM}.tex"],
                cwd=work, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
            )
            if run.returncode:
                sys.stderr.write(run.stdout[-3000:])
                return ["pdflatex failed"]
        log = (work / f"{STEM}.log").read_text(encoding="utf-8", errors="replace")
        problems = [marker for marker in FAIL_MARKERS if marker in log]
        overfull = log.count("Overfull \\hbox")
        for warning in re.findall(r"Overfull \\hbox[^\n]*(?:\n[^\n]*){0,4}", log):
            print(warning)
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(work / f"{STEM}.tex", out_dir / f"{STEM}.tex")
        shutil.copyfile(work / f"{STEM}.pdf", out_dir / f"{STEM}.pdf")
    print(f"built {STEM}.tex and {STEM}.pdf ({overfull} overfull hbox warnings)")
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=PACKAGE)
    args = parser.parse_args(argv)
    print(json.dumps(tool_versions(), sort_keys=True))
    problems = build(args.out)
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
