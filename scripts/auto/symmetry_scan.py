"""Origin: scripts/auto/symmetry_scan.py (new code for the adapted the_symbol_game auto-symmetry-hunter skill, which had no script)
Claim: compares every prose copy of four honesty invariants (the allowed Lean axioms, the forbidden Lean tokens, the status order and the validator's forbidden words) with the code constants that enforce them, and reports where a copy names an item the code does not or omits one it does
AuthorityEffect: None
Scope Fence: the code constants are taken as the reference only for comparison; a finding says two copies differ, not which one should change, and prose extraction is heuristic, so an empty scan does not show the copies agree
Level: L4

Usage (from the repository root):
    python -I -X utf8 scripts/auto/symmetry_scan.py
    python -I -X utf8 scripts/auto/symmetry_scan.py --changed-since origin/main
Exit status: 0 ok; 1 a finding at or above --fail-on (default HIGH); 2 usage or environment error.
"""

from __future__ import annotations

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:  # python -I does not put the script directory on sys.path
    sys.path.insert(0, str(HERE))

from auto_common import AuditError, Finding, base_parser, changed_files, emit, read_text, run_main, sentences, tracked_files  # noqa: E402

TOOL = "symmetry_scan"
SCANNER = "scripts/overclaim_scan.py"
VALIDATOR = "dag/validate_derivation_dag.py"
LINT = "scripts/auto/anti_pattern_lint.py"
PROSE_PATTERNS = ("README.md", "CONTRIBUTING.md", "REVIEWING.md", "dag/pfp/campaign/README.md",
                  "dag/derivation_dag_reading_note.md", ".claude/skills/*.md", ".claude/rules/*.md",
                  ".agents/rules/*.md", ".agents/patterns/*.md")
AXIOM_VOCAB = ("propext", "Classical.choice", "Quot.sound", "funext", "sorryAx", "Lean.ofReduceBool",
               "Lean.trustCompiler", "Classical.em")
TOKEN_VOCAB = ("sorry", "admit", "axiom", "native_decide", "unsafe", "implemented_by", "extern")
STATUS_CHAIN = re.compile(r"\b[A-Z][A-Z_]{2,}(?:\s*<\s*[A-Z][A-Z_]{2,}){2,}")
QUOTED = re.compile(r"[`\"']([a-z][a-z ]{1,30}[a-z])[`\"']")
FORBIDDEN_CUE = re.compile(r"validator(?:'s)?\b.*\b(?:refuses|FORBIDDEN|forbidden)|FORBIDDEN.*\bvalidator", re.IGNORECASE)


@dataclass(frozen=True)
class Reference:
    axioms: frozenset[str]
    tokens: frozenset[str]
    ranks: dict[str, int]
    forbidden: frozenset[str]


def literal_assignment(root: Path, rel: str, name: str) -> Any:
    """The literal value assigned to a module-level name, read without importing the module."""
    text = read_text(root, rel)
    if text is None:
        raise AuditError(f"{rel} is missing")
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        raise AuditError(f"{rel} does not parse: {error}") from error
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == name for t in targets) and node.value is not None:
            try:
                return ast.literal_eval(node.value)
            except ValueError as error:
                raise AuditError(f"{rel}: {name} is not a literal") from error
    raise AuditError(f"{rel} has no module-level {name}")


def load_reference(root: Path) -> tuple[Reference, list[Finding]]:
    axioms = frozenset(literal_assignment(root, SCANNER, "ALLOWED_AXIOMS"))
    scanner_tokens = frozenset(literal_assignment(root, SCANNER, "LEAN_ADMISSION_TOKENS")) | {"axiom"}
    ranks = dict(literal_assignment(root, VALIDATOR, "PFP_STATUS_RANK"))
    forbidden = frozenset(word.lower() for word in literal_assignment(root, VALIDATOR, "FORBIDDEN"))
    found: list[Finding] = []
    if (root / LINT).is_file():
        lint_tokens = frozenset(literal_assignment(root, LINT, "LEAN_FORBIDDEN"))
        if lint_tokens != scanner_tokens:
            found.append(Finding("SYM_TOKENS", "HIGH", LINT, 0, "CONTRADICTION: forbidden Lean tokens differ from the overclaim scanner",
                                 f"lint {sorted(lint_tokens)}, scanner {sorted(scanner_tokens)}"))
    return Reference(axioms, scanner_tokens, ranks, forbidden), found


def _present(vocab: tuple[str, ...], sentence: str) -> set[str]:
    return {word for word in vocab if re.search(r"(?<![\w.])" + re.escape(word) + r"(?![\w])", sentence)}


def check_axioms(rel: str, number: int, sentence: str, ref: Reference) -> list[Finding]:
    named = _present(AXIOM_VOCAB, sentence)
    if len(named & ref.axioms) < 2 or not re.search(r"\bonly\b", sentence, re.IGNORECASE):
        return []
    found: list[Finding] = []
    extra, missing = named - ref.axioms, ref.axioms - named
    if extra:
        found.append(Finding("SYM_AXIOMS", "HIGH", rel, number, f"DANGEROUS_DRIFT: allowed-axiom list adds {', '.join(sorted(extra))}"))
    if missing:
        found.append(Finding("SYM_AXIOMS", "MEDIUM", rel, number, f"MISSING_PROPAGATION: allowed-axiom list omits {', '.join(sorted(missing))}"))
    return found


def check_tokens(rel: str, number: int, sentence: str, ref: Reference) -> list[Finding]:
    named = _present(TOKEN_VOCAB, sentence)
    if not {"sorry", "native_decide"} <= named:
        return []
    found: list[Finding] = []
    if named - ref.tokens:
        found.append(Finding("SYM_TOKENS", "LOW", rel, number, f"EXTENSION: forbidden-token list adds {', '.join(sorted(named - ref.tokens))}"))
    if ref.tokens - named:
        found.append(Finding("SYM_TOKENS", "MEDIUM", rel, number, f"MISSING_PROPAGATION: forbidden-token list omits {', '.join(sorted(ref.tokens - named))}"))
    return found


def check_status_order(rel: str, number: int, line: str, ref: Reference) -> list[Finding]:
    found: list[Finding] = []
    for match in STATUS_CHAIN.finditer(line):
        chain = [item.strip() for item in match.group(0).split("<")]
        unknown = [item for item in chain if item not in ref.ranks]
        if unknown:
            found.append(Finding("SYM_STATUS", "MEDIUM", rel, number, f"STALE_RULE: status order names unknown {', '.join(unknown)}"))
            continue
        for low, high in zip(chain, chain[1:]):
            if ref.ranks[low] >= ref.ranks[high]:
                found.append(Finding("SYM_STATUS", "HIGH", rel, number,
                                     f"CONTRADICTION: prose orders {low} < {high}, validator ranks {ref.ranks[low]} and {ref.ranks[high]}"))
    return found


def quoted_runs(line: str, min_len: int = 3, max_gap: int = 30) -> list[list[str]]:
    """Runs of quoted words separated only by short connective text (a written-out word list)."""
    runs: list[list[str]] = []
    current: list[str] = []
    last_end = None
    for match in QUOTED.finditer(line):
        gap = line[last_end : match.start()] if last_end is not None else ""
        if last_end is None or len(gap) > max_gap or any(q in gap for q in "`\""):
            if len(current) >= min_len:
                runs.append(current)
            current = []
        current.append(match.group(1).lower())
        last_end = match.end()
    if len(current) >= min_len:
        runs.append(current)
    return runs


def check_forbidden_words(rel: str, number: int, line: str, ref: Reference) -> list[Finding]:
    """A line that says the validator refuses words, and lists three or more quoted words, must list only FORBIDDEN words."""
    if not FORBIDDEN_CUE.search(line):
        return []
    quoted = {word for run in quoted_runs(line) for word in run if len(word.split()) <= 3}
    stray = sorted(word for word in quoted if word not in ref.forbidden and word != "forbidden")
    if not stray:
        return []
    return [Finding("SYM_FORBIDDEN", "MEDIUM", rel, number,
                    f"CONTRADICTION: prose says the validator refuses {', '.join(stray)}, which its FORBIDDEN list lacks")]


def paragraphs(text: str) -> list[tuple[int, str]]:
    """(first line number, paragraph text) for each blank-line-separated block outside fenced code."""
    out: list[tuple[int, str]] = []
    block: list[str] = []
    start, fenced = 0, False
    for number, line in enumerate(text.splitlines() + [""], 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.strip():
            start = start or number
            block.append(line)
        elif block:
            out.append((start, " ".join(block)))
            block, start = [], 0
    return out


def scan_text(rel: str, text: str, ref: Reference) -> list[Finding]:
    found: list[Finding] = []
    for number, line in enumerate(text.splitlines(), 1):
        found.extend(check_forbidden_words(rel, number, line, ref))
    for number, para in paragraphs(text):
        found.extend(check_status_order(rel, number, para, ref))
        for sentence in sentences(para):
            found.extend(check_axioms(rel, number, sentence, ref))
            found.extend(check_tokens(rel, number, sentence, ref))
    return found


def prose_files(root: Path, ref_name: str | None) -> list[str]:
    files = tracked_files(root, PROSE_PATTERNS)
    if ref_name:
        changed = set(changed_files(root, ref_name))
        files = [rel for rel in files if rel in changed]
    return files


def scan(root: Path, ref_name: str | None) -> tuple[list[Finding], str]:
    reference, found = load_reference(root)
    files = prose_files(root, ref_name)
    for rel in files:
        text = read_text(root, rel)
        if text is None:
            found.append(Finding("UNREADABLE", "LOW", rel, 0, "prose file is not readable UTF-8; not compared"))
        else:
            found.extend(scan_text(rel, text, reference))
    scope = f"{len(files)} prose files" + (f" changed since {ref_name}" if ref_name else "") + "; code constants always compared"
    return found, scope


def main(argv: list[str] | None = None) -> int:
    parser = base_parser(__doc__.splitlines()[1])
    args = parser.parse_args(argv)

    def body() -> int:
        root = args.repo_root.resolve()
        if not (root / ".git").exists():
            raise AuditError(f"{root} is not a git checkout")
        findings, scope = scan(root, args.changed_since)
        return emit(TOOL, "Symmetry scan", findings, args, scope)

    return run_main(TOOL, body)


if __name__ == "__main__":
    sys.exit(main())
