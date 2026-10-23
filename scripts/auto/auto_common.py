"""Origin: scripts/auto/auto_common.py (ported and reduced from the_symbol_game auto-* skill scripts)
Claim: shared helpers for the scripts/auto scanners: the repository root, git file lists and added-line sets, one Finding record, YAML front-matter parsing, sentence splitting and report rendering
AuthorityEffect: None
Scope Fence: helpers only; nothing here reads a DAG status as evidence, decides whether a claim is proved, or writes outside the paths a caller names
Level: L4

Standard library plus PyYAML. Every git call is read-only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[2]
SEVERITIES = ("HIGH", "MEDIUM", "LOW")
SEV_RANK = {name: index for index, name in enumerate(SEVERITIES)}
FAIL_CHOICES = ("HIGH", "MEDIUM", "LOW", "none")
EXIT_OK, EXIT_FINDINGS, EXIT_ENV = 0, 1, 2

# Sealed model-output snapshots and vendored trees are data, not code or prose under review (the exclusions of
# scripts/score_scope_contracts.py and the draft governance/policy.json).
EXCLUDED_PREFIXES = ("dag/results/", "dag/sealed_runs/", "sealed_runs/", "atlas/")
EXCLUDED_PARTS = frozenset({".lake", "target", "node_modules", "__pycache__"})
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
SENTENCE_END = re.compile(r"(?<=[.!?;])\s+(?=[A-Z`*(\"'])")


class AuditError(Exception):
    """An environment or input problem that stops a scan (exit status 2), never a finding."""


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    path: str
    line: int
    message: str
    detail: str = ""

    def __post_init__(self) -> None:
        if self.severity not in SEV_RANK:
            raise AuditError(f"unknown severity {self.severity!r}")

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        tail = f" ({self.detail})" if self.detail else ""
        return f"[{self.severity}] {self.rule} {where}: {self.message}{tail}"


def git(root: Path, *args: str) -> str:
    """Run a read-only git command in root and return stdout; raise AuditError on failure."""
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as error:
        raise AuditError(f"git is not available: {error}") from error
    if done.returncode != 0:
        raise AuditError(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout


def in_scope(rel: str) -> bool:
    """False for sealed run snapshots, atlas/ and build or cache directories."""
    return not rel.startswith(EXCLUDED_PREFIXES) and not EXCLUDED_PARTS.intersection(rel.split("/"))


def _split_z(text: str) -> list[str]:
    return [item.replace("\\", "/") for item in text.split("\0") if item]


def tracked_files(root: Path, patterns: Sequence[str] = (), untracked: bool = False) -> list[str]:
    """Files in the git index (plus untracked, not ignored, files when asked), repository-relative and sorted.

    Untracked listing walks the whole working tree, which is slow on large Windows checkouts; changed_files
    already adds untracked files for --changed-since runs.
    """
    extra = ("--others", "--exclude-standard") if untracked else ()
    out = git(root, "ls-files", "--cached", *extra, "-z", "--", *patterns)
    return sorted({name for name in _split_z(out) if (root / name).is_file()})


def merge_base(root: Path, ref: str) -> str:
    return git(root, "merge-base", ref, "HEAD").strip()


def changed_files(root: Path, ref: str) -> list[str]:
    """Files added, copied, modified or renamed since the merge base with ref (working tree included), plus untracked files."""
    base = merge_base(root, ref)
    names = set(_split_z(git(root, "diff", "--name-only", "--diff-filter=ACMR", "-z", base)))
    names.update(_split_z(git(root, "ls-files", "--others", "--exclude-standard", "-z")))
    return sorted(name for name in names if (root / name).is_file())


def added_lines(root: Path, ref: str, rel: str) -> set[int]:
    """Line numbers (1-based, in the current file) added since the merge base; every line for a file new to git."""
    base = merge_base(root, ref)
    if not git(root, "ls-files", "--", rel).strip() or not git(root, "ls-tree", "--name-only", base, "--", rel).strip():
        text = read_text(root, rel)
        return set(range(1, len(text.splitlines()) + 1)) if text is not None else set()
    lines: set[int] = set()
    for row in git(root, "diff", "-U0", base, "--", rel).splitlines():
        match = HUNK.match(row)
        if match:
            start = int(match.group(1))
            count = 1 if match.group(2) is None else int(match.group(2))
            lines.update(range(start, start + count))
    return lines


def show_at(root: Path, ref: str, rel: str) -> str | None:
    """File content at a commit, or None when the path did not exist there."""
    try:
        return git(root, "show", f"{ref}:{rel}")
    except AuditError:
        return None


def read_text(root: Path, rel: str) -> str | None:
    try:
        return (root / rel).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def parse_front_matter(text: str) -> tuple[dict | None, str, str]:
    """Return (mapping, body, error). error is empty on success; mapping is None when absent or invalid."""
    import yaml  # PyYAML; imported here so modules that never parse front matter do not need it

    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return None, normalized, "no opening front-matter delimiter"
    end = normalized.find("\n---", 4)
    if end < 0:
        return None, normalized, "no closing front-matter delimiter"
    try:
        data = yaml.safe_load(normalized[4:end])
    except yaml.YAMLError as error:
        return None, normalized, f"front matter is not valid YAML: {error}"
    if not isinstance(data, dict):
        return None, normalized, "front matter is not a mapping"
    return data, normalized[end + 4 :], ""


def sentences(text: str) -> list[str]:
    """Split one line or paragraph into sentences; a heuristic, good enough for prompts."""
    return [part.strip() for part in SENTENCE_END.split(text) if part.strip()]


def sort_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(set(findings), key=lambda f: (SEV_RANK[f.severity], f.rule, f.path, f.line, f.message))


def counts(findings: Sequence[Finding]) -> dict[str, int]:
    return {sev: sum(1 for f in findings if f.severity == sev) for sev in SEVERITIES}


def exit_status(findings: Sequence[Finding], fail_on: str) -> int:
    if fail_on == "none":
        return EXIT_OK
    limit = SEV_RANK[fail_on]
    return EXIT_FINDINGS if any(SEV_RANK[f.severity] <= limit for f in findings) else EXIT_OK


def render_markdown(title: str, findings: Sequence[Finding], scope: str, limit: int = 200) -> str:
    tally = counts(findings)
    head = [f"## {title}", "", f"Scope: {scope}. Findings: " + ", ".join(f"{tally[s]} {s}" for s in SEVERITIES) + ".", ""]
    if not findings:
        return "\n".join(head + ["No findings. An empty scan is not a review.", ""])
    rows = ["| Sev | Rule | Where | Finding |", "|---|---|---|---|"]
    for item in findings[:limit]:
        where = f"{item.path}:{item.line}" if item.line else item.path
        text = (item.message + (f" ({item.detail})" if item.detail else "")).replace("|", "\\|")
        rows.append(f"| {item.severity} | {item.rule} | `{where}` | {text} |")
    more = [f"", f"{len(findings) - limit} more findings not shown."] if len(findings) > limit else []
    return "\n".join(head + rows + more + [""])


def render_json(tool: str, findings: Sequence[Finding], scope: str) -> str:
    doc = {"tool": tool, "AuthorityEffect": "None", "scope": scope, "counts": counts(findings),
           "findings": [asdict(f) for f in findings]}
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--changed-since", metavar="REF", help="restrict to files changed since the merge base with REF")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    parser.add_argument("--summary", type=Path, help="append a markdown summary to this file (for $GITHUB_STEP_SUMMARY)")
    parser.add_argument("--fail-on", choices=FAIL_CHOICES, default="HIGH",
                        help="exit 1 if a finding at or above this severity exists (default HIGH; 'none' never fails)")
    return parser


def emit(tool: str, title: str, findings: Sequence[Finding], args: argparse.Namespace, scope: str) -> int:
    """Print the findings, append the optional summary, and return the exit status."""
    ordered = sort_findings(findings)
    if args.json:
        print(render_json(tool, ordered, scope), end="")
    else:
        for item in ordered:
            print(item.render())
        tally = counts(ordered)
        print(f"{tool}: " + ", ".join(f"{tally[s]} {s}" for s in SEVERITIES) + f" ({scope})")
    if args.summary:
        try:
            with args.summary.open("a", encoding="utf-8") as handle:
                handle.write(render_markdown(title, ordered, scope))
        except OSError as error:
            raise AuditError(f"cannot write summary {args.summary}: {error}") from error
    return exit_status(ordered, args.fail_on)


def run_main(tool: str, body) -> int:
    """Wrap a scanner main: AuditError becomes exit status 2 with one message on stderr."""
    import sys

    try:
        return body()
    except AuditError as error:
        print(f"{tool}: error: {error}", file=sys.stderr)
        return EXIT_ENV
