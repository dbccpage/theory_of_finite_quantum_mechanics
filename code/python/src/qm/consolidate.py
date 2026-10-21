"""Rebuild the consolidated claim ledger and source inventory from the F004 sources.

This is the application's intake stage. It reads every numbered package under
`coda_atlas/F004_papers/003_quantum_foundations/`, normalises their several
claim-table schemas into one, and records what each source's Lean and Python trees
mechanically support *today*. Evidence is heterogeneous: some sources retain
central `True` scaffolds, while Papers 020, 060, 061, and 122 carry substantive
package-local tests or Lean sources. Every row is typed from its current loci.

Re-run it after editing a source, then run the suite: the governance tests bind
the generated files to the tree and fail when a recorded hash or stub count moves.

    python code/consolidate_sources.py
    python code/consolidate_sources.py --check   # CI: fail if regeneration would change anything

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import itertools
import pathlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path as _Path

import yaml

from .campaigns import audit_map

APP_ROOT = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm")
REPO_ROOT = APP_ROOT.parents[1]
QF = REPO_ROOT / "coda_atlas/F004_papers/003_quantum_foundations"

SOURCE_KEYS = None

PUBLISHED = {
    "020_born_normalization_and_conditional_hilbert_lift": "https://zenodo.org/records/20683775",
    "080_cptp_trace_norm_geometry_and_quantum_dual_witnesses": "https://zenodo.org/records/20550459",
}

REDIRECT_STUBS = {
    "003_residual_density_calculus_l1_l2_boundary": "004_general_obstruction_management_calculus",
    "007_quantum_realization_spine": "006_quantum_realization_requires_finite_descent",
    "028_the_u1_selector": "062_the_u1_selector",
}

TITLES = {
    "000": "Primitive difference for quantum carriers",
    "001": "Tower walk / registry-relative interface lift",
    "002": "Cofiber to Banach quotient bridge",
    "003": "Residual density calculus (L1/L2 boundary) -- redirect stub",
    "004": "General obstruction management calculus",
    "005": "Finite quantum packet theorem for M2",
    "006": "Quantum realization requires finite descent",
    "007": "Quantum realization spine -- redirect stub",
    "008": "Finite descent to GTFOC projection",
    "010": "Hilbert space cochains / QM cohomology",
    "011": "State-effect pairing audit",
    "012": "Density matrices as diagonal residual weights",
    "020": "Conditional Hilbert lifts of l1 sector weights and Born normalization redundancy",
    "021": "Selective measurement update as idempotent conditioning",
    "028": "The U(1) selector -- dual-alias stub",
    "030": "Finite weighted transport calculus",
    "031": "Finite path-sum as graded transport",
    "032": "GTTA Feynman finite shadow histories",
    "033": "Discrete Schrodinger cochain transport and l1 probability conservation",
    "034": "Unitary finite shadow",
    "035": "Hamiltonian generator admission",
}


def _path_key(p: pathlib.Path) -> str:
    """Platform-stable sort key for filesystem paths.

    `sorted()` on Path objects is NOT portable: PurePath ordering compares
    case-insensitively on Windows and case-sensitively on POSIX, so
    `H001Rats.lean` and `H001_probability_simplex.lean` swap places between a
    developer's machine and CI ('R' is 0x52, '_' is 0x5F). That made the
    generated inventory differ by platform, so `--check` passed locally and
    reported STALE on Linux for the same tree. Sort the string instead.
    """
    return p.as_posix()

def title_for(name: str) -> str:
    """A curated title where we have one, otherwise the directory name read out."""
    key = name[:3]
    if key in TITLES:
        return TITLES[key]
    return name[4:].replace("_", " ").strip().capitalize() or name


CLAIM_COLS = (
    "claim (abbreviated)", "claim", "claim (paper location)", "claim (location)", "statement",
)
STATUS_COLS = (
    "status", "type", "status / lean", "evidence / note", "support / note", "evidence",
)
ID_COLS = ("id", "#", "claim id")

TRIVIAL_STUB = ": True := by trivial"
TAUTOLOGY = "assert mod is not None or True"

TYPE_MEANING = {
    "ASSERTED": "Prose argument only; source claimed PROVEN; no mechanical evidence survives",
    "SCOPE FENCE": "A non-claim / firewall statement, not an empirical assertion",
    "DEFINITION": "Definitional; nothing to prove",
    "UNTYPED": "Source ledger gave no parseable status -- **needs triage**",
    "OPEN": "Source ledger already recorded this as open or conjectural",
    "CONDITIONAL": "Holds only under a stated antecedent",
    "REFUSAL": "A typed refusal",
    "DECLARED": "A declared or imported input, not a result",
    "FINITE FIXTURE": "Backed by passing regression fixtures -- the source's own scope, "
                      "not a theorem proof",
    "LEAN SOURCE (UNREPLAYED)": "A real Lean declaration exists, but no lake config builds it "
                                "here -- source text, not a replayed receipt",
    "REFUTED BY AUDIT": "The 2026-08-19 adversarial audit refuted this row -- **do not cite**",
    "LEAN PROVED (RECEIPTED)": "A real Lean declaration, sorry-free, under a build receipt and "
                               "axiom report",
}




def _is_rule(line: str) -> bool:
    return set(line.strip().strip("|").replace("|", "")) <= set("-: ")


_ESCAPED_PIPE = "\x00PIPE\x00"


def _cells(line: str) -> list[str]:
    protected = line.replace(r"\|", _ESCAPED_PIPE)
    protected = re.sub(r"(`[^`]+`)", lambda m: m.group(0).replace("|", _ESCAPED_PIPE), protected)
    protected = re.sub(r"(\$[^$]+\$)", lambda m: m.group(0).replace("|", _ESCAPED_PIPE), protected)
    protected = re.sub(r"(\\\([^\\]+\\\))", lambda m: m.group(0).replace("|", _ESCAPED_PIPE), protected)
    protected = re.sub(r"(\|<[^>]+>)", lambda m: m.group(0).replace("|", _ESCAPED_PIPE), protected)
    protected = re.sub(r"(\|[\\a-zA-Z0-9_+^-]+>)", lambda m: m.group(0).replace("|", _ESCAPED_PIPE), protected)
    protected = re.sub(r"(\|[\\a-zA-Z0-9_+^-]+\|)", lambda m: m.group(0).replace("|", _ESCAPED_PIPE), protected)
    protected = re.sub(r"\|c\|", _ESCAPED_PIPE + "c" + _ESCAPED_PIPE, protected)
    return [c.strip().replace(_ESCAPED_PIPE, "|") for c in protected.strip().strip("|").split("|")]


def table_kind(header: list[str]) -> str:
    """Classify a markdown table by its header row.

    Only a table carrying both an id-ish and a claim-ish column is a claim table.
    `Action | Detail` and `Consumes | Role` are prose tables and are dropped.
    """
    joined = " ".join(header)
    if "what would upgrade it" in joined:
        return "upgrade"
    if header[0] == "enc":
        return "enc"
    if "obligation" in joined:
        return "obligation"
    if header[0] in ID_COLS and any(c in CLAIM_COLS for c in header):
        return "claim"
    return "other"


def parse_tables(path: pathlib.Path) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] | None = None
    kind = "other"
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            header = None
            continue
        if _is_rule(line):
            continue
        if i + 1 < len(lines) and lines[i + 1].startswith("|") and _is_rule(lines[i + 1]):
            header = [c.lower() for c in _cells(line)]
            kind = table_kind(header)
            continue
        if header is None or kind == "other":
            continue
        row_cells = _cells(line)
        if len(row_cells) > len(header):
            stmt_idx = None
            for idx, col in enumerate(header):
                if col in CLAIM_COLS:
                    stmt_idx = idx
                    break
            if stmt_idx is not None:
                extra = len(row_cells) - len(header)
                merged = "|".join(row_cells[stmt_idx:stmt_idx + extra + 1])
                row_cells = row_cells[:stmt_idx] + [merged] + row_cells[stmt_idx + extra + 1:]
        out[kind].append(dict(zip(header, row_cells)))
    return out


def first(rec: dict, keys) -> str:
    for k in keys:
        if rec.get(k):
            return rec[k]
    return ""


def load_claim_code_map(d: pathlib.Path) -> dict[str, str]:
    """Bind claim ids to existing test nodes from either supported map schema.

    Maps in the estate use both a list of records and a mapping keyed by claim id,
    with `test`, `tests`, or nested `python.tests` loci. Only nodes whose test file
    exists are admitted.
    """
    path = d / "docs" / "claim_code_map.yaml"
    if not path.is_file():
        return {}
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    if not isinstance(doc, dict):
        return {}
    claims_doc = doc.get("claims") or []
    if isinstance(claims_doc, dict):
        entries = [dict(value, id=key) for key, value in claims_doc.items()
                   if isinstance(value, dict)]
    elif isinstance(claims_doc, list):
        entries = [entry for entry in claims_doc if isinstance(entry, dict)]
    else:
        entries = []

    out: dict[str, str] = {}
    for entry in entries:
        cid = str(entry.get("id", "")).strip()
        py = entry.get("python") if isinstance(entry.get("python"), dict) else {}
        raw_nodes = entry.get("tests") or entry.get("test") or py.get("tests") or []
        if isinstance(raw_nodes, str):
            raw_nodes = [raw_nodes]
        nodes = [str(t) for t in raw_nodes if (d / str(t).split("::")[0]).is_file()]
        if not cid or not nodes:
            continue
        out[cid] = ", ".join(f"`{d.name}/{n}`" for n in nodes)
    return out


def retype(source_status: str, mapped_evidence: str | None = None) -> tuple[str, str]:
    """Map a source ledger's status onto an honest type plus an evidence note.

    `mapped_evidence`, when present, is a verified pointer at passing regression
    tests. It can lift a would-be ASSERTED row to FINITE FIXTURE -- but no
    further: the sources that carry such maps declare their own evidence scope as
    "fixed numerical regression fixtures; not theorem proof", and this function
    does not out-rank a source's own scope statement.
    """
    u = source_status.upper()
    if "SCOPE FENCE" in u or "NON-CLAIM" in u or "NONCLAIM" in u:
        return "SCOPE FENCE", "n/a -- a fence, not an empirical claim"
    if "REFUS" in u:
        return "REFUSAL", "n/a -- a typed refusal"
    if "DEFINITION" in u or "SCHEMA" in u:
        return "DEFINITION", "n/a -- definitional"
    if "OPEN" in u or "CONJECT" in u:
        return "OPEN", "none"
    if "CONDITIONAL" in u:
        return "CONDITIONAL", "none"
    if "PROVEN" in u or "PROVED" in u or "MECHANIZED" in u:
        if mapped_evidence:
            return "FINITE FIXTURE", mapped_evidence
        return "ASSERTED", "none -- source says PROVEN; no surviving mechanical evidence"
    if "DECLARED" in u or "IMPORT" in u:
        return "DECLARED", "n/a -- declared/imported input"
    if mapped_evidence:
        return "FINITE FIXTURE", mapped_evidence
    return "UNTYPED", "none"




def source_dirs() -> list[pathlib.Path]:
    return sorted(
        d
        for d in QF.iterdir()
        if d.is_dir()
        and d.name[:3].isdigit()
        and (SOURCE_KEYS is None or d.name[:3] in SOURCE_KEYS)
    )


def strip_lean_comments(text: str) -> str:
    """Drop Lean block and line comments before counting proof obligations.

    QM_120's scaffold carries a doc comment reading "MECHANIZED: Lean theorem
    builds without sorry, admit, or declared axiom" -- attached to a
    `theorem ... : True := by trivial`. Counting the word inside that comment
    would report a proof obligation that is not there, and would also let the
    comment's own false claim pass unnoticed. Strip comments, count code.
    """
    text = re.sub(r"/-.*?-/", " ", text, flags=re.DOTALL)
    return re.sub("--[^" + chr(10) + "]*", " ", text)
    return re.sub("--[^" + chr(10) + "]*", " ", text)


def lean_files_for(d: pathlib.Path) -> tuple[list[pathlib.Path], str]:
    """A source's own Lean files, or none."""
    local = d / "lean4"
    if local.is_dir() and any(local.glob("*.lean")):
        return sorted(local.glob("*.lean"), key=_path_key), "local"
    return [], "none"


def paper_of(d: pathlib.Path) -> pathlib.Path | None:
    return next(
        (
            p
            for p in sorted(d.glob("*.md"), key=_path_key)
            if not re.search(r"_(change_log|claim_ledger)\.md$", p.name) and p.name != "README.md"
        ),
        None,
    )


def build_inventory() -> dict:
    sources = []
    for d in source_dirs():
        paper = paper_of(d)
        ledger = next(iter(sorted(d.glob("*_claim_ledger.md"), key=_path_key)), None)
        lean_files, lean_home = lean_files_for(d)
        tests = sorted(d.rglob("test_*.py"), key=_path_key)
        receipt = next(
            (
                r
                for r in (d / "evidence" / "axiom_report.txt", d / "evidence" / "build_receipt.md")
                if r.is_file()
            ),
            None,
        )

        theorems = sum(
            len(re.findall(r"^\s*(?:theorem|lemma)\s", f.read_text(encoding="utf-8"), re.M))
            for f in lean_files
        )
        stubs = sum(f.read_text(encoding="utf-8").count(TRIVIAL_STUB) for f in lean_files)
        sorries = sum(
            len(re.findall(r"\bsorry\b", strip_lean_comments(f.read_text(encoding="utf-8"))))
            for f in lean_files
        )
        tautological = (
            all(TAUTOLOGY in t.read_text(encoding="utf-8") for t in tests) if tests else None
        )

        sources.append(
            {
                "source_id": f"SRC-{d.name[:3]}",
                "title": title_for(d.name),
                "origin": f"coda_atlas/F004_papers/003_quantum_foundations/{d.name}",
                "paper": paper.name if paper else None,
                "paper_lines": len(paper.read_text(encoding="utf-8").splitlines()) if paper else 0,
                "paper_sha256": hashlib.sha256(paper.read_bytes()).hexdigest() if paper else None,
                "claim_ledger": ledger.name if ledger else None,
                "zenodo": PUBLISHED.get(d.name),
                "free_to_rewrite": d.name not in PUBLISHED,
                "disposition": (
                    "redirect_stub_absorbed_into_" + REDIRECT_STUBS[d.name]
                    if d.name in REDIRECT_STUBS
                    else "mine_for_prose_and_claims"
                ),
                "lean_evidence": {
                    "home": lean_home,
                    "files": [f.name for f in lean_files],
                    "theorems": theorems,
                    "trivial_true_stubs": stubs,
                    "sorry": sorries,
                    "build_receipt": receipt.name if receipt else None,
                    "verdict": (
                        f"no_evidence: all {theorems} declarations are `{TRIVIAL_STUB}`"
                        if theorems and theorems == stubs
                        else (
                            "no_lean_file"
                            if not lean_files
                            else (
                                f"real_lean: {theorems} declarations, {sorries} sorry, "
                                f"0 True-stubs, build receipt {receipt.name}"
                                if receipt and not stubs and not sorries
                                else "review_required"
                            )
                        )
                    ),
                },
                "python_evidence": {
                    "files": [t.relative_to(d).as_posix() for t in tests],
                    "tautological": tautological,
                    "claims_mapped_to_tests": len(load_claim_code_map(d)),
                    "verdict": (
                        f"no_evidence: the only assertion is the tautology `{TAUTOLOGY}`"
                        if tautological
                        else (
                            "no_test_file"
                            if not tests
                            else (
                                f"real_tests: {len(load_claim_code_map(d))} claims bound to "
                                "existing tests via docs/claim_code_map.yaml; the source declares "
                                "its own scope as regression fixtures, not theorem proof"
                                if load_claim_code_map(d)
                                else "real_tests_but_unmapped: no claim_code_map binds them"
                            )
                        )
                    ),
                },
            }
        )
    return {
        "schema_version": "1.0.0",
        "app": "apps/finite_qm",
        "authority_effect": "None",
        "generated": "2026-09-04",
        "note": (
            "Disposition of every numbered F004 quantum-foundations package consolidated into this "
            "application. lean_evidence and python_evidence record what each source tree "
            "mechanically supports today, not what its ledger asserts."
        ),
        "sources": sources,
    }


AUDIT: dict[str, dict] = {}


def receipted_lean_files(d: pathlib.Path) -> set[str]:
    """Lean file stems for a source whose own `lean4/` is real AND receipted.

    "Real" means sorry-free with no `True` stubs; "receipted" means an axiom
    report or build receipt sits in `evidence/`. Only QM_122 qualifies. A ledger
    row whose `Where` names one of these stems is the only thing in this corpus
    that earns LEAN PROVED (RECEIPTED).
    """
    files, home = lean_files_for(d)
    if home != "local" or not files:
        return set()
    if not any((d / "evidence" / n).is_file() for n in ("axiom_report.txt", "build_receipt.md")):
        return set()
    for f in files:
        text = f.read_text(encoding="utf-8")
        if TRIVIAL_STUB in text or re.search(r"\bsorry\b", text):
            return set()
    return {f.stem for f in files}


def build_claims() -> tuple[list[dict], list[dict], list[dict]]:
    claims: list[dict] = []
    upgrades: list[dict] = []
    dropped: list[dict] = []
    for d in source_dirs():
        ledger = next(iter(sorted(d.glob("*_claim_ledger.md"), key=_path_key)), None)
        if ledger is None:
            continue
        tables = parse_tables(ledger)
        code_map = load_claim_code_map(d)
        key3 = d.name[:3]
        audited = audit_map.index_by_normalised(AUDIT.get(key3, {}), key3)
        audit_used: set[str] = set()
        receipted = receipted_lean_files(d)
        for rec in tables.get("claim", []):
            cid = first(rec, ID_COLS).strip("` *")
            statement = first(rec, CLAIM_COLS)
            status = " . ".join(v for k, v in rec.items() if k in STATUS_COLS and v)
            if not cid or not statement:
                dropped.append({"source": d.name, "row": rec})
                continue
            mapped = code_map.get(cid) or code_map.get(cid.rsplit("-", 1)[-1])
            ctype, evidence = retype(status, mapped)
            where = (rec.get("where") or "").strip("` ")
            stem = where.split(".")[0].strip("` ")
            if stem and any(s.startswith(stem) for s in receipted):
                named = sorted(s for s in receipted if s.startswith(stem))
                ctype = "LEAN PROVED (RECEIPTED)"
                evidence = (
                    f"`{d.name}/lean4/{named[0]}.lean`"
                    + (f" (+{len(named) - 1} more)" if len(named) > 1 else "")
                    + f", sorry-free, receipt `{d.name}/evidence/axiom_report.txt`"
                )
            hit = audited.get(audit_map.normalise_id(cid, key3))
            arec = hit[1] if hit else None
            if hit:
                audit_used.add(hit[0])
            if arec is not None:
                ctype, evidence = audit_map.retype_from_audit(arec)
                if arec["repair_required"]:
                    upgrades.append(
                        {
                            "source": d.name,
                            "id": cid,
                            "what would upgrade it": arec["repair_required"],
                            "difficulty": "",
                            "lean/numerical?": arec["exists_stub"],
                        }
                    )
            claims.append(
                {
                    "id": f"{d.name[:3]}:{cid}",
                    "statement": statement,
                    "type": ctype,
                    "evidence": evidence,
                    "source": d.name,
                    "locus": rec.get("location") or rec.get("where", ""),
                    "source_status": status,
                }
            )
        for cid, arec in AUDIT.get(key3, {}).items():
            if cid in audit_used:
                continue
            ctype, evidence = audit_map.retype_from_audit(arec)
            claims.append(
                {
                    "id": f"{key3}:audit:{cid}",
                    "statement": (arec["lean_declaration"] or arec["test"] or cid)[:220],
                    "type": ctype,
                    "evidence": evidence,
                    "source": d.name,
                    "locus": "QM_122 PAPER_CLAIM_MAP (audit row; no ledger row matches)",
                    "source_status": f"audit: {arec['audit_status']}",
                }
            )
            if arec["repair_required"]:
                upgrades.append(
                    {
                        "source": d.name,
                        "id": cid,
                        "what would upgrade it": arec["repair_required"],
                        "difficulty": "",
                        "lean/numerical?": arec["exists_stub"],
                    }
                )
        for rec in tables.get("upgrade", []):
            upgrades.append({"source": d.name, **rec})
    return claims, upgrades, dropped



EVIDENCED_CLAIMS = [
    (
        "FQM-E1",
        "A finite density matrix is Hermitian, unit-trace, and positive semidefinite; the "
        "predicate decides it",
        "FINITE COMPUTATION",
        "`code/density_matrix.py`, `code/tests/unit/test_density_matrix.py`",
    ),
    (
        "FQM-E2",
        "The depolarizing channel is trace-norm contractive on the tested pairs",
        "FINITE COMPUTATION",
        "`code/cptp_channel.py`, `code/tests/unit/test_cptp_contractivity.py`",
    ),
    (
        "FQM-E3",
        "For the tested pairs W = UV* attains the trace norm, so the sampled duality gap is zero",
        "FINITE FIXTURE",
        "`code/cptp_channel.py` -- fixture-level only; see GAP-F001-S000-001",
    ),
    (
        "FQM-E4",
        "The Mermin-Peres 3x3 grid has commuting rows and columns, row products +I, and column "
        "products (+I, +I, -I)",
        "EXACT FINITE ALGEBRA",
        "`code/mermin_peres.py`, `code/tests/unit/test_mermin_peres.py`",
    ),
    (
        "FQM-E6",
        "QM-001-C4: D(x,y) = y - x is antisymmetric, and sameness holds exactly when the "
        "difference vanishes -- certified, never assumed",
        "EXACT FINITE ALGEBRA",
        "`code/cochain.py`, `code/tests/unit/test_cochain.py`",
    ),
    (
        "FQM-E7",
        "QM-001-C5: the declared packet is a complex, d1 d0 = 0, and it fails to be one when a "
        "2-cell is not a closed loop",
        "EXACT FINITE ALGEBRA",
        "`code/cochain.py`, `code/tests/unit/test_cochain.py`",
    ),
    (
        "FQM-E8",
        "Phi_1 vanishes on im(d0), is invariant under adding a coboundary, scales with the "
        "declared weights, and never exceeds any representative's norm -- evaluated numerically via LP (HiGHS) with declared tolerance 1e-9",
        "FINITE COMPUTATION",
        "`code/cochain.py`, `code/tests/unit/test_cochain.py`",
    ),
    (
        "FQM-E9",
        "QM-001-C6: the Phi_1/Gamma_2 trichotomy is exhaustive on the sampled family and reads the "
        "class, not the representative -- shifting by a coboundary never changes the verdict",
        "FINITE COMPUTATION",
        "`code/cochain.py`, `code/tests/unit/test_cochain.py`",
    ),
    (
        "FQM-E5",
        "State preparation, depolarizing noise, then projective update preserves density-matrix "
        "validity",
        "FINITE COMPUTATION",
        "`code/tests/integration/test_quantum_pipeline.py`",
    ),
]

APPLICATION_CLAIMS: list[dict] = [
    {
        "id": "FQM-E1",
        "statement": (
            "A finite density matrix is Hermitian, unit-trace, and positive semidefinite; "
            "the predicate decides it"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/density_matrix.py, code/tests/unit/test_density_matrix.py",
        "source": "012_density_matrices_as_diagonal_residual_weights",
    },
    {
        "id": "FQM-E2",
        "statement": "The depolarizing channel is trace-norm contractive on the tested pairs",
        "type": "FINITE COMPUTATION",
        "evidence": "code/cptp_channel.py, code/tests/unit/test_cptp_contractivity.py",
        "source": "080_cptp_trace_norm_geometry_and_quantum_dual_witnesses",
    },
    {
        "id": "FQM-E3",
        "statement": "For the tested pairs W = UV* attains the trace norm, so the sampled duality gap is zero",
        "type": "FINITE FIXTURE",
        "evidence": "code/cptp_channel.py -- fixture-level only; see GAP-F001-S000-001",
        "source": "080_cptp_trace_norm_geometry_and_quantum_dual_witnesses",
    },
    {
        "id": "FQM-E4",
        "statement": (
            "The Mermin-Peres 3x3 grid has commuting rows and columns, row products +I, "
            "and column products (+I, +I, -I)"
        ),
        "type": "EXACT FINITE ALGEBRA",
        "evidence": "code/mermin_peres.py, code/tests/unit/test_mermin_peres.py",
        "source": "120_mermin_peres_contextuality_cochain_obstruction",
    },
    {
        "id": "FQM-E5",
        "statement": (
            "State preparation, depolarizing noise, then projective update preserves "
            "density-matrix validity"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/tests/integration/test_quantum_pipeline.py",
        "source": "012_density_matrices_as_diagonal_residual_weights",
    },
    {
        "id": "FQM-E6",
        "statement": (
            "QM-001-C4: D(x,y) = y - x is antisymmetric, and sameness holds exactly when "
            "the difference vanishes -- certified, never assumed"
        ),
        "type": "EXACT FINITE ALGEBRA",
        "evidence": "code/cochain.py, code/tests/unit/test_cochain.py",
        "source": "001_tower_walk_registry_relative_interface_lift",
    },
    {
        "id": "FQM-E7",
        "statement": (
            "QM-001-C5: the declared packet is a complex, d1 d0 = 0, and it fails to be one "
            "when a 2-cell is not a closed loop"
        ),
        "type": "EXACT FINITE ALGEBRA",
        "evidence": "code/cochain.py, code/tests/unit/test_cochain.py",
        "source": "001_tower_walk_registry_relative_interface_lift",
    },
    {
        "id": "FQM-E8",
        "statement": (
            "Phi_1 vanishes on im(d0), is invariant under adding a coboundary, scales "
            "with the declared weights, and never exceeds any representative's norm -- evaluated "
            "numerically via LP (HiGHS) with declared tolerance 1e-9"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/cochain.py, code/tests/unit/test_cochain.py",
        "source": "001_tower_walk_registry_relative_interface_lift",
    },
    {
        "id": "FQM-E9",
        "statement": (
            "QM-001-C6: the Phi_1/Gamma_2 trichotomy is exhaustive on the sampled family and "
            "reads the class, not the representative -- shifting by a coboundary never changes "
            "the verdict"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/cochain.py, code/tests/unit/test_cochain.py",
        "source": "001_tower_walk_registry_relative_interface_lift",
    },
    {
        "id": "FQM-F1",
        "statement": (
            "Rung 1: Primitive Difference D(x, y) = y - x certifies sameness if and only if "
            "difference vanishes; antisymmetric and 1-cocycle"
        ),
        "type": "EXACT FINITE ALGEBRA",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py, lean4/PrimitiveDifference.lean",
        "source": "000_primitive_difference_for_quantum_carriers",
    },
    {
        "id": "FQM-F2",
        "statement": (
            "Rung 2: Finite Cochain Packet satisfies boundary nilpotence d1 d0 = 0, exactness "
            "H^1 = 0 on filled triangle, and exact obstruction on open cycle"
        ),
        "type": "EXACT FINITE ALGEBRA",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py, lean4/FiniteCochain.lean",
        "source": "001_tower_walk_registry_relative_interface_lift",
    },
    {
        "id": "FQM-F3",
        "statement": (
            "Rung 3: Positive residual weights yield L^1 ray-invariant probability distributions; "
            "Born rule amplitude mapping enforces quadratic curvature"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py, lean4/FiniteDensity.lean",
        "source": "020_born_normalization_and_conditional_hilbert_lift",
    },
    {
        "id": "FQM-F4",
        "statement": (
            "Rung 4: U(1) holonomy around closed cycles yields non-L^1 interference resources; "
            "Sorkin 3-slit higher-order interference vanishes identically"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py",
        "source": "061_interference_as_the_non_l1_resource",
    },
    {
        "id": "FQM-F5",
        "statement": (
            "Rung 5: Bipartite tensor composition exhibits pure state entanglement (Schmidt rank > 1) "
            "and state-independent Mermin-Peres contextuality obstruction"
        ),
        "type": "EXACT FINITE ALGEBRA",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py, lean4/DualWitness.lean",
        "source": "120_mermin_peres_contextuality_cochain_obstruction",
    },
    {
        "id": "FQM-F6",
        "statement": (
            "Rung 6: Discrete unitary dynamics preserves L^2 norm; continuous-time Hamiltonian generator "
            "has multi-branch logarithm obstruction"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py",
        "source": "034_unitary_finite_shadow",
    },
    {
        "id": "FQM-F7",
        "statement": (
            "Rung 7: Valid POVMs yield non-negative Born probabilities summing to unity; non-selective "
            "measurement induces decoherence; CPTP maps are trace-norm contractive"
        ),
        "type": "FINITE COMPUTATION",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py, lean4/FiniteDensity.lean",
        "source": "021_measurement_update_as_idempotent_conditioning",
    },
    {
        "id": "FQM-F8",
        "statement": (
            "Rung 8: Boundary defense certifies exact scope where finite presentation stops, refusing "
            "continuum Hilbert lift and continuous-time generator"
        ),
        "type": "SCOPE FENCE",
        "evidence": "code/foundations.py, code/tests/e2e/test_quantum_walk_e2e.py",
        "source": "122_finite_hilbert_boundary_from_primitive_difference",
    },
]


def load_application_claims() -> list[dict]:
    """Load application-level claims from existing ledger, falling back to declared constants."""
    ledger_path = APP_ROOT / "claims/claim_ledger.yaml"
    if ledger_path.is_file():
        try:
            existing = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
            if isinstance(existing, dict) and "application_claims" in existing:
                return existing["application_claims"]
        except Exception:
            pass
    return list(APPLICATION_CLAIMS)


def _esc(s: str, max_len: int | None = None) -> str:
    val = (s or "").replace("\n", " ").strip()
    if max_len is not None and len(val) > max_len:
        val = val[:max_len].rstrip()
    res = val.rstrip().replace("|", "\\|")
    if res.endswith("\\") and not res.endswith("\\\\"):
        res = res[:-1]
    return res


def emit_markdown(
    claims, upgrades, dropped, inventory, app_claims: list[dict] | None = None
) -> str:
    if app_claims is None:
        app_claims = load_application_claims()
    by_source: dict[str, list[dict]] = defaultdict(list)
    for c in claims:
        by_source[c["source"]].append(c)
    dist = Counter(c["type"] for c in claims)
    unsupported = dist["ASSERTED"] + dist["UNTYPED"]
    source_count = len(inventory["sources"])
    stub_total = sum(s["lean_evidence"]["trivial_true_stubs"] for s in inventory["sources"])
    tautology_sources = sum(
        s["python_evidence"]["tautological"] is True for s in inventory["sources"]
    )

    out = [
        "# Claim Ledger -- Finite Quantum Mechanics (consolidated)",
        "",
        "<!-- Source TeX uses underscores for subscripts, not Markdown emphasis. -->",
        "<!-- markdownlint-disable MD049 -->",
        "",
        "**App:** `apps/finite_qm/`",
        "",
        "**AuthorityEffect:** None.",
        "",
        "**Citation:** `sealed-derivation-v1 (3100c4e)`",
        "",
        "**Date:** 2026-09-04",
        "",
        "**Generated by:** `code/consolidate_sources.py` -- do not hand-edit; edit the source or "
        "the generator.",
        "",
        f"**Sources:** all {source_count} numbered packages of "
        "`coda_atlas/F004_papers/003_quantum_foundations/`, plus the code and gap register of "
        "`coda_atlas/F001_quantum/S000_finite_quantum_mechanics/`.",
        "",
        "## Read this first",
        "",
        "Evidence is typed per source from the tree as it stands today:",
        "",
        f"- The selected Lean trees still contain **{stub_total}** declarations of the form "
        "`theorem X : True := by trivial`; those rows receive no proof credit.",
        f"- **{tautology_sources}** sources have test files whose assertions are all the corpus "
        "tautology `assert mod is not None or True`; those files receive no test credit.",
        "- Package-local tests and receipted Lean sources are recorded separately. A mapped test "
        "supports only a finite fixture; a Lean source earns proof status only under a receipt.",
        "",
        "A source row reading PROVEN is therefore recorded here as **ASSERTED**: the prose argument",
        "may well be correct, but nothing mechanical stands behind it in this repository. Promoting",
        "a row out of ASSERTED requires a real Lean theorem or a real test named in `evidence`, and",
        "`code/tests/unit/test_claim_ledger.py` enforces that pairing.",
        "",
        "## Distribution",
        "",
        "| Type | Count | Meaning |",
        "| --- | --- | --- |",
    ]
    for t, n in dist.most_common():
        out.append(f"| {t} | {n} | {TYPE_MEANING.get(t, '')} |")
    out += [
        f"| **Total** | **{len(claims)}** | |",
        "",
        f"**{dist['ASSERTED']} ASSERTED + {dist['UNTYPED']} UNTYPED = {unsupported} rows carrying "
        "no evidence and no settled type.**",
        "That is the working surface of this application.",
        "",
    ]
    if dropped:
        out += [
            f"{len(dropped)} further table rows were dropped as non-claim prose "
            "(`Action | Detail`, `Consumes | Role`); see `table_kind` in "
            "`code/consolidate_sources.py`.",
            "",
        ]

    out += [
        "## Claims with real evidence",
        "",
        "Carried in from `coda_atlas/F001_quantum/S000_finite_quantum_mechanics/` and application foundations,",
        "which -- unlike the F004 packages -- have Lean with no `sorry` and no `True` stubs, and tests that assert",
        "something.",
        "",
        "| ID | Claim | Type | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    for ac in app_claims:
        out.append(f"| {ac['id']} | {_esc(ac['statement'])} | {ac['type']} | {_esc(ac['evidence'])} |")
    out.append("")

    out += [
        "## Upgrade paths the source authors recorded",
        "",
        "From the `What would upgrade it` tables: the cheapest available map of what is missing,",
        "written by whoever last understood each paper.",
        "",
        "| Source | Claim | What would upgrade it | Difficulty | Lean/numerical? |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in upgrades:
        out.append(
            f"| {r['source'][:3]} | {_esc(r.get('id'), 40)} | "
            f"{_esc(r.get('what would upgrade it'), 200)} | {_esc(r.get('difficulty'), 40)} | "
            f"{_esc(r.get('lean/numerical?'), 60)} |"
        )
    out.append("")

    out += ["## Claims by source", ""]
    for src in sorted(by_source):
        out += [
            f"### SRC-{src[:3]} -- {title_for(src)}",
            "",
            f"`coda_atlas/F004_papers/003_quantum_foundations/{src}`",
            "",
            "| ID | Claim | Type | Evidence | Source status |",
            "| --- | --- | --- | --- | --- |",
        ]
        for c in by_source[src]:
            out.append(
                f"| {_esc(c['id'])} | {_esc(c['statement'], 220)} | {c['type']} | "
                f"{_esc(c['evidence'])} | {_esc(c['source_status'], 120)} |"
            )
        out.append("")

    out += [
        "## Non-claims",
        "",
        "This ledger does **not** assert that finite quantum mechanics is achievable, nor that it",
        "is obstructed. It records what the source papers claimed and what evidence exists for",
        "each. The open bridges are in `claims/gap_register.yaml`.",
        "",
        "`AuthorityEffect: None.`",
    ]
    return re.sub(r" {2,}(?=\|)", " ", "\n".join(out)) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Rebuild the consolidated ledger and inventory.")
    ap.add_argument("--check", action="store_true", help="fail if the generated files would change")
    args = ap.parse_args(argv)

    global AUDIT
    AUDIT = audit_map.parse(QF)
    inventory = build_inventory()
    claims, upgrades, dropped = build_claims()
    app_claims = load_application_claims()
    ledger = {
        "schema_version": "1.0.0",
        "app": "apps/finite_qm",
        "authority_effect": "None",
        "generated": "2026-09-04",
        "evidence_note": (
            "Claim types are derived from current source status, verified test-map loci, "
            "receipted Lean sources, and the imported adversarial audit. A mapped test supports "
            "only a finite fixture; unreceipted Lean remains source rather than a replayed proof."
        ),
        "claims": claims,
        "application_claims": app_claims,
    }

    targets = {
        APP_ROOT / "claims/source_inventory.yaml": yaml.safe_dump(
            inventory, sort_keys=False, allow_unicode=True, width=100
        ),
        APP_ROOT / "claims/claim_ledger.yaml": yaml.safe_dump(
            ledger, sort_keys=False, allow_unicode=True, width=110
        ),
        APP_ROOT / "finite_quantum_mechanics_claim_ledger.md": emit_markdown(
            claims, upgrades, dropped, inventory, app_claims
        ),
    }

    if args.check:
        stale = [
            p for p, text in targets.items()
            if not p.is_file() or p.read_text(encoding="utf-8") != text
        ]
        for p in stale:
            print(f"STALE: {p.relative_to(APP_ROOT)}", file=sys.stderr)
            if not p.is_file():
                print("  file is absent entirely", file=sys.stderr)
                continue
            on_disk = p.read_text(encoding="utf-8").splitlines()
            regenerated = targets[p].splitlines()
            print(
                f"  on disk {len(on_disk)} lines, regenerated {len(regenerated)} lines",
                file=sys.stderr,
            )
            for line in itertools.islice(
                difflib.unified_diff(
                    on_disk, regenerated, "on-disk", "regenerated", lineterm="", n=1
                ),
                40,
            ):
                print(f"  {line}", file=sys.stderr)
        return 1 if stale else 0

    APP_ROOT.joinpath("claims").mkdir(exist_ok=True)
    for p, text in targets.items():
        p.write_text(text, encoding="utf-8", newline="")

    dist = Counter(c["type"] for c in claims)
    print(f"audit rows: {sum(len(v) for v in AUDIT.values())} across {len(AUDIT)} papers")
    print(f"sources   : {len(inventory['sources'])}")
    print(f"claims    : {len(claims)}   (dropped {len(dropped)} non-claim rows)")
    print(f"upgrades  : {len(upgrades)}")
    for t, n in dist.most_common():
        print(f"  {t:<14} {n:>4}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

__all__ = ['APPLICATION_CLAIMS', 'APP_ROOT', 'AUDIT', 'CLAIM_COLS', 'EVIDENCED_CLAIMS', 'ID_COLS', 'PUBLISHED', 'QF', 'REDIRECT_STUBS', 'REPO_ROOT', 'SOURCE_KEYS', 'STATUS_COLS', 'TAUTOLOGY', 'TITLES', 'TRIVIAL_STUB', 'TYPE_MEANING', 'build_claims', 'build_inventory', 'emit_markdown', 'first', 'lean_files_for', 'load_application_claims', 'load_claim_code_map', 'main', 'paper_of', 'parse_tables', 'receipted_lean_files', 'retype', 'source_dirs', 'strip_lean_comments', 'table_kind', 'title_for']
