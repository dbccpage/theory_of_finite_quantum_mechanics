"""Deposit gate for the Discrete Deformation Calculus v1.0.3.

Default checks, all hermetic to this directory:

1. required files exist;
2. MANIFEST.sha256 and SHA256SUMS match, and no deposit file is unlisted;
3. no UTF-8 BOM, no markdownlint suppression, no dead relative link;
4. named test files pass sequentially with at least 95 % runtime line and branch coverage.

``--lean`` adds the Lean build and the axiom census (needs elan and Lean
v4.34.0). ``--full`` adds ``--lean``, the notebooks under nbclient, the PDF and
TeX rebuild, archive member verification and the mutation audit.

Exit 0 when every requested check passes. AuthorityEffect: None.
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

ROOT = Path(__file__).resolve().parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(ROOT / "scripts"))

from deposit_files import (  # noqa: E402
    ARCHIVE,
    MANIFEST,
    SUMS,
    deposit_files,
    verify_archive,
    verify_hashes,
)

REQUIRED = (
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "CITATION.cff",
    "zenodo_metadata.json",
    "pyproject.toml",
    "discrete_deformation_calculus.md",
    "discrete_deformation_calculus.tex",
    "discrete_deformation_calculus.pdf",
    "discrete_deformation_calculus_change_log.md",
    "lean4/lakefile.lean",
    "lean4/lean-toolchain",
    "lean4/axiom_report.txt",
    "lean4/AxiomCensus.lean",
    "jupyter_notebooks/01_enter_the_calculus.ipynb",
    "jupyter_notebooks/02_falsify_the_laws.ipynb",
    MANIFEST,
    SUMS,
)
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
TEXT_SUFFIXES = {".md", ".py", ".lean", ".yaml", ".json", ".toml", ".txt", ".cff", ".tex", ".ipynb"}


def check_required() -> list[str]:
    return [f"missing required file: {name}" for name in REQUIRED if not (ROOT / name).is_file()]


def check_hashes() -> list[str]:
    return verify_hashes(ROOT)


def check_text_hygiene() -> list[str]:
    problems = []
    for name in deposit_files():
        path = ROOT / name
        if path.suffix not in TEXT_SUFFIXES and path.name not in ("LICENSE", "LICENSE-CODE", SUMS, MANIFEST):
            continue
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            problems.append(f"UTF-8 BOM in {name}")
        if path.suffix == ".md":
            text = data.decode("utf-8")
            if "markdownlint-disable" in text:
                problems.append(f"markdownlint suppression in {name}")
            for target in LINK.findall(text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    problems.append(f"dead link in {name}: {target}")
    return problems


def run_tests(report_path: Path | None = None) -> list[str]:
    tests = sorted((ROOT / "code/tests").glob("test_*.py"))
    if not tests:
        return ["no test files collected"]
    with tempfile.TemporaryDirectory(prefix="ddc-coverage-") as tmp:
        env = dict(os.environ, COVERAGE_FILE=str(Path(tmp) / ".coverage"), PYTHONUTF8="1")
        for test in tests:
            command = [sys.executable, "-m", "coverage", "run", "--branch", "--append",
                       "--source=code/ddc", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(test)]
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=60)
            print(f"{test.name}: " + (result.stdout.strip().splitlines() or ["no output"])[-1])
            if result.returncode:
                return [f"{test.name} failed:\n{result.stdout[-3000:]}{result.stderr[-1000:]}"]
        report = Path(tmp) / "coverage.json"
        result = subprocess.run([sys.executable, "-m", "coverage", "json", "-o", str(report)], cwd=ROOT,
                                env=env, capture_output=True, text=True, timeout=60)
        if result.returncode or not report.is_file():
            return ["coverage report was not generated"]
        totals = json.loads(report.read_text(encoding="utf-8"))["totals"]
        if report_path is not None:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(report, report_path)
        lines = 100 * totals["covered_lines"] / max(1, totals["num_statements"])
        branches = 100 * totals["covered_branches"] / max(1, totals["num_branches"])
        print(f"runtime coverage: lines={lines:.2f}% branches={branches:.2f}%")
        return [] if min(lines, branches) >= 95 else ["runtime line/branch coverage below 95%"]


def run_script(*args: str) -> list[str]:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    result = subprocess.run([sys.executable, "-X", "utf8", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env, timeout=300)
    output = (result.stdout + result.stderr).strip()
    print(output.splitlines()[-1] if output else f"{args[0]}: no output")
    return [] if result.returncode == 0 else [f"{' '.join(args)} failed:\n{output[-2000:]}"]


def run_notebooks() -> list[str]:
    return run_script("scripts/replay_notebooks.py", "--check")


def normalize_tex(text: str) -> str:
    """Normalize LaTeX for cross-toolchain semantic comparison.

    Extracts document body, strips comments, reconciles Pandoc 3.1 vs 3.7+
    writer conventions (heading hypertarget wrappers, internal link commands,
    table columnwidth versus linewidth metrics, and optional environment brackets),
    and collapses whitespace.
    """
    body_match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, re.DOTALL)
    content = body_match.group(1) if body_match else text

    # Strip LaTeX comments
    lines = []
    for line in content.splitlines():
        line = re.sub(r"(?<!\\)%.*$", "", line).strip()
        if line:
            lines.append(line)
    content = "\n".join(lines)

    # Unwrap Pandoc <= 3.1 hypertarget wrappers around headings:
    # \hypertarget{slug}{ \section{Title}\label{slug} } -> \section{Title}\label{slug}
    content = re.sub(
        r"\\hypertarget\{([^}]+)\}\s*\{(\s*\\(?:part|chapter|(?:sub)*section|paragraph|subparagraph)\*?\{.*?\}(?:\s*\\label\{[^}]*\})?\s*)\}",
        r"\2",
        content,
        flags=re.DOTALL,
    )

    # Reconcile internal link commands to canonical \hyperlink{target}{text}
    # Pandoc <= 3.1: \protect\hyperlink{target}{text} or \hyperlink{target}{text}
    # Pandoc >= 3.2: \hyperref[target]{text}
    content = re.sub(r"\\protect\s*\\hyperlink\{", r"\\hyperlink{", content)
    content = re.sub(r"\\hyperref\[([^\]]+)\]\{", r"\\hyperlink{\1}{", content)

    # Reconcile table column metric keywords: \columnwidth -> \linewidth
    content = re.sub(r"\\columnwidth\b", r"\\linewidth", content)

    # Reconcile optional empty brackets on longtable/tabular environments
    content = re.sub(r"\\begin\{longtable\}\[\]", r"\\begin{longtable}", content)

    return " ".join(content.split())


def check_artifacts() -> list[str]:
    problems = []
    with tempfile.TemporaryDirectory(prefix="ddc-verify-") as tmp:
        out = Path(tmp)
        problems += run_script("scripts/build_paper_artifacts.py", "--out", str(out / "paper"))
        for name in ("discrete_deformation_calculus.tex", "discrete_deformation_calculus.pdf"):
            rebuilt = out / "paper" / name
            if not rebuilt.is_file() or rebuilt.stat().st_size == 0:
                problems.append(f"missing rebuilt artifact: {name}")
            elif name.endswith(".tex"):
                rebuilt_tex = rebuilt.read_text(encoding="utf-8")
                deposited_tex = (ROOT / name).read_text(encoding="utf-8")
                if rebuilt_tex != deposited_tex and normalize_tex(rebuilt_tex) != normalize_tex(deposited_tex):
                    problems.append("rebuilt TeX differs semantically from the deposited source; use recorded Pandoc 3.7.0.2 or compatible (>= 3.1)")
        if not problems:
            try:
                import pymupdf  # type: ignore[import-untyped]
                with pymupdf.open(out / "paper/discrete_deformation_calculus.pdf") as rebuilt_pdf, pymupdf.open(ROOT / "discrete_deformation_calculus.pdf") as published:
                    # PDF metadata, compression and font versions need not be byte-identical.
                    def text(doc):
                        return " ".join(" ".join(page.get_text().split()) for page in doc)
                    if text(rebuilt_pdf) != text(published):
                        problems.append("rebuilt PDF text differs from the deposited publication")
            except ImportError:
                problems.append("PyMuPDF is required for --full PDF comparison")
        if (ROOT / ARCHIVE).is_file():
            problems += verify_archive(ROOT / ARCHIVE, ROOT)
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lean", action="store_true", help="also build Lean and check the axiom census")
    parser.add_argument("--full", action="store_true", help="also notebooks, artifacts and mutation audit")
    parser.add_argument("--static", action="store_true", help="inventory, identity, and links only; no tests/builds")
    parser.add_argument("--coverage-json", type=Path, help="save runtime coverage outside the release payload")
    args = parser.parse_args(argv)
    problems = check_required()
    if not problems:
        problems += check_hashes()
        if not problems:
            problems += check_text_hygiene()
            problems += check_identity()
            if (ROOT / ARCHIVE).is_file():
                problems += verify_archive(ROOT / ARCHIVE, ROOT)
        if not problems and not args.static:
            problems += run_tests(args.coverage_json)
        if args.lean or args.full:
            problems += run_script("scripts/lean_census.py", "--check")
        if args.full:
            problems += run_notebooks()
            problems += check_artifacts()
            problems += run_script("scripts/mutation_audit.py")
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print("verify_deposit: " + ("PASS" if not problems else f"FAIL ({len(problems)} problems)"))
    return 1 if problems else 0


def check_identity() -> list[str]:
    metadata = json.loads((ROOT / "zenodo_metadata.json").read_text(encoding="utf-8"))
    version, date = metadata["version"], metadata["publication_date"]
    expected = {
        "discrete_deformation_calculus.md": (f'**Version:** {version}', f'**Date:** {date}'),
        "README.md": (f"v{version}", date),
        "CITATION.cff": (f'version: "{version}"', f'date-released: "{date}"',
                         'license: "PolyForm-Noncommercial-1.0.0"'),
        "pyproject.toml": (f'version = "{version}"', 'PolyForm-Noncommercial-1.0.0'),
        "discrete_deformation_calculus_change_log.md": (f"## [{version}] — {date}",),
        "lean4/lakefile.lean": (f'v!"{version}"',),
    }
    return [f"identity mismatch in {name}: {token}" for name, tokens in expected.items()
            for token in tokens if token not in (ROOT / name).read_text(encoding="utf-8")]


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"verify_deposit: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1) from error
