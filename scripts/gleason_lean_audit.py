#!/usr/bin/env python3
"""Fail-closed audit of the Gleason Lean modules (FQ-GLEASON-QI3-* / FQ-BORN-QI3-*).

AuthorityEffect: None. This tool checks a build; it establishes no mathematical claim.

The five Gleason modules are non-default Lake targets, so a green default build says nothing
about them. This tool makes their kernel check explicit and reproducible:

    python -I -X utf8 scripts/gleason_lean_audit.py inventory            # declarations, full Unicode names
    python -I -X utf8 scripts/gleason_lean_audit.py emit lean4/.audit/GleasonAudit.lean
    cd lean4 && lake build <the five targets> && lake env lean .audit/GleasonAudit.lean > ../audit.txt
    python -I -X utf8 scripts/gleason_lean_audit.py verify --lean-output audit.txt
    python -I -X utf8 scripts/gleason_lean_audit.py update --lean-output audit.txt   # maintainer: re-pin

``inventory`` reads the module sources, strips comments, follows ``namespace``/``section``
nesting and returns every named ``theorem``/``lemma``/``def``/``abbrev``/``structure``/
``inductive``/``class``/``instance`` with its complete identifier. Identifiers keep every
Unicode character (``ι``, ``f₀``, ``C₁``); a truncated or duplicated name is an error.

``verify`` fails (exit 1) when any of these holds:

* a pinned source (the five modules, their four project dependencies, the toolchain, the Lake
  manifest or the lakefile) has a different sha256 than the expectation file records;
* the inventory of the current sources differs from the recorded one;
* a comment-stripped module source contains ``sorry``, ``admit``, ``native_decide``, ``unsafe``,
  ``partial``, ``implemented_by``, ``opaque`` or ``axiom``;
* the Lean output lacks a ``#print axioms`` report for any recorded declaration, or contains an
  ``error`` line;
* any report lists an axiom outside the allowlist (``propext``, ``Classical.choice``,
  ``Quot.sound``); ``sorryAx`` is therefore rejected.

The expectation file is ``dag/research/gleason_lean_audit.json``. ``update`` rewrites it from the
current sources and a passing Lean output; it is a maintainer action recorded in version control,
not something CI does.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTATION = "dag/research/gleason_lean_audit.json"
SCHEMA = "gleason_lean_audit.v1"
MODULES = (
    "BornGaussianParallelogramRigidity",
    "GleasonRealSphere",
    "GleasonComplexSphere",
    "GleasonGaussianBridge",
    "GleasonBornCompletion",
)
DEPENDENCIES = (
    "BornGaussRat",
    "BornGaussianRationalFrameObstruction",
    "BornGaussianFrameRays",
    "BornGaussianTomographyReduction",
)
PINS = ("lean4/lean-toolchain", "lean4/lake-manifest.json", "lean4/lakefile.lean")
ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
FORBIDDEN_TOKENS = ("sorry", "admit", "native_decide", "unsafe", "partial", "implemented_by", "opaque", "axiom")

DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)*(?P<mods>(?:(?:private|protected|noncomputable|nonrec)\s+)*)"
    r"(?P<kw>theorem|lemma|def|abbrev|structure|inductive|class|instance|opaque|axiom)\s+"
    r"(?P<name>[^\s:(\[{⟨|]+)"
)
SCOPE = re.compile(r"^(?P<kw>namespace|section|end)(?:\s+(?P<name>\S+))?\s*$")
# A declaration name may itself end in a prime (`completeness'`), so the name is read lazily up to
# the quote that precedes the report text.
REPORT = re.compile(r"'(.+?)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")


def module_path(name: str) -> str:
    return f"lean4/{name}.lean"


def sha256(root: Path, rel: str) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


def strip_comments(source: str) -> str:
    """Remove ``--`` line comments and ``/- ... -/`` block comments (nesting respected)."""
    out: list[str] = []
    i, depth, n = 0, 0, len(source)
    while i < n:
        if source.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth and source.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth:
            if source[i] == "\n":
                out.append("\n")  # keep line structure
            i += 1
            continue
        if source.startswith("--", i):
            j = source.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(source[i])
        i += 1
    return "".join(out)


def inventory_of(source: str) -> list[str]:
    """Fully qualified names of the named declarations in one module source, in order."""
    names: list[str] = []
    stack: list[tuple[str, str | None]] = []
    for raw in strip_comments(source).splitlines():
        line = raw.rstrip()
        scope = SCOPE.match(line)
        if scope:
            kw, name = scope.group("kw"), scope.group("name")
            if kw == "end":
                if stack:
                    stack.pop()
            else:
                stack.append((kw, name))
            continue
        decl = DECL.match(line)
        if not decl:
            continue
        if "private" in decl.group("mods"):
            continue  # mangled name, not an exported binding
        name = decl.group("name")
        if decl.group("kw") == "instance" and name.startswith(":"):
            continue  # anonymous instance
        prefix = ".".join(n for kw, n in stack if kw == "namespace" and n)
        names.append(f"{prefix}.{name}" if prefix else name)
    return names


def inventory(root: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for module in MODULES:
        names = inventory_of((root / module_path(module)).read_text(encoding="utf-8"))
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            raise SystemExit(f"duplicate declaration names in {module}: {dupes}")
        result[module] = names
    return result


def forbidden_tokens(root: Path) -> list[str]:
    hits: list[str] = []
    for module in MODULES:
        text = strip_comments((root / module_path(module)).read_text(encoding="utf-8"))
        for token in FORBIDDEN_TOKENS:
            if re.search(rf"(?<![\w.']){re.escape(token)}(?![\w'])", text):
                hits.append(f"{module}: {token}")
    return hits


def pins(root: Path) -> dict[str, str]:
    paths = [module_path(m) for m in MODULES + DEPENDENCIES] + list(PINS)
    return {p: sha256(root, p) for p in paths}


def parse_reports(text: str) -> dict[str, list[str]]:
    reports: dict[str, list[str]] = {}
    for name, axioms in REPORT.findall(text):
        reports[name] = [a.strip() for a in axioms.split(",") if a.strip()] if axioms else []
    return reports


def emit(root: Path, target: Path) -> int:
    inv = inventory(root)
    lines = [f"import {m}" for m in MODULES] + [""]
    for module, names in inv.items():
        lines.append(f"-- {module}")
        lines += [f"#print axioms {n}" for n in names]
        lines.append("")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    return sum(len(v) for v in inv.values())


def verify(root: Path, lean_output: str, expectation: dict) -> list[str]:
    errors: list[str] = []
    if expectation.get("schema_version") != SCHEMA:
        errors.append(f"expectation schema is {expectation.get('schema_version')!r}, want {SCHEMA!r}")
    current = pins(root)
    for path, digest in expectation.get("pins", {}).items():
        if current.get(path) != digest:
            errors.append(f"stale source pin: {path}")
    for path in current:
        if path not in expectation.get("pins", {}):
            errors.append(f"unpinned source: {path}")
    inv = inventory(root)
    if inv != expectation.get("declarations"):
        errors.append("declaration inventory differs from the expectation file (run `update` after review)")
    errors += [f"forbidden token: {h}" for h in forbidden_tokens(root)]
    if re.search(r"^.*\berror\b", lean_output, flags=re.M):
        errors.append("Lean output contains an error line")
    reports = parse_reports(lean_output)
    allowed = set(expectation.get("allowed_axioms", ALLOWED_AXIOMS))
    for names in expectation.get("declarations", {}).values():
        for name in names:
            if name not in reports:
                errors.append(f"missing report: {name}")
                continue
            extra = sorted(set(reports[name]) - allowed)
            if extra:
                errors.append(f"unexpected axioms for {name}: {extra}")
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(ROOT))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inventory")
    e = sub.add_parser("emit")
    e.add_argument("target")
    for cmd in ("verify", "update"):
        p = sub.add_parser(cmd)
        p.add_argument("--lean-output", required=True)
        p.add_argument("--expectation", default=EXPECTATION)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()

    if args.cmd == "inventory":
        print(json.dumps(inventory(root), indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "emit":
        count = emit(root, Path(args.target))
        print(json.dumps({"written": args.target, "declarations": count}))
        return 0

    lean_output = Path(args.lean_output).read_text(encoding="utf-8", errors="replace")
    exp_path = root / args.expectation
    if args.cmd == "update":
        expectation = {
            "schema_version": SCHEMA,
            "authority_effect": "None",
            "note": "Expectation for scripts/gleason_lean_audit.py: pinned sources, the full-identifier "
                    "declaration inventory of the five Gleason modules and the axiom allowlist. "
                    "Rewritten only by `update` after a passing local audit; CI only verifies.",
            "modules": list(MODULES),
            "dependencies": list(DEPENDENCIES),
            "allowed_axioms": list(ALLOWED_AXIOMS),
            "pins": pins(root),
            "declarations": inventory(root),
            "lean_toolchain": (root / "lean4/lean-toolchain").read_text(encoding="utf-8").strip(),
        }
        errors = verify(root, lean_output, expectation)
        if errors:
            print(json.dumps({"all_passed": False, "errors": errors}, indent=2, ensure_ascii=False))
            return 1
        exp_path.write_text(json.dumps(expectation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"written": args.expectation, "declarations": sum(len(v) for v in expectation["declarations"].values())}))
        return 0

    if not exp_path.is_file():
        print(json.dumps({"all_passed": False, "errors": [f"missing expectation file {args.expectation}"]}))
        return 1
    expectation = json.loads(exp_path.read_text(encoding="utf-8"))
    errors = verify(root, lean_output, expectation)
    summary = {
        "all_passed": not errors,
        "declarations_checked": sum(len(v) for v in expectation.get("declarations", {}).values()),
        "errors": errors,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
