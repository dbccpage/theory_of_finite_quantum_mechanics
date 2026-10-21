#!/usr/bin/env python3
"""Build paper.tex and paper.pdf from paper.md with Pandoc and XeLaTeX.

The title, author line and date/version line are read from the centered header
block at the top of ``paper.md``; nothing about the paper is hard-coded here.
The version and date must match ``zenodo_metadata.json``. The generated
``paper.tex`` is standalone: it compiles from the package root with

    xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape paper.tex

The tool runs three XeLaTeX passes in a temporary directory, refuses any
"Overfull \\hbox" warning, and copies only the PDF back. It makes no network
calls.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE_FORMAT = "markdown+tex_math_single_backslash+tex_math_dollars"
TITLE_BLOCK = r"""\makeatletter
\begin{center}
{\LARGE \@title\par}
\vspace{0.8em}
{\normalsize \@author\par}
\vspace{0.5em}
{\small \@date\par}
\end{center}
\makeatother"""


def run(command: list[str], *, text: str | None = None, cwd: Path = PACKAGE) -> str:
    result = subprocess.run(
        command,
        input=text,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {command}\n"
            f"{result.stdout[-4000:]}\n{result.stderr[-2000:]}"
        )
    return result.stdout


def header_fields(text: str) -> tuple[str, str, str]:
    """Return the title, the author line and the date/version line."""
    author_m = re.search(r"^\*\*Author:\*\*\s*(.+)$", text, re.M)
    date_m = re.search(r"^\*\*Date:\*\*\s*(.+)$", text, re.M)
    version_m = re.search(r"^\*\*Version:\*\*\s*(.+)$", text, re.M)
    license_m = re.search(r"^\*\*License:\*\*\s*(.+)$", text, re.M)
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    if author_m and date_m and version_m and title_m:
        title = title_m.group(1).strip()
        author = author_m.group(1).strip()
        date_str = date_m.group(1).strip()
        version_str = version_m.group(1).strip()
        lic_str = license_m.group(1).strip() if license_m else "CC-BY-4.0"
        return title, author, f"{date_str} · Version {version_str} · {lic_str}"

    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("# "))
    rest: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith(("## ", "</div>")):
            break
        if stripped:
            rest.append(stripped.rstrip("\\").strip())
    if len(rest) < 2:
        raise ValueError("header block needs an author line and a date/version line")
    return lines[start][2:].strip(), rest[0], rest[1]


def check_metadata(title: str, meta_line: str) -> None:
    metadata = json.loads((PACKAGE / "zenodo_metadata.json").read_text(encoding="utf-8"))
    match = re.match(r"^(\d{4}-\d{2}-\d{2}) · Version (\d+\.\d+\.\d+)", meta_line)
    if match is None:
        raise ValueError(f"unexpected date/version line: {meta_line!r}")
    date, version = match.groups()
    expected = (metadata.get("title"), metadata.get("version"), metadata.get("publication_date"))
    if (title, version, date) != expected:
        raise ValueError(f"manuscript header {(title, version, date)} != metadata {expected}")


def wrap_inline_paths(node: object) -> None:
    """Let long paths, identifiers and digests break across lines."""
    if isinstance(node, list):
        for value in node:
            wrap_inline_paths(value)
    elif isinstance(node, dict):
        if node.get("t") in ("Code", "Str"):
            token = node["c"][1] if node["t"] == "Code" else node["c"]
            identifier = any(char in token for char in "/_.") or re.fullmatch(
                r"[a-fA-F0-9]{32,}", token
            )
            if len(token) > 24 and identifier and re.fullmatch(r"[A-Za-z0-9_./:+-]+", token):
                node.update(t="RawInline", c=["latex", r"\nolinkurl{" + token + "}"])
                return
        for value in node.values():
            wrap_inline_paths(value)


def render_tex(pandoc: str, text: str, title: str, author: str, date: str) -> str:
    ast = json.loads(run([pandoc, "-f", SOURCE_FORMAT, "-t", "json"], text=text))
    body_start = next(
        i
        for i, block in enumerate(ast["blocks"])
        if block.get("t") == "Header" and block["c"][0] == 2
    )
    ast["blocks"] = ast["blocks"][body_start:]
    wrap_inline_paths(ast)
    tex = run(
        [
            pandoc,
            "-f",
            "json",
            "-t",
            "latex",
            "--standalone",
            "--listings",
            "--include-in-header",
            str(PACKAGE / "tools" / "tex_header.tex"),
            "-V",
            "geometry:margin=25mm",
            "-V",
            "fontsize:11pt",
            "-V",
            "colorlinks:true",
            "-M",
            "title=" + title,
            "-M",
            "author=" + author,
            "-M",
            "date=" + date,
        ],
        text=json.dumps(ast),
    )
    if tex.count(r"\maketitle") != 1:
        raise RuntimeError("expected exactly one generated \\maketitle")
    return tex.replace(r"\maketitle", TITLE_BLOCK)


def compile_pdf(xelatex: str, tex: Path, pdf: Path) -> None:
    """Three XeLaTeX passes in a scratch directory; refuse overfull lines."""
    with tempfile.TemporaryDirectory(prefix="meron-tex-") as scratch:
        for _ in range(3):
            log = run(
                [
                    xelatex,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-no-shell-escape",
                    f"-output-directory={scratch}",
                    tex.name,
                ],
                cwd=tex.parent,
            )
            overfull = [line for line in log.splitlines() if "Overfull \\hbox" in line]
            if overfull:
                raise RuntimeError(f"{len(overfull)} overfull line warning(s): {overfull[:5]}")
        shutil.copyfile(Path(scratch) / (tex.stem + ".pdf"), pdf)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pandoc", default=shutil.which("pandoc"))
    parser.add_argument("--xelatex", default=shutil.which("xelatex"))
    parser.add_argument("--tex-only", action="store_true", help="write paper.tex only")
    args = parser.parse_args()
    if not args.pandoc or (not args.tex_only and not args.xelatex):
        parser.error("Pandoc and XeLaTeX must be installed or given explicitly")
    source = PACKAGE / "paper.md"
    text = source.read_text(encoding="utf-8")
    title, author, date = header_fields(text)
    check_metadata(title, date)
    tex = PACKAGE / "paper.tex"
    tex.write_text(render_tex(args.pandoc, text, title, author, date), encoding="utf-8", newline="\n")
    print(f"wrote {tex.name}")
    if not args.tex_only:
        compile_pdf(args.xelatex, tex, PACKAGE / "paper.pdf")
        print("wrote paper.pdf (three XeLaTeX passes, no overfull lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
