"""Origin: scripts/auto/anti_pattern_lint.py (merges the_symbol_game auto-anti-pattern-lint/scripts/anti_pattern_lint.py and auto-code-anti-pattern-hunter/scripts/hunt_antipatterns.py, adapted)
Claim: checks that every anti-pattern card in .agents/patterns has a dual healthy-pattern card, and finds the mechanical signatures of the cards that have one: Lean admission tokens and axiom declarations, blanket type ignores, host-absolute paths, tautological tests and floating point in independent checks
AuthorityEffect: None
Scope Fence: a finding is a prompt for the human pass of .claude/skills/auto-code-anti-pattern-hunter; an empty scan does not show that code is free of anti-patterns, and the cards that have no signature here are read by hand
Level: L4

Usage (from the repository root):
    python -I -X utf8 scripts/auto/anti_pattern_lint.py                               # whole checkout
    python -I -X utf8 scripts/auto/anti_pattern_lint.py --changed-since origin/main   # changed files; Lean rules on added lines only
    python -I -X utf8 scripts/auto/anti_pattern_lint.py --catalog-only
Exit status: 0 ok; 1 a finding at or above --fail-on (default HIGH); 2 usage or environment error.
With --changed-since, the only HIGH rules (AP_LN_001, AP_LN_004) read added Lean lines, so the default gate is the
campaign rule "no sorry, admit, axiom, native_decide or unsafe in added Lean".
"""

from __future__ import annotations

import ast
import io
import re
import sys
import tokenize
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
for entry in (HERE, HERE.parent):  # python -I does not put the script directory on sys.path
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from auto_common import AuditError, Finding, added_lines, base_parser, changed_files, emit, in_scope, parse_front_matter, read_text, run_main, tracked_files  # noqa: E402
from overclaim_lean import strip_lean  # noqa: E402

TOOL = "anti_pattern_lint"
CATALOG = ".agents/patterns"
REQUIRED_SLOTS = ("lean4", "markdown", "math", "python", "rust")
CARD_NAME = re.compile(r"^(AP|HP)_([A-Z0-9]+_\d{3})_[a-z0-9_]+\.md$")

# The tokens the campaign honesty gate forbids in added Lean (dag/pfp/campaign/README.md). axiom is a declaration keyword
# and has its own rule; the other four are matched as whole words outside comments and strings.
LEAN_FORBIDDEN = ("sorry", "admit", "native_decide", "unsafe", "axiom")  # a literal: scripts/auto/symmetry_scan.py reads it
LEAN_ADMISSION_TOKENS = tuple(token for token in LEAN_FORBIDDEN if token != "axiom")
ADMISSION_RE = re.compile(r"(?<![\w.'])(" + "|".join(LEAN_ADMISSION_TOKENS) + r")(?![\w'])")
AXIOM_DECL_RE = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe|partial)\s+)*axiom\s+\S")
BLANKET_IGNORE = re.compile(r"#\s*type:\s*ignore(?!\s*\[)")
HOST_PATH = re.compile(r"""^[rRbBuUfF]{0,2}['"]{1,3}(?:file:///)?(?:[A-Za-z]:[\\/]+(?:Users|home)[\\/]|/(?:home|Users)/[^/'"\s]+/)""")
INDEPENDENT_PREFIX = "checks/independent/"
FLOAT_FUNCS = {"sqrt", "exp", "log", "sin", "cos", "tan", "atan2", "hypot"}
FLOAT_CONSTANTS = {"pi", "e", "tau", "inf", "nan"}


# `admit` is also an ordinary Lean identifier (`def admit ...`, `unfold admit`, `admit d guards`). The tactic takes no
# argument, so it is followed by the end of the line or by a closing or separating token.
ADMIT_TACTIC_END = re.compile(r"\s*(?:$|[)};,\]|<]|--|=>)")
IDENTIFIER_CONTEXT = re.compile(r"(?:\b(?:def|theorem|lemma|abbrev|instance|unfold|delta)|[\[,])\s*$")


def not_the_tactic(line: str, hit: re.Match[str], constructor: bool = False) -> bool:
    """True when the matched token is a name (constructor, match arm, or the identifier `admit`), not the tactic."""
    before = line[: hit.start()].rstrip()
    if before.endswith("|") and hit.group(1) == "admit":
        # A tactic alternative also starts with |; only constructor context or
        # an actual match-arm arrow identifies the ordinary identifier here.
        if constructor or "=>" in line[hit.end() :]:
            return True
    if hit.group(1) != "admit":
        return False
    return bool(IDENTIFIER_CONTEXT.search(before)) or not ADMIT_TACTIC_END.match(line[hit.end() :])


def is_test_file(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    return name.startswith("test_") or name.endswith("_test.py") or "/tests/" in f"/{rel}"


# --------------------------------------------------------------------------------------------
# Catalog layout


def audit_catalog(root: Path) -> list[Finding]:
    base = root / CATALOG
    if not base.is_dir():
        return [Finding("CATALOG_MISSING", "MEDIUM", CATALOG, 0, "the pattern catalog directory is absent")]
    found: list[Finding] = []
    for side in ("anti", "helpful"):
        for slot in REQUIRED_SLOTS:
            if not (base / side / slot).is_dir():
                found.append(Finding("CATALOG_SLOT_MISSING", "MEDIUM", f"{CATALOG}/{side}/{slot}", 0, "required catalog slot is absent"))
    cards = {path.stem: path for path in sorted(base.glob("*/*/*.md")) if path.parent.parent.name in ("anti", "helpful")}
    for stem, path in cards.items():
        found.extend(_audit_card(root, stem, path, cards))
    return found


def _audit_card(root: Path, stem: str, path: Path, cards: dict[str, Path]) -> list[Finding]:
    rel = path.relative_to(root).as_posix()
    side = path.parent.parent.name
    match = CARD_NAME.match(path.name)
    if not match or (match.group(1) == "AP") != (side == "anti"):
        return [Finding("CARD_NAME", "MEDIUM", rel, 0, "card name must be AP_<ID>_<words>.md under anti/ or HP_<ID>_<words>.md under helpful/")]
    meta, _, error = parse_front_matter(read_text(root, rel) or "")
    if meta is None:
        return [Finding("CARD_FRONT_MATTER", "MEDIUM", rel, 1, error)]
    found: list[Finding] = []
    expected_id = f"{match.group(1)}_{match.group(2)}"
    if meta.get("pattern_id") != expected_id:
        found.append(Finding("CARD_ID_MISMATCH", "MEDIUM", rel, 1, f"pattern_id {meta.get('pattern_id')!r} differs from file name {expected_id}"))
    dual = str(meta.get("dual_pattern") or "")
    if not dual:
        found.append(Finding("DUAL_MISSING", "MEDIUM", rel, 1, "card names no dual_pattern"))
    elif dual not in cards:
        found.append(Finding("DUAL_FILE_MISSING", "MEDIUM", rel, 1, f"dual card {dual}.md is absent"))
    else:
        back, _, _ = parse_front_matter(read_text(root, cards[dual].relative_to(root).as_posix()) or "")
        if back is not None and str(back.get("dual_pattern") or "") != stem:
            found.append(Finding("DUAL_NOT_RECIPROCAL", "MEDIUM", rel, 1, f"{dual} does not name this card as its dual"))
    return found


# --------------------------------------------------------------------------------------------
# File signatures


def lean_findings(rel: str, text: str, only_lines: set[int] | None) -> list[Finding]:
    found: list[Finding] = []
    constructor = False
    for number, line in enumerate(strip_lean(text).splitlines(), 1):
        if re.match(r"^\s*(?:(?:private|protected)\s+)*inductive\b", line):
            constructor = True
        elif re.match(r"^\s*(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|example|instance|abbrev|namespace|end)\b", line):
            constructor = False
        if only_lines is not None and number not in only_lines:
            continue
        hit = next((m for m in ADMISSION_RE.finditer(line) if not not_the_tactic(line, m, constructor)), None)
        if hit:
            found.append(Finding("AP_LN_001", "HIGH", rel, number, f"Lean admission token `{hit.group(1)}` outside comments and strings"))
        if AXIOM_DECL_RE.match(line):
            found.append(Finding("AP_LN_004", "HIGH", rel, number, "Lean `axiom` declaration"))
    return found


def _python_tokens(text: str) -> list[tokenize.TokenInfo]:
    try:
        return list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return []


def python_token_findings(rel: str, text: str) -> list[Finding]:
    found: list[Finding] = []
    test = is_test_file(rel)
    for tok in _python_tokens(text):
        if tok.type == tokenize.COMMENT and BLANKET_IGNORE.search(tok.string):
            found.append(Finding("AP_PY_001", "LOW", rel, tok.start[0], "blanket `# type: ignore` without an error code"))
        elif tok.type == tokenize.STRING and not test and HOST_PATH.match(tok.string):
            found.append(Finding("AP_PY_006", "MEDIUM", rel, tok.start[0], "host-absolute path literal", tok.string[:60]))
        elif tok.type == tokenize.NUMBER and rel.startswith(INDEPENDENT_PREFIX) and _is_float_literal(tok.string):
            found.append(Finding("AP_MATH_011", "MEDIUM", rel, tok.start[0], f"floating-point literal {tok.string} in an independent check"))
    return found


def _is_float_literal(token: str) -> bool:
    lowered = token.lower().replace("_", "")
    if lowered.startswith(("0x", "0o", "0b")) or lowered.endswith("j"):
        return False
    return "." in lowered or "e" in lowered


def _all_constant(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.Tuple, ast.List)):
        return all(_all_constant(item) for item in node.elts)
    if isinstance(node, ast.UnaryOp):
        return _all_constant(node.operand)
    if isinstance(node, ast.BinOp):
        return _all_constant(node.left) and _all_constant(node.right)
    return False


def _tautological_assert(node: ast.Assert) -> bool:
    test = node.test
    if isinstance(test, ast.Constant):
        return bool(test.value)
    if isinstance(test, ast.Compare):
        return _all_constant(test.left) and all(_all_constant(item) for item in test.comparators)
    return False


def _raises_only_raise(node: ast.With) -> bool:
    calls = [item.context_expr for item in node.items if isinstance(item.context_expr, ast.Call)]
    named = any(isinstance(c.func, ast.Attribute) and c.func.attr == "raises" for c in calls)
    return named and len(node.body) == 1 and isinstance(node.body[0], ast.Raise)


def python_ast_findings(rel: str, text: str) -> list[Finding]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)  # invalid escapes in scanned files are not this tool's findings
            tree = ast.parse(text)
    except SyntaxError as error:
        return [Finding("UNPARSEABLE", "LOW", rel, error.lineno or 0, "Python does not parse; token and AST rules not applied")]
    found: list[Finding] = []
    test = is_test_file(rel)
    independent = rel.startswith(INDEPENDENT_PREFIX)
    for node in ast.walk(tree):
        if test and isinstance(node, ast.Assert) and _tautological_assert(node):
            found.append(Finding("AP_PY_019", "MEDIUM", rel, node.lineno, "assert over constants only; it cannot fail on the code under test"))
        elif test and isinstance(node, ast.With) and _raises_only_raise(node):
            found.append(Finding("AP_PY_019", "MEDIUM", rel, node.lineno, "pytest.raises around a bare raise; no code under test runs"))
        elif independent and isinstance(node, ast.Call) and _float_call(node.func):
            found.append(Finding("AP_MATH_011", "MEDIUM", rel, node.lineno, f"floating-point call `{_call_name(node.func)}` in an independent check"))
        elif independent and isinstance(node, ast.Attribute) and _float_constant(node):
            found.append(Finding("AP_MATH_011", "MEDIUM", rel, node.lineno, f"floating-point constant `math.{node.attr}` in an independent check"))
    return found


def _float_constant(node: ast.AST) -> bool:
    return (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
            and node.value.id in ("math", "cmath") and node.attr in FLOAT_CONSTANTS)


def _call_name(func: ast.AST) -> str:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _float_call(func: ast.AST) -> bool:
    if isinstance(func, ast.Name):
        return func.id == "float"
    if isinstance(func, ast.Attribute):
        owner = func.value.id if isinstance(func.value, ast.Name) else ""
        return func.attr == "evalf" or (owner in ("math", "cmath") and func.attr in FLOAT_FUNCS)
    return False


def scan_file(root: Path, rel: str, only_added: set[int] | None) -> list[Finding]:
    """Findings for one file. only_added restricts the Lean rules to those line numbers (None: every line)."""
    if not rel.endswith((".lean", ".py")):
        return []
    text = read_text(root, rel)
    if text is None:
        return [Finding("UNREADABLE", "LOW", rel, 0, "file is not readable UTF-8; not scanned")]
    if rel.endswith(".lean"):
        return lean_findings(rel, text, only_added)
    if rel.endswith(".py"):
        return python_token_findings(rel, text) + python_ast_findings(rel, text)
    return []


def scan(root: Path, ref: str | None, catalog_only: bool = False) -> tuple[list[Finding], str]:
    found = audit_catalog(root)
    if catalog_only:
        return found, "pattern catalog"
    if ref:
        files = [name for name in changed_files(root, ref) if name.endswith((".lean", ".py")) and in_scope(name)]
        for rel in files:
            found.extend(scan_file(root, rel, added_lines(root, ref, rel) if rel.endswith(".lean") else None))
        return found, f"{len(files)} changed .lean/.py files since {ref} (Lean rules: added lines)"
    files = [name for name in tracked_files(root, ("*.lean", "*.py")) if in_scope(name)]
    for rel in files:
        found.extend(scan_file(root, rel, None))
    return found, f"whole checkout, {len(files)} .lean/.py files"


def main(argv: list[str] | None = None) -> int:
    parser = base_parser(__doc__.splitlines()[1])
    parser.add_argument("--catalog-only", action="store_true", help="check only the .agents/patterns catalog")
    args = parser.parse_args(argv)

    def body() -> int:
        root = args.repo_root.resolve()
        if not (root / ".git").exists():
            raise AuditError(f"{root} is not a git checkout")
        findings, scope = scan(root, args.changed_since, args.catalog_only)
        return emit(TOOL, "Anti-pattern lint", findings, args, scope)

    return run_main(TOOL, body)


if __name__ == "__main__":
    sys.exit(main())
