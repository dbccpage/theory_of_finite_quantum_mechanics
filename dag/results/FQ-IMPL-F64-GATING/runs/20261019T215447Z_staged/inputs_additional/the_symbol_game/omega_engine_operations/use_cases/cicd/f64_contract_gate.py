#!/usr/bin/env python3
"""Float contract gate: no new floating point in tracked Rust code.

AuthorityEffect: None. The gate reports findings; it grants no standing.

Rule (Jeremy, 2026-10-16): no ``f64`` anywhere outside a search or solver
unless it is agreed and written into a fixed contract. Searches and solvers
may use floats to propose; they never authorize a result.

The gate scans every tracked ``*.rs`` file, with comments and string or char
literals removed, and counts three kinds of float use per file:

  f64            the ``f64`` type token (``as f64``, ``f64::EPSILON``, ...)
  f32            the ``f32`` type token
  float_literal  a float literal (``0.5``, ``1e-9``, ``2.``, ``1f64``)

It compares the counts with ``f64_contract.json``, which has two parts:

  sealed       agreed float use. Each entry names a class
               (``SEARCH_OR_SOLVER`` or ``DIAGNOSTIC_ONLY``), a reason,
               ``approved_by`` and ``approved_on``. Only Jeremy adds or
               raises an entry here.
  legacy_debt  the float use that existed when the gate was introduced.
               It may only shrink.

Findings (each fails the gate):

  NEW_FLOAT          a file uses more of a kind than sealed + legacy allow.
  STALE_DEBT         legacy debt is larger than the file needs, or names a
                     file that is gone. Run ``--shrink``; it only lowers.
  CEILING_EXCEEDED   legacy debt totals exceed ``LEGACY_DEBT_CEILING``.
  DEBT_WIDENED       against ``--base``, a legacy entry is new or larger.
  SEALED_WIDENED     against ``--base``, a sealed entry is new or larger.
                     Only ``--approve-sealed-widening`` passes it, and only
                     Jeremy may give that flag.
  SEALED_MALFORMED   a sealed entry lacks its class, reason or approval.

Moved files. When a file with legacy debt is gone from the tree and a file
with no debt entry needs no more of each kind than the gone file had, the
debt follows it, provided git history confirms the move: the new file's
lines match the old file's last committed text at least
``MOVE_SIMILARITY`` of the way (``difflib`` ratio over stripped, non-blank
lines). A followed move is reported as ``MOVED`` and does not fail;
``--shrink`` re-keys the contract. Without that history (a shallow clone)
the move is not followed and the file reports ``NEW_FLOAT``. Total debt
never rises: each gone entry moves to at most one file.

Usage::

    python omega_engine_operations/use_cases/cicd/f64_contract_gate.py --repo-root . --base origin/main
    ... --report     # list every counted file
    ... --shrink     # re-key moved files, lower legacy debt to what the tree needs (never raises)

Exit status: 0 clean, 1 findings, 2 usage or contract error.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

CONTRACT_NAME = "f64_contract.json"
CONTRACT_REL = f"omega_engine_operations/use_cases/cicd/{CONTRACT_NAME}"
SCHEMA = "omega.f64_contract.v1"
KINDS: tuple[str, ...] = ("f64", "f32", "float_literal")
SEALED_CLASSES = frozenset({"SEARCH_OR_SOLVER", "DIAGNOSTIC_ONLY"})
SEALED_FIELDS = ("class", "reason", "approved_by", "approved_on", "kinds")
APPROVER = "dbccpage"
#: Legacy debt totals when the gate was introduced (2026-10-16, origin/main bef50fb2e).
#: The contract may fall below these, never rise above. Pinned by the tests.
LEGACY_DEBT_CEILING: Mapping[str, int] = {"f64": 4607, "f32": 2, "float_literal": 9030}
MAX_FILE_BYTES = 4_000_000
#: Least ``difflib`` ratio between a gone file's last text and a new file for debt to follow.
MOVE_SIMILARITY = 0.5

_TYPE_TOKEN = {kind: re.compile(rf"\b{kind}\b") for kind in ("f64", "f32")}
_DIGITS = r"\d[\d_]*"
_EXP = rf"[eE][+-]?_*{_DIGITS}"
_SUFFIX = r"(?:_*f(?:32|64))?"
_FLOAT_LITERAL = re.compile(
    rf"(?<![\w.])(?:"
    rf"{_DIGITS}\.{_DIGITS}(?:{_EXP})?{_SUFFIX}"  # 0.5  1.0e-9  2.5f32
    rf"|{_DIGITS}{_EXP}{_SUFFIX}"  # 1e-9
    rf"|{_DIGITS}_*f(?:32|64)"  # 1f64
    rf"|{_DIGITS}\.(?![\w.])"  # 2.
    rf")"
)
_RAW_STRING_START = re.compile(r'b?r(#*)"')
#: Every place a comment or literal can begin; ``_literal_end`` decides whether one does.
_LITERAL_START = re.compile(r"""//|/\*|b?r#*"|b?["']""")
_NOT_NEWLINE = re.compile(r"[^\n]")
#: A file with no match here has no float use; stripping only removes text.
_MAYBE_FLOAT = re.compile(r"f64|f32|\d[._]*[.eEf]")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    detail: str

    def line(self) -> str:
        return f"{self.code} {self.path}: {self.detail}"


class ContractError(Exception):
    """The contract file is missing or malformed."""


# --------------------------------------------------------------------------- scanning


def _skip_block_comment(src: str, i: int) -> int:
    depth, i = 1, i + 2
    while i < len(src) and depth:
        if src.startswith("/*", i):
            depth, i = depth + 1, i + 2
        elif src.startswith("*/", i):
            depth, i = depth - 1, i + 2
        else:
            i += 1
    return i


def _skip_quoted(src: str, i: int, quote: str) -> int:
    i += 1
    while i < len(src) and src[i] != quote:
        i += 2 if src[i] == "\\" else 1
    return i + 1


def _char_literal_end(src: str, i: int) -> int | None:
    """End of a char literal at ``src[i] == "'"``, or None for a lifetime or label."""
    if src.startswith("'\\", i):
        return _skip_quoted(src, i, "'")
    if i + 2 < len(src) and src[i + 2] == "'" and src[i + 1] != "'":
        return i + 3
    return None


def _literal_end(src: str, i: int) -> int | None:
    """End of the comment or literal starting at ``i``, or None if none starts there."""
    if src.startswith("//", i):
        end = src.find("\n", i)
        return len(src) if end < 0 else end
    if src.startswith("/*", i):
        return _skip_block_comment(src, i)
    prev_word = i > 0 and (src[i - 1].isalnum() or src[i - 1] == "_")
    raw = None if prev_word else _RAW_STRING_START.match(src, i)
    if raw:
        close = '"' + raw.group(1)
        end = src.find(close, raw.end())
        return len(src) if end < 0 else end + len(close)
    if src[i] == '"' or (src.startswith('b"', i) and not prev_word):
        return _skip_quoted(src, i + (src[i] == "b"), '"')
    if src[i] == "'" or (src.startswith("b'", i) and not prev_word):
        return _char_literal_end(src, i + (src[i] == "b"))
    return None


def strip_rust(src: str) -> str:
    """Blank out comments and string/char literals, keeping every newline."""
    out: list[str] = []
    i = 0
    while True:
        hit = _LITERAL_START.search(src, i)
        if hit is None:
            out.append(src[i:])
            return "".join(out)
        start = hit.start()
        end = _literal_end(src, start)
        if end is None:
            out.append(src[i : start + 1])
            i = start + 1
            continue
        out.append(src[i:start])
        out.append(_NOT_NEWLINE.sub(" ", src[start:end]))
        i = end


def count_floats(src: str) -> dict[str, list[int]]:
    """Line numbers of each float use in ``src``, by kind (only non-empty kinds)."""
    if not _MAYBE_FLOAT.search(src):
        return {}
    code = strip_rust(src)
    newlines = [m.start() for m in re.finditer("\n", code)]
    found: dict[str, list[int]] = {}
    patterns = (*_TYPE_TOKEN.items(), ("float_literal", _FLOAT_LITERAL))
    for kind, pattern in patterns:
        lines = [bisect.bisect_left(newlines, m.start()) + 1 for m in pattern.finditer(code)]
        if lines:
            found[kind] = lines
    return found


def tracked_rust_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.rs"],
        cwd=root, capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise ContractError(f"git ls-files failed: {result.stderr.decode(errors='replace').strip()}")
    return sorted(p for p in result.stdout.decode().split("\0") if p)


def scan(root: Path, files: Iterable[str]) -> dict[str, dict[str, list[int]]]:
    usage: dict[str, dict[str, list[int]]] = {}
    for rel in files:
        path = root / rel
        if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
            continue
        found = count_floats(path.read_text(encoding="utf-8", errors="replace"))
        if found:
            usage[rel] = found
    return usage


# --------------------------------------------------------------------------- contract


def load_contract_text(text: str, origin: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ContractError(f"{origin}: not JSON ({exc})") from exc
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ContractError(f"{origin}: schema is not {SCHEMA}")
    for part in ("sealed", "legacy_debt"):
        if not isinstance(data.get(part), dict):
            raise ContractError(f"{origin}: missing object {part!r}")
    for path, kinds in data["legacy_debt"].items():
        _check_kinds(kinds, f"{origin}: legacy_debt[{path}]")
    for path, entry in data["sealed"].items():
        if not isinstance(entry, dict):
            raise ContractError(f"{origin}: sealed[{path}] is not an object")
        _check_kinds(entry.get("kinds", {}), f"{origin}: sealed[{path}].kinds")
    return data


def _check_kinds(kinds: object, where: str) -> None:
    if not isinstance(kinds, dict):
        raise ContractError(f"{where} is not an object")
    for kind, count in kinds.items():
        if kind not in KINDS:
            raise ContractError(f"{where}: unknown kind {kind!r}")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise ContractError(f"{where}.{kind}: count must be a positive integer")


def load_contract(root: Path) -> dict:
    path = root / CONTRACT_REL
    if not path.is_file():
        raise ContractError(f"{CONTRACT_REL} is missing")
    return load_contract_text(path.read_text(encoding="utf-8"), CONTRACT_REL)


def base_contract(root: Path, base: str) -> dict | None:
    """The contract at the merge base of ``base`` and HEAD, or None if it did not exist."""
    merge = subprocess.run(
        ["git", "merge-base", base, "HEAD"], cwd=root, capture_output=True, text=True, check=False
    )
    if merge.returncode != 0:
        raise ContractError(f"git merge-base {base} HEAD failed: {merge.stderr.strip()}")
    show = subprocess.run(
        ["git", "cat-file", "-p", f"{merge.stdout.strip()}:{CONTRACT_REL}"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if show.returncode != 0:
        return None
    return load_contract_text(show.stdout, f"{base}:{CONTRACT_REL}")


def _sealed_kinds(contract: Mapping, path: str) -> Mapping[str, int]:
    entry = contract["sealed"].get(path)
    return entry.get("kinds", {}) if entry else {}


def _debt_totals(contract: Mapping) -> dict[str, int]:
    totals = dict.fromkeys(KINDS, 0)
    for kinds in contract["legacy_debt"].values():
        for kind, count in kinds.items():
            totals[kind] += count
    return totals


def needed_debt(contract: Mapping, usage: Mapping[str, Mapping[str, list[int]]]) -> dict:
    """Legacy debt each file needs once its sealed allowance is spent."""
    needed: dict[str, dict[str, int]] = {}
    for path, found in usage.items():
        sealed = _sealed_kinds(contract, path)
        extra = {k: len(lines) - sealed.get(k, 0) for k, lines in found.items()}
        extra = {k: n for k, n in extra.items() if n > 0}
        if extra:
            needed[path] = extra
    return needed


# --------------------------------------------------------------------------- moved files


def _git_text(root: Path, rev: str, rel: str) -> str | None:
    show = subprocess.run(
        ["git", "cat-file", "-p", f"{rev}:{rel}"], cwd=root, capture_output=True, check=False
    )
    return show.stdout.decode("utf-8", errors="replace") if show.returncode == 0 else None


def last_committed_text(root: Path, rel: str) -> str | None:
    """The text ``rel`` had in the last commit that held it, or None without that history."""
    last = subprocess.run(
        ["git", "rev-list", "-1", "HEAD", "--", rel], cwd=root, capture_output=True, text=True,
        check=False,
    )
    rev = last.stdout.strip()
    if last.returncode != 0 or not rev:
        return None
    text = _git_text(root, rev, rel)
    return text if text is not None else _git_text(root, f"{rev}^", rel)


def _lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def same_file(old_text: str, new_text: str) -> bool:
    old, new = _lines(old_text), _lines(new_text)
    if not old or not new:
        return False
    return SequenceMatcher(None, old, new, autojunk=False).ratio() >= MOVE_SIMILARITY


def git_confirms_move(root: Path) -> Callable[[str, str], bool]:
    def confirm(old: str, new: str) -> bool:
        old_text = last_committed_text(root, old)
        path = root / new
        if old_text is None or not path.is_file():
            return False
        return same_file(old_text, path.read_text(encoding="utf-8", errors="replace"))
    return confirm


def _fits(need: Mapping[str, int], debt: Mapping[str, int], exact: bool) -> bool:
    if exact:
        return dict(need) == dict(debt)
    return all(n <= debt.get(k, 0) for k, n in need.items())


def find_moves(
    contract: Mapping,
    usage: Mapping[str, Mapping[str, list[int]]],
    tracked: set[str],
    confirm: Callable[[str, str], bool],
) -> dict[str, str]:
    """Map each moved file to the gone path whose debt it takes over.

    A gone path is a legacy entry whose file is no longer tracked. A newcomer
    needs debt and has no entry. Exact count matches pair first, then a
    newcomer needing no more of each kind than the gone entry. Each gone path
    goes to at most one newcomer, so total debt is unchanged.
    """
    debt = contract["legacy_debt"]
    needed = needed_debt(contract, usage)
    gone = sorted(p for p in debt if p not in tracked)
    newcomers = sorted(p for p in needed if p not in debt)
    moves: dict[str, str] = {}
    for exact in (True, False):
        for new in newcomers:
            if new in moves:
                continue
            for old in gone:
                if _fits(needed[new], debt[old], exact) and confirm(old, new):
                    moves[new] = old
                    gone.remove(old)
                    break
    return moves


def follow_moves(contract: Mapping, moves: Mapping[str, str]) -> dict:
    """The contract with each moved file's debt filed under its new path."""
    debt = dict(contract["legacy_debt"])
    for new, old in moves.items():
        debt[new] = debt.pop(old)
    return {**contract, "legacy_debt": dict(sorted(debt.items()))}


# --------------------------------------------------------------------------- checks


def check_usage(contract: Mapping, usage: Mapping[str, Mapping[str, list[int]]]) -> list[Finding]:
    findings: list[Finding] = []
    debt = contract["legacy_debt"]
    for path, extra in needed_debt(contract, usage).items():
        allowed = debt.get(path, {})
        for kind, n in sorted(extra.items()):
            if n > allowed.get(kind, 0):
                lines = usage[path][kind]
                shown = ", ".join(map(str, lines[:12])) + (" ..." if len(lines) > 12 else "")
                findings.append(Finding(
                    "NEW_FLOAT", path,
                    f"{kind} used {len(lines)}x, contract allows "
                    f"{allowed.get(kind, 0) + _sealed_kinds(contract, path).get(kind, 0)}; lines {shown}",
                ))
    return findings


def check_stale(contract: Mapping, usage: Mapping[str, Mapping[str, list[int]]]) -> list[Finding]:
    needed = needed_debt(contract, usage)
    findings = []
    for path, kinds in sorted(contract["legacy_debt"].items()):
        for kind, count in sorted(kinds.items()):
            need = needed.get(path, {}).get(kind, 0)
            if count > need:
                findings.append(Finding(
                    "STALE_DEBT", path, f"{kind} debt {count}, tree needs {need}; run --shrink"
                ))
    return findings


def check_ceiling(contract: Mapping) -> list[Finding]:
    totals = _debt_totals(contract)
    return [
        Finding("CEILING_EXCEEDED", CONTRACT_REL,
                f"{kind} legacy debt {totals[kind]} exceeds ceiling {LEGACY_DEBT_CEILING[kind]}")
        for kind in KINDS if totals[kind] > LEGACY_DEBT_CEILING[kind]
    ]


def check_sealed_shape(contract: Mapping) -> list[Finding]:
    findings = []
    for path, entry in sorted(contract["sealed"].items()):
        missing = [f for f in SEALED_FIELDS if not entry.get(f)]
        if missing:
            findings.append(Finding("SEALED_MALFORMED", path, f"missing {', '.join(missing)}"))
        elif entry["class"] not in SEALED_CLASSES:
            findings.append(Finding("SEALED_MALFORMED", path, f"class {entry['class']!r} is not one of "
                                    f"{sorted(SEALED_CLASSES)}"))
        elif entry["approved_by"] != APPROVER:
            findings.append(Finding("SEALED_MALFORMED", path, f"approved_by must be {APPROVER}"))
    return findings


def _widened(old: Mapping[str, int], new: Mapping[str, int]) -> list[str]:
    return [f"{k} {old.get(k, 0)} -> {n}" for k, n in sorted(new.items()) if n > old.get(k, 0)]


def check_widening(old: Mapping | None, new: Mapping, approve_sealed: bool) -> list[Finding]:
    if old is None:
        return []
    findings = []
    for path, kinds in sorted(new["legacy_debt"].items()):
        grew = _widened(old["legacy_debt"].get(path, {}), kinds)
        if grew:
            findings.append(Finding("DEBT_WIDENED", path, "; ".join(grew)))
    if approve_sealed:
        return findings
    for path in sorted(new["sealed"]):
        grew = _widened(_sealed_kinds(old, path), _sealed_kinds(new, path))
        if grew:
            findings.append(Finding(
                "SEALED_WIDENED", path,
                "; ".join(grew) + " (needs Jeremy: --approve-sealed-widening)",
            ))
    return findings


def run_checks(
    root: Path, base: str | None, approve_sealed: bool
) -> tuple[list[Finding], dict, dict[str, str]]:
    tracked = tracked_rust_files(root)
    usage = scan(root, tracked)
    confirm = git_confirms_move(root)
    written = load_contract(root)
    moves = find_moves(written, usage, set(tracked), confirm)
    contract = follow_moves(written, moves)
    old = base_contract(root, base) if base else None
    if old is not None:
        old = follow_moves(old, find_moves(old, usage, set(tracked), confirm))
    findings = [
        *check_sealed_shape(contract),
        *check_usage(contract, usage),
        *check_stale(contract, usage),
        *check_ceiling(contract),
        *check_widening(old, contract, approve_sealed),
    ]
    return findings, usage, moves


# --------------------------------------------------------------------------- writing


def shrunk_contract(contract: Mapping, usage: Mapping[str, Mapping[str, list[int]]]) -> dict:
    """The contract with every legacy count lowered to need; nothing is raised or added."""
    needed = needed_debt(contract, usage)
    debt: dict[str, dict[str, int]] = {}
    for path, kinds in contract["legacy_debt"].items():
        lowered = {k: min(n, needed.get(path, {}).get(k, 0)) for k, n in kinds.items()}
        lowered = {k: n for k, n in lowered.items() if n > 0}
        if lowered:
            debt[path] = dict(sorted(lowered.items()))
    return {**contract, "legacy_debt": dict(sorted(debt.items()))}


def write_contract(root: Path, contract: Mapping) -> None:
    text = json.dumps(contract, indent=2, ensure_ascii=False) + "\n"
    (root / CONTRACT_REL).write_bytes(text.encode("utf-8"))


# --------------------------------------------------------------------------- cli


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="f64_contract_gate", description=__doc__.split("\n")[0])
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", help="compare the contract with this revision's merge base")
    parser.add_argument("--report", action="store_true", help="print the count for every file")
    parser.add_argument("--shrink", action="store_true", help="lower stale legacy debt, then check")
    parser.add_argument("--approve-sealed-widening", action="store_true",
                        help="Jeremy only: accept new or larger sealed entries")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    root = args.repo_root.resolve()
    try:
        if args.shrink:
            tracked = tracked_rust_files(root)
            usage = scan(root, tracked)
            contract = load_contract(root)
            moved = follow_moves(
                contract, find_moves(contract, usage, set(tracked), git_confirms_move(root))
            )
            write_contract(root, shrunk_contract(moved, usage))
        findings, usage, moves = run_checks(root, args.base, args.approve_sealed_widening)
        totals = _debt_totals(load_contract(root))
    except ContractError as exc:
        print(f"f64_contract_gate: CONTRACT_ERROR {exc}", file=sys.stderr)
        return 2
    if args.report:
        for path, found in sorted(usage.items()):
            print(f"  {path}: " + ", ".join(f"{k}={len(v)}" for k, v in sorted(found.items())))
    for new, old in sorted(moves.items()):
        print(f"MOVED {old} -> {new}: debt follows the file; --shrink re-keys the contract")
    for finding in findings:
        print(finding.line())
    debt = ", ".join(f"{k}={totals[k]}" for k in KINDS)
    status = "FAIL" if findings else "PASS"
    print(f"f64_contract_gate: {status}; {len(usage)} Rust files use floats; legacy debt {debt}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
