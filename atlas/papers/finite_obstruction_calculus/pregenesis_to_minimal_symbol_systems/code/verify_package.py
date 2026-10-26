"""Verify source custody, local manuscript references and grammar controls."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from grammar.check_grammars import Grammar

ROOT = Path(__file__).resolve().parents[1]


def verify_sources(root: Path = ROOT) -> int:
    manifest = json.loads((root / "manifests/imported_sources.json").read_text(encoding="utf-8"))
    if manifest["source_commit"] != "d1d2f034198a72b730320a69691e63351557c019":
        raise ValueError("unexpected source revision")
    seen = set()
    for row in manifest["files"]:
        relative = row["path"]
        path = (root / relative).resolve()
        path.relative_to(root.resolve())
        if relative in seen or path.is_symlink():
            raise ValueError("duplicate or symbolic source")
        seen.add(relative)
        data = path.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"] or blob != row["git_blob_sha1"]:
            raise ValueError("source bytes changed: " + relative)
        if row["source_commit"] != manifest["source_commit"]:
            raise ValueError("mixed source revisions")
    return len(seen)


def verify_references(root: Path = ROOT) -> int:
    text = (root / "paper.md").read_text(encoding="utf-8")
    if re.search(r"(?i)\bpaper\s*00[012]\b|WDP Paper Trio", text):
        raise ValueError("retired paper-series label in manuscript")
    if "<div align=\"center\">2026-10-09</div>\n<div align=\"center\">Version 1.0.0</div>" not in text:
        raise ValueError("date and centered version block missing")
    links = re.findall(r"\]\(([^)]+)\)", text)
    for target in links:
        if "://" in target or target.startswith("#"):
            continue
        path = (root / target.split("#", 1)[0]).resolve()
        path.relative_to(root.resolve())
        if not path.is_file():
            raise ValueError("broken manuscript reference: " + target)
    return len(links)


def verify_grammars(root: Path = ROOT) -> dict[str, int]:
    counts = {}
    for name in ("pre_genesis", "sn", "mssn"):
        directory = root / "code/grammar"
        grammar = Grammar((directory / f"{name}.ebnf").read_text(encoding="utf-8"))
        cases = json.loads((directory / f"{name}_conformance_cases.json").read_text(encoding="utf-8"))
        for case in cases:
            actual = grammar.accepts(case["start"], case["text"])
            if actual != case["accept"]:
                raise ValueError(f"grammar divergence: {name}/{case['id']}")
        counts[name] = len(cases)
    return counts


def main() -> None:
    print(json.dumps(dict(source_blobs=verify_sources(), manuscript_links=verify_references(),
                          grammar_controls=verify_grammars(), authority_effect="None"), indent=2))


if __name__ == "__main__":
    main()
