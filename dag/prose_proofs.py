"""Prose proofs in papers/ for nodes of the derivation DAG.

A proof section is the part of a Markdown file under papers/ that starts at a line
"DAG node: `ID`" (one or more backticked node ids) and runs to the next heading or the next such
line. It must contain a paragraph opening with "*Proof.*", and every Lean reference written as
`lean4/<file>.lean::<name>` in it must resolve in this checkout.

A PROVED_PROSE node has a prose proof by definition (its cited source is one). A PROVED_LEAN or
COMPUTATIONALLY_CHECKED node has one when a proof section names it. Run this file to print the
coverage of PROVED_LEAN nodes and the ones still without a prose proof.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROOF_STATUSES = ("PROVED_LEAN", "PROVED_PROSE", "COMPUTATIONALLY_CHECKED")

_NODE_LINE = re.compile(r"^DAG nodes?: (.+)$")
_HEADING = re.compile(r"^#{1,6} ")
_TICKED = re.compile(r"`([^`]+)`")
_LEAN_REF = re.compile(r"`(lean4/[^`:]+\.lean)::([^`]+)`")


def load_nodes(root: Path = ROOT) -> dict[str, dict]:
    dag = json.loads((root / "dag" / "derivation_dag.json").read_text(encoding="utf-8"))
    return {n["id"]: n for n in dag["nodes"]}


def proof_sections(root: Path = ROOT) -> list[dict]:
    """Every proof section under papers/, with its node ids, text and location."""
    sections = []
    for path in sorted((root / "papers").rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        current = None
        for lineno, line in enumerate(lines, 1):
            match = _NODE_LINE.match(line)
            if match or _HEADING.match(line):
                if current:
                    sections.append(current)
                current = None
            if match:
                current = {
                    "file": path.relative_to(root).as_posix(),
                    "line": lineno,
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
    file = root / path
    return file.is_file() and name.split(".")[-1] in file.read_text(encoding="utf-8", errors="replace")


def section_errors(section: dict, nodes: dict[str, dict], root: Path = ROOT) -> list[str]:
    where = f"{section['file']}:{section['line']}"
    errs = []
    if not section["ids"]:
        errs.append(f"{where}: no node id on the DAG node line")
    if "*Proof.*" not in section["text"]:
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


def covered_ids(root: Path = ROOT) -> set[str]:
    return {i for s in proof_sections(root) for i in s["ids"]}


def main() -> int:
    nodes = load_nodes()
    errs = [e for s in proof_sections() for e in section_errors(s, nodes)]
    for e in errs:
        print(e)
    covered = covered_ids()
    lean = [i for i, n in nodes.items() if n["status"] == "PROVED_LEAN"]
    prose = [i for i, n in nodes.items() if n["status"] == "PROVED_PROSE"]
    missing = [i for i in lean if i not in covered]
    print(f"PROVED_PROSE nodes: {len(prose)}")
    print(f"PROVED_LEAN nodes with a prose proof: {len(lean) - len(missing)} of {len(lean)}")
    if "--missing" in sys.argv:
        for i in missing:
            print(f"  {nodes[i]['stage']}\t{i}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
