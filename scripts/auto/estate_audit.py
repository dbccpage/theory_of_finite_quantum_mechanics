"""Origin: scripts/auto/estate_audit.py (adapted from the_symbol_game auto-review-skills/scripts/skills_audit.py, auto-review-agents/scripts/agents_audit.py and omega_engine_operations/use_cases/packaging/agent_skill_manifest_audit.py; the operad colour, registry and capability-slice checks are not ported because this repository has none)
Claim: audits the agent estate and the documentation a change touches: skill and agent front matter (name, description, name matching the path), relative links and cited repository paths that do not resolve, paths that exist only in the_symbol_game, authority-unsafe wording (self-certification, raising a status, automatic admission), and the provenance header of new scripts
AuthorityEffect: None
Scope Fence: a structural audit; it does not judge whether a skill is useful or a document is correct, it archives and edits nothing, and an empty result is not a review
Level: L4

Usage (from the repository root):
    python -I -X utf8 scripts/auto/estate_audit.py skills
    python -I -X utf8 scripts/auto/estate_audit.py agents
    python -I -X utf8 scripts/auto/estate_audit.py docs --changed-since origin/main
    python -I -X utf8 scripts/auto/estate_audit.py docs --paths README.md docs/overclaim
Exit status: 0 ok; 1 a finding at or above --fail-on (default HIGH); 2 usage or environment error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:  # python -I does not put the script directory on sys.path
    sys.path.insert(0, str(HERE))

from auto_common import AuditError, Finding, base_parser, changed_files, emit, in_scope, parse_front_matter, read_text, run_main, sentences, tracked_files  # noqa: E402

TOOL = "estate_audit"
SKILL_GLOBS = (".claude/skills/*/SKILL.md", ".agents/skills/*/SKILL.md")
AGENT_GLOBS = (".claude/agents/*.md", ".agents/agents/*.md")
BRIEF_GLOB = ".agents/teamwork/*/BRIEFING.md"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
DESCRIPTION_RANGE = (40, 1024)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_PATH = re.compile(r"`((?:scripts|dag|docs|checks|code|lean4|evidence|papers|\.claude|\.agents|\.github)/[^`\s]+)`")
PLACEHOLDER = re.compile(r"[<>*{}$]|\.\.\.")
FOREIGN = re.compile(r"omega_engine_operads/|omega_engine_operations/|omega_engine_epistemic_immune_system|omega_engine_woland"
                     r"|_intelligence/|\booutwire\b|\.codex/|\.grok/|\bomega_engine/")
FOREIGN_EXEMPT = re.compile(r"the_symbol_game|Adapted from|Origin:", re.IGNORECASE)
UNSAFE = re.compile(r"self-certif\w*|approves? (?:its|their|your) own|final (?:authority|enforcement)|waives? (?:the )?evidence"
                    r"|raises? (?:a|the|any) status|promotes? (?:a|the) (?:status|node)|admitted automatically|auto-admit\w*"
                    r"|without (?:human )?review|mark\w* (?:it|them|the node) (?:as )?PROVED", re.IGNORECASE)
NEGATED = re.compile(r"\b(?:never|not|no|cannot|must not|do not|does not|refuse\w*|forbid\w*|without asking|flag\w*|reject\w*"
                     r"|check\w* for|detect\w*|hunt\w*|look for|catch\w*|audit\w*)\b|n't\b", re.IGNORECASE)
FENCE = re.compile(r"^[ \t]*(```|~~~).*?(?:^[ \t]*\1[^\n]*$|\Z)", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
MENTION = re.compile(r"`[^`\n]*`|\"[^\"\n]*\"")  # quoted or backticked text is a mention of a phrase, not a use
HEADER_FIELDS = ("Origin:", "Claim:", "AuthorityEffect:", "Scope Fence:")
HEADER_SCOPES = ("scripts/auto/",)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def blank(pattern: re.Pattern, text: str) -> str:
    """Replace each match with spaces, keeping newlines, so offsets and line numbers still hold."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def link_findings(root: Path, rel: str, text: str) -> list[Finding]:
    """Relative markdown links and backticked repository paths that do not resolve (fenced code is not read)."""
    found: list[Finding] = []
    folder = (root / rel).parent
    text = blank(FENCE, text)
    for match in LINK.finditer(blank(INLINE_CODE, text)):
        target = match.group(1).split("#", 1)[0]
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE) or PLACEHOLDER.search(target):
            continue
        if not (folder / target).exists() and not (root / target.lstrip("/")).exists():
            found.append(Finding("BROKEN_LINK", "MEDIUM", rel, _line_of(text, match.start()), f"relative link {target} does not resolve"))
    for match in CODE_PATH.finditer(text):
        target = match.group(1).rstrip(".,;:")
        if PLACEHOLDER.search(target) or (root / target).exists():
            continue
        found.append(Finding("MISSING_PATH", "LOW", rel, _line_of(text, match.start()), f"cited path {target} does not exist"))
    return found


def wording_findings(rel: str, text: str) -> list[Finding]:
    """the_symbol_game-only paths, and authority-unsafe wording outside negated sentences."""
    found: list[Finding] = []
    for number, line in enumerate(text.splitlines(), 1):
        if FOREIGN.search(line) and not FOREIGN_EXEMPT.search(line):
            found.append(Finding("FOREIGN_PATH", "HIGH", rel, number, "names a path that exists only in the_symbol_game", FOREIGN.search(line).group(0)))
        for sentence in sentences(MENTION.sub(lambda m: " " * len(m.group(0)), line)):
            hit = UNSAFE.search(sentence)
            if hit and not NEGATED.search(sentence[: hit.start()]):
                found.append(Finding("AUTHORITY_UNSAFE", "MEDIUM", rel, number, f"authority-unsafe wording `{hit.group(0)}`", sentence[:120]))
    return found


def manifest_findings(rel: str, text: str, expected_name: str, kind: str) -> list[Finding]:
    meta, body, error = parse_front_matter(text)
    if meta is None:
        return [Finding("INVALID_FRONT_MATTER", "HIGH", rel, 1, error)]
    found: list[Finding] = []
    name, description = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not name:
        found.append(Finding("MISSING_FIELD", "HIGH", rel, 1, "front matter has no name"))
    elif name != expected_name:
        found.append(Finding("NAME_PATH_MISMATCH", "HIGH", rel, 1, f"name {name!r} differs from {kind} path {expected_name!r}"))
    elif not NAME_RE.match(name):
        found.append(Finding("NAME_FORMAT", "MEDIUM", rel, 1, "name must be lowercase letters, digits and hyphens, at most 64 characters"))
    if not isinstance(description, str) or not description.strip():
        found.append(Finding("MISSING_FIELD", "HIGH", rel, 1, "front matter has no description"))
    elif not DESCRIPTION_RANGE[0] <= len(description) <= DESCRIPTION_RANGE[1]:
        found.append(Finding("DESCRIPTION_LENGTH", "MEDIUM", rel, 1,
                             f"description has {len(description)} characters; allowed {DESCRIPTION_RANGE[0]} to {DESCRIPTION_RANGE[1]}"))
    if kind == "skill" and not re.search(r"^## \S", body, re.MULTILINE):
        found.append(Finding("NO_SECTIONS", "LOW", rel, 1, "body has no level-2 section"))
    return found


def audit_document(root: Path, rel: str, kind: str) -> list[Finding]:
    text = read_text(root, rel)
    if text is None:
        return [Finding("UNREADABLE", "HIGH", rel, 0, "file is not readable UTF-8")]
    found = link_findings(root, rel, text) + wording_findings(rel, text)
    if kind == "skill":
        found += manifest_findings(rel, text, rel.split("/")[-2], kind)
    elif kind == "agent":
        found += manifest_findings(rel, text, Path(rel).stem, kind)
    return found


def header_findings(root: Path, rel: str) -> list[Finding]:
    text = read_text(root, rel) or ""
    head = text[:2000]
    missing = [field for field in HEADER_FIELDS if field not in head]
    if not missing:
        return []
    return [Finding("MISSING_HEADER", "LOW", rel, 1, f"script docstring lacks {', '.join(missing)}")]


def estate_files(root: Path, patterns: tuple[str, ...]) -> list[str]:
    """Filesystem glob, not git: .claude/ is gitignored, so a skill that is not yet force-added is still audited."""
    return sorted({p.relative_to(root).as_posix() for pattern in patterns for p in root.glob(pattern) if p.is_file()})


def audit_skills(root: Path) -> tuple[list[Finding], str]:
    files = estate_files(root, SKILL_GLOBS)
    found: list[Finding] = []
    for rel in files:
        found.extend(audit_document(root, rel, "skill"))
        folder = rel.rsplit("/", 1)[0]
        for extra in estate_files(root, (f"{folder}/*.md", f"{folder}/references/*.md")):
            if extra != rel:
                found.extend(audit_document(root, extra, "reference"))
    return found, f"{len(files)} skills"


def audit_agents(root: Path) -> tuple[list[Finding], str]:
    agents = estate_files(root, AGENT_GLOBS)
    briefs = estate_files(root, (BRIEF_GLOB,))
    found: list[Finding] = []
    for rel in agents:
        found.extend(audit_document(root, rel, "agent"))
    for rel in briefs:
        found.extend(wording_findings(rel, read_text(root, rel) or ""))
    return found, f"{len(agents)} agent definitions, {len(briefs)} teamwork briefs"


def audit_docs(root: Path, ref: str | None, paths: list[str]) -> tuple[list[Finding], str]:
    if paths:
        targets = sorted({rel for path in paths for rel in _expand(root, path)})
        scope = f"{len(targets)} files under {', '.join(paths)}"
    elif ref:
        targets = [rel for rel in changed_files(root, ref) if in_scope(rel)]
        scope = f"{len(targets)} files changed since {ref}"
    else:
        targets = [rel for rel in tracked_files(root, ("*.md", "*.py")) if in_scope(rel)]
        scope = f"whole checkout, {len(targets)} .md/.py files"
    found: list[Finding] = []
    for rel in targets:
        if rel.endswith(".md"):
            text = read_text(root, rel)
            if text is None:
                found.append(Finding("UNREADABLE", "LOW", rel, 0, "file is not readable UTF-8; links not checked"))
            else:
                found.extend(link_findings(root, rel, text))
        elif rel.endswith(".py") and rel.startswith(HEADER_SCOPES):
            found.extend(header_findings(root, rel))
    return found, scope


def _expand(root: Path, path: str) -> list[str]:
    target = (root / path).resolve()
    if target.is_file():
        return [target.relative_to(root).as_posix()]
    if target.is_dir():
        return [p.relative_to(root).as_posix() for p in sorted(target.rglob("*")) if p.suffix in (".md", ".py") and p.is_file()]
    raise AuditError(f"{path} does not exist")


def main(argv: list[str] | None = None) -> int:
    parser = base_parser(__doc__.splitlines()[1])
    parser.add_argument("target", choices=("skills", "agents", "docs"))
    parser.add_argument("--paths", nargs="*", default=[], help="docs only: files or directories to audit instead of the changed set")
    args = parser.parse_args(argv)

    def body() -> int:
        root = args.repo_root.resolve()
        if not (root / ".git").exists():
            raise AuditError(f"{root} is not a git checkout")
        if args.target == "skills":
            findings, scope = audit_skills(root)
        elif args.target == "agents":
            findings, scope = audit_agents(root)
        else:
            findings, scope = audit_docs(root, args.changed_since, args.paths)
        return emit(TOOL, f"Estate audit: {args.target}", findings, args, scope)

    return run_main(TOOL, body)


if __name__ == "__main__":
    sys.exit(main())
