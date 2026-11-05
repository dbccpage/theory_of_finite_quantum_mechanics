"""Build the monograph's .tex and .pdf from the canonical Markdown.

Follows ``006_primitive_axiomatics/scripts/build_paper_artifacts.py``. The title
block is typeset explicitly (no pandoc ``\\maketitle``) from the Markdown front
matter, and the PDF is compiled three times with xelatex under a fixed source date
so the table of contents and its page numbers stabilize.
Typesetting is not evidence for any claim.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

PAPER_MD = PACKAGE_ROOT / "witnessed_difference_programme.md"
PREAMBLE = PACKAGE_ROOT / "scripts" / "obstruction-preamble.tex"
TEX_OUT = PACKAGE_ROOT / "witnessed_difference_programme.tex"
PDF_OUT = PACKAGE_ROOT / "witnessed_difference_programme.pdf"

PANDOC_FROM = (
    "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex"
    "+backtick_code_blocks+fenced_code_attributes"
)


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        raise SystemExit(f"BLOCKED: {tool} not found on PATH")
    return path


def split_front_matter(text: str) -> tuple[str, str]:
    """Split the manuscript's own title block off the body."""
    try:
        from omega_engine_atlas.coda_atlas._kits.paper_header_schema import extract_header_block
        return extract_header_block(text)
    except ImportError:
        div_match = re.match(r"(<div\s+align=[\"']center[\"']>.*?</div>)", text, re.DOTALL | re.IGNORECASE)
        if div_match:
            header_block = div_match.group(1)
            remaining = text[div_match.end():].lstrip()
            if remaining.startswith("---"):
                remaining = re.sub(r"^---\s*", "", remaining)
            return header_block, remaining
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.strip() == "---" or line.strip().startswith("## ") or line.strip().startswith("> "):
                return "\n".join(lines[:index]), "\n".join(lines[index:])
        return "", text


def field(head: str, pattern: str) -> str:
    match = re.search(pattern, head, re.M)
    if match is None:
        raise SystemExit(f"front matter lacks {pattern!r}")
    return match.group(1).strip()


def front_matter() -> dict[str, str]:
    raw = PAPER_MD.read_text(encoding="utf-8")
    try:
        from omega_engine_atlas.coda_atlas._kits.paper_header_schema import parse_paper_header
        hdr, _body = parse_paper_header(raw, strict=False)
        return {
            "title": hdr.title,
            "subtitle": hdr.subtitle or "",
            "author": hdr.author,
            "date": hdr.date,
            "version": hdr.version,
            "license": hdr.license,
        }
    except Exception:
        head, _body = split_front_matter(raw)
        title = field(head, r"^#\s+(.+)$")
        sub_match = re.search(r"^#{2,3}\s+(.+)$", head, re.M)
        subtitle = sub_match.group(1).strip() if sub_match else ""
        if subtitle == title:
            subtitle = ""
        return {
            "title": title,
            "subtitle": subtitle,
            "author": field(head, r"\*\*Author:\*\*\s*(.+)$"),
            "date": field(head, r"\*\*Date:\*\*\s*(\S+)"),
            "version": field(head, r"\*\*Version:\*\*\s*(\S+)"),
            "license": field(head, r"\*\*License:\*\*\s*(.+)$"),
        }


LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(value: str) -> str:
    return "".join(LATEX_SPECIALS.get(char, char) for char in value)


def title_block(raw: dict[str, str]) -> str:
    try:
        from omega_engine_atlas.coda_atlas._kits.paper_header_schema import PaperHeader, render_latex_header
        hdr = PaperHeader(
            title=raw["title"],
            subtitle=raw.get("subtitle") or None,
            author=raw.get("author", "Jeremy H. Carroll"),
            date=raw["date"],
            version=raw["version"],
            license=raw["license"],
        )
        return render_latex_header(hdr) + "\n\\vspace{1.0em}\n"
    except Exception:
        meta = {key: latex_escape(value) for key, value in raw.items()}
        subtitle_part = (
            f"\n\\vspace{{0.5em}}\n{{\\large {meta['subtitle']} \\par}}"
            if meta.get("subtitle") and meta["subtitle"] != meta["title"]
            else ""
        )
        return (
            "\\begin{center}\n"
            f"{{\\LARGE\\bfseries {meta['title']} \\par}}"
            f"{subtitle_part}\n"
            "\\vspace{1.0em}\n"
            f"{{\\textbf{{{meta.get('author', 'Jeremy H. Carroll')}}}}} \\par\n"
            "\\vspace{0.4em}\n"
            f"{{\\small {meta['date']} \\quad $\\cdot$ \\quad Version {meta['version']}}} \\par\n"
            "\\vspace{0.2em}\n"
            f"{{\\footnotesize {meta['license']}}} \\par\n"
            "\\end{center}\n"
            "\\vspace{1.0em}\n"
        )


def build_tex(destination: Path) -> Path:
    pandoc = need("pandoc")
    meta = front_matter()
    _head, body = split_front_matter(PAPER_MD.read_text(encoding="utf-8"))
    yaml = (
        "---\n"
        f"date: '{meta['date']}'\n"
        "documentclass: article\n"
        "fontsize: 11pt\n"
        "colorlinks: true\n"
        "toc: true\n"
        "toc-depth: 2\n"
        "---\n\n"
    )
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        source = tmp / "paper.md"
        source.write_bytes((yaml + body).encode("utf-8"))
        before = tmp / "title.tex"
        before.write_text(title_block(meta), encoding="utf-8", newline="\n")
        cmd = [
            pandoc, str(source),
            "--from", PANDOC_FROM,
            "--to", "latex",
            "--standalone",
            "--pdf-engine", "xelatex",
            "--include-in-header", str(PREAMBLE),
            "--include-before-body", str(before),
            "--highlight-style", "kate",
            "--wrap", "preserve",
            "-V", f"title-meta={latex_escape(meta['title'])}",
            "-V", f"author-meta={latex_escape(meta['author'])}",
            "-V", "linkcolor=RoyalBlue",
            "-o", str(destination),
        ]
        try:
            run = subprocess.run(cmd, capture_output=True, timeout=1800, check=False)
        except subprocess.TimeoutExpired as error:
            raise SystemExit("pandoc timed out after 1800 s") from error
        err = run.stderr.decode("utf-8", errors="replace")
        if run.returncode != 0:
            raise SystemExit("pandoc failed:\n" + run.stdout.decode("utf-8", errors="replace") + err)
        for line in err.strip().splitlines()[:10]:
            if line.strip():
                print(f"    pandoc: {line}")
    normalized = destination.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    binding = f"% manuscript-sha256: {hashlib.sha256(PAPER_MD.read_bytes()).hexdigest()}\n"
    destination.write_bytes(binding.encode("utf-8") + normalized)
    return destination


def source_epoch() -> int:
    day = datetime.strptime(front_matter()["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(day.timestamp())


def build_pdf(tex: Path, destination: Path) -> Path:
    xelatex = need("xelatex")
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = str(source_epoch())
    env["FORCE_SOURCE_DATE"] = "1"
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        work = tmp / tex.name
        shutil.copyfile(tex, work)
        for index in (1, 2, 3):
            try:
                run = subprocess.run(
                    [xelatex, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", work.name],
                    cwd=tmp,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1800,
                    env=env,
                    check=False,
                )
            except subprocess.TimeoutExpired as error:
                raise SystemExit(f"xelatex pass {index} timed out after 1800 s") from error
            if run.returncode != 0:
                log = tmp / (work.stem + ".log")
                tail = ""
                if log.exists():
                    tail = "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-40:])
                raise SystemExit(f"xelatex pass {index} failed:\n{tail}")
        log_text = (tmp / (work.stem + ".log")).read_text(encoding="utf-8", errors="replace")
        overfull = [line for line in log_text.splitlines() if line.startswith("Overfull \\hbox")]
        print(f"    xelatex: {len(overfull)} overfull hbox warning(s)")
        for line in overfull:
            print(f"    {line}")
        missing = [line for line in log_text.splitlines() if "Missing character:" in line]
        if missing or overfull:
            shutil.copyfile(tmp / (work.stem + ".log"), destination.with_suffix(".log"))
            raise SystemExit(
                f"PDF layout refused: {len(missing)} missing glyph(s), "
                f"{len(overfull)} overfull hbox warning(s)"
            )
        shutil.copyfile(tmp / (tex.stem + ".pdf"), destination)
        for suffix in (".log", ".toc", ".aux"):
            source_file = tmp / (tex.stem + suffix)
            if source_file.exists():
                shutil.copyfile(source_file, destination.with_suffix(suffix))
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex-only", action="store_true")
    args = parser.parse_args()
    print(f"Building .tex: {TEX_OUT.name}")
    build_tex(TEX_OUT)
    if args.tex_only:
        return
    print(f"Building .pdf: {PDF_OUT.name}")
    build_pdf(TEX_OUT, PDF_OUT)
    print("Build complete.")


if __name__ == "__main__":
    main()
