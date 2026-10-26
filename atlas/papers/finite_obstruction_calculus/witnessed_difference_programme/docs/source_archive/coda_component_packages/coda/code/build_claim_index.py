"""Derive the machine index from the authoritative Markdown claim ledger."""

import json
import re
from pathlib import Path
from typing import Any


def destinations(text: str) -> list[str]:
    result: list[str] = []
    for match in re.finditer(r"\bCODA-(\d{2})(?:\.\.(\d{2}))?\b", text):
        first = int(match[1])
        last = int(match[2] or match[1])
        result.extend(f"CODA-{n:02}" for n in range(first, last + 1))
    return result


def build_index(root: Path) -> dict:
    ledger = (root / "coda_claim_ledger.md").read_text(encoding="utf-8")
    claims: list[dict[str, Any]] = []
    for match in re.finditer(
        r"^\| \[(CODA-\d{2})\]\(coda\.md(?:#[^)]*)?\) \| ([A-Z_]+) \|", ledger, re.M
    ):
        claims.append({"id": match[1], "status": match[2], "lean_declarations": []})
    by_id = {row["id"]: row for row in claims}
    for match in re.finditer(r"^\| (CODA-\d{2}) \| ([^\n|]*) \|", ledger, re.M):
        by_id[match[1]]["lean_declarations"].extend(
            f"Coda.{name}" for name in re.findall(r"`([A-Za-z_0-9]+)`", match[2])
        )
    legacy: list[dict[str, Any]] = []
    for match in re.finditer(
        r"^\| ((?:DES-\d{2}|FDN-\d{2}|CD-\d{2}[ab]?)) \| ([^|]+) \| ([^|]+) \|$",
        ledger,
        re.M,
    ):
        legacy.append(
            {
                "id": match[1],
                "current_claims": destinations(match[2]),
                "disposition": match[3].strip(),
            }
        )
    expected = [f"CODA-{n:02}" for n in range(1, 27)]
    if [row["id"] for row in claims] != expected or len(legacy) != 48:
        raise ValueError(
            "The ledger must contain twenty-six current claims and 48 source dispositions"
        )
    return {
        "schema_version": 1,
        "paper_version": "2.0.1",
        "authority_effect": "None",
        "ledger": "coda_claim_ledger.md",
        "claims": claims,
        "legacy_dispositions": legacy,
    }


def render_lean_map(index: dict) -> str:
    lines = [
        "# Lean claim map — CODA", "",
        "Generated from the authoritative claim ledger by `code/build_claim_index.py`.",
        "A declaration listed beside a policy or finite example supports only the",
        "narrow statement specified in the ledger; it does not upgrade that status.", "",
        "| Claim | Status | Local Lean declarations |",
        "|---|---|---|",
    ]
    for row in index["claims"]:
        declarations = ", ".join(f"`{name}`" for name in row["lean_declarations"]) or "None"
        lines.append(f"| {row['id']} | {row['status']} | {declarations} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    index = build_index(root)
    (root / "claim_index.json").write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (root / "docs/lean_claim_map.md").write_text(
        render_lean_map(index), encoding="utf-8", newline="\n"
    )
