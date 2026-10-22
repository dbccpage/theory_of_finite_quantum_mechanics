"""Origin: scripts/overclaim_scan.py
Claim: a deterministic, offline scan of the derivation DAG, its cited Lean modules, its replay receipts and the public prose finds the mechanical signs of an overclaim: a status without checkable evidence, a Lean module with an admission, a receipt that no longer matches its source, a node described as proved that is not, promotional wording
AuthorityEffect: None
Scope Fence: this file does not decide whether a node statement is the theorem its Lean declaration proves; a finding is a prompt for the statement-vs-theorem review in .claude/skills/overclaim-hunter/SKILL.md, and an empty report is not evidence that nothing is overclaimed
Level: L5

No network, no model call, no Lean build. Reads derivation_dag.json, the Lean/Rust/Python files it cites,
dag/research/*lean_replay*.json, dag/derivations/**.md, README.md, docs/**, papers/**.

Usage (from the repository root):
    python -I -X utf8 scripts/overclaim_scan.py                      # print the summary
    python -I -X utf8 scripts/overclaim_scan.py --write              # write docs/overclaim/report.{md,json}
    python -I -X utf8 scripts/overclaim_scan.py --check              # exit 1 if the committed report is stale
    python -I -X utf8 scripts/overclaim_scan.py --write-baseline     # write docs/overclaim/baseline.json
    python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict
Exit status: 0 ok; 1 stale report (--check) or a new HIGH finding (--strict); 2 usage or environment error.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent

# --------------------------------------------------------------------------------------------
# Constants (edit here, not in the rules).

SEVERITIES = ("HIGH", "MEDIUM", "LOW")
SEV_ORDER = {name: index for index, name in enumerate(SEVERITIES)}

# The axioms a replay receipt may list (R4) and the Lean tokens that void a PROVED_LEAN/CONDITIONAL module (R3).
ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
LEAN_ADMISSION_TOKENS = ("sorry", "admit", "native_decide", "unsafe")

# Statuses a prose sentence may call proved/derived without a finding (R6), and the ones that carry a proof claim.
PROVED_STATUSES = ("PROVED_LEAN", "PROVED_PROSE", "COMPUTATIONALLY_CHECKED")
CLAIM_STATUSES = ("PROVED_LEAN", "PROVED_PROSE", "COMPUTATIONALLY_CHECKED", "CONDITIONAL")

# Absolute or promotional wording in public prose (R7). Case-insensitive, whole phrase.
PROMOTIONAL_PHRASES = (
    "derives quantum mechanics",
    "derive quantum mechanics",
    "derived quantum mechanics",
    "derives qm",
    "complete derivation",
    "first ever",
    "first-ever",
    "revolutionary",
    "proves qm",
    "proves quantum mechanics",
    "fully derived",
    "fully proved",
    "fully proven",
    "completely derived",
    "no assumptions",
    "without any assumptions",
    "assumption-free",
    "theory of everything",
    "groundbreaking",
    "paradigm shift",
    "unprecedented",
)
# Text before a phrase in the same sentence that makes it a quoted negation or a list of banned words, not a claim.
NEGATION_BEFORE = re.compile(
    r"\b(not|no|never|no claim|cannot|neither|nor|nothing|rather than|avoid\w*|forbid\w*|forbidden|refus\w*|den(?:y|ies)|"
    r"disclaim\w*|overclaim\w*|promotional|banned|reject\w*)\b|n't\b",
    re.IGNORECASE,
)
NEGATION_FOLLOW = re.compile(r"^\W*(beyond|other than|except|apart from|besides|but)\b", re.IGNORECASE)

# Prose that calls a node proved/derived (R6) and the hedges that make a sentence not such a claim.
PROOF_VERBS = re.compile(r"\b(proves?|proved|proven|derives?|derived|establish(?:es|ed)|shows? that)\b", re.IGNORECASE)
HEDGES = re.compile(
    r"\b(not|no|never|cannot|nor|neither|without|yet|unproved|unproven|if|whether|would|could|should|might|may|"
    r"aims?|goal|target|attempts?|candidate|proposed?|expected|hope\w*|want\w*|until|unless)\b|n't\b",
    re.IGNORECASE,
)
# Generated boilerplate that says "derived" about a record's parent link, not about a result.
BOILERPLATE_DERIVED = re.compile(r"derived from (?:parent|the parent)", re.IGNORECASE)
# A preceding line that sets up a list of non-claims.
CONTEXT_NEGATION = re.compile(
    r"\b(not|never)\s+(claim|assert|establish|show|prove|derive|imply|mean)\w*|\bnon-?claims?\b|\bno claim\b|\bnot claimed\b|\bdisclaim\w*|\bcannot be claimed\b",
    re.IGNORECASE,
)

# Wording of a node statement that claims generality (R2).
UNIVERSAL_WORDING = re.compile(
    r"\b(every|all|for any|for all|for each|unique|uniquely|iff|if and only if)\b|\bno\b[^.;]{0,80}\bexist|\bthere is no\b",
    re.IGNORECASE,
)

R8_AI_LINE = "Status: AI-drafted, awaiting human review."
R8_REVIEWED = re.compile(r"^Status: Reviewed by [^,]+, \d{4}-\d{2}-\d{2}\.$")

PROSE_ROOTS_R6 = ("README.md", "docs", "papers", "dag/derivations")
PROSE_ROOTS_R7 = ("README.md", "PROJECT.md", "SCORING.md", "TOP_5_DIFFICULT_DERIVATIONS.md", "docs", "papers", "dag/derivations")
SKIP_DIRS = ("docs/overclaim/", ".lake/", "node_modules/", ".git/")

RULES = {
    "R1": ("HIGH", "PROVED_LEAN node without a Lean reference that resolves in this checkout"),
    "R2": ("MEDIUM", "PROVED_LEAN node whose Lean declarations look like an instance, not the stated generality"),
    "R3": ("HIGH", "sorry, admit, axiom, native_decide or unsafe in a Lean module cited by a PROVED_LEAN or CONDITIONAL node"),
    "R4": ("HIGH", "replay receipt whose sha256 differs from the file, or whose axioms exceed the allowed three"),
    "R5": ("LOW", "number in a node statement, derivation note or README found in none of the node's cited files"),
    "R6": ("HIGH", "public prose calls a node proved or derived when its DAG status is not a proved status"),
    "R7": ("MEDIUM", "absolute or promotional wording in public prose"),
    "R8": ("MEDIUM", "independent derivation note without the required Status line"),
    "R9": ("HIGH", "status rose versus the git ref with no new resolving Lean reference and replay receipt in the diff"),
    "R10": ("LOW", "PROVED_LEAN node whose cited Lean modules appear in no replay receipt"),
}
ACTIONS = {
    "R1": "Run the statement-vs-theorem review; if no Lean declaration in this checkout states it, lower the status (propose OPEN or the status the evidence supports).",
    "R2": "Read the cited declaration: if it proves one closed instance, narrow the statement to the instance and move the general claim to the bottleneck.",
    "R3": "Remove the admission and replay, or lower every node that cites the module.",
    "R4": "Rebuild and re-pin the receipt, or lower the nodes it supports; a non-standard axiom voids the proof claim.",
    "R5": "Recompute the number (exact arithmetic) from the cited file or an independent check; correct or delete it.",
    "R6": "Reword the sentence to the node's DAG status, or lower nothing: the status is the source of truth.",
    "R7": "Replace with a scoped, checkable statement; see README 'does not claim to derive quantum mechanics'.",
    "R8": "Make the first line exactly the AI-drafted line, or the reviewed line naming a human and an ISO date.",
    "R9": "Add the resolving Lean reference and the replay receipt in the same PR, or revert the status; then do the statement-vs-theorem review.",
    "R10": "Replay the module and add a receipt, or accept that the compile evidence lives outside this repository.",
}

SELF_REPORT = "docs/overclaim/report.md"
SELF_JSON = "docs/overclaim/report.json"
SELF_BASELINE = "docs/overclaim/baseline.json"


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    subject: str  # node id, or a repository-relative file path
    line: int  # 0 when not line based
    evidence: str
    action: str
    key: str  # stable identity for the baseline; contains no line number
    nodes: tuple[str, ...] = field(default=(), compare=False)  # scoping only; not reported
    files: tuple[str, ...] = field(default=(), compare=False)

    def sort_key(self) -> tuple[int, str, str, int, str]:
        return (SEV_ORDER[self.severity], self.rule, self.subject, self.line, self.key)

    def as_dict(self) -> dict[str, object]:
        return {
            "severity": self.severity,
            "rule": self.rule,
            "subject": self.subject,
            "line": self.line,
            "evidence": self.evidence,
            "action": self.action,
            "key": self.key,
        }


def short(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def make(rule: str, subject: str, evidence: str, key_detail: str, *, line: int = 0, severity: str | None = None,
         nodes: tuple[str, ...] = (), files: tuple[str, ...] = ()) -> Finding:
    sev = severity or RULES[rule][0]
    return Finding(sev, rule, subject, line, short(evidence), ACTIONS[rule], f"{rule}|{subject}|{key_detail}", nodes, files)


# --------------------------------------------------------------------------------------------
# Repository access.


def load_validator(root: Path):
    """Reuse the DAG validator's reference helpers; they are read from the root being scanned when it has them."""
    for base in (root, DEFAULT_ROOT):
        dag_dir = base / "dag"
        if (dag_dir / "validate_derivation_dag.py").is_file():
            if str(dag_dir) not in sys.path:
                sys.path.insert(0, str(dag_dir))
            return importlib.import_module("validate_derivation_dag")
    raise SystemExit("overclaim_scan: dag/validate_derivation_dag.py not found")


class Repo:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.v = load_validator(self.root)
        self._text: dict[str, str | None] = {}
        self._tokens: dict[str, frozenset[str]] = {}
        dag_path = self.root / "dag" / "derivation_dag.json"
        self.dag: dict = json.loads(dag_path.read_text(encoding="utf-8")) if dag_path.is_file() else {}
        self.nodes: dict[str, dict] = {n["id"]: n for n in self.dag.get("nodes", []) if isinstance(n, dict) and "id" in n}
        self.records: list[dict] = [r for r in self.dag.get("records", []) if isinstance(r, dict)]

    def text(self, rel: str) -> str | None:
        """File text with CRLF folded to LF, or None when it is not a readable file."""
        if rel not in self._text:
            path = self.root / rel
            try:
                data = path.read_bytes() if path.is_file() else None
            except OSError:
                data = None
            self._text[rel] = None if data is None else data.replace(b"\r\n", b"\n").decode("utf-8", errors="replace")
        return self._text[rel]

    def raw_sha(self, rel: str) -> tuple[str, str] | None:
        path = self.root / rel
        if not path.is_file():
            return None
        data = path.read_bytes()
        return hashlib.sha256(data).hexdigest(), hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()

    def files(self, roots: tuple[str, ...], suffix: str = ".md") -> list[str]:
        out: set[str] = set()
        for entry in roots:
            base = self.root / entry
            if base.is_file():
                out.add(entry)
            elif base.is_dir():
                for path in base.rglob("*" + suffix):
                    rel = path.relative_to(self.root).as_posix()
                    if path.is_file() and not any(rel.startswith(s) or ("/" + s) in rel for s in SKIP_DIRS):
                        out.add(rel)
        return sorted(out)

    def refs(self, node: dict, field_name: str) -> list[str]:
        value = node.get(field_name)
        return [r for r in value if isinstance(r, str)] if isinstance(value, list) else []

    def lean_resolution(self, node: dict) -> tuple[list[str], list[str]]:
        """(resolving refs, unresolved refs) of a node's lean field, by the validator's own symbol check."""
        good: list[str] = []
        bad: list[str] = []
        for ref in self.refs(node, "lean"):
            if self.v.is_external(ref):
                continue
            if self.v._symbol_errors(self.root, node.get("id"), "lean", ref):
                bad.append(ref)
            else:
                good.append(ref)
        return good, bad


# --------------------------------------------------------------------------------------------
# Lean text handling.


def strip_lean(src: str) -> str:
    """Blank comments, string literals and character literals, keeping every newline (so line numbers hold)."""
    out: list[str] = []
    i, n, depth = 0, len(src), 0
    while i < n:
        c = src[i]
        if depth > 0:
            if src.startswith("/-", i):
                depth += 1
                out.append("  ")
                i += 2
            elif src.startswith("-/", i):
                depth -= 1
                out.append("  ")
                i += 2
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
            continue
        if src.startswith("/-", i):
            depth = 1
            out.append("  ")
            i += 2
            continue
        if src.startswith("--", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
            continue
        if c == "'" and (i == 0 or not (src[i - 1].isalnum() or src[i - 1] in "_'.")):
            m = re.match(r"'(\\.|[^\\'\n])'", src[i : i + 4])
            if m:
                out.append(" " * len(m.group(0)))
                i += len(m.group(0))
                continue
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            seg = src[i + 1 : j]
            out.append('"' + "".join("\n" if ch == "\n" else " " for ch in seg) + '"')
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


DECL_START = re.compile(
    r"^(?:@\[[^\]\n]*\]\s*)*(?:(?:private|protected|noncomputable|partial|unsafe|nonrec)\s+)*"
    r"(theorem|lemma|def|abbrev|instance|example|structure|inductive|class|opaque|axiom)\b[ \t]*([^\s:({\[⦃]*)"
)
BOUNDARY = re.compile(
    r"^(?:@\[|theorem\b|lemma\b|def\b|abbrev\b|instance\b|example\b|structure\b|inductive\b|class\b|opaque\b|axiom\b|namespace\b|"
    r"end\b|section\b|open\b|variable\b|universe\b|#|private\b|protected\b|noncomputable\b|partial\b|unsafe\b|set_option\b|"
    r"attribute\b|import\b|macro\b|syntax\b|notation\b|local\b|scoped\b|mutual\b|deriving\b)"
)
NAMESPACE = re.compile(r"^namespace\s+(\S+)")
SECTION = re.compile(r"^section\b")
END = re.compile(r"^end\b(?:\s+(\S+))?")
TRIVIAL_TACTIC = re.compile(
    r"^(decide(\s*\+\w+)?|decide!|rfl|exact rfl|exact by decide|exact decide|norm_num(\s*\[[^\]]*\])?|simp|native_decide|trivial)$"
)


@dataclass
class Decl:
    kind: str
    name: str  # as written
    full: str  # with namespaces
    line: int
    header: str  # between the name and ':=' (binders and type)
    body: str  # after ':='

    def binders_and_type(self) -> tuple[str, str]:
        depth = 0
        for index, ch in enumerate(self.header):
            if ch in "([{⟨⦃":
                depth += 1
            elif ch in ")]}⟩⦄":
                depth -= 1
            elif ch == ":" and depth == 0:
                return self.header[:index], self.header[index + 1 :]
        return self.header, ""

    def is_general(self) -> bool:
        binders, typ = self.binders_and_type()
        return bool(re.search(r"[\(\{\[⦃]", binders)) or bool(re.search(r"∀|Π|\bforall\b", typ))

    def type_is_true(self) -> bool:
        return self.binders_and_type()[1].strip() == "True"

    def trivial_closed(self) -> bool:
        if self.is_general() or not self.body.strip():
            return False
        body = self.body.strip()
        if body.startswith("by"):
            body = body[2:]
        parts = [p.strip() for p in re.split(r"[\n;]|<;>", body) if p.strip()]
        return bool(parts) and all(TRIVIAL_TACTIC.match(p) for p in parts)


def parse_decls(stripped: str) -> list[Decl]:
    lines = stripped.split("\n")
    ns: list[str] = []
    stack: list[str | None] = []
    decls: list[Decl] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = NAMESPACE.match(line)
        if m:
            ns.extend(m.group(1).split("."))
            stack.append(m.group(1))
        elif SECTION.match(line):
            stack.append(None)
        else:
            m = END.match(line)
            if m and stack:
                top = stack.pop()
                if top is not None:
                    del ns[len(ns) - len(top.split(".")) :]
        d = DECL_START.match(line)
        if d:
            j = i + 1
            while j < len(lines) and not BOUNDARY.match(lines[j]):
                j += 1
            block = "\n".join(lines[i:j])
            head_end = d.end()
            rest = block[head_end:]
            cut = _top_level_assign(rest)
            header, body = (rest[:cut], rest[cut + 2 :]) if cut >= 0 else (rest, "")
            name = d.group(2)
            full = name[len("_root_.") :] if name.startswith("_root_.") else ".".join([*ns, name] if name else ns)
            decls.append(Decl(d.group(1), name, full, i + 1, header, body))
            i = j
            continue
        i += 1
    return decls


def _top_level_assign(text: str) -> int:
    depth = 0
    for index, ch in enumerate(text):
        if ch in "([{⟨⦃":
            depth += 1
        elif ch in ")]}⟩⦄":
            depth -= 1
        elif ch == ":" and depth == 0 and text[index : index + 2] == ":=":
            return index
    return -1


def find_decl(decls: list[Decl], symbol: str) -> Decl | None:
    leaf = symbol.split(".")[-1]
    for pred in (
        lambda d: d.full == symbol,
        lambda d: d.full.endswith("." + symbol) or d.name == symbol,
        lambda d: d.full.split(".")[-1] == leaf,
    ):
        for d in decls:
            if pred(d):
                return d
    return None


# --------------------------------------------------------------------------------------------
# Receipts.


@dataclass
class Receipt:
    path: str
    data: dict | None
    entries: list[dict]


def load_receipts(repo: Repo) -> list[Receipt]:
    out: list[Receipt] = []
    base = repo.root / "dag" / "research"
    if not base.is_dir():
        return out
    for path in sorted(base.glob("*lean_replay*.json")):
        rel = path.relative_to(repo.root).as_posix()
        try:
            data = json.loads(repo.text(rel) or "")
        except json.JSONDecodeError:
            out.append(Receipt(rel, None, []))
            continue
        results = []
        if isinstance(data, dict):
            replay = data.get("lean_replay")
            results = (replay.get("results") if isinstance(replay, dict) else None) or data.get("results") or []
        out.append(Receipt(rel, data if isinstance(data, dict) else None, [e for e in results if isinstance(e, dict)]))
    return out


# --------------------------------------------------------------------------------------------
# Rules.


def rule_r1(repo: Repo) -> list[Finding]:
    out: list[Finding] = []
    for node_id, node in sorted(repo.nodes.items()):
        if node.get("status") != "PROVED_LEAN":
            continue
        good, bad = repo.lean_resolution(node)
        if good:
            continue
        if not bad:
            why = "no lean reference"
        else:
            tops = sorted({r.split("/")[0] for r in bad})
            absent = [t for t in tops if not (repo.root / t).exists()]
            why = "atlas-only (not in this checkout: " + ", ".join(absent) + ")" if absent and len(absent) == len(tops) else "cited path or symbol missing"
        out.append(make("R1", node_id, f"{why}; refs: {'; '.join(bad[:2]) or 'none'}", why.split(" ")[0], nodes=(node_id,)))
    return out


def rule_r2(repo: Repo) -> list[Finding]:
    out: list[Finding] = []
    for node_id, node in sorted(repo.nodes.items()):
        if node.get("status") != "PROVED_LEAN":
            continue
        universal = bool(UNIVERSAL_WORDING.search(str(node.get("statement", ""))))
        found: list[Decl] = []
        by_ref: dict[str, str] = {}
        for ref in repo.refs(node, "lean"):
            path, _, symbol = ref.partition("::")
            if not symbol or repo.v.is_external(ref):
                continue
            text = repo.text(path)
            if text is None:
                continue
            decl = find_decl(parse_decls(strip_lean(text)), symbol)
            if decl and decl.kind in ("theorem", "lemma", "example"):
                found.append(decl)
                by_ref[decl.full] = f"{path}:{decl.line}"
        if not found:
            continue
        true_typed = [d for d in found if d.type_is_true()]
        trivial = [d for d in found if d.trivial_closed()]
        all_closed = all(not d.is_general() for d in found)
        reasons: list[str] = []
        if true_typed:
            reasons.append("type True: " + ", ".join(d.name for d in true_typed[:3]))
        if universal and all_closed:
            reasons.append("statement uses universal wording but every cited theorem is closed (no binder, no forall)")
        if trivial:
            reasons.append("proof is only decide/rfl/norm_num on a closed instance: " + ", ".join(d.name for d in trivial[:3]))
        if not reasons:
            continue
        where = by_ref.get((true_typed or trivial or found)[0].full, "")
        paths = tuple(sorted({v.split(":")[0] for v in by_ref.values()}))
        out.append(make("R2", node_id, "; ".join(reasons) + f" [{where}]" + (" [universal wording: yes]" if universal else " [universal wording: no]"),
                        digest("|".join(reasons)), nodes=(node_id,), files=paths))
    return out


def rule_r3(repo: Repo) -> list[Finding]:
    cited: dict[str, set[str]] = defaultdict(set)
    for node_id, node in repo.nodes.items():
        if node.get("status") in ("PROVED_LEAN", "CONDITIONAL"):
            for ref in repo.refs(node, "lean"):
                path = ref.partition("::")[0]
                if not repo.v.is_external(ref) and path.endswith(".lean"):
                    cited[path].add(node_id)
    out: list[Finding] = []
    for path in sorted(cited):
        text = repo.text(path)
        if text is None:
            continue
        stripped = strip_lean(text)
        seen: set[tuple[str, int]] = set()
        patterns = [(tok, re.compile(r"(?<![\w.])" + tok + r"(?![\w'])")) for tok in LEAN_ADMISSION_TOKENS]
        patterns.append(("axiom", re.compile(r"^(?:@\[[^\]\n]*\]\s*)*(?:(?:private|protected|noncomputable)\s+)*axiom\b", re.MULTILINE)))
        for tok, pat in patterns:
            for m in pat.finditer(stripped):
                lineno = stripped.count("\n", 0, m.start()) + 1
                if (tok, lineno) in seen:
                    continue
                before = stripped[stripped.rfind("\n", 0, m.start()) + 1 : m.start()].rstrip()
                if before.endswith("|"):  # a constructor or match-arm name, not the tactic
                    continue
                seen.add((tok, lineno))
                src_line = text.split("\n")[lineno - 1]
                nodes = tuple(sorted(cited[path]))
                out.append(make("R3", path, f"`{tok}` at line {lineno}: {src_line.strip()} (cited by {', '.join(nodes[:4])}{' ...' if len(nodes) > 4 else ''})",
                                f"{tok}|{digest(src_line.strip())}", line=lineno, nodes=nodes, files=(path,)))
    return out


def rule_r4(repo: Repo, receipts: list[Receipt]) -> list[Finding]:
    out: list[Finding] = []
    for rc in receipts:
        if rc.data is None:
            out.append(make("R4", rc.path, "receipt is not parseable JSON", "unparseable", files=(rc.path,)))
            continue
        for entry in rc.entries:
            source = str(entry.get("source", ""))
            recorded = str(entry.get("sha256", ""))
            module = str(entry.get("module", source))
            node = str(entry.get("dag_node", ""))
            nodes = (node,) if node in repo.nodes else ()
            shas = repo.raw_sha(source) if source else None
            if source and shas is None:
                out.append(make("R4", rc.path, f"{module}: recorded source {source} does not exist", f"{module}|missing", nodes=nodes, files=(rc.path,)))
            elif shas is not None and recorded not in shas:
                out.append(make("R4", rc.path, f"{module}: recorded sha256 {recorded[:12]} but {source} is now {shas[1][:12]}", f"{module}|sha", nodes=nodes, files=(rc.path, source)))
            bad: dict[str, list[str]] = defaultdict(list)
            axioms = entry.get("axioms")
            if isinstance(axioms, dict):
                for decl, listed in axioms.items():
                    for ax in listed if isinstance(listed, list) else []:
                        if ax not in ALLOWED_AXIOMS:
                            bad[str(ax)].append(str(decl))
            if bad:
                text = "; ".join(f"{ax} in {', '.join(sorted(ds)[:2])}" for ax, ds in sorted(bad.items()))
                out.append(make("R4", rc.path, f"{module}: axioms beyond the allowed three: {text}", f"{module}|axioms|{'|'.join(sorted(bad))}", nodes=nodes, files=(rc.path,)))
    return out


# ---- R5: numbers -------------------------------------------------------------------------

NUM_RE = re.compile(r"(?<![\w./-])(?<![A-Za-z]-)(\d+/\d+|\d+(?:,\d{3})*(?:\.\d+)?)(?![\w/])")
TOKEN_RE = re.compile(r"\d+(?:_\d+)*(?:\.\d+)?")
NOISE_RES = (
    re.compile(r"https?://\S+"),
    re.compile(r"\]\([^)]*\)"),
    re.compile(r"\b\d{4}-\d{2}-\d{2}(?:T[\d:.]+Z?)?\b"),
    re.compile(r"`[^`\n]*(?:\.(?:lean|rs|py|md|json|yaml|txt)|::)[^`\n]*`"),
    re.compile(r"[\w./-]+\.(?:lean|rs|py|md|json|yaml|txt)(?::\d+(?:[-,]\d+)*)?(?:#\S*)?"),
    re.compile(r"(?:PR|pull request|issue)s?\s*#?\d+|#\d+"),
    re.compile(r"^\s*\d+[.)]\s", re.MULTILINE),
    re.compile(r"\bUUID\b[^\n]*"),
)


def prose_numbers(text: str) -> list[str]:
    for pat in NOISE_RES:
        text = pat.sub(" ", text)
    seen: dict[str, None] = {}
    for m in NUM_RE.finditer(text):
        raw = m.group(1)
        norm = raw.replace(",", "")
        if "/" in norm:
            if len(norm.replace("/", "")) >= 2 and not re.fullmatch(r"\d/\d", norm):
                seen[norm] = None
        elif len(norm.replace(".", "")) >= 2:
            seen[norm] = None
    return list(seen)


def file_tokens(repo: Repo, rel: str) -> frozenset[str]:
    if rel not in repo._tokens:
        text = repo.text(rel) or ""
        repo._tokens[rel] = frozenset(t.replace("_", "") for t in TOKEN_RE.findall(text))
    return repo._tokens[rel]


def node_evidence_files(repo: Repo, node_id: str, receipts: list[Receipt], record_map: dict[str, list[dict]]) -> list[str]:
    node = repo.nodes[node_id]
    cands: list[str] = []
    for ref in repo.refs(node, "lean") + repo.refs(node, "rust"):
        if not repo.v.is_external(ref):
            cands.append(ref.partition("::")[0])
    for ref in repo.refs(node, "source"):
        if not repo.v.is_external(ref):
            p = repo.v.line_ref_path(ref)
            if p.endswith((".lean", ".rs", ".py", ".json")):
                cands.append(p)
    for rec in record_map.get(node_id, []):
        for fld in ("lean4", "python", "rust"):
            for ref in rec.get(fld, []) if isinstance(rec.get(fld), list) else []:
                if isinstance(ref, str) and not repo.v.is_external(ref):
                    cands.append(ref.partition("::")[0])
    cands.append(f"checks/independent/{node_id.lower()}.py")
    return sorted({c for c in cands if repo.text(c) is not None})


def receipt_tokens(receipts: list[Receipt], node_id: str, files: set[str]) -> frozenset[str]:
    toks: set[str] = set()
    for rc in receipts:
        for entry in rc.entries:
            if entry.get("dag_node") == node_id or entry.get("source") in files:
                body = {k: v for k, v in entry.items() if k != "output"}
                toks.update(t.replace("_", "") for t in TOKEN_RE.findall(json.dumps(body)))
    return frozenset(toks)


def build_record_map(repo: Repo) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for rec in repo.records:
        for nid in rec.get("existing_derivation_dag_ids", []) if isinstance(rec.get("existing_derivation_dag_ids"), list) else []:
            out[nid].append(rec)
    return out


def missing_numbers(repo: Repo, receipts: list[Receipt], record_map: dict[str, list[dict]], node_ids: list[str], numbers: list[str]) -> list[str]:
    toks: set[str] = set()
    for nid in node_ids:
        files = node_evidence_files(repo, nid, receipts, record_map)
        for f in files:
            toks |= file_tokens(repo, f)
        toks |= receipt_tokens(receipts, nid, set(files))
    out = []
    for n in numbers:
        if "/" in n:
            a, b = n.split("/")
            if a in toks and b in toks:
                continue
        elif n in toks:
            continue
        out.append(n)
    return out


def rule_r5(repo: Repo, receipts: list[Receipt]) -> list[Finding]:
    record_map = build_record_map(repo)
    out: list[Finding] = []
    for node_id, node in sorted(repo.nodes.items()):
        if node.get("status") not in CLAIM_STATUSES:
            continue
        nums = prose_numbers(str(node.get("statement", "")))
        miss = missing_numbers(repo, receipts, record_map, [node_id], nums)
        if miss:
            out.append(make("R5", node_id, f"statement: {len(miss)} of {len(nums)} numbers in no cited file: {', '.join(miss[:8])}", "statement|" + digest(",".join(miss)), nodes=(node_id,)))
    rec_nodes = {r.get("id"): [n for n in r.get("existing_derivation_dag_ids", []) if n in repo.nodes] for r in repo.records}
    lower = {n.lower(): n for n in repo.nodes}
    for rel in repo.files(("dag/derivations",)):
        stem = Path(rel).stem
        m = re.match(r"tfq_(\d{4})_", stem)
        ids = rec_nodes.get("TFQ-" + m.group(1), []) if m else ([lower[stem.lower()]] if stem.lower() in lower else [])
        ids = [i for i in ids if repo.nodes[i].get("status") in CLAIM_STATUSES]
        if not ids:
            continue
        nums = prose_numbers(repo.text(rel) or "")
        miss = missing_numbers(repo, receipts, record_map, ids, nums)
        if miss:
            out.append(make("R5", rel, f"note for {', '.join(ids[:3])}: {len(miss)} of {len(nums)} numbers in no cited file: {', '.join(miss[:8])}", "note|" + digest(",".join(miss)), nodes=tuple(ids), files=(rel,)))
    if repo.text("README.md") is not None:
        id_re = node_id_regex(repo)
        for lineno, line in enumerate((repo.text("README.md") or "").split("\n"), 1):
            ids = sorted({m.group(1) for m in id_re.finditer(line)}) if id_re else []
            ids = [i for i in ids if repo.nodes[i].get("status") in CLAIM_STATUSES]
            if not ids:
                continue
            nums = prose_numbers(re.sub(r"`[^`]*`", " ", line))
            miss = missing_numbers(repo, receipts, record_map, ids, nums)
            if miss:
                out.append(make("R5", "README.md", f"line mentions {', '.join(ids[:3])}: numbers in no cited file: {', '.join(miss[:8])}", "readme|" + digest(line), line=lineno, nodes=tuple(ids), files=("README.md",)))
    return out


# ---- R6, R7: prose ---------------------------------------------------------------------


def node_id_regex(repo: Repo):
    ids = sorted(repo.nodes, key=lambda s: (-len(s), s))
    if not ids:
        return None
    return re.compile(r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(i) for i in ids) + r")(?![A-Za-z0-9_-])")


def sentences(line: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?;])\s+|\s\|\s", line) if s.strip()]


def rule_r6(repo: Repo) -> list[Finding]:
    id_re = node_id_regex(repo)
    out: list[Finding] = []
    if id_re is None:
        return out
    for rel in repo.files(PROSE_ROOTS_R6):
        text = repo.text(rel) or ""
        for lineno, line in enumerate(text.split("\n"), 1):
            if not PROOF_VERBS.search(line):
                continue
            for sent in sentences(line):
                bare = id_re.sub(" ID ", sent)  # node ids contain words such as NO, OPEN or PROVES
                if not PROOF_VERBS.search(bare) or HEDGES.search(bare) or BOILERPLATE_DERIVED.search(bare):
                    continue
                for m in id_re.finditer(sent):
                    nid = m.group(1)
                    status = str(repo.nodes[nid].get("status"))
                    if status in PROVED_STATUSES or re.search(r"\b" + status + r"\b", bare):
                        continue
                    out.append(make("R6", rel, f"{nid} is {status} but the text says: {short(sent, 160)}", f"{nid}|{digest(sent.strip())}",
                                    line=lineno, nodes=(nid,), files=(rel,)))
    return out


def rule_r7(repo: Repo) -> list[Finding]:
    pats = [(p, re.compile(r"\b" + re.escape(p) + r"\b", re.IGNORECASE)) for p in PROMOTIONAL_PHRASES]
    out: list[Finding] = []
    for rel in repo.files(PROSE_ROOTS_R7):
        all_lines = (repo.text(rel) or "").split("\n")
        for lineno, line in enumerate(all_lines, 1):
            low = line.lower()
            if not any(p in low for p in PROMOTIONAL_PHRASES):
                continue
            context = [line]  # the paragraph above, at most four lines, may set up a list of non-claims
            back = lineno - 2
            while back >= 0 and len(context) < 5 and all_lines[back].strip():
                context.append(all_lines[back])
                back -= 1
            if CONTEXT_NEGATION.search(" ".join(context)):
                continue
            for sent in sentences(line):
                for phrase, pat in pats:
                    m = pat.search(sent)
                    if not m:
                        continue
                    if NEGATION_BEFORE.search(sent[: m.start()]) or NEGATION_FOLLOW.match(sent[m.end() :]):
                        continue
                    out.append(make("R7", rel, f"\"{phrase}\": {short(sent, 160)}", f"{phrase}|{digest(sent.strip())}", line=lineno, files=(rel,)))
    return out


def rule_r8(repo: Repo) -> list[Finding]:
    out: list[Finding] = []
    for rel in repo.files(("dag/derivations/independent",)):
        text = (repo.text(rel) or "").lstrip("\ufeff")
        first = text.split("\n", 1)[0].strip()
        if first != R8_AI_LINE and not R8_REVIEWED.match(first):
            out.append(make("R8", rel, f"first line is {short(first, 100)!r}", "first-line", line=1, files=(rel,)))
    return out


def rule_r10(repo: Repo, receipts: list[Receipt]) -> list[Finding]:
    covered = {str(e.get("source")) for rc in receipts for e in rc.entries}
    out: list[Finding] = []
    for node_id, node in sorted(repo.nodes.items()):
        if node.get("status") != "PROVED_LEAN":
            continue
        good, _ = repo.lean_resolution(node)
        mods = sorted({g.partition("::")[0] for g in good if g.partition("::")[0].endswith(".lean")})
        if mods and not any(m in covered for m in mods):
            out.append(make("R10", node_id, f"{len(mods)} cited Lean module(s) in no replay receipt, e.g. {mods[0]}", "no-receipt", nodes=(node_id,)))
    return out


# ---- R9: status rise versus a git ref --------------------------------------------------


def git(root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    if proc.returncode != 0 and check:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout.decode("utf-8", errors="replace")


@dataclass
class Diff:
    base: str
    changed_files: set[str]
    base_nodes: dict[str, dict]


def load_diff(root: Path, ref: str) -> Diff:
    try:
        base = git(root, "merge-base", ref, "HEAD").strip() or ref
    except RuntimeError:
        base = ref
    names = git(root, "diff", "--name-only", "--no-renames", base).split("\n")
    names += git(root, "ls-files", "--others", "--exclude-standard").split("\n")
    changed = {n.strip() for n in names if n.strip()}
    try:
        raw = git(root, "show", f"{base}:dag/derivation_dag.json")
        base_nodes = {n["id"]: n for n in json.loads(raw).get("nodes", []) if isinstance(n, dict) and "id" in n}
    except (RuntimeError, json.JSONDecodeError):
        base_nodes = {}
    return Diff(base, changed, base_nodes)


def rule_r9(repo: Repo, receipts: list[Receipt], diff: Diff) -> list[Finding]:
    rank = repo.v.PFP_STATUS_RANK
    changed_receipts = [rc for rc in receipts if rc.path in diff.changed_files]
    out: list[Finding] = []
    for node_id, node in sorted(repo.nodes.items()):
        cur = str(node.get("status"))
        before = diff.base_nodes.get(node_id)
        if before is None:
            rose = cur in PROVED_STATUSES
            prev = "(new node)"
        else:
            prev = str(before.get("status"))
            rose = prev in rank and cur in rank and rank[cur] > rank[prev]
        if not rose:
            continue
        old_lean = set(repo.refs(before, "lean")) if before else set()
        good, _ = repo.lean_resolution(node)
        new_lean = [g for g in good if g not in old_lean]
        mods = {g.partition("::")[0] for g in good}
        has_receipt = any(e.get("dag_node") == node_id or e.get("source") in mods for rc in changed_receipts for e in rc.entries)
        has_check = f"checks/independent/{node_id.lower()}.py" in diff.changed_files and cur == "COMPUTATIONALLY_CHECKED"
        if (new_lean and has_receipt) or has_check:
            continue
        lacks = []
        if not new_lean:
            lacks.append("no new resolving Lean reference")
        if not has_receipt:
            lacks.append("no replay receipt for it in the diff")
        out.append(make("R9", node_id, f"status {prev} -> {cur}; " + " and ".join(lacks), f"{prev}->{cur}", nodes=(node_id,)))
    return out


# --------------------------------------------------------------------------------------------
# Driver.


def scan(root: Path, diff: Diff | None = None) -> list[Finding]:
    repo = Repo(root)
    receipts = load_receipts(repo)
    found: list[Finding] = []
    found += rule_r1(repo)
    found += rule_r2(repo)
    found += rule_r3(repo)
    found += rule_r4(repo, receipts)
    found += rule_r5(repo, receipts)
    found += rule_r6(repo)
    found += rule_r7(repo)
    found += rule_r8(repo)
    found += rule_r10(repo, receipts)
    if diff is not None:
        found += rule_r9(repo, receipts, diff)
        found = restrict(repo, found, diff)
    return sorted(set(found), key=Finding.sort_key)


def restrict(repo: Repo, found: list[Finding], diff: Diff) -> list[Finding]:
    """Keep findings about nodes or files the diff touches."""
    affected: set[str] = set()
    for node_id, node in repo.nodes.items():
        if diff.base_nodes.get(node_id) != node:
            affected.add(node_id)
            continue
        paths = {r.partition("::")[0] for f in ("lean", "rust") for r in repo.refs(node, f)}
        paths |= {repo.v.line_ref_path(r) for r in repo.refs(node, "source")}
        if paths & diff.changed_files:
            affected.add(node_id)
    return [f for f in found if set(f.nodes) & affected or set(f.files) & diff.changed_files
            or (f.rule in ("R1", "R2", "R5", "R10", "R9") and f.subject in affected)]


def counts(findings: list[Finding]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {rule: {s: 0 for s in SEVERITIES} for rule in RULES}
    for f in findings:
        out[f.rule][f.severity] += 1
    return out


def md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_json(findings: list[Finding]) -> str:
    c = counts(findings)
    doc = {
        "schema": "overclaim_report.v1",
        "authority_effect": "None",
        "rules": {r: {"severity": RULES[r][0], "title": RULES[r][1]} for r in RULES},
        "counts": c,
        "totals": {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES},
        "findings": [f.as_dict() for f in findings],
    }
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


LOW_SHOWN = 15


def render_md(findings: list[Finding], *, scope: str = "whole checkout") -> str:
    c = counts(findings)
    totals = {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES}
    lines = [
        "# Overclaim scan",
        "",
        "**AuthorityEffect:** None.",
        "",
        "Generated by `python -I -X utf8 scripts/overclaim_scan.py --write`. Do not edit by hand. Offline and deterministic: no network, no model call, no Lean build.",
        "A finding is a prompt for a statement-vs-theorem review (`.claude/skills/overclaim-hunter/SKILL.md`), not a verdict. An empty cell is not evidence that nothing is overclaimed: the scanner cannot read what a Lean statement means.",
        "",
        f"Scope: {scope}. HIGH {totals['HIGH']}, MEDIUM {totals['MEDIUM']}, LOW {totals['LOW']}.",
        "",
        "## Counts by rule",
        "",
        "| Rule | Severity | What | HIGH | MEDIUM | LOW |",
        "|---|---|---|---|---|---|",
    ]
    for rule, (sev, title) in RULES.items():
        row = c[rule]
        lines.append(f"| {rule} | {sev} | {md_cell(title)} | {row['HIGH']} | {row['MEDIUM']} | {row['LOW']} |")
    for sev in ("HIGH", "MEDIUM"):
        rows = [f for f in findings if f.severity == sev]
        lines += ["", f"## {sev} findings ({len(rows)})", ""]
        if not rows:
            lines.append("None.")
            continue
        lines += ["| Rule | Subject | Evidence |", "|---|---|---|"]
        for f in rows:
            where = f.subject + (f":{f.line}" if f.line else "")
            lines.append(f"| {f.rule} | `{md_cell(where)}` | {md_cell(f.evidence)} |")
    low = [f for f in findings if f.severity == "LOW"]
    lines += ["", f"## LOW findings ({len(low)})", "", f"Listed in full in `report.json`; the first {LOW_SHOWN} of each rule are shown here.", ""]
    for rule in RULES:
        rows = [f for f in low if f.rule == rule]
        if not rows:
            continue
        lines += [f"### {rule} ({len(rows)})", "", "| Subject | Evidence |", "|---|---|"]
        for f in rows[:LOW_SHOWN]:
            where = f.subject + (f":{f.line}" if f.line else "")
            lines.append(f"| `{md_cell(where)}` | {md_cell(f.evidence)} |")
        lines.append("")
    lines += ["## Suggested action by rule", ""]
    lines += [f"- {rule}: {ACTIONS[rule]}" for rule in RULES]
    return "\n".join(lines).rstrip("\n") + "\n"


def baseline_doc(findings: list[Finding]) -> str:
    high = [f for f in findings if f.severity == "HIGH"]
    doc = {
        "schema": "overclaim_baseline.v1",
        "authority_effect": "None",
        "note": "HIGH findings present when the baseline was written. --strict fails only on a HIGH finding whose key is not listed here. Removing an entry is always safe; adding one needs a reason in the PR.",
        "high": [{"key": f.key, "rule": f.rule, "subject": f.subject} for f in high],
    }
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def load_baseline(path: Path) -> set[str]:
    try:
        return {row["key"] for row in json.loads(path.read_text(encoding="utf-8")).get("high", [])}
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return set()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def summary_md(findings: list[Finding], new_high: list[Finding], scope: str) -> str:
    totals = {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES}
    lines = ["## Overclaim scan", "", f"Scope: {scope}. HIGH {totals['HIGH']}, MEDIUM {totals['MEDIUM']}, LOW {totals['LOW']}.", ""]
    if new_high:
        lines += [f"**{len(new_high)} NEW HIGH finding(s) (not in docs/overclaim/baseline.json) - this check fails.**", "", "| Rule | Subject | Evidence |", "|---|---|---|"]
        lines += [f"| {f.rule} | `{md_cell(f.subject)}{':' + str(f.line) if f.line else ''}` | {md_cell(f.evidence)} |" for f in new_high]
    else:
        lines.append("No new HIGH findings.")
    rest = [f for f in findings if f.severity in ("HIGH", "MEDIUM") and f not in new_high]
    if rest:
        lines += ["", f"<details><summary>{len(rest)} other HIGH/MEDIUM finding(s) in scope</summary>", "", "| Sev | Rule | Subject | Evidence |", "|---|---|---|---|"]
        lines += [f"| {f.severity} | {f.rule} | `{md_cell(f.subject)}{':' + str(f.line) if f.line else ''}` | {md_cell(f.evidence)} |" for f in rest[:200]]
        lines += ["", "</details>"]
    lines += ["", "Every node whose status or statement changed still needs the statement-vs-theorem review in `.claude/skills/overclaim-hunter/SKILL.md`.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else None)
    ap.add_argument("--repo-root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--write", action="store_true", help="write docs/overclaim/report.md and report.json")
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed report is stale")
    ap.add_argument("--write-baseline", action="store_true", help="write docs/overclaim/baseline.json from the current HIGH findings")
    ap.add_argument("--changed-since", metavar="REF", help="restrict to nodes and files changed since REF (merge base) and add rule R9")
    ap.add_argument("--strict", action="store_true", help="exit 1 if a HIGH finding is not in docs/overclaim/baseline.json")
    ap.add_argument("--baseline", type=Path, help="baseline file (default docs/overclaim/baseline.json)")
    ap.add_argument("--summary", type=Path, help="append a markdown summary to this file (for $GITHUB_STEP_SUMMARY)")
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    if (args.write or args.check or args.write_baseline) and args.changed_since:
        print("overclaim_scan: --write, --check and --write-baseline use the whole checkout; drop --changed-since", file=sys.stderr)
        return 2
    diff = None
    if args.changed_since:
        try:
            diff = load_diff(root, args.changed_since)
        except (RuntimeError, OSError) as error:
            print(f"overclaim_scan: {error}", file=sys.stderr)
            return 2
    findings = scan(root, diff)
    scope = "whole checkout" if diff is None else f"changes since {args.changed_since} (merge base {diff.base[:12]})"
    status = 0
    if args.write:
        write_text(root / SELF_REPORT, render_md(findings))
        write_text(root / SELF_JSON, render_json(findings))
        print(f"wrote {SELF_REPORT} and {SELF_JSON}")
    if args.write_baseline:
        write_text(root / SELF_BASELINE, baseline_doc(findings))
        print(f"wrote {SELF_BASELINE}")
    if args.check:
        for rel, want in ((SELF_REPORT, render_md(findings)), (SELF_JSON, render_json(findings))):
            have = (root / rel).read_bytes().replace(b"\r\n", b"\n").decode("utf-8") if (root / rel).is_file() else None
            if have != want:
                print(f"{rel} is stale; run: python -I -X utf8 scripts/overclaim_scan.py --write")
                status = 1
    totals = {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES}
    print(f"overclaim_scan: scope={scope}; HIGH={totals['HIGH']} MEDIUM={totals['MEDIUM']} LOW={totals['LOW']}")
    base_path = args.baseline or (root / SELF_BASELINE)
    known = load_baseline(base_path)
    new_high = [f for f in findings if f.severity == "HIGH" and f.key not in known]
    if args.strict or diff is not None:
        for f in new_high:
            print(f"NEW HIGH {f.rule} {f.subject}{':' + str(f.line) if f.line else ''}: {f.evidence}")
        if args.strict and new_high:
            status = 1
    if args.summary:
        with open(args.summary, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(summary_md(findings, new_high, scope))
    return status


if __name__ == "__main__":
    sys.exit(main())
