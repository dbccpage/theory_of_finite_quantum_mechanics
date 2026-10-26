"""Offline citation custody: exact Git blobs and local manuscript references.

The saved source inventory is the trust root for upstream Git identities.
These checks establish byte custody and readable destinations, not that a
citation supports a mathematical claim or that its owner authorized publication.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from audit_source import AuditFailure, load_contract, regular_file, relative_path

ROOT = Path(__file__).resolve().parents[1]


def verify_origin(data: bytes, record: dict[str, Any], origin: dict[str, Any] | None = None) -> None:
    """Check current bytes, including line endings, against their origin."""
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if (len(data) != record["bytes"] or blob != record["git_blob_sha1"]
            or hashlib.sha256(data).hexdigest() != record["sha256"]):
        raise AuditFailure(f"source byte identity mismatch: {record['path']}")
    if origin is not None and (blob != origin["git_blob_sha1"]
                               or len(data) != origin["size_bytes"]):
        raise AuditFailure(f"source differs from pinned Git inventory: {record['path']}")
    data.decode("utf-8")


def check_references(root: Path, manuscript: str, sources: set[str]) -> int:
    """Require local destinations and valid source-line anchors, without network."""
    definitions: dict[str, str] = {}
    for name, target in re.findall(r"^\[([^\]\n]+)\]:\s+(\S+)\s*$", manuscript, re.MULTILINE):
        name = name.casefold()
        if name in definitions:
            raise AuditFailure(f"duplicate reference definition: {name}")
        definitions[name] = target
    for label, name in re.findall(r"\[([^\]\n]+)\]\[([^\]\n]*)\]", manuscript):
        if (name or label).casefold() not in definitions:
            raise AuditFailure(f"undefined reference: {name or label}")
    targets = list(definitions.values())
    targets += re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", manuscript)
    for target in targets:
        if ":" in target or target.startswith("//"):
            raise AuditFailure(f"manuscript reference requires external access: {target}")
        name, _, anchor = target.partition("#")
        if not name:
            raise AuditFailure("empty citation destination")
        path = regular_file(root, relative_path(name))
        if anchor.startswith("L"):
            match = re.fullmatch(r"L([1-9][0-9]*)(?:-L([1-9][0-9]*))?", anchor)
            if match is None or not 1 <= int(match[1]) <= int(match[2] or match[1]) <= len(
                    path.read_text(encoding="utf-8").splitlines()):
                raise AuditFailure(f"invalid source line anchor: {target}")
        if name.startswith(("docs/sources/", "code/derivation/", "lean4/Derivation/",
                            "lean4/SecondRun/")) and name not in sources:
            raise AuditFailure(f"citation has no pinned source record: {name}")
    return len(targets)


def check_sources(root: Path = ROOT) -> dict[str, int]:
    contract, inventory = load_contract(root / "manifests/source_inventory.json")
    mechanism = json.loads((root / "manifests/mechanization_sources.json").read_text(encoding="utf-8"))
    citations = json.loads((root / "manifests/cited_sources.json").read_text(encoding="utf-8"))
    if (mechanism["source_commit"] != contract["source_commit"]
            or citations["schema"] != "genesis.cited_sources.v1"):
        raise AuditFailure("citation and source inventory identities disagree")
    for record in mechanism["files"]:
        path = regular_file(root, relative_path(record["path"]))
        verify_origin(path.read_bytes(), record, inventory[record["source"]])
    repositories = {row["repository"]: row for row in citations["repositories"]}
    sources: set[str] = set()
    for record in citations["files"]:
        name = record["path"]
        if name in sources:
            raise AuditFailure(f"duplicate citation destination: {name}")
        sources.add(name)
        repository = repositories[record["repository"]]
        if record["commit"] != repository["commit"]:
            raise AuditFailure(f"citation revision differs from repository pin: {name}")
        expected_url = (f"https://github.com/{record['repository']}/blob/"
                        f"{record['commit']}/{record['source']}")
        if record["source_url"] != expected_url:
            raise AuditFailure(f"citation origin URL disagrees with source pin: {name}")
        origin = None
        if record["repository"] == "dbccpage/19L57G1":
            if record["commit"] != contract["source_commit"]:
                raise AuditFailure("citation differs from upstream source pin")
            origin = inventory[record["source"]]
        path = regular_file(root, relative_path(name))
        verify_origin(path.read_bytes(), record, origin)
    for repository in repositories.values():
        if repository["license_path"] not in sources:
            raise AuditFailure("source license is not bound by the citation manifest")
    manuscript = (root / "paper.md").read_text(encoding="utf-8")
    return {"exact_pinned_mechanization_blobs": len(mechanism["files"]),
            "cited_source_records": len(sources),
            "local_manuscript_references": check_references(root, manuscript, sources)}


if __name__ == "__main__":
    print(json.dumps(check_sources(), indent=2))
