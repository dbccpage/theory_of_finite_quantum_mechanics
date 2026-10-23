"""Build the paper's .tex and .pdf from the canonical Markdown.

AuthorityEffect: None. Rendering the manuscript is not evidence for any claim
in it, and a clean LaTeX run certifies nothing about the mathematics.

The Markdown is the source of truth. This script never edits it: the .tex is a
derived artifact and is regenerated, not hand-maintained, so the two cannot
drift.

    python scripts/build_paper_artifacts.py            build .tex and .pdf
    python scripts/build_paper_artifacts.py --tex-only
    python scripts/build_paper_artifacts.py --check    rebuild and compare

Requires pandoc and xelatex on PATH. xelatex rather than pdflatex: the
manuscript carries twelve non-ASCII characters that pdflatex cannot set
without per-character declarations.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PAPER_MD = PACKAGE_ROOT / "projection_obstruction.md"
PREAMBLE = PACKAGE_ROOT / "scripts" / "obstruction-preamble.tex"
TEX_OUT = PACKAGE_ROOT / "projection_obstruction.tex"
PDF_OUT = PACKAGE_ROOT / "projection_obstruction.pdf"

TITLE = "Projection Obstruction for Factorized States"
SUBTITLE = ("Nonlinear Dynamics, Conditional $\\ell^1$ Diagnostics, "
            "and Exact Short-Time Defect Bounds")
AUTHOR = "Jeremy H. Carroll"

# The declared publication date, as a UTC epoch. Pinning it removes the wall
# clock from the PDF, which is what makes two builds *on this toolchain* agree
# byte for byte.
#
# It does not make the PDF portable, and the difference matters. The same
# shipped .tex produces 271,208 bytes at PDF version 1.7 under MiKTeX and
# 271,122 bytes at PDF 1.5 under TeX Live: engine build, font files and
# default PDF version all enter the bytes. Only the release ZIP is
# cross-platform byte-reproducible. TeX and PDF bytes are reproducible within
# the named Pandoc/XeLaTeX/font toolchain and no further, and the toolchain is
# printed on every run so the scope of the claim is legible.
IDENTITY = json.loads((PACKAGE_ROOT / "release_identity.json").read_text(encoding="utf-8"))
RELEASE_DATE = date.fromisoformat(IDENTITY["release_date"])
SOURCE_EPOCH = int(datetime.combine(RELEASE_DATE, datetime.min.time(), timezone.utc).timestamp())


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        raise SystemExit(f"BLOCKED: {tool} not found on PATH")
    return path


def tool_version(tool: str) -> str:
    """First line of `<tool> --version`, for the receipt.

    Recorded because the .tex is reproducible against a fixed Pandoc and not
    across Pandoc releases. A claim whose scope is a tool version should name
    the version.
    """
    try:
        out = subprocess.run([need(tool), "--version"],
                             capture_output=True, timeout=120, check=False)
    except (OSError, subprocess.SubprocessError, SystemExit):
        return f"{tool} (version unavailable)"
    first = out.stdout.decode("utf-8", errors="replace").strip().splitlines()
    return first[0].strip() if first else f"{tool} (no version output)"


REPO_ROOT = PACKAGE_ROOT.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def front_matter(text: str) -> tuple[str, str]:
    """Split the manuscript's own title block off the body."""
    try:
        from omega_engine_atlas.coda_atlas._kits.paper_header_schema import extract_header_block
        return extract_header_block(text)
    except ImportError:
        lines = text.splitlines()
        for i, ln in enumerate(lines):
            if ln.strip() == "---" or ln.strip().startswith("## ") or ln.strip().startswith("> "):
                return "\n".join(lines[:i]), "\n".join(lines[i:])
        return "", text


def build_tex(destination: Path) -> Path:
    pandoc = need("pandoc")
    raw = PAPER_MD.read_text(encoding="utf-8")

    date = IDENTITY["release_date"]
    try:
        from omega_engine_atlas.coda_atlas._kits.paper_header_schema import parse_paper_header
        hdr, body = parse_paper_header(raw, strict=False)
        date = hdr.date
    except Exception:
        _head, body = front_matter(raw)
        match = re.search(r"^\*Date:\*\s*(\S+)", raw, re.M)
        if match:
            date = match.group(1)

    # Single-quoted YAML scalars, not double-quoted. A double-quoted YAML
    # scalar processes backslash escapes, so the subtitle's `\ell` became a
    # literal ESC byte (0x1B) and xelatex refused the file with "Text line
    # contains an invalid character". Single quotes pass backslashes through.
    meta = (
        "---\n"
        f"title: '{TITLE}'\n"
        f"subtitle: '{SUBTITLE}'\n"
        f"author: '{AUTHOR}'\n"
        f"subject: 'PO-000 release {IDENTITY['release_version']}; Python {IDENTITY['code_version']}'\n"
        f"date: 'Release {IDENTITY['release_version']} -- {date}'\n"
        "documentclass: article\n"
        "fontsize: 11pt\n"
        "colorlinks: true\n"
        "toc: true\n"
        "toc-depth: 2\n"
        "---\n\n"
    )
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        header = tmp / "preamble.tex"
        header.write_text(
            "\\newcommand{\\POReleaseVersion}{" + IDENTITY["release_version"] + "}\n"
            + PREAMBLE.read_text(encoding="utf-8"), encoding="utf-8"
        )
        source = tmp / "paper.md"
        source.write_bytes((meta + body).encode("utf-8"))
        cmd = [
            pandoc, str(source),
            "--from", "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex"
                      "+backtick_code_blocks+fenced_code_attributes",
            "--to", "latex",
            "--standalone",
            "--pdf-engine", "xelatex",
            "--include-in-header", str(header),
            "--highlight-style", "kate",
            "--wrap", "preserve",
            "-V", "linkcolor=RoyalBlue",
            "-o", str(destination),
        ]
        # Bytes, not text=True: the tool chain emits output the Windows locale
        # codec cannot decode, and a UnicodeDecodeError raised in subprocess's
        # reader thread would obscure an otherwise successful build.
        run = subprocess.run(cmd, capture_output=True, timeout=1800, check=False)
        err = run.stderr.decode("utf-8", errors="replace")
        if run.returncode != 0:
            raise SystemExit("pandoc failed:\n"
                             + run.stdout.decode("utf-8", errors="replace")
                             + err)
        for line in err.strip().splitlines()[:10]:
            if line.strip():
                print(f"    pandoc: {line}")
    # Pandoc follows the host newline convention.  The generated TeX is a
    # tracked release input, so normalize it before hashing or compiling.
    destination.write_bytes(
        destination.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    )
    return destination


def build_pdf(tex: Path, destination: Path) -> Path:
    """Three xelatex passes to stabilize the table of contents.

    The run is pinned to a fixed date. A PDF embeds its creation time, so two
    builds of identical input otherwise differ in bytes, and this deposit's
    whole discipline is that an archive can be rebuilt and compared. With
    SOURCE_DATE_EPOCH and FORCE_SOURCE_DATE set, xelatex stamps the declared
    publication date instead of the wall clock.
    """
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
                [xelatex, "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", work.name],
                cwd=tmp, capture_output=True, timeout=1800, env=env, check=False)
            if run.returncode != 0:
                log = (tmp / (work.stem + ".log"))
                tail = ""
                if log.is_file():
                    text = log.read_text(encoding="utf-8", errors="replace")
                    tail = "\n".join(
                        ln for ln in text.splitlines()
                        if ln.startswith("!") or ".tex:" in ln)[-4000:]
                raise SystemExit(f"xelatex pass {index} failed:\n{tail}")
        produced = tmp / (work.stem + ".pdf")
        if not produced.is_file():
            raise SystemExit("xelatex produced no PDF")
        log = (tmp / (work.stem + ".log")).read_text(encoding="utf-8",
                                                     errors="replace")
        audit_log(log)
        shutil.copyfile(produced, destination)
        for ext in (".log", ".toc", ".aux"):
            src_file = tmp / (work.stem + ext)
            if src_file.is_file():
                shutil.copyfile(src_file, PACKAGE_ROOT / (work.stem + ext))
    return destination


# A "Missing character" warning means a glyph was silently dropped from the
# PDF. The first release build carried eleven of them: omega, subscript one,
# less-or-equal, greater-or-equal and nu vanished out of a dependency diagram,
# and script ell out of a reference title, leaving corrupted formulas that read
# as ordinary text. xelatex reports this and exits 0, so nothing caught it.
_MISSING = re.compile(r"^Missing character: There is no (.+?) in font (.+?)!?$",
                      re.M)
_OVERFULL = re.compile(r"^Overfull \\hbox \(([0-9.]+)pt too wide\)"
                       r"(?: in paragraph at lines (\S+))?", re.M)

# Boxes below this are a hair over the margin and invisible in the rendered
# page; above it, text runs into or past the margin and a reader sees it.
OVERFULL_LIMIT_PT = 10.0


def audit_log(log: str) -> None:
    """Refuse a PDF with dropped glyphs or text outside the text block."""
    missing = _MISSING.findall(log)
    overfull = [(float(pt), lines or "?") for pt, lines in _OVERFULL.findall(log)]
    material = sorted((o for o in overfull if o[0] > OVERFULL_LIMIT_PT),
                      reverse=True)

    problems = []
    if missing:
        counts: dict[tuple[str, str], int] = {}
        for glyph, font in missing:
            counts[(glyph, font.split("/")[0])] = \
                counts.get((glyph, font.split("/")[0]), 0) + 1
        problems.append(
            "characters dropped from the PDF (the glyph is absent from the "
            "font, so it is not drawn):")
        for (glyph, font), count in sorted(counts.items()):
            problems.append(f"    {glyph!r} x{count} in {font}")
    if material:
        problems.append(
            f"text past the margin, over {OVERFULL_LIMIT_PT:g}pt "
            f"({len(material)} of {len(overfull)} overfull boxes):")
        for pt, lines in material[:12]:
            problems.append(f"    {pt:8.2f}pt at .tex lines {lines}")

    if problems:
        raise SystemExit(
            "BLOCKED: the PDF built, but it is not presentable.\n  "
            + "\n  ".join(problems)
            + "\n\n  A PDF that renders with holes in it is worse than one "
              "that fails to build, because it looks finished.")

    print(f"    log: 0 missing characters, "
          f"{len(overfull)} overfull box(es), none over "
          f"{OVERFULL_LIMIT_PT:g}pt")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tex-only", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="rebuild into a temp dir and compare the .tex")
    args = parser.parse_args(argv)

    if not PAPER_MD.is_file():
        raise SystemExit(f"BLOCKED: no manuscript at {PAPER_MD}")
    if not PREAMBLE.is_file():
        raise SystemExit(f"BLOCKED: no preamble at {PREAMBLE}")

    print("build_paper_artifacts   AuthorityEffect: None")
    print(f"  source : {PAPER_MD.name} "
          f"({len(PAPER_MD.read_text(encoding='utf-8').splitlines())} lines)")

    print(f"  toolchain: {tool_version('pandoc')} | {tool_version('xelatex')}")

    if args.check:
        with tempfile.TemporaryDirectory() as raw_tmp:
            probe = build_tex(Path(raw_tmp) / TEX_OUT.name)
            same = TEX_OUT.is_file() and filecmp.cmp(probe, TEX_OUT, shallow=False)
            # The scope of this claim is one Pandoc version, and saying so
            # matters: a reviewer running a different Pandoc got False here and
            # was right to. Pandoc's LaTeX writer changes between releases, so
            # the .tex is reproducible against a fixed writer, not universally.
            #
            # An earlier version of this comment said the PDF was "byte-
            # identical on any machine". That was false and was corrected
            # 2026-09-04: the same shipped .tex gives 271,208 bytes at PDF 1.7
            # under MiKTeX and 271,122 bytes at PDF 1.5 under TeX Live. Only
            # the ZIP is cross-platform byte-reproducible; TeX and PDF bytes
            # are reproducible within the named toolchain and no further.
            print(f"  tex reproducible against {tool_version('pandoc')}: {same}")
            if not same:
                print("  (a different Pandoc version writes different LaTeX "
                      "for the same input; regenerate rather than compare "
                      "across versions)")
            return 0 if same else 1

    build_tex(TEX_OUT)
    print(f"  tex    : {TEX_OUT.name}  "
          f"{TEX_OUT.stat().st_size:,} bytes  sha256 {sha(TEX_OUT)[:16]}")
    if args.tex_only:
        return 0

    build_pdf(TEX_OUT, PDF_OUT)
    print(f"  pdf    : {PDF_OUT.name}  "
          f"{PDF_OUT.stat().st_size:,} bytes  sha256 {sha(PDF_OUT)[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
