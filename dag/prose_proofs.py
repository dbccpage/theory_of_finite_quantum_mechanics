"""Prose proofs in papers/ for nodes of the derivation DAG.

A proof section is the part of a Markdown file under papers/ that starts at a line
"DAG node: `ID`" (one or more backticked node ids) and runs to the next heading or the next such
line. It must contain a paragraph opening with "*Proof.*", and every Lean reference written as
`lean4/<file>.lean::<name>` (or a `.lean` file under papers/) in it must match a declaration in this checkout. Comments, strings and fenced Markdown
examples are excluded. These lexical checks establish neither compilation nor the validity of a
mathematical argument; coverage counts only sections passing the structural checks.

A PROVED_PROSE node has a prose proof by definition (its cited source is one). A PROVED_LEAN or
COMPUTATIONALLY_CHECKED node has one when a proof section names it. Run this file to print the
coverage of PROVED_LEAN nodes and the ones still without a prose proof.

The links run both ways. A section names its nodes, and dag/prose_proofs.md lists, stage by stage,
every PROVED_LEAN node with a link "papers/<file>.md#<anchor>" to each section that proves it
(<anchor> is the GitHub anchor of the heading above the section) or "none yet". Run with
--write-index to regenerate it after a paper changes; the test fails while it is stale.
"""

from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Reuse the repository's comment-aware lexical Lean reader. This is a source
# citation check, not Lean elaboration or verification of the prose argument.
sys.path.insert(0, str(ROOT / "scripts"))
from overclaim_lean import parse_decls, strip_lean  # noqa: E402

PROOF_STATUSES = ("PROVED_LEAN", "PROVED_PROSE", "COMPUTATIONALLY_CHECKED")

_NODE_LINE = re.compile(r"^DAG nodes?: (.+)$")
_HEADING = re.compile(r"^#{1,6} ")
_TICKED = re.compile(r"`([^`]+)`")
_LEAN_REF = re.compile(r"`((?:lean4|papers)/[^`:]+\.lean)::([^`]+)`")
_DAG = Path("dag") / "derivation_dag.json"
_INDEX = Path("dag") / "prose_proofs.md"


def heading_anchor(heading: str, seen: dict[str, int]) -> str:
    """The anchor GitHub gives a Markdown heading, with -1, -2 for repeats in one file."""
    slug = re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")
    n = seen.get(slug, 0)
    seen[slug] = n + 1
    return f"{slug}-{n}" if n else slug


def load_nodes(root: Path = ROOT) -> dict[str, dict]:
    dag = json.loads((root / _DAG).read_text(encoding="utf-8"))
    return {n["id"]: n for n in dag["nodes"]}


def proof_sections(root: Path = ROOT) -> list[dict]:
    """Every proof section under papers/, with its node ids, text and location."""
    sections = []
    for path in sorted((root / "papers").rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        current = None
        fence = None
        anchor, title, seen = "", "", {}
        for lineno, line in enumerate(lines, 1):
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if fence is not None:
                if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                    fence = None
                continue
            if marker:
                fence = marker[1]
                continue
            match = _NODE_LINE.match(line)
            if match or _HEADING.match(line):
                if current:
                    sections.append(current)
                current = None
            if _HEADING.match(line):
                title = line.lstrip("#").strip()
                anchor = heading_anchor(title, seen)
            if match:
                current = {
                    "file": path.relative_to(root).as_posix(),
                    "line": lineno,
                    "anchor": anchor,
                    "title": title,
                    "ids": _TICKED.findall(match.group(1)),
                    "text": [],
                }
            elif current:
                current["text"].append(line)
        if current:
            sections.append(current)
    for s in sections:
        s["text"] = "\n".join(s["text"])
    return sections


def lean_refs(text: str) -> list[tuple[str, str]]:
    return _LEAN_REF.findall(text)


def lean_ref_resolves(root: Path, path: str, name: str) -> bool:
    file = (root / path).resolve()
    roots = (root.resolve() / "lean4", root.resolve() / "papers")
    if ".." in Path(path).parts or not any(file.is_relative_to(p) for p in roots) or not file.is_file():
        return False
    declarations = declaration_names(file.read_text(encoding="utf-8"))
    if name in declarations:
        return True
    # Historical citations may use an unqualified name or a namespace suffix.
    # Require a unique declaration, and never accept only a matching leaf of a
    # different supplied namespace.
    return sum(full.endswith("." + name) for full in declarations) == 1


@lru_cache(maxsize=128)
def declaration_names(source: str) -> tuple[str, ...]:
    return tuple(d.full for d in parse_decls(strip_lean(source)))


def section_errors(section: dict, nodes: dict[str, dict], root: Path = ROOT) -> list[str]:
    where = f"{section['file']}:{section['line']}"
    errs = []
    if not section["ids"]:
        errs.append(f"{where}: no node id on the DAG node line")
    if not re.search(r"^\*Proof\.\*(?:\s|$)", section["text"], re.M):
        errs.append(f"{where}: no *Proof.* paragraph")
    refs = lean_refs(section["text"])
    for path, name in refs:
        if not lean_ref_resolves(root, path, name):
            errs.append(f"{where}: Lean reference {path}::{name} does not resolve")
    cited = {f"{p}::{n}" for p, n in refs}
    for node_id in section["ids"]:
        node = nodes.get(node_id)
        if node is None:
            errs.append(f"{where}: unknown node {node_id}")
            continue
        if node["status"] not in PROOF_STATUSES:
            errs.append(f"{where}: {node_id} has status {node['status']}, which takes no proof")
        if node["status"] == "PROVED_LEAN" and not cited & set(node["lean"]):
            errs.append(f"{where}: cites none of the Lean declarations of {node_id}")
    return errs


def covered_ids(root: Path = ROOT, nodes: dict[str, dict] | None = None) -> set[str]:
    """Count only sections that pass the structural and citation checks."""
    if nodes is None:
        nodes = load_nodes(root)
    return {i for s in proof_sections(root) if not section_errors(s, nodes, root) for i in s["ids"]}


def section_links(root: Path = ROOT) -> dict[str, list[tuple[str, str]]]:
    """Node id -> (papers/<file>.md#<anchor>, link text) for each valid section that proves it."""
    links: dict[str, list[tuple[str, str]]] = {}
    nodes = load_nodes(root)
    for s in proof_sections(root):
        if section_errors(s, nodes, root):
            continue
        link = f"{s['file']}#{s['anchor']}" if s["anchor"] else s["file"]
        text = f"{Path(s['file']).stem}: {s['title']}" if s["title"] else Path(s["file"]).stem
        for i in s["ids"]:
            if (link, text) not in links.setdefault(i, []):
                links[i].append((link, text))
    return links


def render_index(root: Path = ROOT) -> str:
    """The Markdown index from DAG nodes to the paper sections that prove them, by stage."""
    nodes = load_nodes(root)
    links = section_links(root)
    out = [
        "# Prose proofs of DAG nodes",
        "",
        "Generated by `python3 dag/prose_proofs.py --write-index` from `derivation_dag.json` and the",
        "proof sections under `papers/`; `dag/test_prose_proofs.py` fails when it is stale. Each row",
        "links a node to the paper section that proves it in prose; that section cites the Lean",
        "declarations. A PROVED_LEAN node listed as *none yet* has a Lean proof and no written proof.",
        "PROVED_PROSE nodes are proved by their cited source and are not listed. Nodes with any other",
        "status are not claimed as proved and have no proof section.",
        "",
    ]
    stages: dict[str, list[str]] = {}
    for i, n in nodes.items():
        if n["status"] == "PROVED_LEAN" or i in links:
            stages.setdefault(n["stage"], []).append(i)
    for stage, ids in stages.items():
        done = sum(1 for i in ids if i in links)
        out += [f"## {stage}", "", f"{done} of {len(ids)} with a prose proof.", ""]
        out += ["| Node | Status | Prose proof |", "|---|---|---|"]
        for i in sorted(ids):
            cells = "; ".join(f"[{t.replace('|', '/')}](../{l})" for l, t in links.get(i, [])) or "*none yet*"
            out.append(f"| `{i}` | {nodes[i]['status']} | {cells} |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    if "--write-index" in sys.argv:
        (ROOT / _INDEX).write_text(render_index(), encoding="utf-8")
    nodes = load_nodes()
    errs = [e for s in proof_sections() for e in section_errors(s, nodes)]
    for e in errs:
        print(e)
    covered = covered_ids(nodes=nodes)
    lean = [i for i, n in nodes.items() if n["status"] == "PROVED_LEAN"]
    prose = [i for i, n in nodes.items() if n["status"] == "PROVED_PROSE"]
    missing = [i for i in lean if i not in covered]
    print(f"PROVED_PROSE nodes: {len(prose)}")
    print(f"PROVED_LEAN nodes with a valid linked prose section: {len(lean) - len(missing)} of {len(lean)}")
    if (ROOT / _INDEX).read_text(encoding="utf-8") != render_index():
        errs.append("stale index")
        print(f"{_INDEX} is stale; run with --write-index")
    if "--missing" in sys.argv:
        for i in missing:
            print(f"  {nodes[i]['stage']}\t{i}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
