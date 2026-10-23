"""Origin: scripts/overclaim_lean.py
Claim: a small reader for Lean 4 source blanks comments and strings, lists top-level declarations with their binders and type, and finds the declaration a DAG reference names
AuthorityEffect: None
Scope Fence: this file does not elaborate Lean; it is a lexical approximation used by scripts/overclaim_scan.py to ask whether a cited theorem has binders or a universal quantifier
Level: L5
"""

from __future__ import annotations

import re
from dataclasses import dataclass

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

@dataclass
class Decl:
    kind: str
    name: str  # as written
    full: str  # with namespaces
    line: int
    header: str  # between the name and ':=' (binders and type)

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
            header = rest[:cut] if cut >= 0 else rest
            name = d.group(2)
            full = name[len("_root_.") :] if name.startswith("_root_.") else ".".join([*ns, name] if name else ns)
            decls.append(Decl(d.group(1), name, full, i + 1, header))
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
