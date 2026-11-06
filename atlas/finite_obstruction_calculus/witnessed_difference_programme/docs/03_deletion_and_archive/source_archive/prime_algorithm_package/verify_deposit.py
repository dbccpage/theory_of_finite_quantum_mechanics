"""Deposit gate for the Algorithm Prime Triad v1.0.0.

Default checks, all hermetic to this directory:

1. required files exist;
2. MANIFEST.sha256 and SHA256SUMS match, and no deposit file is unlisted;
3. no UTF-8 BOM, no markdownlint suppression, no dead relative link;
4. the claim ledger and the manuscript carry exactly the same claim IDs, with
   statuses from the vocabulary;
5. the claim maps are current, and every cited test and Lean name exists;
6. the archive contains exactly the manifest and its pinned files;
7. the test suite passes with at least 95 % implementation line coverage.

``--extracted`` checks the archive's unpacked directory using its internal
manifest. The external SHA256SUMS and the archive itself are not required in
that mode; all payload files remain required and hash-checked.

``--lean`` adds the Lean build and the axiom census (needs elan and Lean
v4.34.0). ``--full`` adds ``--lean``, the notebooks under nbclient, the PDF and
TeX rebuild, the archive rebuild and the mutation audit.

Exit 0 when every requested check passes. AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_claim_maps  # noqa: E402
from deposit_files import (  # noqa: E402
    ARCHIVE,
    ARCHIVE_ROOT,
    MANIFEST,
    SUMS,
    build_archive,
    deposit_files,
    manifest_names,
)

REQUIRED = (
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "CITATION.cff",
    "zenodo_metadata.json",
    "pyproject.toml",
    "oe_prime_algorithms.md",
    "oe_prime_algorithms.tex",
    "oe_prime_algorithms.pdf",
    "oe_prime_algorithms_claim_ledger.md",
    "oe_prime_algorithms_claim_ledger.yaml",
    "oe_prime_algorithms_change_log.md",
    "code/oe_prime_algorithms.py",
    "code/test_oe_prime_algorithms.py",
    "lean4/lakefile.lean",
    "lean4/lean-toolchain",
    "lean4/axiom_report.txt",
    "lean4/AxiomCensus.lean",
    "docs/claim_code_map.yaml",
    "docs/claim_ir.yaml",
    "docs/lean_claim_map.md",
    "docs/residual_aware_can_continue.md",
    "docs/descriptions.md",
    "docs/keywords.md",
    "docs/nonclaims.md",
    "docs/mutation_audit.md",
    "docs/quick_start.md",
    "docs/references.md",
    "jupyter_notebooks/01_enter_the_triad.ipynb",
    "jupyter_notebooks/02_falsify_the_laws.ipynb",
    MANIFEST,
    SUMS,
    ARCHIVE,
)
BODY = ("oe_prime_algorithms.md",)
LEDGER = "oe_prime_algorithms_claim_ledger.md"
CLAIM_ID = re.compile(r"\b(OE00[1-4]-\d{2})\b")
LEDGER_ROW = re.compile(r"^\| (OE00[1-4]-\d{2}) \| ([^|]+) \|", re.MULTILINE)
STATUSES = {
    "Definition",
    "Finite theorem",
    "Conditional theorem",
    "Computed fixture",
    "Model consequence",
    "Positioning",
    "Scope",
    "Open problem",
}
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
TEXT_SUFFIXES = {".md", ".py", ".lean", ".yaml", ".json", ".toml", ".txt", ".cff", ".tex", ".ipynb"}


def check_required(*, extracted: bool = False) -> list[str]:
    required = [name for name in REQUIRED if not extracted or name not in (SUMS, ARCHIVE)]
    return [f"missing required file: {name}" for name in required if not (ROOT / name).is_file()]


def _parse_sums(name: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
        digest, _, path = line.partition("  ")
        entries[path] = digest
    return entries


def check_hashes(*, extracted: bool = False) -> list[str]:
    import hashlib

    problems = []
    manifest = _parse_sums(MANIFEST)
    if sorted(manifest) != manifest_names():
        problems.append(f"{MANIFEST} does not list exactly the deposit files")
    listings = [(MANIFEST, manifest)]
    if not extracted:
        sums = _parse_sums(SUMS)
        expected_sums = [n for n in deposit_files() if n != SUMS]
        if sorted(sums, key=lambda s: s.encode("utf-8")) != expected_sums:
            problems.append(f"{SUMS} does not list exactly the deposit files")
        listings.append((SUMS, sums))
    for listing, entries in listings:
        for path, digest in entries.items():
            target = ROOT / path
            if not target.is_file():
                problems.append(f"{listing}: {path} is missing")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                problems.append(f"{listing}: {path} hash mismatch")
    return problems


def check_archive() -> list[str]:
    """Bind the ZIP payload to the current package, independently of its outer hash."""
    problems = []
    expected = {f"{ARCHIVE_ROOT}/{name}": name for name in manifest_names() + [MANIFEST]}
    try:
        with zipfile.ZipFile(ROOT / ARCHIVE) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                problems.append(f"{ARCHIVE}: duplicate members")
            if set(names) != set(expected):
                problems.append(f"{ARCHIVE}: member set does not match the deposit manifest")
            for member in sorted(set(names) & set(expected)):
                if archive.read(member) != (ROOT / expected[member]).read_bytes():
                    problems.append(f"{ARCHIVE}: {expected[member]} differs from the current package")
    except (OSError, zipfile.BadZipFile, RuntimeError, EOFError) as error:
        problems.append(f"{ARCHIVE}: cannot verify archive: {error}")
    return problems


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
                if target.startswith(("http://", "https://", "mailto:", "file:///")):
                    continue
                if not (path.parent / target).resolve().exists():
                    problems.append(f"dead link in {name}: {target}")
    return problems


def check_ledger() -> list[str]:
    problems = []
    body_files = [ROOT / n for n in BODY]
    body_ids = set()
    for path in body_files:
        body_ids |= set(CLAIM_ID.findall(path.read_text(encoding="utf-8")))
    rows = LEDGER_ROW.findall((ROOT / LEDGER).read_text(encoding="utf-8"))
    ids = [row[0] for row in rows]
    if len(ids) != len(set(ids)):
        problems.append("duplicate ledger rows")
    for claim_id, status in rows:
        if status.strip() not in STATUSES:
            problems.append(f"{claim_id}: status {status.strip()!r} is not in the vocabulary")
    for missing in sorted(body_ids - set(ids)):
        problems.append(f"claim {missing} appears in the manuscript but not in the ledger")
    for extra in sorted(set(ids) - body_ids):
        problems.append(f"ledger row {extra} is not cited in the manuscript")
    if not problems:
        print(f"ledger: {len(ids)} claims, one-to-one with the manuscript")
    return problems


def check_claim_maps() -> list[str]:
    problems = []
    if build_claim_maps.main(["--check"]):
        problems.append("claim maps are stale; run scripts/build_claim_maps.py")
    lean_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "lean4" / "Prime").glob("*.lean"))
    for row in build_claim_maps.claims():
        for ref in row["tests"]:
            file_part, _, test = ref.partition("::")
            source = ROOT / file_part
            if not source.is_file() or f"def {test}(" not in source.read_text(encoding="utf-8"):
                problems.append(f"{row['id']}: cited test {ref} does not exist")
        for name in row["lean"]:
            short = name.split(".", 1)[1]
            if not re.search(rf"^(theorem|def|structure|inductive) {re.escape(short)}\b", lean_text, re.M):
                problems.append(f"{row['id']}: cited Lean name {name} does not exist")
    return problems


def run_tests() -> list[str]:
    command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--cov=oe_prime_algorithms", "--cov-fail-under=95"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    tail = (result.stdout.strip().splitlines() or ["(no output)"])[-1]
    print(f"tests: {tail}")
    return [] if result.returncode == 0 else ["test suite or coverage gate failed:\n" + result.stdout[-2000:] + result.stderr[-1000:]]


def run_script(*args: str) -> list[str]:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env)
    output = (result.stdout + result.stderr).strip()
    print(output.splitlines()[-1] if output else f"{args[0]}: no output")
    return [] if result.returncode == 0 else [f"{' '.join(args)} failed:\n{output[-2000:]}"]


def run_notebooks() -> list[str]:
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        return ["nbclient and nbformat are required for --full (pip install -e .[notebooks])"]
    problems = []
    for path in sorted((ROOT / "jupyter_notebooks").glob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        try:
            NotebookClient(notebook, timeout=300, kernel_name="python3",
                           resources={"metadata": {"path": str(path.parent)}}).execute()
            print(f"notebook: {path.name} executed")
        except Exception as error:  # noqa: BLE001 - report any kernel failure
            problems.append(f"notebook {path.name} failed: {error}")
    return problems


def check_artifacts(*, extracted: bool = False) -> list[str]:
    problems = []
    with tempfile.TemporaryDirectory(prefix="prime-verify-") as tmp:
        out = Path(tmp)
        problems += run_script("scripts/build_paper_artifacts.py", "--out", str(out / "paper"))
        for name in ("oe_prime_algorithms.tex", "oe_prime_algorithms.pdf"):
            rebuilt = out / "paper" / name
            if rebuilt.is_file() and rebuilt.read_bytes() != (ROOT / name).read_bytes():
                problems.append(f"{name} is not reproducible from the sources")
        if not extracted:
            build_archive(out / ARCHIVE)
            if (out / ARCHIVE).read_bytes() != (ROOT / ARCHIVE).read_bytes():
                problems.append(f"{ARCHIVE} is not reproducible from the manifest")
            else:
                print(f"archive: {ARCHIVE} reproduced byte for byte")
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lean", action="store_true", help="also build Lean and check the axiom census")
    parser.add_argument("--full", action="store_true", help="also notebooks, artifacts and mutation audit")
    parser.add_argument("--extracted", action="store_true", help="verify an unpacked ZIP using its internal manifest")
    args = parser.parse_args(argv)
    problems = check_required(extracted=args.extracted)
    if not problems:
        problems += check_hashes(extracted=args.extracted)
        if not args.extracted:
            problems += check_archive()
        problems += check_text_hygiene()
        problems += check_ledger()
        problems += check_claim_maps()
        problems += run_tests()
        if args.lean or args.full:
            problems += run_script("scripts/lean_census.py", "--check")
        if args.full:
            problems += run_notebooks()
            problems += check_artifacts(extracted=args.extracted)
            problems += run_script("scripts/mutation_audit.py")
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print("verify_deposit: " + ("PASS" if not problems else f"FAIL ({len(problems)} problems)"))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
