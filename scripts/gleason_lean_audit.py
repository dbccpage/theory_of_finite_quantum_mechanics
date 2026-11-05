#!/usr/bin/env python3
"""Fail-closed audit of the Gleason Lean modules (FQ-GLEASON-QI3-* / FQ-BORN-QI3-*).

AuthorityEffect: None. This tool checks a build; it establishes no mathematical claim.

The five Gleason modules are non-default Lake targets, so a green default build says nothing
about them. This tool makes their kernel check explicit and reproducible:

    python -I -X utf8 scripts/gleason_lean_audit.py inventory            # declarations, full Unicode names
    python -I -X utf8 scripts/gleason_lean_audit.py emit lean4/.audit/GleasonAudit.lean
    cd lean4 && lake build <the five targets> && lake env lean .audit/GleasonAudit.lean > ../audit.txt 2>&1
    python -I -X utf8 scripts/gleason_lean_audit.py verify --lean-output audit.txt
    python -I -X utf8 scripts/gleason_lean_audit.py update --lean-output audit.txt   # maintainer: re-pin

``inventory`` reads the module sources, strips comments, follows ``namespace``/``section``/
``noncomputable section``/``mutual`` nesting (including indented declarations and scope commands)
and returns every named ``theorem``/``lemma``/``def``/``abbrev``/``structure``/``inductive``/
``class``/``instance`` with its complete identifier. Identifiers keep every Unicode character
(``ι``, ``f₀``, ``C₁``) and prime suffix (``completeness'``). Unsupported declaration/scope
syntax, mismatched or unclosed scopes, duplicate declaration names and empty module inventories
fail visibly.

``verify`` fails (exit 1) when any of these holds:

* a pinned source (the five modules, their four project dependencies, the toolchain, the Lake
  manifest or the lakefile) has a different sha256 than the expectation file records;
* any module or dependency imports an unpinned local module;
* the expectation file or current source inventory is missing a module, is empty, has duplicate
  declaration names, fails scope/syntax validation or differs from the recorded expectation;
* a comment-stripped module or dependency source contains ``sorry``, ``admit``, ``native_decide``,
  ``unsafe``, ``partial``, ``implemented_by``, ``opaque`` or ``axiom``;
* the Lean output lacks a ``#print axioms`` report for any recorded declaration, contains
  duplicate or contradictory reports, contains an unexpected report or contains an ``error`` line;
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
EXTERNAL_PACKAGES = (
    "Mathlib",
    "Init",
    "Std",
    "Lean",
    "Batteries",
    "Qq",
    "Aesop",
    "ProofWidgets",
    "ImportGraph",
    "LeanSearchClient",
    "Plausible",
    "Cli",
    "Lake",
)
PINS = ("lean4/lean-toolchain", "lean4/lake-manifest.json", "lean4/lakefile.lean")
ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
FORBIDDEN_TOKENS = ("sorry", "admit", "native_decide", "unsafe", "partial", "implemented_by", "opaque", "axiom")

MODIFIER_RE = re.compile(r"^(?P<mod>private|protected|public|noncomputable|nonrec|scoped|local|unsafe|partial)\b\s*")
SCOPE = re.compile(
    r"^(?:(?P<sec_mod>noncomputable)\s+)?(?P<kw>namespace|section|mutual|end)"
    r"(?:\s+(?P<name>[A-Za-z_\u0080-\uffff][\w.']*))?\s*$"
)
DECL_HEAD = re.compile(
    r"^(?P<kw>class\s+inductive|theorem|lemma|def|abbrev|structure|inductive|class|instance|opaque|axiom)"
    r"(?P<tail>\s+.*)?$"
)
DECL_NAME = re.compile(r"^(?P<name>[^\s:(\[{⟨|]+)(?P<after>.*)$")
RESERVED_KW = re.compile(
    r"(?<![\w.'«])(theorem|lemma|def|abbrev|structure|inductive|class|instance|opaque|axiom|namespace|section|end)(?![\w'»])"
)
IMPORT_RE = re.compile(r"^\s*import\s+(?P<mod>[A-Za-z_\u0080-\uffff][\w.]*)\s*$")
# A declaration name may itself end in a prime (`completeness'`), so the name is read lazily up to
# the quote that precedes the report text.
REPORT = re.compile(r"'(.+?)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")
COMPILER_DECL = re.compile(r"^COMPILER_DECL:([A-Za-z0-9_.]+):(\S+)\s*$", re.M)
IND_AUX = (
    "recOn",
    "casesOn",
    "noConfusion",
    "noConfusionType",
    "below",
    "ibelow",
    "brecOn",
    "binductionOn",
    "inj",
    "injEq",
    "sizeOf_spec",
    "ctorIdx",
)


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
    if depth:
        raise SystemExit("unclosed block comment in Lean source")
    return "".join(out)


def _strip_one_attribute(text: str) -> tuple[str, bool, bool]:
    """Strip one leading ``@[...]`` attribute with balanced brackets.

    Returns ``(remainder, consumed, unclosed)``.
    """
    s = text.lstrip()
    if not s.startswith("@["):
        return s, False, False
    depth = 1
    i = 2
    n = len(s)
    while i < n and depth > 0:
        if s[i] == "[":
            depth += 1
        elif s[i] == "]":
            depth -= 1
        i += 1
    if depth > 0:
        return s, True, True
    return s[i:].lstrip(), True, False


def _consume_attrs_and_modifiers(text: str) -> tuple[str, set[str], bool, bool]:
    """Consume any interleaved ``@[...]`` attributes and declaration modifiers."""
    s = text.lstrip()
    mods: set[str] = set()
    saw_attr = False
    while True:
        s_next, consumed, unclosed = _strip_one_attribute(s)
        if unclosed:
            return s, mods, saw_attr, True
        if consumed:
            saw_attr = True
            s = s_next
            continue
        m = MODIFIER_RE.match(s)
        if m:
            mods.add(m.group("mod"))
            s = s[m.end():].lstrip()
            continue
        break
    return s, mods, saw_attr, False


def inventory_of(source: str) -> list[str]:
    """Fully qualified names of the named declarations in one module source, in order."""
    names: list[str] = []
    stack: list[tuple[str, str | None]] = []
    pending_attr = False
    pending_mods: set[str] = set()

    for lineno, raw in enumerate(strip_comments(source).splitlines(), 1):
        stripped = raw.strip()
        if not stripped:
            continue

        scope = SCOPE.match(stripped)
        if scope and not pending_mods:
            sec_mod, kw, name = scope.group("sec_mod"), scope.group("kw"), scope.group("name")
            if sec_mod and kw != "section":
                raise SystemExit(f"line {lineno}: invalid modifier {sec_mod!r} on {kw}")
            if kw == "namespace":
                if pending_attr:
                    raise SystemExit(f"line {lineno}: dangling attribute before namespace")
                if not name or "" in name.split("."):
                    raise SystemExit(f"line {lineno}: invalid namespace command: {stripped!r}")
                for part in name.split("."):
                    stack.append(("namespace", part))
            elif kw == "section":
                pending_attr = False
                if name is None:
                    stack.append(("section", None))
                else:
                    if "" in name.split("."):
                        raise SystemExit(f"line {lineno}: invalid section name: {stripped!r}")
                    for part in name.split("."):
                        stack.append(("section", part))
            elif kw == "mutual":
                pending_attr = False
                if name is not None:
                    raise SystemExit(f"line {lineno}: unexpected name on mutual: {stripped!r}")
                stack.append(("mutual", None))
            elif kw == "end":
                if pending_attr:
                    raise SystemExit(f"line {lineno}: dangling attribute before end")
                if name is None:
                    if not stack:
                        raise SystemExit(f"line {lineno}: unmatched 'end' with empty scope stack")
                    top_kw, top_name = stack[-1]
                    if top_name is not None:
                        raise SystemExit(
                            f"line {lineno}: anonymous 'end' cannot close named {top_kw} {top_name!r}"
                        )
                    stack.pop()
                else:
                    parts = name.split(".")
                    if "" in parts:
                        raise SystemExit(f"line {lineno}: invalid end name: {stripped!r}")
                    for part in reversed(parts):
                        if not stack or stack[-1][1] != part:
                            expected = stack[-1][1] if stack else None
                            raise SystemExit(
                                f"line {lineno}: mismatched 'end {name}': expected {expected!r}, got {part!r}"
                            )
                        stack.pop()
            continue

        rest, line_mods, saw_attr, unclosed_attr = _consume_attrs_and_modifiers(stripped)
        if unclosed_attr:
            raise SystemExit(f"line {lineno}: unclosed attribute in {stripped!r}")

        if not rest and (saw_attr or line_mods):
            pending_attr = pending_attr or saw_attr
            pending_mods |= line_mods
            continue

        mods = pending_mods | line_mods
        had_prefix = pending_attr or saw_attr or bool(mods)
        pending_attr = False
        pending_mods = set()

        if rest in ("section", "mutual") or rest.startswith("section "):
            scope_after = SCOPE.match(rest)
            if scope_after and mods <= {"noncomputable", "public"}:
                name = scope_after.group("name")
                if scope_after.group("kw") == "mutual":
                    if name is not None:
                        raise SystemExit(f"line {lineno}: unexpected name on mutual: {stripped!r}")
                    stack.append(("mutual", None))
                elif name is None:
                    stack.append(("section", None))
                else:
                    if "" in name.split("."):
                        raise SystemExit(f"line {lineno}: invalid section name: {stripped!r}")
                    for part in name.split("."):
                        stack.append(("section", part))
                continue

        decl_head = DECL_HEAD.match(rest)
        if decl_head:
            kw = re.sub(r"\s+", " ", decl_head.group("kw"))
            tail = (decl_head.group("tail") or "").lstrip()
            if not tail:
                raise SystemExit(f"line {lineno}: incomplete {kw} declaration: {stripped!r}")
            if kw == "instance" and tail.startswith((":", "(", "[", "{")):
                if RESERVED_KW.search(tail):
                    raise SystemExit(f"line {lineno}: embedded keyword in anonymous instance: {stripped!r}")
                continue  # anonymous instance
            m_name = DECL_NAME.match(tail)
            if not m_name:
                raise SystemExit(f"line {lineno}: malformed {kw} declaration: {stripped!r}")
            name = m_name.group("name")
            after = m_name.group("after")
            if name.startswith(".") or name.endswith(".") or ".." in name:
                raise SystemExit(f"line {lineno}: invalid declaration identifier {name!r}")
            if RESERVED_KW.search(after):
                raise SystemExit(f"line {lineno}: multiple or unsupported commands on one line: {stripped!r}")
            if "private" in mods:
                continue  # mangled name, not an exported binding
            prefix = ".".join(n for kw_s, n in stack if kw_s == "namespace" and n)
            names.append(f"{prefix}.{name}" if prefix else name)
            continue

        if had_prefix:
            raise SystemExit(
                f"line {lineno}: attributes or modifiers not followed by a supported declaration: {stripped!r}"
            )
        if RESERVED_KW.search(stripped):
            raise SystemExit(f"line {lineno}: unsupported declaration or scope syntax: {stripped!r}")

    if pending_attr or pending_mods:
        raise SystemExit("dangling attributes or modifiers at end of module")
    if stack:
        raise SystemExit(f"unclosed scope(s) at end of module: {stack}")
    return names


def inventory(root: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for module in MODULES:
        names = inventory_of((root / module_path(module)).read_text(encoding="utf-8"))
        if not names:
            raise SystemExit(f"empty declaration inventory in {module}")
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            raise SystemExit(f"duplicate declaration names in {module}: {dupes}")
        result[module] = names
    return result


def forbidden_tokens(root: Path) -> list[str]:
    hits: list[str] = []
    for module in MODULES + DEPENDENCIES:
        text = strip_comments((root / module_path(module)).read_text(encoding="utf-8"))
        for token in FORBIDDEN_TOKENS:
            if re.search(rf"(?<![\w.']){re.escape(token)}(?![\w'])", text):
                hits.append(f"{module}: {token}")
    return hits


def unpinned_imports(root: Path) -> list[str]:
    allowed_local = set(MODULES) | set(DEPENDENCIES)
    hits: list[str] = []
    for module in MODULES + DEPENDENCIES:
        text = strip_comments((root / module_path(module)).read_text(encoding="utf-8"))
        for raw in text.splitlines():
            m = IMPORT_RE.match(raw)
            if not m:
                continue
            imp = m.group("mod")
            top = imp.split(".", 1)[0]
            if top in EXTERNAL_PACKAGES or imp in allowed_local:
                continue
            hits.append(f"{module}: {imp}")
    return hits


def pins(root: Path) -> dict[str, str]:
    paths = [module_path(m) for m in MODULES + DEPENDENCIES] + list(PINS)
    return {p: sha256(root, p) for p in paths}


def parse_all_reports(text: str) -> dict[str, list[list[str]]]:
    reports: dict[str, list[list[str]]] = {}
    for name, axioms in REPORT.findall(text):
        parsed = [a.strip() for a in axioms.split(",") if a.strip()] if axioms else []
        reports.setdefault(name, []).append(parsed)
    return reports


def parse_reports(text: str) -> dict[str, list[str]]:
    reports: dict[str, list[str]] = {}
    for name, entries in parse_all_reports(text).items():
        merged: list[str] = []
        for entry in entries:
            for ax in entry:
                if ax not in merged:
                    merged.append(ax)
        reports[name] = merged
    return reports


def parse_compiler_declarations(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for mod, name in COMPILER_DECL.findall(text):
        result.setdefault(mod, []).append(name)
    return result


def emit(root: Path, target: Path) -> int:
    inv = inventory(root)
    lines = [f"import {m}" for m in MODULES] + ["import Lean", ""]
    for module, names in inv.items():
        lines.append(f"-- {module}")
        lines += [f"#print axioms {n}" for n in names]
        lines.append("")
    ind_aux_lit = ", ".join(json.dumps(s) for s in IND_AUX)
    expected_entries = []
    for module, names in inv.items():
        names_lit = ", ".join(json.dumps(n, ensure_ascii=False) for n in names)
        expected_entries.append(f"    (`{module}, [{names_lit}])")
    lines += [
        "-- Compiler-derived declaration check (independent of source regex parser)",
        "open Lean Elab Command in",
        "#eval liftTermElabM do",
        "  let env ← getEnv",
        f"  let indAux : List String := [{ind_aux_lit}]",
        "  let expected : List (Name × List String) := [",
        ",\n".join(expected_entries),
        "  ]",
        "  for (modName, want) in expected do",
        '    let some modIdx := env.getModuleIdx? modName | throwError s!"missing module {modName}"',
        "    let modData := env.header.moduleData[modIdx.toNat]!",
        "    let mut found : List String := []",
        "    for name in modData.constNames do",
        "      if name.isInternalDetail then continue",
        "      match env.find? name with",
        "      | some (.ctorInfo _) | some (.recInfo _) => continue",
        "      | _ => pure ()",
        "      if env.isProjectionFn name then continue",
        "      if let .str p s := name then",
        "        if indAux.contains s then",
        "          if let some (.inductInfo _) := env.find? p then continue",
        "      let rendered := name.toString (escape := false)",
        "      found := rendered :: found",
        '      IO.println s!"COMPILER_DECL:{modName}:{rendered}"',
        "      if !want.contains rendered then",
        '        throwError s!"compiler declaration missing from audit inventory in {modName}: {rendered}"',
        "    for w in want do",
        "      if !found.contains w then",
        '        throwError s!"audit inventory declaration missing from compiler environment in {modName}: {w}"',
        "",
    ]
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

    exp_decls = expectation.get("declarations")
    if not isinstance(exp_decls, dict) or set(exp_decls.keys()) != set(MODULES):
        errors.append("expectation declarations missing required modules")
    else:
        for module in MODULES:
            mod_names = exp_decls.get(module)
            if not isinstance(mod_names, list) or not mod_names:
                errors.append(f"empty expected declaration inventory: {module}")
            elif len(set(mod_names)) != len(mod_names):
                errors.append(f"duplicate expected declaration names: {module}")

    try:
        inv = inventory(root)
    except SystemExit as exc:
        errors.append(f"inventory error: {exc}")
        inv = None

    if inv is not None and inv != exp_decls:
        errors.append("declaration inventory differs from the expectation file (run `update` after review)")

    compiler_decls = parse_compiler_declarations(lean_output)
    if compiler_decls and isinstance(exp_decls, dict):
        for module in MODULES:
            want_set = set(exp_decls.get(module) or [])
            got_set = set(compiler_decls.get(module) or [])
            if got_set != want_set:
                errors.append(f"compiler declaration inventory differs for {module}")

    try:
        errors += [f"forbidden token: {h}" for h in forbidden_tokens(root)]
        errors += [f"unpinned import: {h}" for h in unpinned_imports(root)]
    except SystemExit as exc:
        errors.append(f"source scan error: {exc}")

    if re.search(r"^.*\berror\b", lean_output, flags=re.M):
        errors.append("Lean output contains an error line")

    all_reports = parse_all_reports(lean_output)
    for name, entries in all_reports.items():
        if len(entries) > 1:
            first = set(entries[0])
            if any(set(other) != first for other in entries[1:]):
                errors.append(f"contradictory duplicate reports for {name}")
            else:
                errors.append(f"duplicate report for {name}")

    reports = parse_reports(lean_output)
    allowed = set(expectation.get("allowed_axioms", ALLOWED_AXIOMS))
    expected_set: set[str] = set()
    if isinstance(exp_decls, dict):
        for names in exp_decls.values():
            if not isinstance(names, list):
                continue
            for name in names:
                expected_set.add(name)
                if name not in reports:
                    errors.append(f"missing report: {name}")
                    continue
                extra = sorted(set(reports[name]) - allowed)
                if extra:
                    errors.append(f"unexpected axioms for {name}: {extra}")
    for name in sorted(set(reports) - expected_set):
        errors.append(f"unexpected report: {name}")
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
    exp_decls = expectation.get("declarations", {})
    checked = sum(len(v) for v in exp_decls.values() if isinstance(v, list)) if isinstance(exp_decls, dict) else 0
    summary = {
        "all_passed": not errors,
        "declarations_checked": checked,
        "errors": errors,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
