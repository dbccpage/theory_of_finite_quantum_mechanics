#!/usr/bin/env python3
"""Build PO-033's .tex and .pdf from canonical Markdown.

Rendering the manuscript is not evidence for any claim in it, and a clean
LaTeX run certifies nothing about the mathematics.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PAPER_MD = PACKAGE_ROOT / "033_certified_adaptive_quantum_dynamics.md"
PREAMBLE = PACKAGE_ROOT / "scripts" / "obstruction-preamble.tex"
TEX_OUT = PACKAGE_ROOT / "033_certified_adaptive_quantum_dynamics.tex"
PDF_OUT = PACKAGE_ROOT / "033_certified_adaptive_quantum_dynamics.pdf"

SOURCE_EPOCH = 1791676800  # 2026-10-11 UTC, fixed for this reviewed artifact.


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        raise SystemExit(f"BLOCKED: {tool} not found on PATH")
    return path


def build_tex(destination: Path) -> Path:
    pandoc = need("pandoc")
    cmd = [
        pandoc,
        str(PAPER_MD),
        "--from",
        "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex+backtick_code_blocks+fenced_code_attributes",
        "--to",
        "latex",
        "--standalone",
        "--pdf-engine",
        "xelatex",
        "--include-in-header",
        str(PREAMBLE),
        "--no-highlight",
        "--wrap",
        "preserve",
        "-V",
        "geometry:margin=1in",
        "-V",
        "linkcolor=RoyalBlue",
        "-o",
        str(destination),
    ]
    run = subprocess.run(cmd, cwd=PACKAGE_ROOT, capture_output=True, timeout=1800)
    err = run.stderr.decode("utf-8", errors="replace")
    if run.returncode != 0:
        raise SystemExit("pandoc failed:\n" + run.stdout.decode("utf-8", errors="replace") + err)
    for line in err.strip().splitlines()[:10]:
        if line.strip():
            print(f"    pandoc: {line}")

    tex_text = destination.read_text(encoding="utf-8")

    source = PAPER_MD.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", source, re.M).group(1)
    if title != "Certified Adaptive Quantum Dynamics from Projection Residuals":
        raise ValueError("unexpected manuscript title; update the rendering contract explicitly")
    for field in ("Subtitle", "Authors", "Date", "Version"):
        if re.search(r"^\*\*" + field + r":\*\* (.+)$", source, re.M) is None:
            raise ValueError(f"missing canonical manuscript field: {field}")
    digest = hashlib.sha256(PAPER_MD.read_bytes()).hexdigest()

    # Keep authors, date, version, and subtitle from the canonical body; the
    # title replacement must not inject stale metadata or duplicate the header.
    header_block = r"""\begin{center}
{\LARGE\bfseries Certified Adaptive Quantum Dynamics from Projection Residuals \par}
\end{center}"""

    # Replace markdown main section title with centered zero-line header block
    tex_text, title_count = re.subn(
        r"\\hypertarget\{certified-adaptive-quantum-dynamics-from-projection-residuals\}\{%?\s*"
        r"\\section\{Certified Adaptive Quantum Dynamics from Projection Residuals\}"
        r"\\label\{certified-adaptive-quantum-dynamics-from-projection-residuals\}\}",
        lambda m: header_block,
        tex_text,
        count=1,
    )
    if title_count == 0:
        # Pandoc 3.1.11 emits a section/label without the older hypertarget
        # wrapper. Match that complete known form, retaining fail-closed title
        # validation rather than replacing an arbitrary first section.
        tex_text, title_count = re.subn(
            r"\\section\{Certified Adaptive Quantum Dynamics from Projection Residuals\}"
            r"\\label\{certified-adaptive-quantum-dynamics-from-projection-residuals\}",
            lambda m: header_block, tex_text, count=1,
        )
    if title_count != 1:
        raise ValueError("canonical title wrapper not found in generated TeX")

    # Replace any \maketitle
    tex_text = tex_text.replace(r"\maketitle", "")
    tex_text = tex_text.replace(r"% add subtitle to \maketitle", r"% add subtitle to title block")

    # Remove any horizontal rules injected around title
    tex_text = re.sub(r"\\begin\{center\}\\rule\{[^\}]+\}\{[^\}]+\}\\end\{center\}", "", tex_text)

    # Sanitize any accidental authorityeffect tokens
    tex_text = re.sub(r"(?i)authorityeffect\s*:\s*none\.?", "", tex_text)
    tex_text = tex_text.replace(r"\textbf{AuthorityEffect}", r"\textbf{Authority status}")
    tex_text = tex_text.replace("AuthorityEffect", "Authority status")
    marker = "manuscript-sha256:" + digest
    tex_text = tex_text.replace(r"\begin{document}",
                               "% " + marker + "\n"
                               + r"\hypersetup{pdfkeywords={" + marker + "}}\n"
                               + r"\begin{document}")

    destination.write_text(tex_text.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8")
    return destination


def build_pdf(tex: Path, destination: Path) -> Path:
    xelatex = need("xelatex")
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = str(SOURCE_EPOCH)
    env["FORCE_SOURCE_DATE"] = "1"
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        work = tmp / tex.name
        shutil.copyfile(tex, work)
        for index in (1, 2, 3):
            run = subprocess.run(
                [
                    xelatex,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-file-line-error",
                    work.name,
                ],
                cwd=tmp,
                capture_output=True,
                timeout=1800,
                env=env,
            )
            log = tmp / (work.stem + ".log")
            tail = ""
            if log.exists():
                log_text = log.read_text(encoding="utf-8", errors="replace")
                shutil.copyfile(log, destination.with_suffix(".log"))
                if "Missing character:" in log_text:
                    raise SystemExit("xelatex reported missing glyphs; inspect the manuscript fonts")
                if "Overfull \\hbox" in log_text:
                    overfull_lines = [l for l in log_text.splitlines() if "Overfull \\hbox" in l]
                    raise SystemExit(f"xelatex reported overfull lines: {overfull_lines[:3]}")
                tail = "\n".join(log_text.splitlines()[-40:])
            if run.returncode != 0:
                raise SystemExit(f"xelatex pass {index} failed:\n{tail}")
            print(f"    xelatex pass {index} complete.")
        shutil.copyfile(tmp / (tex.stem + ".pdf"), destination)
        for suffix in (".log", ".aux", ".toc"):
            generated = tmp / (tex.stem + suffix)
            if generated.exists():
                shutil.copyfile(generated, destination.with_suffix(suffix))
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex-only", action="store_true")
    args = parser.parse_args()

    print(f"Building .tex: {TEX_OUT}")
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        tex, pdf = tmp / TEX_OUT.name, tmp / PDF_OUT.name
        build_tex(tex)
        if args.tex_only:
            shutil.copyfile(tex, TEX_OUT)
            return
        print(f"Building .pdf: {PDF_OUT}")
        try:
            build_pdf(tex, pdf)
        finally:
            # Preserve compiler diagnostics even when a build fails. Successful
            # manuscript artifacts are replaced only after build_pdf returns.
            for suffix in (".log", ".aux", ".toc"):
                generated = pdf.with_suffix(suffix)
                if generated.exists():
                    shutil.copyfile(generated, PDF_OUT.with_suffix(suffix))
        shutil.copyfile(tex, TEX_OUT)
        shutil.copyfile(pdf, PDF_OUT)
    print("Build complete.")


if __name__ == "__main__":
    main()
