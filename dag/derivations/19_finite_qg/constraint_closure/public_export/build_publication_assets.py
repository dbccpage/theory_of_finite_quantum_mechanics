"""Build publication text, TeX, PDF, manifest, and Zenodo zip for GR-002.

The PDF path is intentionally a real TeX build. The script converts the
canonical Markdown manuscript into a conservative LaTeX document, preserves
inline and display math as TeX math, and compiles it with Tectonic/XeTeX.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3] if len(ROOT.parents) > 3 else ROOT
MANUSCRIPT = ROOT / "constraint_closure_and_the_l1structure_of_physical_law.md"
TEXT_OUT = ROOT / "constraint_closure_and_the_l1structure_of_physical_law.txt"
TEX_OUT = ROOT / "constraint_closure_and_the_l1structure_of_physical_law.tex"
PDF_OUT = ROOT / "constraint_closure_and_the_l1structure_of_physical_law.pdf"
MANIFEST_OUT = ROOT / "publication_assets_manifest.json"
ZIP_OUT = ROOT / "constraint_closure_toy_model_zenodo_v1_2.zip"
OLD_ZIP_OUT = ROOT / "constraint_closure_toy_model_zenodo_v1_1.zip"

PACKAGE_VERSION = "1.2"
PACKAGE_PREFIX = "constraint_closure_toy_model_zenodo_v1_2"
ZIP_TIMESTAMP = (2026, 9, 11, 0, 0, 0)
PDF_METADATA_DATE = "D:20260911000000-04'00'"
PDF_TITLE = "A Constraint-Closure Toy Model for ℓ¹ Residuals on Finite Complexes"
PDF_AUTHOR = "Jeremy H. Carroll"
PDF_SUBJECT = "As-is toy-model republication with finite ℓ¹ quotient certificates"
PDF_KEYWORDS = "toy model, finite complexes, ℓ¹ quotient, Regge calculus, Lean 4"
PDF_CREATOR = "CODA GR-002 public_export/build_publication_assets.py"

EXCLUDE_DIRS = {
    ".git",
    ".lake",
    ".pytest_cache",
    ".tectonic-cache",
    ".tectonic-config",
    ".venv",
    "__pycache__",
    "gr002_constraint_closure_l1.egg-info",
    "target",
}
EXCLUDE_SUFFIXES = {".aux", ".log", ".out", ".toc", ".pyc", ".pyo"}
EXCLUDE_FILES = {ZIP_OUT.name, OLD_ZIP_OUT.name}

SYMBOL_REPLACEMENTS = {
    r"\ell": "ℓ",
    r"\mathbb{R}": "ℝ",
    r"\mathbb{Q}": "ℚ",
    r"\mathbb{Z}": "ℤ",
    r"\mathbb{N}": "ℕ",
    r"\operatorname{im}": "im",
    r"\operatorname{ker}": "ker",
    r"\alpha": "α",
    r"\beta": "β",
    r"\gamma": "γ",
    r"\delta": "δ",
    r"\varepsilon": "ε",
    r"\epsilon": "ε",
    r"\theta": "θ",
    r"\Theta": "Θ",
    r"\omega": "ω",
    r"\Phi": "Φ",
    r"\Psi": "Ψ",
    r"\Delta": "Δ",
    r"\Sigma": "Σ",
    r"\Lambda": "Λ",
    r"\partial": "∂",
    r"\infty": "∞",
    r"\langle": "⟨",
    r"\rangle": "⟩",
    r"\Vert": "‖",
    r"\lVert": "‖",
    r"\rVert": "‖",
    r"\|": "‖",
    r"\leq": "≤",
    r"\geq": "≥",
    r"\le": "≤",
    r"\ge": "≥",
    r"\ne": "≠",
    r"\neq": "≠",
    r"\times": "×",
    r"\to": "→",
    r"\mapsto": "↦",
    r"\oplus": "⊕",
    r"\cong": "≅",
    r"\approx": "≈",
    r"\pm": "±",
    r"\sum": "∑",
    r"\prod": "∏",
    r"\forall": "∀",
    r"\in": "∈",
    r"\notin": "∉",
    r"\Longleftrightarrow": "⟺",
    r"\longleftrightarrow": "⟷",
    r"\Rightarrow": "⇒",
    r"\Leftarrow": "⇐",
}

SUPERSCRIPT = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "+": "⁺",
    "-": "⁻",
    "=": "⁼",
    "(": "⁽",
    ")": "⁾",
    "n": "ⁿ",
    "i": "ⁱ",
    "j": "ʲ",
    "k": "ᵏ",
    "D": "ᴰ",
    "T": "ᵀ",
}
SUBSCRIPT = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
    "+": "₊",
    "-": "₋",
    "=": "₌",
    "(": "₍",
    ")": "₎",
    "a": "ₐ",
    "b": "ᵦ",
    "e": "ₑ",
    "h": "ₕ",
    "i": "ᵢ",
    "j": "ⱼ",
    "k": "ₖ",
    "m": "ₘ",
    "n": "ₙ",
    "o": "ₒ",
    "p": "ₚ",
    "r": "ᵣ",
    "s": "ₛ",
    "t": "ₜ",
    "u": "ᵤ",
    "v": "ᵥ",
    "x": "ₓ",
}


@dataclass
class PdfAudit:
    pages: int
    tex_engine: str
    tex_log: str
    overfull_hbox_count: int
    underfull_hbox_count: int


@dataclass(frozen=True)
class ManuscriptMetadata:
    author: str = PDF_AUTHOR
    date: str = "2026-09-10"
    version: str = f"{PACKAGE_VERSION} Pre-Print"
    publication_posture: str = (
        "As-is continuation of an earlier toy model, written as an exploratory "
        "exercise and not as a claim to derive physical law."
    )


def find_omega_engine_source() -> Path:
    for candidate in (ROOT / "omega_engine", *(parent / "omega_engine" for parent in ROOT.parents)):
        if candidate.exists():
            return candidate
    return REPO_ROOT / "omega_engine"


PACKAGE_OMEGA_ENGINE = ROOT / "omega_engine"
OMEGA_ENGINE_SOURCE = find_omega_engine_source()
BUNDLED_EXTERNAL_DIRS = (
    {} if OMEGA_ENGINE_SOURCE == PACKAGE_OMEGA_ENGINE else {Path("omega_engine"): OMEGA_ENGINE_SOURCE}
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def escape_tex_text(text: str) -> str:
    text = html.unescape(text)
    replacements = {
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
    return "".join(replacements.get(char, char) for char in text)


def escape_tex_url(url: str) -> str:
    return url.replace("\\", "/").replace("%", r"\%")


def convert_text_span(span: str) -> str:
    span = span.replace("&mdash;", "—").replace("–", "--").replace("—", "---")
    patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        ("code", re.compile(r"`([^`]+)`")),
        ("link", re.compile(r"\[([^\]]+)\]\(([^)]+)\)")),
        ("bold_star", re.compile(r"\*\*(.+?)\*\*")),
        ("bold_underscore", re.compile(r"__(.+?)__")),
        ("italic_star", re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)")),
    )
    output: list[str] = []
    position = 0
    while position < len(span):
        matches: list[tuple[int, int, str, re.Match[str]]] = []
        for kind, pattern in patterns:
            match = pattern.search(span, position)
            if match:
                matches.append((match.start(), match.end(), kind, match))
        if not matches:
            output.append(escape_tex_text(span[position:]))
            break
        start, end, kind, match = min(matches, key=lambda item: (item[0], item[1]))
        if start > position:
            output.append(escape_tex_text(span[position:start]))
        if kind == "code":
            output.append(r"\texttt{" + escape_tex_text(match.group(1)) + "}")
        elif kind == "link":
            label = tex_inline(match.group(1))
            url = escape_tex_url(match.group(2))
            output.append(rf"\href{{{url}}}{{{label}}}")
        elif kind.startswith("bold"):
            output.append(r"\textbf{" + tex_inline(match.group(1)) + "}")
        else:
            output.append(r"\emph{" + tex_inline(match.group(1)) + "}")
        position = end
    return "".join(output)


def tex_inline(text: str) -> str:
    math_segments: dict[str, str] = {}

    def math_repl(match: re.Match[str]) -> str:
        token = f"@@MATH{len(math_segments)}@@"
        math_segments[token] = match.group(0)
        return token

    protected = re.sub(r"\$[^$]+\$", math_repl, text)
    rendered = convert_text_span(protected)
    for token, math in math_segments.items():
        rendered = rendered.replace(token, math)
    return rendered.strip()


def unicode_scripts(text: str, marker: str, mapping: dict[str, str]) -> str:
    def braced(match: re.Match[str]) -> str:
        value = match.group(1).replace(" ", "")
        return "".join(mapping.get(char, char) for char in value)

    def bare(match: re.Match[str]) -> str:
        value = match.group(1)
        return mapping.get(value, value)

    text = re.sub(rf"\{marker}\{{([^}}]+)\}}", braced, text)
    text = re.sub(rf"\{marker}([A-Za-z0-9+\-=()])", bare, text)
    return text


def latexish_to_unicode(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = text.replace("&mdash;", "—")
    text = re.sub(r"\\(mathrm|operatorname|texttt|text|mathbf|mathit)\{([^{}]+)\}", r"\2", text)
    for source, target in SYMBOL_REPLACEMENTS.items():
        text = text.replace(source, target)
    text = unicode_scripts(text, "^", SUPERSCRIPT)
    text = unicode_scripts(text, "_", SUBSCRIPT)
    text = text.replace(r"\\", " ")
    text = text.replace("$", "").replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def markdown_to_plain(markdown: str) -> str:
    output: list[str] = []
    in_code = False
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            output.append("")
            continue
        if in_code:
            output.append(line)
            continue
        if line.startswith("#"):
            output.append(latexish_to_unicode(line.lstrip("# ")).upper())
            output.append("")
            continue
        if re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*", line):
            continue
        output.append(latexish_to_unicode(line))

    wrapped: list[str] = []
    for line in output:
        if not line:
            wrapped.append("")
        elif line.startswith("|"):
            wrapped.extend(textwrap.wrap(line, width=110, break_long_words=True))
        else:
            wrapped.extend(textwrap.wrap(line, width=100, break_long_words=False) or [""])
    return "\n".join(wrapped).rstrip() + "\n"


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*", line.strip()))


def table_column_spec(count: int) -> str:
    def ragged(width: str) -> str:
        return rf">{{\raggedright\arraybackslash}}p{{{width}\textwidth}}"

    if count <= 2:
        return ragged("0.30") + ragged("0.62")
    if count == 3:
        return ragged("0.23") + ragged("0.27") + ragged("0.42")
    width = round(0.92 / max(count, 1), 3)
    return "".join([ragged(f"{width}") for _ in range(count)])


def render_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    column_count = max(len(row) for row in rows)
    rendered = [r"\begin{small}", rf"\begin{{longtable}}{{{table_column_spec(column_count)}}}", r"\toprule"]
    for index, row in enumerate(rows):
        padded = row + [""] * (column_count - len(row))
        rendered.append(" & ".join(tex_inline(cell) for cell in padded) + r" \\")
        rendered.append(r"\midrule" if index == 0 else r"\addlinespace[0.25em]")
    rendered.extend([r"\bottomrule", r"\end{longtable}", r"\end{small}"])
    return rendered


def parse_metadata_line(stripped: str) -> tuple[str, str] | None:
    match = re.match(r"^\*\*(Author|Date|Version|Publication posture):\*\*\s*(.+)$", stripped)
    if not match:
        return None
    key = match.group(1).lower().replace(" ", "_")
    return key, match.group(2).strip()


def markdown_body_to_tex(markdown: str) -> tuple[str, str, ManuscriptMetadata, str]:
    lines = markdown.splitlines()
    title = "A Constraint-Closure Toy Model for $\\ell^1$ Residuals on Finite Complexes"
    subtitle = ""
    metadata_values: dict[str, str] = {}
    output: list[str] = []
    paragraph: list[str] = []
    table_rows: list[list[str]] = []
    active_list: str | None = None
    in_code = False
    code_lines: list[str] = []
    in_math = False
    math_lines: list[str] = []

    def close_list() -> None:
        nonlocal active_list
        if active_list:
            output.append(rf"\end{{{active_list}}}")
            active_list = None

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            close_list()
            output.append(tex_inline(" ".join(paragraph)))
            output.append("")
            paragraph = []

    def flush_table() -> None:
        nonlocal table_rows
        if table_rows:
            close_list()
            output.extend(render_table(table_rows))
            output.append("")
            table_rows = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            output.append(
                r"\begin{Verbatim}[breaklines=true,breakanywhere=true,fontsize=\small]"
            )
            output.extend(code_lines)
            output.append(r"\end{Verbatim}")
            output.append("")
            code_lines = []

    def flush_math() -> None:
        nonlocal math_lines
        if math_lines:
            output.append(r"\begin{equation*}")
            output.extend(math_lines)
            output.append(r"\end{equation*}")
            output.append("")
            math_lines = []

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_paragraph()
                flush_table()
                close_list()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped == "$$":
            if in_math:
                flush_math()
                in_math = False
            else:
                flush_paragraph()
                flush_table()
                close_list()
                in_math = True
            continue
        if in_math:
            math_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            flush_table()
            close_list()
            continue
        metadata_line = parse_metadata_line(stripped)
        if metadata_line:
            flush_paragraph()
            flush_table()
            close_list()
            key, value = metadata_line
            metadata_values[key] = value
            continue
        if is_table_separator(stripped):
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            close_list()
            table_rows.append(split_table_row(stripped))
            continue
        flush_table()
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1:
                title = text
                continue
            if level == 2 and not subtitle and not output:
                subtitle = text
                continue
            command = {2: "section", 3: "subsection", 4: "subsubsection"}.get(level, "paragraph")
            bookmark = escape_tex_text(latexish_to_unicode(text))
            output.append(rf"\{command}{{\texorpdfstring{{{tex_inline(text)}}}{{{bookmark}}}}}")
            output.append("")
            continue
        if stripped == "---":
            flush_paragraph()
            close_list()
            output.append(r"\medskip\hrule\medskip")
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if bullet or numbered:
            flush_paragraph()
            env = "itemize" if bullet else "enumerate"
            if active_list and active_list != env:
                close_list()
            if not active_list:
                output.append(rf"\begin{{{env}}}[leftmargin=1.4em,itemsep=0.2em]")
                active_list = env
            item = bullet.group(1) if bullet else numbered.group(1)
            output.append(r"\item " + tex_inline(item))
            continue
        paragraph.append(stripped)

    flush_paragraph()
    flush_table()
    flush_code()
    flush_math()
    close_list()
    metadata = ManuscriptMetadata(
        author=metadata_values.get("author", PDF_AUTHOR),
        date=metadata_values.get("date", "2026-09-10"),
        version=metadata_values.get("version", f"{PACKAGE_VERSION} Pre-Print"),
        publication_posture=metadata_values.get(
            "publication_posture",
            ManuscriptMetadata().publication_posture,
        ),
    )
    return title, subtitle, metadata, "\n".join(output).strip() + "\n"


def latex_public_title_block(title: str, subtitle: str, metadata: ManuscriptMetadata) -> str:
    subtitle_tex = (
        rf"\vspace{{0.45em}}{{\large {tex_inline(subtitle)}\par}}" if subtitle else ""
    )
    metadata_lines = [
        rf"\textbf{{Author:}} {tex_inline(metadata.author)}",
        rf"\textbf{{Date:}} {tex_inline(metadata.date)}",
        rf"\textbf{{Version:}} {tex_inline(metadata.version)}",
        rf"\textbf{{Publication posture:}} {tex_inline(metadata.publication_posture)}",
    ]
    metadata_tex = "\\\\[0.28em]\n".join(metadata_lines)
    return rf"""\begin{{center}}
{{\LARGE\bfseries {tex_inline(title)}\par}}
{subtitle_tex}
\vspace{{0.95em}}
\begin{{minipage}}{{0.88\textwidth}}
\centering
{{\small
{metadata_tex}
}}
\end{{minipage}}
\end{{center}}
\vspace{{0.75em}}
"""


def tex_document(markdown: str) -> str:
    title, subtitle, metadata, body = markdown_body_to_tex(markdown)
    title_block = latex_public_title_block(title, subtitle, metadata)
    return rf"""\documentclass[11pt]{{article}}
\usepackage[letterpaper,margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\usepackage{{textcomp}}
\usepackage{{amsmath,amssymb,mathtools}}
\usepackage{{microtype}}
\usepackage{{booktabs,longtable,array}}
\usepackage{{enumitem}}
\usepackage{{fvextra}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}
\hypersetup{{
  colorlinks=true,
  linkcolor=blue!45!black,
  urlcolor=blue!45!black,
  pdftitle={{{escape_tex_text(latexish_to_unicode(title))}}},
  pdfauthor={{{PDF_AUTHOR}}},
  pdfsubject={{{PDF_SUBJECT}}},
  pdfkeywords={{{PDF_KEYWORDS}}}
}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{0.62em}}
\setlength{{\LTpre}}{{0.35em}}
\setlength{{\LTpost}}{{0.35em}}
\renewcommand{{\arraystretch}}{{1.18}}
\sloppy
\emergencystretch=5em
\allowdisplaybreaks
\begin{{document}}
\thispagestyle{{empty}}

{title_block}

{body}

\end{{document}}
"""


def discover_tex_engine() -> Path:
    env_path = os.environ.get("TECTONIC") or os.environ.get("CODA_TECTONIC")
    candidates: list[Path] = []
    if env_path:
        candidates.append(Path(env_path))
    for name in ("tectonic", "tectonic.exe"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    candidates.extend(
        [
            Path("C:/Users/a343o/AppData/Local/Temp/codex-tools/tectonic-0.17.0/tectonic.exe"),
            Path("C:/Users/a343o/AppData/Local/Programs/Tectonic/tectonic.exe"),
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "No TeX engine found. Install Tectonic or set CODA_TECTONIC/TECTONIC to tectonic.exe."
    )


def build_pdf_with_tex(tex_path: Path, pdf_path: Path) -> PdfAudit:
    engine = discover_tex_engine()
    temp_root = Path(tempfile.gettempdir())
    cache_dir = temp_root / "coda-tectonic-cache-gr002"
    config_dir = temp_root / "coda-tectonic-config-gr002"
    build_dir = temp_root / "coda-gr002-tex-build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)
    cache_dir.mkdir(exist_ok=True)
    config_dir.mkdir(exist_ok=True)
    build_tex = build_dir / "paper.tex"
    build_pdf = build_dir / "paper.pdf"
    build_log = build_dir / "paper.log"
    build_tex.write_text(tex_path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    env = os.environ.copy()
    env.setdefault("TECTONIC_CACHE_DIR", str(cache_dir))
    env.setdefault("XDG_CACHE_HOME", str(cache_dir))
    env.setdefault("XDG_CONFIG_HOME", str(config_dir))
    command = [
        str(engine),
        "--keep-logs",
        "--keep-intermediates",
        "--outdir",
        str(build_dir),
        str(build_tex),
    ]
    result = subprocess.run(command, cwd=build_dir, text=True, capture_output=True, check=False, env=env)
    log_text = (result.stdout or "") + "\n" + (result.stderr or "")
    if build_log.exists():
        log_text += "\n" + build_log.read_text(encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"TeX build failed with exit code {result.returncode}\n{log_text[-4000:]}")
    if not build_pdf.exists():
        raise FileNotFoundError(f"TeX build did not produce {build_pdf}")
    shutil.copy2(build_pdf, pdf_path)
    if build_log.exists():
        shutil.copy2(build_log, tex_path.with_suffix(".log"))
    reader = PdfReader(str(pdf_path))
    return PdfAudit(
        pages=len(reader.pages),
        tex_engine=str(engine),
        tex_log=tex_path.with_suffix(".log").name if build_log.exists() else "",
        overfull_hbox_count=log_text.count("Overfull \\hbox"),
        underfull_hbox_count=log_text.count("Underfull \\hbox"),
    )


def normalize_pdf_metadata(path: Path) -> None:
    reader = PdfReader(str(path))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(
        {
            "/Title": PDF_TITLE,
            "/Author": PDF_AUTHOR,
            "/Subject": PDF_SUBJECT,
            "/Keywords": PDF_KEYWORDS,
            "/Creator": PDF_CREATOR,
            "/Producer": "Tectonic XeTeX and pypdf",
            "/CreationDate": PDF_METADATA_DATE,
            "/ModDate": PDF_METADATA_DATE,
        }
    )
    temporary = path.with_suffix(".normalized.pdf")
    try:
        with temporary.open("wb") as handle:
            writer.write(handle)
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def should_exclude(path: Path, base: Path) -> bool:
    relative_parts = path.relative_to(base).parts
    if any(part in EXCLUDE_DIRS for part in relative_parts):
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return path.name in EXCLUDE_FILES


def iter_package_files() -> Iterable[tuple[Path, Path]]:
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir():
            continue
        if should_exclude(path, ROOT):
            continue
        yield path, path.relative_to(ROOT)
    for archive_root, source_root in BUNDLED_EXTERNAL_DIRS.items():
        if not source_root.exists():
            raise FileNotFoundError(f"Bundled dependency root not found: {source_root}")
        for path in sorted(source_root.rglob("*")):
            if path.is_dir():
                continue
            if should_exclude(path, source_root):
                continue
            yield path, archive_root / path.relative_to(source_root)


def write_zip(output_path: Path) -> tuple[int, int]:
    files = list(iter_package_files())
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, relative_path in files:
            archive_name = Path(PACKAGE_PREFIX) / relative_path
            info = zipfile.ZipInfo(archive_name.as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    total_bytes = sum(path.stat().st_size for path, _ in files)
    return len(files), total_bytes


def main() -> int:
    if not MANUSCRIPT.exists():
        raise FileNotFoundError(MANUSCRIPT)
    if OLD_ZIP_OUT.exists():
        OLD_ZIP_OUT.unlink()
    markdown = MANUSCRIPT.read_text(encoding="utf-8")
    TEXT_OUT.write_text(markdown_to_plain(markdown), encoding="utf-8", newline="\n")
    TEX_OUT.write_text(tex_document(markdown), encoding="utf-8", newline="\n")
    audit = build_pdf_with_tex(TEX_OUT, PDF_OUT)
    normalize_pdf_metadata(PDF_OUT)

    manifest = {
        "authority_effect": "None",
        "package_version": PACKAGE_VERSION,
        "source": MANUSCRIPT.name,
        "text": TEXT_OUT.name,
        "tex": TEX_OUT.name,
        "pdf": PDF_OUT.name,
        "zip": ZIP_OUT.name,
        "pdf_pages": audit.pages,
        "tex_engine": audit.tex_engine,
        "tex_log": audit.tex_log,
        "tex_overfull_hbox_count": audit.overfull_hbox_count,
        "tex_underfull_hbox_count": audit.underfull_hbox_count,
        "bundled_external_roots": [path.as_posix() for path in BUNDLED_EXTERNAL_DIRS],
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    zip_count, zip_source_bytes = write_zip(ZIP_OUT)
    manifest["zip_file_count"] = zip_count
    manifest["zip_source_bytes"] = zip_source_bytes
    for path in [TEXT_OUT, TEX_OUT, PDF_OUT, ZIP_OUT]:
        manifest[f"sha256_{path.name}"] = sha256_file(path)
        manifest[f"bytes_{path.name}"] = path.stat().st_size
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
