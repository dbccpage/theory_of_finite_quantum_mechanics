"""Ingest QM_122's `evidence/PAPER_CLAIM_MAP.md`.

That file is the single most useful artifact in the corpus: a 2026-08-19 audit of
seventeen papers, 37 agents, every row adversarially verified by an independent
agent, with a restricted status vocabulary and an explicit `exists / stub` column
saying whether the cited Lean declaration is real or a `True` stub. It also
carries a `repair required` column -- the source authors' own list of what would
close each hole.

Two cautions the map states about itself, both honoured here:

* Its narrative cells are truncated summaries; the un-truncated evidence lives in
  a workflow transcript that is not committed. So a row is a triage signal, not a
  replayable receipt.
* A Lean declaration existing is not a Lean declaration built. The map repeatedly
  notes that no lake config covers `lean4/original_lean_20260809`, so "exists"
  means source text, not a replayed build.

Consequently the strongest type this module ever awards is
LEAN SOURCE (UNREPLAYED). Nothing here mints PROVEN.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import re

# Cells escape literal pipes as `\|` (norms, inner products). Protect them
# before splitting on the real column separators.
_ESCAPED_PIPE = "\x00PIPE\x00"

MAP_RELPATH = (
    "122_finite_hilbert_boundary_from_primitive_difference/evidence/PAPER_CLAIM_MAP.md"
)

# The audit's restricted status vocabulary, mapped onto this application's types.
# `proved` is deliberately NOT mapped to a proof: see the module docstring.
STATUS_TYPE = {
    "proved": "LEAN SOURCE (UNREPLAYED)",
    "computed": "FINITE FIXTURE",
    "conditional": "CONDITIONAL",
    "imported": "DECLARED",
    "suggested": "OPEN",
    "refuted": "REFUTED BY AUDIT",
}


def _split_row(line: str) -> list[str]:
    protected = line.replace(r"\|", _ESCAPED_PIPE)
    cells = [c.strip().replace(_ESCAPED_PIPE, "|") for c in protected.strip().strip("|").split("|")]
    return cells


def _clean_status(raw: str) -> str:
    """Strip the audit's `\\*` verifier-correction marker and normalise."""
    return raw.replace("\\*", "").replace("*", "").strip().lower()


def parse(qf_root: pathlib.Path) -> dict[str, dict]:
    """Return {paper_key: {claim_id: record}} for the seventeen audited papers.

    `paper_key` is the three-digit source key ("020", "060", ...). A record
    carries the audit's status, its Lean declaration and exists/stub reading, its
    test note, its countermodel, and the repair it asks for.
    """
    path = qf_root / MAP_RELPATH
    if not path.is_file():
        return {}

    out: dict[str, dict] = {}
    current: str | None = None
    header: list[str] | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+QM_(\d{3})\b", line)
        if heading:
            current = heading.group(1)
            out.setdefault(current, {})
            header = None
            continue
        if current is None or not line.strip():
            continue
        if "|" not in line:
            continue

        cells = _split_row(line)
        if cells and cells[0].lower() == "claim id":
            header = [c.lower() for c in cells]
            continue
        if header is None or len(cells) < len(header):
            continue
        if set("".join(cells)) <= set("-: "):
            continue

        rec = dict(zip(header, cells))
        cid = rec.get("claim id", "").strip()
        status = _clean_status(rec.get("status", ""))
        if not cid or status not in STATUS_TYPE:
            continue

        out[current][cid] = {
            "audit_status": status,
            "type": STATUS_TYPE[status],
            "lean_declaration": rec.get("lean declaration", "")[:300],
            "exists_stub": rec.get("exists / stub", "").replace("\\*", "").strip(),
            "test": rec.get("test or finite certificate", "")[:300],
            "countermodel": rec.get("countermodel", "")[:300],
            "repair_required": rec.get("repair required", "")[:400],
        }
    return out


def evidence_for(rec: dict) -> str:
    """The evidence string this application records for an audited claim."""
    exists = rec["exists_stub"].lower()
    if exists.startswith("yes / yes"):
        return (
            "none -- the cited Lean declaration is a `True := by trivial` stub "
            "(QM_122 PAPER_CLAIM_MAP, 2026-08-19 audit)"
        )
    if exists.startswith("no /"):
        return "none -- no Lean declaration exists (QM_122 PAPER_CLAIM_MAP, 2026-08-19 audit)"
    if exists.startswith("yes / no"):
        decl = rec["lean_declaration"].split(";")[0].strip()
        return (
            f"Lean source only, no replayed build: `{decl[:160]}` "
            "(QM_122 PAPER_CLAIM_MAP; no lake config covers lean4/original_lean_20260809)"
        )
    return "none -- audit did not resolve the Lean binding"


def retype_from_audit(rec: dict) -> tuple[str, str]:
    """Type a claim from its audit row, never above LEAN SOURCE (UNREPLAYED)."""
    exists = rec["exists_stub"].lower()
    ctype = rec["type"]
    # A "proved" row whose declaration is a stub, or absent, proves nothing.
    if ctype == "LEAN SOURCE (UNREPLAYED)" and not exists.startswith("yes / no"):
        ctype = "ASSERTED"
    # A refuted row carries no evidence, whatever Lean it once pointed at:
    # citing the declaration would read as support for a claim that was struck.
    if ctype == "REFUTED BY AUDIT":
        return ctype, "none -- refuted by the 2026-08-19 adversarial audit; do not cite"
    return ctype, evidence_for(rec)


def normalise_id(claim_id: str, paper_key: str) -> str:
    """Collapse the three spellings of a claim id onto one key.

    Ledgers and the audit disagree: `C1`, `QM-020-C1`, `QM_200-C0`, `QM206-C1`
    all occur. Upper-case, drop separators, then strip a leading `QM<key>`.
    """
    s = re.sub(r"[^A-Za-z0-9]", "", claim_id).upper()
    for prefix in (f"QM{paper_key}", "QM"):
        if s.startswith(prefix) and len(s) > len(prefix):
            s = s[len(prefix):]
            break
    return s


def index_by_normalised(records: dict, paper_key: str) -> dict[str, tuple[str, dict]]:
    """{normalised_id: (original_id, record)} for one paper."""
    return {normalise_id(cid, paper_key): (cid, rec) for cid, rec in records.items()}

__all__ = ['MAP_RELPATH', 'STATUS_TYPE', 'evidence_for', 'index_by_normalised', 'normalise_id', 'parse', 'retype_from_audit']
